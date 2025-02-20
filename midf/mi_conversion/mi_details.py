import logging

import shapely
from jord.shapely_utilities import clean_shape, dilate

from integration_system.model import LocationType
from midf.constants import DETAIL_LOCATION_TYPE_NAME
from midf.mi_utilities import clean_admin_id
from midf.model import MIDFDetail

logger = logging.getLogger(__name__)

__all__ = ["convert_details"]


def convert_details(floor_key, level, mi_solution):
    if level.details:
        for detail in level.details:
            detail: MIDFDetail

            detail_name = detail.id

            detail_geom = dilate(clean_shape(detail.geometry))

            location_type_key = LocationType.compute_key(name=DETAIL_LOCATION_TYPE_NAME)
            if mi_solution.location_types.get(location_type_key) is None:
                mi_solution.add_location_type(name=DETAIL_LOCATION_TYPE_NAME)

            if isinstance(detail_geom, shapely.Polygon):
                mi_solution.add_area(
                    admin_id=clean_admin_id(detail.id),
                    name=detail_name,
                    polygon=detail_geom,
                    floor_key=floor_key,
                    location_type_key=location_type_key,
                )
            else:
                logger.error(f"Ignoring {detail}")
