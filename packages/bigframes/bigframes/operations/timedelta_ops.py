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
        if input_types[0] in (dtypes.INT_DTYPE, dtypes.FLOAT_DTYPE):
            return dtypes.TIMEDELTA_DTYPE
        raise TypeError("expected integer or float input")


@dataclasses.dataclass(frozen=True)
class TimestampAdd(base_ops.BinaryOp):
    name: typing.ClassVar[str] = "timestamp_add"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        # timestamp + timedelta => timestamp
        if (
            dtypes.is_datetime_like(input_types[0])
            and input_types[1] is dtypes.TIMEDELTA_DTYPE
        ):
            return input_types[0]
        # timedelta + timestamp => timestamp
        if input_types[0] is dtypes.TIMEDELTA_DTYPE and dtypes.is_datetime_like(
            input_types[1]
        ):
            return input_types[1]

        raise TypeError(
            f"unsupported types for timestamp_add. left: {input_types[0]} right: {input_types[1]}"
        )


timestamp_add_op = TimestampAdd()


@dataclasses.dataclass(frozen=True)
class TimestampSub(base_ops.BinaryOp):
    name: typing.ClassVar[str] = "timestamp_sub"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        # timestamp - timedelta => timestamp
        if (
            dtypes.is_datetime_like(input_types[0])
            and input_types[1] is dtypes.TIMEDELTA_DTYPE
        ):
            return input_types[0]

        raise TypeError(
            f"unsupported types for timestamp_sub. left: {input_types[0]} right: {input_types[1]}"
        )


timestamp_sub_op = TimestampSub()
