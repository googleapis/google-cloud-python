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

import dataclasses
import functools
import itertools

from bigframes import operations as ops
from bigframes.core import (
    agg_expressions,
    expression,
    guid,
    identifiers,
    nodes,
    ordering,
)
import bigframes.dtypes
from bigframes.operations import aggregations as agg_ops


def simplify_complex_windows(
    window_expr: agg_expressions.WindowExpression,
) -> expression.Expression:
    result_expr: expression.Expression = window_expr
    agg_expr = window_expr.analytic_expr
    window_spec = window_expr.window
    clauses: list[tuple[expression.Expression, expression.Expression]] = []
    if window_spec.min_periods and len(agg_expr.inputs) > 0:
        if not agg_expr.op.nulls_count_for_min_values:
            is_observation = ops.notnull_op.as_expr()

            # Most operations do not count NULL values towards min_periods
            per_col_does_count = (
                ops.notnull_op.as_expr(input) for input in agg_expr.inputs
            )
            # All inputs must be non-null for observation to count
            is_observation = functools.reduce(
                lambda x, y: ops.and_op.as_expr(x, y), per_col_does_count
            )
            observation_sentinel = ops.AsTypeOp(bigframes.dtypes.INT_DTYPE).as_expr(
                is_observation
            )
            observation_count_expr = agg_expressions.WindowExpression(
                agg_expressions.UnaryAggregation(agg_ops.sum_op, observation_sentinel),
                window_spec,
            )
        else:
            # Operations like count treat even NULLs as valid observations for the sake of min_periods
            # notnull is just used to convert null values to non-null (FALSE) values to be counted
            is_observation = ops.notnull_op.as_expr(agg_expr.inputs[0])
            observation_count_expr = agg_expressions.WindowExpression(
                agg_ops.count_op.as_expr(is_observation),
                window_spec,
            )
        clauses.append(
            (
                ops.lt_op.as_expr(
                    observation_count_expr, expression.const(window_spec.min_periods)
                ),
                expression.const(None),
            )
        )
    if clauses:
        case_inputs = [
            *itertools.chain.from_iterable(clauses),
            expression.const(True),
            result_expr,
        ]
        result_expr = ops.CaseWhenOp().as_expr(*case_inputs)
    return result_expr


def rewrite_range_rolling(node: nodes.BigFrameNode) -> nodes.BigFrameNode:
    if not isinstance(node, nodes.WindowOpNode):
        return node

    if not node.window_spec.is_range_bounded:
        return node

    if len(node.window_spec.ordering) != 1:
        raise ValueError(
            "Range rolling should only be performed on exactly one column."
        )

    ordering_expr = node.window_spec.ordering[0]

    new_ordering = dataclasses.replace(
        ordering_expr,
        scalar_expression=ops.UnixMicros().as_expr(ordering_expr.scalar_expression),
    )

    return dataclasses.replace(
        node,
        window_spec=dataclasses.replace(node.window_spec, ordering=(new_ordering,)),
    )


def pull_out_window_order(root: nodes.BigFrameNode) -> nodes.BigFrameNode:
    return root.bottom_up(rewrite_window_node)


def rewrite_window_node(node: nodes.BigFrameNode) -> nodes.BigFrameNode:
    if not isinstance(node, nodes.WindowOpNode):
        return node
    if len(node.window_spec.ordering) == 0:
        return node
    else:
        offsets_id = guid.generate_guid()
        w_offsets = nodes.PromoteOffsetsNode(
            node.child, identifiers.ColumnId(offsets_id)
        )
        sorted_child = nodes.OrderByNode(w_offsets, node.window_spec.ordering)
        new_window_node = dataclasses.replace(
            node,
            child=sorted_child,
            window_spec=node.window_spec.without_order(force=True),
        )
        w_resetted_order = nodes.OrderByNode(
            new_window_node,
            by=(ordering.ascending_over(identifiers.ColumnId(offsets_id)),),
            is_total_order=True,
        )
        w_offsets_dropped = nodes.SelectionNode(
            w_resetted_order, tuple(nodes.AliasedRef.identity(id) for id in node.ids)
        )
        return w_offsets_dropped
