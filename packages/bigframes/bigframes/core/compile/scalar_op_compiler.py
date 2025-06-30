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

import bigframes_vendored.ibis.expr.api as ibis_api
import bigframes_vendored.ibis.expr.datatypes as ibis_dtypes
import bigframes_vendored.ibis.expr.operations.generic as ibis_generic
import bigframes_vendored.ibis.expr.operations.udf as ibis_udf
import bigframes_vendored.ibis.expr.types as ibis_types
import numpy as np
import pandas as pd

from bigframes.core.compile.constants import UNIT_TO_US_CONVERSION_FACTORS
import bigframes.core.compile.default_ordering
import bigframes.core.compile.ibis_types
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

_OBJ_REF_STRUCT_SCHEMA = (
    ("uri", ibis_dtypes.String),
    ("version", ibis_dtypes.String),
    ("authorizer", ibis_dtypes.String),
    ("details", ibis_dtypes.JSON),
)
_OBJ_REF_IBIS_DTYPE = ibis_dtypes.Struct.from_tuples(_OBJ_REF_STRUCT_SCHEMA)  # type: ignore


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
        return bigframes.core.compile.ibis_types.literal_to_ibis_scalar(
            expression.value, expression.dtype
        )

    @compile_expression.register
    def _(
        self,
        expression: ex.DerefOp,
        bindings: typing.Dict[str, ibis_types.Value],
    ) -> ibis_types.Value:
        if expression.id.sql not in bindings:
            raise ValueError(f"Could not resolve unbound variable {expression.id}")
        else:
            return bindings[expression.id.sql]

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

    def register_nary_op(
        self, op_ref: typing.Union[ops.NaryOp, type[ops.NaryOp]], pass_op: bool = False
    ):
        """
        Decorator to register a nary op implementation.

        Args:
            op_ref (NaryOp or NaryOp type):
                Class or instance of operator that is implemented by the decorated function.
            pass_op (bool):
                Set to true if implementation takes the operator object as the last argument.
                This is needed for parameterized ops where parameters are part of op object.
        """
        key = typing.cast(str, op_ref.name)

        def decorator(impl: typing.Callable[..., ibis_types.Value]):
            def normalized_impl(args: typing.Sequence[ibis_types.Value], op: ops.RowOp):
                if pass_op:
                    return impl(*args, op=op)
                else:
                    return impl(*args)

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


@scalar_op_compiler.register_unary_op(ops.pos_op)
def pos_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.NumericValue, x)


@scalar_op_compiler.register_unary_op(ops.neg_op)
def neg_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.NumericValue, x).negate()


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
    return x.__invert__()  # type: ignore


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


@scalar_op_compiler.register_unary_op(ops.StrLstripOp, pass_op=True)
def str_lstrip_op_impl(x: ibis_types.Value, op: ops.StrStripOp):
    return str_lstrip_op(x, to_strip=op.to_strip)


@scalar_op_compiler.register_unary_op(ops.StrRstripOp, pass_op=True)
def str_rstrip_op_impl(x: ibis_types.Value, op: ops.StrRstripOp):
    return str_rstrip_op(x, to_strip=op.to_strip)


@scalar_op_compiler.register_unary_op(ops.StrStripOp, pass_op=True)
def str_strip_op_impl(x: ibis_types.Value, op: ops.StrStripOp):
    return str_strip_op(x, to_strip=op.to_strip)


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
    pad_length = typing.cast(
        ibis_types.IntegerValue, ibis_api.greatest(str_val.length(), op.length)
    )
    if op.side == "left":
        return str_val.lpad(pad_length, op.fillchar)
    elif op.side == "right":
        return str_val.rpad(pad_length, op.fillchar)
    else:  # side == both
        # Pad more on right side if can't pad both sides equally
        two = typing.cast(ibis_types.IntegerValue, 2)
        lpad_amount = ((pad_length - str_val.length()) // two) + str_val.length()
        return str_val.lpad(
            length=typing.cast(ibis_types.IntegerValue, lpad_amount), pad=op.fillchar
        ).rpad(pad_length, op.fillchar)


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


@scalar_op_compiler.register_unary_op(ops.StringSplitOp, pass_op=True)
def stringsplit_op_impl(x: ibis_types.Value, op: ops.StringSplitOp):
    return typing.cast(ibis_types.StringValue, x).split(delimiter=op.pat)  # type: ignore


@scalar_op_compiler.register_unary_op(ops.ZfillOp, pass_op=True)
def zfill_op_impl(x: ibis_types.Value, op: ops.ZfillOp):
    str_value = typing.cast(ibis_types.StringValue, x)
    return (
        ibis_api.case()
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


@scalar_op_compiler.register_unary_op(ops.iso_day_op)
def iso_day_op_impl(x: ibis_types.Value):
    # Plus 1 because iso day of week uses 1-based indexing
    return dayofweek_op_impl(x) + 1


@scalar_op_compiler.register_unary_op(ops.iso_week_op)
def iso_week_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.TimestampValue, x).week_of_year()


@scalar_op_compiler.register_unary_op(ops.iso_year_op)
def iso_year_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.TimestampValue, x).iso_year()


@scalar_op_compiler.register_unary_op(ops.dayofweek_op)
def dayofweek_op_impl(x: ibis_types.Value):
    return (
        typing.cast(ibis_types.TimestampValue, x)
        .day_of_week.index()
        .cast(ibis_dtypes.int64)
    )


