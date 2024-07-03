from dataclasses import dataclass
from typing import Optional

from geojson import Feature, Point

from model.enums import Labels


@dataclass
class FeatureProperties:
  pass


@dataclass
class NamedFeatureProperties(FeatureProperties):
  name: Optional[Labels]
  alt_name: Optional[Labels]
  display_point: Optional[Point]


@dataclass
class FeatureReference:
  id: str
  feature_type: str


@dataclass
class IMDFFeature(Feature):
  feature_type: str
  properties: FeatureProperties
