"""Run against Compose to verify an acknowledged receipt survives API restart."""
import subprocess
import time
import urllib.error
import uuid

from integration import call


def main():
    key = str(uuid.uuid4())
    body = {"student_id": key, "exam_id": "restart", "idempotency_key": key,
            "sequence": 1, "answers": {"q1": "B"}}
    status, row = call("/submissions", "demo-key-a", body)
    assert status == 202
    receipt_id = row["receipt_id"]
    subprocess.run(["docker", "compose", "restart", "api"], check=True)
    for attempt in range(20):
        try:
            status, retrieved = call("/submissions/" + receipt_id, "demo-key-a")
            break
        except (urllib.error.URLError, OSError):
            if attempt == 19:
                raise
            time.sleep(0.5)
    assert status == 200 and retrieved["id"] == receipt_id
    assert call("/submissions/" + receipt_id, "demo-key-b")[0] == 404
    print("PASS: acknowledged receipt survived API restart and remained isolated")


if __name__ == "__main__":
    main()
