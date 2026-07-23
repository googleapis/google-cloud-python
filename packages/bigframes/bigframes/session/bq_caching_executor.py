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

import asyncio
import concurrent.futures
import dataclasses
import math
import threading
from typing import Literal, Optional, Sequence, Tuple

import google.api_core.exceptions
import google.cloud.bigquery_storage_v1
from google.cloud import bigquery

import bigframes
import bigframes.constants
import bigframes.core
import bigframes.core.events
import bigframes.core.guid
import bigframes.core.nodes as nodes
import bigframes.core.ordering
import bigframes.core.schema as schemata
import bigframes.core.tree_properties as tree_properties
import bigframes.dtypes
import bigframes.functions._function_session as bff_session
import bigframes.operations as ops
import bigframes.session._io.bigquery as bq_io
import bigframes.session.execution_cache as execution_cache
import bigframes.session.execution_spec as ex_spec
import bigframes.session.metrics
import bigframes.session.planner
import bigframes.session.temporary_storage
from bigframes.core import (
    compile,
    expression,
    guid,
    identifiers,
    local_data,
    rewrite,
)
from bigframes.core.compile.sqlglot import sql as sg_sql
from bigframes.core.compile.sqlglot import sqlglot_ir
from bigframes.functions import udf_def
from bigframes.session import (
    direct_gbq_execution,
    executor,
    loader,
    local_scan_executor,
    read_api_execution,
    semi_executor,
)

# Max complexity that should be executed as a single query
QUERY_COMPLEXITY_LIMIT = 1e7
# Number of times to factor out subqueries before giving up.
MAX_SUBTREE_FACTORINGS = 5
_MAX_CLUSTER_COLUMNS = 4
MAX_SMALL_RESULT_BYTES = 10 * 1024 * 1024 * 1024  # 10G


_bg_loop = None
_bg_thread = None
_bg_lock = threading.Lock()


def _get_bg_loop():
    global _bg_loop, _bg_thread
    with _bg_lock:
        if _bg_loop is None:
            loop = asyncio.new_event_loop()
            _bg_loop = loop

            def run():
                asyncio.set_event_loop(loop)
                loop.run_forever()

            _bg_thread = threading.Thread(
                target=run, daemon=True, name="bigframes-bg-loop"
            )
            _bg_thread.start()
    return _bg_loop


