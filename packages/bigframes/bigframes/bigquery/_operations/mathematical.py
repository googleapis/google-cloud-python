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

from bigframes import dtypes
from bigframes import operations as ops
import bigframes.core.col
import bigframes.core.expression


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
