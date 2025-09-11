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
import functools
import typing

from bigframes import dtypes
from bigframes.operations import base_ops
import bigframes.operations.type as op_typing

InvertOp = base_ops.create_unary_op(
    name="invert",
    type_signature=op_typing.TypePreserving(
        dtypes.is_binary_like,
        description="binary-like",
    ),
)
invert_op = InvertOp()

IsNullOp = base_ops.create_unary_op(
    name="isnull",
    type_signature=op_typing.FixedOutputType(
        lambda x: True, dtypes.BOOL_DTYPE, description="nullable"
    ),
)
isnull_op = IsNullOp()

NotNullOp = base_ops.create_unary_op(
    name="notnull",
    type_signature=op_typing.FixedOutputType(
        lambda x: True, dtypes.BOOL_DTYPE, description="nullable"
    ),
)
notnull_op = NotNullOp()

HashOp = base_ops.create_unary_op(
    name="hash",
    type_signature=op_typing.FixedOutputType(
        dtypes.is_string_like, dtypes.INT_DTYPE, description="string-like"
    ),
)
hash_op = HashOp()

# source, dest type
_VALID_CASTS = set(
    (
        # INT casts
        (
            dtypes.BOOL_DTYPE,
            dtypes.INT_DTYPE,
        ),
        (
            dtypes.FLOAT_DTYPE,
            dtypes.INT_DTYPE,
        ),
        (
            dtypes.NUMERIC_DTYPE,
            dtypes.INT_DTYPE,
        ),
        (
            dtypes.BIGNUMERIC_DTYPE,
            dtypes.INT_DTYPE,
        ),
        (
            dtypes.TIME_DTYPE,
            dtypes.INT_DTYPE,
        ),
        (
            dtypes.DATETIME_DTYPE,
            dtypes.INT_DTYPE,
        ),
        (
            dtypes.TIMESTAMP_DTYPE,
            dtypes.INT_DTYPE,
        ),
        (
            dtypes.TIMEDELTA_DTYPE,
            dtypes.INT_DTYPE,
        ),
        (
            dtypes.STRING_DTYPE,
            dtypes.INT_DTYPE,
        ),
        (
            dtypes.JSON_DTYPE,
            dtypes.INT_DTYPE,
        ),
        # Float casts
        (
            dtypes.BOOL_DTYPE,
            dtypes.FLOAT_DTYPE,
        ),
        (
            dtypes.NUMERIC_DTYPE,
            dtypes.FLOAT_DTYPE,
        ),
        (
            dtypes.BIGNUMERIC_DTYPE,
            dtypes.FLOAT_DTYPE,
        ),
        (
            dtypes.INT_DTYPE,
            dtypes.FLOAT_DTYPE,
        ),
        (
            dtypes.STRING_DTYPE,
            dtypes.FLOAT_DTYPE,
        ),
        (
            dtypes.JSON_DTYPE,
            dtypes.FLOAT_DTYPE,
        ),
        # Bool casts
        (
            dtypes.INT_DTYPE,
            dtypes.BOOL_DTYPE,
        ),
        (
            dtypes.FLOAT_DTYPE,
            dtypes.BOOL_DTYPE,
        ),
        (
            dtypes.JSON_DTYPE,
            dtypes.BOOL_DTYPE,
        ),
        # String casts
        (
            dtypes.BYTES_DTYPE,
            dtypes.STRING_DTYPE,
        ),
        (
            dtypes.BOOL_DTYPE,
            dtypes.STRING_DTYPE,
        ),
        (
            dtypes.FLOAT_DTYPE,
            dtypes.STRING_DTYPE,
        ),
        (
            dtypes.TIME_DTYPE,
            dtypes.STRING_DTYPE,
        ),
        (
            dtypes.INT_DTYPE,
            dtypes.STRING_DTYPE,
        ),
        (
            dtypes.DATETIME_DTYPE,
            dtypes.STRING_DTYPE,
        ),
        (
            dtypes.TIMESTAMP_DTYPE,
            dtypes.STRING_DTYPE,
        ),
        (
            dtypes.DATE_DTYPE,
            dtypes.STRING_DTYPE,
        ),
        (
            dtypes.JSON_DTYPE,
            dtypes.STRING_DTYPE,
        ),
        # bytes casts
        (
            dtypes.STRING_DTYPE,
            dtypes.BYTES_DTYPE,
        ),
        # decimal casts
        (
            dtypes.STRING_DTYPE,
            dtypes.NUMERIC_DTYPE,
        ),
        (
            dtypes.INT_DTYPE,
            dtypes.NUMERIC_DTYPE,
        ),
        (
            dtypes.FLOAT_DTYPE,
            dtypes.NUMERIC_DTYPE,
        ),
        (
            dtypes.BIGNUMERIC_DTYPE,
            dtypes.NUMERIC_DTYPE,
        ),
        # big decimal casts
        (
            dtypes.STRING_DTYPE,
            dtypes.BIGNUMERIC_DTYPE,
        ),
        (
            dtypes.INT_DTYPE,
            dtypes.BIGNUMERIC_DTYPE,
        ),
        (
            dtypes.FLOAT_DTYPE,
            dtypes.BIGNUMERIC_DTYPE,
        ),
        (
            dtypes.NUMERIC_DTYPE,
            dtypes.BIGNUMERIC_DTYPE,
        ),
        # time casts
        (
            dtypes.INT_DTYPE,
            dtypes.TIME_DTYPE,
        ),
        (
            dtypes.DATETIME_DTYPE,
            dtypes.TIME_DTYPE,
        ),
        (
            dtypes.TIMESTAMP_DTYPE,
            dtypes.TIME_DTYPE,
        ),
        # date casts
        (
            dtypes.STRING_DTYPE,
            dtypes.DATE_DTYPE,
        ),
        (
            dtypes.DATETIME_DTYPE,
            dtypes.DATE_DTYPE,
        ),
        (
            dtypes.TIMESTAMP_DTYPE,
            dtypes.DATE_DTYPE,
        ),
        # datetime casts
        (
            dtypes.DATE_DTYPE,
            dtypes.DATETIME_DTYPE,
        ),
        (
            dtypes.STRING_DTYPE,
            dtypes.DATETIME_DTYPE,
        ),
        (
            dtypes.TIMESTAMP_DTYPE,
            dtypes.DATETIME_DTYPE,
        ),
        (
            dtypes.INT_DTYPE,
            dtypes.DATETIME_DTYPE,
        ),
        # timestamp casts
        (
            dtypes.DATE_DTYPE,
            dtypes.TIMESTAMP_DTYPE,
        ),
        (
            dtypes.STRING_DTYPE,
            dtypes.TIMESTAMP_DTYPE,
        ),
        (
            dtypes.DATETIME_DTYPE,
            dtypes.TIMESTAMP_DTYPE,
        ),
        (
            dtypes.INT_DTYPE,
            dtypes.TIMESTAMP_DTYPE,
        ),
        # timedelta casts
        (
            dtypes.INT_DTYPE,
            dtypes.TIMEDELTA_DTYPE,
        ),
        # json casts
        (
            dtypes.BOOL_DTYPE,
            dtypes.JSON_DTYPE,
        ),
        (
            dtypes.FLOAT_DTYPE,
            dtypes.JSON_DTYPE,
        ),
        (
            dtypes.STRING_DTYPE,
            dtypes.JSON_DTYPE,
        ),
        (
            dtypes.INT_DTYPE,
            dtypes.JSON_DTYPE,
        ),
    )
)


