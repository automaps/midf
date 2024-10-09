from attr import dataclass

from midf.typing import MIDFFeature, MIDFLabels

__all__ = ["MIDFOccupant"]


@dataclass
class MIDFOccupant(MIDFFeature):
    name: MIDFLabels
    category: str
    hours: str
    phone: str
    website: str
    validity: str
    correlation_id: str
