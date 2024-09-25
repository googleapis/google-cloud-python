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

import functools
import typing
from typing import cast, List, Optional

import bigframes_vendored.constants as constants
import bigframes_vendored.ibis.expr.operations as vendored_ibis_ops
import ibis
import ibis.expr.datatypes as ibis_dtypes
import ibis.expr.operations as ibis_ops
import ibis.expr.types as ibis_types
import pandas as pd

import bigframes.core.compile.ibis_types as compile_ibis_types
import bigframes.core.compile.scalar_op_compiler as scalar_compilers
import bigframes.core.expression as ex
import bigframes.core.window_spec as window_spec
import bigframes.operations.aggregations as agg_ops

scalar_compiler = scalar_compilers.scalar_op_compiler


# TODO(swast): We can remove this if ibis adds general approx_quantile
# See: https://github.com/ibis-project/ibis/issues/9541
@ibis.udf.agg.builtin
def approx_quantiles(expression: float, number) -> List[float]:
    """APPROX_QUANTILES

    https://cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions#approx_quantiles
    """
    return []  # pragma: NO COVER


def compile_aggregate(
    aggregate: ex.Aggregation,
    bindings: typing.Dict[str, ibis_types.Value],
    order_by: typing.Sequence[ibis_types.Value] = [],
) -> ibis_types.Value:
    if isinstance(aggregate, ex.NullaryAggregation):
        return compile_nullary_agg(aggregate.op)
    if isinstance(aggregate, ex.UnaryAggregation):
        input = scalar_compiler.compile_expression(aggregate.arg, bindings=bindings)
        if aggregate.op.can_order_by:
            return compile_ordered_unary_agg(aggregate.op, input, order_by=order_by)
        else:
            return compile_unary_agg(aggregate.op, input)
    elif isinstance(aggregate, ex.BinaryAggregation):
        left = scalar_compiler.compile_expression(aggregate.left, bindings=bindings)
        right = scalar_compiler.compile_expression(aggregate.right, bindings=bindings)
        return compile_binary_agg(aggregate.op, left, right)
    else:
        raise ValueError(f"Unexpected aggregation: {aggregate}")


def compile_analytic(
    aggregate: ex.Aggregation,
    window: window_spec.WindowSpec,
    bindings: typing.Dict[str, ibis_types.Value],
) -> ibis_types.Value:
    if isinstance(aggregate, ex.NullaryAggregation):
        return compile_nullary_agg(aggregate.op, window)
    elif isinstance(aggregate, ex.UnaryAggregation):
        input = scalar_compiler.compile_expression(aggregate.arg, bindings=bindings)
        return compile_unary_agg(aggregate.op, input, window)
    elif isinstance(aggregate, ex.BinaryAggregation):
        raise NotImplementedError("binary analytic operations not yet supported")
    else:
        raise ValueError(f"Unexpected analytic operation: {aggregate}")


@functools.singledispatch
def compile_binary_agg(
    op: agg_ops.WindowOp,
    left: ibis_types.Column,
    right: ibis_types.Column,
    window: Optional[window_spec.WindowSpec] = None,
) -> ibis_types.Value:
    raise ValueError(f"Can't compile unrecognized operation: {op}")


@functools.singledispatch
def compile_unary_agg(
    op: agg_ops.WindowOp,
    input: ibis_types.Column,
    window: Optional[window_spec.WindowSpec] = None,
) -> ibis_types.Value:
    raise ValueError(f"Can't compile unrecognized operation: {op}")


@functools.singledispatch
def compile_ordered_unary_agg(
    op: agg_ops.WindowOp,
    input: ibis_types.Column,
    window: Optional[window_spec.WindowSpec] = None,
    order_by: typing.Sequence[ibis_types.Value] = [],
) -> ibis_types.Value:
    raise ValueError(f"Can't compile unrecognized operation: {op}")


@functools.singledispatch
def compile_nullary_agg(
    op: agg_ops.WindowOp,
    window: Optional[window_spec.WindowSpec] = None,
) -> ibis_types.Value:
    raise ValueError(f"Can't compile unrecognized operation: {op}")


