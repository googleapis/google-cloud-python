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
import typing

import google.cloud.bigquery

from bigframes.core import nodes, ordering


@dataclasses.dataclass(frozen=True)
class CompileRequest:
    node: nodes.BigFrameNode
    sort_rows: bool
    materialize_all_order_keys: bool = False
    peek_count: typing.Optional[int] = None


@dataclasses.dataclass(frozen=True)
class CompileResult:
    sql: str
    sql_schema: typing.Sequence[google.cloud.bigquery.SchemaField]
    row_order: typing.Optional[ordering.RowOrdering]
