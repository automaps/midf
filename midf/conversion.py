import logging
from collections import defaultdict

import shapely
from jord.shapely_utilities import clean_shape, dilate

from integration_system.model import (
    Building,
    FALLBACK_OSM_GRAPH,
    Solution,
    VenueType,
)
from midf.enums import IMDFVenueCategory
from midf.mi_conversion import (
    convert_amenities,
    convert_buildings,
    convert_footprints,
    convert_geofences,
    convert_levels,
    convert_occupant_categories,
    convert_relationships,
    convert_venues,
)
from midf.model import MIDFSolution

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

logger = logging.getLogger(__name__)

ASSUME_OUTDOOR_IF_MISSING_BUILDING = True
DETAIL_LOCATION_TYPE_NAME = "Detail"
KIOSK_LOCATION_TYPE_NAME = "Kiosk"
OUTDOOR_BUILDING_NAME = "General Area"
ANCHOR_NAME = "Anchor"


def make_mi_building_admin_id_midf(building_id: str, venue_key: str) -> str:
    return f"{building_id.lower().replace(' ', '_')}_{venue_key}"


def to_mi_solution(midf_solution: MIDFSolution) -> Solution:
    mi_solution = Solution(
        external_id=f"{midf_solution.manifest.generated_by}{midf_solution.manifest.version}",
        name=midf_solution.manifest.generated_by,
        customer_id="953f7a89334a4013927857ab",
        occupants_enabled=True,
    )

    address_venue_mapping = defaultdict(list)

    venue, venue_key = convert_venues(address_venue_mapping, mi_solution, midf_solution)

    assert venue_key is not None, "No venue was found in the data"

    venue_graph_key = mi_solution.add_graph(
        graph_id=venue_key,
        osm_xml=FALLBACK_OSM_GRAPH,
        boundary=dilate(shapely.Point(0, 0)),
    )

    building_footprint_mapping = defaultdict(list)

    anchor_location_type = mi_solution.add_location_type(name=ANCHOR_NAME)

    occupant_category_mapping = convert_occupant_categories(mi_solution)

    convert_footprints(building_footprint_mapping, midf_solution)

    found_venue_key = convert_buildings(
        address_venue_mapping,
        building_footprint_mapping,
        mi_solution,
        midf_solution,
        venue,
        venue_key,
    )

    convert_levels(
        anchor_location_type,
        found_venue_key,
        mi_solution,
        midf_solution,
        occupant_category_mapping,
        venue_graph_key,
        venue_key,
    )

    convert_amenities(mi_solution, midf_solution)

    convert_geofences(found_venue_key, mi_solution, midf_solution)

    convert_relationships(mi_solution, midf_solution)

    solution_locations_union = shapely.convex_hull(
        shapely.unary_union(
            [a.polygon for a in mi_solution.areas]
            + [r.polygon for r in mi_solution.rooms]
            + [r.point for r in mi_solution.points_of_interest]
        )
    )

    blk = make_mi_building_admin_id_midf(OUTDOOR_BUILDING_NAME, found_venue_key)
    if mi_solution.buildings.get(Building.compute_key(admin_id=blk)) is not None:
        mi_solution.update_building(blk, polygon=solution_locations_union)

    mi_solution.update_graph(venue_graph_key, boundary=solution_locations_union)

    mi_solution.update_venue(
        found_venue_key, polygon=solution_locations_union, graph_key=venue_graph_key
    )

    return mi_solution
