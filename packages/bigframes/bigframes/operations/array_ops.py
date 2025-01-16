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
class ArrayToStringOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "array_to_string"
    delimiter: str

    def output_type(self, *input_types):
        input_type = input_types[0]
        if not dtypes.is_array_string_like(input_type):
            raise TypeError("Input type must be an array of string type.")
        return dtypes.STRING_DTYPE


@dataclasses.dataclass(frozen=True)
class ArrayIndexOp(base_ops.UnaryOp):
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
class ArraySliceOp(base_ops.UnaryOp):
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
