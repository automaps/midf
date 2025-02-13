from collections import defaultdict
from typing import Collection, Dict, List, Mapping

from warg.data_structures.mappings import to_dict

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFAnchor, IMDFFeature
from midf.model import MIDFAnchor

__all__ = ["link_anchors"]


def link_anchors(
    found_occupant_anchors,
    imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]],
    occupants,
) -> Dict[str, List[MIDFAnchor]]:
    anchors = defaultdict(list)
    for anchor in imdf_dict[IMDFFeatureType.anchor]:
        anchor: IMDFAnchor
        anchors[anchor.unit_id].append(
            MIDFAnchor(
                id=anchor.id,
                geometry=anchor.geometry,
                # address=addresses[section.address_id], # TODO: INVALID IMDF!
                occupants=(
                    occupants.pop(anchor.id)
                    if anchor.id in found_occupant_anchors
                    else None
                ),
            )
        )
    return to_dict(anchors)
