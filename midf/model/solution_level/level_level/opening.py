from typing import Any, List, Optional

import shapely
from attr import dataclass

from midf.typing import MIDFFeature, MIDFLabels

__all__ = ["MIDFOpening"]


@dataclass
class MIDFOpening(MIDFFeature):
    geometry: shapely.LineString

    category: str
    accessibility: Optional[List[str]] = None

    access_control: Optional[List[str]] = None

    door: Optional[Any] = None

    name: Optional[MIDFLabels] = None
    alt_name: Optional[MIDFLabels] = None

    display_point: Optional[shapely.Point] = None
