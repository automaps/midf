import json
import logging
from itertools import count
from pathlib import Path

import osmnx
import pyproj
import shapely
from jord.networkx_utilities import add_shapely_node, assertive_add_edge
from networkx import MultiDiGraph
from warg import recursive_flatten

logger = logging.getLogger(__name__)


def save_graph(new_graph: MultiDiGraph, save_path: Path) -> None:
    new_graph.graph["crs"] = pyproj.CRS.from_user_input("EPSG:4326")

    osmnx.settings.all_oneway = True

    edge_tags = set(
        recursive_flatten([edge.keys() for edge in new_graph.edges.values()])
    )
    node_tags = set(
        recursive_flatten([node.keys() for node in new_graph.nodes.values()])
    )

    osmnx.save_graph_xml(
        new_graph,
        filepath=save_path,
        edge_tags=list(edge_tags),
        node_tags=list(node_tags),
        # edge_tag_aggs=[("length", "sum")],
        oneway=True,
        merge_edges=False,
        precision=11,
    )


def parse_route(route_file_path: Path):
    assert route_file_path.exists()
    assert route_file_path.is_file()
    assert route_file_path.suffix == ".json"

    with open(route_file_path) as route_file:
        route_dict = json.load(route_file)

        coordinates = route_dict["coordinates"]
        links = route_dict["links"]
        level_coords = route_dict["level_coords"]

        coordinate_levels = {i: None for i in range(len(coordinates))}
        for level_index, (from_idx, num) in level_coords.items():
            for i in range(from_idx, from_idx + num):
                assert coordinate_levels[i] is None
                coordinate_levels[i] = level_index

        assert all(coordinate_levels.values())

        graph = MultiDiGraph()

        node_id_offset = 1

        for i, coords in enumerate(coordinates):
            add_shapely_node(
                graph=graph,
                u=i + node_id_offset,
                point=shapely.Point(coords),
                level=coordinate_levels[i],
            )

        edge_id_counter = iter(count())
        if node_id_offset:  # OSM does not like 0 as id
            next(edge_id_counter)
        for i, edges in enumerate(links):
            for edge in edges:
                (to_distance, to_link) = edge.values()
                if i != to_link:
                    assertive_add_edge(
                        graph=graph,
                        u=i + node_id_offset,
                        v=to_link + node_id_offset,
                        uniqueid=next(edge_id_counter),
                        attributes=dict(
                            distance=to_distance, level=coordinate_levels[i]
                        ),
                        allow_loops=False,
                        allow_duplicates=False,
                    )
                else:
                    logger.error(f"Loop detected {i, to_link}")

        save_graph(graph, Path("../test.osm"))


if __name__ == "__main__":
    parse_route(Path(__file__).parent / "data" / "Routes.json")
