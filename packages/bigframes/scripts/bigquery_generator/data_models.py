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

from __future__ import annotations

import dataclasses
import pathlib
from typing import Any

from . import constants


@dataclasses.dataclass
class BQFuncArg:
    name: str
    value: str  # The type of the arg
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
    series_accessor_arg: str | None


@dataclasses.dataclass
class BQModule:
    yaml_file: pathlib.Path
    functions: list[BQFunc]

    @property
    def module_path(self) -> pathlib.Path:
        return self.yaml_file.relative_to(constants.DATA_DIR).with_suffix("")

    @property
    def namespace(self) -> tuple[str, ...]:
        parts = self.module_path.parts
        if "global_namespace" in parts:
            return tuple()
        return parts

    @property
    def is_global(self) -> bool:
        return "global_namespace" in self.module_path.parts


@dataclasses.dataclass
class BigFramesOp:
    internal_name: str
    sql_name: str
    arg_specs: str
    signature: str
    signature_definition: str | None


@dataclasses.dataclass
class BigFramesFuncArg:
    name: str
    types: set[str]
    optional: bool
    keyword_only: bool

    @property
    def type_hint(self) -> str:
        types = [constants.PY_TYPE_MAP.get(t, "Any") for t in sorted(self.types)] + [
            "Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]"
        ]

        if len(types) > 1:
            return "Union[" + ", ".join(sorted(set(types))) + "]"

        return types[0]

    @property
    def default(self) -> str | None:
        if self.optional:
            return "sentinels.Sentinel.ARGUMENT_DEFAULT"
        return None


@dataclasses.dataclass
class BigFramesFunc:
    name: str
    op_name: str
    description: str
    args: list[BigFramesFuncArg]
    series_accessor_arg: str | None
    import_module: str | None = None


@dataclasses.dataclass
class Accessor:
    class_name: str
    bigframes_class_name: str
    pandas_class_name: str
    is_root: bool
    description: str
    children: list[Accessor]
    functions: list[BigFramesFunc]
    prop_name: str | None = None
