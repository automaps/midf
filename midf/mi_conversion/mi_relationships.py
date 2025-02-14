import logging

from jord.shapely_utilities import clean_shape, dilate

from integration_system.model import Solution
from midf.model import MIDFSolution

logger = logging.getLogger(__name__)

__all__ = ["convert_relationships"]


def convert_relationships(mi_solution: Solution, midf_solution: MIDFSolution) -> None:
    if midf_solution.relationships:
        for relationship in midf_solution.relationships:
            ...  # TODO: IMPLEMENT
