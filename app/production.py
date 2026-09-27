"""Production workflow commands for the hybrid content system.

Default behavior is safe: generate drafts and stop at human review.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from app.analytics import ContentAnalytics
from app.full_pipeline import HybridPipeline
from app.scheduler import ContentScheduler

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"


def write_report(payload: dict) -> Path:
    REPORTS.mkdir(parents=True, exist_ok=True)
    path = REPORTS / f"run-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def generate(niche: str, count: int) -> None:
    pipeline = HybridPipeline()
    items = pipeline.generate_batch(niche, count)
    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "mode": "draft-only",
        "niche": niche,
        "count": len(items),
        "message": "Review drafts manually before approving or uploading.",
    }
    print(f"Generated {len(items)} drafts.")
    print(f"Report: {write_report(report)}")


def queue() -> None:
    scheduler = ContentScheduler()
    data = scheduler.load_queue()
    print(json.dumps({
        "pending": len(data.get("pending", [])),
        "approved": len(data.get("approved", [])),
        "rejected": len(data.get("rejected", [])),
    }, indent=2))


def report() -> None:
    analytics = ContentAnalytics()
    data = analytics.load_data()
    videos = data.get("videos", [])
    ranked = sorted(
        videos,
        key=lambda item: item.get("views", 0) + 2 * item.get("likes", 0) + 3 * item.get("shares", 0),
        reverse=True,
    )
    print(json.dumps({"videos": len(videos), "top": ranked[:10]}, indent=2, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser(description="Hybrid content production workflow")
    sub = parser.add_subparsers(dest="command", required=True)

    p_generate = sub.add_parser("generate", help="Create drafts; no uploads")
    p_generate.add_argument("--niche", default="technology")
    p_generate.add_argument("--count", type=int, default=3)

    sub.add_parser("queue", help="Show pending/approved/rejected counts")
    sub.add_parser("report", help="Show local performance report")

    args = parser.parse_args()
    if args.command == "generate":
        generate(args.niche, max(1, min(args.count, 10)))
    elif args.command == "queue":
        queue()
    elif args.command == "report":
        report()


if __name__ == "__main__":
    main()
