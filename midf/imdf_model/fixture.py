from typing import Any, Mapping, Optional

from .other import IMDFFeature

__all__ = ["IMDFFixture"]


class IMDFFixture(IMDFFeature):
    geometry: Any  # shapely.geometry.base.BaseGeometry
    level_id: str

    category: str = ""
    anchor_id: Any = None

    name: Optional[Mapping[str, str]] = None
    alt_name: Optional[Mapping[str, str]] = None
