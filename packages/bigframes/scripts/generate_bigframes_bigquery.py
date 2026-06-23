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

SCRIPTS_DIRECTORY = pathlib.Path(__file__).parent.absolute()
PACKAGE_ROOT = SCRIPTS_DIRECTORY.parent
CODE_ROOT = PACKAGE_ROOT / "bigframes"
SCRIPT_PATH_RELATIVE = pathlib.Path(__file__).relative_to(PACKAGE_ROOT)

# Directory containing the YAML files
DATA_DIR = SCRIPTS_DIRECTORY / "data" / "sql-functions"
# Directory where the generated Python files will be placed
OUTPUT_DIR = CODE_ROOT / "operations" / "googlesql"
# Directory where the generated test files will be placed
TEST_OUTPUT_DIR = PACKAGE_ROOT / "tests" / "unit" / "bigquery" / "generated"
# Directory containing the Jinja2 templates
TEMPLATE_DIR = SCRIPTS_DIRECTORY / "templates"


RUFF_COMMON_ARGS = [
    "--target-version=py310",
    "--line-length=88",
]
RUFF_CHECK_ARGS = [
    "ruff",
    "check",
    "--select",
    "I,F",
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
    "decimal<76,38>": "bignumeric_col",
}

_PYTHON_BUILTINS = {
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


def _collect_args(impls):
    args_by_name = {}
    arg_order = []
    arg_appearances = {}
    for impl in impls:
        seen_in_impl = set()
        for arg in impl["args"]:
            name = arg["name"]
            seen_in_impl.add(name)
            if name not in args_by_name:
                args_by_name[name] = {
                    "types": set(),
                    "optional": arg["optional"],
                    "keyword_only": arg["keyword_only"],
                }
                arg_order.append(name)
            else:
                # If it was marked optional or keyword_only in any previous impl, keep it.
                # Or if this impl marks it as optional/keyword_only, update it.
                if arg["optional"]:
                    args_by_name[name]["optional"] = True
                if arg["keyword_only"]:
                    args_by_name[name]["keyword_only"] = True
            args_by_name[name]["types"].add(arg["value"])
        for name in seen_in_impl:
            arg_appearances[name] = arg_appearances.get(name, 0) + 1

    # If an argument is not in all impls, it must be optional overall
    num_impls = len(impls)
    for name, count in arg_appearances.items():
        if count < num_impls:
            args_by_name[name]["optional"] = True

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


def _validate_types(impls):
    for impl in impls:
        for arg in impl["args"]:
            val = arg["value"]
            if val == "any1":
                continue
            if val.startswith("list<") and val.endswith(">"):
                inner = val[5:-1]
                if inner != "any1" and inner not in DTYPE_MAP:
                    raise ValueError(f"Unsupported inner type: {inner}")
                continue
            if val == "struct":
                continue
            if val not in DTYPE_MAP:
                raise ValueError(f"Unsupported type: {val}")

        ret = impl["return"]
        if ret == "any1":
            continue
        if ret.startswith("list<") and ret.endswith(">"):
            inner = ret[5:-1]
            if inner != "any1" and inner not in DTYPE_MAP:
                raise ValueError(f"Unsupported inner type: {inner}")
            continue
        if ret not in DTYPE_MAP:
            raise ValueError(f"Unsupported type: {ret}")


def _generate_signature_def(python_name, impls, sql_name, template):
    for impl in impls:
        uses_any1 = False
        if "any1" in str(impl["return"]):
            uses_any1 = True
        for arg in impl["args"]:
            if "any1" in str(arg["value"]):
                uses_any1 = True
        impl["uses_any1"] = uses_any1

    return_types = {impl["return"] for impl in impls}

    # Optimization: if all impls return the same concrete type,
    # we can skip type checking and just return that type.
    if len(return_types) == 1:
        ret_type = next(iter(return_types))
        if _is_concrete_type(ret_type):
            sig_expr = f"lambda *args: {_get_concrete_type_expr(ret_type)}"
            return sig_expr, None

    _validate_types(impls)

    func_name = f"_{python_name.upper()}_SIG"
    max_args = max(len(impl["args"]) for impl in impls)

    rendered = template.render(
        func_name=func_name,
        max_args=max_args,
        impls=impls,
        sql_name=sql_name,
        dtype_map=DTYPE_MAP,
    )

    return func_name, rendered


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


def parse_scalar_functions(data, module_name, signature_def_template, is_global=False):
    ops_list = []
    functions_list = []

    if "scalar_functions" not in data:
        return ops_list, functions_list

    for func_data in data["scalar_functions"]:
        sql_name = func_data["name"]
        python_name = to_snake_case(sql_name)
        if not is_global and python_name.startswith(module_name + "_"):
            python_name = python_name[len(module_name) + 1 :]

        op_base_name = python_name
        if python_name in _PYTHON_BUILTINS:
            python_name = python_name + "_"

        internal_op_name = f"_{op_base_name.upper()}_OP"

        # Aggregate args across impls
        args_by_name, arg_order = _collect_args(func_data["impls"])

        # Build ArgSpecs
        arg_specs = _build_arg_specs(args_by_name, arg_order)
        arg_specs_str = ", ".join(arg_specs)
        if len(arg_specs) == 1:
            arg_specs_str += ","

        # Determine return dtype
        sig_name, sig_def = _generate_signature_def(
            op_base_name,
            func_data["impls"],
            sql_name,
            signature_def_template,
        )

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

        # Read series_accessor_arg
        series_accessor_arg = func_data.get("series_accessor_arg")

        functions_list.append(
            {
                "name": python_name,
                "op_name": internal_op_name,
                "description": func_data["description"],
                "args": func_args,
                "test_args": test_args,
                "series_accessor_arg": series_accessor_arg,
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


def process_yaml_file(yaml_file, templates):
    print(f"Processing {yaml_file}...")
    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)

    rel_path = yaml_file.relative_to(DATA_DIR)
    module_path = rel_path.with_suffix("")
    module_name = module_path.name
    output_file = OUTPUT_DIR.joinpath(module_path).with_suffix(".py")

    is_global = "global_namespace" in module_path.parts
    namespace = get_namespace(yaml_file)

    if not data or not isinstance(data, dict) or "scalar_functions" not in data:
        # If the file is empty or has no functions, just create the namespace.
        return [{"namespace": namespace}]

    ops_list, functions_list = parse_scalar_functions(
        data,
        module_name,
        templates["signature_def"],
        is_global=is_global,
    )

    # Render and write
    output_file.parent.mkdir(parents=True, exist_ok=True)
    ensure_init_py(output_file.parent, OUTPUT_DIR.parent, templates["license"])
    yaml_file_relative = yaml_file.relative_to(PACKAGE_ROOT)
    content = templates["operation"].render(
        yaml_path=yaml_file_relative,
        script_path=SCRIPT_PATH_RELATIVE,
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
    ensure_init_py(
        test_output_file.parent, TEST_OUTPUT_DIR.parent, templates["license"]
    )
    test_content = templates["test_operation"].render(
        yaml_path=yaml_file_relative,
        script_path=SCRIPT_PATH_RELATIVE,
        import_path=import_path,
        short_name=module_path.name,
        is_global=is_global,
        functions=functions_list,
    )
    with open(test_output_file, "w") as f:
        f.write(test_content)

    run_ruff(test_output_file)
    print(f"  Generated {test_output_file}")

    # Collect functions for Series accessor
    accessor_functions = []
    for func in functions_list:
        if func.get("series_accessor_arg"):
            import_module = (
                f"bigframes.operations.googlesql.{'.'.join(module_path.parts)}"
            )
            accessor_functions.append(
                {
                    "name": func["name"],
                    "import_module": import_module,
                    "namespace": namespace,
                    "description": func["description"],
                    "args": func["args"],
                    "series_accessor_arg": func["series_accessor_arg"],
                }
            )

    return accessor_functions


def get_namespace(yaml_file: pathlib.Path) -> tuple[str, ...] | None:
    rel_path = yaml_file.relative_to(DATA_DIR)
    parts = rel_path.with_suffix("").parts
    if "global_namespace" in parts:
        return None
    return parts


def get_class_name(ns_tuple: tuple[str, ...], prefix: str = "") -> str:
    if not ns_tuple:
        return f"{prefix}BigQuerySeriesAccessor"
    camel_parts = [part.capitalize() for part in ns_tuple]
    return f"{prefix}{''.join(camel_parts)}SeriesAccessor"


def generate_series_accessors(functions: list[dict], templates: dict):
    print("Generating Series accessors...")
    # Find all active namespaces
    active_namespaces = set()
    for func in functions:
        ns = func["namespace"] or ()
        for i in range(len(ns) + 1):
            active_namespaces.add(ns[:i])

    # Sort namespaces by depth so parents come first
    sorted_namespaces = sorted(list(active_namespaces), key=len)

    # Build namespace definitions
    ns_defs = []
    ns_by_tuple = {}
    for ns in sorted_namespaces:
        class_name = get_class_name(ns)
        bf_class_name = get_class_name(ns, prefix="Bigframes")
        pd_class_name = get_class_name(ns, prefix="Pandas")

        ns_def = {
            "ns_tuple": ns,
            "class_name": class_name,
            "bigframes_class_name": bf_class_name,
            "pandas_class_name": pd_class_name,
            "is_root": len(ns) == 0,
            "description": (
                f"Series accessor for BigQuery {'.'.join(ns)} functions."
                if ns
                else "Series accessor for BigQuery functions."
            ),
            "children": [],
            "functions": [],
        }
        ns_defs.append(ns_def)
        ns_by_tuple[ns] = ns_def

    # Populate functions
    for func in functions:
        if "name" in func:
            ns = func["namespace"] or ()
            ns_by_tuple[ns]["functions"].append(func)

    # Populate children properties
    for ns in sorted_namespaces:
        if len(ns) > 0:
            parent_ns = ns[:-1]
            parent_def = ns_by_tuple[parent_ns]
            child_def = ns_by_tuple[ns]
            parent_def["children"].append(
                {
                    "prop_name": ns[-1],
                    "class_name": child_def["class_name"],
                    "bigframes_class_name": child_def["bigframes_class_name"],
                    "pandas_class_name": child_def["pandas_class_name"],
                }
            )

    # Render and write core
    core_output_file = CODE_ROOT / "extensions" / "core" / "series_accessor.py"
    core_output_file.parent.mkdir(parents=True, exist_ok=True)
    ensure_init_py(core_output_file.parent, CODE_ROOT, templates["license"])
    core_content = templates["core_series_accessor"].render(
        script_path=SCRIPT_PATH_RELATIVE,
        namespaces=ns_defs,
    )
    with open(core_output_file, "w") as f:
        f.write(core_content)
    run_ruff(core_output_file)
    print(f"  Generated {core_output_file}")

    # Render and write bigframes
    bf_output_file = CODE_ROOT / "extensions" / "bigframes" / "series_accessor.py"
    bf_output_file.parent.mkdir(parents=True, exist_ok=True)
    ensure_init_py(bf_output_file.parent, CODE_ROOT, templates["license"])
    bf_content = templates["bigframes_series_accessor"].render(
        script_path=SCRIPT_PATH_RELATIVE,
        namespaces=ns_defs,
    )
    with open(bf_output_file, "w") as f:
        f.write(bf_content)
    run_ruff(bf_output_file)
    print(f"  Generated {bf_output_file}")

    # Render and write pandas
    pd_output_file = CODE_ROOT / "extensions" / "pandas" / "series_accessor.py"
    pd_output_file.parent.mkdir(parents=True, exist_ok=True)
    ensure_init_py(pd_output_file.parent, CODE_ROOT, templates["license"])
    pd_content = templates["pandas_series_accessor"].render(
        script_path=SCRIPT_PATH_RELATIVE,
        namespaces=ns_defs,
    )
    with open(pd_output_file, "w") as f:
        f.write(pd_content)
    run_ruff(pd_output_file)
    print(f"  Generated {pd_output_file}")


def main():
    templates = load_templates()

    all_accessor_functions = []
    for yaml_file in sorted(DATA_DIR.glob("**/*.yaml")):
        accessor_funcs = process_yaml_file(yaml_file, templates)
        all_accessor_functions.extend(accessor_funcs)

    if all_accessor_functions:
        generate_series_accessors(all_accessor_functions, templates)


if __name__ == "__main__":
    main()
