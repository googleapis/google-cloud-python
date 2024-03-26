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
import bigframes.core.expression as ex
import bigframes.dtypes
import bigframes.operations as ops

_ZERO = typing.cast(ibis_types.NumericValue, ibis_types.literal(0))
_NAN = typing.cast(ibis_types.NumericValue, ibis_types.literal(np.nan))
_INF = typing.cast(ibis_types.NumericValue, ibis_types.literal(np.inf))
_NEG_INF = typing.cast(ibis_types.NumericValue, ibis_types.literal(-np.inf))

# Approx Highest number you can pass in to EXP function and get a valid FLOAT64 result
# FLOAT64 has 11 exponent bits, so max values is about 2**(2**10)
# ln(2**(2**10)) == (2**10)*ln(2) ~= 709.78, so EXP(x) for x>709.78 will overflow.
_FLOAT64_EXP_BOUND = typing.cast(ibis_types.NumericValue, ibis_types.literal(709.78))

# Datetime constants
UNIT_TO_US_CONVERSION_FACTORS = {
    "W": 7 * 24 * 60 * 60 * 1000 * 1000,
    "d": 24 * 60 * 60 * 1000 * 1000,
    "D": 24 * 60 * 60 * 1000 * 1000,
    "h": 60 * 60 * 1000 * 1000,
    "m": 60 * 1000 * 1000,
    "s": 1000 * 1000,
    "ms": 1000,
    "us": 1,
    "ns": 1e-3,
}


class ScalarOpCompiler:
    # Mapping of operation name to implemenations
    _registry: dict[
        str,
        typing.Callable[
            [typing.Sequence[ibis_types.Value], ops.RowOp], ibis_types.Value
        ],
    ] = {}

    @functools.singledispatchmethod
    def compile_expression(
        self,
        expression: ex.Expression,
        bindings: typing.Dict[str, ibis_types.Value],
    ) -> ibis_types.Value:
        raise NotImplementedError(f"Unrecognized expression: {expression}")

    @compile_expression.register
    def _(
        self,
        expression: ex.ScalarConstantExpression,
        bindings: typing.Dict[str, ibis_types.Value],
    ) -> ibis_types.Value:
        return bigframes.dtypes.literal_to_ibis_scalar(
            expression.value, expression.dtype
        )

    @compile_expression.register
    def _(
        self,
        expression: ex.UnboundVariableExpression,
        bindings: typing.Dict[str, ibis_types.Value],
    ) -> ibis_types.Value:
        if expression.id not in bindings:
            raise ValueError(f"Could not resolve unbound variable {expression.id}")
        else:
            return bindings[expression.id]

    @compile_expression.register
    def _(
        self,
        expression: ex.OpExpression,
        bindings: typing.Dict[str, ibis_types.Value],
    ) -> ibis_types.Value:
        inputs = [
            self.compile_expression(sub_expr, bindings)
            for sub_expr in expression.inputs
        ]
        return self.compile_row_op(expression.op, inputs)

    def compile_row_op(
        self, op: ops.RowOp, inputs: typing.Sequence[ibis_types.Value]
    ) -> ibis_types.Value:
        impl = self._registry[op.name]
        return impl(inputs, op)

    def register_unary_op(
        self,
        op_ref: typing.Union[ops.UnaryOp, type[ops.UnaryOp]],
        pass_op: bool = False,
    ):
        """
        Decorator to register a unary op implementation.

        Args:
            op_ref (UnaryOp or UnaryOp type):
                Class or instance of operator that is implemented by the decorated function.
            pass_op (bool):
                Set to true if implementation takes the operator object as the last argument.
                This is needed for parameterized ops where parameters are part of op object.
        """
        key = typing.cast(str, op_ref.name)

        def decorator(impl: typing.Callable[..., ibis_types.Value]):
            def normalized_impl(args: typing.Sequence[ibis_types.Value], op: ops.RowOp):
                if pass_op:
                    return impl(args[0], op)
                else:
                    return impl(args[0])

            self._register(key, normalized_impl)
            return impl

        return decorator

    def register_binary_op(
        self,
        op_ref: typing.Union[ops.BinaryOp, type[ops.BinaryOp]],
        pass_op: bool = False,
    ):
        """
        Decorator to register a binary op implementation.

        Args:
            op_ref (BinaryOp or BinaryOp type):
                Class or instance of operator that is implemented by the decorated function.
            pass_op (bool):
                Set to true if implementation takes the operator object as the last argument.
                This is needed for parameterized ops where parameters are part of op object.
        """
        key = typing.cast(str, op_ref.name)

        def decorator(impl: typing.Callable[..., ibis_types.Value]):
            def normalized_impl(args: typing.Sequence[ibis_types.Value], op: ops.RowOp):
                if pass_op:
                    return impl(args[0], args[1], op)
                else:
                    return impl(args[0], args[1])

            self._register(key, normalized_impl)
            return impl

        return decorator

    def register_ternary_op(
        self, op_ref: typing.Union[ops.TernaryOp, type[ops.TernaryOp]]
    ):
        """
        Decorator to register a ternary op implementation.

        Args:
            op_ref (TernaryOp or TernaryOp type):
                Class or instance of operator that is implemented by the decorated function.
        """
        key = typing.cast(str, op_ref.name)

        def decorator(impl: typing.Callable[..., ibis_types.Value]):
            def normalized_impl(args: typing.Sequence[ibis_types.Value], op: ops.RowOp):
                return impl(args[0], args[1], args[2])

            self._register(key, normalized_impl)
            return impl

        return decorator

    def _register(
        self,
        op_name: str,
        impl: typing.Callable[
            [typing.Sequence[ibis_types.Value], ops.RowOp], ibis_types.Value
        ],
    ):
        if op_name in self._registry:
            raise ValueError(f"Operation name {op_name} already registered")
        self._registry[op_name] = impl


