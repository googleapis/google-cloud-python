# Copyright 2019 Google LLC
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

"""Shared helper functions for connecting BigQuery and pandas."""

import concurrent.futures
import functools
import logging
import warnings

from six.moves import queue

try:
    from google.cloud import bigquery_storage_v1beta1
except ImportError:  # pragma: NO COVER
    bigquery_storage_v1beta1 = None

try:
    import pandas
except ImportError:  # pragma: NO COVER
    pandas = None

try:
    import pyarrow
    import pyarrow.parquet
except ImportError:  # pragma: NO COVER
    pyarrow = None

from google.cloud.bigquery import schema


_LOGGER = logging.getLogger(__name__)

_NO_BQSTORAGE_ERROR = (
    "The google-cloud-bigquery-storage library is not installed, "
    "please install google-cloud-bigquery-storage to use bqstorage features."
)

_PROGRESS_INTERVAL = 0.2  # Maximum time between download status checks, in seconds.

_PANDAS_DTYPE_TO_BQ = {
    "bool": "BOOLEAN",
    "datetime64[ns, UTC]": "TIMESTAMP",
    "datetime64[ns]": "DATETIME",
    "float32": "FLOAT",
    "float64": "FLOAT",
    "int8": "INTEGER",
    "int16": "INTEGER",
    "int32": "INTEGER",
    "int64": "INTEGER",
    "uint8": "INTEGER",
    "uint16": "INTEGER",
    "uint32": "INTEGER",
}


class _DownloadState(object):
    """Flag to indicate that a thread should exit early."""

    def __init__(self):
        # No need for a lock because reading/replacing a variable is defined to
        # be an atomic operation in the Python language definition (enforced by
        # the global interpreter lock).
        self.done = False


def pyarrow_datetime():
    return pyarrow.timestamp("us", tz=None)


def pyarrow_numeric():
    return pyarrow.decimal128(38, 9)


def pyarrow_time():
    return pyarrow.time64("us")


def pyarrow_timestamp():
    return pyarrow.timestamp("us", tz="UTC")


if pyarrow:
    # This dictionary is duplicated in bigquery_storage/test/unite/test_reader.py
    # When modifying it be sure to update it there as well.
    BQ_TO_ARROW_SCALARS = {
        "BOOL": pyarrow.bool_,
        "BOOLEAN": pyarrow.bool_,
        "BYTES": pyarrow.binary,
        "DATE": pyarrow.date32,
        "DATETIME": pyarrow_datetime,
        "FLOAT": pyarrow.float64,
        "FLOAT64": pyarrow.float64,
        "GEOGRAPHY": pyarrow.string,
        "INT64": pyarrow.int64,
        "INTEGER": pyarrow.int64,
        "NUMERIC": pyarrow_numeric,
        "STRING": pyarrow.string,
        "TIME": pyarrow_time,
        "TIMESTAMP": pyarrow_timestamp,
    }
else:  # pragma: NO COVER
    BQ_TO_ARROW_SCALARS = {}  # pragma: NO COVER


def bq_to_arrow_struct_data_type(field):
    arrow_fields = []
    for subfield in field.fields:
        arrow_subfield = bq_to_arrow_field(subfield)
        if arrow_subfield:
            arrow_fields.append(arrow_subfield)
        else:
            # Could not determine a subfield type. Fallback to type
            # inference.
            return None
    return pyarrow.struct(arrow_fields)


def bq_to_arrow_data_type(field):
    """Return the Arrow data type, corresponding to a given BigQuery column.

    Returns None if default Arrow type inspection should be used.
    """
    if field.mode is not None and field.mode.upper() == "REPEATED":
        inner_type = bq_to_arrow_data_type(
            schema.SchemaField(field.name, field.field_type, fields=field.fields)
        )
        if inner_type:
            return pyarrow.list_(inner_type)
        return None

    if field.field_type.upper() in schema._STRUCT_TYPES:
        return bq_to_arrow_struct_data_type(field)

    data_type_constructor = BQ_TO_ARROW_SCALARS.get(field.field_type.upper())
    if data_type_constructor is None:
        return None
    return data_type_constructor()


def bq_to_arrow_field(bq_field):
    """Return the Arrow field, corresponding to a given BigQuery column.

    Returns None if the Arrow type cannot be determined.
    """
    arrow_type = bq_to_arrow_data_type(bq_field)
    if arrow_type:
        is_nullable = bq_field.mode.upper() == "NULLABLE"
        return pyarrow.field(bq_field.name, arrow_type, nullable=is_nullable)

    warnings.warn("Unable to determine type for field '{}'.".format(bq_field.name))
    return None


