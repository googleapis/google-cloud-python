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

_NAN = sge.Cast(this=sge.convert("NaN"), to="FLOAT64")
_INF = sge.Cast(this=sge.convert("Infinity"), to="FLOAT64")

# Approx Highest number you can pass in to EXP function and get a valid FLOAT64 result
# FLOAT64 has 11 exponent bits, so max values is about 2**(2**10)
# ln(2**(2**10)) == (2**10)*ln(2) ~= 709.78, so EXP(x) for x>709.78 will overflow.
_FLOAT64_EXP_BOUND = sge.convert(709.78)

UNARY_OP_REGISTRATION = OpRegistration()


def compile(op: ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return UNARY_OP_REGISTRATION[op](op, expr)


@UNARY_OP_REGISTRATION.register(ops.abs_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.Abs(this=expr.expr)


@UNARY_OP_REGISTRATION.register(ops.arccosh_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=expr.expr < sge.convert(1),
                true=_NAN,
            )
        ],
        default=sge.func("ACOSH", expr.expr),
    )


@UNARY_OP_REGISTRATION.register(ops.arccos_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=sge.func("ABS", expr.expr) > sge.convert(1),
                true=_NAN,
            )
        ],
        default=sge.func("ACOS", expr.expr),
    )


@UNARY_OP_REGISTRATION.register(ops.arcsin_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=sge.func("ABS", expr.expr) > sge.convert(1),
                true=_NAN,
            )
        ],
        default=sge.func("ASIN", expr.expr),
    )


@UNARY_OP_REGISTRATION.register(ops.arcsinh_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.func("ASINH", expr.expr)


@UNARY_OP_REGISTRATION.register(ops.arctan_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.func("ATAN", expr.expr)


@UNARY_OP_REGISTRATION.register(ops.arctanh_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=sge.func("ABS", expr.expr) > sge.convert(1),
                true=_NAN,
            )
        ],
        default=sge.func("ATANH", expr.expr),
    )


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


@UNARY_OP_REGISTRATION.register(ops.capitalize_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.Initcap(this=expr.expr)


@UNARY_OP_REGISTRATION.register(ops.ceil_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.Ceil(this=expr.expr)


@UNARY_OP_REGISTRATION.register(ops.cos_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.func("COS", expr.expr)


@UNARY_OP_REGISTRATION.register(ops.cosh_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=sge.func("ABS", expr.expr) > sge.convert(709.78),
                true=_INF,
            )
        ],
        default=sge.func("COSH", expr.expr),
    )


@UNARY_OP_REGISTRATION.register(ops.date_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.Date(this=expr.expr)


@UNARY_OP_REGISTRATION.register(ops.day_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="DAY"), expression=expr.expr)


@UNARY_OP_REGISTRATION.register(ops.dayofweek_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    # Adjust the 1-based day-of-week index (from SQL) to a 0-based index.
    return sge.Extract(
        this=sge.Identifier(this="DAYOFWEEK"), expression=expr.expr
    ) - sge.convert(1)


@UNARY_OP_REGISTRATION.register(ops.dayofyear_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="DAYOFYEAR"), expression=expr.expr)


@UNARY_OP_REGISTRATION.register(ops.exp_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=expr.expr > _FLOAT64_EXP_BOUND,
                true=_INF,
            )
        ],
        default=sge.func("EXP", expr.expr),
    )


@UNARY_OP_REGISTRATION.register(ops.expm1_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=expr.expr > _FLOAT64_EXP_BOUND,
                true=_INF,
            )
        ],
        default=sge.func("EXP", expr.expr),
    ) - sge.convert(1)


@UNARY_OP_REGISTRATION.register(ops.floor_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.Floor(this=expr.expr)


@UNARY_OP_REGISTRATION.register(ops.hash_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.func("FARM_FINGERPRINT", expr.expr)


@UNARY_OP_REGISTRATION.register(ops.isnull_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.Is(this=expr.expr, expression=sge.Null())


@UNARY_OP_REGISTRATION.register(ops.notnull_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.Not(this=sge.Is(this=expr.expr, expression=sge.Null()))


@UNARY_OP_REGISTRATION.register(ops.sin_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.func("SIN", expr.expr)


@UNARY_OP_REGISTRATION.register(ops.sinh_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=sge.func("ABS", expr.expr) > _FLOAT64_EXP_BOUND,
                true=sge.func("SIGN", expr.expr) * _INF,
            )
        ],
        default=sge.func("SINH", expr.expr),
    )


@UNARY_OP_REGISTRATION.register(ops.tan_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.func("TAN", expr.expr)


@UNARY_OP_REGISTRATION.register(ops.tanh_op)
def _(op: ops.base_ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return sge.func("TANH", expr.expr)


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