@scalar_op_compiler.register_unary_op(ops.dayofyear_op)
def dayofyear_op_impl(x: ibis_types.Value):
    return (
        typing.cast(ibis_types.TimestampValue, x).day_of_year().cast(ibis_dtypes.int64)
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


@scalar_op_compiler.register_unary_op(ops.UnixSeconds)
def unix_seconds_op_impl(x: ibis_types.TimestampValue):
    return x.epoch_seconds()


@scalar_op_compiler.register_unary_op(ops.UnixMicros)
def unix_micros_op_impl(x: ibis_types.TimestampValue):
    return unix_micros(x)


@scalar_op_compiler.register_unary_op(ops.UnixMillis)
def unix_millis_op_impl(x: ibis_types.TimestampValue):
    return unix_millis(x)


@scalar_op_compiler.register_binary_op(ops.timestamp_diff_op)
def timestamp_diff_op_impl(x: ibis_types.TimestampValue, y: ibis_types.TimestampValue):
    return x.delta(y, "microsecond")


@scalar_op_compiler.register_binary_op(ops.timestamp_add_op)
def timestamp_add_op_impl(x: ibis_types.TimestampValue, y: ibis_types.IntegerValue):
    return x + y.to_interval("us")


@scalar_op_compiler.register_binary_op(ops.timestamp_sub_op)
def timestamp_sub_op_impl(x: ibis_types.TimestampValue, y: ibis_types.IntegerValue):
    return x - y.to_interval("us")


@scalar_op_compiler.register_binary_op(ops.date_diff_op)
def date_diff_op_impl(x: ibis_types.DateValue, y: ibis_types.DateValue):
    return x.delta(y, "day") * int(UNIT_TO_US_CONVERSION_FACTORS["d"])  # type: ignore


@scalar_op_compiler.register_binary_op(ops.date_add_op)
def date_add_op_impl(x: ibis_types.DateValue, y: ibis_types.IntegerValue):
    return x.cast(ibis_dtypes.timestamp()) + y.to_interval("us")  # type: ignore


@scalar_op_compiler.register_binary_op(ops.date_sub_op)
def date_sub_op_impl(x: ibis_types.DateValue, y: ibis_types.IntegerValue):
    return x.cast(ibis_dtypes.timestamp()) - y.to_interval("us")  # type: ignore


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
    result = result.truncate(ibis_freq)  # type: ignore
    return result.cast(result_type)


@scalar_op_compiler.register_binary_op(ops.DatetimeToIntegerLabelOp, pass_op=True)
def datetime_to_integer_label_op_impl(
    x: ibis_types.Value, y: ibis_types.Value, op: ops.DatetimeToIntegerLabelOp
):
    # Determine if the frequency is fixed by checking if 'op.freq.nanos' is defined.
    try:
        return datetime_to_integer_label_fixed_frequency(x, y, op)
    except ValueError:
        return datetime_to_integer_label_non_fixed_frequency(x, y, op)


def datetime_to_integer_label_fixed_frequency(
    x: ibis_types.Value, y: ibis_types.Value, op: ops.DatetimeToIntegerLabelOp
):
    """
    This function handles fixed frequency conversions where the unit can range
    from microseconds (us) to days.
    """
    us = op.freq.nanos / 1000
    x_int = x.cast(ibis_dtypes.Timestamp(timezone="UTC")).cast(ibis_dtypes.int64)
    first = calculate_resample_first(y, op.origin)
    x_int_label = (x_int - first) // us
    return x_int_label


def datetime_to_integer_label_non_fixed_frequency(
    x: ibis_types.Value, y: ibis_types.Value, op: ops.DatetimeToIntegerLabelOp
):
    """
    This function handles non-fixed frequency conversions for units ranging
    from weeks to years.
    """
    rule_code = op.freq.rule_code
    n = op.freq.n
    if rule_code == "W-SUN":  # Weekly
        us = n * 7 * 24 * 60 * 60 * 1000000
        x = x.truncate("week") + ibis_api.interval(days=6)  # type: ignore
        y = y.truncate("week") + ibis_api.interval(days=6)  # type: ignore
        x_int = x.cast(ibis_dtypes.Timestamp(timezone="UTC")).cast(ibis_dtypes.int64)
        first = y.cast(ibis_dtypes.Timestamp(timezone="UTC")).cast(ibis_dtypes.int64)
        x_int_label = (
            ibis_api.case()
            .when(x_int == first, 0)
            .else_((x_int - first - 1) // us + 1)  # type: ignore
            .end()
        )
    elif rule_code == "ME":  # Monthly
        x_int = x.year() * 12 + x.month() - 1  # type: ignore
        first = y.year() * 12 + y.month() - 1  # type: ignore
        x_int_label = (
            ibis_api.case()
            .when(x_int == first, 0)
            .else_((x_int - first - 1) // n + 1)  # type: ignore
            .end()
        )
    elif rule_code == "QE-DEC":  # Quarterly
        x_int = x.year() * 4 + x.quarter() - 1  # type: ignore
        first = y.year() * 4 + y.quarter() - 1  # type: ignore
        x_int_label = (
            ibis_api.case()
            .when(x_int == first, 0)
            .else_((x_int - first - 1) // n + 1)  # type: ignore
            .end()
        )
    elif rule_code == "YE-DEC":  # Yearly
        x_int = x.year()  # type: ignore
        first = y.year()  # type: ignore
        x_int_label = (
            ibis_api.case()
            .when(x_int == first, 0)
            .else_((x_int - first - 1) // n + 1)  # type: ignore
            .end()
        )
    else:
        raise ValueError(rule_code)
    return x_int_label


@scalar_op_compiler.register_binary_op(ops.IntegerLabelToDatetimeOp, pass_op=True)
def integer_label_to_datetime_op_impl(
    x: ibis_types.Value, y: ibis_types.Value, op: ops.IntegerLabelToDatetimeOp
):
    # Determine if the frequency is fixed by checking if 'op.freq.nanos' is defined.
    try:
        return integer_label_to_datetime_op_fixed_frequency(x, y, op)
    except ValueError:
        return integer_label_to_datetime_op_non_fixed_frequency(x, y, op)


def integer_label_to_datetime_op_fixed_frequency(
    x: ibis_types.Value, y: ibis_types.Value, op: ops.IntegerLabelToDatetimeOp
):
    """
    This function handles fixed frequency conversions where the unit can range
    from microseconds (us) to days.
    """
    us = op.freq.nanos / 1000

    first = calculate_resample_first(y, op.origin)

    x_label = (
        (x * us + first)  # type: ignore
        .cast(ibis_dtypes.int64)
        .to_timestamp(unit="us")
        .cast(ibis_dtypes.Timestamp(timezone="UTC"))
        .cast(y.type())
    )
    return x_label


def integer_label_to_datetime_op_non_fixed_frequency(
    x: ibis_types.Value, y: ibis_types.Value, op: ops.IntegerLabelToDatetimeOp
):
    """
    This function handles non-fixed frequency conversions for units ranging
    from weeks to years.
    """
    rule_code = op.freq.rule_code
    n = op.freq.n
    if rule_code == "W-SUN":  # Weekly
        us = n * 7 * 24 * 60 * 60 * 1000000
        first = (
            y.cast(ibis_dtypes.Timestamp(timezone="UTC")).truncate("week")  # type: ignore
            + ibis_api.interval(days=6)
        ).cast(ibis_dtypes.int64)
        x_label = (
            (x * us + first)  # type: ignore
            .cast(ibis_dtypes.int64)
            .to_timestamp(unit="us")
            .cast(ibis_dtypes.Timestamp(timezone="UTC"))
            .cast(y.type())
        )
    elif rule_code == "ME":  # Monthly
        one = ibis_types.literal(1)
        twelve = ibis_types.literal(12)
        first = y.year() * twelve + y.month() - one  # type: ignore

        x = x * n + first  # type: ignore
        year = x // twelve  # type: ignore
        month = (x % twelve) + one  # type: ignore

        next_year = (month == twelve).ifelse(year + one, year)
        next_month = (month == twelve).ifelse(one, month + one)
        next_month_date = ibis_api.timestamp(
            typing.cast(ibis_types.IntegerValue, next_year),
            typing.cast(ibis_types.IntegerValue, next_month),
            1,
            0,
            0,
            0,
        )
        x_label = next_month_date - ibis_api.interval(days=1)
    elif rule_code == "QE-DEC":  # Quarterly
        one = ibis_types.literal(1)
        three = ibis_types.literal(3)
        four = ibis_types.literal(4)
        twelve = ibis_types.literal(12)
        first = y.year() * four + y.quarter() - one  # type: ignore

        x = x * n + first  # type: ignore
        year = x // four  # type: ignore
        month = ((x % four) + one) * three  # type: ignore

        next_year = (month == twelve).ifelse(year + one, year)
        next_month = (month == twelve).ifelse(one, month + one)
        next_month_date = ibis_api.timestamp(
            typing.cast(ibis_types.IntegerValue, next_year),
            typing.cast(ibis_types.IntegerValue, next_month),
            1,
            0,
            0,
            0,
        )

        x_label = next_month_date - ibis_api.interval(days=1)
    elif rule_code == "YE-DEC":  # Yearly
        one = ibis_types.literal(1)
        first = y.year()  # type: ignore
        x = x * n + first  # type: ignore
        next_year = x + one  # type: ignore
        next_month_date = ibis_api.timestamp(
            typing.cast(ibis_types.IntegerValue, next_year),
            1,
            1,
            0,
            0,
            0,
        )
        x_label = next_month_date - ibis_api.interval(days=1)

    return x_label.cast(ibis_dtypes.Timestamp(timezone="UTC")).cast(y.type())


def calculate_resample_first(y: ibis_types.Value, origin):
    if origin == "epoch":
        return ibis_types.literal(0)
    elif origin == "start_day":
        return (
            y.cast(ibis_dtypes.date)
            .cast(ibis_dtypes.Timestamp(timezone="UTC"))
            .cast(ibis_dtypes.int64)
        )
    elif origin == "start":
        return y.cast(ibis_dtypes.Timestamp(timezone="UTC")).cast(ibis_dtypes.int64)
    else:
        raise ValueError(f"Origin {origin} not supported")


@scalar_op_compiler.register_unary_op(ops.time_op)
def time_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.TimestampValue, x).time()


@scalar_op_compiler.register_unary_op(ops.year_op)
def year_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.TimestampValue, x).year().cast(ibis_dtypes.int64)


@scalar_op_compiler.register_unary_op(ops.normalize_op)
def normalize_op_impl(x: ibis_types.Value):
    result_type = x.type()
    result = x.truncate("D")  # type: ignore
    return result.cast(result_type)


# Geo Ops
@scalar_op_compiler.register_unary_op(ops.geo_area_op)
def geo_area_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.GeoSpatialValue, x).area()


@scalar_op_compiler.register_unary_op(ops.geo_st_astext_op)
def geo_st_astext_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.GeoSpatialValue, x).as_text()


@scalar_op_compiler.register_unary_op(ops.geo_st_boundary_op, pass_op=False)
def geo_st_boundary_op_impl(x: ibis_types.Value):
    return st_boundary(x)


@scalar_op_compiler.register_binary_op(ops.geo_st_difference_op, pass_op=False)
def geo_st_difference_op_impl(x: ibis_types.Value, y: ibis_types.Value):
    return typing.cast(ibis_types.GeoSpatialValue, x).difference(
        typing.cast(ibis_types.GeoSpatialValue, y)
    )


@scalar_op_compiler.register_binary_op(ops.GeoStDistanceOp, pass_op=True)
def geo_st_distance_op_impl(
    x: ibis_types.Value, y: ibis_types.Value, op: ops.GeoStDistanceOp
):
    return st_distance(x, y, op.use_spheroid)


@scalar_op_compiler.register_unary_op(ops.geo_st_geogfromtext_op)
def geo_st_geogfromtext_op_impl(x: ibis_types.Value):
    # Ibis doesn't seem to provide a dedicated method to cast from string to geography,
    # so we use a BigQuery scalar function, st_geogfromtext(), directly.
    return st_geogfromtext(x)


@scalar_op_compiler.register_binary_op(ops.geo_st_geogpoint_op, pass_op=False)
def geo_st_geogpoint_op_impl(x: ibis_types.Value, y: ibis_types.Value):
    return typing.cast(ibis_types.NumericValue, x).point(
        typing.cast(ibis_types.NumericValue, y)
    )


@scalar_op_compiler.register_binary_op(ops.geo_st_intersection_op, pass_op=False)
def geo_st_intersection_op_impl(x: ibis_types.Value, y: ibis_types.Value):
    return typing.cast(ibis_types.GeoSpatialValue, x).intersection(
        typing.cast(ibis_types.GeoSpatialValue, y)
    )


@scalar_op_compiler.register_unary_op(ops.geo_st_isclosed_op, pass_op=False)
def geo_st_isclosed_op_impl(x: ibis_types.Value):
    return st_isclosed(x)


@scalar_op_compiler.register_unary_op(ops.geo_x_op)
def geo_x_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.GeoSpatialValue, x).x()


