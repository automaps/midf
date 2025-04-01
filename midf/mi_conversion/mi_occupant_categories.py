import logging
from typing import Mapping

from integration_system.model import Solution
from midf.enums import IMDFOccupantCategory

logger = logging.getLogger(__name__)

__all__ = ["convert_occupant_categories"]


def convert_occupant_categories(mi_solution: Solution) -> Mapping[str, str]:
    occupant_category_mapping = {}
    for occupant_category in IMDFOccupantCategory:
        occupant_category_mapping[occupant_category] = (
            mi_solution.add_occupant_category(occupant_category.name)
        )
    return occupant_category_mapping
