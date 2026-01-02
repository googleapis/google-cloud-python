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

from bigframes import dtypes
from bigframes import operations as ops
from bigframes.core.compile.constants import UNIT_TO_US_CONVERSION_FACTORS
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr
import bigframes.core.compile.sqlglot.scalar_compiler as scalar_compiler

register_unary_op = scalar_compiler.scalar_op_compiler.register_unary_op


@register_unary_op(ops.timedelta_floor_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Floor(this=expr.expr)


@register_unary_op(ops.ToTimedeltaOp, pass_op=True)
def _(expr: TypedExpr, op: ops.ToTimedeltaOp) -> sge.Expression:
    value = expr.expr
    if expr.dtype == dtypes.TIMEDELTA_DTYPE:
        return value

    factor = UNIT_TO_US_CONVERSION_FACTORS[op.unit]
    if factor != 1:
        value = sge.Mul(this=value, expression=sge.convert(factor))
    if expr.dtype == dtypes.FLOAT_DTYPE:
        value = sge.Cast(this=sge.Floor(this=value), to=sge.DataType(this="INT64"))
    return value
