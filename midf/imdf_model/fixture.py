from typing import Any, Mapping, Optional

from .base import IMDFFeature

__all__ = ["IMDFFixture"]

from ..enums import FixtureCategory
from ..typing import Polygonal


class IMDFFixture(IMDFFeature):
    geometry: Polygonal
    level_id: str

    category: FixtureCategory
    anchor_id: Any = None

    name: Optional[Mapping[str, str]] = None
    alt_name: Optional[Mapping[str, str]] = None
