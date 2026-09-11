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

"""Asynchronous tests for Resumable Upload protocol implementation."""

import asyncio
import datetime
import io
import json
from typing import Any, AsyncIterator, Dict, List, Mapping, Optional, Tuple, Union
from unittest import mock

import pytest

try:
    import aiohttp  # noqa: F401
    import google.auth.aio.transport  # noqa: F401

    GOOGLE_AUTH_AIO_INSTALLED = True
except ImportError:
    GOOGLE_AUTH_AIO_INSTALLED = False


@pytest.fixture(autouse=True)
def check_async_rest_installed(request: pytest.FixtureRequest) -> None:
    if request.node.name == "test_async_ensure_aiohttp_missing":
        return
    if not GOOGLE_AUTH_AIO_INSTALLED:
        pytest.skip("Skipped because google-api-core[async_rest] is not installed")


import proto
from google.protobuf import empty_pb2

from google.api_core import exceptions
from google.api_core.resumable_transfer import (
    AsyncResumableUploadSession,
    AsyncUploadOperation,
    MissingStatusHeaderError,
    ProgressState,
    ResumableUploadConfig,
    TransferStalledError,
    UnseekableStreamError,
    UploadCancelledError,
    UploadProgress,
    common,
    upload_async,
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
        d = json.loads(data.decode("utf-8") if isinstance(data, bytes) else data)
        return cls(name=d.get("name", ""), size=d.get("size", 0))


class DummyAsyncResponse:
    """Mock HTTP response conforming to aiohttp.ClientResponse interface."""

    def __init__(
        self,
        status: int = 200,
        headers: Optional[Mapping[str, str]] = None,
        body: bytes = b"",
    ) -> None:
        """Initializes a DummyAsyncResponse.

        Args:
            status: HTTP status code.
            headers: HTTP response headers mapping.
            body: Response payload bytes.
        """
        self.status = status
        self.headers = headers or {}
        self._body = body

    async def read(self) -> bytes:
        """Reads and returns response payload bytes.

        Returns:
            Raw response payload bytes.
        """
        return self._body

    async def __aenter__(self) -> "DummyAsyncResponse":
        """Enters the asynchronous context manager.

        Returns:
            The DummyAsyncResponse instance.
        """
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exits the asynchronous context manager.

        Args:
            exc_type: Exception type if raised.
            exc_val: Exception value if raised.
            exc_tb: Exception traceback if raised.
        """
        pass


class DummyAsyncSession:
    """Mock asynchronous HTTP client session conforming to aiohttp.ClientSession interface."""

    def __init__(self, responses: Optional[List[DummyAsyncResponse]] = None) -> None:
        """Initializes a DummyAsyncSession.

        Args:
            responses: Sequence of canned DummyAsyncResponse objects.
        """
        self._responses: List[DummyAsyncResponse] = list(responses or [])
        self.requests: List[Tuple[str, str, Dict[str, Any]]] = []

    def request(self, method: str, url: str, **kwargs: Any) -> DummyAsyncResponse:
        """Records the request and yields the next canned response.

        Args:
            method: HTTP method verb.
            url: Destination endpoint URL.
            **kwargs: Additional request parameters.

        Returns:
            Next canned DummyAsyncResponse.
        """
        self.requests.append((method, url, kwargs))
        if not self._responses:
            return DummyAsyncResponse(status=200, headers={}, body=b"")
        return self._responses.pop(0)


class NonSeekableBytesIO(io.BytesIO):
    """BytesIO stream simulation with seekable returning False."""

    def seekable(self) -> bool:
        """Reports whether the stream supports random access.

        Returns:
            False unconditionally.
        """
        return False


# =====================================================================
# 1. Initialization and Configuration Tests
# =====================================================================


def test_async_session_initialization_defaults() -> None:
    """Validates default attribute values of an uninitiated async session."""
    session = AsyncResumableUploadSession(upload_url="https://api.example.com/start")
    assert session.upload_url is None
    assert session.chunk_size == common.DEFAULT_CHUNK_SIZE
    assert session.response is None
    assert session.bytes_uploaded == 0
    assert session.finished is False


def test_async_missing_transport_raises() -> None:
    """Verifies that invoking session operations without a transport raises ValueError."""
    session = AsyncResumableUploadSession()

    with pytest.raises(ValueError, match="aiohttp.ClientSession"):
        session.upload(stream=b"data")

    with pytest.raises(ValueError, match="aiohttp.ClientSession"):
        session.resume(upload_url="https://upload.example.com", stream=b"data")


@pytest.mark.asyncio
async def test_async_cancel_missing_transport_raises() -> None:
    """Verifies that cancel without a transport raises ValueError."""
    session = AsyncResumableUploadSession()
    with pytest.raises(ValueError, match="aiohttp.ClientSession"):
        await session.cancel()


def test_async_ensure_aiohttp_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verifies that _ensure_aiohttp raises ImportError when aiohttp is unavailable."""
    monkeypatch.setattr(upload_async, "aiohttp", None)
    session = AsyncResumableUploadSession()
    with pytest.raises(ImportError, match="google-api-core\\[async_rest\\]"):
        session._ensure_aiohttp()


# =====================================================================
# 2. Upload Execution and Operation Handle Tests
# =====================================================================


@pytest.mark.asyncio
async def test_async_upload_direct_execution() -> None:
    """Verifies single-chunk upload execution with protobuf deserialization."""
    start_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-async",
        },
        body=b"",
    )
    chunk_resp = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "final"},
        body=b'{"name": "async_file.txt", "size": 10}',
    )

    async_transport = DummyAsyncSession([start_resp, chunk_resp])
    config = ResumableUploadConfig(response_type=DummyResponse)
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=config,
        transport=async_transport,
    )

    result = await session.upload(stream=b"0123456789", request_body='{"name": "test"}')

    assert isinstance(result, DummyResponse)
    assert result.name == "async_file.txt"
    assert result.size == 10
    assert session.finished is True
    assert session.bytes_uploaded == 10
    assert session.upload_url == "https://upload.example.com/resumable-async"


