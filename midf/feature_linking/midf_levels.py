from typing import Collection, Dict, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFFeature, IMDFLevel
from midf.model import MIDFLevel

__all__ = ["link_levels"]


def link_levels(
    *,
    buildings,
    details,
    fixtures,
    found_detail_levels,
    found_fixture_levels,
    found_kiosk_levels,
    found_opening_levels,
    found_section_levels,
    found_unit_levels,
    imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]],
    kiosks,
    openings,
    sections,
    units,
) -> Dict[str, MIDFLevel]:
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
    return levels
