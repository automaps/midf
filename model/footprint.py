from dataclasses import dataclass, field

from model import FeatureProperties, FeatureType, FootprintId, IMDFFeature, Polygonal


@dataclass
class Footprint(IMDFFeature):
  id: FootprintId

  geometry: Polygonal
  properties: FeatureProperties = field(default_factory=lambda: {
    "category": "",
    "name": None,
    "building_ids": []
  })
  feature_type: FeatureType = FeatureType.FOOTPRINT
