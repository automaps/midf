from attr import dataclass

from midf.enums import IMDFOccupantCategory
from midf.typing import Labels, MIDFFeature, Temporality

__all__ = ["MIDFOccupant"]

@dataclass
class MIDFOccupant(MIDFFeature):
  name: Labels
  category: IMDFOccupantCategory
  hours: str
  phone: str
  website: str
  validity: Temporality
  correlation_id: str
