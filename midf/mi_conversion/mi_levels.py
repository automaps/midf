import logging

from jord.shapely_utilities import clean_shape, dilate

from integration_system.model import Building, Solution
from midf.conversion import (
    ASSUME_OUTDOOR_IF_MISSING_BUILDING,
    OUTDOOR_BUILDING_NAME,
    make_mi_building_admin_id_midf,
)
from midf.mi_conversion import (
    convert_details,
    convert_fixtures,
    convert_kiosks,
    convert_openings,
    convert_sections,
    convert_units,
)
from midf.model import MIDFSolution

logger = logging.getLogger(__name__)

__all__ = ["convert_levels"]


def convert_levels(
    anchor_location_type,
    found_venue_key,
    mi_solution: Solution,
    midf_solution: MIDFSolution,
    occupant_category_mapping,
    venue_graph_key: str,
    venue_key: str,
) -> None:
    for level in midf_solution.levels:
        # level.address TODO: UNUSED ATM

        if level.buildings is None:
            if level.outdoor or ASSUME_OUTDOOR_IF_MISSING_BUILDING:
                assert found_venue_key, "Venue key not found"
                c = make_mi_building_admin_id_midf(
                    OUTDOOR_BUILDING_NAME, found_venue_key
                )
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
            a = make_mi_building_admin_id_midf(
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

        convert_units(
            anchor_location_type,
            floor_key,
            level,
            mi_solution,
            occupant_category_mapping,
        )

        convert_details(floor_key, level, mi_solution)

        convert_kiosks(floor_key, level, mi_solution)

        convert_sections(floor_key, level, mi_solution)

        convert_fixtures(floor_key, level, mi_solution)

        convert_openings(level, mi_solution, venue_graph_key, floor_key)
