import logging

import shapely
from jord.shapely_utilities import clean_shape, dilate

from integration_system.model import LocationType
from midf.conversion import KIOSK_LOCATION_TYPE_NAME

logger = logging.getLogger(__name__)

__all__ = ["convert_kiosks"]


def convert_kiosks(floor_key, level, mi_solution):
    if level.kiosks:
        for kiosk in level.kiosks:
            kiosk_name = next(iter(level.name.values()))
            kiosk_geom = clean_shape(kiosk.geometry)

            location_type_key = LocationType.compute_key(name=KIOSK_LOCATION_TYPE_NAME)
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
