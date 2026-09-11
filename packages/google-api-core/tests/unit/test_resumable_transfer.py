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

import io
from typing import Union
from unittest import mock

import pytest
import requests
from google.protobuf import empty_pb2
import proto

from tests.helpers import EchoResponse
from google.api_core import exceptions
from google.api_core.resumable_transfer import (
    DEFAULT_CHUNK_SIZE,
    Command,
    MissingStatusHeaderError,
    ProgressState,
    ResumableUploadConfig,
    ResumableUploadSession,
    Status,
    TransferStalledError,
    UnseekableStreamError,
    UploadCancelledError,
    UploadProgress,
    common,
    upload_state,
)


class DummyResponse:
    """Mock response class representing a deserialized protobuf message."""

    def __init__(self, name: str, size: int) -> None:
        """Initializes a DummyResponse.

        Args:
            name: Resource name string.
            size: Resource size in bytes.
        """
        self.name = name
        self.size = size

    @classmethod
    def from_json(cls, data: Union[str, bytes]) -> "DummyResponse":
        """Deserializes JSON payload into a DummyResponse instance.

        Args:
            data: JSON byte string or text.

        Returns:
            A DummyResponse instance.
        """
        import json

        d = json.loads(data.decode("utf-8") if isinstance(data, bytes) else data)
        return cls(name=d.get("name", ""), size=d.get("size", 0))


# =====================================================================
# 1. Common Constants and Error Types
# =====================================================================


def test_common_constants():
    assert DEFAULT_CHUNK_SIZE == 10 * 1024 * 1024
    assert common.HEADER_PROTOCOL == "X-Goog-Upload-Protocol"
    assert common.HEADER_COMMAND == "X-Goog-Upload-Command"
    assert common.HEADER_STATUS == "X-Goog-Upload-Status"
    assert common.HEADER_URL == "X-Goog-Upload-URL"
    assert common.HEADER_OFFSET == "X-Goog-Upload-Offset"
    assert common.HEADER_SIZE_RECEIVED == "X-Goog-Upload-Size-Received"
    assert common.PROTOCOL_RESUMABLE == "resumable"

    assert Command.START == "start"
    assert Command.UPLOAD == "upload"
    assert Command.FINALIZE == "finalize"
    assert Command.QUERY == "query"
    assert Command.CANCEL == "cancel"

    assert Status.ACTIVE == "active"
    assert Status.FINAL == "final"
    assert Status.CANCELLED == "cancelled"

    assert ProgressState.STARTED == "started"
    assert ProgressState.UPLOADING == "uploading"
    assert ProgressState.RECOVERING == "recovering"
    assert ProgressState.OFFSET_RECEIVED == "offset received"
    assert ProgressState.FINALIZED == "finalized"


def test_upload_progress_dataclass():
    prog = UploadProgress(
        upload_url="https://upload.example.com/session123",
        chunk_size=1024,
        bytes_uploaded=512,
        total_bytes=2048,
        state=ProgressState.UPLOADING,
    )
    assert prog.upload_url == "https://upload.example.com/session123"
    assert prog.chunk_size == 1024
    assert prog.bytes_uploaded == 512
    assert prog.total_bytes == 2048
    assert prog.state == ProgressState.UPLOADING


def test_exception_hierarchy():
    assert issubclass(TransferStalledError, exceptions.GoogleAPICallError)
    assert issubclass(UnseekableStreamError, exceptions.GoogleAPICallError)
    assert issubclass(UploadCancelledError, exceptions.GoogleAPICallError)
    assert issubclass(MissingStatusHeaderError, exceptions.GoogleAPICallError)
    assert exceptions.TransferStalledError is TransferStalledError
    assert exceptions.UnseekableStreamError is UnseekableStreamError
    assert exceptions.UploadCancelledError is UploadCancelledError
    assert exceptions.MissingStatusHeaderError is MissingStatusHeaderError


# =====================================================================
# 2. Pure Sans-I/O State Machine (upload_state.py)
# =====================================================================


