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

import collections
from typing import Dict, Generic, Hashable, Iterable, Iterator, Tuple, TypeVar

import bigframes.core.ordered_sets as sets

T = TypeVar("T", bound=Hashable)


class DiGraph(Generic[T]):
    def __init__(self, nodes: Iterable[T], edges: Iterable[Tuple[T, T]]):
        self._parents: Dict[T, sets.InsertionOrderedSet[T]] = collections.defaultdict(
            sets.InsertionOrderedSet
        )
        self._children: Dict[T, sets.InsertionOrderedSet[T]] = collections.defaultdict(
            sets.InsertionOrderedSet
        )
        self._sinks: sets.InsertionOrderedSet[T] = sets.InsertionOrderedSet()
        for node in nodes:
            self._children[node]
            self._parents[node]
            self._sinks.add(node)
        for src, dst in edges:
            assert src in self.nodes
            assert dst in self.nodes
            self._children[src].add(dst)
            self._parents[dst].add(src)
            # sinks have no children
            if src in self._sinks:
                self._sinks.remove(src)

    @property
    def nodes(self):
        # should be the same set of ids as self._parents
        return self._children.keys()

    @property
    def sinks(self) -> Iterable[T]:
        return self._sinks

    @property
    def empty(self):
        return len(self.nodes) == 0

    def parents(self, node: T) -> Iterator[T]:
        assert node in self._parents
        yield from self._parents[node]

    def children(self, node: T) -> Iterator[T]:
        assert node in self._children
        yield from self._children[node]

    def remove_node(self, node: T) -> None:
        for child in self._children[node]:
            self._parents[child].remove(node)
        for parent in self._parents[node]:
            self._children[parent].remove(node)
            if len(self._children[parent]) == 0:
                self._sinks.add(parent)
        del self._children[node]
        del self._parents[node]
        if node in self._sinks:
            self._sinks.remove(node)
