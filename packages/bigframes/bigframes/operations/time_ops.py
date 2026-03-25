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

from bigframes import dtypes
from bigframes.operations import base_ops
import bigframes.operations.type as op_typing

HourOp = base_ops.create_unary_op(
    name="hour",
    type_signature=op_typing.TIMELIKE_ACCESSOR,
)
hour_op = HourOp()

MinuteOp = base_ops.create_unary_op(
    name="minute",
    type_signature=op_typing.TIMELIKE_ACCESSOR,
)
minute_op = MinuteOp()

SecondOp = base_ops.create_unary_op(
    name="second",
    type_signature=op_typing.TIMELIKE_ACCESSOR,
)
second_op = SecondOp()

NormalizeOp = base_ops.create_unary_op(
    name="normalize",
    type_signature=op_typing.TypePreserving(
        dtypes.is_time_like,
        description="time-like",
    ),
)
normalize_op = NormalizeOp()
