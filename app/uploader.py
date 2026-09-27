"""Persistent browser profiles for manual first-time login and authorized uploads."""
from __future__ import annotations

import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PROFILES = ROOT / "data" / "browser_profiles"


def login(platform: str) -> None:
    urls = {"tiktok": "https://www.tiktok.com/upload", "youtube": "https://studio.youtube.com/"}
    if platform not in urls:
        raise ValueError("Ondersteund: tiktok, youtube")
    profile = PROFILES / platform
    profile.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(str(profile), headless=False)
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(urls[platform], wait_until="domcontentloaded")
        print("Log handmatig in in het geopende venster. Sluit daarna de browser om de sessie op te slaan.")
        try:
            page.wait_for_timeout(180000)
        finally:
            context.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["login"])
    parser.add_argument("--platform", required=True)
    args = parser.parse_args()
    login(args.platform)
