from typing import List, Mapping

from pandas import DataFrame

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFRelationship

__all__ = ["load_imdf_relationships"]


def load_imdf_relationships(
    dataframes: Mapping[IMDFFeatureType, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFRelationship]],
) -> None:
    if IMDFFeatureType.relationship.value in dataframes:
        for ith_row, relationship_row in dataframes[
            IMDFFeatureType.relationship.value
        ].iterrows():
            relationship_dict = relationship_row.to_dict()

            relationship = IMDFRelationship(**relationship_dict)
            out[IMDFFeatureType.relationship].append(relationship)
