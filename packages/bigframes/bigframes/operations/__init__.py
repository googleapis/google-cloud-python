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
import pandas as pd
import pyarrow as pa

import bigframes.dtypes as dtypes
import bigframes.operations.type as op_typing

if typing.TYPE_CHECKING:
    # Avoids circular dependency
    import bigframes.core.expression


class RowOp(typing.Protocol):
    @property
    def name(self) -> str:
        ...

    @property
    def arguments(self) -> int:
        """The number of column argument the operation takes"""
        ...

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        ...

    @property
    def order_preserving(self) -> bool:
        """Whether the row operation preserves total ordering. Can be pruned from ordering expressions."""
        ...


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

    @property
    def order_preserving(self) -> bool:
        """Whether the row operation preserves total ordering. Can be pruned from ordering expressions."""
        return False


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

    @property
    def order_preserving(self) -> bool:
        """Whether the row operation preserves total ordering. Can be pruned from ordering expressions."""
        return False


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

    @property
    def order_preserving(self) -> bool:
        """Whether the row operation preserves total ordering. Can be pruned from ordering expressions."""
        return False


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
def create_unary_op(name: str, type_signature: op_typing.UnaryTypeSignature) -> UnaryOp:
    return dataclasses.make_dataclass(
        name,
        [("name", typing.ClassVar[str], name), ("output_type", typing.ClassVar[typing.Callable], type_signature.as_method)],  # type: ignore
        bases=(UnaryOp,),
        frozen=True,
    )()


def create_binary_op(
    name: str, type_signature: op_typing.BinaryTypeSignature
) -> BinaryOp:
    return dataclasses.make_dataclass(
        name,
        [("name", typing.ClassVar[str], name), ("output_type", typing.ClassVar[typing.Callable], type_signature.as_method)],  # type: ignore
        bases=(BinaryOp,),
        frozen=True,
    )()


