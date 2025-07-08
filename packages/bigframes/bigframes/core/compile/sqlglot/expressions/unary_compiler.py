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

import sqlglot
import sqlglot.expressions as sge

from bigframes import operations as ops
from bigframes.core.compile.sqlglot.expressions.op_registration import OpRegistration
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr

UNARY_OP_REGISTRATION = OpRegistration()


def compile(op: ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return UNARY_OP_REGISTRATION[op](op, expr)


@UNARY_OP_REGISTRATION.register(ops.ArrayToStringOp)
def _(op: ops.ArrayToStringOp, expr: TypedExpr) -> sge.Expression:
    return sge.ArrayToString(this=expr.expr, expression=f"'{op.delimiter}'")


@UNARY_OP_REGISTRATION.register(ops.ArrayIndexOp)
def _(op: ops.ArrayIndexOp, expr: TypedExpr) -> sge.Expression:
    return sge.Bracket(
        this=expr.expr,
        expressions=[sge.Literal.number(op.index)],
        safe=True,
        offset=False,
    )


@UNARY_OP_REGISTRATION.register(ops.ArraySliceOp)
def _(op: ops.ArraySliceOp, expr: TypedExpr) -> sge.Expression:
    slice_idx = sqlglot.to_identifier("slice_idx")

    conditions: typing.List[sge.Predicate] = [slice_idx >= op.start]

    if op.stop is not None:
        conditions.append(slice_idx < op.stop)

    # local name for each element in the array
    el = sqlglot.to_identifier("el")

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


# JSON Ops
@UNARY_OP_REGISTRATION.register(ops.JSONExtract)
def _(op: ops.JSONExtract, expr: TypedExpr) -> sge.Expression:
    return sge.func("JSON_EXTRACT", expr.expr, sge.convert(op.json_path))


@UNARY_OP_REGISTRATION.register(ops.JSONExtractArray)
def _(op: ops.JSONExtractArray, expr: TypedExpr) -> sge.Expression:
    return sge.func("JSON_EXTRACT_ARRAY", expr.expr, sge.convert(op.json_path))


@UNARY_OP_REGISTRATION.register(ops.JSONExtractStringArray)
def _(op: ops.JSONExtractStringArray, expr: TypedExpr) -> sge.Expression:
    return sge.func("JSON_EXTRACT_STRING_ARRAY", expr.expr, sge.convert(op.json_path))


@UNARY_OP_REGISTRATION.register(ops.JSONQuery)
def _(op: ops.JSONQuery, expr: TypedExpr) -> sge.Expression:
    return sge.func("JSON_QUERY", expr.expr, sge.convert(op.json_path))


@UNARY_OP_REGISTRATION.register(ops.JSONQueryArray)
def _(op: ops.JSONQueryArray, expr: TypedExpr) -> sge.Expression:
    return sge.func("JSON_QUERY_ARRAY", expr.expr, sge.convert(op.json_path))


@UNARY_OP_REGISTRATION.register(ops.JSONValue)
def _(op: ops.JSONValue, expr: TypedExpr) -> sge.Expression:
    return sge.func("JSON_VALUE", expr.expr, sge.convert(op.json_path))


@UNARY_OP_REGISTRATION.register(ops.JSONValueArray)
def _(op: ops.JSONValueArray, expr: TypedExpr) -> sge.Expression:
    return sge.func("JSON_VALUE_ARRAY", expr.expr, sge.convert(op.json_path))


@UNARY_OP_REGISTRATION.register(ops.ParseJSON)
def _(op: ops.ParseJSON, expr: TypedExpr) -> sge.Expression:
    return sge.func("PARSE_JSON", expr.expr)


@UNARY_OP_REGISTRATION.register(ops.ToJSONString)
def _(op: ops.ToJSONString, expr: TypedExpr) -> sge.Expression:
    return sge.func("TO_JSON_STRING", expr.expr)