# Singleton compiler
scalar_op_compiler = ScalarOpCompiler()


### Unary Ops
@scalar_op_compiler.register_unary_op(ops.isnull_op)
def isnull_op_impl(x: ibis_types.Value):
    return x.isnull()


@scalar_op_compiler.register_unary_op(ops.notnull_op)
def notnull_op_impl(x: ibis_types.Value):
    return x.notnull()


@scalar_op_compiler.register_unary_op(ops.hash_op)
def hash_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.IntegerValue, x).hash()


# Trig Functions
@scalar_op_compiler.register_unary_op(ops.sin_op)
def sin_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.NumericValue, x).sin()


@scalar_op_compiler.register_unary_op(ops.cos_op)
def cos_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.NumericValue, x).cos()


@scalar_op_compiler.register_unary_op(ops.tan_op)
def tan_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.NumericValue, x).tan()


# Inverse trig functions
@scalar_op_compiler.register_unary_op(ops.arcsin_op)
def arcsin_op_impl(x: ibis_types.Value):
    numeric_value = typing.cast(ibis_types.NumericValue, x)
    domain = numeric_value.abs() <= _ibis_num(1)
    return (~domain).ifelse(_NAN, numeric_value.asin())


@scalar_op_compiler.register_unary_op(ops.arccos_op)
def arccos_op_impl(x: ibis_types.Value):
    numeric_value = typing.cast(ibis_types.NumericValue, x)
    domain = numeric_value.abs() <= _ibis_num(1)
    return (~domain).ifelse(_NAN, numeric_value.acos())


@scalar_op_compiler.register_unary_op(ops.arctan_op)
def arctan_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.NumericValue, x).atan()


@scalar_op_compiler.register_binary_op(ops.arctan2_op)
def arctan2_op_impl(x: ibis_types.Value, y: ibis_types.Value):
    return typing.cast(ibis_types.NumericValue, x).atan2(
        typing.cast(ibis_types.NumericValue, y)
    )


# Hyperbolic trig functions
# BQ has these functions, but Ibis doesn't
@scalar_op_compiler.register_unary_op(ops.sinh_op)
def sinh_op_impl(x: ibis_types.Value):
    numeric_value = typing.cast(ibis_types.NumericValue, x)
    sinh_result = (numeric_value.exp() - (numeric_value.negate()).exp()) / _ibis_num(2)
    domain = numeric_value.abs() < _FLOAT64_EXP_BOUND
    return (~domain).ifelse(_INF * numeric_value.sign(), sinh_result)


@scalar_op_compiler.register_unary_op(ops.cosh_op)
def cosh_op_impl(x: ibis_types.Value):
    numeric_value = typing.cast(ibis_types.NumericValue, x)
    cosh_result = (numeric_value.exp() + (numeric_value.negate()).exp()) / _ibis_num(2)
    domain = numeric_value.abs() < _FLOAT64_EXP_BOUND
    return (~domain).ifelse(_INF, cosh_result)


@scalar_op_compiler.register_unary_op(ops.tanh_op)
def tanh_op_impl(x: ibis_types.Value):
    numeric_value = typing.cast(ibis_types.NumericValue, x)
    tanh_result = (numeric_value.exp() - (numeric_value.negate()).exp()) / (
        numeric_value.exp() + (numeric_value.negate()).exp()
    )
    # Beyond +-20, is effectively just the sign function
    domain = numeric_value.abs() < _ibis_num(20)
    return (~domain).ifelse(numeric_value.sign(), tanh_result)


@scalar_op_compiler.register_unary_op(ops.arcsinh_op)
def arcsinh_op_impl(x: ibis_types.Value):
    numeric_value = typing.cast(ibis_types.NumericValue, x)
    sqrt_part = ((numeric_value * numeric_value) + _ibis_num(1)).sqrt()
    return (numeric_value.abs() + sqrt_part).ln() * numeric_value.sign()


@scalar_op_compiler.register_unary_op(ops.arccosh_op)
def arccosh_op_impl(x: ibis_types.Value):
    numeric_value = typing.cast(ibis_types.NumericValue, x)
    sqrt_part = ((numeric_value * numeric_value) - _ibis_num(1)).sqrt()
    acosh_result = (numeric_value + sqrt_part).ln()
    domain = numeric_value >= _ibis_num(1)
    return (~domain).ifelse(_NAN, acosh_result)


@scalar_op_compiler.register_unary_op(ops.arctanh_op)
def arctanh_op_impl(x: ibis_types.Value):
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


