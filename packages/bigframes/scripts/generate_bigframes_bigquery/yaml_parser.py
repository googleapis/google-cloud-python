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

import constants
import data_models
import yaml


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


def _parse_bq_func(func_data: Any) -> data_models.BQFunc:
    return data_models.BQFunc(
        name=func_data["name"],
        description=func_data["description"],
        impls=[_parse_func_impl(impl) for impl in func_data["impls"]],
    )


def parse_yaml(yaml_file: pathlib.Path) -> data_models.BQModule:
    print(f"Parsing {yaml_file}...")

    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)

    functions = []
    if isinstance(data, dict) and "scalar_functions" in data:
        functions = [
            _parse_bq_func(func_data) for func_data in data["scalar_functions"]
        ]

    return data_models.BQModule(
        module_path=yaml_file.relative_to(constants.DATA_DIR).with_suffix(""),
        functions=functions,
    )
