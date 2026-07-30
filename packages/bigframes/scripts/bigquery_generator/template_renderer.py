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


"""
Renders jinja template with module data parsed from yaml.
"""

from typing import Sequence

import jinja2

from . import constants, data_models


def _load_templates() -> dict[str, jinja2.Template]:
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(constants.SCRIPTS_DIRECTORY / "templates"),
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


def _unwrap_list_type(yaml_type: str) -> str | None:
    if yaml_type.startswith("list<") and yaml_type.endswith(">"):
        return yaml_type[5:-1]
    return None


def _try_get_concrete_type_expr(yaml_type: str) -> str | None:
    if yaml_type in constants.DTYPE_MAP:
        return constants.DTYPE_MAP[yaml_type]
    inner = _unwrap_list_type(yaml_type)
    if inner and inner in constants.DTYPE_MAP:
        # TODO (b/540011825): Support recursive type parsing
        return f"dtypes.list_type({constants.DTYPE_MAP[inner]})"
    return None


def _get_concrete_type_expr(yaml_type: str) -> str:
    expr = _try_get_concrete_type_expr(yaml_type)
    if expr is None:
        raise ValueError(f"Not a concrete type: {yaml_type}")
    return expr


def _is_concrete_type(yaml_type: str) -> bool:
    return _try_get_concrete_type_expr(yaml_type) is not None


def _validate_type(yaml_type: str) -> None:
    if yaml_type in ("any1", "struct") or yaml_type in constants.DTYPE_MAP:
        return
    inner = _unwrap_list_type(yaml_type)
    if inner is not None:
        if inner == "any1" or inner in constants.DTYPE_MAP:
            return
        raise ValueError(f"Unsupported inner type: {inner}")
    raise ValueError(f"Unsupported type: {yaml_type}")


def _validate_types(impls: Sequence[data_models.BQFuncImpl]) -> None:
    for impl in impls:
        for arg in impl.args:
            _validate_type(arg.value)
        _validate_type(impl.return_type)


