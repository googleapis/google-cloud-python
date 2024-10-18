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
from typing import (
    Callable,
    cast,
    Iterator,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
)
import warnings
import weakref

import google.api_core.exceptions
import google.cloud.bigquery as bigquery
import google.cloud.bigquery.job as bq_job
import google.cloud.bigquery.table as bq_table
import google.cloud.bigquery_storage_v1
import pyarrow

import bigframes.core
import bigframes.core.compile
import bigframes.core.guid
import bigframes.core.identifiers
import bigframes.core.nodes as nodes
import bigframes.core.ordering as order
import bigframes.core.schema
import bigframes.core.tree_properties as tree_properties
import bigframes.features
import bigframes.formatting_helpers as formatting_helpers
import bigframes.session._io.bigquery as bq_io
import bigframes.session.metrics
import bigframes.session.planner
import bigframes.session.temp_storage

# Max complexity that should be executed as a single query
QUERY_COMPLEXITY_LIMIT = 1e7
# Number of times to factor out subqueries before giving up.
MAX_SUBTREE_FACTORINGS = 5
_MAX_CLUSTER_COLUMNS = 4
# TODO: b/338258028 Enable pruning to reduce text size.
ENABLE_PRUNING = False


@dataclasses.dataclass(frozen=True)
class ExecuteResult:
    arrow_batches: Callable[[], Iterator[pyarrow.RecordBatch]]
    schema: bigframes.core.schema.ArraySchema
    query_job: Optional[bigquery.QueryJob] = None
    total_bytes: Optional[int] = None
    total_rows: Optional[int] = None

    def to_arrow_table(self) -> pyarrow.Table:
        # Need to provide schema if no result rows, as arrow can't infer
        # If ther are rows, it is safest to infer schema from batches.
        # Any discrepencies between predicted schema and actual schema will produce errors.
        return pyarrow.Table.from_batches(
            self.arrow_batches(),
            self.schema.to_pyarrow() if not self.total_rows else None,
        )


