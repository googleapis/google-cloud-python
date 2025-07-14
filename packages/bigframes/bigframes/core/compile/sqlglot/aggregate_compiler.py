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

import functools
import typing

import sqlglot.expressions as sge

from bigframes.core import expression, window_spec
from bigframes.core.compile.sqlglot.expressions import typed_expr
import bigframes.core.compile.sqlglot.scalar_compiler as scalar_compiler
import bigframes.core.compile.sqlglot.sqlglot_ir as ir
import bigframes.operations as ops


def compile_aggregate(
    aggregate: expression.Aggregation,
    order_by: tuple[sge.Expression, ...],
) -> sge.Expression:
    """Compiles BigFrames aggregation expression into SQLGlot expression."""
    if isinstance(aggregate, expression.NullaryAggregation):
        return compile_nullary_agg(aggregate.op)
    if isinstance(aggregate, expression.UnaryAggregation):
        column = typed_expr.TypedExpr(
            scalar_compiler.compile_scalar_expression(aggregate.arg),
            aggregate.arg.output_type,
        )
        if not aggregate.op.order_independent:
            return compile_ordered_unary_agg(aggregate.op, column, order_by=order_by)
        else:
            return compile_unary_agg(aggregate.op, column)
    elif isinstance(aggregate, expression.BinaryAggregation):
        left = typed_expr.TypedExpr(
            scalar_compiler.compile_scalar_expression(aggregate.left),
            aggregate.left.output_type,
        )
        right = typed_expr.TypedExpr(
            scalar_compiler.compile_scalar_expression(aggregate.right),
            aggregate.right.output_type,
        )
        return compile_binary_agg(aggregate.op, left, right)
    else:
        raise ValueError(f"Unexpected aggregation: {aggregate}")


@functools.singledispatch
def compile_nullary_agg(
    op: ops.aggregations.WindowOp,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    raise ValueError(f"Can't compile unrecognized operation: {op}")


@functools.singledispatch
def compile_binary_agg(
    op: ops.aggregations.WindowOp,
    left: typed_expr.TypedExpr,
    right: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    raise ValueError(f"Can't compile unrecognized operation: {op}")


@functools.singledispatch
def compile_unary_agg(
    op: ops.aggregations.WindowOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    raise ValueError(f"Can't compile unrecognized operation: {op}")


@functools.singledispatch
def compile_ordered_unary_agg(
    op: ops.aggregations.WindowOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
    order_by: typing.Sequence[sge.Expression] = [],
) -> sge.Expression:
    raise ValueError(f"Can't compile unrecognized operation: {op}")


@compile_unary_agg.register
def _(
    op: ops.aggregations.SumOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    # Will be null if all inputs are null. Pandas defaults to zero sum though.
    expr = _apply_window_if_present(sge.func("SUM", column.expr), window)
    return sge.func("IFNULL", expr, ir._literal(0, column.dtype))


def _apply_window_if_present(
    value: sge.Expression,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    if window is not None:
        raise NotImplementedError("Can't apply window to the expression.")
    return value
