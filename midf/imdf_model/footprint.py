from typing import Any, List, Mapping, Optional

from .other import IMDFFeature

__all__ = ["IMDFFootprint"]

class IMDFFootprint(IMDFFeature):
  geometry: Any  # Polygonal
  category: str = ""
  name: Optional[Mapping[str, str]] = None
  building_ids: Optional[List[str]] = None  # TODO: SHOULD NOT BE NULLABLE!
