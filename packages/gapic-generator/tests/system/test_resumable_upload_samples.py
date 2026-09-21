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
import aiohttp
import pytest

from google.api_core.resumable_transfer import (
    AsyncResumableUploadSession,
    ProgressState,
    ResumableUploadConfig,
    ResumableUploadSession,
)
from google.showcase import UploadMediaResponse


def test_sample_upload_media_sync(intercepted_resumable_upload_rest):
    """Option 1: Upload a stream directly from start to completion (sync)."""
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"

    # Configure optional transfer settings such as chunk size and stall detection
    config = ResumableUploadConfig(
        chunk_size=256,
        stall_minimum_rate=64 * 1024,
        stall_timeout=120,
    )

    # Create an upload session for the request
    upload_session = ResumableUploadSession(
        upload_url=initial_url,
        config=config,
        transport=client.transport._session,
        response_type=UploadMediaResponse,
    )

    # Upload the entire stream directly and return the final response
    payload = b"Example upload data " * 30
    stream = io.BytesIO(payload)
    response = upload_session.upload(
        stream, request_body='{"name": "sample_direct_sync.txt"}'
    )

    # Handle the response
    assert response.name == "sample_direct_sync.txt"
    assert response.size == len(payload)


def test_sample_upload_media_with_progress_sync(intercepted_resumable_upload_rest):
    """Option 2: Upload a stream while receiving progress updates per chunk (sync)."""
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"

    # Configure optional transfer settings such as chunk size and stall detection
    config = ResumableUploadConfig(
        chunk_size=256,
        stall_minimum_rate=64 * 1024,
        stall_timeout=120,
    )

    # Create an upload session for the request
    upload_session = ResumableUploadSession(
        upload_url=initial_url,
        config=config,
        transport=client.transport._session,
        response_type=UploadMediaResponse,
    )

    # Iterate over the upload to receive progress updates as each chunk is transmitted
    payload = b"Example upload data " * 30
    stream = io.BytesIO(payload)
    progress_updates = []
    for progress in upload_session.iter_upload(
        stream, request_body='{"name": "sample_progress_sync.txt"}'
    ):
        print(
            f"Uploaded {progress.bytes_uploaded} bytes | State: {progress.state.name}"
        )
        print(f"Session URL: {progress.upload_url}")
        progress_updates.append(progress)

    # After iteration completes, the final response is available on the session
    response = upload_session.response

    # Handle the response
    assert len(progress_updates) >= 2
    assert progress_updates[0].state == ProgressState.STARTED
    assert progress_updates[-1].state == ProgressState.FINALIZED
    assert response.name == "sample_progress_sync.txt"
    assert response.size == len(payload)


def test_sample_upload_media_resume_sync(intercepted_resumable_upload_rest):
    """Option 3: Resume an interrupted upload using a previously saved session URL (sync)."""
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    payload = b"Example upload data " * 30

    # First obtain a live upload_url and chunk_size by starting an upload and interrupting it
    initial_session = ResumableUploadSession(
        upload_url=initial_url,
        config=ResumableUploadConfig(chunk_size=256),
        transport=client.transport._session,
        response_type=UploadMediaResponse,
    )
    upload_url = None
    chunk_size = 256
    for progress in initial_session.iter_upload(
        io.BytesIO(payload), request_body='{"name": "sample_resume_sync.txt"}'
    ):
        upload_url = progress.upload_url
        chunk_size = progress.chunk_size
        break

    # Create an upload session for resuming the request
    upload_session = ResumableUploadSession(
        transport=client.transport._session,
        response_type=UploadMediaResponse,
    )

    # Resume the interrupted upload from the saved session URL and chunk size
    stream = io.BytesIO(payload)
    response = upload_session.resume(upload_url, stream, chunk_size=chunk_size)

    # Handle the response
    assert response.name == "sample_resume_sync.txt"
    assert response.size == len(payload)


def test_sample_upload_media_resume_with_progress_sync(
    intercepted_resumable_upload_rest,
):
    """Option 4: Resume an interrupted upload while receiving progress updates (sync)."""
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    payload = b"Example upload data " * 30

    # First obtain a live upload_url and chunk_size by starting an upload and interrupting it
    initial_session = ResumableUploadSession(
        upload_url=initial_url,
        config=ResumableUploadConfig(chunk_size=256),
        transport=client.transport._session,
        response_type=UploadMediaResponse,
    )
    upload_url = None
    chunk_size = 256
    for progress in initial_session.iter_upload(
        io.BytesIO(payload),
        request_body='{"name": "sample_resume_progress_sync.txt"}',
    ):
        upload_url = progress.upload_url
        chunk_size = progress.chunk_size
        break

    # Create an upload session for resuming the request
    upload_session = ResumableUploadSession(
        transport=client.transport._session,
        response_type=UploadMediaResponse,
    )

    # Resume the interrupted upload while iterating over progress updates
    stream = io.BytesIO(payload)
    progress_updates = []
    for progress in upload_session.iter_resume(
        upload_url, stream, chunk_size=chunk_size
    ):
        print(
            f"Resumed {progress.bytes_uploaded} bytes | State: {progress.state.name}"
        )
        print(f"Session URL: {progress.upload_url}")
        print(f"Chunk size: {progress.chunk_size}")
        progress_updates.append(progress)

    # After iteration completes, the final response is available on the session
    response = upload_session.response

    # Handle the response
    assert len(progress_updates) >= 1
    assert progress_updates[-1].state == ProgressState.FINALIZED
    assert response.name == "sample_resume_progress_sync.txt"
    assert response.size == len(payload)


