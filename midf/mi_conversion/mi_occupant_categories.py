import logging
from typing import Mapping

from jord.shapely_utilities import clean_shape, dilate

from midf.enums import IMDFOccupantCategory

logger = logging.getLogger(__name__)

__all__ = ["convert_occupant_categories"]


def convert_occupant_categories(mi_solution) -> Mapping[str, str]:
    occupant_category_mapping = {}
    for occupant_category in IMDFOccupantCategory:
        occupant_category_mapping[occupant_category] = (
            mi_solution.add_occupant_category(occupant_category.name)
        )
    return occupant_category_mapping
