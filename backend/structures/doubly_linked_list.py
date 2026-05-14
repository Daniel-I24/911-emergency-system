from __future__ import annotations

from typing import Any, Optional

from backend.models.node import Node


class DoublyLinkedList:
    """
    A doubly linked list implementation specialized for storing patient dictionaries.

    The list maintains head, tail, and length to support O(1) insertion/removal at both ends
    and bidirectional traversal through next/prev pointers.
    """

    def __init__(self) -> None:
        """Initialize an empty doubly linked list."""
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._length: int = 0

    def get_length(self) -> int:
        """Return the total number of nodes in the list."""
        return self._length

    def append(self, data: dict[str, Any]) -> None:
        """Add a patient dictionary to the end of the list."""
        new_node = Node(data=data)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
            self._length = 1
            return

        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node
        self._length += 1

    def prepend(self, data: dict[str, Any]) -> None:
        """Add a patient dictionary to the start of the list."""
        new_node = Node(data=data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self._length = 1
            return

        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node
        self._length += 1

    def _node_at(self, index: int) -> Node:
        """Return the node at a given index (index must be valid)."""
        if self.head is None or self.tail is None:
            raise IndexError("List is empty.")

        from_head_distance = index
        from_tail_distance = (self._length - 1) - index

        if from_head_distance <= from_tail_distance:
            current = self.head
            current_index = 0
            while current_index < index:
                if current.next is None:
                    raise IndexError("Index out of bounds.")
                current = current.next
                current_index += 1
            return current

        current = self.tail
        current_index = self._length - 1
        while current_index > index:
            if current.prev is None:
                raise IndexError("Index out of bounds.")
            current = current.prev
            current_index -= 1
        return current

    def insert(self, index: int, data: dict[str, Any]) -> None:
        """Insert a patient dictionary at a specific position."""
        if index < 0 or index > self._length:
            raise IndexError("Index out of bounds.")

        if index == 0:
            self.prepend(data=data)
            return

        if index == self._length:
            self.append(data=data)
            return

        new_node = Node(data=data)
        current = self._node_at(index=index)
        previous = current.prev

        new_node.prev = previous
        new_node.next = current

        if previous is not None:
            previous.next = new_node
        current.prev = new_node

        self._length += 1

    def remove(self, index: int) -> dict[str, Any]:
        """Remove a node by position and return its stored patient dictionary."""
        if index < 0 or index >= self._length:
            raise IndexError("Index out of bounds.")

        if self.head is None or self.tail is None:
            raise IndexError("List is empty.")

        if self._length == 1:
            removed = self.head
            self.head = None
            self.tail = None
            self._length = 0
            return removed.data

        if index == 0:
            removed = self.head
            new_head = removed.next
            if new_head is None:
                raise IndexError("Index out of bounds.")
            new_head.prev = None
            removed.next = None
            self.head = new_head
            self._length -= 1
            return removed.data

        if index == self._length - 1:
            removed = self.tail
            new_tail = removed.prev
            if new_tail is None:
                raise IndexError("Index out of bounds.")
            new_tail.next = None
            removed.prev = None
            self.tail = new_tail
            self._length -= 1
            return removed.data

        removed = self._node_at(index=index)
        previous = removed.prev
        next_node = removed.next

        if previous is None or next_node is None:
            raise IndexError("Index out of bounds.")

        previous.next = next_node
        next_node.prev = previous
        removed.prev = None
        removed.next = None
        self._length -= 1
        return removed.data

    def get_all(self) -> list[dict[str, Any]]:
        """Return all stored patient dictionaries in order."""
        patients: list[dict[str, Any]] = []
        current = self.head
        while current is not None:
            patients.append(current.data)
            current = current.next
        return patients

    def find_by_id(self, patient_id: int) -> Optional[dict[str, Any]]:
        """Search for a patient by ID and return its dictionary if found."""
        current = self.head
        while current is not None:
            current_id = current.data.get("id")
            if current_id == patient_id:
                return current.data
            current = current.next
        return None
