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

import dataclasses
import inspect
import typing

import bigframes.core.expression as ex
from bigframes._config import options
from bigframes.exceptions import TranspilationError
from bigframes.functions import Udf
from bigframes.functions.udf_def import BigqueryUdf, PythonUdf
from bigframes.operations import base_ops, remote_function_ops

ArgKind = typing.Literal[
    "positional_only",
    "positional_or_keyword",
    "keyword_only",
    "var_positional",
    "var_keyword",
]

_ARGKIND_MAP: dict[inspect._ParameterKind, ArgKind] = {
    inspect.Parameter.POSITIONAL_ONLY: "positional_only",
    inspect.Parameter.POSITIONAL_OR_KEYWORD: "positional_or_keyword",
    inspect.Parameter.VAR_POSITIONAL: "var_positional",
    inspect.Parameter.KEYWORD_ONLY: "keyword_only",
    inspect.Parameter.VAR_KEYWORD: "var_keyword",
}


@dataclasses.dataclass(frozen=True)
class ArgumentSpec:
    """
    Information about a single argument to a function
    """

    name: str
    default_value: typing.Any
    argkind: ArgKind

    @property
    def is_positional(self) -> bool:
        return self.argkind in ["positional_only", "positional_or_keyword"]

    @property
    def is_keyword(self) -> bool:
        return self.argkind in ["keyword_only", "positional_or_keyword"]

    @property
    def is_var_positional(self) -> bool:
        return self.argkind == "var_positional"

    @property
    def is_var_keyword(self) -> bool:
        return self.argkind == "var_keyword"

    @property
    def is_varargs(self) -> bool:
        return self.is_var_positional


@dataclasses.dataclass(frozen=True)
class CallableExpression:
    """
    Encodes a calling convention and an expression to bind arguments to.
    """

    expr: ex.Expression
    arg_specs: typing.Sequence[ArgumentSpec]

    @classmethod
    def from_callable(cls, func: typing.Callable) -> CallableExpression:
        sig = inspect.signature(func)
        arg_specs = []
        for name, param in sig.parameters.items():
            arg_specs.append(
                ArgumentSpec(
                    name=name,
                    default_value=param.default,
                    argkind=_ARGKIND_MAP[param.kind],
                )
            )

        from bigframes.core.bytecode import py_to_expression

        try:
            expr = py_to_expression(func)
        except Exception as ex:
            raise TranspilationError(f"Failed to transpile function {func}") from ex
        return cls(expr=expr, arg_specs=arg_specs)

    def apply(self, *args, **kwargs) -> ex.Expression:
        """
        Apply the arguments to the expression.

        All args are expected to be column references, or scalars.
        """
        return self.bind_partial(*args, _offset=0, **kwargs).expr

    def bind_partial(
        self,
        *args,
        _offset: int = 0,
        **kwargs,
    ) -> CallableExpression:
        """
        Bind a subset of arguments and return a new CallableExpression with the remaining unbound arguments.
        """
        bindings: dict[typing.Hashable, ex.Expression] = {}
        pos_idx = 0
        allowed_params = self.arg_specs[_offset:]
        allowed_names = {spec.name for spec in allowed_params}

        # Validate unexpected keyword arguments
        for key in kwargs:
            if key not in allowed_names:
                raise TypeError(f"got an unexpected keyword argument '{key}'")

        def to_expr(val):
            if isinstance(val, ex.Expression):
                return val
            return ex.const(val)

        for spec in allowed_params:
            if spec.is_varargs:
                raise NotImplementedError(
                    "varargs in compiled python functions is not supported"
                )

            if pos_idx < len(args):
                if spec.name in kwargs:
                    raise TypeError(
                        f"got multiple values for keyword argument '{spec.name}'"
                    )
                bindings[spec.name] = to_expr(args[pos_idx])
                pos_idx += 1
            elif spec.name in kwargs:
                bindings[spec.name] = to_expr(kwargs[spec.name])
            elif spec.default_value is not inspect.Parameter.empty:
                bindings[spec.name] = to_expr(spec.default_value)
            else:
                raise TypeError(f"missing required argument: '{spec.name}'")

        if pos_idx < len(args):
            raise TypeError(
                f"too many positional arguments: expected {len(allowed_params)}, got {len(args)}"
            )

        new_expr = self.expr.bind_variables(bindings, allow_partial_bindings=True)
        remaining_specs = list(self.arg_specs[:_offset])
        return CallableExpression(expr=new_expr, arg_specs=remaining_specs)


def func_to_expr(op) -> CallableExpression:
    """
    Convert various bigframes, python functions into bigframes CallableExpression.
    """
    if isinstance(op, Udf):
        bq_op: base_ops.NaryOp
        if isinstance(op.udf_def, BigqueryUdf):
            bq_op = remote_function_ops.RemoteFunctionOp(function_def=op.udf_def)
        elif isinstance(op.udf_def, PythonUdf):
            bq_op = remote_function_ops.PythonUdfOp(function_def=op.udf_def)
        else:
            raise TypeError(f"Unsupported UDF definition: {op.udf_def}")

        inputs_expr = tuple(
            ex.free_var(arg.name) for arg in op.udf_def.signature.inputs
        )
        expr = ex.OpExpression(bq_op, inputs_expr)

        arg_specs = [
            ArgumentSpec(
                name=arg.name,
                default_value=inspect.Parameter.empty,
                # Udf specs don't have concept of positional only or keyword only yet,
                # so default to positional_or_keyword.
                argkind="positional_or_keyword",
            )
            for arg in op.udf_def.signature.inputs
        ]
        return CallableExpression(expr=expr, arg_specs=arg_specs)

    elif options.experiments.enable_python_transpiler and callable(op):
        return CallableExpression.from_callable(op)

    else:
        raise TypeError(f"Unsupported function type: {op}")
