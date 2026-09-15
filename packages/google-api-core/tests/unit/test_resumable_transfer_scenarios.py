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

"""Test suite covering edge cases, stream boundaries, retry interactions, and sync/async parity.

These tests evaluate:
1. Stream continuity and subsequent chunk delivery following full/partial chunk recovery.
2. Parity in return types, retry configuration, and exception handling between sync and async.
3. Memory efficiency when consuming streaming iterables.
4. Coordination of retry policies, backoffs, and timeout handling during transport interruptions.
"""

import datetime
from unittest import mock
import pytest
import requests

import google.api_core.retry
from google.api_core.resumable_transfer.upload import (
    ResumableUploadConfig,
    ResumableUploadSession,
)
from google.api_core.resumable_transfer.upload_async import (
    AsyncResumableUploadSession,
)


class _MockAiohttpResp:
    """Mock for aiohttp response context manager."""

    def __init__(self, status: int, headers: dict, body: bytes):
        self.status = status
        self.headers = headers
        self._body = body

    async def read(self) -> bytes:
        return self._body

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass


# ==============================================================================
# 1. Stream Recovery & Chunk Continuity
# ==============================================================================


def test_full_chunk_recovery_transmits_subsequent_chunks_sync():
    """Verifies that sync upload continues transmitting subsequent chunks after full chunk recovery.

    When chunk 1 (bytes 0..100) encounters a transport error (e.g. 409 Conflict)
    and the subsequent status query confirms the server received all 100 bytes,
    the session should advance to chunk 2 (bytes 100..200) rather than finalizing early.
    """
    transport = mock.Mock()
    start_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/session1",
        },
    )
    resp_409 = mock.Mock(
        ok=False,
        status_code=409,
        text="Conflict",
        content=b"Conflict",
        headers={},
        json=lambda: {},
    )
    query_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-Size-Received": "100",
        },
    )
    final_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={"X-Goog-Upload-Status": "final"},
        content=b"done",
    )
    transport.request.side_effect = [start_resp, resp_409, query_resp, final_resp]

    # Total payload: 200 bytes across two 100-byte chunks
    payload = b"A" * 100 + b"B" * 100
    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=ResumableUploadConfig(chunk_size=100),
        transport=transport,
    )
    session.upload(stream=payload)

    transmitted_chunks = [
        call.kwargs.get("data")
        for call in transport.request.call_args_list
        if call.kwargs.get("headers", {}).get("X-Goog-Upload-Command")
        in ("upload", "upload, finalize")
    ]
    total_bytes_sent = sum(len(c) for c in transmitted_chunks if c is not None)
    assert total_bytes_sent == 200, (
        f"Expected 200 bytes uploaded across all chunks, but received {total_bytes_sent} "
        f"bytes. Transmitted chunks: {transmitted_chunks}"
    )


@pytest.mark.asyncio
async def test_full_chunk_recovery_transmits_subsequent_chunks_async():
    """Async counterpart verifying subsequent chunks continue transmitting after full chunk recovery."""
    transport = mock.Mock()
    start_resp = _MockAiohttpResp(
        200,
        {
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/session1",
        },
        b"",
    )
    resp_409 = _MockAiohttpResp(409, {}, b"Conflict")
    query_resp = _MockAiohttpResp(
        200,
        {"X-Goog-Upload-Status": "active", "X-Goog-Upload-Size-Received": "100"},
        b"",
    )
    final_resp = _MockAiohttpResp(200, {"X-Goog-Upload-Status": "final"}, b"done")
    transport.request.side_effect = [start_resp, resp_409, query_resp, final_resp]

    payload = b"A" * 100 + b"B" * 100
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=ResumableUploadConfig(chunk_size=100),
        transport=transport,
    )
    await session.upload(stream=payload)

    transmitted_chunks = [
        call.kwargs.get("data")
        for call in transport.request.call_args_list
        if call.kwargs.get("headers", {}).get("X-Goog-Upload-Command")
        in ("upload", "upload, finalize")
    ]
    total_bytes_sent = sum(len(c) for c in transmitted_chunks if c is not None)
    assert total_bytes_sent == 200, (
        f"Expected 200 bytes uploaded across all chunks, but received {total_bytes_sent} "
        f"bytes. Transmitted chunks: {transmitted_chunks}"
    )


