from typing import Any, Mapping, Optional, Union

from .other import IMDFFeature

__all__ = ["IMDFUnit"]

from ..enums import UnitCategory


class IMDFUnit(IMDFFeature):
    geometry: Any  # Polygonal
    level_id: str
    category: Union[UnitCategory, str]
    restriction: Optional[str] = None
    accessibility: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    hours: Optional[str] = None
    display_point: Optional[Any] = None  # shapely.Point
    address_od: Optional[str] = None
    name: Optional[Mapping[str, str]] = None
    alt_name: Optional[Mapping[str, str]] = None
