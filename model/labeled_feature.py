from dataclasses import dataclass
from typing import Optional

from geojson import Point

from model.base import NamedFeatureProperties
from model.enums import LevelId


@dataclass
class LabeledFeatureProperties(NamedFeatureProperties):
  level_id: LevelId
  display_point: Optional[Point]
