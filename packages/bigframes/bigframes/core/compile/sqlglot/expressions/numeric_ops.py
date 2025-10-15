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

import bigframes_vendored.constants as bf_constants
import sqlglot.expressions as sge

from bigframes import dtypes
from bigframes import operations as ops
import bigframes.core.compile.sqlglot.expressions.constants as constants
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr
import bigframes.core.compile.sqlglot.scalar_compiler as scalar_compiler

register_unary_op = scalar_compiler.scalar_op_compiler.register_unary_op
register_binary_op = scalar_compiler.scalar_op_compiler.register_binary_op


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
                this=expr.expr <= sge.convert(0),
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
                this=expr.expr <= sge.convert(0),
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
                this=expr.expr <= sge.convert(-1),
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


@register_binary_op(ops.add_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    if left.dtype == dtypes.STRING_DTYPE and right.dtype == dtypes.STRING_DTYPE:
        # String addition
        return sge.Concat(expressions=[left.expr, right.expr])

    if dtypes.is_numeric(left.dtype) and dtypes.is_numeric(right.dtype):
        left_expr = _coerce_bool_to_int(left)
        right_expr = _coerce_bool_to_int(right)
        return sge.Add(this=left_expr, expression=right_expr)

    if (
        dtypes.is_time_or_date_like(left.dtype)
        and right.dtype == dtypes.TIMEDELTA_DTYPE
    ):
        left_expr = _coerce_date_to_datetime(left)
        return sge.TimestampAdd(
            this=left_expr, expression=right.expr, unit=sge.Var(this="MICROSECOND")
        )
    if (
        dtypes.is_time_or_date_like(right.dtype)
        and left.dtype == dtypes.TIMEDELTA_DTYPE
    ):
        right_expr = _coerce_date_to_datetime(right)
        return sge.TimestampAdd(
            this=right_expr, expression=left.expr, unit=sge.Var(this="MICROSECOND")
        )
    if left.dtype == dtypes.TIMEDELTA_DTYPE and right.dtype == dtypes.TIMEDELTA_DTYPE:
        return sge.Add(this=left.expr, expression=right.expr)

    raise TypeError(
        f"Cannot add type {left.dtype} and {right.dtype}. {bf_constants.FEEDBACK_LINK}"
    )


@register_binary_op(ops.div_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    left_expr = _coerce_bool_to_int(left)
    right_expr = _coerce_bool_to_int(right)

    result = sge.func("IEEE_DIVIDE", left_expr, right_expr)
    if left.dtype == dtypes.TIMEDELTA_DTYPE and dtypes.is_numeric(right.dtype):
        return sge.Cast(this=sge.Floor(this=result), to="INT64")
    else:
        return result


@register_binary_op(ops.floordiv_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    left_expr = _coerce_bool_to_int(left)
    right_expr = _coerce_bool_to_int(right)

    result: sge.Expression = sge.Cast(
        this=sge.Floor(this=sge.func("IEEE_DIVIDE", left_expr, right_expr)), to="INT64"
    )

    # DIV(N, 0) will error in bigquery, but needs to return `0` for int, and
    # `inf`` for float in BQ so we short-circuit in this case.
    # Multiplying left by zero propogates nulls.
    zero_result = (
        constants._INF
        if (left.dtype == dtypes.FLOAT_DTYPE or right.dtype == dtypes.FLOAT_DTYPE)
        else constants._ZERO
    )
    result = sge.Case(
        ifs=[
            sge.If(
                this=sge.EQ(this=right_expr, expression=constants._ZERO),
                true=zero_result * left_expr,
            )
        ],
        default=result,
    )

    if dtypes.is_numeric(right.dtype) and left.dtype == dtypes.TIMEDELTA_DTYPE:
        result = sge.Cast(this=sge.Floor(this=result), to="INT64")

    return result


@register_binary_op(ops.mod_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    # In BigQuery returned value has the same sign as X. In pandas, the sign of y is used, so we need to flip the result if sign(x) != sign(y)
    left_expr = _coerce_bool_to_int(left)
    right_expr = _coerce_bool_to_int(right)

    # BigQuery MOD function doesn't support float types, so cast to BIGNUMERIC
    if left.dtype == dtypes.FLOAT_DTYPE or right.dtype == dtypes.FLOAT_DTYPE:
        left_expr = sge.Cast(this=left_expr, to="BIGNUMERIC")
        right_expr = sge.Cast(this=right_expr, to="BIGNUMERIC")

    # MOD(N, 0) will error in bigquery, but needs to return null
    bq_mod = sge.Mod(this=left_expr, expression=right_expr)
    zero_result = (
        constants._NAN
        if (left.dtype == dtypes.FLOAT_DTYPE or right.dtype == dtypes.FLOAT_DTYPE)
        else constants._ZERO
    )
    return sge.Case(
        ifs=[
            sge.If(
                this=sge.EQ(this=right_expr, expression=constants._ZERO),
                true=zero_result * left_expr,
            ),
            sge.If(
                this=sge.and_(
                    right_expr < constants._ZERO,
                    bq_mod > constants._ZERO,
                ),
                true=right_expr + bq_mod,
            ),
            sge.If(
                this=sge.and_(
                    right_expr > constants._ZERO,
                    bq_mod < constants._ZERO,
                ),
                true=right_expr + bq_mod,
            ),
        ],
        default=bq_mod,
    )


@register_binary_op(ops.mul_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    left_expr = _coerce_bool_to_int(left)
    right_expr = _coerce_bool_to_int(right)

    result = sge.Mul(this=left_expr, expression=right_expr)

    if (dtypes.is_numeric(left.dtype) and right.dtype == dtypes.TIMEDELTA_DTYPE) or (
        left.dtype == dtypes.TIMEDELTA_DTYPE and dtypes.is_numeric(right.dtype)
    ):
        return sge.Cast(this=sge.Floor(this=result), to="INT64")
    else:
        return result


@register_binary_op(ops.sub_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    if dtypes.is_numeric(left.dtype) and dtypes.is_numeric(right.dtype):
        left_expr = _coerce_bool_to_int(left)
        right_expr = _coerce_bool_to_int(right)
        return sge.Sub(this=left_expr, expression=right_expr)

    if (
        dtypes.is_time_or_date_like(left.dtype)
        and right.dtype == dtypes.TIMEDELTA_DTYPE
    ):
        left_expr = _coerce_date_to_datetime(left)
        return sge.TimestampSub(
            this=left_expr, expression=right.expr, unit=sge.Var(this="MICROSECOND")
        )
    if dtypes.is_time_or_date_like(left.dtype) and dtypes.is_time_or_date_like(
        right.dtype
    ):
        left_expr = _coerce_date_to_datetime(left)
        right_expr = _coerce_date_to_datetime(right)
        return sge.TimestampDiff(
            this=left_expr, expression=right_expr, unit=sge.Var(this="MICROSECOND")
        )

    if left.dtype == dtypes.TIMEDELTA_DTYPE and right.dtype == dtypes.TIMEDELTA_DTYPE:
        return sge.Sub(this=left.expr, expression=right.expr)

    raise TypeError(
        f"Cannot subtract type {left.dtype} and {right.dtype}. {bf_constants.FEEDBACK_LINK}"
    )


def _coerce_bool_to_int(typed_expr: TypedExpr) -> sge.Expression:
    """Coerce boolean expression to integer."""
    if typed_expr.dtype == dtypes.BOOL_DTYPE:
        return sge.Cast(this=typed_expr.expr, to="INT64")
    return typed_expr.expr


def _coerce_date_to_datetime(typed_expr: TypedExpr) -> sge.Expression:
    """Coerce date expression to datetime."""
    if typed_expr.dtype == dtypes.DATE_DTYPE:
        return sge.Cast(this=typed_expr.expr, to="DATETIME")
    return typed_expr.expr