def test_partial_chunk_recovery_does_not_finalize_prematurely_sync():
    """Verifies that retransmitting a partial chunk does not prematurely finalize the upload.

    When server confirms 50 bytes received out of 100, the remaining buffer slice
    has length 50. The retransmission request should not mark the chunk as 'finalize'
    if more bytes remain in the overall stream.
    """
    transport = mock.Mock()
    start_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/session1",
        },
    )
    resp_409 = mock.Mock(
        ok=False,
        status_code=409,
        text="Conflict",
        content=b"Conflict",
        headers={},
        json=lambda: {},
    )
    query_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-Size-Received": "50",
        },
    )
    final_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={"X-Goog-Upload-Status": "final"},
        content=b"done",
    )
    transport.request.side_effect = [start_resp, resp_409, query_resp, final_resp]

    # Total payload: 200 bytes across two 100-byte chunks
    payload = b"A" * 100 + b"B" * 100
    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=ResumableUploadConfig(chunk_size=100),
        transport=transport,
    )
    session.upload(stream=payload)

    calls = transport.request.call_args_list
    call_3_cmd = calls[3].kwargs.get("headers", {}).get("X-Goog-Upload-Command")
    assert call_3_cmd == "upload", (
        f"Call 3 used command '{call_3_cmd}' instead of 'upload'. "
        "A partial retransmit should not mark finalize when subsequent chunks remain."
    )


@pytest.mark.asyncio
async def test_partial_chunk_recovery_does_not_finalize_prematurely_async():
    """Async counterpart verifying partial chunk retransmission does not prematurely finalize."""
    transport = mock.Mock()
    start_resp = _MockAiohttpResp(
        200,
        {
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/session1",
        },
        b"",
    )
    resp_409 = _MockAiohttpResp(409, {}, b"Conflict")
    query_resp = _MockAiohttpResp(
        200,
        {"X-Goog-Upload-Status": "active", "X-Goog-Upload-Size-Received": "50"},
        b"",
    )
    final_resp = _MockAiohttpResp(200, {"X-Goog-Upload-Status": "final"}, b"done")
    transport.request.side_effect = [start_resp, resp_409, query_resp, final_resp]

    payload = b"A" * 100 + b"B" * 100
    session = AsyncResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=ResumableUploadConfig(chunk_size=100),
        transport=transport,
    )
    await session.upload(stream=payload)

    calls = transport.request.call_args_list
    call_3_cmd = calls[3].kwargs.get("headers", {}).get("X-Goog-Upload-Command")
    assert call_3_cmd == "upload", (
        f"Async call 3 used command '{call_3_cmd}' instead of 'upload'. "
        "A partial retransmit should not mark finalize when subsequent chunks remain."
    )


# ==============================================================================
# 2. Sync vs Async Consistency & Parity
# ==============================================================================


@pytest.mark.asyncio
async def test_sync_async_return_type_parity():
    """Verifies consistent return types between sync and async when response_type is None."""
    # Sync session
    transport_sync = mock.Mock()
    start_sync = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/s1",
        },
    )
    chunk_sync = mock.Mock(
        ok=True,
        status_code=200,
        headers={"X-Goog-Upload-Status": "final"},
        content=b'{"status": "ok"}',
    )
    transport_sync.request.side_effect = [start_sync, chunk_sync]
    s_sync = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=ResumableUploadConfig(),
        transport=transport_sync,
    )
    sync_result = s_sync.upload(stream=b"data")

    # Async session
    transport_async = mock.Mock()
    start_async = _MockAiohttpResp(
        200,
        {
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/s1",
        },
        b"",
    )
    chunk_async = _MockAiohttpResp(
        200,
        {"X-Goog-Upload-Status": "final"},
        b'{"status": "ok"}',
    )
    transport_async.request.side_effect = [start_async, chunk_async]
    s_async = AsyncResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=ResumableUploadConfig(),
        transport=transport_async,
    )
    async_result = await s_async.upload(stream=b"data")

    assert type(sync_result) is type(async_result), (
        f"Expected consistent return types: sync returned {type(sync_result).__name__}, "
        f"while async returned {type(async_result).__name__}."
    )


