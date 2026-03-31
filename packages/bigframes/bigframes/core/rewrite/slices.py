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
from typing import Optional, Sequence, Tuple

import bigframes.core.expression as scalar_exprs
import bigframes.core.guid as guids
import bigframes.core.identifiers as ids
import bigframes.core.nodes as nodes
import bigframes.core.slices as slices
import bigframes.operations as ops


def pull_up_limits(root: nodes.ResultNode) -> nodes.ResultNode:
    new_child, pulled_limit = pull_out_limit(root.child)
    if new_child == root.child:
        return root
    elif pulled_limit is None:
        return dataclasses.replace(root, child=new_child)
    else:
        # new child has redundant slice ops removed now
        new_limit = min(pulled_limit, root.limit) if root.limit else pulled_limit
        return dataclasses.replace(root, child=new_child, limit=new_limit)


def pull_out_limit(
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
            new_root, prior_limit = pull_out_limit(root.child)
            if (prior_limit is not None) and (prior_limit < limit):
                limit = prior_limit
            return new_root, limit
        if root.is_noop:
            new_root, prior_limit = pull_out_limit(root.child)
            return new_root, prior_limit
    elif (
        isinstance(root, (nodes.SelectionNode, nodes.ProjectionNode))
        and root.row_preserving
    ):
        new_child, prior_limit = pull_out_limit(root.child)
        if prior_limit is not None:
            return root.transform_children(lambda _: new_child), prior_limit
    # Most ops don't support pulling up slice, like filter, agg, join, etc.
    return root, None


def rewrite_slice(node: nodes.BigFrameNode):
    if not isinstance(node, nodes.SliceNode):
        return node

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
        nodes.AliasedRef(scalar_exprs.DerefOp(id), id)
        for id in node.ids
        if id not in drop_cols
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


def merge_predicates(
    predicates: Sequence[scalar_exprs.Expression],
) -> Optional[scalar_exprs.Expression]:
    if len(predicates) == 0:
        return None

    return functools.reduce(ops.and_op.as_expr, predicates)
