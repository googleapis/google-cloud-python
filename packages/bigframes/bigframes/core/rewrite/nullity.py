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

from bigframes.core import nodes
import dataclasses


def simplify_join(node: nodes.BigFrameNode) -> nodes.BigFrameNode:
    """Simplify a join node by removing nullity checks."""
    # if join conditions are provably non-null, we can set nulls_equal=False
    if isinstance(node, nodes.JoinNode):
        # even better, we can always make nulls_equal false, but wrap the join keys in coalesce
        # to handle nulls correctly, this is more granular than the current implementation
        for left_ref, right_ref in node.conditions:
            if (
                node.left_child.field_by_id[left_ref.id].nullable
                and node.right_child.field_by_id[right_ref.id].nullable
            ):
                return node
        return dataclasses.replace(node, nulls_equal=False)
    elif isinstance(node, nodes.InNode):
        if (
            node.left_child.field_by_id[node.left_col.id].nullable
            and node.right_child.fields[0].nullable
        ):
            return node
        return dataclasses.replace(node, nulls_equal=False)
    else:
        return node
