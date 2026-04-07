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

import collections.abc
import functools
import itertools
from typing import Iterable, Iterator, Sequence, TypeVar

ColumnIdentifierType = str


T = TypeVar("T")

# Further optimizations possible:
# * Support mapping operators
# * Support insertions and deletions


class ChainedSequence(collections.abc.Sequence[T]):
    """
    Memory-optimized sequence from composing chain of existing sequences.

    Will use the provided parts as underlying storage - so do not mutate provided parts.
    May merge small underlying parts for better access performance.
    """

    def __init__(self, *parts: Sequence[T]):
        # Could build an index that makes random access faster?
        self._parts: tuple[Sequence[T], ...] = tuple(
            _defrag_parts(_flatten_parts(parts))
        )

    def __getitem__(self, index):
        if isinstance(index, slice):
            return tuple(self)[index]
        if index < 0:
            index = len(self) + index
        if index < 0:
            raise IndexError("Index out of bounds")

        offset = 0
        for part in self._parts:
            if (index - offset) < len(part):
                return part[index - offset]
            offset += len(part)
        raise IndexError("Index out of bounds")

    @functools.cache
    def __len__(self):
        return sum(map(len, self._parts))

    def __iter__(self):
        for part in self._parts:
            yield from part


def _flatten_parts(parts: Iterable[Sequence[T]]) -> Iterator[Sequence[T]]:
    for part in parts:
        if isinstance(part, ChainedSequence):
            yield from part._parts
        else:
            yield part


# Should be a cache-friendly chunk size?
_TARGET_SIZE = 128
_MAX_MERGABLE = 32


def _defrag_parts(parts: Iterable[Sequence[T]]) -> Iterator[Sequence[T]]:
    """
    Merge small chunks into larger chunks for better performance.
    """
    parts_queue: list[Sequence[T]] = []
    queued_items = 0
    for part in parts:
        # too big, just yield from the buffer
        if len(part) > _MAX_MERGABLE:
            yield from parts_queue
            parts_queue = []
            queued_items = 0
            yield part
        else:  # can be merged, so lets add to the queue
            parts_queue.append(part)
            queued_items += len(part)
        # if queue has reached target size, merge, dump and reset queue
        if queued_items >= _TARGET_SIZE:
            yield tuple(itertools.chain(*parts_queue))
            parts_queue = []
            queued_items = 0

    yield from parts_queue
