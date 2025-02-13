import json
from typing import List, Mapping

import shapely
from pandas import DataFrame

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFVenue

__all__ = ["load_imdf_venues"]


def load_imdf_venues(
    dataframes: Mapping[IMDFFeatureType, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFVenue]],
) -> None:
    if IMDFFeatureType.venue.value in dataframes:
        for ith_row, venue_row in dataframes[IMDFFeatureType.venue.value].iterrows():
            venue_dict = venue_row.to_dict()

            name = venue_dict.pop("name")
            if False:
                if name is not None:
                    name = json.loads(name)

            display_point = venue_dict.pop("display_point")
            if display_point is not None:
                if isinstance(display_point, dict):
                    display_point = shapely.from_geojson(json.dumps(display_point))
                else:
                    display_point = shapely.from_geojson(display_point)

            venue = IMDFVenue(**venue_dict, name=name, display_point=display_point)
            out[IMDFFeatureType.venue].append(venue)
