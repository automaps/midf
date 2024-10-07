from typing import Any

from .other import IMDFFeature

__all__ = ["IMDFGeofence"]

class IMDFGeofence(IMDFFeature):
  geometry: Any  # Polygonal
  category: str = ""
