from typing import Any

from .other import IMDFFeature

__all__ = ["IMDFAnchor"]


class IMDFAnchor(IMDFFeature):
    geometry: Any  # shapely.Point
    address_id: Any = None
    unit_id: str = ""
