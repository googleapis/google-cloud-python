# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import unittest
from unittest import mock

import packaging.version
import pytest

from google.cloud.bigquery import _arrow_query
from google.cloud.bigquery import _job_helpers
from google.cloud.bigquery import _versions_helpers
from google.cloud.bigquery import exceptions
from google.cloud.bigquery.client import Client
from google.cloud.bigquery.enums import QueryResultsCompressionCodec
from google.cloud.bigquery.enums import TimestampPrecision
from google.cloud.bigquery.enums import WriteDisposition
from google.cloud.bigquery.job import QueryJobConfig
from google.cloud.bigquery.table import RowIterator, _EmptyRowIterator

from .helpers import make_client

# The Arrow serialization options that jobs.query and ReadRows get when the
# caller sets none.
_DEFAULT_QUERY_OPTIONS = {
    "bufferCompression": "COMPRESSION_UNSPECIFIED",
    "picosTimestampPrecision": "TIMESTAMP_PRECISION_MICROS",
}
_DEFAULT_READ_OPTIONS = {
    "buffer_compression": "COMPRESSION_UNSPECIFIED",
    "picos_timestamp_precision": "TIMESTAMP_PRECISION_MICROS",
}

# The real check, saved before the autouse fixture below replaces it.
_check_dependencies = _arrow_query._check_dependencies


@pytest.fixture(autouse=True)
def check_dependencies():
    """Skip the ARROW dependency check, which depends on installed packages."""
    with mock.patch.object(_arrow_query, "_check_dependencies") as check:
        yield check


