import logging

import shapely.geometry
from shapely.validation import explain_validity

logger = logging.getLogger(__name__)


def check_holes(geom: shapely.geometry.Polygon) -> bool:
    """Return True if the geometry has holes (interior rings)."""
    return len(geom.interiors) > 0


def check_self_intersection(geom: shapely.geometry.Polygon) -> bool:
    """Return True if the geometry is self-intersecting."""
    # TODO: Shapely independent?
    self_intersection = False
    if not geom.is_valid:
        self_intersection = "Self-intersection" in explain_validity(geom)

    return self_intersection


def check_duplicate_nodes(geometry: dict) -> bool:
    """Return True if there are duplicate nodes, excluding the acceptable duplicate of a closed ring."""
    if not geometry["coordinates"]:
        return True

    coords = geometry["coordinates"][0]
    unique_coords = set(map(tuple, coords))

    has_duplicates = len(unique_coords) < len(coords)
    is_closed_ring = coords[0] == coords[-1]
    only_closed_ring_duplicate = (
        is_closed_ring and len(unique_coords) == len(coords) - 1
    )

    return has_duplicates and not only_closed_ring_duplicate


def check_3d_coordinates(geometry: dict, n_first_coords=2) -> bool:
    """Return True if any coordinates are more than 2D."""
    # TODO: should all coordinates be checked?
    if not geometry["coordinates"]:
        return False

    for coords in geometry["coordinates"][0][:n_first_coords]:
        if len(coords) > 2:
            return True

    return False


def check_outside_lat_lon_boundaries(geometry: dict) -> bool:
    """Return True if not all coordinates are within the standard lat/lon boundaries."""

    if not geometry["coordinates"]:
        return True

    def _inside_boundaries(lon, lat):
        return -180 <= lon <= 180 and -90 <= lat <= 90

    for coords in geometry["coordinates"][0]:
        if not _inside_boundaries(coords[0], coords[1]):
            return True

    return False


def check_crosses_antimeridian(geometry: dict) -> bool:
    """Return True if the geometry crosses the antimeridian (meridian at 180 longitude)."""
    if not geometry["coordinates"]:
        return False

    coords = geometry["coordinates"][0]
    for start, end in zip(coords, coords[1:]):
        # Normalize longitudes to -180 to 180 range
        norm_start_lon = (start[0] + 180) % 360 - 180
        norm_end_lon = (end[0] + 180) % 360 - 180

        # Check for longitude switch indicating crossing
        if abs(norm_end_lon - norm_start_lon) > 180:
            return True

    return False
