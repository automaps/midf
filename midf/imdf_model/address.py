from typing import Any

from .other import IMDFFeature

__all__ = ["IMDFAddress"]

class IMDFAddress(IMDFFeature):
  address: Any = ""
  unit: Any = None
  locality: Any = ""
  province: Any = None
  country: Any = ""
  postal_code: Any = None
  postal_code_ext: Any = None
  postal_code_vanity: Any = None
