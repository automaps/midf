from typing import Any, Mapping, Optional

from .base import IMDFFeature

__all__ = ["IMDFFixture"]

from ..enums import IMDFFixtureCategory
from ..typing import Polygonal

class IMDFFixture(IMDFFeature):
  geometry: Polygonal
  level_id: str

  category: IMDFFixtureCategory
  anchor_id: Any = None

  name: Optional[Mapping[str, str]] = None
  alt_name: Optional[Mapping[str, str]] = None
