import json
import logging
from collections import defaultdict
from pathlib import Path
from typing import Collection, Union

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
from .typing import Door, Temporality

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

    for ith_row, building_row in dataframes[IMDFFeatureType.building.value].iterrows():
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

    for ith_row, fixture_row in dataframes[IMDFFeatureType.fixture.value].iterrows():
        fixture_dict = fixture_row.to_dict()

        name = fixture_dict.pop("name")
        if False:
            if name is not None:
                name = json.loads(name)

        alt_name = fixture_dict.pop("alt_name")
        if False:
            if alt_name is not None:
                alt_name = json.loads(alt_name)

        display_point = fixture_dict.pop("display_point")
        if display_point is not None:
            if isinstance(display_point, dict):
                display_point = shapely.from_geojson(json.dumps(display_point))
            else:
                display_point = shapely.from_geojson(display_point)

        fixture = IMDFFixture(
            **fixture_dict,
            name=name,
            alt_name=alt_name,
            display_point=display_point,
        )

        out[IMDFFeatureType.fixture].append(fixture)

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

        display_point = unit_dict.pop("display_point")
        if display_point is not None:
            if isinstance(display_point, dict):
                display_point = shapely.from_geojson(json.dumps(display_point))
            else:
                display_point = shapely.from_geojson(display_point)

        unit = IMDFUnit(
            **unit_dict, name=name, alt_name=alt_name, display_point=display_point
        )
        out[IMDFFeatureType.unit].append(unit)

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

        display_point = level_dict.pop("display_point")
        if display_point is not None:
            if isinstance(display_point, dict):
                display_point = shapely.from_geojson(json.dumps(display_point))
            else:
                display_point = shapely.from_geojson(display_point)

        level = IMDFLevel(
            **level_dict,
            name=name,
            short_name=short_name,
            display_point=display_point,
        )
        out[IMDFFeatureType.level].append(level)

    for ith_row, section_row in dataframes[IMDFFeatureType.section.value].iterrows():
        section_dict = section_row.to_dict()

        name = section_dict.pop("name")
        if False:
            if name is not None:
                name = json.loads(name)

        alt_name = section_dict.pop("alt_name")
        if False:
            if alt_name is not None:
                alt_name = json.loads(alt_name)

        display_point = section_dict.pop("display_point")
        if display_point is not None:
            if isinstance(display_point, dict):
                display_point = shapely.from_geojson(json.dumps(display_point))
            else:
                display_point = shapely.from_geojson(display_point)

        section = IMDFSection(
            **section_dict,
            name=name,
            alt_name=alt_name,
            display_point=display_point,
        )
        out[IMDFFeatureType.section].append(section)

    for ith_row, occupant_row in dataframes[IMDFFeatureType.occupant.value].iterrows():
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

    for ith_row, opening_row in dataframes[IMDFFeatureType.opening.value].iterrows():
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

    for ith_row, relationship_row in dataframes[
        IMDFFeatureType.relationship.value
    ].iterrows():
        relationship_dict = relationship_row.to_dict()

        relationship = IMDFRelationship(**relationship_dict)
        out[IMDFFeatureType.relationship].append(relationship)

    for ith_row, kiosk_row in dataframes[IMDFFeatureType.kiosk.value].iterrows():
        kiosk_dict = kiosk_row.to_dict()

        kiosk = IMDFKiosk(**kiosk_dict)
        out[IMDFFeatureType.kiosk].append(kiosk)

    for ith_row, detail_row in dataframes[IMDFFeatureType.detail.value].iterrows():
        detail_dict = detail_row.to_dict()

        detail = IMDFDetail(**detail_dict)
        out[IMDFFeatureType.detail].append(detail)

    for ith_row, anchor_row in dataframes[IMDFFeatureType.anchor.value].iterrows():
        anchor_dict = anchor_row.to_dict()

        anchor = IMDFAnchor(**anchor_dict)
        out[IMDFFeatureType.anchor].append(anchor)

    for ith_row, address_row in dataframes[IMDFFeatureType.address.value].iterrows():
        address_dict = address_row.to_dict()

        address = IMDFAddress(**address_dict)
        out[IMDFFeatureType.address].append(address)

    for ith_row, amenity_row in dataframes[IMDFFeatureType.amenity.value].iterrows():
        amenity_dict = amenity_row.to_dict()

        amenity = IMDFAmenity(**amenity_dict)
        out[IMDFFeatureType.amenity].append(amenity)

    return out
