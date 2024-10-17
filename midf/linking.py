from collections import defaultdict
from datetime import datetime
from typing import Collection, Mapping, Union

from midf.enums import IMDFFeatureType
from midf.imdf_model import (
  IMDFAddress,
  IMDFAnchor,
  IMDFBuilding,
  IMDFDetail,
  IMDFFeature,
  IMDFFixture,
  IMDFFootprint,
  IMDFGeofence,
  IMDFKiosk,
  IMDFLevel,
  IMDFManifest,
  IMDFOccupant,
  IMDFOpening,
  IMDFRelationship,
  IMDFSection,
  IMDFUnit,
  IMDFVenue,
  )
from midf.loading import MANIFEST_KEY
from midf.model import (
  MIDFAddress,
  MIDFAnchor,
  MIDFBuilding,
  MIDFDetail,
  MIDFFixture,
  MIDFFootprint,
  MIDFGeofence,
  MIDFKiosk,
  MIDFLevel,
  MIDFManifest,
  MIDFOccupant,
  MIDFOpening,
  MIDFRelationship,
  MIDFSection,
  MIDFSolution,
  MIDFUnit,
  MIDFVenue,
  )

def parse_datetime(created):
  return (
      datetime.strptime(created, "%Y-%m-%dT%H:%M:%S.%fZ")
      if created is not None
      else None
  )