# Unary Ops
## Generic Ops
invert_op = create_unary_op(
    name="invert",
    type_signature=op_typing.TypePreserving(
        dtypes.is_binary_like,
        description="binary-like",
    ),
)  # numeric
isnull_op = create_unary_op(
    name="isnull",
    type_signature=op_typing.FixedOutputType(
        lambda x: True, dtypes.BOOL_DTYPE, description="nullable"
    ),
)
notnull_op = create_unary_op(
    name="notnull",
    type_signature=op_typing.FixedOutputType(
        lambda x: True, dtypes.BOOL_DTYPE, description="nullable"
    ),
)
hash_op = create_unary_op(
    name="hash",
    type_signature=op_typing.FixedOutputType(
        dtypes.is_string_like, dtypes.INT_DTYPE, description="string-like"
    ),
)
## String Ops
len_op = create_unary_op(
    name="len",
    type_signature=op_typing.FixedOutputType(
        dtypes.is_iterable, dtypes.INT_DTYPE, description="iterable"
    ),
)
reverse_op = create_unary_op(name="reverse", type_signature=op_typing.STRING_TRANSFORM)
lower_op = create_unary_op(name="lower", type_signature=op_typing.STRING_TRANSFORM)
upper_op = create_unary_op(name="upper", type_signature=op_typing.STRING_TRANSFORM)
strip_op = create_unary_op(name="strip", type_signature=op_typing.STRING_TRANSFORM)
isalnum_op = create_unary_op(name="isalnum", type_signature=op_typing.STRING_PREDICATE)
isalpha_op = create_unary_op(name="isalpha", type_signature=op_typing.STRING_PREDICATE)
isdecimal_op = create_unary_op(
    name="isdecimal", type_signature=op_typing.STRING_PREDICATE
)
isdigit_op = create_unary_op(name="isdigit", type_signature=op_typing.STRING_PREDICATE)
isnumeric_op = create_unary_op(
    name="isnumeric", type_signature=op_typing.STRING_PREDICATE
)
isspace_op = create_unary_op(name="isspace", type_signature=op_typing.STRING_PREDICATE)
islower_op = create_unary_op(name="islower", type_signature=op_typing.STRING_PREDICATE)
isupper_op = create_unary_op(name="isupper", type_signature=op_typing.STRING_PREDICATE)
rstrip_op = create_unary_op(name="rstrip", type_signature=op_typing.STRING_TRANSFORM)
lstrip_op = create_unary_op(name="lstrip", type_signature=op_typing.STRING_TRANSFORM)
capitalize_op = create_unary_op(
    name="capitalize", type_signature=op_typing.STRING_TRANSFORM
)
## DateTime Ops
### datelike accessors
day_op = create_unary_op(
    name="day",
    type_signature=op_typing.DATELIKE_ACCESSOR,
)
month_op = create_unary_op(
    name="month",
    type_signature=op_typing.DATELIKE_ACCESSOR,
)
year_op = create_unary_op(
    name="year",
    type_signature=op_typing.DATELIKE_ACCESSOR,
)
dayofweek_op = create_unary_op(
    name="dayofweek",
    type_signature=op_typing.DATELIKE_ACCESSOR,
)
quarter_op = create_unary_op(
    name="quarter",
    type_signature=op_typing.DATELIKE_ACCESSOR,
)
### timelike accessors
hour_op = create_unary_op(
    name="hour",
    type_signature=op_typing.TIMELIKE_ACCESSOR,
)
minute_op = create_unary_op(
    name="minute",
    type_signature=op_typing.TIMELIKE_ACCESSOR,
)
second_op = create_unary_op(
    name="second",
    type_signature=op_typing.TIMELIKE_ACCESSOR,
)
normalize_op = create_unary_op(
    name="normalize",
    type_signature=op_typing.TypePreserving(
        dtypes.is_time_like,
        description="time-like",
    ),
)
### datetimelike accessors
date_op = create_unary_op(
    name="date",
    type_signature=op_typing.FixedOutputType(
        dtypes.is_date_like, dtypes.DATE_DTYPE, description="date-like"
    ),
)
time_op = create_unary_op(
    name="time",
    type_signature=op_typing.FixedOutputType(
        dtypes.is_time_like, dtypes.TIME_DTYPE, description="time-like"
    ),
)
## Trigonometry Ops
sin_op = create_unary_op(name="sin", type_signature=op_typing.UNARY_REAL_NUMERIC)
cos_op = create_unary_op(name="cos", type_signature=op_typing.UNARY_REAL_NUMERIC)
tan_op = create_unary_op(name="tan", type_signature=op_typing.UNARY_REAL_NUMERIC)
arcsin_op = create_unary_op(name="arcsin", type_signature=op_typing.UNARY_REAL_NUMERIC)
arccos_op = create_unary_op(name="arccos", type_signature=op_typing.UNARY_REAL_NUMERIC)
arctan_op = create_unary_op(name="arctan", type_signature=op_typing.UNARY_REAL_NUMERIC)
sinh_op = create_unary_op(name="sinh", type_signature=op_typing.UNARY_REAL_NUMERIC)
cosh_op = create_unary_op(name="cosh", type_signature=op_typing.UNARY_REAL_NUMERIC)
tanh_op = create_unary_op(name="tanh", type_signature=op_typing.UNARY_REAL_NUMERIC)
arcsinh_op = create_unary_op(
    name="arcsinh", type_signature=op_typing.UNARY_REAL_NUMERIC
)
arccosh_op = create_unary_op(
    name="arccosh", type_signature=op_typing.UNARY_REAL_NUMERIC
)
arctanh_op = create_unary_op(
    name="arctanh", type_signature=op_typing.UNARY_REAL_NUMERIC
)
## Numeric Ops
floor_op = create_unary_op(name="floor", type_signature=op_typing.UNARY_REAL_NUMERIC)
ceil_op = create_unary_op(name="ceil", type_signature=op_typing.UNARY_REAL_NUMERIC)
abs_op = create_unary_op(name="abs", type_signature=op_typing.UNARY_NUMERIC)
exp_op = create_unary_op(name="exp", type_signature=op_typing.UNARY_REAL_NUMERIC)
expm1_op = create_unary_op(name="expm1", type_signature=op_typing.UNARY_REAL_NUMERIC)
ln_op = create_unary_op(name="log", type_signature=op_typing.UNARY_REAL_NUMERIC)
log10_op = create_unary_op(name="log10", type_signature=op_typing.UNARY_REAL_NUMERIC)
log1p_op = create_unary_op(name="log1p", type_signature=op_typing.UNARY_REAL_NUMERIC)
sqrt_op = create_unary_op(name="sqrt", type_signature=op_typing.UNARY_REAL_NUMERIC)


