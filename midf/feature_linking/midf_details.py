from collections import defaultdict
from typing import Collection, Dict, List, Mapping

from warg.data_structures.mappings import to_dict

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFDetail, IMDFFeature
from midf.model import MIDFDetail

__all__ = ["link_details"]


def link_details(
    imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]]
) -> Dict[str, List[MIDFDetail]]:
    details = defaultdict(list)
    for detail in imdf_dict[IMDFFeatureType.detail]:
        detail: IMDFDetail
        details[detail.level_id].append(
            MIDFDetail(
                id=detail.id,
                geometry=detail.geometry,
            )
        )
    return to_dict(details)
