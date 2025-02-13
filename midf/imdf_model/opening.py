from typing import Any, Mapping, Optional, Union

import shapely

from .base import IMDFFeature
from ..enums import IMDFOpeningCategory
from ..midf_typing import Door

__all__ = ["IMDFOpening"]


class IMDFOpening(IMDFFeature):
    geometry: shapely.LineString
    category: Union[
        IMDFOpeningCategory, str
    ]  # TODO: Some openings have a category that is not in the enum, so we allow a
    # string here, but we should validate it, it is not valid, we should raise an error.
    level_id: str

    accessibility: Any = None
    access_control: Any = None
    door: Optional[Door] = None
    name: Optional[Mapping[str, str]] = None
    alt_name: Optional[Mapping[str, str]] = None
    display_point: Optional[shapely.Point] = None
