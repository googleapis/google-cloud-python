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

from bigframes import dtypes
from bigframes import operations as ops
from bigframes.core.compile.constants import UNIT_TO_US_CONVERSION_FACTORS
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr
import bigframes.core.compile.sqlglot.scalar_compiler as scalar_compiler

register_unary_op = scalar_compiler.scalar_op_compiler.register_unary_op


@register_unary_op(ops.FloorDtOp, pass_op=True)
def _(expr: TypedExpr, op: ops.FloorDtOp) -> sge.Expression:
    pandas_to_bq_freq_map = {
        "Y": "YEAR",
        "Q": "QUARTER",
        "M": "MONTH",
        "W": "WEEK(MONDAY)",
        "D": "DAY",
        "h": "HOUR",
        "min": "MINUTE",
        "s": "SECOND",
        "ms": "MILLISECOND",
        "us": "MICROSECOND",
        "ns": "NANOSECOND",
    }
    if op.freq not in pandas_to_bq_freq_map.keys():
        raise NotImplementedError(
            f"Unsupported freq paramater: {op.freq}"
            + " Supported freq parameters are: "
            + ",".join(pandas_to_bq_freq_map.keys())
        )

    bq_freq = pandas_to_bq_freq_map[op.freq]
    return sge.TimestampTrunc(this=expr.expr, unit=sge.Identifier(this=bq_freq))


@register_unary_op(ops.hour_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="HOUR"), expression=expr.expr)


@register_unary_op(ops.minute_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="MINUTE"), expression=expr.expr)


@register_unary_op(ops.month_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="MONTH"), expression=expr.expr)


@register_unary_op(ops.normalize_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.TimestampTrunc(this=expr.expr, unit=sge.Identifier(this="DAY"))


@register_unary_op(ops.quarter_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="QUARTER"), expression=expr.expr)


@register_unary_op(ops.second_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="SECOND"), expression=expr.expr)


@register_unary_op(ops.StrftimeOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrftimeOp) -> sge.Expression:
    func_name = ""
    if expr.dtype == dtypes.DATE_DTYPE:
        func_name = "FORMAT_DATE"
    elif expr.dtype == dtypes.DATETIME_DTYPE:
        func_name = "FORMAT_DATETIME"
    elif expr.dtype == dtypes.TIME_DTYPE:
        func_name = "FORMAT_TIME"
    elif expr.dtype == dtypes.TIMESTAMP_DTYPE:
        func_name = "FORMAT_TIMESTAMP"

    return sge.func(func_name, sge.convert(op.date_format), expr.expr)


@register_unary_op(ops.time_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("TIME", expr.expr)


@register_unary_op(ops.ToDatetimeOp, pass_op=True)
def _(expr: TypedExpr, op: ops.ToDatetimeOp) -> sge.Expression:
    if op.format:
        result = expr.expr
        if expr.dtype != dtypes.STRING_DTYPE:
            result = sge.Cast(this=result, to="STRING")
        result = sge.func(
            "PARSE_TIMESTAMP", sge.convert(op.format), result, sge.convert("UTC")
        )
        return sge.Cast(this=result, to="DATETIME")

    if expr.dtype == dtypes.STRING_DTYPE:
        return sge.TryCast(this=expr.expr, to="DATETIME")

    value = expr.expr
    unit = op.unit or "ns"
    factor = UNIT_TO_US_CONVERSION_FACTORS[unit]
    if factor != 1:
        value = sge.Mul(this=value, expression=sge.convert(factor))
    value = sge.func("TRUNC", value)
    return sge.Cast(
        this=sge.func("TIMESTAMP_MICROS", sge.Cast(this=value, to="INT64")),
        to="DATETIME",
    )


@register_unary_op(ops.ToTimestampOp, pass_op=True)
def _(expr: TypedExpr, op: ops.ToTimestampOp) -> sge.Expression:
    if op.format:
        result = expr.expr
        if expr.dtype != dtypes.STRING_DTYPE:
            result = sge.Cast(this=result, to="STRING")
        return sge.func(
            "PARSE_TIMESTAMP", sge.convert(op.format), expr.expr, sge.convert("UTC")
        )

    if expr.dtype == dtypes.STRING_DTYPE:
        return sge.func("TIMESTAMP", expr.expr)

    value = expr.expr
    unit = op.unit or "ns"
    factor = UNIT_TO_US_CONVERSION_FACTORS[unit]
    if factor != 1:
        value = sge.Mul(this=value, expression=sge.convert(factor))
    value = sge.func("TRUNC", value)
    return sge.Cast(
        this=sge.func("TIMESTAMP_MICROS", sge.Cast(this=value, to="INT64")),
        to="TIMESTAMP",
    )


@register_unary_op(ops.UnixMicros)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("UNIX_MICROS", expr.expr)


@register_unary_op(ops.UnixMillis)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("UNIX_MILLIS", expr.expr)


@register_unary_op(ops.UnixSeconds, pass_op=True)
def _(expr: TypedExpr, op: ops.UnixSeconds) -> sge.Expression:
    return sge.func("UNIX_SECONDS", expr.expr)


@register_unary_op(ops.year_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="YEAR"), expression=expr.expr)
