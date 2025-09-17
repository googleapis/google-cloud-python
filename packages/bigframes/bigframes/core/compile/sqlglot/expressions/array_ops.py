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
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr
import bigframes.core.compile.sqlglot.scalar_compiler as scalar_compiler

register_unary_op = scalar_compiler.scalar_op_compiler.register_unary_op


@register_unary_op(ops.ArrayToStringOp, pass_op=True)
def _(expr: TypedExpr, op: ops.ArrayToStringOp) -> sge.Expression:
    return sge.ArrayToString(this=expr.expr, expression=f"'{op.delimiter}'")


@register_unary_op(ops.ArrayIndexOp, pass_op=True)
def _(expr: TypedExpr, op: ops.ArrayIndexOp) -> sge.Expression:
    return sge.Bracket(
        this=expr.expr,
        expressions=[sge.Literal.number(op.index)],
        safe=True,
        offset=False,
    )


@register_unary_op(ops.ArraySliceOp, pass_op=True)
def _(expr: TypedExpr, op: ops.ArraySliceOp) -> sge.Expression:
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
