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
import time
from typing import (
    Any,
    AsyncIterable,
    AsyncIterator,
    Dict,
    List,
    Mapping,
    Optional,
    Tuple,
    Union,
)
from unittest import mock

import pytest
from google.protobuf import empty_pb2

from google.api_core import exceptions
from google.api_core.resumable_transfer import (
    AsyncResumableUploadSession,
    AsyncUploadOperation,
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


@pytest.mark.parametrize("invalid_stream", ["invalid_string", {"key": "value"}, 12345])
def test_async_upload_rejects_invalid_stream_types(invalid_stream: Any) -> None:
    """Verifies that str, dict, and non-stream objects raise TypeError synchronously on upload()."""
    async_transport = DummyAsyncSession([])
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        transport=async_transport,
    )
    with pytest.raises(TypeError, match="Unsupported stream type"):
        session.upload(stream=invalid_stream)


@pytest.mark.parametrize("invalid_stream", ["invalid_string", {"key": "value"}, 12345])
def test_async_resume_rejects_invalid_stream_types(invalid_stream: Any) -> None:
    """Verifies that str, dict, and non-stream objects raise TypeError synchronously on resume()."""
    async_transport = DummyAsyncSession([])
    session = AsyncResumableUploadSession(
        transport=async_transport,
    )
    with pytest.raises(TypeError, match="Unsupported stream type"):
        session.resume(
            upload_url="https://upload.example.com/resumable-async",
            stream=invalid_stream,
        )


def test_async_enrich_exception_without_dict() -> None:
    """Verifies that _enrich_exception handles objects without __dict__."""
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
    )
    exc = Exception()
    session._enrich_exception(exc)


def test_async_notify_progress_branches() -> None:
    """Verifies progress notification callbacks and queues."""
    called = []
    config = ResumableUploadConfig(on_progress=lambda p: called.append(p))
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=config,
    )
    # When upload_url is established on state
    session._state._resumable_url = "https://upload.example.com/resumable-async"
    q: asyncio.Queue = asyncio.Queue()
    session._notify_progress(common.ProgressState.UPLOADING, queue=q)
    assert len(called) == 1
    assert q.qsize() == 1


def test_async_deadline_handling_and_start_timeout() -> None:
    """Verifies deadline remaining calculations and start timeout calculation."""
    # Past deadline raises DeadlineExceeded
    past = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=10)
    config = ResumableUploadConfig(deadline=past)
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=config,
    )
    with pytest.raises(exceptions.DeadlineExceeded):
        session._get_deadline_remaining()

    # Naive future deadline is localized to UTC
    future_naive = datetime.datetime.now() + datetime.timedelta(hours=1)
    config2 = ResumableUploadConfig(deadline=future_naive)
    session2 = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        config=config2,
    )
    rem = session2._get_deadline_remaining()
    assert rem is not None and rem > 0
    t = session2._get_start_timeout()
    assert t > 0


@pytest.mark.asyncio
async def test_async_retry_branches() -> None:
    """Verifies retry predicate branches in _async_retry."""
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
    )

    # MissingStatusHeaderError retries and raises on final attempt
    attempts = 0

    async def fail_missing_header():
        nonlocal attempts
        attempts += 1
        raise exceptions.MissingStatusHeaderError("missing")

    with pytest.raises(exceptions.MissingStatusHeaderError):
        await session._async_retry(fail_missing_header, max_attempts=2)
    assert attempts == 2

    # Non-retryable GoogleAPICallError raises immediately
    async def fail_400():
        raise exceptions.from_http_status(400, "Bad Request")

    with pytest.raises(exceptions.BadRequest):
        await session._async_retry(fail_400, max_attempts=3)

    # Retryable GoogleAPICallError retries and raises on final attempt
    attempts_503 = 0

    async def fail_503():
        nonlocal attempts_503
        attempts_503 += 1
        raise exceptions.from_http_status(503, "Service Unavailable")

    with pytest.raises(exceptions.ServiceUnavailable):
        await session._async_retry(fail_503, max_attempts=2)
    assert attempts_503 == 2


def test_async_transport_missing_errors() -> None:
    """Verifies ValueError when transport is missing from upload, resume, and cancel."""
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
    )
    with pytest.raises(
        ValueError, match="An aiohttp.ClientSession transport must be provided"
    ):
        session.upload(stream=b"data")

    with pytest.raises(
        ValueError, match="An aiohttp.ClientSession transport must be provided"
    ):
        session.resume(upload_url="https://upload.example.com/123", stream=b"data")