def bq_to_arrow_schema(bq_schema):
    """Return the Arrow schema, corresponding to a given BigQuery schema.

    Returns None if any Arrow type cannot be determined.
    """
    arrow_fields = []
    for bq_field in bq_schema:
        arrow_field = bq_to_arrow_field(bq_field)
        if arrow_field is None:
            # Auto-detect the schema if there is an unknown field type.
            return None
        arrow_fields.append(arrow_field)
    return pyarrow.schema(arrow_fields)


def bq_to_arrow_array(series, bq_field):
    arrow_type = bq_to_arrow_data_type(bq_field)
    if bq_field.mode.upper() == "REPEATED":
        return pyarrow.ListArray.from_pandas(series, type=arrow_type)
    if bq_field.field_type.upper() in schema._STRUCT_TYPES:
        return pyarrow.StructArray.from_pandas(series, type=arrow_type)
    return pyarrow.array(series, type=arrow_type)


def get_column_or_index(dataframe, name):
    """Return a column or index as a pandas series."""
    if name in dataframe.columns:
        return dataframe[name].reset_index(drop=True)

    if isinstance(dataframe.index, pandas.MultiIndex):
        if name in dataframe.index.names:
            return (
                dataframe.index.get_level_values(name)
                .to_series()
                .reset_index(drop=True)
            )
    else:
        if name == dataframe.index.name:
            return dataframe.index.to_series().reset_index(drop=True)

    raise ValueError("column or index '{}' not found.".format(name))


def list_columns_and_indexes(dataframe):
    """Return all index and column names with dtypes.

    Returns:
        Sequence[Tuple[dtype, str]]:
            Returns a sorted list of indexes and column names with
            corresponding dtypes. If an index is missing a name or has the
            same name as a column, the index is omitted.
    """
    column_names = frozenset(dataframe.columns)
    columns_and_indexes = []
    if isinstance(dataframe.index, pandas.MultiIndex):
        for name in dataframe.index.names:
            if name and name not in column_names:
                values = dataframe.index.get_level_values(name)
                columns_and_indexes.append((name, values.dtype))
    else:
        if dataframe.index.name and dataframe.index.name not in column_names:
            columns_and_indexes.append((dataframe.index.name, dataframe.index.dtype))

    columns_and_indexes += zip(dataframe.columns, dataframe.dtypes)
    return columns_and_indexes


def dataframe_to_bq_schema(dataframe, bq_schema):
    """Convert a pandas DataFrame schema to a BigQuery schema.

    Args:
        dataframe (pandas.DataFrame):
            DataFrame for which the client determines the BigQuery schema.
        bq_schema (Sequence[google.cloud.bigquery.schema.SchemaField]):
            A BigQuery schema. Use this argument to override the autodetected
            type for some or all of the DataFrame columns.

    Returns:
        Optional[Sequence[google.cloud.bigquery.schema.SchemaField]]:
            The automatically determined schema. Returns None if the type of
            any column cannot be determined.
    """
    if bq_schema:
        for field in bq_schema:
            if field.field_type in schema._STRUCT_TYPES:
                raise ValueError(
                    "Uploading dataframes with struct (record) column types "
                    "is not supported. See: "
                    "https://github.com/googleapis/google-cloud-python/issues/8191"
                )
        bq_schema_index = {field.name: field for field in bq_schema}
        bq_schema_unused = set(bq_schema_index.keys())
    else:
        bq_schema_index = {}
        bq_schema_unused = set()

    bq_schema_out = []
    for column, dtype in list_columns_and_indexes(dataframe):
        # Use provided type from schema, if present.
        bq_field = bq_schema_index.get(column)
        if bq_field:
            bq_schema_out.append(bq_field)
            bq_schema_unused.discard(bq_field.name)
            continue

        # Otherwise, try to automatically determine the type based on the
        # pandas dtype.
        bq_type = _PANDAS_DTYPE_TO_BQ.get(dtype.name)
        if not bq_type:
            warnings.warn(u"Unable to determine type of column '{}'.".format(column))
            return None
        bq_field = schema.SchemaField(column, bq_type)
        bq_schema_out.append(bq_field)

    # Catch any schema mismatch. The developer explicitly asked to serialize a
    # column, but it was not found.
    if bq_schema_unused:
        raise ValueError(
            u"bq_schema contains fields not present in dataframe: {}".format(
                bq_schema_unused
            )
        )
    return tuple(bq_schema_out)


