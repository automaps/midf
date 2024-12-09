import logging
from collections import defaultdict

import shapely
from jord.shapely_utilities import clean_shape, dilate

from integration_system.model import (
    Building,
    LocationType,
    OccupantType,
    PostalAddress,
    Solution,
    VenueType,
)
from midf.enums import IMDFOccupantCategory, IMDFVenueCategory
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


def to_mi_solution(midf_solution: MIDFSolution) -> Solution:
    mi_solution = Solution(
        external_id=f"{midf_solution.manifest.generated_by}{midf_solution.manifest.version}",
        name=midf_solution.manifest.generated_by,
        customer_id="953f7a89334a4013927857ab",
        occupants_enabled=True,
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

    anchor_name = "Anchor"
    anchor_location_type = mi_solution.add_location_type(name=anchor_name)

    occupant_category_mapping = {}
    for occupant_category in IMDFOccupantCategory:
        occupant_category_mapping[occupant_category] = (
            mi_solution.add_occupant_category(occupant_category.name)
        )

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
                    outdoor_building_key = mi_solution.add_building(
                        outdoor_building_admin_id,
                        "General Area",
                        mi_solution.venues.get(venue_key).polygon,
                        venue_key=found_venue_key,
                    )
                    found_building = mi_solution.buildings.get(outdoor_building_key)
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

                if unit.anchors:
                    for anchor in unit.anchors:
                        anchor_key = mi_solution.add_point_of_interest(
                            admin_id=anchor.id,
                            name=anchor_name,
                            point=anchor.geometry,
                            floor_key=floor_key,
                            location_type_key=anchor_location_type,
                        )

                        for occupant in anchor.occupants:
                            occupant_name = next(iter(occupant.name.values()))

                            occupant_template_key = mi_solution.add_occupant_template(
                                name=occupant_name,
                                occupant_type=OccupantType.OCCUPANT,
                                occupant_category_key=occupant_category_mapping[
                                    occupant.category
                                ],
                                # business_hours=occupant.hours,
                                # contact=occupant.phone + occupant.website,
                            )
                            mi_solution.add_occupant(
                                location_key=anchor_key,
                                occupant_template_key=occupant_template_key,
                            )

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
            for kiosk in level.kiosks:
                kiosk_name = next(iter(level.name.values()))
                kiosk_geom = clean_shape(kiosk.geometry)

                location_type_key = LocationType.compute_key(name=kiosk.category)
                if mi_solution.location_types.get(location_type_key) is None:
                    mi_solution.add_location_type(name=kiosk.category)

                if isinstance(kiosk_geom, shapely.Polygon):
                    mi_solution.add_area(
                        admin_id=kiosk.id,
                        name=kiosk_name,
                        polygon=kiosk_geom,
                        floor_key=floor_key,
                        location_type_key=location_type_key,
                    )
                else:
                    logger.error(f"Ignoring {kiosk}")

        if level.sections:
            for section in level.sections:
                section_name = next(iter(level.name.values()))
                section_geom = clean_shape(section.geometry)

                location_type_key = LocationType.compute_key(name=section.category)
                if mi_solution.location_types.get(location_type_key) is None:
                    mi_solution.add_location_type(name=section.category)

                if isinstance(section_geom, shapely.Polygon):
                    mi_solution.add_area(
                        admin_id=section.id,
                        name=section_name,
                        polygon=section_geom,
                        floor_key=floor_key,
                        location_type_key=location_type_key,
                    )
                else:
                    logger.error(f"Ignoring {section}")

        if level.fixtures:
            for fixture in level.fixtures:
                fixture_name = next(iter(level.name.values()))
                fixture_geom = clean_shape(fixture.geometry)

                location_type_key = LocationType.compute_key(name=fixture.category)
                if mi_solution.location_types.get(location_type_key) is None:
                    mi_solution.add_location_type(name=fixture.category)

                if isinstance(fixture_geom, shapely.Polygon):
                    mi_solution.add_area(
                        admin_id=fixture.id,
                        name=fixture_name,
                        polygon=fixture_geom,
                        floor_key=floor_key,
                        location_type_key=location_type_key,
                    )
                else:
                    logger.error(f"Ignoring {fixture}")

        if level.openings:
            for opening in level.openings:
                opening_name = next(iter(level.name.values()))
                opening_geom = dilate(clean_shape(opening.geometry))

                location_type_key = LocationType.compute_key(name=opening.category)
                if mi_solution.location_types.get(location_type_key) is None:
                    mi_solution.add_location_type(name=opening.category)

                if isinstance(opening_geom, shapely.Polygon):
                    mi_solution.add_area(
                        admin_id=opening.id,
                        name=opening_name,
                        polygon=opening_geom,
                        floor_key=floor_key,
                        location_type_key=location_type_key,
                    )
                else:
                    logger.error(f"Ignoring {opening}")

                    # opening.door

        for geofence in midf_solution.geofences:
            for building in geofence.buildings:
                ...

            for level in geofence.levels:
                ...

            geofence_name = next(iter(geofence.name.values()))

            # mi_solution.add_area(admin_id=geofence.id, name=geofence_name, polygon=geofence.geometry,
            # floor_key=floor_key)

        for relationship in midf_solution.relationships:
            ...

    area_union = shapely.convex_hull(
        shapely.unary_union([a.polygon for a in mi_solution.areas])
    )

    mi_solution.update_building(outdoor_building_admin_id, polygon=area_union)
    mi_solution.update_venue(found_venue_key, polygon=area_union)

    return mi_solution
