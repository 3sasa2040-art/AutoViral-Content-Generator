"""TikTok upload automation with saved browser profiles."""
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PROFILE_DIR = ROOT / "data" / "browser_profiles" / "tiktok"


class TikTokUploader:
    """Class for controlled browser-based upload operations on TikTok."""

    def __init__(self, profile_dir: str | None = None) -> None:
        self.profile_dir = Path(profile_dir) if profile_dir else PROFILE_DIR
        self.profile_dir.mkdir(parents=True, exist_ok=True)

    def upload_video(self, video_path: str, caption: str, hashtags: list[str], scheduled_time: datetime | None = None) -> bool:
        """Upload a ready video to TikTok."""
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch_persistent_context(str(self.profile_dir), headless=False)
                page = browser.new_page()
                page.goto("https://www.tiktok.com/upload", wait_until="domcontentloaded")
                page.wait_for_timeout(5000)
                page.set_input_files("input[type='file']", video_path)
                page.wait_for_timeout(6000)
                text_box = page.locator("[contenteditable='true'], [aria-label*='caption']").first
                if text_box.count() > 0:
                    text_box.fill(caption + " " + " ".join(hashtags))
                page.click("button:has-text('Post')", timeout=15000)
                print("TikTok upload launched successfully")
                browser.close()
                return True
        except Exception as exc:
            print(f"TikTok upload failed: {exc}")
            return False


def login() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch_persistent_context(str(PROFILE_DIR), headless=False)
        page = browser.new_page()
        page.goto("https://www.tiktok.com/upload", wait_until="domcontentloaded")
        print("Log in manually. Close the browser afterwards.")
        page.wait_for_timeout(180000)
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["login"])
    args = parser.parse_args()
    if args.command == "login":
        login()
