from typing import Any, Optional

from .other import IMDFFeature

__all__ = ["IMDFRelationship"]


class IMDFRelationship(IMDFFeature):
    category: str = ""
    direction: str = ""
    origin: Any = None
    intermediary: Any = None
    destination: Any = None
    hours: Any = None
    geometry: Optional[Any] = None  # shapely.geometry.base.BaseGeometry
