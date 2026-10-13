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
from typing import Iterator, Optional, TYPE_CHECKING

try:
    import pyarrow  # type: ignore
except ImportError:
    pyarrow = None  # type: ignore[assignment]

if TYPE_CHECKING:  # pragma: NO COVER
    from google.cloud import bigquery_storage
    from google.cloud.bigquery.table import RowIterator

_NO_PYARROW_ERROR = (
    "The pyarrow library is not installed, please install "
    "pyarrow to use the to_arrow() function."
)


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
    reader = bqstorage_client.read_rows(stream_name, offset=offset, timeout=timeout)
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
