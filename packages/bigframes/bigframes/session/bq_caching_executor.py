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

from __future__ import annotations

import dataclasses
import math
import os
from typing import cast, Literal, Mapping, Optional, Sequence, Tuple, Union
import warnings
import weakref

import google.api_core.exceptions
from google.cloud import bigquery
import google.cloud.bigquery.job as bq_job
import google.cloud.bigquery.table as bq_table
import google.cloud.bigquery_storage_v1

import bigframes.core
from bigframes.core import compile, rewrite
import bigframes.core.guid
import bigframes.core.nodes as nodes
import bigframes.core.ordering as order
import bigframes.core.tree_properties as tree_properties
import bigframes.dtypes
import bigframes.exceptions as bfe
import bigframes.features
from bigframes.session import executor, local_scan_executor, read_api_execution
import bigframes.session._io.bigquery as bq_io
import bigframes.session.metrics
import bigframes.session.planner
import bigframes.session.temporary_storage

# Max complexity that should be executed as a single query
QUERY_COMPLEXITY_LIMIT = 1e7
# Number of times to factor out subqueries before giving up.
MAX_SUBTREE_FACTORINGS = 5
_MAX_CLUSTER_COLUMNS = 4
MAX_SMALL_RESULT_BYTES = 10 * 1024 * 1024 * 1024  # 10G


@dataclasses.dataclass
class OutputSpec:
    require_bq_table: bool
    cluster_cols: tuple[str, ...]

    def with_require_table(self, value: bool) -> OutputSpec:
        return dataclasses.replace(self, require_bq_table=value)


def _get_default_output_spec() -> OutputSpec:
    return OutputSpec(
        require_bq_table=bigframes.options._allow_large_results, cluster_cols=()
    )


class ExecutionCache:
    def __init__(self):
        # current assumption is only 1 cache of a given node
        # in future, might have multiple caches, with different layout, localities
        self._cached_executions: weakref.WeakKeyDictionary[
            nodes.BigFrameNode, nodes.BigFrameNode
        ] = weakref.WeakKeyDictionary()

    @property
    def mapping(self) -> Mapping[nodes.BigFrameNode, nodes.BigFrameNode]:
        return self._cached_executions

    def cache_results_table(
        self,
        original_root: nodes.BigFrameNode,
        table: bigquery.Table,
        ordering: order.RowOrdering,
    ):
        # Assumption: GBQ cached table uses field name as bq column name
        scan_list = nodes.ScanList(
            tuple(
                nodes.ScanItem(field.id, field.dtype, field.id.sql)
                for field in original_root.fields
            )
        )
        cached_replacement = nodes.CachedTableNode(
            source=nodes.BigqueryDataSource(
                nodes.GbqTable.from_table(table),
                ordering=ordering,
                n_rows=table.num_rows,
            ),
            scan_list=scan_list,
            table_session=original_root.session,
            original_node=original_root,
        )
        assert original_root.schema == cached_replacement.schema
        self._cached_executions[original_root] = cached_replacement


