from __future__ import annotations

from typing import Any, Callable, Optional

from backend.models.node import Node


class SinglyLinkedList:
    """
    Implementación de una lista enlazada simple para almacenar diccionarios de datos.
    Mantiene referencias tanto a la cabeza (head) como a la cola (tail) para optimizar inserciones al final.
    """
    def __init__(self) -> None:
        """
        Inicializa una lista enlazada vacía.
        """
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._length: int = 0

    def get_length(self) -> int:
        """
        Obtiene la longitud actual de la lista.
        
        Returns:
            int: Número de nodos en la lista.
        """
        return self._length

    def append(self, data: dict[str, Any]) -> None:
        """
        Agrega un nuevo nodo con los datos proporcionados al final de la lista.
        
        Args:
            data (dict[str, Any]): Los datos a almacenar en el nuevo nodo.
        """
        new_node = Node(data=data)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
            self._length = 1
            return

        self.tail.next = new_node
        self.tail = new_node
        self._length += 1

    def prepend(self, data: dict[str, Any]) -> None:
        """
        Agrega un nuevo nodo con los datos proporcionados al principio de la lista.
        
        Args:
            data (dict[str, Any]): Los datos a almacenar en el nuevo nodo.
        """
        new_node = Node(data=data, next=self.head)
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self._length += 1

    def insert(self, index: int, data: dict[str, Any]) -> None:
        """
        Inserta un nuevo nodo en el índice especificado.
        
        Args:
            index (int): La posición donde insertar (0-indexado).
            data (dict[str, Any]): Los datos a almacenar.
            
        Raises:
            IndexError: Si el índice está fuera de los límites de la lista.
        """
        if index < 0 or index > self._length:
            raise IndexError("Index out of bounds")

        if index == 0:
            self.prepend(data=data)
            return

        if index == self._length:
            self.append(data=data)
            return

        previous = self._node_at(index=index - 1)
        new_node = Node(data=data, next=previous.next)
        previous.next = new_node
        self._length += 1

    def remove(self, index: int) -> dict[str, Any]:
        """
        Elimina el nodo en el índice especificado y devuelve sus datos.
        
        Args:
            index (int): La posición del nodo a eliminar.
            
        Returns:
            dict[str, Any]: Los datos del nodo eliminado.
            
        Raises:
            IndexError: Si la lista está vacía o el índice está fuera de rango.
        """
        if index < 0 or index >= self._length:
            raise IndexError("Index out of bounds")

        if self.head is None:
            raise IndexError("List is empty")

        if index == 0:
            removed = self.head
            self.head = removed.next
            removed.next = None
            self._length -= 1
            if self._length == 0:
                self.tail = None
            return removed.data

        previous = self._node_at(index=index - 1)
        removed = previous.next
        if removed is None:
            raise IndexError("Index out of bounds")

        previous.next = removed.next
        removed.next = None
        self._length -= 1

        if index == self._length:
            self.tail = previous

        return removed.data

    def get_all(self) -> list[dict[str, Any]]:
        """
        Recupera los datos de todos los nodos en la lista y los devuelve en una lista de Python.
        
        Returns:
            list[dict[str, Any]]: Una lista con todos los diccionarios de datos en orden.
        """
        items: list[dict[str, Any]] = []
        current = self.head
        while current is not None:
            items.append(current.data)
            current = current.next
        return items

    def find_first(self, predicate: Callable[[dict[str, Any]], bool]) -> Optional[dict[str, Any]]:
        """
        Busca el primer elemento que cumpla con la condición especificada por el predicado.
        
        Args:
            predicate (Callable): Función que toma los datos y devuelve True si hay coincidencia.
            
        Returns:
            Optional[dict[str, Any]]: Los datos encontrados, o None si no se encuentra ninguno.
        """
        current = self.head
        while current is not None:
            if predicate(current.data):
                return current.data
            current = current.next
        return None

    def _node_at(self, index: int) -> Node:
        """
        Función auxiliar privada para obtener el nodo en un índice específico.
        
        Args:
            index (int): El índice del nodo a recuperar.
            
        Returns:
            Node: El nodo encontrado.
            
        Raises:
            IndexError: Si la lista está vacía o el índice está fuera de rango.
        """
        if self.head is None:
            raise IndexError("List is empty")

        current = self.head
        current_index = 0
        while current_index < index:
            if current.next is None:
                raise IndexError("Index out of bounds")
            current = current.next
            current_index += 1
        return current

