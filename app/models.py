from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional


@dataclass
class Account:
    platform: str
    username: str
    password: str
    email: Optional[str] = None
    enabled: bool = True
    schedule: Optional[str] = None


@dataclass
class ContentPlan:
    platform: str
    niche: str
    title: str
    description: str
    hashtags: List[str]
    source_url: Optional[str] = None
    output_path: Optional[str] = None


@dataclass
class TrendSource:
    name: str
    url: str
    active: bool = True
