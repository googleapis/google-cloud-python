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


@register_unary_op(ops.date_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Date(this=expr.expr)


@register_unary_op(ops.day_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="DAY"), expression=expr.expr)


@register_unary_op(ops.dayofweek_op)
def _(expr: TypedExpr) -> sge.Expression:
    return dayofweek_op_impl(expr)


@register_unary_op(ops.dayofyear_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="DAYOFYEAR"), expression=expr.expr)


@register_unary_op(ops.iso_day_op)
def _(expr: TypedExpr) -> sge.Expression:
    # Plus 1 because iso day of week uses 1-based indexing
    return dayofweek_op_impl(expr) + sge.convert(1)


@register_unary_op(ops.iso_week_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="ISOWEEK"), expression=expr.expr)


@register_unary_op(ops.iso_year_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="ISOYEAR"), expression=expr.expr)


# Helpers
def dayofweek_op_impl(expr: TypedExpr) -> sge.Expression:
    # BigQuery SQL Extract(DAYOFWEEK) returns 1 for Sunday through 7 for Saturday.
    # We want 0 for Monday through 6 for Sunday to be compatible with Pandas.
    extract_expr = sge.Extract(
        this=sge.Identifier(this="DAYOFWEEK"), expression=expr.expr
    )
    return sge.Cast(
        this=sge.Mod(this=extract_expr + sge.convert(5), expression=sge.convert(7)),
        to="INT64",
    )