def _valid_scalar_cast(src: dtypes.Dtype, dst: dtypes.Dtype):
    if src == dst:
        return True
    elif (src, dst) in _VALID_CASTS:
        return True
    return False


def _valid_cast(src: dtypes.Dtype, dst: dtypes.Dtype):
    if src == dst:
        return True
    # TODO: Might need to be more strict within list/array context
    if dtypes.is_array_like(src) and dtypes.is_array_like(dst):
        src_inner = dtypes.get_array_inner_type(src)
        dst_inner = dtypes.get_array_inner_type(dst)
        return _valid_cast(src_inner, dst_inner)
    if dtypes.is_struct_like(src) and dtypes.is_struct_like(dst):
        src_fields = dtypes.get_struct_fields(src)
        dst_fields = dtypes.get_struct_fields(dst)
        if len(src_fields) != len(dst_fields):
            return False
        for (_, src_dtype), (_, dst_dtype) in zip(
            src_fields.items(), dst_fields.items()
        ):
            if not _valid_cast(src_dtype, dst_dtype):
                return False
        return True

    return _valid_scalar_cast(src, dst)


@dataclasses.dataclass(frozen=True)
class AsTypeOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "astype"
    # TODO: Convert strings to dtype earlier
    to_type: dtypes.Dtype
    safe: bool = False

    def output_type(self, *input_types):
        if not _valid_cast(input_types[0], self.to_type):
            raise TypeError(f"Cannot cast {input_types[0]} to {self.to_type}")

        return self.to_type


