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
_NEG_INF = typing.cast(ibis_types.NumericValue, ibis_types.literal(-np.inf))

# Approx Highest number you can pass in to EXP function and get a valid FLOAT64 result
# FLOAT64 has 11 exponent bits, so max values is about 2**(2**10)
# ln(2**(2**10)) == (2**10)*ln(2) ~= 709.78, so EXP(x) for x>709.78 will overflow.
_FLOAT64_EXP_BOUND = typing.cast(ibis_types.NumericValue, ibis_types.literal(709.78))
_INT64_EXP_BOUND = typing.cast(ibis_types.NumericValue, ibis_types.literal(43.6))

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


# Trig Functions
class AbsOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.NumericValue, x).abs()


class SinOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.NumericValue, x).sin()


class CosOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.NumericValue, x).cos()


class TanOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.NumericValue, x).tan()


# Inverse trig functions
class ArcsinOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        numeric_value = typing.cast(ibis_types.NumericValue, x)
        domain = numeric_value.abs() <= _ibis_num(1)
        return (~domain).ifelse(_NAN, numeric_value.asin())


class ArccosOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        numeric_value = typing.cast(ibis_types.NumericValue, x)
        domain = numeric_value.abs() <= _ibis_num(1)
        return (~domain).ifelse(_NAN, numeric_value.acos())


class ArctanOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.NumericValue, x).atan()


# Hyperbolic trig functions
# BQ has these functions, but Ibis doesn't
class SinhOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        numeric_value = typing.cast(ibis_types.NumericValue, x)
        sinh_result = (
            numeric_value.exp() - (numeric_value.negate()).exp()
        ) / _ibis_num(2)
        domain = numeric_value.abs() < _FLOAT64_EXP_BOUND
        return (~domain).ifelse(_INF * numeric_value.sign(), sinh_result)


class CoshOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        numeric_value = typing.cast(ibis_types.NumericValue, x)
        cosh_result = (
            numeric_value.exp() + (numeric_value.negate()).exp()
        ) / _ibis_num(2)
        domain = numeric_value.abs() < _FLOAT64_EXP_BOUND
        return (~domain).ifelse(_INF, cosh_result)


class TanhOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        numeric_value = typing.cast(ibis_types.NumericValue, x)
        tanh_result = (numeric_value.exp() - (numeric_value.negate()).exp()) / (
            numeric_value.exp() + (numeric_value.negate()).exp()
        )
        # Beyond +-20, is effectively just the sign function
        domain = numeric_value.abs() < _ibis_num(20)
        return (~domain).ifelse(numeric_value.sign(), tanh_result)


class ArcsinhOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        numeric_value = typing.cast(ibis_types.NumericValue, x)
        sqrt_part = ((numeric_value * numeric_value) + _ibis_num(1)).sqrt()
        return (numeric_value.abs() + sqrt_part).ln() * numeric_value.sign()


class ArccoshOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        numeric_value = typing.cast(ibis_types.NumericValue, x)
        sqrt_part = ((numeric_value * numeric_value) - _ibis_num(1)).sqrt()
        acosh_result = (numeric_value + sqrt_part).ln()
        domain = numeric_value >= _ibis_num(1)
        return (~domain).ifelse(_NAN, acosh_result)


class ArctanhOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        numeric_value = typing.cast(ibis_types.NumericValue, x)
        domain = numeric_value.abs() < _ibis_num(1)
        numerator = numeric_value + _ibis_num(1)
        denominator = _ibis_num(1) - numeric_value
        ln_input = typing.cast(ibis_types.NumericValue, numerator.div(denominator))
        atanh_result = ln_input.ln().div(2)

        out_of_domain = (numeric_value.abs() == _ibis_num(1)).ifelse(
            _INF * numeric_value, _NAN
        )

        return (~domain).ifelse(out_of_domain, atanh_result)


class SqrtOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        numeric_value = typing.cast(ibis_types.NumericValue, x)
        domain = numeric_value >= _ZERO
        return (~domain).ifelse(_NAN, numeric_value.sqrt())


