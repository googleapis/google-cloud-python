# Render jinja template with module data parsed from yaml
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

import re
import pathlib

import constants
import data_models
import jinja2


def _to_snake_case(name):
    # Replace dots with underscores
    name = name.replace(".", "_")
    # Handle CamelCase to snake_case
    name = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    # Replace multiple underscores with one
    name = re.sub(r"_+", "_", name)
    return name


def _get_concrete_type_expr(yaml_type: str) -> str:
    if yaml_type in constants.DTYPE_MAP:
        return constants.DTYPE_MAP[yaml_type]
    if yaml_type.startswith("list<") and yaml_type.endswith(">"):
        inner = yaml_type[5:-1]
        if inner in constants.DTYPE_MAP:
            return f"dtypes.list_type({constants.DTYPE_MAP[inner]})"
    raise ValueError(f"Not a concrete type: {yaml_type}")


def _is_concrete_type(yaml_type: str) -> bool:
    try:
        _get_concrete_type_expr(yaml_type)
        return True
    except ValueError:
        return False


def _validate_types(impls):
    for impl in impls:
        for arg in impl.args:
            val = arg.value
            if val == "any1":
                continue
            if val.startswith("list<") and val.endswith(">"):
                inner = val[5:-1]
                if inner != "any1" and inner not in constants.DTYPE_MAP:
                    raise ValueError(f"Unsupported inner type: {inner}")
                continue
            if val == "struct":
                continue
            if val not in constants.DTYPE_MAP:
                raise ValueError(f"Unsupported type: {val}")

        ret = impl.return_type
        if ret == "any1":
            continue
        if ret.startswith("list<") and ret.endswith(">"):
            inner = ret[5:-1]
            if inner != "any1" and inner not in constants.DTYPE_MAP:
                raise ValueError(f"Unsupported inner type: {inner}")
            continue
        if ret not in constants.DTYPE_MAP:
            raise ValueError(f"Unsupported type: {ret}")


def render_signature_def(
    bq_func: data_models.BQFunc,
    hosting_bq_module: data_models.BQModule,
) -> tuple[str, str | None]:
    """
    Returns the signature function name and it's definition.
    If the signature function can be inlined, the first return value is the lambda,
    and the second value is None.
    """
    op_base_name = _to_snake_case(bq_func.name)

    module_name = hosting_bq_module.name
    if not hosting_bq_module.is_global_namespace and op_base_name.startswith(
        module_name + "_"
    ):
        op_base_name = op_base_name[len(module_name) + 1 :]

    return_types = {impl.return_type for impl in bq_func.impls}
    # Optimization: if all impls return the same concrete type,
    # inline the signature function as a lambda
    if len(return_types) == 1:
        ret_type = next(iter(return_types))
        if _is_concrete_type(ret_type):
            sig_expr = f"lambda *args: {_get_concrete_type_expr(ret_type)}"
            return sig_expr, None

    _validate_types(bq_func.impls)

    python_name = op_base_name
    if python_name in constants.PYTHON_BUILTINS:
        python_name = python_name + "_"
    sig_func_name = f"_{python_name.upper()}_SIG"

    max_args = max(len(impl.args) for impl in bq_func.impls)

    rendered = constants.TEMPLATES["signature_def"].render(
        func_name=sig_func_name,
        max_args=max_args,
        impls=[impl.to_dict() for impl in bq_func.impls],
        sql_name=bq_func.name,
        dtype_map=constants.DTYPE_MAP,
    )

    return sig_func_name, rendered


def _to_bigframes_op(bq_func: data_models.BQFunc) -> data_models.BigFramesOp:
    pass


def _to_bigframes_func(bq_func: data_models.BQFunc) -> data_models.BigFramesFunc:
    pass


def render_operation(
    yaml_file: pathlib.Path, bq_module: data_models.BQModule, template: jinja2.Template
) -> str:
    ops = []
    functions = []

    return template.render(
        yaml_path=yaml_file.relative_to(constants.PACKAGE_ROOT),
        script_path=constants.SCRIPT_PATH_RELATIVE,
        ops=ops,
        functions=functions,
    )


def render_series_accessor() -> str:
    pass


def render_tests() -> str:
    pass
