import logging
from collections import defaultdict

import shapely
from jord.shapely_utilities import clean_shape, dilate

from integration_system.model import (
    Building,
    LocationType,
    PostalAddress,
    Solution,
    VenueType,
)
from midf.enums import VenueCategory
from midf.model import MIDFSolution

IMDF_VENUE_CATEGORY_TO_MI_VENUE_TYPE = {
    VenueCategory.airport: VenueType.airport,
    VenueCategory.airport_intl: VenueType.airport_intl,
    VenueCategory.aquarium: VenueType.aquarium,
    VenueCategory.resort: VenueType.resort,
    VenueCategory.governmentfacility: VenueType.government_facility,
    VenueCategory.shoppingcenter: VenueType.shopping_center,
    VenueCategory.hotel: VenueType.hotel,
    VenueCategory.businesscampus: VenueType.business_campus,
    VenueCategory.casino: VenueType.casino,
    VenueCategory.communitycenter: VenueType.community_center,
    VenueCategory.conventioncenter: VenueType.convention_center,
    VenueCategory.healthcarefacility: VenueType.healthcare_facility,
    VenueCategory.museum: VenueType.museum,
    VenueCategory.parkingfacility: VenueType.parking_facility,
    VenueCategory.retailstore: VenueType.retail_store,
    VenueCategory.stadium: VenueType.stadium,
    VenueCategory.stripmall: VenueType.strip_mall,
    VenueCategory.theater: VenueType.theater,
    VenueCategory.themepark: VenueType.theme_park,
    VenueCategory.trainstation: VenueType.train_station,
    VenueCategory.transitstation: VenueType.transit_station,
    VenueCategory.university: VenueType.university,
}

logger = logging.getLogger(__name__)

ASSUME_OUTDOOR_IF_MISSING_BUILDING = True


