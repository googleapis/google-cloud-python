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

import functools
import typing

import ibis
import ibis.common.exceptions
import ibis.expr.datatypes as ibis_dtypes
import ibis.expr.operations.generic
import ibis.expr.types as ibis_types
import numpy as np
import pandas as pd

import bigframes.constants as constants
import bigframes.dtypes
import bigframes.dtypes as dtypes

_ZERO = typing.cast(ibis_types.NumericValue, ibis_types.literal(0))
_NAN = typing.cast(ibis_types.NumericValue, ibis_types.literal(np.nan))
_INF = typing.cast(ibis_types.NumericValue, ibis_types.literal(np.inf))

BinaryOp = typing.Callable[[ibis_types.Value, ibis_types.Value], ibis_types.Value]
TernaryOp = typing.Callable[
    [ibis_types.Value, ibis_types.Value, ibis_types.Value], ibis_types.Value
]


### Unary Ops
class UnaryOp:
    def _as_ibis(self, x):
        raise NotImplementedError(
            f"Base class UnaryOp has no implementation. {constants.FEEDBACK_LINK}"
        )

    @property
    def is_windowed(self):
        return False


class AbsOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.NumericValue, x).abs()


class InvertOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.NumericValue, x).negate()


class IsNullOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return x.isnull()


class LenOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.StringValue, x).length()


class NotNullOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return x.notnull()


class ReverseOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.StringValue, x).reverse()


class LowerOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.StringValue, x).lower()


class UpperOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.StringValue, x).upper()


class StripOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.StringValue, x).strip()


class IsNumericOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        # catches all members of the Unicode number class, which matches pandas isnumeric
        # see https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#regexp_contains
        return typing.cast(ibis_types.StringValue, x).re_search(r"^(\pN*)$")


class RstripOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.StringValue, x).rstrip()


class LstripOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.StringValue, x).lstrip()


class CapitalizeOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.StringValue, x).capitalize()


class ContainsStringOp(UnaryOp):
    def __init__(self, pat: str, case: bool = True):
        self._pat = pat

    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.StringValue, x).contains(self._pat)


class ContainsRegexOp(UnaryOp):
    def __init__(self, pat: str):
        self._pat = pat

    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.StringValue, x).re_search(self._pat)


class ReplaceStringOp(UnaryOp):
    def __init__(self, pat: str, repl: str):
        self._pat = pat
        self._repl = repl

    def _as_ibis(self, x: ibis_types.Value):
        pat_str_value = typing.cast(
            ibis_types.StringValue, ibis_types.literal(self._pat)
        )
        repl_str_value = typing.cast(
            ibis_types.StringValue, ibis_types.literal(self._pat)
        )

        return typing.cast(ibis_types.StringValue, x).replace(
            pat_str_value, repl_str_value
        )


class ReplaceRegexOp(UnaryOp):
    def __init__(self, pat: str, repl: str):
        self._pat = pat
        self._repl = repl

    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.StringValue, x).re_replace(self._pat, self._repl)


class StartsWithOp(UnaryOp):
    def __init__(self, pat: typing.Sequence[str]):
        self._pat = pat

    def _as_ibis(self, x: ibis_types.Value):
        any_match = None
        for pat in self._pat:
            pat_match = typing.cast(ibis_types.StringValue, x).startswith(pat)
            if any_match is not None:
                any_match = any_match | pat_match
            else:
                any_match = pat_match
        return any_match if any_match is not None else ibis_types.literal(False)


class EndsWithOp(UnaryOp):
    def __init__(self, pat: typing.Sequence[str]):
        self._pat = pat

    def _as_ibis(self, x: ibis_types.Value):
        any_match = None
        for pat in self._pat:
            pat_match = typing.cast(ibis_types.StringValue, x).endswith(pat)
            if any_match is not None:
                any_match = any_match | pat_match
            else:
                any_match = pat_match
        return any_match if any_match is not None else ibis_types.literal(False)


class HashOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.IntegerValue, x).hash()


class DayOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.TimestampValue, x).day()


class DateOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.TimestampValue, x).date()


class DayofweekOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.TimestampValue, x).day_of_week.index()


class HourOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.TimestampValue, x).hour()


class MinuteOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.TimestampValue, x).minute()


class MonthOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.TimestampValue, x).month()


class QuarterOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.TimestampValue, x).quarter()


class SecondOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.TimestampValue, x).second()


class TimeOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.TimestampValue, x).time()


class YearOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.TimestampValue, x).year()


# Parameterized ops
class AsTypeOp(UnaryOp):
    def __init__(self, to_type: dtypes.DtypeString | dtypes.Dtype):
        self.to_type = bigframes.dtypes.bigframes_dtype_to_ibis_dtype(to_type)

    def _as_ibis(self, x: ibis_types.Value):
        if isinstance(x, ibis_types.NullScalar):
            return ibis_types.null().cast(self.to_type)

        return bigframes.dtypes.cast_ibis_value(x, self.to_type)


class FindOp(UnaryOp):
    def __init__(self, sub, start, end):
        self._sub = sub
        self._start = start
        self._end = end

    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.StringValue, x).find(
            self._sub, self._start, self._end
        )


