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
from pandas import Int64Dtype

import bigframes.constants as constants
import bigframes.dtypes as dtypes
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


class PopVarOp(AggregateOp):
    name = "popvar"

    @numeric_op
    def _as_ibis(self, x: ibis_types.Column, window=None) -> ibis_types.Value:
        return _apply_window_if_present(
            typing.cast(ibis_types.NumericColumn, x).var(how="pop"), window
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
        self._bins_ibis = dtypes.literal_to_ibis_scalar(bins, force_dtype=Int64Dtype())
        self._bins_int = bins

    def _as_ibis(self, x: ibis_types.Column, window=None):
        col_min = _apply_window_if_present(x.min(), window)
        col_max = _apply_window_if_present(x.max(), window)
        bin_width = (col_max - col_min) / self._bins_ibis
        out = ibis.case()
        for this_bin in range(self._bins_int - 1):
            out = out.when(
                x <= (col_min + (this_bin + 1) * bin_width),
                dtypes.literal_to_ibis_scalar(this_bin, force_dtype=Int64Dtype()),
            )
        out = out.when(x.notnull(), self._bins_ibis - 1)
        return out.end()

    @property
    def skips_nulls(self):
        return False

    @property
    def handles_ties(self):
        return True


class QcutOp(WindowOp):
    def __init__(self, quantiles: typing.Union[int, typing.Sequence[float]]):
        self.name = f"qcut-{quantiles}"
        self._quantiles = quantiles

    @numeric_op
    def _as_ibis(
        self, column: ibis_types.Column, window=None
    ) -> ibis_types.IntegerValue:
        if isinstance(self._quantiles, int):
            quantiles_ibis = dtypes.literal_to_ibis_scalar(self._quantiles)
            percent_ranks = typing.cast(
                ibis_types.FloatingColumn,
                _apply_window_if_present(column.percent_rank(), window),
            )
            float_bucket = typing.cast(
                ibis_types.FloatingColumn, (percent_ranks * quantiles_ibis)
            )
            return float_bucket.ceil().clip(lower=_ibis_num(1)) - _ibis_num(1)
        else:
            percent_ranks = typing.cast(
                ibis_types.FloatingColumn,
                _apply_window_if_present(column.percent_rank(), window),
            )
            out = ibis.case()
            first_ibis_quantile = dtypes.literal_to_ibis_scalar(self._quantiles[0])
            out = out.when(percent_ranks < first_ibis_quantile, None)
            for bucket_n in range(len(self._quantiles) - 1):
                ibis_quantile = dtypes.literal_to_ibis_scalar(
                    self._quantiles[bucket_n + 1]
                )
                out = out.when(
                    percent_ranks <= ibis_quantile,
                    dtypes.literal_to_ibis_scalar(bucket_n, force_dtype=Int64Dtype()),
                )
            out = out.else_(None)
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


class AnyValueOp(AggregateOp):
    # Warning: only use if all values are equal. Non-deterministic otherwise.
    # Do not expose to users. For special cases only (e.g. pivot).
    name = "any_value"

    def _as_ibis(
        self, column: ibis_types.Column, window=None
    ) -> ibis_types.IntegerValue:
        return _apply_window_if_present(column.arbitrary(), window)

    @property
    def skips_nulls(self):
        return True


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


class FirstNonNullOp(WindowOp):
    @property
    def skips_nulls(self):
        return False

    def _as_ibis(self, column: ibis_types.Column, window=None) -> ibis_types.Value:
        return _apply_window_if_present(
            vendored_ibis_ops.FirstNonNullValue(column).to_expr(), window  # type: ignore
        )


class LastNonNullOp(WindowOp):
    @property
    def skips_nulls(self):
        return False

    def _as_ibis(self, column: ibis_types.Column, window=None) -> ibis_types.Value:
        return _apply_window_if_present(
            vendored_ibis_ops.LastNonNullValue(column).to_expr(), window  # type: ignore
        )


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


class DiffOp(WindowOp):
    def __init__(self, periods: int):
        self._periods = periods

    def _as_ibis(self, column: ibis_types.Column, window=None) -> ibis_types.Value:
        shifted = ShiftOp(self._periods)._as_ibis(column, window)
        if column.type().is_boolean():
            return typing.cast(ibis_types.BooleanColumn, column) != typing.cast(
                ibis_types.BooleanColumn, shifted
            )
        elif column.type().is_numeric():
            return typing.cast(ibis_types.NumericColumn, column) - typing.cast(
                ibis_types.NumericColumn, shifted
            )
        else:
            raise TypeError(f"Cannot perform diff on type{column.type()}")

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
_AGGREGATIONS_LOOKUP: dict[str, AggregateOp] = {
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


def lookup_agg_func(key: str) -> AggregateOp:
    if callable(key):
        raise NotImplementedError(
            "Aggregating with callable object not supported, pass method name as string instead (eg. 'sum' instead of np.sum)."
        )
    if not isinstance(key, str):
        raise ValueError(
            f"Cannot aggregate using object of type: {type(key)}. Use string method name (eg. 'sum')"
        )
    if key in _AGGREGATIONS_LOOKUP:
        return _AGGREGATIONS_LOOKUP[key]
    else:
        raise ValueError(f"Unrecognize aggregate function: {key}")


def _ibis_num(number: float):
    return typing.cast(ibis_types.NumericValue, ibis_types.literal(number))
