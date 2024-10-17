from typing import Any, List, Mapping, Optional

from .base import IMDFFeature

__all__ = ["IMDFFootprint"]

from ..enums import IMDFFootprintCategory

class IMDFFootprint(IMDFFeature):
  geometry: Any  # Polygonal
  category: IMDFFootprintCategory
  name: Optional[Mapping[str, str]] = None
  building_ids: Optional[List[str]] = None  # TODO: SHOULD NOT BE NULLABLE!
