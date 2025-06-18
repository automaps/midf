import logging
from typing import List, Mapping

import shapely

from integration_system.common_models import MIVenueType
from integration_system.model import LanguageBundle, PostalAddress, Solution
from midf.constants import IMDF_VENUE_CATEGORY_TO_MI_VENUE_TYPE
from midf.mi_utilities import clean_admin_id
from midf.model import MIDFAddress, MIDFSolution, MIDFVenue

logger = logging.getLogger(__name__)

__all__ = ["convert_venues"]


def convert_venues(
    address_venue_mapping: Mapping[str, List[MIDFAddress]],
    mi_solution: Solution,
    midf_solution: MIDFSolution,
) -> (MIDFVenue, str):
    venue_key = None
    venue = None

    for address in midf_solution.addresses:
        if address.venues:
            for venue in address.venues:
                venue: MIDFVenue

                venue_name = None
                if venue.name:
                    venue_name = next(iter(venue.name.values()))

                if venue_name is None or venue_name == "":
                    if venue.alt_name:
                        venue_name = next(iter(venue.alt_name.values()))

                if venue_name is None or venue_name == "":
                    venue_name = venue.id

                venue_key = mi_solution.add_venue(
                    admin_id=clean_admin_id(venue.id),
                    translations={"en": LanguageBundle(name=venue_name)},
                    venue_type=(
                        IMDF_VENUE_CATEGORY_TO_MI_VENUE_TYPE[venue.category]
                        if venue.category in IMDF_VENUE_CATEGORY_TO_MI_VENUE_TYPE
                        else MIVenueType.not_specified
                    ),
                    address=PostalAddress(
                        postal_code=address.postal_code,
                        street1=address.address,
                        country=address.country,
                        city=address.locality,
                        region=address.province,
                    ),
                    polygon=venue.geometry,
                    # dilate(venue.display_point),
                )
                address_venue_mapping[address.id].append(venue_key)

    if venue is None:
        logger.error("No venues found in the MIDF solution.")
        venue_key = mi_solution.add_venue(
            admin_id="default-venue",
            translations={"en": LanguageBundle(name="Default Venue")},
            address=PostalAddress(
                postal_code="",
                street1="",
                country="",
                city="",
                region="",
            ),
            polygon=shapely.Point(0, 0).buffer(0.01),
        )

    return venue, venue_key