# Numeric Ops
@scalar_op_compiler.register_unary_op(ops.floor_op)
def floor_op_impl(x: ibis_types.Value):
    x_numeric = typing.cast(ibis_types.NumericValue, x)
    if x_numeric.type().is_integer():
        return x_numeric.cast(ibis_dtypes.Float64())
    if x_numeric.type().is_floating():
        # Default ibis impl tries to cast to integer, which doesn't match pandas and can overflow
        return float_floor(x_numeric)
    else:  # numeric
        return x_numeric.floor()


@scalar_op_compiler.register_unary_op(ops.ceil_op)
def ceil_op_impl(x: ibis_types.Value):
    x_numeric = typing.cast(ibis_types.NumericValue, x)
    if x_numeric.type().is_integer():
        return x_numeric.cast(ibis_dtypes.Float64())
    if x_numeric.type().is_floating():
        # Default ibis impl tries to cast to integer, which doesn't match pandas and can overflow
        return float_ceil(x_numeric)
    else:  # numeric
        return x_numeric.ceil()


@scalar_op_compiler.register_unary_op(ops.abs_op)
def abs_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.NumericValue, x).abs()


@scalar_op_compiler.register_unary_op(ops.sqrt_op)
def sqrt_op_impl(x: ibis_types.Value):
    numeric_value = typing.cast(ibis_types.NumericValue, x)
    domain = numeric_value >= _ZERO
    return (~domain).ifelse(_NAN, numeric_value.sqrt())


@scalar_op_compiler.register_unary_op(ops.log10_op)
def log10_op_impl(x: ibis_types.Value):
    numeric_value = typing.cast(ibis_types.NumericValue, x)
    domain = numeric_value > _ZERO
    out_of_domain = (numeric_value == _ZERO).ifelse(_NEG_INF, _NAN)
    return (~domain).ifelse(out_of_domain, numeric_value.log10())


@scalar_op_compiler.register_unary_op(ops.ln_op)
def ln_op_impl(x: ibis_types.Value):
    numeric_value = typing.cast(ibis_types.NumericValue, x)
    domain = numeric_value > _ZERO
    out_of_domain = (numeric_value == _ZERO).ifelse(_NEG_INF, _NAN)
    return (~domain).ifelse(out_of_domain, numeric_value.ln())


@scalar_op_compiler.register_unary_op(ops.log1p_op)
def log1p_op_impl(x: ibis_types.Value):
    return ln_op_impl(_ibis_num(1) + x)


@scalar_op_compiler.register_unary_op(ops.exp_op)
def exp_op_impl(x: ibis_types.Value):
    numeric_value = typing.cast(ibis_types.NumericValue, x)
    domain = numeric_value < _FLOAT64_EXP_BOUND
    return (~domain).ifelse(_INF, numeric_value.exp())


@scalar_op_compiler.register_unary_op(ops.expm1_op)
def expm1_op_impl(x: ibis_types.Value):
    return exp_op_impl(x) - _ibis_num(1)


@scalar_op_compiler.register_unary_op(ops.invert_op)
def invert_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.NumericValue, x).negate()


## String Operation
@scalar_op_compiler.register_unary_op(ops.len_op)
def len_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.StringValue, x).length().cast(ibis_dtypes.int64)


@scalar_op_compiler.register_unary_op(ops.reverse_op)
def reverse_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.StringValue, x).reverse()


@scalar_op_compiler.register_unary_op(ops.lower_op)
def lower_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.StringValue, x).lower()


@scalar_op_compiler.register_unary_op(ops.upper_op)
def upper_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.StringValue, x).upper()


@scalar_op_compiler.register_unary_op(ops.strip_op)
def strip_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.StringValue, x).strip()


@scalar_op_compiler.register_unary_op(ops.isnumeric_op)
def isnumeric_op_impl(x: ibis_types.Value):
    # catches all members of the Unicode number class, which matches pandas isnumeric
    # see https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#regexp_contains
    # TODO: Validate correctness, my miss eg ⅕ character
    return typing.cast(ibis_types.StringValue, x).re_search(r"^(\pN+)$")


@scalar_op_compiler.register_unary_op(ops.isalpha_op)
def isalpha_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.StringValue, x).re_search(
        r"^(\p{Lm}|\p{Lt}|\p{Lu}|\p{Ll}|\p{Lo})+$"
    )


@scalar_op_compiler.register_unary_op(ops.isdigit_op)
def isdigit_op_impl(x: ibis_types.Value):
    # Based on docs, should include superscript/subscript-ed numbers
    # Tests however pass only when set to Nd unicode class
    return typing.cast(ibis_types.StringValue, x).re_search(r"^(\p{Nd})+$")


@scalar_op_compiler.register_unary_op(ops.isdecimal_op)
def isdecimal_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.StringValue, x).re_search(r"^(\p{Nd})+$")


@scalar_op_compiler.register_unary_op(ops.isalnum_op)
def isalnum_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.StringValue, x).re_search(
        r"^(\p{N}|\p{Lm}|\p{Lt}|\p{Lu}|\p{Ll}|\p{Lo})+$"
    )


@scalar_op_compiler.register_unary_op(ops.isspace_op)
def isspace_op_impl(x: ibis_types.Value):
    # All characters are whitespace characters, False for empty string
    return typing.cast(ibis_types.StringValue, x).re_search(r"^\s+$")


