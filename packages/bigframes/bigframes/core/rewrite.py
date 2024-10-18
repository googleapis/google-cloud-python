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
import functools
import itertools
from typing import cast, Mapping, Optional, Sequence, Tuple

import bigframes.core.expression as scalar_exprs
import bigframes.core.guid as guids
import bigframes.core.identifiers as ids
import bigframes.core.join_def as join_defs
import bigframes.core.nodes as nodes
import bigframes.core.ordering as order
import bigframes.core.slices as slices
import bigframes.operations as ops

Selection = Tuple[Tuple[scalar_exprs.Expression, ids.ColumnId], ...]

REWRITABLE_NODE_TYPES = (
    nodes.SelectionNode,
    nodes.ProjectionNode,
    nodes.FilterNode,
    nodes.ReversedNode,
    nodes.OrderByNode,
)


@dataclasses.dataclass(frozen=True)
class SquashedSelect:
    """Squash nodes together until target node, separating out the projection, filter and reordering expressions."""

    root: nodes.BigFrameNode
    columns: Tuple[Tuple[scalar_exprs.Expression, ids.ColumnId], ...]
    predicate: Optional[scalar_exprs.Expression]
    ordering: Tuple[order.OrderingExpression, ...]
    reverse_root: bool = False

    @classmethod
    def from_node_span(
        cls, node: nodes.BigFrameNode, target: nodes.BigFrameNode
    ) -> SquashedSelect:
        if node == target:
            selection = tuple(
                (scalar_exprs.DerefOp(id), id) for id in get_node_column_ids(node)
            )
            return cls(node, selection, None, ())

        if isinstance(node, nodes.SelectionNode):
            return cls.from_node_span(node.child, target).select(
                node.input_output_pairs
            )
        elif isinstance(node, nodes.ProjectionNode):
            return cls.from_node_span(node.child, target).project(node.assignments)
        elif isinstance(node, nodes.FilterNode):
            return cls.from_node_span(node.child, target).filter(node.predicate)
        elif isinstance(node, nodes.ReversedNode):
            return cls.from_node_span(node.child, target).reverse()
        elif isinstance(node, nodes.OrderByNode):
            return cls.from_node_span(node.child, target).order_with(node.by)
        else:
            raise ValueError(f"Cannot rewrite node {node}")

    @property
    def column_lookup(self) -> Mapping[ids.ColumnId, scalar_exprs.Expression]:
        return {col_id: expr for expr, col_id in self.columns}

    def select(
        self, input_output_pairs: Tuple[Tuple[scalar_exprs.DerefOp, ids.ColumnId], ...]
    ) -> SquashedSelect:
        new_columns = tuple(
            (
                input.bind_refs(self.column_lookup),
                output,
            )
            for input, output in input_output_pairs
        )
        return SquashedSelect(
            self.root, new_columns, self.predicate, self.ordering, self.reverse_root
        )

    def project(
        self, projection: Tuple[Tuple[scalar_exprs.Expression, ids.ColumnId], ...]
    ) -> SquashedSelect:
        existing_columns = self.columns
        new_columns = tuple(
            (expr.bind_refs(self.column_lookup), id) for expr, id in projection
        )
        return SquashedSelect(
            self.root,
            (*existing_columns, *new_columns),
            self.predicate,
            self.ordering,
            self.reverse_root,
        )

    def filter(self, predicate: scalar_exprs.Expression) -> SquashedSelect:
        if self.predicate is None:
            new_predicate = predicate.bind_refs(self.column_lookup)
        else:
            new_predicate = ops.and_op.as_expr(
                self.predicate, predicate.bind_refs(self.column_lookup)
            )
        return SquashedSelect(
            self.root, self.columns, new_predicate, self.ordering, self.reverse_root
        )

    def reverse(self) -> SquashedSelect:
        new_ordering = tuple(expr.with_reverse() for expr in self.ordering)
        return SquashedSelect(
            self.root, self.columns, self.predicate, new_ordering, not self.reverse_root
        )

    def order_with(self, by: Tuple[order.OrderingExpression, ...]):
        adjusted_orderings = [
            order_part.bind_refs(self.column_lookup) for order_part in by
        ]
        new_ordering = (*adjusted_orderings, *self.ordering)
        return SquashedSelect(
            self.root, self.columns, self.predicate, new_ordering, self.reverse_root
        )

    def can_merge(
        self,
        right: SquashedSelect,
        join_keys: Tuple[join_defs.CoalescedColumnMapping, ...],
    ) -> bool:
        """Determines whether the two selections can be merged into a single selection."""
        r_exprs_by_id = {id.name: expr for expr, id in right.columns}
        l_exprs_by_id = {id.name: expr for expr, id in self.columns}
        l_join_exprs = [
            l_exprs_by_id[join_key.left_source_id] for join_key in join_keys
        ]
        r_join_exprs = [
            r_exprs_by_id[join_key.right_source_id] for join_key in join_keys
        ]

        if self.root != right.root:
            return False
        if len(l_join_exprs) != len(r_join_exprs):
            return False
        if any(l_expr != r_expr for l_expr, r_expr in zip(l_join_exprs, r_join_exprs)):
            return False
        return True

    def merge(
        self,
        right: SquashedSelect,
        join_type: join_defs.JoinType,
        join_keys: Tuple[join_defs.CoalescedColumnMapping, ...],
        mappings: Tuple[join_defs.JoinColumnMapping, ...],
    ) -> SquashedSelect:
        if self.root != right.root:
            raise ValueError("Cannot merge expressions with different roots")
        # Mask columns and remap names to expected schema
        lselection = self.columns
        rselection = right.columns
        if join_type == "inner":
            new_predicate = and_predicates(self.predicate, right.predicate)
        elif join_type == "outer":
            new_predicate = or_predicates(self.predicate, right.predicate)
        elif join_type == "left":
            new_predicate = self.predicate
        elif join_type == "right":
            new_predicate = right.predicate

        l_relative, r_relative = relative_predicates(self.predicate, right.predicate)
        lmask = l_relative if join_type in {"right", "outer"} else None
        rmask = r_relative if join_type in {"left", "outer"} else None
        new_columns = merge_expressions(
            join_keys, mappings, lselection, rselection, lmask, rmask
        )

        # Reconstruct ordering
        reverse_root = self.reverse_root
        if join_type == "right":
            new_ordering = right.ordering
            reverse_root = right.reverse_root
        elif join_type == "outer":
            if lmask is not None:
                prefix = order.OrderingExpression(lmask, order.OrderingDirection.DESC)
                left_ordering = tuple(
                    order.OrderingExpression(
                        apply_mask(ref.scalar_expression, lmask),
                        ref.direction,
                        ref.na_last,
                    )
                    for ref in self.ordering
                )
                right_ordering = (
                    tuple(
                        order.OrderingExpression(
                            apply_mask(ref.scalar_expression, rmask),
                            ref.direction,
                            ref.na_last,
                        )
                        for ref in right.ordering
                    )
                    if rmask
                    else right.ordering
                )
                new_ordering = (prefix, *left_ordering, *right_ordering)
            else:
                new_ordering = self.ordering
        elif join_type in {"inner", "left"}:
            new_ordering = self.ordering
        else:
            raise ValueError(f"Unexpected join type {join_type}")
        return SquashedSelect(
            self.root, new_columns, new_predicate, new_ordering, reverse_root
        )

    def expand(self) -> nodes.BigFrameNode:
        # Safest to apply predicates first, as it may filter out inputs that cannot be handled by other expressions
        root = self.root
        if self.reverse_root:
            root = nodes.ReversedNode(child=root)
        if self.predicate:
            root = nodes.FilterNode(child=root, predicate=self.predicate)
        if self.ordering:
            root = nodes.OrderByNode(child=root, by=self.ordering)
        selection = tuple((scalar_exprs.DerefOp(id), id) for _, id in self.columns)
        return nodes.SelectionNode(
            child=nodes.ProjectionNode(child=root, assignments=self.columns),
            input_output_pairs=selection,
        )


