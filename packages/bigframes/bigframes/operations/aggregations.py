# Copyright 2023 Google LLC
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

import ibis
import ibis.expr.datatypes as ibis_dtypes
import ibis.expr.types as ibis_types

import bigframes.constants as constants
import third_party.bigframes_vendored.ibis.expr.operations as vendored_ibis_ops


class WindowOp:
    def _as_ibis(self, value: ibis_types.Column, window=None):
        raise NotImplementedError("Base class WindowOp has no implementaiton.")

    @property
    def skips_nulls(self):
        """Whether the window op skips null rows."""
        return True

    @property
    def handles_ties(self):
        """Whether the operator can handle ties without nondeterministic output. (eg. rank operator can handle ties but not the count operator)"""
        return False


class AggregateOp(WindowOp):
    name = "abstract_aggregate"

    def _as_ibis(self, value: ibis_types.Column, window=None):
        raise NotImplementedError("Base class AggregateOp has no implementaiton.")


def numeric_op(operation):
    def constrained_op(op, column: ibis_types.Column, window=None):
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


class SumOp(AggregateOp):
    name = "sum"

    @numeric_op
    def _as_ibis(
        self, column: ibis_types.NumericColumn, window=None
    ) -> ibis_types.NumericValue:
        # Will be null if all inputs are null. Pandas defaults to zero sum though.
        bq_sum = _apply_window_if_present(column.sum(), window)
        return (
            ibis.case().when(bq_sum.isnull(), ibis_types.literal(0)).else_(bq_sum).end()
        )


