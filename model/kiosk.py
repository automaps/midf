from dataclasses import dataclass

from model import FeatureType, IMDFFeature, KioskId, KioskProperties, Polygonal


@dataclass
class Kiosk(IMDFFeature):
  id: KioskId

  geometry: Polygonal
  properties: KioskProperties
  feature_type: FeatureType = FeatureType.KIOSK
