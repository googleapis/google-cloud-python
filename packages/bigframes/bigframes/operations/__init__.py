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

import dataclasses
import typing

import numpy as np

import bigframes.dtypes as dtypes
import bigframes.operations.type as op_typing

if typing.TYPE_CHECKING:
    # Avoids circular dependency
    import bigframes.core.expression


class RowOp(typing.Protocol):
    @property
    def name(self) -> str:
        raise NotImplementedError("RowOp abstract base class has no implementation")

    @property
    def arguments(self) -> int:
        """The number of column argument the operation takes"""
        raise NotImplementedError("RowOp abstract base class has no implementation")

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        raise NotImplementedError("Abstract typing rule has no output type")


# These classes can be used to create simple ops that don't take local parameters
# All is needed is a unique name, and to register an implementation in ibis_mappings.py
@dataclasses.dataclass(frozen=True)
class UnaryOp:
    @property
    def name(self) -> str:
        raise NotImplementedError("RowOp abstract base class has no implementation")

    @property
    def arguments(self) -> int:
        return 1

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        raise NotImplementedError("Abstract operation has no output type")

    def as_expr(
        self, input_id: typing.Union[str, bigframes.core.expression.Expression] = "arg"
    ) -> bigframes.core.expression.Expression:
        import bigframes.core.expression

        return bigframes.core.expression.OpExpression(
            self, (_convert_expr_input(input_id),)
        )


@dataclasses.dataclass(frozen=True)
class BinaryOp:
    @property
    def name(self) -> str:
        raise NotImplementedError("RowOp abstract base class has no implementation")

    @property
    def arguments(self) -> int:
        return 2

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        raise NotImplementedError("Abstract operation has no output type")

    def as_expr(
        self,
        left_input: typing.Union[str, bigframes.core.expression.Expression] = "arg1",
        right_input: typing.Union[str, bigframes.core.expression.Expression] = "arg2",
    ) -> bigframes.core.expression.Expression:
        import bigframes.core.expression

        return bigframes.core.expression.OpExpression(
            self,
            (
                _convert_expr_input(left_input),
                _convert_expr_input(right_input),
            ),
        )


@dataclasses.dataclass(frozen=True)
class TernaryOp:
    @property
    def name(self) -> str:
        raise NotImplementedError("RowOp abstract base class has no implementation")

    @property
    def arguments(self) -> int:
        return 3

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        raise NotImplementedError("Abstract operation has no output type")

    def as_expr(
        self,
        input1: typing.Union[str, bigframes.core.expression.Expression] = "arg1",
        input2: typing.Union[str, bigframes.core.expression.Expression] = "arg2",
        input3: typing.Union[str, bigframes.core.expression.Expression] = "arg3",
    ) -> bigframes.core.expression.Expression:
        import bigframes.core.expression

        return bigframes.core.expression.OpExpression(
            self,
            (
                _convert_expr_input(input1),
                _convert_expr_input(input2),
                _convert_expr_input(input3),
            ),
        )


def _convert_expr_input(
    input: typing.Union[str, bigframes.core.expression.Expression]
) -> bigframes.core.expression.Expression:
    """Allows creating free variables with just a string"""
    import bigframes.core.expression

    if isinstance(input, str):
        return bigframes.core.expression.UnboundVariableExpression(input)
    else:
        return input


# Operation Factories
def create_unary_op(
    name: str, type_rule: op_typing.OpTypeRule = op_typing.INPUT_TYPE
) -> UnaryOp:
    return dataclasses.make_dataclass(
        name,
        [("name", typing.ClassVar[str], name), ("output_type", typing.ClassVar[typing.Callable], type_rule.as_method)],  # type: ignore
        bases=(UnaryOp,),
        frozen=True,
    )()


def create_binary_op(
    name: str, type_rule: op_typing.OpTypeRule = op_typing.Supertype()
) -> BinaryOp:
    return dataclasses.make_dataclass(
        name,
        [("name", typing.ClassVar[str], name), ("output_type", typing.ClassVar[typing.Callable], type_rule.as_method)],  # type: ignore
        bases=(BinaryOp,),
        frozen=True,
    )()


def create_ternary_op(
    name: str, type_rule: op_typing.OpTypeRule = op_typing.Supertype()
) -> TernaryOp:
    return dataclasses.make_dataclass(
        name,
        [("name", typing.ClassVar[str], name), ("output_type", typing.ClassVar[typing.Callable], type_rule.as_method)],  # type: ignore
        bases=(TernaryOp,),
        frozen=True,
    )()


