from dataclasses import dataclass
from typing import Optional


@dataclass
class Door:
  type: Optional[str] = None
  automatic: bool = False
  material: Optional[str] = None
