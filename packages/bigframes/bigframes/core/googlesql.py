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

from typing import TYPE_CHECKING, Any, Optional, Union

import pandas as pd

import bigframes.core.col
import bigframes.core.expression as ex
import bigframes.core.global_session as global_session
import bigframes.core.sentinels as sentinels
import bigframes.series as series
from bigframes.operations import googlesql

if TYPE_CHECKING:
    import bigframes.session


def _is_pandas_series(arg: Any) -> bool:
    return isinstance(arg, pd.Series)


def _find_session(*args: Any) -> Optional[bigframes.session.Session]:
    import bigframes.core.indexes as indexes
    import bigframes.dataframe as dataframe

    for arg in args:
        if isinstance(arg, (series.Series, dataframe.DataFrame, indexes.Index)):
            return arg._session
    return None


def _get_session(*args: Any) -> bigframes.session.Session:
    session = _find_session(*args)
    if session is not None:
        return session
    return global_session.get_global_session()


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
    has_pandas_series = any(_is_pandas_series(arg) for arg in args)

    if has_pandas_series:
        session = _get_session(*args)
        args = tuple(
            session.read_pandas(arg) if _is_pandas_series(arg) else arg for arg in args
        )

    # Find the first Series to use for alignment
    first_series = None
    for arg in args:
        if isinstance(arg, series.Series):
            first_series = arg
            break

    if first_series is not None:
        processed_args: list[Union[bigframes.core.col.Expression, series.Series]] = []
        block = first_series._block
        for arg in args:
            if isinstance(arg, bigframes.core.col.Expression):
                block, col_id = block.project_expr(bigframes.core.col._as_bf_expr(arg))
                processed_args.append(series.Series(block.select_column(col_id)))
            elif arg is sentinels.Sentinel.ARGUMENT_DEFAULT:
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
        elif arg is sentinels.Sentinel.ARGUMENT_DEFAULT:
            expr_args.append(ex.OmittedArg())
        else:
            expr_args.append(ex.const(arg))

    return bigframes.core.col.Expression(ex.OpExpression(op, tuple(expr_args)))
