"""Hybrid pipeline: automatic generation + human review + scheduled publish."""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from app.analytics import ContentAnalytics
from app.idea_generator import ContentIdeaGenerator
from app.script_generator import ScriptGenerator
from app.video_creator import VideoCreator
from app.voiceover_generator import VoiceoverGenerator
from app.scheduler import ContentScheduler

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output"


class HybridPipeline:
    """Semi-automated production pipeline with review and optimized scheduling."""

    def __init__(self) -> None:
        self.idea_gen = ContentIdeaGenerator()
        self.script_gen = ScriptGenerator()
        self.video_creator = VideoCreator()
        self.voiceover = VoiceoverGenerator()
        self.scheduler = ContentScheduler()
        self.analytics = ContentAnalytics()

    def generate_batch(self, niche: str, count: int = 3) -> list[dict]:
        items: list[dict] = []
        topics = self.idea_gen.fetch_trending_topics(niche)[:count]
        for topic in topics:
            base_topic = topic.get("title") or topic.get("angle") or niche
            idea = self.idea_gen.generate_original_idea(base_topic, niche)
            script = self.script_gen.generate_script(base_topic, niche)
            youtube_title = self.script_gen.generate_youtube_title(script)
            youtube_desc = self.script_gen.generate_youtube_description(script)
            tiktok_caption = self.script_gen.generate_tiktok_caption(script)
            thumbnail_path = self.video_creator.create_thumbnail(youtube_title, str(OUTPUT_DIR / "thumbnails" / f"{base_topic[:20]}_thumb.jpg"))
            voiceover_path = self.voiceover.generate_voiceover(script["solution"], str(OUTPUT_DIR / "audio" / f"{base_topic[:20]}_voice.mp3"))
            item = {
                "idea": idea,
                "script": script,
                "youtube_title": youtube_title,
                "youtube_description": youtube_desc,
                "tiktok_caption": tiktok_caption,
                "thumbnail_path": thumbnail_path,
                "voiceover_path": voiceover_path,
                "status": "draft",
                "created_at": datetime.now().isoformat(),
            }
            items.append(item)
            self.scheduler.add_pending_video(item)
            self.analytics.log_video(youtube_title, "youtube", niche, "draft")
        return items

    def list_pending(self) -> list[dict]:
        queue = self.scheduler.load_queue()
        return queue.get("pending", [])

    def approve(self, index: int) -> None:
        self.scheduler.approve(index)

    def reject(self, index: int) -> None:
        self.scheduler.reject(index)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--niche", default="technology")
    parser.add_argument("--count", type=int, default=3)
    args = parser.parse_args()
    pipeline = HybridPipeline()
    items = pipeline.generate_batch(args.niche, args.count)
    print(f"Generated {len(items)} draft items for review.")
    print(pipeline.list_pending())
