import logging
from typing import Mapping

import shapely
from jord.shapely_utilities import clean_shape, dilate

from integration_system.model import (
    InvalidPolygonError,
    LocationType,
    Occupant,
    OccupantTemplate,
    OccupantType,
    Solution,
)
from midf.constants import ANCHOR_NAME
from midf.mi_utilities import clean_admin_id
from midf.model import MIDFLevel, MIDFOccupant, MIDFUnit

logger = logging.getLogger(__name__)

__all__ = ["convert_units"]


def convert_units(
    anchor_location_type: str,
    floor_key: str,
    level: MIDFLevel,
    mi_solution: Solution,
    occupant_category_mapping: Mapping,
) -> None:
    if level.units:
        for unit in level.units:
            unit: MIDFUnit

            unit_name = None
            if unit.name:
                unit_name = next(iter(unit.name.values()))

            if unit_name is None or unit_name == "":
                if unit.alt_name:
                    unit_name = next(iter(unit.alt_name.values()))

            if unit_name is None or unit_name == "":
                unit_name = unit.id

            unit_geom = clean_shape(unit.geometry)

            location_type_key = LocationType.compute_key(name=unit.category)
            if mi_solution.location_types.get(location_type_key) is None:
                mi_solution.add_location_type(name=unit.category)

            if isinstance(unit_geom, shapely.Polygon):
                if False:
                    unit_location_key = mi_solution.add_area(
                        admin_id=clean_admin_id(unit.id),
                        name=unit_name,
                        polygon=unit_geom,
                        floor_key=floor_key,
                        location_type_key=location_type_key,
                    )
                else:
                    try:
                        unit_location_key = mi_solution.add_room(
                            admin_id=clean_admin_id(unit.id),
                            name=unit_name,
                            polygon=unit_geom,
                            floor_key=floor_key,
                            location_type_key=location_type_key,
                        )
                    except InvalidPolygonError as e:
                        logger.error(f"Invalid polygon: {e}")
                        continue
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
                            admin_id=clean_admin_id(anchor.id),
                            name=ANCHOR_NAME,
                            point=anchor.geometry,
                            floor_key=floor_key,
                            location_type_key=anchor_location_type,
                        )

                    if anchor.occupants:
                        for occupant in anchor.occupants:
                            occupant: MIDFOccupant

                            occupant_name = None
                            if occupant.name:
                                occupant_name = next(iter(occupant.name.values()))

                            if occupant_name is None or occupant_name == "":
                                occupant_name = occupant.id

                            l = occupant_category_mapping.get(occupant.category)
                            if l is None:
                                logger.error(
                                    f"Occupant category {occupant.category} not found."
                                )
                                continue

                            a = OccupantTemplate.compute_key(
                                name=occupant_name,
                                occupant_category_key=l,
                            )
                            if mi_solution.occupant_templates.get(a) is None:
                                occupant_template_key = mi_solution.add_occupant_template(
                                    name=occupant_name,
                                    occupant_type=OccupantType.occupant,
                                    occupant_category_key=l,
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
