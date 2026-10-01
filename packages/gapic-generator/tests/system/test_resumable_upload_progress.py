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
import os
import pytest

from google.api_core.resumable_transfer import (
    DEFAULT_CHUNK_SIZE,
    ProgressState,
    ResumableUploadConfig,
    ResumableUploadSession,
    UploadProgress,
)
from google.showcase import UploadMediaRequest, UploadMediaResponse

from conftest import make_resumable_upload


class _UnknownSizeUnseekableStream:
    """Stream wrapper with unknown total size and non-seekable semantics."""

    def __init__(self, data: bytes) -> None:
        self._buf = io.BytesIO(data)

    def read(self, size: int = -1) -> bytes:
        return self._buf.read(size)

    def seekable(self) -> bool:
        return False


def test_make_resumable_upload_end_to_end(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    stream = io.BytesIO(b"0123456789" * 100)

    # Use make_resumable_upload from start to finish
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "full_e2e_upload.txt"}'

    response = make_resumable_upload(
        transport=client.transport._session,
        request_body=request_body,
        stream=stream,
        upload_url=initial_url,
        chunk_size=256,
    )
    assert isinstance(response, bytes)

    final_response = UploadMediaResponse.from_json(response)
    assert final_response.name == "full_e2e_upload.txt"
    assert final_response.size == len(stream.getvalue())


