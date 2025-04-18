from integration_system.common_models import MIVenueType
from midf.enums import IMDFVenueCategory

IMDF_VENUE_CATEGORY_TO_MI_VENUE_TYPE = {
    IMDFVenueCategory.airport: MIVenueType.airport,
    IMDFVenueCategory.airport_intl: MIVenueType.airport_intl,
    IMDFVenueCategory.aquarium: MIVenueType.aquarium,
    IMDFVenueCategory.resort: MIVenueType.resort,
    IMDFVenueCategory.governmentfacility: MIVenueType.government_facility,
    IMDFVenueCategory.shoppingcenter: MIVenueType.shopping_center,
    IMDFVenueCategory.hotel: MIVenueType.hotel,
    IMDFVenueCategory.businesscampus: MIVenueType.business_campus,
    IMDFVenueCategory.casino: MIVenueType.casino,
    IMDFVenueCategory.communitycenter: MIVenueType.community_center,
    IMDFVenueCategory.conventioncenter: MIVenueType.convention_center,
    IMDFVenueCategory.healthcarefacility: MIVenueType.healthcare_facility,
    IMDFVenueCategory.museum: MIVenueType.museum,
    IMDFVenueCategory.parkingfacility: MIVenueType.parking_facility,
    IMDFVenueCategory.retailstore: MIVenueType.retail_store,
    IMDFVenueCategory.stadium: MIVenueType.stadium,
    IMDFVenueCategory.stripmall: MIVenueType.strip_mall,
    IMDFVenueCategory.theater: MIVenueType.theater,
    IMDFVenueCategory.themepark: MIVenueType.theme_park,
    IMDFVenueCategory.trainstation: MIVenueType.train_station,
    IMDFVenueCategory.transitstation: MIVenueType.transit_station,
    IMDFVenueCategory.university: MIVenueType.university,
}
ASSUME_OUTDOOR_IF_MISSING_BUILDING = True
DETAIL_LOCATION_TYPE_NAME = "Detail"
KIOSK_LOCATION_TYPE_NAME = "Kiosk"
OUTDOOR_BUILDING_NAME = "General Area"
ANCHOR_NAME = "Anchor"
PATCH_DATA = True
UNIT_LESS_OCCUPANT_LEVEL_NAME = "UNIT_LESS_OCCUPANT_LEVEL"
UNIT_LESS_POINT_SIZE = 1e-7