def test_protocol_state_start_request():
    state = upload_state.ProtocolState(upload_url="https://api.example.com/start")
    method, url, headers, payload = state.build_start_request(
        body='{"name": "test"}',
        headers=[("X-Custom", "val")],
        content_type="text/plain",
        size=1000,
    )

    assert method == "POST"
    assert url == "https://api.example.com/start"
    assert headers["X-Goog-Upload-Protocol"] == "resumable"
    assert headers["X-Goog-Upload-Command"] == "start"
    assert headers["X-Goog-Upload-Header-Content-Type"] == "text/plain"
    assert headers["X-Goog-Upload-Header-Content-Length"] == "1000"
    assert headers["X-Custom"] == "val"
    assert payload == b'{"name": "test"}'


def test_protocol_state_process_start_response():
    state = upload_state.ProtocolState(upload_url="https://api.example.com/start")
    headers = {
        "X-Goog-Upload-Status": "active",
        "X-Goog-Upload-URL": "https://upload.example.com/resumable-id",
        "X-Goog-Upload-Chunk-Granularity": "262144",
    }
    url = state.process_start_response(200, headers)
    assert url == "https://upload.example.com/resumable-id"
    assert state.resumable_url == "https://upload.example.com/resumable-id"
    assert state._chunk_granularity == 262144


def test_protocol_state_start_response_missing_status():
    state = upload_state.ProtocolState(upload_url="https://api.example.com/start")
    headers = {"X-Goog-Upload-URL": "https://upload.example.com/resumable-id"}
    with pytest.raises(MissingStatusHeaderError):
        state.process_start_response(200, headers)


def test_protocol_state_start_response_missing_url():
    state = upload_state.ProtocolState(upload_url="https://api.example.com/start")
    headers = {"X-Goog-Upload-Status": "active"}
    with pytest.raises(ValueError, match="Server did not return"):
        state.process_start_response(200, headers)


def test_protocol_state_granularity_alignment():
    state = upload_state.ProtocolState(chunk_size=500)
    assert state.chunk_size == 500
    state._chunk_granularity = 256
    # 500 rounded up to multiple of 256 is 512
    assert state.chunk_size == 512


def test_protocol_state_chunk_request_and_response():
    state = upload_state.ProtocolState(
        resumable_url="https://upload.example.com/session"
    )

    # First chunk: not last
    method, url, headers, payload = state.build_chunk_request(
        data=b"0123456789", is_last_chunk=False
    )
    assert headers["X-Goog-Upload-Command"] == "upload"
    assert headers["X-Goog-Upload-Offset"] == "0"
    assert payload == b"0123456789"

    state.process_chunk_response(200, {"X-Goog-Upload-Status": "active"}, 10)
    assert state.bytes_uploaded == 10
    assert not state.finished

    # Second chunk: last chunk
    method, url, headers, payload = state.build_chunk_request(
        data=b"abcdef", is_last_chunk=True, content_type="text/plain"
    )
    assert headers["X-Goog-Upload-Command"] == "upload, finalize"
    assert headers["X-Goog-Upload-Offset"] == "10"
    assert headers["Content-Type"] == "text/plain"

    state.process_chunk_response(200, {"X-Goog-Upload-Status": "final"}, 6)
    assert state.bytes_uploaded == 16
    assert state.finished


def test_protocol_state_chunk_missing_status_header():
    state = upload_state.ProtocolState(
        resumable_url="https://upload.example.com/session"
    )
    with pytest.raises(MissingStatusHeaderError):
        state.process_chunk_response(200, {}, 10)


def test_protocol_state_query_and_cancel():
    state = upload_state.ProtocolState(
        resumable_url="https://upload.example.com/session"
    )
    method, url, headers, payload = state.build_query_request()
    assert headers["X-Goog-Upload-Command"] == "query"

    received = state.process_query_response(
        200, {"X-Goog-Upload-Status": "active", "X-Goog-Upload-Size-Received": "1024"}
    )
    assert received == 1024
    assert state.bytes_uploaded == 1024

    method, url, headers, payload = state.build_cancel_request()
    assert headers["X-Goog-Upload-Command"] == "cancel"
    state.process_cancel_response(200, {})
    assert state.invalid


