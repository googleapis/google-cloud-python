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

import bigframes_vendored.sqlglot.expressions as sge
import pandas as pd
import pyarrow as pa

from bigframes import operations as ops
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr
import bigframes.core.compile.sqlglot.scalar_compiler as scalar_compiler

register_nary_op = scalar_compiler.scalar_op_compiler.register_nary_op
register_unary_op = scalar_compiler.scalar_op_compiler.register_unary_op


@register_unary_op(ops.StructFieldOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StructFieldOp) -> sge.Expression:
    if isinstance(op.name_or_index, str):
        name = op.name_or_index
    else:
        pa_type = typing.cast(pd.ArrowDtype, expr.dtype)
        pa_struct_type = typing.cast(pa.StructType, pa_type.pyarrow_dtype)
        name = pa_struct_type.field(op.name_or_index).name

    return sge.Column(
        this=sge.to_identifier(name, quoted=True),
        catalog=expr.expr,
    )


@register_nary_op(ops.StructOp, pass_op=True)
def _(*exprs: TypedExpr, op: ops.StructOp) -> sge.Struct:
    return sge.Struct(
        expressions=[
            sge.PropertyEQ(this=sge.to_identifier(col), expression=expr.expr)
            for col, expr in zip(op.column_names, exprs)
        ]
    )
