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

register_binary_op = scalar_compiler.scalar_op_compiler.register_binary_op

# TODO: add parenthesize for operators


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


@register_binary_op(ops.eq_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    left_expr = _coerce_bool_to_int(left)
    right_expr = _coerce_bool_to_int(right)
    return sge.EQ(this=left_expr, expression=right_expr)


@register_binary_op(ops.eq_null_match_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    left_expr = left.expr
    if right.dtype != dtypes.BOOL_DTYPE:
        left_expr = _coerce_bool_to_int(left)

    right_expr = right.expr
    if left.dtype != dtypes.BOOL_DTYPE:
        right_expr = _coerce_bool_to_int(right)

    sentinel = sge.convert("$NULL_SENTINEL$")
    left_coalesce = sge.Coalesce(
        this=sge.Cast(this=left_expr, to="STRING"), expressions=[sentinel]
    )
    right_coalesce = sge.Coalesce(
        this=sge.Cast(this=right_expr, to="STRING"), expressions=[sentinel]
    )
    return sge.EQ(this=left_coalesce, expression=right_coalesce)


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


@register_binary_op(ops.ge_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    left_expr = _coerce_bool_to_int(left)
    right_expr = _coerce_bool_to_int(right)
    return sge.GTE(this=left_expr, expression=right_expr)


@register_binary_op(ops.gt_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    left_expr = _coerce_bool_to_int(left)
    right_expr = _coerce_bool_to_int(right)
    return sge.GT(this=left_expr, expression=right_expr)


@register_binary_op(ops.JSONSet, pass_op=True)
def _(left: TypedExpr, right: TypedExpr, op) -> sge.Expression:
    return sge.func("JSON_SET", left.expr, sge.convert(op.json_path), right.expr)


@register_binary_op(ops.lt_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    left_expr = _coerce_bool_to_int(left)
    right_expr = _coerce_bool_to_int(right)
    return sge.LT(this=left_expr, expression=right_expr)


@register_binary_op(ops.le_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    left_expr = _coerce_bool_to_int(left)
    right_expr = _coerce_bool_to_int(right)
    return sge.LTE(this=left_expr, expression=right_expr)


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


@register_binary_op(ops.ne_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    left_expr = _coerce_bool_to_int(left)
    right_expr = _coerce_bool_to_int(right)
    return sge.NEQ(this=left_expr, expression=right_expr)


@register_binary_op(ops.obj_make_ref_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    return sge.func("OBJ.MAKE_REF", left.expr, right.expr)


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
