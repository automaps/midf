from typing import Any, Optional

from .base import IMDFFeature

__all__ = ["IMDFKiosk"]

class IMDFKiosk(IMDFFeature):
  geometry: Any  # Polygonal
  anchorId: Optional[str] = None
  levelId: Optional[str] = None
