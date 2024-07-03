from dataclasses import dataclass, field

from geojson import LineString

from model import FeatureType, IMDFFeature, LabeledFeatureProperties, OpeningId


@dataclass
class Opening(IMDFFeature):
  id: OpeningId

  geometry: LineString
  feature_type: FeatureType = FeatureType.OPENING
  properties: LabeledFeatureProperties = field(default_factory=lambda: {
    "category": "",
    "accessibility": None,
    "access_control": None,
    "door": None
  })
