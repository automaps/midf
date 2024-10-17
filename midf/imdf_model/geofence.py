from typing import Any

from .base import IMDFFeature

__all__ = ["IMDFGeofence"]

from ..enums import IMDFGeofenceCategory


class IMDFGeofence(IMDFFeature):
    geometry: Any  # Polygonal
    category: IMDFGeofenceCategory
