from dataclasses import dataclass, field

from geojson import Point

from model.base import FeatureProperties, IMDFFeature
from model.enums import AnchorId, FeatureType


@dataclass
class Anchor(IMDFFeature):
  id: AnchorId

  geometry: Point
  properties: FeatureProperties = field(default_factory=lambda: {
    "address_id": None,
    "unit_id": ""
  })
  feature_type: FeatureType = FeatureType.ANCHOR
