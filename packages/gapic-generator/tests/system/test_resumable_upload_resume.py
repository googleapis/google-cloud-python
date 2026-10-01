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
    ProgressState,
    ResumableUploadConfig,
    ResumableUploadSession,
)
from google.showcase import UploadMediaResponse

from conftest import resume_resumable_upload


class _UnseekableBytesStream:
    """File-like stream wrapper that disables seek()."""

    def __init__(self, data: bytes):
        self._buf = io.BytesIO(data)

    def read(self, size: int = -1) -> bytes:
        return self._buf.read(size)

    def seekable(self) -> bool:
        return False


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
    )
    session1 = ResumableUploadSession(
        upload_url=initial_url,
        config=config1,
        transport=client.transport._session,
        response_type=UploadMediaResponse,
    )
    session1._initiate(
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
    )
    session2 = ResumableUploadSession(
        config=config2,
        transport=client.transport._session,
        response_type=UploadMediaResponse,
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
    )
    session1 = ResumableUploadSession(
        upload_url=initial_url,
        config=config1,
        transport=client.transport._session,
        response_type=UploadMediaResponse,
    )
    session1._initiate(
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
    )
    session2 = ResumableUploadSession(
        config=config2,
        transport=client.transport._session,
        response_type=UploadMediaResponse,
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


def test_resumable_upload_resume_chunk_size_override(
    intercepted_resumable_upload_rest,
):
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
    )
    session1 = ResumableUploadSession(
        upload_url=initial_url,
        config=config1,
        transport=client.transport._session,
        response_type=UploadMediaResponse,
    )
    session1._initiate(
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
    )
    session2 = ResumableUploadSession(
        config=config2,
        transport=client.transport._session,
        response_type=UploadMediaResponse,
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


def test_resumable_upload_resume_helper_with_raw_bytes(
    intercepted_resumable_upload_rest,
):
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
    session1._initiate(
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
    )
    final_response = resume_resumable_upload(
        transport=client.transport._session,
        upload_url=saved_url,
        stream=data,
        config=config2,
        response_type=UploadMediaResponse,
    )

    assert isinstance(final_response, UploadMediaResponse)
    assert final_response.name == "helper_bytes.bin"
    assert final_response.size == len(data)


def test_resume_in_progress_upload(intercepted_resumable_upload_rest):
    """2.5 Resumption Suite - Case 1: Resume an in-progress multi-chunk upload."""
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "resume_in_progress.mp4"}'
    total_size = 1_500_000
    chunk_size = 524_288  # 512 KiB
    data = b"P" * total_size
    stream = io.BytesIO(data)

    session1 = ResumableUploadSession(
        upload_url=initial_url,
        config=ResumableUploadConfig(chunk_size=chunk_size),
        transport=client.transport._session,
        response_type=UploadMediaResponse,
    )
    session1._initiate(
        transport=client.transport._session,
        request_body=request_body,
        size=total_size,
    )
    saved_url = session1.upload_url
    assert saved_url is not None

    # Upload only the first 512 KiB chunk
    session1._transmit_chunk(client.transport._session, stream, total_size)
    assert session1.bytes_uploaded == 524_288
    assert not session1.finished

    # Resume from a fresh session with a rewound stream
    stream.seek(0)
    session2 = ResumableUploadSession(
        config=ResumableUploadConfig(chunk_size=chunk_size),
        transport=client.transport._session,
        response_type=UploadMediaResponse,
    )
    snapshots = list(
        session2.iter_resume(
            upload_url=saved_url,
            stream=stream,
            size=total_size,
            chunk_size=chunk_size,
            transport=client.transport._session,
        )
    )

    assert [(p.state, p.bytes_uploaded) for p in snapshots] == [
        (ProgressState.OFFSET_RECEIVED, 524_288),
        (ProgressState.UPLOADING, 1_048_576),
        (ProgressState.FINALIZED, 1_500_000),
    ]
    assert isinstance(session2.response, UploadMediaResponse)
    assert session2.response.name == "resume_in_progress.mp4"
    assert session2.response.size == total_size


