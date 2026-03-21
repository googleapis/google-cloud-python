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

from typing import cast, Iterable, Optional

import pandas
import pandas.api.extensions

import bigframes.core.global_session as bf_session
from bigframes.core.logging import log_adapter
import bigframes.pandas as bpd


@log_adapter.class_logger
class PandasAIAccessor:
    """
    Pandas DataFrame accessor for BigQuery AI functions.
    """

    def __init__(self, pandas_obj: pandas.DataFrame):
        self._obj = pandas_obj

    def forecast(
        self,
        *,
        data_col: str,
        timestamp_col: str,
        model: str = "TimesFM 2.0",
        id_cols: Optional[Iterable[str]] = None,
        horizon: int = 10,
        confidence_level: float = 0.95,
        context_window: Optional[int] = None,
        output_historical_time_series: bool = False,
        session=None,
    ) -> pandas.DataFrame:
        """
        Forecast time series at future horizon using BigQuery AI.FORECAST.

        See: https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-forecast

        Args:
            data_col (str):
                A str value that specifies the name of the data column. The data column contains the data to forecast.
                The data column must use one of the following data types: INT64, NUMERIC and FLOAT64
            timestamp_col (str):
                A str value that specified the name of the time points column.
                The time points column provides the time points used to generate the forecast.
                The time points column must use one of the following data types: TIMESTAMP, DATE and DATETIME
            model (str, default "TimesFM 2.0"):
                A str value that specifies the name of the model. "TimesFM 2.0" and "TimesFM 2.5" are supported.
            id_cols (Iterable[str], optional):
                An iterable of str value that specifies the names of one or more ID columns. Each ID identifies a unique time series to forecast.
                Specify one or more values for this argument in order to forecast multiple time series using a single query.
                The columns that you specify must use one of the following data types: STRING, INT64, ARRAY<STRING> and ARRAY<INT64>
            horizon (int, default 10):
                An int value that specifies the number of time points to forecast. The default value is 10. The valid input range is [1, 10,000].
            confidence_level (float, default 0.95):
                A FLOAT64 value that specifies the percentage of the future values that fall in the prediction interval.
                The default value is 0.95. The valid input range is [0, 1).
            context_window (int, optional):
                An int value that specifies the context window length used by BigQuery ML's built-in TimesFM model.
                The context window length determines how many of the most recent data points from the input time series are use by the model.
                If you don't specify a value, the AI.FORECAST function automatically chooses the smallest possible context window length to use
                that is still large enough to cover the number of time series data points in your input data.
            output_historical_time_series (bool, default False):
                A boolean value that determines whether to include the input time series history in the forecast.
            session (bigframes.session.Session, optional):
                The BigFrames session to use. If not provided, the default global session is used.

        Returns:
            pandas.DataFrame:
                The forecast DataFrame result.
        """
        import bigframes.bigquery.ai

        if session is None:
            session = bf_session.get_global_session()

        bf_df = cast(bpd.DataFrame, session.read_pandas(self._obj))
        result = bigframes.bigquery.ai.forecast(
            bf_df,
            data_col=data_col,
            timestamp_col=timestamp_col,
            model=model,
            id_cols=id_cols,
            horizon=horizon,
            confidence_level=confidence_level,
            context_window=context_window,
            output_historical_time_series=output_historical_time_series,
        )
        return result.to_pandas(ordered=True)


@pandas.api.extensions.register_dataframe_accessor("bigquery")
@log_adapter.class_logger
class PandasBigQueryDataFrameAccessor:
    """
    Pandas DataFrame accessor for BigQuery DataFrames functionality.

    This accessor is registered under the ``bigquery`` namespace on pandas DataFrame objects.
    """

    def __init__(self, pandas_obj: pandas.DataFrame):
        self._obj = pandas_obj

    @property
    def ai(self) -> "PandasAIAccessor":
        """
        Accessor for BigQuery AI functions.
        """
        return PandasAIAccessor(self._obj)

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
