from typing import List, Optional

import shapely
from attr import dataclass

from midf.midf_typing import Labels, MIDFFeature, Polygonal
from ..address import MIDFAddress

__all__ = ["MIDFSection"]


@dataclass
class MIDFSection(MIDFFeature):
    geometry: Polygonal
    category: str

    restriction: Optional[str] = None
    accessibility: Optional[List[str]] = None
    name: Optional[Labels] = None
    alt_name: Optional[Labels] = None
    display_point: Optional[shapely.Point] = None
    correlation_id: Optional[str] = None

    address: Optional[MIDFAddress] = None
    parents: Optional[List["MIDFSection"]] = None
