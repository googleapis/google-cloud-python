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

"""Python classes representing GoogleSQL syntax nodes, adhering to the official syntax:
https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax"""

from __future__ import annotations

from bigframes.core.compile.googlesql.datatype import DataType
from bigframes.core.compile.googlesql.expression import (
    _escape_chars,
    AliasExpression,
    ColumnExpression,
    CTEExpression,
    identifier,
    StarExpression,
    TableExpression,
)
from bigframes.core.compile.googlesql.function import Cast
from bigframes.core.compile.googlesql.query import (
    AsAlias,
    FromClause,
    FromItem,
    NonRecursiveCTE,
    QueryExpr,
    Select,
    SelectAll,
    SelectExpression,
)

__all__ = [
    "_escape_chars",
    "identifier",
    "AliasExpression",
    "AsAlias",
    "Cast",
    "ColumnExpression",
    "CTEExpression",
    "DataType",
    "FromClause",
    "FromItem",
    "NonRecursiveCTE",
    "QueryExpr",
    "Select",
    "SelectAll",
    "SelectExpression",
    "StarExpression",
    "StringType",
    "TableExpression",
]
