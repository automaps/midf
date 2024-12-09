from typing import Any

import shapely

from .base import IMDFFeature

__all__ = ["IMDFAnchor"]


class IMDFAnchor(IMDFFeature):
    geometry: shapely.Point
    address_id: Any = None
    unit_id: str = ""
