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

from bigframes.operations import base_ops


@dataclasses.dataclass(frozen=True)
class RemoteFunctionOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "remote_function"
    func: typing.Callable
    apply_on_null: bool

    @property
    def expensive(self) -> bool:
        return True

    def output_type(self, *input_types):
        # The output dtype should be set to a valid Dtype by @udf decorator,
        # @remote_function decorator, or read_gbq_function method.
        if hasattr(self.func, "bigframes_bigquery_function_output_dtype"):
            return self.func.bigframes_bigquery_function_output_dtype

        raise AttributeError("bigframes_bigquery_function_output_dtype not defined")


@dataclasses.dataclass(frozen=True)
class BinaryRemoteFunctionOp(base_ops.BinaryOp):
    name: typing.ClassVar[str] = "binary_remote_function"
    func: typing.Callable

    @property
    def expensive(self) -> bool:
        return True

    def output_type(self, *input_types):
        # The output dtype should be set to a valid Dtype by @udf decorator,
        # @remote_function decorator, or read_gbq_function method.
        if hasattr(self.func, "bigframes_bigquery_function_output_dtype"):
            return self.func.bigframes_bigquery_function_output_dtype

        raise AttributeError("bigframes_bigquery_function_output_dtype not defined")


@dataclasses.dataclass(frozen=True)
class NaryRemoteFunctionOp(base_ops.NaryOp):
    name: typing.ClassVar[str] = "nary_remote_function"
    func: typing.Callable

    @property
    def expensive(self) -> bool:
        return True

    def output_type(self, *input_types):
        # The output dtype should be set to a valid Dtype by @udf decorator,
        # @remote_function decorator, or read_gbq_function method.
        if hasattr(self.func, "bigframes_bigquery_function_output_dtype"):
            return self.func.bigframes_bigquery_function_output_dtype

        raise AttributeError("bigframes_bigquery_function_output_dtype not defined")
