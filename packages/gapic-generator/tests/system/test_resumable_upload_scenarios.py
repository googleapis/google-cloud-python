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

from google.api_core import exceptions as core_exceptions
from google.api_core.resumable_transfer import (
    ResumableUploadConfig,
    ResumableUploadSession,
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


def test_resumable_upload_scenario_non_fatal_start_error(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "retry_start_upload.txt"}'
    stream = io.BytesIO(b"Hello world!")

    # Injects 503 error on start attempt, which gets automatically retried
    scenario_headers = [
        ("X-Goog-Test-Scenario", "non_fatal_error_on_start"),
        ("X-Goog-Test-Scenario-Config", '{"error_code":503,"failure_count":1}'),
    ]

    response = make_resumable_upload(
        transport=client.transport._session,
        request_body=request_body,
        stream=stream,
        upload_url=initial_url,
        chunk_size=256,
        headers=scenario_headers,
    )
    assert response.status_code == 200
    final_response = UploadMediaResponse.from_json(response.content)
    assert final_response.name == "retry_start_upload.txt"
    assert final_response.size == len(stream.getvalue())


def test_resumable_upload_scenario_fatal_start_error(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "fatal_start_upload.txt"}'
    stream = io.BytesIO(b"Hello fatal error!")

    # Injects 403 Forbidden error on start attempt (Category 3 unretriable error)
    scenario_headers = [
        ("X-Goog-Test-Scenario", "fatal_error_on_start"),
        ("X-Goog-Test-Scenario-Config", '{"error_code":403}'),
    ]

    with pytest.raises(core_exceptions.Forbidden):
        make_resumable_upload(
            transport=client.transport._session,
            request_body=request_body,
            stream=stream,
            upload_url=initial_url,
            headers=scenario_headers,
        )


def test_resumable_upload_scenario_missing_status_header_start_retry(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "missing_status_header_upload.txt"}'
    stream = io.BytesIO(b"Retrying on missing status header!")

    # Intercept first start response and strip X-Goog-Upload-Status header to test Category 1 retry
    original_send = client.transport._session.send
    attempt_count = [0]

    def intercepting_send(request, **kwargs):
        resp = original_send(request, **kwargs)
        if request.headers.get("X-Goog-Upload-Command") == "start":
            attempt_count[0] += 1
            if attempt_count[0] == 1:
                # Strip X-Goog-Upload-Status on first attempt
                resp.headers.pop("X-Goog-Upload-Status", None)
                resp.headers.pop("x-goog-upload-status", None)
        return resp

    client.transport._session.send = intercepting_send
    try:
        response = make_resumable_upload(
            transport=client.transport._session,
            request_body=request_body,
            stream=stream,
            upload_url=initial_url,
        )
        assert response.status_code == 200
        assert attempt_count[0] >= 2  # Verified that start was retried upon missing status header
        final_response = UploadMediaResponse.from_json(response.content)
        assert final_response.name == "missing_status_header_upload.txt"
        assert final_response.size == len(stream.getvalue())
    finally:
        client.transport._session.send = original_send


def test_resumable_upload_scenario_non_fatal_chunk_error(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "recovered_chunk_upload.txt"}'
    stream = io.BytesIO(b"A" * 1024)

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
    assert final_response.name == "recovered_chunk_upload.txt"
    assert final_response.size == len(stream.getvalue())


def test_resumable_upload_partial_commit_recovery(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "partial_commit_upload.txt"}'
    data = b"0123456789" * 50
    stream = io.BytesIO(data)

    # Injects 503 error after server commits only 100 bytes of the chunk
    scenario_headers = [
        ("X-Goog-Test-Scenario", "partial_commit_on_chunk_upload"),
        ("X-Goog-Test-Scenario-Config", '{"error_code":503,"failure_count":1,"after_offset":0,"partial_bytes":100}'),
    ]

    response = make_resumable_upload(
        transport=client.transport._session,
        request_body=request_body,
        stream=stream,
        upload_url=initial_url,
        chunk_size=256,
        headers=scenario_headers,
    )
    assert response.status_code == 200
    final_response = UploadMediaResponse.from_json(response.content)
    assert final_response.name == "partial_commit_upload.txt"
    assert final_response.size == len(data)


def test_resumable_upload_chunk_granularity_alignment(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "granularity_upload.txt"}'
    data = b"X" * 1000
    stream = io.BytesIO(data)

    # Server enforces 256 byte chunk granularity
    scenario_headers = [
        ("X-Goog-Test-Scenario", "chunk_granularity"),
    ]

    response = make_resumable_upload(
        transport=client.transport._session,
        request_body=request_body,
        stream=stream,
        upload_url=initial_url,
        chunk_size=300,  # Request unaligned chunk size (300) -> state machine aligns up to 512
        headers=scenario_headers,
    )
    assert response.status_code == 200
    final_response = UploadMediaResponse.from_json(response.content)
    assert final_response.name == "granularity_upload.txt"
    assert final_response.size == len(data)
