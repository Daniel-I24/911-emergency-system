from __future__ import annotations

from typing import Any, Callable, Optional

from backend.models.node import Node


class SinglyLinkedList:
    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._length: int = 0

    def get_length(self) -> int:
        return self._length

    def append(self, data: dict[str, Any]) -> None:
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
        new_node = Node(data=data, next=self.head)
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self._length += 1

    def insert(self, index: int, data: dict[str, Any]) -> None:
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
        items: list[dict[str, Any]] = []
        current = self.head
        while current is not None:
            items.append(current.data)
            current = current.next
        return items

    def find_first(self, predicate: Callable[[dict[str, Any]], bool]) -> Optional[dict[str, Any]]:
        current = self.head
        while current is not None:
            if predicate(current.data):
                return current.data
            current = current.next
        return None

    def _node_at(self, index: int) -> Node:
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

