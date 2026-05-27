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

import asyncio
from typing import Literal, Mapping, Optional, Tuple

import google.api_core.exceptions
import google.cloud.bigquery.job as bq_job
import google.cloud.bigquery.table as bq_table
import google.cloud.bigquery_storage_v1
from google.cloud import bigquery

import bigframes
import bigframes.core.compile
import bigframes.core.events
import bigframes.session._io.bigquery as bq_io
import bigframes.session.metrics
from bigframes import exceptions as bfe
from bigframes.core import bq_data, compile, nodes
from bigframes.core.compile.configs import CompileRequest
from bigframes.session import execution_spec, executor, semi_executor

_WRITE_DISPOSITIONS = {
    "fail": bigquery.WriteDisposition.WRITE_EMPTY,
    "replace": bigquery.WriteDisposition.WRITE_TRUNCATE,
    "append": bigquery.WriteDisposition.WRITE_APPEND,
}


class DirectGbqExecutor(semi_executor.SemiExecutor):
    def __init__(
        self,
        bqclient: bigquery.Client,
        bqstoragereadclient: google.cloud.bigquery_storage_v1.BigQueryReadClient,
        *,
        publisher: bigframes.core.events.Publisher,
        compiler: Literal["ibis", "sqlglot"] = "sqlglot",
        metrics: Optional[bigframes.session.metrics.ExecutionMetrics] = None,
        labels: Mapping[str, str] = {},
    ):
        self.bqclient = bqclient
        self._compiler_name = compiler
        self._bqstoragereadclient = bqstoragereadclient
        self._publisher = publisher
        self._metrics = metrics
        self._labels = labels

    async def execute(
        self,
        plan: nodes.BigFrameNode,
        spec: execution_spec.ExecutionSpec,
    ) -> executor.ExecuteResult:
        """Just execute whatever plan as is, without further caching or decomposition."""
        compiled = compile.compile_sql(
            CompileRequest(
                plan,
                sort_rows=spec.ordered,
                peek_count=spec.peek,
            ),
            compiler_name=self._compiler_name,
        )
        job_config = bigquery.QueryJobConfig()
        dest_spec = spec.destination_spec
        cluster_cols = None
        can_skip_job = True
        if isinstance(dest_spec, execution_spec.TableOutputSpec):
            job_config.destination = dest_spec.table
            job_config.write_disposition = _WRITE_DISPOSITIONS[dest_spec.if_exists]
            cluster_cols = dest_spec.cluster_cols if dest_spec.cluster_cols else None
            job_config.clustering_fields = cluster_cols
            can_skip_job = False
        elif isinstance(dest_spec, execution_spec.EphemeralTableSpec):
            # Need destination table, but jobless execution might not create a destination table
            can_skip_job = False
        elif dest_spec is not None:
            raise ValueError(
                f"Direct GBQ Executor does not support destination: {dest_spec}"
            )

        job_config.labels["bigframes-dtypes"] = compiled.encoded_type_refs
        if self._labels:
            job_config.labels.update(self._labels)
        if spec.bigquery_config is not None:
            if spec.bigquery_config.extra_query_labels:
                job_config.labels.update(spec.bigquery_config.extra_query_labels)
            if spec.bigquery_config.maximum_bytes_billed is not None:
                job_config.maximum_bytes_billed = (
                    spec.bigquery_config.maximum_bytes_billed
                )

        iterator, query_job = await asyncio.to_thread(
            self._run_execute_query,
            sql=compiled.sql,
            job_config=job_config,
            query_with_job=(not can_skip_job),
            session=plan.session,
            cell_execution_count=spec.cell_execution_count,
        )
        result_bq_data = None
        if query_job and query_job.destination:
            dst = query_job.destination
            result_bq_data = bq_data.BigqueryDataSource(
                table=bq_data.GbqNativeTable.from_ref_and_schema(
                    dst,
                    tuple(compiled.sql_schema),
                    cluster_cols=cluster_cols or (),
                    location=iterator.location or self.bqclient.location,
                    table_type="TABLE",
                ),
                schema=plan.schema,
                ordering=compiled.row_order,
                n_rows=iterator.total_rows,
            )

        execution_metadata = executor.ExecutionMetadata.from_iterator_and_job(
            iterator, query_job
        )
        result_mostly_cached = (
            hasattr(iterator, "_is_almost_completely_cached")
            and iterator._is_almost_completely_cached()
        )

        if (isinstance(dest_spec, execution_spec.EphemeralTableSpec)) or (
            (result_bq_data is not None) and not result_mostly_cached
        ):
            assert result_bq_data is not None, "expected result table but none exists"
            return executor.BQTableExecuteResult(
                data=result_bq_data,
                project_id=self.bqclient.project,
                storage_client=self._bqstoragereadclient,
                execution_metadata=execution_metadata,
                selected_fields=tuple((col, col) for col in plan.schema.names),
            )
        else:
            return executor.LocalExecuteResult(
                data=iterator.to_arrow().select(plan.schema.names),
                bf_schema=plan.schema,
                execution_metadata=execution_metadata,
            )

    def _run_execute_query(
        self,
        sql: str,
        job_config: bq_job.QueryJobConfig,
        query_with_job: bool,
        session,
        cell_execution_count: Optional[int] = None,
    ) -> Tuple[bq_table.RowIterator, Optional[bigquery.QueryJob]]:
        """
        Starts BigQuery query job and waits for results.
        """
        try:
            if query_with_job:
                return bq_io.start_query_with_job(
                    self.bqclient,
                    sql,
                    job_config=job_config,
                    metrics=self._metrics,
                    publisher=self._publisher,
                    session=session,
                    cell_execution_count=cell_execution_count,
                )
            else:
                return (
                    bq_io.start_query_job_optional(
                        self.bqclient,
                        sql,
                        job_config=job_config,
                        metrics=self._metrics,
                        publisher=self._publisher,
                        session=session,
                        cell_execution_count=cell_execution_count,
                    ),
                    None,
                )
        except google.api_core.exceptions.BadRequest as e:
            # Unfortunately, this error type does not have a separate error code or exception type
            if "Resources exceeded during query execution" in e.message:
                new_message = "Computation is too complex to execute as a single query. Try using DataFrame.cache() on intermediate results, or setting bigframes.options.compute.enable_multi_query_execution."
                raise bfe.QueryComplexityError(new_message) from e
            else:
                raise