@pytest.mark.asyncio
async def test_sync_async_custom_retry_parity():
    """Verifies that user-configured retry policies are applied in both sync and async sessions."""
    custom_retry = mock.Mock(wraps=google.api_core.retry.Retry())
    config = ResumableUploadConfig(retry=custom_retry)

    # Sync
    transport_sync = mock.Mock()
    start_sync = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/s1",
        },
    )
    chunk_sync = mock.Mock(
        ok=True,
        status_code=200,
        headers={"X-Goog-Upload-Status": "final"},
        content=b"ok",
    )
    transport_sync.request.side_effect = [start_sync, chunk_sync]
    s_sync = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=config,
        transport=transport_sync,
    )
    s_sync.upload(stream=b"data")
    sync_retry_called = custom_retry.called

    # Async
    custom_retry.reset_mock()
    transport_async = mock.Mock()
    start_async = _MockAiohttpResp(
        200,
        {
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/s1",
        },
        b"",
    )
    chunk_async = _MockAiohttpResp(200, {"X-Goog-Upload-Status": "final"}, b"ok")
    transport_async.request.side_effect = [start_async, chunk_async]
    s_async = AsyncResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=config,
        transport=transport_async,
    )
    await s_async.upload(stream=b"data")
    async_retry_called = custom_retry.called

    assert sync_retry_called and async_retry_called, (
        f"Expected custom retry to be invoked in both implementations: "
        f"sync invoked={sync_retry_called}, async invoked={async_retry_called}."
    )


@pytest.mark.asyncio
async def test_sync_async_error_retry_parity():
    """Verifies that non-retriable exceptions (e.g. ValueError) fail fast without retries in both."""
    # Sync: transport raises ValueError
    transport_sync = mock.Mock()
    transport_sync.request.side_effect = ValueError("fatal configuration issue")
    s_sync = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=ResumableUploadConfig(),
        transport=transport_sync,
    )
    with pytest.raises(ValueError):
        s_sync.upload(stream=b"data")
    sync_attempts = transport_sync.request.call_count

    # Async: transport raises ValueError
    transport_async = mock.Mock()
    transport_async.request.side_effect = ValueError("fatal configuration issue")
    s_async = AsyncResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=ResumableUploadConfig(),
        transport=transport_async,
    )
    with pytest.raises(ValueError):
        await s_async.upload(stream=b"data")
    async_attempts = transport_async.request.call_count

    assert sync_attempts == async_attempts == 1, (
        f"Expected non-retriable error to fail after 1 attempt in both implementations: "
        f"sync attempts={sync_attempts}, async attempts={async_attempts}."
    )


def test_iterable_stream_incremental_consumption_sync():
    """Verifies that iterable streams are consumed incrementally rather than loaded upfront."""
    chunks_generated = 0

    def data_generator():
        nonlocal chunks_generated
        for _ in range(10):
            chunks_generated += 1
            yield b"X" * 1024

    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=ResumableUploadConfig(chunk_size=1024),
    )
    # Stream preparation should not exhaust the generator
    stream_obj, size = session._prepare_stream(data_generator(), size=10 * 1024)

    assert chunks_generated == 0, (
        f"Expected iterable stream to be consumed lazily during upload, but all "
        f"{chunks_generated} chunks were buffered into memory during preparation."
    )


def test_timezone_naive_deadline_handling():
    """Verifies that naive future datetimes are compared accurately against current time."""
    future_naive = datetime.datetime.now() + datetime.timedelta(hours=1)
    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=ResumableUploadConfig(deadline=future_naive),
    )
    remaining = session._get_deadline_remaining()
    assert remaining is not None and remaining > 0, (
        f"Expected positive remaining deadline duration for future naive timestamp, got {remaining}s."
    )


# ==============================================================================
# 3. Retry Coordination & Multi-Layer Interactions
# ==============================================================================


def test_single_layer_backoff_coordination():
    """Verifies that retry backoff delays are coordinated through a single layer during chunk recovery.

    During a chunk transfer encounter with transient transport and query errors, backoff
    delays should follow a single coordinated schedule rather than accumulating independent
    delays across nested caller, query, and retransmit loops.
    """
    transport = mock.Mock()
    start_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/s1",
        },
    )
    resp_503 = mock.Mock(
        ok=False,
        status_code=503,
        text="Service Unavailable",
        content=b"503",
        headers={},
        json=lambda: {},
    )
    resp_409 = mock.Mock(
        ok=False,
        status_code=409,
        text="Conflict",
        content=b"Conflict",
        headers={},
        json=lambda: {},
    )
    query_503 = mock.Mock(
        ok=False,
        status_code=503,
        text="Service Unavailable",
        content=b"503",
        headers={},
        json=lambda: {},
    )
    query_200 = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-Size-Received": "0",
        },
    )
    final_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={"X-Goog-Upload-Status": "final"},
        content=b"done",
    )

    transport.request.side_effect = [
        start_resp,
        resp_503,
        resp_409,
        query_503,
        query_200,
        final_resp,
    ]

    sleep_durations = []
    with mock.patch("time.sleep", side_effect=lambda d: sleep_durations.append(d)):
        session = ResumableUploadSession(
            upload_url="https://api.example.com/init",
            config=ResumableUploadConfig(chunk_size=100),
            transport=transport,
        )
        session.upload(stream=b"A" * 100)

    # In a unified single-layer retry architecture, only the primary loop applies backoff.
    assert len(sleep_durations) <= 1, (
        f"Observed multiple independent retry backoff delays ({len(sleep_durations)} sleeps, "
        f"total {sum(sleep_durations):.2f}s: {sleep_durations}) across nested layers during chunk recovery."
    )


