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
from typing import Iterable, Optional, Tuple

import bigframes.core.expression
import bigframes.core.guid
import bigframes.core.identifiers
import bigframes.core.join_def
import bigframes.core.nodes
import bigframes.core.window_spec
import bigframes.operations.aggregations

# Additive nodes leave existing columns completely intact, and only add new columns to the end
ADDITIVE_NODES = (
    bigframes.core.nodes.ProjectionNode,
    bigframes.core.nodes.WindowOpNode,
    bigframes.core.nodes.PromoteOffsetsNode,
)
# Combination of selects and additive nodes can be merged as an explicit keyless "row join"
ALIGNABLE_NODES = (
    *ADDITIVE_NODES,
    bigframes.core.nodes.SelectionNode,
)


@dataclasses.dataclass(frozen=True)
class ExpressionSpec:
    expression: bigframes.core.expression.Expression
    node: bigframes.core.nodes.BigFrameNode


def get_expression_spec(
    node: bigframes.core.nodes.BigFrameNode, id: bigframes.core.identifiers.ColumnId
) -> ExpressionSpec:
    """Normalizes column value by chaining expressions across multiple selection and projection nodes if possible.
    This normalization helps identify whether columns are equivalent.
    """
    # TODO: While we chain expression fragments from different nodes
    # we could further normalize with constant folding and other scalar expression rewrites
    expression: bigframes.core.expression.Expression = (
        bigframes.core.expression.DerefOp(id)
    )
    curr_node = node
    while True:
        if isinstance(curr_node, bigframes.core.nodes.SelectionNode):
            select_mappings = {
                col_id: ref for ref, col_id in curr_node.input_output_pairs
            }
            expression = expression.bind_refs(
                select_mappings, allow_partial_bindings=True
            )
        elif isinstance(curr_node, bigframes.core.nodes.ProjectionNode):
            proj_mappings = {col_id: expr for expr, col_id in curr_node.assignments}
            expression = expression.bind_refs(
                proj_mappings, allow_partial_bindings=True
            )
        elif isinstance(
            curr_node,
            (
                bigframes.core.nodes.WindowOpNode,
                bigframes.core.nodes.PromoteOffsetsNode,
            ),
        ):
            if set(expression.column_references).isdisjoint(
                field.id for field in curr_node.added_fields
            ):
                # we don't yet have a way of normalizing window ops into a ExpressionSpec, which only
                # handles normalizing scalar expressions at the moment.
                pass
            else:
                return ExpressionSpec(expression, curr_node)
        else:
            return ExpressionSpec(expression, curr_node)
        curr_node = curr_node.child


def try_row_join(
    l_node: bigframes.core.nodes.BigFrameNode,
    r_node: bigframes.core.nodes.BigFrameNode,
    join_keys: Tuple[Tuple[str, str], ...],
) -> Optional[bigframes.core.nodes.BigFrameNode]:
    """Joins the two nodes"""
    divergent_node = first_shared_descendent(
        l_node, r_node, descendable_types=ALIGNABLE_NODES
    )
    if divergent_node is None:
        return None
    # check join keys are equivalent by normalizing the expressions as much as posisble
    # instead of just comparing ids
    for l_key, r_key in join_keys:
        # Caller is block, so they still work with raw strings rather than ids
        left_id = bigframes.core.identifiers.ColumnId(l_key)
        right_id = bigframes.core.identifiers.ColumnId(r_key)
        if get_expression_spec(l_node, left_id) != get_expression_spec(
            r_node, right_id
        ):
            return None

    l_node, l_selection = pull_up_selection(l_node, stop=divergent_node)
    r_node, r_selection = pull_up_selection(
        r_node, stop=divergent_node, rename_vars=True
    )  # Rename only right vars to avoid collisions with left vars
    combined_selection = (*l_selection, *r_selection)

    def _linearize_trees(
        base_tree: bigframes.core.nodes.BigFrameNode,
        append_tree: bigframes.core.nodes.BigFrameNode,
    ) -> bigframes.core.nodes.BigFrameNode:
        """Linearize two divergent tree who only diverge through different additive nodes."""
        # base case: append tree does not have any divergent nodes to linearize
        if append_tree == divergent_node:
            return base_tree
        else:
            assert isinstance(append_tree, ADDITIVE_NODES)
            return append_tree.replace_child(
                _linearize_trees(base_tree, append_tree.child)
            )

    merged_node = _linearize_trees(l_node, r_node)
    return bigframes.core.nodes.SelectionNode(merged_node, combined_selection)


