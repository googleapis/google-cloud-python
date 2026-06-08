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
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Iterable,
    List,
    Literal,
    Mapping,
    Tuple,
    TypeVar,
    Union,
)

if TYPE_CHECKING:
    import pandas as pd

    import bigframes.dataframe
    import bigframes.ml.base as ml_base
    import bigframes.series
    import bigframes.session

    PROMPT_TYPE = Union[
        str,
        bigframes.series.Series,
        pd.Series,
        List[Union[str, bigframes.series.Series, pd.Series]],
        Tuple[Union[str, bigframes.series.Series, pd.Series], ...],
    ]
else:
    PROMPT_TYPE = Any

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

    def generate(
        self,
        prompt: PROMPT_TYPE,
        *,
        connection_id: str | None = None,
        endpoint: str | None = None,
        request_type: Literal["dedicated", "shared", "unspecified"] | None = None,
        model_params: Mapping[Any, Any] | None = None,
        output_schema: Mapping[str, str] | None = None,
    ) -> S:
        """
        Returns the AI analysis based on the prompt, which can be any combination of text and unstructured data.

        This is an accessor for :func:`bigframes.bigquery.ai.generate`. See that
        function's documentation for detailed parameter descriptions and examples.
        """
        import bigframes.bigquery.ai

        result = bigframes.bigquery.ai.generate(
            prompt,
            connection_id=connection_id,
            endpoint=endpoint,
            request_type=request_type,
            model_params=model_params,
            output_schema=output_schema,
        )
        return self._to_series(result)

    def generate_bool(
        self,
        prompt: PROMPT_TYPE,
        *,
        connection_id: str | None = None,
        endpoint: str | None = None,
        request_type: Literal["dedicated", "shared", "unspecified"] | None = None,
        model_params: Mapping[Any, Any] | None = None,
    ) -> S:
        """
        Returns the AI analysis based on the prompt, which can be any combination of text and unstructured data.

        This is an accessor for :func:`bigframes.bigquery.ai.generate_bool`. See that
        function's documentation for detailed parameter descriptions and examples.
        """
        import bigframes.bigquery.ai

        result = bigframes.bigquery.ai.generate_bool(
            prompt,
            connection_id=connection_id,
            endpoint=endpoint,
            request_type=request_type,
            model_params=model_params,
        )
        return self._to_series(result)

    def generate_int(
        self,
        prompt: PROMPT_TYPE,
        *,
        connection_id: str | None = None,
        endpoint: str | None = None,
        request_type: Literal["dedicated", "shared", "unspecified"] | None = None,
        model_params: Mapping[Any, Any] | None = None,
    ) -> S:
        """
        Returns the AI analysis based on the prompt, which can be any combination of text and unstructured data.

        This is an accessor for :func:`bigframes.bigquery.ai.generate_int`. See that
        function's documentation for detailed parameter descriptions and examples.
        """
        import bigframes.bigquery.ai

        result = bigframes.bigquery.ai.generate_int(
            prompt,
            connection_id=connection_id,
            endpoint=endpoint,
            request_type=request_type,
            model_params=model_params,
        )
        return self._to_series(result)

    def generate_double(
        self,
        prompt: PROMPT_TYPE,
        *,
        connection_id: str | None = None,
        endpoint: str | None = None,
        request_type: Literal["dedicated", "shared", "unspecified"] | None = None,
        model_params: Mapping[Any, Any] | None = None,
    ) -> S:
        """
        Returns the AI analysis based on the prompt, which can be any combination of text and unstructured data.

        This is an accessor for :func:`bigframes.bigquery.ai.generate_double`. See that
        function's documentation for detailed parameter descriptions and examples.
        """
        import bigframes.bigquery.ai

        result = bigframes.bigquery.ai.generate_double(
            prompt,
            connection_id=connection_id,
            endpoint=endpoint,
            request_type=request_type,
            model_params=model_params,
        )
        return self._to_series(result)

    def generate_embedding(
        self,
        model: ml_base.BaseEstimator | str | pd.Series,
        *,
        output_dimensionality: int | None = None,
        task_type: str | None = None,
        start_second: float | None = None,
        end_second: float | None = None,
        interval_seconds: float | None = None,
        trial_id: int | None = None,
        session: bigframes.session.Session | None = None,
    ) -> T:
        """
        Creates embeddings that describe an entity — for example, a piece of text or an image.

        This is an accessor for :func:`bigframes.bigquery.ai.generate_embedding`. See that
        function's documentation for detailed parameter descriptions and examples.
        """
        import bigframes.bigquery.ai

        bf_df = self._bf_from_dataframe(session)
        result = bigframes.bigquery.ai.generate_embedding(
            model,
            bf_df,
            output_dimensionality=output_dimensionality,
            task_type=task_type,
            start_second=start_second,
            end_second=end_second,
            interval_seconds=interval_seconds,
            trial_id=trial_id,
        )
        return self._to_dataframe(result)

    def generate_text(
        self,
        model: ml_base.BaseEstimator | str | pd.Series,
        *,
        temperature: float | None = None,
        max_output_tokens: int | None = None,
        top_k: int | None = None,
        top_p: float | None = None,
        stop_sequences: List[str] | None = None,
        ground_with_google_search: bool | None = None,
        request_type: str | None = None,
        session: bigframes.session.Session | None = None,
    ) -> T:
        """
        Generates text using a BigQuery ML model.

        This is an accessor for :func:`bigframes.bigquery.ai.generate_text`. See that
        function's documentation for detailed parameter descriptions and examples.
        """
        import bigframes.bigquery.ai

        bf_df = self._bf_from_dataframe(session)
        result = bigframes.bigquery.ai.generate_text(
            model,
            bf_df,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            top_k=top_k,
            top_p=top_p,
            stop_sequences=stop_sequences,
            ground_with_google_search=ground_with_google_search,
            request_type=request_type,
        )
        return self._to_dataframe(result)

    def generate_table(
        self,
        model: ml_base.BaseEstimator | str | pd.Series,
        *,
        output_schema: str | Mapping[str, str],
        temperature: float | None = None,
        top_p: float | None = None,
        max_output_tokens: int | None = None,
        stop_sequences: List[str] | None = None,
        request_type: str | None = None,
        session: bigframes.session.Session | None = None,
    ) -> T:
        """
        Generates a table using a BigQuery ML model.

        This is an accessor for :func:`bigframes.bigquery.ai.generate_table`. See that
        function's documentation for detailed parameter descriptions and examples.
        """
        import bigframes.bigquery.ai

        bf_df = self._bf_from_dataframe(session)
        result = bigframes.bigquery.ai.generate_table(
            model,
            bf_df,
            output_schema=output_schema,
            temperature=temperature,
            top_p=top_p,
            max_output_tokens=max_output_tokens,
            stop_sequences=stop_sequences,
            request_type=request_type,
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
