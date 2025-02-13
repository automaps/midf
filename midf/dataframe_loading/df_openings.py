import json
from typing import List, Mapping

import shapely
from pandas import DataFrame

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFOpening
from midf.midf_typing import Door

__all__ = ["load_imdf_openings"]


def load_imdf_openings(
    dataframes: Mapping[IMDFFeatureType, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFOpening]],
) -> None:
    if IMDFFeatureType.opening.value in dataframes:
        for ith_row, opening_row in dataframes[
            IMDFFeatureType.opening.value
        ].iterrows():
            opening_dict = opening_row.to_dict()

            name = opening_dict.pop("name")
            if False:
                if name is not None:
                    name = json.loads(name)

            alt_name = opening_dict.pop("alt_name")
            if False:
                if alt_name is not None:
                    alt_name = json.loads(alt_name)

            display_point = opening_dict.pop("display_point")
            if display_point is not None:
                if isinstance(display_point, dict):
                    display_point = shapely.from_geojson(json.dumps(display_point))
                else:
                    display_point = shapely.from_geojson(display_point)

            door = opening_dict.pop("door")
            if door is not None:
                door = Door(**json.loads(door))

            opening = IMDFOpening(
                **opening_dict,
                name=name,
                alt_name=alt_name,
                display_point=display_point,
                door=door,
            )
            out[IMDFFeatureType.opening].append(opening)
