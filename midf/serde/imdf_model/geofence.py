from typing import Any

from .other import IMDFFeature

__all__ = ["IMDFAmenity"]


class IMDFAmenity(IMDFFeature):
    geometry: Any  # Polygonal
    category: str = ""
