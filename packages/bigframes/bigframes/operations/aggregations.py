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
from typing import ClassVar, Iterable, Optional

import pandas as pd
import pyarrow as pa

import bigframes.dtypes as dtypes
import bigframes.operations.type as signatures


@dataclasses.dataclass(frozen=True)
class WindowOp:
    @property
    def skips_nulls(self):
        """Whether the window op skips null rows."""
        return True

    @property
    def uses_total_row_ordering(self):
        """Whether the operator needs total row ordering. (eg. lead, lag, array_agg)"""
        return False

    @property
    def can_order_by(self):
        return False

    @property
    def order_independent(self):
        """
        True if the output of the operator does not depend on the ordering of input rows.

        Navigation functions are a notable case that are not order independent.
        """
        return False

    @abc.abstractmethod
    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        ...


@dataclasses.dataclass(frozen=True)
class NullaryWindowOp(WindowOp):
    @property
    def arguments(self) -> int:
        return 0


@dataclasses.dataclass(frozen=True)
class UnaryWindowOp(WindowOp):
    @property
    def arguments(self) -> int:
        return 1

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return input_types[0]


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

    @property
    def order_independent(self):
        """
        True if results don't depend on the order of the input.

        Almost all aggregation functions are order independent, excepting ``array_agg`` and ``string_agg``.
        """
        return not self.can_order_by


@dataclasses.dataclass(frozen=True)
class NullaryAggregateOp(AggregateOp, NullaryWindowOp):
    @property
    def arguments(self) -> int:
        return 0


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
class SizeOp(NullaryAggregateOp):
    name: ClassVar[str] = "size"

    def output_type(self, *input_types: dtypes.ExpressionType):
        return dtypes.INT_DTYPE


@dataclasses.dataclass(frozen=True)
class SumOp(UnaryAggregateOp):
    name: ClassVar[str] = "sum"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        if not dtypes.is_numeric(input_types[0]):
            raise TypeError(f"Type {input_types[0]} is not numeric")
        if pd.api.types.is_bool_dtype(input_types[0]):
            return dtypes.INT_DTYPE
        else:
            return input_types[0]


@dataclasses.dataclass(frozen=True)
class MedianOp(UnaryAggregateOp):
    name: ClassVar[str] = "median"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        # These will change if median is changed to exact implementation.
        if not dtypes.is_orderable(input_types[0]):
            raise TypeError(f"Type {input_types[0]} is not orderable")
        if pd.api.types.is_bool_dtype(input_types[0]):
            return dtypes.INT_DTYPE
        else:
            return input_types[0]


@dataclasses.dataclass(frozen=True)
class QuantileOp(UnaryAggregateOp):
    q: float

    @property
    def name(self):
        return f"{int(self.q * 100)}%"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return signatures.UNARY_REAL_NUMERIC.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class ApproxQuartilesOp(UnaryAggregateOp):
    quartile: int

    @property
    def name(self):
        return f"{self.quartile * 25}%"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        if not dtypes.is_orderable(input_types[0]):
            raise TypeError(f"Type {input_types[0]} is not orderable")
        if pd.api.types.is_bool_dtype(input_types[0]) or pd.api.types.is_integer_dtype(
            input_types[0]
        ):
            return dtypes.FLOAT_DTYPE
        else:
            return input_types[0]


@dataclasses.dataclass(frozen=True)
class ApproxTopCountOp(UnaryAggregateOp):
    name: typing.ClassVar[str] = "approx_top_count"
    number: int

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        if not dtypes.is_orderable(input_types[0]):
            raise TypeError(f"Type {input_types[0]} is not orderable")

        input_type = input_types[0]
        fields = [
            pa.field("value", dtypes.bigframes_dtype_to_arrow_dtype(input_type)),
            pa.field("count", pa.int64()),
        ]
        return pd.ArrowDtype(pa.list_(pa.struct(fields)))


@dataclasses.dataclass(frozen=True)
class MeanOp(UnaryAggregateOp):
    name: ClassVar[str] = "mean"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return signatures.UNARY_REAL_NUMERIC.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class ProductOp(UnaryAggregateOp):
    name: ClassVar[str] = "product"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return signatures.FixedOutputType(
            dtypes.is_numeric, dtypes.FLOAT_DTYPE, "numeric"
        ).output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class MaxOp(UnaryAggregateOp):
    name: ClassVar[str] = "max"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return signatures.TypePreserving(dtypes.is_orderable, "orderable").output_type(
            input_types[0]
        )


@dataclasses.dataclass(frozen=True)
class MinOp(UnaryAggregateOp):
    name: ClassVar[str] = "min"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return signatures.TypePreserving(dtypes.is_orderable, "orderable").output_type(
            input_types[0]
        )


@dataclasses.dataclass(frozen=True)
class StdOp(UnaryAggregateOp):
    name: ClassVar[str] = "std"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return signatures.FixedOutputType(
            dtypes.is_numeric, dtypes.FLOAT_DTYPE, "numeric"
        ).output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class VarOp(UnaryAggregateOp):
    name: ClassVar[str] = "var"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return signatures.FixedOutputType(
            dtypes.is_numeric, dtypes.FLOAT_DTYPE, "numeric"
        ).output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class PopVarOp(UnaryAggregateOp):
    name: ClassVar[str] = "popvar"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return signatures.FixedOutputType(
            dtypes.is_numeric, dtypes.FLOAT_DTYPE, "numeric"
        ).output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class CountOp(UnaryAggregateOp):
    name: ClassVar[str] = "count"

    @property
    def skips_nulls(self):
        return False

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return signatures.FixedOutputType(
            lambda x: True, dtypes.INT_DTYPE, ""
        ).output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class ArrayAggOp(UnaryAggregateOp):
    name: ClassVar[str] = "arrayagg"

    @property
    def can_order_by(self):
        return True

    @property
    def skips_nulls(self):
        return True

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return pd.ArrowDtype(
            pa.list_(dtypes.bigframes_dtype_to_arrow_dtype(input_types[0]))
        )


