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
    return sge.func("FORMAT_TIMESTAMP", sge.convert(op.date_format), expr.expr)


@register_unary_op(ops.time_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("TIME", expr.expr)


@register_unary_op(ops.ToDatetimeOp)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Cast(this=sge.func("TIMESTAMP_SECONDS", expr.expr), to="DATETIME")


@register_unary_op(ops.ToTimestampOp)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("TIMESTAMP_SECONDS", expr.expr)


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
