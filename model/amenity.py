from dataclasses import dataclass, field

from geojson import Point

from model import AmenityId, FeatureProperties, FeatureType, IMDFFeature


@dataclass
class Amenity(IMDFFeature):
  id: AmenityId

  geometry: Point
  properties: FeatureProperties = field(default_factory=lambda: {
    "category": "",
    "accessibility": None,
    "name": None,
    "alt_name": None,
    "hours": None,
    "phone": None,
    "website": None,
    "unit_ids": [],
    "address_id": None,
    "correlation_id": None
  })
  feature_type: FeatureType = FeatureType.AMENITY
