# Copyright 2024 Google LLC
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

import dataclasses

import bigframes.core.compile.googlesql.datatype as datatype
import bigframes.core.compile.googlesql.expression as expr

# Conversion functions:
# https://cloud.google.com/bigquery/docs/reference/standard-sql/conversion_functions


@dataclasses.dataclass
class Cast(expr.Expression):
    """This class represents the `cast` function."""

    expression: expr.ColumnExpression
    type: datatype.DataType

    def sql(self) -> str:
        return f"CAST ({self.expression.sql()} AS {self.type.name})"
