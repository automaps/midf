from dataclasses import dataclass

from midf.midf_typing import Lineal, MIDFFeature

__all__ = ["MIDFDetail"]


@dataclass
class MIDFDetail(MIDFFeature):
    geometry: Lineal