@dataclasses.dataclass(frozen=True)
class CutOp(UnaryWindowOp):
    # TODO: Unintuitive, refactor into multiple ops?
    bins: typing.Union[int, Iterable]
    labels: Optional[bool]

    @property
    def skips_nulls(self):
        return False

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        if isinstance(self.bins, int) and (self.labels is False):
            return dtypes.INT_DTYPE
        else:
            # Assumption: buckets use same numeric type
            interval_dtype = (
                pa.float64()
                if isinstance(self.bins, int)
                else dtypes.infer_literal_arrow_type(list(self.bins)[0][0])
            )
            pa_type = pa.struct(
                [
                    pa.field("left_exclusive", interval_dtype, nullable=True),
                    pa.field("right_inclusive", interval_dtype, nullable=True),
                ]
            )
            return pd.ArrowDtype(pa_type)

    @property
    def order_independent(self):
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

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return signatures.FixedOutputType(
            dtypes.is_orderable, dtypes.INT_DTYPE, "orderable"
        ).output_type(input_types[0])

    @property
    def order_independent(self):
        return True


@dataclasses.dataclass(frozen=True)
class NuniqueOp(UnaryAggregateOp):
    name: ClassVar[str] = "nunique"

    @property
    def skips_nulls(self):
        return False

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return dtypes.INT_DTYPE


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

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return signatures.FixedOutputType(
            dtypes.is_orderable, dtypes.INT_DTYPE, "orderable"
        ).output_type(input_types[0])

    @property
    def order_independent(self):
        return True


@dataclasses.dataclass(frozen=True)
class DenseRankOp(UnaryWindowOp):
    @property
    def skips_nulls(self):
        return False

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return signatures.FixedOutputType(
            dtypes.is_orderable, dtypes.INT_DTYPE, "orderable"
        ).output_type(input_types[0])

    @property
    def order_independent(self):
        return True


@dataclasses.dataclass(frozen=True)
class FirstOp(UnaryWindowOp):
    name: ClassVar[str] = "first"

    @property
    def uses_total_row_ordering(self):
        return True


@dataclasses.dataclass(frozen=True)
class FirstNonNullOp(UnaryWindowOp):
    @property
    def uses_total_row_ordering(self):
        return True

    @property
    def skips_nulls(self):
        return False


@dataclasses.dataclass(frozen=True)
class LastOp(UnaryWindowOp):
    name: ClassVar[str] = "last"

    @property
    def uses_total_row_ordering(self):
        return True


@dataclasses.dataclass(frozen=True)
class LastNonNullOp(UnaryWindowOp):
    @property
    def uses_total_row_ordering(self):
        return True

    @property
    def skips_nulls(self):
        return False


@dataclasses.dataclass(frozen=True)
class ShiftOp(UnaryWindowOp):
    periods: int

    @property
    def uses_total_row_ordering(self):
        return True

    @property
    def skips_nulls(self):
        return False


@dataclasses.dataclass(frozen=True)
class DiffOp(UnaryWindowOp):
    periods: int

    @property
    def uses_total_row_ordering(self):
        return True

    @property
    def skips_nulls(self):
        return False


@dataclasses.dataclass(frozen=True)
class AllOp(UnaryAggregateOp):
    name: ClassVar[str] = "all"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return signatures.FixedOutputType(
            dtypes.is_bool_coercable, dtypes.BOOL_DTYPE, "convertible to boolean"
        ).output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class AnyOp(UnaryAggregateOp):
    name: ClassVar[str] = "any"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return signatures.FixedOutputType(
            dtypes.is_bool_coercable, dtypes.BOOL_DTYPE, "convertible to boolean"
        ).output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class CorrOp(BinaryAggregateOp):
    name: ClassVar[str] = "corr"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return signatures.BINARY_REAL_NUMERIC.output_type(
            input_types[0], input_types[1]
        )


@dataclasses.dataclass(frozen=True)
class CovOp(BinaryAggregateOp):
    name: ClassVar[str] = "cov"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return signatures.BINARY_REAL_NUMERIC.output_type(
            input_types[0], input_types[1]
        )


size_op = SizeOp()
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
_AGGREGATIONS_LOOKUP: typing.Dict[
    str, typing.Union[UnaryAggregateOp, NullaryAggregateOp]
] = {
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
    + [
        # Add size_op separately to avoid Mypy type inference errors.
        size_op,
    ]
}


def lookup_agg_func(key: str) -> typing.Union[UnaryAggregateOp, NullaryAggregateOp]:
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


def is_agg_op_supported(dtype: dtypes.Dtype, op: AggregateOp) -> bool:
    if dtype in dtypes.NUMERIC_BIGFRAMES_TYPES_PERMISSIVE:
        return True

    if dtype in (dtypes.STRING_DTYPE, dtypes.BOOL_DTYPE, dtypes.BYTES_DTYPE):
        return isinstance(op, (CountOp, NuniqueOp))

    # For all other types, support no aggregation
    return False