def test_connection_recovery_with_custom_retry_predicate():
    """Verifies that network connection drops initiate an offset query when a custom retry is set.

    When a caller specifies a custom retry policy (e.g. for ServiceUnavailable), a routine
    connection reset should still initiate a query command to reconcile committed server state.
    """
    transport = mock.Mock()
    start_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/s1",
        },
    )
    query_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-Size-Received": "0",
        },
    )
    final_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={"X-Goog-Upload-Status": "final"},
        content=b"done",
    )

    transport.request.side_effect = [
        start_resp,
        requests.exceptions.ConnectionError("TCP connection reset by peer"),
        query_resp,
        final_resp,
    ]

    user_retry = google.api_core.retry.Retry(
        predicate=google.api_core.retry.if_exception_type(
            google.api_core.exceptions.ServiceUnavailable
        )
    )
    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=ResumableUploadConfig(chunk_size=100, retry=user_retry),
        transport=transport,
    )

    session.upload(stream=b"A" * 100)

    calls = transport.request.call_args_list
    query_calls = [
        c
        for c in calls
        if c.kwargs.get("headers", {}).get("X-Goog-Upload-Command") == "query"
    ]
    assert len(query_calls) >= 1, (
        "Expected transport connection drop to initiate an offset query to reconcile server state."
    )


def test_conflict_response_triggers_offset_query():
    """Verifies that a 409 Conflict status initiates an offset query rather than immediate resend."""
    transport = mock.Mock()
    start_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/s1",
        },
    )
    resp_409 = mock.Mock(
        ok=False,
        status_code=409,
        text="Conflict",
        content=b"Conflict",
        headers={},
        json=lambda: {},
    )
    query_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-Size-Received": "0",
        },
    )
    final_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={"X-Goog-Upload-Status": "final"},
        content=b"done",
    )

    transport.request.side_effect = [
        start_resp,
        resp_409,
        resp_409,
        query_resp,
        final_resp,
    ]

    user_retry = google.api_core.retry.Retry(
        predicate=lambda e: isinstance(e, google.api_core.exceptions.Conflict),
        maximum=0.01,
        deadline=0.05,
    )
    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=ResumableUploadConfig(chunk_size=100, retry=user_retry),
        transport=transport,
    )

    session.upload(stream=b"A" * 100)

    calls = transport.request.call_args_list
    call_2_cmd = calls[2].kwargs.get("headers", {}).get("X-Goog-Upload-Command")
    assert call_2_cmd == "query", (
        f"Expected command 'query' to reconcile server offset after 409 Conflict, but received '{call_2_cmd}'."
    )


def test_socket_timeout_initiates_recovery():
    """Verifies that a transient socket read timeout triggers recovery rather than an immediate terminal stall error."""
    transport = mock.Mock()
    start_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-URL": "https://upload.example.com/s1",
        },
    )
    query_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={
            "X-Goog-Upload-Status": "active",
            "X-Goog-Upload-Size-Received": "0",
        },
    )
    final_resp = mock.Mock(
        ok=True,
        status_code=200,
        headers={"X-Goog-Upload-Status": "final"},
        content=b"done",
    )
    transport.request.side_effect = [
        start_resp,
        requests.exceptions.Timeout("Read timed out on socket"),
        query_resp,
        final_resp,
    ]

    session = ResumableUploadSession(
        upload_url="https://api.example.com/init",
        config=ResumableUploadConfig(chunk_size=100),
        transport=transport,
    )

    session.upload(stream=b"A" * 100)

    calls = transport.request.call_args_list
    assert len(calls) > 2, (
        f"Expected socket read timeout to attempt recovery rather than terminating after {len(calls)} call(s)."
    )
