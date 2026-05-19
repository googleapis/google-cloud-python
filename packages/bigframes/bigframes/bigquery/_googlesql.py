# Copyright 2026 Google LLC
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

"""Utilities for working with GoogleSqlScalarOps."""

from __future__ import annotations

from typing import Any, Union

import bigframes.core.col
import bigframes.core.expression as ex
import bigframes.core.sentinels as sentinels
from bigframes.operations import googlesql
import bigframes.series as series


def apply_googlesql_scalar_op(
    op: googlesql.GoogleSqlScalarOp,
    *args: Any,
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Applies a GoogleSQL scalar operator to the given arguments.

    Handles a mix of Series, Expression, and literal inputs.

    Args:
        op (googlesql.GoogleSqlScalarOp):
            The operator to apply.
        *args (Any):
            The arguments to apply the operator to.

    Returns:
        bigframes.pandas.Series | bigframes.core.col.Expression:
            The result of the operation. If any of ``args`` is a Series, returns
            a Series. Otherwise, returns an Expression.
    """
    # Find the first Series to use for alignment
    first_series = None
    for arg in args:
        if isinstance(arg, series.Series):
            first_series = arg
            break

    if first_series is not None:
        processed_args = []
        block = first_series._block
        for arg in args:
            if isinstance(arg, bigframes.core.col.Expression):
                block, col_id = block.project_expr(bigframes.core.col._as_bf_expr(arg))
                processed_args.append(series.Series(block.select_column(col_id)))
            elif arg is sentinels.DEFAULT:
                processed_args.append(bigframes.core.col.Expression(ex.OmittedArg()))
            else:
                processed_args.append(arg)

        # Apply the n-ary op. _apply_nary_op handles alignment of Series and literals.
        result = first_series._apply_nary_op(op, processed_args, ignore_self=True)
        result.name = None
        return result

    # No Series, return an Expression
    expr_args = []
    for arg in args:
        if isinstance(arg, bigframes.core.col.Expression):
            expr_args.append(bigframes.core.col._as_bf_expr(arg))
        elif arg is sentinels.DEFAULT:
            expr_args.append(ex.OmittedArg())
        else:
            expr_args.append(ex.const(arg))

    return bigframes.core.col.Expression(ex.OpExpression(op, tuple(expr_args)))