def test_resume_finalized_upload(intercepted_resumable_upload_rest):
    """2.5 Resumption Suite - Case 2: Querying/recovering an already-finalized upload."""
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "already_finalized.txt"}'
    total_size = 524_288
    data = b"F" * total_size

    # Complete the upload in Session 1
    session1 = ResumableUploadSession(
        upload_url=initial_url,
        config=ResumableUploadConfig(chunk_size=total_size),
        transport=client.transport._session,
        response_type=UploadMediaResponse,
    )
    resp1 = session1.upload(
        stream=io.BytesIO(data),
        request_body=request_body,
        size=total_size,
    )
    assert isinstance(resp1, UploadMediaResponse)
    assert resp1.size == total_size
    saved_url = session1.upload_url
    assert saved_url is not None

    # Session 2 recovers against the already-finalized session URL
    session2 = ResumableUploadSession(
        config=ResumableUploadConfig(chunk_size=total_size),
        transport=client.transport._session,
        response_type=UploadMediaResponse,
    )
    session2._state._resumable_url = saved_url
    session2._state._upload_url = saved_url
    session2._needs_recovery = True
    progress_queue = []
    snapshots = list(
        session2._transmit_all_chunks(
            client.transport._session,
            io.BytesIO(data),
            total_size,
            progress_queue=progress_queue,
        )
    )

    assert session2.finished
    assert [p.state for p in snapshots] == [
        ProgressState.RECOVERING,
        ProgressState.OFFSET_RECEIVED,
    ]
    assert isinstance(session2.response, UploadMediaResponse)
    assert session2.response.name
    assert session2.response.size == total_size


def test_resume_unseekable_stream_raises(intercepted_resumable_upload_rest):
    """2.5 Resumption Suite - Case 5: Resuming with an unseekable stream raises UnseekableStreamError."""
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "unseekable_resume.bin"}'
    total_size = 1_048_576
    chunk_size = 524_288
    data = b"U" * total_size
    stream1 = io.BytesIO(data)

    # Session 1 uploads first chunk of 512 KiB
    session1 = ResumableUploadSession(
        upload_url=initial_url,
        config=ResumableUploadConfig(chunk_size=chunk_size),
        transport=client.transport._session,
        response_type=UploadMediaResponse,
    )
    session1._initiate(
        transport=client.transport._session,
        request_body=request_body,
        size=total_size,
    )
    saved_url = session1.upload_url
    session1._transmit_chunk(client.transport._session, stream1, total_size)
    assert session1.bytes_uploaded == chunk_size

    # Attempting to resume from offset 524,288 with an unseekable stream must raise UnseekableStreamError
    unseekable_stream = _UnseekableBytesStream(data)
    session2 = ResumableUploadSession(
        config=ResumableUploadConfig(chunk_size=chunk_size),
        transport=client.transport._session,
        response_type=UploadMediaResponse,
    )
    with pytest.raises(exceptions.UnseekableStreamError) as exc_info:
        session2.resume(
            upload_url=saved_url,
            stream=unseekable_stream,
            size=total_size,
            chunk_size=chunk_size,
            transport=client.transport._session,
        )

    assert exc_info.value.upload_url == saved_url
    assert exc_info.value.chunk_size == chunk_size


def test_golden_user_style_resume_seekable(intercepted_resumable_upload_rest):
    """Test Case 3 / 2.5 Case 6: Mid-stream client interruption and resumption with a seekable stream."""
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "golden_user_resume.mp4"}'
    total_size = 1_500_000
    chunk_size = 524_288  # 512 KiB
    data = b"G" * total_size
    stream = io.BytesIO(data)

    class _ClientPauseError(Exception):
        pass

    # Phase 1: Start Session 1 and intentionally abort after the first 512 KiB chunk
    session1 = ResumableUploadSession(
        upload_url=initial_url,
        config=ResumableUploadConfig(chunk_size=chunk_size),
        transport=client.transport._session,
        response_type=UploadMediaResponse,
    )
    session1_snapshots = []
    with pytest.raises(_ClientPauseError):
        for progress in session1.iter_upload(
            stream=stream,
            request_body=request_body,
            size=total_size,
        ):
            session1_snapshots.append(progress)
            if progress.bytes_uploaded >= chunk_size:
                raise _ClientPauseError("Simulated user pause after first chunk")

    # Phase 2: State verification
    saved_url = session1.upload_url
    saved_chunk_size = session1.chunk_size
    assert saved_url is not None
    assert saved_chunk_size == chunk_size
    assert [(p.state, p.bytes_uploaded) for p in session1_snapshots] == [
        (ProgressState.STARTED, 0),
        (ProgressState.UPLOADING, 524_288),
    ]

    # Phase 3: Rewind stream to byte 0 and resume in Session 2
    stream.seek(0)
    session2 = ResumableUploadSession(
        config=ResumableUploadConfig(chunk_size=saved_chunk_size),
        transport=client.transport._session,
        response_type=UploadMediaResponse,
    )
    session2_snapshots = list(
        session2.iter_resume(
            upload_url=saved_url,
            stream=stream,
            size=total_size,
            chunk_size=saved_chunk_size,
            transport=client.transport._session,
        )
    )

    assert [(p.state, p.bytes_uploaded) for p in session2_snapshots] == [
        (ProgressState.OFFSET_RECEIVED, 524_288),
        (ProgressState.UPLOADING, 1_048_576),
        (ProgressState.FINALIZED, 1_500_000),
    ]
    assert session2.finished
    assert isinstance(session2.response, UploadMediaResponse)
    assert session2.response.name == "golden_user_resume.mp4"
    assert session2.response.size == total_size
