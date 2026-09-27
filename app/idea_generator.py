"""Core idea generation for niche research and original content angles."""
from __future__ import annotations

import json
import random
from datetime import datetime
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
IDEAS_DIR = DATA_DIR / "ideas"


class ContentIdeaGenerator:
    """Generate original content ideas without copying existing videos."""

    def __init__(self) -> None:
        self.ideas_dir = IDEAS_DIR
        self.ideas_dir.mkdir(parents=True, exist_ok=True)

    def fetch_trending_topics(self, niche: str = "technology") -> list[dict]:
        """Collect public signals for a niche and return idea candidates."""
        candidates: list[dict] = []

        query = niche.strip().replace(" ", "+")
        try:
            response = requests.get(
                f"https://www.google.com/search?q={query}+trending",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10,
            )
            response.raise_for_status()
            if response.text:
                candidates.append({
                    "source": "public_search",
                    "niche": niche,
                    "title": f"Top trends in {niche} this month",
                    "angle": f"What is changing in {niche} right now?",
                })
        except Exception:
            pass

        try:
            response = requests.get(
                f"https://www.reddit.com/r/{niche}/hot.json?limit=10",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10,
            )
            response.raise_for_status()
            payload = response.json()
            for child in payload.get("data", {}).get("children", [])[:5]:
                title = child.get("data", {}).get("title")
                if title:
                    candidates.append({
                        "source": "reddit",
                        "niche": niche,
                        "title": title,
                        "angle": f"The real story behind {title}",
                    })
        except Exception:
            pass

        if not candidates:
            candidates = [
                {"source": "fallback", "niche": niche, "title": f"{niche} trends explained", "angle": f"Simple guide to {niche}"},
                {"source": "fallback", "niche": niche, "title": f"Common mistakes in {niche}", "angle": f"What most people get wrong about {niche}"},
                {"source": "fallback", "niche": niche, "title": f"Beginner checklist for {niche}", "angle": f"How to get started with {niche}"},
            ]

        return candidates

    def generate_original_idea(self, base_topic: str, niche: str) -> dict:
        """Turn a general topic into an original hook and angle."""
        angles = [
            f"Why {base_topic} is changing faster than most people expect",
            f"The hidden truth about {base_topic}",
            f"What nobody tells you about {base_topic}",
            f"3 mistakes people make with {base_topic}",
            f"How to use {base_topic} without wasting time",
            f"The easiest way to understand {base_topic}",
            f"What {base_topic} looks like in real life",
            f"A beginner-friendly breakdown of {base_topic}",
        ]

        angle = random.choice(angles)
        idea = {
            "base_topic": base_topic,
            "niche": niche,
            "angle": angle,
            "hook": angle,
            "created_at": datetime.now().isoformat(),
        }
        return idea

    def save_idea(self, idea: dict) -> Path:
        safe_name = "_".join(filter(None, [idea.get("niche", "idea"), idea.get("base_topic", "")]))
        safe_name = "".join(ch for ch in safe_name if ch.isalnum() or ch in "-_ ")
        safe_name = safe_name.replace(" ", "_")[:50].strip("_") or "idea"
        path = self.ideas_dir / f"{safe_name}.json"
        path.write_text(json.dumps(idea, indent=2, ensure_ascii=False), encoding="utf-8")
        return path


if __name__ == "__main__":
    generator = ContentIdeaGenerator()
    for idea in generator.fetch_trending_topics("technology")[:3]:
        print(idea)
