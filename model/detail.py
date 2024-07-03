from dataclasses import dataclass, field

from model.base import FeatureProperties, IMDFFeature
from model.enums import DetailId, FeatureType


@dataclass
class Detail(IMDFFeature):
  id: DetailId
  feature_type: FeatureType = FeatureType.DETAIL
  properties: FeatureProperties = field(default_factory=lambda: {
    "level_id": ""
  })
