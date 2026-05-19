#!/usr/bin/env -S uv run --script
#
# /// script
# dependencies = [
#   "autoflake",
#   "jinja2",
#   "pyyaml",
# ]
# ///
#
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
import subprocess

import jinja2
import yaml

# Directory containing the YAML files
DATA_DIR = pathlib.Path("scripts/data/sql-functions")
# Directory where the generated Python files will be placed
OUTPUT_DIR = pathlib.Path("bigframes/bigquery/_operations")
# Directory where the generated test files will be placed
TEST_OUTPUT_DIR = pathlib.Path("tests/unit/bigquery/_operations")

LICENSE_HEADER = """# Copyright 2026 Google LLC
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
"""

TEMPLATE = """{{ license_header }}
#
# DO NOT MODIFY THIS FILE DIRECTLY.
# This file was generated from: {{ yaml_path }}
# by the script: {{ script_path }}

from __future__ import annotations

import datetime
from typing import Any, Optional, TypeVar, Union

from bigframes import dtypes
import bigframes.bigquery._googlesql
import bigframes.core.col
import bigframes.core.expression as ex
import bigframes.core.sentinels as sentinels
from bigframes.operations import googlesql
import bigframes.operations as ops
import bigframes.series as series

T = TypeVar("T", series.Series, bigframes.core.col.Expression)

{% for op in ops %}
{{ op.internal_name }} = googlesql.GoogleSqlScalarOp(
    "{{ op.sql_name }}",
    args=({{ op.arg_specs }}),
    signature={{ op.signature }},
)
{% endfor %}
{% for func in functions %}


def {{ func.name }}(
{% for arg in func.args %}
    {{ arg.name }}: Union[T, bigframes.core.col.Expression, {{ arg.type_hint }}]{% if arg.default %} = {{ arg.default }}{% endif %},
{% endfor %}
) -> T:
    \"\"\"{{ func.description }}\"\"\"
    return bigframes.bigquery._googlesql.apply_googlesql_scalar_op(
        {{ func.op_name }},
{% for arg in func.args %}
        {{ arg.name }},
{% endfor %}
    )  # type: ignore
{% endfor %}
"""

TEST_TEMPLATE = """{{ license_header }}
#
# DO NOT MODIFY THIS FILE DIRECTLY.
# This file was generated from: {{ yaml_path }}
# by the script: {{ script_path }}

from typing import cast

import pytest

import bigframes.pandas as bpd
import {{ import_path }} as {{ short_name }}

pytest.importorskip("pytest_snapshot")


{% for func in functions %}
def test_{{ func.name }}(scalar_types_df: bpd.DataFrame, snapshot):
    result = {{ short_name }}.{{ func.name }}(
{% for arg in func.test_args %}
        cast(bpd.Series, scalar_types_df["{{ arg.col_name }}"]),
{% endfor %}
    ).to_frame()
    snapshot.assert_match(result.sql, "out.sql")


{% endfor %}
"""

DTYPE_MAP = {
    "binary": "dtypes.BYTES_DTYPE",
    "string": "dtypes.STRING_DTYPE",
    "int64": "dtypes.INT_DTYPE",
    "float64": "dtypes.FLOAT_DTYPE",
    "bool": "dtypes.BOOL_DTYPE",
    "geography": "dtypes.GEO_DTYPE",
    "json": "dtypes.JSON_DTYPE",
    "date": "dtypes.DATE_DTYPE",
    "time": "dtypes.TIME_DTYPE",
    "datetime": "dtypes.DATETIME_DTYPE",
    "timestamp": "dtypes.TIMESTAMP_DTYPE",
}

PY_TYPE_MAP = {
    "binary": "bytes",
    "string": "str",
    "int64": "int",
    "float64": "float",
    "bool": "bool",
    "geography": "Any",
    "json": "Any",
    "date": "datetime.date",
    "time": "datetime.time",
    "datetime": "datetime.datetime",
    "timestamp": "datetime.datetime",
    "struct": "dict",
}

YAML_TYPE_TO_COL = {
    "binary": "bytes_col",
    "string": "string_col",
    "int64": "int64_col",
    "float64": "float64_col",
    "bool": "bool_col",
    "geography": "geography_col",
    "date": "date_col",
    "time": "time_col",
    "datetime": "datetime_col",
    "timestamp": "timestamp_col",
}


def to_snake_case(name):
    # Replace dots with underscores
    name = name.replace(".", "_")
    # Handle CamelCase to snake_case
    name = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    # Replace multiple underscores with one
    name = re.sub(r"_+", "_", name)
    return name