class MedianOp(AggregateOp):
    name = "median"

    @numeric_op
    def _as_ibis(
        self, column: ibis_types.NumericColumn, window=None
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
        return typing.cast(ibis_types.NumericValue, column.approx_median())


class ApproxQuartilesOp(AggregateOp):
    def __init__(self, quartile: int):
        self.name = f"{quartile*25}%"
        self._quartile = quartile

    @numeric_op
    def _as_ibis(
        self, column: ibis_types.NumericColumn, window=None
    ) -> ibis_types.NumericValue:
        # PERCENTILE_CONT has very few allowed windows. For example, "window
        # framing clause is not allowed for analytic function percentile_cont".
        if window is not None:
            raise NotImplementedError(
                f"Approx Quartiles with windowing is not supported. {constants.FEEDBACK_LINK}"
            )
        value = vendored_ibis_ops.ApproximateMultiQuantile(
            column, num_bins=4  # type: ignore
        ).to_expr()[self._quartile]
        return typing.cast(ibis_types.NumericValue, value)


class MeanOp(AggregateOp):
    name = "mean"

    @numeric_op
    def _as_ibis(
        self, column: ibis_types.NumericColumn, window=None
    ) -> ibis_types.NumericValue:
        return _apply_window_if_present(column.mean(), window)


class ProductOp(AggregateOp):
    name = "product"

    @numeric_op
    def _as_ibis(
        self, column: ibis_types.NumericColumn, window=None
    ) -> ibis_types.NumericValue:
        # Need to short-circuit as log with zeroes is illegal sql
        is_zero = typing.cast(ibis_types.BooleanColumn, (column == 0))

        # There is no product sql aggregate function, so must implement as a sum of logs, and then
        # apply power after. Note, log and power base must be equal! This impl uses base 2.
        logs = typing.cast(
            ibis_types.NumericColumn,
            ibis.case().when(is_zero, 0).else_(column.abs().log2()).end(),
        )
        logs_sum = _apply_window_if_present(logs.sum(), window)
        magnitude = typing.cast(ibis_types.NumericValue, ibis_types.literal(2)).pow(
            logs_sum
        )

        # Can't determine sign from logs, so have to determine parity of count of negative inputs
        is_negative = typing.cast(
            ibis_types.NumericColumn,
            ibis.case().when(column.sign() == -1, 1).else_(0).end(),
        )
        negative_count = _apply_window_if_present(is_negative.sum(), window)
        negative_count_parity = negative_count % typing.cast(
            ibis_types.NumericValue, ibis.literal(2)
        )  # 1 if result should be negative, otherwise 0

        any_zeroes = _apply_window_if_present(is_zero.any(), window)
        float_result = (
            ibis.case()
            .when(any_zeroes, ibis_types.literal(0))
            .else_(magnitude * pow(-1, negative_count_parity))
            .end()
        )
        return float_result.cast(column.type())


class MaxOp(AggregateOp):
    name = "max"

    def _as_ibis(self, column: ibis_types.Column, window=None) -> ibis_types.Value:
        return _apply_window_if_present(column.max(), window)


class MinOp(AggregateOp):
    name = "min"

    def _as_ibis(self, column: ibis_types.Column, window=None) -> ibis_types.Value:
        return _apply_window_if_present(column.min(), window)


class StdOp(AggregateOp):
    name = "std"

    @numeric_op
    def _as_ibis(self, x: ibis_types.Column, window=None) -> ibis_types.Value:
        return _apply_window_if_present(
            typing.cast(ibis_types.NumericColumn, x).std(), window
        )


class VarOp(AggregateOp):
    name = "var"

    @numeric_op
    def _as_ibis(self, x: ibis_types.Column, window=None) -> ibis_types.Value:
        return _apply_window_if_present(
            typing.cast(ibis_types.NumericColumn, x).var(), window
        )


class CountOp(AggregateOp):
    name = "count"

    def _as_ibis(
        self, column: ibis_types.Column, window=None
    ) -> ibis_types.IntegerValue:
        return _apply_window_if_present(column.count(), window)

    @property
    def skips_nulls(self):
        return False


class CutOp(WindowOp):
    def __init__(self, bins: int):
        self._bins = bins

    def _as_ibis(self, x: ibis_types.Column, window=None):
        col_min = _apply_window_if_present(x.min(), window)
        col_max = _apply_window_if_present(x.max(), window)
        bin_width = (col_max - col_min) / self._bins
        out = ibis.case()
        for bin in range(self._bins - 1):
            out = out.when(x <= (col_min + (bin + 1) * bin_width), bin)
        out = out.when(x.notnull(), self._bins - 1)
        return out.end()

    @property
    def skips_nulls(self):
        return False

    @property
    def handles_ties(self):
        return True


class NuniqueOp(AggregateOp):
    name = "nunique"

    def _as_ibis(
        self, column: ibis_types.Column, window=None
    ) -> ibis_types.IntegerValue:
        return _apply_window_if_present(column.nunique(), window)

    @property
    def skips_nulls(self):
        return False


class RankOp(WindowOp):
    name = "rank"

    def _as_ibis(
        self, column: ibis_types.Column, window=None
    ) -> ibis_types.IntegerValue:
        # Ibis produces 0-based ranks, while pandas creates 1-based ranks
        return _apply_window_if_present(column.rank(), window) + 1

    @property
    def skips_nulls(self):
        return False

    @property
    def handles_ties(self):
        return True


class DenseRankOp(WindowOp):
    def _as_ibis(
        self, column: ibis_types.Column, window=None
    ) -> ibis_types.IntegerValue:
        # Ibis produces 0-based ranks, while pandas creates 1-based ranks
        return _apply_window_if_present(column.dense_rank(), window) + 1

    @property
    def skips_nulls(self):
        return False

    @property
    def handles_ties(self):
        return True


class FirstOp(WindowOp):
    def _as_ibis(self, column: ibis_types.Column, window=None) -> ibis_types.Value:
        return _apply_window_if_present(column.first(), window)


class ShiftOp(WindowOp):
    def __init__(self, periods: int):
        self._periods = periods

    def _as_ibis(self, column: ibis_types.Column, window=None) -> ibis_types.Value:
        if self._periods == 0:  # No-op
            return column
        if self._periods > 0:
            return _apply_window_if_present(column.lag(self._periods), window)
        return _apply_window_if_present(column.lead(-self._periods), window)

    @property
    def skips_nulls(self):
        return False


class AllOp(AggregateOp):
    def _as_ibis(
        self, column: ibis_types.Column, window=None
    ) -> ibis_types.BooleanValue:
        # BQ will return null for empty column, result would be true in pandas.
        result = _is_true(column).all()
        return typing.cast(
            ibis_types.BooleanScalar,
            _apply_window_if_present(result, window).fillna(ibis_types.literal(True)),
        )


class AnyOp(AggregateOp):
    name = "any"

    def _as_ibis(
        self, column: ibis_types.Column, window=None
    ) -> ibis_types.BooleanValue:
        # BQ will return null for empty column, result would be false in pandas.
        result = _is_true(column).any()
        return typing.cast(
            ibis_types.BooleanScalar,
            _apply_window_if_present(result, window).fillna(ibis_types.literal(True)),
        )


def _is_true(column: ibis_types.Column) -> ibis_types.BooleanColumn:
    if column.type().is_boolean():
        return typing.cast(ibis_types.BooleanColumn, column)
    elif column.type().is_numeric():
        result = typing.cast(ibis_types.NumericColumn, column).__ne__(
            ibis_types.literal(0)
        )
        return typing.cast(ibis_types.BooleanColumn, result)
    elif column.type().is_string():
        result = typing.cast(
            ibis_types.StringValue, column
        ).length() > ibis_types.literal(0)
        return typing.cast(ibis_types.BooleanColumn, result)
    else:
        # Time and geo values don't have a 'False' value
        return typing.cast(
            ibis_types.BooleanColumn, _map_to_literal(column, ibis_types.literal(True))
        )


def _apply_window_if_present(value: ibis_types.Value, window):
    return value.over(window) if (window is not None) else value


def _map_to_literal(
    original: ibis_types.Value, literal: ibis_types.Scalar
) -> ibis_types.Column:
    # Hack required to perform aggregations on literals in ibis, even though bigquery will let you directly aggregate literals (eg. 'SELECT COUNT(1) from table1')
    return ibis.ifelse(original.isnull(), literal, literal)


sum_op = SumOp()
mean_op = MeanOp()
median_op = MedianOp()
product_op = ProductOp()
max_op = MaxOp()
min_op = MinOp()
std_op = StdOp()
var_op = VarOp()
count_op = CountOp()
nunique_op = NuniqueOp()
rank_op = RankOp()
dense_rank_op = DenseRankOp()
all_op = AllOp()
any_op = AnyOp()
first_op = FirstOp()


# TODO: Alternative names and lookup from numpy function objects
AGGREGATIONS_LOOKUP: dict[str, AggregateOp] = {
    op.name: op
    for op in [
        sum_op,
        mean_op,
        median_op,
        product_op,
        max_op,
        min_op,
        std_op,
        var_op,
        count_op,
        all_op,
        any_op,
        nunique_op,
        ApproxQuartilesOp(1),
        ApproxQuartilesOp(2),
        ApproxQuartilesOp(3),
    ]
}
