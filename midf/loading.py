import json
import logging
import uuid
from collections import defaultdict
from pathlib import Path
from typing import Collection, List, Union

import shapely

from midf.enums import IMDFFeatureType
from midf.imdf_model import (
    IMDFAddress,
    IMDFAmenity,
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
from .midf_typing import Door, Temporality

logger = logging.getLogger(__name__)

__all__ = ["load_imdf", "MANIFEST_KEY"]

MANIFEST_KEY = "manifest"


def load_imdf(
    imdf_file_path: Path,
) -> dict[str, Union[IMDFManifest, Collection[IMDFFeature]]]:
    from zipfile import ZipFile
    import geopandas

    assert imdf_file_path.exists()
    assert imdf_file_path.is_file()
    assert imdf_file_path.suffix == ".zip"

    dataframes = {}
    manifest = None

    with ZipFile(imdf_file_path) as zf:
        for file in zf.namelist():
            z_file_path = Path(file)
            if z_file_path.suffix == ".geojson":  # optional filtering by filetype
                with zf.open(file) as f:
                    df = geopandas.read_file(f, engine="fiona")
                    feature_name = z_file_path.stem
                    dataframes[feature_name] = df

            elif z_file_path.suffix == ".json":
                with zf.open(file) as f:
                    assert manifest is None
                    manifest = IMDFManifest(**json.loads(f.read()))

            else:
                logger.error(f"{file} was skipped")

    out = defaultdict(list)
    if manifest is not None:
        out[MANIFEST_KEY].append(manifest)

    if IMDFFeatureType.venue.value in dataframes:
        for ith_row, venue_row in dataframes[IMDFFeatureType.venue.value].iterrows():
            venue_dict = venue_row.to_dict()

            name = venue_dict.pop("name")
            if False:
                if name is not None:
                    name = json.loads(name)

            display_point = venue_dict.pop("display_point")
            if display_point is not None:
                if isinstance(display_point, dict):
                    display_point = shapely.from_geojson(json.dumps(display_point))
                else:
                    display_point = shapely.from_geojson(display_point)

            venue = IMDFVenue(**venue_dict, name=name, display_point=display_point)
            out[IMDFFeatureType.venue].append(venue)

    if IMDFFeatureType.building.value in dataframes:
        for ith_row, building_row in dataframes[
            IMDFFeatureType.building.value
        ].iterrows():
            building_dict = building_row.to_dict()

            name = building_dict.pop("name")
            if False:
                if name is not None:
                    name = json.loads(name)

            alt_name = building_dict.pop("alt_name")
            if False:
                if alt_name is not None:
                    alt_name = json.loads(alt_name)

            display_point = building_dict.pop("display_point")
            if display_point is not None:
                if isinstance(display_point, dict):
                    display_point = shapely.from_geojson(json.dumps(display_point))
                else:
                    display_point = shapely.from_geojson(display_point)

            building = IMDFBuilding(
                **building_dict,
                name=name,
                alt_name=alt_name,
                display_point=display_point,
            )

            out[IMDFFeatureType.building].append(building)

    if IMDFFeatureType.footprint.value in dataframes:
        for ith_row, footprint_row in dataframes[
            IMDFFeatureType.footprint.value
        ].iterrows():
            footprint_dict = footprint_row.to_dict()

            name = footprint_dict.pop("name")
            if False:
                if name is not None:
                    name = json.loads(name)

            footprint = IMDFFootprint(**footprint_dict, name=name)
            out[IMDFFeatureType.footprint].append(footprint)

    if IMDFFeatureType.fixture.value in dataframes:
        for ith_row, fixture_row in dataframes[
            IMDFFeatureType.fixture.value
        ].iterrows():
            fixture_dict = fixture_row.to_dict()

            name = fixture_dict.pop("name")
            if False:
                if name is not None:
                    name = json.loads(name)

            alt_name = fixture_dict.pop("alt_name")
            if False:
                if alt_name is not None:
                    alt_name = json.loads(alt_name)

            fixture_id = fixture_dict.pop("id")
            if True:
                if fixture_id is not None:
                    ...
                    # fixture_id = str(fixture_id)
                else:
                    logger.error(
                        f"fixture_id is None, generating a new one"
                        # f"{fixture_row}"
                    )
                    fixture_id = uuid.uuid4().hex

            display_point = fixture_dict.pop("display_point")
            if display_point is not None:
                if isinstance(display_point, dict):
                    display_point = shapely.from_geojson(json.dumps(display_point))
                else:
                    display_point = shapely.from_geojson(display_point)

            fixture = IMDFFixture(
                **fixture_dict,
                id=fixture_id,
                name=name,
                alt_name=alt_name,
                display_point=display_point,
            )

            out[IMDFFeatureType.fixture].append(fixture)

    if IMDFFeatureType.unit.value in dataframes:
        for ith_row, unit_row in dataframes[IMDFFeatureType.unit.value].iterrows():
            unit_dict = unit_row.to_dict()

            name = unit_dict.pop("name")
            if False:
                if name is not None:
                    name = json.loads(name)

            alt_name = unit_dict.pop("alt_name")
            if False:
                if alt_name is not None:
                    alt_name = json.loads(alt_name)

            unit_id = unit_dict.pop("id")
            if True:
                if unit_id is not None:
                    ...
                    # unit_id = str(unit_id)
                else:
                    logger.error(
                        f"unit_id is None, generating a new one"
                        # f"{unit_row}"
                    )
                    unit_id = uuid.uuid4().hex

            display_point = unit_dict.pop("display_point")
            if display_point is not None:
                if isinstance(display_point, dict):
                    display_point = shapely.from_geojson(json.dumps(display_point))
                else:
                    display_point = shapely.from_geojson(display_point)

            unit = IMDFUnit(
                **unit_dict,
                id=unit_id,
                name=name,
                alt_name=alt_name,
                display_point=display_point,
            )
            out[IMDFFeatureType.unit].append(unit)

    if IMDFFeatureType.level.value in dataframes:
        for ith_row, level_row in dataframes[IMDFFeatureType.level.value].iterrows():
            level_dict = level_row.to_dict()

            name = level_dict.pop("name")
            if False:
                if name is not None:
                    name = json.loads(name)

            short_name = level_dict.pop("short_name")
            if False:
                if short_name is not None:
                    short_name = json.loads(short_name)

            outdoor = level_dict.pop("outdoor")
            if True:
                if not isinstance(outdoor, bool):
                    outdoor = bool(outdoor)

            display_point = level_dict.pop("display_point")
            if display_point is not None:
                if isinstance(display_point, dict):
                    display_point = shapely.from_geojson(json.dumps(display_point))
                else:
                    display_point = shapely.from_geojson(display_point)

            building_ids = level_dict.pop("building_ids")
            if True:
                if building_ids is not None:
                    if isinstance(building_ids, List):
                        ...
                    else:
                        building_ids = [building_ids]

            level = IMDFLevel(
                **level_dict,
                name=name,
                short_name=short_name,
                outdoor=outdoor,
                display_point=display_point,
                building_ids=building_ids,
            )
            out[IMDFFeatureType.level].append(level)

    if IMDFFeatureType.section.value in dataframes:
        for ith_row, section_row in dataframes[
            IMDFFeatureType.section.value
        ].iterrows():
            section_dict = section_row.to_dict()

            name = section_dict.pop("name")
            if False:
                if name is not None:
                    name = json.loads(name)

            alt_name = section_dict.pop("alt_name")
            if False:
                if alt_name is not None:
                    alt_name = json.loads(alt_name)

            section_id = section_dict.pop("id")
            if True:
                if section_id is not None:
                    ...
                    # section_id = str(section_id)
                else:
                    logger.error(
                        f"section_id is None, generating a new one"
                        # f"{section_row}"
                    )
                    section_id = uuid.uuid4().hex

            display_point = section_dict.pop("display_point")
            if display_point is not None:
                if isinstance(display_point, dict):
                    display_point = shapely.from_geojson(json.dumps(display_point))
                else:
                    display_point = shapely.from_geojson(display_point)

            section = IMDFSection(
                **section_dict,
                id=section_id,
                name=name,
                alt_name=alt_name,
                display_point=display_point,
            )
            out[IMDFFeatureType.section].append(section)

    if IMDFFeatureType.occupant.value in dataframes:
        for ith_row, occupant_row in dataframes[
            IMDFFeatureType.occupant.value
        ].iterrows():
            occupant_dict = occupant_row.to_dict()

            name = occupant_dict.pop("name")
            if False:
                if name is not None:
                    name = json.loads(name)

            validity = occupant_dict.pop("validity")
            if validity is not None:
                validity = Temporality(**json.loads(validity))

            occupant = IMDFOccupant(**occupant_dict, name=name, validity=validity)
            out[IMDFFeatureType.occupant].append(occupant)

    if IMDFFeatureType.opening.value in dataframes:
        for ith_row, opening_row in dataframes[
            IMDFFeatureType.opening.value
        ].iterrows():
            opening_dict = opening_row.to_dict()

            name = opening_dict.pop("name")
            if False:
                if name is not None:
                    name = json.loads(name)

            alt_name = opening_dict.pop("alt_name")
            if False:
                if alt_name is not None:
                    alt_name = json.loads(alt_name)

            display_point = opening_dict.pop("display_point")
            if display_point is not None:
                if isinstance(display_point, dict):
                    display_point = shapely.from_geojson(json.dumps(display_point))
                else:
                    display_point = shapely.from_geojson(display_point)

            door = opening_dict.pop("door")
            if door is not None:
                door = Door(**json.loads(door))

            opening = IMDFOpening(
                **opening_dict,
                name=name,
                alt_name=alt_name,
                display_point=display_point,
                door=door,
            )
            out[IMDFFeatureType.opening].append(opening)

    if IMDFFeatureType.relationship.value in dataframes:
        for ith_row, relationship_row in dataframes[
            IMDFFeatureType.relationship.value
        ].iterrows():
            relationship_dict = relationship_row.to_dict()

            relationship = IMDFRelationship(**relationship_dict)
            out[IMDFFeatureType.relationship].append(relationship)

    if IMDFFeatureType.kiosk.value in dataframes:
        for ith_row, kiosk_row in dataframes[IMDFFeatureType.kiosk.value].iterrows():
            kiosk_dict = kiosk_row.to_dict()

            kiosk = IMDFKiosk(**kiosk_dict)
            out[IMDFFeatureType.kiosk].append(kiosk)

    if IMDFFeatureType.detail.value in dataframes:
        for ith_row, detail_row in dataframes[IMDFFeatureType.detail.value].iterrows():
            detail_dict = detail_row.to_dict()

            detail = IMDFDetail(**detail_dict)
            out[IMDFFeatureType.detail].append(detail)

    if IMDFFeatureType.anchor.value in dataframes:
        for ith_row, anchor_row in dataframes[IMDFFeatureType.anchor.value].iterrows():
            anchor_dict = anchor_row.to_dict()

            anchor = IMDFAnchor(**anchor_dict)
            out[IMDFFeatureType.anchor].append(anchor)

    if IMDFFeatureType.geofence.value in dataframes:
        for ith_row, geofence_row in dataframes[
            IMDFFeatureType.geofence.value
        ].iterrows():
            geofence_dict = geofence_row.to_dict()

            geofence = IMDFGeofence(**geofence_dict)
            out[IMDFFeatureType.geofence].append(geofence)

    if IMDFFeatureType.address.value in dataframes:
        for ith_row, address_row in dataframes[
            IMDFFeatureType.address.value
        ].iterrows():
            address_dict = address_row.to_dict()

            address = IMDFAddress(**address_dict)
            out[IMDFFeatureType.address].append(address)

    if IMDFFeatureType.amenity.value in dataframes:
        for ith_row, amenity_row in dataframes[
            IMDFFeatureType.amenity.value
        ].iterrows():
            amenity_dict = amenity_row.to_dict()

            amenity = IMDFAmenity(**amenity_dict)
            out[IMDFFeatureType.amenity].append(amenity)

    return out
