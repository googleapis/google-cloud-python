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
from datetime import datetime
import functools
from itertools import islice
import logging
import queue
import warnings
from typing import Any, Union


from google.cloud.bigquery import _pyarrow_helpers
from google.cloud.bigquery import _versions_helpers
from google.cloud.bigquery import schema

try:
    import pandas  # type: ignore

    pandas_import_exception = None
except ImportError as exc:
    pandas = None
    pandas_import_exception = exc
else:
    import numpy

try:
    import db_dtypes  # type: ignore

    date_dtype_name = db_dtypes.DateDtype.name
    time_dtype_name = db_dtypes.TimeDtype.name
    db_dtypes_import_exception = None
except ImportError as exc:
    db_dtypes = None
    db_dtypes_import_exception = exc
    date_dtype_name = time_dtype_name = ""  # Use '' rather than None because pytype

pyarrow = _versions_helpers.PYARROW_VERSIONS.try_import()

try:
    # _BaseGeometry is used to detect shapely objevys in `bq_to_arrow_array`
    from shapely.geometry.base import BaseGeometry as _BaseGeometry  # type: ignore
except ImportError:
    # No shapely, use NoneType for _BaseGeometry as a placeholder.
    _BaseGeometry = type(None)
else:
    # We don't have any unit test sessions that install shapely but not pandas.
    if pandas is not None:  # pragma: NO COVER

        def _to_wkb():
            from shapely import wkb  # type: ignore

            write = wkb.dumps
            notnull = pandas.notnull

            def _to_wkb(v):
                return write(v) if notnull(v) else v

            return _to_wkb

        _to_wkb = _to_wkb()

try:
    from google.cloud.bigquery_storage import ArrowSerializationOptions
except ImportError:
    _ARROW_COMPRESSION_SUPPORT = False
else:
    # Having BQ Storage available implies that pyarrow >=1.0.0 is available, too.
    _ARROW_COMPRESSION_SUPPORT = True

_LOGGER = logging.getLogger(__name__)

_PROGRESS_INTERVAL = 0.2  # Maximum time between download status checks, in seconds.

_MAX_QUEUE_SIZE_DEFAULT = object()  # max queue size sentinel for BQ Storage downloads

_NO_PANDAS_ERROR = "Please install the 'pandas' package to use this function."
_NO_DB_TYPES_ERROR = "Please install the 'db-dtypes' package to use this function."

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
    "geometry": "GEOGRAPHY",
    date_dtype_name: "DATE",
    time_dtype_name: "TIME",
}


class _DownloadState(object):
    """Flag to indicate that a thread should exit early."""

    def __init__(self):
        # No need for a lock because reading/replacing a variable is defined to
        # be an atomic operation in the Python language definition (enforced by
        # the global interpreter lock).
        self.done = False


