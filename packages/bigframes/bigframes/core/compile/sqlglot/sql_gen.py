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

from __future__ import annotations

import dataclasses

import sqlglot.dialects.bigquery
import sqlglot.expressions as sge


@dataclasses.dataclass(frozen=True)
class SQLGen:
    """Helper class to build SQLGlot Query and generate SQL string."""

    dialect = sqlglot.dialects.bigquery.BigQuery
    """The SQL dialect used for generation."""

    quoted: bool = True
    """Whether to quote identifiers in the generated SQL."""

    pretty: bool = True
    """Whether to pretty-print the generated SQL."""

    def sql(self, expr: sge.Expression) -> str:
        """Generate SQL string from the given expression."""
        return expr.sql(dialect=self.dialect, pretty=self.pretty)
