from dataclasses import dataclass, field
from enum import StrEnum
from typing import Dict, List, Optional, Union

from geojson import MultiPolygon, Point, Polygon

from model.base import IMDFFeature, NamedFeatureProperties

Polygonal = Union[Polygon, MultiPolygon]

Hours = str
Phone = str
Website = str
ISO3166 = str
ISO3166_2 = str

FeatureId = str
AddressId = str
AmenityId = str
AnchorId = str
BuildingId = str
DetailId = str
FixtureId = str
FootprintId = str
GeofenceId = str
KioskId = str
LevelId = str
OccupantId = str
OpeningId = str
RelationshipId = str
SectionId = str
UnitId = str
VenueId = str

Labels = Dict[str, str]


@dataclass
class LabeledFeatureProperties(NamedFeatureProperties):
  level_id: LevelId
  display_point: Optional[Point]


class FeatureType(StrEnum):
  ADDRESS = "address"
  AMENITY = "amenity"
  ANCHOR = "anchor"
  BUILDING = "building"
  DETAIL = "detail"
  FIXTURE = "fixture"
  FOOTPRINT = "footprint"
  GEOFENCE = "geofence"
  KIOSK = "kiosk"
  LEVEL = "level"
  OCCUPANT = "occupant"
  OPENING = "opening"
  RELATIONSHIP = "relationship"
  SECTION = "section"
  UNIT = "unit"
  VENUE = "venue"


@dataclass
class Temporality:
  start: str
  end: str
  modified: str


@dataclass
class BuildingProperties(NamedFeatureProperties):
  category: str
  restriction: str
  address_id: Optional[AddressId] = None


@dataclass
class Fixture(IMDFFeature):
  id: FixtureId

  geometry: Polygonal
  properties: LabeledFeatureProperties = field(default_factory=lambda: {
    "category": "",
    "anchor_id": None
  })
  feature_type: FeatureType = FeatureType.FIXTURE


@dataclass
class KioskProperties(NamedFeatureProperties):
  anchorId: Optional[AnchorId] = None
  levelId: Optional[LevelId] = None


@dataclass
class LevelProperties(NamedFeatureProperties):
  category: str
  restriction: Optional[str]
  outdoor: bool = False
  ordinal: int = 0
  short_name: Labels = field(default_factory=dict)
  address_id: Optional[AddressId] = None
  building_ids: Optional[List[BuildingId]] = None


@dataclass
class UnitProperties(LabeledFeatureProperties):
  category: str
  restriction: Optional[str] = None
  accessibility: Optional[str] = None


# Enums
class ACCESS_CONTROL_CATEGORY(StrEnum):
  BADGEREADER = "badgereader"
  FINGERPRINTREADER = "fingerprintreader"
  GUARD = "guard"
  KEYACCESS = "keyaccess"
  OUTOFSERVICE = "outofservice"
  PASSWORDACCESS = "passwordaccess"
  RETINASCANNER = "retinascanner"
  VOICERECOGNITION = "voicerecognition"


class ACCESSIBILITY_CATEGORY(StrEnum):
  ASSISTED_LISTENING = "assisted.listening"
  BRAILLE = "braille"
  HEARING = "hearing"
  HEARINGLOOP = "hearingloop"
  SIGNLANGINTERPRETER = "signlanginterpreter"
  TACTILEPAVING = "tactilepaving"
  TDD = "tdd"
  TRS = "trs"
  VOLUME = "volume"
  WHEELCHAIR = "wheelchair"


class AMENITY_CATEGORY(StrEnum):
  ...
  # ... (all enum values from the TypeScript code)


class BUILDING_CATEGORY(StrEnum):
  PARKING = "parking"
  TRANSIT = "transit"
  TRANSIT_BUS = "transit.bus"
  TRANSIT_TRAIN = "transit.train"
  UNSPECIFIED = "unspecified"


class DOOR_CATEGORY(StrEnum):
  DOOR = "door"
  MOVABLEPARTITION = "movablepartition"
  OPEN = "open"
  REVOLVING = "revolving"
  SHUTTER = "shutter"
  SLIDING = "sliding"
  SWINGING = "swinging"
  TURNSTILE = "turnstile"
  TURNSTILE_FULLHEIGHT = "turnstile.fullheight"
  TURNSTILE_WAISTHEIGHT = "turnstile.waistheight"
  UNSPECIFIED = "unspecified"


