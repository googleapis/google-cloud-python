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

"""This module integrates BigQuery built-in AI functions for use with Series/DataFrame objects,
such as AI.GENERATE_BOOL:
https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-bool"""

from bigframes.bigquery._operations.ai import (
    classify,
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
)

__all__ = [
    "classify",
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
]
