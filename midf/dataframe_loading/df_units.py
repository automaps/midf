import json
import uuid
from typing import List, Mapping

import shapely
from pandas import DataFrame

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFUnit
from midf.loading import logger

__all__ = ["load_imdf_units"]


def load_imdf_units(
    dataframes: Mapping[IMDFFeatureType, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFUnit]],
) -> None:
    if IMDFFeatureType.unit.value in dataframes:
        for ith_row, unit_row in dataframes[IMDFFeatureType.unit.value].iterrows():
            unit_dict = unit_row.to_dict()

            name = unit_dict.pop("name")
            if False:
                if name is not None:
                    name = json.loads(name)

            alt_name = unit_dict.pop("alt_name")
            if False:
                if alt_name is not None:
                    alt_name = json.loads(alt_name)

            unit_id = unit_dict.pop("id")
            if True:
                if unit_id is not None:
                    ...
                    # unit_id = str(unit_id)
                else:
                    logger.error(
                        f"unit_id is None, generating a new one"
                        # f"{unit_row}"
                    )
                    unit_id = uuid.uuid4().hex

            display_point = unit_dict.pop("display_point")
            if display_point is not None:
                if isinstance(display_point, dict):
                    display_point = shapely.from_geojson(json.dumps(display_point))
                else:
                    display_point = shapely.from_geojson(display_point)

            unit = IMDFUnit(
                **unit_dict,
                id=unit_id,
                name=name,
                alt_name=alt_name,
                display_point=display_point,
            )
            out[IMDFFeatureType.unit].append(unit)
