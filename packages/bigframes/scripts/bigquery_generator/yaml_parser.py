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
import re
from typing import Any

from . import constants
from . import data_models
import yaml


def _to_snake_case(name: str) -> str:
    # Replace dots with underscores
    name = name.replace(".", "_")
    # Handle CamelCase to snake_case
    name = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    # Replace multiple underscores with one
    name = re.sub(r"_+", "_", name)
    return name


def _parse_func_arg(arg_data: Any) -> data_models.BQFuncArg:
    return data_models.BQFuncArg(
        name=arg_data["name"],
        value=arg_data["value"],
        optional=arg_data["optional"],
        keyword_only=arg_data["keyword_only"],
    )


def _parse_func_impl(impl_data: Any) -> data_models.BQFuncImpl:
    return data_models.BQFuncImpl(
        args=[_parse_func_arg(arg) for arg in impl_data["args"]],
        return_type=impl_data["return"],
    )


def _parse_bq_func(
    func_data: Any, module_name: str, is_global: bool
) -> data_models.BQFunc:
    op_base_name = _to_snake_case(func_data["name"])

    if not is_global and op_base_name.startswith(module_name + "_"):
        op_base_name = op_base_name[len(module_name) + 1 :]

    return data_models.BQFunc(
        name=func_data["name"],
        op_base_name=op_base_name,
        description=func_data["description"],
        impls=[_parse_func_impl(impl) for impl in func_data["impls"]],
        series_accessor_arg=func_data.get("series_accessor_arg", None),
    )


def parse_yaml(yaml_file: pathlib.Path) -> data_models.BQModule:
    print(f"Parsing {yaml_file}...")

    with open(yaml_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    functions = []
    module_path = yaml_file.relative_to(constants.DATA_DIR).with_suffix("")
    is_global = "global_namespace" in module_path.parts
    if isinstance(data, dict) and "scalar_functions" in data:
        functions = [
            _parse_bq_func(func_data, module_path.name, is_global)
            for func_data in data["scalar_functions"]
        ]

    return data_models.BQModule(
        yaml_file=yaml_file,
        functions=functions,
    )
