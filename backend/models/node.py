from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Node:
    data: dict[str, Any]
    next: Optional["Node"] = None

