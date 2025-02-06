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
import itertools
from typing import cast, Optional, Sequence, Set, Tuple

import bigframes.core.expression
import bigframes.core.guid
import bigframes.core.identifiers
import bigframes.core.join_def
import bigframes.core.nodes
import bigframes.core.window_spec
import bigframes.operations.aggregations

# Combination of selects and additive nodes can be merged as an explicit keyless "row join"
ALIGNABLE_NODES = (
    bigframes.core.nodes.SelectionNode,
    bigframes.core.nodes.ProjectionNode,
    bigframes.core.nodes.WindowOpNode,
    bigframes.core.nodes.PromoteOffsetsNode,
    bigframes.core.nodes.InNode,
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
                bigframes.core.nodes.InNode,
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
        curr_node = curr_node.child_nodes[0]


def try_row_join(
    l_node: bigframes.core.nodes.BigFrameNode,
    r_node: bigframes.core.nodes.BigFrameNode,
    join_keys: Tuple[Tuple[str, str], ...],
) -> Optional[bigframes.core.nodes.BigFrameNode]:
    """Joins the two nodes"""
    divergent_node = first_shared_descendent(
        {l_node, r_node}, descendable_types=ALIGNABLE_NODES
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
    combined_selection = l_selection + r_selection

    def _linearize_trees(
        base_tree: bigframes.core.nodes.BigFrameNode,
        append_tree: bigframes.core.nodes.BigFrameNode,
    ) -> bigframes.core.nodes.BigFrameNode:
        """Linearize two divergent tree who only diverge through different additive nodes."""
        # base case: append tree does not have any divergent nodes to linearize
        if append_tree == divergent_node:
            return base_tree

        assert isinstance(append_tree, bigframes.core.nodes.AdditiveNode)
        return append_tree.replace_additive_base(
            _linearize_trees(base_tree, append_tree.additive_base)
        )

    merged_node = _linearize_trees(l_node, r_node)
    return bigframes.core.nodes.SelectionNode(merged_node, combined_selection)


def pull_up_selection(
    node: bigframes.core.nodes.BigFrameNode,
    stop: bigframes.core.nodes.BigFrameNode,
    rename_vars: bool = False,
) -> Tuple[
    bigframes.core.nodes.BigFrameNode,
    Tuple[bigframes.core.nodes.AliasedRef, ...],
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
            bigframes.core.nodes.AliasedRef.identity(field.id) for field in node.fields
        )
    # InNode needs special handling, as its a binary node, but row identity is from left side only.
    # TODO: Merge code with unary op paths
    if isinstance(node, bigframes.core.nodes.InNode):
        child_node, child_selections = pull_up_selection(
            node.left_child, stop=stop, rename_vars=rename_vars
        )
        mapping = {out: ref.id for ref, out in child_selections}

        new_in_node: bigframes.core.nodes.InNode = dataclasses.replace(
            node, left_child=child_node
        )
        new_in_node = new_in_node.remap_refs(mapping)
        if rename_vars:
            new_in_node = cast(
                bigframes.core.nodes.InNode,
                new_in_node.remap_vars(
                    {node.indicator_col: bigframes.core.identifiers.ColumnId.unique()}
                ),
            )
        added_selection = tuple(
            (
                bigframes.core.nodes.AliasedRef(
                    bigframes.core.expression.DerefOp(new_in_node.indicator_col),
                    node.indicator_col,
                ),
            )
        )
        new_selection = child_selections + added_selection
        return new_in_node, new_selection

    if isinstance(node, bigframes.core.nodes.AdditiveNode):
        child_node, child_selections = pull_up_selection(
            node.additive_base, stop, rename_vars=rename_vars
        )
        mapping = {out: ref.id for ref, out in child_selections}
        new_node: bigframes.core.nodes.BigFrameNode = node.replace_additive_base(
            child_node
        )
        new_node = new_node.remap_refs(mapping)
        if rename_vars:
            var_renames = {
                field.id: bigframes.core.identifiers.ColumnId.unique()
                for field in node.added_fields
            }
            new_node = new_node.remap_vars(var_renames)
        else:
            var_renames = {}
        assert isinstance(new_node, bigframes.core.nodes.AdditiveNode)
        added_selections = tuple(
            bigframes.core.nodes.AliasedRef.identity(field.id).remap_refs(var_renames)
            for field in node.added_fields
        )
        new_selection = child_selections + added_selections
        return new_node, new_selection
    elif isinstance(node, bigframes.core.nodes.SelectionNode):
        child_node, child_selections = pull_up_selection(
            node.child, stop, rename_vars=rename_vars
        )
        mapping = {out: ref.id for ref, out in child_selections}
        return child_node, tuple(
            ref.remap_refs(mapping) for ref in node.input_output_pairs
        )
    raise ValueError(f"Couldn't pull up select from node: {node}")


## Traversal helpers
def first_shared_descendent(
    roots: Set[bigframes.core.nodes.BigFrameNode],
    descendable_types: Tuple[type[bigframes.core.nodes.BigFrameNode], ...],
) -> Optional[bigframes.core.nodes.BigFrameNode]:
    if not roots:
        return None
    if len(roots) == 1:
        return next(iter(roots))

    min_height = min(root.height for root in roots)

    def descend(
        root: bigframes.core.nodes.BigFrameNode,
    ) -> Sequence[bigframes.core.nodes.BigFrameNode]:
        # Special case to not descend into right side of IsInNode
        if isinstance(root, bigframes.core.nodes.AdditiveNode):
            return (root.additive_base,)
        return root.child_nodes

    roots_to_descend = set(root for root in roots if root.height > min_height)
    if not roots_to_descend:
        roots_to_descend = roots
    if any(not isinstance(root, descendable_types) for root in roots_to_descend):
        return None
    as_is = roots - roots_to_descend
    descended = set(
        itertools.chain.from_iterable(descend(root) for root in roots_to_descend)
    )
    return first_shared_descendent(as_is.union(descended), descendable_types)