# Parameterized unary ops
@dataclasses.dataclass(frozen=True)
class StrContainsOp(UnaryOp):
    name: typing.ClassVar[str] = "str_contains"
    pat: str

    def output_type(self, *input_types):
        return op_typing.STRING_PREDICATE.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class StrContainsRegexOp(UnaryOp):
    name: typing.ClassVar[str] = "str_contains_regex"
    pat: str

    def output_type(self, *input_types):
        return op_typing.STRING_PREDICATE.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class StrGetOp(UnaryOp):
    name: typing.ClassVar[str] = "str_get"
    i: int

    def output_type(self, *input_types):
        return op_typing.STRING_TRANSFORM.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class StrPadOp(UnaryOp):
    name: typing.ClassVar[str] = "str_pad"
    length: int
    fillchar: str
    side: typing.Literal["both", "left", "right"]

    def output_type(self, *input_types):
        return op_typing.STRING_TRANSFORM.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class ReplaceStrOp(UnaryOp):
    name: typing.ClassVar[str] = "str_replace"
    pat: str
    repl: str

    def output_type(self, *input_types):
        return op_typing.STRING_TRANSFORM.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class RegexReplaceStrOp(UnaryOp):
    name: typing.ClassVar[str] = "str_rereplace"
    pat: str
    repl: str

    def output_type(self, *input_types):
        return op_typing.STRING_TRANSFORM.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class StartsWithOp(UnaryOp):
    name: typing.ClassVar[str] = "str_startswith"
    pat: typing.Sequence[str]

    def output_type(self, *input_types):
        return op_typing.STRING_PREDICATE.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class EndsWithOp(UnaryOp):
    name: typing.ClassVar[str] = "str_endswith"
    pat: typing.Sequence[str]

    def output_type(self, *input_types):
        return op_typing.STRING_PREDICATE.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class ZfillOp(UnaryOp):
    name: typing.ClassVar[str] = "str_zfill"
    width: int

    def output_type(self, *input_types):
        return op_typing.STRING_TRANSFORM.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class StrFindOp(UnaryOp):
    name: typing.ClassVar[str] = "str_find"
    substr: str
    start: typing.Optional[int]
    end: typing.Optional[int]

    def output_type(self, *input_types):
        signature = op_typing.FixedOutputType(
            dtypes.is_string_like, dtypes.INT_DTYPE, "string-like"
        )
        return signature.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class StrExtractOp(UnaryOp):
    name: typing.ClassVar[str] = "str_extract"
    pat: str
    n: int = 1

    def output_type(self, *input_types):
        return op_typing.STRING_TRANSFORM.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class StrSliceOp(UnaryOp):
    name: typing.ClassVar[str] = "str_slice"
    start: typing.Optional[int]
    end: typing.Optional[int]

    def output_type(self, *input_types):
        return op_typing.STRING_TRANSFORM.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class StrRepeatOp(UnaryOp):
    name: typing.ClassVar[str] = "str_repeat"
    repeats: int

    def output_type(self, *input_types):
        return op_typing.STRING_TRANSFORM.output_type(input_types[0])


# Other parameterized unary operations
@dataclasses.dataclass(frozen=True)
class StructFieldOp(UnaryOp):
    name: typing.ClassVar[str] = "struct_field"
    name_or_index: str | int

    def output_type(self, *input_types):
        input_type = input_types[0]
        if not isinstance(input_type, pd.ArrowDtype):
            raise TypeError("field accessor input must be a struct type")

        pa_type = input_type.pyarrow_dtype
        if not isinstance(pa_type, pa.StructType):
            raise TypeError("field accessor input must be a struct type")

        pa_result_type = pa_type[self.name_or_index].type
        # TODO: Directly convert from arrow to pandas type
        ibis_result_type = dtypes.arrow_dtype_to_ibis_dtype(pa_result_type)
        return dtypes.ibis_dtype_to_bigframes_dtype(ibis_result_type)


@dataclasses.dataclass(frozen=True)
class AsTypeOp(UnaryOp):
    name: typing.ClassVar[str] = "astype"
    # TODO: Convert strings to dtype earlier
    to_type: dtypes.DtypeString | dtypes.Dtype

    def output_type(self, *input_types):
        # TODO: We should do this conversion earlier
        if self.to_type == pa.string():
            return dtypes.STRING_DTYPE
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
        # This property should be set to a valid Dtype by the @remote_function decorator or read_gbq_function method
        return self.func.output_dtype


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
        timezone = "UTC" if self.utc else None
        return pd.ArrowDtype(pa.timestamp("us", tz=timezone))


@dataclasses.dataclass(frozen=True)
class StrftimeOp(UnaryOp):
    name: typing.ClassVar[str] = "strftime"
    date_format: str

    def output_type(self, *input_types):
        return dtypes.STRING_DTYPE


@dataclasses.dataclass(frozen=True)
class FloorDtOp(UnaryOp):
    name: typing.ClassVar[str] = "floor_dt"
    freq: str

    def output_type(self, *input_types):
        return input_types[0]


# Binary Ops
fillna_op = create_binary_op(name="fillna", type_signature=op_typing.COERCE)
cliplower_op = create_binary_op(name="clip_lower", type_signature=op_typing.COERCE)
clipupper_op = create_binary_op(name="clip_upper", type_signature=op_typing.COERCE)
coalesce_op = create_binary_op(name="coalesce", type_signature=op_typing.COERCE)


