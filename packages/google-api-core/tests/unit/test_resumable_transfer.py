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

import datetime
import io
from typing import Union
from unittest import mock

import pytest
import requests
from google.protobuf import empty_pb2

import google.api_core.retry
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
from tests.helpers import EchoResponse


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
    assert config.headers is None
    assert config.deadline is None


def test_resumable_upload_config_fallbacks_and_headers():
    retry1 = mock.Mock()
    config1 = ResumableUploadConfig(
        start_timeout=45.0,
        retry=retry1,
        headers={"X-Test": "1"},
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
        headers=[("X-Test", "2")],
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


def test_sync_retry_predicate_allows_timeout_with_stall_control():
    config = ResumableUploadConfig(stall_minimum_rate=1024, stall_timeout=1.0)
    session = ResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=config,
    )
    predicate = session._get_retry_predicate()
    assert predicate(requests.exceptions.Timeout("Read timed out")) is True


@pytest.mark.parametrize("invalid_stream", ["invalid_string", {"key": "value"}, 12345])
def test_sync_upload_rejects_invalid_stream_types(invalid_stream):
    session_transport = mock.create_autospec(requests.Session, instance=True)
    session = ResumableUploadSession(
        upload_url="https://api.example.com/start",
        transport=session_transport,
    )
    with pytest.raises(TypeError, match="Unsupported stream type"):
        session.upload(stream=invalid_stream)


def test_upload_state_properties():
    state = upload_state.ProtocolState("https://api.example.com/init", chunk_size=500)
    assert state.initial_url == "https://api.example.com/init"
    assert state.resumable_url is None
    assert state.bytes_uploaded == 0
    assert state.total_bytes is None
    assert state.finished is False
    assert state.invalid is False
    assert state.chunk_size == 500

    # With granularity alignment
    state._chunk_granularity = 256
    assert state.chunk_size == 512


def test_upload_state_start_errors():
    state = upload_state.ProtocolState("https://api.example.com/init")
    with pytest.raises(ValueError, match="Start command failed with status 500"):
        state.process_start_response(500, {})
    assert state.invalid is True

    state2 = upload_state.ProtocolState("https://api.example.com/init")
    with pytest.raises(ValueError, match="Server did not return"):
        state2.process_start_response(200, {"X-Goog-Upload-Status": "active"})
    assert state2.invalid is True


def test_upload_state_chunk_and_query_errors():
    state = upload_state.ProtocolState("https://api.example.com/init")
    with pytest.raises(ValueError, match="Upload session URL not established"):
        state.build_chunk_request(b"data", is_last_chunk=True)

    with pytest.raises(ValueError, match="Upload session URL not established"):
        state.build_query_request()

    with pytest.raises(ValueError, match="Upload session URL not established"):
        state.build_cancel_request()

    # process_chunk_response with non-200/201 status code
    state.process_chunk_response(503, {}, 10)
    assert state.bytes_uploaded == 0

    # process_query_response with non-200/201 status code
    with pytest.raises(ValueError, match="Query recovery failed with status 500"):
        state.process_query_response(500, {})
    assert state.invalid is True

    # process_query_response with final status
    state3 = upload_state.ProtocolState("https://api.example.com/init")
    state3.process_query_response(200, {"X-Goog-Upload-Status": "final"})
    assert state3.finished is True

    # process_query_response with cancelled status
    state4 = upload_state.ProtocolState("https://api.example.com/init")
    with pytest.raises(UploadCancelledError):
        state4.process_query_response(200, {"X-Goog-Upload-Status": "cancelled"})
    assert state4.invalid is True


def test_sync_upload_session_properties_and_enrichment():
    session_transport = mock.create_autospec(requests.Session, instance=True)
    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        transport=session_transport,
    )
    assert session._get_transport(None) is session_transport
    assert session._state.resumable_url is None
    assert session.bytes_uploaded == 0
    assert session._state.total_bytes is None
    assert session.finished is False
    assert session._state.invalid is False

    # Exception without __dict__ does not fail _enrich_exception
    exc_no_dict = Exception()
    session._enrich_exception(exc_no_dict)


def test_sync_upload_session_transport_missing():
    session = ResumableUploadSession(upload_url="https://api.example.com/init")
    with pytest.raises(
        ValueError, match="A requests.Session transport must be provided"
    ):
        session.upload(stream=b"payload")

    with pytest.raises(
        ValueError, match="A requests.Session transport must be provided"
    ):
        session.cancel()


