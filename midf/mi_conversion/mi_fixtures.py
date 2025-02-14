import logging

import shapely
from jord.shapely_utilities import clean_shape, dilate

from integration_system.model import LocationType

logger = logging.getLogger(__name__)

__all__ = ["convert_fixtures"]


def convert_fixtures(floor_key, level, mi_solution) -> None:
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
