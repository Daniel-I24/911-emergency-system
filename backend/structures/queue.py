from __future__ import annotations

from collections import deque
from typing import Deque, Generic, TypeVar

T = TypeVar("T")


class Queue(Generic[T]):
    def __init__(self) -> None:
        self._items: Deque[T] = deque()

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def enqueue(self, item: T) -> None:
        self._items.append(item)

    def dequeue(self) -> T:
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items.popleft()

    def front(self) -> T:
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items[0]

    def rear(self) -> T:
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items[-1]

    def size(self) -> int:
        return len(self._items)

    def to_list(self) -> list[T]:
        return list(self._items)

