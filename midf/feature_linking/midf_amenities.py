from collections import defaultdict
from typing import Collection, Dict, Mapping

from warg.data_structures.mappings import to_dict

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFAmenity, IMDFFeature

__all__ = ["link_amenities"]

from midf.model.solution_level.amenity import MIDFAmenity


def link_amenities(
    imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]], units
) -> Dict[str, MIDFAmenity]:
    amenities = defaultdict()

    unit_id_mapping = {unit.id: unit for a in units.values() for unit in a}

    for amenity in imdf_dict[IMDFFeatureType.amenity]:
        amenity: IMDFAmenity
        amenities[amenity.id] = MIDFAmenity(
            id=amenity.id,
            name=amenity.name,
            category=amenity.category,
            hours=amenity.hours,
            phone=amenity.phone,
            website=amenity.website,
            correlation_id=amenity.correlation_id,
            units=[unit_id_mapping[uid] for uid in amenity.unit_ids],
            geometry=amenity.geometry,
        )

    return to_dict(amenities)
