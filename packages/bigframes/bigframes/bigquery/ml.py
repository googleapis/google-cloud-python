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

"""This module exposes `BigQuery ML
<https://docs.cloud.google.com/bigquery/docs/bqml-introduction>`_ functions
by directly mapping to the equivalent function names in SQL syntax.

For an interface more familiar to Scikit-Learn users, see :mod:`bigframes.ml`.
"""

from bigframes.bigquery._operations.ml import (
    create_model,
    evaluate,
    explain_predict,
    generate_embedding,
    generate_text,
    global_explain,
    predict,
    transform,
)

__all__ = [
    "create_model",
    "evaluate",
    "predict",
    "explain_predict",
    "global_explain",
    "transform",
    "generate_text",
    "generate_embedding",
]
