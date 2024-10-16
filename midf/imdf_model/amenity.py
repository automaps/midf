from typing import Any, List, Optional

import shapely

from .base import IMDFFeature

__all__ = ["IMDFAmenity"]

from ..enums import AmenityCategory


class IMDFAmenity(IMDFFeature):
    geometry: shapely.Point
    unit_ids: Optional[List[str]] = None  # TODO: SHOULD NOT BE NULLABLE!
    category: AmenityCategory
    accessibility: Any = None
    name: Any = None
    alt_name: Any = None
    hours: Any = None
    phone: Any = None
    website: Any = None

    address_id: Any = None
    correlation_id: Any = None
