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

from pandas import Int64Dtype
import pandas as pd

import bigframes.dtypes as dtypes


class WindowOp:
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


class SumOp(AggregateOp):
    name = "sum"


class MedianOp(AggregateOp):
    name = "median"


class ApproxQuartilesOp(AggregateOp):
    def __init__(self, quartile: int):
        self.name = f"{quartile*25}%"
        self._quartile = quartile


class MeanOp(AggregateOp):
    name = "mean"


class ProductOp(AggregateOp):
    name = "product"


class MaxOp(AggregateOp):
    name = "max"


class MinOp(AggregateOp):
    name = "min"


class StdOp(AggregateOp):
    name = "std"


class VarOp(AggregateOp):
    name = "var"


class PopVarOp(AggregateOp):
    name = "popvar"


class CountOp(AggregateOp):
    name = "count"

    @property
    def skips_nulls(self):
        return False


class CutOp(WindowOp):
    def __init__(self, bins: typing.Union[int, pd.IntervalIndex], labels=None):
        if isinstance(bins, int):
            if not bins > 0:
                raise ValueError("`bins` should be a positive integer.")
            self._bins_int = bins
            self._bins = dtypes.literal_to_ibis_scalar(bins, force_dtype=Int64Dtype())
        else:
            self._bins_int = 0
            self._bins = bins

        self._labels = labels

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

    @property
    def skips_nulls(self):
        return False

    @property
    def handles_ties(self):
        return True


class NuniqueOp(AggregateOp):
    name = "nunique"

    @property
    def skips_nulls(self):
        return False


class AnyValueOp(AggregateOp):
    # Warning: only use if all values are equal. Non-deterministic otherwise.
    # Do not expose to users. For special cases only (e.g. pivot).
    name = "any_value"

    @property
    def skips_nulls(self):
        return True


class RankOp(WindowOp):
    name = "rank"

    @property
    def skips_nulls(self):
        return False

    @property
    def handles_ties(self):
        return True


class DenseRankOp(WindowOp):
    @property
    def skips_nulls(self):
        return False

    @property
    def handles_ties(self):
        return True


class FirstOp(WindowOp):
    name = "first"


class FirstNonNullOp(WindowOp):
    @property
    def skips_nulls(self):
        return False


class LastOp(WindowOp):
    name = "last"


class LastNonNullOp(WindowOp):
    @property
    def skips_nulls(self):
        return False


class ShiftOp(WindowOp):
    def __init__(self, periods: int):
        self._periods = periods

    @property
    def skips_nulls(self):
        return False


class DiffOp(WindowOp):
    def __init__(self, periods: int):
        self._periods = periods

    @property
    def skips_nulls(self):
        return False


class AllOp(AggregateOp):
    name = "all"


class AnyOp(AggregateOp):
    name = "any"


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