@pytest.mark.asyncio
async def test_async_cancel_missing_transport_and_error() -> None:
    """Verifies cancel method with missing transport and server error."""
    session = AsyncResumableUploadSession(
        resumable_url="https://upload.example.com/123",
    )
    with pytest.raises(
        ValueError, match="An aiohttp.ClientSession transport must be provided"
    ):
        await session.cancel()

    err_resp = DummyAsyncResponse(status=500, headers={}, body=b"Cancel Error")
    sess_transport = DummyAsyncSession([err_resp])
    session2 = AsyncResumableUploadSession(
        resumable_url="https://upload.example.com/123",
        transport=sess_transport,
    )
    with pytest.raises(exceptions.GoogleAPICallError):
        await session2.cancel()


@pytest.mark.asyncio
async def test_async_prepare_async_reader_types() -> None:
    """Verifies async reader preparation for native async reader, tell error, and iterables."""
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
    )

    class AsyncReader(AsyncIterable[bytes]):  # Inherit to satisfy mypy
        async def read(self, n: int) -> bytes:
            return b"chunk"

        async def __aiter__(self) -> AsyncIterator[bytes]:
            yield b"chunk"

    reader_fn, size, obj = session._prepare_async_reader(AsyncReader(), None)
    chunk = await reader_fn(5)
    assert chunk == b"chunk"

    # Sync stream whose tell() raises OSError
    class TellFailingStream(io.BytesIO):
        def tell(self) -> int:
            raise OSError("tell error")

    stream = TellFailingStream(b"data")
    reader_fn2, size2, obj2 = session._prepare_async_reader(stream, None)
    chunk2 = await reader_fn2(4)
    assert chunk2 == b"data"
    assert session._start_stream_offset == 0

    # Sync Iterable[bytes]
    reader_fn3, size3, obj3 = session._prepare_async_reader([b"part1", b"part2"], None)
    chunk3 = await reader_fn3(10)
    assert chunk3 == b"part1part2"


@pytest.mark.asyncio
async def test_async_initiate_and_recover_failures() -> None:
    """Verifies initiate and recover error handling when server returns error codes."""
    err_resp = DummyAsyncResponse(status=400, headers={}, body=b"Bad Request")
    sess_transport = DummyAsyncSession([err_resp])
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        transport=sess_transport,
    )
    with pytest.raises(exceptions.BadRequest):
        await session.initiate(transport=sess_transport)

    err_resp2 = DummyAsyncResponse(status=400, headers={}, body=b"Query Failed")
    sess_transport2 = DummyAsyncSession([err_resp2])
    session2 = AsyncResumableUploadSession(
        transport=sess_transport2,
    )
    session2._state._resumable_url = "https://upload.example.com/123"
    with pytest.raises(exceptions.BadRequest):
        await session2._recover(sess_transport2)


@pytest.mark.asyncio
async def test_async_recover_stream_errors() -> None:
    """Verifies UnseekableStreamError during async recovery."""
    query_resp = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "active", "X-Goog-Upload-Size-Received": "10"},
        body=b"",
    )
    sess_transport = DummyAsyncSession([query_resp])
    session = AsyncResumableUploadSession(
        transport=sess_transport,
    )
    session._state._resumable_url = "https://upload.example.com/123"

    # Stream whose seekable() returns False
    unseekable = mock.Mock()
    unseekable.seekable.return_value = False
    with pytest.raises(UnseekableStreamError, match="Stream is not seekable"):
        await session._recover(sess_transport, stream_obj=unseekable)

    # Stream whose seek() raises OSError
    sess_transport2 = DummyAsyncSession([query_resp])
    session2 = AsyncResumableUploadSession(
        transport=sess_transport2,
    )
    session2._state._resumable_url = "https://upload.example.com/123"
    failing_seek = mock.Mock()
    failing_seek.seekable.return_value = True
    failing_seek.seek.side_effect = OSError("Seek error")
    with pytest.raises(UnseekableStreamError, match="Failed to seek stream"):
        await session2._recover(sess_transport2, stream_obj=failing_seek)