def join_as_projection(
    l_node: nodes.BigFrameNode,
    r_node: nodes.BigFrameNode,
    join_keys: Tuple[join_defs.CoalescedColumnMapping, ...],
    mappings: Tuple[join_defs.JoinColumnMapping, ...],
    how: join_defs.JoinType,
) -> Optional[nodes.BigFrameNode]:
    rewrite_common_node = common_selection_root(l_node, r_node)
    if rewrite_common_node is not None:
        left_side = SquashedSelect.from_node_span(l_node, rewrite_common_node)
        right_side = SquashedSelect.from_node_span(r_node, rewrite_common_node)
        if not left_side.can_merge(right_side, join_keys):
            # Most likely because join keys didn't match
            return None
        merged = left_side.merge(right_side, how, join_keys, mappings)
        assert (
            merged is not None
        ), "Couldn't merge nodes. This shouldn't happen. Please share full stacktrace with the BigQuery DataFrames team at bigframes-feedback@google.com."
        return merged.expand()
    else:
        return None


def merge_expressions(
    join_keys: Tuple[join_defs.CoalescedColumnMapping, ...],
    mappings: Tuple[join_defs.JoinColumnMapping, ...],
    lselection: Selection,
    rselection: Selection,
    lmask: Optional[scalar_exprs.Expression],
    rmask: Optional[scalar_exprs.Expression],
) -> Selection:
    new_selection: Selection = tuple()
    # Assumption is simple ids
    l_exprs_by_id = {id.name: expr for expr, id in lselection}
    r_exprs_by_id = {id.name: expr for expr, id in rselection}
    for key in join_keys:
        # Join keys expressions are equivalent on both sides, so can choose either left or right key
        assert l_exprs_by_id[key.left_source_id] == r_exprs_by_id[key.right_source_id]
        expr = l_exprs_by_id[key.left_source_id]
        id = key.destination_id
        new_selection = (*new_selection, (expr, ids.ColumnId(id)))
    for mapping in mappings:
        if mapping.source_table == join_defs.JoinSide.LEFT:
            expr = l_exprs_by_id[mapping.source_id]
            if lmask is not None:
                expr = apply_mask(expr, lmask)
        else:  # Right
            expr = r_exprs_by_id[mapping.source_id]
            if rmask is not None:
                expr = apply_mask(expr, rmask)
        new_selection = (*new_selection, (expr, ids.ColumnId(mapping.destination_id)))
    return new_selection