def numeric_op(operation):
    @functools.wraps(operation)
    def constrained_op(
        op,
        column: ibis_types.Column,
        window=None,
        order_by: typing.Sequence[ibis_types.Value] = [],
    ):
        if column.type().is_boolean():
            column = typing.cast(
                ibis_types.NumericColumn, column.cast(ibis_dtypes.int64)
            )
        if column.type().is_numeric():
            return operation(op, column, window)
        else:
            raise ValueError(
                f"Numeric operation cannot be applied to type {column.type()}. {constants.FEEDBACK_LINK}"
            )

    return constrained_op


### Specific Op implementations Below


@compile_nullary_agg.register
def _(op: agg_ops.SizeOp, window=None) -> ibis_types.NumericValue:
    return _apply_window_if_present(vendored_ibis_ops.count(1), window)


@compile_unary_agg.register
@numeric_op
def _(
    op: agg_ops.SumOp,
    column: ibis_types.NumericColumn,
    window=None,
) -> ibis_types.NumericValue:
    # Will be null if all inputs are null. Pandas defaults to zero sum though.
    bq_sum = _apply_window_if_present(column.sum(), window)
    return (
        ibis.case().when(bq_sum.isnull(), ibis_types.literal(0)).else_(bq_sum).end()  # type: ignore
    )


@compile_unary_agg.register
@numeric_op
def _(
    op: agg_ops.MedianOp,
    column: ibis_types.NumericColumn,
    window=None,
) -> ibis_types.NumericValue:
    # PERCENTILE_CONT has very few allowed windows. For example, "window
    # framing clause is not allowed for analytic function percentile_cont".
    if window is not None:
        raise NotImplementedError(
            f"Median with windowing is not supported. {constants.FEEDBACK_LINK}"
        )

    # TODO(swast): Allow switching between exact and approximate median.
    # For now, the best we can do is an approximate median when we're doing
    # an aggregation, as PERCENTILE_CONT is only an analytic function.
    return cast(ibis_types.NumericValue, column.approx_median())


@compile_unary_agg.register
@numeric_op
def _(
    op: agg_ops.ApproxQuartilesOp,
    column: ibis_types.NumericColumn,
    window=None,
) -> ibis_types.NumericValue:
    # APPROX_QUANTILES has very few allowed windows.
    if window is not None:
        raise NotImplementedError(
            f"Approx Quartiles with windowing is not supported. {constants.FEEDBACK_LINK}"
        )
    value = approx_quantiles(column, 4)[op.quartile]  # type: ignore
    return cast(ibis_types.NumericValue, value)


@compile_unary_agg.register
def _(
    op: agg_ops.ApproxTopCountOp,
    column: ibis_types.Column,
    window=None,
) -> ibis_types.ArrayColumn:
    # APPROX_TOP_COUNT has very few allowed windows.
    if window is not None:
        raise NotImplementedError(
            f"Approx top count with windowing is not supported. {constants.FEEDBACK_LINK}"
        )

    # Define a user-defined function (UDF) that approximates the top counts of an expression.
    # The type of value is dynamically matching the input column.
    def approx_top_count(expression, number: ibis_dtypes.int64):  # type: ignore
        ...

    return_type = ibis_dtypes.Array(
        ibis_dtypes.Struct.from_tuples(
            [("value", column.type()), ("count", ibis_dtypes.int64)]
        )
    )
    approx_top_count.__annotations__["return"] = return_type
    udf_op = ibis_ops.udf.agg.builtin(approx_top_count)

    return udf_op(expression=column, number=op.number)


@compile_unary_agg.register
@numeric_op
def _(
    op: agg_ops.QuantileOp,
    column: ibis_types.NumericColumn,
    window=None,
) -> ibis_types.NumericValue:
    return _apply_window_if_present(column.quantile(op.q), window)


@compile_unary_agg.register
@numeric_op
def _(
    op: agg_ops.MeanOp,
    column: ibis_types.NumericColumn,
    window=None,
    # order_by: typing.Sequence[ibis_types.Value] = [],
) -> ibis_types.NumericValue:
    return _apply_window_if_present(column.mean(), window)


