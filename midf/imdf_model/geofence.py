from typing import Any

from .other import IMDFFeature

__all__ = ["IMDFGeofence"]

from ..enums import GeofenceCategory


class IMDFGeofence(IMDFFeature):
    geometry: Any  # Polygonal
    category: GeofenceCategory
