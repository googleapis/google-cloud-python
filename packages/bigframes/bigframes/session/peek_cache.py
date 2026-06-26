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

import threading
from collections import OrderedDict
from typing import Optional

from bigframes.core import local_data, nodes


class PeekCache:
    """
    Thread-safe LRU cache for storing local samples of query relations.
    This enables fast iteration on subsequent compatible operations.
    """

    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self._cache: OrderedDict[nodes.BigFrameNode, local_data.ManagedArrowTable] = (
            OrderedDict()
        )
        self._lock = threading.Lock()

    def get(self, key: nodes.BigFrameNode) -> Optional[local_data.ManagedArrowTable]:
        with self._lock:
            if key not in self._cache:
                return None
            # Move to end (most recently used)
            self._cache.move_to_end(key)
            return self._cache[key]

    def put(self, key: nodes.BigFrameNode, value: local_data.ManagedArrowTable) -> None:
        with self._lock:
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
    min_rows_required: int,
) -> nodes.BigFrameNode:
    """
    Recursively replaces subplans in the tree that have a cached local sample
    in the peek cache with a ReadLocalNode, provided that all ancestors
    of the subplan are compatible with running on a sample, and the cached
    sample contains at least the required number of rows.
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
        if ancestors_compatible:
            cached_sample = peek_cache.get(node)
            if (
                cached_sample is not None
                and cached_sample.data.num_rows >= min_rows_required
            ):
                # Replace the node with a ReadLocalNode containing the cached sample
                scan_list = nodes.ScanList(
                    tuple(
                        nodes.ScanItem(field.id, field.id.name) for field in node.fields
                    )
                )
                session = node.session if node.session is not None else root.session
                return nodes.ReadLocalNode(
                    local_data_source=cached_sample,
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