@scalar_op_compiler.register_unary_op(ops.GeoStLengthOp, pass_op=True)
def geo_length_op_impl(x: ibis_types.Value, op: ops.GeoStLengthOp):
    # Call the st_length UDF defined in this file (or imported)
    return st_length(x, op.use_spheroid)


@scalar_op_compiler.register_unary_op(ops.geo_y_op)
def geo_y_op_impl(x: ibis_types.Value):
    return typing.cast(ibis_types.GeoSpatialValue, x).y()


# Parameterized ops
@scalar_op_compiler.register_unary_op(ops.StructFieldOp, pass_op=True)
def struct_field_op_impl(x: ibis_types.Value, op: ops.StructFieldOp):
    struct_value = typing.cast(ibis_types.StructValue, x)
    if isinstance(op.name_or_index, str):
        name = op.name_or_index
    else:
        name = struct_value.names[op.name_or_index]

    result = struct_value[name]
    return result.cast(result.type()(nullable=True)).name(name)


def numeric_to_datetime(
    x: ibis_types.Value, unit: str, safe: bool = False
) -> ibis_types.TimestampValue:
    if not isinstance(x, ibis_types.IntegerValue) and not isinstance(
        x, ibis_types.FloatingValue
    ):
        raise TypeError("Non-numerical types are not supposed to reach this function.")

    if unit not in UNIT_TO_US_CONVERSION_FACTORS:
        raise ValueError(f"Cannot convert input with unit '{unit}'.")
    x_converted = x * typing.cast(
        ibis_types.IntegerValue, UNIT_TO_US_CONVERSION_FACTORS[unit]
    )
    x_converted = (
        x_converted.try_cast(ibis_dtypes.int64)  # type: ignore
        if safe
        else x_converted.cast(ibis_dtypes.int64)
    )

    # Note: Due to an issue where casting directly to a timestamp
    # without a timezone does not work, we first cast to UTC. This
    # approach appears to bypass a potential bug in Ibis's cast function,
    # allowing for subsequent casting to a timestamp type without timezone
    # information. Further investigation is needed to confirm this behavior.
    return x_converted.to_timestamp(unit="us").cast(  # type: ignore
        ibis_dtypes.Timestamp(timezone="UTC")
    )


