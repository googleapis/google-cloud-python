# Copyright 2025 Google LLC
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

import dataclasses
import typing

import pandas as pd
import pyarrow as pa

from bigframes import dtypes
from bigframes.operations import base_ops
import bigframes.operations.type as op_typing

LenOp = base_ops.create_unary_op(
    name="len",
    type_signature=op_typing.FixedOutputType(
        dtypes.is_iterable, dtypes.INT_DTYPE, description="iterable"
    ),
)
len_op = LenOp()

ReverseOp = base_ops.create_unary_op(
    name="reverse", type_signature=op_typing.STRING_TRANSFORM
)
reverse_op = ReverseOp()

LowerOp = base_ops.create_unary_op(
    name="lower", type_signature=op_typing.STRING_TRANSFORM
)
lower_op = LowerOp()

UpperOp = base_ops.create_unary_op(
    name="upper", type_signature=op_typing.STRING_TRANSFORM
)
upper_op = UpperOp()

IsAlnumOp = base_ops.create_unary_op(
    name="isalnum", type_signature=op_typing.STRING_PREDICATE
)
isalnum_op = IsAlnumOp()

IsAlphaOp = base_ops.create_unary_op(
    name="isalpha", type_signature=op_typing.STRING_PREDICATE
)
isalpha_op = IsAlphaOp()

IsDecimalOp = base_ops.create_unary_op(
    name="isdecimal", type_signature=op_typing.STRING_PREDICATE
)
isdecimal_op = IsDecimalOp()

IsDigitOp = base_ops.create_unary_op(
    name="isdigit", type_signature=op_typing.STRING_PREDICATE
)
isdigit_op = IsDigitOp()

IsNumericOp = base_ops.create_unary_op(
    name="isnumeric", type_signature=op_typing.STRING_PREDICATE
)
isnumeric_op = IsNumericOp()

IsSpaceOp = base_ops.create_unary_op(
    name="isspace", type_signature=op_typing.STRING_PREDICATE
)
isspace_op = IsSpaceOp()

IsLowerOp = base_ops.create_unary_op(
    name="islower", type_signature=op_typing.STRING_PREDICATE
)
islower_op = IsLowerOp()

IsUpperOp = base_ops.create_unary_op(
    name="isupper", type_signature=op_typing.STRING_PREDICATE
)
isupper_op = IsUpperOp()

CapitalizeOp = base_ops.create_unary_op(
    name="capitalize", type_signature=op_typing.STRING_TRANSFORM
)
capitalize_op = CapitalizeOp()


@dataclasses.dataclass(frozen=True)
class StrContainsOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "str_contains"
    pat: str

    def output_type(self, *input_types):
        return op_typing.STRING_PREDICATE.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class StrContainsRegexOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "str_contains_regex"
    pat: str

    def output_type(self, *input_types):
        return op_typing.STRING_PREDICATE.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class StrGetOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "str_get"
    i: int

    def output_type(self, *input_types):
        return op_typing.STRING_TRANSFORM.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class StrPadOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "str_pad"
    length: int
    fillchar: str
    side: typing.Literal["both", "left", "right"]

    def output_type(self, *input_types):
        return op_typing.STRING_TRANSFORM.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class StrStripOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "str_strip"
    to_strip: str

    def output_type(self, *input_types):
        return op_typing.STRING_TRANSFORM.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class StrLstripOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "str_lstrip"
    to_strip: str

    def output_type(self, *input_types):
        return op_typing.STRING_TRANSFORM.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class StrRstripOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "str_rstrip"
    to_strip: str

    def output_type(self, *input_types):
        return op_typing.STRING_TRANSFORM.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class ReplaceStrOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "str_replace"
    pat: str
    repl: str

    def output_type(self, *input_types):
        return op_typing.STRING_TRANSFORM.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class RegexReplaceStrOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "str_rereplace"
    pat: str
    repl: str

    def output_type(self, *input_types):
        return op_typing.STRING_TRANSFORM.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class StartsWithOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "str_startswith"
    pat: typing.Sequence[str]

    def output_type(self, *input_types):
        return op_typing.STRING_PREDICATE.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class StringSplitOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "str_split"
    pat: typing.Sequence[str]

    def output_type(self, *input_types):
        input_type = input_types[0]
        if not isinstance(input_type, pd.StringDtype):
            raise TypeError("field accessor input must be a string type")
        arrow_type = dtypes.bigframes_dtype_to_arrow_dtype(input_type)
        return pd.ArrowDtype(pa.list_(arrow_type))


@dataclasses.dataclass(frozen=True)
class EndsWithOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "str_endswith"
    pat: typing.Sequence[str]

    def output_type(self, *input_types):
        return op_typing.STRING_PREDICATE.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class ZfillOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "str_zfill"
    width: int

    def output_type(self, *input_types):
        return op_typing.STRING_TRANSFORM.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class StrFindOp(base_ops.UnaryOp):
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
class StrExtractOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "str_extract"
    pat: str
    n: int = 1

    def output_type(self, *input_types):
        return op_typing.STRING_TRANSFORM.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class StrSliceOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "str_slice"
    start: typing.Optional[int]
    end: typing.Optional[int]

    def output_type(self, *input_types):
        return op_typing.STRING_TRANSFORM.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class StrRepeatOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "str_repeat"
    repeats: int

    def output_type(self, *input_types):
        return op_typing.STRING_TRANSFORM.output_type(input_types[0])


@dataclasses.dataclass(frozen=True)
class StrConcatOp(base_ops.BinaryOp):
    name: typing.ClassVar[str] = "str_concat"

    # Note: this is actualyl a vararg op, but we don't model that yet
    def output_type(self, *input_types):
        if not all(map(dtypes.is_string_like, input_types)):
            raise TypeError("string concat requires string-like arguments")
        if len(set(input_types)) != 1:
            raise TypeError("string concat requires like-typed arguments")
        return input_types[0]


strconcat_op = StrConcatOp()