@compile_unary_agg.register
@numeric_op
def _(
    op: agg_ops.ProductOp,
    column: ibis_types.NumericColumn,
    window=None,
) -> ibis_types.NumericValue:
    # Need to short-circuit as log with zeroes is illegal sql
    is_zero = cast(ibis_types.BooleanColumn, (column == 0))

    # There is no product sql aggregate function, so must implement as a sum of logs, and then
    # apply power after. Note, log and power base must be equal! This impl uses base 2.
    logs = cast(
        ibis_types.NumericColumn,
        ibis.case().when(is_zero, 0).else_(column.abs().log2()).end(),
    )
    logs_sum = _apply_window_if_present(logs.sum(), window)
    magnitude = cast(ibis_types.NumericValue, ibis_types.literal(2)).pow(logs_sum)

    # Can't determine sign from logs, so have to determine parity of count of negative inputs
    is_negative = cast(
        ibis_types.NumericColumn,
        ibis.case().when(column.sign() == -1, 1).else_(0).end(),
    )
    negative_count = _apply_window_if_present(is_negative.sum(), window)
    negative_count_parity = negative_count % cast(
        ibis_types.NumericValue, ibis.literal(2)
    )  # 1 if result should be negative, otherwise 0

    any_zeroes = _apply_window_if_present(is_zero.any(), window)
    float_result = (
        ibis.case()
        .when(any_zeroes, ibis_types.literal(0))
        .else_(magnitude * pow(-1, negative_count_parity))
        .end()
    )
    return float_result


@compile_unary_agg.register
def _(
    op: agg_ops.MaxOp,
    column: ibis_types.Column,
    window=None,
) -> ibis_types.Value:
    return _apply_window_if_present(column.max(), window)


@compile_unary_agg.register
def _(
    op: agg_ops.MinOp,
    column: ibis_types.Column,
    window=None,
) -> ibis_types.Value:
    return _apply_window_if_present(column.min(), window)


@compile_unary_agg.register
@numeric_op
def _(
    op: agg_ops.StdOp,
    x: ibis_types.Column,
    window=None,
) -> ibis_types.Value:
    return _apply_window_if_present(cast(ibis_types.NumericColumn, x).std(), window)


@compile_unary_agg.register
@numeric_op
def _(
    op: agg_ops.VarOp,
    x: ibis_types.Column,
    window=None,
) -> ibis_types.Value:
    return _apply_window_if_present(cast(ibis_types.NumericColumn, x).var(), window)


@compile_unary_agg.register
@numeric_op
def _(
    op: agg_ops.PopVarOp,
    x: ibis_types.Column,
    window=None,
) -> ibis_types.Value:
    return _apply_window_if_present(
        cast(ibis_types.NumericColumn, x).var(how="pop"), window
    )


@compile_unary_agg.register
def _(
    op: agg_ops.CountOp,
    column: ibis_types.Column,
    window=None,
) -> ibis_types.IntegerValue:
    return _apply_window_if_present(column.count(), window)


@compile_unary_agg.register
def _(
    op: agg_ops.CutOp,
    x: ibis_types.Column,
    window=None,
):
    out = ibis.case()
    if isinstance(op.bins, int):
        col_min = _apply_window_if_present(x.min(), window)
        col_max = _apply_window_if_present(x.max(), window)
        bin_width = (col_max - col_min) / op.bins

        if op.labels is False:
            for this_bin in range(op.bins - 1):
                out = out.when(
                    x <= (col_min + (this_bin + 1) * bin_width),
                    compile_ibis_types.literal_to_ibis_scalar(
                        this_bin, force_dtype=pd.Int64Dtype()
                    ),
                )
            out = out.when(x.notnull(), op.bins - 1)
        else:
            interval_struct = None
            adj = (col_max - col_min) * 0.001
            for this_bin in range(op.bins):
                left_edge = (
                    col_min + this_bin * bin_width - (0 if this_bin > 0 else adj)
                )
                right_edge = col_min + (this_bin + 1) * bin_width
                interval_struct = ibis.struct(
                    {
                        "left_exclusive": left_edge,
                        "right_inclusive": right_edge,
                    }
                )

                if this_bin < op.bins - 1:
                    out = out.when(
                        x <= (col_min + (this_bin + 1) * bin_width),
                        interval_struct,
                    )
                else:
                    out = out.when(x.notnull(), interval_struct)
    else:  # Interpret as intervals
        for interval in op.bins:
            left = compile_ibis_types.literal_to_ibis_scalar(interval[0])
            right = compile_ibis_types.literal_to_ibis_scalar(interval[1])
            condition = (x > left) & (x <= right)
            interval_struct = ibis.struct(
                {"left_exclusive": left, "right_inclusive": right}
            )
            out = out.when(condition, interval_struct)
    return out.end()


