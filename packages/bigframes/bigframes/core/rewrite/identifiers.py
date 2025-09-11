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

import dataclasses
import typing

from bigframes.core import identifiers, nodes


# TODO: May as well just outright remove selection nodes in this process.
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
    # Step 1: Recursively remap children to get their new nodes and ID mappings.
    new_child_nodes: list[nodes.BigFrameNode] = []
    new_child_mappings: list[dict[identifiers.ColumnId, identifiers.ColumnId]] = []
    for child in root.child_nodes:
        new_child, child_mappings = remap_variables(child, id_generator=id_generator)
        new_child_nodes.append(new_child)
        new_child_mappings.append(child_mappings)

    # Step 2: Transform children to use their new nodes.
    remapped_children: dict[nodes.BigFrameNode, nodes.BigFrameNode] = {
        child: new_child for child, new_child in zip(root.child_nodes, new_child_nodes)
    }
    new_root = root.transform_children(lambda node: remapped_children[node])

    # Step 3: Transform the current node using the mappings from its children.
    downstream_mappings: dict[identifiers.ColumnId, identifiers.ColumnId] = {
        k: v for mapping in new_child_mappings for k, v in mapping.items()
    }
    if isinstance(new_root, nodes.InNode):
        new_root = typing.cast(nodes.InNode, new_root)
        new_root = dataclasses.replace(
            new_root,
            left_col=new_root.left_col.remap_column_refs(
                new_child_mappings[0], allow_partial_bindings=True
            ),
            right_col=new_root.right_col.remap_column_refs(
                new_child_mappings[1], allow_partial_bindings=True
            ),
        )
    else:
        new_root = new_root.remap_refs(downstream_mappings)

    # Step 4: Create new IDs for columns defined by the current node.
    node_defined_mappings = {
        old_id: next(id_generator) for old_id in root.node_defined_ids
    }
    new_root = new_root.remap_vars(node_defined_mappings)

    new_root._validate()

    # Step 5: Determine which mappings to propagate up to the parent.
    if root.defines_namespace:
        # If a node defines a new namespace (e.g., a join), mappings from its
        # children are not visible to its parents.
        mappings_for_parent = node_defined_mappings
    else:
        # Otherwise, pass up the combined mappings from children and the current node.
        mappings_for_parent = downstream_mappings | node_defined_mappings

    return new_root, mappings_for_parent
