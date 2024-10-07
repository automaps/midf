from typing import List, Optional

from attr import dataclass

from midf.typing import MIDFFeature
from .address_level import MIDFVenue

__all__ = ["MIDFAddress"]

@dataclass
class MIDFAddress(MIDFFeature):
  address: str

  locality: str
  country: str
  province: Optional[str] = None

  unit: Optional[str] = None

  postal_code: Optional[str] = None
  postal_code_ext: Optional[str] = None
  postal_code_vanity: Optional[str] = None

  venues: Optional[List[MIDFVenue]] = None