@pytest.mark.asyncio
async def test_async_upload_multi_chunk_operation_handle() -> None:
    """Verifies multi-chunk upload dispatching and AsyncUploadOperation property handles."""
    start_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-async",
        },
        body=b"",
    )
    chunk1_resp = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "active"},
        body=b"",
    )
    chunk2_resp = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "final"},
        body=b'{"name": "multi.txt", "size": 8}',
    )

    async_transport = DummyAsyncSession([start_resp, chunk1_resp, chunk2_resp])
    config = ResumableUploadConfig(chunk_size=4, response_type=DummyResponse)
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=config,
        transport=async_transport,
    )

    upload_op = session.upload(stream=b"12345678")
    assert isinstance(upload_op, AsyncUploadOperation)
    assert upload_op.chunk_size == 4

    result = await upload_op
    assert isinstance(result, DummyResponse)
    assert result.name == "multi.txt"
    assert upload_op.response == result
    assert upload_op.bytes_uploaded == 8
    assert upload_op.upload_url == "https://upload.example.com/resumable-async"

    # Validate commands dispatched in request history
    assert len(async_transport.requests) == 3
    # Start request
    assert async_transport.requests[0][2]["headers"]["X-Goog-Upload-Command"] == "start"
    # Chunk 1 request
    assert (
        async_transport.requests[1][2]["headers"]["X-Goog-Upload-Command"] == "upload"
    )
    assert async_transport.requests[1][2]["headers"]["X-Goog-Upload-Offset"] == "0"
    # Chunk 2 request (last chunk concludes transfer)
    assert (
        async_transport.requests[2][2]["headers"]["X-Goog-Upload-Command"]
        == "upload, finalize"
    )
    assert async_transport.requests[2][2]["headers"]["X-Goog-Upload-Offset"] == "4"


