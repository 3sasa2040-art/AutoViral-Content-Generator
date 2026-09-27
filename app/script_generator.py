"""Original script and caption generation for short-form video creation."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
SCRIPTS_DIR = DATA_DIR / "scripts"


class ScriptGenerator:
    """Generate script variants for original short-form videos."""

    def __init__(self) -> None:
        self.scripts_dir = SCRIPTS_DIR
        self.scripts_dir.mkdir(parents=True, exist_ok=True)

    def generate_script(self, topic: str, niche: str = "general") -> dict:
        """Generate a complete original short-form script."""
        hook = f"Here is the real reason {topic} is so confusing for most people."
        problem = f"Most people think {topic} is harder than it really is."
        solution = f"The simple version is this: stop overthinking {topic} and focus on the essentials."
        takeaway = f"If you want to be better at {niche}, this is the biggest mindset shift to remember."

        script = {
            "topic": topic,
            "niche": niche,
            "hook": hook,
            "problem": problem,
            "solution": solution,
            "cta": "Follow for more practical insights like this.",
            "takeaway": takeaway,
            "duration_seconds": 45,
        }
        return script

    def generate_youtube_title(self, script: dict) -> str:
        """Generate a YouTube-optimized title."""
        return f"{script['hook']} | {script['niche'].title()}"

    def generate_youtube_description(self, script: dict) -> str:
        """Generate a strong video description."""
        return (
            f"{script['solution']}\n\n"
            f"Why it matters:\n{script['problem']}\n\n"
            f"Takeaway:\n{script['takeaway']}\n\n"
            f"Follow for more practical content about {script['niche']}."
        )

    def generate_tiktok_caption(self, script: dict) -> str:
        """Generate a TikTok-ready caption."""
        return (
            f"{script['hook']}\n\n"
            f"{script['takeaway']}\n\n"
            f"#{script['niche']} #shorts #learn #tips #viral #2026"
        )

    def save_script(self, topic: str, script: dict) -> Path:
        safe_name = "".join(ch for ch in topic if ch.isalnum() or ch in "-_")[:50] or "script"
        path = self.scripts_dir / f"{safe_name}.json"
        path.write_text(json.dumps(script, indent=2, ensure_ascii=False), encoding="utf-8")
        return path


if __name__ == "__main__":
    s = ScriptGenerator()
    script = s.generate_script("AI content strategy", "marketing")
    print(script)
