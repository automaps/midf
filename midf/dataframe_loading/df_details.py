from typing import List, Mapping

from pandas import DataFrame

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFDetail

__all__ = ["load_imdf_details"]


def load_imdf_details(
    dataframes: Mapping[IMDFFeatureType, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFDetail]],
) -> None:
    if IMDFFeatureType.detail.value in dataframes:
        for ith_row, detail_row in dataframes[IMDFFeatureType.detail.value].iterrows():
            detail_dict = detail_row.to_dict()

            detail = IMDFDetail(**detail_dict)
            out[IMDFFeatureType.detail].append(detail)
