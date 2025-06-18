import logging

import shapely

from integration_system.model import LanguageBundle, LocationType, Solution
from jord.shapely_utilities import clean_shape
from midf.mi_utilities import clean_admin_id
from midf.model import MIDFFixture, MIDFLevel

logger = logging.getLogger(__name__)

__all__ = ["convert_fixtures"]


def convert_fixtures(floor_key: str, level: MIDFLevel, mi_solution: Solution) -> None:
    if level.fixtures:
        for fixture in level.fixtures:
            fixture: MIDFFixture

            fixture_name = None
            if fixture.name:
                fixture_name = next(iter(fixture.name.values()))

            if fixture_name is None or fixture_name == "":
                if fixture.alt_name:
                    fixture_name = next(iter(fixture.alt_name.values()))

            if fixture_name is None or fixture_name == "":
                fixture_name = fixture.id

            fixture_geom = clean_shape(fixture.geometry)

            location_type_key = LocationType.compute_key(admin_id=fixture.category)
            if mi_solution.location_types.get(location_type_key) is None:
                location_type_key = mi_solution.add_location_type(
                    admin_id=fixture.category,
                    translations={"en": LanguageBundle(name=fixture.category)},
                )

            if fixture_geom.is_valid and (not fixture_geom.is_empty):
                if isinstance(fixture_geom, shapely.Polygon):
                    mi_solution.add_area(
                        admin_id=clean_admin_id(fixture.id),
                        translations={"en": LanguageBundle(name=fixture_name)},
                        polygon=fixture_geom,
                        floor_key=floor_key,
                        location_type_key=location_type_key,
                    )
                elif isinstance(fixture_geom, shapely.MultiPolygon):
                    for ith, polygon in enumerate(fixture_geom.geoms):
                        mi_solution.add_area(
                            admin_id=clean_admin_id(f"{fixture.id}_part_{str(ith)}"),
                            translations={"en": LanguageBundle(name=fixture_name)},
                            polygon=polygon,
                            floor_key=floor_key,
                            location_type_key=location_type_key,
                        )
                else:
                    logger.error(f"Ignoring {fixture}")
            else:
                logger.error(f"Ignoring {fixture}")
