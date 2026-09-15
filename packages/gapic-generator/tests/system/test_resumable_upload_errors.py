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

import io
import pytest

from google.api_core import exceptions
from google.api_core.resumable_transfer import (
    ResumableUploadConfig,
    ResumableUploadSession,
    UnseekableStreamError,
    UploadCancelledError,
)
from google.showcase import UploadMediaResponse


def make_resumable_upload(
    transport,
    request_body,
    stream,
    upload_url,
    size=None,
    config=None,
    **kwargs,
):
    if config is None:
        config = ResumableUploadConfig(**kwargs)
    elif kwargs:
        for k, v in kwargs.items():
            if hasattr(config, k):
                setattr(config, k, v)

    session = ResumableUploadSession(
        upload_url=upload_url,
        config=config,
        transport=transport,
    )
    return session.upload(
        stream=stream,
        request_body=request_body,
        size=size,
        transport=transport,
    )


class StrictlyUnseekableStream(io.RawIOBase):
    """Stream that disallows seeking to test unseekable error handling."""

    def __init__(self, data: bytes):
        self._data = data
        self._pos = 0

    def readable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return False

    def readinto(self, b) -> int:
        if self._pos >= len(self._data):
            return 0
        n = min(len(b), len(self._data) - self._pos)
        b[:n] = self._data[self._pos : self._pos + n]
        self._pos += n
        return n

    def seek(self, offset, whence=io.SEEK_SET):
        raise io.UnsupportedOperation("Stream does not support seeking")


def test_resumable_upload_exception_surfaces_attributes(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "error_attributes.txt"}'
    data = b"E" * 1024
    stream = io.BytesIO(data)

    # Server scenario terminates chunk upload with non-recoverable error
    scenario_headers = [
        ("X-Goog-Test-Scenario", "non_fatal_error_on_chunk_upload"),
        ("X-Goog-Test-Scenario-Config", '{"error_code":403,"failure_count":1}'),
    ]

    config = ResumableUploadConfig(
        chunk_size=512,
        headers=scenario_headers,
    )

    with pytest.raises(exceptions.GoogleAPICallError) as exc_info:
        make_resumable_upload(
            transport=client.transport._session,
            request_body=request_body,
            stream=stream,
            upload_url=initial_url,
            config=config,
        )

    # Verify exception attributes
    assert hasattr(exc_info.value, "upload_url")
    assert exc_info.value.upload_url is not None
    assert "/upload?sid=" in exc_info.value.upload_url
    assert hasattr(exc_info.value, "chunk_size")
    assert exc_info.value.chunk_size == 262144


def test_resumable_upload_crash_recovery_flow(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "crash_recovery.txt"}'
    data = b"C" * 1536
    stream = io.BytesIO(data)

    scenario_headers = [
        ("X-Goog-Test-Scenario", "chunk_granularity"),
    ]

    # Session 1: Client begins upload
    config1 = ResumableUploadConfig(
        chunk_size=512,
        headers=scenario_headers,
        response_type=UploadMediaResponse,
    )
    session1 = ResumableUploadSession(
        upload_url=initial_url,
        config=config1,
        transport=client.transport._session,
    )
    session1.initiate(
        transport=client.transport._session,
        request_body=request_body,
        size=len(data),
    )

    # First chunk succeeds
    session1._transmit_chunk(client.transport._session, stream, len(data))
    assert session1.bytes_uploaded == 512

    # Simulate process crash by capturing URL and chunk size
    crashed_url = session1.upload_url
    crashed_chunk_size = session1.chunk_size

    # Session 2: Fresh process recovers upload from captured URL
    config2 = ResumableUploadConfig(
        chunk_size=crashed_chunk_size,
        response_type=UploadMediaResponse,
    )
    session2 = ResumableUploadSession(
        config=config2,
        transport=client.transport._session,
    )

    # Rewind stream to beginning (full file available in new process)
    stream.seek(0)
    response = session2.resume(
        upload_url=crashed_url,
        stream=stream,
        size=len(data),
        transport=client.transport._session,
    )

    assert isinstance(response, UploadMediaResponse)
    assert response.name == "crash_recovery.txt"
    assert response.size == len(data)
    assert session2.bytes_uploaded == len(data)
    assert session2.finished


def test_resumable_upload_unseekable_stream_beyond_buffer_raises(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "unseekable_error.bin"}'
    data = b"U" * 2048
    unseekable = StrictlyUnseekableStream(data)

    scenario_headers = [
        ("X-Goog-Test-Scenario", "chunk_granularity"),
    ]
    config = ResumableUploadConfig(
        chunk_size=512,
        headers=scenario_headers,
        response_type=UploadMediaResponse,
    )
    session = ResumableUploadSession(
        upload_url=initial_url,
        config=config,
        transport=client.transport._session,
    )
    session.initiate(
        transport=client.transport._session,
        request_body=request_body,
        size=len(data),
    )

    # First chunk is transmitted and committed; in-memory buffer is discarded
    session._transmit_chunk(client.transport._session, unseekable, len(data))
    assert session.bytes_uploaded == 512
    assert session._buffered_chunk is None

    # Simulating server recovery request to offset 0 (outside discarded buffer)
    # on an unseekable stream must raise UnseekableStreamError
    with pytest.raises(UnseekableStreamError) as exc_info:
        session._reposition_stream_offset(unseekable, 0)

    assert hasattr(exc_info.value, "upload_url")
    assert exc_info.value.upload_url == session.upload_url
    assert exc_info.value.chunk_size == 512


def test_resumable_upload_session_cancellation(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "cancel_session.txt"}'
    data = b"X" * 1024
    stream = io.BytesIO(data)

    scenario_headers = [
        ("X-Goog-Test-Scenario", "chunk_granularity"),
    ]
    session = ResumableUploadSession(
        upload_url=initial_url,
        config=ResumableUploadConfig(chunk_size=512, headers=scenario_headers),
        transport=client.transport._session,
    )
    session.initiate(
        transport=client.transport._session,
        request_body=request_body,
        size=len(data),
    )
    assert session.upload_url is not None

    # Transmit first chunk
    session._transmit_chunk(client.transport._session, stream, len(data))
    assert session.bytes_uploaded == 512

    # Cancel session
    session.cancel(transport=client.transport._session)

    # Attempting to upload to cancelled session triggers query which discovers cancelled status (410 Gone) or 400
    with pytest.raises(exceptions.GoogleAPICallError) as exc_info:
        session._transmit_chunk(client.transport._session, stream, len(data))

    assert exc_info.value.code in (400, 410)
