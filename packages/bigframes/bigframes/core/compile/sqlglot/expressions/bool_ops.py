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
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr
import bigframes.core.compile.sqlglot.scalar_compiler as scalar_compiler

register_binary_op = scalar_compiler.scalar_op_compiler.register_binary_op


@register_binary_op(ops.and_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    if left.dtype == dtypes.BOOL_DTYPE and right.dtype == dtypes.BOOL_DTYPE:
        return sge.And(this=left.expr, expression=right.expr)
    return sge.BitwiseAnd(this=left.expr, expression=right.expr)


@register_binary_op(ops.or_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    if left.dtype == dtypes.BOOL_DTYPE and right.dtype == dtypes.BOOL_DTYPE:
        return sge.Or(this=left.expr, expression=right.expr)
    return sge.BitwiseOr(this=left.expr, expression=right.expr)


@register_binary_op(ops.xor_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    if left.dtype == dtypes.BOOL_DTYPE and right.dtype == dtypes.BOOL_DTYPE:
        left_expr = sge.And(this=left.expr, expression=sge.Not(this=right.expr))
        right_expr = sge.And(this=sge.Not(this=left.expr), expression=right.expr)
        return sge.Or(this=left_expr, expression=right_expr)
    return sge.BitwiseXor(this=left.expr, expression=right.expr)
