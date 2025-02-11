from typing import Any, Dict, Optional, Union

from .base import IMDFFeature

__all__ = ["IMDFOccupant"]

from ..enums import IMDFOccupantCategory
from ..midf_typing import Temporality


class IMDFOccupant(IMDFFeature):
    geometry: Optional[Any] = None

    name: Dict[str, str] = {}

    category: Union[
        IMDFOccupantCategory, str
    ]  # TODO: Some occupants have a category that is not in the enum, so we allow a
    # string here, but we should validate it, it is not valid, we should raise an error.
    anchor_id: str = ""
    hours: Any = None
    phone: Any = None
    website: Any = None
    validity: Optional[Temporality] = None
    correlation_id: Any = None
