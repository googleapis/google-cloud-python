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

import typing

import bigframes_vendored.sqlglot.expressions as sge
import pandas as pd

from bigframes import dtypes
from bigframes import operations as ops
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr
import bigframes.core.compile.sqlglot.scalar_compiler as scalar_compiler

register_unary_op = scalar_compiler.scalar_op_compiler.register_unary_op
register_binary_op = scalar_compiler.scalar_op_compiler.register_binary_op


@register_unary_op(ops.IsInOp, pass_op=True)
def _(expr: TypedExpr, op: ops.IsInOp) -> sge.Expression:
    values = []
    is_numeric_expr = dtypes.is_numeric(expr.dtype, include_bool=False)
    for value in op.values:
        if _is_null(value):
            continue
        dtype = dtypes.bigframes_type(type(value))
        if (
            expr.dtype == dtype
            or is_numeric_expr
            and dtypes.is_numeric(dtype, include_bool=False)
        ):
            values.append(sge.convert(value))

    if op.match_nulls:
        contains_nulls = any(_is_null(value) for value in op.values)
        if contains_nulls:
            if len(values) == 0:
                return sge.Is(this=expr.expr, expression=sge.Null())
            return sge.Is(this=expr.expr, expression=sge.Null()) | sge.In(
                this=expr.expr, expressions=values
            )

    if len(values) == 0:
        return sge.convert(False)

    return sge.func(
        "COALESCE", sge.In(this=expr.expr, expressions=values), sge.convert(False)
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


@register_binary_op(ops.maximum_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    return sge.Greatest(expressions=[left.expr, right.expr])


@register_binary_op(ops.minimum_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    return sge.Least(this=left.expr, expressions=right.expr)


@register_binary_op(ops.ne_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    left_expr = _coerce_bool_to_int(left)
    right_expr = _coerce_bool_to_int(right)
    return sge.NEQ(this=left_expr, expression=right_expr)


# Helpers
def _is_null(value) -> bool:
    # float NaN/inf should be treated as distinct from 'true' null values
    return typing.cast(bool, pd.isna(value)) and not isinstance(value, float)


def _coerce_bool_to_int(typed_expr: TypedExpr) -> sge.Expression:
    """Coerce boolean expression to integer."""
    if typed_expr.dtype == dtypes.BOOL_DTYPE:
        return sge.Cast(this=typed_expr.expr, to="INT64")
    return typed_expr.expr
