import logging

import shapely
from jord.shapely_utilities import clean_shape, dilate

from integration_system.model import DoorType, LocationType

logger = logging.getLogger(__name__)

__all__ = ["convert_openings"]


def convert_openings(level, mi_solution, venue_graph_key, floor_key) -> None:
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
