from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Node:
    """
    Representa un nodo básico utilizado en estructuras de datos enlazadas (como listas enlazadas).
    
    Attributes:
        data (dict[str, Any]): Un diccionario que contiene los datos almacenados en este nodo.
        next (Optional["Node"]): Una referencia al siguiente nodo en la estructura. Por defecto es None.
    """
    data: dict[str, Any]
    next: Optional["Node"] = None

