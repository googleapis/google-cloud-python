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

import math
import threading
from typing import Literal, Mapping, Optional, Sequence, Tuple
import weakref

import google.api_core.exceptions
from google.cloud import bigquery
import google.cloud.bigquery.job as bq_job
import google.cloud.bigquery.table as bq_table
import google.cloud.bigquery_storage_v1

import bigframes
from bigframes import exceptions as bfe
import bigframes.constants
import bigframes.core
from bigframes.core import bq_data, compile, local_data, rewrite
import bigframes.core.compile.sqlglot.sqlglot_ir as sqlglot_ir
import bigframes.core.events
import bigframes.core.guid
import bigframes.core.identifiers
import bigframes.core.nodes as nodes
import bigframes.core.schema as schemata
import bigframes.core.tree_properties as tree_properties
import bigframes.dtypes
from bigframes.session import (
    executor,
    loader,
    local_scan_executor,
    read_api_execution,
    semi_executor,
)
import bigframes.session._io.bigquery as bq_io
import bigframes.session.execution_spec as ex_spec
import bigframes.session.metrics
import bigframes.session.planner
import bigframes.session.temporary_storage

# Max complexity that should be executed as a single query
QUERY_COMPLEXITY_LIMIT = 1e7
# Number of times to factor out subqueries before giving up.
MAX_SUBTREE_FACTORINGS = 5
_MAX_CLUSTER_COLUMNS = 4
MAX_SMALL_RESULT_BYTES = 10 * 1024 * 1024 * 1024  # 10G

SourceIdMapping = Mapping[str, str]