def and_predicates(
    expr1: Optional[scalar_exprs.Expression], expr2: Optional[scalar_exprs.Expression]
) -> Optional[scalar_exprs.Expression]:
    if expr1 is None:
        return expr2
    if expr2 is None:
        return expr1
    left_predicates = decompose_conjunction(expr1)
    right_predicates = decompose_conjunction(expr2)
    # remove common predicates
    all_predicates = itertools.chain(
        left_predicates, [p for p in right_predicates if p not in left_predicates]
    )
    return merge_predicates(list(all_predicates))


def or_predicates(
    expr1: Optional[scalar_exprs.Expression], expr2: Optional[scalar_exprs.Expression]
) -> Optional[scalar_exprs.Expression]:
    if (expr1 is None) or (expr2 is None):
        return None
    # TODO(tbergeron): Factor out common predicates
    return ops.or_op.as_expr(expr1, expr2)


def relative_predicates(
    expr1: Optional[scalar_exprs.Expression], expr2: Optional[scalar_exprs.Expression]
) -> Tuple[Optional[scalar_exprs.Expression], Optional[scalar_exprs.Expression]]:
    left_predicates = decompose_conjunction(expr1) if expr1 else ()
    right_predicates = decompose_conjunction(expr2) if expr2 else ()
    left_relative = tuple(
        pred for pred in left_predicates if pred not in right_predicates
    )
    right_relative = tuple(
        pred for pred in right_predicates if pred not in left_predicates
    )
    return merge_predicates(left_relative), merge_predicates(right_relative)


def apply_mask(
    expr: scalar_exprs.Expression, mask: scalar_exprs.Expression
) -> scalar_exprs.Expression:
    return ops.where_op.as_expr(expr, mask, scalar_exprs.const(None))


def merge_predicates(
    predicates: Sequence[scalar_exprs.Expression],
) -> Optional[scalar_exprs.Expression]:
    if len(predicates) == 0:
        return None

    return functools.reduce(ops.and_op.as_expr, predicates)


def decompose_conjunction(
    expr: scalar_exprs.Expression,
) -> Tuple[scalar_exprs.Expression, ...]:
    if isinstance(expr, scalar_exprs.OpExpression) and isinstance(
        expr.op, type(ops.and_op)
    ):
        return tuple(
            itertools.chain.from_iterable(decompose_conjunction(i) for i in expr.inputs)
        )
    else:
        return (expr,)


