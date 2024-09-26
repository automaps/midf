from dataclasses import dataclass
from typing import Optional

__all__ = ["IMDFDoor"]


@dataclass
class IMDFDoor:
    type: Optional[str] = None
    automatic: bool = False
    material: Optional[str] = None