def test_sync_deadline_handling():
    past = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=10)
    config = ResumableUploadConfig(deadline=past)
    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=config,
    )
    with pytest.raises(exceptions.DeadlineExceeded):
        session._get_deadline_remaining()

    future_naive = datetime.datetime.now() + datetime.timedelta(hours=1)
    config2 = ResumableUploadConfig(deadline=future_naive)
    session2 = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=config2,
    )
    rem = session2._get_deadline_remaining()
    assert rem is not None and rem > 0


def test_sync_retry_predicate_branches():
    session = ResumableUploadSession(upload_url="https://api.example.com/init")
    pred = session._get_retry_predicate()

    assert pred(exceptions.DeadlineExceeded("deadline")) is False
    assert pred(TransferStalledError("stalled")) is False
    assert pred(UploadCancelledError("cancelled")) is False
    assert pred(MissingStatusHeaderError("missing")) is True
    assert pred(requests.exceptions.ConnectionError("conn")) is True
    assert pred(requests.exceptions.ChunkedEncodingError("chunked")) is True
    assert pred(exceptions.from_http_status(503, "503")) is True
    assert pred(exceptions.from_http_status(400, "400")) is False
    assert pred(TypeError("other")) is False


def test_sync_reposition_stream_errors():
    session_transport = mock.create_autospec(requests.Session, instance=True)
    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        transport=session_transport,
    )

    unseekable = mock.Mock()
    unseekable.seekable.return_value = False
    with pytest.raises(UnseekableStreamError, match="Stream is not seekable"):
        session._reposition_stream_offset(unseekable, 100)

    failing_seek = mock.Mock()
    failing_seek.seekable.return_value = True
    failing_seek.seek.side_effect = OSError("Disk read failure")
    with pytest.raises(UnseekableStreamError, match="Failed to seek stream"):
        session._reposition_stream_offset(failing_seek, 100)


def test_sync_prepare_stream_seekable_and_iterable():
    session_transport = mock.create_autospec(requests.Session, instance=True)
    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        transport=session_transport,
    )

    stream_obj, computed_size = session._prepare_stream([b"hello ", b"world"], None)
    assert stream_obj.read() == b"hello world"
    assert computed_size == 11

    class CustomSeekable:
        def __init__(self, data: bytes):
            self._bio = io.BytesIO(data)

        def read(self, n: int = -1) -> bytes:
            return self._bio.read(n)

        def seek(self, offset: int, whence: int = io.SEEK_SET) -> int:
            return self._bio.seek(offset, whence)

        def tell(self) -> int:
            return self._bio.tell()

        def seekable(self) -> bool:
            return True

    custom = CustomSeekable(b"0123456789")
    custom.seek(2)
    stream_obj2, computed_size2 = session._prepare_stream(custom, None)
    assert computed_size2 == 8
    assert custom.tell() == 2


def test_sync_config_fallbacks_and_headers():
    cfg1 = ResumableUploadConfig(start_timeout=15.0)
    assert cfg1.timeout == 15.0

    cfg2 = ResumableUploadConfig(timeout=25.0)
    assert cfg2.start_timeout == 25.0

    ret = mock.Mock(spec=google.api_core.retry.Retry)
    cfg3 = ResumableUploadConfig(start_retry=ret)
    assert cfg3.retry is ret

    cfg4 = ResumableUploadConfig(retry=ret)
    assert cfg4.start_retry is ret

    cfg_dict = ResumableUploadConfig(headers={"X-Key": "Val"})
    assert cfg_dict.start_headers == [("X-Key", "Val")]

    cfg_list = ResumableUploadConfig(headers=[("X-Key", "Val")])
    assert cfg_list.start_headers == [("X-Key", "Val")]

    cfg_none = ResumableUploadConfig(headers=None)
    assert cfg_none.start_headers is None


def test_sync_cancel_failure_raises():
    session_transport = mock.create_autospec(requests.Session, instance=True)
    err_resp = mock.create_autospec(requests.Response, instance=True)
    err_resp.ok = False
    err_resp.status_code = 500
    err_resp.headers = {}
    err_resp.request = mock.Mock(method="POST", url="https://upload.example.com")
    err_resp.json.return_value = {"error": {"message": "Server Error", "errors": []}}
    session_transport.request.return_value = err_resp

    session = ResumableUploadSession(
        resumable_url="https://upload.example.com/resumable-123",
        transport=session_transport,
    )
    with pytest.raises(exceptions.GoogleAPICallError):
        session.cancel()


def test_sync_resume_chunk_size_override():
    session_transport = mock.create_autospec(requests.Session, instance=True)
    query_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-Size-Received": "0",
        },
    )
    chunk_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={"X-Goog-Upload-Status": "final"},
        content=b"done",
    )
    session_transport.request.side_effect = [query_resp, chunk_resp]

    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        transport=session_transport,
    )
    session.resume(
        upload_url="https://upload.example.com/resumable-123",
        stream=b"data",
        chunk_size=1024,
    )
    assert session.chunk_size == 1024


