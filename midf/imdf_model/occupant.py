from typing import Any, Dict, Optional, Union

from .base import IMDFFeature

__all__ = ["IMDFOccupant"]

from ..enums import IMDFFeatureType, IMDFOccupantCategory
from ..midf_typing import Temporality


class IMDFOccupant(IMDFFeature):
    # geometry: None # Nonsense

    name: Dict[str, str] = {}

    category: Union[
        IMDFOccupantCategory, str
    ]  # TODO: Some occupants have a category that is not in the enum, so we allow a
    # string here, but we should validate it, it is not valid, we should raise an error. # TODO: REMOVE FOR
    #  STRICT
    anchor_id: str = ""
    hours: Any = None
    phone: Any = None
    website: Any = None
    validity: Optional[Temporality] = None
    correlation_id: Any = None

    def to_imdf_spec_feature(self) -> dict[str, Any]:
        out = self.model_dump()

        out["feature_type"] = IMDFFeatureType.occupant.value
        out["geometry"] = None

        return out
