# Copyright 2026 Google LLC
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

import dataclasses
import threading
from collections import OrderedDict
from typing import Optional

from bigframes.core import local_data, nodes


@dataclasses.dataclass(frozen=True)
class CachedRelation:
    table: local_data.ManagedArrowTable
    is_complete: bool = False


class PeekCache:
    """
    Thread-safe LRU cache for storing local samples or complete copies of query relations.
    This enables fast iteration on subsequent compatible operations.
    """

    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self._cache: OrderedDict[nodes.BigFrameNode, CachedRelation] = OrderedDict()
        self._lock = threading.Lock()

    def get(self, key: nodes.BigFrameNode) -> Optional[CachedRelation]:
        with self._lock:
            if key not in self._cache:
                return None
            # Move to end (most recently used)
            self._cache.move_to_end(key)
            return self._cache[key]

    def put(
        self,
        key: nodes.BigFrameNode,
        table: local_data.ManagedArrowTable,
        is_complete: bool = False,
    ) -> None:
        with self._lock:
            value = CachedRelation(table, is_complete)
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = value
            if len(self._cache) > self.capacity:
                self._cache.popitem(last=False)

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()


def substitute_peek_cached_subplans(
    root: nodes.BigFrameNode,
    peek_cache: PeekCache,
    min_rows_required: Optional[int],
) -> nodes.BigFrameNode:
    """
    Recursively replaces subplans in the tree that have a cached local relation
    in the peek cache with a ReadLocalNode, provided that:
    1. The cached relation is complete (contains the entire dataset).
    2. Or, all ancestors of the subplan are compatible with running on a sample,
       and the cached sample contains at least the required number of rows.
    """
    # Intermediate nodes that preserve the semantic validity of a sample.
    # WindowOpNode, AggregateNode, OrderByNode, JoinNode, etc. are excluded
    # because evaluating them on a sample breaks semantic contracts.
    _COMPATIBLE_ANCESTOR_CLASSES = (
        nodes.SelectionNode,
        nodes.ProjectionNode,
        nodes.FilterNode,
        nodes.PromoteOffsetsNode,
    )

    def traverse(
        node: nodes.BigFrameNode, ancestors_compatible: bool
    ) -> nodes.BigFrameNode:
        cached_entry = peek_cache.get(node)
        if cached_entry is not None:
            if cached_entry.is_complete or (
                ancestors_compatible
                and min_rows_required is not None
                and cached_entry.table.data.num_rows >= min_rows_required
            ):
                # Replace the node with a ReadLocalNode containing the cached relation
                scan_list = nodes.ScanList(
                    tuple(
                        nodes.ScanItem(field.id, field.id.name) for field in node.fields
                    )
                )
                session = node.session if node.session is not None else root.session
                return nodes.ReadLocalNode(
                    local_data_source=cached_entry.table,
                    scan_list=scan_list,
                    session=session,
                )

        # If we didn't replace, recursively transform children
        is_current_compatible = isinstance(node, _COMPATIBLE_ANCESTOR_CLASSES)
        next_ancestors_compatible = ancestors_compatible and is_current_compatible

        return node.transform_children(
            lambda child: traverse(child, next_ancestors_compatible)
        )

    return traverse(root, True)
