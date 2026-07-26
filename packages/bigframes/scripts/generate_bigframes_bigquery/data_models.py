# Copyright 2026 Google LLC
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
import pathlib
from typing import Any

import constants


@dataclasses.dataclass
class BQFuncArg:
    name: str
    value: str  # The type of the arg
    optional: bool
    keyword_only: bool


@dataclasses.dataclass
class BigFramesFuncArg:
    name: str
    types: set[str]
    optional: bool
    keyword_only: bool


@dataclasses.dataclass
class BQFuncImpl:
    args: list[BQFuncArg]
    return_type: str

    @property
    def uses_any1(self) -> bool:
        if "any1" in self.return_type:
            return True

        return any("any1" in arg.value for arg in self.args)

    def to_dict(self) -> dict[str, Any]:
        result = dataclasses.asdict(self)

        result["uses_any1"] = self.uses_any1

        # We cannot use "return" as a field name, but we need to use it
        # as a key for template rendering
        result["return"] = self.return_type
        del result["return_type"]

        return result


@dataclasses.dataclass
class BQFunc:
    name: str
    op_base_name: str
    description: str
    impls: list[BQFuncImpl]


@dataclasses.dataclass
class BQModule:
    yaml_file: pathlib.Path
    functions: list[BQFunc]

    @property
    def module_path(self):
        return self.yaml_file.relative_to(constants.DATA_DIR).with_suffix("")


@dataclasses.dataclass
class BigFramesOp:
    internal_name: str
    sql_name: str
    arg_specs: str
    signature: str
    signature_definition: str | None


@dataclasses.dataclass
class BigFramesFunc:
    name: str
    op_name: str
    description: str
    args: list[str]
    series_accessor_arg: list[str]
