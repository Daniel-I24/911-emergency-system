from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Node:
    """
    Represents a node in a doubly linked list.

    Each node stores a patient information dictionary and two pointers:
    - next: points to the next node
    - prev: points to the previous node
    """

    data: dict[str, Any]
    next: Optional["Node"] = None
    prev: Optional["Node"] = None