# =====================================================================
# 3. ResumableUploadConfig Sensible Defaults
# =====================================================================


def test_resumable_upload_config_defaults():
    config = ResumableUploadConfig()
    assert config.chunk_size == 10 * 1024 * 1024
    assert config.stall_minimum_rate == 64 * 1024
    assert config.stall_timeout == 120.0
    assert config.start_timeout is None
    assert config.start_retry is None
    assert config.additional_headers is None
    assert config.deadline is None


def test_resumable_upload_config_fallbacks_and_headers():
    retry1 = mock.Mock()
    config1 = ResumableUploadConfig(
        start_timeout=45.0,
        retry=retry1,
        additional_headers={"X-Test": "1"},
    )
    assert config1.timeout == 45.0
    assert config1.start_timeout == 45.0
    assert config1.retry is retry1
    assert config1.start_retry is retry1
    assert config1.start_headers == [("X-Test", "1")]

    retry2 = mock.Mock()
    config2 = ResumableUploadConfig(
        timeout=30.0,
        start_retry=retry2,
        additional_headers=[("X-Test", "2")],
    )
    assert config2.timeout == 30.0
    assert config2.start_timeout == 30.0
    assert config2.retry is retry2
    assert config2.start_retry is retry2
    assert config2.start_headers == [("X-Test", "2")]


# =====================================================================
# 4. Synchronous ResumableUploadSession (upload.py)
# =====================================================================


def test_sync_upload_direct_execution():
    session_transport = mock.create_autospec(requests.Session, instance=True)

    # 1. Start response
    start_resp = mock.Mock()
    start_resp.ok = True
    start_resp.status_code = 200
    start_resp.headers = {
        "X-Goog-Upload-Status": "active",
        "X-Goog-Upload-URL": "https://upload.example.com/resumable-123",
    }

    # 2. Chunk response
    chunk_resp = mock.Mock()
    chunk_resp.ok = True
    chunk_resp.status_code = 200
    chunk_resp.headers = {"X-Goog-Upload-Status": "final"}
    chunk_resp.content = b'{"name": "done.txt", "size": 11}'

    session_transport.request.side_effect = [start_resp, chunk_resp]

    config = ResumableUploadConfig(response_type=DummyResponse)
    session = ResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=config,
        transport=session_transport,
    )

    payload = b"Hello world"
    result = session.upload(stream=payload, request_body='{"name": "test"}')

    assert isinstance(result, DummyResponse)
    assert result.name == "done.txt"
    assert result.size == 11
    assert session.finished is True
    assert session.bytes_uploaded == 11
    assert session.upload_url == "https://upload.example.com/resumable-123"
    assert session.response == result


def test_sync_upload_iterative_progress():
    session_transport = mock.create_autospec(requests.Session, instance=True)

    start_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-123",
        },
    )
    chunk1_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={"X-Goog-Upload-Status": "active"},
    )
    chunk2_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={"X-Goog-Upload-Status": "final"},
        content=b'{"name": "stream.txt", "size": 8}',
    )

    session_transport.request.side_effect = [start_resp, chunk1_resp, chunk2_resp]

    config = ResumableUploadConfig(chunk_size=4, response_type=DummyResponse)
    session = ResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=config,
        transport=session_transport,
    )

    progress_events = list(session.iter_upload(stream=b"12345678"))
    assert len(progress_events) == 3
    assert progress_events[0].state == ProgressState.STARTED
    assert progress_events[1].state == ProgressState.UPLOADING
    assert progress_events[1].bytes_uploaded == 4
    assert progress_events[2].state == ProgressState.FINALIZED
    assert progress_events[2].bytes_uploaded == 8

    assert session.response.name == "stream.txt"
    assert session.response.size == 8


