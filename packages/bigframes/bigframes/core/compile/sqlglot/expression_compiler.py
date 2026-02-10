# Copyright 2025 Google LLC
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

import functools
import typing

import bigframes_vendored.sqlglot.expressions as sge

import bigframes.core.agg_expressions as agg_exprs
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr
import bigframes.core.compile.sqlglot.sqlglot_ir as ir
import bigframes.core.expression as ex
import bigframes.operations as ops


class ExpressionCompiler:
    # Mapping of operation name to implemenations
    _registry: dict[
        str,
        typing.Callable[[typing.Sequence[TypedExpr], ops.RowOp], sge.Expression],
    ] = {}

    # A set of SQLGlot classes that may need to be parenthesized
    SQLGLOT_NEEDS_PARENS = {
        # Numeric operations
        sge.Add,
        sge.Sub,
        sge.Mul,
        sge.Div,
        sge.Mod,
        sge.Pow,
        # Comparison operations
        sge.GTE,
        sge.GT,
        sge.LTE,
        sge.LT,
        sge.EQ,
        sge.NEQ,
        # Logical operations
        sge.And,
        sge.Or,
        sge.Xor,
        # Bitwise operations
        sge.BitwiseAnd,
        sge.BitwiseOr,
        sge.BitwiseXor,
        sge.BitwiseLeftShift,
        sge.BitwiseRightShift,
        sge.BitwiseNot,
        # Other operations
        sge.Is,
    }

    @functools.singledispatchmethod
    def compile_expression(
        self,
        expression: ex.Expression,
    ) -> sge.Expression:
        """Compiles BigFrames scalar expression into SQLGlot expression."""
        raise NotImplementedError(f"Unrecognized expression: {expression}")

    @compile_expression.register
    def _(self, expr: ex.DerefOp) -> sge.Expression:
        return sge.Column(this=sge.to_identifier(expr.id.sql, quoted=True))

    @compile_expression.register
    def _(self, expr: ex.ScalarConstantExpression) -> sge.Expression:
        return ir._literal(expr.value, expr.dtype)

    @compile_expression.register
    def _(self, expr: agg_exprs.WindowExpression) -> sge.Expression:
        import bigframes.core.compile.sqlglot.aggregate_compiler as agg_compile

        return agg_compile.compile_analytic(
            expr.analytic_expr,
            expr.window,
        )

    @compile_expression.register
    def _(self, expr: ex.OpExpression) -> sge.Expression:
        # Non-recursively compiles the children scalar expressions.
        inputs = tuple(
            TypedExpr(self.compile_expression(sub_expr), sub_expr.output_type)
            for sub_expr in expr.inputs
        )
        return self.compile_row_op(expr.op, inputs)

    def compile_row_op(
        self, op: ops.RowOp, inputs: typing.Sequence[TypedExpr]
    ) -> sge.Expression:
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

        def decorator(impl: typing.Callable[..., sge.Expression]):
            def normalized_impl(args: typing.Sequence[TypedExpr], op: ops.RowOp):
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

        def decorator(impl: typing.Callable[..., sge.Expression]):
            def normalized_impl(args: typing.Sequence[TypedExpr], op: ops.RowOp):
                left = self._add_parentheses(args[0])
                right = self._add_parentheses(args[1])
                if pass_op:
                    return impl(left, right, op)
                else:
                    return impl(left, right)

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

        def decorator(impl: typing.Callable[..., sge.Expression]):
            def normalized_impl(args: typing.Sequence[TypedExpr], op: ops.RowOp):
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

        def decorator(impl: typing.Callable[..., sge.Expression]):
            def normalized_impl(args: typing.Sequence[TypedExpr], op: ops.RowOp):
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
        impl: typing.Callable[[typing.Sequence[TypedExpr], ops.RowOp], sge.Expression],
    ):
        if op_name in self._registry:
            raise ValueError(f"Operation name {op_name} already registered")
        self._registry[op_name] = impl

    @classmethod
    def _add_parentheses(cls, expr: TypedExpr) -> TypedExpr:
        if type(expr.expr) in cls.SQLGLOT_NEEDS_PARENS:
            return TypedExpr(sge.paren(expr.expr, copy=False), expr.dtype)
        return expr


# Singleton compiler
expression_compiler = ExpressionCompiler()
