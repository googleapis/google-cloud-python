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
import datetime
import functools
import typing
from typing import Union

import numpy as np
import pandas as pd
from pandas.tseries.offsets import DateOffset
import pyarrow as pa

import bigframes.dtypes
import bigframes.dtypes as dtypes
import bigframes.operations.type as op_typing

if typing.TYPE_CHECKING:
    # Avoids circular dependency
    import bigframes.core.expression


class RowOp(typing.Protocol):
    @property
    def name(self) -> str:
        ...

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        ...

    @property
    def order_preserving(self) -> bool:
        """Whether the row operation preserves total ordering. Can be pruned from ordering expressions."""
        ...


@dataclasses.dataclass(frozen=True)
class ScalarOp:
    @property
    def name(self) -> str:
        raise NotImplementedError("RowOp abstract base class has no implementation")

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        raise NotImplementedError("Abstract operation has no output type")

    @property
    def order_preserving(self) -> bool:
        """Whether the row operation preserves total ordering. Can be pruned from ordering expressions."""
        return False


@dataclasses.dataclass(frozen=True)
class NaryOp(ScalarOp):
    def as_expr(
        self,
        *exprs: Union[str | bigframes.core.expression.Expression],
    ) -> bigframes.core.expression.Expression:
        import bigframes.core.expression

        # Keep this in sync with output_type and compilers
        inputs: list[bigframes.core.expression.Expression] = []

        for expr in exprs:
            inputs.append(_convert_expr_input(expr))

        return bigframes.core.expression.OpExpression(
            self,
            tuple(inputs),
        )


# These classes can be used to create simple ops that don't take local parameters
# All is needed is a unique name, and to register an implementation in ibis_mappings.py
@dataclasses.dataclass(frozen=True)
class UnaryOp(ScalarOp):
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
class BinaryOp(ScalarOp):
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
class TernaryOp(ScalarOp):
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
    """Allows creating column references with just a string"""
    import bigframes.core.expression

    if isinstance(input, str):
        return bigframes.core.expression.deref(input)
    else:
        return input


# Operation Factories
def create_unary_op(name: str, type_signature: op_typing.UnaryTypeSignature) -> UnaryOp:
    return dataclasses.make_dataclass(
        name,
        [
            ("name", typing.ClassVar[str], name),
            ("output_type", typing.ClassVar[typing.Callable], type_signature.as_method),
        ],
        bases=(UnaryOp,),
        frozen=True,
    )()


def create_binary_op(
    name: str, type_signature: op_typing.BinaryTypeSignature
) -> BinaryOp:
    return dataclasses.make_dataclass(
        name,
        [
            ("name", typing.ClassVar[str], name),
            ("output_type", typing.ClassVar[typing.Callable], type_signature.as_method),
        ],
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
)
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
pos_op = create_unary_op(name="pos", type_signature=op_typing.UNARY_NUMERIC)
neg_op = create_unary_op(name="neg", type_signature=op_typing.UNARY_NUMERIC)
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
class StringSplitOp(UnaryOp):
    name: typing.ClassVar[str] = "str_split"
    pat: typing.Sequence[str]

    def output_type(self, *input_types):
        input_type = input_types[0]
        if not isinstance(input_type, pd.StringDtype):
            raise TypeError("field accessor input must be a string type")
        arrow_type = dtypes.bigframes_dtype_to_arrow_dtype(input_type)
        return pd.ArrowDtype(pa.list_(arrow_type))


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
        return dtypes.arrow_dtype_to_bigframes_dtype(pa_result_type)


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
            return dtypes.BIGFRAMES_STRING_TO_BIGFRAMES[
                typing.cast(dtypes.DtypeString, self.to_type)
            ]
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
        if hasattr(self.func, "output_dtype"):
            return self.func.output_dtype
        else:
            raise AttributeError("output_dtype not defined")


@dataclasses.dataclass(frozen=True)
class MapOp(UnaryOp):
    name = "map_values"
    mappings: typing.Tuple[typing.Tuple[typing.Hashable, typing.Hashable], ...]

    def output_type(self, *input_types):
        return input_types[0]


