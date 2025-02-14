import logging

import shapely
from jord.shapely_utilities import clean_shape, dilate

from integration_system.model import (
    LocationType,
    Occupant,
    OccupantTemplate,
    OccupantType,
    Solution,
)
from midf.conversion import ANCHOR_NAME
from midf.model import MIDFOccupant

logger = logging.getLogger(__name__)

__all__ = ["convert_units"]


def convert_units(
    anchor_location_type,
    floor_key,
    level,
    mi_solution: Solution,
    occupant_category_mapping,
) -> None:
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
                            name=ANCHOR_NAME,
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
