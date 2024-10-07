from typing import Any, Mapping, Optional

from .other import IMDFFeature

__all__ = ["IMDFUnit"]

class IMDFUnit(IMDFFeature):
  geometry: Any  # Polygonal
  level_id: str
  category: str = ""
  restriction: Optional[str] = None
  accessibility: Optional[str] = None
  phone: Optional[str] = None
  website: Optional[str] = None
  hours: Optional[str] = None
  display_point: Optional[Any] = None  # shapely.Point
  address_od: Optional[str] = None
  name: Optional[Mapping[str, str]] = None
  alt_name: Optional[Mapping[str, str]] = None
