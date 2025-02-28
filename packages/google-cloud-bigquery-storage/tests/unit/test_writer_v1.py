# Copyright 2021 Google LLC
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

import queue
import threading
import time
import unittest
from unittest import mock

from google.api_core import exceptions
from google.protobuf import descriptor_pb2
import pytest

from google.cloud.bigquery_storage_v1 import exceptions as bqstorage_exceptions
from google.cloud.bigquery_storage_v1 import gapic_version as package_version
from google.cloud.bigquery_storage_v1 import types as gapic_types
from google.cloud.bigquery_storage_v1.services import big_query_write

REQUEST_TEMPLATE = gapic_types.AppendRowsRequest()


class TestAppendRowsStream(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery_storage_v1.writer import AppendRowsStream

        return AppendRowsStream

    @staticmethod
    def _make_mock_client():
        return mock.create_autospec(big_query_write.BigQueryWriteClient)

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_defaults(self):
        from google.cloud.bigquery_storage_v1.writer import _process_request_template

        mock_client = self._make_mock_client()
        stream = self._make_one(mock_client, REQUEST_TEMPLATE)

        assert stream._client is mock_client
        assert stream._initial_request_template == _process_request_template(
            REQUEST_TEMPLATE
        )
        assert stream._closed is False
        assert not stream._close_callbacks
        assert isinstance(stream._futures_queue, queue.Queue)
        assert stream._futures_queue.empty()
        assert stream._metadata == ()
        assert stream._rpc is None
        assert stream._stream_name is None
        assert stream._consumer is None

    def test_is_active(self):
        mock_client = self._make_mock_client()
        stream = self._make_one(mock_client, REQUEST_TEMPLATE)

        assert stream.is_active is False

        with mock.patch("google.api_core.bidi.BackgroundConsumer") as MockConsumer:
            MockConsumer.return_value.is_active = True
            stream._consumer = MockConsumer()
            assert stream.is_active is True

    def test_add_close_callback(self):
        mock_client = self._make_mock_client()
        stream = self._make_one(mock_client, REQUEST_TEMPLATE)

        assert not stream._close_callbacks

        callbacks = [lambda x: x + i for i in range(3)]
        for item in callbacks:
            stream.add_close_callback(item)

        assert stream._close_callbacks == callbacks

    def test_close_before_open(self):
        mock_client = self._make_mock_client()
        manager = self._make_one(mock_client, REQUEST_TEMPLATE)
        manager.close()
        with pytest.raises(bqstorage_exceptions.StreamClosedError):
            manager.send(object())

    @mock.patch("google.api_core.bidi.BidiRpc", autospec=True)
    @mock.patch("google.api_core.bidi.BackgroundConsumer", autospec=True)
    def test_initial_send(self, background_consumer, bidi_rpc):
        from google.cloud.bigquery_storage_v1.writer import AppendRowsFuture

        mock_client = self._make_mock_client()
        request_template = gapic_types.AppendRowsRequest(
            write_stream="stream-name-from-REQUEST_TEMPLATE",
            offset=0,
            proto_rows=gapic_types.AppendRowsRequest.ProtoData(
                writer_schema=gapic_types.ProtoSchema(
                    proto_descriptor=descriptor_pb2.DescriptorProto()
                )
            ),
        )
        manager = self._make_one(mock_client, request_template)
        type(bidi_rpc.return_value).is_active = mock.PropertyMock(
            return_value=(False, True)
        )
        proto_rows = gapic_types.ProtoRows()
        proto_rows.serialized_rows.append(b"hello, world")
        initial_request = gapic_types.AppendRowsRequest(
            write_stream="this-is-a-stream-resource-path",
            offset=42,
            proto_rows=gapic_types.AppendRowsRequest.ProtoData(rows=proto_rows),
        )

        future = manager.send(initial_request)

        assert isinstance(future, AppendRowsFuture)
        background_consumer.assert_called_once_with(manager._rpc, manager._on_response)
        background_consumer.return_value.start.assert_called_once()
        assert manager._consumer == background_consumer.return_value

        # Make sure the request template and the first request are merged as
        # expected. Needs to be especially careful that nested properties such as
        # writer_schema and rows are merged as expected.
        expected_request = gapic_types.AppendRowsRequest(
            write_stream="this-is-a-stream-resource-path",
            offset=42,
            proto_rows=gapic_types.AppendRowsRequest.ProtoData(
                writer_schema=gapic_types.ProtoSchema(
                    proto_descriptor=descriptor_pb2.DescriptorProto()
                ),
                rows=proto_rows,
            ),
            trace_id=f"python-writer:{package_version.__version__}",
        )
        bidi_rpc.assert_called_once_with(
            start_rpc=mock_client.append_rows,
            initial_request=expected_request,
            # Extra header is required to route requests to the correct location.
            metadata=(
                (
                    "x-goog-request-params",
                    "write_stream=this-is-a-stream-resource-path",
                ),
            ),
        )

        bidi_rpc.return_value.add_done_callback.assert_called_once_with(
            manager._on_rpc_done
        )
        assert manager._rpc == bidi_rpc.return_value

        manager._consumer.is_active = True
        assert manager.is_active is True

    @mock.patch("google.api_core.bidi.BidiRpc", autospec=True)
    @mock.patch("google.api_core.bidi.BackgroundConsumer", autospec=True)
    def test_initial_send_with_timeout(self, background_consumer, bidi_rpc):
        from google.cloud.bigquery_storage_v1 import writer

        mock_client = self._make_mock_client()
        manager = self._make_one(mock_client, REQUEST_TEMPLATE)
        type(bidi_rpc.return_value).is_active = mock.PropertyMock(return_value=False)
        type(background_consumer.return_value).is_active = mock.PropertyMock(
            return_value=False
        )
        initial_request = gapic_types.AppendRowsRequest(
            write_stream="this-is-a-stream-resource-path"
        )
        now = time.monotonic()
        later = now + writer._DEFAULT_TIMEOUT + 1
        with mock.patch.object(writer.time, "sleep"), mock.patch.object(
            writer.time, "monotonic", mock.MagicMock(side_effect=(now, later))
        ), pytest.raises(exceptions.Unknown):
            manager.send(initial_request)

    @mock.patch("google.api_core.bidi.BidiRpc", autospec=True)
    @mock.patch("google.api_core.bidi.BackgroundConsumer", autospec=True)
    def test_send(self, background_consumer, bidi_rpc):
        mock_client = self._make_mock_client()
        stream = self._make_one(mock_client, REQUEST_TEMPLATE)
        stream._consumer = background_consumer
        stream._rpc = bidi_rpc

        type(background_consumer.return_value).is_active = mock.PropertyMock(
            return_value=True
        )
        request = gapic_types.AppendRowsRequest(
            write_stream="this-is-a-stream-resource-path"
        )
        stream.send(request)

        bidi_rpc.send.assert_called_once_with(request)
        assert stream._futures_queue.qsize() == 1

    @mock.patch("google.api_core.bidi.BidiRpc", autospec=True)
    @mock.patch("google.api_core.bidi.BackgroundConsumer", autospec=True)
    def test_close(self, background_consumer, bidi_rpc):
        from google.cloud.bigquery_storage_v1 import writer

        type(background_consumer.return_value).is_active = mock.PropertyMock(
            return_value=True
        )
        mock_client = self._make_mock_client()
        stream = self._make_one(mock_client, REQUEST_TEMPLATE)
        stream._consumer = background_consumer
        stream._rpc = bidi_rpc
        futures = [writer.AppendRowsFuture(stream) for _ in range(3)]
        for f in futures:
            stream._futures_queue.put(f)
        stream._close_callbacks = [mock.Mock() for _ in range(3)]
        close_exception = Exception("test exception")

        assert stream._closed is False

        stream.close(reason=close_exception)

        assert stream._closed is True
        assert stream._consumer is None
        assert stream._futures_queue.empty() is True
        background_consumer.stop.assert_called_once()
        bidi_rpc.close.assert_called_once()
        for f in futures:
            assert f.done() is True
            with pytest.raises(Exception, match="test exception"):
                f.result()

        for callback in stream._close_callbacks:
            callback.assert_called_once_with(stream, close_exception)


class Test_Connection(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery_storage_v1.writer import _Connection

        return _Connection

    @staticmethod
    def _make_mock_client():
        return mock.create_autospec(big_query_write.BigQueryWriteClient)

    @staticmethod
    def _make_mock_stream():
        from google.cloud.bigquery_storage_v1.writer import _process_request_template

        writer = mock.Mock()
        template = mock.PropertyMock(
            return_value=_process_request_template(REQUEST_TEMPLATE)
        )
        type(writer)._initial_request_template = template
        return writer

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_defaults(self):
        mock_client = self._make_mock_client()
        mock_stream = self._make_mock_stream()
        connection = self._make_one(mock_client, mock_stream)

        assert connection._client is mock_client
        assert connection._writer is mock_stream

        assert connection._metadata == ()

        assert isinstance(connection._thread_lock, type(threading.RLock()))
        assert connection._rpc is None
        assert connection._consumer is None
        assert connection._stream_name is None
        assert isinstance(connection._queue, queue.Queue)

        assert connection._closed is False

    def test_is_active(self):
        mock_client = self._make_mock_client()
        mock_stream = self._make_mock_stream()
        connection = self._make_one(mock_client, mock_stream)

        assert connection.is_active is False

        with mock.patch("google.api_core.bidi.BackgroundConsumer") as MockConsumer:
            MockConsumer.return_value.is_active = True
            connection._consumer = MockConsumer()
            assert connection.is_active is True

    @mock.patch("google.api_core.bidi.BidiRpc", autospec=True)
    @mock.patch("google.api_core.bidi.BackgroundConsumer", autospec=True)
    def test_initial_send(self, background_consumer, bidi_rpc):
        from google.cloud.bigquery_storage_v1.writer import AppendRowsFuture

        mock_client = self._make_mock_client()
        mock_stream = self._make_mock_stream()
        connection = self._make_one(mock_client, mock_stream)

        type(bidi_rpc.return_value).is_active = mock.PropertyMock(
            return_value=(False, True)
        )
        proto_rows = gapic_types.ProtoRows()
        proto_rows.serialized_rows.append(b"hello, world")
        initial_request = gapic_types.AppendRowsRequest(
            write_stream="this-is-a-stream-resource-path",
            offset=42,
            proto_rows=gapic_types.AppendRowsRequest.ProtoData(rows=proto_rows),
        )

        future = connection.send(initial_request)

        assert isinstance(future, AppendRowsFuture)
        background_consumer.assert_called_once_with(
            connection._rpc, connection._on_response
        )
        background_consumer.return_value.start.assert_called_once()
        assert connection._consumer == background_consumer.return_value

        # Make sure the request template and the first request are merged as
        # expected. Needs to be especially careful that nested properties such as
        # writer_schema and rows are merged as expected.
        expected_request = gapic_types.AppendRowsRequest(
            write_stream="this-is-a-stream-resource-path",
            offset=42,
            proto_rows=gapic_types.AppendRowsRequest.ProtoData(
                writer_schema=gapic_types.ProtoSchema(
                    proto_descriptor=descriptor_pb2.DescriptorProto()
                ),
                rows=proto_rows,
            ),
            trace_id=f"python-writer:{package_version.__version__}",
        )
        bidi_rpc.assert_called_once_with(
            start_rpc=mock_client.append_rows,
            initial_request=expected_request,
            # Extra header is required to route requests to the correct location.
            metadata=(
                (
                    "x-goog-request-params",
                    "write_stream=this-is-a-stream-resource-path",
                ),
            ),
        )

        bidi_rpc.return_value.add_done_callback.assert_called_once_with(
            connection._on_rpc_done
        )
        assert connection._rpc == bidi_rpc.return_value

        connection._consumer.is_active = True
        assert connection.is_active is True

    @mock.patch("google.api_core.bidi.BidiRpc", autospec=True)
    @mock.patch("google.api_core.bidi.BackgroundConsumer", autospec=True)
    def test_initial_send_with_timeout(self, background_consumer, bidi_rpc):
        from google.cloud.bigquery_storage_v1 import writer

        mock_client = self._make_mock_client()
        mock_stream = self._make_mock_stream()
        connection = self._make_one(mock_client, mock_stream)

        type(bidi_rpc.return_value).is_active = mock.PropertyMock(return_value=False)
        type(background_consumer.return_value).is_active = mock.PropertyMock(
            return_value=False
        )
        initial_request = gapic_types.AppendRowsRequest(
            write_stream="this-is-a-stream-resource-path"
        )
        now = time.monotonic()
        later = now + writer._DEFAULT_TIMEOUT + 1
        with mock.patch.object(writer.time, "sleep"), mock.patch.object(
            writer.time, "monotonic", mock.MagicMock(side_effect=(now, later))
        ), pytest.raises(exceptions.Unknown):
            connection.send(initial_request)

    @mock.patch("google.api_core.bidi.BidiRpc", autospec=True)
    @mock.patch("google.api_core.bidi.BackgroundConsumer", autospec=True)
    def test_send(self, background_consumer, bidi_rpc):
        mock_client = self._make_mock_client()
        mock_stream = self._make_mock_stream()
        connection = self._make_one(mock_client, mock_stream)

        connection._consumer = background_consumer
        connection._rpc = bidi_rpc

        type(background_consumer.return_value).is_active = mock.PropertyMock(
            return_value=True
        )
        request = gapic_types.AppendRowsRequest(
            write_stream="this-is-a-stream-resource-path"
        )
        connection.send(request)

        bidi_rpc.send.assert_called_once_with(request)
        assert connection._queue.qsize() == 1

    @mock.patch("google.api_core.bidi.BidiRpc", autospec=True)
    @mock.patch("google.api_core.bidi.BackgroundConsumer", autospec=True)
    def test_close(self, background_consumer, bidi_rpc):
        from google.cloud.bigquery_storage_v1 import writer

        type(background_consumer.return_value).is_active = mock.PropertyMock(
            return_value=True
        )
        mock_client = self._make_mock_client()
        mock_stream = self._make_mock_stream()
        connection = self._make_one(mock_client, mock_stream)

        connection._consumer = background_consumer
        connection._rpc = bidi_rpc

        futures = [writer.AppendRowsFuture(connection._writer) for _ in range(3)]
        for f in futures:
            connection._queue.put(f)
        close_exception = Exception("test exception")

        assert connection._closed is False

        with self.assertLogs(writer._LOGGER, level="DEBUG") as cm:
            connection.close(reason=close_exception)
        assert "Stopping consumer." in str(cm.output)
        assert "Finished stopping manager." in str(cm.output)

        assert connection._closed is True
        assert connection._queue.empty() is True
        assert connection._consumer is None
        bidi_rpc.close.assert_called_once()
        background_consumer.stop.assert_called_once()
        for f in futures:
            assert f.done() is True
            with pytest.raises(Exception, match="test exception"):
                f.result()

    def test__on_response_closed(self):
        mock_client = self._make_mock_client()
        mock_stream = self._make_mock_stream()
        connection = self._make_one(mock_client, mock_stream)

        response = gapic_types.AppendRowsResponse()

        connection._closed = True
        with pytest.raises(
            bqstorage_exceptions.StreamClosedError, match="Stream closed"
        ):
            connection._on_response(response)

    def test__on_response_exception(self):
        from google.cloud.bigquery_storage_v1.writer import AppendRowsFuture

        mock_client = self._make_mock_client()
        mock_stream = self._make_mock_stream()
        connection = self._make_one(mock_client, mock_stream)
        connection._queue = mock.Mock()
        future = AppendRowsFuture(mock_stream)
        connection._queue.get_nowait.return_value = future
        response = gapic_types.AppendRowsResponse(
            {
                "error": {
                    "code": 404,
                    "message": "test error",
                }
            }
        )

        connection._on_response(response)

        assert future._is_done is True
        with pytest.raises(Exception, match="test error"):
            future.result()

    def test__on_response_result(self):
        from google.cloud.bigquery_storage_v1.writer import AppendRowsFuture

        mock_client = self._make_mock_client()
        mock_stream = self._make_mock_stream()
        connection = self._make_one(mock_client, mock_stream)
        connection._queue = mock.Mock()
        future = AppendRowsFuture(mock_stream)
        connection._queue.get_nowait.return_value = future
        response = gapic_types.AppendRowsResponse()

        connection._on_response(response)

        assert future._is_done is True
        future.result()

    def test__on_rpc_done(self):
        from google.cloud.bigquery_storage_v1.writer import AppendRowsFuture

        mock_client = self._make_mock_client()
        mock_stream = self._make_mock_stream()
        connection = self._make_one(mock_client, mock_stream)
        future = AppendRowsFuture(mock_stream)

        connection._on_rpc_done(future)

        mock_stream._on_rpc_done.assert_called_once_with(future)

    def test__process_request_template(self):
        from google.cloud.bigquery_storage_v1.writer import _process_request_template

        request = gapic_types.AppendRowsRequest(
            write_stream="this-is-a-stream-resource-path"
        )

        new_request = _process_request_template(request)

        # Verify this is deep copy
        assert new_request is not request

        # Verify that proto3-only fields are deleted
        proto_descriptor = new_request.proto_rows.writer_schema.proto_descriptor
        assert len(proto_descriptor.field) == 0
        assert len(proto_descriptor.oneof_decl) == 0


class TestAppendRowsFuture(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery_storage_v1.writer import AppendRowsFuture

        return AppendRowsFuture

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_future_done_false(self):
        from google.cloud.bigquery_storage_v1.writer import AppendRowsStream

        mock_client = mock.create_autospec(big_query_write.BigQueryWriteClient)
        manager = AppendRowsStream(mock_client, REQUEST_TEMPLATE)
        future = self._make_one(manager)
        assert not future.done()

    def test_future_done_true_with_result(self):
        from google.cloud.bigquery_storage_v1.writer import AppendRowsStream

        mock_client = mock.create_autospec(big_query_write.BigQueryWriteClient)
        manager = AppendRowsStream(mock_client, REQUEST_TEMPLATE)
        future = self._make_one(manager)
        future.set_result(object())
        assert future.done()

    def test_future_done_true_with_exception(self):
        from google.cloud.bigquery_storage_v1.writer import AppendRowsStream

        mock_client = mock.create_autospec(big_query_write.BigQueryWriteClient)
        manager = AppendRowsStream(mock_client, REQUEST_TEMPLATE)
        future = self._make_one(manager)
        future.set_exception(ValueError())
        assert future.done()