@scalar_op_compiler.register_unary_op(ops.islower_op)
def islower_op_impl(x: ibis_types.Value):
    # No upper case characters, min one cased character
    # See: https://docs.python.org/3/library/stdtypes.html#str
    return typing.cast(ibis_types.StringValue, x).re_search(r"\p{Ll}") & ~typing.cast(
        ibis_types.StringValue, x
    ).re_search(r"\p{Lu}|\p{Lt}")


@scalar_op_compiler.register_unary_op(ops.isupper_op)
def isupper_op_impl(x: ibis_types.Value):
    # No lower case characters, min one cased character
    # See: https://docs.python.org/3/library/stdtypes.html#str
    return typing.cast(ibis_types.StringValue, x).re_search(r"\p{Lu}") & ~typing.cast(
        ibis_types.StringValue, x
    ).re_search(r"\p{Ll}|\p{Lt}")


@scalar_op_compiler.register_unary_op(ops.rstrip_op)
def rstrip_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.StringValue, x).rstrip()


@scalar_op_compiler.register_unary_op(ops.lstrip_op)
def lstrip_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.StringValue, x).lstrip()


@scalar_op_compiler.register_unary_op(ops.capitalize_op)
def capitalize_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.StringValue, x).capitalize()


@scalar_op_compiler.register_unary_op(ops.StrContainsOp, pass_op=True)
def strcontains_op(x: ibis_types.Value, op: ops.StrContainsOp):
    return typing.cast(ibis_types.StringValue, x).contains(op.pat)


@scalar_op_compiler.register_unary_op(ops.StrContainsRegexOp, pass_op=True)
def contains_regex_op_impl(x: ibis_types.Value, op: ops.StrContainsRegexOp):
    return typing.cast(ibis_types.StringValue, x).re_search(op.pat)


@scalar_op_compiler.register_unary_op(ops.StrGetOp, pass_op=True)
def strget_op_impl(x: ibis_types.Value, op: ops.StrGetOp):
    substr = typing.cast(
        ibis_types.StringValue, typing.cast(ibis_types.StringValue, x)[op.i]
    )
    return substr.nullif(ibis_types.literal(""))


@scalar_op_compiler.register_unary_op(ops.StrPadOp, pass_op=True)
def strpad_op_impl(x: ibis_types.Value, op: ops.StrPadOp):
    str_val = typing.cast(ibis_types.StringValue, x)

    # SQL pad operations will truncate, we do not want to truncate though.
    pad_length = ibis.greatest(str_val.length(), op.length)
    if op.side == "left":
        return str_val.lpad(pad_length, op.fillchar)
    elif op.side == "right":
        return str_val.rpad(pad_length, op.fillchar)
    else:  # side == both
        # Pad more on right side if can't pad both sides equally
        lpad_amount = ((pad_length - str_val.length()) // 2) + str_val.length()
        return str_val.lpad(lpad_amount, op.fillchar).rpad(pad_length, op.fillchar)


@scalar_op_compiler.register_unary_op(ops.ReplaceStrOp, pass_op=True)
def replacestring_op_impl(x: ibis_types.Value, op: ops.ReplaceStrOp):
    pat_str_value = typing.cast(ibis_types.StringValue, ibis_types.literal(op.pat))
    repl_str_value = typing.cast(ibis_types.StringValue, ibis_types.literal(op.repl))
    return typing.cast(ibis_types.StringValue, x).replace(pat_str_value, repl_str_value)


@scalar_op_compiler.register_unary_op(ops.RegexReplaceStrOp, pass_op=True)
def replaceregex_op_impl(x: ibis_types.Value, op: ops.RegexReplaceStrOp):
    return typing.cast(ibis_types.StringValue, x).re_replace(op.pat, op.repl)


@scalar_op_compiler.register_unary_op(ops.StartsWithOp, pass_op=True)
def startswith_op_impl(x: ibis_types.Value, op: ops.StartsWithOp):
    any_match = None
    for pat in op.pat:
        pat_match = typing.cast(ibis_types.StringValue, x).startswith(pat)
        if any_match is not None:
            any_match = any_match | pat_match
        else:
            any_match = pat_match
    return any_match if any_match is not None else ibis_types.literal(False)


@scalar_op_compiler.register_unary_op(ops.EndsWithOp, pass_op=True)
def endswith_op_impl(x: ibis_types.Value, op: ops.EndsWithOp):
    any_match = None
    for pat in op.pat:
        pat_match = typing.cast(ibis_types.StringValue, x).endswith(pat)
        if any_match is not None:
            any_match = any_match | pat_match
        else:
            any_match = pat_match
    return any_match if any_match is not None else ibis_types.literal(False)


@scalar_op_compiler.register_unary_op(ops.ZfillOp, pass_op=True)
def zfill_op_impl(x: ibis_types.Value, op: ops.ZfillOp):
    str_value = typing.cast(ibis_types.StringValue, x)
    return (
        ibis.case()
        .when(
            str_value[0] == "-",
            "-"
            + strpad_op_impl(
                str_value.substr(1),
                ops.StrPadOp(length=op.width - 1, fillchar="0", side="left"),
            ),
        )
        .else_(
            strpad_op_impl(
                str_value, ops.StrPadOp(length=op.width, fillchar="0", side="left")
            )
        )
        .end()
    )


@scalar_op_compiler.register_unary_op(ops.StrFindOp, pass_op=True)
def find_op_impl(x: ibis_types.Value, op: ops.StrFindOp):
    return typing.cast(ibis_types.StringValue, x).find(op.substr, op.start, op.end)


@scalar_op_compiler.register_unary_op(ops.StrExtractOp, pass_op=True)
def extract_op_impl(x: ibis_types.Value, op: ops.StrExtractOp):
    return typing.cast(ibis_types.StringValue, x).re_extract(op.pat, op.n)


@scalar_op_compiler.register_unary_op(ops.StrSliceOp, pass_op=True)
def slice_op_impl(x: ibis_types.Value, op: ops.StrSliceOp):
    return typing.cast(ibis_types.StringValue, x)[op.start : op.end]


@scalar_op_compiler.register_unary_op(ops.StrRepeatOp, pass_op=True)
def repeat_op_impl(x: ibis_types.Value, op: ops.StrRepeatOp):
    return typing.cast(ibis_types.StringValue, x).repeat(op.repeats)


## Datetime Ops
@scalar_op_compiler.register_unary_op(ops.day_op)
def day_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.TimestampValue, x).day().cast(ibis_dtypes.int64)