@pytest.mark.asyncio
async def test_async_operation_cancel_and_base_exception() -> None:
    """Verifies op.cancel() cancels background task and propagates to progress()."""
    # 1. upload cancel
    class SlowResponse(DummyAsyncResponse):
        async def __aenter__(self):
            await asyncio.sleep(10.0)
            return self

    class SlowSession:
        def request(self, *args, **kwargs):
            return SlowResponse(200, {}, b"")

    slow_session_transport = SlowSession()

    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/start",
        transport=slow_session_transport,
    )
    op = session.upload(stream=b"data")
    await asyncio.sleep(0.01)
    op.cancel()
    with pytest.raises(asyncio.CancelledError):
        await op

    with pytest.raises(asyncio.CancelledError):
        async for _ in op.progress():
            pass

    # 2. resume cancel
    session_resume = AsyncResumableUploadSession(
        transport=slow_session_transport,
    )
    op_resume = session_resume.resume(
        upload_url="https://upload.example.com/resumable-123",
        stream=b"data",
        chunk_size=1024,
    )
    assert session_resume.chunk_size == 1024
    await asyncio.sleep(0.01)
    op_resume.cancel()
    with pytest.raises(asyncio.CancelledError):
        await op_resume

    with pytest.raises(asyncio.CancelledError):
        async for _ in op_resume.progress():
            pass


def test_async_notify_progress_edge_cases() -> None:
    """Verifies _notify_progress when upload_url is None and target_queue is None."""
    session = AsyncResumableUploadSession()
    session._notify_progress(common.ProgressState.STARTED)

    session_with_url = AsyncResumableUploadSession(resumable_url="https://upload.example.com/1")
    session_with_url._notify_progress(common.ProgressState.STARTED, progress_queue=None, queue=None)


def test_async_predicate_branches() -> None:
    """Verifies all branches of _get_retry_predicate and _get_streaming_predicate."""
    session = AsyncResumableUploadSession(upload_url="https://api.example.com/start")
    retry_pred = session._get_retry_predicate()
    stream_pred = session._get_streaming_predicate()

    assert retry_pred(exceptions.MissingStatusHeaderError("missing")) is True
    assert retry_pred(asyncio.TimeoutError()) is True
    assert retry_pred(aiohttp.ClientConnectionError("conn")) is True
    assert retry_pred(ValueError("other")) is False

    assert stream_pred(asyncio.TimeoutError()) is True
    assert stream_pred(aiohttp.ClientConnectionError("conn")) is True
    assert stream_pred(ValueError("other")) is False


def test_async_retry_configuration_conversions() -> None:
    """Verifies _get_async_retry and _get_async_streaming_retry conversions."""
    import google.api_core.retry
    import google.api_core.retry_async

    # start_retry as AsyncRetry
    async_ret = google.api_core.retry_async.AsyncRetry()
    cfg1 = ResumableUploadConfig(start_retry=async_ret)
    s1 = AsyncResumableUploadSession(config=cfg1)
    assert s1._get_async_retry(is_start=True) is async_ret

    # start_retry as sync Retry
    sync_ret = google.api_core.retry.Retry()
    cfg2 = ResumableUploadConfig(start_retry=sync_ret)
    s2 = AsyncResumableUploadSession(config=cfg2)
    res_retry = s2._get_async_retry(is_start=True)
    assert isinstance(res_retry, google.api_core.retry_async.AsyncRetry)

    # retry as AsyncRetry
    cfg3 = ResumableUploadConfig(retry=async_ret)
    s3 = AsyncResumableUploadSession(config=cfg3)
    assert s3._get_async_retry(is_start=False) is async_ret

    # retry as sync Retry
    cfg4 = ResumableUploadConfig(retry=sync_ret)
    s4 = AsyncResumableUploadSession(config=cfg4)
    res_retry2 = s4._get_async_retry(is_start=False)
    assert isinstance(res_retry2, google.api_core.retry_async.AsyncRetry)

    # retry as AsyncStreamingRetry
    async_stream_ret = google.api_core.retry.AsyncStreamingRetry()
    cfg5 = ResumableUploadConfig(retry=async_stream_ret)
    s5 = AsyncResumableUploadSession(config=cfg5)
    assert s5._get_async_streaming_retry() is async_stream_ret


@pytest.mark.asyncio
async def test_async_retry_generic_exception() -> None:
    """Verifies _async_retry retries generic Exception up to max_attempts."""
    session = AsyncResumableUploadSession()
    attempts = 0

    async def fail_generic():
        nonlocal attempts
        attempts += 1
        raise KeyError("generic error")

    with pytest.raises(KeyError):
        await session._async_retry(fail_generic, max_attempts=3, initial_delay=0.01)
    assert attempts == 3

    # max_attempts=0 loop exit
    assert await session._async_retry(mock.AsyncMock(), max_attempts=0) is None