## Math Ops
@dataclasses.dataclass(frozen=True)
class AddOp(BinaryOp):
    name: typing.ClassVar[str] = "add"

    def output_type(self, *input_types):
        left_type = input_types[0]
        right_type = input_types[1]
        if all(map(dtypes.is_string_like, input_types)) and len(set(input_types)) == 1:
            # String addition
            return input_types[0]
        if (left_type is None or dtypes.is_numeric(left_type)) and (
            right_type is None or dtypes.is_numeric(right_type)
        ):
            # Numeric addition
            return dtypes.coerce_to_common(left_type, right_type)
        # TODO: Add temporal addition once delta types supported
        raise TypeError(f"Cannot add dtypes {left_type} and {right_type}")


@dataclasses.dataclass(frozen=True)
class SubOp(BinaryOp):
    name: typing.ClassVar[str] = "sub"

    # Note: this is actualyl a vararg op, but we don't model that yet
    def output_type(self, *input_types):
        left_type = input_types[0]
        right_type = input_types[1]
        if (left_type is None or dtypes.is_numeric(left_type)) and (
            right_type is None or dtypes.is_numeric(right_type)
        ):
            # Numeric subtraction
            return dtypes.coerce_to_common(left_type, right_type)
        # TODO: Add temporal addition once delta types supported
        raise TypeError(f"Cannot subtract dtypes {left_type} and {right_type}")


add_op = AddOp()
sub_op = SubOp()
mul_op = create_binary_op(name="mul", type_signature=op_typing.BINARY_NUMERIC)
div_op = create_binary_op(name="div", type_signature=op_typing.BINARY_REAL_NUMERIC)
floordiv_op = create_binary_op(name="floordiv", type_signature=op_typing.BINARY_NUMERIC)
pow_op = create_binary_op(name="pow", type_signature=op_typing.BINARY_NUMERIC)
mod_op = create_binary_op(name="mod", type_signature=op_typing.BINARY_NUMERIC)
arctan2_op = create_binary_op(
    name="arctan2", type_signature=op_typing.BINARY_REAL_NUMERIC
)
round_op = create_binary_op(name="round", type_signature=op_typing.BINARY_REAL_NUMERIC)
unsafe_pow_op = create_binary_op(
    name="unsafe_pow_op", type_signature=op_typing.BINARY_REAL_NUMERIC
)
# Logical Ops
and_op = create_binary_op(name="and", type_signature=op_typing.LOGICAL)
or_op = create_binary_op(name="or", type_signature=op_typing.LOGICAL)

## Comparison Ops
eq_op = create_binary_op(name="eq", type_signature=op_typing.COMPARISON)
eq_null_match_op = create_binary_op(
    name="eq_nulls_match", type_signature=op_typing.COMPARISON
)
ne_op = create_binary_op(name="ne", type_signature=op_typing.COMPARISON)
lt_op = create_binary_op(name="lt", type_signature=op_typing.COMPARISON)
gt_op = create_binary_op(name="gt", type_signature=op_typing.COMPARISON)
le_op = create_binary_op(name="le", type_signature=op_typing.COMPARISON)
ge_op = create_binary_op(name="ge", type_signature=op_typing.COMPARISON)


## String Ops
@dataclasses.dataclass(frozen=True)
class StrConcatOp(BinaryOp):
    name: typing.ClassVar[str] = "str_concat"

    # Note: this is actualyl a vararg op, but we don't model that yet
    def output_type(self, *input_types):
        if not all(map(dtypes.is_string_like, input_types)):
            raise TypeError("string concat requires string-like arguments")
        if len(set(input_types)) != 1:
            raise TypeError("string concat requires like-typed arguments")
        return input_types[0]


strconcat_op = StrConcatOp()


# Ternary Ops
@dataclasses.dataclass(frozen=True)
class WhereOp(TernaryOp):
    name: typing.ClassVar[str] = "where"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        if input_types[1] != dtypes.BOOL_DTYPE:
            raise TypeError("where condition must be a boolean")
        return dtypes.coerce_to_common(input_types[0], input_types[2])


where_op = WhereOp()


@dataclasses.dataclass(frozen=True)
class ClipOp(TernaryOp):
    name: typing.ClassVar[str] = "clip"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return dtypes.coerce_to_common(
            input_types[0], dtypes.coerce_to_common(input_types[1], input_types[2])
        )


clip_op = ClipOp()

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
    np.floor: floor_op,
    np.ceil: ceil_op,
    np.log1p: log1p_op,
    np.expm1: expm1_op,
}


NUMPY_TO_BINOP: typing.Final = {
    np.add: add_op,
    np.subtract: sub_op,
    np.multiply: mul_op,
    np.divide: div_op,
    np.power: pow_op,
    np.arctan2: arctan2_op,
}
