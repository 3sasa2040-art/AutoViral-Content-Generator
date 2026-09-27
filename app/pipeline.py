"""Safe local pipeline: discover public ideas and create reviewable drafts."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUTPUT = ROOT / "output" / "drafts"


def discover(niche: str, limit: int) -> list[dict]:
    # Uses public search pages only; it does not bypass login or access controls.
    url = "https://www.youtube.com/results?search_query=" + quote_plus(niche)
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    results: list[dict] = []
    for anchor in soup.select("a#video-title"):
        title = anchor.get("title") or anchor.get_text(" ", strip=True)
        href = anchor.get("href", "")
        if title and href.startswith("/watch?v="):
            results.append({"title": title, "url": "https://www.youtube.com" + href, "niche": niche, "source": "youtube"})
        if len(results) >= limit:
            break
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "trends.json").write_text(json.dumps({"updated_at": datetime.now(timezone.utc).isoformat(), "items": results}, indent=2), encoding="utf-8")
    return results


def make_drafts(niche: str, limit: int) -> None:
    source = DATA / "trends.json"
    items = json.loads(source.read_text(encoding="utf-8")).get("items", []) if source.exists() else discover(niche, limit)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for item in items[:limit]:
        safe = re.sub(r"[^a-zA-Z0-9_-]+", "-", item["title"]).strip("-").lower()[:70] or "draft"
        folder = OUTPUT / safe
        folder.mkdir(exist_ok=True)
        plan = {"title": item["title"], "source_url": item["url"], "niche": niche, "status": "review", "caption": f"{item['title']} #shorts #{niche.replace(' ', '')}"}
        (folder / "content.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
        (folder / "README.txt").write_text("Maak hier alleen originele/licentie-toegestane media klaar. Review vóór publicatie.\n", encoding="utf-8")
        print(f"Draft aangemaakt: {folder}")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("discover", "drafts"):
        p = sub.add_parser(name)
        p.add_argument("--niche", default="tech")
        p.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()
    if args.command == "discover":
        for item in discover(args.niche, args.limit):
            print(item["title"], item["url"])
    else:
        make_drafts(args.niche, args.limit)


if __name__ == "__main__":
    main()