class ExtractOp(UnaryOp):
    def __init__(self, pat: str, n: int = 1):
        self._pat = pat
        self._n = n

    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.StringValue, x).re_extract(self._pat, self._n)


class SliceOp(UnaryOp):
    def __init__(self, start, stop):
        self._start = start
        self._stop = stop

    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.StringValue, x)[self._start : self._stop]


class IsInOp(UnaryOp):
    def __init__(self, values, match_nulls: bool = True):
        self._values = values
        self._match_nulls = match_nulls

    def _as_ibis(self, x: ibis_types.Value):
        if self._match_nulls and any(is_null(value) for value in self._values):
            return x.isnull() | x.isin(
                [val for val in self._values if not is_null(val)]
            )
        else:
            return x.isin(self._values)


class BinopPartialRight(UnaryOp):
    def __init__(self, binop: BinaryOp, right_scalar: typing.Any):
        self._binop = binop
        self._right = dtypes.literal_to_ibis_scalar(right_scalar, validate=False)

    def _as_ibis(self, x):
        return self._binop(x, self._right)


class BinopPartialLeft(UnaryOp):
    def __init__(self, binop: BinaryOp, left_scalar: typing.Any):
        self._binop = binop
        self._left = dtypes.literal_to_ibis_scalar(left_scalar, validate=False)

    def _as_ibis(self, x):
        return self._binop(self._left, x)


class RepeatOp(UnaryOp):
    def __init__(self, repeats):
        self._repeats = repeats

    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.StringValue, x).repeat(self._repeats)


class RemoteFunctionOp(UnaryOp):
    def __init__(self, func: typing.Callable, apply_on_null=True):
        if not hasattr(func, "bigframes_remote_function"):
            raise TypeError(
                f"only a bigframes remote function is supported as a callable. {constants.FEEDBACK_LINK}"
            )

        self._func = func
        self._apply_on_null = apply_on_null

    def _as_ibis(self, x: ibis_types.Value):
        x_transformed = self._func(x)
        if not self._apply_on_null:
            x_transformed = where_op(x, x.isnull(), x_transformed)
        return x_transformed


abs_op = AbsOp()
invert_op = InvertOp()
isnull_op = IsNullOp()
len_op = LenOp()
notnull_op = NotNullOp()
reverse_op = ReverseOp()
lower_op = LowerOp()
upper_op = UpperOp()
strip_op = StripOp()
isnumeric_op = IsNumericOp()
rstrip_op = RstripOp()
lstrip_op = LstripOp()
hash_op = HashOp()
day_op = DayOp()
dayofweek_op = DayofweekOp()
date_op = DateOp()
hour_op = HourOp()
minute_op = MinuteOp()
month_op = MonthOp()
quarter_op = QuarterOp()
second_op = SecondOp()
time_op = TimeOp()
year_op = YearOp()
capitalize_op = CapitalizeOp()


### Binary Ops
def short_circuit_nulls(type_override: typing.Optional[ibis_dtypes.DataType] = None):
    """Wraps a binary operator to generate nulls of the expected type if either input is a null scalar."""

    def short_circuit_nulls_inner(binop):
        @functools.wraps(binop)
        def wrapped_binop(x: ibis_types.Value, y: ibis_types.Value):
            if isinstance(x, ibis_types.NullScalar):
                return ibis_types.null().cast(type_override or y.type())
            elif isinstance(y, ibis_types.NullScalar):
                return ibis_types.null().cast(type_override or x.type())
            else:
                return binop(x, y)

        return wrapped_binop

    return short_circuit_nulls_inner


def concat_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    x_string = typing.cast(ibis_types.StringValue, x)
    y_string = typing.cast(ibis_types.StringValue, y)
    return x_string.concat(y_string)


def eq_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return x == y


def ne_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return x != y


def and_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return typing.cast(ibis_types.BooleanValue, x) & typing.cast(
        ibis_types.BooleanValue, y
    )


def or_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return typing.cast(ibis_types.BooleanValue, x) | typing.cast(
        ibis_types.BooleanValue, y
    )


@short_circuit_nulls()
def add_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    if isinstance(x, ibis_types.NullScalar) or isinstance(x, ibis_types.NullScalar):
        return
    return typing.cast(ibis_types.NumericValue, x) + typing.cast(
        ibis_types.NumericValue, y
    )


@short_circuit_nulls()
def sub_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return typing.cast(ibis_types.NumericValue, x) - typing.cast(
        ibis_types.NumericValue, y
    )


@short_circuit_nulls()
def mul_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return typing.cast(ibis_types.NumericValue, x) * typing.cast(
        ibis_types.NumericValue, y
    )


@short_circuit_nulls(ibis_dtypes.float)
def div_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return typing.cast(ibis_types.NumericValue, x) / typing.cast(
        ibis_types.NumericValue, y
    )


@short_circuit_nulls(ibis_dtypes.bool)
def lt_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return x < y


@short_circuit_nulls(ibis_dtypes.bool)
def le_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return x <= y


@short_circuit_nulls(ibis_dtypes.bool)
def gt_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return x > y


