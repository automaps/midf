import json
from typing import List, Mapping

from pandas import DataFrame

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFFootprint

__all__ = ["load_imdf_footprints"]


def load_imdf_footprints(
    dataframes: Mapping[IMDFFeatureType, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFFootprint]],
) -> None:
    if IMDFFeatureType.footprint.value in dataframes:
        for ith_row, footprint_row in dataframes[
            IMDFFeatureType.footprint.value
        ].iterrows():
            footprint_dict = footprint_row.to_dict()

            name = footprint_dict.pop("name")
            if False:
                if name is not None:
                    name = json.loads(name)

            footprint = IMDFFootprint(**footprint_dict, name=name)
            out[IMDFFeatureType.footprint].append(footprint)
