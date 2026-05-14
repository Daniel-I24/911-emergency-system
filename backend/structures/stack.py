from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items.pop()

    def top(self) -> T:
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items[-1]

    def size(self) -> int:
        return len(self._items)

