from typing import Any, Optional

import shapely

from .base import IMDFFeature

__all__ = ["IMDFVenue"]

from ..enums import IMDFVenueCategory
from ..midf_typing import Labels, Polygonal


class IMDFVenue(IMDFFeature):
    geometry: Polygonal
    name: Labels  # Language:Value # { ""en"": ""Kansas City International Airport"" }"
    address_id: str  # 984eb70b-da05-4ed7-809b-4d0e169f5d29
    display_point: shapely.Point
    category: IMDFVenueCategory  # airport.intl
    hours: Optional[str] = None  # 24/7
    website: Optional[str] = None  # https://www.flykci.com/
    phone: Optional[str] = None  # +1-816-243-5237
    restriction: Optional[Any] = None
    alt_name: Optional[Labels] = None
