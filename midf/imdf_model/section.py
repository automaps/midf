from typing import Any, Mapping, Optional, Union

import shapely

from .base import IMDFFeature
from ..enums import IMDFSectionCategory

__all__ = ["IMDFSection"]


class IMDFSection(IMDFFeature):
    geometry: Any  # Polygonal

    category: Union[
        IMDFSectionCategory, str
    ]  # TODO: Some sections have a category that is not in the enum, so we allow a
    # string here, but we should validate it, it is not valid, we should raise an error. # TODO: REMOVE FOR
    #  STRICT
    restriction: Any = None
    accessibility: Any = None
    address_id: Any = None
    correlation_id: Any = None
    parents: Any = None
    level_id: str = None
    display_point: Optional[shapely.Point] = None
    alt_name: Optional[Mapping[str, str]] = None
    name: Optional[Mapping[str, str]] = None
