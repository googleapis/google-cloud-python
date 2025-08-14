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

import bigframes_vendored.constants as constants
import sqlglot.expressions as sge

from bigframes import dtypes
from bigframes import operations as ops
from bigframes.core.compile.sqlglot.expressions.op_registration import OpRegistration
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr

BINARY_OP_REGISTRATION = OpRegistration()


def compile(op: ops.BinaryOp, left: TypedExpr, right: TypedExpr) -> sge.Expression:
    return BINARY_OP_REGISTRATION[op](op, left, right)


# TODO: add parenthesize for operators
@BINARY_OP_REGISTRATION.register(ops.add_op)
def _(op, left: TypedExpr, right: TypedExpr) -> sge.Expression:
    if left.dtype == dtypes.STRING_DTYPE and right.dtype == dtypes.STRING_DTYPE:
        # String addition
        return sge.Concat(expressions=[left.expr, right.expr])

    if dtypes.is_numeric(left.dtype) and dtypes.is_numeric(right.dtype):
        left_expr = left.expr
        if left.dtype == dtypes.BOOL_DTYPE:
            left_expr = sge.Cast(this=left_expr, to="INT64")
        right_expr = right.expr
        if right.dtype == dtypes.BOOL_DTYPE:
            right_expr = sge.Cast(this=right_expr, to="INT64")
        return sge.Add(this=left_expr, expression=right_expr)

    if (
        dtypes.is_time_or_date_like(left.dtype)
        and right.dtype == dtypes.TIMEDELTA_DTYPE
    ):
        left_expr = left.expr
        if left.dtype == dtypes.DATE_DTYPE:
            left_expr = sge.Cast(this=left_expr, to="DATETIME")
        return sge.TimestampAdd(
            this=left_expr, expression=right.expr, unit=sge.Var(this="MICROSECOND")
        )
    if (
        dtypes.is_time_or_date_like(right.dtype)
        and left.dtype == dtypes.TIMEDELTA_DTYPE
    ):
        right_expr = right.expr
        if right.dtype == dtypes.DATE_DTYPE:
            right_expr = sge.Cast(this=right_expr, to="DATETIME")
        return sge.TimestampAdd(
            this=right_expr, expression=left.expr, unit=sge.Var(this="MICROSECOND")
        )
    if left.dtype == dtypes.TIMEDELTA_DTYPE and right.dtype == dtypes.TIMEDELTA_DTYPE:
        return sge.Add(this=left.expr, expression=right.expr)

    raise TypeError(
        f"Cannot add type {left.dtype} and {right.dtype}. {constants.FEEDBACK_LINK}"
    )


@BINARY_OP_REGISTRATION.register(ops.div_op)
def _(op, left: TypedExpr, right: TypedExpr) -> sge.Expression:
    left_expr = left.expr
    if left.dtype == dtypes.BOOL_DTYPE:
        left_expr = sge.Cast(this=left_expr, to="INT64")
    right_expr = right.expr
    if right.dtype == dtypes.BOOL_DTYPE:
        right_expr = sge.Cast(this=right_expr, to="INT64")

    result = sge.func("IEEE_DIVIDE", left_expr, right_expr)
    if left.dtype == dtypes.TIMEDELTA_DTYPE and dtypes.is_numeric(right.dtype):
        return sge.Cast(this=sge.Floor(this=result), to="INT64")
    else:
        return result


@BINARY_OP_REGISTRATION.register(ops.ge_op)
def _(op, left: TypedExpr, right: TypedExpr) -> sge.Expression:
    return sge.GTE(this=left.expr, expression=right.expr)


@BINARY_OP_REGISTRATION.register(ops.JSONSet)
def _(op, left: TypedExpr, right: TypedExpr) -> sge.Expression:
    return sge.func("JSON_SET", left.expr, sge.convert(op.json_path), right.expr)


@BINARY_OP_REGISTRATION.register(ops.mul_op)
def _(op, left: TypedExpr, right: TypedExpr) -> sge.Expression:
    left_expr = left.expr
    if left.dtype == dtypes.BOOL_DTYPE:
        left_expr = sge.Cast(this=left_expr, to="INT64")
    right_expr = right.expr
    if right.dtype == dtypes.BOOL_DTYPE:
        right_expr = sge.Cast(this=right_expr, to="INT64")

    result = sge.Mul(this=left_expr, expression=right_expr)

    if (dtypes.is_numeric(left.dtype) and right.dtype == dtypes.TIMEDELTA_DTYPE) or (
        left.dtype == dtypes.TIMEDELTA_DTYPE and dtypes.is_numeric(right.dtype)
    ):
        return sge.Cast(this=sge.Floor(this=result), to="INT64")
    else:
        return result


@BINARY_OP_REGISTRATION.register(ops.sub_op)
def _(op, left: TypedExpr, right: TypedExpr) -> sge.Expression:
    if dtypes.is_numeric(left.dtype) and dtypes.is_numeric(right.dtype):
        left_expr = left.expr
        if left.dtype == dtypes.BOOL_DTYPE:
            left_expr = sge.Cast(this=left_expr, to="INT64")
        right_expr = right.expr
        if right.dtype == dtypes.BOOL_DTYPE:
            right_expr = sge.Cast(this=right_expr, to="INT64")
        return sge.Sub(this=left_expr, expression=right_expr)

    if (
        dtypes.is_time_or_date_like(left.dtype)
        and right.dtype == dtypes.TIMEDELTA_DTYPE
    ):
        left_expr = left.expr
        if left.dtype == dtypes.DATE_DTYPE:
            left_expr = sge.Cast(this=left_expr, to="DATETIME")
        return sge.TimestampSub(
            this=left_expr, expression=right.expr, unit=sge.Var(this="MICROSECOND")
        )
    if dtypes.is_time_or_date_like(left.dtype) and dtypes.is_time_or_date_like(
        right.dtype
    ):
        left_expr = left.expr
        if left.dtype == dtypes.DATE_DTYPE:
            left_expr = sge.Cast(this=left_expr, to="DATETIME")
        right_expr = right.expr
        if right.dtype == dtypes.DATE_DTYPE:
            right_expr = sge.Cast(this=right_expr, to="DATETIME")
        return sge.TimestampDiff(
            this=left_expr, expression=right_expr, unit=sge.Var(this="MICROSECOND")
        )

    if left.dtype == dtypes.TIMEDELTA_DTYPE and right.dtype == dtypes.TIMEDELTA_DTYPE:
        return sge.Sub(this=left.expr, expression=right.expr)

    raise TypeError(
        f"Cannot subtract type {left.dtype} and {right.dtype}. {constants.FEEDBACK_LINK}"
    )
