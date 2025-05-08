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
import io
import itertools
import os
import typing
from typing import (
    Dict,
    Generator,
    Hashable,
    IO,
    Iterable,
    List,
    Literal,
    Optional,
    overload,
    Sequence,
    Tuple,
)

import bigframes_vendored.constants as constants
import bigframes_vendored.pandas.io.gbq as third_party_pandas_gbq
import google.api_core.exceptions
from google.cloud import bigquery_storage_v1
import google.cloud.bigquery as bigquery
from google.cloud.bigquery_storage_v1 import types as bq_storage_types
import pandas
import pyarrow as pa

from bigframes.core import guid, local_data, utils
import bigframes.core as core
import bigframes.core.blocks as blocks
import bigframes.core.schema as schemata
import bigframes.dtypes
import bigframes.formatting_helpers as formatting_helpers
from bigframes.session import dry_runs
import bigframes.session._io.bigquery as bf_io_bigquery
import bigframes.session._io.bigquery.read_gbq_table as bf_read_gbq_table
import bigframes.session.metrics
import bigframes.session.temporary_storage
import bigframes.session.time as session_time

# Avoid circular imports.
if typing.TYPE_CHECKING:
    import bigframes.dataframe as dataframe
    import bigframes.session

_PLACEHOLDER_SCHEMA = (
    google.cloud.bigquery.SchemaField("bf_loader_placeholder", "INTEGER"),
)

_LOAD_JOB_TYPE_OVERRIDES = {
    # Json load jobs not supported yet: b/271321143
    bigframes.dtypes.JSON_DTYPE: "STRING",
    # Timedelta is emulated using integer in bq type system
    bigframes.dtypes.TIMEDELTA_DTYPE: "INTEGER",
}

_STREAM_JOB_TYPE_OVERRIDES = {
    # Timedelta is emulated using integer in bq type system
    bigframes.dtypes.TIMEDELTA_DTYPE: "INTEGER",
}


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


