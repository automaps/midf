import shapely

__all__ = ["convert_display_point"]


def convert_display_point(v):
    """
    DISPLAY_PO
    DISPLAY__1
    DISPLAY__2

    :param v:
    :return:
    """

    if "DISPLAY_POINT" in v:
        if v["DISPLAY_POINT"] is not None:
            return shapely.from_geojson(str(v["DISPLAY_POINT"]).replace("'", '"'))

    return None