def test_sync_resume():
    session_transport = mock.create_autospec(requests.Session, instance=True)

    # 1. Query response returns offset 5
    query_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-Size-Received": "5",
        },
    )
    # 2. Remaining chunk response
    chunk_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={"X-Goog-Upload-Status": "final"},
        content=b'{"name": "resumed.txt", "size": 10}',
    )
    session_transport.request.side_effect = [query_resp, chunk_resp]

    config = ResumableUploadConfig(response_type=DummyResponse)
    session = ResumableUploadSession(config=config)

    stream = io.BytesIO(b"0123456789")
    resp = session.resume(
        upload_url="https://upload.example.com/resumable-123",
        stream=stream,
        transport=session_transport,
    )

    assert isinstance(resp, DummyResponse)
    assert resp.name == "resumed.txt"
    assert session.bytes_uploaded == 10
    assert session.finished is True


def test_sync_iter_resume():
    """Verifies streaming progress during upload resumption."""
    session_transport = mock.create_autospec(requests.Session, instance=True)

    query_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-Size-Received": "5",
        },
    )
    chunk_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={"X-Goog-Upload-Status": "final"},
        content=b'{"name": "iter_resumed.txt", "size": 10}',
    )
    session_transport.request.side_effect = [query_resp, chunk_resp]

    config = ResumableUploadConfig(response_type=DummyResponse)
    session = ResumableUploadSession(config=config)

    stream = io.BytesIO(b"0123456789")
    progress_list = list(
        session.iter_resume(
            upload_url="https://upload.example.com/resumable-123",
            stream=stream,
            transport=session_transport,
        )
    )

    assert session.response.name == "iter_resumed.txt"
    assert session.bytes_uploaded == 10
    assert session.finished is True
    assert len(progress_list) == 2
    assert progress_list[0].state == ProgressState.OFFSET_RECEIVED
    assert progress_list[1].state == ProgressState.FINALIZED


def test_sync_recoverable_status_code_triggers_offset_recovery():
    session_transport = mock.create_autospec(requests.Session, instance=True)

    start_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-123",
        },
    )
    # First chunk upload fails with 400 (recoverable Category 2)
    err400_resp = mock.Mock(
        ok=False,
        status_code=400,
        headers={},
    )
    err400_resp.json.return_value = {"error": {"message": "Bad Request", "details": []}}
    err400_resp.text = '{"error": {"message": "Bad Request"}}'
    err400_resp.content = err400_resp.text.encode("utf-8")
    # Recovery query returns offset 0
    query_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-Size-Received": "0",
        },
    )
    # Retry chunk upload succeeds
    success_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={"X-Goog-Upload-Status": "final"},
        content=b'{"name": "recovered.txt", "size": 5}',
    )

    session_transport.request.side_effect = [
        start_resp,
        err400_resp,
        query_resp,
        success_resp,
    ]

    session = ResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=ResumableUploadConfig(response_type=DummyResponse),
        transport=session_transport,
    )

    resp = session.upload(stream=b"12345")
    assert resp.name == "recovered.txt"
    assert session.bytes_uploaded == 5


def test_sync_exceptions_carry_upload_url_and_chunk_size():
    session_transport = mock.create_autospec(requests.Session, instance=True)

    start_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-123",
        },
    )
    # Fatal 403 error on chunk upload
    err403_resp = mock.Mock(
        ok=False,
        status_code=403,
        headers={},
    )
    err403_resp.json.return_value = {"error": {"message": "Forbidden", "details": []}}
    err403_resp.text = '{"error": {"message": "Forbidden"}}'
    err403_resp.content = err403_resp.text.encode("utf-8")
    session_transport.request.side_effect = [start_resp, err403_resp]

    session = ResumableUploadSession(
        upload_url="https://api.example.com/start",
        transport=session_transport,
    )

    with pytest.raises(exceptions.GoogleAPICallError) as exc_info:
        session.upload(stream=b"data")

    err = exc_info.value
    assert err.upload_url == "https://upload.example.com/resumable-123"
    assert err.chunk_size == session.chunk_size


