from typing import List, Optional

import shapely
from attr import dataclass

from midf.typing import Labels, MIDFFeature, Polygonal
from .building import MIDFBuilding
from .level import MIDFLevel

__all__ = ["MIDFGeofence"]


@dataclass
class MIDFGeofence(MIDFFeature):
    geometry: Polygonal

    category: str
    restriction: Optional[str] = None
    accessibility: Optional[List[str]] = None

    name: Optional[Labels] = None
    alt_name: Optional[Labels] = None

    correlation_id: Optional[str] = None
    display_point: Optional[shapely.Point] = None

    buildings: Optional[List[MIDFBuilding]] = None
    levels: Optional[List[MIDFLevel]] = None
    parents: Optional[List["MIDFGeofence"]] = None
