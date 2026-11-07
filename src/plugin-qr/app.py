from flask import Flask, jsonify, request

app = Flask(__name__)


@app.post("/validate")
def validate():
    body = request.get_json(silent=True) or {}
    # Demonstration plugin contract: code QR-<tenant>-<session>.
    tenant = body.get("tenant")
    code = body.get("code", "")
    valid = tenant in ("a", "b") and isinstance(code, str) and code.startswith(f"QR-{tenant}-") and len(code) > 5
    return jsonify(valid=valid)