def test_resumable_upload_generator_progress_tracking(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    payload = b"0123456789" * 100
    stream = io.BytesIO(payload)

    scenario_headers = [("X-Goog-Test-Scenario", "chunk_granularity")]
    config = ResumableUploadConfig(
        chunk_size=256,
        headers=scenario_headers,
    )
    session = ResumableUploadSession(
        upload_url=initial_url,
        config=config,
        transport=client.transport._session,
        response_type=UploadMediaResponse,
    )

    progress_list = []
    # PEP 255 generator progress tracking
    for progress in session.iter_upload(stream, request_body='{"name": "generator_upload.txt"}'):
        progress_list.append(progress)
        assert isinstance(progress, UploadProgress)
        assert "sid=" in progress.upload_url
        assert progress.chunk_size == 256
        assert progress.total_bytes == len(payload)

    # Verify yielded snapshots
    assert len(progress_list) >= 3
    assert progress_list[0].state == ProgressState.STARTED
    assert progress_list[-1].state == ProgressState.FINALIZED
    assert progress_list[-1].bytes_uploaded == len(payload)

    # Verify response populated on session after generator exhaustion
    assert session.response is not None
    assert session.response.name == "generator_upload.txt"
    assert session.response.size == len(payload)


def test_resumable_upload_unseekable_stream_recovery(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "unseekable_stream_upload.txt"}'

    class UnseekableStream(io.BytesIO):
        def seekable(self):
            return False

        def seek(self, offset, whence=io.SEEK_SET):
            raise io.UnsupportedOperation("Stream is not seekable")

    data = b"B" * 1024
    stream = UnseekableStream(data)

    # Injects 503 error on first chunk attempt, which ResumableUploadSession recovers via in-memory buffer
    scenario_headers = [
        ("X-Goog-Test-Scenario", "non_fatal_error_on_chunk_upload"),
        ("X-Goog-Test-Scenario-Config", '{"error_code":503,"failure_count":1,"after_offset":0}'),
    ]

    response = make_resumable_upload(
        transport=client.transport._session,
        request_body=request_body,
        stream=stream,
        upload_url=initial_url,
        size=len(data),
        chunk_size=512,
        headers=scenario_headers,
    )
    assert isinstance(response, bytes)
    final_response = UploadMediaResponse.from_json(response)
    assert final_response.name == "unseekable_stream_upload.txt"
    assert final_response.size == len(data)


def test_multi_chunk_known_size(intercepted_resumable_upload_rest):
    """Golden Path Case 1: Multi-chunk upload with known size (1.5 MB, 512 KiB chunks)."""
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    total_size = 1_500_000
    chunk_size = 524_288  # 512 KiB
    payload = b"M" * total_size
    stream = io.BytesIO(payload)

    config = ResumableUploadConfig(chunk_size=chunk_size)
    session = ResumableUploadSession(
        upload_url=initial_url,
        config=config,
        transport=client.transport._session,
        response_type=UploadMediaResponse,
    )

    progress_records = list(
        session.iter_upload(
            stream,
            request_body='{"name": "multi_chunk_known_size.mp4"}',
            size=total_size,
        )
    )

    assert isinstance(session.response, UploadMediaResponse)
    assert session.response.name == "multi_chunk_known_size.mp4"
    assert session.response.size == total_size

    phases = [p.state for p in progress_records]
    offsets = [p.bytes_uploaded for p in progress_records]
    assert phases == [
        ProgressState.STARTED,
        ProgressState.UPLOADING,
        ProgressState.UPLOADING,
        ProgressState.FINALIZED,
    ]
    assert offsets == [0, 524_288, 1_048_576, 1_500_000]
    assert all(p.total_bytes == total_size for p in progress_records)


def test_small_upload_default_chunk_size(intercepted_resumable_upload_rest):
    """Golden Path Case 2: Default chunk size on small upload (~100 KB)."""
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    total_size = 100_000
    payload = b"S" * total_size
    stream = io.BytesIO(payload)

    session = ResumableUploadSession(
        upload_url=initial_url,
        transport=client.transport._session,
        response_type=UploadMediaResponse,
    )

    progress_records = list(
        session.iter_upload(
            stream,
            request_body='{"name": "small_default_chunk.bin"}',
            size=total_size,
        )
    )

    assert session.chunk_size <= DEFAULT_CHUNK_SIZE
    assert isinstance(session.response, UploadMediaResponse)
    assert session.response.name == "small_default_chunk.bin"
    assert session.response.size == total_size

    phases = [p.state for p in progress_records]
    offsets = [p.bytes_uploaded for p in progress_records]
    assert phases == [
        ProgressState.STARTED,
        ProgressState.FINALIZED,
    ]
    assert offsets == [0, 100_000]
    assert all(p.total_bytes == total_size for p in progress_records)


def test_standalone_finalize_unseekable_stream(intercepted_resumable_upload_rest):
    """Golden Path Case 3: Unseekable stream with unknown size and exact chunk multiple."""
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    chunk_size = 262_144  # 256 KiB
    total_size = 3 * chunk_size  # 786_432 bytes
    payload = b"U" * total_size
    stream = _UnknownSizeUnseekableStream(payload)

    config = ResumableUploadConfig(chunk_size=chunk_size)
    session = ResumableUploadSession(
        upload_url=initial_url,
        config=config,
        transport=client.transport._session,
        response_type=UploadMediaResponse,
    )

    progress_records = list(
        session.iter_upload(
            stream,
            request_body='{"name": "unseekable_exact_multiple.bin"}',
            size=None,
        )
    )

    assert isinstance(session.response, UploadMediaResponse)
    assert session.response.name == "unseekable_exact_multiple.bin"
    assert session.response.size == total_size

    phases = [p.state for p in progress_records]
    offsets = [p.bytes_uploaded for p in progress_records]
    assert phases == [
        ProgressState.STARTED,
        ProgressState.UPLOADING,
        ProgressState.UPLOADING,
        ProgressState.UPLOADING,
        ProgressState.FINALIZED,
    ]
    assert offsets == [0, 262_144, 524_288, 786_432, 786_432]
    assert all(p.total_bytes is None for p in progress_records)


def test_client_upload_media_passes_request_body(intercepted_resumable_upload_rest):
    """ Verify that invoking `client.upload_media(request=UploadMediaRequest(...))`
    and calling `session.upload(stream=...)` forwards the serialized request body
    on the initial upload session start request so the server echoes back the
    expected resource name in `UploadMediaResponse.name`."""
    client, _ = intercepted_resumable_upload_rest
    payload = b"0123456789" * 100
    stream = io.BytesIO(payload)

    session = client.upload_media(
        request=UploadMediaRequest(name="client_upload_media.txt"),
    )
    response = session.upload(stream=stream)

    assert isinstance(response, UploadMediaResponse)
    assert response.name == "client_upload_media.txt"
    assert response.size == len(payload)


if os.environ.get("GAPIC_PYTHON_ASYNC", "true") == "true":

    @pytest.mark.asyncio
    async def test_async_client_upload_media_end_to_end(
        intercepted_resumable_upload_rest_async,
    ):
        """Verify end-to-end async resumable upload via ResumableUploadServiceAsyncClient."""
        client, _ = intercepted_resumable_upload_rest_async
        payload = b"0123456789" * 100
        stream = io.BytesIO(payload)

        session = await client.upload_media(
            request=UploadMediaRequest(name="async_client_upload_media.txt"),
            config=ResumableUploadConfig(chunk_size=256),
        )
        response = await session.upload(stream=stream)

        assert isinstance(response, UploadMediaResponse)
        assert response.name == "async_client_upload_media.txt"
        assert response.size == len(payload)

    @pytest.mark.asyncio
    async def test_async_client_upload_media_progress_tracking(
        intercepted_resumable_upload_rest_async,
    ):
        """Verify async progress iteration over ResumableUploadServiceAsyncClient.upload_media."""
        client, _ = intercepted_resumable_upload_rest_async
        chunk_size = 262_144  # 256 KiB
        total_size = 600_000
        payload = b"A" * total_size
        stream = io.BytesIO(payload)

        session = await client.upload_media(
            request=UploadMediaRequest(name="async_multi_chunk.bin"),
            config=ResumableUploadConfig(chunk_size=chunk_size),
        )

        progress_records = [
            p async for p in session.upload(stream=stream, size=total_size)
        ]

        assert isinstance(session.response, UploadMediaResponse)
        assert session.response.name == "async_multi_chunk.bin"
        assert session.response.size == total_size

        phases = [p.state for p in progress_records]
        offsets = [p.bytes_uploaded for p in progress_records]
        assert phases == [
            ProgressState.STARTED,
            ProgressState.UPLOADING,
            ProgressState.UPLOADING,
            ProgressState.FINALIZED,
        ]
        assert offsets == [0, 262_144, 524_288, 600_000]
        assert all(p.total_bytes == total_size for p in progress_records)
