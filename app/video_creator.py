"""Original video rendering and thumbnail generation for short-form content."""
from __future__ import annotations

import subprocess
import textwrap
from pathlib import Path
from typing import Optional

from moviepy.editor import CompositeVideoClip, TextClip, VideoFileClip, concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output" / "videos"
THUMBNAIL_DIR = ROOT / "output" / "thumbnails"


class VideoCreator:
    """Create original short-form videos from source clips or generated assets."""

    def __init__(self) -> None:
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.thumbnail_dir = THUMBNAIL_DIR
        self.thumbnail_dir.mkdir(parents=True, exist_ok=True)

    def create_video_from_clips(self, clip_paths: list[str], title: str, output_path: str) -> Optional[str]:
        """Combine multiple source clips into a single vertical video."""
        try:
            clip_files = [Path(p) for p in clip_paths if Path(p).exists()]
            if not clip_files:
                return None
            clips = [VideoFileClip(str(p)).resize((1080, 1920)) for p in clip_files[:6]]
            if not clips:
                return None
            final = concatenate_videoclips(clips, method="compose")
            title_clip = TextClip(
                title,
                fontsize=52,
                color="white",
                font="Arial-Bold",
                method="caption",
                size=(900, None),
            ).set_position(("center", "top")).set_duration(final.duration)
            final = CompositeVideoClip([final, title_clip])
            final.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac", verbose=False, logger=None)
            return output_path
        except Exception:
            return None

    def create_thumbnail(self, title: str, output_path: str) -> Optional[str]:
        """Create a usable thumbnail for a short form video."""
        try:
            width, height = 1280, 720
            image = Image.new("RGB", (width, height), color=(18, 18, 24))
            draw = ImageDraw.Draw(image)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
            except Exception:
                font = ImageFont.load_default()

            wrapped = textwrap.wrap(title, width=18)
            y = 240
            for line in wrapped[:3]:
                draw.text((60, y), line, fill=(255, 245, 150), font=font)
                y += 90

            image.save(output_path)
            return output_path
        except Exception:
            return None

    def create_subtitle_file(self, subtitle_lines: list[dict], output_path: str) -> Optional[str]:
        """Create an SRT file from subtitle lines."""
        try:
            content = []
            for idx, line in enumerate(subtitle_lines, 1):
                content.append(str(idx))
                content.append(f"{line['start']} --> {line['end']}")
                content.append(line['text'])
                content.append("")
            Path(output_path).write_text("\n".join(content), encoding="utf-8")
            return output_path
        except Exception:
            return None


if __name__ == "__main__":
    creator = VideoCreator()
    output = creator.create_thumbnail("AI content strategy that actually works", str(ROOT / "output" / "demo_thumbnail.jpg"))
    print(output)