@compile_unary_agg.register
@numeric_op
def _(
    self: agg_ops.QcutOp,
    column: ibis_types.Column,
    window=None,
) -> ibis_types.IntegerValue:
    if isinstance(self.quantiles, int):
        quantiles_ibis = compile_ibis_types.literal_to_ibis_scalar(self.quantiles)
        percent_ranks = cast(
            ibis_types.FloatingColumn,
            _apply_window_if_present(column.percent_rank(), window),
        )
        float_bucket = cast(ibis_types.FloatingColumn, (percent_ranks * quantiles_ibis))
        return float_bucket.ceil().clip(lower=_ibis_num(1)) - _ibis_num(1)
    else:
        percent_ranks = cast(
            ibis_types.FloatingColumn,
            _apply_window_if_present(column.percent_rank(), window),
        )
        out = ibis.case()
        first_ibis_quantile = compile_ibis_types.literal_to_ibis_scalar(
            self.quantiles[0]
        )
        out = out.when(percent_ranks < first_ibis_quantile, None)
        for bucket_n in range(len(self.quantiles) - 1):
            ibis_quantile = compile_ibis_types.literal_to_ibis_scalar(
                self.quantiles[bucket_n + 1]
            )
            out = out.when(
                percent_ranks <= ibis_quantile,
                compile_ibis_types.literal_to_ibis_scalar(
                    bucket_n, force_dtype=pd.Int64Dtype()
                ),
            )
        out = out.else_(None)
        return out.end()  # type: ignore


@compile_unary_agg.register
def _(
    op: agg_ops.NuniqueOp,
    column: ibis_types.Column,
    window=None,
) -> ibis_types.IntegerValue:
    return _apply_window_if_present(column.nunique(), window)


@compile_unary_agg.register
def _(
    op: agg_ops.AnyValueOp,
    column: ibis_types.Column,
    window=None,
) -> ibis_types.IntegerValue:
    return _apply_window_if_present(column.arbitrary(), window)


@compile_unary_agg.register
def _(
    op: agg_ops.RankOp,
    column: ibis_types.Column,
    window=None,
) -> ibis_types.IntegerValue:
    # Ibis produces 0-based ranks, while pandas creates 1-based ranks
    return _apply_window_if_present(ibis.rank(), window) + 1


@compile_unary_agg.register
def _(
    op: agg_ops.DenseRankOp,
    column: ibis_types.Column,
    window=None,
) -> ibis_types.IntegerValue:
    # Ibis produces 0-based ranks, while pandas creates 1-based ranks
    return _apply_window_if_present(column.dense_rank(), window) + 1


@compile_unary_agg.register
def _(op: agg_ops.FirstOp, column: ibis_types.Column, window=None) -> ibis_types.Value:
    return _apply_window_if_present(column.first(), window)


@compile_unary_agg.register
def _(
    op: agg_ops.FirstNonNullOp,
    column: ibis_types.Column,
    window=None,
) -> ibis_types.Value:
    return _apply_window_if_present(
        vendored_ibis_ops.FirstNonNullValue(column).to_expr(), window  # type: ignore
    )


@compile_unary_agg.register
def _(
    op: agg_ops.LastOp,
    column: ibis_types.Column,
    window=None,
) -> ibis_types.Value:
    return _apply_window_if_present(column.last(), window)


@compile_unary_agg.register
def _(
    op: agg_ops.LastNonNullOp,
    column: ibis_types.Column,
    window=None,
) -> ibis_types.Value:
    return _apply_window_if_present(
        vendored_ibis_ops.LastNonNullValue(column).to_expr(), window  # type: ignore
    )


@compile_unary_agg.register
def _(
    op: agg_ops.ShiftOp,
    column: ibis_types.Column,
    window=None,
) -> ibis_types.Value:
    if op.periods == 0:  # No-op
        return column
    if op.periods > 0:
        return _apply_window_if_present(column.lag(op.periods), window)
    return _apply_window_if_present(column.lead(-op.periods), window)


@compile_unary_agg.register
def _(
    op: agg_ops.DiffOp,
    column: ibis_types.Column,
    window=None,
) -> ibis_types.Value:
    shifted = compile_unary_agg(agg_ops.ShiftOp(op.periods), column, window)
    if column.type().is_boolean():
        return cast(ibis_types.BooleanColumn, column) != cast(
            ibis_types.BooleanColumn, shifted
        )
    elif column.type().is_numeric():
        return cast(ibis_types.NumericColumn, column) - cast(
            ibis_types.NumericColumn, shifted
        )
    else:
        raise TypeError(f"Cannot perform diff on type{column.type()}")


