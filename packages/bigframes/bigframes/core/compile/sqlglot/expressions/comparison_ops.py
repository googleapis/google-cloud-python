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

import pandas as pd
import sqlglot.expressions as sge

from bigframes import operations as ops
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr
import bigframes.core.compile.sqlglot.scalar_compiler as scalar_compiler
import bigframes.dtypes as dtypes

register_unary_op = scalar_compiler.scalar_op_compiler.register_unary_op


@register_unary_op(ops.IsInOp, pass_op=True)
def _(expr: TypedExpr, op: ops.IsInOp) -> sge.Expression:
    values = []
    is_numeric_expr = dtypes.is_numeric(expr.dtype)
    for value in op.values:
        if value is None:
            continue
        dtype = dtypes.bigframes_type(type(value))
        if expr.dtype == dtype or is_numeric_expr and dtypes.is_numeric(dtype):
            values.append(sge.convert(value))

    if op.match_nulls:
        contains_nulls = any(_is_null(value) for value in op.values)
        if contains_nulls:
            return sge.Is(this=expr.expr, expression=sge.Null()) | sge.In(
                this=expr.expr, expressions=values
            )

    if len(values) == 0:
        return sge.convert(False)

    return sge.func(
        "COALESCE", sge.In(this=expr.expr, expressions=values), sge.convert(False)
    )


# Helpers
def _is_null(value) -> bool:
    # float NaN/inf should be treated as distinct from 'true' null values
    return typing.cast(bool, pd.isna(value)) and not isinstance(value, float)
