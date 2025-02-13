from typing import Optional

import shapely
from attr import dataclass

from midf.midf_typing import Labels, MIDFFeature, Polygonal

__all__ = ["MIDFVenue"]


@dataclass
class MIDFVenue(MIDFFeature):
    geometry: Polygonal
    category: str

    name: Labels

    display_point: shapely.Point

    restriction: Optional[str] = None
    alt_name: Optional[Labels] = None
    hours: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
