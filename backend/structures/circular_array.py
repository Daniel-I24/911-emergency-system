from __future__ import annotations

from typing import Generic, Sequence, TypeVar

T = TypeVar("T")


class CircularArray(Generic[T]):
    """
    Estructura de datos de un arreglo circular. 
    Permite iterar continuamente sobre una secuencia finita de elementos.
    """
    def __init__(self, items: Sequence[T] | None = None) -> None:
        """
        Inicializa el arreglo circular con una secuencia de elementos opcional.
        
        Args:
            items (Sequence[T] | None): Secuencia inicial de elementos.
        """
        self._items: list[T] = list(items) if items is not None else []
        self._index: int = 0

    def set_items(self, items: Sequence[T]) -> None:
        """
        Reemplaza los elementos actuales con una nueva secuencia y reinicia el índice.
        
        Args:
            items (Sequence[T]): La nueva secuencia de elementos.
        """
        self._items = list(items)
        self._index = 0

    def is_empty(self) -> bool:
        """
        Verifica si el arreglo circular está vacío.
        
        Returns:
            bool: True si está vacío, False en caso contrario.
        """
        return len(self._items) == 0

    def next(self) -> T:
        """
        Devuelve el elemento actual y avanza el índice al siguiente. 
        Si llega al final, el índice vuelve a 0 de forma circular.
        
        Returns:
            T: El elemento actual en la secuencia.
            
        Raises:
            IndexError: Si el arreglo circular está vacío.
        """
        if self.is_empty():
            raise IndexError("CircularArray is empty")
        value = self._items[self._index]
        self._index = (self._index + 1) % len(self._items)
        return value

    def to_list(self) -> list[T]:
        """
        Convierte el arreglo circular a una lista estándar de Python.
        
        Returns:
            list[T]: Una copia de los elementos subyacentes.
        """
        return list(self._items)

