from typing import Any, Mapping, Optional

import shapely

from .base import IMDFFeature
from ..enums import OpeningCategory
from ..typing import Door

__all__ = ["IMDFOpening"]


class IMDFOpening(IMDFFeature):
    geometry: shapely.LineString
    category: OpeningCategory
    level_id: str

    accessibility: Any = None
    access_control: Any = None
    door: Optional[Door] = None
    name: Optional[Mapping[str, str]] = None
    alt_name: Optional[Mapping[str, str]] = None
    display_point: Optional[shapely.Point] = None
