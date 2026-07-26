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


import constants
import data_models


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
) -> tuple[str, str | None]:
    """
    Returns the signature function name and it's definition.
    If the signature function can be inlined, the first return value is the lambda,
    and the second value is None.
    """
    return_types = {impl.return_type for impl in bq_func.impls}
    # Optimization: if all impls return the same concrete type,
    # inline the signature function as a lambda
    if len(return_types) == 1:
        ret_type = next(iter(return_types))
        if _is_concrete_type(ret_type):
            sig_expr = f"lambda *args: {_get_concrete_type_expr(ret_type)}"
            return sig_expr, None

    _validate_types(bq_func.impls)

    python_name = bq_func.op_base_name
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


def _get_bigframes_func_args(
    bq_func: data_models.BQFunc,
) -> list[data_models.BigFramesFuncArg]:
    """
    Coalesces arguments from all the implementations of this function,
    and return them in the order of appearance in the yaml file
    """
    args_by_name = {}
    arg_order = []
    arg_appearances = {}
    for impl in bq_func.impls:
        seen_in_impl = set()
        for bq_func_arg in impl.args:
            name = bq_func_arg.name
            seen_in_impl.add(name)
            if name not in args_by_name:
                args_by_name[name] = data_models.BigFramesFuncArg(
                    name=name,
                    types=set(),
                    optional=bq_func_arg.optional,
                    keyword_only=bq_func_arg.keyword_only,
                )
                arg_order.append(name)
            else:
                # If it was marked optional or keyword_only in any previous impl, keep it.
                # Or if this impl marks it as optional/keyword_only, update it.
                if bq_func_arg.optional:
                    args_by_name[name].optional = True
                if bq_func_arg.keyword_only:
                    args_by_name[name].keyword_only = True
            args_by_name[name].types.add(bq_func_arg.value)
        for name in seen_in_impl:
            arg_appearances[name] = arg_appearances.get(name, 0) + 1

    # If an argument is not in all impls, it must be optional overall
    num_impls = len(bq_func.impls)
    for name, count in arg_appearances.items():
        if count < num_impls:
            args_by_name[name].optional = True

    return [args_by_name[name] for name in arg_order]


def _to_bigframes_op(bq_func: data_models.BQFunc) -> data_models.BigFramesOp:
    arg_specs = []
    for bf_func_arg in _get_bigframes_func_args(bq_func):
        spec = "googlesql.ArgSpec("
        if bf_func_arg.keyword_only:
            spec += f'arg_name="{bf_func_arg.name}", '
        if bf_func_arg.optional:
            spec += "optional=True, "
        spec = spec.rstrip(", ") + ")"
        arg_specs.append(spec)

    arg_specs_str = ", ".join(arg_specs)
    if len(arg_specs) == 1:
        arg_specs_str += ","

    (signature, signature_definition) = render_signature_def(bq_func)

    return data_models.BigFramesOp(
        internal_name=f"_{bq_func.op_base_name.upper()}_OP",
        sql_name=bq_func.name.upper(),
        arg_specs=arg_specs_str,
        signature=signature,
        signature_definition=signature_definition,
    )


def _to_bigframes_func(bq_func: data_models.BQFunc) -> data_models.BigFramesFunc:
    func_args = []
    for arg in _get_bigframes_func_args(bq_func):
        types = [constants.PY_TYPE_MAP.get(t, "Any") for t in sorted(arg.types)] + [
            "Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]"
        ]
        type_hint = (
            "Union[" + ", ".join(sorted(set(types))) + "]"
            if len(types) > 1
            else types[0]
        )
        func_args.append(
            {
                "name": arg.name,
                "type_hint": type_hint,
                "default": (
                    "sentinels.Sentinel.ARGUMENT_DEFAULT" if arg.optional else ""
                ),
            }
        )

    # Clean up default values for mandatory args
    # In Python, mandatory args come first.
    for arg in func_args:
        if not arg.get("default"):
            arg.pop("default", None)

    python_name = bq_func.op_base_name
    if python_name in constants.PYTHON_BUILTINS:
        python_name = python_name + "_"

    return data_models.BigFramesFunc(
        name=python_name,
        op_name=f"_{bq_func.op_base_name.upper()}_OP",
        description=bq_func.description,
        args=func_args,
        series_accessor_arg=[],
    )


def render_operation(
    bq_module: data_models.BQModule,
) -> str:
    ops = []
    functions = []

    for bq_func in bq_module.functions:
        ops.append(_to_bigframes_op(bq_func))
        functions.append(_to_bigframes_func(bq_func))

    return constants.TEMPLATES["operation"].render(
        yaml_path=bq_module.yaml_file.relative_to(constants.PACKAGE_ROOT),
        script_path=constants.SCRIPT_PATH_RELATIVE,
        ops=ops,
        functions=functions,
    )


def render_tests(bq_module: data_models.BQModule) -> str:

    pass
