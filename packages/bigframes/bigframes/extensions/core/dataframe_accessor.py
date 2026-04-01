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

from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Generic, Iterable, TypeVar

if TYPE_CHECKING:
    import bigframes.dataframe
    import bigframes.session

T = TypeVar("T")
S = TypeVar("S")


class AbstractBigQueryDataFrameAccessor(abc.ABC, Generic[T, S]):
    @abc.abstractmethod
    def _bf_from_dataframe(
        self, session: bigframes.session.Session | None
    ) -> bigframes.dataframe.DataFrame:
        """Convert the accessor's object to a BigFrames DataFrame."""

    @abc.abstractmethod
    def _to_dataframe(self, bf_df: bigframes.dataframe.DataFrame) -> T:
        """Convert a BigFrames DataFrame to the accessor's object type."""

    @abc.abstractmethod
    def _to_series(self, bf_series: bigframes.series.Series) -> S:
        """Convert a BigFrames Series to the accessor's object type."""


class AIAccessor(AbstractBigQueryDataFrameAccessor[T, S]):
    """
    DataFrame accessor for BigQuery AI functions.
    """

    def __init__(self, obj: T):
        self._obj = obj

    def forecast(
        self,
        *,
        data_col: str,
        timestamp_col: str,
        model: str = "TimesFM 2.0",
        id_cols: Iterable[str] | None = None,
        horizon: int = 10,
        confidence_level: float = 0.95,
        context_window: int | None = None,
        output_historical_time_series: bool = False,
        session: bigframes.session.Session | None = None,
    ) -> T:
        """
        Forecast time series at future horizon using BigQuery AI.FORECAST.

        This is an accessor for :func:`bigframes.bigquery.ai.forecast`. See that
        function's documentation for detailed parameter descriptions and examples.
        """
        import bigframes.bigquery.ai

        bf_df = self._bf_from_dataframe(session)
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
        return self._to_dataframe(result)


class BigQueryDataFrameAccessor(AbstractBigQueryDataFrameAccessor[T, S]):
    """
    DataFrame accessor for BigQuery DataFrames functionality.
    """

    def __init__(self, obj: T):
        self._obj = obj

    @property
    @abc.abstractmethod
    def ai(self) -> AIAccessor:
        """
        Accessor for BigQuery AI functions.

        Returns:
            AIAccessor: Accessor for BigQuery AI functions.
        """

    def sql_scalar(
        self,
        sql_template: str,
        *,
        output_dtype=None,
        session: bigframes.session.Session | None = None,
    ) -> S:
        """
        Compute a new Series by applying a SQL scalar function to the DataFrame.

        This is an accessor for :func:`bigframes.bigquery.sql_scalar`. See that
        function's documentation for detailed parameter descriptions and examples.
        """
        import bigframes.bigquery

        bf_df = self._bf_from_dataframe(session)
        result = bigframes.bigquery.sql_scalar(
            sql_template, bf_df, output_dtype=output_dtype
        )
        return self._to_series(result)
