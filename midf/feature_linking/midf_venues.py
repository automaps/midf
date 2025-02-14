from collections import defaultdict
from typing import Collection, Dict, List, Mapping

from warg.data_structures.mappings import to_dict

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFFeature, IMDFVenue
from midf.model import MIDFVenue

__all__ = ["link_venues"]


def link_venues(
    imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]],
) -> Dict[str, List[MIDFVenue]]:
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

    return to_dict(venue_mapping)
