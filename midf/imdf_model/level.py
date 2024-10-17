from typing import Any, Dict, List, Optional

from .base import IMDFFeature

__all__ = ["IMDFLevel"]

from ..enums import IMDFLevelCategory

class IMDFLevel(IMDFFeature):
  geometry: Any  # Polygonal

  category: IMDFLevelCategory
  restriction: Optional[str] = None
  outdoor: bool = False
  ordinal: int = 0

  name: dict[str, str]
  short_name: Dict[str, str] = None
  address_id: Optional[str] = None
  building_ids: Optional[List[str]] = None
