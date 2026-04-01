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
import dataclasses
import functools
from typing import Optional

from bigframes.core import nodes
import bigframes.core.rewrite.slices


def try_reduce_to_table_scan(root: nodes.BigFrameNode) -> Optional[nodes.ReadTableNode]:
    for node in root.unique_nodes():
        if not isinstance(node, (nodes.ReadTableNode, nodes.SelectionNode)):
            return None
    result = root.bottom_up(merge_scan)
    if isinstance(result, nodes.ReadTableNode):
        return result
    return None


def try_reduce_to_local_scan(
    node: nodes.BigFrameNode,
) -> Optional[tuple[nodes.ReadLocalNode, Optional[int]]]:
    """Create a ReadLocalNode with optional limit, if possible.

    Similar to ReadApiSemiExecutor._try_adapt_plan.
    """
    node, limit = bigframes.core.rewrite.slices.pull_out_limit(node)

    if not all(
        map(
            lambda x: isinstance(x, (nodes.ReadLocalNode, nodes.SelectionNode)),
            node.unique_nodes(),
        )
    ):
        return None
    result = node.bottom_up(merge_scan)
    if isinstance(result, nodes.ReadLocalNode):
        return result, limit
    return None


@functools.singledispatch
def merge_scan(node: nodes.BigFrameNode) -> nodes.BigFrameNode:
    return node


@merge_scan.register
def _(node: nodes.SelectionNode) -> nodes.BigFrameNode:
    if not isinstance(node.child, (nodes.ReadTableNode, nodes.ReadLocalNode)):
        return node
    if node.has_multi_referenced_ids:
        return node
    if isinstance(node, nodes.ReadLocalNode) and node.offsets_col is not None:
        return node
    selection = {
        aliased_ref.ref.id: aliased_ref.id for aliased_ref in node.input_output_pairs
    }
    new_scan_list = node.child.scan_list.project(selection)
    return dataclasses.replace(node.child, scan_list=new_scan_list)
