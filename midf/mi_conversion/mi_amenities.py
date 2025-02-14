from integration_system.model import LocationType, Room, Solution
from midf.model import MIDFSolution

__all__ = ["convert_amenities"]

import logging
from jord.shapely_utilities import clean_shape, dilate

logger = logging.getLogger(__name__)


def convert_amenities(mi_solution: Solution, midf_solution: MIDFSolution) -> None:
    if midf_solution.amenities:
        for amenity in midf_solution.amenities:
            for unit in amenity.units:
                amenity_name = next(iter(amenity.name.values()))
                amenity_category_key = LocationType.compute_key(name=amenity.category)
                if mi_solution.location_types.get(amenity_category_key) is None:
                    mi_solution.add_location_type(name=amenity.category)

                ref_unit_floor_key = mi_solution.rooms.get(
                    Room.compute_key(admin_id=unit.id)
                ).floor.key

                mi_solution.add_point_of_interest(
                    admin_id=amenity.id,
                    name=amenity_name,
                    point=amenity.geometry,
                    location_type_key=amenity_category_key,
                    floor_key=ref_unit_floor_key,
                    description=f"{amenity.hours} {amenity.phone} {amenity.website} {amenity.accessibility} "
                    f"{amenity.alt_name} {amenity.correlation_id} {amenity.address}",
                )