def get_node_column_ids(node: nodes.BigFrameNode) -> Tuple[ids.ColumnId, ...]:
    return tuple(field.id for field in node.fields)


def common_selection_root(
    l_tree: nodes.BigFrameNode, r_tree: nodes.BigFrameNode
) -> Optional[nodes.BigFrameNode]:
    """Find common subtree between join subtrees"""
    l_node = l_tree
    l_nodes: set[nodes.BigFrameNode] = set()
    while isinstance(l_node, REWRITABLE_NODE_TYPES):
        l_nodes.add(l_node)
        l_node = l_node.child
    l_nodes.add(l_node)

    r_node = r_tree
    while isinstance(r_node, REWRITABLE_NODE_TYPES):
        if r_node in l_nodes:
            return r_node
        r_node = r_node.child

    if r_node in l_nodes:
        return r_node
    return None


def pullup_limit_from_slice(
    root: nodes.BigFrameNode,
) -> Tuple[nodes.BigFrameNode, Optional[int]]:
    """
    This is a BQ-sql specific optimization that can be helpful as ORDER BY LIMIT is more efficient than WHERE + ROW_NUMBER().

    Only use this if writing to an unclustered table. Clustering is not compatible with ORDER BY.
    """
    if isinstance(root, nodes.SliceNode):
        # head case
        # More cases could be handled, but this is by far the most important, as it is used by df.head(), df[:N]
        if root.is_limit:
            assert not root.start
            assert root.step == 1
            assert root.stop is not None
            limit = root.stop
            new_root, prior_limit = pullup_limit_from_slice(root.child)
            if (prior_limit is not None) and (prior_limit < limit):
                limit = prior_limit
            return new_root, limit
    elif (
        isinstance(root, (nodes.SelectionNode, nodes.ProjectionNode))
        and root.row_preserving
    ):
        new_child, prior_limit = pullup_limit_from_slice(root.child)
        if prior_limit is not None:
            return root.transform_children(lambda _: new_child), prior_limit
    # Most ops don't support pulling up slice, like filter, agg, join, etc.
    return root, None


def replace_slice_ops(root: nodes.BigFrameNode) -> nodes.BigFrameNode:
    # TODO: we want to pull up some slices into limit op if near root.
    if isinstance(root, nodes.SliceNode):
        root = root.transform_children(replace_slice_ops)
        return rewrite_slice(cast(nodes.SliceNode, root))
    else:
        return root.transform_children(replace_slice_ops)


def rewrite_slice(node: nodes.SliceNode):
    slice_def = (node.start, node.stop, node.step)

    # no-op (eg. df[::1])
    if slices.is_noop(slice_def, node.child.row_count):
        return node.child

    # No filtering, just reverse (eg. df[::-1])
    if slices.is_reverse(slice_def, node.child.row_count):
        return nodes.ReversedNode(node.child)

    if node.child.row_count:
        slice_def = slices.to_forward_offsets(slice_def, node.child.row_count)
    return slice_as_filter(node.child, *slice_def)


def slice_as_filter(
    node: nodes.BigFrameNode, start: Optional[int], stop: Optional[int], step: int
) -> nodes.BigFrameNode:
    if (
        ((start is None) or (start >= 0))
        and ((stop is None) or (stop >= 0))
        and (step > 0)
    ):
        node_w_offset = add_offsets(node)
        predicate = convert_simple_slice(
            scalar_exprs.DerefOp(node_w_offset.col_id), start or 0, stop, step
        )
        filtered = nodes.FilterNode(node_w_offset, predicate)
        return drop_cols(filtered, (node_w_offset.col_id,))

    # fallback cases, generate both forward and backward offsets
    if step < 0:
        forward_offsets = add_offsets(node)
        reversed_offsets = add_offsets(nodes.ReversedNode(forward_offsets))
        dual_indexed = reversed_offsets
    else:
        reversed_offsets = add_offsets(nodes.ReversedNode(node))
        forward_offsets = add_offsets(nodes.ReversedNode(reversed_offsets))
        dual_indexed = forward_offsets
    default_start = 0 if step >= 0 else -1
    predicate = convert_complex_slice(
        scalar_exprs.DerefOp(forward_offsets.col_id),
        scalar_exprs.DerefOp(reversed_offsets.col_id),
        start if (start is not None) else default_start,
        stop,
        step,
    )
    filtered = nodes.FilterNode(dual_indexed, predicate)
    return drop_cols(filtered, (forward_offsets.col_id, reversed_offsets.col_id))


