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

from typing import cast

import pandas
import pandas.api.extensions

import bigframes.core.global_session as bf_session
import bigframes.pandas as bpd


@pandas.api.extensions.register_dataframe_accessor("bigquery")
class BigQueryDataFrameAccessor:
    """
    Pandas DataFrame accessor for BigQuery DataFrames functionality.

    This accessor is registered under the ``bigquery`` namespace on pandas DataFrame objects.
    """

    def __init__(self, pandas_obj: pandas.DataFrame):
        self._obj = pandas_obj

    def sql_scalar(self, sql_template: str, *, output_dtype=None, session=None):
        """
        Compute a new pandas Series by applying a SQL scalar function to the DataFrame.

        The DataFrame is converted to BigFrames by calling ``read_pandas``, then the SQL
        template is applied using ``bigframes.bigquery.sql_scalar``, and the result is
        converted back to a pandas Series using ``to_pandas``.

        Args:
            sql_template (str):
                A SQL format string with Python-style {0}, {1}, etc. placeholders for each of
                the columns in the DataFrame (in the order they appear in ``df.columns``).
            output_dtype (a BigQuery DataFrames compatible dtype, optional):
                If provided, BigQuery DataFrames uses this to determine the output
                of the returned Series. This avoids a dry run query.
            session (bigframes.session.Session, optional):
                The BigFrames session to use. If not provided, the default global session is used.

        Returns:
            pandas.Series:
                The result of the SQL scalar function as a pandas Series.
        """
        # Import bigframes.bigquery here to avoid circular imports
        import bigframes.bigquery

        if session is None:
            session = bf_session.get_global_session()

        bf_df = cast(bpd.DataFrame, session.read_pandas(self._obj))
        result = bigframes.bigquery.sql_scalar(
            sql_template, bf_df, output_dtype=output_dtype
        )
        return result.to_pandas(ordered=True)
