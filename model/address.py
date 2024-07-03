from dataclasses import dataclass, field

from model import AddressId, FeatureProperties, FeatureType, IMDFFeature


@dataclass
class Address(IMDFFeature):
  id: AddressId
  feature_type: FeatureType = FeatureType.ADDRESS
  geometry: None = None
  properties: FeatureProperties = field(default_factory=lambda: {
    "address": "",
    "unit": None,
    "locality": "",
    "province": None,
    "country": "",
    "postal_code": None,
    "postal_code_ext": None,
    "postal_code_vanity": None
  })