class BigQueryCachingExecutor:
    """Computes BigFrames values using BigQuery Engine.

    This executor can cache expressions. If those expressions are executed later, this session
    will re-use the pre-existing results from previous executions.

    This class is not thread-safe.
    """

    def __init__(
        self,
        bqclient: bigquery.Client,
        storage_manager: bigframes.session.temp_storage.TemporaryGbqStorageManager,
        bqstoragereadclient: google.cloud.bigquery_storage_v1.BigQueryReadClient,
        strictly_ordered: bool = True,
        metrics: Optional[bigframes.session.metrics.ExecutionMetrics] = None,
    ):
        self.bqclient = bqclient
        self.storage_manager = storage_manager
        self.compiler: bigframes.core.compile.SQLCompiler = (
            bigframes.core.compile.SQLCompiler(strict=strictly_ordered)
        )
        self.strictly_ordered: bool = strictly_ordered
        self._cached_executions: weakref.WeakKeyDictionary[
            nodes.BigFrameNode, nodes.BigFrameNode
        ] = weakref.WeakKeyDictionary()
        self.metrics = metrics
        self.bqstoragereadclient = bqstoragereadclient

    def to_sql(
        self,
        array_value: bigframes.core.ArrayValue,
        offset_column: Optional[str] = None,
        col_id_overrides: Mapping[str, str] = {},
        ordered: bool = False,
        enable_cache: bool = True,
    ) -> str:
        """
        Convert an ArrayValue to a sql query that will yield its value.
        """
        if offset_column:
            array_value, internal_offset_col = array_value.promote_offsets()
            col_id_overrides = dict(col_id_overrides)
            col_id_overrides[internal_offset_col] = offset_column
        node = (
            self.replace_cached_subtrees(array_value.node)
            if enable_cache
            else array_value.node
        )
        if ordered:
            return self.compiler.compile_ordered(
                node, col_id_overrides=col_id_overrides
            )
        return self.compiler.compile_unordered(node, col_id_overrides=col_id_overrides)

    def execute(
        self,
        array_value: bigframes.core.ArrayValue,
        *,
        ordered: bool = True,
        col_id_overrides: Mapping[str, str] = {},
        use_explicit_destination: bool = False,
        get_size_bytes: bool = False,
        page_size: Optional[int] = None,
        max_results: Optional[int] = None,
    ):
        """
        Execute the ArrayValue, storing the result to a temporary session-owned table.
        """
        if bigframes.options.compute.enable_multi_query_execution:
            self._simplify_with_caching(array_value)

        sql = self.to_sql(
            array_value, ordered=ordered, col_id_overrides=col_id_overrides
        )
        adjusted_schema = array_value.schema.rename(col_id_overrides)
        job_config = bigquery.QueryJobConfig()
        # Use explicit destination to avoid 10GB limit of temporary table
        if use_explicit_destination:
            destination_table = self.storage_manager.create_temp_table(
                adjusted_schema.to_bigquery(), cluster_cols=[]
            )
            job_config.destination = destination_table
        # TODO(swast): plumb through the api_name of the user-facing api that
        # caused this query.
        iterator, query_job = self._run_execute_query(
            sql=sql,
            job_config=job_config,
            page_size=page_size,
            max_results=max_results,
        )

        # Though we provide the read client, iterator may or may not use it based on what is efficient for the result
        def iterator_supplier():
            return iterator.to_arrow_iterable(bqstorage_client=self.bqstoragereadclient)

        if get_size_bytes is True:
            size_bytes = self.bqclient.get_table(query_job.destination).num_bytes
        else:
            size_bytes = None

        # Runs strict validations to ensure internal type predictions and ibis are completely in sync
        # Do not execute these validations outside of testing suite.
        if "PYTEST_CURRENT_TEST" in os.environ and len(col_id_overrides) == 0:
            self._validate_result_schema(array_value, iterator.schema)

        return ExecuteResult(
            arrow_batches=iterator_supplier,
            schema=adjusted_schema,
            query_job=query_job,
            total_bytes=size_bytes,
            total_rows=iterator.total_rows,
        )

    def export_gbq(
        self,
        array_value: bigframes.core.ArrayValue,
        col_id_overrides: Mapping[str, str],
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
        sql = self.to_sql(array_value, ordered=False, col_id_overrides=col_id_overrides)
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
        return query_job

    def export_gcs(
        self,
        array_value: bigframes.core.ArrayValue,
        col_id_overrides: Mapping[str, str],
        uri: str,
        format: Literal["json", "csv", "parquet"],
        export_options: Mapping[str, Union[bool, str]],
    ):
        """
        Export the ArrayValue to gcs.
        """
        query_job = self.execute(
            array_value,
            ordered=False,
            col_id_overrides=col_id_overrides,
        ).query_job
        result_table = query_job.destination
        export_data_statement = bq_io.create_export_data_statement(
            f"{result_table.project}.{result_table.dataset_id}.{result_table.table_id}",
            uri=uri,
            format=format,
            export_options=dict(export_options),
        )
        job_config = bigquery.QueryJobConfig()
        bq_io.add_labels(job_config, api_name=f"dataframe-to_{format.lower()}")
        export_job = self.bqclient.query(export_data_statement, job_config=job_config)
        self._wait_on_job(export_job)
        return query_job

    def dry_run(
        self, array_value: bigframes.core.ArrayValue, ordered: bool = True
    ) -> bigquery.QueryJob:
        """
        Dry run executing the ArrayValue.

        Does not actually execute the data but will get stats and indicate any invalid query errors.
        """
        sql = self.to_sql(array_value, ordered=ordered)
        job_config = bigquery.QueryJobConfig(dry_run=True)
        bq_io.add_labels(job_config)
        query_job = self.bqclient.query(sql, job_config=job_config)
        _ = query_job.result()
        return query_job

    def peek(
        self,
        array_value: bigframes.core.ArrayValue,
        n_rows: int,
    ) -> ExecuteResult:
        """
        A 'peek' efficiently accesses a small number of rows in the dataframe.
        """
        plan = self.replace_cached_subtrees(array_value.node)
        if not tree_properties.can_fast_peek(plan):
            warnings.warn("Peeking this value cannot be done efficiently.")

        sql = self.compiler.compile_peek(plan, n_rows)

        # TODO(swast): plumb through the api_name of the user-facing api that
        # caused this query.
        iterator, query_job = self._run_execute_query(sql=sql)
        return ExecuteResult(
            # Probably don't need read client for small peek results, but let client decide
            arrow_batches=lambda: iterator.to_arrow_iterable(
                bqstorage_client=self.bqstoragereadclient
            ),
            schema=array_value.schema,
            query_job=query_job,
            total_rows=iterator.total_rows,
        )

    # This is used exclusively to optimize __repr__
    # TODO: We need to model this
    def head(
        self, array_value: bigframes.core.ArrayValue, n_rows: int
    ) -> ExecuteResult:
        """
        Preview the first n rows of the dataframe. This is less efficient than the unordered peek preview op.
        """
        maybe_row_count = self._local_get_row_count(array_value)
        if (maybe_row_count is not None) and (maybe_row_count <= n_rows):
            return self.execute(array_value, ordered=True)

        if not self.strictly_ordered and not array_value.node.explicitly_ordered:
            # No user-provided ordering, so just get any N rows, its faster!
            return self.peek(array_value, n_rows)

        plan = self.replace_cached_subtrees(array_value.node)
        if not tree_properties.can_fast_head(plan):
            # If can't get head fast, we are going to need to execute the whole query
            # Will want to do this in a way such that the result is reusable, but the first
            # N values can be easily extracted.
            # This currently requires clustering on offsets.
            self._cache_with_offsets(array_value)
            # Get a new optimized plan after caching
            plan = self.replace_cached_subtrees(array_value.node)
            assert tree_properties.can_fast_head(plan)

        head_plan = generate_head_plan(plan, n_rows)
        sql = self.compiler.compile_ordered(head_plan)

        # TODO(swast): plumb through the api_name of the user-facing api that
        # caused this query.
        iterator, query_job = self._run_execute_query(sql=sql)
        return ExecuteResult(
            # Probably don't need read client for small head results, but let client decide
            arrow_batches=lambda: iterator.to_arrow_iterable(
                bqstorage_client=self.bqstoragereadclient
            ),
            schema=array_value.schema,
            query_job=query_job,
            total_rows=iterator.total_rows,
        )

    # TODO: Remove. We shouldn't need this method, row count node can automatically be detected
    def get_row_count(self, array_value: bigframes.core.ArrayValue) -> int:
        count = self._local_get_row_count(array_value)
        if count is not None:
            return count
        else:
            row_count_plan = self.replace_cached_subtrees(
                generate_row_count_plan(array_value.node)
            )
            sql = self.compiler.compile_unordered(row_count_plan)
            iter, _ = self._run_execute_query(sql)
            return next(iter)[0]

    def _local_get_row_count(
        self, array_value: bigframes.core.ArrayValue
    ) -> Optional[int]:
        # optimized plan has cache materializations which will have row count metadata
        # that is more likely to be usable than original leaf nodes.
        plan = self.replace_cached_subtrees(array_value.node)
        return tree_properties.row_count(plan)

    # Helpers
    def _run_execute_query(
        self,
        sql: str,
        job_config: Optional[bq_job.QueryJobConfig] = None,
        api_name: Optional[str] = None,
        page_size: Optional[int] = None,
        max_results: Optional[int] = None,
    ) -> Tuple[bq_table.RowIterator, bigquery.QueryJob]:
        """
        Starts BigQuery query job and waits for results.
        """
        job_config = bq_job.QueryJobConfig() if job_config is None else job_config
        if bigframes.options.compute.maximum_bytes_billed is not None:
            job_config.maximum_bytes_billed = (
                bigframes.options.compute.maximum_bytes_billed
            )
        # Note: add_labels is global scope which may have unexpected effects
        bq_io.add_labels(job_config, api_name=api_name)

        if not self.strictly_ordered:
            job_config.labels["bigframes-mode"] = "unordered"
        try:
            query_job = self.bqclient.query(sql, job_config=job_config)
            return (
                self._wait_on_job(
                    query_job, max_results=max_results, page_size=page_size
                ),
                query_job,
            )

        except google.api_core.exceptions.BadRequest as e:
            # Unfortunately, this error type does not have a separate error code or exception type
            if "Resources exceeded during query execution" in e.message:
                new_message = "Computation is too complex to execute as a single query. Try using DataFrame.cache() on intermediate results, or setting bigframes.options.compute.enable_multi_query_execution."
                raise bigframes.exceptions.QueryComplexityError(new_message) from e
            else:
                raise

    def _wait_on_job(
        self,
        query_job: bigquery.QueryJob,
        page_size: Optional[int] = None,
        max_results: Optional[int] = None,
    ) -> bq_table.RowIterator:
        opts = bigframes.options.display
        if opts.progress_bar is not None and not query_job.configuration.dry_run:
            results_iterator = formatting_helpers.wait_for_query_job(
                query_job,
                progress_bar=opts.progress_bar,
                max_results=max_results,
                page_size=page_size,
            )
        else:
            results_iterator = query_job.result(
                max_results=max_results, page_size=page_size
            )

        if self.metrics is not None:
            self.metrics.count_job_stats(query_job)
        return results_iterator

    def replace_cached_subtrees(self, node: nodes.BigFrameNode) -> nodes.BigFrameNode:
        return tree_properties.replace_nodes(node, (dict(self._cached_executions)))

    def _is_trivially_executable(self, array_value: bigframes.core.ArrayValue):
        """
        Can the block be evaluated very cheaply?
        If True, the array_value probably is not worth caching.
        """
        # Once rewriting is available, will want to rewrite before
        # evaluating execution cost.
        return tree_properties.is_trivially_executable(
            self.replace_cached_subtrees(array_value.node)
        )

    def _cache_with_cluster_cols(
        self, array_value: bigframes.core.ArrayValue, cluster_cols: Sequence[str]
    ):
        """Executes the query and uses the resulting table to rewrite future executions."""

        sql, schema, ordering_info = self.compiler.compile_raw(
            self.replace_cached_subtrees(array_value.node)
        )
        tmp_table = self._sql_as_cached_temp_table(
            sql,
            schema,
            cluster_cols=bq_io.select_cluster_cols(schema, cluster_cols),
        )
        cached_replacement = array_value.as_cached(
            cache_table=self.bqclient.get_table(tmp_table),
            ordering=ordering_info,
        ).node
        self._cached_executions[array_value.node] = cached_replacement

    def _cache_with_offsets(self, array_value: bigframes.core.ArrayValue):
        """Executes the query and uses the resulting table to rewrite future executions."""
        offset_column = bigframes.core.guid.generate_guid("bigframes_offsets")
        w_offsets, offset_column = array_value.promote_offsets()
        sql = self.compiler.compile_unordered(
            self.replace_cached_subtrees(w_offsets.node)
        )

        tmp_table = self._sql_as_cached_temp_table(
            sql,
            w_offsets.schema.to_bigquery(),
            cluster_cols=[offset_column],
        )
        cached_replacement = array_value.as_cached(
            cache_table=self.bqclient.get_table(tmp_table),
            ordering=order.TotalOrdering.from_offset_col(offset_column),
        ).node
        self._cached_executions[array_value.node] = cached_replacement

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
            node_with_cache = self.replace_cached_subtrees(array_value.node)
            if node_with_cache.planning_complexity < QUERY_COMPLEXITY_LIMIT:
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
            cache=dict(self._cached_executions),
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
        query_job.destination
        query_job.result()
        return query_job.destination

    def _validate_result_schema(
        self,
        array_value: bigframes.core.ArrayValue,
        bq_schema: list[bigquery.schema.SchemaField],
    ):
        actual_schema = tuple(bq_schema)
        ibis_schema = bigframes.core.compile.test_only_ibis_inferred_schema(
            self.replace_cached_subtrees(array_value.node)
        )
        internal_schema = array_value.schema
        if not bigframes.features.PANDAS_VERSIONS.is_arrow_list_dtype_usable:
            return
        if internal_schema.to_bigquery() != actual_schema:
            raise ValueError(
                f"This error should only occur while testing. BigFrames internal schema: {internal_schema.to_bigquery()} does not match actual schema: {actual_schema}"
            )
        if ibis_schema.to_bigquery() != actual_schema:
            raise ValueError(
                f"This error should only occur while testing. Ibis schema: {ibis_schema.to_bigquery()} does not match actual schema: {actual_schema}"
            )


def generate_head_plan(node: nodes.BigFrameNode, n: int):
    return nodes.SliceNode(node, start=None, stop=n)


def generate_row_count_plan(node: nodes.BigFrameNode):
    return nodes.RowCountNode(node)
