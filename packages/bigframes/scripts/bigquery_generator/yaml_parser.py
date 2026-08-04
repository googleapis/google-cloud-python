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


import pathlib
from typing import Any

import yaml

from . import data_models


def _build_func_arg_ir(arg_data: Any) -> data_models.BQFuncArg:
    return data_models.BQFuncArg(
        name=arg_data["name"],
        value=arg_data["value"],
        optional=arg_data["optional"],
        keyword_only=arg_data["keyword_only"],
    )


def _build_func_impl_ir(impl_data: Any) -> data_models.BQFuncImpl:
    return data_models.BQFuncImpl(
        args=tuple(_build_func_arg_ir(arg) for arg in impl_data["args"]),
        return_type=impl_data["return"],
    )


def _build_func_ir(func_data: Any) -> data_models.BQFunc:
    return data_models.BQFunc(
        name=func_data["name"],
        description=func_data["description"],
        impls=tuple(_build_func_impl_ir(impl) for impl in func_data["impls"]),
        series_accessor_arg=func_data.get("series_accessor_arg", None),
    )


def parse_yaml(yaml_file: pathlib.Path) -> data_models.BQModule:
    print(f"Parsing {yaml_file}...")

    with open(yaml_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    functions: tuple[data_models.BQFunc, ...] = ()
    if isinstance(data, dict) and "scalar_functions" in data:
        functions = tuple(
            _build_func_ir(func_data) for func_data in data["scalar_functions"]
        )

    return data_models.BQModule(
        yaml_file=yaml_file,
        functions=functions,
    )
