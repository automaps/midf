from typing import List, Mapping

from pandas import DataFrame

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFKiosk

__all__ = ["load_imdf_kiosks"]


def load_imdf_kiosks(
    dataframes: Mapping[IMDFFeatureType, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFKiosk]],
) -> None:
    if IMDFFeatureType.kiosk.value in dataframes:
        for ith_row, kiosk_row in dataframes[IMDFFeatureType.kiosk.value].iterrows():
            kiosk_dict = kiosk_row.to_dict()

            kiosk = IMDFKiosk(**kiosk_dict)
            out[IMDFFeatureType.kiosk].append(kiosk)
