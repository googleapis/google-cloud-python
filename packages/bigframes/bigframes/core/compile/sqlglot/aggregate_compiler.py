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

from bigframes.core import expression
from bigframes.core.compile.sqlglot.aggregations import (
    binary_compiler,
    nullary_compiler,
    ordered_unary_compiler,
    unary_compiler,
)
from bigframes.core.compile.sqlglot.expressions import typed_expr
import bigframes.core.compile.sqlglot.scalar_compiler as scalar_compiler


def compile_aggregate(
    aggregate: expression.Aggregation,
    order_by: tuple[sge.Expression, ...],
) -> sge.Expression:
    """Compiles BigFrames aggregation expression into SQLGlot expression."""
    if isinstance(aggregate, expression.NullaryAggregation):
        return nullary_compiler.compile(aggregate.op)
    if isinstance(aggregate, expression.UnaryAggregation):
        column = typed_expr.TypedExpr(
            scalar_compiler.compile_scalar_expression(aggregate.arg),
            aggregate.arg.output_type,
        )
        if not aggregate.op.order_independent:
            return ordered_unary_compiler.compile(
                aggregate.op, column, order_by=order_by
            )
        else:
            return unary_compiler.compile(aggregate.op, column)
    elif isinstance(aggregate, expression.BinaryAggregation):
        left = typed_expr.TypedExpr(
            scalar_compiler.compile_scalar_expression(aggregate.left),
            aggregate.left.output_type,
        )
        right = typed_expr.TypedExpr(
            scalar_compiler.compile_scalar_expression(aggregate.right),
            aggregate.right.output_type,
        )
        return binary_compiler.compile(aggregate.op, left, right)
    else:
        raise ValueError(f"Unexpected aggregation: {aggregate}")
