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
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr
import bigframes.core.compile.sqlglot.scalar_compiler as scalar_compiler

register_unary_op = scalar_compiler.scalar_op_compiler.register_unary_op
register_binary_op = scalar_compiler.scalar_op_compiler.register_binary_op


@register_unary_op(ops.JSONExtract, pass_op=True)
def _(expr: TypedExpr, op: ops.JSONExtract) -> sge.Expression:
    return sge.func("JSON_EXTRACT", expr.expr, sge.convert(op.json_path))


@register_unary_op(ops.JSONExtractArray, pass_op=True)
def _(expr: TypedExpr, op: ops.JSONExtractArray) -> sge.Expression:
    return sge.func("JSON_EXTRACT_ARRAY", expr.expr, sge.convert(op.json_path))


@register_unary_op(ops.JSONExtractStringArray, pass_op=True)
def _(expr: TypedExpr, op: ops.JSONExtractStringArray) -> sge.Expression:
    return sge.func("JSON_EXTRACT_STRING_ARRAY", expr.expr, sge.convert(op.json_path))


@register_unary_op(ops.JSONQuery, pass_op=True)
def _(expr: TypedExpr, op: ops.JSONQuery) -> sge.Expression:
    return sge.func("JSON_QUERY", expr.expr, sge.convert(op.json_path))


@register_unary_op(ops.JSONQueryArray, pass_op=True)
def _(expr: TypedExpr, op: ops.JSONQueryArray) -> sge.Expression:
    return sge.func("JSON_QUERY_ARRAY", expr.expr, sge.convert(op.json_path))


@register_unary_op(ops.JSONValue, pass_op=True)
def _(expr: TypedExpr, op: ops.JSONValue) -> sge.Expression:
    return sge.func("JSON_VALUE", expr.expr, sge.convert(op.json_path))


@register_unary_op(ops.JSONValueArray, pass_op=True)
def _(expr: TypedExpr, op: ops.JSONValueArray) -> sge.Expression:
    return sge.func("JSON_VALUE_ARRAY", expr.expr, sge.convert(op.json_path))


@register_unary_op(ops.ParseJSON)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("PARSE_JSON", expr.expr)


@register_unary_op(ops.ToJSONString)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("TO_JSON_STRING", expr.expr)


@register_binary_op(ops.JSONSet, pass_op=True)
def _(left: TypedExpr, right: TypedExpr, op) -> sge.Expression:
    return sge.func("JSON_SET", left.expr, sge.convert(op.json_path), right.expr)
