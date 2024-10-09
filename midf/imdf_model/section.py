from typing import Any, Mapping, Optional

from .other import IMDFFeature
from ..enums import SectionCategory

__all__ = ["IMDFSection"]


class IMDFSection(IMDFFeature):
    geometry: Any  # Polygonal

    category: SectionCategory
    restriction: Any = None
    accessibility: Any = None
    address_id: Any = None
    correlation_id: Any = None
    parents: Any = None
    level_id: str = None
    display_point: Any = None  # shapely.Point
    alt_name: Optional[Mapping[str, str]] = None
    name: Optional[Mapping[str, str]] = None
