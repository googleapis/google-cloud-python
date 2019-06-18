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

import collections
import concurrent.futures
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


_NO_BQSTORAGE_ERROR = (
    "The google-cloud-bigquery-storage library is not installed, "
    "please install google-cloud-bigquery-storage to use bqstorage features."
)

STRUCT_TYPES = ("RECORD", "STRUCT")
_PROGRESS_INTERVAL = 0.2  # Maximum time between download status checks, in seconds.


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
            schema.SchemaField(field.name, field.field_type)
        )
        if inner_type:
            return pyarrow.list_(inner_type)
        return None

    if field.field_type.upper() in STRUCT_TYPES:
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


def bq_to_arrow_array(series, bq_field):
    arrow_type = bq_to_arrow_data_type(bq_field)
    if bq_field.mode.upper() == "REPEATED":
        return pyarrow.ListArray.from_pandas(series, type=arrow_type)
    if bq_field.field_type.upper() in STRUCT_TYPES:
        return pyarrow.StructArray.from_pandas(series, type=arrow_type)
    return pyarrow.array(series, type=arrow_type)


def dataframe_to_arrow(dataframe, bq_schema):
    """Convert pandas dataframe to Arrow table, using BigQuery schema.

    Args:
        dataframe (pandas.DataFrame):
            DataFrame to convert to convert to Parquet file.
        bq_schema (Sequence[google.cloud.bigquery.schema.SchemaField]):
            Desired BigQuery schema. Number of columns must match number of
            columns in the DataFrame.

    Returns:
        pyarrow.Table:
            Table containing dataframe data, with schema derived from
            BigQuery schema.
    """
    if len(bq_schema) != len(dataframe.columns):
        raise ValueError(
            "Number of columns in schema must match number of columns in dataframe."
        )

    arrow_arrays = []
    arrow_names = []
    arrow_fields = []
    for bq_field in bq_schema:
        arrow_fields.append(bq_to_arrow_field(bq_field))
        arrow_names.append(bq_field.name)
        arrow_arrays.append(bq_to_arrow_array(dataframe[bq_field.name], bq_field))

    if all((field is not None for field in arrow_fields)):
        return pyarrow.Table.from_arrays(
            arrow_arrays, schema=pyarrow.schema(arrow_fields)
        )
    return pyarrow.Table.from_arrays(arrow_arrays, names=arrow_names)


def dataframe_to_parquet(dataframe, bq_schema, filepath):
    """Write dataframe as a Parquet file, according to the desired BQ schema.

    This function requires the :mod:`pyarrow` package. Arrow is used as an
    intermediate format.

    Args:
        dataframe (pandas.DataFrame):
            DataFrame to convert to convert to Parquet file.
        bq_schema (Sequence[google.cloud.bigquery.schema.SchemaField]):
            Desired BigQuery schema. Number of columns must match number of
            columns in the DataFrame.
        filepath (str):
            Path to write Parquet file to.
    """
    if pyarrow is None:
        raise ValueError("pyarrow is required for BigQuery schema conversion.")

    arrow_table = dataframe_to_arrow(dataframe, bq_schema)
    pyarrow.parquet.write_table(arrow_table, filepath)


def _tabledata_list_page_to_dataframe(page, column_names, dtypes):
    columns = collections.defaultdict(list)
    for row in page:
        for column in column_names:
            columns[column].append(row[column])
    for column in dtypes:
        columns[column] = pandas.Series(columns[column], dtype=dtypes[column])
    return pandas.DataFrame(columns, columns=column_names)


def download_dataframe_tabledata_list(pages, schema, dtypes):
    """Use (slower, but free) tabledata.list to construct a DataFrame."""
    column_names = [field.name for field in schema]
    for page in pages:
        yield _tabledata_list_page_to_dataframe(page, column_names, dtypes)


def _download_dataframe_bqstorage_stream(
    download_state,
    bqstorage_client,
    column_names,
    dtypes,
    session,
    stream,
    worker_queue,
):
    position = bigquery_storage_v1beta1.types.StreamPosition(stream=stream)
    rowstream = bqstorage_client.read_rows(position).rows(session)

    for page in rowstream.pages:
        if download_state.done:
            return
        # page.to_dataframe() does not preserve column order in some versions
        # of google-cloud-bigquery-storage. Access by column name to rearrange.
        frame = page.to_dataframe(dtypes=dtypes)[column_names]
        worker_queue.put(frame)


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


def download_dataframe_bqstorage(
    project_id,
    table,
    bqstorage_client,
    column_names,
    dtypes,
    preserve_order=False,
    selected_fields=None,
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
        read_options=read_options,
        requested_streams=requested_streams,
    )

    # Avoid reading rows from an empty table. pandas.concat will fail on an
    # empty list.
    if not session.streams:
        yield pandas.DataFrame(columns=column_names)
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
                    _download_dataframe_bqstorage_stream,
                    download_state,
                    bqstorage_client,
                    column_names,
                    dtypes,
                    session,
                    stream,
                    worker_queue,
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
            while not worker_queue.empty():
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
