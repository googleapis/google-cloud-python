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

from bigframes import dtypes
from bigframes.operations import base_ops


@dataclasses.dataclass(frozen=True)
class ToTimedeltaOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "to_timedelta"
    unit: typing.Literal["us", "ms", "s", "m", "h", "d", "W"]

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        if input_types[0] in (
            dtypes.INT_DTYPE,
            dtypes.FLOAT_DTYPE,
            dtypes.TIMEDELTA_DTYPE,
        ):
            return dtypes.TIMEDELTA_DTYPE
        raise TypeError("expected integer or float input")


@dataclasses.dataclass(frozen=True)
class TimedeltaFloorOp(base_ops.UnaryOp):
    """Floors the numeric value to the nearest integer and use it to represent a timedelta.

    This operator is only meant to be used during expression tree rewrites. Do not use it anywhere else!
    """

    name: typing.ClassVar[str] = "timedelta_floor"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        input_type = input_types[0]
        if dtypes.is_numeric(input_type) or input_type == dtypes.TIMEDELTA_DTYPE:
            return dtypes.TIMEDELTA_DTYPE
        raise TypeError(f"unsupported type: {input_type}")


timedelta_floor_op = TimedeltaFloorOp()


@dataclasses.dataclass(frozen=True)
class TimestampAddOp(base_ops.BinaryOp):
    name: typing.ClassVar[str] = "timestamp_add"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        # timestamp + timedelta => timestamp
        if (
            dtypes.is_datetime_like(input_types[0])
            and input_types[1] == dtypes.TIMEDELTA_DTYPE
        ):
            return input_types[0]
        # timedelta + timestamp => timestamp
        if input_types[0] == dtypes.TIMEDELTA_DTYPE and dtypes.is_datetime_like(
            input_types[1]
        ):
            return input_types[1]

        raise TypeError(
            f"unsupported types for timestamp_add. left: {input_types[0]} right: {input_types[1]}"
        )


timestamp_add_op = TimestampAddOp()


@dataclasses.dataclass(frozen=True)
class TimestampSubOp(base_ops.BinaryOp):
    name: typing.ClassVar[str] = "timestamp_sub"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        # timestamp - timedelta => timestamp
        if (
            dtypes.is_datetime_like(input_types[0])
            and input_types[1] == dtypes.TIMEDELTA_DTYPE
        ):
            return input_types[0]

        raise TypeError(
            f"unsupported types for timestamp_sub. left: {input_types[0]} right: {input_types[1]}"
        )


timestamp_sub_op = TimestampSubOp()


@dataclasses.dataclass(frozen=True)
class DateAddOp(base_ops.BinaryOp):
    name: typing.ClassVar[str] = "date_add"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        # date + timedelta => timestamp without timezone
        if (
            input_types[0] == dtypes.DATE_DTYPE
            and input_types[1] == dtypes.TIMEDELTA_DTYPE
        ):
            return dtypes.DATETIME_DTYPE
        # timedelta + date => timestamp without timezone
        if (
            input_types[0] == dtypes.TIMEDELTA_DTYPE
            and input_types[1] == dtypes.DATE_DTYPE
        ):
            return dtypes.DATETIME_DTYPE

        raise TypeError(
            f"unsupported types for date_add. left: {input_types[0]} right: {input_types[1]}"
        )


date_add_op = DateAddOp()


@dataclasses.dataclass(frozen=True)
class DateSubOp(base_ops.BinaryOp):
    name: typing.ClassVar[str] = "date_sub"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        # date - timedelta => timestamp without timezone
        if (
            input_types[0] == dtypes.DATE_DTYPE
            and input_types[1] == dtypes.TIMEDELTA_DTYPE
        ):
            return dtypes.DATETIME_DTYPE

        raise TypeError(
            f"unsupported types for date_sub. left: {input_types[0]} right: {input_types[1]}"
        )


date_sub_op = DateSubOp()
