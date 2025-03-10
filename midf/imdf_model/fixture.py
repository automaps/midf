from typing import Any, Mapping, Optional, Union

from .base import IMDFFeature

__all__ = ["IMDFFixture"]

from ..enums import IMDFFixtureCategory
from ..midf_typing import Polygonal


class IMDFFixture(IMDFFeature):
    geometry: Polygonal
    level_id: str

    category: Union[
        IMDFFixtureCategory, str
    ]  # TODO: Some fixtures have a category that is not in the enum, so we allow a
    # string here, but we should validate it, it is not valid, we should raise an error. # TODO: REMOVE FOR
    #  STRICT
    anchor_id: Any = None

    display_point: Optional[Any] = None

    name: Optional[Mapping[str, str]] = None
    alt_name: Optional[Mapping[str, str]] = None
