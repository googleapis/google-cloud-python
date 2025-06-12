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
    cast,
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
import google.cloud.bigquery
import google.cloud.bigquery as bigquery
from google.cloud.bigquery_storage_v1 import types as bq_storage_types
import pandas
import pyarrow as pa

from bigframes.core import guid, identifiers, local_data, nodes, ordering, utils
import bigframes.core as core
import bigframes.core.blocks as blocks
import bigframes.core.schema as schemata
import bigframes.dtypes
import bigframes.formatting_helpers as formatting_helpers
from bigframes.session import dry_runs
import bigframes.session._io.bigquery as bf_io_bigquery
import bigframes.session._io.bigquery.read_gbq_query as bf_read_gbq_query
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


def _check_duplicates(name: str, columns: Optional[Iterable[str]] = None):
    """Check for duplicate column names in the provided iterable."""
    if columns is None:
        return
    columns_list = list(columns)
    set_columns = set(columns_list)
    if len(columns_list) > len(set_columns):
        raise ValueError(
            f"The '{name}' argument contains duplicate names. "
            f"All column names specified in '{name}' must be unique."
        )


def _check_index_col_param(
    index_cols: Iterable[str],
    columns: Iterable[str],
    *,
    table_columns: Optional[Iterable[str]] = None,
    index_col_in_columns: Optional[bool] = False,
):
    """Checks for duplicates in `index_cols` and resolves overlap with `columns`.

    Args:
        index_cols (Iterable[str]):
            Column names designated as the index columns.
        columns (Iterable[str]):
            Used column names from table_columns.
        table_columns (Iterable[str]):
            A full list of column names in the table schema.
        index_col_in_columns (bool):
            A flag indicating how to handle overlap between `index_cols` and
            `columns`.
            - If `False`, the two lists must be disjoint (contain no common
              elements). An error is raised if any overlap is found.
            - If `True`, `index_cols` is expected to be a subset of
              `columns`. An error is raised if an index column is not found
              in the `columns` list.
    """
    _check_duplicates("index_col", index_cols)

    if columns is not None and len(list(columns)) > 0:
        set_index = set(list(index_cols) if index_cols is not None else [])
        set_columns = set(list(columns) if columns is not None else [])

        if index_col_in_columns:
            if not set_index.issubset(set_columns):
                raise ValueError(
                    f"The specified index column(s) were not found: {set_index - set_columns}. "
                    f"Available columns are: {set_columns}"
                )
        else:
            if not set_index.isdisjoint(set_columns):
                raise ValueError(
                    "Found column names that exist in both 'index_col' and 'columns' arguments. "
                    "These arguments must specify distinct sets of columns."
                )

    if not index_col_in_columns and table_columns is not None:
        for key in index_cols:
            if key not in table_columns:
                possibility = min(
                    table_columns,
                    key=lambda item: bigframes._tools.strings.levenshtein_distance(
                        key, item
                    ),
                )
                raise ValueError(
                    f"Column '{key}' of `index_col` not found in this table. Did you mean '{possibility}'?"
                )


def _check_columns_param(columns: Iterable[str], table_columns: Iterable[str]):
    """Validates that the specified columns are present in the table columns.

    Args:
        columns (Iterable[str]):
            Used column names from table_columns.
        table_columns (Iterable[str]):
            A full list of column names in the table schema.
    Raises:
        ValueError: If any column in `columns` is not found in the table columns.
    """
    for column_name in columns:
        if column_name not in table_columns:
            possibility = min(
                table_columns,
                key=lambda item: bigframes._tools.strings.levenshtein_distance(
                    column_name, item
                ),
            )
            raise ValueError(
                f"Column '{column_name}' is not found. Did you mean '{possibility}'?"
            )


