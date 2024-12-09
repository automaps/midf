from attr import dataclass

from midf.typing import Lineal, MIDFFeature

__all__ = ["MIDFDetail"]


@dataclass
class MIDFDetail(MIDFFeature):
    geometry: Lineal
