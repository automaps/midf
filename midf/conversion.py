import logging
from collections import defaultdict

import shapely
from jord.shapely_utilities import clean_shape, dilate

from integration_system.model import (
    Building,
    DoorType,
    FALLBACK_OSM_GRAPH,
    LocationType,
    Occupant,
    OccupantTemplate,
    OccupantType,
    PostalAddress,
    Solution,
    VenueType,
)
from midf.enums import IMDFOccupantCategory, IMDFVenueCategory
from midf.model import MIDFGeofence, MIDFOccupant, MIDFSolution

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
anchor_name = "Anchor"


def make_mi_building_admin_id2(building_id: str, venue_key: str) -> str:
    return f"{building_id.lower().replace(' ', '_')}_{venue_key}"


def to_mi_solution(midf_solution: MIDFSolution) -> Solution:
    mi_solution = Solution(
        external_id=f"{midf_solution.manifest.generated_by}{midf_solution.manifest.version}",
        name=midf_solution.manifest.generated_by,
        customer_id="953f7a89334a4013927857ab",
        occupants_enabled=True,
    )

    address_venue_mapping = defaultdict(list)

    venue_key = None
    for address in midf_solution.addresses:
        if address.venues:
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

    assert venue_key is not None, "No venue was found in the data"

    venue_graph_key = mi_solution.add_graph(
        graph_id=venue_key,
        osm_xml=FALLBACK_OSM_GRAPH,
        boundary=dilate(shapely.Point(0, 0)),
    )

    building_footprint_mapping = defaultdict(list)

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
            elif isinstance(fp.geometry, shapely.MultiPolygon):
                for p in fp.geometry.geoms:
                    building_footprint |= p
            else:
                logger.error(f"Ignoring {fp}")

        if building_footprint.is_empty:
            if building.display_point:
                building_footprint |= dilate(building.display_point)

        if building_footprint.is_empty:
            if venue.display_point:
                building_footprint |= dilate(venue.display_point)

        if isinstance(building_footprint, shapely.MultiPolygon):
            building_footprint = shapely.convex_hull(building_footprint)

        if building.name:
            building_name = next(iter(building.name.values()))
        else:
            building_name = "Building"

        b = make_mi_building_admin_id2(building.id, found_venue_key)

        mi_solution.add_building(
            b,
            name=building_name,
            polygon=building_footprint,
            venue_key=found_venue_key,
        )

    for level in midf_solution.levels:
        # level.address TODO: UNUSED ATM

        if level.buildings is None:
            if level.outdoor or ASSUME_OUTDOOR_IF_MISSING_BUILDING:
                assert found_venue_key, "Venue key not found"
                c = make_mi_building_admin_id2(OUTDOOR_BUILDING_NAME, found_venue_key)
                found_building = mi_solution.buildings.get(
                    Building.compute_key(admin_id=c)
                )
                if found_building is None:
                    outdoor_building_key = mi_solution.add_building(
                        c,
                        OUTDOOR_BUILDING_NAME,
                        mi_solution.venues.get(venue_key).polygon,
                        venue_key=found_venue_key,
                    )
                    found_building = mi_solution.buildings.get(outdoor_building_key)
            else:
                logger.error(f"Skipping {level}")
                continue
        else:
            a = make_mi_building_admin_id2(
                next(iter(level.buildings)).id, found_venue_key
            )
            found_building = mi_solution.buildings.get(Building.compute_key(admin_id=a))

        floor_name = next(iter(level.name.values()))
        if floor_name is None:
            floor_name = "Floor No Name Found"

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
                    if False:
                        unit_location_key = mi_solution.add_area(
                            admin_id=unit.id,
                            name=unit_name,
                            polygon=unit_geom,
                            floor_key=floor_key,
                            location_type_key=location_type_key,
                        )
                    else:
                        unit_location_key = mi_solution.add_room(
                            admin_id=unit.id,
                            name=unit_name,
                            polygon=unit_geom,
                            floor_key=floor_key,
                            location_type_key=location_type_key,
                        )
                else:
                    logger.error(f"Ignoring {unit}")
                    continue

                if unit.anchors:
                    for anchor in unit.anchors:
                        if (
                            mi_solution.occupants.get(
                                Occupant.compute_key(location_key=unit_location_key)
                            )
                            is not None
                        ):
                            anchor_key = unit_location_key
                        else:  # Location already has an occupant, add anchor as a point of interest for the occupant to
                            # occupy
                            anchor_key = mi_solution.add_point_of_interest(
                                admin_id=anchor.id,
                                name=anchor_name,
                                point=anchor.geometry,
                                floor_key=floor_key,
                                location_type_key=anchor_location_type,
                            )

                        if anchor.occupants:
                            for occupant in anchor.occupants:
                                occupant: MIDFOccupant
                                occupant_name = next(iter(occupant.name.values()))

                                a = OccupantTemplate.compute_key(
                                    name=occupant_name,
                                    occupant_category_key=occupant_category_mapping[
                                        occupant.category
                                    ],
                                )
                                if mi_solution.occupant_templates.get(a) is None:
                                    occupant_template_key = mi_solution.add_occupant_template(
                                        name=occupant_name,
                                        occupant_type=OccupantType.occupant,
                                        occupant_category_key=occupant_category_mapping[
                                            occupant.category
                                        ],
                                        description=f"{occupant.hours} {occupant.phone} {occupant.website}",
                                        # business_hours=occupant.hours, # TODO: CONVERT?
                                        # contact=occupant.phone + occupant.website,
                                    )
                                else:
                                    occupant_template_key = a

                                mi_solution.add_occupant(
                                    location_key=anchor_key,
                                    occupant_template_key=occupant_template_key,
                                )

        if level.details:
            for detail in level.details:
                detail_name = next(iter(level.name.values()))
                detail_geom = dilate(clean_shape(detail.geometry))

                location_type_key = LocationType.compute_key(
                    name=DETAIL_LOCATION_TYPE_NAME
                )
                if mi_solution.location_types.get(location_type_key) is None:
                    mi_solution.add_location_type(name=DETAIL_LOCATION_TYPE_NAME)

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

                location_type_key = LocationType.compute_key(
                    name=KIOSK_LOCATION_TYPE_NAME
                )
                if mi_solution.location_types.get(location_type_key) is None:
                    mi_solution.add_location_type(name=KIOSK_LOCATION_TYPE_NAME)

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
                if False:
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
                else:
                    mi_solution.add_door(
                        admin_id=opening.id,
                        floor_index=level.ordinal,
                        graph_key=venue_graph_key,
                        linestring=opening.geometry,
                        door_type=DoorType.door,
                    )

                    # opening.door

    if midf_solution.geofences:
        for geofence in midf_solution.geofences:
            geofence: MIDFGeofence

            ltk = LocationType.compute_key(name=geofence.category)
            if mi_solution.location_types.get(ltk) is None:
                ltk = mi_solution.add_location_type(name=geofence.category)

            if geofence.buildings:
                for building in geofence.buildings:
                    ...
            if geofence.levels:
                for level in geofence.levels:
                    ...
            if geofence.parents:
                for parent in geofence.parents:
                    ...

            geofence_name = None
            if geofence.name:
                geofence_name = next(iter(geofence.name.values()))
            else:
                if geofence.alt_name:
                    geofence_name = next(iter(geofence.alt_name.values()))
                if geofence_name is None:
                    geofence_name = geofence.category

            blk = Building.compute_key(
                admin_id=make_mi_building_admin_id2(
                    OUTDOOR_BUILDING_NAME, found_venue_key
                )
            )

            floor_key = None
            for floor in mi_solution.floors:
                if floor.building.key == blk:
                    floor_key = floor.key
                    break

            if floor_key is None:  # TODO: FIX, bad assumption
                logger.error(f"Floor not found for {geofence}")
                floor_key = next(iter(mi_solution.floors)).key

            gid = geofence.id  # + found_venue_key
            mi_solution.add_area(
                admin_id=gid,
                name=geofence_name,
                polygon=geofence.geometry,
                floor_key=floor_key,
                location_type_key=ltk,
            )

    if midf_solution.relationships:
        for relationship in midf_solution.relationships:
            ...  # TODO: IMPLEMENT

    solution_locations_union = shapely.convex_hull(
        shapely.unary_union(
            [a.polygon for a in mi_solution.areas]
            + [r.polygon for r in mi_solution.rooms]
            + [r.point for r in mi_solution.points_of_interest]
        )
    )

    blk = make_mi_building_admin_id2(OUTDOOR_BUILDING_NAME, found_venue_key)
    if mi_solution.buildings.get(Building.compute_key(admin_id=blk)) is not None:
        mi_solution.update_building(blk, polygon=solution_locations_union)

    mi_solution.update_graph(venue_graph_key, boundary=solution_locations_union)

    mi_solution.update_venue(
        found_venue_key, polygon=solution_locations_union, graph_key=venue_graph_key
    )

    return mi_solution
