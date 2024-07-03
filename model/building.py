from dataclasses import dataclass

from model.base import IMDFFeature
from model.enums import BuildingId, BuildingProperties, FeatureType


@dataclass
class Building(IMDFFeature):
  id: BuildingId
  feature_type: FeatureType = FeatureType.BUILDING
  geometry: None = None
  properties: BuildingProperties
