from typing import Optional

from .base import IMDFFeature

__all__ = ["IMDFAddress"]


class IMDFAddress(IMDFFeature):
    # geometry: None # Nonsense

    address: str = ""  # No default value for STRICT!
    locality: str = ""  # No default value for STRICT!
    country: str = ""  # No default value for STRICT! # actual type ISO 3166

    province: Optional[str] = None  # actual type ISO 3166-2
    unit: Optional[str] = None
    postal_code: Optional[str] = None
    postal_code_ext: Optional[str] = None
    postal_code_vanity: Optional[str] = None
