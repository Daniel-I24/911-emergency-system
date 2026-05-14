from __future__ import annotations

from typing import Generic, Sequence, TypeVar

T = TypeVar("T")


class CircularArray(Generic[T]):
    def __init__(self, items: Sequence[T] | None = None) -> None:
        self._items: list[T] = list(items) if items is not None else []
        self._index: int = 0

    def set_items(self, items: Sequence[T]) -> None:
        self._items = list(items)
        self._index = 0

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def next(self) -> T:
        if self.is_empty():
            raise IndexError("CircularArray is empty")
        value = self._items[self._index]
        self._index = (self._index + 1) % len(self._items)
        return value

    def to_list(self) -> list[T]:
        return list(self._items)

