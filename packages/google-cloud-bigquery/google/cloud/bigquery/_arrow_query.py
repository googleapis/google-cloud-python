# Copyright 2026 Google LLC
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

"""Read query results returned in Apache Arrow format."""

from __future__ import annotations

import base64
from typing import Dict, Iterator, Optional, TYPE_CHECKING

from google.cloud.bigquery import _versions_helpers
from google.cloud.bigquery import enums
from google.cloud.bigquery import exceptions

try:
    import pyarrow  # type: ignore
except ImportError:
    pyarrow = None  # type: ignore[assignment]

if TYPE_CHECKING:  # pragma: NO COVER
    from google.cloud import bigquery_storage
    from google.cloud.bigquery import job
    from google.cloud.bigquery.table import RowIterator

_NO_PYARROW_ERROR = (
    "The pyarrow library is not installed, please install "
    "pyarrow to use the to_arrow() function."
)


def validate_query(
    query_results_format: Optional[str],
    job_config: Optional["job.QueryJobConfig"],
    *,
    compression_codec: Optional[str] = None,
) -> None:
    """Raise before sending a query whose ``ARROW`` results can't be read.

    Args:
        query_results_format: The ``query_results_format`` passed to
            ``query_and_wait()``.
        job_config: The job config, already merged with
            ``Client.default_query_job_config``.
        compression_codec: The ``compression_codec`` passed to
            ``query_and_wait()``.

    Raises:
        ValueError:
            If ``compression_codec`` is set without ``ARROW``, or if an
            ``ARROW`` query uses ``WRITE_APPEND``.
        google.cloud.bigquery.exceptions.BigQueryError:
            If pyarrow or google-cloud-bigquery-storage is missing or too old
            to read ``ARROW`` results.
    """
    if query_results_format != enums.QueryResultsFormat.ARROW:
        if compression_codec is not None:
            raise ValueError("compression_codec requires query_results_format=ARROW.")
        return

    # Results that don't fit in the jobs.query response are read from the
    # destination table, which with WRITE_APPEND also holds older rows.
    if (
        job_config is not None
        and job_config.write_disposition == enums.WriteDisposition.WRITE_APPEND
    ):
        raise ValueError(
            "query_results_format=ARROW doesn't support WRITE_APPEND, because "
            "the results would also include the rows already in the "
            "destination table."
        )

    # Check before the query runs, so a query doesn't succeed while its
    # results fit in the first page and then fail once they need a stream.
    _check_dependencies()


def _check_dependencies() -> None:
    """Raise if pyarrow or google-cloud-bigquery-storage can't read ``ARROW``
    results."""
    _versions_helpers.PYARROW_VERSIONS.try_import(raise_if_error=True)
    _versions_helpers.BQ_STORAGE_VERSIONS.try_import(raise_if_error=True)
    if not _versions_helpers.BQ_STORAGE_VERSIONS.supports_arrow_serialization_options:
        raise exceptions.LegacyBigQueryStorageError(
            "query_results_format=ARROW needs a google-cloud-bigquery-storage "
            "release whose BigQueryReadClient.read_rows() accepts "
            "arrow_serialization_options, please upgrade it "
            "(`pip install --upgrade google-cloud-bigquery-storage`) "
            "(version found: "
            f"{_versions_helpers.BQ_STORAGE_VERSIONS.installed_version})."
        )


def serialization_options(compression_codec: Optional[str]) -> Dict[str, str]:
    """Build the ``arrowSerializationOptions`` sent on ``jobs.query``.

    ``ReadRows`` gets the same options. Options the caller didn't set are sent
    with their defaults, so every batch uses one encoding, whatever each
    endpoint would default to.
    """
    return {
        "bufferCompression": getattr(compression_codec, "value", compression_codec)
        or "COMPRESSION_UNSPECIFIED",
        "picosTimestampPrecision": "TIMESTAMP_PRECISION_MICROS",
    }


def _read_rows_options(options: Optional[Dict[str, str]]) -> Dict[str, str]:
    """Convert ``jobs.query`` ``arrowSerializationOptions`` to the
    ``ArrowSerializationOptions`` fields that ``ReadRows`` takes."""
    options = options or serialization_options(None)
    return {
        "buffer_compression": options["bufferCompression"],
        "picos_timestamp_precision": options["picosTimestampPrecision"],
    }


def download_arrow_from_job(
    row_iterator: "RowIterator",
    bqstorage_client: Optional["bigquery_storage.BigQueryReadClient"] = None,
    timeout: Optional[float] = None,
) -> Iterator["pyarrow.RecordBatch"]:
    """Yield Arrow record batches for ``row_iterator``'s ARROW query results.

    See :meth:`google.cloud.bigquery.table.RowIterator._download_arrow_from_job_id`.
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
                "The google-cloud-bigquery-storage library is required to read Arrow results."
            )

    offset = 0
    pa_schema = None
    total_rows = row_iterator.total_rows
    job_complete = False

    # Step 2: Process initial inline Arrow response from jobs.query if available.
    if row_iterator._first_page_response:
        first_page = row_iterator._first_page_response
        row_iterator._first_page_response = None

        job_complete = bool(first_page.get("jobComplete", False))
        if job_complete:
            total_rows = int(first_page.get("totalRows", 0))

        arrow_schema_json = first_page.get("arrowSchema")
        if isinstance(arrow_schema_json, dict):
            schema_bytes = arrow_schema_json.get("serializedSchema")
            if schema_bytes:
                if isinstance(schema_bytes, str):
                    schema_bytes = base64.b64decode(schema_bytes)
                pa_schema = pyarrow.ipc.read_schema(pyarrow.py_buffer(schema_bytes))

        arrow_batch_json = first_page.get("arrowRecordBatch")
        if isinstance(arrow_batch_json, dict) and pa_schema is not None:
            batch_bytes = arrow_batch_json.get("serializedRecordBatch")
            if batch_bytes:
                if isinstance(batch_bytes, str):
                    batch_bytes = base64.b64decode(batch_bytes)
                batch = pyarrow.ipc.read_record_batch(
                    pyarrow.py_buffer(batch_bytes),
                    pa_schema,
                )
                offset += batch.num_rows
                yield batch

    # Step 3: Return early if all results were delivered in the first page response.
    if job_complete and offset >= total_rows:
        return

    # Step 4: Stream remaining Arrow record batches from the job default stream.
    project = row_iterator._project or (
        row_iterator.client.project if row_iterator.client else None
    )
    location = row_iterator._location or (
        row_iterator.client.location if row_iterator.client else None
    )
    stream_name = f"projects/{project}/locations/{location}/jobs/{row_iterator._job_id}/streams/_default"
    reader = bqstorage_client.read_rows(
        stream_name,
        offset=offset,
        timeout=timeout,
        arrow_serialization_options=_read_rows_options(
            row_iterator._arrow_serialization_options
        ),
    )
    for response in reader:
        if (
            response.arrow_schema
            and response.arrow_schema.serialized_schema
            and pa_schema is None
        ):
            pa_schema = pyarrow.ipc.read_schema(
                pyarrow.py_buffer(response.arrow_schema.serialized_schema)
            )
        if (
            response.arrow_record_batch
            and response.arrow_record_batch.serialized_record_batch
            and pa_schema is not None
        ):
            batch = pyarrow.ipc.read_record_batch(
                pyarrow.py_buffer(response.arrow_record_batch.serialized_record_batch),
                pa_schema,
            )
            yield batch
