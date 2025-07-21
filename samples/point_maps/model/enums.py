try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum

__all__ = ["PointConsultingFeatureStem"]


class PointConsultingFeatureStem(StrEnum):
    basemap = "basemap"
    building = "building"
    category = "categor"
    dictionary = "dictionar"
    fixture = "fixture"
    level = "level"
    occupant = "occupant"
    opening = "opening"
    point = "point"
    route = "route"
    section = "section"
    setting = "setting"
    style = "style"
    unit = "unit"
    venue = "venue"
