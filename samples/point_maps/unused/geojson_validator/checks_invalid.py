import logging

import shapely.geometry

logger = logging.getLogger(__name__)


def check_unclosed(geometry: dict) -> bool:
    """Return True if the geometry is not closed (first coordinate != last coordinate)."""
    # This needs to check the original json string, as shapely or geopandas automatically close.
    # assert len(geometry["coordinates"]) > 0, f"{geometry} has no coordinates"
    if not geometry["coordinates"]:
        return True

    coords = geometry["coordinates"][0]
    return coords[0] != coords[-1]


def check_less_three_unique_nodes(geometry: dict) -> bool:
    """Return True if there are fewer than three unique nodes in the geometry."""
    # assert len(geometry["coordinates"]) > 0, f"{geometry} has no coordinates"
    if not geometry["coordinates"]:
        return True

    coords = geometry["coordinates"][0]
    return len(set(map(tuple, coords))) < 3


def check_exterior_not_ccw(geom: shapely.geometry.Polygon) -> bool:
    """Return True if the exterior ring is not counter-clockwise."""
    return not geom.exterior.is_ccw


def check_interior_not_cw(geom: shapely.geometry.Polygon) -> bool:
    """Return True if any interior ring is counter-clockwise."""
    return any(interior.is_ccw for interior in geom.interiors)


def check_inner_and_exterior_ring_intersect(geom: shapely.geometry.Polygon) -> bool:
    """Return True if any interior ring intersects with the exterior ring."""
    return any(geom.exterior.intersects(interior) for interior in geom.interiors)
