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

import copy
import dataclasses
import datetime
import itertools
import os
import typing
from typing import Dict, Hashable, IO, Iterable, List, Optional, Sequence, Tuple, Union

import bigframes_vendored.constants as constants
import bigframes_vendored.pandas.io.gbq as third_party_pandas_gbq
import google.api_core.exceptions
import google.auth.credentials
import google.cloud.bigquery as bigquery
import google.cloud.bigquery.table
import google.cloud.bigquery_connection_v1
import google.cloud.bigquery_storage_v1
import google.cloud.functions_v2
import google.cloud.resourcemanager_v3
import jellyfish
import pandas
import pandas_gbq.schema.pandas_to_bigquery  # type: ignore

import bigframes.clients
import bigframes.constants
import bigframes.core as core
import bigframes.core.blocks as blocks
import bigframes.core.compile
import bigframes.core.expression as expression
import bigframes.core.guid
import bigframes.core.ordering
import bigframes.core.pruning
import bigframes.core.schema as schemata
import bigframes.dataframe
import bigframes.dtypes
import bigframes.exceptions
import bigframes.formatting_helpers as formatting_helpers
import bigframes.operations
import bigframes.operations.aggregations as agg_ops
import bigframes.session._io.bigquery as bf_io_bigquery
import bigframes.session._io.bigquery.read_gbq_table as bf_read_gbq_table
import bigframes.session._io.pandas as bf_io_pandas
import bigframes.session.clients
import bigframes.session.executor
import bigframes.session.metrics
import bigframes.session.planner
import bigframes.session.temp_storage
import bigframes.session.time as session_time
import bigframes.version

# Avoid circular imports.
if typing.TYPE_CHECKING:
    import bigframes.core.indexes
    import bigframes.dataframe as dataframe
    import bigframes.series
    import bigframes.session

_MAX_CLUSTER_COLUMNS = 4


def _to_index_cols(
    index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = (),
) -> List[str]:
    """Convert index_col into a list of column names."""
    if isinstance(index_col, bigframes.enums.DefaultIndexKind):
        index_cols: List[str] = []
    elif isinstance(index_col, str):
        index_cols = [index_col]
    else:
        index_cols = list(index_col)

    return index_cols