# Unary Ops
## Generic Ops
invert_op = create_unary_op(name="invert", type_rule=op_typing.INPUT_TYPE)
isnull_op = create_unary_op(name="isnull", type_rule=op_typing.PREDICATE)
notnull_op = create_unary_op(name="notnull", type_rule=op_typing.PREDICATE)
hash_op = create_unary_op(name="hash", type_rule=op_typing.INTEGER)
## String Ops
len_op = create_unary_op(name="len", type_rule=op_typing.INTEGER)
reverse_op = create_unary_op(name="reverse", type_rule=op_typing.STRING)
lower_op = create_unary_op(name="lower", type_rule=op_typing.STRING)
upper_op = create_unary_op(name="upper", type_rule=op_typing.STRING)
strip_op = create_unary_op(name="strip", type_rule=op_typing.STRING)
isalnum_op = create_unary_op(name="isalnum", type_rule=op_typing.PREDICATE)
isalpha_op = create_unary_op(name="isalpha", type_rule=op_typing.PREDICATE)
isdecimal_op = create_unary_op(name="isdecimal", type_rule=op_typing.PREDICATE)
isdigit_op = create_unary_op(name="isdigit", type_rule=op_typing.PREDICATE)
isnumeric_op = create_unary_op(name="isnumeric", type_rule=op_typing.PREDICATE)
isspace_op = create_unary_op(name="isspace", type_rule=op_typing.PREDICATE)
islower_op = create_unary_op(name="islower", type_rule=op_typing.PREDICATE)
isupper_op = create_unary_op(name="isupper", type_rule=op_typing.PREDICATE)
rstrip_op = create_unary_op(name="rstrip", type_rule=op_typing.STRING)
lstrip_op = create_unary_op(name="lstrip", type_rule=op_typing.STRING)
capitalize_op = create_unary_op(name="capitalize", type_rule=op_typing.STRING)
## DateTime Ops
day_op = create_unary_op(name="day", type_rule=op_typing.INTEGER)
dayofweek_op = create_unary_op(name="dayofweek", type_rule=op_typing.INTEGER)
date_op = create_unary_op(name="date")
hour_op = create_unary_op(name="hour", type_rule=op_typing.INTEGER)
minute_op = create_unary_op(name="minute", type_rule=op_typing.INTEGER)
month_op = create_unary_op(name="month", type_rule=op_typing.INTEGER)
quarter_op = create_unary_op(name="quarter", type_rule=op_typing.INTEGER)
second_op = create_unary_op(name="second", type_rule=op_typing.INTEGER)
time_op = create_unary_op(name="time", type_rule=op_typing.INTEGER)
year_op = create_unary_op(name="year", type_rule=op_typing.INTEGER)
## Trigonometry Ops
sin_op = create_unary_op(name="sin", type_rule=op_typing.REAL_NUMERIC)
cos_op = create_unary_op(name="cos", type_rule=op_typing.REAL_NUMERIC)
tan_op = create_unary_op(name="tan", type_rule=op_typing.REAL_NUMERIC)
arcsin_op = create_unary_op(name="arcsin", type_rule=op_typing.REAL_NUMERIC)
arccos_op = create_unary_op(name="arccos", type_rule=op_typing.REAL_NUMERIC)
arctan_op = create_unary_op(name="arctan", type_rule=op_typing.REAL_NUMERIC)
sinh_op = create_unary_op(name="sinh", type_rule=op_typing.REAL_NUMERIC)
cosh_op = create_unary_op(name="cosh", type_rule=op_typing.REAL_NUMERIC)
tanh_op = create_unary_op(name="tanh", type_rule=op_typing.REAL_NUMERIC)
arcsinh_op = create_unary_op(name="arcsinh", type_rule=op_typing.REAL_NUMERIC)
arccosh_op = create_unary_op(name="arccosh", type_rule=op_typing.REAL_NUMERIC)
arctanh_op = create_unary_op(name="arctanh", type_rule=op_typing.REAL_NUMERIC)
## Numeric Ops
abs_op = create_unary_op(name="abs", type_rule=op_typing.INPUT_TYPE)
exp_op = create_unary_op(name="exp", type_rule=op_typing.REAL_NUMERIC)
ln_op = create_unary_op(name="log", type_rule=op_typing.REAL_NUMERIC)
log10_op = create_unary_op(name="log10", type_rule=op_typing.REAL_NUMERIC)
sqrt_op = create_unary_op(name="sqrt", type_rule=op_typing.REAL_NUMERIC)