def main():
    env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)
    template = env.from_string(TEMPLATE)
    test_template = env.from_string(TEST_TEMPLATE)

    for yaml_file in DATA_DIR.glob("**/*.yaml"):
        print(f"Processing {yaml_file}...")
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f)

        rel_path = yaml_file.relative_to(DATA_DIR)
        module_path = rel_path.with_suffix("")
        module_name = module_path.name
        output_file = OUTPUT_DIR.joinpath(module_path).with_suffix(".py")

        ops_list = []
        functions_list = []

        if "scalar_functions" in data:
            for func_data in data["scalar_functions"]:
                sql_name = func_data["name"]
                python_name = to_snake_case(sql_name)
                if python_name.startswith(module_name + "_"):
                    python_name = python_name[len(module_name) + 1 :]

                internal_op_name = f"_{python_name.upper()}_OP"

                # Aggregate args across impls
                args_by_name = {}
                arg_order = []
                for impl in func_data["impls"]:
                    for arg in impl["args"]:
                        name = arg["name"]
                        if name not in args_by_name:
                            args_by_name[name] = {
                                "types": set(),
                                "optional": arg["optional"],
                                "keyword_only": arg["keyword_only"],
                            }
                            arg_order.append(name)
                        args_by_name[name]["types"].add(arg["value"])

                # Build ArgSpecs
                arg_specs = []
                for name in arg_order:
                    arg_info = args_by_name[name]
                    spec = "googlesql.ArgSpec("
                    if arg_info["keyword_only"]:
                        spec += f'arg_name="{name}", '
                    if arg_info["optional"]:
                        spec += "optional=True, "
                    spec = spec.rstrip(", ") + ")"
                    arg_specs.append(spec)

                # Determine return dtype
                return_types = {impl["return"] for impl in func_data["impls"]}
                if len(return_types) == 1:
                    ret_type = list(return_types)[0]
                    signature = f"lambda *args: {DTYPE_MAP.get(ret_type, 'None')}"
                else:
                    # Fallback to Any/None if ambiguous
                    signature = "lambda *args: None"

                ops_list.append(
                    {
                        "internal_name": internal_op_name,
                        "sql_name": sql_name.upper(),
                        "arg_specs": ", ".join(arg_specs),
                        "signature": signature,
                    }
                )

                # Function args
                func_args = []
                for name in arg_order:
                    arg_info = args_by_name[name]
                    types = [PY_TYPE_MAP.get(t, "Any") for t in arg_info["types"]]
                    type_hint = (
                        "Union[" + ", ".join(sorted(set(types))) + "]"
                        if len(types) > 1
                        else types[0]
                    )
                    default = "sentinels.DEFAULT" if arg_info["optional"] else ""
                    func_args.append(
                        {
                            "name": name,
                            "type_hint": type_hint,
                            "default": default,
                        }
                    )

                # Clean up default values for mandatory args
                # In Python, mandatory args come first.
                for arg in func_args:
                    if not arg["default"]:
                        del arg["default"]

                # Test args
                test_args = []
                for name in arg_order:
                    arg_info = args_by_name[name]
                    some_type = list(arg_info["types"])[0]
                    col_name = YAML_TYPE_TO_COL.get(some_type, "string_col")
                    test_args.append({"col_name": col_name})

                functions_list.append(
                    {
                        "name": python_name,
                        "op_name": internal_op_name,
                        "description": func_data["description"],
                        "args": func_args,
                        "test_args": test_args,
                    }
                )

        # Render and write
        output_file.parent.mkdir(parents=True, exist_ok=True)
        content = template.render(
            license_header=LICENSE_HEADER,
            yaml_path=str(yaml_file),
            script_path="scripts/generate_bigframes_bigquery.py",
            ops=ops_list,
            functions=functions_list,
        )
        with open(output_file, "w") as f:
            f.write(content)

        subprocess.run(
            [
                "autoflake",
                "--in-place",
                "--remove-all-unused-imports",
                str(output_file),
            ],
            check=True,
        )
        print(f"  Generated {output_file}")

        # Render and write test
        import_path = "bigframes.bigquery._operations." + ".".join(module_path.parts)
        test_output_file = TEST_OUTPUT_DIR.joinpath(
            module_path.with_name(f"test_{module_path.name}")
        ).with_suffix(".py")

        test_output_file.parent.mkdir(parents=True, exist_ok=True)
        test_content = test_template.render(
            license_header=LICENSE_HEADER,
            yaml_path=str(yaml_file),
            script_path="scripts/generate_bigframes_bigquery.py",
            import_path=import_path,
            short_name=module_path.name,
            functions=functions_list,
        )
        with open(test_output_file, "w") as f:
            f.write(test_content)

        subprocess.run(
            [
                "autoflake",
                "--in-place",
                "--remove-all-unused-imports",
                str(test_output_file),
            ],
            check=True,
        )
        print(f"  Generated {test_output_file}")

        print(f"  Updating snapshots for {test_output_file}...")
        subprocess.run(
            [
                "pytest",
                str(test_output_file),
                "--snapshot-update",
            ],
            check=False,
        )


if __name__ == "__main__":
    main()
