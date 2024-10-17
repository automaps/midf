__all__ = ["Polygonal", "Lineal", "MIDFFeature", "Labels", "Direction", "Temporality"]

from typing import Mapping, Optional, Union

try:
  from enum import StrEnum
except ImportError:
  from strenum import StrEnum
import shapely
from attr import dataclass

Polygonal = Union[shapely.Polygon, shapely.MultiPolygon]
Lineal = Union[shapely.LineString, shapely.MultiLineString]
Labels = Mapping[str, str]

@dataclass
class MIDFFeature:
  id: str

class Direction(StrEnum):
  directed = "directed"
  undirected = "undirected"

@dataclass
class Temporality:
  start: str
  end: str
  modified: str

@dataclass
class Door:
  type: Optional[str] = None
  automatic: bool = False
  material: Optional[str] = None
