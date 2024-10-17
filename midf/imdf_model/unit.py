from typing import Any, Mapping, Optional, Union

import shapely

from .base import IMDFFeature
from ..enums import IMDFUnitCategory

__all__ = ["IMDFUnit"]


class IMDFUnit(IMDFFeature):
    geometry: Any  # Polygonal
    level_id: str
    category: Union[IMDFUnitCategory, str]
    restriction: Optional[str] = None
    accessibility: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    hours: Optional[str] = None
    display_point: Optional[shapely.Point] = None
    address_od: Optional[str] = None
    name: Optional[Mapping[str, str]] = None
    alt_name: Optional[Mapping[str, str]] = None