@scalar_op_compiler.register_unary_op(ops.AsTypeOp, pass_op=True)
def astype_op_impl(x: ibis_types.Value, op: ops.AsTypeOp):
    to_type = bigframes.core.compile.ibis_types.bigframes_dtype_to_ibis_dtype(
        op.to_type
    )
    if isinstance(x, ibis_types.NullScalar):
        return ibis_types.null().cast(to_type)

    # When casting DATETIME column into INT column, we need to convert the column into TIMESTAMP first.
    if to_type == ibis_dtypes.int64 and x.type() == ibis_dtypes.timestamp:
        utc_time_type = ibis_dtypes.Timestamp(timezone="UTC")
        x_converted = x.try_cast(utc_time_type) if op.safe else x.cast(utc_time_type)
        return bigframes.core.compile.ibis_types.cast_ibis_value(
            x_converted, to_type, safe=op.safe
        )

    if to_type == ibis_dtypes.int64 and x.type() == ibis_dtypes.time:
        # The conversion unit is set to "us" (microseconds) for consistency
        # with pandas converting time64[us][pyarrow] to int64[pyarrow].
        return x.delta(ibis_api.time("00:00:00"), part="microsecond")  # type: ignore

    if x.type() == ibis_dtypes.int64:
        # The conversion unit is set to "us" (microseconds) for consistency
        # with pandas converting int64[pyarrow] to timestamp[us][pyarrow],
        # timestamp[us, tz=UTC][pyarrow], and time64[us][pyarrow].
        unit = "us"
        x_converted = numeric_to_datetime(x, unit, safe=op.safe)
        if to_type == ibis_dtypes.timestamp:
            return (
                x_converted.try_cast(ibis_dtypes.Timestamp())
                if op.safe
                else x_converted.cast(ibis_dtypes.Timestamp())
            )
        elif to_type == ibis_dtypes.Timestamp(timezone="UTC"):
            return x_converted
        elif to_type == ibis_dtypes.time:
            return x_converted.time()

    if to_type == ibis_dtypes.json:
        if x.type() == ibis_dtypes.string:
            return parse_json_in_safe(x) if op.safe else parse_json(x)
        if x.type() == ibis_dtypes.bool:
            x_bool = typing.cast(
                ibis_types.StringValue,
                bigframes.core.compile.ibis_types.cast_ibis_value(
                    x, ibis_dtypes.string, safe=op.safe
                ),
            ).lower()
            return parse_json_in_safe(x_bool) if op.safe else parse_json(x_bool)
        if x.type() in (ibis_dtypes.int64, ibis_dtypes.float64):
            x_str = bigframes.core.compile.ibis_types.cast_ibis_value(
                x, ibis_dtypes.string, safe=op.safe
            )
            return parse_json_in_safe(x_str) if op.safe else parse_json(x_str)

    if x.type() == ibis_dtypes.json:
        if to_type == ibis_dtypes.int64:
            return cast_json_to_int64_in_safe(x) if op.safe else cast_json_to_int64(x)
        if to_type == ibis_dtypes.float64:
            return (
                cast_json_to_float64_in_safe(x) if op.safe else cast_json_to_float64(x)
            )
        if to_type == ibis_dtypes.bool:
            return cast_json_to_bool_in_safe(x) if op.safe else cast_json_to_bool(x)
        if to_type == ibis_dtypes.string:
            return cast_json_to_string_in_safe(x) if op.safe else cast_json_to_string(x)

    # TODO: either inline this function, or push rest of this op into the function
    return bigframes.core.compile.ibis_types.cast_ibis_value(x, to_type, safe=op.safe)


@scalar_op_compiler.register_unary_op(ops.IsInOp, pass_op=True)
def isin_op_impl(x: ibis_types.Value, op: ops.IsInOp):
    contains_nulls = any(is_null(value) for value in op.values)
    matchable_ibis_values = []
    for item in op.values:
        if not is_null(item):
            try:
                # we want values that *could* be cast to the dtype, but we don't want
                # to actually cast it, as that could be lossy (eg float -> int)
                item_inferred_type = ibis_types.literal(item).type()
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
        return x.try_cast(ibis_dtypes.Timestamp(None))  # type: ignore
    else:
        # Numerical inputs.
        if op.format:
            x = x.cast(ibis_dtypes.str).to_timestamp(op.format)  # type: ignore
        else:
            # The default unit is set to "ns" (nanoseconds) for consistency
            # with pandas, where "ns" is the default unit for datetime operations.
            unit = op.unit or "ns"
            x = numeric_to_datetime(x, unit)

    return x.cast(ibis_dtypes.Timestamp(None))  # type: ignore


@scalar_op_compiler.register_unary_op(ops.ToTimestampOp, pass_op=True)
def to_timestamp_op_impl(x: ibis_types.Value, op: ops.ToTimestampOp):
    if x.type() == ibis_dtypes.str:
        x = (
            typing.cast(ibis_types.StringValue, x).to_timestamp(op.format)
            if op.format
            else timestamp(x)
        )
    else:
        # Numerical inputs.
        if op.format:
            x = x.cast(ibis_dtypes.str).to_timestamp(op.format)  # type: ignore
        else:
            # The default unit is set to "ns" (nanoseconds) for consistency
            # with pandas, where "ns" is the default unit for datetime operations.
            unit = op.unit or "ns"
            x = numeric_to_datetime(x, unit)

    return x.cast(ibis_dtypes.Timestamp(timezone="UTC"))


@scalar_op_compiler.register_unary_op(ops.ToTimedeltaOp, pass_op=True)
def to_timedelta_op_impl(x: ibis_types.Value, op: ops.ToTimedeltaOp):
    return (
        typing.cast(ibis_types.NumericValue, x) * UNIT_TO_US_CONVERSION_FACTORS[op.unit]  # type: ignore
    ).floor()