@pytest.mark.asyncio
async def test_async_upload_progress_tracking() -> None:
    """Verifies that progress stream yields snapshots matching transmission milestones."""
    start_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-async",
        },
        body=b"",
    )
    chunk1_resp = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "active"},
        body=b"",
    )
    chunk2_resp = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "final"},
        body=b'{"name": "progress.txt", "size": 8}',
    )

    async_transport = DummyAsyncSession([start_resp, chunk1_resp, chunk2_resp])
    config = ResumableUploadConfig(chunk_size=4, response_type=DummyResponse)
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=config,
        transport=async_transport,
    )

    upload_op = session.upload(stream=b"12345678")
    progress_list: List[UploadProgress] = []
    async for p in upload_op.progress():
        progress_list.append(p)

    final_resp = await upload_op
    assert isinstance(final_resp, DummyResponse)
    assert len(progress_list) == 3
    assert progress_list[0].state == ProgressState.STARTED
    assert progress_list[1].state == ProgressState.UPLOADING
    assert progress_list[1].bytes_uploaded == 4
    assert progress_list[2].state == ProgressState.FINALIZED
    assert progress_list[2].bytes_uploaded == 8


# =====================================================================
# 3. Stream Input Types Tests
# =====================================================================


@pytest.mark.asyncio
async def test_async_stream_types_async_iterable() -> None:
    """Verifies upload compatibility with an asynchronous generator stream."""
    start_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-async",
        },
        body=b"",
    )
    chunk_resp = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "final"},
        body=b'{"name": "async_gen.txt", "size": 6}',
    )

    async_transport = DummyAsyncSession([start_resp, chunk_resp])

    async def async_generator() -> AsyncIterator[bytes]:
        yield b"abc"
        yield b"def"

    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=ResumableUploadConfig(response_type=DummyResponse),
        transport=async_transport,
    )

    resp = await session.upload(stream=async_generator())
    assert resp.name == "async_gen.txt"
    assert session.bytes_uploaded == 6


@pytest.mark.asyncio
async def test_async_stream_types_binary_io() -> None:
    """Verifies upload compatibility with a seekable BinaryIO stream."""
    start_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-async",
        },
        body=b"",
    )
    chunk_resp = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "final"},
        body=b'{"name": "bytes_io.txt", "size": 5}',
    )

    async_transport = DummyAsyncSession([start_resp, chunk_resp])
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=ResumableUploadConfig(response_type=DummyResponse),
        transport=async_transport,
    )

    stream = io.BytesIO(b"hello")
    resp = await session.upload(stream=stream)
    assert resp.name == "bytes_io.txt"
    assert session.bytes_uploaded == 5


@pytest.mark.asyncio
async def test_async_stream_types_sync_iterable() -> None:
    """Verifies upload compatibility with a synchronous iterable of byte chunks."""
    start_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-async",
        },
        body=b"",
    )
    chunk_resp = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "final"},
        body=b'{"name": "iterable.txt", "size": 6}',
    )

    async_transport = DummyAsyncSession([start_resp, chunk_resp])
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=ResumableUploadConfig(response_type=DummyResponse),
        transport=async_transport,
    )

    resp = await session.upload(stream=[b"foo", b"bar"])
    assert resp.name == "iterable.txt"
    assert session.bytes_uploaded == 6


def test_async_stream_types_unsupported_raises() -> None:
    """Verifies that passing an unsupported stream type raises TypeError."""
    session = AsyncResumableUploadSession(transport=DummyAsyncSession())
    with pytest.raises(TypeError, match="Unsupported stream type"):
        session._prepare_async_reader(stream=12345, size=10)  # type: ignore


# =====================================================================
# 4. Resume and Offset Recovery Tests
# =====================================================================


