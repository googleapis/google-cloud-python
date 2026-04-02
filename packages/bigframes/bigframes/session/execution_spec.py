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
from typing import Literal, Optional, Union

from google.cloud import bigquery


@dataclasses.dataclass(frozen=True)
class ExecutionSpec:
    destination_spec: Union[TableOutputSpec, GcsOutputSpec, CacheSpec, None] = None
    peek: Optional[int] = None
    ordered: bool = (
        False  # ordered and promise_under_10gb must both be together for bq execution
    )
    # This is an optimization flag for gbq execution, it doesn't change semantics, but if promise is falsely made, errors may occur
    promise_under_10gb: bool = False


# This one is temporary, in future, caching will not be done through immediate execution, but will label nodes
# that will be cached only when a super-tree is executed
@dataclasses.dataclass(frozen=True)
class CacheSpec:
    cluster_cols: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class TableOutputSpec:
    table: bigquery.TableReference
    cluster_cols: tuple[str, ...]
    if_exists: Literal["fail", "replace", "append"] = "fail"


@dataclasses.dataclass(frozen=True)
class GcsOutputSpec:
    uri: str
    format: Literal["json", "csv", "parquet"]
    # sequence of (option, value) pairs
    export_options: tuple[tuple[str, Union[bool, str]], ...]