# Parameterized unary ops
@dataclasses.dataclass(frozen=True)
class StrContainsOp(UnaryOp):
    name: typing.ClassVar[str] = "str_contains"
    pat: str

    def output_type(self, *input_types):
        return dtypes.BOOL_DTYPE


@dataclasses.dataclass(frozen=True)
class StrContainsRegexOp(UnaryOp):
    name: typing.ClassVar[str] = "str_contains_regex"
    pat: str

    def output_type(self, *input_types):
        return dtypes.BOOL_DTYPE


@dataclasses.dataclass(frozen=True)
class StrGetOp(UnaryOp):
    name: typing.ClassVar[str] = "str_get"
    i: int

    def output_type(self, *input_types):
        return dtypes.STRING_DTYPE


@dataclasses.dataclass(frozen=True)
class StrPadOp(UnaryOp):
    name: typing.ClassVar[str] = "str_pad"
    length: int
    fillchar: str
    side: typing.Literal["both", "left", "right"]

    def output_type(self, *input_types):
        return dtypes.STRING_DTYPE


@dataclasses.dataclass(frozen=True)
class ReplaceStrOp(UnaryOp):
    name: typing.ClassVar[str] = "str_replace"
    pat: str
    repl: str

    def output_type(self, *input_types):
        return dtypes.STRING_DTYPE


@dataclasses.dataclass(frozen=True)
class RegexReplaceStrOp(UnaryOp):
    name: typing.ClassVar[str] = "str_rereplace"
    pat: str
    repl: str

    def output_type(self, *input_types):
        return dtypes.STRING_DTYPE


@dataclasses.dataclass(frozen=True)
class StartsWithOp(UnaryOp):
    name: typing.ClassVar[str] = "str_startswith"
    pat: typing.Sequence[str]

    def output_type(self, *input_types):
        return dtypes.BOOL_DTYPE


@dataclasses.dataclass(frozen=True)
class EndsWithOp(UnaryOp):
    name: typing.ClassVar[str] = "str_endswith"
    pat: typing.Sequence[str]

    def output_type(self, *input_types):
        return dtypes.BOOL_DTYPE


@dataclasses.dataclass(frozen=True)
class ZfillOp(UnaryOp):
    name: typing.ClassVar[str] = "str_zfill"
    width: int

    def output_type(self, *input_types):
        return dtypes.STRING_DTYPE


@dataclasses.dataclass(frozen=True)
class StrFindOp(UnaryOp):
    name: typing.ClassVar[str] = "str_find"
    substr: str
    start: typing.Optional[int]
    end: typing.Optional[int]

    def output_type(self, *input_types):
        return dtypes.BOOL_DTYPE


@dataclasses.dataclass(frozen=True)
class StrExtractOp(UnaryOp):
    name: typing.ClassVar[str] = "str_extract"
    pat: str
    n: int = 1

    def output_type(self, *input_types):
        return dtypes.STRING_DTYPE


@dataclasses.dataclass(frozen=True)
class StrSliceOp(UnaryOp):
    name: typing.ClassVar[str] = "str_slice"
    start: typing.Optional[int]
    end: typing.Optional[int]

    def output_type(self, *input_types):
        return dtypes.STRING_DTYPE


@dataclasses.dataclass(frozen=True)
class StrRepeatOp(UnaryOp):
    name: typing.ClassVar[str] = "str_repeat"
    repeats: int

    def output_type(self, *input_types):
        return dtypes.STRING_DTYPE


# Other parameterized unary operations
@dataclasses.dataclass(frozen=True)
class StructFieldOp(UnaryOp):
    name: typing.ClassVar[str] = "struct_field"
    name_or_index: str | int


@dataclasses.dataclass(frozen=True)
class AsTypeOp(UnaryOp):
    name: typing.ClassVar[str] = "astype"
    # TODO: Convert strings to dtype earlier
    to_type: dtypes.DtypeString | dtypes.Dtype

    def output_type(self, *input_types):
        if isinstance(self.to_type, str):
            return dtypes.BIGFRAMES_STRING_TO_BIGFRAMES[self.to_type]
        return self.to_type


@dataclasses.dataclass(frozen=True)
class IsInOp(UnaryOp):
    name: typing.ClassVar[str] = "is_in"
    values: typing.Tuple
    match_nulls: bool = True

    def output_type(self, *input_types):
        return dtypes.BOOL_DTYPE