def _check_column_duplicates(index_cols: Iterable[str], columns: Iterable[str]):
    index_cols_list = list(index_cols) if index_cols is not None else []
    columns_list = list(columns) if columns is not None else []
    set_index = set(index_cols_list)
    set_columns = set(columns_list)

    if len(index_cols_list) > len(set_index):
        raise ValueError(
            "The 'index_col' argument contains duplicate names. "
            "All column names specified in 'index_col' must be unique."
        )

    if len(columns_list) > len(set_columns):
        raise ValueError(
            "The 'columns' argument contains duplicate names. "
            "All column names specified in 'columns' must be unique."
        )

    if not set_index.isdisjoint(set_columns):
        raise ValueError(
            "Found column names that exist in both 'index_col' and 'columns' arguments. "
            "These arguments must specify distinct sets of columns."
        )


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
        write_client: bigquery_storage_v1.BigQueryWriteClient,
        storage_manager: bigframes.session.temporary_storage.TemporaryStorageManager,
        default_index_type: bigframes.enums.DefaultIndexKind,
        scan_index_uniqueness: bool,
        force_total_order: bool,
        metrics: Optional[bigframes.session.metrics.ExecutionMetrics] = None,
    ):
        self._bqclient = bqclient
        self._write_client = write_client
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

    def read_pandas(
        self,
        pandas_dataframe: pandas.DataFrame,
        method: Literal["load", "stream", "write"],
        api_name: str,
    ) -> dataframe.DataFrame:
        # TODO: Push this into from_pandas, along with index flag
        from bigframes import dataframe

        val_cols, idx_cols = utils.get_standardized_ids(
            pandas_dataframe.columns, pandas_dataframe.index.names, strict=True
        )
        prepared_df = pandas_dataframe.reset_index(drop=False).set_axis(
            [*idx_cols, *val_cols], axis="columns"
        )
        managed_data = local_data.ManagedArrowTable.from_pandas(prepared_df)

        if method == "load":
            array_value = self.load_data(managed_data, api_name=api_name)
        elif method == "stream":
            array_value = self.stream_data(managed_data)
        elif method == "write":
            array_value = self.write_data(managed_data)
        else:
            raise ValueError(f"Unsupported read method {method}")

        block = blocks.Block(
            array_value,
            index_columns=idx_cols,
            column_labels=pandas_dataframe.columns,
            index_labels=pandas_dataframe.index.names,
        )
        return dataframe.DataFrame(block)

    def load_data(
        self, data: local_data.ManagedArrowTable, api_name: Optional[str] = None
    ) -> core.ArrayValue:
        """Load managed data into bigquery"""
        ordering_col = guid.generate_guid("load_offsets_")

        # JSON support incomplete
        for item in data.schema.items:
            _validate_dtype_can_load(item.column, item.dtype)

        schema_w_offsets = data.schema.append(
            schemata.SchemaItem(ordering_col, bigframes.dtypes.INT_DTYPE)
        )
        bq_schema = schema_w_offsets.to_bigquery(_LOAD_JOB_TYPE_OVERRIDES)

        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.PARQUET

        # Ensure we can load pyarrow.list_ / BQ ARRAY type.
        # See internal issue 414374215.
        parquet_options = bigquery.ParquetOptions()
        parquet_options.enable_list_inference = True
        job_config.parquet_options = parquet_options

        job_config.schema = bq_schema
        if api_name:
            job_config.labels = {"bigframes-api": api_name}

        load_table_destination = self._storage_manager.create_temp_table(
            bq_schema, [ordering_col]
        )

        buffer = io.BytesIO()
        data.to_parquet(
            buffer,
            offsets_col=ordering_col,
            geo_format="wkt",
            duration_type="duration",
            json_type="string",
        )
        buffer.seek(0)
        load_job = self._bqclient.load_table_from_file(
            buffer, destination=load_table_destination, job_config=job_config
        )
        self._start_generic_job(load_job)
        # must get table metadata after load job for accurate metadata
        destination_table = self._bqclient.get_table(load_table_destination)
        return core.ArrayValue.from_table(
            table=destination_table,
            schema=schema_w_offsets,
            session=self._session,
            offsets_col=ordering_col,
            n_rows=data.data.num_rows,
        ).drop_columns([ordering_col])

    def stream_data(self, data: local_data.ManagedArrowTable) -> core.ArrayValue:
        """Load managed data into bigquery"""
        ordering_col = guid.generate_guid("stream_offsets_")
        schema_w_offsets = data.schema.append(
            schemata.SchemaItem(ordering_col, bigframes.dtypes.INT_DTYPE)
        )
        bq_schema = schema_w_offsets.to_bigquery(_STREAM_JOB_TYPE_OVERRIDES)
        load_table_destination = self._storage_manager.create_temp_table(
            bq_schema, [ordering_col]
        )

        rows = data.itertuples(
            geo_format="wkt", duration_type="int", json_type="object"
        )
        rows_w_offsets = ((*row, offset) for offset, row in enumerate(rows))

        for errors in self._bqclient.insert_rows(
            load_table_destination,
            rows_w_offsets,
            selected_fields=bq_schema,
            row_ids=map(str, itertools.count()),  # used to ensure only-once insertion
        ):
            if errors:
                raise ValueError(
                    f"Problem loading at least one row from DataFrame: {errors}. {constants.FEEDBACK_LINK}"
                )
        destination_table = self._bqclient.get_table(load_table_destination)
        return core.ArrayValue.from_table(
            table=destination_table,
            schema=schema_w_offsets,
            session=self._session,
            offsets_col=ordering_col,
            n_rows=data.data.num_rows,
        ).drop_columns([ordering_col])

    def write_data(self, data: local_data.ManagedArrowTable) -> core.ArrayValue:
        """Load managed data into bigquery"""
        ordering_col = guid.generate_guid("stream_offsets_")
        schema_w_offsets = data.schema.append(
            schemata.SchemaItem(ordering_col, bigframes.dtypes.INT_DTYPE)
        )
        bq_schema = schema_w_offsets.to_bigquery(_STREAM_JOB_TYPE_OVERRIDES)
        bq_table_ref = self._storage_manager.create_temp_table(
            bq_schema, [ordering_col]
        )

        requested_stream = bq_storage_types.stream.WriteStream()
        requested_stream.type_ = bq_storage_types.stream.WriteStream.Type.COMMITTED  # type: ignore

        stream_request = bq_storage_types.CreateWriteStreamRequest(
            parent=bq_table_ref.to_bqstorage(), write_stream=requested_stream
        )
        stream = self._write_client.create_write_stream(request=stream_request)

        def request_gen() -> Generator[bq_storage_types.AppendRowsRequest, None, None]:
            schema, batches = data.to_arrow(
                offsets_col=ordering_col, duration_type="int"
            )
            offset = 0
            for batch in batches:
                request = bq_storage_types.AppendRowsRequest(
                    write_stream=stream.name, offset=offset
                )
                request.arrow_rows.writer_schema.serialized_schema = (
                    schema.serialize().to_pybytes()
                )
                request.arrow_rows.rows.serialized_record_batch = (
                    batch.serialize().to_pybytes()
                )
                offset += batch.num_rows
                yield request

        for response in self._write_client.append_rows(requests=request_gen()):
            if response.row_errors:
                raise ValueError(
                    f"Problem loading at least one row from DataFrame: {response.row_errors}. {constants.FEEDBACK_LINK}"
                )
        # This step isn't strictly necessary in COMMITTED mode, but avoids max active stream limits
        response = self._write_client.finalize_write_stream(name=stream.name)
        assert response.row_count == data.data.num_rows

        destination_table = self._bqclient.get_table(bq_table_ref)
        return core.ArrayValue.from_table(
            table=destination_table,
            schema=schema_w_offsets,
            session=self._session,
            offsets_col=ordering_col,
            n_rows=data.data.num_rows,
        ).drop_columns([ordering_col])

    def _start_generic_job(self, job: formatting_helpers.GenericJob):
        if bigframes.options.display.progress_bar is not None:
            formatting_helpers.wait_for_job(
                job, bigframes.options.display.progress_bar
            )  # Wait for the job to complete
        else:
            job.result()

    @overload
    def read_gbq_table(  # type: ignore[overload-overlap]
        self,
        table_id: str,
        *,
        index_col: Iterable[str]
        | str
        | Iterable[int]
        | int
        | bigframes.enums.DefaultIndexKind = ...,
        columns: Iterable[str] = ...,
        names: Optional[Iterable[str]] = ...,
        max_results: Optional[int] = ...,
        api_name: str = ...,
        use_cache: bool = ...,
        filters: third_party_pandas_gbq.FiltersType = ...,
        enable_snapshot: bool = ...,
        dry_run: Literal[False] = ...,
        force_total_order: Optional[bool] = ...,
    ) -> dataframe.DataFrame:
        ...

    @overload
    def read_gbq_table(
        self,
        table_id: str,
        *,
        index_col: Iterable[str]
        | str
        | Iterable[int]
        | int
        | bigframes.enums.DefaultIndexKind = ...,
        columns: Iterable[str] = ...,
        names: Optional[Iterable[str]] = ...,
        max_results: Optional[int] = ...,
        api_name: str = ...,
        use_cache: bool = ...,
        filters: third_party_pandas_gbq.FiltersType = ...,
        enable_snapshot: bool = ...,
        dry_run: Literal[True] = ...,
        force_total_order: Optional[bool] = ...,
    ) -> pandas.Series:
        ...

    def read_gbq_table(
        self,
        table_id: str,
        *,
        index_col: Iterable[str]
        | str
        | Iterable[int]
        | int
        | bigframes.enums.DefaultIndexKind = (),
        columns: Iterable[str] = (),
        names: Optional[Iterable[str]] = None,
        max_results: Optional[int] = None,
        api_name: str = "read_gbq_table",
        use_cache: bool = True,
        filters: third_party_pandas_gbq.FiltersType = (),
        enable_snapshot: bool = True,
        dry_run: bool = False,
        force_total_order: Optional[bool] = None,
    ) -> dataframe.DataFrame | pandas.Series:
        import bigframes._tools.strings
        import bigframes.dataframe as dataframe

        # ---------------------------------
        # Validate and transform parameters
        # ---------------------------------

        if max_results and max_results <= 0:
            raise ValueError(
                f"`max_results` should be a positive number, got {max_results}."
            )

        table_ref = google.cloud.bigquery.table.TableReference.from_string(
            table_id, default_project=self._bqclient.project
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
                    key=lambda item: bigframes._tools.strings.levenshtein_distance(
                        key, item
                    ),
                )
                raise ValueError(
                    f"Column '{key}' of `columns` not found in this table. Did you mean '{possibility}'?"
                )

        # TODO(b/408499371): check `names` work with `use_cols` for read_csv method.
        if names is not None:
            len_names = len(list(names))
            len_columns = len(table.schema)
            if len_names > len_columns:
                raise ValueError(
                    f"Too many columns specified: expected {len_columns}"
                    f" and found {len_names}"
                )
            elif len_names < len_columns:
                if (
                    isinstance(index_col, bigframes.enums.DefaultIndexKind)
                    or index_col != ()
                ):
                    raise KeyError(
                        "When providing both `index_col` and `names`, ensure the "
                        "number of `names` matches the number of columns in your "
                        "data."
                    )
                index_col = range(len_columns - len_names)
                names = [
                    field.name for field in table.schema[: len_columns - len_names]
                ] + list(names)

        # Converting index_col into a list of column names requires
        # the table metadata because we might use the primary keys
        # when constructing the index.
        index_cols = bf_read_gbq_table.get_index_cols(
            table=table,
            index_col=index_col,
            names=names,
        )
        _check_column_duplicates(index_cols, columns)

        for key in index_cols:
            if key not in table_column_names:
                possibility = min(
                    table_column_names,
                    key=lambda item: bigframes._tools.strings.levenshtein_distance(
                        key, item
                    ),
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
        if max_results is not None:
            # TODO(b/338111344): If we are running a query anyway, we might as
            # well generate ROW_NUMBER() at the same time.
            all_columns: Iterable[str] = (
                itertools.chain(index_cols, columns) if columns else ()
            )
            query = bf_io_bigquery.to_query(
                table_id,
                columns=all_columns,
                sql_predicate=bf_io_bigquery.compile_filters(filters)
                if filters
                else None,
                max_results=max_results,
                # We're executing the query, so we don't need time travel for
                # determinism.
                time_travel_timestamp=None,
            )

            df = self.read_gbq_query(  # type: ignore # for dry_run overload
                query,
                index_col=index_cols,
                columns=columns,
                api_name=api_name,
                use_cache=use_cache,
                dry_run=dry_run,
            )
            return df

        if dry_run:
            return dry_runs.get_table_stats(table)

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
        if (
            # If the user has explicitly selected or disabled total ordering for
            # this API call, respect that choice.
            (force_total_order is not None and force_total_order)
            # If the user has not explicitly selected or disabled total ordering
            # for this API call, respect the default choice for the session.
            or (force_total_order is None and self._force_total_order)
        ):
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
        if names is not None:
            renamed_cols: Dict[str, str] = {
                col: new_name for col, new_name in zip(array_value.column_ids, names)
            }
            index_names = [
                renamed_cols.get(index_col, index_col) for index_col in index_cols
            ]
            value_columns = [renamed_cols.get(col, col) for col in value_columns]

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

    def load_file(
        self,
        filepath_or_buffer: str | IO["bytes"],
        *,
        job_config: bigquery.LoadJobConfig,
    ) -> str:
        # Need to create session table beforehand
        table = self._storage_manager.create_temp_table(_PLACEHOLDER_SCHEMA)
        # but, we just overwrite the placeholder schema immediately with the load job
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
        if isinstance(filepath_or_buffer, str):
            filepath_or_buffer = os.path.expanduser(filepath_or_buffer)
            if filepath_or_buffer.startswith("gs://"):
                load_job = self._bqclient.load_table_from_uri(
                    filepath_or_buffer, destination=table, job_config=job_config
                )
            elif os.path.exists(filepath_or_buffer):  # local file path
                with open(filepath_or_buffer, "rb") as source_file:
                    load_job = self._bqclient.load_table_from_file(
                        source_file, destination=table, job_config=job_config
                    )
            else:
                raise NotImplementedError(
                    f"BigQuery engine only supports a local file path or GCS path. "
                    f"{constants.FEEDBACK_LINK}"
                )
        else:
            load_job = self._bqclient.load_table_from_file(
                filepath_or_buffer, destination=table, job_config=job_config
            )

        self._start_generic_job(load_job)
        table_id = f"{table.project}.{table.dataset_id}.{table.table_id}"
        return table_id

    @overload
    def read_gbq_query(  # type: ignore[overload-overlap]
        self,
        query: str,
        *,
        index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = ...,
        columns: Iterable[str] = ...,
        configuration: Optional[Dict] = ...,
        max_results: Optional[int] = ...,
        api_name: str = ...,
        use_cache: Optional[bool] = ...,
        filters: third_party_pandas_gbq.FiltersType = ...,
        dry_run: Literal[False] = ...,
        force_total_order: Optional[bool] = ...,
    ) -> dataframe.DataFrame:
        ...

    @overload
    def read_gbq_query(
        self,
        query: str,
        *,
        index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = ...,
        columns: Iterable[str] = ...,
        configuration: Optional[Dict] = ...,
        max_results: Optional[int] = ...,
        api_name: str = ...,
        use_cache: Optional[bool] = ...,
        filters: third_party_pandas_gbq.FiltersType = ...,
        dry_run: Literal[True] = ...,
        force_total_order: Optional[bool] = ...,
    ) -> pandas.Series:
        ...

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
        dry_run: bool = False,
        force_total_order: Optional[bool] = None,
    ) -> dataframe.DataFrame | pandas.Series:
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
        _check_column_duplicates(index_cols, columns)

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

        if dry_run:
            job_config = typing.cast(
                bigquery.QueryJobConfig,
                bigquery.QueryJobConfig.from_api_repr(configuration),
            )
            job_config.dry_run = True
            query_job = self._bqclient.query(query, job_config=job_config)
            return dry_runs.get_query_stats_with_inferred_dtypes(
                query_job, list(columns), index_cols
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
            force_total_order=force_total_order,
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


def _has_json_arrow_type(arrow_type: pa.DataType) -> bool:
    """
    Searches recursively for JSON array type within a PyArrow DataType.
    """
    if arrow_type == bigframes.dtypes.JSON_ARROW_TYPE:
        return True
    if pa.types.is_list(arrow_type):
        return _has_json_arrow_type(arrow_type.value_type)
    if pa.types.is_struct(arrow_type):
        for i in range(arrow_type.num_fields):
            if _has_json_arrow_type(arrow_type.field(i).type):
                return True
        return False
    return False


def _validate_dtype_can_load(name: str, column_type: bigframes.dtypes.Dtype):
    """
    Determines whether a datatype is supported by bq load jobs.

    Due to a BigQuery IO limitation with loading JSON from Parquet files (b/374784249),
    we're using a workaround: storing JSON as strings and then parsing them into JSON
    objects.
    TODO(b/395912450): Remove workaround solution once b/374784249 got resolved.

    Raises:
        NotImplementedError: Type is not yet supported by load jobs.
    """
    # we can handle top-level json, but not nested yet through string conversion
    if column_type == bigframes.dtypes.JSON_DTYPE:
        return

    if isinstance(column_type, pandas.ArrowDtype) and _has_json_arrow_type(
        column_type.pyarrow_dtype
    ):
        raise NotImplementedError(
            f"Nested JSON types, found in column `{name}`: `{column_type}`', "
            f"are currently unsupported for upload. {constants.FEEDBACK_LINK}"
        )
