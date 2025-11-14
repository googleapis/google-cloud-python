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

import bigframes.core.compile.sqlglot.aggregations.op_registration as reg
import bigframes.core.compile.sqlglot.expressions.typed_expr as typed_expr
from bigframes.operations import aggregations as agg_ops

ORDERED_UNARY_OP_REGISTRATION = reg.OpRegistration()


def compile(
    op: agg_ops.WindowOp,
    column: typed_expr.TypedExpr,
    *,
    order_by: tuple[sge.Expression, ...] = (),
) -> sge.Expression:
    return ORDERED_UNARY_OP_REGISTRATION[op](op, column, order_by=order_by)


@ORDERED_UNARY_OP_REGISTRATION.register(agg_ops.ArrayAggOp)
def _(
    op: agg_ops.ArrayAggOp,
    column: typed_expr.TypedExpr,
    *,
    order_by: tuple[sge.Expression, ...],
) -> sge.Expression:
    expr = column.expr
    if len(order_by) > 0:
        expr = sge.Order(this=column.expr, expressions=list(order_by))
    return sge.IgnoreNulls(this=sge.ArrayAgg(this=expr))


@ORDERED_UNARY_OP_REGISTRATION.register(agg_ops.StringAggOp)
def _(
    op: agg_ops.StringAggOp,
    column: typed_expr.TypedExpr,
    *,
    order_by: tuple[sge.Expression, ...],
) -> sge.Expression:
    expr = column.expr
    if len(order_by) > 0:
        expr = sge.Order(this=expr, expressions=list(order_by))

    expr = sge.GroupConcat(this=expr, separator=sge.convert(op.sep))
    return sge.func("COALESCE", expr, sge.convert(""))
