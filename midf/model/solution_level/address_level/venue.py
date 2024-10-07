from typing import Optional

import shapely
from attr import dataclass

from midf.typing import MIDFFeature, MIDFLabels, Polygonal

__all__ = ["MIDFVenue"]

@dataclass
class MIDFVenue(MIDFFeature):
  geometry: Polygonal
  category: str

  name: MIDFLabels

  display_point: shapely.Point

  restriction: Optional[str] = None
  alt_name: Optional[MIDFLabels] = None
  hours: Optional[str] = None
  phone: Optional[str] = None
  website: Optional[str] = None
