# Copyright 2025 Google LLC
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
Integrate BigQuery built-in AI functions into your BigQuery DataFrames workflow.

The ``bigframes.bigquery.ai`` module provides a Pythonic interface to leverage BigQuery ML's
generative AI and predictive functions directly on BigQuery DataFrames and Series objects.
These functions enable you to perform advanced AI tasks at scale without moving data
out of BigQuery.

Key capabilities include:

* **Generative AI:** Use :func:`bigframes.bigquery.ai.generate` (Gemini) to
  perform text analysis, translation, or
  content generation. Specialized versions like
  :func:`~bigframes.bigquery.ai.generate_bool`,
  :func:`~bigframes.bigquery.ai.generate_int`, and
  :func:`~bigframes.bigquery.ai.generate_double` are available for structured
  outputs.
* **Embeddings:** Generate vector embeddings for text using
  :func:`~bigframes.bigquery.ai.generate_embedding`, which are essential for
  semantic search and retrieval-augmented generation (RAG) workflows.
* **Classification and Scoring:** Apply machine learning models to your data for
  predictive tasks with :func:`~bigframes.bigquery.ai.classify` and
  :func:`~bigframes.bigquery.ai.score`.
* **Forecasting:** Predict future values in time-series data using
  :func:`~bigframes.bigquery.ai.forecast`.

**Example usage:**

    >>> import bigframes.pandas as bpd
    >>> import bigframes.bigquery as bbq

    >>> df = bpd.DataFrame({
    ...     "text_input": [
    ...         "Is this a positive review? The food was terrible.",
    ...     ],
    ... })  # doctest: +SKIP

    >>> # Assuming a Gemini model has been created in BigQuery as 'my_gemini_model'
    >>> result = bq.ai.generate_text("my_gemini_model", df["text_input"])  # doctest: +SKIP

For more information on the underlying BigQuery ML syntax, see:
https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-bool
"""

from bigframes.bigquery._operations.ai import (
    classify,
    embed,
    forecast,
    generate,
    generate_bool,
    generate_double,
    generate_embedding,
    generate_int,
    generate_table,
    generate_text,
    if_,
    score,
    similarity,
)

__all__ = [
    "classify",
    "embed",
    "forecast",
    "generate",
    "generate_bool",
    "generate_double",
    "generate_embedding",
    "generate_int",
    "generate_table",
    "generate_text",
    "if_",
    "score",
    "similarity",
]
