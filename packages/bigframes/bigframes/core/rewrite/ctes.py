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

from collections import defaultdict

from bigframes.core import nodes


def extract_ctes(root: nodes.BigFrameNode) -> nodes.BigFrameNode:
    # identify candidates
    node_parents: dict[nodes.BigFrameNode, int] = defaultdict(int)
    for parent in root.unique_nodes():
        for child in parent.child_nodes:
            node_parents[child] += 1

    # everywhere a multi-parent node is referenced, wrap it in a CTE node
    def insert_cte_markers(node: nodes.BigFrameNode) -> nodes.BigFrameNode:
        def _add_cte_if_needed(child: nodes.BigFrameNode) -> nodes.BigFrameNode:
            if node_parents[child] > 1:
                return nodes.CteNode(child)
            return child

        if isinstance(node, nodes.CteNode):
            # don't re-wrap CTE nodes
            return node

        return node.transform_children(_add_cte_if_needed)

    return root.top_down(insert_cte_markers)
