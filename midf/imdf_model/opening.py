from typing import Mapping, Optional, Union

import shapely
from attr import dataclass
from strenum import StrEnum

from .base import IMDFFeature
from ..enums import (
    IMDFAccessControlCategory,
    IMDFAccessibilityCategory,
    IMDFDoorCategory,
    IMDFDoorMaterial,
    IMDFOpeningCategory,
)

__all__ = ["IMDFOpening", "IMDFDirection", "IMDFDoor"]


class IMDFDirection(StrEnum):
    directed = "directed"
    undirected = "undirected"


@dataclass
class IMDFDoor:
    type: Optional[IMDFDoorCategory] = None
    automatic: Optional[bool] = None
    material: Optional[IMDFDoorMaterial] = None


class IMDFOpening(IMDFFeature):
    geometry: shapely.LineString
    category: Union[
        IMDFOpeningCategory, str
    ]  # TODO: Some openings have a category that is not in the enum, so we allow a
    # string here, but we should validate it, it is not valid, we should raise an error. # TODO: REMOVE FOR
    #  STRICT
    level_id: str

    accessibility: Optional[IMDFAccessibilityCategory] = None
    access_control: Optional[IMDFAccessControlCategory] = None
    door: Optional[IMDFDoor] = None
    name: Optional[Mapping[str, str]] = None
    alt_name: Optional[Mapping[str, str]] = None
    display_point: Optional[shapely.Point] = None
