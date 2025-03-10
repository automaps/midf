from typing import Any, List, Mapping, Optional, Union

from .base import IMDFFeature

__all__ = ["IMDFGeofence"]

from ..enums import (
    IMDFAccessibilityCategory,
    IMDFGeofenceCategory,
    IMDFRestrictionCategory,
)


class IMDFGeofence(IMDFFeature):
    geometry: Any  # Polygonal
    category: Union[
        IMDFGeofenceCategory, str
    ]  # TODO: Some geofences have a category that is not in the enum, so we allow a # TODO: REMOVE FOR STRICT
    name: Optional[Mapping[str, str]] = None
    alt_name: Optional[Mapping[str, str]] = None
    restriction: Optional[IMDFRestrictionCategory] = None
    accessibility: Optional[IMDFAccessibilityCategory] = None
    correlation_id: Optional[str] = None
    display_point: Optional[Any] = None
    building_ids: Optional[List[str]] = None
    level_ids: Optional[List[str]] = None
    parents: Optional[List[str]] = None
