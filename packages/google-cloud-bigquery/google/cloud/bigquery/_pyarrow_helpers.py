# Copyright 2023 Google LLC
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

"""Shared helper functions for connecting BigQuery and pyarrow.

NOTE: This module is DEPRECATED. Please make updates in the pandas-gbq package,
instead. See: go/pandas-gbq-and-bigframes-redundancy,
https://github.com/googleapis/python-bigquery-pandas/blob/main/pandas_gbq/schema/bigquery_to_pyarrow.py
and
https://github.com/googleapis/python-bigquery-pandas/blob/main/pandas_gbq/schema/pyarrow_to_bigquery.py
"""

from __future__ import annotations

import base64
from typing import Any, Dict, Iterator, Optional, TYPE_CHECKING, Union

from google.cloud.bigquery import _versions_helpers
from google.cloud.bigquery import enums
from google.cloud.bigquery import exceptions

if TYPE_CHECKING:  # pragma: NO COVER
    from google.cloud import bigquery_storage
    from google.cloud.bigquery import job
    from google.cloud.bigquery.table import RowIterator

try:
    import pyarrow  # type: ignore
except ImportError:
    pyarrow = None  # type: ignore[assignment]

try:
    import db_dtypes  # type: ignore

    db_dtypes_import_exception = None
except ImportError as exc:
    db_dtypes = None
    db_dtypes_import_exception = exc


def pyarrow_datetime():
    return pyarrow.timestamp("us", tz=None)


def pyarrow_numeric():
    return pyarrow.decimal128(38, 9)


def pyarrow_bignumeric():
    # 77th digit is partial.
    # https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#decimal_types
    return pyarrow.decimal256(76, 38)


def pyarrow_time():
    return pyarrow.time64("us")


def pyarrow_timestamp():
    return pyarrow.timestamp("us", tz="UTC")


_BQ_TO_ARROW_SCALARS = {}
_ARROW_SCALAR_IDS_TO_BQ = {}

if pyarrow:
    # This dictionary is duplicated in bigquery_storage/test/unite/test_reader.py
    # When modifying it be sure to update it there as well.
    # Note(todo!!): type "BIGNUMERIC"'s matching pyarrow type is added in _pandas_helpers.py
    _BQ_TO_ARROW_SCALARS = {
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
        # Normally, we'd prefer JSON type built-in to pyarrow (added in 19.0.0),
        # but we'd like this to map as closely to the BQ Storage API as
        # possible, which uses the string() dtype, as JSON support in Arrow
        # predates JSON support in BigQuery by several years.
        "JSON": pyarrow.string,
        "NUMERIC": pyarrow_numeric,
        "STRING": pyarrow.string,
        "TIME": pyarrow_time,
        "TIMESTAMP": pyarrow_timestamp,
    }

    # DEPRECATED: update pandas_gbq.schema.pyarrow_to_bigquery, instead.
    _ARROW_SCALAR_IDS_TO_BQ = {
        # https://arrow.apache.org/docs/python/api/datatypes.html#type-classes
        pyarrow.bool_().id: "BOOL",
        pyarrow.int8().id: "INT64",
        pyarrow.int16().id: "INT64",
        pyarrow.int32().id: "INT64",
        pyarrow.int64().id: "INT64",
        pyarrow.uint8().id: "INT64",
        pyarrow.uint16().id: "INT64",
        pyarrow.uint32().id: "INT64",
        pyarrow.uint64().id: "INT64",
        pyarrow.float16().id: "FLOAT64",
        pyarrow.float32().id: "FLOAT64",
        pyarrow.float64().id: "FLOAT64",
        pyarrow.time32("ms").id: "TIME",
        pyarrow.time64("ns").id: "TIME",
        pyarrow.timestamp("ns").id: "TIMESTAMP",
        pyarrow.date32().id: "DATE",
        pyarrow.date64().id: "DATETIME",  # because millisecond resolution
        pyarrow.binary().id: "BYTES",
        pyarrow.string().id: "STRING",  # also alias for pyarrow.utf8()
        pyarrow.large_string().id: "STRING",
        # The exact scale and precision don't matter, see below.
        pyarrow.decimal128(38, scale=9).id: "NUMERIC",
        # NOTE: all extension types (e.g. json_, uuid, db_dtypes.JSONArrowType)
        # have the same id (31 as of version 19.0.1), so these should not be
        # matched by id.
    }

    _BQ_TO_ARROW_SCALARS["BIGNUMERIC"] = pyarrow_bignumeric
    # The exact decimal's scale and precision are not important, as only
    # the type ID matters, and it's the same for all decimal256 instances.
    _ARROW_SCALAR_IDS_TO_BQ[pyarrow.decimal256(76, scale=38).id] = "BIGNUMERIC"


