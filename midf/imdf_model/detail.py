from .base import IMDFFeature

__all__ = ["IMDFDetail"]

from ..typing import Lineal


class IMDFDetail(IMDFFeature):
    level_id: str
    geometry: Lineal