def test_sync_unseekable_stream_error_on_preceding_offset():
    session_transport = mock.create_autospec(requests.Session, instance=True)

    query_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-Size-Received": "50",
        },
    )
    session_transport.request.side_effect = [query_resp]

    session = ResumableUploadSession(
        config=ResumableUploadConfig(),
        transport=session_transport,
    )

    # Mock an unseekable stream
    unseekable = mock.Mock(spec=io.RawIOBase)
    unseekable.seekable.return_value = False

    with pytest.raises(UnseekableStreamError) as exc_info:
        session.resume(
            upload_url="https://upload.example.com/resumable-123",
            stream=unseekable,
            transport=session_transport,
        )

    assert exc_info.value.upload_url == "https://upload.example.com/resumable-123"


def test_sync_stall_control_timeout():
    session_transport = mock.create_autospec(requests.Session, instance=True)

    start_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-123",
        },
    )
    session_transport.request.side_effect = [
        start_resp,
        requests.exceptions.Timeout("Read timed out"),
    ]

    # Configure stall control with 0.1s timeout
    config = ResumableUploadConfig(
        stall_minimum_rate=1024,
        stall_timeout=0.1,
    )
    session = ResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=config,
        transport=session_transport,
    )

    with pytest.raises(TransferStalledError) as exc_info:
        session.upload(stream=b"test data")

    assert exc_info.value.upload_url == "https://upload.example.com/resumable-123"


def test_sync_cancel():
    session_transport = mock.create_autospec(requests.Session, instance=True)
    cancel_resp = mock.Mock(ok=True, status_code=200, headers={})
    session_transport.request.return_value = cancel_resp

    session = ResumableUploadSession(
        resumable_url="https://upload.example.com/resumable-123",
        transport=session_transport,
    )
    session.cancel()
    assert session._state.invalid is True


def test_sync_response_type_proto_message():
    session_transport = mock.create_autospec(requests.Session, instance=True)
    start_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-123",
        },
    )
    chunk_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={"X-Goog-Upload-Status": "final"},
        content=b'{"content": "proto_payload"}',
    )
    session_transport.request.side_effect = [start_resp, chunk_resp]

    session = ResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=ResumableUploadConfig(response_type=EchoResponse),
        transport=session_transport,
    )
    resp = session.upload(stream=b"payload")
    assert isinstance(resp, EchoResponse)
    assert resp.content == "proto_payload"


def test_sync_response_type_protobuf_message():
    session_transport = mock.create_autospec(requests.Session, instance=True)
    start_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-123",
        },
    )
    chunk_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={"X-Goog-Upload-Status": "final"},
        content=b"{}",
    )
    session_transport.request.side_effect = [start_resp, chunk_resp]

    session = ResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=ResumableUploadConfig(response_type=empty_pb2.Empty),
        transport=session_transport,
    )
    resp = session.upload(stream=b"payload")
    assert isinstance(resp, empty_pb2.Empty)


def test_sync_response_type_callable():
    session_transport = mock.create_autospec(requests.Session, instance=True)
    start_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-123",
        },
    )
    chunk_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={"X-Goog-Upload-Status": "final"},
        content=b"custom_payload",
    )
    session_transport.request.side_effect = [start_resp, chunk_resp]

    session = ResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=ResumableUploadConfig(response_type=lambda c: c.decode("utf-8").upper()),
        transport=session_transport,
    )
    resp = session.upload(stream=b"payload")
    assert resp == "CUSTOM_PAYLOAD"


def test_sync_response_type_raw_response():
    session_transport = mock.create_autospec(requests.Session, instance=True)
    start_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-123",
        },
    )
    chunk_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={"X-Goog-Upload-Status": "final"},
        content=b"raw_content",
    )
    session_transport.request.side_effect = [start_resp, chunk_resp]

    session = ResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=ResumableUploadConfig(response_type=None),
        transport=session_transport,
    )
    resp = session.upload(stream=b"payload")
    assert resp is chunk_resp