class ExecutionCache:
    def __init__(self):
        # current assumption is only 1 cache of a given node
        # in future, might have multiple caches, with different layout, localities
        self._cached_executions: weakref.WeakKeyDictionary[
            nodes.BigFrameNode, nodes.CachedTableNode
        ] = weakref.WeakKeyDictionary()
        self._uploaded_local_data: weakref.WeakKeyDictionary[
            local_data.ManagedArrowTable,
            tuple[bq_data.BigqueryDataSource, SourceIdMapping],
        ] = weakref.WeakKeyDictionary()

    @property
    def mapping(self) -> Mapping[nodes.BigFrameNode, nodes.BigFrameNode]:
        return self._cached_executions

    def cache_results_table(
        self,
        original_root: nodes.BigFrameNode,
        data: bq_data.BigqueryDataSource,
    ):
        # Assumption: GBQ cached table uses field name as bq column name
        scan_list = nodes.ScanList(
            tuple(
                nodes.ScanItem(field.id, field.id.sql) for field in original_root.fields
            )
        )
        cached_replacement = nodes.CachedTableNode(
            source=data,
            scan_list=scan_list,
            table_session=original_root.session,
            original_node=original_root,
        )
        assert original_root.schema == cached_replacement.schema
        self._cached_executions[original_root] = cached_replacement

    def cache_remote_replacement(
        self,
        local_data: local_data.ManagedArrowTable,
        bq_data: bq_data.BigqueryDataSource,
    ):
        # bq table has one extra column for offsets, those are implicit for local data
        assert len(local_data.schema.items) + 1 == len(bq_data.table.physical_schema)
        mapping = {
            local_data.schema.items[i].column: bq_data.table.physical_schema[i].name
            for i in range(len(local_data.schema))
        }
        self._uploaded_local_data[local_data] = (bq_data, mapping)


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
        loader: loader.GbqDataLoader,
        *,
        strictly_ordered: bool = True,
        metrics: Optional[bigframes.session.metrics.ExecutionMetrics] = None,
        enable_polars_execution: bool = False,
        publisher: bigframes.core.events.Publisher,
    ):
        self.bqclient = bqclient
        self.storage_manager = storage_manager
        self.strictly_ordered: bool = strictly_ordered
        self.cache: ExecutionCache = ExecutionCache()
        self.metrics = metrics
        self.loader = loader
        self.bqstoragereadclient = bqstoragereadclient
        self._enable_polars_execution = enable_polars_execution
        self._publisher = publisher

        # TODO(tswast): Send events from semi-executors, too.
        self._semi_executors: Sequence[semi_executor.SemiExecutor] = (
            read_api_execution.ReadApiSemiExecutor(
                bqstoragereadclient=bqstoragereadclient,
                project=self.bqclient.project,
            ),
            local_scan_executor.LocalScanExecutor(),
        )
        if enable_polars_execution:
            from bigframes.session import polars_executor

            self._semi_executors = (
                *self._semi_executors,
                polars_executor.PolarsExecutor(),
            )
        self._upload_lock = threading.Lock()

    def to_sql(
        self,
        array_value: bigframes.core.ArrayValue,
        offset_column: Optional[str] = None,
        ordered: bool = False,
        enable_cache: bool = True,
    ) -> str:
        if offset_column:
            array_value, _ = array_value.promote_offsets()
        node = (
            self.prepare_plan(array_value.node, target="simplify")
            if enable_cache
            else array_value.node
        )
        node = self._substitute_large_local_sources(node)
        compiled = compile.compile_sql(compile.CompileRequest(node, sort_rows=ordered))
        return compiled.sql

    def execute(
        self,
        array_value: bigframes.core.ArrayValue,
        execution_spec: ex_spec.ExecutionSpec,
    ) -> executor.ExecuteResult:
        self._publisher.publish(bigframes.core.events.ExecutionStarted())

        # TODO: Support export jobs in combination with semi executors
        if execution_spec.destination_spec is None:
            plan = self.prepare_plan(array_value.node, target="simplify")
            for exec in self._semi_executors:
                maybe_result = exec.execute(
                    plan, ordered=execution_spec.ordered, peek=execution_spec.peek
                )
                if maybe_result:
                    self._publisher.publish(
                        bigframes.core.events.ExecutionFinished(
                            result=maybe_result,
                        )
                    )
                    return maybe_result

        if isinstance(execution_spec.destination_spec, ex_spec.TableOutputSpec):
            if execution_spec.peek or execution_spec.ordered:
                raise NotImplementedError(
                    "Ordering and peeking not supported for gbq export"
                )
            # separate path for export_gbq, as it has all sorts of annoying logic, such as possibly running as dml
            result = self._export_gbq(array_value, execution_spec.destination_spec)
            self._publisher.publish(
                bigframes.core.events.ExecutionFinished(
                    result=result,
                )
            )
            return result

        result = self._execute_plan_gbq(
            array_value.node,
            ordered=execution_spec.ordered,
            peek=execution_spec.peek,
            cache_spec=execution_spec.destination_spec
            if isinstance(execution_spec.destination_spec, ex_spec.CacheSpec)
            else None,
            must_create_table=not execution_spec.promise_under_10gb,
        )
        # post steps: export
        if isinstance(execution_spec.destination_spec, ex_spec.GcsOutputSpec):
            self._export_result_gcs(result, execution_spec.destination_spec)

        self._publisher.publish(
            bigframes.core.events.ExecutionFinished(
                result=result,
            )
        )
        return result

    def _export_result_gcs(
        self, result: executor.ExecuteResult, gcs_export_spec: ex_spec.GcsOutputSpec
    ):
        query_job = result.query_job
        assert query_job is not None
        result_table = query_job.destination
        assert result_table is not None
        export_data_statement = bq_io.create_export_data_statement(
            f"{result_table.project}.{result_table.dataset_id}.{result_table.table_id}",
            uri=gcs_export_spec.uri,
            format=gcs_export_spec.format,
            export_options=dict(gcs_export_spec.export_options),
        )
        bq_io.start_query_with_client(
            self.bqclient,
            export_data_statement,
            job_config=bigquery.QueryJobConfig(),
            metrics=self.metrics,
            project=None,
            location=None,
            timeout=None,
            query_with_job=True,
            publisher=self._publisher,
        )

    def _maybe_find_existing_table(
        self, spec: ex_spec.TableOutputSpec
    ) -> Optional[bigquery.Table]:
        # validate destination table
        try:
            table = self.bqclient.get_table(spec.table)
            if spec.if_exists == "fail":
                raise ValueError(f"Table already exists: {spec.table.__str__()}")

            if len(spec.cluster_cols) != 0:
                if (table.clustering_fields is None) or (
                    tuple(table.clustering_fields) != spec.cluster_cols
                ):
                    raise ValueError(
                        "Table clustering fields cannot be changed after the table has "
                        f"been created. Requested clustering fields: {spec.cluster_cols}, existing clustering fields: {table.clustering_fields}"
                    )
            return table
        except google.api_core.exceptions.NotFound:
            return None

    def _export_gbq(
        self, array_value: bigframes.core.ArrayValue, spec: ex_spec.TableOutputSpec
    ) -> executor.ExecuteResult:
        """
        Export the ArrayValue to an existing BigQuery table.
        """
        plan = self.prepare_plan(array_value.node, target="bq_execution")

        # validate destination table
        existing_table = self._maybe_find_existing_table(spec)

        compiled = compile.compile_sql(compile.CompileRequest(plan, sort_rows=False))
        sql = compiled.sql

        if (existing_table is not None) and _if_schema_match(
            existing_table.schema, array_value.schema
        ):
            # b/409086472: Uses DML for table appends and replacements to avoid
            # BigQuery `RATE_LIMIT_EXCEEDED` errors, as per quota limits:
            # https://cloud.google.com/bigquery/quotas#standard_tables
            job_config = bigquery.QueryJobConfig()
            ir = sqlglot_ir.SQLGlotIR.from_query_string(sql)
            if spec.if_exists == "append":
                sql = ir.insert(spec.table)
            else:  # for "replace"
                assert spec.if_exists == "replace"
                sql = ir.replace(spec.table)
        else:
            dispositions = {
                "fail": bigquery.WriteDisposition.WRITE_EMPTY,
                "replace": bigquery.WriteDisposition.WRITE_TRUNCATE,
                "append": bigquery.WriteDisposition.WRITE_APPEND,
            }
            job_config = bigquery.QueryJobConfig(
                write_disposition=dispositions[spec.if_exists],
                destination=spec.table,
                clustering_fields=spec.cluster_cols if spec.cluster_cols else None,
            )

        # TODO(swast): plumb through the api_name of the user-facing api that
        # caused this query.
        iterator, job = self._run_execute_query(
            sql=sql,
            job_config=job_config,
            session=array_value.session,
        )

        has_timedelta_col = any(
            t == bigframes.dtypes.TIMEDELTA_DTYPE for t in array_value.schema.dtypes
        )

        if spec.if_exists != "append" and has_timedelta_col:
            # Only update schema if this is not modifying an existing table, and the
            # new table contains timedelta columns.
            table = self.bqclient.get_table(spec.table)
            table.schema = array_value.schema.to_bigquery()
            self.bqclient.update_table(table, ["schema"])

        return executor.EmptyExecuteResult(
            bf_schema=array_value.schema,
            execution_metadata=executor.ExecutionMetadata.from_iterator_and_job(
                iterator, job
            ),
        )

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
        query_with_job: bool = True,
        session=None,
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
            # Trick the type checker into thinking we got a literal.
            if query_with_job:
                return bq_io.start_query_with_client(
                    self.bqclient,
                    sql,
                    job_config=job_config,
                    metrics=self.metrics,
                    project=None,
                    location=None,
                    timeout=None,
                    query_with_job=True,
                    publisher=self._publisher,
                    session=session,
                )
            else:
                return bq_io.start_query_with_client(
                    self.bqclient,
                    sql,
                    job_config=job_config,
                    metrics=self.metrics,
                    project=None,
                    location=None,
                    timeout=None,
                    query_with_job=False,
                    publisher=self._publisher,
                    session=session,
                )

        except google.api_core.exceptions.BadRequest as e:
            # Unfortunately, this error type does not have a separate error code or exception type
            if "Resources exceeded during query execution" in e.message:
                new_message = "Computation is too complex to execute as a single query. Try using DataFrame.cache() on intermediate results, or setting bigframes.options.compute.enable_multi_query_execution."
                raise bfe.QueryComplexityError(new_message) from e
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
            self.prepare_plan(array_value.node)
        )

    def prepare_plan(
        self,
        plan: nodes.BigFrameNode,
        target: Literal["simplify", "bq_execution"] = "simplify",
    ) -> nodes.BigFrameNode:
        """
        Prepare the plan by simplifying it with caches, removing unused operators. Has modes for different contexts.

        "simplify" removes unused operations and subsitutes subtrees with their previously cached equivalents
        "bq_execution" is the most heavy option, preparing the plan for bq execution by also caching subtrees, uploading large local sources
        """
        # TODO: We should model plan decomposition and data uploading as work steps rather than as plan preparation.
        if (
            target == "bq_execution"
            and bigframes.options.compute.enable_multi_query_execution
        ):
            self._simplify_with_caching(plan)

        plan = self.replace_cached_subtrees(plan)
        plan = rewrite.column_pruning(plan)
        plan = plan.top_down(rewrite.fold_row_counts)

        if target == "bq_execution":
            plan = self._substitute_large_local_sources(plan)

        return plan

    def _cache_with_cluster_cols(
        self, array_value: bigframes.core.ArrayValue, cluster_cols: Sequence[str]
    ):
        """Executes the query and uses the resulting table to rewrite future executions."""
        execution_spec = ex_spec.ExecutionSpec(
            destination_spec=ex_spec.CacheSpec(cluster_cols=tuple(cluster_cols))
        )
        self.execute(
            array_value,
            execution_spec=execution_spec,
        )

    def _cache_with_offsets(self, array_value: bigframes.core.ArrayValue):
        """Executes the query and uses the resulting table to rewrite future executions."""
        execution_spec = ex_spec.ExecutionSpec(
            destination_spec=ex_spec.CacheSpec(cluster_cols=tuple())
        )
        self.execute(
            array_value,
            execution_spec=execution_spec,
        )

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

    def _simplify_with_caching(self, plan: nodes.BigFrameNode):
        """Attempts to handle the complexity by caching duplicated subtrees and breaking the query into pieces."""
        # Apply existing caching first
        for _ in range(MAX_SUBTREE_FACTORINGS):
            if (
                self.prepare_plan(plan, "simplify").planning_complexity
                < QUERY_COMPLEXITY_LIMIT
            ):
                return

            did_cache = self._cache_most_complex_subtree(plan)
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

    def _substitute_large_local_sources(self, original_root: nodes.BigFrameNode):
        """
        Replace large local sources with the uploaded version of those datasources.
        """
        # Step 1: Upload all previously un-uploaded data
        for leaf in original_root.unique_nodes():
            if isinstance(leaf, nodes.ReadLocalNode):
                if (
                    leaf.local_data_source.metadata.total_bytes
                    > bigframes.constants.MAX_INLINE_BYTES
                ):
                    self._upload_local_data(leaf.local_data_source)

        # Step 2: Replace local scans with remote scans
        def map_local_scans(node: nodes.BigFrameNode):
            if not isinstance(node, nodes.ReadLocalNode):
                return node
            if node.local_data_source not in self.cache._uploaded_local_data:
                return node
            bq_source, source_mapping = self.cache._uploaded_local_data[
                node.local_data_source
            ]
            scan_list = node.scan_list.remap_source_ids(source_mapping)
            # offsets_col isn't part of ReadTableNode, so emulate by adding to end of scan_list
            if node.offsets_col is not None:
                # Offsets are always implicitly the final column of uploaded data
                # See: Loader.load_data
                scan_list = scan_list.append(
                    bq_source.table.physical_schema[-1].name,
                    bigframes.dtypes.INT_DTYPE,
                    node.offsets_col,
                )
            return nodes.ReadTableNode(bq_source, scan_list, node.session)

        return original_root.bottom_up(map_local_scans)

    def _upload_local_data(self, local_table: local_data.ManagedArrowTable):
        if local_table in self.cache._uploaded_local_data:
            return
        # Lock prevents concurrent repeated work, but slows things down.
        # Might be better as a queue and a worker thread
        with self._upload_lock:
            if local_table not in self.cache._uploaded_local_data:
                uploaded = self.loader.load_data(
                    local_table, bigframes.core.guid.generate_guid()
                )
                self.cache.cache_remote_replacement(local_table, uploaded)

    def _execute_plan_gbq(
        self,
        plan: nodes.BigFrameNode,
        ordered: bool,
        peek: Optional[int] = None,
        cache_spec: Optional[ex_spec.CacheSpec] = None,
        must_create_table: bool = True,
    ) -> executor.ExecuteResult:
        """Just execute whatever plan as is, without further caching or decomposition."""
        # TODO(swast): plumb through the api_name of the user-facing api that
        # caused this query.

        og_plan = plan
        og_schema = plan.schema

        plan = self.prepare_plan(plan, target="bq_execution")
        create_table = must_create_table
        cluster_cols: Sequence[str] = []
        if cache_spec is not None:
            if peek is not None:
                raise ValueError("peek is not compatible with caching.")

            create_table = True
            if not cache_spec.cluster_cols:

                offsets_id = bigframes.core.identifiers.ColumnId(
                    bigframes.core.guid.generate_guid()
                )
                plan = nodes.PromoteOffsetsNode(plan, offsets_id)
                cluster_cols = [offsets_id.sql]
            else:
                cluster_cols = [
                    col
                    for col in cache_spec.cluster_cols
                    if bigframes.dtypes.is_clusterable(plan.schema.get_type(col))
                ]
                cluster_cols = cluster_cols[:_MAX_CLUSTER_COLUMNS]

        compiled = compile.compile_sql(
            compile.CompileRequest(
                plan,
                sort_rows=ordered,
                peek_count=peek,
                materialize_all_order_keys=(cache_spec is not None),
            )
        )
        # might have more columns than og schema, for hidden ordering columns
        compiled_schema = compiled.sql_schema

        destination_table: Optional[bigquery.TableReference] = None

        job_config = bigquery.QueryJobConfig()
        if create_table:
            destination_table = self.storage_manager.create_temp_table(
                compiled_schema, cluster_cols
            )
            job_config.destination = destination_table

        iterator, query_job = self._run_execute_query(
            sql=compiled.sql,
            job_config=job_config,
            query_with_job=(destination_table is not None),
            session=plan.session,
        )

        # we could actually cache even when caching is not explicitly requested, but being conservative for now
        result_bq_data = None
        if query_job and query_job.destination:
            # we might add extra sql columns in compilation, esp if caching w ordering, infer a bigframes type for them
            result_bf_schema = _result_schema(og_schema, list(compiled.sql_schema))
            dst = query_job.destination
            result_bq_data = bq_data.BigqueryDataSource(
                table=bq_data.GbqTable(
                    dst.project,
                    dst.dataset_id,
                    dst.table_id,
                    tuple(compiled_schema),
                    is_physically_stored=True,
                    cluster_cols=tuple(cluster_cols),
                ),
                schema=result_bf_schema,
                ordering=compiled.row_order,
                n_rows=iterator.total_rows,
            )

        if cache_spec is not None:
            assert result_bq_data is not None
            assert compiled.row_order is not None
            self.cache.cache_results_table(og_plan, result_bq_data)

        execution_metadata = executor.ExecutionMetadata.from_iterator_and_job(
            iterator, query_job
        )
        result_mostly_cached = (
            hasattr(iterator, "_is_almost_completely_cached")
            and iterator._is_almost_completely_cached()
        )
        if result_bq_data is not None and not result_mostly_cached:
            return executor.BQTableExecuteResult(
                data=result_bq_data,
                project_id=self.bqclient.project,
                storage_client=self.bqstoragereadclient,
                execution_metadata=execution_metadata,
                selected_fields=tuple((col, col) for col in og_schema.names),
            )
        else:
            return executor.LocalExecuteResult(
                data=iterator.to_arrow().select(og_schema.names),
                bf_schema=plan.schema,
                execution_metadata=execution_metadata,
            )


def _result_schema(
    logical_schema: schemata.ArraySchema, sql_schema: list[bigquery.SchemaField]
) -> schemata.ArraySchema:
    inferred_schema = bigframes.dtypes.bf_type_from_type_kind(sql_schema)
    inferred_schema.update(logical_schema._mapping)
    return schemata.ArraySchema(
        tuple(schemata.SchemaItem(col, dtype) for col, dtype in inferred_schema.items())
    )


def _if_schema_match(
    table_schema: Tuple[bigquery.SchemaField, ...], schema: schemata.ArraySchema
) -> bool:
    if len(table_schema) != len(schema.items):
        return False
    for field in table_schema:
        if field.name not in schema.names:
            return False
        if bigframes.dtypes.convert_schema_field(field)[1] != schema.get_type(
            field.name
        ):
            return False
    return True
