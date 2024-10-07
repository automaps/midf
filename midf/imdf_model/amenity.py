from typing import Any, List, Optional

from .other import IMDFFeature

__all__ = ["IMDFAmenity"]

class IMDFAmenity(IMDFFeature):
  geometry: Any  # shapely.Point
  unit_ids: Optional[List[str]] = None  # TODO: SHOULD NOT BE NULLABLE!
  category: Any = ""
  accessibility: Any = None
  name: Any = None
  alt_name: Any = None
  hours: Any = None
  phone: Any = None
  website: Any = None

  address_id: Any = None
  correlation_id: Any = None
