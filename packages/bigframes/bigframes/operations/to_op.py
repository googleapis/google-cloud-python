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
import bigframes.core.identifiers as ids
import bigframes.dtypes as dtypes
from bigframes._config import options
from bigframes.functions import Udf
from bigframes.functions.udf_def import BigqueryUdf, PythonUdf
from bigframes.operations import base_ops, remote_function_ops


@dataclasses.dataclass(frozen=True)
class ArgumentSpec:
    """
    Information about a single argument to a function
    """

    name: str
    default_value: typing.Any
    is_varargs: bool


@dataclasses.dataclass(frozen=True)
class CallableExpression(ex.Expression):
    """
    Encodes a calling convention and an expression to bind arguments to.
    """

    expr: ex.Expression
    arg_specs: typing.Sequence[ArgumentSpec]

    @classmethod
    def from_callable(
        cls, func: typing.Callable, unpack_mode: bool = False
    ) -> CallableExpression:
        sig = inspect.signature(func)
        arg_specs = []
        for name, param in sig.parameters.items():
            is_varargs = param.kind == inspect.Parameter.VAR_POSITIONAL
            arg_specs.append(
                ArgumentSpec(
                    name=name,
                    default_value=param.default,
                    is_varargs=is_varargs,
                )
            )

        from bigframes.core.bytecode import dis_to_expr

        expr = dis_to_expr(func, unpack_mode=unpack_mode)
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

    @property
    def column_references(self) -> typing.Tuple[ids.ColumnId, ...]:
        return self.expr.column_references

    @property
    def free_variables(self) -> typing.Tuple[typing.Hashable, ...]:
        return self.expr.free_variables

    @property
    def is_const(self) -> bool:
        return self.expr.is_const

    @property
    def is_resolved(self) -> bool:
        return False

    @property
    def output_type(self) -> dtypes.ExpressionType:
        raise ValueError(
            "CallableExpression does not have a fixed output type until arguments are applied."
        )

    def bind_refs(
        self,
        bindings: typing.Mapping[ids.ColumnId, ex.Expression],
        allow_partial_bindings: bool = False,
    ) -> CallableExpression:
        return dataclasses.replace(
            self,
            expr=self.expr.bind_refs(
                bindings, allow_partial_bindings=allow_partial_bindings
            ),
        )

    def bind_variables(
        self,
        bindings: typing.Mapping[typing.Hashable, ex.Expression],
        allow_partial_bindings: bool = False,
    ) -> CallableExpression:
        arg_names = {spec.name for spec in self.arg_specs}
        filtered_bindings = {k: v for k, v in bindings.items() if k not in arg_names}
        return dataclasses.replace(
            self,
            expr=self.expr.bind_variables(
                filtered_bindings, allow_partial_bindings=allow_partial_bindings
            ),
        )

    def transform_children(
        self, t: typing.Callable[[ex.Expression], ex.Expression]
    ) -> ex.Expression:
        new_expr = t(self.expr)
        if new_expr != self.expr:
            return dataclasses.replace(self, expr=new_expr)
        return self


def func_to_expr(op, unpack_mode: bool = False) -> CallableExpression:
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
                is_varargs=False,
            )
            for arg in op.udf_def.signature.inputs
        ]
        return CallableExpression(expr=expr, arg_specs=arg_specs)

    elif options.experiments.enable_python_transpiler and callable(op):
        return CallableExpression.from_callable(op, unpack_mode=unpack_mode)

    else:
        raise TypeError(f"Unsupported function type: {op}")