@scalar_op_compiler.register_unary_op(ops.timedelta_floor_op)
def timedelta_floor_op_impl(x: ibis_types.NumericValue):
    return x.floor()


@scalar_op_compiler.register_unary_op(ops.RemoteFunctionOp, pass_op=True)
def remote_function_op_impl(x: ibis_types.Value, op: ops.RemoteFunctionOp):
    udf_sig = op.function_def.signature
    ibis_py_sig = (udf_sig.py_input_types, udf_sig.py_output_type)

    @ibis_udf.scalar.builtin(
        name=str(op.function_def.routine_ref), signature=ibis_py_sig
    )
    def udf(input):
        ...

    x_transformed = udf(x)
    if not op.apply_on_null:
        return ibis_api.case().when(x.isnull(), x).else_(x_transformed).end()
    return x_transformed


@scalar_op_compiler.register_binary_op(ops.BinaryRemoteFunctionOp, pass_op=True)
def binary_remote_function_op_impl(
    x: ibis_types.Value, y: ibis_types.Value, op: ops.BinaryRemoteFunctionOp
):
    udf_sig = op.function_def.signature
    ibis_py_sig = (udf_sig.py_input_types, udf_sig.py_output_type)

    @ibis_udf.scalar.builtin(
        name=str(op.function_def.routine_ref), signature=ibis_py_sig
    )
    def udf(input1, input2):
        ...

    x_transformed = udf(x, y)
    return x_transformed


@scalar_op_compiler.register_nary_op(ops.NaryRemoteFunctionOp, pass_op=True)
def nary_remote_function_op_impl(
    *operands: ibis_types.Value, op: ops.NaryRemoteFunctionOp
):
    udf_sig = op.function_def.signature
    ibis_py_sig = (udf_sig.py_input_types, udf_sig.py_output_type)
    arg_names = tuple(arg.name for arg in udf_sig.input_types)

    @ibis_udf.scalar.builtin(
        name=str(op.function_def.routine_ref),
        signature=ibis_py_sig,
        param_name_overrides=arg_names,
    )
    def udf(*inputs):
        ...

    result = udf(*operands)
    return result


@scalar_op_compiler.register_unary_op(ops.MapOp, pass_op=True)
def map_op_impl(x: ibis_types.Value, op: ops.MapOp):
    case = ibis_api.case()
    for mapping in op.mappings:
        case = case.when(x == mapping[0], mapping[1])
    return case.else_(x).end()


# Array Ops
@scalar_op_compiler.register_unary_op(ops.ArrayToStringOp, pass_op=True)
def array_to_string_op_impl(x: ibis_types.Value, op: ops.ArrayToStringOp):
    return typing.cast(ibis_types.ArrayValue, x).join(op.delimiter)


@scalar_op_compiler.register_unary_op(ops.ArrayIndexOp, pass_op=True)
def array_index_op_impl(x: ibis_types.Value, op: ops.ArrayIndexOp):
    res = typing.cast(ibis_types.ArrayValue, x)[op.index]
    if x.type().is_string():
        return _null_or_value(res, res != ibis_types.literal(""))
    else:
        return res


@scalar_op_compiler.register_unary_op(ops.ArraySliceOp, pass_op=True)
def array_slice_op_impl(x: ibis_types.Value, op: ops.ArraySliceOp):
    res = typing.cast(ibis_types.ArrayValue, x)[op.start : op.stop : op.step]
    if x.type().is_string():
        return _null_or_value(res, res != ibis_types.literal(""))
    else:
        return res


# JSON Ops
@scalar_op_compiler.register_binary_op(ops.JSONSet, pass_op=True)
def json_set_op_impl(x: ibis_types.Value, y: ibis_types.Value, op: ops.JSONSet):
    return json_set(json_obj=x, json_path=op.json_path, json_value=y)


@scalar_op_compiler.register_unary_op(ops.JSONExtract, pass_op=True)
def json_extract_op_impl(x: ibis_types.Value, op: ops.JSONExtract):
    # Define a user-defined function whose returned type is dynamically matching the input.
    def json_extract(json_or_json_string, json_path: ibis_dtypes.str):  # type: ignore
        """Extracts a JSON value and converts it to a SQL JSON-formatted STRING or JSON value."""
        ...

    return_type = x.type()
    json_extract.__annotations__["return"] = return_type
    json_extract_op = ibis_udf.scalar.builtin(json_extract)
    return json_extract_op(json_or_json_string=x, json_path=op.json_path)


@scalar_op_compiler.register_unary_op(ops.JSONExtractArray, pass_op=True)
def json_extract_array_op_impl(x: ibis_types.Value, op: ops.JSONExtractArray):
    # Define a user-defined function whose returned type is dynamically matching the input.
    def json_extract_array(json_or_json_string, json_path: ibis_dtypes.str):  # type: ignore
        """Extracts a JSON value and converts it to a SQL JSON-formatted STRING or JSON value."""
        ...

    return_type = x.type()
    json_extract_array.__annotations__["return"] = ibis_dtypes.Array[return_type]  # type: ignore
    json_extract_op = ibis_udf.scalar.builtin(json_extract_array)
    return json_extract_op(json_or_json_string=x, json_path=op.json_path)


@scalar_op_compiler.register_unary_op(ops.JSONExtractStringArray, pass_op=True)
def json_extract_string_array_op_impl(
    x: ibis_types.Value, op: ops.JSONExtractStringArray
):
    return json_extract_string_array(json_obj=x, json_path=op.json_path)


@scalar_op_compiler.register_unary_op(ops.JSONQuery, pass_op=True)
def json_query_op_impl(x: ibis_types.Value, op: ops.JSONQuery):
    # Define a user-defined function whose returned type is dynamically matching the input.
    def json_query(json_or_json_string, json_path: ibis_dtypes.str):  # type: ignore
        """Extracts a JSON value and converts it to a SQL JSON-formatted STRING or JSON value."""
        ...

    return_type = x.type()
    json_query.__annotations__["return"] = return_type
    json_query_op = ibis_udf.scalar.builtin(json_query)
    return json_query_op(json_or_json_string=x, json_path=op.json_path)


@scalar_op_compiler.register_unary_op(ops.JSONQueryArray, pass_op=True)
def json_query_array_op_impl(x: ibis_types.Value, op: ops.JSONQueryArray):
    # Define a user-defined function whose returned type is dynamically matching the input.
    def json_query_array(json_or_json_string, json_path: ibis_dtypes.str):  # type: ignore
        """Extracts a JSON value and converts it to a SQL JSON-formatted STRING or JSON value."""
        ...

    return_type = x.type()
    json_query_array.__annotations__["return"] = ibis_dtypes.Array[return_type]  # type: ignore
    json_query_op = ibis_udf.scalar.builtin(json_query_array)
    return json_query_op(json_or_json_string=x, json_path=op.json_path)


