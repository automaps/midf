__all__ = ["Polygonal", "Lineal", "MIDFFeature", "Labels", "Temporality"]

from dataclasses import dataclass
from typing import Mapping, Union

try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum

import shapely

Polygonal = Union[shapely.Polygon, shapely.MultiPolygon]
Lineal = Union[shapely.LineString, shapely.MultiLineString]
Labels = Mapping[str, str]


@dataclass
class MIDFFeature:
    id: str


@dataclass
class Temporality:
    start: str
    end: str
    modified: str
