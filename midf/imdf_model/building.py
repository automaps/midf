from typing import Mapping, Optional, Union

import shapely

from midf.imdf_model.base import IMDFFeature

__all__ = ["IMDFBuilding"]

from ..enums import BuildingCategory


class IMDFBuilding(IMDFFeature):
    category: Union[
        BuildingCategory, str
    ]  # May have invalid categories, hence the union with str
    restriction: Optional[str] = None
    name: Optional[Mapping[str, str]] = None
    alt_name: Optional[Mapping[str, str]] = None
    display_point: Optional[shapely.Point] = None
    address_id: Optional[str] = None
