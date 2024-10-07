__all__ = ["Polygonal", "Lineal", "MIDFFeature", "MIDFLabels", "Direction"]

from typing import Mapping, Union

import shapely
from attr import dataclass

Polygonal = Union[shapely.Polygon, shapely.MultiPolygon]
Lineal = Union[shapely.LineString, shapely.MultiLineString]

@dataclass
class MIDFFeature:
  id: str

MIDFLabels = Mapping[str, str]

try:
  from enum import StrEnum
except ImportError:
  from strenum import StrEnum

class Direction(StrEnum):
  directed = "directed"
  undirected = "undirected"
