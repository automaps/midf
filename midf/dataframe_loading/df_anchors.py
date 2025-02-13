from typing import List, Mapping

from pandas import DataFrame

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFAnchor

__all__ = ["load_imdf_anchors"]


def load_imdf_anchors(
    dataframes: Mapping[IMDFFeatureType, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFAnchor]],
) -> None:
    if IMDFFeatureType.anchor.value in dataframes:
        for ith_row, anchor_row in dataframes[IMDFFeatureType.anchor.value].iterrows():
            anchor_dict = anchor_row.to_dict()

            anchor = IMDFAnchor(**anchor_dict)
            out[IMDFFeatureType.anchor].append(anchor)
