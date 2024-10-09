from typing import Any, Mapping

from .other import IMDFFeature

__all__ = ["IMDFVenue"]

from ..enums import VenueCategory


class IMDFVenue(IMDFFeature):
    geometry: Any  # shapely.Polygon
    name: Mapping[
        str, str
    ]  # Language:Value # "{ ""en"": ""Kansas City International Airport"" }"
    address_id: str  # 984eb70b-da05-4ed7-809b-4d0e169f5d29
    display_point: Any  # shapely.Point
    category: VenueCategory  # airport.intl
    hours: str  # 24/7
    website: str  # https://www.flykci.com/
    phone: str  # +1-816-243-5237
    restriction: Any = None
    alt_name: Any = None
