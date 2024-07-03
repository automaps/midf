from dataclasses import dataclass, field

from model import FeatureProperties, FeatureType, IMDFFeature, Polygonal, VenueId


@dataclass
class Venue(IMDFFeature):
  id: VenueId
  geometry: Polygonal
  feature_type: FeatureType = FeatureType.VENUE

  properties: FeatureProperties = field(default_factory=lambda: {
    "category": "",
    "restriction": None,
    "name": {},
    "alt_name": None,
    "hours": None,
    "phone": None,
    "website": None,
    "display_point": None,
    "address_id": ""
  })
