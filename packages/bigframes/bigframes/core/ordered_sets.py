# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

from typing import (
    Any,
    Dict,
    Generic,
    Hashable,
    Iterable,
    Iterator,
    MutableSet,
    Optional,
    TypeVar,
)

T = TypeVar("T", bound=Hashable)


class _ListNode(Generic[T]):
    """A private class representing a node in the doubly linked list."""

    __slots__ = ("value", "prev", "next")

    def __init__(
        self,
        value: Optional[T],
        prev: Optional[_ListNode[T]] = None,
        next_node: Optional[_ListNode[T]] = None,
    ):
        self.value = value
        self.prev = prev
        self.next = next_node


class InsertionOrderedSet(MutableSet[T]):
    """
    An ordered set implementation that maintains the order in which elements were
    first inserted. It provides O(1) average time complexity for addition,
    membership testing, and deletion, similar to Python's built-in set.
    """

    def __init__(self, iterable: Optional[Iterable] = None):
        # Dictionary mapping element value -> _ListNode instance for O(1) lookup
        self._dict: Dict[T, _ListNode[T]] = {}

        # Sentinel nodes for the doubly linked list. They don't hold actual data.
        # head.next is the first element, tail.prev is the last element.
        self._head: _ListNode[T] = _ListNode(None)
        self._tail: _ListNode[T] = _ListNode(None)
        self._head.next = self._tail
        self._tail.prev = self._head

        if iterable:
            self.update(iterable)

    def __len__(self) -> int:
        """Return the number of elements in the set."""
        return len(self._dict)

    def __contains__(self, item: Any) -> bool:
        """Check if an item is a member of the set (O(1) average)."""
        return item in self._dict

    def __iter__(self) -> Iterator[T]:
        """Iterate over the elements in insertion order (O(N))."""
        current = self._head.next
        while current is not self._tail:
            yield current.value  # type: ignore
            current = current.next  # type: ignore

    def _unlink_node(self, node: _ListNode[T]) -> None:
        """Helper to remove a node from the linked list."""
        node.prev.next = node.next  # type: ignore
        node.next.prev = node.prev  # type: ignore
        # Clear references to aid garbage collection
        node.prev = None
        node.next = None

    def _append_node(self, node: _ListNode[T]) -> None:
        """Helper to append a node to the end of the linked list."""
        last_node = self._tail.prev
        last_node.next = node  # type: ignore
        node.prev = last_node
        node.next = self._tail
        self._tail.prev = node

    def add(self, value: T) -> None:
        """Add an element to the set. If it exists, its order is unchanged (O(1) average)."""
        if value not in self._dict:
            new_node = _ListNode(value)
            self._dict[value] = new_node
            self._append_node(new_node)

    def discard(self, value: T) -> None:
        """Remove an element from the set if it is a member (O(1) average)."""
        if value in self._dict:
            node = self._dict.pop(value)
            self._unlink_node(node)

    def remove(self, value: T) -> None:
        """Remove an element from the set; raises KeyError if not present (O(1) average)."""
        if value not in self._dict:
            raise KeyError(f"{value} not found in set")
        self.discard(value)

    def update(self, *others: Iterable[T]) -> None:
        """Update the set with the union of itself and all others."""
        for other in others:
            for item in other:
                self.add(item)

    def clear(self) -> None:
        """Remove all elements from the set."""
        self._dict.clear()
        self._head.next = self._tail
        self._tail.prev = self._head

    def _replace_contents(self, source: InsertionOrderedSet) -> InsertionOrderedSet:
        """Helper method for inplace operators to transfer content from a result set."""
        self.clear()
        for item in source:
            self.add(item)
        return self

    def __repr__(self) -> str:
        """Representation of the set."""
        return f"InsertionOrderedSet({list(self)})"
