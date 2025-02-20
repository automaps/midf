import logging
import uuid
from itertools import count

from jord.shapely_utilities import clean_shape, dilate

from integration_system.model import Area, ConnectionType, Connector, Room, Solution
from midf.enums import IMDFRelationshipCategory
from midf.imdf_model.opening import IMDFDirection
from midf.mi_utilities import clean_admin_id
from midf.model import MIDFRelationship, MIDFSolution, MIDFUnit

logger = logging.getLogger(__name__)

__all__ = ["convert_relationships"]


def convert_relationships(
    mi_solution: Solution, midf_solution: MIDFSolution, venue_graph_key: str
) -> None:
    if midf_solution.relationships:
        id_counter = iter(count())
        for relationship in midf_solution.relationships:
            relationship: MIDFRelationship

            category_ = relationship.category
            connection_type = ConnectionType.elevator
            if category_ == IMDFRelationshipCategory.elevator:
                connection_type = ConnectionType.elevator
            elif category_ == IMDFRelationshipCategory.escalator:
                connection_type = ConnectionType.escalator
            elif category_ == IMDFRelationshipCategory.stairs:
                connection_type = ConnectionType.steps
            elif category_ == IMDFRelationshipCategory.ramp:
                connection_type = ConnectionType.ramp
            elif category_ == IMDFRelationshipCategory.moving_walkway:
                continue
                connection_type = ConnectionType.escalator  # skip?
            elif category_ == IMDFRelationshipCategory.traversal:
                continue
                connection_type = ConnectionType.wheel_chair_ramp
            elif category_ == IMDFRelationshipCategory.traversal_path:
                continue
                connection_type = ConnectionType.wheel_chair_lift
            else:
                logger.warning(f"Unknown relationship category {category_}")

            if (
                relationship.direction == IMDFDirection.directed
            ):  # TODO: Directed relationships are not supported,
                # so we skip them for now.
                logger.error(f"Directed relationships are not supported {relationship}")
                ...

            origin_room = mi_solution.rooms.get(
                key=Room.compute_key(admin_id=clean_admin_id(relationship.origin.id))
            )
            if not origin_room:
                logger.error(f"Origin room not found for relationship {relationship}")
                if mi_solution.areas.get(
                    key=Area.compute_key(
                        admin_id=clean_admin_id(relationship.origin.id)
                    )
                ):
                    logger.error(f"Origin area found for relationship {relationship}")
                continue

            connectors = [
                Connector(
                    uuid.uuid4().hex,
                    floor_index=origin_room.floor.floor_index,
                    point=relationship.origin.geometry.representative_point(),
                ),
            ]

            if relationship.intermediary:
                for unit in relationship.intermediary:
                    if not isinstance(unit, MIDFUnit):
                        logger.error(f"Intermediary is not a unit {unit}")
                        continue

                    in_room = mi_solution.rooms.get(
                        key=Room.compute_key(admin_id=clean_admin_id(unit.id))
                    )

                    if not in_room:
                        logger.error(
                            f"Intermediary room not found for relationship {relationship}"
                        )
                        if mi_solution.areas.get(
                            key=Area.compute_key(admin_id=clean_admin_id(unit.id))
                        ):
                            logger.error(
                                f"Intermediary area found for relationship {relationship}"
                            )
                        continue

                    connectors.append(
                        Connector(
                            uuid.uuid4().hex,
                            floor_index=in_room.floor.floor_index,
                            point=unit.geometry.representative_point(),
                        )
                    )

            destination_room = mi_solution.rooms.get(
                key=Room.compute_key(
                    admin_id=clean_admin_id(relationship.destination.id)
                )
            )
            if not destination_room:
                logger.error(
                    f"Destination room not found for relationship {relationship}"
                )
                if mi_solution.areas.get(
                    key=Area.compute_key(
                        admin_id=clean_admin_id(relationship.destination.id)
                    )
                ):
                    logger.error(
                        f"Destination area found for relationship {relationship}"
                    )
                continue

            connectors.append(
                Connector(
                    uuid.uuid4().hex,
                    floor_index=destination_room.floor.floor_index,
                    point=relationship.origin.geometry.representative_point(),
                )
            )

            mi_solution.add_connection(
                next(id_counter),
                graph_key=venue_graph_key,
                connection_type=connection_type,
                connectors=connectors,
            )
