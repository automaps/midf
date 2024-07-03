from dataclasses import dataclass, field

from model import FeatureProperties, FeatureType, IMDFFeature, OccupantId


@dataclass
class Occupant(IMDFFeature):
  id: OccupantId
  feature_type: FeatureType = FeatureType.OCCUPANT
  geometry: None = None
  properties: FeatureProperties = field(default_factory=lambda: {
    "name": {},
    "category": "",
    "anchor_id": "",
    "hours": None,
    "phone": None,
    "website": None,
    "validity": None,
    "correlation_id": None
  })