@pytest.mark.asyncio
async def test_async_resume_success() -> None:
    """Verifies resuming an existing upload by querying server offset."""
    query_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-Size-Received": "5",
        },
        body=b"",
    )
    chunk_resp = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "final"},
        body=b'{"name": "resumed_async.txt", "size": 10}',
    )

    async_transport = DummyAsyncSession([query_resp, chunk_resp])
    session = AsyncResumableUploadSession(
        config=ResumableUploadConfig(response_type=DummyResponse),
        transport=async_transport,
    )

    upload_op = session.resume(
        upload_url="https://upload.example.com/resumable-async",
        stream=b"0123456789",
    )
    resp = await upload_op
    assert resp.name == "resumed_async.txt"
    assert session.bytes_uploaded == 10
    assert session.finished is True

    # First request was query
    assert async_transport.requests[0][2]["headers"]["X-Goog-Upload-Command"] == "query"
    # Second request was remaining chunk starting from offset 5
    assert async_transport.requests[1][2]["headers"]["X-Goog-Upload-Offset"] == "5"


@pytest.mark.asyncio
async def test_async_resume_recovery_unseekable_stream_raises() -> None:
    """Verifies that UnseekableStreamError is raised if server offset cannot be rewound."""
    query_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-Size-Received": "100",
        },
        body=b"",
    )

    async_transport = DummyAsyncSession([query_resp])
    session = AsyncResumableUploadSession(
        config=ResumableUploadConfig(response_type=DummyResponse),
        transport=async_transport,
    )

    stream = NonSeekableBytesIO(b"some content")
    upload_op = session.resume(
        upload_url="https://upload.example.com/resumable-async",
        stream=stream,
    )

    with pytest.raises(UnseekableStreamError) as exc_info:
        await upload_op

    assert exc_info.value.upload_url == "https://upload.example.com/resumable-async"


@pytest.mark.asyncio
async def test_async_resume_recovery_seekable_stream() -> None:
    """Verifies that seekable streams are rewound to committed server offset."""
    query_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-Size-Received": "3",
        },
        body=b"",
    )
    chunk_resp = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "final"},
        body=b'{"name": "seekable.txt", "size": 6}',
    )

    async_transport = DummyAsyncSession([query_resp, chunk_resp])
    session = AsyncResumableUploadSession(
        config=ResumableUploadConfig(response_type=DummyResponse),
        transport=async_transport,
    )

    stream = io.BytesIO(b"abcdef")
    upload_op = session.resume(
        upload_url="https://upload.example.com/resumable-async",
        stream=stream,
    )
    resp = await upload_op
    assert resp.name == "seekable.txt"
    assert session.bytes_uploaded == 6


# =====================================================================
# 5. Cancellation Tests
# =====================================================================


@pytest.mark.asyncio
async def test_async_cancel_success() -> None:
    """Verifies client-initiated cancellation marks session state invalid."""
    cancel_resp = DummyAsyncResponse(status=200, headers={}, body=b"")
    async_transport = DummyAsyncSession([cancel_resp])

    session = AsyncResumableUploadSession(
        resumable_url="https://upload.example.com/resumable-async",
        transport=async_transport,
    )
    await session.cancel()
    assert session._state.invalid is True
    assert (
        async_transport.requests[0][2]["headers"]["X-Goog-Upload-Command"] == "cancel"
    )


@pytest.mark.asyncio
async def test_async_server_cancelled_raises_error() -> None:
    """Verifies that server returning cancelled status raises UploadCancelledError."""
    start_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-async",
        },
        body=b"",
    )
    chunk_resp = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "cancelled"},
        body=b"",
    )

    async_transport = DummyAsyncSession([start_resp, chunk_resp])
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        transport=async_transport,
    )

    with pytest.raises(UploadCancelledError, match="cancelled by server"):
        await session.upload(stream=b"12345")


# =====================================================================
# 6. Retry and Error Handling Tests
# =====================================================================


