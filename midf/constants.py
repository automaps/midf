from integration_system.model import VenueType
from midf.enums import IMDFVenueCategory

IMDF_VENUE_CATEGORY_TO_MI_VENUE_TYPE = {
    IMDFVenueCategory.airport: VenueType.airport,
    IMDFVenueCategory.airport_intl: VenueType.airport_intl,
    IMDFVenueCategory.aquarium: VenueType.aquarium,
    IMDFVenueCategory.resort: VenueType.resort,
    IMDFVenueCategory.governmentfacility: VenueType.government_facility,
    IMDFVenueCategory.shoppingcenter: VenueType.shopping_center,
    IMDFVenueCategory.hotel: VenueType.hotel,
    IMDFVenueCategory.businesscampus: VenueType.business_campus,
    IMDFVenueCategory.casino: VenueType.casino,
    IMDFVenueCategory.communitycenter: VenueType.community_center,
    IMDFVenueCategory.conventioncenter: VenueType.convention_center,
    IMDFVenueCategory.healthcarefacility: VenueType.healthcare_facility,
    IMDFVenueCategory.museum: VenueType.museum,
    IMDFVenueCategory.parkingfacility: VenueType.parking_facility,
    IMDFVenueCategory.retailstore: VenueType.retail_store,
    IMDFVenueCategory.stadium: VenueType.stadium,
    IMDFVenueCategory.stripmall: VenueType.strip_mall,
    IMDFVenueCategory.theater: VenueType.theater,
    IMDFVenueCategory.themepark: VenueType.theme_park,
    IMDFVenueCategory.trainstation: VenueType.train_station,
    IMDFVenueCategory.transitstation: VenueType.transit_station,
    IMDFVenueCategory.university: VenueType.university,
}
ASSUME_OUTDOOR_IF_MISSING_BUILDING = True
DETAIL_LOCATION_TYPE_NAME = "Detail"
KIOSK_LOCATION_TYPE_NAME = "Kiosk"
OUTDOOR_BUILDING_NAME = "General Area"
ANCHOR_NAME = "Anchor"
PATCH_DATA = True
UNIT_LESS_OCCUPANT_LEVEL_NAME = "UNIT_LESS_OCCUPANT_LEVEL"
UNIT_LESS_POINT_SIZE = 1e-7
