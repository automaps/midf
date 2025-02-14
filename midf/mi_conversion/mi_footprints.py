__all__ = ["convert_footprints"]

import logging

from jord.shapely_utilities import clean_shape, dilate

logger = logging.getLogger(__name__)


def convert_footprints(building_footprint_mapping, midf_solution):
    for footprint in midf_solution.footprints:
        for building in footprint.buildings:
            building_footprint_mapping[building.id].append(footprint)
