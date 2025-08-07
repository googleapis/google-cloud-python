# Copyright 2023 Google LLC
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

"""To avoid circular imports, this module should _not_ depend on any ops."""

from __future__ import annotations

import functools
import typing
from typing import TYPE_CHECKING

import bigframes_vendored.ibis.expr.types as ibis_types

import bigframes.core.compile.ibis_types
import bigframes.core.expression as ex

if TYPE_CHECKING:
    import bigframes.operations as ops


class ScalarOpCompiler:
    # Mapping of operation name to implemenations
    _registry: dict[
        str,
        typing.Callable[
            [typing.Sequence[ibis_types.Value], ops.RowOp], ibis_types.Value
        ],
    ] = {}

    @functools.singledispatchmethod
    def compile_expression(
        self,
        expression: ex.Expression,
        bindings: typing.Dict[str, ibis_types.Value],
    ) -> ibis_types.Value:
        raise NotImplementedError(f"Unrecognized expression: {expression}")

    @compile_expression.register
    def _(
        self,
        expression: ex.ScalarConstantExpression,
        bindings: typing.Dict[str, ibis_types.Value],
    ) -> ibis_types.Value:
        return bigframes.core.compile.ibis_types.literal_to_ibis_scalar(
            expression.value, expression.dtype
        )

    @compile_expression.register
    def _(
        self,
        expression: ex.DerefOp,
        bindings: typing.Dict[str, ibis_types.Value],
    ) -> ibis_types.Value:
        if expression.id.sql not in bindings:
            raise ValueError(f"Could not resolve unbound variable {expression.id}")
        else:
            return bindings[expression.id.sql]

    @compile_expression.register
    def _(
        self,
        expression: ex.OpExpression,
        bindings: typing.Dict[str, ibis_types.Value],
    ) -> ibis_types.Value:
        inputs = [
            self.compile_expression(sub_expr, bindings)
            for sub_expr in expression.inputs
        ]
        return self.compile_row_op(expression.op, inputs)

    def compile_row_op(
        self, op: ops.RowOp, inputs: typing.Sequence[ibis_types.Value]
    ) -> ibis_types.Value:
        impl = self._registry[op.name]
        return impl(inputs, op)

    def register_unary_op(
        self,
        op_ref: typing.Union[ops.UnaryOp, type[ops.UnaryOp]],
        pass_op: bool = False,
    ):
        """
        Decorator to register a unary op implementation.

        Args:
            op_ref (UnaryOp or UnaryOp type):
                Class or instance of operator that is implemented by the decorated function.
            pass_op (bool):
                Set to true if implementation takes the operator object as the last argument.
                This is needed for parameterized ops where parameters are part of op object.
        """
        key = typing.cast(str, op_ref.name)

        def decorator(impl: typing.Callable[..., ibis_types.Value]):
            def normalized_impl(args: typing.Sequence[ibis_types.Value], op: ops.RowOp):
                if pass_op:
                    return impl(args[0], op)
                else:
                    return impl(args[0])

            self._register(key, normalized_impl)
            return impl

        return decorator

    def register_binary_op(
        self,
        op_ref: typing.Union[ops.BinaryOp, type[ops.BinaryOp]],
        pass_op: bool = False,
    ):
        """
        Decorator to register a binary op implementation.

        Args:
            op_ref (BinaryOp or BinaryOp type):
                Class or instance of operator that is implemented by the decorated function.
            pass_op (bool):
                Set to true if implementation takes the operator object as the last argument.
                This is needed for parameterized ops where parameters are part of op object.
        """
        key = typing.cast(str, op_ref.name)

        def decorator(impl: typing.Callable[..., ibis_types.Value]):
            def normalized_impl(args: typing.Sequence[ibis_types.Value], op: ops.RowOp):
                if pass_op:
                    return impl(args[0], args[1], op)
                else:
                    return impl(args[0], args[1])

            self._register(key, normalized_impl)
            return impl

        return decorator

    def register_ternary_op(
        self, op_ref: typing.Union[ops.TernaryOp, type[ops.TernaryOp]]
    ):
        """
        Decorator to register a ternary op implementation.

        Args:
            op_ref (TernaryOp or TernaryOp type):
                Class or instance of operator that is implemented by the decorated function.
        """
        key = typing.cast(str, op_ref.name)

        def decorator(impl: typing.Callable[..., ibis_types.Value]):
            def normalized_impl(args: typing.Sequence[ibis_types.Value], op: ops.RowOp):
                return impl(args[0], args[1], args[2])

            self._register(key, normalized_impl)
            return impl

        return decorator

    def register_nary_op(
        self, op_ref: typing.Union[ops.NaryOp, type[ops.NaryOp]], pass_op: bool = False
    ):
        """
        Decorator to register a nary op implementation.

        Args:
            op_ref (NaryOp or NaryOp type):
                Class or instance of operator that is implemented by the decorated function.
            pass_op (bool):
                Set to true if implementation takes the operator object as the last argument.
                This is needed for parameterized ops where parameters are part of op object.
        """
        key = typing.cast(str, op_ref.name)

        def decorator(impl: typing.Callable[..., ibis_types.Value]):
            def normalized_impl(args: typing.Sequence[ibis_types.Value], op: ops.RowOp):
                if pass_op:
                    return impl(*args, op=op)
                else:
                    return impl(*args)

            self._register(key, normalized_impl)
            return impl

        return decorator

    def _register(
        self,
        op_name: str,
        impl: typing.Callable[
            [typing.Sequence[ibis_types.Value], ops.RowOp], ibis_types.Value
        ],
    ):
        if op_name in self._registry:
            raise ValueError(f"Operation name {op_name} already registered")
        self._registry[op_name] = impl


# Singleton compiler
scalar_op_compiler = ScalarOpCompiler()
