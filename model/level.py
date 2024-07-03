from dataclasses import dataclass

from model import FeatureType, IMDFFeature, LevelId, LevelProperties, Polygonal


@dataclass
class Level(IMDFFeature):
  id: LevelId

  geometry: Polygonal
  properties: LevelProperties
  feature_type: FeatureType = FeatureType.LEVEL
