import logging

import shapely
from jord.shapely_utilities import clean_shape, dilate

from integration_system.model import Venue
from midf.mi_utilities import make_mi_building_admin_id_midf
from midf.model import MIDFBuilding

logger = logging.getLogger(__name__)

__all__ = ["convert_buildings"]


def convert_buildings(
    address_venue_mapping,
    building_footprint_mapping,
    mi_solution,
    midf_solution,
    venue: Venue,
    venue_key: str,
) -> str:
    for building in midf_solution.buildings:
        building: MIDFBuilding

        if building.address:
            found_venue_key = next(iter(address_venue_mapping[building.address.id]))
        else:
            found_venue_key = venue_key

        building_footprint = shapely.Polygon()

        for fp in building_footprint_mapping[building.id]:
            if isinstance(fp.geometry, shapely.Polygon):
                building_footprint |= fp.geometry
            elif isinstance(fp.geometry, shapely.MultiPolygon):
                for p in fp.geometry.geoms:
                    building_footprint |= p
            else:
                logger.error(f"Ignoring {fp}")

        if building_footprint.is_empty:
            if building.display_point:
                building_footprint |= dilate(building.display_point)

        if building_footprint.is_empty:
            if venue.display_point:
                building_footprint |= dilate(venue.display_point)

        if isinstance(building_footprint, shapely.MultiPolygon):
            building_footprint = shapely.convex_hull(building_footprint)

        building_name = None
        if building.name:
            building_name = next(iter(building.name.values()))

        if building_name is None or building_name == "":
            if building.alt_name:
                building_name = next(iter(building.alt_name.values()))

        if building_name is None or building_name == "":
            building_name = building.id

        b = make_mi_building_admin_id_midf(building.id, found_venue_key)

        mi_solution.add_building(
            b,
            name=building_name,
            polygon=clean_shape(building_footprint),
            venue_key=found_venue_key,
        )
    return found_venue_key