@pytest.mark.asyncio
async def test_async_retry_transient_http_errors() -> None:
    """Verifies transparent retries on transient HTTP status codes (503 Service Unavailable)."""
    start_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-async",
        },
        body=b"",
    )
    chunk_503 = DummyAsyncResponse(status=503, headers={}, body=b"Service Unavailable")
    chunk_success = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "final"},
        body=b'{"name": "retried.txt", "size": 5}',
    )

    async_transport = DummyAsyncSession([start_resp, chunk_503, chunk_success])
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=ResumableUploadConfig(response_type=DummyResponse),
        transport=async_transport,
    )

    with mock.patch("asyncio.sleep", new_callable=mock.AsyncMock):
        resp = await session.upload(stream=b"hello")

    assert resp.name == "retried.txt"
    assert session.finished is True


@pytest.mark.asyncio
async def test_async_non_retryable_error_raises() -> None:
    """Verifies that non-retryable errors (e.g. 404 Not Found) terminate immediately."""
    start_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-async",
        },
        body=b"",
    )
    chunk_404 = DummyAsyncResponse(status=404, headers={}, body=b"Not Found")

    async_transport = DummyAsyncSession([start_resp, chunk_404])
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        transport=async_transport,
    )

    with pytest.raises(exceptions.NotFound):
        await session.upload(stream=b"test")


@pytest.mark.asyncio
async def test_async_recoverable_status_code_triggers_recovery() -> None:
    """Verifies that recoverable error status codes trigger query and offset reconciliation."""
    start_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-async",
        },
        body=b"",
    )
    # Chunk 1 returns 409 Conflict
    chunk_conflict = DummyAsyncResponse(status=409, headers={}, body=b"Conflict")
    # Recovery query returns confirmed committed offset 0
    query_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-Size-Received": "0",
        },
        body=b"",
    )
    # Retransmission succeeds
    chunk_success = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "final"},
        body=b'{"name": "recovered.txt", "size": 5}',
    )

    async_transport = DummyAsyncSession(
        [start_resp, chunk_conflict, query_resp, chunk_success]
    )
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=ResumableUploadConfig(response_type=DummyResponse),
        transport=async_transport,
    )

    with mock.patch("asyncio.sleep", new_callable=mock.AsyncMock):
        resp = await session.upload(stream=b"hello")

    assert resp.name == "recovered.txt"
    assert session.bytes_uploaded == 5


@pytest.mark.asyncio
async def test_async_missing_status_header_triggers_recovery() -> None:
    """Verifies that missing status header triggers query recovery."""
    start_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-async",
        },
        body=b"",
    )
    # Successful HTTP status but missing X-Goog-Upload-Status header
    chunk_missing_hdr = DummyAsyncResponse(status=200, headers={}, body=b"")
    # Recovery query
    query_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-Size-Received": "0",
        },
        body=b"",
    )
    chunk_success = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "final"},
        body=b'{"name": "header_recovered.txt", "size": 5}',
    )

    async_transport = DummyAsyncSession(
        [start_resp, chunk_missing_hdr, query_resp, chunk_success]
    )
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=ResumableUploadConfig(response_type=DummyResponse),
        transport=async_transport,
    )

    with mock.patch("asyncio.sleep", new_callable=mock.AsyncMock):
        resp = await session.upload(stream=b"hello")

    assert resp.name == "header_recovered.txt"


# =====================================================================
# 7. Stall Control and Deadline Tests
# =====================================================================


