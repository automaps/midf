from typing import Any, Mapping, Optional

from .other.base import IMDFFeature

__all__ = ["IMDFBuilding"]

from ..enums import BuildingCategory


class IMDFBuilding(IMDFFeature):
    geometry: Any = None  # shapely.geometry.base.BaseGeometry
    category: BuildingCategory
    restriction: Optional[str] = None
    name: Optional[Mapping[str, str]] = None
    alt_name: Optional[Mapping[str, str]] = None
    display_point: Any  # shapely.Point
    address_id: Optional[str] = None


# """
# 'category' = {str} 'footprint'
# 'name' = {NoneType} None
# 'alt_name' = {NoneType} None
# 'restriction' = {NoneType} None
# 'display_point' = {str} '{ "type": "Point", "coordinates": [ -94.719525354500007, 39.298384401500002 ] }'
# 'address_id' = {str} '984eb70b-da05-4ed7-809b-4d0e169f5d29'
# 'geometry' = {NoneType} None
# """
