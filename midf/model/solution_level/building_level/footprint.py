from typing import Collection

from attr import dataclass

from midf.typing import Labels, MIDFFeature, Polygonal
from ..building import MIDFBuilding

__all__ = ["MIDFFootprint"]


@dataclass
class MIDFFootprint(MIDFFeature):
    geometry: Polygonal
    category: str
    name: Labels
    buildings: Collection[MIDFBuilding]