class TestQueryResultsFormatOption1(unittest.TestCase):
    def test_supported_by_jobs_query_includes_query_results_format(self):
        body = {"query": "SELECT 1", "queryResultsFormat": "ARROW"}
        self.assertTrue(_job_helpers._supported_by_jobs_query(body))

    def test_job_helpers_query_and_wait_sets_request_body(self):
        client = mock.MagicMock(spec=Client)
        client._call_api.return_value = {
            "jobReference": {"projectId": "p", "jobId": "j", "location": "us"},
            "jobComplete": True,
            "rows": [],
            "schema": {"fields": []},
        }

        row_iterator = _job_helpers.query_and_wait(
            client=client,
            query="SELECT 1",
            project="p",
            location="us",
            job_config=None,
            retry=None,
            job_retry=None,
            query_results_format="ARROW",
        )

        self.assertEqual(row_iterator._query_results_format, "ARROW")
        call_args = client._call_api.call_args
        self.assertIn("queryResultsFormat", call_args.kwargs["data"])
        self.assertEqual(call_args.kwargs["data"]["queryResultsFormat"], "ARROW")

    def test_job_helpers_query_and_wait_sets_compression_codec(self):
        client = mock.MagicMock(spec=Client)
        client._call_api.return_value = {
            "jobReference": {"projectId": "p", "jobId": "j", "location": "us"},
            "jobComplete": True,
            "rows": [],
            "schema": {"fields": []},
        }

        _job_helpers.query_and_wait(
            client=client,
            query="SELECT 1",
            project="p",
            location="us",
            job_config=None,
            retry=None,
            job_retry=None,
            query_results_format="ARROW",
            compression_codec="LZ4_FRAME",
        )

        call_args = client._call_api.call_args
        self.assertNotIn(
            "arrowSerializationOptions", call_args.kwargs["data"]["formatOptions"]
        )
        self.assertEqual(
            call_args.kwargs["data"]["arrowSerializationOptions"],
            {
                "bufferCompression": "LZ4_FRAME",
                "picosTimestampPrecision": "TIMESTAMP_PRECISION_MICROS",
            },
        )

    def test_job_helpers_query_and_wait_fallback_preserves_query_results_format(self):
        client = mock.MagicMock(spec=Client)
        unsupported_body = {"unsupportedKey": "val"}
        job_mock = mock.MagicMock()
        fake_iterator = mock.MagicMock(spec=RowIterator)
        job_mock.result.return_value = fake_iterator

        with mock.patch.object(
            _job_helpers, "_to_query_request", return_value=unsupported_body
        ), mock.patch.object(_job_helpers, "query_jobs_insert", return_value=job_mock):
            res_iterator = _job_helpers.query_and_wait(
                client=client,
                query="SELECT 1",
                project="p",
                location="us",
                job_config=None,
                retry=None,
                job_retry=None,
                query_results_format="ARROW",
            )
            self.assertEqual(res_iterator._query_results_format, "ARROW")

    def test_row_iterator_non_arrow_iteration_raises_value_error(self):
        iterator = RowIterator(
            client=mock.MagicMock(),
            api_request=mock.MagicMock(),
            path=None,
            schema=(),
            query_results_format="ARROW",
        )

        with self.assertRaises(ValueError) as ctx:
            iter(iterator)
        self.assertIn("Cannot iterate over non-arrow results", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            next(iterator)
        self.assertIn("Cannot iterate over non-arrow results", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            _ = iterator.pages
        self.assertIn("Cannot iterate over non-arrow results", str(ctx.exception))

    def test_empty_row_iterator_non_arrow_iteration_raises_value_error(self):
        iterator = _EmptyRowIterator(query_results_format="ARROW")

        with self.assertRaises(ValueError) as ctx:
            iter(iterator)
        self.assertIn("Cannot iterate over non-arrow results", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            next(iterator)
        self.assertIn("Cannot iterate over non-arrow results", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            _ = iterator.pages
        self.assertIn("Cannot iterate over non-arrow results", str(ctx.exception))

    def test_row_iterator_standard_format_allows_iteration(self):
        iterator = RowIterator(
            client=mock.MagicMock(),
            api_request=mock.MagicMock(),
            path=None,
            schema=(),
            query_results_format=None,
        )
        self.assertIsNotNone(iterator.pages)

    def test_row_iterator_to_arrow_iterable_delegates_when_format_is_arrow(self):
        iterator = RowIterator(
            client=mock.MagicMock(),
            api_request=mock.MagicMock(),
            path=None,
            schema=(),
            project="proj",
            location="loc",
            job_id="job123",
            query_results_format="ARROW",
        )

        with mock.patch.object(
            iterator,
            "_download_arrow_from_job_id",
            return_value=iter(["batch1", "batch2"]),
        ) as mock_download:
            res = list(iterator.to_arrow_iterable(timeout=10.0))
            self.assertEqual(res, ["batch1", "batch2"])
            mock_download.assert_called_once_with(bqstorage_client=None, timeout=10.0)

    def test_download_arrow_from_job_id_constructs_stream_and_reads(self):
        mock_client = mock.MagicMock()
        mock_bqstorage = mock.MagicMock()
        mock_client._ensure_bqstorage_client.return_value = mock_bqstorage

        iterator = RowIterator(
            client=mock_client,
            api_request=mock.MagicMock(),
            path=None,
            schema=(),
            project="test-proj",
            location="US",
            job_id="test-job-456",
            query_results_format="ARROW",
        )

        mock_response = mock.MagicMock()
        mock_response.arrow_schema = None
        mock_response.arrow_record_batch = None
        mock_bqstorage.read_rows.return_value = [mock_response]

        with mock.patch("google.cloud.bigquery._arrow_query.pyarrow") as mock_pyarrow:
            mock_pyarrow.py_buffer = lambda x: x
            batches = list(iterator._download_arrow_from_job_id(timeout=5.0))
            self.assertEqual(batches, [])

            expected_stream_name = (
                "projects/test-proj/locations/US/jobs/test-job-456/streams/_default"
            )
            mock_bqstorage.read_rows.assert_called_once_with(
                expected_stream_name,
                offset=0,
                timeout=5.0,
                arrow_serialization_options=_DEFAULT_READ_OPTIONS,
            )

    def test_download_arrow_from_job_id_with_first_page_response(self):
        mock_client = mock.MagicMock()
        mock_bqstorage = mock.MagicMock()
        mock_client._ensure_bqstorage_client.return_value = mock_bqstorage

        raw_schema_bytes = b"schema_bytes_123"
        raw_batch_bytes = b"batch_bytes_123"
        b64_schema = base64.b64encode(raw_schema_bytes).decode("ascii")
        b64_batch = base64.b64encode(raw_batch_bytes).decode("ascii")

        first_page_response = {
            "arrowSchema": {"serializedSchema": b64_schema},
            "arrowRecordBatch": {"serializedRecordBatch": b64_batch},
        }

        iterator = RowIterator(
            client=mock_client,
            api_request=mock.MagicMock(),
            path=None,
            schema=(),
            project="test-proj",
            location="US",
            job_id="test-job-sync",
            query_results_format="ARROW",
            first_page_response=first_page_response,
        )

        mock_first_batch = mock.MagicMock()
        mock_first_batch.num_rows = 10

        mock_second_batch = mock.MagicMock()
        mock_second_batch.num_rows = 5

        # Subsequent ReadRows response chunk without arrow_schema
        mock_response = mock.MagicMock()
        mock_response.arrow_schema = None
        mock_batch_msg = mock.MagicMock()
        mock_batch_msg.serialized_record_batch = b"stream_batch_bytes"
        mock_response.arrow_record_batch = mock_batch_msg

        mock_bqstorage.read_rows.return_value = [mock_response]

        with mock.patch("google.cloud.bigquery._arrow_query.pyarrow") as mock_pyarrow:
            mock_pyarrow.py_buffer = lambda x: x
            mock_pyarrow.ipc.read_schema.return_value = "deserialized_schema"
            mock_pyarrow.ipc.read_record_batch.side_effect = [
                mock_first_batch,
                mock_second_batch,
            ]

            batches = list(iterator._download_arrow_from_job_id(timeout=5.0))

            self.assertEqual(batches, [mock_first_batch, mock_second_batch])
            self.assertIsNone(iterator._first_page_response)

            mock_pyarrow.ipc.read_schema.assert_called_once_with(raw_schema_bytes)
            mock_pyarrow.ipc.read_record_batch.assert_has_calls(
                [
                    mock.call(raw_batch_bytes, "deserialized_schema"),
                    mock.call(b"stream_batch_bytes", "deserialized_schema"),
                ]
            )

            expected_stream_name = (
                "projects/test-proj/locations/US/jobs/test-job-sync/streams/_default"
            )
            mock_bqstorage.read_rows.assert_called_once_with(
                expected_stream_name,
                offset=10,
                timeout=5.0,
                arrow_serialization_options=_DEFAULT_READ_OPTIONS,
            )

    def test_download_arrow_from_job_id_with_first_page_response_schema_only(self):
        mock_client = mock.MagicMock()
        mock_bqstorage = mock.MagicMock()
        mock_client._ensure_bqstorage_client.return_value = mock_bqstorage

        raw_schema_bytes = b"schema_bytes_456"
        first_page_response = {
            "arrowSchema": {"serializedSchema": raw_schema_bytes},
        }

        iterator = RowIterator(
            client=mock_client,
            api_request=mock.MagicMock(),
            path=None,
            schema=(),
            project="test-proj",
            location="US",
            job_id="test-job-schema-only",
            query_results_format="ARROW",
            first_page_response=first_page_response,
        )

        mock_stream_batch = mock.MagicMock()
        mock_response = mock.MagicMock()
        mock_response.arrow_schema = None
        mock_batch_msg = mock.MagicMock()
        mock_batch_msg.serialized_record_batch = b"stream_batch_bytes"
        mock_response.arrow_record_batch = mock_batch_msg

        mock_bqstorage.read_rows.return_value = [mock_response]

        with mock.patch("google.cloud.bigquery._arrow_query.pyarrow") as mock_pyarrow:
            mock_pyarrow.py_buffer = lambda x: x
            mock_pyarrow.ipc.read_schema.return_value = "deserialized_schema"
            mock_pyarrow.ipc.read_record_batch.return_value = mock_stream_batch

            batches = list(iterator._download_arrow_from_job_id(timeout=5.0))

            self.assertEqual(batches, [mock_stream_batch])
            self.assertIsNone(iterator._first_page_response)
            mock_pyarrow.ipc.read_schema.assert_called_once_with(raw_schema_bytes)
            mock_pyarrow.ipc.read_record_batch.assert_called_once_with(
                b"stream_batch_bytes", "deserialized_schema"
            )
            expected_stream_name = "projects/test-proj/locations/US/jobs/test-job-schema-only/streams/_default"
            mock_bqstorage.read_rows.assert_called_once_with(
                expected_stream_name,
                offset=0,
                timeout=5.0,
                arrow_serialization_options=_DEFAULT_READ_OPTIONS,
            )

    def test_download_arrow_from_job_id_missing_storage_client_raises_value_error(self):
        mock_client = mock.MagicMock()
        mock_client._ensure_bqstorage_client.return_value = None

        iterator = RowIterator(
            client=mock_client,
            api_request=mock.MagicMock(),
            path=None,
            schema=(),
            project="test-proj",
            location="US",
            job_id="test-job-456",
            query_results_format="ARROW",
        )

        with mock.patch("google.cloud.bigquery._arrow_query.pyarrow"):
            with self.assertRaises(ValueError) as ctx:
                list(iterator._download_arrow_from_job_id())
            self.assertIn(
                "The google-cloud-bigquery-storage library is required",
                str(ctx.exception),
            )

    def test_download_arrow_from_job_id_with_schema_and_batch(self):
        mock_client = mock.MagicMock()
        mock_bqstorage = mock.MagicMock()
        mock_client._ensure_bqstorage_client.return_value = mock_bqstorage

        iterator = RowIterator(
            client=mock_client,
            api_request=mock.MagicMock(),
            path=None,
            schema=(),
            project="test-proj",
            location="US",
            job_id="test-job-789",
            query_results_format="ARROW",
        )

        mock_schema_msg = mock.MagicMock()
        mock_schema_msg.serialized_schema = b"schema_bytes"
        mock_batch_msg = mock.MagicMock()
        mock_batch_msg.serialized_record_batch = b"batch_bytes"

        mock_response = mock.MagicMock()
        mock_response.arrow_schema = mock_schema_msg
        mock_response.arrow_record_batch = mock_batch_msg

        mock_bqstorage.read_rows.return_value = [mock_response]

        with mock.patch("google.cloud.bigquery._arrow_query.pyarrow") as mock_pyarrow:
            mock_pyarrow.py_buffer = lambda x: x
            mock_pyarrow.ipc.read_schema.return_value = "fake_schema"
            mock_pyarrow.ipc.read_record_batch.return_value = "fake_batch"

            batches = list(iterator._download_arrow_from_job_id(timeout=5.0))
            self.assertEqual(batches, ["fake_batch"])
            mock_pyarrow.ipc.read_schema.assert_called_once_with(b"schema_bytes")
            mock_pyarrow.ipc.read_record_batch.assert_called_once_with(
                b"batch_bytes", "fake_schema"
            )

    def test_empty_row_iterator_to_arrow_iterable_checks_pyarrow(self):
        iterator = _EmptyRowIterator(query_results_format="ARROW")
        with mock.patch("google.cloud.bigquery.table.pyarrow", None):
            with self.assertRaises(ValueError) as ctx:
                iterator.to_arrow_iterable()
            self.assertIn("pyarrow", str(ctx.exception).lower())

    def test_download_arrow_from_job_id_avoids_read_rows_when_all_rows_present(self):
        mock_client = mock.MagicMock()
        raw_schema_bytes = b"schema_bytes_789"
        raw_batch_bytes = b"batch_bytes_789"
        b64_schema = base64.b64encode(raw_schema_bytes).decode("ascii")
        b64_batch = base64.b64encode(raw_batch_bytes).decode("ascii")

        first_page_response = {
            "jobComplete": True,
            "totalRows": "10",
            "arrowSchema": {"serializedSchema": b64_schema},
            "arrowRecordBatch": {"serializedRecordBatch": b64_batch},
        }

        iterator = RowIterator(
            client=mock_client,
            api_request=mock.MagicMock(),
            path=None,
            schema=(),
            project="test-proj",
            location="US",
            job_id="test-job-complete",
            query_results_format="ARROW",
            first_page_response=first_page_response,
        )

        mock_first_batch = mock.MagicMock()
        mock_first_batch.num_rows = 10

        with mock.patch("google.cloud.bigquery._arrow_query.pyarrow") as mock_pyarrow:
            mock_pyarrow.py_buffer = lambda x: x
            mock_pyarrow.ipc.read_schema.return_value = "deserialized_schema"
            mock_pyarrow.ipc.read_record_batch.return_value = mock_first_batch

            batches = list(iterator._download_arrow_from_job_id(timeout=5.0))
            self.assertEqual(batches, [mock_first_batch])
            mock_client._ensure_bqstorage_client.assert_called_once()

    def test_download_arrow_from_job_id_calls_read_rows_when_job_not_complete(self):
        mock_client = mock.MagicMock()
        mock_bqstorage = mock.MagicMock()
        mock_client._ensure_bqstorage_client.return_value = mock_bqstorage

        raw_schema_bytes = b"schema_bytes_789"
        raw_batch_bytes = b"batch_bytes_789"
        b64_schema = base64.b64encode(raw_schema_bytes).decode("ascii")
        b64_batch = base64.b64encode(raw_batch_bytes).decode("ascii")

        first_page_response = {
            "jobComplete": False,
            "totalRows": "10",
            "arrowSchema": {"serializedSchema": b64_schema},
            "arrowRecordBatch": {"serializedRecordBatch": b64_batch},
        }

        iterator = RowIterator(
            client=mock_client,
            api_request=mock.MagicMock(),
            path=None,
            schema=(),
            project="test-proj",
            location="US",
            job_id="test-job-incomplete",
            query_results_format="ARROW",
            first_page_response=first_page_response,
        )

        mock_first_batch = mock.MagicMock()
        mock_first_batch.num_rows = 10
        mock_bqstorage.read_rows.return_value = []

        with mock.patch("google.cloud.bigquery._arrow_query.pyarrow") as mock_pyarrow:
            mock_pyarrow.py_buffer = lambda x: x
            mock_pyarrow.ipc.read_schema.return_value = "deserialized_schema"
            mock_pyarrow.ipc.read_record_batch.return_value = mock_first_batch

            batches = list(iterator._download_arrow_from_job_id(timeout=5.0))
            self.assertEqual(batches, [mock_first_batch])
            mock_client._ensure_bqstorage_client.assert_called_once()
            expected_stream = "projects/test-proj/locations/US/jobs/test-job-incomplete/streams/_default"
            mock_bqstorage.read_rows.assert_called_once_with(
                expected_stream,
                offset=10,
                timeout=5.0,
                arrow_serialization_options=_DEFAULT_READ_OPTIONS,
            )

    def test_enums_values(self):
        from google.cloud.bigquery.enums import (
            QueryResultsFormat,
            QueryResultsCompressionCodec,
        )

        self.assertEqual(QueryResultsFormat.ARROW, "ARROW")
        self.assertEqual(QueryResultsCompressionCodec.LZ4_FRAME, "LZ4_FRAME")
        self.assertEqual(QueryResultsCompressionCodec.ZSTD, "ZSTD")

    def test_job_helpers_query_and_wait_accepts_enums(self):
        from google.cloud.bigquery.enums import (
            QueryResultsFormat,
            QueryResultsCompressionCodec,
        )

        client = mock.MagicMock(spec=Client)
        client._call_api.return_value = {
            "jobReference": {"projectId": "p", "jobId": "j", "location": "us"},
            "jobComplete": True,
            "rows": [],
            "schema": {"fields": []},
        }

        row_iterator = _job_helpers.query_and_wait(
            client=client,
            query="SELECT 1",
            project="p",
            location="us",
            job_config=None,
            retry=None,
            job_retry=None,
            query_results_format=QueryResultsFormat.ARROW,
            compression_codec=QueryResultsCompressionCodec.LZ4_FRAME,
        )
        self.assertEqual(row_iterator._query_results_format, "ARROW")

        call_args = client._call_api.call_args
        self.assertEqual(call_args.kwargs["data"]["queryResultsFormat"], "ARROW")
        self.assertEqual(
            call_args.kwargs["data"]["arrowSerializationOptions"]["bufferCompression"],
            "LZ4_FRAME",
        )

    def test_row_iterator_to_dataframe_iterable_when_format_is_arrow(self):
        pytest.importorskip("pandas")
        mock_client = mock.MagicMock()
        mock_client._ensure_bqstorage_client.return_value = mock.MagicMock()

        iterator = RowIterator(
            client=mock_client,
            api_request=mock.MagicMock(),
            path=None,
            schema=(),
            query_results_format="ARROW",
        )

        mock_batch = mock.MagicMock()
        mock_batch.to_pandas.return_value = "df_chunk"

        with mock.patch.object(
            iterator, "to_arrow_iterable", return_value=[mock_batch]
        ):
            with mock.patch("google.cloud.bigquery.table._pandas_helpers"):
                dfs = list(iterator.to_dataframe_iterable())
                self.assertEqual(dfs, ["df_chunk"])

    def test_row_iterator_to_dataframe_when_format_is_arrow(self):
        pytest.importorskip("pandas")
        mock_client = mock.MagicMock()
        mock_client._ensure_bqstorage_client.return_value = mock.MagicMock()

        iterator = RowIterator(
            client=mock_client,
            api_request=mock.MagicMock(),
            path=None,
            schema=(),
            query_results_format="ARROW",
        )

        mock_table = mock.MagicMock()
        mock_table.__iter__.return_value = iter([])
        mock_table.to_pandas.return_value = "full_df"

        with mock.patch.object(iterator, "to_arrow", return_value=mock_table):
            with mock.patch("google.cloud.bigquery.table._pandas_helpers"):
                df = iterator.to_dataframe()
                self.assertEqual(df, "full_df")


def _query_and_wait(client, **kwargs):
    return _job_helpers.query_and_wait(
        client,
        "SELECT 1",
        project="p",
        location="us",
        retry=None,
        job_retry=None,
        **{"job_config": None, **kwargs},
    )


def test_query_and_wait_compression_codec_requires_arrow(check_dependencies):
    client = mock.MagicMock(spec=Client)

    with pytest.raises(ValueError, match="compression_codec requires"):
        _query_and_wait(client, compression_codec="LZ4_FRAME")

    client._call_api.assert_not_called()
    check_dependencies.assert_not_called()


def test_query_and_wait_without_arrow_skips_dependency_check(check_dependencies):
    client = mock.MagicMock(spec=Client)
    client._call_api.return_value = {
        "jobReference": {"projectId": "p", "jobId": "j", "location": "us"},
        "jobComplete": True,
        "rows": [],
        "schema": {"fields": []},
    }

    _query_and_wait(client)

    check_dependencies.assert_not_called()


def test_query_and_wait_arrow_rejects_write_append():
    client = mock.MagicMock(spec=Client)
    job_config = QueryJobConfig(write_disposition=WriteDisposition.WRITE_APPEND)

    with pytest.raises(ValueError, match="WRITE_APPEND"):
        _query_and_wait(client, job_config=job_config, query_results_format="ARROW")

    client._call_api.assert_not_called()


def test_query_and_wait_arrow_rejects_default_write_append():
    client = make_client(
        default_query_job_config=QueryJobConfig(
            destination="p.d.t", write_disposition=WriteDisposition.WRITE_APPEND
        )
    )
    client._call_api = mock.Mock()

    with pytest.raises(ValueError, match="WRITE_APPEND"):
        client.query_and_wait("SELECT 1", query_results_format="ARROW")

    client._call_api.assert_not_called()


@pytest.mark.parametrize(
    "write_disposition",
    [None, WriteDisposition.WRITE_TRUNCATE, WriteDisposition.WRITE_EMPTY],
)
def test_validate_query_allows_other_write_dispositions(
    check_dependencies, write_disposition
):
    job_config = QueryJobConfig(write_disposition=write_disposition)

    _arrow_query.validate_query("ARROW", job_config, compression_codec="ZSTD")

    check_dependencies.assert_called_once_with()


def test_query_and_wait_arrow_checks_dependencies_before_sending(check_dependencies):
    check_dependencies.side_effect = exceptions.BigQueryStorageNotFoundError("missing")
    client = mock.MagicMock(spec=Client)

    with pytest.raises(exceptions.BigQueryStorageNotFoundError):
        _query_and_wait(client, query_results_format="ARROW")

    client._call_api.assert_not_called()


def test_check_dependencies_requires_pyarrow():
    error = exceptions.LegacyPyarrowError("pyarrow is not installed")
    with mock.patch.object(
        _versions_helpers.PYARROW_VERSIONS, "try_import", side_effect=error
    ) as try_import:
        with pytest.raises(exceptions.LegacyPyarrowError):
            _check_dependencies()

    try_import.assert_called_once_with(raise_if_error=True)


def test_check_dependencies_requires_bigquery_storage():
    error = exceptions.BigQueryStorageNotFoundError("not installed")
    with (
        mock.patch.object(_versions_helpers.PYARROW_VERSIONS, "try_import"),
        mock.patch.object(
            _versions_helpers.BQ_STORAGE_VERSIONS, "try_import", side_effect=error
        ) as try_import,
    ):
        with pytest.raises(exceptions.BigQueryStorageNotFoundError):
            _check_dependencies()

    try_import.assert_called_once_with(raise_if_error=True)


@pytest.mark.parametrize("supported", [True, False])
def test_check_dependencies_requires_read_rows_arrow_options(supported):
    versions_type = type(_versions_helpers.BQ_STORAGE_VERSIONS)
    with (
        mock.patch.object(_versions_helpers.PYARROW_VERSIONS, "try_import"),
        mock.patch.object(_versions_helpers.BQ_STORAGE_VERSIONS, "try_import"),
        mock.patch.object(
            versions_type,
            "supports_arrow_serialization_options",
            new_callable=mock.PropertyMock,
            return_value=supported,
        ),
        mock.patch.object(
            versions_type,
            "installed_version",
            new_callable=mock.PropertyMock,
            return_value=packaging.version.Version("2.42.0"),
        ),
    ):
        if supported:
            _check_dependencies()
        else:
            with pytest.raises(
                exceptions.LegacyBigQueryStorageError,
                match=r"pip install --upgrade google-cloud-bigquery-storage.*"
                r"\(version found: 2\.42\.0\)",
            ):
                _check_dependencies()


def test_query_and_wait_arrow_sends_default_serialization_options():
    client = mock.MagicMock(spec=Client)
    client._call_api.return_value = {
        "jobReference": {"projectId": "p", "jobId": "j", "location": "us"},
        "jobComplete": True,
        "schema": {"fields": []},
    }

    row_iterator = _query_and_wait(client, query_results_format="ARROW")

    data = client._call_api.call_args.kwargs["data"]
    assert data["arrowSerializationOptions"] == _DEFAULT_QUERY_OPTIONS
    assert "arrowSerializationOptions" not in data["formatOptions"]
    assert row_iterator._arrow_serialization_options == _DEFAULT_QUERY_OPTIONS


def test_query_and_wait_without_arrow_sends_no_serialization_options():
    client = mock.MagicMock(spec=Client)
    client._call_api.return_value = {
        "jobReference": {"projectId": "p", "jobId": "j", "location": "us"},
        "jobComplete": True,
        "rows": [],
        "schema": {"fields": []},
    }

    row_iterator = _query_and_wait(client)

    assert "arrowSerializationOptions" not in client._call_api.call_args.kwargs["data"]
    assert row_iterator._arrow_serialization_options is None


def test_query_and_wait_arrow_waits_with_the_same_options():
    client = mock.MagicMock(spec=Client)
    client._call_api.return_value = {
        "jobReference": {"projectId": "p", "jobId": "j", "location": "us"},
        "jobComplete": False,
    }

    with (
        mock.patch.object(_job_helpers, "_to_query_job") as to_query_job,
        mock.patch.object(_job_helpers, "_wait_or_cancel") as wait_or_cancel,
    ):
        _query_and_wait(client, query_results_format="ARROW", compression_codec="ZSTD")

    wait_or_cancel.assert_called_once_with(
        to_query_job.return_value,
        api_timeout=mock.ANY,
        wait_timeout=mock.ANY,
        retry=mock.ANY,
        page_size=mock.ANY,
        max_results=mock.ANY,
        query_results_format="ARROW",
        arrow_serialization_options={
            "bufferCompression": "ZSTD",
            "picosTimestampPrecision": "TIMESTAMP_PRECISION_MICROS",
        },
        callback=mock.ANY,
    )


def test_wait_or_cancel_sets_arrow_serialization_options():
    job = mock.MagicMock(dry_run=False)
    job.result.return_value = RowIterator(
        client=mock.MagicMock(), api_request=mock.MagicMock(), path=None, schema=()
    )

    rows = _job_helpers._wait_or_cancel(
        job,
        api_timeout=None,
        wait_timeout=None,
        retry=None,
        page_size=None,
        max_results=None,
        query_results_format="ARROW",
        arrow_serialization_options=_DEFAULT_QUERY_OPTIONS,
    )

    assert rows._query_results_format == "ARROW"
    assert rows._arrow_serialization_options == _DEFAULT_QUERY_OPTIONS


def test_query_and_wait_arrow_jobs_insert_omits_arrow_fields():
    client = make_client()
    client._call_api = mock.Mock(
        return_value={
            "jobReference": {"projectId": "PROJECT", "jobId": "j", "location": "US"},
            "configuration": {"query": {"query": "SELECT 1"}},
            "status": {"state": "RUNNING"},
        }
    )
    # jobs.query doesn't accept a destination table, so this uses jobs.insert.
    job_config = QueryJobConfig(destination="PROJECT.dataset.table")

    with mock.patch.object(_job_helpers, "_wait_or_cancel") as wait_or_cancel:
        client.query_and_wait(
            "SELECT 1", job_config=job_config, query_results_format="ARROW"
        )

    (insert_call,) = client._call_api.call_args_list
    assert insert_call.kwargs["path"] == "/projects/PROJECT/jobs"
    query_config = insert_call.kwargs["data"]["configuration"]["query"]
    assert "queryResultsFormat" not in query_config
    assert "arrowSerializationOptions" not in query_config
    wait_or_cancel.assert_called_once_with(
        mock.ANY,
        api_timeout=mock.ANY,
        wait_timeout=mock.ANY,
        retry=mock.ANY,
        page_size=mock.ANY,
        max_results=mock.ANY,
        query_results_format="ARROW",
        arrow_serialization_options=_DEFAULT_QUERY_OPTIONS,
        callback=mock.ANY,
    )


def test_supported_by_jobs_query_includes_arrow_serialization_options():
    body = {
        "query": "SELECT 1",
        "queryResultsFormat": "ARROW",
        "arrowSerializationOptions": _DEFAULT_QUERY_OPTIONS,
    }

    assert _job_helpers._supported_by_jobs_query(body)


@pytest.mark.parametrize("codec", ["LZ4_FRAME", QueryResultsCompressionCodec.LZ4_FRAME])
def test_serialization_options_accepts_str_and_enum(codec):
    assert _arrow_query.serialization_options(codec) == {
        "bufferCompression": "LZ4_FRAME",
        "picosTimestampPrecision": "TIMESTAMP_PRECISION_MICROS",
    }


def test_read_rows_options():
    assert _arrow_query._read_rows_options(None) == _DEFAULT_READ_OPTIONS
    assert _arrow_query._read_rows_options(
        {
            "bufferCompression": "ZSTD",
            "picosTimestampPrecision": "TIMESTAMP_PRECISION_PICOS",
        }
    ) == {
        "buffer_compression": "ZSTD",
        "picos_timestamp_precision": "TIMESTAMP_PRECISION_PICOS",
    }


def test_download_arrow_from_job_id_sends_query_options_on_read_rows():
    bqstorage_client = mock.MagicMock()
    bqstorage_client.read_rows.return_value = []
    iterator = RowIterator(
        client=mock.MagicMock(),
        api_request=mock.MagicMock(),
        path=None,
        schema=(),
        project="p",
        location="US",
        job_id="j",
        query_results_format="ARROW",
        arrow_serialization_options={
            "bufferCompression": "LZ4_FRAME",
            "picosTimestampPrecision": "TIMESTAMP_PRECISION_MICROS",
        },
    )

    with mock.patch("google.cloud.bigquery._arrow_query.pyarrow"):
        list(iterator._download_arrow_from_job_id(bqstorage_client=bqstorage_client))

    bqstorage_client.read_rows.assert_called_once_with(
        "projects/p/locations/US/jobs/j/streams/_default",
        offset=0,
        timeout=None,
        arrow_serialization_options={
            "buffer_compression": "LZ4_FRAME",
            "picos_timestamp_precision": "TIMESTAMP_PRECISION_MICROS",
        },
    )


@pytest.mark.parametrize(
    "timestamp_precision",
    [TimestampPrecision.MICROSECOND, TimestampPrecision.PICOSECOND],
)
def test_query_and_wait_timestamp_precision_requires_arrow(
    check_dependencies, timestamp_precision
):
    client = mock.MagicMock(spec=Client)

    with pytest.raises(ValueError, match="timestamp_precision requires"):
        _query_and_wait(client, timestamp_precision=timestamp_precision)

    client._call_api.assert_not_called()
    check_dependencies.assert_not_called()


@pytest.mark.parametrize(
    ("timestamp_precision", "expected"),
    [
        (None, "TIMESTAMP_PRECISION_MICROS"),
        (TimestampPrecision.MICROSECOND, "TIMESTAMP_PRECISION_MICROS"),
        (TimestampPrecision.PICOSECOND, "TIMESTAMP_PRECISION_PICOS"),
    ],
)
def test_client_query_and_wait_arrow_timestamp_precision(timestamp_precision, expected):
    client = make_client()
    client._call_api = mock.Mock(
        return_value={
            "jobReference": {"projectId": "PROJECT", "jobId": "j", "location": "US"},
            "jobComplete": True,
            "schema": {"fields": []},
        }
    )

    rows = client.query_and_wait(
        "SELECT 1",
        query_results_format="ARROW",
        timestamp_precision=timestamp_precision,
    )

    data = client._call_api.call_args.kwargs["data"]
    assert data["arrowSerializationOptions"]["picosTimestampPrecision"] == expected
    assert rows._arrow_serialization_options["picosTimestampPrecision"] == expected
    # formatOptions only shapes STRUCT_ENCODING rows, which ARROW doesn't return.
    assert "timestampOutputFormat" not in data["formatOptions"]


if __name__ == "__main__":
    unittest.main()
