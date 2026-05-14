from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    """
    Implementación genérica de una pila (Stack) utilizando una lista,
    basada en el principio LIFO (Last In, First Out).
    """
    def __init__(self) -> None:
        """
        Inicializa una pila vacía.
        """
        self._items: list[T] = []

    def is_empty(self) -> bool:
        """
        Verifica si la pila está vacía.
        
        Returns:
            bool: True si la pila está vacía, False en caso contrario.
        """
        return len(self._items) == 0

    def push(self, item: T) -> None:
        """
        Agrega un elemento a la parte superior de la pila.
        
        Args:
            item (T): El elemento a agregar.
        """
        self._items.append(item)

    def pop(self) -> T:
        """
        Elimina y devuelve el elemento en la parte superior de la pila.
        
        Returns:
            T: El elemento superior de la pila.
            
        Raises:
            IndexError: Si la pila está vacía.
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items.pop()

    def top(self) -> T:
        """
        Devuelve el elemento en la parte superior de la pila sin eliminarlo.
        
        Returns:
            T: El elemento superior de la pila.
            
        Raises:
            IndexError: Si la pila está vacía.
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items[-1]

    def size(self) -> int:
        """
        Devuelve el número de elementos en la pila.
        
        Returns:
            int: La cantidad de elementos.
        """
        return len(self._items)