@scalar_op_compiler.register_unary_op(ops.date_op)
def date_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.TimestampValue, x).date()


@scalar_op_compiler.register_unary_op(ops.dayofweek_op)
def dayofweek_op_impl(x: ibis_types.Value):
    return (
        typing.cast(ibis_types.TimestampValue, x)
        .day_of_week.index()
        .cast(ibis_dtypes.int64)
    )


@scalar_op_compiler.register_unary_op(ops.hour_op)
def hour_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.TimestampValue, x).hour().cast(ibis_dtypes.int64)


@scalar_op_compiler.register_unary_op(ops.minute_op)
def minute_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.TimestampValue, x).minute().cast(ibis_dtypes.int64)


@scalar_op_compiler.register_unary_op(ops.month_op)
def month_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.TimestampValue, x).month().cast(ibis_dtypes.int64)


@scalar_op_compiler.register_unary_op(ops.quarter_op)
def quarter_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.TimestampValue, x).quarter().cast(ibis_dtypes.int64)


@scalar_op_compiler.register_unary_op(ops.second_op)
def second_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.TimestampValue, x).second().cast(ibis_dtypes.int64)


@scalar_op_compiler.register_unary_op(ops.StrftimeOp, pass_op=True)
def strftime_op_impl(x: ibis_types.Value, op: ops.StrftimeOp):
    return (
        typing.cast(ibis_types.TimestampValue, x)
        .strftime(op.date_format)
        .cast(ibis_dtypes.str)
    )


@scalar_op_compiler.register_unary_op(ops.FloorDtOp, pass_op=True)
def floor_dt_op_impl(x: ibis_types.Value, op: ops.FloorDtOp):
    supported_freqs = ["Y", "Q", "M", "W", "D", "h", "min", "s", "ms", "us", "ns"]
    pandas_to_ibis_freqs = {"min": "m"}
    if op.freq not in supported_freqs:
        raise NotImplementedError(
            f"Unsupported freq paramater: {op.freq}"
            + " Supported freq parameters are: "
            + ",".join(supported_freqs)
        )
    if op.freq in pandas_to_ibis_freqs:
        ibis_freq = pandas_to_ibis_freqs[op.freq]
    else:
        ibis_freq = op.freq
    result_type = x.type()
    result = typing.cast(ibis_types.TimestampValue, x)
    result = result.truncate(ibis_freq)
    return result.cast(result_type)


@scalar_op_compiler.register_unary_op(ops.time_op)
def time_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.TimestampValue, x).time()


@scalar_op_compiler.register_unary_op(ops.year_op)
def year_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.TimestampValue, x).year().cast(ibis_dtypes.int64)


@scalar_op_compiler.register_unary_op(ops.normalize_op)
def normalize_op_impl(x: ibis_types.Value):
    result_type = x.type()
    result = x.truncate("D")
    return result.cast(result_type)


# Parameterized ops
@scalar_op_compiler.register_unary_op(ops.StructFieldOp, pass_op=True)
def struct_field_op_impl(x: ibis_types.Value, op: ops.StructFieldOp):
    struct_value = typing.cast(ibis_types.StructValue, x)
    if isinstance(op.name_or_index, str):
        name = op.name_or_index
    else:
        name = struct_value.names[op.name_or_index]
    return struct_value[name].name(name)


def numeric_to_datatime(x: ibis_types.Value, unit: str) -> ibis_types.TimestampValue:
    if not isinstance(x, ibis_types.IntegerValue) and not isinstance(
        x, ibis_types.FloatingValue
    ):
        raise TypeError("Non-numerical types are not supposed to reach this function.")

    if unit not in UNIT_TO_US_CONVERSION_FACTORS:
        raise ValueError(f"Cannot convert input with unit '{unit}'.")
    x_converted = x * UNIT_TO_US_CONVERSION_FACTORS[unit]
    x_converted = x_converted.cast(ibis_dtypes.int64)

    # Note: Due to an issue where casting directly to a timestamp
    # without a timezone does not work, we first cast to UTC. This
    # approach appears to bypass a potential bug in Ibis's cast function,
    # allowing for subsequent casting to a timestamp type without timezone
    # information. Further investigation is needed to confirm this behavior.
    return x_converted.to_timestamp(unit="us").cast(
        ibis_dtypes.Timestamp(timezone="UTC")
    )


