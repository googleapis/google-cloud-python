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

from bigframes.functions import udf_def
from bigframes.operations import base_ops


@dataclasses.dataclass(frozen=True)
class PythonUdfOp(base_ops.NaryOp):
    name: typing.ClassVar[str] = "python_udf"
    function_def: udf_def.PythonUdf

    @property
    def expensive(self) -> bool:
        return True

    def output_type(self, *input_types):
        return self.function_def.signature.output.bf_type


@dataclasses.dataclass(frozen=True)
class RemoteFunctionOp(base_ops.NaryOp):
    name: typing.ClassVar[str] = "remote_function"
    function_def: udf_def.BigqueryUdf

    @property
    def expensive(self) -> bool:
        return True

    def output_type(self, *input_types):
        return self.function_def.signature.output.bf_type
