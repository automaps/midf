from typing import Any, List, Optional

import shapely

from .base import IMDFFeature
from ..enums import RelationshipCategory

__all__ = ["IMDFRelationship"]

from ..typing import Direction


class IMDFRelationship(IMDFFeature):
    category: RelationshipCategory
    direction: Direction
    origin: Optional[IMDFFeature] = None
    intermediary: Optional[List[IMDFFeature]] = None
    destination: Optional[IMDFFeature] = None
    hours: Any = None
    geometry: Optional[shapely.geometry.base.BaseGeometry] = None
