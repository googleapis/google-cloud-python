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
    UploadProgress,
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
    assert response.status_code == 200

    final_response = UploadMediaResponse.from_json(response.content)
    assert final_response.name == "full_e2e_upload.txt"
    assert final_response.size == len(stream.getvalue())


def test_resumable_upload_callback_progress_tracking(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "progress_tracked_upload.txt"}'
    payload = b"0123456789" * 100
    stream = io.BytesIO(payload)

    progress_events = []

    def on_progress(p):
        progress_events.append((p.bytes_uploaded, p.state.value, p.upload_url, p.chunk_size))

    scenario_headers = [("X-Goog-Test-Scenario", "chunk_granularity")]
    config = ResumableUploadConfig(
        chunk_size=256,
        on_progress=on_progress,
        headers=scenario_headers,
    )

    response = make_resumable_upload(
        transport=client.transport._session,
        request_body=request_body,
        stream=stream,
        upload_url=initial_url,
        config=config,
    )
    assert response.status_code == 200

    # Verify progress notifications occurred in order
    assert len(progress_events) >= 3
    assert progress_events[0][1] == "started"
    assert progress_events[-1][1] == "finalized"
    assert progress_events[-1][0] == len(payload)
    for bytes_up, state, u, chunk_sz in progress_events:
        assert "sid=" in u
        assert chunk_sz == 256


def test_resumable_upload_generator_progress_tracking(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    payload = b"0123456789" * 100
    stream = io.BytesIO(payload)

    scenario_headers = [("X-Goog-Test-Scenario", "chunk_granularity")]
    config = ResumableUploadConfig(
        chunk_size=256,
        response_type=UploadMediaResponse,
        headers=scenario_headers,
    )
    session = ResumableUploadSession(
        upload_url=initial_url,
        config=config,
        transport=client.transport._session,
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
        chunk_size=512,
        headers=scenario_headers,
    )
    assert response.status_code == 200
    final_response = UploadMediaResponse.from_json(response.content)
    assert final_response.name == "unseekable_stream_upload.txt"
    assert final_response.size == len(data)
