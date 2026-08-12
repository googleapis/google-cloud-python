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

import pytest

from google.cloud.bigquery import _job_helpers
from google.cloud.bigquery.client import Client
from google.cloud.bigquery.table import RowIterator, _EmptyRowIterator


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
        self.assertIn("formatOptions", call_args.kwargs["data"])
        self.assertEqual(
            call_args.kwargs["data"]["formatOptions"]["arrowSerializationOptions"][
                "bufferCompression"
            ],
            "LZ4_FRAME",
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

        with mock.patch("google.cloud.bigquery.table.pyarrow") as mock_pyarrow:
            mock_pyarrow.py_buffer = lambda x: x
            batches = list(iterator._download_arrow_from_job_id(timeout=5.0))
            self.assertEqual(batches, [])

            expected_stream_name = (
                "projects/test-proj/locations/US/jobs/test-job-456/streams/_default"
            )
            mock_bqstorage.read_rows.assert_called_once_with(
                expected_stream_name, offset=0, timeout=5.0
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

        with mock.patch("google.cloud.bigquery.table.pyarrow") as mock_pyarrow:
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
                expected_stream_name, offset=10, timeout=5.0
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

        with mock.patch("google.cloud.bigquery.table.pyarrow") as mock_pyarrow:
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
                expected_stream_name, offset=0, timeout=5.0
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

        with mock.patch("google.cloud.bigquery.table.pyarrow"):
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

        with mock.patch("google.cloud.bigquery.table.pyarrow") as mock_pyarrow:
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

        with mock.patch("google.cloud.bigquery.table.pyarrow") as mock_pyarrow:
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

        with mock.patch("google.cloud.bigquery.table.pyarrow") as mock_pyarrow:
            mock_pyarrow.py_buffer = lambda x: x
            mock_pyarrow.ipc.read_schema.return_value = "deserialized_schema"
            mock_pyarrow.ipc.read_record_batch.return_value = mock_first_batch

            batches = list(iterator._download_arrow_from_job_id(timeout=5.0))
            self.assertEqual(batches, [mock_first_batch])
            mock_client._ensure_bqstorage_client.assert_called_once()
            expected_stream = "projects/test-proj/locations/US/jobs/test-job-incomplete/streams/_default"
            mock_bqstorage.read_rows.assert_called_once_with(
                expected_stream, offset=10, timeout=5.0
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
            call_args.kwargs["data"]["formatOptions"]["arrowSerializationOptions"][
                "bufferCompression"
            ],
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


if __name__ == "__main__":
    unittest.main()
