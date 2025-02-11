from typing import List, Optional

import shapely
from attr import dataclass

from midf.midf_typing import Direction, MIDFFeature

__all__ = ["MIDFRelationship"]


@dataclass
class MIDFRelationship(MIDFFeature):
    category: str
    direction: Direction

    geometry: Optional[shapely.geometry.base.BaseGeometry] = None
    origin: Optional[MIDFFeature] = None
    intermediary: Optional[List[MIDFFeature]] = None
    destination: Optional[MIDFFeature] = None

    hours: Optional[str] = None