def test_sync_on_progress_and_capture():
    callback_mock = mock.Mock()
    config = ResumableUploadConfig(on_progress=callback_mock)
    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=config,
    )
    session._state._resumable_url = "https://api.example.com/init"
    with session._capture_progress() as captured:
        session._notify_progress(common.ProgressState.UPLOADING)
    assert len(captured) == 1
    assert captured[0].state == common.ProgressState.UPLOADING
    assert callback_mock.called
    assert callback_mock.call_args[0][0] is captured[0]


def test_sync_naive_deadline_tz():
    naive = datetime.datetime.now() + datetime.timedelta(hours=1)
    config = ResumableUploadConfig(deadline=naive)
    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=config,
    )
    rem = session._get_deadline_remaining()
    assert rem is not None and rem > 0
    assert session._get_start_timeout() <= rem


def test_sync_get_retry_start_and_fallback():
    ret_start = mock.Mock(spec=google.api_core.retry.Retry)
    ret_fallback = mock.Mock(spec=google.api_core.retry.Retry)
    config = ResumableUploadConfig(start_retry=ret_start, retry=ret_fallback)
    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=config,
    )
    assert session._get_retry(is_start=True) is ret_start
    assert session._get_retry() is ret_fallback


def test_sync_stall_control_with_deadline():
    import time

    # 1. compute_chunk_timeout with fallback timeout and stall control active
    config = ResumableUploadConfig(
        stall_minimum_rate=1024,
        stall_timeout=10.0,
        timeout=15.0,
    )
    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=config,
    )
    t1 = session._compute_chunk_timeout(512)
    assert t1 <= 15.0

    # 2. compute_chunk_timeout with deadline active
    config2 = ResumableUploadConfig(
        stall_minimum_rate=1024,
        stall_timeout=10.0,
        deadline=datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(seconds=5),
    )
    session2 = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=config2,
    )
    t2 = session2._compute_chunk_timeout(512)
    assert t2 <= 5.0

    # 3. update_stall_control raises DeadlineExceeded
    config3 = ResumableUploadConfig(
        stall_minimum_rate=1024,
        stall_timeout=10.0,
        deadline=datetime.datetime.now(datetime.timezone.utc)
        - datetime.timedelta(seconds=5),
    )
    session3 = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=config3,
    )
    with pytest.raises(exceptions.DeadlineExceeded):
        session3._update_stall_control(512, time.monotonic() - 15.0, 15.0)

    # 4. update_stall_control raises TransferStalledError (no deadline)
    config4 = ResumableUploadConfig(
        stall_minimum_rate=1024,
        stall_timeout=10.0,
    )
    session4 = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=config4,
    )
    session4._state._resumable_url = "https://api.example.com/init"
    with pytest.raises(exceptions.TransferStalledError):
        session4._update_stall_control(512, time.monotonic() - 15.0, 15.0)


def test_sync_update_stall_control_disabled():
    import time

    config = ResumableUploadConfig(stall_minimum_rate=0, stall_timeout=10.0)
    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=config,
    )
    session._update_stall_control(512, time.monotonic(), 5.0)
    assert session._aggregate_lag == 0.0


def test_sync_initiate_failure():
    transport = mock.create_autospec(requests.Session, instance=True)
    resp = mock.create_autospec(requests.Response, instance=True)
    resp.ok = False
    resp.status_code = 400
    resp.headers = {}
    resp.json.return_value = {"error": {"message": "Init Failed"}}
    resp.request = mock.Mock(method="POST", url="https://api.example.com/init")
    transport.request.return_value = resp

    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        transport=transport,
    )
    with pytest.raises(exceptions.GoogleAPICallError):
        session.initiate(transport=transport)


def test_sync_transmit_empty_stream():
    transport = mock.create_autospec(requests.Session, instance=True)
    resp = mock.create_autospec(requests.Response, instance=True)
    resp.ok = True
    resp.status_code = 200
    resp.headers = {"X-Goog-Upload-Status": "final"}
    resp.content = b"done"
    transport.request.return_value = resp

    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        transport=transport,
    )
    stream = io.BytesIO(b"")
    session._state._resumable_url = "https://upload.example.com/resumable-123"
    result = session._transmit_chunk(transport, stream, size=0)
    assert result is resp