@scalar_op_compiler.register_unary_op(ops.ParseJSON, pass_op=True)
def parse_json_op_impl(x: ibis_types.Value, op: ops.ParseJSON):
    return parse_json(json_str=x)


@scalar_op_compiler.register_unary_op(ops.ToJSONString)
def to_json_string_op_impl(json_obj: ibis_types.Value):
    return to_json_string(json_obj=json_obj)


@scalar_op_compiler.register_unary_op(ops.JSONValue, pass_op=True)
def json_value_op_impl(x: ibis_types.Value, op: ops.JSONValue):
    return json_value(json_obj=x, json_path=op.json_path)


@scalar_op_compiler.register_unary_op(ops.JSONValueArray, pass_op=True)
def json_value_array_op_impl(x: ibis_types.Value, op: ops.JSONValueArray):
    return json_value_array(json_obj=x, json_path=op.json_path)


# Blob Ops
@scalar_op_compiler.register_unary_op(ops.obj_fetch_metadata_op)
def obj_fetch_metadata_op_impl(obj_ref: ibis_types.Value):
    return obj_fetch_metadata(obj_ref=obj_ref)


@scalar_op_compiler.register_unary_op(ops.ObjGetAccessUrl, pass_op=True)
def obj_get_access_url_op_impl(obj_ref: ibis_types.Value, op: ops.ObjGetAccessUrl):
    return obj_get_access_url(obj_ref=obj_ref, mode=op.mode)


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
    x, y = _coerce_comparables(x, y)
    return x == y


@scalar_op_compiler.register_binary_op(ops.eq_null_match_op)
def eq_nulls_match_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    """Variant of eq_op where nulls match each other. Only use where dtypes are known to be same."""
    x, y = _coerce_comparables(x, y)
    literal = ibis_types.literal("$NULL_SENTINEL$")
    if hasattr(x, "fill_null"):
        left = x.cast(ibis_dtypes.str).fill_null(literal)
        right = y.cast(ibis_dtypes.str).fill_null(literal)
    else:
        left = x.cast(ibis_dtypes.str).fillna(literal)
        right = y.cast(ibis_dtypes.str).fillna(literal)

    return left == right


@scalar_op_compiler.register_binary_op(ops.ne_op)
def ne_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    x, y = _coerce_comparables(x, y)
    return x != y


def _null_or_value(value: ibis_types.Value, where_value: ibis_types.BooleanValue):
    return ibis_api.ifelse(
        where_value,
        value,
        ibis_types.null(),
    )


def _coerce_comparables(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    if x.type().is_boolean() and not y.type().is_boolean():
        x = x.cast(ibis_dtypes.int64)
    elif y.type().is_boolean() and not x.type().is_boolean():
        y = y.cast(ibis_dtypes.int64)
    return x, y


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
        return _null_or_value(y, y == ibis_types.literal(False))

    if isinstance(y, ibis_types.NullScalar):
        return _null_or_value(x, x == ibis_types.literal(False))
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
        return _null_or_value(y, y == ibis_types.literal(True))

    if isinstance(y, ibis_types.NullScalar):
        return _null_or_value(x, x == ibis_types.literal(True))
    return typing.cast(ibis_types.BooleanValue, x) | typing.cast(
        ibis_types.BooleanValue, y
    )


@scalar_op_compiler.register_binary_op(ops.xor_op)
def xor_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    return typing.cast(ibis_types.BooleanValue, x) ^ typing.cast(
        ibis_types.BooleanValue, y
    )


@scalar_op_compiler.register_binary_op(ops.add_op)
@short_circuit_nulls()
def add_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    if isinstance(x, ibis_types.NullScalar) or isinstance(x, ibis_types.NullScalar):
        return ibis_types.null()
    return x + y  # type: ignore


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
        ibis_api.case()
        .when((overflow_cond), ibis_types.null())
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
        ibis_api.case()
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
    x, y = _coerce_comparables(x, y)
    return x < y


@scalar_op_compiler.register_binary_op(ops.le_op)
@short_circuit_nulls(ibis_dtypes.bool)
def le_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    x, y = _coerce_comparables(x, y)
    return x <= y


@scalar_op_compiler.register_binary_op(ops.gt_op)
@short_circuit_nulls(ibis_dtypes.bool)
def gt_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    x, y = _coerce_comparables(x, y)
    return x > y


@scalar_op_compiler.register_binary_op(ops.ge_op)
@short_circuit_nulls(ibis_dtypes.bool)
def ge_op(
    x: ibis_types.Value,
    y: ibis_types.Value,
):
    x, y = _coerce_comparables(x, y)
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
        ibis_api.case()
        .when(y_numeric == _ZERO, zero_result * x_numeric)
        .else_(floordiv_expr)
        .end()
    )


