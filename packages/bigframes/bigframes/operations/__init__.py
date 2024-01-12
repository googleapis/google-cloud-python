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
def create_unary_op(name: str) -> UnaryOp:
    return dataclasses.make_dataclass(
        name,
        [("name", typing.ClassVar[str], name)],  # type: ignore
        bases=(UnaryOp,),
        frozen=True,
    )()


def create_binary_op(name: str) -> BinaryOp:
    return dataclasses.make_dataclass(
        name,
        [("name", typing.ClassVar[str], name)],  # type: ignore
        bases=(BinaryOp,),
        frozen=True,
    )()


def create_ternary_op(name: str) -> TernaryOp:
    return dataclasses.make_dataclass(
        name,
        [("name", typing.ClassVar[str], name)],  # type: ignore
        bases=(TernaryOp,),
        frozen=True,
    )()


# Unary Ops
## Generic Ops
invert_op = create_unary_op(name="invert")
isnull_op = create_unary_op(name="isnull")
notnull_op = create_unary_op(name="notnull")
hash_op = create_unary_op(name="hash")
## String Ops
len_op = create_unary_op(name="len")
reverse_op = create_unary_op(name="reverse")
lower_op = create_unary_op(name="lower")
upper_op = create_unary_op(name="upper")
strip_op = create_unary_op(name="strip")
isalnum_op = create_unary_op(name="isalnum")
isalpha_op = create_unary_op(name="isalpha")
isdecimal_op = create_unary_op(name="isdecimal")
isdigit_op = create_unary_op(name="isdigit")
isnumeric_op = create_unary_op(name="isnumeric")
isspace_op = create_unary_op(name="isspace")
islower_op = create_unary_op(name="islower")
isupper_op = create_unary_op(name="isupper")
rstrip_op = create_unary_op(name="rstrip")
lstrip_op = create_unary_op(name="lstrip")
capitalize_op = create_unary_op(name="capitalize")
## DateTime Ops
day_op = create_unary_op(name="day")
dayofweek_op = create_unary_op(name="dayofweek")
date_op = create_unary_op(name="date")
hour_op = create_unary_op(name="hour")
minute_op = create_unary_op(name="minute")
month_op = create_unary_op(name="month")
quarter_op = create_unary_op(name="quarter")
second_op = create_unary_op(name="second")
time_op = create_unary_op(name="time")
year_op = create_unary_op(name="year")
## Trigonometry Ops
sin_op = create_unary_op(name="sin")
cos_op = create_unary_op(name="cos")
tan_op = create_unary_op(name="tan")
arcsin_op = create_unary_op(name="arcsin")
arccos_op = create_unary_op(name="arccos")
arctan_op = create_unary_op(name="arctan")
sinh_op = create_unary_op(name="sinh")
cosh_op = create_unary_op(name="cosh")
tanh_op = create_unary_op(name="tanh")
arcsinh_op = create_unary_op(name="arcsinh")
arccosh_op = create_unary_op(name="arccosh")
arctanh_op = create_unary_op(name="arctanh")
## Numeric Ops
abs_op = create_unary_op(name="abs")
exp_op = create_unary_op(name="exp")
ln_op = create_unary_op(name="log")
log10_op = create_unary_op(name="log10")
sqrt_op = create_unary_op(name="sqrt")


# Parameterized unary ops
@dataclasses.dataclass(frozen=True)
class StrContainsOp(UnaryOp):
    name: typing.ClassVar[str] = "str_contains"
    pat: str


@dataclasses.dataclass(frozen=True)
class StrContainsRegexOp(UnaryOp):
    name: typing.ClassVar[str] = "str_contains_regex"
    pat: str


@dataclasses.dataclass(frozen=True)
class StrGetOp(UnaryOp):
    name: typing.ClassVar[str] = "str_get"
    i: int


@dataclasses.dataclass(frozen=True)
class StrPadOp(UnaryOp):
    name: typing.ClassVar[str] = "str_pad"
    length: int
    fillchar: str
    side: typing.Literal["both", "left", "right"]


