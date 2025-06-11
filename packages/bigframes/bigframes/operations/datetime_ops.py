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

DateOp = base_ops.create_unary_op(
    name="date",
    type_signature=op_typing.FixedOutputType(
        dtypes.is_date_like, dtypes.DATE_DTYPE, description="date-like"
    ),
)
date_op = DateOp()

TimeOp = base_ops.create_unary_op(
    name="time",
    type_signature=op_typing.FixedOutputType(
        dtypes.is_time_like, dtypes.TIME_DTYPE, description="time-like"
    ),
)
time_op = TimeOp()


@dataclasses.dataclass(frozen=True)
class ToDatetimeOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "to_datetime"
    format: typing.Optional[str] = None
    unit: typing.Optional[str] = None

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        if input_types[0] not in (
            dtypes.FLOAT_DTYPE,
            dtypes.INT_DTYPE,
            dtypes.STRING_DTYPE,
        ):
            raise TypeError("expected string or numeric input")
        return pd.ArrowDtype(pa.timestamp("us", tz=None))


@dataclasses.dataclass(frozen=True)
class ToTimestampOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "to_timestamp"
    format: typing.Optional[str] = None
    unit: typing.Optional[str] = None

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        # Must be numeric or string
        if input_types[0] not in (
            dtypes.FLOAT_DTYPE,
            dtypes.INT_DTYPE,
            dtypes.STRING_DTYPE,
        ):
            raise TypeError("expected string or numeric input")
        return pd.ArrowDtype(pa.timestamp("us", tz="UTC"))


@dataclasses.dataclass(frozen=True)
class StrftimeOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "strftime"
    date_format: str

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return dtypes.STRING_DTYPE


@dataclasses.dataclass(frozen=True)
class UnixSeconds(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "unix_seconds"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        if input_types[0] != dtypes.TIMESTAMP_DTYPE:
            raise TypeError("expected timestamp input")
        return dtypes.INT_DTYPE


@dataclasses.dataclass(frozen=True)
class UnixMillis(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "unix_millis"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        if input_types[0] != dtypes.TIMESTAMP_DTYPE:
            raise TypeError("expected timestamp input")
        return dtypes.INT_DTYPE


@dataclasses.dataclass(frozen=True)
class UnixMicros(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "unix_micros"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        if input_types[0] != dtypes.TIMESTAMP_DTYPE:
            raise TypeError("expected timestamp input")
        return dtypes.INT_DTYPE


@dataclasses.dataclass(frozen=True)
class TimestampDiff(base_ops.BinaryOp):
    name: typing.ClassVar[str] = "timestamp_diff"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        if input_types[0] != input_types[1]:
            raise TypeError(
                f"two inputs have different types. left: {input_types[0]}, right: {input_types[1]}"
            )

        if not dtypes.is_datetime_like(input_types[0]):
            raise TypeError("expected timestamp input")

        return dtypes.TIMEDELTA_DTYPE


timestamp_diff_op = TimestampDiff()