@scalar_op_compiler.register_unary_op(ops.AsTypeOp, pass_op=True)
def astype_op_impl(x: ibis_types.Value, op: ops.AsTypeOp):
    to_type = bigframes.dtypes.bigframes_dtype_to_ibis_dtype(op.to_type)
    if isinstance(x, ibis_types.NullScalar):
        return ibis_types.null().cast(to_type)

    # When casting DATETIME column into INT column, we need to convert the column into TIMESTAMP first.
    if to_type == ibis_dtypes.int64 and x.type() == ibis_dtypes.timestamp:
        x_converted = x.cast(ibis_dtypes.Timestamp(timezone="UTC"))
        return bigframes.dtypes.cast_ibis_value(x_converted, to_type)

    if to_type == ibis_dtypes.int64 and x.type() == ibis_dtypes.time:
        # The conversion unit is set to "us" (microseconds) for consistency
        # with pandas converting time64[us][pyarrow] to int64[pyarrow].
        return x.delta(ibis.time("00:00:00"), part="microsecond")

    if x.type() == ibis_dtypes.int64:
        # The conversion unit is set to "us" (microseconds) for consistency
        # with pandas converting int64[pyarrow] to timestamp[us][pyarrow],
        # timestamp[us, tz=UTC][pyarrow], and time64[us][pyarrow].
        unit = "us"
        x_converted = numeric_to_datatime(x, unit)
        if to_type == ibis_dtypes.timestamp:
            return x_converted.cast(ibis_dtypes.Timestamp())
        elif to_type == ibis_dtypes.Timestamp(timezone="UTC"):
            return x_converted
        elif to_type == ibis_dtypes.time:
            return x_converted.time()

    return bigframes.dtypes.cast_ibis_value(x, to_type)


@scalar_op_compiler.register_unary_op(ops.IsInOp, pass_op=True)
def isin_op_impl(x: ibis_types.Value, op: ops.IsInOp):
    contains_nulls = any(is_null(value) for value in op.values)
    matchable_ibis_values = []
    for item in op.values:
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

    if op.match_nulls and contains_nulls:
        return x.isnull() | x.isin(matchable_ibis_values)
    else:
        return x.isin(matchable_ibis_values)


@scalar_op_compiler.register_unary_op(ops.ToDatetimeOp, pass_op=True)
def to_datetime_op_impl(x: ibis_types.Value, op: ops.ToDatetimeOp):
    if x.type() == ibis_dtypes.str:
        x = x.to_timestamp(op.format) if op.format else timestamp(x)
    elif x.type() == ibis_dtypes.Timestamp(timezone="UTC"):
        if op.format:
            raise NotImplementedError(
                f"Format parameter is not supported for Timestamp input types. {constants.FEEDBACK_LINK}"
            )
        return x
    elif x.type() != ibis_dtypes.timestamp:
        if op.format:
            x = x.cast(ibis_dtypes.str).to_timestamp(op.format)
        else:
            # The default unit is set to "ns" (nanoseconds) for consistency
            # with pandas, where "ns" is the default unit for datetime operations.
            unit = op.unit or "ns"
            x = numeric_to_datatime(x, unit)

    return x.cast(ibis_dtypes.Timestamp(timezone="UTC" if op.utc else None))


@scalar_op_compiler.register_unary_op(ops.RemoteFunctionOp, pass_op=True)
def remote_function_op_impl(x: ibis_types.Value, op: ops.RemoteFunctionOp):
    if not hasattr(op.func, "bigframes_remote_function"):
        raise TypeError(
            f"only a bigframes remote function is supported as a callable. {constants.FEEDBACK_LINK}"
        )
    x_transformed = op.func(x)
    if not op.apply_on_null:
        x_transformed = ibis.case().when(x.isnull(), x).else_(x_transformed).end()
    return x_transformed


@scalar_op_compiler.register_unary_op(ops.MapOp, pass_op=True)
def map_op_impl(x: ibis_types.Value, op: ops.MapOp):
    case = ibis.case()
    for mapping in op.mappings:
        case = case.when(x == mapping[0], mapping[1])
    return case.else_(x).end()


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


@scalar_op_compiler.register_binary_op(ops.strconcat_op)
def concat_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    x_string = typing.cast(ibis_types.StringValue, x)
    y_string = typing.cast(ibis_types.StringValue, y)
    return x_string.concat(y_string)


@scalar_op_compiler.register_binary_op(ops.eq_op)
def eq_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return x == y


@scalar_op_compiler.register_binary_op(ops.eq_null_match_op)
def eq_nulls_match_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    """Variant of eq_op where nulls match each other. Only use where dtypes are known to be same."""
    left = x.cast(ibis_dtypes.str).fillna(ibis_types.literal("$NULL_SENTINEL$"))
    right = y.cast(ibis_dtypes.str).fillna(ibis_types.literal("$NULL_SENTINEL$"))
    return left == right


@scalar_op_compiler.register_binary_op(ops.ne_op)
def ne_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return x != y


