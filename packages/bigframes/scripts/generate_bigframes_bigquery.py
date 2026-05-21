#!/usr/bin/env -S uv run --active --script
#
# /// script
# dependencies = [
#   "jinja2",
#   "pyyaml",
#   "ruff==0.14.14",
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
OUTPUT_DIR = pathlib.Path("bigframes/operations/googlesql")
# Directory where the generated test files will be placed
TEST_OUTPUT_DIR = pathlib.Path("tests/unit/bigquery/generated")
# Directory containing the Jinja2 templates
TEMPLATE_DIR = pathlib.Path("scripts/templates")

RUFF_ARGS = [
    "ruff",
    "check",
    "--select",
    "I",
    "--fix",
    "--target-version=py310",
    "--line-length=88",
]

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


def load_templates():
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return (
        env.get_template("operation.py.j2"),
        env.get_template("test_operation.py.j2"),
        env.get_template("license.py.j2"),
    )


def _collect_args(impls):
    args_by_name = {}
    arg_order = []
    for impl in impls:
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
    return args_by_name, arg_order


def _build_arg_specs(args_by_name, arg_order):
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
    return arg_specs


def _get_return_signature(impls):
    return_types = {impl["return"] for impl in impls}
    if len(return_types) == 1:
        ret_type = sorted(return_types)[0]
        return f"lambda *args: {DTYPE_MAP.get(ret_type, 'None')}"
    else:
        # Fallback to Any/None if ambiguous
        return "lambda *args: None"


def _get_func_args(args_by_name, arg_order):
    func_args = []
    for name in arg_order:
        arg_info = args_by_name[name]
        types = [PY_TYPE_MAP.get(t, "Any") for t in sorted(arg_info["types"])] + [
            "Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]"
        ]
        type_hint = (
            "Union[" + ", ".join(sorted(set(types))) + "]"
            if len(types) > 1
            else types[0]
        )
        default = "sentinels.Sentinel.ARGUMENT_DEFAULT" if arg_info["optional"] else ""
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
        if not arg.get("default"):
            arg.pop("default", None)

    return func_args


def _get_test_args(args_by_name, arg_order):
    test_args = []
    for name in arg_order:
        arg_info = args_by_name[name]
        some_type = sorted(arg_info["types"])[0]
        col_name = YAML_TYPE_TO_COL.get(some_type, "string_col")
        test_args.append({"col_name": col_name})
    return test_args


def parse_scalar_functions(data, module_name, is_global=False):
    ops_list = []
    functions_list = []

    if "scalar_functions" not in data:
        return ops_list, functions_list

    for func_data in data["scalar_functions"]:
        sql_name = func_data["name"]
        python_name = to_snake_case(sql_name)
        if not is_global and python_name.startswith(module_name + "_"):
            python_name = python_name[len(module_name) + 1 :]

        internal_op_name = f"_{python_name.upper()}_OP"

        # Aggregate args across impls
        args_by_name, arg_order = _collect_args(func_data["impls"])

        # Build ArgSpecs
        arg_specs = _build_arg_specs(args_by_name, arg_order)
        arg_specs_str = ", ".join(arg_specs)
        if len(arg_specs) == 1:
            arg_specs_str += ","

        # Determine return dtype
        signature = _get_return_signature(func_data["impls"])

        ops_list.append(
            {
                "internal_name": internal_op_name,
                "sql_name": sql_name.upper(),
                "arg_specs": arg_specs_str,
                "signature": signature,
            }
        )

        # Function args
        func_args = _get_func_args(args_by_name, arg_order)

        # Test args
        test_args = _get_test_args(args_by_name, arg_order)

        functions_list.append(
            {
                "name": python_name,
                "op_name": internal_op_name,
                "description": func_data["description"],
                "args": func_args,
                "test_args": test_args,
            }
        )

    return ops_list, functions_list


def run_ruff(path: pathlib.Path):
    import sys

    subprocess.run(
        [sys.executable, "-m", "ruff"]
        + RUFF_ARGS[1:]
        + [
            str(path),
        ],
        check=True,
    )


def ensure_init_py(
    directory: pathlib.Path, limit_dir: pathlib.Path, license_template
):
    """Ensures __init__.py exists in the directory and its parents up to limit_dir."""
    curr = directory
    while curr != limit_dir and curr != curr.parent:
        init_file = curr / "__init__.py"
        if not init_file.exists():
            print(f"  Creating {init_file}")
            content = license_template.render()
            with open(init_file, "w") as f:
                f.write(content)
            run_ruff(init_file)
        curr = curr.parent


def process_yaml_file(yaml_file, template, test_template, license_template):
    print(f"Processing {yaml_file}...")
    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)

    rel_path = yaml_file.relative_to(DATA_DIR)
    module_path = rel_path.with_suffix("")
    module_name = module_path.name
    output_file = OUTPUT_DIR.joinpath(module_path).with_suffix(".py")

    is_global = "global_namespace" in module_path.parts
    ops_list, functions_list = parse_scalar_functions(
        data, module_name, is_global=is_global
    )

    # Render and write
    output_file.parent.mkdir(parents=True, exist_ok=True)
    ensure_init_py(output_file.parent, OUTPUT_DIR.parent, license_template)
    content = template.render(
        yaml_path=str(yaml_file),
        script_path="scripts/generate_bigframes_bigquery.py",
        ops=ops_list,
        functions=functions_list,
    )
    with open(output_file, "w") as f:
        f.write(content)

    run_ruff(output_file)
    print(f"  Generated {output_file}")

    # Render and write test
    import_path = "bigframes.operations.googlesql." + ".".join(module_path.parts)
    test_output_file = TEST_OUTPUT_DIR.joinpath(
        module_path.with_name(f"test_{module_path.name}")
    ).with_suffix(".py")

    test_output_file.parent.mkdir(parents=True, exist_ok=True)
    ensure_init_py(test_output_file.parent, TEST_OUTPUT_DIR.parent, license_template)
    test_content = test_template.render(
        yaml_path=str(yaml_file),
        script_path="scripts/generate_bigframes_bigquery.py",
        import_path=import_path,
        short_name=module_path.name,
        is_global=is_global,
        functions=functions_list,
    )
    with open(test_output_file, "w") as f:
        f.write(test_content)

    run_ruff(test_output_file)
    print(f"  Generated {test_output_file}")


def main():
    template, test_template, license_template = load_templates()

    for yaml_file in sorted(DATA_DIR.glob("**/*.yaml")):
        process_yaml_file(yaml_file, template, test_template, license_template)


if __name__ == "__main__":
    main()
