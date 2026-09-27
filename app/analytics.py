"""Performance and optimization tracking for original content."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"


class ContentAnalytics:
    """Track local metrics and learn which content performs best."""

    def __init__(self) -> None:
        self.data_dir = DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load_data(self) -> dict:
        path = self.data_dir / "analytics.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return {"videos": []}

    def save_data(self, data: dict) -> None:
        path = self.data_dir / "analytics.json"
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def log_video(self, title: str, platform: str, niche: str, status: str = "queued") -> None:
        data = self.load_data()
        item = {
            "title": title,
            "platform": platform,
            "niche": niche,
            "status": status,
            "views": 0,
            "likes": 0,
            "comments": 0,
            "shares": 0,
        }
        data["videos"].append(item)
        self.save_data(data)

    def get_top_by_niche(self, niche: str) -> list[dict]:
        data = self.load_data()
        items = [item for item in data.get("videos", []) if item.get("niche") == niche]
        return sorted(items, key=lambda x: x.get("views", 0) + x.get("likes", 0) * 2 + x.get("shares", 0) * 3, reverse=True)


if __name__ == "__main__":
    analytics = ContentAnalytics()
    analytics.log_video("Sample video", "youtube", "technology", "draft")
    print(analytics.get_top_by_niche("technology"))
