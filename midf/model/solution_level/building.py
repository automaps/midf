from typing import Optional

import shapely
from attr import dataclass

from midf.typing import Labels, MIDFFeature
from .address import MIDFAddress

__all__ = ["MIDFBuilding"]


@dataclass
class MIDFBuilding(MIDFFeature):
    category: str

    name: Optional[Labels] = None
    alt_name: Optional[Labels] = None

    restriction: Optional[str] = None
    display_point: Optional[shapely.Point] = None

    address: Optional[MIDFAddress] = None
