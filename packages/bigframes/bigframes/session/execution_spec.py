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

from bigframes._config import ComputeOptions


@dataclasses.dataclass(frozen=True)
class BqComputeOptions:
    enable_multi_query_execution: bool = True
    maximum_bytes_billed: Optional[int] = None
    extra_query_labels: tuple[tuple[str, str], ...] = ()

    @classmethod
    def from_compute_options(cls, compute_options: ComputeOptions) -> BqComputeOptions:
        return cls(
            enable_multi_query_execution=compute_options.enable_multi_query_execution,
            maximum_bytes_billed=compute_options.maximum_bytes_billed,
            extra_query_labels=tuple(compute_options.extra_query_labels.items()),
        )

    def push_labels(self, labels: Mapping[str, str]) -> BqComputeOptions:
        return dataclasses.replace(
            self,
            extra_query_labels=tuple(labels.items()) + self.extra_query_labels,
        )


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

    # BigQuery specific options
    bigquery_config: Optional[BqComputeOptions] = None
    cell_execution_count: Optional[int] = None

    def with_bq_labels(self, labels: Mapping[str, str]) -> ExecutionSpec:
        bq_config = self.bigquery_config or BqComputeOptions()
        return dataclasses.replace(self, bigquery_config=bq_config.push_labels(labels))

    def with_compute_options(self, compute_options: ComputeOptions) -> ExecutionSpec:
        """
        Grabs the current global or thread-local config and binds it to the execution spec.

        Returns a new ExecutionSpec with the current configuration applied.
        """
        new_bq_config = BqComputeOptions.from_compute_options(compute_options)
        if self.bigquery_config:
            # merge labels, new ComputeOptions takes priority for everything else
            new_bq_config = new_bq_config.push_labels(
                dict(self.bigquery_config.extra_query_labels)
            )

        cell_execution_count = self.cell_execution_count
        if cell_execution_count is None:
            from bigframes.core.utils import get_ipython_execution_count

            cell_execution_count = get_ipython_execution_count()

        return dataclasses.replace(
            self,
            bigquery_config=new_bq_config,
            cell_execution_count=cell_execution_count,
        )


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