def test_sync_transmit_chunk_timeout_with_stall_control_active():
    transport = mock.create_autospec(requests.Session, instance=True)
    transport.request.side_effect = requests.exceptions.Timeout("Read timeout")

    config = ResumableUploadConfig(
        stall_minimum_rate=1024,
        stall_timeout=10.0,
    )
    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=config,
        transport=transport,
    )
    session._state._resumable_url = "https://upload.example.com/resumable-123"

    with pytest.raises(exceptions.TransferStalledError):
        session._transmit_chunk(transport, io.BytesIO(b"data"), size=4)

    config_dl = ResumableUploadConfig(
        stall_minimum_rate=1024,
        stall_timeout=10.0,
        deadline=datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(seconds=5),
    )
    session_dl = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=config_dl,
        transport=transport,
    )
    session_dl._state._resumable_url = "https://upload.example.com/resumable-123"
    session_dl._get_deadline_remaining = mock.Mock(side_effect=[5.0, -1.0])
    with pytest.raises(exceptions.DeadlineExceeded):
        session_dl._transmit_chunk(transport, io.BytesIO(b"data"), size=4)


def test_sync_transmit_chunk_timeout_outer_exception():
    transport = mock.create_autospec(requests.Session, instance=True)
    transport.request.side_effect = requests.exceptions.Timeout("Read timeout")

    config = ResumableUploadConfig(
        stall_minimum_rate=0,
        retry=google.api_core.retry.Retry(predicate=lambda e: False),
    )
    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=config,
        transport=transport,
    )
    session._state._resumable_url = "https://upload.example.com/resumable-123"
    with pytest.raises(exceptions.TransferStalledError):
        session._transmit_chunk(transport, io.BytesIO(b"data"), size=4)

    # To hit line 554-558 (outer exception handler with elapsed deadline)
    config_dl = ResumableUploadConfig(
        stall_minimum_rate=0,
        deadline=datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(seconds=5),
        retry=google.api_core.retry.Retry(predicate=lambda e: False),
    )
    session_dl = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=config_dl,
        transport=transport,
    )
    session_dl._state._resumable_url = "https://upload.example.com/resumable-123"
    session_dl._get_deadline_remaining = mock.Mock(side_effect=[5.0, -1.0])
    with pytest.raises(exceptions.DeadlineExceeded):
        session_dl._transmit_chunk(transport, io.BytesIO(b"data"), size=4)


def test_sync_recover_failure():
    transport = mock.create_autospec(requests.Session, instance=True)
    resp = mock.create_autospec(requests.Response, instance=True)
    resp.ok = False
    resp.status_code = 400
    resp.headers = {}
    resp.json.return_value = {"error": {"message": "Recovery Failed"}}
    resp.request = mock.Mock(
        method="POST", url="https://upload.example.com/resumable-123"
    )
    transport.request.return_value = resp

    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        transport=transport,
    )
    session._state._resumable_url = "https://upload.example.com/resumable-123"
    with pytest.raises(exceptions.GoogleAPICallError):
        session._recover(transport, io.BytesIO(b"data"))


def test_sync_transmit_all_chunks_completed_without_response():
    transport = mock.create_autospec(requests.Session, instance=True)
    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        transport=transport,
    )
    session._state._finished = True
    with pytest.raises(
        ValueError, match="Upload completed without receiving a final response"
    ):
        list(session._transmit_all_chunks(transport, io.BytesIO(b"data"), 4))


def test_sync_iter_resume_errors():
    transport = mock.create_autospec(requests.Session, instance=True)
    session = ResumableUploadSession(transport=transport)
    with pytest.raises(ValueError, match="An upload URL must be provided to resume"):
        list(session.iter_resume(upload_url=None, stream=b"data"))

    with pytest.raises(
        ValueError, match="A data stream or payload must be provided to resume"
    ):
        list(
            session.iter_resume(upload_url="https://api.example.com/init", stream=None)
        )


def test_sync_prepare_stream_tell_error():
    class TellFailingStream(io.BytesIO):
        def tell(self) -> int:
            raise OSError("Tell failed")

    session = ResumableUploadSession()
    stream = TellFailingStream(b"data")
    stream_obj, computed_size = session._prepare_stream(stream, None)
    assert session._start_stream_offset == 0


def test_sync_format_response_payload_custom_inputs():
    from google.api_core.resumable_transfer.upload import _format_response_payload

    class CustomBytesConvertible:
        def __bytes__(self) -> bytes:
            return b"custom_bytes"

    res = _format_response_payload(CustomBytesConvertible(), response_type=None)
    assert isinstance(res, CustomBytesConvertible)

    res_parsed = _format_response_payload(
        CustomBytesConvertible(), response_type=lambda x: x + b"_extra"
    )
    assert res_parsed == b"custom_bytes_extra"

    from google.protobuf import empty_pb2

    msg_instance = empty_pb2.Empty()
    res_msg = _format_response_payload(b"{}", response_type=msg_instance)
    assert isinstance(res_msg, empty_pb2.Empty)
