from dataclasses import dataclass, field

from model import FeatureProperties, FeatureType, GeofenceId, IMDFFeature, Polygonal


@dataclass
class Geofence(IMDFFeature):
  id: GeofenceId

  geometry: Polygonal
  properties: FeatureProperties = field(default_factory=lambda: {
    "category": ""
  })
  feature_type: FeatureType = FeatureType.GEOFENCE
