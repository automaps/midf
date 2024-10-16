from typing import Any, Dict, Optional

from .base import IMDFFeature

__all__ = ["IMDFOccupant"]

from ..enums import OccupantCategory
from ..typing import Temporality


class IMDFOccupant(IMDFFeature):
    geometry: Optional[Any] = None

    name: Dict[str, str] = {}

    category: OccupantCategory
    anchor_id: str = ""
    hours: Any = None
    phone: Any = None
    website: Any = None
    validity: Optional[Temporality] = None
    correlation_id: Any = None
