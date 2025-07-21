import geopandas
import json
import logging
from pathlib import Path
from typing import Collection, Mapping
from zipfile import ZipFile

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFFeature

logger = logging.getLogger(__name__)


def prepare_feature_collection(feature_collection: Collection[IMDFFeature]) -> str:
    out = []
    for feature in feature_collection:
        out.append(feature.to_imdf_spec_feature())

    df = geopandas.GeoDataFrame(out)

    try:
        return df.to_json()
    except Exception as e:
        logger.error(f"{feature_collection}: {e}")
        logger.info("RETURNING empty FeatureCollection")
        return '{"type": "FeatureCollection", "features": []}'


def package_imdf(
    target_imdf_file: Path,
    manifest: Mapping[str, str],
    feature_collections: Mapping[IMDFFeatureType, Collection[IMDFFeature]],
) -> None:
    with ZipFile(target_imdf_file, "w") as zf:
        zf.writestr("manifest.json", json.dumps(manifest))

        for feature_type, feature_collection in feature_collections.items():
            feature_collection_json = prepare_feature_collection(feature_collection)
            zf.writestr(f"{feature_type.value}.geojson", feature_collection_json)