@dataclasses.dataclass(frozen=True)
class IsInOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "is_in"
    values: typing.Tuple
    match_nulls: bool = True

    def output_type(self, *input_types):
        return dtypes.BOOL_DTYPE


@dataclasses.dataclass(frozen=True)
class MapOp(base_ops.UnaryOp):
    name = "map_values"
    mappings: typing.Tuple[typing.Tuple[typing.Hashable, typing.Hashable], ...]

    def output_type(self, *input_types):
        return input_types[0]


FillNaOp = base_ops.create_binary_op(name="fillna", type_signature=op_typing.COERCE)
fillna_op = FillNaOp()

MaximumOp = base_ops.create_binary_op(name="maximum", type_signature=op_typing.COERCE)
maximum_op = MaximumOp()

MinimumOp = base_ops.create_binary_op(name="minimum", type_signature=op_typing.COERCE)
minimum_op = MinimumOp()

CoalesceOp = base_ops.create_binary_op(name="coalesce", type_signature=op_typing.COERCE)
coalesce_op = CoalesceOp()


@dataclasses.dataclass(frozen=True)
class WhereOp(base_ops.TernaryOp):
    name: typing.ClassVar[str] = "where"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        if input_types[1] != dtypes.BOOL_DTYPE:
            raise TypeError("where condition must be a boolean")
        return dtypes.coerce_to_common(input_types[0], input_types[2])


where_op = WhereOp()


@dataclasses.dataclass(frozen=True)
class ClipOp(base_ops.TernaryOp):
    name: typing.ClassVar[str] = "clip"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return dtypes.coerce_to_common(
            input_types[0], dtypes.coerce_to_common(input_types[1], input_types[2])
        )


clip_op = ClipOp()


class CaseWhenOp(base_ops.NaryOp):
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


# Really doesn't need to be its own op, but allows us to try to get the most compact representation
@dataclasses.dataclass(frozen=True)
class RowKey(base_ops.NaryOp):
    name: typing.ClassVar[str] = "rowkey"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return dtypes.STRING_DTYPE

    @property
    def is_bijective(self) -> bool:
        """Whether the operation has a 1:1 mapping between inputs and outputs"""
        return True

    @property
    def deterministic(self) -> bool:
        return False


@dataclasses.dataclass(frozen=True)
class SqlScalarOp(base_ops.NaryOp):
    """An escape to SQL, representing a single column."""

    name: typing.ClassVar[str] = "sql_scalar"
    _output_type: dtypes.ExpressionType
    sql_template: str

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return self._output_type


@dataclasses.dataclass(frozen=True)
class PyUdfOp(base_ops.NaryOp):
    """Represents a local UDF."""

    name: typing.ClassVar[str] = "py_udf"
    fn: typing.Callable
    _output_type: dtypes.ExpressionType

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return self._output_type
