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
import bigframes.series as series

if typing.TYPE_CHECKING:
    import bigframes.dataframe as dataframe


def struct(value: dataframe.DataFrame) -> series.Series:
    """Takes a DataFrame and converts it into a Series of structs with each
    struct entry corresponding to a DataFrame row and each struct field
    corresponding to a DataFrame column

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> import bigframes.series as series
        >>> bpd.options.display.progress_bar = None

        >>> srs = series.Series([{"version": 1, "project": "pandas"}, {"version": 2, "project": "numpy"},])
        >>> df = srs.struct.explode()
        >>> bbq.struct(df)
        0    {'project': 'pandas', 'version': 1}
        1     {'project': 'numpy', 'version': 2}
        dtype: struct<project: string, version: int64>[pyarrow]

        Args:
            value (bigframes.dataframe.DataFrame):
                The DataFrame to be converted to a Series of structs

        Returns:
            bigframes.series.Series: A new Series with struct entries representing rows of the original DataFrame
    """
    block = value._block
    block, result_id = block.apply_nary_op(
        block.value_columns, ops.StructOp(column_names=tuple(block.column_labels))
    )
    block = block.select_column(result_id)
    return series.Series(block)
