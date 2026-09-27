"""Local free TTS and audio stitching for original video drafts."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = ROOT / "output" / "audio"


class VoiceoverGenerator:
    """Generate a local voiceover and attach it to a video."""

    def __init__(self) -> None:
        self.audio_dir = AUDIO_DIR
        self.audio_dir.mkdir(parents=True, exist_ok=True)

    def generate_voiceover(self, text: str, output_path: str) -> Optional[str]:
        """Produce a voiceover using installed local TTS tools when available."""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty("rate", 165)
            engine.save_to_file(text, output_path)
            engine.runAndWait()
            return output_path
        except Exception:
            pass

        try:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run([
                "espeak",
                "-w",
                str(path),
                text,
            ], check=True, capture_output=True)
            return output_path
        except Exception:
            return None

    def merge_audio_to_video(self, video_path: str, audio_path: str, output_path: str) -> Optional[str]:
        """Merge audio with a video file using ffmpeg."""
        try:
            subprocess.run([
                "ffmpeg",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-y", output_path,
            ], check=True, capture_output=True)
            return output_path
        except Exception:
            return None


if __name__ == "__main__":
    voice = VoiceoverGenerator()
    result = voice.generate_voiceover("This is a test voiceover for a generated video.", str(ROOT / "output" / "audio" / "test.mp3"))
    print(result)