def pull_up_selection(
    node: bigframes.core.nodes.BigFrameNode,
    stop: bigframes.core.nodes.BigFrameNode,
    rename_vars: bool = False,
) -> Tuple[
    bigframes.core.nodes.BigFrameNode,
    Tuple[
        Tuple[bigframes.core.expression.DerefOp, bigframes.core.identifiers.ColumnId],
        ...,
    ],
]:
    """Remove all selection nodes above the base node. Returns stripped tree.

    Args:
        node (BigFrameNode):
            The node from which to pull up SelectionNode ops
        rename_vars (bool):
            If true, will rename projected columns to new unique ids.

    Returns:
        BigFrameNode, Selections
    """
    if node == stop:  # base case
        return node, tuple(
            (bigframes.core.expression.DerefOp(field.id), field.id)
            for field in node.fields
        )
    assert isinstance(node, (bigframes.core.nodes.SelectionNode, *ADDITIVE_NODES))
    child_node, child_selections = pull_up_selection(
        node.child, stop, rename_vars=rename_vars
    )
    mapping = {out: ref.id for ref, out in child_selections}
    if isinstance(node, ADDITIVE_NODES):
        new_node: bigframes.core.nodes.BigFrameNode = node.replace_child(child_node)
        new_node = new_node.remap_refs(mapping)
        if rename_vars:
            var_renames = {
                field.id: bigframes.core.identifiers.ColumnId.unique()
                for field in node.added_fields
            }
            new_node = new_node.remap_vars(var_renames)
        else:
            var_renames = {}
        assert isinstance(new_node, ADDITIVE_NODES)
        added_selections = (
            (
                bigframes.core.expression.DerefOp(var_renames.get(field.id, field.id)),
                field.id,
            )
            for field in node.added_fields
        )
        new_selection = (*child_selections, *added_selections)
        return new_node, new_selection
    elif isinstance(node, bigframes.core.nodes.SelectionNode):
        new_selection = tuple(
            (
                bigframes.core.expression.DerefOp(mapping[ref.id]),
                out,
            )
            for ref, out in node.input_output_pairs
        )
        return child_node, new_selection
    raise ValueError(f"Couldn't pull up select from node: {node}")


## Traversal helpers
def first_shared_descendent(
    left: bigframes.core.nodes.BigFrameNode,
    right: bigframes.core.nodes.BigFrameNode,
    descendable_types: Tuple[type[bigframes.core.nodes.UnaryNode], ...],
) -> Optional[bigframes.core.nodes.BigFrameNode]:
    l_path = tuple(descend(left, descendable_types))
    r_path = tuple(descend(right, descendable_types))
    if l_path[-1] != r_path[-1]:
        return None

    for l_node, r_node in zip(l_path[-len(r_path) :], r_path[-len(l_path) :]):
        if l_node == r_node:
            return l_node
    # should be impossible, as l_path[-1] == r_path[-1]
    raise ValueError()


def descend(
    root: bigframes.core.nodes.BigFrameNode,
    descendable_types: Tuple[type[bigframes.core.nodes.UnaryNode], ...],
) -> Iterable[bigframes.core.nodes.BigFrameNode]:
    yield root
    if isinstance(root, descendable_types):
        yield from descend(root.child, descendable_types)