def render_signature_def(
    bq_func: data_models.BQFunc,
) -> tuple[str, str | None]:
    """
    Returns the signature function name and its definition.
    If the signature function can be inlined, the first return value is the lambda,
    and the second value is None.

    Examples:
        Inlined signature function:
            ("lambda *args: dtypes.FLOAT64_DTYPE", None)

        Custom signature function definition:
            ("_ABS_SIG", "def _ABS_SIG(*args): ...")
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

    sig_func_name = f"_{bq_func.op_base_name.upper()}_SIG"

    max_args = max(len(impl.args) for impl in bq_func.impls)

    rendered = TEMPLATES["signature_def"].render(
        func_name=sig_func_name,
        max_args=max_args,
        impls=bq_func.impls,
        sql_name=bq_func.name,
        dtype_map=constants.DTYPE_MAP,
    )

    return sig_func_name, rendered


def _get_bigframes_func_args(
    bq_func: data_models.BQFunc,
) -> tuple[data_models.BigFramesFuncArg, ...]:
    """
    Coalesces arguments from all the signatures of this function,
    and return them in the order of appearance in the yaml file
    """
    args_by_name: dict[str, data_models.BigFramesFuncArgBuilder] = {}
    arg_order: list[str] = []
    arg_appearances: dict[str, int] = {}
    for impl in bq_func.impls:
        seen_in_impl = set()
        for bq_func_arg in impl.args:
            name = bq_func_arg.name
            seen_in_impl.add(name)
            if name not in args_by_name:
                args_by_name[name] = data_models.BigFramesFuncArgBuilder(
                    name=name,
                    types=set(),
                    optional=bq_func_arg.optional,
                    keyword_only=bq_func_arg.keyword_only,
                )
                arg_order.append(name)
            else:
                # If it was marked optional or keyword_only in any previous impl, keep it.
                # Or if this signature marks it as optional/keyword_only, update it.
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

    return tuple(args_by_name[name].build() for name in arg_order)


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


def _to_bigframes_func(
    bq_func: data_models.BQFunc, import_module: str | None = None
) -> data_models.BigFramesFunc:
    python_name = bq_func.op_base_name
    if python_name in constants.PYTHON_BUILTINS:
        python_name = python_name + "_"

    return data_models.BigFramesFunc(
        name=python_name,
        op_name=f"_{bq_func.op_base_name.upper()}_OP",
        description=bq_func.description,
        args=_get_bigframes_func_args(bq_func),
        series_accessor_arg=bq_func.series_accessor_arg,
        import_module=import_module,
    )


def render_license() -> str:
    return TEMPLATES["license"].render()


def render_operation(
    bq_module: data_models.BQModule,
) -> str:
    ops: list[data_models.BigFramesOp] = []
    functions: list[data_models.BigFramesFunc] = []

    for bq_func in bq_module.functions:
        ops.append(_to_bigframes_op(bq_func))
        functions.append(_to_bigframes_func(bq_func))

    return TEMPLATES["operation"].render(
        yaml_path=bq_module.yaml_file.relative_to(constants.PACKAGE_ROOT),
        script_path=constants.SCRIPT_PATH_RELATIVE,
        ops=ops,
        functions=functions,
    )


def render_tests(bq_module: data_models.BQModule) -> str:
    import_path = "bigframes.operations.googlesql." + ".".join(
        bq_module.module_path.parts
    )
    functions: list[data_models.BigFramesFunc] = []
    for bq_func in bq_module.functions:
        functions.append(_to_bigframes_func(bq_func))

    return TEMPLATES["test_operation"].render(
        yaml_path=bq_module.yaml_file.relative_to(constants.PACKAGE_ROOT),
        script_path=constants.SCRIPT_PATH_RELATIVE,
        import_path=import_path,
        short_name=bq_module.module_path.name,
        is_global=bq_module.is_global,
        functions=functions,
    )


def _create_accessor_class_name(namespace: tuple[str, ...], prefix: str = "") -> str:
    if not namespace:
        return f"{prefix}BigQuerySeriesAccessor"
    camel_parts = [part.capitalize() for part in namespace]
    return f"{prefix}{''.join(camel_parts)}SeriesAccessor"


def render_accessor(
    bq_modules: Sequence[data_models.BQModule],
) -> tuple[str, str, str]:
    """
    Returns the content for core accessor, pandas accessor and BF accessor
    """

    namespaces: set[tuple[str, ...]] = set()
    for bq_module in bq_modules:
        for i in range(len(bq_module.namespace) + 1):
            namespaces.add(bq_module.namespace[:i])

    sorted_namespaces = sorted(list(namespaces), key=lambda ns: (len(ns), ns))

    accessors: list[data_models.Accessor] = []
    accessor_lookup_table: dict[tuple[str, ...], data_models.Accessor] = {}
    for namespace in sorted_namespaces:
        accessor = data_models.Accessor(
            class_name=_create_accessor_class_name(namespace),
            bigframes_class_name=_create_accessor_class_name(
                namespace, prefix="Bigframes"
            ),
            pandas_class_name=_create_accessor_class_name(namespace, prefix="Pandas"),
            is_root=len(namespace) == 0,
            description=(
                f"Series accessor for BigQuery {'.'.join(namespace)} functions."
                if namespace
                else "Series accessor for BigQuery functions."
            ),
            children=[],
            functions=[],
        )
        accessors.append(accessor)
        accessor_lookup_table[namespace] = accessor

        # Establish parent-child relations
        if len(namespace) > 0:
            accessor.prop_name = namespace[-1]
            parent_namespace = namespace[:-1]
            accessor_lookup_table[parent_namespace].children.append(accessor)

    # Arrange functions by namespaces
    for bq_module in bq_modules:
        module_parts = bq_module.module_path.parts
        for bq_func in bq_module.functions:
            if bq_func.series_accessor_arg is None:
                continue
            bf_func = _to_bigframes_func(
                bq_func,
                import_module=f"bigframes.operations.googlesql.{'.'.join(module_parts)}",
            )
            accessor_lookup_table[bq_module.namespace].functions.append(bf_func)

    core_content = TEMPLATES["core_series_accessor"].render(
        script_path=constants.SCRIPT_PATH_RELATIVE,
        namespaces=accessors,
    )

    pandas_content = TEMPLATES["pandas_series_accessor"].render(
        script_path=constants.SCRIPT_PATH_RELATIVE, namespaces=accessors
    )

    bigframes_content = TEMPLATES["bigframes_series_accessor"].render(
        script_path=constants.SCRIPT_PATH_RELATIVE, namespaces=accessors
    )

    return core_content, pandas_content, bigframes_content