class Log10Op(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        numeric_value = typing.cast(ibis_types.NumericValue, x)
        domain = numeric_value > _ZERO
        out_of_domain = (numeric_value == _ZERO).ifelse(_NEG_INF, _NAN)
        return (~domain).ifelse(out_of_domain, numeric_value.log10())


class LnOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        numeric_value = typing.cast(ibis_types.NumericValue, x)
        domain = numeric_value > _ZERO
        out_of_domain = (numeric_value == _ZERO).ifelse(_NEG_INF, _NAN)
        return (~domain).ifelse(out_of_domain, numeric_value.ln())


class ExpOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        numeric_value = typing.cast(ibis_types.NumericValue, x)
        domain = numeric_value < _FLOAT64_EXP_BOUND
        return (~domain).ifelse(_INF, numeric_value.exp())


class InvertOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.NumericValue, x).negate()


class IsNullOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return x.isnull()


class LenOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.StringValue, x).length().cast(ibis_dtypes.int64)


class NotNullOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return x.notnull()


class HashOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.IntegerValue, x).hash()


## String Operation
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
        # TODO: Validate correctness, my miss eg ⅕ character
        return typing.cast(ibis_types.StringValue, x).re_search(r"^(\pN+)$")


class IsAlphaOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.StringValue, x).re_search(
            r"^(\p{Lm}|\p{Lt}|\p{Lu}|\p{Ll}|\p{Lo})+$"
        )


class IsDigitOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        # Based on docs, should include superscript/subscript-ed numbers
        # Tests however pass only when set to Nd unicode class
        return typing.cast(ibis_types.StringValue, x).re_search(r"^(\p{Nd})+$")


class IsDecimalOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.StringValue, x).re_search(r"^(\p{Nd})+$")


class IsAlnumOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.StringValue, x).re_search(
            r"^(\p{N}|\p{Lm}|\p{Lt}|\p{Lu}|\p{Ll}|\p{Lo})+$"
        )


class IsSpaceOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        # All characters are whitespace characters, False for empty string
        return typing.cast(ibis_types.StringValue, x).re_search(r"^\s+$")


class IsLowerOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        # No upper case characters, min one cased character
        # See: https://docs.python.org/3/library/stdtypes.html#str
        return typing.cast(ibis_types.StringValue, x).re_search(
            r"\p{Ll}"
        ) & ~typing.cast(ibis_types.StringValue, x).re_search(r"\p{Lu}|\p{Lt}")


class IsUpperOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        # No lower case characters, min one cased character
        # See: https://docs.python.org/3/library/stdtypes.html#str
        return typing.cast(ibis_types.StringValue, x).re_search(
            r"\p{Lu}"
        ) & ~typing.cast(ibis_types.StringValue, x).re_search(r"\p{Ll}|\p{Lt}")


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


class StrGetOp(UnaryOp):
    def __init__(self, i: int):
        self._i = i

    def _as_ibis(self, x: ibis_types.Value):
        substr = typing.cast(
            ibis_types.StringValue, typing.cast(ibis_types.StringValue, x)[self._i]
        )
        return substr.nullif(ibis_types.literal(""))


class StrPadOp(UnaryOp):
    def __init__(
        self, length: int, fillchar: str, side: typing.Literal["both", "left", "right"]
    ):
        self._length = length
        self._fillchar = fillchar
        self._side = side

    def _as_ibis(self, x: ibis_types.Value):
        str_val = typing.cast(ibis_types.StringValue, x)

        # SQL pad operations will truncate, we do not want to truncate though.
        pad_length = ibis.greatest(str_val.length(), self._length)
        if self._side == "left":
            return str_val.lpad(pad_length, self._fillchar)
        elif self._side == "right":
            return str_val.rpad(pad_length, self._fillchar)
        else:  # side == both
            # Pad more on right side if can't pad both sides equally
            lpad_amount = ((pad_length - str_val.length()) // 2) + str_val.length()
            return str_val.lpad(lpad_amount, self._fillchar).rpad(
                pad_length, self._fillchar
            )


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


class ZfillOp(UnaryOp):
    def __init__(self, width: int):
        self._width = width

    def _as_ibis(self, x: ibis_types.Value):
        str_value = typing.cast(ibis_types.StringValue, x)
        return (
            ibis.case()
            .when(
                str_value[0] == "-",
                "-"
                + StrPadOp(self._width - 1, "0", "left")._as_ibis(str_value.substr(1)),
            )
            .else_(StrPadOp(self._width, "0", "left")._as_ibis(str_value))
            .end()
        )


## Datetime Ops
class DayOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.TimestampValue, x).day().cast(ibis_dtypes.int64)


class DateOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.TimestampValue, x).date()


class DayofweekOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return (
            typing.cast(ibis_types.TimestampValue, x)
            .day_of_week.index()
            .cast(ibis_dtypes.int64)
        )


class HourOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.TimestampValue, x).hour().cast(ibis_dtypes.int64)


class MinuteOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return (
            typing.cast(ibis_types.TimestampValue, x).minute().cast(ibis_dtypes.int64)
        )


class MonthOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.TimestampValue, x).month().cast(ibis_dtypes.int64)


class QuarterOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return (
            typing.cast(ibis_types.TimestampValue, x).quarter().cast(ibis_dtypes.int64)
        )


class SecondOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return (
            typing.cast(ibis_types.TimestampValue, x).second().cast(ibis_dtypes.int64)
        )


class TimeOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.TimestampValue, x).time()


class YearOp(UnaryOp):
    def _as_ibis(self, x: ibis_types.Value):
        return typing.cast(ibis_types.TimestampValue, x).year().cast(ibis_dtypes.int64)


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
        contains_nulls = any(is_null(value) for value in self._values)
        matchable_ibis_values = []
        for item in self._values:
            if not is_null(item):
                try:
                    # we want values that *could* be cast to the dtype, but we don't want
                    # to actually cast it, as that could be lossy (eg float -> int)
                    item_inferred_type = ibis.literal(item).type()
                    if (
                        x.type() == item_inferred_type
                        or x.type().is_numeric()
                        and item_inferred_type.is_numeric()
                    ):
                        matchable_ibis_values.append(item)
                except TypeError:
                    pass

        if self._match_nulls and contains_nulls:
            return x.isnull() | x.isin(matchable_ibis_values)
        else:
            return x.isin(matchable_ibis_values)


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
isalnum_op = IsAlnumOp()
isalpha_op = IsAlphaOp()
isdecimal_op = IsDecimalOp()
isdigit_op = IsDigitOp()
isnumeric_op = IsNumericOp()
isspace_op = IsSpaceOp()
islower_op = IsLowerOp()
isupper_op = IsUpperOp()
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

# Just parameterless unary ops for now
# TODO: Parameter mappings
NUMPY_TO_OP: typing.Final = {
    np.sin: SinOp(),
    np.cos: CosOp(),
    np.tan: TanOp(),
    np.arcsin: ArcsinOp(),
    np.arccos: ArccosOp(),
    np.arctan: ArctanOp(),
    np.sinh: SinhOp(),
    np.cosh: CoshOp(),
    np.tanh: TanhOp(),
    np.arcsinh: ArcsinhOp(),
    np.arccosh: ArccoshOp(),
    np.arctanh: ArctanhOp(),
    np.exp: ExpOp(),
    np.log: LnOp(),
    np.log10: Log10Op(),
    np.sqrt: SqrtOp(),
    np.abs: AbsOp(),
}


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


def eq_nulls_match_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    """Variant of eq_op where nulls match each other. Only use where dtypes are known to be same."""
    left = x.cast(ibis_dtypes.str).fillna(ibis_types.literal("$NULL_SENTINEL$"))
    right = y.cast(ibis_dtypes.str).fillna(ibis_types.literal("$NULL_SENTINEL$"))
    return left == right


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


@short_circuit_nulls(ibis_dtypes.float)
def pow_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    if x.type().is_integer() and y.type().is_integer():
        return _int_pow_op(x, y)
    else:
        return _float_pow_op(x, y)


@short_circuit_nulls(ibis_dtypes.float)
def unsafe_pow_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    """For internal use only - where domain and overflow checks are not needed."""
    return typing.cast(ibis_types.NumericValue, x) ** typing.cast(
        ibis_types.NumericValue, y
    )


