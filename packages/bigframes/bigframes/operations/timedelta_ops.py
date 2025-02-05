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

    def output_type(self, *input_types):
        if input_types[0] is not dtypes.INT_DTYPE:
            raise TypeError("expected integer input")
        return dtypes.TIMEDELTA_DTYPE
