# Copyright 2022 Google LLC
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

import libcst

from gapic.configurable_snippetgen import snippet_config_language_pb2


def empty_module() -> libcst.Module:
    return libcst.Module(body=[])


def base_function_def(function_name: str, is_sync: bool) -> libcst.FunctionDef:
    """Returns a FunctionDef node with a placeholder docstring."""
    params = libcst.Parameters(params=[])
    body = libcst.IndentedBlock(body=[libcst.parse_statement('""')])
    asynchronous = None if is_sync else libcst.Asynchronous()
    function_def = libcst.FunctionDef(
        name=libcst.Name(value=function_name),
        params=params,
        body=body,
        asynchronous=asynchronous,
    )

    return function_def