@dataclasses.dataclass(frozen=True)
class RemoteFunctionOp(UnaryOp):
    name: typing.ClassVar[str] = "remote_function"
    func: typing.Callable
    apply_on_null: bool

    def output_type(self, *input_types):
        python_type = self.func.__signature__.output_type
        ibis_type = dtypes.ibis_type_from_python_type(python_type)
        dtype = dtypes.ibis_dtype_to_bigframes_dtype(ibis_type)
        return dtype


@dataclasses.dataclass(frozen=True)
class MapOp(UnaryOp):
    name = "map_values"
    mappings: typing.Tuple[typing.Tuple[typing.Hashable, typing.Hashable], ...]

    def output_type(self, *input_types):
        return input_types[0]


@dataclasses.dataclass(frozen=True)
class ToDatetimeOp(UnaryOp):
    name: typing.ClassVar[str] = "to_datetime"
    utc: bool = False
    format: typing.Optional[str] = None
    unit: typing.Optional[str] = None

    def output_type(self, *input_types):
        return input_types[0]


# Binary Ops
fillna_op = create_binary_op(name="fillna")
cliplower_op = create_binary_op(name="clip_lower")
clipupper_op = create_binary_op(name="clip_upper")
coalesce_op = create_binary_op(name="coalesce")
## Math Ops
add_op = create_binary_op(name="add", type_rule=op_typing.NUMERIC)
sub_op = create_binary_op(name="sub", type_rule=op_typing.NUMERIC)
mul_op = create_binary_op(name="mul", type_rule=op_typing.NUMERIC)
div_op = create_binary_op(name="div", type_rule=op_typing.REAL_NUMERIC)
floordiv_op = create_binary_op(name="floordiv", type_rule=op_typing.REAL_NUMERIC)
pow_op = create_binary_op(name="pow", type_rule=op_typing.REAL_NUMERIC)
mod_op = create_binary_op(name="mod", type_rule=op_typing.NUMERIC)
round_op = create_binary_op(name="round", type_rule=op_typing.REAL_NUMERIC)
unsafe_pow_op = create_binary_op(name="unsafe_pow_op", type_rule=op_typing.REAL_NUMERIC)
# Logical Ops
and_op = create_binary_op(name="and", type_rule=op_typing.PREDICATE)
or_op = create_binary_op(name="or", type_rule=op_typing.PREDICATE)

## Comparison Ops
eq_op = create_binary_op(name="eq", type_rule=op_typing.PREDICATE)
eq_null_match_op = create_binary_op(
    name="eq_nulls_match", type_rule=op_typing.PREDICATE
)
ne_op = create_binary_op(name="ne", type_rule=op_typing.PREDICATE)
lt_op = create_binary_op(name="lt", type_rule=op_typing.PREDICATE)
gt_op = create_binary_op(name="gt", type_rule=op_typing.PREDICATE)
le_op = create_binary_op(name="le", type_rule=op_typing.PREDICATE)
ge_op = create_binary_op(name="ge", type_rule=op_typing.PREDICATE)

## String Ops
strconcat_op = create_binary_op(name="strconcat", type_rule=op_typing.STRING)


# Ternary Ops
@dataclasses.dataclass(frozen=True)
class WhereOp(TernaryOp):
    name: typing.ClassVar[str] = "where"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        # Second input is boolean and doesn't affect output type
        return dtypes.lcd_etype(input_types[0], input_types[2])


where_op = WhereOp()


clip_op = create_ternary_op(name="clip", type_rule=op_typing.Supertype())


# Just parameterless unary ops for now
# TODO: Parameter mappings
NUMPY_TO_OP: typing.Final = {
    np.sin: sin_op,
    np.cos: cos_op,
    np.tan: tan_op,
    np.arcsin: arcsin_op,
    np.arccos: arccos_op,
    np.arctan: arctan_op,
    np.sinh: sinh_op,
    np.cosh: cosh_op,
    np.tanh: tanh_op,
    np.arcsinh: arcsinh_op,
    np.arccosh: arccosh_op,
    np.arctanh: arctanh_op,
    np.exp: exp_op,
    np.log: ln_op,
    np.log10: log10_op,
    np.sqrt: sqrt_op,
    np.abs: abs_op,
}


NUMPY_TO_BINOP: typing.Final = {
    np.add: add_op,
    np.subtract: sub_op,
    np.multiply: mul_op,
    np.divide: div_op,
    np.power: pow_op,
}