@compile_unary_agg.register
def _(
    op: agg_ops.AllOp,
    column: ibis_types.Column,
    window=None,
) -> ibis_types.BooleanValue:
    # BQ will return null for empty column, result would be false in pandas.
    result = _apply_window_if_present(_is_true(column).all(), window)
    literal = ibis_types.literal(True)

    return cast(
        ibis_types.BooleanScalar,
        result.fill_null(literal)
        if hasattr(result, "fill_null")
        else result.fillna(literal),
    )


@compile_unary_agg.register
def _(
    op: agg_ops.AnyOp,
    column: ibis_types.Column,
    window=None,
) -> ibis_types.BooleanValue:
    # BQ will return null for empty column, result would be false in pandas.
    result = _apply_window_if_present(_is_true(column).any(), window)
    literal = ibis_types.literal(False)

    return cast(
        ibis_types.BooleanScalar,
        result.fill_null(literal)
        if hasattr(result, "fill_null")
        else result.fillna(literal),
    )


@compile_ordered_unary_agg.register
def _(
    op: agg_ops.ArrayAggOp,
    column: ibis_types.Column,
    window=None,
    order_by: typing.Sequence[ibis_types.Value] = [],
) -> ibis_types.ArrayValue:
    # BigQuery doesn't currently support using ARRAY_AGG with both window and aggregate
    # functions simultaneously. Some aggregate functions (or its equivalent syntax)
    # are more important, such as:
    #    - `IGNORE NULLS` are required to avoid an raised error if the final result
    #      contains a NULL element.
    #    - `ORDER BY` are required for the default ordering mode.
    # To keep things simpler, windowing support is skipped for now.
    if window is not None:
        raise NotImplementedError(
            f"ArrayAgg with windowing is not supported. {constants.FEEDBACK_LINK}"
        )

    return vendored_ibis_ops.ArrayAggregate(
        column,
        order_by=order_by,
    ).to_expr()


@compile_binary_agg.register
def _(
    op: agg_ops.CorrOp, left: ibis_types.Column, right: ibis_types.Column, window=None
) -> ibis_types.NumericValue:
    # Will be null if all inputs are null. Pandas defaults to zero sum though.
    left_numeric = cast(ibis_types.NumericColumn, left)
    right_numeric = cast(ibis_types.NumericColumn, right)
    bq_corr = _apply_window_if_present(
        left_numeric.corr(right_numeric, how="pop"), window
    )
    return cast(ibis_types.NumericColumn, bq_corr)


@compile_binary_agg.register
def _(
    op: agg_ops.CovOp, left: ibis_types.Column, right: ibis_types.Column, window=None
) -> ibis_types.NumericValue:
    # Will be null if all inputs are null. Pandas defaults to zero sum though.
    left_numeric = cast(ibis_types.NumericColumn, left)
    right_numeric = cast(ibis_types.NumericColumn, right)
    bq_cov = _apply_window_if_present(
        left_numeric.cov(right_numeric, how="sample"), window
    )
    return cast(ibis_types.NumericColumn, bq_cov)


def _apply_window_if_present(value: ibis_types.Value, window):
    return value.over(window) if (window is not None) else value


def _map_to_literal(
    original: ibis_types.Value, literal: ibis_types.Scalar
) -> ibis_types.Column:
    # Hack required to perform aggregations on literals in ibis, even though bigquery will let you directly aggregate literals (eg. 'SELECT COUNT(1) from table1')
    return ibis.ifelse(original.isnull(), literal, literal)  # type: ignore


def _ibis_num(number: float):
    return typing.cast(ibis_types.NumericValue, ibis_types.literal(number))


def _is_true(column: ibis_types.Column) -> ibis_types.BooleanColumn:
    if column.type().is_boolean():
        return cast(ibis_types.BooleanColumn, column)
    elif column.type().is_numeric():
        result = cast(ibis_types.NumericColumn, column).__ne__(ibis_types.literal(0))
        return cast(ibis_types.BooleanColumn, result)
    elif column.type().is_string():
        result = cast(ibis_types.StringValue, column).length() > ibis_types.literal(0)
        return cast(ibis_types.BooleanColumn, result)
    else:
        # Time and geo values don't have a 'False' value
        return cast(
            ibis_types.BooleanColumn, _map_to_literal(column, ibis_types.literal(True))
        )
