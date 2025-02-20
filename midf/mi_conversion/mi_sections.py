import logging

import shapely
from jord.shapely_utilities import clean_shape, dilate

from integration_system.model import LocationType
from midf.mi_utilities import clean_admin_id
from midf.model import MIDFSection

logger = logging.getLogger(__name__)

__all__ = ["convert_sections"]


def convert_sections(floor_key, level, mi_solution) -> None:
    if level.sections:
        for section in level.sections:
            section: MIDFSection

            section_name = None
            if section.name:
                section_name = next(iter(section.name.values()))

            if section_name is None or section_name == "":
                if section.alt_name:
                    section_name = next(iter(section.alt_name.values()))

            if section_name is None or section_name == "":
                section_name = section.id

            section_geom = clean_shape(section.geometry)

            location_type_key = LocationType.compute_key(name=section.category)
            if mi_solution.location_types.get(location_type_key) is None:
                mi_solution.add_location_type(name=section.category)

            if isinstance(section_geom, shapely.Polygon):
                mi_solution.add_area(
                    admin_id=clean_admin_id(section.id),
                    name=section_name,
                    polygon=section_geom,
                    floor_key=floor_key,
                    location_type_key=location_type_key,
                )
            else:
                logger.error(f"Ignoring {section}")
