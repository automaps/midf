from typing import Any, Dict, List, Optional, Union

from .base import IMDFFeature

__all__ = ["IMDFLevel"]

from ..enums import IMDFLevelCategory


class IMDFLevel(IMDFFeature):
    geometry: Any  # Polygonal

    category: Union[
        IMDFLevelCategory, str
    ]  # TODO: Some levels have a category that is not in the enum, so we allow a
    # string here, but we should validate it, it is not valid, we should raise an error.
    restriction: Optional[str] = None
    outdoor: bool = False
    ordinal: int = 0

    display_point: Optional[Any] = None

    name: dict[str, str]
    short_name: Dict[str, str] = None
    address_id: Optional[str] = None
    building_ids: Optional[List[str]] = None
