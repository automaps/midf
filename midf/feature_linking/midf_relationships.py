from typing import Collection, List, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFFeature, IMDFRelationship
from midf.model import MIDFRelationship

__all__ = ["link_relationships"]


def link_relationships(
    imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]]
) -> Mapping[str, List[MIDFRelationship]]:
    relationships = {}
    for relationship in imdf_dict[IMDFFeatureType.relationship]:
        relationship: IMDFRelationship
        relationships[relationship.level_id].append(
            MIDFRelationship(
                id=relationship.id,
                category=relationship.category,
                direction=relationship.direction,
                geometry=relationship.geometry,
                origin=relationship.origin,  # TODO: PARSE
                intermediary=relationship.intermediary,  # TODO: PARSE
                destination=relationship.destination,  # TODO: PARSE
                hours=relationship.hours,  # TODO: PARSE
            )
        )
    return relationships
