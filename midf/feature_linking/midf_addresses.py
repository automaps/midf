from typing import Collection, Dict, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFAddress, IMDFFeature
from midf.model import MIDFAddress

__all__ = ["link_addresses"]


def link_addresses(
    found_venue_addresses,
    imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]],
    venue_mapping,
) -> Dict[str, MIDFAddress]:
    addresses = {}
    for address in imdf_dict[IMDFFeatureType.address]:
        address: IMDFAddress
        assert address.id not in addresses
        addresses[address.id] = MIDFAddress(
            id=address.id,
            address=address.address,
            locality=address.locality,
            country=address.country,
            province=address.province,
            unit=address.unit,
            postal_code=address.postal_code,
            postal_code_ext=address.postal_code_ext,
            postal_code_vanity=address.postal_code_vanity,
            venues=(
                venue_mapping.pop(address.id)
                if address.id in found_venue_addresses
                else None
            ),
        )
    return addresses
