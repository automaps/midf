from datetime import datetime

from typing import List, Optional

__all__ = ["MIDFManifest"]

from dataclasses import dataclass


@dataclass
class MIDFManifest:
    version: str
    created: datetime
    language: str
    generated_by: Optional[str] = None
    extensions: Optional[List[str]] = None