@pytest.mark.asyncio
async def test_sample_upload_media_async(intercepted_resumable_upload_rest):
    """Option 1: Upload a stream directly from start to completion (async)."""
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"

    # Configure optional transfer settings such as chunk size and stall detection
    config = ResumableUploadConfig(
        chunk_size=256,
        stall_minimum_rate=64 * 1024,
        stall_timeout=120,
    )

    async with aiohttp.ClientSession() as transport_session:
        # Create an upload session for the request
        upload_session = AsyncResumableUploadSession(
            upload_url=initial_url,
            config=config,
            transport=transport_session,
            response_type=UploadMediaResponse,
        )

        # Upload the entire stream directly and await the final response
        payload = b"Example upload data " * 30
        stream = io.BytesIO(payload)
        response = await upload_session.upload(
            stream, request_body='{"name": "sample_direct_async.txt"}'
        )

        # Handle the response
        assert response.name == "sample_direct_async.txt"
        assert response.size == len(payload)


@pytest.mark.asyncio
async def test_sample_upload_media_with_progress_async(
    intercepted_resumable_upload_rest,
):
    """Option 2: Upload a stream while receiving progress updates per chunk (async)."""
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"

    # Configure optional transfer settings such as chunk size and stall detection
    config = ResumableUploadConfig(
        chunk_size=256,
        stall_minimum_rate=64 * 1024,
        stall_timeout=120,
    )

    async with aiohttp.ClientSession() as transport_session:
        # Create an upload session for the request
        upload_session = AsyncResumableUploadSession(
            upload_url=initial_url,
            config=config,
            transport=transport_session,
            response_type=UploadMediaResponse,
        )

        # Iterate over the upload to receive progress updates as each chunk is transmitted
        payload = b"Example upload data " * 30
        stream = io.BytesIO(payload)
        progress_updates = []
        async for progress in upload_session.upload(
            stream, request_body='{"name": "sample_progress_async.txt"}'
        ):
            print(
                f"Uploaded {progress.bytes_uploaded} bytes | State: {progress.state.name}"
            )
            print(f"Session URL: {progress.upload_url}")
            progress_updates.append(progress)

        # After iteration completes, the final response is available on the session
        response = upload_session.response

        # Handle the response
        assert len(progress_updates) >= 2
        assert progress_updates[0].state == ProgressState.STARTED
        assert progress_updates[-1].state == ProgressState.FINALIZED
        assert response.name == "sample_progress_async.txt"
        assert response.size == len(payload)


@pytest.mark.asyncio
async def test_sample_upload_media_resume_async(intercepted_resumable_upload_rest):
    """Option 3: Resume an interrupted upload using a previously saved session URL (async)."""
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    payload = b"Example upload data " * 30

    async with aiohttp.ClientSession() as transport_session:
        # First obtain a live upload_url and chunk_size by starting an upload and interrupting it
        initial_session = AsyncResumableUploadSession(
            upload_url=initial_url,
            config=ResumableUploadConfig(chunk_size=256),
            transport=transport_session,
            response_type=UploadMediaResponse,
        )
        upload_url = None
        chunk_size = 256
        async for progress in initial_session.upload(
            io.BytesIO(payload), request_body='{"name": "sample_resume_async.txt"}'
        ):
            upload_url = progress.upload_url
            chunk_size = progress.chunk_size
            break

        # Create an upload session for resuming the request
        upload_session = AsyncResumableUploadSession(
            transport=transport_session,
            response_type=UploadMediaResponse,
        )

        # Resume the interrupted upload from the saved session URL and chunk size
        stream = io.BytesIO(payload)
        response = await upload_session.resume(
            upload_url, stream, chunk_size=chunk_size
        )

        # Handle the response
        assert response.name == "sample_resume_async.txt"
        assert response.size == len(payload)


@pytest.mark.asyncio
async def test_sample_upload_media_resume_with_progress_async(
    intercepted_resumable_upload_rest,
):
    """Option 4: Resume an interrupted upload while receiving progress updates (async)."""
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    payload = b"Example upload data " * 30

    async with aiohttp.ClientSession() as transport_session:
        # First obtain a live upload_url and chunk_size by starting an upload and interrupting it
        initial_session = AsyncResumableUploadSession(
            upload_url=initial_url,
            config=ResumableUploadConfig(chunk_size=256),
            transport=transport_session,
            response_type=UploadMediaResponse,
        )
        upload_url = None
        chunk_size = 256
        async for progress in initial_session.upload(
            io.BytesIO(payload),
            request_body='{"name": "sample_resume_progress_async.txt"}',
        ):
            upload_url = progress.upload_url
            chunk_size = progress.chunk_size
            break

        # Create an upload session for resuming the request
        upload_session = AsyncResumableUploadSession(
            transport=transport_session,
            response_type=UploadMediaResponse,
        )

        # Resume the interrupted upload while iterating over progress updates
        stream = io.BytesIO(payload)
        progress_updates = []
        async for progress in upload_session.resume(
            upload_url, stream, chunk_size=chunk_size
        ):
            print(
                f"Resumed {progress.bytes_uploaded} bytes | State: {progress.state.name}"
            )
            print(f"Session URL: {progress.upload_url}")
            print(f"Chunk size: {progress.chunk_size}")
            progress_updates.append(progress)

        # After iteration completes, the final response is available on the session
        response = upload_session.response

        # Handle the response
        assert len(progress_updates) >= 1
        assert progress_updates[-1].state == ProgressState.FINALIZED
        assert response.name == "sample_resume_progress_async.txt"
        assert response.size == len(payload)
