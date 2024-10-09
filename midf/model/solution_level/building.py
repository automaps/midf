from typing import Optional

import shapely
from attr import dataclass

from midf.typing import MIDFFeature, MIDFLabels
from .address import MIDFAddress

__all__ = ["MIDFBuilding"]


@dataclass
class MIDFBuilding(MIDFFeature):
    category: str

    name: Optional[MIDFLabels] = None
    alt_name: Optional[MIDFLabels] = None

    restriction: Optional[str] = None
    display_point: Optional[shapely.Point] = None

    address: Optional[MIDFAddress] = None
