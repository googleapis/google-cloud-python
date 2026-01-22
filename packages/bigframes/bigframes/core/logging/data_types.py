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

import functools

from bigframes import dtypes
from bigframes.core import agg_expressions, bigframe_node, expression, nodes
from bigframes.core.rewrite import schema_binding

IGNORED_NODES = (
    nodes.SelectionNode,
    nodes.ReadLocalNode,
    nodes.ReadTableNode,
    nodes.ConcatNode,
    nodes.RandomSampleNode,
    nodes.FromRangeNode,
    nodes.PromoteOffsetsNode,
    nodes.ReversedNode,
    nodes.SliceNode,
    nodes.ResultNode,
)


def encode_type_refs(root: bigframe_node.BigFrameNode) -> str:
    return f"{root.reduce_up(_encode_type_refs_from_node):x}"


def _encode_type_refs_from_node(
    node: bigframe_node.BigFrameNode, child_results: tuple[int, ...]
) -> int:
    child_result = functools.reduce(lambda x, y: x | y, child_results, 0)

    curr_result = 0
    if isinstance(node, nodes.FilterNode):
        curr_result = _encode_type_refs_from_expr(node.predicate, node.child)
    elif isinstance(node, nodes.ProjectionNode):
        for assignment in node.assignments:
            expr = assignment[0]
            if isinstance(expr, (expression.DerefOp)):
                # Ignore direct assignments in projection nodes.
                continue
            curr_result = curr_result | _encode_type_refs_from_expr(
                assignment[0], node.child
            )
    elif isinstance(node, nodes.OrderByNode):
        for by in node.by:
            curr_result = curr_result | _encode_type_refs_from_expr(
                by.scalar_expression, node.child
            )
    elif isinstance(node, nodes.JoinNode):
        for left, right in node.conditions:
            curr_result = (
                curr_result
                | _encode_type_refs_from_expr(left, node.left_child)
                | _encode_type_refs_from_expr(right, node.right_child)
            )
    elif isinstance(node, nodes.InNode):
        curr_result = _encode_type_refs_from_expr(node.left_col, node.left_child)
    elif isinstance(node, nodes.AggregateNode):
        for agg, _ in node.aggregations:
            curr_result = curr_result | _encode_type_refs_from_expr(agg, node.child)
    elif isinstance(node, nodes.WindowOpNode):
        for grouping_key in node.window_spec.grouping_keys:
            curr_result = curr_result | _encode_type_refs_from_expr(
                grouping_key, node.child
            )
        for ordering_expr in node.window_spec.ordering:
            curr_result = curr_result | _encode_type_refs_from_expr(
                ordering_expr.scalar_expression, node.child
            )
        for col_def in node.agg_exprs:
            curr_result = curr_result | _encode_type_refs_from_expr(
                col_def.expression, node.child
            )
    elif isinstance(node, nodes.ExplodeNode):
        for col_id in node.column_ids:
            curr_result = curr_result | _encode_type_refs_from_expr(col_id, node.child)
    elif isinstance(node, IGNORED_NODES):
        # Do nothing
        pass
    else:
        # For unseen nodes, do not raise errors as this is the logging path, but
        # we should cover those nodes either in the branches above, or place them
        # in the IGNORED_NODES collection.
        pass

    return child_result | curr_result


def _encode_type_refs_from_expr(
    expr: expression.Expression, child_node: bigframe_node.BigFrameNode
) -> int:
    # TODO(b/409387790): Remove this branch once SQLGlot compiler fully replaces Ibis compiler
    if not expr.is_resolved:
        if isinstance(expr, agg_expressions.Aggregation):
            expr = schema_binding._bind_schema_to_aggregation_expr(expr, child_node)
        else:
            expr = expression.bind_schema_fields(expr, child_node.field_by_id)

    result = _get_dtype_mask(expr.output_type)
    for child_expr in expr.children:
        result = result | _encode_type_refs_from_expr(child_expr, child_node)

    return result


def _get_dtype_mask(dtype: dtypes.Dtype | None) -> int:
    if dtype is None:
        # If the dtype is not given, ignore
        return 0
    if dtype == dtypes.INT_DTYPE:
        return 1 << 1
    if dtype == dtypes.FLOAT_DTYPE:
        return 1 << 2
    if dtype == dtypes.BOOL_DTYPE:
        return 1 << 3
    if dtype == dtypes.STRING_DTYPE:
        return 1 << 4
    if dtype == dtypes.BYTES_DTYPE:
        return 1 << 5
    if dtype == dtypes.DATE_DTYPE:
        return 1 << 6
    if dtype == dtypes.TIME_DTYPE:
        return 1 << 7
    if dtype == dtypes.DATETIME_DTYPE:
        return 1 << 8
    if dtype == dtypes.TIMESTAMP_DTYPE:
        return 1 << 9
    if dtype == dtypes.TIMEDELTA_DTYPE:
        return 1 << 10
    if dtype == dtypes.NUMERIC_DTYPE:
        return 1 << 11
    if dtype == dtypes.BIGNUMERIC_DTYPE:
        return 1 << 12
    if dtype == dtypes.GEO_DTYPE:
        return 1 << 13
    if dtype == dtypes.JSON_DTYPE:
        return 1 << 14

    if dtypes.is_struct_like(dtype):
        mask = 1 << 15
        if dtype == dtypes.OBJ_REF_DTYPE:
            # obj_ref is a special struct type for multi-modal data.
            # It should be double counted as both "struct" and its own type.
            mask = mask | (1 << 17)
        return mask

    if dtypes.is_array_like(dtype):
        return 1 << 16

    # If an unknown datat type is present, mark it with the least significant bit.
    return 1 << 0
