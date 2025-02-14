import logging
from typing import Mapping

from jord.shapely_utilities import clean_shape, dilate, dilate, erode

from integration_system.model import PostalAddress, Solution
from midf.conversion import IMDF_VENUE_CATEGORY_TO_MI_VENUE_TYPE
from midf.imdf_model import IMDFVenue
from midf.model import MIDFSolution

logger = logging.getLogger(__name__)

__all__ = ["convert_venues"]


def convert_venues(
    address_venue_mapping: Mapping, mi_solution: Solution, midf_solution: MIDFSolution
) -> (IMDFVenue, str):
    venue_key = None
    for address in midf_solution.addresses:
        if address.venues:
            for venue in address.venues:
                venue_name = next(iter(venue.name.values()))

                venue_key = mi_solution.add_venue(
                    admin_id=venue.id,
                    name=venue_name,
                    venue_type=IMDF_VENUE_CATEGORY_TO_MI_VENUE_TYPE[venue.category],
                    address=PostalAddress(
                        postal_code=address.postal_code,
                        street1=address.address,
                        country=address.country,
                        city=address.locality,
                        region=address.province,
                    ),
                    polygon=dilate(venue.display_point),
                )
                address_venue_mapping[address.id].append(venue_key)
    return venue, venue_key