def _null_or_value(value: ibis_types.Value, where_value: ibis_types.BooleanValue):
    return ibis.where(
        where_value,
        value,
        ibis.null(),
    )


@scalar_op_compiler.register_binary_op(ops.and_op)
def and_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    # Workaround issue https://github.com/ibis-project/ibis/issues/7775 by
    # implementing three-valued logic ourselves. For AND, when we encounter a
    # NULL value, we only know when the result is FALSE, otherwise the result
    # is unknown (NULL). See: truth table at
    # https://en.wikibooks.org/wiki/Structured_Query_Language/NULLs_and_the_Three_Valued_Logic#AND,_OR
    if isinstance(x, ibis_types.NullScalar):
        return _null_or_value(y, y == ibis.literal(False))

    if isinstance(y, ibis_types.NullScalar):
        return _null_or_value(x, x == ibis.literal(False))
    return typing.cast(ibis_types.BooleanValue, x) & typing.cast(
        ibis_types.BooleanValue, y
    )


@scalar_op_compiler.register_binary_op(ops.or_op)
def or_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    # Workaround issue https://github.com/ibis-project/ibis/issues/7775 by
    # implementing three-valued logic ourselves. For OR, when we encounter a
    # NULL value, we only know when the result is TRUE, otherwise the result
    # is unknown (NULL). See: truth table at
    # https://en.wikibooks.org/wiki/Structured_Query_Language/NULLs_and_the_Three_Valued_Logic#AND,_OR
    if isinstance(x, ibis_types.NullScalar):
        return _null_or_value(y, y == ibis.literal(True))

    if isinstance(y, ibis_types.NullScalar):
        return _null_or_value(x, x == ibis.literal(True))
    return typing.cast(ibis_types.BooleanValue, x) | typing.cast(
        ibis_types.BooleanValue, y
    )


@scalar_op_compiler.register_binary_op(ops.add_op)
@short_circuit_nulls()
def add_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    if isinstance(x, ibis_types.NullScalar) or isinstance(x, ibis_types.NullScalar):
        return ibis.null()
    try:
        # Could be string concatenation or numeric addition.
        return x + y  # type: ignore
    except ibis.common.annotations.SignatureValidationError as exc:
        left_type = bigframes.dtypes.ibis_dtype_to_bigframes_dtype(x.type())
        right_type = bigframes.dtypes.ibis_dtype_to_bigframes_dtype(y.type())
        raise TypeError(
            f"Cannot add {repr(left_type)} and {repr(right_type)}. {constants.FEEDBACK_LINK}"
        ) from exc


@scalar_op_compiler.register_binary_op(ops.sub_op)
@short_circuit_nulls()
def sub_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return typing.cast(ibis_types.NumericValue, x) - typing.cast(
        ibis_types.NumericValue, y
    )


@scalar_op_compiler.register_binary_op(ops.mul_op)
@short_circuit_nulls()
def mul_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return typing.cast(ibis_types.NumericValue, x) * typing.cast(
        ibis_types.NumericValue, y
    )


@scalar_op_compiler.register_binary_op(ops.div_op)
@short_circuit_nulls(ibis_dtypes.float)
def div_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return typing.cast(ibis_types.NumericValue, x) / typing.cast(
        ibis_types.NumericValue, y
    )


@scalar_op_compiler.register_binary_op(ops.pow_op)
@short_circuit_nulls(ibis_dtypes.float)
def pow_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    if x.type().is_integer() and y.type().is_integer():
        return _int_pow_op(x, y)
    else:
        return _float_pow_op(x, y)


@scalar_op_compiler.register_binary_op(ops.unsafe_pow_op)
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


@scalar_op_compiler.register_binary_op(ops.lt_op)
@short_circuit_nulls(ibis_dtypes.bool)
def lt_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return x < y


@scalar_op_compiler.register_binary_op(ops.le_op)
@short_circuit_nulls(ibis_dtypes.bool)
def le_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return x <= y


@scalar_op_compiler.register_binary_op(ops.gt_op)
@short_circuit_nulls(ibis_dtypes.bool)
def gt_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return x > y


@scalar_op_compiler.register_binary_op(ops.ge_op)
@short_circuit_nulls(ibis_dtypes.bool)
def ge_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return x >= y


@scalar_op_compiler.register_binary_op(ops.floordiv_op)
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


def _is_bignumeric(x: ibis_types.Value):
    if not isinstance(x, ibis_types.DecimalValue):
        return False
    # Should be exactly 76 for bignumeric
    return x.precision > 70


def _is_numeric(x: ibis_types.Value):
    # either big-numeric or numeric
    return isinstance(x, ibis_types.DecimalValue)