def bq_to_arrow_scalars(bq_scalar: str):
    """
    DEPRECATED: update pandas_gbq.schema.bigquery_to_pyarrow, instead, which is
    to be added in https://github.com/googleapis/python-bigquery-pandas/pull/893.

    Returns:
        The Arrow scalar type that the input BigQuery scalar type maps to.
        If it cannot find the BigQuery scalar, return None.
    """
    return _BQ_TO_ARROW_SCALARS.get(bq_scalar)


def arrow_scalar_ids_to_bq(arrow_scalar: Any):
    """
    DEPRECATED: update pandas_gbq.schema.pyarrow_to_bigquery, instead.

    Returns:
        The BigQuery scalar type that the input arrow scalar type maps to.
        If it cannot find the arrow scalar, return None.
    """
    return _ARROW_SCALAR_IDS_TO_BQ.get(arrow_scalar)


def _validate_arrow_query(
    query_results_format: Optional[str],
    compression_codec: Optional[str],
    job_config: Optional["job.QueryJobConfig"],
) -> None:
    """Raise before sending a query whose ARROW results can't be returned."""
    if query_results_format != enums.QueryResultsFormat.ARROW:
        if compression_codec is not None:
            raise ValueError("compression_codec requires query_results_format=ARROW.")
        return

    if (
        job_config is not None
        and job_config.write_disposition == enums.WriteDisposition.WRITE_APPEND
    ):
        raise ValueError(
            "query_results_format=ARROW doesn't support WRITE_APPEND, because "
            "the results would also include the rows already in the "
            "destination table."
        )

    _check_arrow_dependencies()


def _check_arrow_dependencies() -> None:
    """Raise if pyarrow or google-cloud-bigquery-storage can't read ARROW results."""
    _versions_helpers.PYARROW_VERSIONS.try_import(raise_if_error=True)
    _versions_helpers.BQ_STORAGE_VERSIONS.try_import(raise_if_error=True)
    if not _versions_helpers.BQ_STORAGE_VERSIONS.supports_arrow_serialization_options:
        raise exceptions.LegacyBigQueryStorageError(
            "Dependency google-cloud-bigquery-storage is outdated, please "
            "upgrade it to version >= "
            f"{_versions_helpers._BQ_STORAGE_ARROW_OPTIONS_VERSION} "
            "(`pip install --upgrade google-cloud-bigquery-storage`) "
            "(version found: "
            f"{_versions_helpers.BQ_STORAGE_VERSIONS.installed_version})."
        )


def _to_rest_arrow_options(
    compression_codec: Optional[str],
) -> Dict[str, str]:
    """Build the ``jobs.query`` ``arrowSerializationOptions`` dict.

    Send the same options on ``jobs.query`` and ``ReadRows``, including the
    defaults, so every batch in the result uses one encoding.
    """
    return {
        "bufferCompression": getattr(compression_codec, "value", compression_codec)
        or "COMPRESSION_UNSPECIFIED",
        "picosTimestampPrecision": "TIMESTAMP_PRECISION_MICROS",
    }


def _to_read_api_arrow_options(
    options: Optional[Dict[str, str]],
) -> Dict[str, str]:
    """Convert ``jobs.query`` ``arrowSerializationOptions`` to the BigQuery
    Storage ``ArrowSerializationOptions`` fields, filling in the defaults.
    """
    options = options or {}
    return {
        "buffer_compression": options.get(
            "bufferCompression", "COMPRESSION_UNSPECIFIED"
        ),
        "picos_timestamp_precision": options.get(
            "picosTimestampPrecision", "TIMESTAMP_PRECISION_MICROS"
        ),
    }


def _deserialize_arrow_schema(
    schema_bytes: Union[bytes, str],
) -> "pyarrow.Schema":
    """Deserialize an Arrow IPC schema from bytes or base64-encoded string."""
    if isinstance(schema_bytes, str):
        schema_bytes = base64.b64decode(schema_bytes)
    return pyarrow.ipc.read_schema(pyarrow.py_buffer(schema_bytes))


