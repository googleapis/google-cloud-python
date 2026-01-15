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

import bigframes_vendored.sqlglot.expressions as sge
import pandas as pd

from bigframes import dtypes
from bigframes.core import window_spec
import bigframes.core.compile.sqlglot.aggregations.op_registration as reg
from bigframes.core.compile.sqlglot.aggregations.windows import apply_window_if_present
from bigframes.core.compile.sqlglot.expressions import constants
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
    expr = column.expr
    if column.dtype != dtypes.BOOL_DTYPE:
        expr = sge.NEQ(this=expr, expression=sge.convert(0))
    expr = apply_window_if_present(sge.func("LOGICAL_AND", expr), window)

    # BQ will return null for empty column, result would be true in pandas.
    return sge.func("COALESCE", expr, sge.convert(True))


@UNARY_OP_REGISTRATION.register(agg_ops.AnyOp)
def _(
    op: agg_ops.AnyOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    expr = column.expr
    if column.dtype != dtypes.BOOL_DTYPE:
        expr = sge.NEQ(this=expr, expression=sge.convert(0))
    expr = apply_window_if_present(sge.func("LOGICAL_OR", expr), window)

    # BQ will return null for empty column, result would be false in pandas.
    return sge.func("COALESCE", expr, sge.convert(False))


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


@UNARY_OP_REGISTRATION.register(agg_ops.CutOp)
def _(
    op: agg_ops.CutOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    if isinstance(op.bins, int):
        case_expr = _cut_ops_w_int_bins(op, column, op.bins, window)
    else:  # Interpret as intervals
        case_expr = _cut_ops_w_intervals(op, column, op.bins, window)
    return case_expr


def _cut_ops_w_int_bins(
    op: agg_ops.CutOp,
    column: typed_expr.TypedExpr,
    bins: int,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Case:
    case_expr = sge.Case()
    col_min = apply_window_if_present(
        sge.func("MIN", column.expr), window or window_spec.WindowSpec()
    )
    col_max = apply_window_if_present(
        sge.func("MAX", column.expr), window or window_spec.WindowSpec()
    )
    adj: sge.Expression = sge.Sub(this=col_max, expression=col_min) * sge.convert(0.001)
    bin_width: sge.Expression = sge.func(
        "IEEE_DIVIDE",
        sge.Sub(this=col_max, expression=col_min),
        sge.convert(bins),
    )

    for this_bin in range(bins):
        value: sge.Expression
        if op.labels is False:
            value = ir._literal(this_bin, dtypes.INT_DTYPE)
        elif isinstance(op.labels, typing.Iterable):
            value = ir._literal(list(op.labels)[this_bin], dtypes.STRING_DTYPE)
        else:
            left_adj: sge.Expression = (
                adj if this_bin == 0 and op.right else sge.convert(0)
            )
            right_adj: sge.Expression = (
                adj if this_bin == bins - 1 and not op.right else sge.convert(0)
            )

            left: sge.Expression = (
                col_min + sge.convert(this_bin) * bin_width - left_adj
            )
            right: sge.Expression = (
                col_min + sge.convert(this_bin + 1) * bin_width + right_adj
            )
            if op.right:
                left_identifier = sge.Identifier(this="left_exclusive", quoted=True)
                right_identifier = sge.Identifier(this="right_inclusive", quoted=True)
            else:
                left_identifier = sge.Identifier(this="left_inclusive", quoted=True)
                right_identifier = sge.Identifier(this="right_exclusive", quoted=True)

            value = sge.Struct(
                expressions=[
                    sge.PropertyEQ(this=left_identifier, expression=left),
                    sge.PropertyEQ(this=right_identifier, expression=right),
                ]
            )

        condition: sge.Expression
        if this_bin == bins - 1:
            condition = sge.Is(this=column.expr, expression=sge.Not(this=sge.Null()))
        else:
            if op.right:
                condition = sge.LTE(
                    this=column.expr,
                    expression=(col_min + sge.convert(this_bin + 1) * bin_width),
                )
            else:
                condition = sge.LT(
                    this=column.expr,
                    expression=(col_min + sge.convert(this_bin + 1) * bin_width),
                )
        case_expr = case_expr.when(condition, value)
    return case_expr


def _cut_ops_w_intervals(
    op: agg_ops.CutOp,
    column: typed_expr.TypedExpr,
    bins: typing.Iterable[typing.Tuple[typing.Any, typing.Any]],
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Case:
    case_expr = sge.Case()
    for this_bin, interval in enumerate(bins):
        left: sge.Expression = ir._literal(
            interval[0], dtypes.infer_literal_type(interval[0])
        )
        right: sge.Expression = ir._literal(
            interval[1], dtypes.infer_literal_type(interval[1])
        )
        condition: sge.Expression
        if op.right:
            condition = sge.And(
                this=sge.GT(this=column.expr, expression=left),
                expression=sge.LTE(this=column.expr, expression=right),
            )
        else:
            condition = sge.And(
                this=sge.GTE(this=column.expr, expression=left),
                expression=sge.LT(this=column.expr, expression=right),
            )

        value: sge.Expression
        if op.labels is False:
            value = ir._literal(this_bin, dtypes.INT_DTYPE)
        elif isinstance(op.labels, typing.Iterable):
            value = ir._literal(list(op.labels)[this_bin], dtypes.STRING_DTYPE)
        else:
            if op.right:
                left_identifier = sge.Identifier(this="left_exclusive", quoted=True)
                right_identifier = sge.Identifier(this="right_inclusive", quoted=True)
            else:
                left_identifier = sge.Identifier(this="left_inclusive", quoted=True)
                right_identifier = sge.Identifier(this="right_exclusive", quoted=True)

            value = sge.Struct(
                expressions=[
                    sge.PropertyEQ(this=left_identifier, expression=left),
                    sge.PropertyEQ(this=right_identifier, expression=right),
                ]
            )
        case_expr = case_expr.when(condition, value)
    return case_expr


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
    if column.dtype == dtypes.BOOL_DTYPE:
        return sge.NEQ(this=column.expr, expression=shifted)

    if column.dtype in (dtypes.INT_DTYPE, dtypes.FLOAT_DTYPE):
        return sge.Sub(this=column.expr, expression=shifted)

    if column.dtype == dtypes.TIMESTAMP_DTYPE:
        return sge.TimestampDiff(
            this=column.expr,
            expression=shifted,
            unit=sge.Identifier(this="MICROSECOND"),
        )

    if column.dtype == dtypes.DATETIME_DTYPE:
        return sge.DatetimeDiff(
            this=column.expr,
            expression=shifted,
            unit=sge.Identifier(this="MICROSECOND"),
        )

    if column.dtype == dtypes.DATE_DTYPE:
        date_diff = sge.DateDiff(
            this=column.expr, expression=shifted, unit=sge.Identifier(this="DAY")
        )
        return sge.Cast(
            this=sge.Floor(this=date_diff * constants._DAY_TO_MICROSECONDS),
            to="INT64",
        )

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


@UNARY_OP_REGISTRATION.register(agg_ops.NuniqueOp)
def _(
    op: agg_ops.NuniqueOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    return apply_window_if_present(
        sge.func("COUNT", sge.Distinct(expressions=[column.expr])), window
    )


@UNARY_OP_REGISTRATION.register(agg_ops.PopVarOp)
def _(
    op: agg_ops.PopVarOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    expr = column.expr
    if column.dtype == dtypes.BOOL_DTYPE:
        expr = sge.Cast(this=expr, to="INT64")

    expr = sge.func("VAR_POP", expr)
    return apply_window_if_present(expr, window)


@UNARY_OP_REGISTRATION.register(agg_ops.ProductOp)
def _(
    op: agg_ops.ProductOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    expr = column.expr
    if column.dtype == dtypes.BOOL_DTYPE:
        expr = sge.Cast(this=expr, to="INT64")

    # Need to short-circuit as log with zeroes is illegal sql
    is_zero = sge.EQ(this=expr, expression=sge.convert(0))

    # There is no product sql aggregate function, so must implement as a sum of logs, and then
    # apply power after. Note, log and power base must be equal! This impl uses natural log.
    logs = sge.If(
        this=is_zero,
        true=sge.convert(0),
        false=sge.func("LOG", sge.convert(2), sge.func("ABS", expr)),
    )
    logs_sum = apply_window_if_present(sge.func("SUM", logs), window)
    magnitude = sge.func("POWER", sge.convert(2), logs_sum)

    # Can't determine sign from logs, so have to determine parity of count of negative inputs
    is_negative = (
        sge.Case()
        .when(
            sge.EQ(this=sge.func("SIGN", expr), expression=sge.convert(-1)),
            sge.convert(1),
        )
        .else_(sge.convert(0))
    )
    negative_count = apply_window_if_present(sge.func("SUM", is_negative), window)
    negative_count_parity = sge.Mod(
        this=negative_count, expression=sge.convert(2)
    )  # 1 if result should be negative, otherwise 0

    any_zeroes = apply_window_if_present(sge.func("LOGICAL_OR", is_zero), window)

    float_result = (
        sge.Case()
        .when(any_zeroes, sge.convert(0))
        .else_(
            sge.Mul(
                this=magnitude,
                expression=sge.func("POWER", sge.convert(-1), negative_count_parity),
            )
        )
    )
    return float_result


@UNARY_OP_REGISTRATION.register(agg_ops.QcutOp)
def _(
    op: agg_ops.QcutOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    percent_ranks_order_by = sge.Ordered(this=column.expr, desc=False)
    percent_ranks = apply_window_if_present(
        sge.func("PERCENT_RANK"),
        window,
        include_framing_clauses=False,
        order_by_override=[percent_ranks_order_by],
    )
    if isinstance(op.quantiles, int):
        scaled_rank = percent_ranks * sge.convert(op.quantiles)
        # Calculate the 0-based bucket index.
        bucket_index = sge.func("CEIL", scaled_rank) - sge.convert(1)
        safe_bucket_index = sge.func("GREATEST", bucket_index, 0)

        return sge.If(
            this=sge.Is(this=column.expr, expression=sge.Null()),
            true=sge.Null(),
            false=sge.Cast(this=safe_bucket_index, to="INT64"),
        )
    else:
        case = sge.Case()
        first_quantile = sge.convert(op.quantiles[0])
        case = case.when(
            sge.LT(this=percent_ranks, expression=first_quantile), sge.Null()
        )
        for bucket_n in range(len(op.quantiles) - 1):
            quantile = sge.convert(op.quantiles[bucket_n + 1])
            bucket = sge.convert(bucket_n)
            case = case.when(sge.LTE(this=percent_ranks, expression=quantile), bucket)
        return case.else_(sge.Null())


@UNARY_OP_REGISTRATION.register(agg_ops.QuantileOp)
def _(
    op: agg_ops.QuantileOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    expr = column.expr
    if column.dtype == dtypes.BOOL_DTYPE:
        expr = sge.Cast(this=expr, to="INT64")

    result: sge.Expression = sge.func("PERCENTILE_CONT", expr, sge.convert(op.q))
    if window is None:
        # PERCENTILE_CONT is a navigation function, not an aggregate function,
        # so it always needs an OVER clause.
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


@UNARY_OP_REGISTRATION.register(agg_ops.StdOp)
def _(
    op: agg_ops.StdOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    expr = column.expr
    if column.dtype == dtypes.BOOL_DTYPE:
        expr = sge.Cast(this=expr, to="INT64")

    expr = sge.func("STDDEV", expr)
    if op.should_floor_result or column.dtype == dtypes.TIMEDELTA_DTYPE:
        expr = sge.Cast(this=sge.func("FLOOR", expr), to="INT64")
    return apply_window_if_present(expr, window)


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


@UNARY_OP_REGISTRATION.register(agg_ops.VarOp)
def _(
    op: agg_ops.VarOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    expr = column.expr
    if column.dtype == dtypes.BOOL_DTYPE:
        expr = sge.Cast(this=expr, to="INT64")

    expr = sge.func("VAR_SAMP", expr)
    return apply_window_if_present(expr, window)
