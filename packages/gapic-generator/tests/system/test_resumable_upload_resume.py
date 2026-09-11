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

from google.api_core.resumable_transfer import (
    ProgressState,
    ResumableUploadConfig,
    ResumableUploadSession,
)
from google.showcase import UploadMediaResponse


def resume_resumable_upload(
    transport,
    upload_url,
    stream,
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
        config=config,
        resumable_url=upload_url,
        transport=transport,
    )
    return session.resume(
        upload_url=upload_url,
        stream=stream,
        size=size,
        transport=transport,
    )


def test_resumable_upload_resume_direct(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "resume_direct.txt"}'
    data = b"R" * 2048
    stream = io.BytesIO(data)

    scenario_headers = [
        ("X-Goog-Test-Scenario", "chunk_granularity"),
    ]

    # Session 1: Initiate and upload first chunk (512 bytes)
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
    saved_url = session1.upload_url
    assert saved_url is not None

    # Transmit only the first chunk
    session1._transmit_chunk(client.transport._session, stream, len(data))
    assert session1.bytes_uploaded == 512
    assert not session1.finished

    # Session 2: Fresh session simulating resumption across process boundaries
    config2 = ResumableUploadConfig(
        chunk_size=512,
        response_type=UploadMediaResponse,
    )
    session2 = ResumableUploadSession(
        config=config2,
        transport=client.transport._session,
    )

    # Rewind stream to simulate providing full file stream on resume
    stream.seek(0)
    final_response = session2.resume(
        upload_url=saved_url,
        stream=stream,
        size=len(data),
        transport=client.transport._session,
    )

    assert isinstance(final_response, UploadMediaResponse)
    assert final_response.name == "resume_direct.txt"
    assert final_response.size == len(data)
    assert session2.bytes_uploaded == len(data)
    assert session2.finished


def test_resumable_upload_iter_resume_generator(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "iter_resume.txt"}'
    data = b"I" * 1536
    stream = io.BytesIO(data)

    scenario_headers = [
        ("X-Goog-Test-Scenario", "chunk_granularity"),
    ]

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
    saved_url = session1.upload_url
    assert saved_url is not None

    # Transmit first chunk
    session1._transmit_chunk(client.transport._session, stream, len(data))
    assert session1.bytes_uploaded == 512

    # Session 2: Resuming with PEP 255 generator iter_resume
    config2 = ResumableUploadConfig(
        chunk_size=512,
        response_type=UploadMediaResponse,
    )
    session2 = ResumableUploadSession(
        config=config2,
        transport=client.transport._session,
    )

    stream.seek(0)
    progress_snapshots = list(
        session2.iter_resume(
            upload_url=saved_url,
            stream=stream,
            size=len(data),
            transport=client.transport._session,
        )
    )

    # First event should be OFFSET_RECEIVED recovering to 512 bytes
    assert len(progress_snapshots) >= 2
    offset_event = progress_snapshots[0]
    assert offset_event.state == ProgressState.OFFSET_RECEIVED
    assert offset_event.bytes_uploaded == 512

    # Final event should be FINALIZED at 1536 bytes
    final_event = progress_snapshots[-1]
    assert final_event.state == ProgressState.FINALIZED
    assert final_event.bytes_uploaded == len(data)

    assert isinstance(session2.response, UploadMediaResponse)
    assert session2.response.name == "iter_resume.txt"
    assert session2.response.size == len(data)


def test_resumable_upload_resume_chunk_size_override(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "chunk_override.txt"}'
    data = b"C" * 2048
    stream = io.BytesIO(data)

    scenario_headers = [
        ("X-Goog-Test-Scenario", "chunk_granularity"),
    ]

    # Session 1: 256-byte chunks
    config1 = ResumableUploadConfig(
        chunk_size=256,
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
    saved_url = session1.upload_url

    # Transmit 256 bytes
    session1._transmit_chunk(client.transport._session, stream, len(data))
    assert session1.bytes_uploaded == 256

    # Session 2: Resumes overriding chunk_size to 512 (valid multiple of 256)
    config2 = ResumableUploadConfig(
        chunk_size=512,
        response_type=UploadMediaResponse,
    )
    session2 = ResumableUploadSession(
        config=config2,
        transport=client.transport._session,
    )

    stream.seek(0)
    response = session2.resume(
        upload_url=saved_url,
        stream=stream,
        chunk_size=512,
        transport=client.transport._session,
    )

    assert session2.chunk_size == 512
    assert isinstance(response, UploadMediaResponse)
    assert response.name == "chunk_override.txt"
    assert response.size == len(data)


def test_resumable_upload_resume_helper_with_raw_bytes(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "helper_bytes.bin"}'
    data = b"B" * 1024

    scenario_headers = [
        ("X-Goog-Test-Scenario", "chunk_granularity"),
    ]

    # Session 1: Start and upload first chunk
    session1 = ResumableUploadSession(
        upload_url=initial_url,
        config=ResumableUploadConfig(
            chunk_size=256,
            headers=scenario_headers,
        ),
        transport=client.transport._session,
    )
    session1.initiate(
        transport=client.transport._session,
        request_body=request_body,
        size=len(data),
    )
    saved_url = session1.upload_url

    stream1 = io.BytesIO(data)
    session1._transmit_chunk(client.transport._session, stream1, len(data))
    assert session1.bytes_uploaded == 256

    # Resume directly using resume_resumable_upload helper with raw bytes
    config2 = ResumableUploadConfig(
        chunk_size=512,
        response_type=UploadMediaResponse,
    )
    final_response = resume_resumable_upload(
        transport=client.transport._session,
        upload_url=saved_url,
        stream=data,
        config=config2,
    )

    assert isinstance(final_response, UploadMediaResponse)
    assert final_response.name == "helper_bytes.bin"
    assert final_response.size == len(data)
