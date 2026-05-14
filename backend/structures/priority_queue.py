from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PriorityItem:
    """
    Representa un elemento dentro de la cola de prioridad.
    
    Attributes:
        rank (int): Nivel de prioridad (menor valor numérico indica mayor prioridad real).
        sequence (int): Secuencia de inserción para resolver empates (FIFO para prioridades iguales).
        call_id (int): Identificador de la llamada de emergencia asociada.
    """
    rank: int
    sequence: int
    call_id: int


class PriorityQueue:
    """
    Estructura de datos de cola de prioridad para gestionar las llamadas de emergencia
    basado en su nivel de prioridad (rank) y orden de llegada (sequence).
    """
    def __init__(self) -> None:
        """
        Inicializa una cola de prioridad vacía con un contador de secuencia en cero.
        """
        self._items: list[PriorityItem] = []
        self._sequence: int = 0

    def is_empty(self) -> bool:
        """
        Verifica si la cola de prioridad está vacía.
        
        Returns:
            bool: True si está vacía, False en caso contrario.
        """
        return len(self._items) == 0

    def enqueue(self, *, call_id: int, rank: int) -> None:
        """
        Agrega una nueva llamada a la cola de prioridad, insertándola en la posición
        correcta según su nivel de prioridad y secuencia de llegada.
        
        Args:
            call_id (int): ID de la llamada.
            rank (int): Nivel de prioridad de la llamada.
        """
        item = PriorityItem(rank=rank, sequence=self._sequence, call_id=call_id)
        self._sequence += 1

        index = 0
        while index < len(self._items):
            current = self._items[index]
            if (item.rank, item.sequence) < (current.rank, current.sequence):
                break
            index += 1
        self._items.insert(index, item)

    def pop_next(self) -> int:
        """
        Elimina y devuelve el ID de la llamada con la mayor prioridad (y que llegó primero).
        
        Returns:
            int: El ID de la llamada extraída.
            
        Raises:
            IndexError: Si la cola de prioridad está vacía.
        """
        if self.is_empty():
            raise IndexError("PriorityQueue is empty")
        return self._items.pop(0).call_id

    def remove(self, *, call_id: int) -> bool:
        """
        Elimina una llamada específica de la cola de prioridad basándose en su ID.
        
        Args:
            call_id (int): El ID de la llamada a eliminar.
            
        Returns:
            bool: True si se encontró y eliminó la llamada, False en caso contrario.
        """
        for idx, item in enumerate(self._items):
            if item.call_id == call_id:
                self._items.pop(idx)
                return True
        return False

    def peek_next(self) -> int:
        """
        Devuelve el ID de la llamada de mayor prioridad sin eliminarla de la cola.
        
        Returns:
            int: El ID de la llamada.
            
        Raises:
            IndexError: Si la cola está vacía.
        """
        if self.is_empty():
            raise IndexError("PriorityQueue is empty")
        return self._items[0].call_id

    def to_list(self) -> list[int]:
        """
        Convierte la cola de prioridad en una lista de IDs de llamadas ordenadas por prioridad.
        
        Returns:
            list[int]: Lista de IDs de llamadas en orden.
        """
        return [item.call_id for item in self._items]