@short_circuit_nulls(ibis_dtypes.bool)
def ge_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return x >= y


@short_circuit_nulls(ibis_dtypes.int)
def floordiv_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    x_numeric = typing.cast(ibis_types.NumericValue, x)
    y_numeric = typing.cast(ibis_types.NumericValue, y)
    floordiv_expr = x_numeric // y_numeric

    # DIV(N, 0) will error in bigquery, but needs to return 0 for int, and inf for float in BQ so we short-circuit in this case.
    # Multiplying left by zero propogates nulls.
    zero_result = _INF if (x.type().is_floating() or y.type().is_floating()) else _ZERO
    return (
        ibis.case()
        .when(y_numeric == _ZERO, zero_result * x_numeric)
        .else_(floordiv_expr)
        .end()
    )


def _is_float(x: ibis_types.Value):
    return isinstance(x, (ibis_types.FloatingColumn, ibis_types.FloatingScalar))


@short_circuit_nulls()
def mod_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    is_result_float = _is_float(x) | _is_float(y)
    x_numeric = typing.cast(
        ibis_types.NumericValue,
        x.cast(ibis_dtypes.Decimal(precision=38, scale=9, nullable=True))
        if is_result_float
        else x,
    )
    y_numeric = typing.cast(
        ibis_types.NumericValue,
        y.cast(ibis_dtypes.Decimal(precision=38, scale=9, nullable=True))
        if is_result_float
        else y,
    )
    # Hacky short-circuit to avoid passing zero-literal to sql backend, evaluate locally instead to null.
    op = y.op()
    if isinstance(op, ibis.expr.operations.generic.Literal) and op.value == 0:
        return ibis_types.null().cast(x.type())

    bq_mod = x_numeric % y_numeric  # Bigquery will maintain x sign here
    if is_result_float:
        bq_mod = typing.cast(ibis_types.NumericValue, bq_mod.cast(ibis_dtypes.float64))

    # In BigQuery returned value has the same sign as X. In pandas, the sign of y is used, so we need to flip the result if sign(x) != sign(y)
    return (
        ibis.case()
        .when(
            y_numeric == _ZERO,
            _NAN * x_numeric if is_result_float else _ZERO * x_numeric,
        )  # Dummy op to propogate nulls and type from x arg
        .when(
            (y_numeric < _ZERO) & (bq_mod > _ZERO), (y_numeric + bq_mod)
        )  # Convert positive result to negative
        .when(
            (y_numeric > _ZERO) & (bq_mod < _ZERO), (y_numeric + bq_mod)
        )  # Convert negative result to positive
        .else_(bq_mod)
        .end()
    )


def fillna_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return x.fillna(typing.cast(ibis_types.Scalar, y))


def clip_lower(
    value: ibis_types.Value,
    lower: ibis_types.Value,
):
    return ibis.case().when(lower.isnull() | (value < lower), lower).else_(value).end()


def clip_upper(
    value: ibis_types.Value,
    upper: ibis_types.Value,
):
    return ibis.case().when(upper.isnull() | (value > upper), upper).else_(value).end()


def reverse(op: BinaryOp) -> BinaryOp:
    return lambda x, y: op(y, x)


def partial_left(op: BinaryOp, scalar: typing.Any) -> UnaryOp:
    return BinopPartialLeft(op, scalar)


def partial_right(op: BinaryOp, scalar: typing.Any) -> UnaryOp:
    return BinopPartialRight(op, scalar)


# Ternary ops
def where_op(
    original: ibis_types.Value,
    condition: ibis_types.Value,
    replacement: ibis_types.Value,
) -> ibis_types.Value:
    """Returns x if y is true, otherwise returns z."""
    return ibis.case().when(condition, original).else_(replacement).end()


def clip_op(
    original: ibis_types.Value,
    lower: ibis_types.Value,
    upper: ibis_types.Value,
) -> ibis_types.Value:
    """Clips value to lower and upper bounds."""
    if isinstance(lower, ibis_types.NullScalar) and (
        not isinstance(upper, ibis_types.NullScalar)
    ):
        return (
            ibis.case()
            .when(upper.isnull() | (original > upper), upper)
            .else_(original)
            .end()
        )
    elif (not isinstance(lower, ibis_types.NullScalar)) and isinstance(
        upper, ibis_types.NullScalar
    ):
        return (
            ibis.case()
            .when(lower.isnull() | (original < lower), lower)
            .else_(original)
            .end()
        )
    elif isinstance(lower, ibis_types.NullScalar) and (
        isinstance(upper, ibis_types.NullScalar)
    ):
        return original
    else:
        # Note: Pandas has unchanged behavior when upper bound and lower bound are flipped. This implementation requires that lower_bound < upper_bound
        return (
            ibis.case()
            .when(lower.isnull() | (original < lower), lower)
            .when(upper.isnull() | (original > upper), upper)
            .else_(original)
            .end()
        )


def is_null(value) -> bool:
    # float NaN/inf should be treated as distinct from 'true' null values
    return typing.cast(bool, pd.isna(value)) and not isinstance(value, float)
