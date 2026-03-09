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

import collections.abc
import json
from typing import Any, List, Mapping, Union

import bigframes.core.sql

STRUCT_VALUES = Union[
    str, int, float, bool, Mapping[str, str], List[str], Mapping[str, Any]
]
STRUCT_TYPE = Mapping[str, STRUCT_VALUES]


def struct_literal(struct_options: STRUCT_TYPE) -> str:
    rendered_options = []
    for option_name, option_value in struct_options.items():
        if option_name == "model_params":
            json_str = json.dumps(option_value)
            # Escape single quotes for SQL string literal
            sql_json_str = json_str.replace("'", "''")
            rendered_val = f"JSON'{sql_json_str}'"
        elif isinstance(option_value, collections.abc.Mapping):
            struct_body = ", ".join(
                [
                    f"{bigframes.core.sql.simple_literal(v)} AS {k}"
                    for k, v in option_value.items()
                ]
            )
            rendered_val = f"STRUCT({struct_body})"
        elif isinstance(option_value, list):
            rendered_val = (
                "["
                + ", ".join(
                    [bigframes.core.sql.simple_literal(v) for v in option_value]
                )
                + "]"
            )
        elif isinstance(option_value, bool):
            rendered_val = str(option_value).lower()
        else:
            rendered_val = bigframes.core.sql.simple_literal(option_value)
        rendered_options.append(f"{rendered_val} AS {option_name}")
    return f"STRUCT({', '.join(rendered_options)})"
