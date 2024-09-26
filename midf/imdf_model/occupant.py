from typing import Any, Dict, Optional

from .other import IMDFFeature

__all__ = ["IMDFOccupant"]


class IMDFOccupant(IMDFFeature):
    geometry: Optional[Any] = None

    name: Dict[str, str] = {}

    category: str = ""
    anchor_id: str = ""
    hours: Any = None
    phone: Any = None
    website: Any = None
    validity: Any = None
    correlation_id: Any = None
