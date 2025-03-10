from typing import Any, List, Optional

import shapely

from .base import IMDFFeature, IMDFFeatureReference
from ..enums import IMDFRelationshipCategory

__all__ = ["IMDFRelationship"]

from .opening import IMDFDirection


class IMDFRelationship(IMDFFeature):
    category: IMDFRelationshipCategory
    direction: IMDFDirection
    origin: Optional[IMDFFeatureReference] = None
    intermediary: Optional[List[IMDFFeatureReference]] = None
    destination: Optional[IMDFFeatureReference] = None
    hours: Any = None  # Actual type HOURS
    geometry: Optional[shapely.geometry.base.BaseGeometry] = None