@dataclasses.dataclass(frozen=True)
class ToDatetimeOp(UnaryOp):
    name: typing.ClassVar[str] = "to_datetime"
    format: typing.Optional[str] = None
    unit: typing.Optional[str] = None

    def output_type(self, *input_types):
        if input_types[0] not in (
            bigframes.dtypes.FLOAT_DTYPE,
            bigframes.dtypes.INT_DTYPE,
            bigframes.dtypes.STRING_DTYPE,
        ):
            raise TypeError("expected string or numeric input")
        return pd.ArrowDtype(pa.timestamp("us", tz=None))


@dataclasses.dataclass(frozen=True)
class ToTimestampOp(UnaryOp):
    name: typing.ClassVar[str] = "to_timestamp"
    format: typing.Optional[str] = None
    unit: typing.Optional[str] = None

    def output_type(self, *input_types):
        # Must be numeric or string
        if input_types[0] not in (
            bigframes.dtypes.FLOAT_DTYPE,
            bigframes.dtypes.INT_DTYPE,
            bigframes.dtypes.STRING_DTYPE,
        ):
            raise TypeError("expected string or numeric input")
        return pd.ArrowDtype(pa.timestamp("us", tz="UTC"))


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


@dataclasses.dataclass(frozen=True)
class DatetimeToIntegerLabelOp(BinaryOp):
    name: typing.ClassVar[str] = "datetime_to_integer_label"
    freq: DateOffset
    closed: typing.Optional[typing.Literal["right", "left"]]
    origin: Union[
        Union[pd.Timestamp, datetime.datetime, np.datetime64, int, float, str],
        typing.Literal["epoch", "start", "start_day", "end", "end_day"],
    ]

    def output_type(self, *input_types):
        return dtypes.INT_DTYPE


@dataclasses.dataclass(frozen=True)
class IntegerLabelToDatetimeOp(BinaryOp):
    name: typing.ClassVar[str] = "integer_label_to_datetime"
    freq: DateOffset
    label: typing.Optional[typing.Literal["right", "left"]]
    origin: Union[
        Union[pd.Timestamp, datetime.datetime, np.datetime64, int, float, str],
        typing.Literal["epoch", "start", "start_day", "end", "end_day"],
    ]

    def output_type(self, *input_types):
        return input_types[1]


## Array Ops
@dataclasses.dataclass(frozen=True)
class ArrayToStringOp(UnaryOp):
    name: typing.ClassVar[str] = "array_to_string"
    delimiter: str

    def output_type(self, *input_types):
        input_type = input_types[0]
        if not dtypes.is_array_string_like(input_type):
            raise TypeError("Input type must be an array of string type.")
        return dtypes.STRING_DTYPE


@dataclasses.dataclass(frozen=True)
class ArrayIndexOp(UnaryOp):
    name: typing.ClassVar[str] = "array_index"
    index: int

    def output_type(self, *input_types):
        input_type = input_types[0]
        if dtypes.is_string_like(input_type):
            return dtypes.STRING_DTYPE
        elif dtypes.is_array_like(input_type):
            return dtypes.arrow_dtype_to_bigframes_dtype(
                input_type.pyarrow_dtype.value_type
            )
        else:
            raise TypeError("Input type must be an array or string-like type.")


@dataclasses.dataclass(frozen=True)
class ArraySliceOp(UnaryOp):
    name: typing.ClassVar[str] = "array_slice"
    start: int
    stop: typing.Optional[int] = None
    step: typing.Optional[int] = None

    def output_type(self, *input_types):
        input_type = input_types[0]
        if dtypes.is_string_like(input_type):
            return dtypes.STRING_DTYPE
        elif dtypes.is_array_like(input_type):
            return input_type
        else:
            raise TypeError("Input type must be an array or string-like type.")


## JSON Ops
@dataclasses.dataclass(frozen=True)
class JSONExtract(UnaryOp):
    name: typing.ClassVar[str] = "json_extract"
    json_path: str

    def output_type(self, *input_types):
        input_type = input_types[0]
        if not dtypes.is_json_like(input_type):
            raise TypeError(
                "Input type must be an valid JSON object or JSON-formatted string type."
                + f" Received type: {input_type}"
            )
        return input_type


@dataclasses.dataclass(frozen=True)
class JSONExtractArray(UnaryOp):
    name: typing.ClassVar[str] = "json_extract_array"
    json_path: str

    def output_type(self, *input_types):
        input_type = input_types[0]
        if not dtypes.is_json_like(input_type):
            raise TypeError(
                "Input type must be an valid JSON object or JSON-formatted string type."
                + f" Received type: {input_type}"
            )
        return pd.ArrowDtype(
            pa.list_(dtypes.bigframes_dtype_to_arrow_dtype(dtypes.STRING_DTYPE))
        )


