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

import bigframes_vendored.sqlglot as sg
import bigframes_vendored.sqlglot.expressions as sge

from bigframes import operations as ops
import bigframes.core.compile.sqlglot.expression_compiler as expression_compiler
from bigframes.core.compile.sqlglot.expressions.string_ops import (
    string_index,
    string_slice,
)
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr
import bigframes.dtypes as dtypes

register_unary_op = expression_compiler.expression_compiler.register_unary_op
register_nary_op = expression_compiler.expression_compiler.register_nary_op


@register_unary_op(ops.ArrayIndexOp, pass_op=True)
def _(expr: TypedExpr, op: ops.ArrayIndexOp) -> sge.Expression:
    if expr.dtype == dtypes.STRING_DTYPE:
        return string_index(expr, op.index)

    return sge.Bracket(
        this=expr.expr,
        expressions=[sge.convert(op.index)],
        safe=True,
        offset=False,
    )


@register_unary_op(ops.ArrayReduceOp, pass_op=True)
def _(expr: TypedExpr, op: ops.ArrayReduceOp) -> sge.Expression:
    sub_expr = sg.to_identifier("bf_arr_reduce_uid")
    sub_type = dtypes.get_array_inner_type(expr.dtype)

    if op.aggregation.order_independent:
        from bigframes.core.compile.sqlglot.aggregations import unary_compiler

        agg_expr = unary_compiler.compile(op.aggregation, TypedExpr(sub_expr, sub_type))
    else:
        from bigframes.core.compile.sqlglot.aggregations import ordered_unary_compiler

        agg_expr = ordered_unary_compiler.compile(
            op.aggregation, TypedExpr(sub_expr, sub_type)
        )

    return (
        sge.select(agg_expr)
        .from_(
            sge.Unnest(
                expressions=[expr.expr],
                alias=sge.TableAlias(columns=[sub_expr]),
            )
        )
        .subquery()
    )


@register_unary_op(ops.ArraySliceOp, pass_op=True)
def _(expr: TypedExpr, op: ops.ArraySliceOp) -> sge.Expression:
    if expr.dtype == dtypes.STRING_DTYPE:
        return string_slice(expr, op.start, op.stop)
    else:
        return _array_slice(expr, op)


@register_unary_op(ops.ArrayToStringOp, pass_op=True)
def _(expr: TypedExpr, op: ops.ArrayToStringOp) -> sge.Expression:
    return sge.ArrayToString(this=expr.expr, expression=f"'{op.delimiter}'")


@register_nary_op(ops.ToArrayOp)
def _(*exprs: TypedExpr) -> sge.Expression:
    do_upcast_bool = any(
        dtypes.is_numeric(expr.dtype, include_bool=False) for expr in exprs
    )
    if do_upcast_bool:
        sg_exprs = [_coerce_bool_to_int(expr) for expr in exprs]
    else:
        sg_exprs = [expr.expr for expr in exprs]
    return sge.Array(expressions=sg_exprs)


def _coerce_bool_to_int(typed_expr: TypedExpr) -> sge.Expression:
    """Coerce boolean expression to integer."""
    if typed_expr.dtype == dtypes.BOOL_DTYPE:
        return sge.Cast(this=typed_expr.expr, to="INT64")
    return typed_expr.expr


def _string_slice(expr: TypedExpr, op: ops.ArraySliceOp) -> sge.Expression:
    # local name for each element in the array
    el = sg.to_identifier("el")
    # local name for the index in the array
    slice_idx = sg.to_identifier("slice_idx")

    conditions: typing.List[sge.Predicate] = [slice_idx >= op.start]
    if op.stop is not None:
        conditions.append(slice_idx < op.stop)

    selected_elements = (
        sge.select(el)
        .from_(
            sge.Unnest(
                expressions=[expr.expr],
                alias=sge.TableAlias(columns=[el]),
                offset=slice_idx,
            )
        )
        .where(*conditions)
    )

    return sge.array(selected_elements)


def _array_slice(expr: TypedExpr, op: ops.ArraySliceOp) -> sge.Expression:
    # local name for each element in the array
    el = sg.to_identifier("el")
    # local name for the index in the array
    slice_idx = sg.to_identifier("slice_idx")

    conditions: typing.List[sge.Predicate] = [slice_idx >= op.start]
    if op.stop is not None:
        conditions.append(slice_idx < op.stop)

    selected_elements = (
        sge.select(el)
        .from_(
            sge.Unnest(
                expressions=[expr.expr],
                alias=sge.TableAlias(columns=[el]),
                offset=slice_idx,
            )
        )
        .where(*conditions)
    )

    return sge.array(selected_elements)
