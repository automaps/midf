from typing import Any, Mapping, Optional

from .other import IMDFDoor, IMDFFeature

__all__ = ["IMDFOpening"]


class IMDFOpening(IMDFFeature):
    geometry: Any  # shapely.LineString
    category: str = ""
    accessibility: Any = None
    access_control: Any = None
    door: Optional[IMDFDoor] = None
    name: Optional[Mapping[str, str]] = None
    alt_name: Optional[Mapping[str, str]] = None
    display_point: Optional[Any] = None  # shapely.Point
    level_id: str
