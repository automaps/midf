from typing import Optional

import shapely
from attr import dataclass

from midf.enums import IMDFFixtureCategory
from midf.midf_typing import Labels, MIDFFeature, Polygonal
from .unit_level import MIDFAnchor

__all__ = ["MIDFFixture"]


@dataclass
class MIDFFixture(MIDFFeature):
    geometry: Polygonal
    category: IMDFFixtureCategory
    name: Optional[Labels] = None
    alt_name: Optional[Labels] = None
    display_point: Optional[shapely.Point] = None

    anchor: Optional[MIDFAnchor] = None
