from collections import defaultdict
from typing import Any, Collection, Dict, List, Mapping

from warg.data_structures.mappings import to_dict

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFFeature, IMDFUnit
from midf.model import MIDFUnit

__all__ = ["link_units"]

import logging

logger = logging.getLogger(__name__)


def link_units(
    anchors: Dict[str, Any],
    imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]],
) -> Dict[str, List[MIDFUnit]]:
    units = defaultdict(list)
    logger.error(f"Linking units {len(imdf_dict[IMDFFeatureType.unit])}")
    found_anchor_unit_ids = anchors.keys()

    anchors_copy = anchors.copy()

    for unit in imdf_dict[IMDFFeatureType.unit]:
        unit: IMDFUnit
        units[unit.level_id].append(
            MIDFUnit(
                id=unit.id,
                geometry=unit.geometry,
                category=unit.category,
                name=unit.name,
                alt_name=unit.alt_name,
                restriction=unit.restriction,
                accessibility=unit.accessibility,
                anchors=(
                    anchors_copy.pop(unit.id)
                    if unit.id in found_anchor_unit_ids
                    else None
                ),
            )
        )
    return to_dict(units)
