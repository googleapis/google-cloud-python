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

import jinja2

SCRIPTS_DIRECTORY = pathlib.Path(__file__).parent.parent.absolute()
PACKAGE_ROOT = SCRIPTS_DIRECTORY.parent
CODE_ROOT = PACKAGE_ROOT / "bigframes"
SCRIPT_PATH_RELATIVE = (
    pathlib.Path(__file__).relative_to(PACKAGE_ROOT).parent.parent
    / "generate_bigframes_bigquery.py"
)


# Directory containing the YAML files
DATA_DIR = SCRIPTS_DIRECTORY / "data" / "sql-functions"
# Directory where the generated Python files will be placed
OUTPUT_DIR = CODE_ROOT / "operations" / "googlesql"
# Directory where the generated test files will be placed
TEST_OUTPUT_DIR = PACKAGE_ROOT / "tests" / "unit" / "bigquery" / "generated"
# Directory containing the Jinja2 templates
TEMPLATE_DIR = SCRIPTS_DIRECTORY / "templates"

PYTHON_BUILTINS = {
    "abs",
    "all",
    "any",
    "ascii",
    "bin",
    "bool",
    "breakpoint",
    "bytearray",
    "bytes",
    "callable",
    "chr",
    "classmethod",
    "compile",
    "complex",
    "delattr",
    "dict",
    "dir",
    "divmod",
    "enumerate",
    "eval",
    "exec",
    "filter",
    "float",
    "format",
    "frozenset",
    "getattr",
    "globals",
    "hasattr",
    "hash",
    "help",
    "hex",
    "id",
    "input",
    "int",
    "isinstance",
    "issubclass",
    "iter",
    "len",
    "list",
    "locals",
    "map",
    "max",
    "memoryview",
    "min",
    "next",
    "object",
    "oct",
    "open",
    "ord",
    "pow",
    "print",
    "property",
    "range",
    "repr",
    "reversed",
    "round",
    "set",
    "setattr",
    "slice",
    "sorted",
    "staticmethod",
    "str",
    "sum",
    "super",
    "tuple",
    "type",
    "vars",
    "zip",
}

DTYPE_MAP = {
    "binary": "dtypes.BYTES_DTYPE",
    "string": "dtypes.STRING_DTYPE",
    "int64": "dtypes.INT_DTYPE",
    "i64": "dtypes.INT_DTYPE",
    "float64": "dtypes.FLOAT_DTYPE",
    "fp64": "dtypes.FLOAT_DTYPE",
    "bool": "dtypes.BOOL_DTYPE",
    "boolean": "dtypes.BOOL_DTYPE",
    "geography": "dtypes.GEO_DTYPE",
    "json": "dtypes.JSON_DTYPE",
    "date": "dtypes.DATE_DTYPE",
    "time": "dtypes.TIME_DTYPE",
    "datetime": "dtypes.DATETIME_DTYPE",
    "timestamp": "dtypes.TIMESTAMP_DTYPE",
    "decimal<38,9>": "dtypes.NUMERIC_DTYPE",
    "decimal<76,38>": "dtypes.BIGNUMERIC_DTYPE",
}

PY_TYPE_MAP = {
    "binary": "bytes",
    "string": "str",
    "int64": "int",
    "i64": "int",
    "float64": "float",
    "fp64": "float",
    "bool": "bool",
    "boolean": "bool",
    "geography": "Any",
    "json": "Any",
    "date": "datetime.date",
    "time": "datetime.time",
    "datetime": "datetime.datetime",
    "timestamp": "datetime.datetime",
    "struct": "dict",
    "decimal<38,9>": "decimal.Decimal",
    "decimal<76,38>": "decimal.Decimal",
    "interval_day": "datetime.timedelta",
}

RUFF_COMMON_ARGS = [
    "--target-version=py310",
    "--line-length=88",
]
RUFF_CHECK_ARGS = [
    "check",
    "--select",
    "I,F",
    "--fix",
] + RUFF_COMMON_ARGS
RUFF_FORMAT_ARGS = [
    "format",
] + RUFF_COMMON_ARGS


def _load_templates() -> dict[str, jinja2.Template]:
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return {
        "operation": env.get_template("operation.py.j2"),
        "test_operation": env.get_template("test_operation.py.j2"),
        "license": env.get_template("license.py.j2"),
        "signature_def": env.get_template("signature_def.py.j2"),
        "core_series_accessor": env.get_template("core_series_accessor.py.j2"),
        "bigframes_series_accessor": env.get_template(
            "bigframes_series_accessor.py.j2"
        ),
        "pandas_series_accessor": env.get_template("pandas_series_accessor.py.j2"),
    }


TEMPLATES: dict[str, jinja2.Template] = _load_templates()


def __getattr__(name: str):
    global _templates

    if name != "TEMPLATES":
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

    if _templates is None:
        _templates = _load_templates()

    return _templates
