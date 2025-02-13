from typing import Any, Mapping, Optional

from .base import IMDFFeature

__all__ = ["IMDFKiosk"]


class IMDFKiosk(IMDFFeature):
    geometry: Any  # Polygonal

    alt_name: Optional[Mapping[str, str]] = None
    name: Optional[Mapping[str, str]] = None
    anchor_id: Optional[str] = None
    level_id: Optional[str] = None
    display_point: Optional[Any] = None