@dataclasses.dataclass(frozen=True)
class ReplaceStrOp(UnaryOp):
    name: typing.ClassVar[str] = "str_replace"
    pat: str
    repl: str


@dataclasses.dataclass(frozen=True)
class RegexReplaceStrOp(UnaryOp):
    name: typing.ClassVar[str] = "str_rereplace"
    pat: str
    repl: str


@dataclasses.dataclass(frozen=True)
class StartsWithOp(UnaryOp):
    name: typing.ClassVar[str] = "str_startswith"
    pat: typing.Sequence[str]


@dataclasses.dataclass(frozen=True)
class EndsWithOp(UnaryOp):
    name: typing.ClassVar[str] = "str_endswith"
    pat: typing.Sequence[str]


@dataclasses.dataclass(frozen=True)
class ZfillOp(UnaryOp):
    name: typing.ClassVar[str] = "str_zfill"
    width: int


@dataclasses.dataclass(frozen=True)
class StrFindOp(UnaryOp):
    name: typing.ClassVar[str] = "str_find"
    substr: str
    start: typing.Optional[int]
    end: typing.Optional[int]


@dataclasses.dataclass(frozen=True)
class StrExtractOp(UnaryOp):
    name: typing.ClassVar[str] = "str_extract"
    pat: str
    n: int = 1


@dataclasses.dataclass(frozen=True)
class StrSliceOp(UnaryOp):
    name: typing.ClassVar[str] = "str_slice"
    start: typing.Optional[int]
    end: typing.Optional[int]


@dataclasses.dataclass(frozen=True)
class StrRepeatOp(UnaryOp):
    name: typing.ClassVar[str] = "str_repeat"
    repeats: int


# Other parameterized unary operations
@dataclasses.dataclass(frozen=True)
class StructFieldOp(UnaryOp):
    name: typing.ClassVar[str] = "struct_field"
    name_or_index: str | int


@dataclasses.dataclass(frozen=True)
class AsTypeOp(UnaryOp):
    name: typing.ClassVar[str] = "astype"
    to_type: dtypes.DtypeString | dtypes.Dtype


@dataclasses.dataclass(frozen=True)
class IsInOp(UnaryOp):
    name: typing.ClassVar[str] = "is_in"
    values: typing.Tuple
    match_nulls: bool = True


@dataclasses.dataclass(frozen=True)
class RemoteFunctionOp(UnaryOp):
    name: typing.ClassVar[str] = "remote_function"
    func: typing.Callable
    apply_on_null: bool


@dataclasses.dataclass(frozen=True)
class MapOp(UnaryOp):
    name = "map_values"
    mappings: typing.Tuple[typing.Tuple[typing.Hashable, typing.Hashable], ...]


# Binary Ops
fillna_op = create_binary_op(name="fillna")
cliplower_op = create_binary_op(name="clip_lower")
clipupper_op = create_binary_op(name="clip_upper")
coalesce_op = create_binary_op(name="coalesce")
## Math Ops
add_op = create_binary_op(name="add")
sub_op = create_binary_op(name="sub")
mul_op = create_binary_op(name="mul")
div_op = create_binary_op(name="div")
floordiv_op = create_binary_op(name="floordiv")
pow_op = create_binary_op(name="pow")
mod_op = create_binary_op(name="mod")
round_op = create_binary_op(name="round")
unsafe_pow_op = create_binary_op(name="unsafe_pow_op")
# Logical Ops
and_op = create_binary_op(name="and")
or_op = create_binary_op(name="or")

## Comparison Ops
eq_op = create_binary_op(name="eq")
eq_null_match_op = create_binary_op(name="eq_nulls_match")
ne_op = create_binary_op(name="ne")
lt_op = create_binary_op(name="lt")
gt_op = create_binary_op(name="gt")
le_op = create_binary_op(name="le")
ge_op = create_binary_op(name="ge")

## String Ops
strconcat_op = create_binary_op(name="strconcat")

# Ternary Ops
where_op = create_ternary_op(name="where")
clip_op = create_ternary_op(name="clip")


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
