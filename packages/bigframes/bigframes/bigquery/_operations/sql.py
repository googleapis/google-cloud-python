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

"""SQL escape hatch features."""

from __future__ import annotations

from typing import Optional, Sequence, Union, cast

import google.cloud.bigquery

import bigframes.dataframe
import bigframes.dtypes
import bigframes.operations
import bigframes.series
from bigframes.core.compile.sqlglot import sql


def _format_names(sql_template: str, dataframe: bigframes.dataframe.DataFrame):
    """Turn sql_template from a template that uses names to one that uses
    numbers.
    """
    names_to_numbers = {name: f"{{{i}}}" for i, name in enumerate(dataframe.columns)}
    numbers = [f"{{{i}}}" for i in range(len(dataframe.columns))]
    return sql_template.format(*numbers, **names_to_numbers)


def sql_scalar(
    sql_template: str,
    columns: Union[bigframes.dataframe.DataFrame, Sequence[bigframes.series.Series]],
    *,
    output_dtype: Optional[bigframes.dtypes.Dtype] = None,
) -> bigframes.series.Series:
    """Create a Series from a SQL template.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq

    Either pass in a sequence of series, in which case use  integers in the
    format strings.

        >>> s = bpd.Series(["1.5", "2.5", "3.5"])
        >>> s = s.astype(pd.ArrowDtype(pa.decimal128(38, 9)))
        >>> bbq.sql_scalar("ROUND({0}, 0, 'ROUND_HALF_EVEN')", [s])
        0    2.000000000
        1    2.000000000
        2    4.000000000
        dtype: decimal128(38, 9)[pyarrow]

    Or pass in a DataFrame, in which case use the column names in the format
    strings.

        >>> df = bpd.DataFrame({"a": ["1.5", "2.5", "3.5"]})
        >>> df = df.astype({"a": pd.ArrowDtype(pa.decimal128(38, 9))})
        >>> bbq.sql_scalar("ROUND({a}, 0, 'ROUND_HALF_EVEN')", df)
        0    2.000000000
        1    2.000000000
        2    4.000000000
        dtype: decimal128(38, 9)[pyarrow]

    You can also use the `.bigquery` DataFrame accessor to apply a SQL scalar function.

        Compute SQL scalar using a pandas DataFrame:

        >>> import pandas as pd
        >>> df = pd.DataFrame({"x": [1, 2, 3]})
        >>> bpd.options.display.progress_bar = None # doctest: +SKIP
        >>> pandas_s = df.bigquery.sql_scalar("POW({0}, 2)") # doctest: +SKIP
        >>> type(pandas_s) # doctest: +SKIP
        <class 'pandas.core.series.Series'>

        Compute SQL scalar using a BigFrames DataFrame:

        >>> bf_df = bpd.DataFrame({"x": [1, 2, 3]})
        >>> bf_s = bf_df.bigquery.sql_scalar("POW({0}, 2)") # doctest: +SKIP
        >>> type(bf_s) # doctest: +SKIP
        <class 'bigframes.series.Series'>


    Args:
        sql_template (str):
            A SQL format string with Python-style {0} placeholders for each of
            the Series objects in ``columns``.
        columns (
            Sequence[bigframes.pandas.Series] | bigframes.pandas.DataFrame
        ):
            Series objects representing the column inputs to the
            ``sql_template``. Must contain at least one Series.
        output_dtype (a BigQuery DataFrames compatible dtype, optional):
            If provided, BigQuery DataFrames uses this to determine the output
            of the returned Series. This avoids a dry run query.

    Returns:
        bigframes.pandas.Series:
            A Series with the SQL applied.

    Raises:
        ValueError: If ``columns`` is empty.
    """
    if isinstance(columns, bigframes.dataframe.DataFrame):
        sql_template = _format_names(sql_template, columns)
        columns = [
            cast(bigframes.series.Series, columns[column]) for column in columns.columns
        ]

    if len(columns) == 0:
        raise ValueError("Must provide at least one column in columns")

    base_series = columns[0]

    # To integrate this into our expression trees, we need to get the output
    # type, so we do some manual compilation and a dry run query to get that.
    # Another benefit of this is that if there is a syntax error in the SQL
    # template, then this will fail with an error earlier in the process,
    # aiding users in debugging.
    if output_dtype is None:
        literals_sql = [
            sql.to_sql(sql.literal(None, column.dtype)) for column in columns
        ]
        select_sql = sql_template.format(*literals_sql)
        dry_run_sql = f"SELECT {select_sql}"

        # Use the executor directly, because we want the original column IDs, not
        # the user-friendly column names that block.to_sql_query() would produce.
        bqclient = base_series._session.bqclient
        job = bqclient.query(
            dry_run_sql, job_config=google.cloud.bigquery.QueryJobConfig(dry_run=True)
        )
        _, output_dtype = bigframes.dtypes.convert_schema_field(job.schema[0])

    op = bigframes.operations.SqlScalarOp(
        _output_type=output_dtype, sql_template=sql_template
    )
    return base_series._apply_nary_op(op, columns[1:])