def _is_bignumeric(x: ibis_types.Value):
    if not isinstance(x, ibis_types.DecimalValue):
        return False
    # Should be exactly 76 for bignumeric
    return x.precision > 70  # type: ignore


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
    if isinstance(op, ibis_generic.Literal) and op.value == 0:
        return ibis_types.null().cast(x.type())

    if x.type().is_integer() and y.type().is_integer():
        # both are ints, no casting necessary
        return _int_mod(
            typing.cast(ibis_types.IntegerValue, x),
            typing.cast(ibis_types.IntegerValue, y),
        )

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
        mod_numeric = _bignumeric_mod(x_numeric, y_numeric)  # type: ignore

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
    if isinstance(op, ibis_generic.Literal) and op.value == 0:
        return ibis_types.null().cast(x.type())

    bq_mod = x % y  # Bigquery will maintain x sign here

    # In BigQuery returned value has the same sign as X. In pandas, the sign of y is used, so we need to flip the result if sign(x) != sign(y)
    return (
        ibis_api.case()
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
    if isinstance(op, ibis_generic.Literal) and op.value == 0:
        return ibis_types.null().cast(x.type())

    bq_mod = x % y  # Bigquery will maintain x sign here

    # In BigQuery returned value has the same sign as X. In pandas, the sign of y is used, so we need to flip the result if sign(x) != sign(y)
    return (
        ibis_api.case()
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
    if hasattr(x, "fill_null"):
        return x.fill_null(typing.cast(ibis_types.Scalar, y))
    else:
        return x.fillna(typing.cast(ibis_types.Scalar, y))


@scalar_op_compiler.register_binary_op(ops.round_op)
def round_op(x: ibis_types.Value, y: ibis_types.Value):
    if x.type().is_integer():
        # bq produces float64, but pandas returns int
        return (
            typing.cast(ibis_types.NumericValue, x)
            .round(digits=typing.cast(ibis_types.IntegerValue, y))
            .cast(ibis_dtypes.int64)
        )
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
        return ibis_api.coalesce(x, y)


@scalar_op_compiler.register_binary_op(ops.maximum_op)
def maximum_impl(
    value: ibis_types.Value,
    lower: ibis_types.Value,
):
    # Note: propagates nulls
    return (
        ibis_api.case().when(lower.isnull() | (value < lower), lower).else_(value).end()
    )


@scalar_op_compiler.register_binary_op(ops.minimum_op)
def minimum_impl(
    value: ibis_types.Value,
    upper: ibis_types.Value,
):
    # Note: propagates nulls
    return (
        ibis_api.case().when(upper.isnull() | (value > upper), upper).else_(value).end()
    )


@scalar_op_compiler.register_binary_op(ops.cosine_distance_op)
def cosine_distance_impl(
    vector1: ibis_types.Value,
    vector2: ibis_types.Value,
):
    return vector_distance(vector1, vector2, "COSINE")


@scalar_op_compiler.register_binary_op(ops.euclidean_distance_op)
def euclidean_distance_impl(
    vector1: ibis_types.Value,
    vector2: ibis_types.Value,
):
    return vector_distance(vector1, vector2, "EUCLIDEAN")


@scalar_op_compiler.register_binary_op(ops.manhattan_distance_op)
def manhattan_distance_impl(
    vector1: ibis_types.Value,
    vector2: ibis_types.Value,
):
    return vector_distance(vector1, vector2, "MANHATTAN")


# Blob Ops
@scalar_op_compiler.register_binary_op(ops.obj_make_ref_op)
def obj_make_ref_op(x: ibis_types.Value, y: ibis_types.Value):
    return obj_make_ref(uri=x, authorizer=y)


# Ternary Operations
@scalar_op_compiler.register_ternary_op(ops.where_op)
def where_op(
    original: ibis_types.Value,
    condition: ibis_types.Value,
    replacement: ibis_types.Value,
) -> ibis_types.Value:
    """Returns x if y is true, otherwise returns z."""
    return ibis_api.case().when(condition, original).else_(replacement).end()  # type: ignore


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
        return ibis_api.least(original, upper)
    elif (not isinstance(lower, ibis_types.NullScalar)) and isinstance(
        upper, ibis_types.NullScalar
    ):
        return ibis_api.greatest(original, lower)
    elif isinstance(lower, ibis_types.NullScalar) and (
        isinstance(upper, ibis_types.NullScalar)
    ):
        return original
    else:
        # Note: Pandas has unchanged behavior when upper bound and lower bound are flipped. This implementation requires that lower_bound < upper_bound
        return ibis_api.greatest(ibis_api.least(original, upper), lower)


# N-ary Operations
@scalar_op_compiler.register_nary_op(ops.case_when_op)
def case_when_op(*cases_and_outputs: ibis_types.Value) -> ibis_types.Value:
    # ibis can handle most type coercions, but we need to force bool -> int
    # TODO: dispatch coercion depending on bigframes dtype schema
    result_values = cases_and_outputs[1::2]
    do_upcast_bool = any(t.type().is_numeric() for t in result_values)
    if do_upcast_bool:
        # Just need to upcast to int, ibis can handle further coercion
        result_values = tuple(
            val.cast(ibis_dtypes.int64) if val.type().is_boolean() else val
            for val in result_values
        )

    case_val = ibis_api.case()
    for predicate, output in zip(cases_and_outputs[::2], result_values):
        case_val = case_val.when(predicate, output)
    return case_val.end()  # type: ignore


@scalar_op_compiler.register_nary_op(ops.SqlScalarOp, pass_op=True)
def sql_scalar_op_impl(*operands: ibis_types.Value, op: ops.SqlScalarOp):
    return ibis_generic.SqlScalar(
        op.sql_template,
        values=tuple(typing.cast(ibis_generic.Value, expr.op()) for expr in operands),
        output_type=bigframes.core.compile.ibis_types.bigframes_dtype_to_ibis_dtype(
            op.output_type()
        ),
    ).to_expr()


@scalar_op_compiler.register_nary_op(ops.StructOp, pass_op=True)
def struct_op_impl(
    *values: ibis_types.Value, op: ops.StructOp
) -> ibis_types.StructValue:
    data = {}
    for i, value in enumerate(values):
        data[op.column_names[i]] = value

    return ibis_types.struct(data)


@scalar_op_compiler.register_nary_op(ops.RowKey, pass_op=True)
def rowkey_op_impl(*values: ibis_types.Value, op: ops.RowKey) -> ibis_types.Value:
    return bigframes.core.compile.default_ordering.gen_row_key(values)


# Helpers
def is_null(value) -> bool:
    # float NaN/inf should be treated as distinct from 'true' null values
    return typing.cast(bool, pd.isna(value)) and not isinstance(value, float)


def _ibis_num(number: float):
    return typing.cast(ibis_types.NumericValue, ibis_types.literal(number))


@ibis_udf.scalar.builtin
def st_geogfromtext(a: str) -> ibis_dtypes.geography:  # type: ignore
    """Convert string to geography."""


@ibis_udf.scalar.builtin
def timestamp(a: str) -> ibis_dtypes.timestamp:  # type: ignore
    """Convert string to timestamp."""


@ibis_udf.scalar.builtin
def unix_millis(a: ibis_dtypes.timestamp) -> int:  # type: ignore
    """Convert a timestamp to milliseconds"""


@ibis_udf.scalar.builtin
def st_boundary(a: ibis_dtypes.geography) -> ibis_dtypes.geography:  # type: ignore
    """Find the boundary of a geography."""


@ibis_udf.scalar.builtin
def st_distance(a: ibis_dtypes.geography, b: ibis_dtypes.geography, use_spheroid: bool) -> ibis_dtypes.float:  # type: ignore
    """Convert string to geography."""


@ibis_udf.scalar.builtin
def st_length(geog: ibis_dtypes.geography, use_spheroid: bool) -> ibis_dtypes.float:  # type: ignore
    """ST_LENGTH BQ builtin. This body is never executed."""
    pass


@ibis_udf.scalar.builtin
def unix_micros(a: ibis_dtypes.timestamp) -> int:  # type: ignore
    """Convert a timestamp to microseconds"""


# Need these because ibis otherwise tries to do casts to int that can fail
@ibis_udf.scalar.builtin(name="floor")
def float_floor(a: float) -> float:
    """Convert string to timestamp."""
    return 0  # pragma: NO COVER


@ibis_udf.scalar.builtin(name="ceil")
def float_ceil(a: float) -> float:
    """Convert string to timestamp."""
    return 0  # pragma: NO COVER


@ibis_udf.scalar.builtin(name="parse_json")
def parse_json(json_str: str) -> ibis_dtypes.JSON:  # type: ignore[empty-body]
    """Converts a JSON-formatted STRING value to a JSON value."""


@ibis_udf.scalar.builtin(name="SAFE.PARSE_JSON")
def parse_json_in_safe(json_str: str) -> ibis_dtypes.JSON:  # type: ignore[empty-body]
    """Converts a JSON-formatted STRING value to a JSON value in the safe mode."""


@ibis_udf.scalar.builtin(name="json_set")
def json_set(  # type: ignore[empty-body]
    json_obj: ibis_dtypes.JSON, json_path: ibis_dtypes.String, json_value
) -> ibis_dtypes.JSON:
    """Produces a new SQL JSON value with the specified JSON data inserted or replaced."""


@ibis_udf.scalar.builtin(name="json_extract_string_array")
def json_extract_string_array(  # type: ignore[empty-body]
    json_obj: ibis_dtypes.JSON, json_path: ibis_dtypes.String
) -> ibis_dtypes.Array[ibis_dtypes.String]:
    """Extracts a JSON array and converts it to a SQL ARRAY of STRINGs."""


@ibis_udf.scalar.builtin(name="to_json_string")
def to_json_string(  # type: ignore[empty-body]
    json_obj: ibis_dtypes.JSON,
) -> ibis_dtypes.String:
    """Convert JSON to STRING."""


@ibis_udf.scalar.builtin(name="json_value")
def json_value(  # type: ignore[empty-body]
    json_obj: ibis_dtypes.JSON, json_path: ibis_dtypes.String
) -> ibis_dtypes.String:
    """Retrieve value of a JSON field as plain STRING."""


@ibis_udf.scalar.builtin(name="json_value_array")
def json_value_array(  # type: ignore[empty-body]
    json_obj: ibis_dtypes.JSON, json_path: ibis_dtypes.String
) -> ibis_dtypes.Array[ibis_dtypes.String]:
    """Extracts a JSON array and converts it to a SQL ARRAY of STRINGs."""


@ibis_udf.scalar.builtin(name="INT64")
def cast_json_to_int64(json_str: ibis_dtypes.JSON) -> ibis_dtypes.Int64:  # type: ignore[empty-body]
    """Converts a JSON number to a SQL INT64 value."""


@ibis_udf.scalar.builtin(name="SAFE.INT64")
def cast_json_to_int64_in_safe(json_str: ibis_dtypes.JSON) -> ibis_dtypes.Int64:  # type: ignore[empty-body]
    """Converts a JSON number to a SQL INT64 value in the safe mode."""


@ibis_udf.scalar.builtin(name="FLOAT64")
def cast_json_to_float64(json_str: ibis_dtypes.JSON) -> ibis_dtypes.Float64:  # type: ignore[empty-body]
    """Attempts to convert a JSON value to a SQL FLOAT64 value."""


@ibis_udf.scalar.builtin(name="SAFE.FLOAT64")
def cast_json_to_float64_in_safe(json_str: ibis_dtypes.JSON) -> ibis_dtypes.Float64:  # type: ignore[empty-body]
    """Attempts to convert a JSON value to a SQL FLOAT64 value."""


@ibis_udf.scalar.builtin(name="BOOL")
def cast_json_to_bool(json_str: ibis_dtypes.JSON) -> ibis_dtypes.Boolean:  # type: ignore[empty-body]
    """Attempts to convert a JSON value to a SQL BOOL value."""


@ibis_udf.scalar.builtin(name="SAFE.BOOL")
def cast_json_to_bool_in_safe(json_str: ibis_dtypes.JSON) -> ibis_dtypes.Boolean:  # type: ignore[empty-body]
    """Attempts to convert a JSON value to a SQL BOOL value."""


@ibis_udf.scalar.builtin(name="STRING")
def cast_json_to_string(json_str: ibis_dtypes.JSON) -> ibis_dtypes.String:  # type: ignore[empty-body]
    """Attempts to convert a JSON value to a SQL STRING value."""


@ibis_udf.scalar.builtin(name="SAFE.STRING")
def cast_json_to_string_in_safe(json_str: ibis_dtypes.JSON) -> ibis_dtypes.String:  # type: ignore[empty-body]
    """Attempts to convert a JSON value to a SQL STRING value."""


@ibis_udf.scalar.builtin(name="ML.DISTANCE")
def vector_distance(vector1, vector2, type: str) -> ibis_dtypes.Float64:  # type: ignore[empty-body]
    """Computes the distance between two vectors using specified type ("EUCLIDEAN", "MANHATTAN", or "COSINE")"""


@ibis_udf.scalar.builtin(name="OBJ.FETCH_METADATA")
def obj_fetch_metadata(obj_ref: _OBJ_REF_IBIS_DTYPE) -> _OBJ_REF_IBIS_DTYPE:  # type: ignore
    """Fetch metadata from ObjectRef Struct."""


@ibis_udf.scalar.builtin(name="OBJ.MAKE_REF")
def obj_make_ref(uri: str, authorizer: str) -> _OBJ_REF_IBIS_DTYPE:  # type: ignore
    """Make ObjectRef Struct from uri and connection."""


@ibis_udf.scalar.builtin(name="OBJ.GET_ACCESS_URL")
def obj_get_access_url(obj_ref: _OBJ_REF_IBIS_DTYPE, mode: ibis_dtypes.String) -> ibis_dtypes.JSON:  # type: ignore
    """Get access url (as ObjectRefRumtime JSON) from ObjectRef."""


@ibis_udf.scalar.builtin(name="ltrim")
def str_lstrip_op(  # type: ignore[empty-body]
    x: ibis_dtypes.String, to_strip: ibis_dtypes.String
) -> ibis_dtypes.String:
    """Remove leading and trailing characters."""


@ibis_udf.scalar.builtin
def st_isclosed(a: ibis_dtypes.geography) -> ibis_dtypes.boolean:  # type: ignore
    """Checks if a geography is closed."""


@ibis_udf.scalar.builtin(name="rtrim")
def str_rstrip_op(  # type: ignore[empty-body]
    x: ibis_dtypes.String, to_strip: ibis_dtypes.String
) -> ibis_dtypes.String:
    """Remove leading and trailing characters."""


@ibis_udf.scalar.builtin(name="trim")
def str_strip_op(  # type: ignore[empty-body]
    x: ibis_dtypes.String, to_strip: ibis_dtypes.String
) -> ibis_dtypes.String:
    """Remove leading and trailing characters."""
