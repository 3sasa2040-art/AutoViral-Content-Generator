"""Scheduling and review queue for hybrid automation."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"


class ContentScheduler:
    """Manage review queues, scheduling and repeatable publishing."""

    def __init__(self) -> None:
        self.data_dir = DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load_queue(self) -> dict:
        path = self.data_dir / "queue.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return {"pending": [], "approved": [], "rejected": []}

    def save_queue(self, queue: dict) -> None:
        path = self.data_dir / "queue.json"
        path.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")

    def add_pending_video(self, content: dict) -> None:
        queue = self.load_queue()
        queue["pending"].append({"created_at": datetime.now().isoformat(), **content})
        self.save_queue(queue)

    def approve(self, idx: int) -> None:
        queue = self.load_queue()
        if idx < len(queue["pending"]):
            item = queue["pending"].pop(idx)
            queue["approved"].append(item)
            self.save_queue(queue)

    def reject(self, idx: int) -> None:
        queue = self.load_queue()
        if idx < len(queue["pending"]):
            item = queue["pending"].pop(idx)
            queue["rejected"].append(item)
            self.save_queue(queue)


if __name__ == "__main__":
    scheduler = ContentScheduler()
    print(scheduler.load_queue())
