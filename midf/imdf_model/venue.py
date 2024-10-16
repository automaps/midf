from typing import Any, Optional

import shapely

from .base import IMDFFeature

__all__ = ["IMDFVenue"]

from ..enums import VenueCategory
from ..typing import Labels, Polygonal


class IMDFVenue(IMDFFeature):
    geometry: Polygonal
    name: Labels  # Language:Value # "{ ""en"": ""Kansas City International Airport"" }"
    address_id: str  # 984eb70b-da05-4ed7-809b-4d0e169f5d29
    display_point: shapely.Point
    category: VenueCategory  # airport.intl
    hours: str  # 24/7
    website: str  # https://www.flykci.com/
    phone: str  # +1-816-243-5237
    restriction: Optional[Any] = None
    alt_name: Optional[Labels] = None
