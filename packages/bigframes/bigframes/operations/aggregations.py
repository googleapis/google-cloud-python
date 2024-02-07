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

import abc
import dataclasses
import typing
from typing import ClassVar, Hashable, Optional, Tuple


@dataclasses.dataclass(frozen=True)
class WindowOp:
    @property
    def skips_nulls(self):
        """Whether the window op skips null rows."""
        return True

    @property
    def handles_ties(self):
        """Whether the operator can handle ties without nondeterministic output. (eg. rank operator can handle ties but not the count operator)"""
        return False


@dataclasses.dataclass(frozen=True)
class UnaryWindowOp(WindowOp):
    @property
    def arguments(self) -> int:
        return 1


@dataclasses.dataclass(frozen=True)
class AggregateOp(WindowOp):
    """Aggregate ops can be applied with or without a window clause."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def arguments(self) -> int:
        ...


@dataclasses.dataclass(frozen=True)
class UnaryAggregateOp(AggregateOp, UnaryWindowOp):
    @property
    def arguments(self) -> int:
        return 1


@dataclasses.dataclass(frozen=True)
class BinaryAggregateOp(AggregateOp):
    @property
    def arguments(self) -> int:
        return 2


@dataclasses.dataclass(frozen=True)
class SumOp(UnaryAggregateOp):
    name: ClassVar[str] = "sum"


@dataclasses.dataclass(frozen=True)
class MedianOp(UnaryAggregateOp):
    name: ClassVar[str] = "median"


@dataclasses.dataclass(frozen=True)
class ApproxQuartilesOp(UnaryAggregateOp):
    quartile: int

    @property
    def name(self):
        return f"{self.quartile*25}%"


@dataclasses.dataclass(frozen=True)
class MeanOp(UnaryAggregateOp):
    name: ClassVar[str] = "mean"


@dataclasses.dataclass(frozen=True)
class ProductOp(UnaryAggregateOp):
    name: ClassVar[str] = "product"


@dataclasses.dataclass(frozen=True)
class MaxOp(UnaryAggregateOp):
    name: ClassVar[str] = "max"


@dataclasses.dataclass(frozen=True)
class MinOp(UnaryAggregateOp):
    name: ClassVar[str] = "min"


@dataclasses.dataclass(frozen=True)
class StdOp(UnaryAggregateOp):
    name: ClassVar[str] = "std"


@dataclasses.dataclass(frozen=True)
class VarOp(UnaryAggregateOp):
    name: ClassVar[str] = "var"


@dataclasses.dataclass(frozen=True)
class PopVarOp(UnaryAggregateOp):
    name: ClassVar[str] = "popvar"


@dataclasses.dataclass(frozen=True)
class CountOp(UnaryAggregateOp):
    name: ClassVar[str] = "count"

    @property
    def skips_nulls(self):
        return False


@dataclasses.dataclass(frozen=True)
class CutOp(UnaryWindowOp):
    # TODO: Unintuitive, refactor into multiple ops?
    bins: typing.Union[int, Tuple[Tuple[Hashable, Hashable], ...]]
    labels: Optional[bool]

    @property
    def skips_nulls(self):
        return False

    @property
    def handles_ties(self):
        return True


@dataclasses.dataclass(frozen=True)
class QcutOp(UnaryWindowOp):
    quantiles: typing.Union[int, typing.Tuple[float, ...]]

    @property
    def name(self):
        return f"qcut-{self.quantiles}"

    @property
    def skips_nulls(self):
        return False

    @property
    def handles_ties(self):
        return True


@dataclasses.dataclass(frozen=True)
class NuniqueOp(UnaryAggregateOp):
    name: ClassVar[str] = "nunique"

    @property
    def skips_nulls(self):
        return False


@dataclasses.dataclass(frozen=True)
class AnyValueOp(UnaryAggregateOp):
    # Warning: only use if all values are equal. Non-deterministic otherwise.
    # Do not expose to users. For special cases only (e.g. pivot).
    name: ClassVar[str] = "any_value"

    @property
    def skips_nulls(self):
        return True


@dataclasses.dataclass(frozen=True)
class RankOp(UnaryWindowOp):
    name: ClassVar[str] = "rank"

    @property
    def skips_nulls(self):
        return False

    @property
    def handles_ties(self):
        return True


@dataclasses.dataclass(frozen=True)
class DenseRankOp(UnaryWindowOp):
    @property
    def skips_nulls(self):
        return False

    @property
    def handles_ties(self):
        return True


@dataclasses.dataclass(frozen=True)
class FirstOp(UnaryWindowOp):
    name: ClassVar[str] = "first"


@dataclasses.dataclass(frozen=True)
class FirstNonNullOp(UnaryWindowOp):
    @property
    def skips_nulls(self):
        return False


@dataclasses.dataclass(frozen=True)
class LastOp(UnaryWindowOp):
    name: ClassVar[str] = "last"


@dataclasses.dataclass(frozen=True)
class LastNonNullOp(UnaryWindowOp):
    @property
    def skips_nulls(self):
        return False


@dataclasses.dataclass(frozen=True)
class ShiftOp(UnaryWindowOp):
    periods: int

    @property
    def skips_nulls(self):
        return False


@dataclasses.dataclass(frozen=True)
class DiffOp(UnaryWindowOp):
    periods: int

    @property
    def skips_nulls(self):
        return False


@dataclasses.dataclass(frozen=True)
class AllOp(UnaryAggregateOp):
    name: ClassVar[str] = "all"


@dataclasses.dataclass(frozen=True)
class AnyOp(UnaryAggregateOp):
    name: ClassVar[str] = "any"


@dataclasses.dataclass(frozen=True)
class CorrOp(BinaryAggregateOp):
    name: ClassVar[str] = "corr"


@dataclasses.dataclass(frozen=True)
class CovOp(BinaryAggregateOp):
    name: ClassVar[str] = "cov"


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
_AGGREGATIONS_LOOKUP: dict[str, UnaryAggregateOp] = {
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


def lookup_agg_func(key: str) -> UnaryAggregateOp:
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
