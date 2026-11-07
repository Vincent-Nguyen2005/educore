import os
import uuid
from contextlib import contextmanager

import psycopg
from flask import Flask, g, jsonify, request
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

from grading import grade

app = Flask(__name__)
_pools = {}


def tenant_config():
    return {
        "a": (os.environ["TENANT_A_KEY"], os.environ["TENANT_A_DSN"]),
        "b": (os.environ["TENANT_B_KEY"], os.environ["TENANT_B_DSN"]),
    }


@app.before_request
def authenticate():
    if request.path == "/health" or request.path.startswith("/static/"):
        return None
    # Demo credential. Production gateway must verify OIDC/SAML signature, issuer,
    # audience, expiry and host-to-tenant mapping before setting this context.
    key = request.headers.get("X-Demo-Key", "")
    matches = [(tenant, dsn) for tenant, (secret, dsn) in tenant_config().items() if key == secret]
    if len(matches) != 1:
        return jsonify(error="unauthorized"), 401
    g.tenant, g.dsn = matches[0]
    return None


@contextmanager
def db():
    # No caller can pass a DSN, tenant_id, schema name or DB role from request data.
    # Pools are per gunicorn process and tenant, bounded to protect PostgreSQL.
    pool = _pools.get(g.tenant)
    if pool is None:
        pool = ConnectionPool(g.dsn, min_size=1, max_size=8, kwargs={"row_factory": dict_row})
        _pools[g.tenant] = pool
    with pool.connection() as conn:
        yield conn


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/formula")
def formula():
    with db() as conn:
        row = conn.execute("SELECT version, weights FROM formulas ORDER BY version DESC LIMIT 1").fetchone()
    return jsonify(tenant=g.tenant, **row)


@app.post("/grade")
def calculate_grade():
    body = request.get_json(silent=True) or {}
    with db() as conn:
        row = conn.execute("SELECT version, weights FROM formulas ORDER BY version DESC LIMIT 1").fetchone()
    try:
        value = grade(row["weights"], body["scores"])
    except (KeyError, ValueError, TypeError, ArithmeticError) as exc:
        return jsonify(error=str(exc)), 400
    return jsonify(tenant=g.tenant, formula_version=row["version"], grade=value)


@app.post("/submissions")
def submit():
    body = request.get_json(silent=True) or {}
    try:
        student = str(body["student_id"])
        exam = str(body["exam_id"])
        key = str(body["idempotency_key"])
        sequence = int(body["sequence"])
        answers = body["answers"]
        if not student or not exam or not key or sequence < 0 or not isinstance(answers, dict):
            raise ValueError("invalid submission")
        if len(student) > 100 or len(exam) > 100 or len(key) > 100:
            raise ValueError("field too long")
    except (KeyError, TypeError, ValueError) as exc:
        return jsonify(error=str(exc)), 400
    receipt_id = str(uuid.uuid4())
    with db() as conn:
        # INSERT and conflict read are in one tenant DB transaction. No HTTP ack
        # before context manager commits; on error Flask returns 5xx.
        row = conn.execute("""
          INSERT INTO receipts(id, student_id, exam_id, idempotency_key, sequence, answers)
          VALUES (%s, %s, %s, %s, %s, %s)
          ON CONFLICT (student_id, exam_id, idempotency_key)
          DO UPDATE SET idempotency_key = EXCLUDED.idempotency_key
          RETURNING id, status
        """, (receipt_id, student, exam, key, sequence, psycopg.types.json.Jsonb(answers))).fetchone()
    return jsonify(tenant=g.tenant, receipt_id=str(row["id"]), status=row["status"]), 202


@app.get("/submissions/<receipt_id>")
def receipt(receipt_id):
    try:
        uuid.UUID(receipt_id)
    except ValueError:
        return jsonify(error="invalid id"), 400
    with db() as conn:
        row = conn.execute("SELECT id, student_id, exam_id, sequence, status FROM receipts WHERE id = %s", (receipt_id,)).fetchone()
    if row is None:
        return jsonify(error="not found"), 404
    return jsonify(tenant=g.tenant, **row)


@app.post("/autosaves")
def autosave():
    body = request.get_json(silent=True) or {}
    try:
        student = str(body["student_id"])
        exam = str(body["exam_id"])
        sequence = int(body["sequence"])
        answers = body["answers"]
        if not student or not exam or sequence < 0 or not isinstance(answers, dict):
            raise ValueError("invalid autosave")
    except (KeyError, TypeError, ValueError) as exc:
        return jsonify(error=str(exc)), 400
    with db() as conn:
        row = conn.execute("""
          INSERT INTO autosaves(student_id, exam_id, sequence, answers)
          VALUES (%s,%s,%s,%s)
          ON CONFLICT (student_id, exam_id) DO UPDATE SET
            sequence=EXCLUDED.sequence, answers=EXCLUDED.answers, updated_at=now()
          WHERE autosaves.sequence < EXCLUDED.sequence
          RETURNING sequence
        """, (student, exam, sequence, psycopg.types.json.Jsonb(answers))).fetchone()
        if row is None:
            row = conn.execute("SELECT sequence FROM autosaves WHERE student_id=%s AND exam_id=%s", (student, exam)).fetchone()
    return jsonify(tenant=g.tenant, sequence=row["sequence"]), 202


@app.get("/autosaves/<student>/<exam>")
def get_autosave(student, exam):
    with db() as conn:
        row = conn.execute("SELECT sequence, answers FROM autosaves WHERE student_id=%s AND exam_id=%s", (student, exam)).fetchone()
    if row is None:
        return jsonify(error="not found"), 404
    return jsonify(tenant=g.tenant, **row)


@app.post("/plugins/qr/enable")
def enable_qr():
    body = request.get_json(silent=True) or {}
    if type(body.get("enabled")) is not bool:
        return jsonify(error="enabled must be boolean"), 400
    with db() as conn:
        conn.execute("UPDATE plugin_registry SET enabled=%s WHERE name='qr'", (body["enabled"],))
    return jsonify(tenant=g.tenant, enabled=body["enabled"])


@app.post("/attendance/qr")
def attendance():
    import urllib.error
    import urllib.request
    import json
    body = request.get_json(silent=True) or {}
    if not all(isinstance(body.get(k), str) and body[k] for k in ("student_id", "course_id", "code")):
        return jsonify(error="missing attendance fields"), 400
    with db() as conn:
        enabled = conn.execute("SELECT enabled FROM plugin_registry WHERE name='qr'").fetchone()["enabled"]
    if not enabled:
        return jsonify(error="plugin disabled"), 404
    payload = json.dumps({"tenant": g.tenant, "code": body["code"]}).encode()
    req = urllib.request.Request(os.environ["QR_URL"] + "/validate", data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=0.5) as response:
            result = json.load(response)
    except (TimeoutError, OSError, urllib.error.URLError):
        return jsonify(error="plugin unavailable"), 503
    if not result.get("valid"):
        return jsonify(error="invalid code"), 400
    with db() as conn:
        conn.execute("""INSERT INTO attendance(student_id, course_id, code) VALUES (%s,%s,%s)
                     ON CONFLICT DO NOTHING""", (body["student_id"], body["course_id"], body["code"]))
    return jsonify(tenant=g.tenant, recorded=True)
