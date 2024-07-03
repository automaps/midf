from dataclasses import dataclass

from model import FeatureType, IMDFFeature, Polygonal, UnitId, UnitProperties


@dataclass
class Unit(IMDFFeature):
  id: UnitId
  geometry: Polygonal
  feature_type: FeatureType = FeatureType.UNIT

  properties: UnitProperties
