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

    def classify(
        self,
        input: PROMPT_TYPE,
        categories: tuple[str, ...] | list[str],
        *,
        examples: list[tuple[str, str]]
        | list[tuple[str, list[str] | tuple[str, ...]]]
        | None = None,
        connection_id: str | None = None,
        endpoint: str | None = None,
        output_mode: Literal["single", "multi"] | None = None,
        optimization_mode: Literal["minimize_cost", "maximize_quality"] | None = None,
        max_error_ratio: float | None = None,
    ) -> S:
        """
        Classifies a given input into one of the specified categories. It will always return one of the provided categories best fit the prompt input.

        This is an accessor for :func:`bigframes.bigquery.ai.classify`. See that
        function's documentation for detailed parameter descriptions and examples.
        """
        import bigframes.bigquery.ai

        result = bigframes.bigquery.ai.classify(
            input,
            categories,
            examples=examples,
            connection_id=connection_id,
            endpoint=endpoint,
            output_mode=output_mode,
            optimization_mode=optimization_mode,
            max_error_ratio=max_error_ratio,
        )
        return self._to_series(result)

    def if_(
        self,
        prompt: PROMPT_TYPE,
        *,
        connection_id: str | None = None,
        endpoint: str | None = None,
        optimization_mode: Literal["minimize_cost", "maximize_quality"] | None = None,
        max_error_ratio: float | None = None,
    ) -> S:
        """
        Evaluates the prompt to True or False. Compared to ``ai.generate_bool()``, this function
        provides optimization such that not all rows are evaluated with the LLM.

        This is an accessor for :func:`bigframes.bigquery.ai.if_`. See that
        function's documentation for detailed parameter descriptions and examples.
        """
        import bigframes.bigquery.ai

        result = bigframes.bigquery.ai.if_(
            prompt,
            connection_id=connection_id,
            endpoint=endpoint,
            optimization_mode=optimization_mode,
            max_error_ratio=max_error_ratio,
        )
        return self._to_series(result)

    def score(
        self,
        prompt: PROMPT_TYPE,
        *,
        connection_id: str | None = None,
        endpoint: str | None = None,
        max_error_ratio: float | None = None,
    ) -> S:
        """
        Computes a score based on rubrics described in natural language. It will return a double value.

        This is an accessor for :func:`bigframes.bigquery.ai.score`. See that
        function's documentation for detailed parameter descriptions and examples.
        """
        import bigframes.bigquery.ai

        result = bigframes.bigquery.ai.score(
            prompt,
            connection_id=connection_id,
            endpoint=endpoint,
            max_error_ratio=max_error_ratio,
        )
        return self._to_series(result)


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