class DOOR_TYPE(StrEnum):
  MOVABLEPARTITION = "movablepartition"
  OPEN = "open"
  REVOLVING = "revolving"
  SHUTTER = "shutter"
  SLIDING = "sliding"
  SWINGING = "swinging"
  TURNSTILE = "turnstile"
  TURNSTILE_FULLHEIGHT = "turnstile.fullheight"
  TURNSTILE_WAISTHEIGHT = "turnstile.waistheight"


class FIXTURE_CATEGORY(StrEnum):
  BAGGAGECAROUSEL = "baggagecarousel"
  BOARDINGGATE_DESK = "boardinggate.desk"
  CHECKIN_DESK = "checkin.desk"
  CHECKIN_KIOSK = "checkin.kiosk"
  DESK = "desk"
  EQUIPMENT = "equipment"
  FURNITURE = "furniture"
  IMMIGRATION_DESK = "immigration.desk"
  INSPECTION_DESK = "inspection.desk"
  OBSTRUCTION = "obstruction"
  SECURITYEQUIPMENT = "securityequipment"
  STAGE = "stage"
  VEGETATION = "vegetation"
  WALL = "wall"


class FOOTPRINT_CATEGORY(StrEnum):
  AERIAL = "aerial"
  GROUND = "ground"
  SUBTERRANEAN = "subterranean"


class GEOFENCE_CATEGORY(StrEnum):
  CONCOURSE = "concourse"
  GEOFENCE = "geofence"
  PAIDAREA = "paidarea"
  PLATFORM = "platform"
  POSTSECURITY = "postsecurity"
  PRESECURITY = "presecurity"
  TERMINAL = "terminal"
  UNDERCONSTRUCTION = "underconstruction"


class LEVEL_CATEGORY(StrEnum):
  ARRIVALS = "arrivals"
  ARRIVALS_DOMESTIC = "arrivals.domestic"
  ARRIVALS_INTL = "arrivals.intl"
  DEPARTURES = "departures"
  DEPARTURES_DOMESTIC = "departures.domestic"
  DEPARTURES_INTL = "departures.intl"
  PARKING = "parking"
  TRANSIT = "transit"
  UNSPECIFIED = "unspecified"


class OCCUPANT_CATEGORY(StrEnum):
  ...
  # ... (all enum values from the TypeScript code)


class OPENING_CATEGORY(StrEnum):
  AUTOMOBILE = "automobile"
  BICYCLE = "bicycle"
  EMERGENCYEXIT = "emergencyexit"
  PEDESTRIAN = "pedestrian"
  PEDESTRIAN_PRINCIPAL = "pedestrian.principal"
  PEDESTRIAN_TRANSIT = "pedestrian.transit"
  SERVICE = "service"


class RELATIONSHIP_CATEGORY(StrEnum):
  ELEVATOR = "elevator"
  ESCALATOR = "escalator"
  MOVINGWALKWAY = "movingwalkway"
  RAMP = "ramp"
  STAIRS = "stairs"
  TRAVERSAL = "traversal"
  TRAVERSAL_PATH = "traversal.path"


class RESTRICTION_CATEGORY(StrEnum):
  EMPLOYEESONLY = "employeesonly"
  RESTRICTED = "restricted"


class SECTION_CATEGORY(StrEnum):
  ...
  # ... (all enum values from the TypeScript code)


class UNIT_CATEGORY(StrEnum):
  ...
  # ... (all enum values from the TypeScript code)


class VENUE_CATEGORY(StrEnum):
  AIRPORT = "airport"
  AIRPORT_INTL = "airport.intl"
  AQUARIUM = "aquarium"
  BUSINESSCAMPUS = "businesscampus"
  CASINO = "casino"
  COMMUNITYCENTER = "communitycenter"
  CONVENTIONCENTER = "conventioncenter"
  GOVERNMENTFACILITY = "governmentfacility"
  HEALTHCAREFACILITY = "healthcarefacility"
  HOTEL = "hotel"
  MUSEUM = "museum"
  PARKINGFACILITY = "parkingfacility"
  RESORT = "resort"
  RETAILSTORE = "retailstore"
  SHOPPINGCENTER = "shoppingcenter"
  STADIUM = "stadium"
  STRIPMALL = "stripmall"
  THEATER = "theater"
  THEMEPARK = "themepark"
  TRAINSTATION = "trainstation"
  TRANSITSTATION = "transitstation"
  UNIVERSITY = "university"