@pytest.mark.asyncio
async def test_async_stall_timeout_raises_transfer_stalled_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verifies that transfer stalling beyond timeout threshold raises TransferStalledError."""
    start_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-async",
        },
        body=b"",
    )
    chunk_resp = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "final"},
        body=b'{"name": "slow.txt", "size": 10}',
    )

    async_transport = DummyAsyncSession([start_resp, chunk_resp])
    # Expect 100 bytes/sec, timeout 1 second
    config = ResumableUploadConfig(stall_minimum_rate=100, stall_timeout=1.0)
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=config,
        transport=async_transport,
    )

    # Simulate elapsed time 10.0 seconds during 10-byte upload (rate = 1 byte/s < 100)
    clock_vals = iter([0.0, 10.0, 10.0, 10.0])
    monkeypatch.setattr(upload_async, "_monotonic_clock", lambda: next(clock_vals))

    with pytest.raises(TransferStalledError, match="Upload stalled"):
        await session.upload(stream=b"0123456789")


@pytest.mark.asyncio
async def test_async_deadline_exceeded() -> None:
    """Verifies that exceeding the configured upload deadline raises DeadlineExceeded."""
    start_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-async",
        },
        body=b"",
    )
    async_transport = DummyAsyncSession([start_resp])
    past_deadline = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
        seconds=10
    )
    config = ResumableUploadConfig(deadline=past_deadline)
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=config,
        transport=async_transport,
    )

    with pytest.raises(exceptions.DeadlineExceeded):
        await session.upload(stream=b"data")


# =====================================================================
# 8. Response Deserialization Types Tests
# =====================================================================


@pytest.mark.asyncio
async def test_async_response_type_proto_message() -> None:
    """Verifies that a proto.Message type parses final response bytes."""
    start_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-async",
        },
        body=b"",
    )
    chunk_resp = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "final"},
        body=b'{"content": "proto_async_payload"}',
    )

    async_transport = DummyAsyncSession([start_resp, chunk_resp])
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=ResumableUploadConfig(response_type=EchoResponse),
        transport=async_transport,
    )

    result = await session.upload(stream=b"data")
    assert isinstance(result, EchoResponse)
    assert result.content == "proto_async_payload"


@pytest.mark.asyncio
async def test_async_response_type_protobuf_message() -> None:
    """Verifies that a google.protobuf.message.Message type parses final response bytes."""
    start_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-async",
        },
        body=b"",
    )
    chunk_resp = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "final"},
        body=b"{}",
    )

    async_transport = DummyAsyncSession([start_resp, chunk_resp])
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=ResumableUploadConfig(response_type=empty_pb2.Empty),
        transport=async_transport,
    )

    result = await session.upload(stream=b"data")
    assert isinstance(result, empty_pb2.Empty)


@pytest.mark.asyncio
async def test_async_response_type_callable() -> None:
    """Verifies that a custom callable deserializer parses final response body bytes."""
    if not GOOGLE_AUTH_AIO_INSTALLED:
        pytest.skip("Skipped because google-api-core[async_rest] is not installed")

    start_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-async",
        },
        body=b"",
    )
    chunk_resp = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "final"},
        body=b"parsed:hello",
    )

    async_transport = DummyAsyncSession([start_resp, chunk_resp])

    def custom_parser(raw: bytes) -> str:
        return raw.decode("utf-8").upper()

    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=ResumableUploadConfig(response_type=custom_parser),
        transport=async_transport,
    )

    result = await session.upload(stream=b"data")
    assert result == "PARSED:HELLO"


@pytest.mark.asyncio
async def test_async_response_type_raw_bytes() -> None:
    """Verifies that raw bytes are returned when response_type is not configured."""
    start_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-async",
        },
        body=b"",
    )
    chunk_resp = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "final"},
        body=b"raw-bytes-output",
    )

    async_transport = DummyAsyncSession([start_resp, chunk_resp])
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        transport=async_transport,
    )

    result = await session.upload(stream=b"data")
    assert result == b"raw-bytes-output"


@pytest.mark.asyncio
async def test_async_operation_error_propagation_in_progress() -> None:
    """Verifies that background task errors propagate through progress queue iteration."""
    start_resp = DummyAsyncResponse(
        status=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/resumable-async",
        },
        body=b"",
    )
    chunk_resp = DummyAsyncResponse(
        status=403,
        headers={},
        body=b"Permission Denied",
    )

    async_transport = DummyAsyncSession([start_resp, chunk_resp])
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        transport=async_transport,
    )

    upload_op = session.upload(stream=b"data")
    with pytest.raises(exceptions.Forbidden):
        async for _ in upload_op.progress():
            pass

    with pytest.raises(exceptions.Forbidden):
        await upload_op
