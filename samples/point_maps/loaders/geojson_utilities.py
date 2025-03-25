import logging
from pathlib import Path

import shapely

__all__ = ["convert_display_point"]

from geojson_validator import fix_geometries


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


def validate_gjson(p: Path):
    s = fix_geometries(p)

    ...


if __name__ == "__main__":

    def ayusghdyug():
        logging.basicConfig(level=logging.WARNING)

        a = Path(__file__).parent.parent / "exclude2" / "national_gallery_1"
        assert a.exists(), f"{a} does not exist"
        for i in a.iterdir():
            if i.is_file() and i.suffix == ".json":
                try:
                    validate_gjson(i)
                except Exception as e:
                    logging.error(f"invalid gjson: {i} {e}")
                    pass

    ayusghdyug()
