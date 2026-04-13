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

import bigframes.core.col
import bigframes.core.expression
from bigframes import dtypes
from bigframes import operations as ops


def rand() -> bigframes.core.col.Expression:
    """
    Generates a pseudo-random value of type FLOAT64 in the range of [0, 1),
    inclusive of 0 and exclusive of 1.

    .. warning::
        This method introduces non-determinism to the expression. Reading the
        same column twice may result in different results. The value might
        change. Do not use this value or any value derived from it as a join
        key.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> df = bpd.DataFrame({"a": [1, 2, 3]})
        >>> df['random'] = bbq.rand()
        >>> # Resulting column 'random' will contain random floats between 0 and 1.

    Returns:
        bigframes.pandas.api.typing.Expression:
            An expression that can be used in
            :func:`~bigframes.pandas.DataFrame.assign` and other methods.  See
            :func:`bigframes.pandas.col`.
    """
    op = ops.SqlScalarOp(
        _output_type=dtypes.FLOAT_DTYPE,
        sql_template="RAND()",
        is_deterministic=False,
    )
    return bigframes.core.col.Expression(bigframes.core.expression.OpExpression(op, ()))


def hparam_range(min: float, max: float) -> bigframes.core.col.Expression:
    """
    Defines the minimum and maximum bounds of the search space of continuous
    values for a hyperparameter.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> # Specify a range of values for a hyperparameter.
        >>> learn_rate = bbq.hparam_range(0.0001, 1.0)

    Args:
        min (float or int):
            The minimum bound of the search space.
        max (float or int):
            The maximum bound of the search space.

    Returns:
        bigframes.pandas.api.typing.Expression:
            An expression that can be used in model options.
    """
    min_expr = bigframes.core.expression.const(min)
    max_expr = bigframes.core.expression.const(max)

    op = ops.SqlScalarOp(
        _output_type=dtypes.FLOAT_DTYPE,
        sql_template="HPARAM_RANGE({0}, {1})",
        is_deterministic=True,
    )
    return bigframes.core.col.Expression(
        bigframes.core.expression.OpExpression(op, (min_expr, max_expr))
    )


def hparam_candidates(
    candidates: list[float | int | str],
) -> bigframes.core.col.Expression:
    """
    Specifies the set of discrete values for the hyperparameter.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> # Specify a set of values for a hyperparameter.
        >>> optimizer = bbq.hparam_candidates(['ADAGRAD', 'SGD', 'FTRL'])

    Args:
        candidates (list):
            The set of discrete values for the hyperparameter.

    Returns:
        bigframes.pandas.api.typing.Expression:
            An expression that can be used in model options.
    """
    candidates_expr = bigframes.core.expression.const(candidates)

    op = ops.SqlScalarOp(
        _output_type=dtypes.STRING_DTYPE,
        sql_template="HPARAM_CANDIDATES({0})",
        is_deterministic=True,
    )
    return bigframes.core.col.Expression(
        bigframes.core.expression.OpExpression(op, (candidates_expr,))
    )
