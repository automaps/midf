from typing import Any, Mapping, Optional

from .other import IMDFFeature

__all__ = ["IMDFFootprint"]


class IMDFFootprint(IMDFFeature):
    geometry: Any  # Polygonal
    category: str = ""
    name: Optional[Mapping[str, str]] = None
    # building_ids: List = ()