def _check_names_param(
    names: Iterable[str],
    index_col: Iterable[str]
    | str
    | Iterable[int]
    | int
    | bigframes.enums.DefaultIndexKind,
    columns: Iterable[str],
    table_columns: Iterable[str],
):
    len_names = len(list(names))
    len_table_columns = len(list(table_columns))
    len_columns = len(list(columns))
    if len_names > len_table_columns:
        raise ValueError(
            f"Too many columns specified: expected {len_table_columns}"
            f" and found {len_names}"
        )
    elif len_names < len_table_columns:
        if isinstance(index_col, bigframes.enums.DefaultIndexKind) or index_col != ():
            raise KeyError(
                "When providing both `index_col` and `names`, ensure the "
                "number of `names` matches the number of columns in your "
                "data."
            )
        if len_columns != 0:
            # The 'columns' must be identical to the 'names'. If not, raise an error.
            if len_columns != len_names:
                raise ValueError(
                    "Number of passed names did not match number of header "
                    "fields in the file"
                )
            if set(list(names)) != set(list(columns)):
                raise ValueError("Usecols do not match columns")


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
        block = blocks.Block(
            self.read_managed_data(managed_data, method=method),
            index_columns=idx_cols,
            column_labels=pandas_dataframe.columns,
            index_labels=pandas_dataframe.index.names,
        )
        return dataframe.DataFrame(block)

    def read_managed_data(
        self,
        data: local_data.ManagedArrowTable,
        method: Literal["load", "stream", "write"],
    ) -> core.ArrayValue:
        offsets_col = guid.generate_guid("upload_offsets_")
        if method == "load":
            gbq_source = self.load_data(data, offsets_col=offsets_col)
        elif method == "stream":
            gbq_source = self.stream_data(data, offsets_col=offsets_col)
        elif method == "write":
            gbq_source = self.write_data(data, offsets_col=offsets_col)
        else:
            raise ValueError(f"Unsupported read method {method}")

        return core.ArrayValue.from_bq_data_source(
            source=gbq_source,
            scan_list=nodes.ScanList(
                tuple(
                    nodes.ScanItem(
                        identifiers.ColumnId(item.column), item.dtype, item.column
                    )
                    for item in data.schema.items
                )
            ),
            session=self._session,
        )

    def load_data(
        self,
        data: local_data.ManagedArrowTable,
        offsets_col: str,
    ) -> nodes.BigqueryDataSource:
        """Load managed data into bigquery"""

        # JSON support incomplete
        for item in data.schema.items:
            _validate_dtype_can_load(item.column, item.dtype)

        schema_w_offsets = data.schema.append(
            schemata.SchemaItem(offsets_col, bigframes.dtypes.INT_DTYPE)
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

        load_table_destination = self._storage_manager.create_temp_table(
            bq_schema, [offsets_col]
        )

        buffer = io.BytesIO()
        data.to_parquet(
            buffer,
            offsets_col=offsets_col,
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
        return nodes.BigqueryDataSource(
            nodes.GbqTable.from_table(destination_table),
            ordering=ordering.TotalOrdering.from_offset_col(offsets_col),
            n_rows=data.metadata.row_count,
        )

    def stream_data(
        self,
        data: local_data.ManagedArrowTable,
        offsets_col: str,
    ) -> nodes.BigqueryDataSource:
        """Load managed data into bigquery"""
        schema_w_offsets = data.schema.append(
            schemata.SchemaItem(offsets_col, bigframes.dtypes.INT_DTYPE)
        )
        bq_schema = schema_w_offsets.to_bigquery(_STREAM_JOB_TYPE_OVERRIDES)
        load_table_destination = self._storage_manager.create_temp_table(
            bq_schema, [offsets_col]
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
        return nodes.BigqueryDataSource(
            nodes.GbqTable.from_table(destination_table),
            ordering=ordering.TotalOrdering.from_offset_col(offsets_col),
            n_rows=data.metadata.row_count,
        )

    def write_data(
        self,
        data: local_data.ManagedArrowTable,
        offsets_col: str,
    ) -> nodes.BigqueryDataSource:
        """Load managed data into bigquery"""
        schema_w_offsets = data.schema.append(
            schemata.SchemaItem(offsets_col, bigframes.dtypes.INT_DTYPE)
        )
        bq_schema = schema_w_offsets.to_bigquery(_STREAM_JOB_TYPE_OVERRIDES)
        bq_table_ref = self._storage_manager.create_temp_table(bq_schema, [offsets_col])

        requested_stream = bq_storage_types.stream.WriteStream()
        requested_stream.type_ = bq_storage_types.stream.WriteStream.Type.COMMITTED  # type: ignore

        stream_request = bq_storage_types.CreateWriteStreamRequest(
            parent=bq_table_ref.to_bqstorage(), write_stream=requested_stream
        )
        stream = self._write_client.create_write_stream(request=stream_request)

        def request_gen() -> Generator[bq_storage_types.AppendRowsRequest, None, None]:
            schema, batches = data.to_arrow(
                offsets_col=offsets_col, duration_type="int"
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
        return nodes.BigqueryDataSource(
            nodes.GbqTable.from_table(destination_table),
            ordering=ordering.TotalOrdering.from_offset_col(offsets_col),
            n_rows=data.metadata.row_count,
        )

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
        use_cache: bool = ...,
        filters: third_party_pandas_gbq.FiltersType = ...,
        enable_snapshot: bool = ...,
        dry_run: Literal[False] = ...,
        force_total_order: Optional[bool] = ...,
        n_rows: Optional[int] = None,
        index_col_in_columns: bool = False,
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
        use_cache: bool = ...,
        filters: third_party_pandas_gbq.FiltersType = ...,
        enable_snapshot: bool = ...,
        dry_run: Literal[True] = ...,
        force_total_order: Optional[bool] = ...,
        n_rows: Optional[int] = None,
        index_col_in_columns: bool = False,
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
        use_cache: bool = True,
        filters: third_party_pandas_gbq.FiltersType = (),
        enable_snapshot: bool = True,
        dry_run: bool = False,
        force_total_order: Optional[bool] = None,
        n_rows: Optional[int] = None,
        index_col_in_columns: bool = False,
    ) -> dataframe.DataFrame | pandas.Series:
        """Read a BigQuery table into a BigQuery DataFrames DataFrame.

        This method allows you to create a DataFrame from a BigQuery table.
        You can specify the columns to load, an index column, and apply
        filters.

        Args:
            table_id (str):
                The identifier of the BigQuery table to read.
            index_col (Iterable[str] | str | Iterable[int] | int | bigframes.enums.DefaultIndexKind, optional):
                The column(s) to use as the index for the DataFrame. This can be
                a single column name or a list of column names. If not provided,
                a default index will be used based on the session's
                ``default_index_type``.
            columns (Iterable[str], optional):
                The columns to read from the table. If not specified, all
                columns will be read.
            names (Optional[Iterable[str]], optional):
                A list of column names to use for the resulting DataFrame. This
                is useful if you want to rename the columns as you read the
                data.
            max_results (Optional[int], optional):
                The maximum number of rows to retrieve from the table. If not
                specified, all rows will be loaded.
            use_cache (bool, optional):
                Whether to use cached results for the query. Defaults to True.
                Setting this to False will force a re-execution of the query.
            filters (third_party_pandas_gbq.FiltersType, optional):
                A list of filters to apply to the data. Filters are specified
                as a list of tuples, where each tuple contains a column name,
                an operator (e.g., '==', '!='), and a value.
            enable_snapshot (bool, optional):
                If True, a snapshot of the table is used to ensure that the
                DataFrame is deterministic, even if the underlying table
                changes. Defaults to True.
            dry_run (bool, optional):
                If True, the function will not actually execute the query but
                will instead return statistics about the table. Defaults to False.
            force_total_order (Optional[bool], optional):
                If True, a total ordering is enforced on the DataFrame, which
                can be useful for operations that require a stable row order.
                If None, the session's default behavior is used.
            n_rows (Optional[int], optional):
                The number of rows to consider for type inference and other
                metadata operations. This does not limit the number of rows
                in the final DataFrame.
            index_col_in_columns (bool, optional):
                Specifies if the ``index_col`` is also present in the ``columns``
                list. Defaults to ``False``.

                * If ``False``, ``index_col`` and ``columns`` must specify
                    distinct sets of columns. An error will be raised if any
                    column is found in both.
                * If ``True``, the column(s) in ``index_col`` are expected to
                    also be present in the ``columns`` list. This is useful
                    when the index is selected from the data columns (e.g., in a
                    ``read_csv`` scenario). The column will be used as the
                    DataFrame's index and removed from the list of value columns.
        """
        import bigframes._tools.strings
        import bigframes.dataframe as dataframe

        # ---------------------------------
        # Validate and transform parameters
        # ---------------------------------

        if max_results and max_results <= 0:
            raise ValueError(
                f"`max_results` should be a positive number, got {max_results}."
            )

        _check_duplicates("columns", columns)

        table_ref = google.cloud.bigquery.table.TableReference.from_string(
            table_id, default_project=self._bqclient.project
        )

        columns = list(columns)
        include_all_columns = columns is None or len(columns) == 0
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

        if table.location.casefold() != self._storage_manager.location.casefold():
            raise ValueError(
                f"Current session is in {self._storage_manager.location} but dataset '{table.project}.{table.dataset_id}' is located in {table.location}"
            )

        table_column_names = [field.name for field in table.schema]
        rename_to_schema: Optional[Dict[str, str]] = None
        if names is not None:
            _check_names_param(names, index_col, columns, table_column_names)

            # Additional unnamed columns is going to set as index columns
            len_names = len(list(names))
            len_schema = len(table.schema)
            if len(columns) == 0 and len_names < len_schema:
                index_col = range(len_schema - len_names)
                names = [
                    field.name for field in table.schema[: len_schema - len_names]
                ] + list(names)

            assert len_schema >= len_names
            assert len_names >= len(columns)

            table_column_names = table_column_names[: len(list(names))]
            rename_to_schema = dict(zip(list(names), table_column_names))

        if len(columns) != 0:
            if names is None:
                _check_columns_param(columns, table_column_names)
            else:
                _check_columns_param(columns, names)
                names = columns
                assert rename_to_schema is not None
                columns = [rename_to_schema[renamed_name] for renamed_name in columns]

        # Converting index_col into a list of column names requires
        # the table metadata because we might use the primary keys
        # when constructing the index.
        index_cols = bf_read_gbq_table.get_index_cols(
            table=table,
            index_col=index_col,
            rename_to_schema=rename_to_schema,
        )
        _check_index_col_param(
            index_cols,
            columns,
            table_columns=table_column_names,
            index_col_in_columns=index_col_in_columns,
        )
        if index_col_in_columns and not include_all_columns:
            set_index = set(list(index_cols) if index_cols is not None else [])
            columns = [col for col in columns if col not in set_index]

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
            # If non in strict ordering mode, don't go through overhead of scanning index column(s) to determine if unique
            metadata_only=not self._scan_index_uniqueness,
        )
        schema = schemata.ArraySchema.from_bq_table(table)
        if not include_all_columns:
            schema = schema.select(index_cols + columns)
        array_value = core.ArrayValue.from_table(
            table,
            schema=schema,
            predicate=filter_str,
            at_time=time_travel_timestamp if enable_snapshot else None,
            primary_key=primary_key,
            session=self._session,
            n_rows=n_rows,
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
            assert rename_to_schema is not None
            schema_to_rename = {value: key for key, value in rename_to_schema.items()}
            if index_col != bigframes.enums.DefaultIndexKind.SEQUENTIAL_INT64:
                index_names = [
                    schema_to_rename.get(index_col, index_col)
                    for index_col in index_cols
                ]
            value_columns = [schema_to_rename.get(col, col) for col in value_columns]

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
        use_cache: Optional[bool] = ...,
        filters: third_party_pandas_gbq.FiltersType = ...,
        dry_run: Literal[False] = ...,
        force_total_order: Optional[bool] = ...,
        allow_large_results: bool = ...,
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
        use_cache: Optional[bool] = ...,
        filters: third_party_pandas_gbq.FiltersType = ...,
        dry_run: Literal[True] = ...,
        force_total_order: Optional[bool] = ...,
        allow_large_results: bool = ...,
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
        use_cache: Optional[bool] = None,
        filters: third_party_pandas_gbq.FiltersType = (),
        dry_run: bool = False,
        force_total_order: Optional[bool] = None,
        allow_large_results: bool = True,
    ) -> dataframe.DataFrame | pandas.Series:
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
        _check_index_col_param(index_cols, columns)

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

        query_job_for_metrics: Optional[bigquery.QueryJob] = None
        destination: Optional[bigquery.TableReference] = None

        # TODO(b/421161077): If an explicit destination table is set in
        # configuration, should we respect that setting?
        if allow_large_results:
            destination, query_job = self._query_to_destination(
                query,
                # No cluster candidates as user query might not be clusterable
                # (eg because of ORDER BY clause)
                cluster_candidates=[],
                configuration=configuration,
            )
            query_job_for_metrics = query_job
            rows = None
        else:
            job_config = typing.cast(
                bigquery.QueryJobConfig,
                bigquery.QueryJobConfig.from_api_repr(configuration),
            )

            # TODO(b/420984164): We may want to set a page_size here to limit
            # the number of results in the first jobs.query response.
            rows = self._start_query_with_job_optional(
                query,
                job_config=job_config,
            )

            # If there is a query job, fetch it so that we can get the
            # statistics and destination table, if needed.
            if rows.job_id and rows.location and rows.project:
                query_job = cast(
                    bigquery.QueryJob,
                    self._bqclient.get_job(
                        rows.job_id, project=rows.project, location=rows.location
                    ),
                )
                destination = query_job.destination
                query_job_for_metrics = query_job

        # We split query execution from results fetching so that we can log
        # metrics from either the query job, row iterator, or both.
        if self._metrics is not None:
            self._metrics.count_job_stats(
                query_job=query_job_for_metrics, row_iterator=rows
            )

        # It's possible that there's no job and corresponding destination table.
        # In this case, we must create a local node.
        #
        # TODO(b/420984164): Tune the threshold for which we download to
        # local node. Likely there are a wide range of sizes in which it
        # makes sense to download the results beyond the first page, even if
        # there is a job and destination table available.
        if rows is not None and destination is None:
            return bf_read_gbq_query.create_dataframe_from_row_iterator(
                rows,
                session=self._session,
            )

        # If there was no destination table and we've made it this far, that
        # means the query must have been DDL or DML. Return some job metadata,
        # instead.
        if not destination:
            return bf_read_gbq_query.create_dataframe_from_query_job_stats(
                query_job_for_metrics,
                session=self._session,
            )

        return self.read_gbq_table(
            f"{destination.project}.{destination.dataset_id}.{destination.table_id}",
            index_col=index_col,
            columns=columns,
            use_cache=configuration["query"]["useQueryCache"],
            force_total_order=force_total_order,
            n_rows=query_job.result().total_rows,
            # max_results and filters are omitted because they are already
            # handled by to_query(), above.
        )

    def _query_to_destination(
        self,
        query: str,
        cluster_candidates: List[str],
        configuration: dict = {"query": {"useQueryCache": True}},
        do_clustering=True,
    ) -> Tuple[Optional[bigquery.TableReference], bigquery.QueryJob]:
        # If a dry_run indicates this is not a query type job, then don't
        # bother trying to do a CREATE TEMP TABLE ... AS SELECT ... statement.
        dry_run_config = bigquery.QueryJobConfig()
        dry_run_config.dry_run = True
        dry_run_job = self._start_query_with_job(
            query,
            job_config=dry_run_config,
        )
        if dry_run_job.statement_type != "SELECT":
            query_job = self._start_query_with_job(query)
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
            query_job = self._start_query_with_job(
                query,
                job_config=job_config,
                timeout=timeout,
            )
            return query_job.destination, query_job
        except google.api_core.exceptions.BadRequest:
            # Some SELECT statements still aren't compatible with cluster
            # tables as the destination. For example, if the query has a
            # top-level ORDER BY, this conflicts with our ability to cluster
            # the table by the index column(s).
            query_job = self._start_query_with_job(query, timeout=timeout)
            return query_job.destination, query_job

    def _prepare_job_config(
        self,
        job_config: Optional[google.cloud.bigquery.QueryJobConfig] = None,
    ) -> google.cloud.bigquery.QueryJobConfig:
        job_config = bigquery.QueryJobConfig() if job_config is None else job_config

        if bigframes.options.compute.maximum_bytes_billed is not None:
            # Maybe this should be pushed down into start_query_with_client
            job_config.maximum_bytes_billed = (
                bigframes.options.compute.maximum_bytes_billed
            )

        return job_config

    def _start_query_with_job_optional(
        self,
        sql: str,
        *,
        job_config: Optional[google.cloud.bigquery.QueryJobConfig] = None,
        timeout: Optional[float] = None,
    ) -> google.cloud.bigquery.table.RowIterator:
        """
        Starts BigQuery query with job optional and waits for results.

        Do not execute dataframe through this API, instead use the executor.
        """
        job_config = self._prepare_job_config(job_config)
        rows, _ = bf_io_bigquery.start_query_with_client(
            self._bqclient,
            sql,
            job_config=job_config,
            timeout=timeout,
            location=None,
            project=None,
            metrics=None,
            query_with_job=False,
        )
        return rows

    def _start_query_with_job(
        self,
        sql: str,
        *,
        job_config: Optional[google.cloud.bigquery.QueryJobConfig] = None,
        timeout: Optional[float] = None,
    ) -> bigquery.QueryJob:
        """
        Starts BigQuery query job and waits for results.

        Do not execute dataframe through this API, instead use the executor.
        """
        job_config = self._prepare_job_config(job_config)
        _, query_job = bf_io_bigquery.start_query_with_client(
            self._bqclient,
            sql,
            job_config=job_config,
            timeout=timeout,
            location=None,
            project=None,
            metrics=None,
            query_with_job=True,
        )
        return query_job


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
