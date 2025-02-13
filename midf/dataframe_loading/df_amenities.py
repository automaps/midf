from typing import List, Mapping

from pandas import DataFrame

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFAmenity

__all__ = ["load_imdf_amenities"]


def load_imdf_amenities(
    dataframes: Mapping[IMDFFeatureType, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFAmenity]],
) -> None:
    if IMDFFeatureType.amenity.value in dataframes:
        for ith_row, amenity_row in dataframes[
            IMDFFeatureType.amenity.value
        ].iterrows():
            amenity_dict = amenity_row.to_dict()

            amenity = IMDFAmenity(**amenity_dict)
            out[IMDFFeatureType.amenity].append(amenity)