def add_offsets(node: nodes.BigFrameNode) -> nodes.PromoteOffsetsNode:
    # Allow providing custom id generator?
    offsets_id = ids.ColumnId(guids.generate_guid())
    return nodes.PromoteOffsetsNode(node, offsets_id)


def drop_cols(
    node: nodes.BigFrameNode, drop_cols: Tuple[ids.ColumnId, ...]
) -> nodes.SelectionNode:
    # adding a whole node that redefines the schema is a lot of overhead, should do something more efficient
    selections = tuple(
        (scalar_exprs.DerefOp(id), id) for id in node.ids if id not in drop_cols
    )
    return nodes.SelectionNode(node, selections)


def convert_simple_slice(
    offsets: scalar_exprs.Expression,
    start: int = 0,
    stop: Optional[int] = None,
    step: int = 1,
) -> scalar_exprs.Expression:
    """Performs slice but only for positive step size."""
    assert start >= 0
    assert (stop is None) or (stop >= 0)

    conditions = []
    if start > 0:
        conditions.append(ops.ge_op.as_expr(offsets, scalar_exprs.const(start)))
    if (stop is not None) and (stop >= 0):
        conditions.append(ops.lt_op.as_expr(offsets, scalar_exprs.const(stop)))
    if step > 1:
        start_diff = ops.sub_op.as_expr(offsets, scalar_exprs.const(start))
        step_cond = ops.eq_op.as_expr(
            ops.mod_op.as_expr(start_diff, scalar_exprs.const(step)),
            scalar_exprs.const(0),
        )
        conditions.append(step_cond)

    return merge_predicates(conditions) or scalar_exprs.const(True)


def convert_complex_slice(
    forward_offsets: scalar_exprs.Expression,
    reverse_offsets: scalar_exprs.Expression,
    start: int,
    stop: Optional[int],
    step: int = 1,
) -> scalar_exprs.Expression:
    conditions = []
    assert step != 0
    if start or ((start is not None) and step < 0):
        if start > 0 and step > 0:
            start_cond = ops.ge_op.as_expr(forward_offsets, scalar_exprs.const(start))
        elif start >= 0 and step < 0:
            start_cond = ops.le_op.as_expr(forward_offsets, scalar_exprs.const(start))
        elif start < 0 and step > 0:
            start_cond = ops.le_op.as_expr(
                reverse_offsets, scalar_exprs.const(-start - 1)
            )
        else:
            assert start < 0 and step < 0
            start_cond = ops.ge_op.as_expr(
                reverse_offsets, scalar_exprs.const(-start - 1)
            )
        conditions.append(start_cond)
    if stop is not None:
        if stop >= 0 and step > 0:
            stop_cond = ops.lt_op.as_expr(forward_offsets, scalar_exprs.const(stop))
        elif stop >= 0 and step < 0:
            stop_cond = ops.gt_op.as_expr(forward_offsets, scalar_exprs.const(stop))
        elif stop < 0 and step > 0:
            stop_cond = ops.gt_op.as_expr(
                reverse_offsets, scalar_exprs.const(-stop - 1)
            )
        else:
            assert (stop < 0) and (step < 0)
            stop_cond = ops.lt_op.as_expr(
                reverse_offsets, scalar_exprs.const(-stop - 1)
            )
        conditions.append(stop_cond)
    if step != 1:
        if step > 1 and start >= 0:
            start_diff = ops.sub_op.as_expr(forward_offsets, scalar_exprs.const(start))
        elif step > 1 and start < 0:
            start_diff = ops.sub_op.as_expr(
                reverse_offsets, scalar_exprs.const(-start + 1)
            )
        elif step < 0 and start >= 0:
            start_diff = ops.add_op.as_expr(forward_offsets, scalar_exprs.const(start))
        else:
            assert step < 0 and start < 0
            start_diff = ops.add_op.as_expr(
                reverse_offsets, scalar_exprs.const(-start + 1)
            )
        step_cond = ops.eq_op.as_expr(
            ops.mod_op.as_expr(start_diff, scalar_exprs.const(step)),
            scalar_exprs.const(0),
        )
        conditions.append(step_cond)
    return merge_predicates(conditions) or scalar_exprs.const(True)