class BigQueryCachingExecutor(executor.Executor):
    """Computes BigFrames values using BigQuery Engine.

    This executor can cache expressions. If those expressions are executed later, this session
    will re-use the pre-existing results from previous executions.

    This class is not thread-safe.
    """

    def __init__(
        self,
        bqclient: bigquery.Client,
        storage_manager: bigframes.session.temporary_storage.TemporaryStorageManager,
        bqstoragereadclient: google.cloud.bigquery_storage_v1.BigQueryReadClient,
        *,
        strictly_ordered: bool = True,
        metrics: Optional[bigframes.session.metrics.ExecutionMetrics] = None,
    ):
        self.bqclient = bqclient
        self.storage_manager = storage_manager
        self.strictly_ordered: bool = strictly_ordered
        self.cache: ExecutionCache = ExecutionCache()
        self.metrics = metrics
        self.bqstoragereadclient = bqstoragereadclient
        # Simple left-to-right precedence for now
        self._semi_executors = (
            read_api_execution.ReadApiSemiExecutor(
                bqstoragereadclient=bqstoragereadclient,
                project=self.bqclient.project,
            ),
            local_scan_executor.LocalScanExecutor(),
        )

    def to_sql(
        self,
        array_value: bigframes.core.ArrayValue,
        offset_column: Optional[str] = None,
        ordered: bool = False,
        enable_cache: bool = True,
    ) -> str:
        if offset_column:
            array_value, _ = array_value.promote_offsets()
        node = self.logical_plan(array_value.node) if enable_cache else array_value.node
        compiled = compile.compile_sql(compile.CompileRequest(node, sort_rows=ordered))
        return compiled.sql

    def execute(
        self,
        array_value: bigframes.core.ArrayValue,
        *,
        ordered: bool = True,
        use_explicit_destination: Optional[bool] = None,
    ) -> executor.ExecuteResult:
        if bigframes.options.compute.enable_multi_query_execution:
            self._simplify_with_caching(array_value)

        output_spec = _get_default_output_spec()
        if use_explicit_destination is not None:
            output_spec = output_spec.with_require_table(use_explicit_destination)

        plan = self.logical_plan(array_value.node)
        return self._execute_plan(
            plan,
            ordered=ordered,
            output_spec=output_spec,
        )

    def peek(
        self,
        array_value: bigframes.core.ArrayValue,
        n_rows: int,
        use_explicit_destination: Optional[bool] = None,
    ) -> executor.ExecuteResult:
        """
        A 'peek' efficiently accesses a small number of rows in the dataframe.
        """
        plan = self.logical_plan(array_value.node)
        if not tree_properties.can_fast_peek(plan):
            msg = bfe.format_message("Peeking this value cannot be done efficiently.")
            warnings.warn(msg)

        output_spec = _get_default_output_spec()
        if use_explicit_destination is not None:
            output_spec = output_spec.with_require_table(use_explicit_destination)

        return self._execute_plan(
            plan, ordered=False, output_spec=output_spec, peek=n_rows
        )

    def export_gbq(
        self,
        array_value: bigframes.core.ArrayValue,
        destination: bigquery.TableReference,
        if_exists: Literal["fail", "replace", "append"] = "fail",
        cluster_cols: Sequence[str] = [],
    ):
        """
        Export the ArrayValue to an existing BigQuery table.
        """
        if bigframes.options.compute.enable_multi_query_execution:
            self._simplify_with_caching(array_value)

        dispositions = {
            "fail": bigquery.WriteDisposition.WRITE_EMPTY,
            "replace": bigquery.WriteDisposition.WRITE_TRUNCATE,
            "append": bigquery.WriteDisposition.WRITE_APPEND,
        }
        sql = self.to_sql(array_value, ordered=False)
        job_config = bigquery.QueryJobConfig(
            write_disposition=dispositions[if_exists],
            destination=destination,
            clustering_fields=cluster_cols if cluster_cols else None,
        )
        # TODO(swast): plumb through the api_name of the user-facing api that
        # caused this query.
        _, query_job = self._run_execute_query(
            sql=sql,
            job_config=job_config,
        )

        has_timedelta_col = any(
            t == bigframes.dtypes.TIMEDELTA_DTYPE for t in array_value.schema.dtypes
        )

        if if_exists != "append" and has_timedelta_col:
            # Only update schema if this is not modifying an existing table, and the
            # new table contains timedelta columns.
            table = self.bqclient.get_table(destination)
            table.schema = array_value.schema.to_bigquery()
            self.bqclient.update_table(table, ["schema"])

        return query_job

    def export_gcs(
        self,
        array_value: bigframes.core.ArrayValue,
        uri: str,
        format: Literal["json", "csv", "parquet"],
        export_options: Mapping[str, Union[bool, str]],
    ):
        query_job = self.execute(
            array_value,
            ordered=False,
            use_explicit_destination=True,
        ).query_job
        assert query_job is not None
        result_table = query_job.destination
        assert result_table is not None
        export_data_statement = bq_io.create_export_data_statement(
            f"{result_table.project}.{result_table.dataset_id}.{result_table.table_id}",
            uri=uri,
            format=format,
            export_options=dict(export_options),
        )

        bq_io.start_query_with_client(
            self.bqclient,
            export_data_statement,
            job_config=bigquery.QueryJobConfig(),
            api_name=f"dataframe-to_{format.lower()}",
            metrics=self.metrics,
        )
        return query_job

    def dry_run(
        self, array_value: bigframes.core.ArrayValue, ordered: bool = True
    ) -> bigquery.QueryJob:
        sql = self.to_sql(array_value, ordered=ordered)
        job_config = bigquery.QueryJobConfig(dry_run=True)
        query_job = self.bqclient.query(sql, job_config=job_config)
        return query_job

    def cached(
        self, array_value: bigframes.core.ArrayValue, *, config: executor.CacheConfig
    ) -> None:
        """Write the block to a session table."""
        # First, see if we can reuse the existing cache
        # TODO(b/415105423): Provide feedback to user on whether new caching action was deemed necessary
        # TODO(b/415105218): Make cached a deferred action
        if config.if_cached == "reuse-any":
            if self._is_trivially_executable(array_value):
                return
        elif config.if_cached == "reuse-strict":
            # This path basically exists to make sure that repr in head mode is optimized for subsequent repr operations.
            if config.optimize_for == "head":
                if tree_properties.can_fast_head(array_value.node):
                    return
            else:
                raise NotImplementedError(
                    "if_cached='reuse-strict' currently only supported with optimize_for='head'"
                )
        elif config.if_cached != "replace":
            raise ValueError(f"Unexpected 'if_cached' arg: {config.if_cached}")

        if config.optimize_for == "auto":
            self._cache_with_session_awareness(array_value)
        elif config.optimize_for == "head":
            self._cache_with_offsets(array_value)
        else:
            assert isinstance(config.optimize_for, executor.HierarchicalKey)
            self._cache_with_cluster_cols(
                array_value, cluster_cols=config.optimize_for.columns
            )

    # Helpers
    def _run_execute_query(
        self,
        sql: str,
        job_config: Optional[bq_job.QueryJobConfig] = None,
        api_name: Optional[str] = None,
        query_with_job: bool = True,
    ) -> Tuple[bq_table.RowIterator, Optional[bigquery.QueryJob]]:
        """
        Starts BigQuery query job and waits for results.
        """
        job_config = bq_job.QueryJobConfig() if job_config is None else job_config
        if bigframes.options.compute.maximum_bytes_billed is not None:
            job_config.maximum_bytes_billed = (
                bigframes.options.compute.maximum_bytes_billed
            )

        if not self.strictly_ordered:
            job_config.labels["bigframes-mode"] = "unordered"

        try:
            iterator, query_job = bq_io.start_query_with_client(
                self.bqclient,
                sql,
                job_config=job_config,
                api_name=api_name,
                metrics=self.metrics,
                query_with_job=query_with_job,
            )
            return iterator, query_job

        except google.api_core.exceptions.BadRequest as e:
            # Unfortunately, this error type does not have a separate error code or exception type
            if "Resources exceeded during query execution" in e.message:
                new_message = "Computation is too complex to execute as a single query. Try using DataFrame.cache() on intermediate results, or setting bigframes.options.compute.enable_multi_query_execution."
                raise bigframes.exceptions.QueryComplexityError(new_message) from e
            else:
                raise

    def replace_cached_subtrees(self, node: nodes.BigFrameNode) -> nodes.BigFrameNode:
        return nodes.top_down(node, lambda x: self.cache.mapping.get(x, x))

    def _is_trivially_executable(self, array_value: bigframes.core.ArrayValue):
        """
        Can the block be evaluated very cheaply?
        If True, the array_value probably is not worth caching.
        """
        # Once rewriting is available, will want to rewrite before
        # evaluating execution cost.
        return tree_properties.is_trivially_executable(
            self.logical_plan(array_value.node)
        )

    def logical_plan(self, root: nodes.BigFrameNode) -> nodes.BigFrameNode:
        """
        Apply universal logical simplifications that are helpful regardless of engine.
        """
        plan = self.replace_cached_subtrees(root)
        plan = rewrite.column_pruning(plan)
        plan = plan.top_down(rewrite.fold_row_counts)
        return plan

    def _cache_with_cluster_cols(
        self, array_value: bigframes.core.ArrayValue, cluster_cols: Sequence[str]
    ):
        """Executes the query and uses the resulting table to rewrite future executions."""
        plan = self.logical_plan(array_value.node)
        compiled = compile.compile_sql(
            compile.CompileRequest(
                plan, sort_rows=False, materialize_all_order_keys=True
            )
        )
        tmp_table_ref = self._sql_as_cached_temp_table(
            compiled.sql,
            compiled.sql_schema,
            cluster_cols=bq_io.select_cluster_cols(compiled.sql_schema, cluster_cols),
        )
        tmp_table = self.bqclient.get_table(tmp_table_ref)
        assert compiled.row_order is not None
        self.cache.cache_results_table(array_value.node, tmp_table, compiled.row_order)

    def _cache_with_offsets(self, array_value: bigframes.core.ArrayValue):
        """Executes the query and uses the resulting table to rewrite future executions."""
        offset_column = bigframes.core.guid.generate_guid("bigframes_offsets")
        w_offsets, offset_column = array_value.promote_offsets()
        compiled = compile.compile_sql(
            compile.CompileRequest(
                self.logical_plan(w_offsets.node),
                sort_rows=False,
            )
        )
        tmp_table_ref = self._sql_as_cached_temp_table(
            compiled.sql,
            compiled.sql_schema,
            cluster_cols=[offset_column],
        )
        tmp_table = self.bqclient.get_table(tmp_table_ref)
        assert compiled.row_order is not None
        self.cache.cache_results_table(array_value.node, tmp_table, compiled.row_order)

    def _cache_with_session_awareness(
        self,
        array_value: bigframes.core.ArrayValue,
    ) -> None:
        session_forest = [obj._block._expr.node for obj in array_value.session.objects]
        # These node types are cheap to re-compute
        target, cluster_cols = bigframes.session.planner.session_aware_cache_plan(
            array_value.node, list(session_forest)
        )
        cluster_cols_sql_names = [id.sql for id in cluster_cols]
        if len(cluster_cols) > 0:
            self._cache_with_cluster_cols(
                bigframes.core.ArrayValue(target), cluster_cols_sql_names
            )
        elif self.strictly_ordered:
            self._cache_with_offsets(bigframes.core.ArrayValue(target))
        else:
            self._cache_with_cluster_cols(bigframes.core.ArrayValue(target), [])

    def _simplify_with_caching(self, array_value: bigframes.core.ArrayValue):
        """Attempts to handle the complexity by caching duplicated subtrees and breaking the query into pieces."""
        # Apply existing caching first
        for _ in range(MAX_SUBTREE_FACTORINGS):
            if (
                self.logical_plan(array_value.node).planning_complexity
                < QUERY_COMPLEXITY_LIMIT
            ):
                return

            did_cache = self._cache_most_complex_subtree(array_value.node)
            if not did_cache:
                return

    def _cache_most_complex_subtree(self, node: nodes.BigFrameNode) -> bool:
        # TODO: If query fails, retry with lower complexity limit
        selection = tree_properties.select_cache_target(
            node,
            min_complexity=(QUERY_COMPLEXITY_LIMIT / 500),
            max_complexity=QUERY_COMPLEXITY_LIMIT,
            cache=dict(self.cache.mapping),
            # Heuristic: subtree_compleixty * (copies of subtree)^2
            heuristic=lambda complexity, count: math.log(complexity)
            + 2 * math.log(count),
        )
        if selection is None:
            # No good subtrees to cache, just return original tree
            return False

        self._cache_with_cluster_cols(bigframes.core.ArrayValue(selection), [])
        return True

    def _sql_as_cached_temp_table(
        self,
        sql: str,
        schema: Sequence[bigquery.SchemaField],
        cluster_cols: Sequence[str],
    ) -> bigquery.TableReference:
        assert len(cluster_cols) <= _MAX_CLUSTER_COLUMNS
        temp_table = self.storage_manager.create_temp_table(schema, cluster_cols)

        # TODO: Get default job config settings
        job_config = cast(
            bigquery.QueryJobConfig,
            bigquery.QueryJobConfig.from_api_repr({}),
        )
        job_config.destination = temp_table
        _, query_job = self._run_execute_query(
            sql,
            job_config=job_config,
            api_name="cached",
        )
        assert query_job is not None
        query_job.result()
        return query_job.destination

    def _validate_result_schema(
        self,
        array_value: bigframes.core.ArrayValue,
        bq_schema: list[bigquery.SchemaField],
    ):
        actual_schema = _sanitize(tuple(bq_schema))
        ibis_schema = compile.test_only_ibis_inferred_schema(
            self.logical_plan(array_value.node)
        ).to_bigquery()
        internal_schema = _sanitize(array_value.schema.to_bigquery())
        if not bigframes.features.PANDAS_VERSIONS.is_arrow_list_dtype_usable:
            return

        if internal_schema != actual_schema:
            raise ValueError(
                f"This error should only occur while testing. BigFrames internal schema: {internal_schema} does not match actual schema: {actual_schema}"
            )

        if ibis_schema != actual_schema:
            raise ValueError(
                f"This error should only occur while testing. Ibis schema: {ibis_schema} does not match actual schema: {actual_schema}"
            )

    def _execute_plan(
        self,
        plan: nodes.BigFrameNode,
        ordered: bool,
        output_spec: OutputSpec,
        peek: Optional[int] = None,
    ) -> executor.ExecuteResult:
        """Just execute whatever plan as is, without further caching or decomposition."""
        # First try to execute fast-paths
        if not output_spec.require_bq_table:
            for semi_executor in self._semi_executors:
                maybe_result = semi_executor.execute(plan, ordered=ordered, peek=peek)
                if maybe_result:
                    return maybe_result

        # Use explicit destination to avoid 10GB limit of temporary table
        destination_table = (
            self.storage_manager.create_temp_table(
                plan.schema.to_bigquery(), cluster_cols=output_spec.cluster_cols
            )
            if output_spec.require_bq_table
            else None
        )

        # TODO(swast): plumb through the api_name of the user-facing api that
        # caused this query.
        job_config = bigquery.QueryJobConfig()
        # Use explicit destination to avoid 10GB limit of temporary table
        if destination_table is not None:
            job_config.destination = destination_table
        compiled = compile.compile_sql(
            compile.CompileRequest(plan, sort_rows=ordered, peek_count=peek)
        )
        iterator, query_job = self._run_execute_query(
            sql=compiled.sql,
            job_config=job_config,
            query_with_job=(destination_table is not None),
        )

        if query_job:
            size_bytes = self.bqclient.get_table(query_job.destination).num_bytes
        else:
            size_bytes = None

        if size_bytes is not None and size_bytes >= MAX_SMALL_RESULT_BYTES:
            msg = bfe.format_message(
                "The query result size has exceeded 10 GB. In BigFrames 2.0 and "
                "later, you might need to manually set `allow_large_results=True` in "
                "the IO method or adjust the BigFrames option: "
                "`bigframes.options.compute.allow_large_results=True`."
            )
            warnings.warn(msg, FutureWarning)
        # Runs strict validations to ensure internal type predictions and ibis are completely in sync
        # Do not execute these validations outside of testing suite.
        if "PYTEST_CURRENT_TEST" in os.environ:
            self._validate_result_schema(
                bigframes.core.ArrayValue(plan), iterator.schema
            )

        return executor.ExecuteResult(
            arrow_batches=iterator.to_arrow_iterable(
                bqstorage_client=self.bqstoragereadclient
            ),
            schema=plan.schema,
            query_job=query_job,
            total_bytes=size_bytes,
            total_rows=iterator.total_rows,
        )


def _sanitize(
    schema: Tuple[bigquery.SchemaField, ...]
) -> Tuple[bigquery.SchemaField, ...]:
    # Schema inferred from SQL strings and Ibis expressions contain only names, types and modes,
    # so we disregard other fields (e.g timedelta description for timedelta columns) for validations.
    return tuple(
        bigquery.SchemaField(
            f.name,
            f.field_type,
            f.mode,  # type:ignore
            fields=_sanitize(f.fields),
        )
        for f in schema
    )
