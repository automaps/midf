from dataclasses import dataclass, field

from model import FeatureType, IMDFFeature, LabeledFeatureProperties, Polygonal, SectionId


@dataclass
class Section(IMDFFeature):
  id: SectionId

  geometry: Polygonal
  feature_type: FeatureType = FeatureType.SECTION
  properties: LabeledFeatureProperties = field(default_factory=lambda: {
    "category": "",
    "restriction": None,
    "accessibility": None,
    "address_id": None,
    "correlation_id": None,
    "parents": None
  })
