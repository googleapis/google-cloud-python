# Copyright 2024 Google LLC
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


"""This module integrates BigQuery built-in functions for use with DataFrame objects,
such as array functions:
https://cloud.google.com/bigquery/docs/reference/standard-sql/array_functions. """


from __future__ import annotations

import typing

import bigframes.operations as ops

if typing.TYPE_CHECKING:
    import bigframes.series as series


def array_length(series: series.Series) -> series.Series:
    """Compute the length of each array element in the Series.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> bpd.options.display.progress_bar = None

        >>> s = bpd.Series([[1, 2, 8, 3], [], [3, 4]])
        >>> bbq.array_length(s)
        0    4
        1    0
        2    2
        dtype: Int64

    You can also apply this function directly to Series.

        >>> s.apply(bbq.array_length, by_row=False)
        0    4
        1    0
        2    2
        dtype: Int64

    Returns:
        bigframes.series.Series: A Series of integer values indicating
            the length of each element in the Series.

    """
    return series._apply_unary_op(ops.len_op)
