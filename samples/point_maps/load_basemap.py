from pathlib import Path

import geopandas

file_path = (
    Path(__file__).parent / "data" / "auxiliary_data" / "SIT" / "basemap.geojson"
)

df = geopandas.read_file(file_path, engine="fiona")
