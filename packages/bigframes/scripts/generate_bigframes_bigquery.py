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

RUFF_COMMON_ARGS = [
    "--target-version=py310",
    "--line-length=88",
]
RUFF_CHECK_ARGS = [
    "ruff",
    "check",
    "--select",
    "I",
    "--fix",
] + RUFF_COMMON_ARGS
RUFF_FORMAT_ARGS = [
    "ruff",
    "format",
] + RUFF_COMMON_ARGS


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
}

YAML_TYPE_TO_COL = {
    "binary": "bytes_col",
    "string": "string_col",
    "int64": "int64_col",
    "i64": "int64_col",
    "float64": "float64_col",
    "fp64": "float64_col",
    "bool": "bool_col",
    "boolean": "bool_col",
    "geography": "geography_col",
    "date": "date_col",
    "time": "time_col",
    "datetime": "datetime_col",
    "timestamp": "timestamp_col",
    "decimal<38,9>": "numeric_col",
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


def _is_concrete_type(yaml_type):
    if yaml_type in DTYPE_MAP:
        return True
    if yaml_type.startswith("list<") and yaml_type.endswith(">"):
        inner = yaml_type[5:-1]
        return inner in DTYPE_MAP
    return False


def _get_concrete_type_expr(yaml_type):
    if yaml_type in DTYPE_MAP:
        return DTYPE_MAP[yaml_type]
    if yaml_type.startswith("list<") and yaml_type.endswith(">"):
        inner = yaml_type[5:-1]
        return f"dtypes.list_type({DTYPE_MAP[inner]})"
    raise ValueError(f"Not a concrete type: {yaml_type}")


def _gen_impl_match_block(impl, impl_idx, return_type_yaml):
    lines = []
    lines.append(f"    # Try matching impl {impl_idx}")
    lines.append("    any1_val = None")
    lines.append("    match_ok = True")

    for idx, arg in enumerate(impl["args"]):
        arg_val = arg["value"]
        arg_var = f"args[{idx}]"

        lines.append(f"    if match_ok and {arg_var} is not None:")

        if arg_val == "any1":
            lines.append(f"        if any1_val is not None:")
            lines.append("            try:")
            lines.append(f"                any1_val = dtypes.coerce_to_common(any1_val, {arg_var})")
            lines.append("            except TypeError:")
            lines.append("                match_ok = False")
            lines.append("        else:")
            lines.append(f"            any1_val = {arg_var}")

        elif arg_val.startswith("list<") and arg_val.endswith(">"):
            inner_type = arg_val[5:-1]
            lines.append(f"        if not dtypes.is_array_like({arg_var}):")
            lines.append("            match_ok = False")
            lines.append("        else:")
            lines.append(f"            inner = dtypes.get_array_inner_type({arg_var})")

            if inner_type == "any1":
                lines.append("            if any1_val is not None:")
                lines.append("                try:")
                lines.append("                    any1_val = dtypes.coerce_to_common(any1_val, inner)")
                lines.append("                except TypeError:")
                lines.append("                    match_ok = False")
                lines.append("            else:")
                lines.append("                any1_val = inner")
            else:
                dtype_expr = DTYPE_MAP.get(inner_type)
                if not dtype_expr:
                     raise ValueError(f"Unsupported inner type: {inner_type}")
                lines.append("            try:")
                lines.append(f"                if dtypes.coerce_to_common(inner, {dtype_expr}) != {dtype_expr}:")
                lines.append("                    match_ok = False")
                lines.append("            except TypeError:")
                lines.append("                match_ok = False")

        elif arg_val == "struct":
            lines.append(f"        if not dtypes.is_struct_like({arg_var}):")
            lines.append("            match_ok = False")

        else:
            dtype_expr = DTYPE_MAP.get(arg_val)
            if not dtype_expr:
                raise ValueError(f"Unsupported type: {arg_val}")
            lines.append("        try:")
            lines.append(f"            if dtypes.coerce_to_common({arg_var}, {dtype_expr}) != {dtype_expr}:")
            lines.append("                match_ok = False")
            lines.append("        except TypeError:")
            lines.append("            match_ok = False")

    # If match_ok is still True, we resolved the inputs!
    lines.append("    if match_ok:")

    if return_type_yaml == "any1":
        lines.append("        return any1_val")
    elif return_type_yaml.startswith("list<") and return_type_yaml.endswith(">"):
        inner_type = return_type_yaml[5:-1]
        if inner_type == "any1":
            lines.append("        if any1_val is not None:")
            lines.append("            return dtypes.list_type(any1_val)")
            lines.append("        else:")
            lines.append("            return None")
        else:
            dtype_expr = DTYPE_MAP.get(inner_type)
            if not dtype_expr:
                raise ValueError(f"Unsupported inner type: {inner_type}")
            lines.append(f"        return dtypes.list_type({dtype_expr})")
    else:
        dtype_expr = DTYPE_MAP.get(return_type_yaml)
        if not dtype_expr:
            raise ValueError(f"Unsupported type: {return_type_yaml}")
        lines.append(f"        return {dtype_expr}")

    return "\n".join(lines)


def _generate_signature_def(python_name, impls, sql_name):
    return_types = {impl["return"] for impl in impls}

    # Optimization: if all impls return the same concrete type,
    # we can skip type checking and just return that type.
    if len(return_types) == 1:
        ret_type = next(iter(return_types))
        if _is_concrete_type(ret_type):
            sig_expr = f"lambda *args: {_get_concrete_type_expr(ret_type)}"
            return sig_expr, None

    func_name = f"_{python_name.upper()}_SIG"

    lines = []
    lines.append(f"def {func_name}(*args):")

    max_args = max(len(impl["args"]) for impl in impls)

    lines.append(f"    # Pad args with None to match max expected args")
    lines.append(f"    args = args + (None,) * ({max_args} - len(args))")

    for idx, impl in enumerate(impls):
        block = _gen_impl_match_block(impl, idx, impl["return"])
        lines.append(block)
        lines.append("")

    lines.append(f"    raise TypeError(f\"Could not find matching signature for {sql_name} with argument types: {{[str(t) for t in args]}}\")")

    return func_name, "\n".join(lines)


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
        sig_name, sig_def = _generate_signature_def(python_name, func_data["impls"], sql_name)

        ops_list.append(
            {
                "internal_name": internal_op_name,
                "sql_name": sql_name.upper(),
                "arg_specs": arg_specs_str,
                "signature": sig_name,
                "signature_definition": sig_def,
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
        + RUFF_CHECK_ARGS[1:]
        + [
            str(path),
        ],
        check=True,
    )

    subprocess.run(
        [sys.executable, "-m", "ruff"]
        + RUFF_FORMAT_ARGS[1:]
        + [
            str(path),
        ],
        check=True,
    )


def ensure_init_py(directory: pathlib.Path, limit_dir: pathlib.Path, license_template):
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
