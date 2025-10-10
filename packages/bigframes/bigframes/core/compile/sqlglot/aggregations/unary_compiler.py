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

import typing

import pandas as pd
import sqlglot.expressions as sge

from bigframes import dtypes
from bigframes.core import window_spec
import bigframes.core.compile.sqlglot.aggregations.op_registration as reg
from bigframes.core.compile.sqlglot.aggregations.windows import apply_window_if_present
import bigframes.core.compile.sqlglot.expressions.typed_expr as typed_expr
import bigframes.core.compile.sqlglot.sqlglot_ir as ir
from bigframes.operations import aggregations as agg_ops

UNARY_OP_REGISTRATION = reg.OpRegistration()


def compile(
    op: agg_ops.WindowOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    return UNARY_OP_REGISTRATION[op](op, column, window=window)


@UNARY_OP_REGISTRATION.register(agg_ops.AllOp)
def _(
    op: agg_ops.AllOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    # BQ will return null for empty column, result would be false in pandas.
    result = apply_window_if_present(sge.func("LOGICAL_AND", column.expr), window)
    return sge.func("IFNULL", result, sge.true())


@UNARY_OP_REGISTRATION.register(agg_ops.ApproxQuartilesOp)
def _(
    op: agg_ops.ApproxQuartilesOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    if window is not None:
        raise NotImplementedError("Approx Quartiles with windowing is not supported.")
    # APPROX_QUANTILES returns an array of the quartiles, so we need to index it.
    # The op.quartile is 1-based for the quartile, but array is 0-indexed.
    # The quartiles are Q0, Q1, Q2, Q3, Q4. op.quartile is 1, 2, or 3.
    # The array has 5 elements (for N=4 intervals).
    # So we want the element at index `op.quartile`.
    approx_quantiles_expr = sge.func("APPROX_QUANTILES", column.expr, sge.convert(4))
    return sge.Bracket(
        this=approx_quantiles_expr,
        expressions=[sge.func("OFFSET", sge.convert(op.quartile))],
    )


@UNARY_OP_REGISTRATION.register(agg_ops.ApproxTopCountOp)
def _(
    op: agg_ops.ApproxTopCountOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    if window is not None:
        raise NotImplementedError("Approx top count with windowing is not supported.")
    return sge.func("APPROX_TOP_COUNT", column.expr, sge.convert(op.number))


@UNARY_OP_REGISTRATION.register(agg_ops.AnyValueOp)
def _(
    op: agg_ops.AnyValueOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    return apply_window_if_present(sge.func("ANY_VALUE", column.expr), window)


@UNARY_OP_REGISTRATION.register(agg_ops.CountOp)
def _(
    op: agg_ops.CountOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    return apply_window_if_present(sge.func("COUNT", column.expr), window)


@UNARY_OP_REGISTRATION.register(agg_ops.DenseRankOp)
def _(
    op: agg_ops.DenseRankOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    return apply_window_if_present(
        sge.func("DENSE_RANK"), window, include_framing_clauses=False
    )


@UNARY_OP_REGISTRATION.register(agg_ops.FirstOp)
def _(
    op: agg_ops.FirstOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    # FIRST_VALUE in BQ respects nulls by default.
    return apply_window_if_present(sge.FirstValue(this=column.expr), window)


@UNARY_OP_REGISTRATION.register(agg_ops.FirstNonNullOp)
def _(
    op: agg_ops.FirstNonNullOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    return apply_window_if_present(
        sge.IgnoreNulls(this=sge.FirstValue(this=column.expr)), window
    )


@UNARY_OP_REGISTRATION.register(agg_ops.LastOp)
def _(
    op: agg_ops.LastOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    # LAST_VALUE in BQ respects nulls by default.
    return apply_window_if_present(sge.LastValue(this=column.expr), window)


@UNARY_OP_REGISTRATION.register(agg_ops.LastNonNullOp)
def _(
    op: agg_ops.LastNonNullOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    return apply_window_if_present(
        sge.IgnoreNulls(this=sge.LastValue(this=column.expr)), window
    )


@UNARY_OP_REGISTRATION.register(agg_ops.DiffOp)
def _(
    op: agg_ops.DiffOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    shift_op_impl = UNARY_OP_REGISTRATION[agg_ops.ShiftOp(0)]
    shifted = shift_op_impl(agg_ops.ShiftOp(op.periods), column, window)
    if column.dtype in (dtypes.BOOL_DTYPE, dtypes.INT_DTYPE, dtypes.FLOAT_DTYPE):
        if column.dtype == dtypes.BOOL_DTYPE:
            return sge.NEQ(this=column.expr, expression=shifted)
        else:
            return sge.Sub(this=column.expr, expression=shifted)
    else:
        raise TypeError(f"Cannot perform diff on type {column.dtype}")


@UNARY_OP_REGISTRATION.register(agg_ops.MaxOp)
def _(
    op: agg_ops.MaxOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    return apply_window_if_present(sge.func("MAX", column.expr), window)


@UNARY_OP_REGISTRATION.register(agg_ops.MeanOp)
def _(
    op: agg_ops.MeanOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    expr = column.expr
    if column.dtype == dtypes.BOOL_DTYPE:
        expr = sge.Cast(this=expr, to="INT64")

    expr = sge.func("AVG", expr)

    should_floor_result = (
        op.should_floor_result or column.dtype == dtypes.TIMEDELTA_DTYPE
    )
    if should_floor_result:
        expr = sge.Cast(this=sge.func("FLOOR", expr), to="INT64")
    return apply_window_if_present(expr, window)


@UNARY_OP_REGISTRATION.register(agg_ops.MedianOp)
def _(
    op: agg_ops.MedianOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    approx_quantiles = sge.func("APPROX_QUANTILES", column.expr, sge.convert(2))
    return sge.Bracket(
        this=approx_quantiles, expressions=[sge.func("OFFSET", sge.convert(1))]
    )


@UNARY_OP_REGISTRATION.register(agg_ops.MinOp)
def _(
    op: agg_ops.MinOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    return apply_window_if_present(sge.func("MIN", column.expr), window)


@UNARY_OP_REGISTRATION.register(agg_ops.QuantileOp)
def _(
    op: agg_ops.QuantileOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    # TODO: Support interpolation argument
    # TODO: Support percentile_disc
    result: sge.Expression = sge.func("PERCENTILE_CONT", column.expr, sge.convert(op.q))
    if window is None:
        # PERCENTILE_CONT is a navigation function, not an aggregate function, so it always needs an OVER clause.
        result = sge.Window(this=result)
    else:
        result = apply_window_if_present(result, window)
    if op.should_floor_result:
        result = sge.Cast(this=sge.func("FLOOR", result), to="INT64")
    return result


@UNARY_OP_REGISTRATION.register(agg_ops.RankOp)
def _(
    op: agg_ops.RankOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    return apply_window_if_present(
        sge.func("RANK"), window, include_framing_clauses=False
    )


@UNARY_OP_REGISTRATION.register(agg_ops.SizeUnaryOp)
def _(
    op: agg_ops.SizeUnaryOp,
    _,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    return apply_window_if_present(sge.func("COUNT", sge.convert(1)), window)


@UNARY_OP_REGISTRATION.register(agg_ops.ShiftOp)
def _(
    op: agg_ops.ShiftOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    if op.periods == 0:  # No-op
        return column.expr
    if op.periods > 0:
        return apply_window_if_present(
            sge.func("LAG", column.expr, sge.convert(op.periods)),
            window,
            include_framing_clauses=False,
        )
    return apply_window_if_present(
        sge.func("LEAD", column.expr, sge.convert(-op.periods)),
        window,
        include_framing_clauses=False,
    )


@UNARY_OP_REGISTRATION.register(agg_ops.SumOp)
def _(
    op: agg_ops.SumOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    expr = column.expr
    if column.dtype == dtypes.BOOL_DTYPE:
        expr = sge.Cast(this=column.expr, to="INT64")

    expr = apply_window_if_present(sge.func("SUM", expr), window)

    # Will be null if all inputs are null. Pandas defaults to zero sum though.
    zero = pd.to_timedelta(0) if column.dtype == dtypes.TIMEDELTA_DTYPE else 0
    return sge.func("IFNULL", expr, ir._literal(zero, column.dtype))