def link_imdf(
    imdf_dict: Mapping[
      Union[str, IMDFFeatureType], Collection[Union[IMDFManifest, IMDFFeature]]
    ]
    ) -> MIDFSolution:
  imdf_manifest: IMDFManifest = next(iter(imdf_dict[MANIFEST_KEY]))

  solution = MIDFSolution(
      manifest=MIDFManifest(
          version=imdf_manifest.version,
          created=parse_datetime(imdf_manifest.created),
          generated_by=imdf_manifest.generated_by,
          language=imdf_manifest.language,
          extensions=imdf_manifest.extensions,
          )
      )

  venue_mapping = defaultdict(list)

  for venue in imdf_dict[IMDFFeatureType.venue]:
    venue: IMDFVenue
    venue_mapping[venue.address_id].append(
        MIDFVenue(
            id=venue.id,
            geometry=venue.geometry,
            name=venue.name,
            category=venue.category,
            display_point=venue.display_point,
            restriction=venue.restriction,
            alt_name=venue.alt_name,
            hours=venue.hours,
            phone=venue.phone,
            website=venue.website,
            )
        )
  found_venue_addresses = venue_mapping.keys()

  addresses = {}
  for address in imdf_dict[IMDFFeatureType.address]:
    address: IMDFAddress
    assert address.id not in addresses
    addresses[address.id] = MIDFAddress(
        id=address.id,
        address=address.address,
        locality=address.locality,
        country=address.country,
        province=address.province,
        unit=address.unit,
        postal_code=address.postal_code,
        postal_code_ext=address.postal_code_ext,
        postal_code_vanity=address.postal_code_vanity,
        venues=(
            venue_mapping.pop(address.id)
            if address.id in found_venue_addresses
            else None
        ),
        )

  buildings = {}
  for building in imdf_dict[IMDFFeatureType.building]:
    building: IMDFBuilding
    buildings[building.id] = MIDFBuilding(
        id=building.id,
        category=building.category,
        name=building.name,
        alt_name=building.alt_name,
        restriction=building.restriction,
        display_point=building.display_point,
        # address=addresses[building.address_id], # TODO: INVALID IMDF!
        )

  footprints = {}
  for footprint in imdf_dict[IMDFFeatureType.footprint]:
    footprint: IMDFFootprint
    footprints[footprint.id] = MIDFFootprint(
        id=footprint.id,
        geometry=footprint.geometry,
        name=footprint.name,
        category=footprint.category,
        buildings=(
            [buildings[b] for b in footprint.building_ids]
            if footprint.building_ids
            else None
        ),
        )

  sections = defaultdict(list)
  for section in imdf_dict[IMDFFeatureType.section]:
    section: IMDFSection
    sections[section.level_id].append(
        MIDFSection(
            id=section.id,
            geometry=section.geometry,
            name=section.name,
            alt_name=section.alt_name,
            category=section.category,
            restriction=section.restriction,
            accessibility=section.accessibility,
            display_point=section.display_point,
            correlation_id=section.correlation_id,
            # address=addresses[section.address_id], # TODO: INVALID IMDF!
            )
        )
  # TODO: LINK section PARENTS...

  found_section_levels = sections.keys()

  occupants = defaultdict(list)
  for occupant in imdf_dict[IMDFFeatureType.occupant]:
    occupant: IMDFOccupant
    occupants[occupant.anchor_id].append(
        MIDFOccupant(
            id=occupant.id,
            name=occupant.name,
            category=occupant.category,
            hours=occupant.hours,
            phone=occupant.phone,
            website=occupant.website,
            validity=occupant.validity,
            correlation_id=occupant.correlation_id,
            )
        )
  found_occupant_anchors = occupants.keys()

  anchors = defaultdict(list)
  for anchor in imdf_dict[IMDFFeatureType.anchor]:
    anchor: IMDFAnchor
    anchors[anchor.unit_id].append(
        MIDFAnchor(
            id=anchor.id,
            geometry=anchor.geometry,
            # address=addresses[section.address_id], # TODO: INVALID IMDF!
            occupants=(
                occupants.pop(anchor.id)
                if anchor.id in found_occupant_anchors
                else None
            ),
            )
        )
  found_anchor_unit_ids = anchors.keys()

  anchor_id_mapping = {anchor_.id: anchor_ for a in anchors.values() for anchor_ in a}

  units = defaultdict(list)

  for unit in imdf_dict[IMDFFeatureType.unit]:
    unit: IMDFUnit
    units[unit.level_id].append(
        MIDFUnit(
            id=unit.id,
            geometry=unit.geometry,
            category=unit.category,
            name=unit.name,
            alt_name=unit.alt_name,
            restriction=unit.restriction,
            accessibility=unit.accessibility,
            anchors=(
                anchors.pop(unit.id) if unit.id in found_anchor_unit_ids else None
            ),
            )
        )
  found_unit_levels = units.keys()

  details = defaultdict(list)

  for detail in imdf_dict[IMDFFeatureType.detail]:
    detail: IMDFDetail
    details[detail.level_id].append(
        MIDFDetail(
            id=detail.id,
            geometry=detail.geometry,
            )
        )
  found_detail_levels = details.keys()

  kiosks = defaultdict(list)

  for kiosk in imdf_dict[IMDFFeatureType.kiosk]:
    kiosk: IMDFKiosk
    kiosks[kiosk.level_id].append(
        MIDFKiosk(
            id=kiosk.id,
            geometry=kiosk.geometry,
            name=kiosk.name,
            alt_name=kiosk.alt_name,
            display_point=kiosk.display_point,
            anchor=anchor_id_mapping[kiosk.anchor_id] if kiosk.anchor_id else None,
            )
        )
  found_kiosk_levels = kiosks.keys()

  fixtures = defaultdict(list)

  for fixture in imdf_dict[IMDFFeatureType.fixture]:
    fixture: IMDFFixture
    fixtures[fixture.level_id].append(
        MIDFFixture(
            id=fixture.id,
            geometry=fixture.geometry,
            category=fixture.category,
            name=fixture.name,
            alt_name=fixture.alt_name,
            anchor=(
                anchor_id_mapping[fixture.anchor_id] if fixture.anchor_id else None
            ),
            )
        )
  found_fixture_levels = fixtures.keys()

  openings = defaultdict(list)

  for opening in imdf_dict[IMDFFeatureType.opening]:
    opening: IMDFOpening
    openings[opening.level_id].append(
        MIDFOpening(
            id=opening.id,
            geometry=opening.geometry,
            category=opening.category,
            name=opening.name,
            alt_name=opening.alt_name,
            display_point=opening.display_point,
            door=opening.door,
            accessibility=opening.accessibility,
            access_control=opening.access_control,
            )
        )
  found_opening_levels = openings.keys()

  levels = {}
  for level in imdf_dict[IMDFFeatureType.level]:
    level: IMDFLevel

    building_references = (
        [buildings[b_id] for b_id in level.building_ids]
        if level.building_ids
        else None
    )

    levels[level.id] = MIDFLevel(
        id=level.id,
        geometry=level.geometry,
        category=level.category,
        outdoor=level.outdoor,
        ordinal=level.ordinal,
        name=level.name,
        short_name=level.short_name,
        restriction=level.restriction,
        # address=addresses[section.address_id], # TODO: INVALID IMDF!
        buildings=building_references,
        sections=(
            sections.pop(level.id) if level.id in found_section_levels else None
        ),
        kiosks=kiosks.pop(level.id) if level.id in found_kiosk_levels else None,
        fixtures=(
            fixtures.pop(level.id) if level.id in found_fixture_levels else None
        ),
        openings=(
            openings.pop(level.id) if level.id in found_opening_levels else None
        ),
        units=units.pop(level.id) if level.id in found_unit_levels else None,
        details=details.pop(level.id) if level.id in found_detail_levels else None,
        )

  geofences = {}
  for geofence in imdf_dict[IMDFFeatureType.geofence]:
    geofence: IMDFGeofence
    geofences[geofence.id] = MIDFGeofence(
        id=geofence.id,
        geometry=geofence.geometry,
        category=geofence.category,
        restriction=geofence.restriction,
        accessibility=geofence.accessibility,
        name=geofence.name,
        alt_name=geofence.alt_name,
        correlation_id=geofence.correlation_id,
        display_point=geofence.display_point,
        # buildings=geofence.buildings, # TODO: PARSE
        # levels=geofence.levels, # TODO: PARSE
        # parents=geofence.parents, # TODO: PARSE
        )

  relationships = []
  for relationship in imdf_dict[IMDFFeatureType.relationship]:
    relationship: IMDFRelationship
    relationships[relationship.level_id].append(
        MIDFRelationship(
            id=relationship.id,
            category=relationship.category,
            direction=relationship.direction,
            geometry=relationship.geometry,
            origin=relationship.origin,  # TODO: PARSE
            intermediary=relationship.intermediary,  # TODO: PARSE
            destination=relationship.destination,  # TODO: PARSE
            hours=relationship.hours,  # TODO: PARSE
            )
        )

  solution.addresses = list(addresses.values())
  solution.buildings = list(buildings.values())
  solution.footprints = list(footprints.values())
  solution.levels = list(levels.values())
  solution.geofences = list(geofences.values())
  solution.relationships = relationships

  return solution
