import json
from pathlib import Path
from typing import Any

__all__ = ["parse_imdf"]

import shapely
import logging

from midf.imdf_model import (
    IMDFBuilding,
    IMDFFeatureType,
    IMDFFootprint,
    IMDFRelationship,
    IMDFUnit,
    IMDFVenue,
    IMDFFixture,
    IMDFLevel,
    IMDFSection,
    IMDFOpening,
    IMDFOccupant,
    IMDFKiosk,
    IMDFDetail,
    IMDFAnchor,
    IMDFAddress,
    IMDFAmenity,
)

logger = logging.getLogger(__name__)


def parse_imdf(imdf_file_path: Path) -> Any:
    from zipfile import ZipFile
    import geopandas

    assert imdf_file_path.exists()
    assert imdf_file_path.is_file()
    assert imdf_file_path.suffix == ".zip"

    dataframes = {}

    with ZipFile(imdf_file_path) as zf:
        for file in zf.namelist():
            z_file_path = Path(file)
            if z_file_path.suffix == ".geojson":  # optional filtering by filetype
                with zf.open(file) as f:
                    df = geopandas.read_file(f)
                    feature_name = z_file_path.stem
                    dataframes[feature_name] = df

            elif file == "manifest.json":
                ...

            else:
                logger.error(f"{file} was skipped")

    if True:
        for ith_row, venue_row in dataframes[IMDFFeatureType.venue.value].iterrows():
            venue_dict = venue_row.to_dict()

            name = venue_dict.pop("name")
            if name is not None:
                name = json.loads(name)

            display_point = shapely.from_geojson(venue_dict.pop("display_point"))

            venue = IMDFVenue(**venue_dict, name=name, display_point=display_point)
            ...

    if True:
        for ith_row, building_row in dataframes[
            IMDFFeatureType.building.value
        ].iterrows():
            building_dict = building_row.to_dict()

            name = building_dict.pop("name")
            if name is not None:
                name = json.loads(name)

            alt_name = building_dict.pop("alt_name")
            if alt_name is not None:
                alt_name = json.loads(alt_name)

            display_point = shapely.from_geojson(building_dict.pop("display_point"))

            building = IMDFBuilding(
                **building_dict,
                name=name,
                alt_name=alt_name,
                display_point=display_point,
            )
            ...

    if True:
        for ith_row, footprint_row in dataframes[
            IMDFFeatureType.footprint.value
        ].iterrows():
            footprint_dict = footprint_row.to_dict()

            name = footprint_dict.pop("name")
            if name is not None:
                name = json.loads(name)

            footprint = IMDFFootprint(**footprint_dict, name=name)
            ...

    if True:
        for ith_row, fixture_row in dataframes[
            IMDFFeatureType.fixture.value
        ].iterrows():
            fixture_dict = fixture_row.to_dict()

            name = fixture_dict.pop("name")
            if name is not None:
                name = json.loads(name)

            alt_name = fixture_dict.pop("alt_name")
            if alt_name is not None:
                alt_name = json.loads(alt_name)

            display_point = shapely.from_geojson(fixture_dict.pop("display_point"))

            fixture = IMDFFixture(
                **fixture_dict,
                name=name,
                alt_name=alt_name,
                display_point=display_point,
            )
            ...

    if True:
        for ith_row, unit_row in dataframes[IMDFFeatureType.unit.value].iterrows():
            unit_dict = unit_row.to_dict()

            name = unit_dict.pop("name")
            if name is not None:
                name = json.loads(name)

            alt_name = unit_dict.pop("alt_name")
            if alt_name is not None:
                alt_name = json.loads(alt_name)

            display_point = shapely.from_geojson(unit_dict.pop("display_point"))

            unit = IMDFUnit(
                **unit_dict, name=name, alt_name=alt_name, display_point=display_point
            )
            ...

    if True:
        for ith_row, level_row in dataframes[IMDFFeatureType.level.value].iterrows():
            level_dict = level_row.to_dict()

            name = level_dict.pop("name")
            if name is not None:
                name = json.loads(name)

            short_name = level_dict.pop("short_name")
            if short_name is not None:
                short_name = json.loads(short_name)

            display_point = shapely.from_geojson(level_dict.pop("display_point"))

            level = IMDFLevel(
                **level_dict,
                name=name,
                short_name=short_name,
                display_point=display_point,
            )
            ...

    if True:
        for ith_row, section_row in dataframes[
            IMDFFeatureType.section.value
        ].iterrows():
            section_dict = section_row.to_dict()

            name = section_dict.pop("name")
            if name is not None:
                name = json.loads(name)

            alt_name = section_dict.pop("alt_name")
            if alt_name is not None:
                alt_name = json.loads(alt_name)

            display_point = shapely.from_geojson(section_dict.pop("display_point"))

            section = IMDFSection(
                **section_dict,
                name=name,
                alt_name=alt_name,
                display_point=display_point,
            )
            ...

    if True:
        for ith_row, occupant_row in dataframes[
            IMDFFeatureType.occupant.value
        ].iterrows():
            occupant_dict = occupant_row.to_dict()

            name = occupant_dict.pop("name")
            if name is not None:
                name = json.loads(name)

            occupant = IMDFOccupant(**occupant_dict, name=name)
            ...

    if True:
        for ith_row, opening_row in dataframes[
            IMDFFeatureType.opening.value
        ].iterrows():
            opening_dict = opening_row.to_dict()

            name = opening_dict.pop("name")
            if name is not None:
                name = json.loads(name)

            alt_name = opening_dict.pop("alt_name")
            if alt_name is not None:
                alt_name = json.loads(alt_name)

            display_point = shapely.from_geojson(opening_dict.pop("display_point"))

            opening = IMDFOpening(
                **opening_dict,
                name=name,
                alt_name=alt_name,
                display_point=display_point,
            )
            ...

    if True:
        for ith_row, relationship_row in dataframes[
            IMDFFeatureType.relationship.value
        ].iterrows():
            relationship_dict = relationship_row.to_dict()

            relationship = IMDFRelationship(**relationship_dict)
            ...

    if True:
        for ith_row, kiosk_row in dataframes[IMDFFeatureType.kiosk.value].iterrows():
            kiosk_dict = kiosk_row.to_dict()

            kiosk = IMDFKiosk(**kiosk_dict)
            ...

    if True:
        for ith_row, detail_row in dataframes[IMDFFeatureType.detail.value].iterrows():
            detail_dict = detail_row.to_dict()

            detail = IMDFDetail(**detail_dict)
            ...

    if True:
        for ith_row, anchor_row in dataframes[IMDFFeatureType.anchor.value].iterrows():
            anchor_dict = anchor_row.to_dict()

            anchor = IMDFAnchor(**anchor_dict)
            ...

    if True:
        for ith_row, address_row in dataframes[
            IMDFFeatureType.address.value
        ].iterrows():
            address_dict = address_row.to_dict()

            address = IMDFAddress(**address_dict)
            ...

    if True:
        for ith_row, amenity_row in dataframes[
            IMDFFeatureType.amenity.value
        ].iterrows():
            amenity_dict = amenity_row.to_dict()

            amenity = IMDFAmenity(**amenity_dict)
            ...
