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

import dataclasses
import functools

import sqlglot.expressions as sge

from bigframes import dtypes
from bigframes.core import expression
import bigframes.core.compile.sqlglot.sqlglot_ir as ir
import bigframes.operations as ops


@dataclasses.dataclass(frozen=True)
class TypedExpr:
    """SQLGlot expression with type."""

    expr: sge.Expression
    dtype: dtypes.ExpressionType


@functools.singledispatch
def compile_scalar_expression(
    expression: expression.Expression,
) -> sge.Expression:
    """Compiles BigFrames scalar expression into SQLGlot expression."""
    raise ValueError(f"Can't compile unrecognized node: {expression}")


@compile_scalar_expression.register
def compile_deref_expression(expr: expression.DerefOp) -> sge.Expression:
    return sge.ColumnDef(this=sge.to_identifier(expr.id.sql, quoted=True))


@compile_scalar_expression.register
def compile_field_ref_expression(
    expr: expression.SchemaFieldRefExpression,
) -> sge.Expression:
    return sge.ColumnDef(this=sge.to_identifier(expr.field.id.sql, quoted=True))


@compile_scalar_expression.register
def compile_constant_expression(
    expr: expression.ScalarConstantExpression,
) -> sge.Expression:
    return ir._literal(expr.value, expr.dtype)


@compile_scalar_expression.register
def compile_op_expression(expr: expression.OpExpression) -> sge.Expression:
    # Non-recursively compiles the children scalar expressions.
    args = tuple(
        TypedExpr(compile_scalar_expression(input), input.output_type)
        for input in expr.inputs
    )

    op = expr.op
    op_name = expr.op.__class__.__name__
    method_name = f"compile_{op_name.lower()}"
    method = globals().get(method_name, None)
    if method is None:
        raise ValueError(
            f"Compilation method '{method_name}' not found for operator '{op_name}'."
        )

    if isinstance(op, ops.UnaryOp):
        return method(op, args[0])
    elif isinstance(op, ops.BinaryOp):
        return method(op, args[0], args[1])
    elif isinstance(op, ops.TernaryOp):
        return method(op, args[0], args[1], args[2])
    elif isinstance(op, ops.NaryOp):
        return method(op, *args)
    else:
        raise TypeError(
            f"Operator '{op_name}' has an unrecognized arity or type "
            "and cannot be compiled."
        )


# TODO: add parenthesize for operators
def compile_addop(op: ops.AddOp, left: TypedExpr, right: TypedExpr) -> sge.Expression:
    if left.dtype == dtypes.STRING_DTYPE and right.dtype == dtypes.STRING_DTYPE:
        # String addition
        return sge.Concat(expressions=[left.expr, right.expr])

    # Numerical addition
    return sge.Add(this=left.expr, expression=right.expr)