@scalar_op_compiler.register_binary_op(ops.mod_op)
@short_circuit_nulls()
def mod_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    # Hacky short-circuit to avoid passing zero-literal to sql backend, evaluate locally instead to null.
    op = y.op()
    if isinstance(op, ibis.expr.operations.generic.Literal) and op.value == 0:
        return ibis_types.null().cast(x.type())

    if x.type().is_integer() and y.type().is_integer():
        # both are ints, no casting necessary
        return _int_mod(x, y)

    else:
        # bigquery doens't support float mod, so just cast to bignumeric and hope for the best
        x_numeric = typing.cast(
            ibis_types.DecimalValue,
            x.cast(ibis_dtypes.Decimal(precision=76, scale=38, nullable=True)),
        )
        y_numeric = typing.cast(
            ibis_types.DecimalValue,
            y.cast(ibis_dtypes.Decimal(precision=76, scale=38, nullable=True)),
        )
        mod_numeric = _bignumeric_mod(x_numeric, y_numeric)

        # Cast back down based on original types
        if _is_bignumeric(x) or _is_bignumeric(y):
            return mod_numeric
        if _is_numeric(x) or _is_numeric(y):
            return mod_numeric.cast(ibis_dtypes.Decimal(38, 9))
        else:
            return mod_numeric.cast(ibis_dtypes.float64)


def _bignumeric_mod(
    x: ibis_types.IntegerValue,
    y: ibis_types.IntegerValue,
):
    # Hacky short-circuit to avoid passing zero-literal to sql backend, evaluate locally instead to null.
    op = y.op()
    if isinstance(op, ibis.expr.operations.generic.Literal) and op.value == 0:
        return ibis_types.null().cast(x.type())

    bq_mod = x % y  # Bigquery will maintain x sign here

    # In BigQuery returned value has the same sign as X. In pandas, the sign of y is used, so we need to flip the result if sign(x) != sign(y)
    return (
        ibis.case()
        .when(
            y == _ZERO,
            _NAN * x,
        )  # Dummy op to propogate nulls and type from x arg
        .when(
            (y < _ZERO) & (bq_mod > _ZERO), (y + bq_mod)
        )  # Convert positive result to negative
        .when(
            (y > _ZERO) & (bq_mod < _ZERO), (y + bq_mod)
        )  # Convert negative result to positive
        .else_(bq_mod)
        .end()
    )


def _int_mod(
    x: ibis_types.IntegerValue,
    y: ibis_types.IntegerValue,
):
    # Hacky short-circuit to avoid passing zero-literal to sql backend, evaluate locally instead to null.
    op = y.op()
    if isinstance(op, ibis.expr.operations.generic.Literal) and op.value == 0:
        return ibis_types.null().cast(x.type())

    bq_mod = x % y  # Bigquery will maintain x sign here

    # In BigQuery returned value has the same sign as X. In pandas, the sign of y is used, so we need to flip the result if sign(x) != sign(y)
    return (
        ibis.case()
        .when(
            y == _ZERO,
            _ZERO * x,
        )  # Dummy op to propogate nulls and type from x arg
        .when(
            (y < _ZERO) & (bq_mod > _ZERO), (y + bq_mod)
        )  # Convert positive result to negative
        .when(
            (y > _ZERO) & (bq_mod < _ZERO), (y + bq_mod)
        )  # Convert negative result to positive
        .else_(bq_mod)
        .end()
    )


@scalar_op_compiler.register_binary_op(ops.fillna_op)
def fillna_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return x.fillna(typing.cast(ibis_types.Scalar, y))


@scalar_op_compiler.register_binary_op(ops.round_op)
def round_op(x: ibis_types.Value, y: ibis_types.Value):
    return typing.cast(ibis_types.NumericValue, x).round(
        digits=typing.cast(ibis_types.IntegerValue, y)
    )


@scalar_op_compiler.register_binary_op(ops.coalesce_op)
def coalesce_impl(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    if x.name("name").equals(y.name("name")):
        return x
    else:
        return ibis.coalesce(x, y)


@scalar_op_compiler.register_binary_op(ops.cliplower_op)
def clip_lower(
    value: ibis_types.Value,
    lower: ibis_types.Value,
):
    return ibis.case().when(lower.isnull() | (value < lower), lower).else_(value).end()


@scalar_op_compiler.register_binary_op(ops.clipupper_op)
def clip_upper(
    value: ibis_types.Value,
    upper: ibis_types.Value,
):
    return ibis.case().when(upper.isnull() | (value > upper), upper).else_(value).end()


# Ternary Operations
@scalar_op_compiler.register_ternary_op(ops.where_op)
def where_op(
    original: ibis_types.Value,
    condition: ibis_types.Value,
    replacement: ibis_types.Value,
) -> ibis_types.Value:
    """Returns x if y is true, otherwise returns z."""
    return ibis.case().when(condition, original).else_(replacement).end()


@scalar_op_compiler.register_ternary_op(ops.clip_op)
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


# Helpers
def is_null(value) -> bool:
    # float NaN/inf should be treated as distinct from 'true' null values
    return typing.cast(bool, pd.isna(value)) and not isinstance(value, float)


def _ibis_num(number: float):
    return typing.cast(ibis_types.NumericValue, ibis_types.literal(number))


@ibis.udf.scalar.builtin
def timestamp(a: str) -> ibis_dtypes.timestamp:
    """Convert string to timestamp."""


# Need these because ibis otherwise tries to do casts to int that can fail
@ibis.udf.scalar.builtin(name="floor")
def float_floor(a: float) -> float:
    """Convert string to timestamp."""
    return 0  # pragma: NO COVER


@ibis.udf.scalar.builtin(name="ceil")
def float_ceil(a: float) -> float:
    """Convert string to timestamp."""
    return 0  # pragma: NO COVER
