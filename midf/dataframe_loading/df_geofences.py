from typing import List, Mapping

from pandas import DataFrame

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFGeofence

__all__ = ["load_imdf_geofences"]


def load_imdf_geofences(
    dataframes: Mapping[IMDFFeatureType, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFGeofence]],
) -> None:
    if IMDFFeatureType.geofence.value in dataframes:
        for ith_row, geofence_row in dataframes[
            IMDFFeatureType.geofence.value
        ].iterrows():
            geofence_dict = geofence_row.to_dict()

            geofence = IMDFGeofence(**geofence_dict)
            out[IMDFFeatureType.geofence].append(geofence)
