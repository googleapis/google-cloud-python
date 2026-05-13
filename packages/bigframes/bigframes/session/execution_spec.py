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
from typing import Literal, Mapping, Optional, Union

from google.cloud import bigquery


@dataclasses.dataclass(frozen=True)
class ExecutionSpec:
    # destination for the result of the operation. Executor may also incidentally create other temporary tables for its own purposes.
    destination_spec: Union[
        TableOutputSpec, GcsOutputSpec, EphemeralTableSpec, None
    ] = None
    # If set, the result will be truncated to the given number of rows. Which N rows is
    # implementation dependent and not stable.
    peek: Optional[int] = None
    # Controls whether output iterator is ordered. Cannot be true if destination is not
    # guaranteed to be ordered.
    ordered: bool = False
    # This is an optimization flag for gbq execution, it doesn't change semantics, but if promise is falsely made, errors may occur
    promise_under_10gb: bool = False

    labels: tuple[tuple[str, str], ...] = ()

    def add_labels(self, labels: Mapping[str, str]) -> ExecutionSpec:
        return dataclasses.replace(self, labels=self.labels + tuple(labels.items()))


# Used internally by execution
@dataclasses.dataclass(frozen=True)
class EphemeralTableSpec:
    """
    Specifies that the result of an operation should be a temporary table of some sort.

    No guarantees on lifetime, may be a session temp table, or a bq-created temp table with <24hr life.

    Used internally when results need temporary staging, because they are large (>10GB), or needed in subsequent operations.
    """

    pass


@dataclasses.dataclass(frozen=True)
class CacheSpec:
    """
    Specifies that the result of an operation should be a session temp table.
    The table will be automatically deleted after the session ends.
    """

    cluster_cols: tuple[
        str, ...
    ] = ()  # if empty, will cluster using order key if ordering_key is set
    # Controls ordering and whether extra columns are materialized to preserve ordering
    # Any extra columns will be appended to the end of the schema.
    # None: ordering may be discarded entirely (ordering metadata will still be provided if ordering is derivable from materialized columns)
    # order_rows: the result iterator itself will be ordered. For gbq execution, result cannot exceed 10GB.
    # order_key: the result set ordered by a key, may materialize extra columns.
    # offsets_col: order the result set by an offsets column, materializes one extra column.
    ordering: Literal["order_rows", "offsets_col", "order_key"] | None = None


@dataclasses.dataclass(frozen=True)
class TableOutputSpec:
    """
    Specifies that the result of an operation should be exported to a specific named table.

    The executor is not responsible for managing lifecycle of the table.
    """

    table: bigquery.TableReference
    cluster_cols: tuple[str, ...] = ()
    if_exists: Literal["fail", "replace", "append"] = "fail"


@dataclasses.dataclass(frozen=True)
class GcsOutputSpec:
    uri: str
    format: Literal["json", "csv", "parquet"]
    # sequence of (option, value) pairs
    export_options: tuple[tuple[str, Union[bool, str]], ...]
