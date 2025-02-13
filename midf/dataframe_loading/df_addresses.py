from typing import List, Mapping

from pandas import DataFrame

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFAddress

__all__ = ["load_imdf_addresses"]


def load_imdf_addresses(
    dataframes: Mapping[IMDFFeatureType, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFAddress]],
) -> None:
    if IMDFFeatureType.address.value in dataframes:
        for ith_row, address_row in dataframes[
            IMDFFeatureType.address.value
        ].iterrows():
            address_dict = address_row.to_dict()

            address = IMDFAddress(**address_dict)
            out[IMDFFeatureType.address].append(address)
