from pydantic import BaseModel
from strenum import StrEnum


class IMDFFeature(BaseModel):
    id: str  # ae095f89-49f8-4189-b5dd-9c6d62de3203


class IMDFFeatureType(StrEnum):
    address = "address"
    amenity = "amenity"
    anchor = "anchor"
    building = "building"
    detail = "detail"
    fixture = "fixture"
    footprint = "footprint"
    geofence = "geofence"
    kiosk = "kiosk"
    level = "level"
    occupant = "occupant"
    opening = "opening"
    relationship = "relationship"
    section = "section"
    unit = "unit"
    venue = "venue"
