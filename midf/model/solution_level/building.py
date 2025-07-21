import shapely
from attr import dataclass
from typing import Optional

from midf.midf_typing import Labels, MIDFFeature
from .address import MIDFAddress

__all__ = ["MIDFBuilding"]

from ...enums import IMDFBuildingCategory


@dataclass
class MIDFBuilding(MIDFFeature):
    category: IMDFBuildingCategory

    name: Optional[Labels] = None
    alt_name: Optional[Labels] = None

    restriction: Optional[str] = None
    display_point: Optional[shapely.Point] = None

    address: Optional[MIDFAddress] = None
