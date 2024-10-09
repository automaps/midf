from typing import Optional

import shapely
from attr import dataclass

from midf.typing import MIDFFeature, MIDFLabels, Polygonal
from .unit_level import MIDFAnchor

__all__ = ["MIDFKiosk"]


@dataclass
class MIDFKiosk(MIDFFeature):
    geometry: Polygonal
    name: Optional[MIDFLabels] = None
    alt_name: Optional[MIDFLabels] = None
    display_point: Optional[shapely.Point] = None

    anchor: Optional[MIDFAnchor] = None