@pytest.mark.asyncio
async def test_async_transmit_chunk_stall_and_timeouts() -> None:
    """Verifies timeouts, deadlines, and stall control inside _transmit_chunk."""
    # 1. empty bytes from reader_fn
    session = AsyncResumableUploadSession(resumable_url="https://upload.example.com/1")
    resp_done = DummyAsyncResponse(200, {"X-Goog-Upload-Status": "final"}, b"done")
    sess_transport = DummyAsyncSession([resp_done])
    async def empty_reader(n: int) -> bytes:
        return b""
    t_resp = await session._transmit_chunk(sess_transport, empty_reader, 0)
    assert session.finished

    # 2. explicit config.timeout and future deadline
    future = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=60)
    cfg_timeout = ResumableUploadConfig(timeout=30.0, deadline=future)
    session_to = AsyncResumableUploadSession(
        resumable_url="https://upload.example.com/1",
        config=cfg_timeout,
    )
    resp_chunk = DummyAsyncResponse(200, {"X-Goog-Upload-Status": "active", "X-Goog-Upload-Size-Received": "4"}, b"")
    sess_transport2 = DummyAsyncSession([resp_chunk])
    async def bytes_reader(n: int) -> bytes:
        return b"1234"
    await session_to._transmit_chunk(sess_transport2, bytes_reader, 4)

    # 3. TimeoutError with deadline remaining <= 0 raises DeadlineExceeded
    session_dl = AsyncResumableUploadSession(
        resumable_url="https://upload.example.com/1",
        config=ResumableUploadConfig(deadline=future),
    )
    class TimeoutTransport:
        def request(self, *args, **kwargs):
            raise asyncio.TimeoutError("timed out")

    session_dl._get_deadline_remaining = mock.Mock(return_value=-1.0)
    with pytest.raises(exceptions.DeadlineExceeded):
        await session_dl._transmit_chunk(TimeoutTransport(), bytes_reader, 4)

    # 4. TimeoutError with deadline remaining > 0 raises TransferStalledError
    session_stall_to = AsyncResumableUploadSession(
        resumable_url="https://upload.example.com/1",
    )
    with pytest.raises(exceptions.TransferStalledError):
        await session_stall_to._transmit_chunk(TimeoutTransport(), bytes_reader, 4)

    # 5. Stall control normal chunk pass and positive lag below timeout
    cfg_stall2 = ResumableUploadConfig(stall_minimum_rate=1024, stall_timeout=10.0)
    session_stall2 = AsyncResumableUploadSession(
        resumable_url="https://upload.example.com/1",
        config=cfg_stall2,
    )
    # First chunk: positive lag below stall_timeout (sets _stall_timeout_started)
    session_stall2._aggregate_lag = 1.0
    assert session_stall2._aggregate_lag == 1.0
    sess_transport4 = DummyAsyncSession([resp_chunk, resp_chunk])
    await session_stall2._transmit_chunk(sess_transport4, bytes_reader, 4)
    assert session_stall2._stall_timeout_started is not None
    session_stall2._stall_timeout_started = time.monotonic()
    assert session_stall2._stall_timeout_started is not None

    # Second chunk: _stall_timeout_started is already set, still below stall_timeout
    await session_stall2._transmit_chunk(sess_transport4, bytes_reader, 4)

    # 6. Stall control lag exceeds stall_timeout
    cfg_stall = ResumableUploadConfig(stall_minimum_rate=1024, stall_timeout=1.0)
    session_stall = AsyncResumableUploadSession(
        resumable_url="https://upload.example.com/1",
        config=cfg_stall,
    )
    session_stall._aggregate_lag = 2.0  # Already exceeds stall_timeout
    sess_transport3 = DummyAsyncSession([resp_chunk])
    with pytest.raises(exceptions.TransferStalledError, match="Upload stalled: transfer rate remained below"):
        await session_stall._transmit_chunk(sess_transport3, bytes_reader, 4)

    # 7. Stall control disabled (stall_minimum_rate=0)
    cfg_no_stall = ResumableUploadConfig(stall_minimum_rate=0)
    session_no_stall = AsyncResumableUploadSession(
        resumable_url="https://upload.example.com/1",
        config=cfg_no_stall,
    )
    sess_transport_no_stall = DummyAsyncSession([resp_chunk])
    await session_no_stall._transmit_chunk(sess_transport_no_stall, bytes_reader, 4)


