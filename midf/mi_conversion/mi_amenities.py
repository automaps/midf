from integration_system.model import LocationType, PointOfInterest, Room, Solution
from midf.mi_utilities import clean_admin_id
from midf.model import MIDFAmenity, MIDFSolution

__all__ = ["convert_amenities"]

import logging
from jord.shapely_utilities import clean_shape, dilate

logger = logging.getLogger(__name__)


def convert_amenities(mi_solution: Solution, midf_solution: MIDFSolution) -> None:
    if midf_solution.amenities:
        for amenity in midf_solution.amenities:
            amenity: MIDFAmenity

            amenity_name = None
            if amenity.name:
                amenity_name = next(iter(amenity.name.values()))

            if amenity_name is None or amenity_name == "":
                if amenity.alt_name:
                    amenity_name = next(iter(amenity.alt_name.values()))

            if amenity_name is None or amenity_name == "":
                amenity_name = amenity.id

            amenity_category_key = LocationType.compute_key(admin_id=amenity.category)
            if mi_solution.location_types.get(amenity_category_key) is None:
                mi_solution.add_location_type(
                    admin_id=amenity.category, name=amenity.category
                )

            for unit in amenity.units:
                ref_unit = mi_solution.rooms.get(
                    Room.compute_key(admin_id=clean_admin_id(unit.id))
                )

                if ref_unit is None:
                    logger.warning(f"Unit {unit.id} not found in the solution.")
                    continue

                admin_id = clean_admin_id(amenity.id)

                if (
                    mi_solution.points_of_interest.get(
                        PointOfInterest.compute_key(admin_id=admin_id)
                    )
                    is not None
                ):
                    logger.warning(f"Point of interest {admin_id} already exists.")
                    continue

                mi_solution.add_point_of_interest(
                    admin_id=admin_id,
                    name=amenity_name,
                    point=amenity.geometry,
                    location_type_key=amenity_category_key,
                    floor_key=ref_unit.floor.key,
                    description=f"{amenity.hours} {amenity.phone} {amenity.website} {amenity.accessibility} "
                    f"{amenity.alt_name} {amenity.correlation_id} {amenity.address}",
                )
