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

import sqlglot.expressions as sge

from bigframes.core import expression
from bigframes.core.compile.sqlglot.expressions import (
    binary_compiler,
    nary_compiler,
    ternary_compiler,
    typed_expr,
    unary_compiler,
)
import bigframes.core.compile.sqlglot.sqlglot_ir as ir
import bigframes.operations as ops


@functools.singledispatch
def compile_scalar_expression(
    expression: expression.Expression,
) -> sge.Expression:
    """Compiles BigFrames scalar expression into SQLGlot expression."""
    raise ValueError(f"Can't compile unrecognized node: {expression}")


@compile_scalar_expression.register
def compile_deref_expression(expr: expression.DerefOp) -> sge.Expression:
    return sge.Column(this=sge.to_identifier(expr.id.sql, quoted=True))


@compile_scalar_expression.register
def compile_constant_expression(
    expr: expression.ScalarConstantExpression,
) -> sge.Expression:
    return ir._literal(expr.value, expr.dtype)


@compile_scalar_expression.register
def compile_op_expression(expr: expression.OpExpression) -> sge.Expression:
    # Non-recursively compiles the children scalar expressions.
    args = tuple(
        typed_expr.TypedExpr(compile_scalar_expression(input), input.output_type)
        for input in expr.inputs
    )

    op = expr.op
    if isinstance(op, ops.UnaryOp):
        return unary_compiler.compile(op, args[0])
    elif isinstance(op, ops.BinaryOp):
        return binary_compiler.compile(op, args[0], args[1])
    elif isinstance(op, ops.TernaryOp):
        return ternary_compiler.compile(op, args[0], args[1], args[2])
    elif isinstance(op, ops.NaryOp):
        return nary_compiler.compile(op, *args)
    else:
        raise TypeError(
            f"Operator '{op.name}' has an unrecognized arity or type "
            "and cannot be compiled."
        )
