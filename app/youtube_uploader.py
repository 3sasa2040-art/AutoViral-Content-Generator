"""YouTube upload automation with saved browser profiles."""
from __future__ import annotations

import argparse
from pathlib import Path
from datetime import datetime

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PROFILE_DIR = ROOT / "data" / "browser_profiles" / "youtube"


class YouTubeUploader:
    """Class for controlled browser-based upload operations on YouTube."""

    def __init__(self, profile_dir: str | None = None) -> None:
        self.profile_dir = Path(profile_dir) if profile_dir else PROFILE_DIR
        self.profile_dir.mkdir(parents=True, exist_ok=True)

    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: list[str],
        scheduled_time: datetime | None = None,
        visibility: str = "private",
    ) -> bool:
        """Upload a ready video to YouTube."""
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch_persistent_context(str(self.profile_dir), headless=False)
                page = browser.new_page()
                page.goto("https://studio.youtube.com/", wait_until="domcontentloaded")
                page.wait_for_timeout(5000)
                page.click("button:has-text('Create')", timeout=5000)
                page.click("a:has-text('Upload video')", timeout=5000)
                file_input = page.locator("input[type='file']").first
                file_input.set_input_files(video_path)
                page.wait_for_timeout(6000)
                title_locator = page.locator("[aria-label='Title']").first
                if title_locator.count() > 0:
                    title_locator.fill(title)
                description_locator = page.locator("[aria-label='Description']").first
                if description_locator.count() > 0:
                    description_locator.fill(description)
                tags_text = ", ".join(tags)
                tag_locator = page.locator("[aria-label='Tags']").first
                if tag_locator.count() > 0:
                    tag_locator.fill(tags_text)
                page.click("button:has-text('Next')", timeout=5000)
                page.click("button:has-text('Next')", timeout=5000)
                page.click("button:has-text('Next')", timeout=5000)
                page.click(f"button:has-text('{visibility.title()}')", timeout=3000)
                page.click("button:has-text('Publish')", timeout=10000)
                print("Upload launched successfully")
                browser.close()
                return True
        except Exception as exc:
            print(f"YouTube upload failed: {exc}")
            return False


def login() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch_persistent_context(str(PROFILE_DIR), headless=False)
        page = browser.new_page()
        page.goto("https://studio.youtube.com/", wait_until="domcontentloaded")
        print("Log in manually. Close the browser afterwards.")
        page.wait_for_timeout(180000)
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["login"])
    args = parser.parse_args()
    if args.command == "login":
        login()