def _deserialize_arrow_batch(
    batch_bytes: Union[bytes, str],
    schema: "pyarrow.Schema",
) -> "pyarrow.RecordBatch":
    """Deserialize an Arrow IPC record batch from bytes or base64-encoded string."""
    if isinstance(batch_bytes, str):
        batch_bytes = base64.b64decode(batch_bytes)
    return pyarrow.ipc.read_record_batch(pyarrow.py_buffer(batch_bytes), schema)


def _open_arrow_read_stream(
    row_iterator: "RowIterator",
    bqstorage_client: Optional["bigquery_storage.BigQueryReadClient"],
    offset: int,
    timeout: Optional[float],
) -> Any:
    """Open a BigQuery Storage Read API stream for remaining Arrow rows."""
    if bqstorage_client is None:
        if row_iterator.client is None:
            raise ValueError("RowIterator client is None.")
        bqstorage_client = row_iterator.client._ensure_bqstorage_client()
        if bqstorage_client is None:
            raise ValueError(
                "The google-cloud-bigquery-storage library is required to read "
                "Arrow results (`pip install google-cloud-bigquery-storage`)."
            )

    read_options = _to_read_api_arrow_options(row_iterator._arrow_serialization_options)
    project = row_iterator._project or (
        row_iterator.client.project if row_iterator.client else None
    )
    location = row_iterator._location or (
        row_iterator.client.location if row_iterator.client else None
    )
    stream_name = f"projects/{project}/locations/{location}/jobs/{row_iterator._job_id}/streams/_default"
    return bqstorage_client.read_rows(
        stream_name,
        offset=offset,
        timeout=timeout,
        arrow_serialization_options=read_options,
    )


_NO_PYARROW_ERROR = (
    "The pyarrow library is not installed, please install "
    "pyarrow to use the to_arrow() function."
)


def download_arrow_from_job(
    row_iterator: "RowIterator",
    bqstorage_client: Optional["bigquery_storage.BigQueryReadClient"] = None,
    timeout: Optional[float] = None,
) -> Iterator["pyarrow.RecordBatch"]:
    """Yield Arrow record batches for query results formatted as ARROW.

    First processes inline Arrow data in the initial page response (if present),
    updating row offset and total row counts. If more rows remain, streams
    remaining batches using the BigQuery Read API.
    """
    if pyarrow is None:
        raise ValueError(_NO_PYARROW_ERROR)

    # Step 1: Ensure BigQuery Read API client is available upfront.
    if bqstorage_client is None:
        if row_iterator.client is None:
            raise ValueError("RowIterator client is None.")
        bqstorage_client = row_iterator.client._ensure_bqstorage_client()
        if bqstorage_client is None:
            raise ValueError(
                "The google-cloud-bigquery-storage library is required to read "
                "Arrow results (`pip install google-cloud-bigquery-storage`)."
            )

    offset = 0
    pa_schema: Optional["pyarrow.Schema"] = None
    total_rows = row_iterator.total_rows
    job_complete = False

    # Step 2: Process initial inline Arrow response from jobs.query if available.
    if row_iterator._first_page_response:
        first_page = row_iterator._first_page_response
        row_iterator._first_page_response = None

        job_complete = bool(first_page.get("jobComplete", False))
        if job_complete:
            total_rows = int(first_page.get("totalRows", 0))

        schema_bytes = (first_page.get("arrowSchema") or {}).get("serializedSchema")
        if schema_bytes:
            pa_schema = _deserialize_arrow_schema(schema_bytes)

        batch_bytes = (first_page.get("arrowRecordBatch") or {}).get(
            "serializedRecordBatch"
        )
        if batch_bytes and pa_schema is not None:
            batch = _deserialize_arrow_batch(batch_bytes, pa_schema)
            offset += batch.num_rows
            yield batch

    # Step 3: Return early if all results were delivered in the first page response.
    if job_complete and offset >= total_rows:
        return

    # Step 4: Stream remaining Arrow record batches from the job default stream.
    reader = _open_arrow_read_stream(
        row_iterator, bqstorage_client, offset, timeout
    )
    for response in reader:
        if (
            response.arrow_schema
            and response.arrow_schema.serialized_schema
            and pa_schema is None
        ):
            pa_schema = _deserialize_arrow_schema(
                response.arrow_schema.serialized_schema
            )
        if (
            response.arrow_record_batch
            and response.arrow_record_batch.serialized_record_batch
            and pa_schema is not None
        ):
            yield _deserialize_arrow_batch(
                response.arrow_record_batch.serialized_record_batch,
                pa_schema,
            )