def _int_pow_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    # Need to avoid any error cases - should produce NaN instead
    # See: https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#pow
    x_as_decimal = typing.cast(
        ibis_types.NumericValue,
        x.cast(ibis_dtypes.Decimal(precision=38, scale=9, nullable=True)),
    )
    y_val = typing.cast(ibis_types.NumericValue, y)

    # BQ POW() function outputs FLOAT64, which can lose precision.
    # Therefore, we do math in NUMERIC and cast back down after.
    # Also, explicit bounds checks, pandas will silently overflow.
    pow_result = x_as_decimal**y_val
    overflow_cond = (pow_result > _ibis_num((2**63) - 1)) | (
        pow_result < _ibis_num(-(2**63))
    )

    return (
        ibis.case()
        .when((overflow_cond), ibis.null())
        .else_(pow_result.cast(ibis_dtypes.int64))
        .end()
    )


def _float_pow_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    # Most conditions here seek to prevent calling BQ POW with inputs that would generate errors.
    # See: https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#pow
    x_val = typing.cast(ibis_types.NumericValue, x)
    y_val = typing.cast(ibis_types.NumericValue, y)

    overflow_cond = (x_val != _ZERO) & ((y_val * x_val.abs().ln()) > _FLOAT64_EXP_BOUND)

    # Float64 lose integer precision beyond 2**53, beyond this insufficient precision to get parity
    exp_too_big = y_val.abs() > _ibis_num(2**53)
    # Treat very large exponents as +=INF
    norm_exp = exp_too_big.ifelse(_INF * y_val.sign(), y_val)

    pow_result = x_val**norm_exp

    # This cast is dangerous, need to only excuted where y_val has been bounds-checked
    # Ibis needs try_cast binding to bq safe_cast
    exponent_is_whole = y_val.cast(ibis_dtypes.int64) == y_val
    odd_exponent = (x_val < _ZERO) & (
        y_val.cast(ibis_dtypes.int64) % _ibis_num(2) == _ibis_num(1)
    )
    infinite_base = x_val.abs() == _INF

    return (
        ibis.case()
        # Might be able to do something more clever with x_val==0 case
        .when(y_val == _ZERO, _ibis_num(1))
        .when(
            x_val == _ibis_num(1), _ibis_num(1)
        )  # Need to ignore exponent, even if it is NA
        .when(
            (x_val == _ZERO) & (y_val < _ZERO), _INF
        )  # This case would error POW function in BQ
        .when(infinite_base, pow_result)
        .when(
            exp_too_big, pow_result
        )  # Bigquery can actually handle the +-inf cases gracefully
        .when((x_val < _ZERO) & (~exponent_is_whole), _NAN)
        .when(
            overflow_cond, _INF * odd_exponent.ifelse(_ibis_num(-1), _ibis_num(1))
        )  # finite overflows would cause bq to error
        .else_(pow_result)
        .end()
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


def coalesce_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    if x.name("name").equals(y.name("name")):
        return x
    else:
        return ibis.coalesce(x, y)


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


def round_op(x: ibis_types.Value, y: ibis_types.Value):
    return typing.cast(ibis_types.NumericValue, x).round(
        digits=typing.cast(ibis_types.IntegerValue, y)
    )


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


NUMPY_TO_BINOP: typing.Final = {
    np.add: add_op,
    np.subtract: sub_op,
    np.multiply: mul_op,
    np.divide: div_op,
    np.power: pow_op,
}


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


def partial_arg1(op: TernaryOp, scalar: typing.Any) -> BinaryOp:
    return lambda x, y: op(dtypes.literal_to_ibis_scalar(scalar, validate=False), x, y)


def partial_arg2(op: TernaryOp, scalar: typing.Any) -> BinaryOp:
    return lambda x, y: op(x, dtypes.literal_to_ibis_scalar(scalar, validate=False), y)


def partial_arg3(op: TernaryOp, scalar: typing.Any) -> BinaryOp:
    return lambda x, y: op(x, y, dtypes.literal_to_ibis_scalar(scalar, validate=False))


def is_null(value) -> bool:
    # float NaN/inf should be treated as distinct from 'true' null values
    return typing.cast(bool, pd.isna(value)) and not isinstance(value, float)


def _ibis_num(number: float):
    return typing.cast(ibis_types.NumericValue, ibis_types.literal(number))
