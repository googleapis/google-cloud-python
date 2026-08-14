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

import bigframes_vendored.sqlglot.expressions as sge

import bigframes.core.compile.sqlglot.expression_compiler as expression_compiler
from bigframes import dtypes
from bigframes import operations as ops
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr

register_unary_op = expression_compiler.expression_compiler.register_unary_op
register_binary_op = expression_compiler.expression_compiler.register_binary_op


@register_unary_op(ops.JSONExtract, pass_op=True)
def _(expr: TypedExpr, op: ops.JSONExtract) -> sge.Expression:
    return sge.func("JSON_EXTRACT", expr.expr, sge.convert(op.json_path))


@register_unary_op(ops.JSONExtractArray, pass_op=True)
def _(expr: TypedExpr, op: ops.JSONExtractArray) -> sge.Expression:
    return sge.func("JSON_EXTRACT_ARRAY", expr.expr, sge.convert(op.json_path))


@register_unary_op(ops.JSONExtractStringArray, pass_op=True)
def _(expr: TypedExpr, op: ops.JSONExtractStringArray) -> sge.Expression:
    return sge.func("JSON_EXTRACT_STRING_ARRAY", expr.expr, sge.convert(op.json_path))


@register_unary_op(ops.JSONKeys, pass_op=True)
def _(expr: TypedExpr, op: ops.JSONKeys) -> sge.Expression:
    return sge.func("JSON_KEYS", expr.expr, sge.convert(op.max_depth))


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


@register_unary_op(ops.ToJSON, pass_op=True)
def _(expr: TypedExpr, op: ops.ToJSON) -> sge.Expression:
    from_type = expr.dtype
    sg_expr = expr.expr

    # Parsing really should be a distinct operation from serialization, but
    # this was the way things were intially launched.
    if from_type == dtypes.STRING_DTYPE:
        func_name = "SAFE.PARSE_JSON" if op.safe else "PARSE_JSON"
        return sge.func(func_name, sg_expr)
    else:
        return sge.func(
            "IF", sg_expr.is_(sge.Null()), sge.Null(), sge.func("TO_JSON", sg_expr)
        )


@register_unary_op(ops.JSONDecode, pass_op=True)
def _(expr: TypedExpr, op: ops.JSONDecode) -> sge.Expression:
    to_type = op.to_type
    sg_expr = expr.expr
    func_name = ""
    if to_type == dtypes.INT_DTYPE:
        func_name = "INT64"
    elif to_type == dtypes.FLOAT_DTYPE:
        func_name = "FLOAT64"
    elif to_type == dtypes.BOOL_DTYPE:
        func_name = "BOOL"
    elif to_type == dtypes.STRING_DTYPE:
        func_name = "STRING"
    if func_name:
        func_name = "SAFE." + func_name if op.safe else func_name
        return sge.func(func_name, sg_expr)
    raise TypeError(f"Cannot cast from {dtypes.JSON_DTYPE} to {to_type}")


@register_unary_op(ops.ToJSONString)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("TO_JSON_STRING", expr.expr)


@register_binary_op(ops.JSONSet, pass_op=True)
def _(left: TypedExpr, right: TypedExpr, op) -> sge.Expression:
    return sge.func("JSON_SET", left.expr, sge.convert(op.json_path), right.expr)
