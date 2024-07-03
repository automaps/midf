from dataclasses import dataclass, field
from typing import Optional

from model.base import FeatureProperties, IMDFFeature
from model.enums import FeatureType, RelationshipId


@dataclass
class Relationship(IMDFFeature):
  id: RelationshipId
  feature_type: FeatureType = FeatureType.RELATIONSHIP
  geometry: Optional[Geometry] = None
  properties: FeatureProperties = field(default_factory=lambda: {
    "category": "",
    "direction": "",
    "origin": None,
    "intermediary": None,
    "destination": None,
    "hours": None
  })
