from collections import defaultdict
from typing import Collection, Dict, List, Mapping

from warg.data_structures.mappings import to_dict

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFFeature, IMDFFixture
from midf.model import MIDFFixture

__all__ = ["link_fixtures"]


def link_fixtures(
    anchor_id_mapping, imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]]
) -> Dict[str, List[MIDFFixture]]:
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
    return to_dict(fixtures)