def to_mi_solution(midf_solution: MIDFSolution) -> Solution:
    mi_solution = Solution(
        external_id=f"{midf_solution.manifest.generated_by}{midf_solution.manifest.version}",
        name=midf_solution.manifest.generated_by,
        customer_id="953f7a89334a4013927857ab",
    )

    address_venue_mapping = defaultdict(list)

    for address in midf_solution.addresses:
        for venue in address.venues:
            venue_name = next(iter(venue.name.values()))

            venue_key = mi_solution.add_venue(
                admin_id=venue.id,
                name=venue_name,
                venue_type=IMDF_VENUE_CATEGORY_TO_MI_VENUE_TYPE[venue.category],
                address=PostalAddress(
                    postal_code=address.postal_code,
                    street1=address.address,
                    country=address.country,
                    city=address.locality,
                    region=address.province,
                ),
                polygon=dilate(venue.display_point),
            )
            address_venue_mapping[address.id].append(venue_key)

    building_footprint_mapping = defaultdict(list)

    outdoor_building_admin_id = "general_area"

    for footprint in midf_solution.footprints:
        for building in footprint.buildings:
            building_footprint_mapping[building.id].append(footprint)

    for building in midf_solution.buildings:
        if building.address:
            found_venue_key = next(iter(address_venue_mapping[building.address.id]))
        else:
            found_venue_key = venue_key

        building_footprint = shapely.Polygon()

        for fp in building_footprint_mapping[building.id]:
            if isinstance(fp.geometry, shapely.Polygon):
                building_footprint |= fp.geometry
            else:
                logger.error(f"Ignoring {fp}")

        if building.name:
            building_name = next(iter(building.name.values()))
        else:
            building_name = "Building"

        mi_solution.add_building(
            building.id,
            name=building_name,
            polygon=building_footprint,
            venue_key=found_venue_key,
        )

    for level in midf_solution.levels:
        # level.address TODO: UNUSED ATM

        if level.buildings is None:
            if level.outdoor or ASSUME_OUTDOOR_IF_MISSING_BUILDING:
                found_building = mi_solution.buildings.get(
                    Building.compute_key(admin_id=outdoor_building_admin_id)
                )
                if found_building is None:
                    found_building_key = mi_solution.add_building(
                        outdoor_building_admin_id,
                        "General Area",
                        mi_solution.venues.get(venue_key).polygon,
                        venue_key=found_venue_key,
                    )
                    found_building = mi_solution.buildings.get(found_building_key)
            else:
                logger.error(f"Skipping {level}")
                continue
        else:
            found_building = mi_solution.buildings.get(
                Building.compute_key(admin_id=next(iter(level.buildings)).id)
            )

        floor_name = next(iter(level.name.values()))

        floor_key = mi_solution.add_floor(
            building_key=found_building.key,
            name=floor_name,
            polygon=found_building.polygon,
            floor_index=level.ordinal,
        )

        if level.units:
            for unit in level.units:
                unit_name = next(iter(level.name.values()))
                unit_geom = clean_shape(unit.geometry)

                location_type_key = LocationType.compute_key(name=unit.category)
                if mi_solution.location_types.get(location_type_key) is None:
                    mi_solution.add_location_type(name=unit.category)

                if isinstance(unit_geom, shapely.Polygon):
                    mi_solution.add_area(
                        admin_id=unit.id,
                        name=unit_name,
                        polygon=unit_geom,
                        floor_key=floor_key,
                        location_type_key=location_type_key,
                    )
                else:
                    logger.error(f"Ignoring {unit}")

        if level.details:
            for detail in level.details:
                detail_name = next(iter(level.name.values()))
                detail_geom = dilate(clean_shape(detail.geometry))

                location_type_key = LocationType.compute_key(name=detail.category)
                if mi_solution.location_types.get(location_type_key) is None:
                    mi_solution.add_location_type(name=detail.category)

                if isinstance(detail_geom, shapely.Polygon):
                    mi_solution.add_area(
                        admin_id=detail.id,
                        name=detail_name,
                        polygon=detail_geom,
                        floor_key=floor_key,
                        location_type_key=location_type_key,
                    )
                else:
                    logger.error(f"Ignoring {detail}")

        if level.kiosks:
            for detail in level.kiosks:
                detail_name = next(iter(level.name.values()))
                detail_geom = clean_shape(detail.geometry)

                location_type_key = LocationType.compute_key(name=detail.category)
                if mi_solution.location_types.get(location_type_key) is None:
                    mi_solution.add_location_type(name=detail.category)

                if isinstance(detail_geom, shapely.Polygon):
                    mi_solution.add_area(
                        admin_id=detail.id,
                        name=detail_name,
                        polygon=detail_geom,
                        floor_key=floor_key,
                        location_type_key=location_type_key,
                    )
                else:
                    logger.error(f"Ignoring {detail}")

        if level.sections:
            for detail in level.sections:
                detail_name = next(iter(level.name.values()))
                detail_geom = clean_shape(detail.geometry)

                location_type_key = LocationType.compute_key(name=detail.category)
                if mi_solution.location_types.get(location_type_key) is None:
                    mi_solution.add_location_type(name=detail.category)

                if isinstance(detail_geom, shapely.Polygon):
                    mi_solution.add_area(
                        admin_id=detail.id,
                        name=detail_name,
                        polygon=detail_geom,
                        floor_key=floor_key,
                        location_type_key=location_type_key,
                    )
                else:
                    logger.error(f"Ignoring {detail}")

        if level.fixtures:
            for detail in level.fixtures:
                detail_name = next(iter(level.name.values()))
                detail_geom = clean_shape(detail.geometry)

                location_type_key = LocationType.compute_key(name=detail.category)
                if mi_solution.location_types.get(location_type_key) is None:
                    mi_solution.add_location_type(name=detail.category)

                if isinstance(detail_geom, shapely.Polygon):
                    mi_solution.add_area(
                        admin_id=detail.id,
                        name=detail_name,
                        polygon=detail_geom,
                        floor_key=floor_key,
                        location_type_key=location_type_key,
                    )
                else:
                    logger.error(f"Ignoring {detail}")

        if level.openings:
            for detail in level.openings:
                detail_name = next(iter(level.name.values()))
                detail_geom = dilate(clean_shape(detail.geometry))

                location_type_key = LocationType.compute_key(name=detail.category)
                if mi_solution.location_types.get(location_type_key) is None:
                    mi_solution.add_location_type(name=detail.category)

                if isinstance(detail_geom, shapely.Polygon):
                    mi_solution.add_area(
                        admin_id=detail.id,
                        name=detail_name,
                        polygon=detail_geom,
                        floor_key=floor_key,
                        location_type_key=location_type_key,
                    )
                else:
                    logger.error(f"Ignoring {detail}")

    area_union = shapely.convex_hull(
        shapely.unary_union([a.polygon for a in mi_solution.areas])
    )

    mi_solution.update_building(outdoor_building_admin_id, polygon=area_union)
    mi_solution.update_venue(found_venue_key, polygon=area_union)

    return mi_solution