BQ_FIELD_TYPE_TO_ARROW_FIELD_METADATA = {
    "GEOGRAPHY": {
        b"ARROW:extension:name": b"google:sqlType:geography",
        b"ARROW:extension:metadata": b'{"encoding": "WKT"}',
    },
    "DATETIME": {b"ARROW:extension:name": b"google:sqlType:datetime"},
}


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

    Returns:
        None: if default Arrow type inspection should be used.
    """
    if field.mode is not None and field.mode.upper() == "REPEATED":
        inner_type = bq_to_arrow_data_type(
            schema.SchemaField(field.name, field.field_type, fields=field.fields)
        )
        if inner_type:
            return pyarrow.list_(inner_type)
        return None

    field_type_upper = field.field_type.upper() if field.field_type else ""
    if field_type_upper in schema._STRUCT_TYPES:
        return bq_to_arrow_struct_data_type(field)

    data_type_constructor = _pyarrow_helpers.bq_to_arrow_scalars(field_type_upper)
    if data_type_constructor is None:
        return None
    return data_type_constructor()


def bq_to_arrow_field(bq_field, array_type=None):
    """Return the Arrow field, corresponding to a given BigQuery column.

    Returns:
        None: if the Arrow type cannot be determined.
    """
    arrow_type = bq_to_arrow_data_type(bq_field)
    if arrow_type is not None:
        if array_type is not None:
            arrow_type = array_type  # For GEOGRAPHY, at least initially
        metadata = BQ_FIELD_TYPE_TO_ARROW_FIELD_METADATA.get(
            bq_field.field_type.upper() if bq_field.field_type else ""
        )
        return pyarrow.field(
            bq_field.name,
            arrow_type,
            # Even if the remote schema is REQUIRED, there's a chance there's
            # local NULL values. Arrow will gladly interpret these NULL values
            # as non-NULL and give you an arbitrary value. See:
            # https://github.com/googleapis/python-bigquery/issues/1692
            nullable=True,
            metadata=metadata,
        )

    warnings.warn("Unable to determine type for field '{}'.".format(bq_field.name))
    return None


def bq_to_arrow_schema(bq_schema):
    """Return the Arrow schema, corresponding to a given BigQuery schema.

    Returns:
        None: if any Arrow type cannot be determined.
    """
    arrow_fields = []
    for bq_field in bq_schema:
        arrow_field = bq_to_arrow_field(bq_field)
        if arrow_field is None:
            # Auto-detect the schema if there is an unknown field type.
            return None
        arrow_fields.append(arrow_field)
    return pyarrow.schema(arrow_fields)


def default_types_mapper(
    date_as_object: bool = False,
    bool_dtype: Union[Any, None] = None,
    int_dtype: Union[Any, None] = None,
    float_dtype: Union[Any, None] = None,
    string_dtype: Union[Any, None] = None,
    date_dtype: Union[Any, None] = None,
    datetime_dtype: Union[Any, None] = None,
    time_dtype: Union[Any, None] = None,
    timestamp_dtype: Union[Any, None] = None,
):
    """Create a mapping from pyarrow types to pandas types.

    This overrides the pandas defaults to use null-safe extension types where
    available.

    See: https://arrow.apache.org/docs/python/api/datatypes.html for a list of
    data types. See:
    tests/unit/test__pandas_helpers.py::test_bq_to_arrow_data_type for
    BigQuery to Arrow type mapping.

    Note to google-cloud-bigquery developers: If you update the default dtypes,
    also update the docs at docs/usage/pandas.rst.
    """

    def types_mapper(arrow_data_type):
        if bool_dtype is not None and pyarrow.types.is_boolean(arrow_data_type):
            return bool_dtype

        elif int_dtype is not None and pyarrow.types.is_integer(arrow_data_type):
            return int_dtype

        elif float_dtype is not None and pyarrow.types.is_floating(arrow_data_type):
            return float_dtype

        elif string_dtype is not None and pyarrow.types.is_string(arrow_data_type):
            return string_dtype

        elif (
            # If date_as_object is True, we know some DATE columns are
            # out-of-bounds of what is supported by pandas.
            date_dtype is not None
            and not date_as_object
            and pyarrow.types.is_date(arrow_data_type)
        ):
            return date_dtype

        elif (
            datetime_dtype is not None
            and pyarrow.types.is_timestamp(arrow_data_type)
            and arrow_data_type.tz is None
        ):
            return datetime_dtype

        elif (
            timestamp_dtype is not None
            and pyarrow.types.is_timestamp(arrow_data_type)
            and arrow_data_type.tz is not None
        ):
            return timestamp_dtype

        elif time_dtype is not None and pyarrow.types.is_time(arrow_data_type):
            return time_dtype

    return types_mapper


def bq_to_arrow_array(series, bq_field):
    if bq_field.field_type.upper() == "GEOGRAPHY":
        arrow_type = None
        first = _first_valid(series)
        if first is not None:
            if series.dtype.name == "geometry" or isinstance(first, _BaseGeometry):
                arrow_type = pyarrow.binary()
                # Convert shapey geometry to WKB binary format:
                series = series.apply(_to_wkb)
            elif isinstance(first, bytes):
                arrow_type = pyarrow.binary()
        elif series.dtype.name == "geometry":
            # We have a GeoSeries containing all nulls, convert it to a pandas series
            series = pandas.Series(numpy.array(series))

        if arrow_type is None:
            arrow_type = bq_to_arrow_data_type(bq_field)
    else:
        arrow_type = bq_to_arrow_data_type(bq_field)

    field_type_upper = bq_field.field_type.upper() if bq_field.field_type else ""

    try:
        if bq_field.mode.upper() == "REPEATED":
            return pyarrow.ListArray.from_pandas(series, type=arrow_type)
        if field_type_upper in schema._STRUCT_TYPES:
            return pyarrow.StructArray.from_pandas(series, type=arrow_type)
        return pyarrow.Array.from_pandas(series, type=arrow_type)
    except pyarrow.ArrowTypeError:
        msg = f"""Error converting Pandas column with name: "{series.name}" and datatype: "{series.dtype}" to an appropriate pyarrow datatype: Array, ListArray, or StructArray"""
        _LOGGER.error(msg)
        raise pyarrow.ArrowTypeError(msg)


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
        Sequence[Tuple[str, dtype]]:
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


def _first_valid(series):
    first_valid_index = series.first_valid_index()
    if first_valid_index is not None:
        return series.at[first_valid_index]


def _first_array_valid(series):
    """Return the first "meaningful" element from the array series.

    Here, "meaningful" means the first non-None element in one of the arrays that can
    be used for type detextion.
    """
    first_valid_index = series.first_valid_index()
    if first_valid_index is None:
        return None

    valid_array = series.at[first_valid_index]
    valid_item = next((item for item in valid_array if not pandas.isna(item)), None)

    if valid_item is not None:
        return valid_item

    # Valid item is None because all items in the "valid" array are invalid. Try
    # to find a true valid array manually.
    for array in islice(series, first_valid_index + 1, None):
        try:
            array_iter = iter(array)
        except TypeError:
            continue  # Not an array, apparently, e.g. None, thus skip.
        valid_item = next((item for item in array_iter if not pandas.isna(item)), None)
        if valid_item is not None:
            break

    return valid_item


def dataframe_to_bq_schema(dataframe, bq_schema):
    """Convert a pandas DataFrame schema to a BigQuery schema.

    Args:
        dataframe (pandas.DataFrame):
            DataFrame for which the client determines the BigQuery schema.
        bq_schema (Sequence[Union[ \
            :class:`~google.cloud.bigquery.schema.SchemaField`, \
            Mapping[str, Any] \
        ]]):
            A BigQuery schema. Use this argument to override the autodetected
            type for some or all of the DataFrame columns.

    Returns:
        Optional[Sequence[google.cloud.bigquery.schema.SchemaField]]:
            The automatically determined schema. Returns None if the type of
            any column cannot be determined.
    """
    if bq_schema:
        bq_schema = schema._to_schema_fields(bq_schema)
        bq_schema_index = {field.name: field for field in bq_schema}
        bq_schema_unused = set(bq_schema_index.keys())
    else:
        bq_schema_index = {}
        bq_schema_unused = set()

    bq_schema_out = []
    unknown_type_fields = []

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
        if bq_type is None:
            sample_data = _first_valid(dataframe.reset_index()[column])
            if (
                isinstance(sample_data, _BaseGeometry)
                and sample_data is not None  # Paranoia
            ):
                bq_type = "GEOGRAPHY"
        bq_field = schema.SchemaField(column, bq_type)
        bq_schema_out.append(bq_field)

        if bq_field.field_type is None:
            unknown_type_fields.append(bq_field)

    # Catch any schema mismatch. The developer explicitly asked to serialize a
    # column, but it was not found.
    if bq_schema_unused:
        raise ValueError(
            "bq_schema contains fields not present in dataframe: {}".format(
                bq_schema_unused
            )
        )

    # If schema detection was not successful for all columns, also try with
    # pyarrow, if available.
    if unknown_type_fields:
        if not pyarrow:
            msg = "Could not determine the type of columns: {}".format(
                ", ".join(field.name for field in unknown_type_fields)
            )
            warnings.warn(msg)
            return None  # We cannot detect the schema in full.

        # The augment_schema() helper itself will also issue unknown type
        # warnings if detection still fails for any of the fields.
        bq_schema_out = augment_schema(dataframe, bq_schema_out)

    return tuple(bq_schema_out) if bq_schema_out else None


def augment_schema(dataframe, current_bq_schema):
    """Try to deduce the unknown field types and return an improved schema.

    This function requires ``pyarrow`` to run. If all the missing types still
    cannot be detected, ``None`` is returned. If all types are already known,
    a shallow copy of the given schema is returned.

    Args:
        dataframe (pandas.DataFrame):
            DataFrame for which some of the field types are still unknown.
        current_bq_schema (Sequence[google.cloud.bigquery.schema.SchemaField]):
            A BigQuery schema for ``dataframe``. The types of some or all of
            the fields may be ``None``.
    Returns:
        Optional[Sequence[google.cloud.bigquery.schema.SchemaField]]
    """
    # pytype: disable=attribute-error
    augmented_schema = []
    unknown_type_fields = []
    for field in current_bq_schema:
        if field.field_type is not None:
            augmented_schema.append(field)
            continue

        arrow_table = pyarrow.array(dataframe.reset_index()[field.name])

        if pyarrow.types.is_list(arrow_table.type):
            # `pyarrow.ListType`
            detected_mode = "REPEATED"
            detected_type = _pyarrow_helpers.arrow_scalar_ids_to_bq(
                arrow_table.values.type.id
            )

            # For timezone-naive datetimes, pyarrow assumes the UTC timezone and adds
            # it to such datetimes, causing them to be recognized as TIMESTAMP type.
            # We thus additionally check the actual data to see if we need to overrule
            # that and choose DATETIME instead.
            # Note that this should only be needed for datetime values inside a list,
            # since scalar datetime values have a proper Pandas dtype that allows
            # distinguishing between timezone-naive and timezone-aware values before
            # even requiring the additional schema augment logic in this method.
            if detected_type == "TIMESTAMP":
                valid_item = _first_array_valid(dataframe[field.name])
                if isinstance(valid_item, datetime) and valid_item.tzinfo is None:
                    detected_type = "DATETIME"
        else:
            detected_mode = field.mode
            detected_type = _pyarrow_helpers.arrow_scalar_ids_to_bq(arrow_table.type.id)
            if detected_type == "NUMERIC" and arrow_table.type.scale > 9:
                detected_type = "BIGNUMERIC"

        if detected_type is None:
            unknown_type_fields.append(field)
            continue

        new_field = schema.SchemaField(
            name=field.name,
            field_type=detected_type,
            mode=detected_mode,
            description=field.description,
            fields=field.fields,
        )
        augmented_schema.append(new_field)

    if unknown_type_fields:
        warnings.warn(
            "Pyarrow could not determine the type of columns: {}.".format(
                ", ".join(field.name for field in unknown_type_fields)
            )
        )
        return None

    return augmented_schema
    # pytype: enable=attribute-error


def dataframe_to_arrow(dataframe, bq_schema):
    """Convert pandas dataframe to Arrow table, using BigQuery schema.

    Args:
        dataframe (pandas.DataFrame):
            DataFrame to convert to Arrow table.
        bq_schema (Sequence[Union[ \
            :class:`~google.cloud.bigquery.schema.SchemaField`, \
            Mapping[str, Any] \
        ]]):
            Desired BigQuery schema. The number of columns must match the
            number of columns in the DataFrame.

    Returns:
        pyarrow.Table:
            Table containing dataframe data, with schema derived from
            BigQuery schema.
    """
    column_names = set(dataframe.columns)
    column_and_index_names = set(
        name for name, _ in list_columns_and_indexes(dataframe)
    )

    bq_schema = schema._to_schema_fields(bq_schema)
    bq_field_names = set(field.name for field in bq_schema)

    extra_fields = bq_field_names - column_and_index_names
    if extra_fields:
        raise ValueError(
            "bq_schema contains fields not present in dataframe: {}".format(
                extra_fields
            )
        )

    # It's okay for indexes to be missing from bq_schema, but it's not okay to
    # be missing columns.
    missing_fields = column_names - bq_field_names
    if missing_fields:
        raise ValueError(
            "bq_schema is missing fields from dataframe: {}".format(missing_fields)
        )

    arrow_arrays = []
    arrow_names = []
    arrow_fields = []
    for bq_field in bq_schema:
        arrow_names.append(bq_field.name)
        arrow_arrays.append(
            bq_to_arrow_array(get_column_or_index(dataframe, bq_field.name), bq_field)
        )
        arrow_fields.append(bq_to_arrow_field(bq_field, arrow_arrays[-1].type))

    if all((field is not None for field in arrow_fields)):
        return pyarrow.Table.from_arrays(
            arrow_arrays, schema=pyarrow.schema(arrow_fields)
        )
    return pyarrow.Table.from_arrays(arrow_arrays, names=arrow_names)


def dataframe_to_parquet(
    dataframe,
    bq_schema,
    filepath,
    parquet_compression="SNAPPY",
    parquet_use_compliant_nested_type=True,
):
    """Write dataframe as a Parquet file, according to the desired BQ schema.

    This function requires the :mod:`pyarrow` package. Arrow is used as an
    intermediate format.

    Args:
        dataframe (pandas.DataFrame):
            DataFrame to convert to Parquet file.
        bq_schema (Sequence[Union[ \
            :class:`~google.cloud.bigquery.schema.SchemaField`, \
            Mapping[str, Any] \
        ]]):
            Desired BigQuery schema. Number of columns must match number of
            columns in the DataFrame.
        filepath (str):
            Path to write Parquet file to.
        parquet_compression (Optional[str]):
            The compression codec to use by the the ``pyarrow.parquet.write_table``
            serializing method. Defaults to "SNAPPY".
            https://arrow.apache.org/docs/python/generated/pyarrow.parquet.write_table.html#pyarrow-parquet-write-table
        parquet_use_compliant_nested_type (bool):
            Whether the ``pyarrow.parquet.write_table`` serializing method should write
            compliant Parquet nested type (lists). Defaults to ``True``.
            https://github.com/apache/parquet-format/blob/master/LogicalTypes.md#nested-types
            https://arrow.apache.org/docs/python/generated/pyarrow.parquet.write_table.html#pyarrow-parquet-write-table

            This argument is ignored for ``pyarrow`` versions earlier than ``4.0.0``.
    """
    pyarrow = _versions_helpers.PYARROW_VERSIONS.try_import(raise_if_error=True)

    import pyarrow.parquet  # type: ignore

    kwargs = (
        {"use_compliant_nested_type": parquet_use_compliant_nested_type}
        if _versions_helpers.PYARROW_VERSIONS.use_compliant_nested_type
        else {}
    )

    bq_schema = schema._to_schema_fields(bq_schema)
    arrow_table = dataframe_to_arrow(dataframe, bq_schema)
    pyarrow.parquet.write_table(
        arrow_table,
        filepath,
        compression=parquet_compression,
        **kwargs,
    )


def _row_iterator_page_to_arrow(page, column_names, arrow_types):
    # Iterate over the page to force the API request to get the page data.
    try:
        next(iter(page))
    except StopIteration:
        pass

    arrays = []
    for column_index, arrow_type in enumerate(arrow_types):
        arrays.append(pyarrow.array(page._columns[column_index], type=arrow_type))

    if isinstance(column_names, pyarrow.Schema):
        return pyarrow.RecordBatch.from_arrays(arrays, schema=column_names)
    return pyarrow.RecordBatch.from_arrays(arrays, names=column_names)


def download_arrow_row_iterator(pages, bq_schema):
    """Use HTTP JSON RowIterator to construct an iterable of RecordBatches.

    Args:
        pages (Iterator[:class:`google.api_core.page_iterator.Page`]):
            An iterator over the result pages.
        bq_schema (Sequence[Union[ \
            :class:`~google.cloud.bigquery.schema.SchemaField`, \
            Mapping[str, Any] \
        ]]):
            A decription of the fields in result pages.
    Yields:
        :class:`pyarrow.RecordBatch`
        The next page of records as a ``pyarrow`` record batch.
    """
    bq_schema = schema._to_schema_fields(bq_schema)
    column_names = bq_to_arrow_schema(bq_schema) or [field.name for field in bq_schema]
    arrow_types = [bq_to_arrow_data_type(field) for field in bq_schema]

    for page in pages:
        yield _row_iterator_page_to_arrow(page, column_names, arrow_types)


def _row_iterator_page_to_dataframe(page, column_names, dtypes):
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


def download_dataframe_row_iterator(pages, bq_schema, dtypes):
    """Use HTTP JSON RowIterator to construct a DataFrame.

    Args:
        pages (Iterator[:class:`google.api_core.page_iterator.Page`]):
            An iterator over the result pages.
        bq_schema (Sequence[Union[ \
            :class:`~google.cloud.bigquery.schema.SchemaField`, \
            Mapping[str, Any] \
        ]]):
            A decription of the fields in result pages.
        dtypes(Mapping[str, numpy.dtype]):
            The types of columns in result data to hint construction of the
            resulting DataFrame. Not all column types have to be specified.
    Yields:
        :class:`pandas.DataFrame`
        The next page of records as a ``pandas.DataFrame`` record batch.
    """
    bq_schema = schema._to_schema_fields(bq_schema)
    column_names = [field.name for field in bq_schema]
    for page in pages:
        yield _row_iterator_page_to_dataframe(page, column_names, dtypes)


def _bqstorage_page_to_arrow(page):
    return page.to_arrow()


def _bqstorage_page_to_dataframe(column_names, dtypes, page):
    # page.to_dataframe() does not preserve column order in some versions
    # of google-cloud-bigquery-storage. Access by column name to rearrange.
    return page.to_dataframe(dtypes=dtypes)[column_names]


def _download_table_bqstorage_stream(
    download_state, bqstorage_client, session, stream, worker_queue, page_to_item
):
    reader = bqstorage_client.read_rows(stream.name)

    # Avoid deprecation warnings for passing in unnecessary read session.
    # https://github.com/googleapis/python-bigquery-storage/issues/229
    if _versions_helpers.BQ_STORAGE_VERSIONS.is_read_session_optional:
        rowstream = reader.rows()
    else:
        rowstream = reader.rows(session)

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
    max_queue_size=_MAX_QUEUE_SIZE_DEFAULT,
):
    """Use (faster, but billable) BQ Storage API to construct DataFrame."""

    # Passing a BQ Storage client in implies that the BigQuery Storage library
    # is available and can be imported.
    from google.cloud import bigquery_storage

    if "$" in table.table_id:
        raise ValueError(
            "Reading from a specific partition is not currently supported."
        )
    if "@" in table.table_id:
        raise ValueError("Reading from a specific snapshot is not currently supported.")

    requested_streams = 1 if preserve_order else 0

    requested_session = bigquery_storage.types.ReadSession(
        table=table.to_bqstorage(), data_format=bigquery_storage.types.DataFormat.ARROW
    )
    if selected_fields is not None:
        for field in selected_fields:
            requested_session.read_options.selected_fields.append(field.name)

    if _ARROW_COMPRESSION_SUPPORT:
        requested_session.read_options.arrow_serialization_options.buffer_compression = (
            ArrowSerializationOptions.CompressionCodec.LZ4_FRAME
        )

    session = bqstorage_client.create_read_session(
        parent="projects/{}".format(project_id),
        read_session=requested_session,
        max_stream_count=requested_streams,
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
    #
    # The queue needs to be bounded by default, because if the user code processes the
    # fetched result pages too slowly, while at the same time new pages are rapidly being
    # fetched from the server, the queue can grow to the point where the process runs
    # out of memory.
    if max_queue_size is _MAX_QUEUE_SIZE_DEFAULT:
        max_queue_size = total_streams
    elif max_queue_size is None:
        max_queue_size = 0  # unbounded

    worker_queue = queue.Queue(maxsize=max_queue_size)

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
            while True:  # pragma: NO COVER
                try:
                    frame = worker_queue.get_nowait()
                    yield frame
                except queue.Empty:  # pragma: NO COVER
                    break
        finally:
            # No need for a lock because reading/replacing a variable is
            # defined to be an atomic operation in the Python language
            # definition (enforced by the global interpreter lock).
            download_state.done = True

            # Shutdown all background threads, now that they should know to
            # exit early.
            pool.shutdown(wait=True)


def download_arrow_bqstorage(
    project_id,
    table,
    bqstorage_client,
    preserve_order=False,
    selected_fields=None,
    max_queue_size=_MAX_QUEUE_SIZE_DEFAULT,
):
    return _download_table_bqstorage(
        project_id,
        table,
        bqstorage_client,
        preserve_order=preserve_order,
        selected_fields=selected_fields,
        page_to_item=_bqstorage_page_to_arrow,
        max_queue_size=max_queue_size,
    )


def download_dataframe_bqstorage(
    project_id,
    table,
    bqstorage_client,
    column_names,
    dtypes,
    preserve_order=False,
    selected_fields=None,
    max_queue_size=_MAX_QUEUE_SIZE_DEFAULT,
):
    page_to_item = functools.partial(_bqstorage_page_to_dataframe, column_names, dtypes)
    return _download_table_bqstorage(
        project_id,
        table,
        bqstorage_client,
        preserve_order=preserve_order,
        selected_fields=selected_fields,
        page_to_item=page_to_item,
        max_queue_size=max_queue_size,
    )


def dataframe_to_json_generator(dataframe):
    for row in dataframe.itertuples(index=False, name=None):
        output = {}
        for column, value in zip(dataframe.columns, row):
            # Omit NaN values.
            is_nan = pandas.isna(value)

            # isna() can also return an array-like of bools, but the latter's boolean
            # value is ambiguous, hence an extra check. An array-like value is *not*
            # considered a NaN, however.
            if isinstance(is_nan, bool) and is_nan:
                continue

            # Convert numpy types to corresponding Python types.
            # https://stackoverflow.com/a/60441783/101923
            if isinstance(value, numpy.bool_):
                value = bool(value)
            elif isinstance(
                value,
                (
                    numpy.int64,
                    numpy.int32,
                    numpy.int16,
                    numpy.int8,
                    numpy.uint64,
                    numpy.uint32,
                    numpy.uint16,
                    numpy.uint8,
                ),
            ):
                value = int(value)
            output[column] = value

        yield output


def verify_pandas_imports():
    if pandas is None:
        raise ValueError(_NO_PANDAS_ERROR) from pandas_import_exception
    if db_dtypes is None:
        raise ValueError(_NO_DB_TYPES_ERROR) from db_dtypes_import_exception
