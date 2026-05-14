from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PriorityItem:
    rank: int
    sequence: int
    call_id: int


class PriorityQueue:
    def __init__(self) -> None:
        self._items: list[PriorityItem] = []
        self._sequence: int = 0

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def enqueue(self, *, call_id: int, rank: int) -> None:
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
        if self.is_empty():
            raise IndexError("PriorityQueue is empty")
        return self._items.pop(0).call_id

    def remove(self, *, call_id: int) -> bool:
        for idx, item in enumerate(self._items):
            if item.call_id == call_id:
                self._items.pop(idx)
                return True
        return False

    def peek_next(self) -> int:
        if self.is_empty():
            raise IndexError("PriorityQueue is empty")
        return self._items[0].call_id

    def to_list(self) -> list[int]:
        return [item.call_id for item in self._items]