@dataclasses.dataclass
class GbqDataLoader:
    """
    Responsible for loading data into BigFrames using temporary bigquery tables.

    This loader is constrained to loading local data and queries against data sources in the same region as the storage manager.


    Args:
        session (bigframes.session.Session):
            The session the data will be loaded into. Objects will not be compatible with other sessions.
        bqclient (bigquery.Client):
            An object providing client library objects.
        storage_manager (bigframes.session.temp_storage.TemporaryGbqStorageManager):
            Manages temporary storage used by the loader.
        default_index_type (bigframes.enums.DefaultIndexKind):
            Determines the index type created for data loaded from gcs or gbq.
        scan_index_uniqueness (bool):
            Whether the loader will scan index columns to determine whether the values are unique.
            This behavior is useful in total ordering mode to use index column as order key.
        metrics (bigframes.session.metrics.ExecutionMetrics or None):
            Used to record query execution statistics.
    """

    def __init__(
        self,
        session: bigframes.session.Session,
        bqclient: bigquery.Client,
        storage_manager: bigframes.session.temp_storage.TemporaryGbqStorageManager,
        default_index_type: bigframes.enums.DefaultIndexKind,
        scan_index_uniqueness: bool,
        force_total_order: bool,
        metrics: Optional[bigframes.session.metrics.ExecutionMetrics] = None,
    ):
        self._bqclient = bqclient
        self._storage_manager = storage_manager
        self._default_index_type = default_index_type
        self._scan_index_uniqueness = scan_index_uniqueness
        self._force_total_order = force_total_order
        self._df_snapshot: Dict[
            bigquery.TableReference, Tuple[datetime.datetime, bigquery.Table]
        ] = {}
        self._metrics = metrics
        # Unfortunate circular reference, but need to pass reference when constructing objects
        self._session = session
        self._clock = session_time.BigQuerySyncedClock(bqclient)
        self._clock.sync()

    def read_pandas_load_job(
        self, pandas_dataframe: pandas.DataFrame, api_name: str
    ) -> dataframe.DataFrame:
        import bigframes.dataframe as dataframe

        df_and_labels = bf_io_pandas.pandas_to_bq_compatible(pandas_dataframe)
        pandas_dataframe_copy = df_and_labels.df
        new_idx_ids = pandas_dataframe_copy.index.names
        ordering_col = df_and_labels.ordering_col

        # TODO(https://github.com/googleapis/python-bigquery-pandas/issues/760):
        # Once pandas-gbq can show a link to the running load job like
        # bigframes does, switch to using pandas-gbq to load the
        # bigquery-compatible pandas DataFrame.
        schema: list[
            bigquery.SchemaField
        ] = pandas_gbq.schema.pandas_to_bigquery.dataframe_to_bigquery_fields(
            pandas_dataframe_copy,
            index=True,
        )

        job_config = bigquery.LoadJobConfig()
        job_config.schema = schema

        # TODO: Remove this. It's likely that the slower load job due to
        # clustering doesn't improve speed of queries because pandas tables are
        # small.
        cluster_cols = [ordering_col]
        job_config.clustering_fields = cluster_cols

        job_config.labels = {"bigframes-api": api_name}

        load_table_destination = self._storage_manager._random_table()
        load_job = self._bqclient.load_table_from_dataframe(
            pandas_dataframe_copy,
            load_table_destination,
            job_config=job_config,
        )
        self._start_generic_job(load_job)

        destination_table = self._bqclient.get_table(load_table_destination)
        array_value = core.ArrayValue.from_table(
            table=destination_table,
            # TODO (b/394156190): Generate this directly from original pandas df.
            schema=schemata.ArraySchema.from_bq_table(
                destination_table, df_and_labels.col_type_overrides
            ),
            session=self._session,
            offsets_col=ordering_col,
        ).drop_columns([ordering_col])

        block = blocks.Block(
            array_value,
            index_columns=new_idx_ids,
            column_labels=df_and_labels.column_labels,
            index_labels=df_and_labels.index_labels,
        )
        return dataframe.DataFrame(block)

    def read_pandas_streaming(
        self,
        pandas_dataframe: pandas.DataFrame,
    ) -> dataframe.DataFrame:
        """Same as pandas_to_bigquery_load, but uses the BQ legacy streaming API."""
        import bigframes.dataframe as dataframe

        df_and_labels = bf_io_pandas.pandas_to_bq_compatible(pandas_dataframe)
        pandas_dataframe_copy = df_and_labels.df
        new_idx_ids = pandas_dataframe_copy.index.names
        ordering_col = df_and_labels.ordering_col

        # TODO(https://github.com/googleapis/python-bigquery-pandas/issues/300):
        # Once pandas-gbq can do streaming inserts (again), switch to using
        # pandas-gbq to write the bigquery-compatible pandas DataFrame.
        schema: list[
            bigquery.SchemaField
        ] = pandas_gbq.schema.pandas_to_bigquery.dataframe_to_bigquery_fields(
            pandas_dataframe_copy,
            index=True,
        )

        destination = self._storage_manager.create_temp_table(
            schema,
            [ordering_col],
        )
        destination_table = bigquery.Table(destination, schema=schema)
        # TODO(swast): Confirm that the index is written.
        for errors in self._bqclient.insert_rows_from_dataframe(
            destination_table,
            pandas_dataframe_copy,
        ):
            if errors:
                raise ValueError(
                    f"Problem loading at least one row from DataFrame: {errors}. {constants.FEEDBACK_LINK}"
                )
        array_value = (
            core.ArrayValue.from_table(
                table=destination_table,
                schema=schemata.ArraySchema.from_bq_table(
                    destination_table, df_and_labels.col_type_overrides
                ),
                session=self._session,
                # Don't set the offsets column because we want to group by it.
            )
            # There may be duplicate rows because of hidden retries, so use a query to
            # deduplicate based on the ordering ID, which is guaranteed to be unique.
            # We know that rows with same ordering ID are duplicates,
            # so ANY_VALUE() is deterministic.
            .aggregate(
                by_column_ids=[ordering_col],
                aggregations=[
                    (
                        expression.UnaryAggregation(
                            agg_ops.AnyValueOp(),
                            expression.deref(field.name),
                        ),
                        field.name,
                    )
                    for field in destination_table.schema
                    if field.name != ordering_col
                ],
            ).drop_columns([ordering_col])
        )
        block = blocks.Block(
            array_value,
            index_columns=new_idx_ids,
            column_labels=df_and_labels.column_labels,
            index_labels=df_and_labels.index_labels,
        )
        return dataframe.DataFrame(block)

    def _start_generic_job(self, job: formatting_helpers.GenericJob):
        if bigframes.options.display.progress_bar is not None:
            formatting_helpers.wait_for_job(
                job, bigframes.options.display.progress_bar
            )  # Wait for the job to complete
        else:
            job.result()

    def read_gbq_table(
        self,
        query: str,
        *,
        index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = (),
        columns: Iterable[str] = (),
        max_results: Optional[int] = None,
        api_name: str,
        use_cache: bool = True,
        filters: third_party_pandas_gbq.FiltersType = (),
        enable_snapshot: bool = True,
    ) -> dataframe.DataFrame:
        import bigframes.dataframe as dataframe

        # ---------------------------------
        # Validate and transform parameters
        # ---------------------------------

        if max_results and max_results <= 0:
            raise ValueError(
                f"`max_results` should be a positive number, got {max_results}."
            )

        table_ref = google.cloud.bigquery.table.TableReference.from_string(
            query, default_project=self._bqclient.project
        )

        columns = list(columns)
        filters = typing.cast(list, list(filters))

        # ---------------------------------
        # Fetch table metadata and validate
        # ---------------------------------

        time_travel_timestamp, table = bf_read_gbq_table.get_table_metadata(
            self._bqclient,
            table_ref=table_ref,
            bq_time=self._clock.get_time(),
            cache=self._df_snapshot,
            use_cache=use_cache,
        )
        table_column_names = {field.name for field in table.schema}

        if table.location.casefold() != self._storage_manager.location.casefold():
            raise ValueError(
                f"Current session is in {self._storage_manager.location} but dataset '{table.project}.{table.dataset_id}' is located in {table.location}"
            )

        for key in columns:
            if key not in table_column_names:
                possibility = min(
                    table_column_names,
                    key=lambda item: jellyfish.levenshtein_distance(key, item),
                )
                raise ValueError(
                    f"Column '{key}' of `columns` not found in this table. Did you mean '{possibility}'?"
                )

        # Converting index_col into a list of column names requires
        # the table metadata because we might use the primary keys
        # when constructing the index.
        index_cols = bf_read_gbq_table.get_index_cols(
            table=table,
            index_col=index_col,
        )

        for key in index_cols:
            if key not in table_column_names:
                possibility = min(
                    table_column_names,
                    key=lambda item: jellyfish.levenshtein_distance(key, item),
                )
                raise ValueError(
                    f"Column '{key}' of `index_col` not found in this table. Did you mean '{possibility}'?"
                )

        # -----------------------------
        # Optionally, execute the query
        # -----------------------------

        # max_results introduces non-determinism and limits the cost on
        # clustered tables, so fallback to a query. We do this here so that
        # the index is consistent with tables that have primary keys, even
        # when max_results is set.
        # TODO(b/338419730): We don't need to fallback to a query for wildcard
        # tables if we allow some non-determinism when time travel isn't supported.
        if max_results is not None or bf_io_bigquery.is_table_with_wildcard_suffix(
            query
        ):
            # TODO(b/338111344): If we are running a query anyway, we might as
            # well generate ROW_NUMBER() at the same time.
            all_columns: Iterable[str] = (
                itertools.chain(index_cols, columns) if columns else ()
            )
            query = bf_io_bigquery.to_query(
                query,
                columns=all_columns,
                sql_predicate=bf_io_bigquery.compile_filters(filters)
                if filters
                else None,
                max_results=max_results,
                # We're executing the query, so we don't need time travel for
                # determinism.
                time_travel_timestamp=None,
            )

            return self.read_gbq_query(
                query,
                index_col=index_cols,
                columns=columns,
                api_name="read_gbq_table",
                use_cache=use_cache,
            )

        # -----------------------------------------
        # Validate table access and features
        # -----------------------------------------

        # Use a time travel to make sure the DataFrame is deterministic, even
        # if the underlying table changes.

        # If a dry run query fails with time travel but
        # succeeds without it, omit the time travel clause and raise a warning
        # about potential non-determinism if the underlying tables are modified.
        filter_str = bf_io_bigquery.compile_filters(filters) if filters else None
        all_columns = (
            ()
            if len(columns) == 0
            else (*columns, *[col for col in index_cols if col not in columns])
        )

        try:
            enable_snapshot = enable_snapshot and bf_read_gbq_table.validate_table(
                self._bqclient,
                table,
                all_columns,
                time_travel_timestamp,
                filter_str,
            )
        except google.api_core.exceptions.Forbidden as ex:
            if "Drive credentials" in ex.message:
                ex.message += "\nCheck https://cloud.google.com/bigquery/docs/query-drive-data#Google_Drive_permissions."
            raise

        # ----------------------------
        # Create ordering and validate
        # ----------------------------

        # TODO(b/337925142): Generate a new subquery with just the index_cols
        # in the Ibis table expression so we don't have a "SELECT *" subquery
        # in the query that checks for index uniqueness.
        # TODO(b/338065601): Provide a way to assume uniqueness and avoid this
        # check.
        primary_key = bf_read_gbq_table.infer_unique_columns(
            bqclient=self._bqclient,
            table=table,
            index_cols=index_cols,
            api_name=api_name,
            # If non in strict ordering mode, don't go through overhead of scanning index column(s) to determine if unique
            metadata_only=not self._scan_index_uniqueness,
        )
        schema = schemata.ArraySchema.from_bq_table(table)
        if columns:
            schema = schema.select(index_cols + columns)
        array_value = core.ArrayValue.from_table(
            table,
            schema=schema,
            predicate=filter_str,
            at_time=time_travel_timestamp if enable_snapshot else None,
            primary_key=primary_key,
            session=self._session,
        )
        # if we don't have a unique index, we order by row hash if we are in strict mode
        if self._force_total_order:
            if not primary_key:
                array_value = array_value.order_by(
                    [
                        bigframes.core.ordering.OrderingExpression(
                            bigframes.operations.RowKey().as_expr(
                                *(id for id in array_value.column_ids)
                            ),
                            # More concise SQL this way.
                            na_last=False,
                        )
                    ],
                    is_total_order=True,
                )

        # ----------------------------------------------------
        # Create Default Sequential Index if still have no index
        # ----------------------------------------------------

        # If no index columns provided or found, fall back to session default
        if (index_col != bigframes.enums.DefaultIndexKind.NULL) and len(
            index_cols
        ) == 0:
            index_col = self._default_index_type

        index_names: Sequence[Hashable] = index_cols
        if index_col == bigframes.enums.DefaultIndexKind.SEQUENTIAL_INT64:
            array_value, sequential_index_col = array_value.promote_offsets()
            index_cols = [sequential_index_col]
            index_names = [None]

        value_columns = [col for col in array_value.column_ids if col not in index_cols]
        block = blocks.Block(
            array_value,
            index_columns=index_cols,
            column_labels=value_columns,
            index_labels=index_names,
        )
        if max_results:
            block = block.slice(stop=max_results)
        df = dataframe.DataFrame(block)

        # If user provided index columns, should sort over it
        if len(index_cols) > 0:
            df.sort_index()
        return df

    def _read_bigquery_load_job(
        self,
        filepath_or_buffer: str | IO["bytes"],
        table: Union[bigquery.Table, bigquery.TableReference],
        *,
        job_config: bigquery.LoadJobConfig,
        index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = (),
        columns: Iterable[str] = (),
    ) -> dataframe.DataFrame:
        index_cols = _to_index_cols(index_col)

        if not job_config.clustering_fields and index_cols:
            job_config.clustering_fields = index_cols[:_MAX_CLUSTER_COLUMNS]

        if isinstance(filepath_or_buffer, str):
            if filepath_or_buffer.startswith("gs://"):
                load_job = self._bqclient.load_table_from_uri(
                    filepath_or_buffer, table, job_config=job_config
                )
            elif os.path.exists(filepath_or_buffer):  # local file path
                with open(filepath_or_buffer, "rb") as source_file:
                    load_job = self._bqclient.load_table_from_file(
                        source_file, table, job_config=job_config
                    )
            else:
                raise NotImplementedError(
                    f"BigQuery engine only supports a local file path or GCS path. "
                    f"{constants.FEEDBACK_LINK}"
                )
        else:
            load_job = self._bqclient.load_table_from_file(
                filepath_or_buffer, table, job_config=job_config
            )

        self._start_generic_job(load_job)
        table_id = f"{table.project}.{table.dataset_id}.{table.table_id}"

        # Update the table expiration so we aren't limited to the default 24
        # hours of the anonymous dataset.
        table_expiration = bigquery.Table(table_id)
        table_expiration.expires = (
            datetime.datetime.now(datetime.timezone.utc)
            + bigframes.constants.DEFAULT_EXPIRATION
        )
        self._bqclient.update_table(table_expiration, ["expires"])

        # The BigQuery REST API for tables.get doesn't take a session ID, so we
        # can't get the schema for a temp table that way.

        return self.read_gbq_table(
            query=table_id,
            index_col=index_col,
            columns=columns,
            api_name="read_gbq_table",
        )

    def read_gbq_query(
        self,
        query: str,
        *,
        index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = (),
        columns: Iterable[str] = (),
        configuration: Optional[Dict] = None,
        max_results: Optional[int] = None,
        api_name: str = "read_gbq_query",
        use_cache: Optional[bool] = None,
        filters: third_party_pandas_gbq.FiltersType = (),
    ) -> dataframe.DataFrame:
        import bigframes.dataframe as dataframe

        configuration = _transform_read_gbq_configuration(configuration)

        if "query" not in configuration:
            configuration["query"] = {}

        if "query" in configuration["query"]:
            raise ValueError(
                "The query statement must not be included in the ",
                "'configuration' because it is already provided as",
                " a separate parameter.",
            )

        if "useQueryCache" in configuration["query"]:
            if use_cache is not None:
                raise ValueError(
                    "'useQueryCache' in 'configuration' conflicts with"
                    " 'use_cache' parameter. Please specify only one."
                )
        else:
            configuration["query"]["useQueryCache"] = (
                True if use_cache is None else use_cache
            )

        index_cols = _to_index_cols(index_col)

        filters_copy1, filters_copy2 = itertools.tee(filters)
        has_filters = len(list(filters_copy1)) != 0
        filters = typing.cast(third_party_pandas_gbq.FiltersType, filters_copy2)
        if has_filters or max_results is not None:
            # TODO(b/338111344): If we are running a query anyway, we might as
            # well generate ROW_NUMBER() at the same time.
            all_columns = itertools.chain(index_cols, columns) if columns else ()
            query = bf_io_bigquery.to_query(
                query,
                all_columns,
                bf_io_bigquery.compile_filters(filters) if has_filters else None,
                max_results=max_results,
                # We're executing the query, so we don't need time travel for
                # determinism.
                time_travel_timestamp=None,
            )

        # No cluster candidates as user query might not be clusterable (eg because of ORDER BY clause)
        destination, query_job = self._query_to_destination(
            query,
            cluster_candidates=[],
            api_name=api_name,
            configuration=configuration,
        )

        if self._metrics is not None:
            self._metrics.count_job_stats(query_job)

        # If there was no destination table, that means the query must have
        # been DDL or DML. Return some job metadata, instead.
        if not destination:
            return dataframe.DataFrame(
                data=pandas.DataFrame(
                    {
                        "statement_type": [
                            query_job.statement_type if query_job else "unknown"
                        ],
                        "job_id": [query_job.job_id if query_job else "unknown"],
                        "location": [query_job.location if query_job else "unknown"],
                    }
                ),
                session=self._session,
            )

        return self.read_gbq_table(
            f"{destination.project}.{destination.dataset_id}.{destination.table_id}",
            index_col=index_col,
            columns=columns,
            use_cache=configuration["query"]["useQueryCache"],
            api_name=api_name,
            # max_results and filters are omitted because they are already
            # handled by to_query(), above.
        )

    def _query_to_destination(
        self,
        query: str,
        cluster_candidates: List[str],
        api_name: str,
        configuration: dict = {"query": {"useQueryCache": True}},
        do_clustering=True,
    ) -> Tuple[Optional[bigquery.TableReference], bigquery.QueryJob]:
        # If a dry_run indicates this is not a query type job, then don't
        # bother trying to do a CREATE TEMP TABLE ... AS SELECT ... statement.
        dry_run_config = bigquery.QueryJobConfig()
        dry_run_config.dry_run = True
        _, dry_run_job = self._start_query(
            query, job_config=dry_run_config, api_name=api_name
        )
        if dry_run_job.statement_type != "SELECT":
            _, query_job = self._start_query(query, api_name=api_name)
            return query_job.destination, query_job

        # Create a table to workaround BigQuery 10 GB query results limit. See:
        # internal issue 303057336.
        # Since we have a `statement_type == 'SELECT'`, schema should be populated.
        schema = dry_run_job.schema
        assert schema is not None
        if do_clustering:
            cluster_cols = bf_io_bigquery.select_cluster_cols(
                schema, cluster_candidates=cluster_candidates
            )
        else:
            cluster_cols = []
        temp_table = self._storage_manager.create_temp_table(schema, cluster_cols)

        timeout_ms = configuration.get("jobTimeoutMs") or configuration["query"].get(
            "timeoutMs"
        )

        # Convert timeout_ms to seconds, ensuring a minimum of 0.1 seconds to avoid
        # the program getting stuck on too-short timeouts.
        timeout = max(int(timeout_ms) * 1e-3, 0.1) if timeout_ms else None

        job_config = typing.cast(
            bigquery.QueryJobConfig,
            bigquery.QueryJobConfig.from_api_repr(configuration),
        )
        job_config.destination = temp_table

        try:
            # Write to temp table to workaround BigQuery 10 GB query results
            # limit. See: internal issue 303057336.
            job_config.labels["error_caught"] = "true"
            _, query_job = self._start_query(
                query,
                job_config=job_config,
                timeout=timeout,
                api_name=api_name,
            )
            return query_job.destination, query_job
        except google.api_core.exceptions.BadRequest:
            # Some SELECT statements still aren't compatible with cluster
            # tables as the destination. For example, if the query has a
            # top-level ORDER BY, this conflicts with our ability to cluster
            # the table by the index column(s).
            _, query_job = self._start_query(query, timeout=timeout, api_name=api_name)
            return query_job.destination, query_job

    def _start_query(
        self,
        sql: str,
        job_config: Optional[google.cloud.bigquery.QueryJobConfig] = None,
        max_results: Optional[int] = None,
        timeout: Optional[float] = None,
        api_name: Optional[str] = None,
    ) -> Tuple[google.cloud.bigquery.table.RowIterator, bigquery.QueryJob]:
        """
        Starts BigQuery query job and waits for results.

        Do not execute dataframe through this API, instead use the executor.
        """
        job_config = bigquery.QueryJobConfig() if job_config is None else job_config
        if bigframes.options.compute.maximum_bytes_billed is not None:
            # Maybe this should be pushed down into start_query_with_client
            job_config.maximum_bytes_billed = (
                bigframes.options.compute.maximum_bytes_billed
            )
        iterator, query_job = bf_io_bigquery.start_query_with_client(
            self._bqclient,
            sql,
            job_config=job_config,
            max_results=max_results,
            timeout=timeout,
            api_name=api_name,
        )
        assert query_job is not None
        return iterator, query_job


def _transform_read_gbq_configuration(configuration: Optional[dict]) -> dict:
    """
    For backwards-compatibility, convert any previously client-side only
    parameters such as timeoutMs to the property name expected by the REST API.

    Makes a copy of configuration if changes are needed.
    """

    if configuration is None:
        return {}

    timeout_ms = configuration.get("query", {}).get("timeoutMs")
    if timeout_ms is not None:
        # Transform timeoutMs to an actual server-side configuration.
        # https://github.com/googleapis/python-bigquery-pandas/issues/479
        configuration = copy.deepcopy(configuration)
        del configuration["query"]["timeoutMs"]
        configuration["jobTimeoutMs"] = timeout_ms

    return configuration