def _run_sync(coro):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop is None:
        return asyncio.run(coro)
    else:
        bg_loop = _get_bg_loop()
        future = asyncio.run_coroutine_threadsafe(coro, bg_loop)
        return future.result()


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
        metrics: Optional[bigframes.session.metrics.ExecutionMetrics] = None,
        enable_polars_execution: bool = False,
        publisher: bigframes.core.events.Publisher,
        labels: tuple[tuple[str, str], ...] = (),
        compiler_name: Literal["ibis", "sqlglot"] = "sqlglot",
        cache: Optional[execution_cache.ExecutionCache] = None,
        function_manager: bff_session.FunctionSession,
    ):
        self.bqclient = bqclient
        self.storage_manager = storage_manager
        self.cache: execution_cache.ExecutionCache = (
            cache or execution_cache.ExecutionCache()
        )
        self.metrics = metrics
        self.loader = loader
        self._enable_polars_execution = enable_polars_execution
        self._publisher = publisher
        self._compiler_name = compiler_name

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
        self._gbq_executor = direct_gbq_execution.DirectGbqExecutor(
            bqclient,
            compiler=compiler_name,
            bqstoragereadclient=bqstoragereadclient,
            metrics=self.metrics,
            publisher=self._publisher,
            labels=dict(labels),
        )
        self._function_manager = function_manager

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
            self._prepare_plan_simplify(array_value.node)
            if enable_cache
            else array_value.node
        )
        node = _run_sync(self._substitute_large_local_sources(node))
        compiled = compile.compile_sql(
            compile.CompileRequest(node, sort_rows=ordered),
            compiler_name=self._compiler_name,
        )
        return compiled.sql

    def execute(
        self,
        array_value: bigframes.core.ArrayValue,
        execution_spec: ex_spec.ExecutionSpec,
    ) -> executor.ExecuteResult:
        # Need to grab thread local before starting async execution.
        execution_spec = execution_spec.with_compute_options(bigframes.options.compute)
        return _run_sync(
            self._execute_async(
                array_value,
                execution_spec,
            )
        )

    async def _execute_async(
        self,
        array_value: bigframes.core.ArrayValue,
        execution_spec: ex_spec.ExecutionSpec,
    ) -> executor.ExecuteResult:
        await self._publisher.publish_async(bigframes.core.events.ExecutionStarted())
        maybe_result = await self._try_execute_semi_executors(
            array_value, execution_spec
        )
        if maybe_result is not None:
            return maybe_result
        result = await self._execute_bigquery(
            array_value,
            execution_spec,
        )
        await self._publisher.publish_async(
            bigframes.core.events.EventEnvelope(
                event=bigframes.core.events.ExecutionFinished(result=result),
                cell_execution_count=execution_spec.cell_execution_count,
            )
        )
        return result

    async def _try_execute_semi_executors(
        self,
        array_value: bigframes.core.ArrayValue,
        execution_spec: ex_spec.ExecutionSpec,
    ) -> Optional[executor.ExecuteResult]:
        plan = self._prepare_plan_simplify(array_value.node)
        for exec in self._semi_executors:
            maybe_result = await exec.execute(plan, execution_spec)
            if maybe_result:
                await self._publisher.publish_async(
                    bigframes.core.events.EventEnvelope(
                        event=bigframes.core.events.ExecutionFinished(
                            result=maybe_result,
                        ),
                        cell_execution_count=execution_spec.cell_execution_count,
                    )
                )
                return maybe_result
        return None

    async def _execute_bigquery(
        self,
        array_value: bigframes.core.ArrayValue,
        execution_spec: ex_spec.ExecutionSpec,
    ) -> executor.ExecuteResult:
        dest_spec = execution_spec.destination_spec
        # Recursive handlers for different cases, maybe extract to explicit interface.
        if isinstance(dest_spec, ex_spec.GcsOutputSpec):
            execution_spec = dataclasses.replace(
                execution_spec, destination_spec=ex_spec.EphemeralTableSpec()
            )
            results = await self._execute_bigquery(
                array_value,
                execution_spec,
            )
            await self._export_result_gcs(results, dest_spec)
            return results
        elif isinstance(dest_spec, ex_spec.TableOutputSpec):
            return await self._execute_gbq_table_export(
                array_value,
                execution_spec,
            )
        # Force table creation if result might be large (and user explicitly allowed large results)
        elif isinstance(dest_spec, ex_spec.EphemeralTableSpec) or (dest_spec is None):
            if not execution_spec.promise_under_10gb:
                table = await asyncio.to_thread(
                    self.storage_manager.create_temp_table,
                    array_value.schema.to_bigquery(),
                )
                execution_spec = dataclasses.replace(
                    execution_spec,
                    destination_spec=ex_spec.TableOutputSpec(
                        table=table, if_exists="append"
                    ),
                )
                # We don't use _execute_gbq_table_export, as this result is internal, not exported.
                return await self._execute_gbq_query_only(
                    array_value,
                    execution_spec,
                )
        # At this point, dst should be unspecified, a specific bq table, or an ephemeral temp table that fits in <10gb
        return await self._execute_gbq_query_only(
            array_value,
            execution_spec,
        )

    async def _execute_gbq_table_export(
        self,
        array_value: bigframes.core.ArrayValue,
        execution_spec: ex_spec.ExecutionSpec,
    ) -> executor.ExecuteResult:
        dest_spec = execution_spec.destination_spec
        assert isinstance(dest_spec, ex_spec.TableOutputSpec)
        existing_table = await self._maybe_find_existing_table(dest_spec)
        if (existing_table is not None) and _is_schema_match(
            existing_table.schema, array_value.schema
        ):
            # Special DML path - maybe this should be configurable, dml vs query destination has tradeoffs
            execution_spec = dataclasses.replace(
                execution_spec, destination_spec=ex_spec.EphemeralTableSpec()
            )
            results = await self._execute_bigquery(
                array_value,
                execution_spec,
            )
            assert isinstance(results, executor.BQTableExecuteResult)
            await self._export_gbq_with_dml(results, dest_spec)
            result: executor.ExecuteResult = results
        else:
            result = await self._execute_gbq_query_only(
                array_value,
                execution_spec,
            )

        has_special_dtype_col = any(
            t in (bigframes.dtypes.TIMEDELTA_DTYPE, bigframes.dtypes.OBJ_REF_DTYPE)
            for t in array_value.schema.dtypes
        )
        if dest_spec.if_exists != "append" and has_special_dtype_col:
            table = await asyncio.to_thread(self.bqclient.get_table, dest_spec.table)
            table.schema = array_value.schema.to_bigquery()
            await asyncio.to_thread(self.bqclient.update_table, table, ["schema"])

        return result

    async def _execute_gbq_query_only(
        self,
        array_value: bigframes.core.ArrayValue,
        execution_spec: ex_spec.ExecutionSpec,
    ) -> executor.ExecuteResult:
        gbq_plan = await self._prepare_plan_bq_execution(
            array_value.node, execution_spec.bigquery_config
        )
        result = await self._gbq_executor.execute(gbq_plan, execution_spec)
        if result is None:
            raise ValueError(
                f"Couldn't execute plan {array_value.node} with {execution_spec}"
            )
        return result

    async def _export_result_gcs(
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
        await asyncio.to_thread(
            bq_io.start_query_with_job,
            self.bqclient,
            export_data_statement,
            job_config=bigquery.QueryJobConfig(),
            metrics=self.metrics,
            project=None,
            location=None,
            timeout=None,
            publisher=self._publisher,
        )

    async def _export_gbq_with_dml(
        self, result: executor.BQTableExecuteResult, spec: ex_spec.TableOutputSpec
    ):
        """
        Export the ArrayValue to an existing BigQuery table, using DML.
        """
        # b/409086472: Uses DML for table appends and replacements to avoid
        # BigQuery `RATE_LIMIT_EXCEEDED` errors, as per quota limits:
        # https://cloud.google.com/bigquery/quotas#standard_tables
        assert result.query_job is not None
        assert result.query_job.destination is not None
        ir = sqlglot_ir.SQLGlotIR.from_table(
            result.query_job.destination.project,
            result.query_job.destination.dataset_id,
            result.query_job.destination.table_id,
        )
        sql = ""
        if spec.if_exists == "append":
            sql = sg_sql.to_sql(sg_sql.insert(ir.expr.as_select_all(), spec.table))
        else:  # for "replace"
            assert spec.if_exists == "replace"
            sql = sg_sql.to_sql(sg_sql.replace(ir.expr.as_select_all(), spec.table))

        await asyncio.to_thread(
            bq_io.start_query_with_job,
            self.bqclient,
            sql,
            job_config=bigquery.QueryJobConfig(),
            metrics=self.metrics,
            publisher=self._publisher,
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
        # Get compute options before passing to async method, can be thread-local
        bq_compute_options = ex_spec.BqComputeOptions.from_compute_options(
            bigframes.options.compute
        )
        return _run_sync(
            self._cached_async(
                array_value, config=config, compute_options=bq_compute_options
            )
        )

    async def _cached_async(
        self,
        array_value: bigframes.core.ArrayValue,
        *,
        config: executor.CacheConfig,
        compute_options: ex_spec.BqComputeOptions,
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
            await self._cache_with_session_awareness(
                array_value, compute_options=compute_options
            )
        elif config.optimize_for == "head":
            await self._cache_with_offsets(array_value, compute_options=compute_options)
        else:
            assert isinstance(config.optimize_for, executor.HierarchicalKey)
            await self._cache_with_cluster_cols(
                array_value,
                cluster_cols=config.optimize_for.columns,
                compute_options=compute_options,
            )

    async def _execute_to_cached_table(
        self,
        plan: nodes.BigFrameNode,
        cache_spec: ex_spec.CacheSpec,
        compute_options: ex_spec.BqComputeOptions,
    ) -> executor.ExecuteResult:
        # "ephemeral" temp tables created in the course of exeuction, don't need to be allocated
        # materialized ordering only really makes sense for internal temp tables used by caching
        cluster_cols = cache_spec.cluster_cols
        # Rewrite plan to materialize ordering as extra columns
        if cache_spec.ordering == "offsets_col":
            order_col_id = guid.generate_guid()
            plan = nodes.PromoteOffsetsNode(plan, identifiers.ColumnId(order_col_id))
            cluster_cols = (order_col_id,)
            ordering: bigframes.core.ordering.RowOrdering = (
                bigframes.core.ordering.TotalOrdering.from_offset_col(order_col_id)
            )
        elif cache_spec.ordering == "order_key":
            plan, ordering = rewrite.pull_out_order(plan)
        destination_table = await asyncio.to_thread(
            self.storage_manager.create_temp_table,
            plan.schema.to_bigquery(),
            cluster_cols,
        )
        arr_value = bigframes.core.ArrayValue(plan)
        execution_spec = ex_spec.ExecutionSpec(
            destination_spec=ex_spec.TableOutputSpec(
                table=destination_table,
                cluster_cols=cluster_cols,
                if_exists="replace",
            ),
            bigquery_config=compute_options,
        )
        # We don't use _execute_gbq_table_export, as this result is internal, not exported.
        result = await self._execute_gbq_query_only(
            arr_value,
            execution_spec,
        )
        assert isinstance(result, executor.BQTableExecuteResult), (
            "expected result to be BQTableExecuteResult"
        )
        result._data = dataclasses.replace(result._data, ordering=ordering)
        return result

    # Helpers
    def _is_trivially_executable(self, array_value: bigframes.core.ArrayValue):
        """
        Can the block be evaluated very cheaply?
        If True, the array_value probably is not worth caching.
        """
        # Once rewriting is available, will want to rewrite before
        # evaluating execution cost.
        simplified_plan = self._prepare_plan_simplify(array_value.node)
        return tree_properties.is_trivially_executable(simplified_plan)

    def _prepare_plan_simplify(self, plan: nodes.BigFrameNode) -> nodes.BigFrameNode:
        """Prepare the plan by simplifying it with caches and removing unused operators."""
        plan = self.cache.subsitute_cached_subplans(plan)
        plan = rewrite.column_pruning(plan)
        plan = plan.top_down(rewrite.fold_row_counts)
        return plan

    async def _deploy_undeployed_udfs(
        self, plan: nodes.BigFrameNode
    ) -> nodes.BigFrameNode:
        referenced_udfs = list(set(self._collect_udf_defs(plan)))
        deployed_mapping: dict[udf_def.PythonUdf, udf_def.BigqueryUdf] = {}
        tasks = [
            asyncio.to_thread(
                self._function_manager._deploy_udf,
                udf,
            )
            for udf in referenced_udfs
        ]
        results = await asyncio.gather(*tasks)
        deployed_mapping = dict(zip(referenced_udfs, results))

        return self._subsitute_temporary_functions(plan, deployed_mapping)

    def _collect_udf_defs(self, plan: nodes.BigFrameNode) -> list[udf_def.PythonUdf]:
        udf_defs: list[udf_def.PythonUdf] = []
        exprs = [
            expr for node in plan.unique_nodes() for expr in node._node_expressions
        ]
        expr_nodes = [expr for expr in exprs for expr in expr.walk()]
        for expr_node in expr_nodes:
            if (
                isinstance(expr_node, expression.OpExpression)
                and isinstance(expr_node.op, ops.PythonUdfOp)
                and isinstance(expr_node.op.function_def, udf_def.PythonUdf)
            ):
                udf_defs.append(expr_node.op.function_def)
        return udf_defs

    def _subsitute_temporary_functions(
        self,
        plan: nodes.BigFrameNode,
        deployed_mapping: dict[udf_def.PythonUdf, udf_def.BigqueryUdf],
    ) -> nodes.BigFrameNode:
        def replace_udf_expr(e: expression.Expression) -> expression.Expression:
            if isinstance(e, expression.OpExpression) and isinstance(
                e.op, ops.PythonUdfOp
            ):
                func_def = e.op.function_def
                # We will have already deployed the function
                assert func_def in deployed_mapping
                deployed_func = deployed_mapping[func_def]
                rf_op = ops.RemoteFunctionOp(function_def=deployed_func)
                return dataclasses.replace(e, op=rf_op)
            return e

        def replace_in_expr(expr: expression.Expression) -> expression.Expression:
            return expr.bottom_up(replace_udf_expr)

        def replace_in_node(node: nodes.BigFrameNode) -> nodes.BigFrameNode:
            if hasattr(node, "transform_exprs"):
                return node.transform_exprs(replace_in_expr)
            return node

        return plan.bottom_up(replace_in_node)

    async def _prepare_plan_bq_execution(
        self,
        plan: nodes.BigFrameNode,
        compute_options: Optional[ex_spec.BqComputeOptions] = None,
    ) -> nodes.BigFrameNode:
        """Prepare the plan for BigQuery execution by caching subtrees and uploading large local sources."""
        plan = await self._deploy_undeployed_udfs(plan)
        if compute_options is not None and compute_options.enable_multi_query_execution:
            await self._simplify_with_caching(plan, compute_options=compute_options)
        plan = self._prepare_plan_simplify(plan)
        plan = await self._substitute_large_local_sources(plan)
        return plan

    async def _cache_with_cluster_cols(
        self,
        array_value: bigframes.core.ArrayValue,
        cluster_cols: Sequence[str],
        compute_options: ex_spec.BqComputeOptions,
    ):
        """Executes the query and uses the resulting table to rewrite future executions."""
        cluster_cols = [
            col
            for col in cluster_cols
            if bigframes.dtypes.is_clusterable(array_value.schema.get_type(col))
        ]
        cluster_cols = cluster_cols[:_MAX_CLUSTER_COLUMNS]
        result = await self._execute_to_cached_table(
            array_value.node,
            ex_spec.CacheSpec(cluster_cols=tuple(cluster_cols), ordering="order_key"),
            compute_options=compute_options,
        )
        assert isinstance(result, executor.BQTableExecuteResult)
        assert result._data.ordering is not None
        self.cache.cache_results_table(array_value.node, result._data)

    async def _cache_with_offsets(
        self,
        array_value: bigframes.core.ArrayValue,
        compute_options: ex_spec.BqComputeOptions,
    ):
        """Executes the query and uses the resulting table to rewrite future executions."""
        result = await self._execute_to_cached_table(
            array_value.node,
            ex_spec.CacheSpec(ordering="offsets_col"),
            compute_options=compute_options,
        )
        assert isinstance(result, executor.BQTableExecuteResult)
        assert result._data.ordering is not None
        self.cache.cache_results_table(array_value.node, result._data)

    async def _cache_with_session_awareness(
        self,
        array_value: bigframes.core.ArrayValue,
        compute_options: ex_spec.BqComputeOptions,
    ) -> None:
        session_forest = [obj._block._expr.node for obj in array_value.session.objects]
        # These node types are cheap to re-compute
        target, cluster_cols = bigframes.session.planner.session_aware_cache_plan(
            array_value.node, list(session_forest)
        )
        cluster_cols_sql_names = [id.sql for id in cluster_cols]
        if len(cluster_cols) > 0:
            await self._cache_with_cluster_cols(
                bigframes.core.ArrayValue(target),
                cluster_cols_sql_names,
                compute_options=compute_options,
            )
        elif not target.order_ambiguous:
            await self._cache_with_offsets(
                bigframes.core.ArrayValue(target),
                compute_options=compute_options,
            )
        else:
            await self._cache_with_cluster_cols(
                bigframes.core.ArrayValue(target),
                [],
                compute_options=compute_options,
            )

    async def _simplify_with_caching(
        self, plan: nodes.BigFrameNode, compute_options: ex_spec.BqComputeOptions
    ):
        """Attempts to handle the complexity by caching duplicated subtrees and breaking the query into pieces."""
        # Apply existing caching first
        for _ in range(MAX_SUBTREE_FACTORINGS):
            if (
                self._prepare_plan_simplify(plan).planning_complexity
                < QUERY_COMPLEXITY_LIMIT
            ):
                return

            did_cache = await self._cache_most_complex_subtree(
                plan, compute_options=compute_options
            )
            if not did_cache:
                return

    async def _cache_most_complex_subtree(
        self, node: nodes.BigFrameNode, compute_options: ex_spec.BqComputeOptions
    ) -> bool:
        # TODO: If query fails, retry with lower complexity limit
        selection = tree_properties.select_cache_target(
            node,
            min_complexity=(QUERY_COMPLEXITY_LIMIT / 500),
            max_complexity=QUERY_COMPLEXITY_LIMIT,
            cache=self.cache,
            # Heuristic: subtree_compleixty * (copies of subtree)^2
            heuristic=lambda complexity, count: (
                math.log(complexity) + 2 * math.log(count)
            ),
        )
        if selection is None:
            # No good subtrees to cache, just return original tree
            return False

        await self._cache_with_cluster_cols(
            bigframes.core.ArrayValue(selection),
            [],
            compute_options=compute_options,
        )
        return True

    async def _substitute_large_local_sources(self, original_root: nodes.BigFrameNode):
        """
        Replace large local sources with the uploaded version of those datasources.
        """
        # Step 1: Upload all previously un-uploaded data
        needs_upload = []
        for leaf in original_root.unique_nodes():
            if isinstance(leaf, nodes.ReadLocalNode):
                if (
                    leaf.local_data_source.metadata.total_bytes
                    > bigframes.constants.MAX_INLINE_BYTES
                ):
                    needs_upload.append(leaf.local_data_source)

        futures: dict[concurrent.futures.Future, local_data.ManagedArrowTable] = dict()
        for local_source in needs_upload:
            future = self.loader.read_data_async(
                local_source, bigframes.core.guid.generate_guid()
            )
            futures[future] = local_source
        try:
            results = await asyncio.gather(
                *(asyncio.wrap_future(f) for f in futures.keys())
            )
            for future, result in zip(futures.keys(), results):
                self.cache.cache_remote_replacement(futures[future], result)
        except Exception as e:
            # cancel all futures
            for future in futures:
                future.cancel()
            raise e

        # Step 2: Replace local scans with remote scans
        def map_local_scans(node: nodes.BigFrameNode):
            if not isinstance(node, nodes.ReadLocalNode):
                return node
            uploaded_local_data = self.cache.get_uploaded_local_data(
                node.local_data_source
            )
            if uploaded_local_data is None:
                return node

            scan_list = node.scan_list.remap_source_ids(
                uploaded_local_data.source_mapping
            )
            # offsets_col isn't part of ReadTableNode, so emulate by adding to end of scan_list
            if node.offsets_col is not None:
                # Offsets are always implicitly the final column of uploaded data
                # See: Loader.load_data
                scan_list = scan_list.append(
                    uploaded_local_data.bq_source.table.physical_schema[-1].name,
                    bigframes.dtypes.INT_DTYPE,
                    node.offsets_col,
                )
            return nodes.ReadTableNode(
                uploaded_local_data.bq_source, scan_list, node.session
            )

        return original_root.bottom_up(map_local_scans)

    async def _maybe_find_existing_table(
        self, spec: ex_spec.TableOutputSpec
    ) -> Optional[bigquery.Table]:
        # validate destination table
        try:
            table = await asyncio.to_thread(self.bqclient.get_table, spec.table)
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


def _is_schema_match(
    table_schema: Tuple[bigquery.SchemaField, ...],
    schema: schemata.ArraySchema,
) -> bool:
    if len(table_schema) != len(schema.items):
        return False
    for field, schema_item in zip(table_schema, schema.items):
        if field.name != schema_item.column:
            return False
        _, field_dtype = bigframes.dtypes.convert_schema_field(field)
        if field_dtype != schema_item.dtype:
            return False
    return True
