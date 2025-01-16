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
class RemoteFunctionOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "remote_function"
    func: typing.Callable
    apply_on_null: bool

    def output_type(self, *input_types):
        # This property should be set to a valid Dtype by the @remote_function decorator or read_gbq_function method
        if hasattr(self.func, "output_dtype"):
            if dtypes.is_array_like(self.func.output_dtype):
                # TODO(b/284515241): remove this special handling to support
                # array output types once BQ remote functions support ARRAY.
                # Until then, use json serialized strings at the remote function
                # level, and parse that to the intended output type at the
                # bigframes level.
                return dtypes.STRING_DTYPE
            return self.func.output_dtype
        else:
            raise AttributeError("output_dtype not defined")


@dataclasses.dataclass(frozen=True)
class BinaryRemoteFunctionOp(base_ops.BinaryOp):
    name: typing.ClassVar[str] = "binary_remote_function"
    func: typing.Callable

    def output_type(self, *input_types):
        # This property should be set to a valid Dtype by the @remote_function decorator or read_gbq_function method
        if hasattr(self.func, "output_dtype"):
            if dtypes.is_array_like(self.func.output_dtype):
                # TODO(b/284515241): remove this special handling to support
                # array output types once BQ remote functions support ARRAY.
                # Until then, use json serialized strings at the remote function
                # level, and parse that to the intended output type at the
                # bigframes level.
                return dtypes.STRING_DTYPE
            return self.func.output_dtype
        else:
            raise AttributeError("output_dtype not defined")


@dataclasses.dataclass(frozen=True)
class NaryRemoteFunctionOp(base_ops.NaryOp):
    name: typing.ClassVar[str] = "nary_remote_function"
    func: typing.Callable

    def output_type(self, *input_types):
        # This property should be set to a valid Dtype by the @remote_function decorator or read_gbq_function method
        if hasattr(self.func, "output_dtype"):
            if dtypes.is_array_like(self.func.output_dtype):
                # TODO(b/284515241): remove this special handling to support
                # array output types once BQ remote functions support ARRAY.
                # Until then, use json serialized strings at the remote function
                # level, and parse that to the intended output type at the
                # bigframes level.
                return dtypes.STRING_DTYPE
            return self.func.output_dtype
        else:
            raise AttributeError("output_dtype not defined")