def dataframe_to_arrow(dataframe, bq_schema):
    """Convert pandas dataframe to Arrow table, using BigQuery schema.

    Args:
        dataframe (pandas.DataFrame):
            DataFrame to convert to Arrow table.
        bq_schema (Sequence[google.cloud.bigquery.schema.SchemaField]):
            Desired BigQuery schema. Number of columns must match number of
            columns in the DataFrame.

    Returns:
        pyarrow.Table:
            Table containing dataframe data, with schema derived from
            BigQuery schema.
    """
    column_names = set(dataframe.columns)
    column_and_index_names = set(
        name for name, _ in list_columns_and_indexes(dataframe)
    )
    bq_field_names = set(field.name for field in bq_schema)

    extra_fields = bq_field_names - column_and_index_names
    if extra_fields:
        raise ValueError(
            u"bq_schema contains fields not present in dataframe: {}".format(
                extra_fields
            )
        )

    # It's okay for indexes to be missing from bq_schema, but it's not okay to
    # be missing columns.
    missing_fields = column_names - bq_field_names
    if missing_fields:
        raise ValueError(
            u"bq_schema is missing fields from dataframe: {}".format(missing_fields)
        )

    arrow_arrays = []
    arrow_names = []
    arrow_fields = []
    for bq_field in bq_schema:
        arrow_fields.append(bq_to_arrow_field(bq_field))
        arrow_names.append(bq_field.name)
        arrow_arrays.append(
            bq_to_arrow_array(get_column_or_index(dataframe, bq_field.name), bq_field)
        )

    if all((field is not None for field in arrow_fields)):
        return pyarrow.Table.from_arrays(
            arrow_arrays, schema=pyarrow.schema(arrow_fields)
        )
    return pyarrow.Table.from_arrays(arrow_arrays, names=arrow_names)


def dataframe_to_parquet(dataframe, bq_schema, filepath, parquet_compression="SNAPPY"):
    """Write dataframe as a Parquet file, according to the desired BQ schema.

    This function requires the :mod:`pyarrow` package. Arrow is used as an
    intermediate format.

    Args:
        dataframe (pandas.DataFrame):
            DataFrame to convert to Parquet file.
        bq_schema (Sequence[google.cloud.bigquery.schema.SchemaField]):
            Desired BigQuery schema. Number of columns must match number of
            columns in the DataFrame.
        filepath (str):
            Path to write Parquet file to.
        parquet_compression (str):
            (optional) The compression codec to use by the the
            ``pyarrow.parquet.write_table`` serializing method. Defaults to
            "SNAPPY".
            https://arrow.apache.org/docs/python/generated/pyarrow.parquet.write_table.html#pyarrow-parquet-write-table
    """
    if pyarrow is None:
        raise ValueError("pyarrow is required for BigQuery schema conversion.")

    arrow_table = dataframe_to_arrow(dataframe, bq_schema)
    pyarrow.parquet.write_table(arrow_table, filepath, compression=parquet_compression)


def _tabledata_list_page_to_arrow(page, column_names, arrow_types):
    # Iterate over the page to force the API request to get the page data.
    try:
        next(iter(page))
    except StopIteration:
        pass

    arrays = []
    for column_index, arrow_type in enumerate(arrow_types):
        arrays.append(pyarrow.array(page._columns[column_index], type=arrow_type))

    return pyarrow.RecordBatch.from_arrays(arrays, column_names)


def download_arrow_tabledata_list(pages, schema):
    """Use tabledata.list to construct an iterable of RecordBatches."""
    column_names = bq_to_arrow_schema(schema) or [field.name for field in schema]
    arrow_types = [bq_to_arrow_data_type(field) for field in schema]

    for page in pages:
        yield _tabledata_list_page_to_arrow(page, column_names, arrow_types)


def _tabledata_list_page_to_dataframe(page, column_names, dtypes):
    # Iterate over the page to force the API request to get the page data.
    try:
        next(iter(page))
    except StopIteration:
        pass

    columns = {}
    for column_index, column_name in enumerate(column_names):
        dtype = dtypes.get(column_name)
        columns[column_name] = pandas.Series(page._columns[column_index], dtype=dtype)

    return pandas.DataFrame(columns, columns=column_names)


def download_dataframe_tabledata_list(pages, schema, dtypes):
    """Use (slower, but free) tabledata.list to construct a DataFrame."""
    column_names = [field.name for field in schema]
    for page in pages:
        yield _tabledata_list_page_to_dataframe(page, column_names, dtypes)


def _bqstorage_page_to_arrow(page):
    return page.to_arrow()


def _bqstorage_page_to_dataframe(column_names, dtypes, page):
    # page.to_dataframe() does not preserve column order in some versions
    # of google-cloud-bigquery-storage. Access by column name to rearrange.
    return page.to_dataframe(dtypes=dtypes)[column_names]


def _download_table_bqstorage_stream(
    download_state, bqstorage_client, session, stream, worker_queue, page_to_item
):
    position = bigquery_storage_v1beta1.types.StreamPosition(stream=stream)
    rowstream = bqstorage_client.read_rows(position).rows(session)

    for page in rowstream.pages:
        if download_state.done:
            return
        item = page_to_item(page)
        worker_queue.put(item)