# Binary Ops
fillna_op = create_binary_op(name="fillna", type_signature=op_typing.COERCE)
maximum_op = create_binary_op(name="maximum", type_signature=op_typing.COERCE)
minimum_op = create_binary_op(name="minimum", type_signature=op_typing.COERCE)
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


@dataclasses.dataclass(frozen=True)
class BinaryRemoteFunctionOp(BinaryOp):
    name: typing.ClassVar[str] = "binary_remote_function"
    func: typing.Callable

    def output_type(self, *input_types):
        # This property should be set to a valid Dtype by the @remote_function decorator or read_gbq_function method
        if hasattr(self.func, "output_dtype"):
            return self.func.output_dtype
        else:
            raise AttributeError("output_dtype not defined")


@dataclasses.dataclass(frozen=True)
class NaryRemoteFunctionOp(NaryOp):
    name: typing.ClassVar[str] = "nary_remote_function"
    func: typing.Callable

    def output_type(self, *input_types):
        # This property should be set to a valid Dtype by the @remote_function decorator or read_gbq_function method
        if hasattr(self.func, "output_dtype"):
            return self.func.output_dtype
        else:
            raise AttributeError("output_dtype not defined")


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
xor_op = create_binary_op(name="xor", type_signature=op_typing.LOGICAL)

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


cosine_distance_op = create_binary_op(
    name="ml_cosine_distance", type_signature=op_typing.VECTOR_METRIC
)
manhattan_distance_op = create_binary_op(
    name="ml_manhattan_distance", type_signature=op_typing.VECTOR_METRIC
)
euclidean_distance_op = create_binary_op(
    name="ml_euclidean_distance", type_signature=op_typing.VECTOR_METRIC
)


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


## JSON Ops
@dataclasses.dataclass(frozen=True)
class JSONSet(BinaryOp):
    name: typing.ClassVar[str] = "json_set"
    json_path: str

    def output_type(self, *input_types):
        left_type = input_types[0]
        right_type = input_types[1]
        if not dtypes.is_json_like(left_type):
            raise TypeError(
                "Input type must be an valid JSON object or JSON-formatted string type."
                + f" Received type: {left_type}"
            )
        if not dtypes.is_json_encoding_type(right_type):
            raise TypeError(
                "The value to be assigned must be a type that can be encoded as JSON."
                + f"Received type: {right_type}"
            )

        # After JSON type implementation, ONLY return JSON data.
        return left_type


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


class CaseWhenOp(NaryOp):
    name: typing.ClassVar[str] = "switch"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        assert len(input_types) % 2 == 0
        # predicate1, output1, predicate2, output2...
        if not all(map(lambda x: x == dtypes.BOOL_DTYPE, input_types[::2])):
            raise TypeError(f"Case inputs {input_types[::2]} must be boolean-valued")
        output_expr_types = input_types[1::2]
        return functools.reduce(
            lambda t1, t2: dtypes.coerce_to_common(t1, t2),
            output_expr_types,
        )


case_when_op = CaseWhenOp()


@dataclasses.dataclass(frozen=True)
class StructOp(NaryOp):
    name: typing.ClassVar[str] = "struct"
    column_names: tuple[str]

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        num_input_types = len(input_types)
        # value1, value2, ...
        assert num_input_types == len(self.column_names)
        fields = []

        for i in range(num_input_types):
            arrow_type = dtypes.bigframes_dtype_to_arrow_dtype(input_types[i])
            fields.append(
                pa.field(
                    self.column_names[i],
                    arrow_type,
                    nullable=(not pa.types.is_list(arrow_type)),
                )
            )
        return pd.ArrowDtype(
            pa.struct(fields)
        )  # [(name1, value1), (name2, value2), ...]


# Just parameterless unary ops for now
# TODO: Parameter mappings
NUMPY_TO_OP: dict[np.ufunc, UnaryOp] = {
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


NUMPY_TO_BINOP: dict[np.ufunc, BinaryOp] = {
    np.add: add_op,
    np.subtract: sub_op,
    np.multiply: mul_op,
    np.divide: div_op,
    np.power: pow_op,
    np.arctan2: arctan2_op,
    np.maximum: maximum_op,
    np.minimum: minimum_op,
}
