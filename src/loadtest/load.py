"""Async arrival-rate exam load test. Requires aiohttp (`pip install aiohttp`)."""
import argparse
import asyncio
import json
import math
import time
import uuid

import aiohttp


def percentile(values, fraction):
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, math.ceil(len(ordered) * fraction) - 1)]


async def one(index, start, args, session):
    target = start + args.seconds * index / args.users
    await asyncio.sleep(max(0, target - time.perf_counter()))
    begun = time.perf_counter()
    started_ms = (begun - start) * 1000
    body = {"student_id": f"load-{uuid.uuid4()}", "exam_id": "final-load",
            "idempotency_key": str(uuid.uuid4()), "sequence": 1, "answers": {"q1": "A"}}
    try:
        async with session.post(args.base + "/submissions", json=body) as response:
            payload = await response.json()
            return {"index": index, "started_ms": started_ms,
                    "ms": (time.perf_counter() - begun) * 1000, "status": response.status,
                    "receipt_id": payload.get("receipt_id")}
    except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
        return {"index": index, "started_ms": started_ms,
                "ms": (time.perf_counter() - begun) * 1000, "status": 0,
                "error": str(exc)}


async def run(args):
    start = time.perf_counter() + 1
    timeout = aiohttp.ClientTimeout(total=120)
    connector = aiohttp.TCPConnector(limit=args.connections)
    async with aiohttp.ClientSession(timeout=timeout, connector=connector,
            headers={"X-Demo-Key": "demo-key-a"}) as session:
        rows = await asyncio.gather(*(one(i, start, args, session) for i in range(args.users)))
    latencies = [r["ms"] for r in rows]
    success = sum(r["status"] == 202 for r in rows)
    return {"users": args.users, "seconds": args.seconds,
            "connections": args.connections, "success": success,
            "errors": args.users - success,
            "started_within_window": sum(0 <= r["started_ms"] < args.seconds * 1000 for r in rows),
            "last_start_ms": max(r["started_ms"] for r in rows),
            "p50_ms": percentile(latencies, .5), "p95_ms": percentile(latencies, .95),
            "p99_ms": percentile(latencies, .99), "rows": rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--users", type=int, default=8000)
    parser.add_argument("--seconds", type=float, default=60)
    parser.add_argument("--connections", type=int, default=2000)
    parser.add_argument("--base", default="http://localhost:8080")
    parser.add_argument("--output", default="load-results.json")
    args = parser.parse_args()
    if args.users < 1 or args.seconds <= 0 or args.connections < 1:
        parser.error("users, seconds and connections must be positive")
    report = asyncio.run(run(args))
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(json.dumps({k: v for k, v in report.items() if k != "rows"}, indent=2))
