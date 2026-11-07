"""Run after docker compose up -d: python tests/integration.py."""
import json
import urllib.error
import urllib.request
import uuid

BASE = "http://localhost:8080"


def call(path, key, body=None, method=None):
    data = None if body is None else json.dumps(body).encode()
    request = urllib.request.Request(BASE + path, data=data, method=method,
        headers={"X-Demo-Key": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as exc:
        return exc.code, json.load(exc)


def main():
    a = "demo-key-a"
    b = "demo-key-b"
    scores = {"attendance": 100, "midterm": 80, "final": 70}
    assert call("/grade", a, {"scores": scores})[1]["grade"] == "76.00"
    assert call("/grade", b, {"scores": scores})[1]["grade"] == "78.00"
    unique = str(uuid.uuid4())
    payload = {"student_id": unique, "exam_id": "final", "sequence": 1,
               "idempotency_key": unique, "answers": {"q1": "A"}}
    status, receipt = call("/submissions", a, payload)
    assert status == 202
    assert call("/submissions", a, payload)[1]["receipt_id"] == receipt["receipt_id"]
    assert call("/submissions/" + receipt["receipt_id"], b)[0] == 404
    assert call("/submissions/" + receipt["receipt_id"], a)[0] == 200
    assert call("/formula", "invalid")[0] == 401
    save = {"student_id": unique, "exam_id": "final", "sequence": 2, "answers": {"q1": "B"}}
    assert call("/autosaves", a, save)[0] == 202
    save["sequence"] = 1
    save["answers"] = {"q1": "A"}
    assert call("/autosaves", a, save)[1]["sequence"] == 2
    assert call(f"/autosaves/{unique}/final", a)[1]["answers"] == {"q1": "B"}
    assert call(f"/autosaves/{unique}/final", b)[0] == 404
    assert call("/plugins/qr/enable", a, {"enabled": False})[0] == 200
    assert call("/plugins/qr/enable", b, {"enabled": False})[0] == 200
    assert call("/attendance/qr", a, {"student_id": unique, "course_id": "c", "code": "QR-a-1"})[0] == 404
    assert call("/plugins/qr/enable", a, {"enabled": True})[0] == 200
    assert call("/attendance/qr", a, {"student_id": unique, "course_id": "c", "code": "QR-a-1"})[0] == 200
    assert call("/attendance/qr", b, {"student_id": unique, "course_id": "c", "code": "QR-b-1"})[0] == 404
    print("PASS: tenant grading, cross-tenant isolation, idempotency, autosave ordering, runtime QR")


if __name__ == "__main__":
    main()
