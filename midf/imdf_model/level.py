from typing import Any, Dict, Optional

from .other import IMDFFeature

__all__ = ["IMDFLevel"]


class IMDFLevel(IMDFFeature):
    geometry: Any  # Polygonal

    category: str = ""
    restriction: Optional[str] = None
    outdoor: bool = False
    ordinal: int = 0

    short_name: Dict[str, str] = None
    address_id: Optional[str] = None
    # building_ids: Optional[List[str]] = None
