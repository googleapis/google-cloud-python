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

import datetime
import io
import pytest

from google.api_core import exceptions
from google.api_core.resumable_transfer import (
    ResumableUploadConfig,
    ResumableUploadSession,
    TransferStalledError,
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


def test_resumable_upload_stall_control_success(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "stall_control_success.txt"}'
    data = b"S" * 1024
    stream = io.BytesIO(data)

    # Stall control: 100 bytes/s minimum rate, 5s timeout -> fast upload succeeds easily
    config = ResumableUploadConfig(
        chunk_size=512,
        stall_min_rate=100.0,
        stall_timeout=5.0,
    )

    response = make_resumable_upload(
        transport=client.transport._session,
        request_body=request_body,
        stream=stream,
        upload_url=initial_url,
        config=config,
    )
    assert response.status_code == 200
    final_response = UploadMediaResponse.from_json(response.content)
    assert final_response.name == "stall_control_success.txt"
    assert final_response.size == len(data)


def test_resumable_upload_stall_control_triggers_abort(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "stall_abort.txt"}'
    data = b"S" * 2048
    stream = io.BytesIO(data)

    # Server injects 600ms delay per chunk; client requires high rate (10000000 bytes/s) with 0.5s stall timeout
    scenario_headers = [
        ("X-Goog-Test-Scenario", "happy_path"),
        ("X-Goog-Test-Scenario-Config", '{"delay_ms":600}'),
    ]

    config = ResumableUploadConfig(
        chunk_size=512,
        stall_min_rate=10_000_000.0,  # 10 MB/s minimum
        stall_timeout=0.5,            # Abort if lagging for > 500ms
        headers=scenario_headers,
    )

    with pytest.raises(TransferStalledError) as exc_info:
        make_resumable_upload(
            transport=client.transport._session,
            request_body=request_body,
            stream=stream,
            upload_url=initial_url,
            config=config,
        )

    assert "Upload stalled" in str(exc_info.value)


def test_resumable_upload_overall_deadline_exceeded(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    request_body = '{"name": "deadline_exceeded.txt"}'
    data = b"D" * 2048
    stream = io.BytesIO(data)

    scenario_headers = [
        ("X-Goog-Test-Scenario", "happy_path"),
        ("X-Goog-Test-Scenario-Config", '{"delay_ms":600}'),
    ]

    # Deadline is 300ms from now; 600ms server chunk delay forces deadline expiration
    deadline = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(milliseconds=300)
    config = ResumableUploadConfig(
        chunk_size=512,
        deadline=deadline,
        headers=scenario_headers,
    )

    with pytest.raises(exceptions.DeadlineExceeded) as exc_info:
        make_resumable_upload(
            transport=client.transport._session,
            request_body=request_body,
            stream=stream,
            upload_url=initial_url,
            config=config,
        )

    assert "deadline" in str(exc_info.value).lower()


def test_resumable_upload_stall_vs_deadline_conversion(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"

    scenario_headers = [
        ("X-Goog-Test-Scenario", "happy_path"),
        ("X-Goog-Test-Scenario-Config", '{"delay_ms":600}'),
    ]

    # Case A: Stall occurs before deadline -> raises TransferStalledError
    future_deadline = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=10.0)
    config_stall = ResumableUploadConfig(
        chunk_size=512,
        stall_min_rate=10_000_000.0,
        stall_timeout=0.4,
        deadline=future_deadline,
        headers=scenario_headers,
    )
    with pytest.raises(TransferStalledError) as exc_stall:
        make_resumable_upload(
            transport=client.transport._session,
            request_body='{"name": "stall_before_deadline.txt"}',
            stream=io.BytesIO(b"A" * 1024),
            upload_url=initial_url,
            config=config_stall,
        )
    assert "Upload stalled" in str(exc_stall.value)

    # Case B: Server delay causes overall deadline to expire -> raises DeadlineExceeded
    near_deadline = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(milliseconds=300)
    config_deadline = ResumableUploadConfig(
        chunk_size=512,
        stall_min_rate=10_000_000.0,
        stall_timeout=0.4,
        deadline=near_deadline,
        headers=scenario_headers,
    )
    with pytest.raises(exceptions.DeadlineExceeded) as exc_dead:
        make_resumable_upload(
            transport=client.transport._session,
            request_body='{"name": "deadline_before_stall.txt"}',
            stream=io.BytesIO(b"B" * 1024),
            upload_url=initial_url,
            config=config_deadline,
        )
    assert "deadline" in str(exc_dead.value).lower()

