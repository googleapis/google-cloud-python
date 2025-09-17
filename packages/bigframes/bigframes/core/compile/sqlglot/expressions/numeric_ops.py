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

import sqlglot.expressions as sge

from bigframes import operations as ops
import bigframes.core.compile.sqlglot.expressions.constants as constants
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr
import bigframes.core.compile.sqlglot.scalar_compiler as scalar_compiler

register_unary_op = scalar_compiler.scalar_op_compiler.register_unary_op


@register_unary_op(ops.abs_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Abs(this=expr.expr)


@register_unary_op(ops.arccosh_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=expr.expr < sge.convert(1),
                true=constants._NAN,
            )
        ],
        default=sge.func("ACOSH", expr.expr),
    )


@register_unary_op(ops.arccos_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=sge.func("ABS", expr.expr) > sge.convert(1),
                true=constants._NAN,
            )
        ],
        default=sge.func("ACOS", expr.expr),
    )


@register_unary_op(ops.arcsin_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=sge.func("ABS", expr.expr) > sge.convert(1),
                true=constants._NAN,
            )
        ],
        default=sge.func("ASIN", expr.expr),
    )


@register_unary_op(ops.arcsinh_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("ASINH", expr.expr)


@register_unary_op(ops.arctan_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("ATAN", expr.expr)


@register_unary_op(ops.arctanh_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=sge.func("ABS", expr.expr) > sge.convert(1),
                true=constants._NAN,
            )
        ],
        default=sge.func("ATANH", expr.expr),
    )


@register_unary_op(ops.ceil_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Ceil(this=expr.expr)


@register_unary_op(ops.cos_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("COS", expr.expr)


@register_unary_op(ops.cosh_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=sge.func("ABS", expr.expr) > sge.convert(709.78),
                true=constants._INF,
            )
        ],
        default=sge.func("COSH", expr.expr),
    )


@register_unary_op(ops.exp_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=expr.expr > constants._FLOAT64_EXP_BOUND,
                true=constants._INF,
            )
        ],
        default=sge.func("EXP", expr.expr),
    )


@register_unary_op(ops.expm1_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=expr.expr > constants._FLOAT64_EXP_BOUND,
                true=constants._INF,
            )
        ],
        default=sge.func("EXP", expr.expr),
    ) - sge.convert(1)


@register_unary_op(ops.floor_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Floor(this=expr.expr)


@register_unary_op(ops.invert_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.BitwiseNot(this=expr.expr)


@register_unary_op(ops.ln_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=expr.expr < sge.convert(0),
                true=constants._NAN,
            )
        ],
        default=sge.Ln(this=expr.expr),
    )


@register_unary_op(ops.log10_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=expr.expr < sge.convert(0),
                true=constants._NAN,
            )
        ],
        default=sge.Log(this=expr.expr, expression=sge.convert(10)),
    )


@register_unary_op(ops.log1p_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=expr.expr < sge.convert(-1),
                true=constants._NAN,
            )
        ],
        default=sge.Ln(this=sge.convert(1) + expr.expr),
    )


@register_unary_op(ops.neg_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Neg(this=expr.expr)


@register_unary_op(ops.pos_op)
def _(expr: TypedExpr) -> sge.Expression:
    return expr.expr


@register_unary_op(ops.sqrt_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=expr.expr < sge.convert(0),
                true=constants._NAN,
            )
        ],
        default=sge.Sqrt(this=expr.expr),
    )


@register_unary_op(ops.sin_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("SIN", expr.expr)


@register_unary_op(ops.sinh_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=sge.func("ABS", expr.expr) > constants._FLOAT64_EXP_BOUND,
                true=sge.func("SIGN", expr.expr) * constants._INF,
            )
        ],
        default=sge.func("SINH", expr.expr),
    )


@register_unary_op(ops.tan_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("TAN", expr.expr)


@register_unary_op(ops.tanh_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("TANH", expr.expr)
