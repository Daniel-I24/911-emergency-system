from __future__ import annotations

from collections import deque
from typing import Deque, Generic, TypeVar

T = TypeVar("T")


class Queue(Generic[T]):
    """
    Implementación genérica de una cola (Queue) utilizando collections.deque,
    basada en el principio FIFO (First In, First Out).
    """
    def __init__(self) -> None:
        """
        Inicializa una cola vacía.
        """
        self._items: Deque[T] = deque()

    def is_empty(self) -> bool:
        """
        Verifica si la cola está vacía.
        
        Returns:
            bool: True si la cola está vacía, False en caso contrario.
        """
        return len(self._items) == 0

    def enqueue(self, item: T) -> None:
        """
        Agrega un elemento al final de la cola.
        
        Args:
            item (T): El elemento a agregar.
        """
        self._items.append(item)

    def dequeue(self) -> T:
        """
        Elimina y devuelve el elemento en la parte frontal de la cola.
        
        Returns:
            T: El elemento frontal de la cola.
            
        Raises:
            IndexError: Si la cola está vacía.
        """
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items.popleft()

    def front(self) -> T:
        """
        Devuelve el elemento en la parte frontal de la cola sin eliminarlo.
        
        Returns:
            T: El elemento frontal de la cola.
            
        Raises:
            IndexError: Si la cola está vacía.
        """
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items[0]

    def rear(self) -> T:
        """
        Devuelve el elemento en la parte trasera (final) de la cola sin eliminarlo.
        
        Returns:
            T: El elemento en la parte trasera de la cola.
            
        Raises:
            IndexError: Si la cola está vacía.
        """
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items[-1]

    def size(self) -> int:
        """
        Devuelve el número de elementos en la cola.
        
        Returns:
            int: La cantidad de elementos.
        """
        return len(self._items)

    def to_list(self) -> list[T]:
        """
        Convierte la cola en una lista estándar de Python.
        
        Returns:
            list[T]: Una lista que contiene todos los elementos de la cola.
        """
        return list(self._items)

