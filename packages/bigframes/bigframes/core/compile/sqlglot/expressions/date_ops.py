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
    # Adjust the 1-based day-of-week index (from SQL) to a 0-based index.
    return sge.Extract(
        this=sge.Identifier(this="DAYOFWEEK"), expression=expr.expr
    ) - sge.convert(1)


@register_unary_op(ops.dayofyear_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="DAYOFYEAR"), expression=expr.expr)


@register_unary_op(ops.iso_day_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="DAYOFWEEK"), expression=expr.expr)


@register_unary_op(ops.iso_week_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="ISOWEEK"), expression=expr.expr)


@register_unary_op(ops.iso_year_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="ISOYEAR"), expression=expr.expr)
