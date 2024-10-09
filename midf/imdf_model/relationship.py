from typing import Any, Optional

from .other import IMDFFeature
from ..enums import RelationshipCategory

__all__ = ["IMDFRelationship"]


class IMDFRelationship(IMDFFeature):
    category: RelationshipCategory
    direction: str = ""
    origin: Any = None
    intermediary: Any = None
    destination: Any = None
    hours: Any = None
    geometry: Optional[Any] = None  # shapely.geometry.base.BaseGeometry
