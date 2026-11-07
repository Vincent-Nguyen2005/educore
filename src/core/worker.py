import os
import time

import psycopg


def run_once(dsn):
    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id FROM receipts WHERE status='pending'
                ORDER BY created_at LIMIT 100 FOR UPDATE SKIP LOCKED
            """)
            ids = [row[0] for row in cur.fetchall()]
            for receipt_id in ids:
                cur.execute("UPDATE receipts SET status='processed' WHERE id=%s", (receipt_id,))
    return len(ids)


if __name__ == "__main__":
    while True:
        for name in ("TENANT_A_DSN", "TENANT_B_DSN"):
            try:
                run_once(os.environ[name])
            except psycopg.Error as exc:
                print(f"worker {name}: {exc}", flush=True)
        time.sleep(0.2)
