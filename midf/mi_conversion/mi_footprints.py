__all__ = ["convert_footprints"]

import logging

from jord.shapely_utilities import clean_shape, dilate

from midf.model import MIDFBuilding, MIDFFootprint

logger = logging.getLogger(__name__)


def convert_footprints(building_footprint_mapping, midf_solution) -> None:
    for footprint in midf_solution.footprints:
        footprint: MIDFFootprint
        for building in footprint.buildings:
            building: MIDFBuilding
            building_footprint_mapping[building.id].append(footprint)
