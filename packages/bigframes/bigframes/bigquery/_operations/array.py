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

"""
Array functions defined from
https://cloud.google.com/bigquery/docs/reference/standard-sql/array_functions
"""


from __future__ import annotations

import typing

import bigframes_vendored.constants as constants

import bigframes.core.groupby as groupby
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops
import bigframes.series as series

if typing.TYPE_CHECKING:
    import bigframes.dataframe as dataframe


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

    Args:
        series (bigframes.series.Series): A Series with array columns.

    Returns:
        bigframes.series.Series: A Series of integer values indicating
            the length of each element in the Series.

    """
    return series._apply_unary_op(ops.len_op)


def array_agg(
    obj: groupby.SeriesGroupBy | groupby.DataFrameGroupBy,
) -> series.Series | dataframe.DataFrame:
    """Group data and create arrays from selected columns, omitting NULLs to avoid
    BigQuery errors (NULLs not allowed in arrays).

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> import numpy as np
        >>> bpd.options.display.progress_bar = None

    For a SeriesGroupBy object:

        >>> lst = ['a', 'a', 'b', 'b', 'a']
        >>> s = bpd.Series([1, 2, 3, 4, np.nan], index=lst)
        >>> bbq.array_agg(s.groupby(level=0))
        a    [1. 2.]
        b    [3. 4.]
        dtype: list<item: double>[pyarrow]

    For a DataFrameGroupBy object:

        >>> l = [[1, 2, 3], [1, None, 4], [2, 1, 3], [1, 2, 2]]
        >>> df = bpd.DataFrame(l, columns=["a", "b", "c"])
        >>> bbq.array_agg(df.groupby(by=["b"]))
                 a      c
        b
        1.0    [2]    [3]
        2.0  [1 1]  [3 2]
        <BLANKLINE>
        [2 rows x 2 columns]

    Args:
        obj (groupby.SeriesGroupBy | groupby.DataFrameGroupBy):
            A GroupBy object to be applied the function.

    Returns:
        bigframes.series.Series | bigframes.dataframe.DataFrame: A Series or
            DataFrame containing aggregated array columns, and indexed by the
            original group columns.
    """
    if isinstance(obj, groupby.SeriesGroupBy):
        return obj._aggregate(agg_ops.ArrayAggOp())
    elif isinstance(obj, groupby.DataFrameGroupBy):
        return obj._aggregate_all(agg_ops.ArrayAggOp(), numeric_only=False)
    else:
        raise ValueError(
            f"Unsupported type {type(obj)} to apply `array_agg` function. {constants.FEEDBACK_LINK}"
        )


def array_to_string(series: series.Series, delimiter: str) -> series.Series:
    """Converts array elements within a Series into delimited strings.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> import numpy as np
        >>> bpd.options.display.progress_bar = None

        >>> s = bpd.Series([["H", "i", "!"], ["Hello", "World"], np.nan, [], ["Hi"]])
        >>> bbq.array_to_string(s, delimiter=", ")
            0         H, i, !
            1    Hello, World
            2
            3
            4              Hi
            dtype: string

    Args:
        series (bigframes.series.Series): A Series containing arrays.
        delimiter (str): The string used to separate array elements.

    Returns:
        bigframes.series.Series: A Series containing delimited strings.

    """
    return series._apply_unary_op(ops.ArrayToStringOp(delimiter=delimiter))
