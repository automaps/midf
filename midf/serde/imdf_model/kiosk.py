from typing import Any, Optional

from .other import IMDFFeature

__all__ = ["IMDFKiosk"]


class IMDFKiosk(IMDFFeature):
    geometry: Any  # Polygonal
    anchorId: Optional[str] = None
    levelId: Optional[str] = None
