from typing import Collection, Dict, Mapping

from warg.data_structures.mappings import to_dict

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFFeature, IMDFFootprint
from midf.model import MIDFFootprint

__all__ = ["link_footprints"]


def link_footprints(
    buildings, imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]]
) -> Dict[str, MIDFFootprint]:
    footprints = {}
    for footprint in imdf_dict[IMDFFeatureType.footprint]:
        footprint: IMDFFootprint
        footprints[footprint.id] = MIDFFootprint(
            id=footprint.id,
            geometry=footprint.geometry,
            name=footprint.name,
            category=footprint.category,
            buildings=(
                [buildings[b] for b in footprint.building_ids]
                if footprint.building_ids
                else None
            ),
        )
    return to_dict(footprints)