@pytest.mark.asyncio
async def test_async_recover_final_status_and_unseekable_buffer() -> None:
    """Verifies _recover when query returns FINAL and when server offset is outside buffer."""
    # 1. Query returns FINAL
    final_query_resp = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "final"},
        body=b"completed",
    )
    sess_transport = DummyAsyncSession([final_query_resp])
    session = AsyncResumableUploadSession(
        resumable_url="https://upload.example.com/1",
        transport=sess_transport,
    )
    await session._recover(sess_transport)
    assert session.finished
    assert session.response == b"completed"

    # 2. Server offset outside buffered chunk with unseekable/None stream
    active_query_resp = DummyAsyncResponse(
        status=200,
        headers={"X-Goog-Upload-Status": "active", "X-Goog-Upload-Size-Received": "100"},
        body=b"",
    )
    sess_transport2 = DummyAsyncSession([active_query_resp])
    session2 = AsyncResumableUploadSession(
        resumable_url="https://upload.example.com/1",
        transport=sess_transport2,
    )
    session2._buffered_chunk = memoryview(b"12345")
    session2._buffered_chunk_offset = 0  # received (100) is outside 0..5
    with pytest.raises(UnseekableStreamError, match="Server offset 100 precedes active buffer"):
        await session2._recover(sess_transport2, stream_obj=None)


@pytest.mark.asyncio
async def test_async_transmit_all_chunks_already_finished() -> None:
    """Verifies _async_transmit_all_chunks returns None if upload already finished."""
    session = AsyncResumableUploadSession(resumable_url="https://upload.example.com/1")
    session._state._finished = True
    res = await session._async_transmit_all_chunks(
        mock.Mock(), mock.Mock(), 0, asyncio.Queue(), None
    )
    assert res is None


@pytest.mark.asyncio
async def test_async_upload_and_resume_missing_final_response() -> None:
    """Verifies ValueError when upload/resume completes without final response."""
    # 1. upload missing final response
    session = AsyncResumableUploadSession(upload_url="https://api.example.com/start")
    session._ensure_aiohttp = mock.Mock()
    session._transport = mock.Mock()
    session.initiate = mock.AsyncMock()
    session._async_transmit_all_chunks = mock.AsyncMock(return_value=None)
    op = session.upload(stream=b"data")
    with pytest.raises(ValueError, match="Upload completed without receiving a final response"):
        await op

    # upload finished True but response is None
    session._state._finished = True
    session._response = None
    session._async_transmit_all_chunks = mock.AsyncMock(return_value=None)
    op_finished_none = session.upload(stream=b"data")
    with pytest.raises(ValueError, match="Upload completed without receiving a final response"):
        await op_finished_none

    # 2. resume missing final response
    session_resume = AsyncResumableUploadSession()
    session_resume._ensure_aiohttp = mock.Mock()
    session_resume._transport = mock.Mock()
    session_resume._async_transmit_all_chunks = mock.AsyncMock(return_value=None)
    op2 = session_resume.resume(upload_url="https://upload.example.com/1", stream=b"data")
    with pytest.raises(ValueError, match="Upload completed without receiving a final response"):
        await op2

    # resume finished True but response is None
    session_resume._state._finished = True
    session_resume._response = None
    session_resume._async_transmit_all_chunks = mock.AsyncMock(return_value=None)
    op_res_finished_none = session_resume.resume(upload_url="https://upload.example.com/1", stream=b"data")
    with pytest.raises(ValueError, match="Upload completed without receiving a final response"):
        await op_res_finished_none


@pytest.mark.asyncio
async def test_async_prepare_async_reader_additional_cases() -> None:
    """Verifies explicit size, stream without tell, and buffered reading from AsyncIterable."""
    session = AsyncResumableUploadSession()

    # 1. bytes with explicit size
    r1, s1, _ = session._prepare_async_reader(b"hello", size=5)
    assert s1 == 5
    assert await r1(5) == b"hello"

    # 2. sync stream with explicit size and without tell
    class SyncStreamNoTell:
        def read(self, n: int) -> bytes:
            return b"chunk"

    r2, s2, _ = session._prepare_async_reader(SyncStreamNoTell(), size=5)
    assert s2 == 5
    assert await r2(5) == b"chunk"

    # 3. AsyncIterable reading with pre-buffered data (len(buffer) >= n)
    async def byte_generator():
        yield b"abcdefghij"

    r3, s3, _ = session._prepare_async_reader(byte_generator(), None)
    c1 = await r3(3)
    assert c1 == b"abc"
    c2 = await r3(3)
    assert c2 == b"def"

