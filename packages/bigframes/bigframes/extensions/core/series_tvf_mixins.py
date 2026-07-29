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

from typing import List, Mapping, TypeVar

import pandas as pd

from bigframes import session
from bigframes.extensions.core import abstract_series_accessor
from bigframes.ml import base as ml_base

T = TypeVar("T")
S = TypeVar("S")


class AITVFMixin(abstract_series_accessor.AbstractBigQuerySeriesAccessor[T, S]):
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
        session: session.Session | None = None,
    ) -> T:
        """
        Creates embeddings that describe an entity — for example, a piece of text or an image.

        This is an accessor for :func:`bigframes.bigquery.ai.generate_embedding`. See that
        function's documentation for detailed parameter descriptions and examples.
        """
        import bigframes.bigquery.ai

        bf_series = self._bf_from_series(session)
        result = bigframes.bigquery.ai.generate_embedding(
            model,
            bf_series,
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
        session: session.Session | None = None,
    ) -> T:
        """
        Generates text using a BigQuery ML model.

        This is an accessor for :func:`bigframes.bigquery.ai.generate_text`. See that
        function's documentation for detailed parameter descriptions and examples.
        """
        import bigframes.bigquery.ai

        bf_series = self._bf_from_series(session)
        result = bigframes.bigquery.ai.generate_text(
            model,
            bf_series,
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
        session: session.Session | None = None,
    ) -> T:
        """
        Generates a table using a BigQuery ML model.

        This is an accessor for :func:`bigframes.bigquery.ai.generate_table`. See that
        function's documentation for detailed parameter descriptions and examples.
        """
        import bigframes.bigquery.ai

        bf_series = self._bf_from_series(session)
        result = bigframes.bigquery.ai.generate_table(
            model,
            bf_series,
            output_schema=output_schema,
            temperature=temperature,
            top_p=top_p,
            max_output_tokens=max_output_tokens,
            stop_sequences=stop_sequences,
            request_type=request_type,
        )
        return self._to_dataframe(result)