def _nowait(futures):
    """Separate finished and unfinished threads, much like
    :func:`concurrent.futures.wait`, but don't wait.
    """
    done = []
    not_done = []
    for future in futures:
        if future.done():
            done.append(future)
        else:
            not_done.append(future)
    return done, not_done


def _download_table_bqstorage(
    project_id,
    table,
    bqstorage_client,
    preserve_order=False,
    selected_fields=None,
    page_to_item=None,
):
    """Use (faster, but billable) BQ Storage API to construct DataFrame."""
    if "$" in table.table_id:
        raise ValueError(
            "Reading from a specific partition is not currently supported."
        )
    if "@" in table.table_id:
        raise ValueError("Reading from a specific snapshot is not currently supported.")

    read_options = bigquery_storage_v1beta1.types.TableReadOptions()
    if selected_fields is not None:
        for field in selected_fields:
            read_options.selected_fields.append(field.name)

    requested_streams = 0
    if preserve_order:
        requested_streams = 1

    session = bqstorage_client.create_read_session(
        table.to_bqstorage(),
        "projects/{}".format(project_id),
        format_=bigquery_storage_v1beta1.enums.DataFormat.ARROW,
        read_options=read_options,
        requested_streams=requested_streams,
    )
    _LOGGER.debug(
        "Started reading table '{}.{}.{}' with BQ Storage API session '{}'.".format(
            table.project, table.dataset_id, table.table_id, session.name
        )
    )

    # Avoid reading rows from an empty table.
    if not session.streams:
        return

    total_streams = len(session.streams)

    # Use _DownloadState to notify worker threads when to quit.
    # See: https://stackoverflow.com/a/29237343/101923
    download_state = _DownloadState()

    # Create a queue to collect frames as they are created in each thread.
    worker_queue = queue.Queue()

    with concurrent.futures.ThreadPoolExecutor(max_workers=total_streams) as pool:
        try:
            # Manually submit jobs and wait for download to complete rather
            # than using pool.map because pool.map continues running in the
            # background even if there is an exception on the main thread.
            # See: https://github.com/googleapis/google-cloud-python/pull/7698
            not_done = [
                pool.submit(
                    _download_table_bqstorage_stream,
                    download_state,
                    bqstorage_client,
                    session,
                    stream,
                    worker_queue,
                    page_to_item,
                )
                for stream in session.streams
            ]

            while not_done:
                # Don't block on the worker threads. For performance reasons,
                # we want to block on the queue's get method, instead. This
                # prevents the queue from filling up, because the main thread
                # has smaller gaps in time between calls to the queue's get
                # method. For a detailed explaination, see:
                # https://friendliness.dev/2019/06/18/python-nowait/
                done, not_done = _nowait(not_done)
                for future in done:
                    # Call result() on any finished threads to raise any
                    # exceptions encountered.
                    future.result()

                try:
                    frame = worker_queue.get(timeout=_PROGRESS_INTERVAL)
                    yield frame
                except queue.Empty:  # pragma: NO COVER
                    continue

            # Return any remaining values after the workers finished.
            while not worker_queue.empty():  # pragma: NO COVER
                try:
                    # Include a timeout because even though the queue is
                    # non-empty, it doesn't guarantee that a subsequent call to
                    # get() will not block.
                    frame = worker_queue.get(timeout=_PROGRESS_INTERVAL)
                    yield frame
                except queue.Empty:  # pragma: NO COVER
                    continue
        finally:
            # No need for a lock because reading/replacing a variable is
            # defined to be an atomic operation in the Python language
            # definition (enforced by the global interpreter lock).
            download_state.done = True

            # Shutdown all background threads, now that they should know to
            # exit early.
            pool.shutdown(wait=True)


def download_arrow_bqstorage(
    project_id, table, bqstorage_client, preserve_order=False, selected_fields=None
):
    return _download_table_bqstorage(
        project_id,
        table,
        bqstorage_client,
        preserve_order=preserve_order,
        selected_fields=selected_fields,
        page_to_item=_bqstorage_page_to_arrow,
    )


def download_dataframe_bqstorage(
    project_id,
    table,
    bqstorage_client,
    column_names,
    dtypes,
    preserve_order=False,
    selected_fields=None,
):
    page_to_item = functools.partial(_bqstorage_page_to_dataframe, column_names, dtypes)
    return _download_table_bqstorage(
        project_id,
        table,
        bqstorage_client,
        preserve_order=preserve_order,
        selected_fields=selected_fields,
        page_to_item=page_to_item,
    )
