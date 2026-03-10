# Copyright 2024 Google LLC
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

import typing

from bigframes.core import identifiers, nodes


def _create_mapping_operator(
    id_def_remapping_by_node: dict[
        nodes.BigFrameNode, dict[identifiers.ColumnId, identifiers.ColumnId]
    ],
    id_ref_remapping_by_node: dict[
        nodes.BigFrameNode, dict[identifiers.ColumnId, identifiers.ColumnId]
    ],
):
    """
    Builds a remapping operator that uses predefined local remappings for ids.

    Args:
        id_remapping_by_node: A mapping from nodes to their local remappings.

    Returns:
        A remapping operator.
    """

    def _mapping_operator(node: nodes.BigFrameNode) -> nodes.BigFrameNode:
        # Step 1: Get the local remapping for the current node.
        local_def_remaps = id_def_remapping_by_node[node]
        local_ref_remaps = id_ref_remapping_by_node[node]

        result = node.remap_vars(local_def_remaps)
        result = result.remap_refs(local_ref_remaps)

        return result

    return _mapping_operator


def remap_variables(
    root: nodes.BigFrameNode,
    id_generator: typing.Iterator[identifiers.ColumnId],
) -> typing.Tuple[
    nodes.BigFrameNode,
    dict[identifiers.ColumnId, identifiers.ColumnId],
]:
    """Remaps `ColumnId`s in the expression tree to be deterministic and sequential.

    This function performs a post-order traversal. It recursively remaps children
    nodes first, then remaps the current node's references and definitions.

    Note: this will convert a DAG to a tree by duplicating shared nodes.

    Args:
        root: The root node of the expression tree.
        id_generator: An iterator that yields new column IDs.

    Returns:
        A tuple of the new root node and a mapping from old to new column IDs
        visible to the parent node.
    """
    # step 1: defined remappings for each individual unique node
    # step 2: top down traversal to apply remappings (mappings are value-based, so bottom-up doesn't work)

    id_def_remaps: dict[
        nodes.BigFrameNode, dict[identifiers.ColumnId, identifiers.ColumnId]
    ] = {}
    id_ref_remaps: dict[
        nodes.BigFrameNode, dict[identifiers.ColumnId, identifiers.ColumnId]
    ] = {}
    for node in root.iter_nodes_topo():  # bottom up
        local_def_remaps = {
            col_id: next(id_generator) for col_id in node.node_defined_ids
        }
        id_def_remaps[node] = local_def_remaps

        local_ref_remaps = {}

        # InNode is special case as ID scope inherited purely from left side
        inheriting_nodes = (
            [node.child_nodes[0]]
            if isinstance(node, nodes.InNode)
            else node.child_nodes
        )
        for child in inheriting_nodes:  # inherit ref and def mappings from children
            if not child.defines_namespace:  # these nodes represent new id spaces
                local_ref_remaps.update(
                    {
                        old_id: new_id
                        for old_id, new_id in id_ref_remaps[child].items()
                        if old_id in child.ids
                    }
                )
            local_ref_remaps.update(id_def_remaps[child])
        id_ref_remaps[node] = local_ref_remaps

    # have to do top down to preserve node identities
    return (
        root.top_down(_create_mapping_operator(id_def_remaps, id_ref_remaps)),
        # Only used by unit tests
        {
            old_id: (id_def_remaps[root] | id_ref_remaps[root])[old_id]
            for old_id in root.ids
        },
    )
