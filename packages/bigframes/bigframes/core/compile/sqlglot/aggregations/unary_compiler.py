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

import sqlglot.expressions as sge

from bigframes import dtypes
from bigframes.core import window_spec
import bigframes.core.compile.sqlglot.aggregations.op_registration as reg
from bigframes.core.compile.sqlglot.aggregations.windows import apply_window_if_present
import bigframes.core.compile.sqlglot.expressions.typed_expr as typed_expr
import bigframes.core.compile.sqlglot.sqlglot_ir as ir
from bigframes.operations import aggregations as agg_ops

UNARY_OP_REGISTRATION = reg.OpRegistration()


def compile(
    op: agg_ops.WindowOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    return UNARY_OP_REGISTRATION[op](op, column, window=window)


@UNARY_OP_REGISTRATION.register(agg_ops.SumOp)
def _(
    op: agg_ops.SumOp,
    column: typed_expr.TypedExpr,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    expr = column.expr
    if column.dtype == dtypes.BOOL_DTYPE:
        expr = sge.Cast(this=column.expr, to="INT64")
    # Will be null if all inputs are null. Pandas defaults to zero sum though.
    expr = apply_window_if_present(sge.func("SUM", expr), window)
    return sge.func("IFNULL", expr, ir._literal(0, column.dtype))


@UNARY_OP_REGISTRATION.register(agg_ops.SizeUnaryOp)
def _(
    op: agg_ops.SizeUnaryOp,
    _,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    return apply_window_if_present(sge.func("COUNT", sge.convert(1)), window)
