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
from google.showcase import (
    ResumableUploadServiceClient,
    UploadMediaRequest,
    UploadMediaResponse,
)


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


def test_resumable_upload_start(intercepted_resumable_upload_rest):
    client, interceptor = intercepted_resumable_upload_rest
    response = client.upload_media(request=UploadMediaRequest(name="test_file.txt"))

    assert isinstance(response, UploadMediaResponse)
    assert response.name == ""
    assert response.size == 0

    # Verify that the generated client automatically added the resumable upload protocol headers
    req_meta = dict(interceptor.request_metadata)
    assert req_meta.get("x-goog-upload-protocol") == "resumable"
    assert req_meta.get("x-goog-upload-command") == "start"

    # Verify that the server responded with active status and upload URL
    resp_meta = {k.lower(): str(v) for k, v in interceptor.response_metadata}
    assert resp_meta.get("x-goog-upload-status") == "active"
    assert "x-goog-upload-url" in resp_meta


def test_resumable_upload_custom_metadata(intercepted_resumable_upload_rest):
    client, interceptor = intercepted_resumable_upload_rest
    custom_metadata = [("x-custom-header", "custom-val")]
    response = client.upload_media(
        request=UploadMediaRequest(name="test_file.txt"),
        metadata=custom_metadata,
    )

    assert isinstance(response, UploadMediaResponse)
    assert response.name == ""
    assert response.size == 0

    req_meta = dict(interceptor.request_metadata)
    assert req_meta.get("x-goog-upload-protocol") == "resumable"
    assert req_meta.get("x-goog-upload-command") == "start"
    assert req_meta.get("x-custom-header") == "custom-val"

    resp_meta = {k.lower(): str(v) for k, v in interceptor.response_metadata}
    assert resp_meta.get("x-goog-upload-status") == "active"


def test_resumable_upload_finalize_response(intercepted_resumable_upload_rest):
    client, interceptor = intercepted_resumable_upload_rest

    # 1. Start upload session
    client.upload_media(request=UploadMediaRequest(name="test_file.txt"))
    resp_meta = {k.lower(): str(v) for k, v in interceptor.response_metadata}
    upload_url = resp_meta.get("x-goog-upload-url")

    # 2. Upload and finalize using the resumable media helper
    stream = io.BytesIO(b"Hello world from resumable upload!")
    finalize_response = resume_resumable_upload(
        transport=client.transport._session,
        upload_url=upload_url,
        stream=stream,
    )
    assert finalize_response.status_code == 200

    # 3. Deserialize backend response proto
    final_response = UploadMediaResponse.from_json(finalize_response.content)

    # Verify that the backend service returned the resource name and size matching the request
    assert final_response.name == "test_file.txt"
    assert final_response.size == len(stream.getvalue())


@pytest.mark.parametrize(
    "content_type, payload",
    [
        ("application/json", b'{"name": "test_file.json"}'),
        ("text/plain", b"Hello, this is plain text content!"),
        ("application/octet-stream", b"\x00\x01\x02\x03\x04\x05\xff\xfe"),
        ("image/png", b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00"),
    ],
)
def test_resumable_upload_different_content_types(
    intercepted_resumable_upload_rest, content_type, payload
):
    client, interceptor = intercepted_resumable_upload_rest

    # 1. Start upload session
    client.upload_media(request=UploadMediaRequest(name="test_upload"))
    resp_meta = {k.lower(): str(v) for k, v in interceptor.response_metadata}
    upload_url = resp_meta.get("x-goog-upload-url")

    # 2. Upload and finalize with the specific Content-Type using helper
    finalize_response = resume_resumable_upload(
        transport=client.transport._session,
        upload_url=upload_url,
        stream=payload,
        content_type=content_type,
    )
    assert finalize_response.status_code == 200

    # 3. Deserialize and verify response name and size
    final_response = UploadMediaResponse.from_json(finalize_response.content)
    assert final_response.name == "test_upload"
    assert final_response.size == len(payload)




def test_resumable_upload_session_direct_execution(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    payload = b"Direct execution payload using ResumableUploadSession!"

    config = ResumableUploadConfig(
        response_type=UploadMediaResponse,
        chunk_size=256,
    )
    session = ResumableUploadSession(
        upload_url=initial_url,
        config=config,
        transport=client.transport._session,
    )

    response = session.upload(
        stream=io.BytesIO(payload),
        request_body='{"name": "direct_session.txt"}',
    )

    assert isinstance(response, UploadMediaResponse)
    assert response.name == "direct_session.txt"
    assert response.size == len(payload)

    # Verify session properties
    assert session.finished is True
    assert session.bytes_uploaded == len(payload)
    assert session.response is not None
    assert session.response.name == "direct_session.txt"
    assert session.upload_url is not None
    assert "sid=" in session.upload_url
    assert session.chunk_size > 0


def test_resumable_upload_session_raw_bytes_payload(intercepted_resumable_upload_rest):
    client, _ = intercepted_resumable_upload_rest
    initial_url = f"{client.transport._host}/resumable/upload/v1beta1/media/upload"
    payload = b"Raw bytes payload directly passed to upload() method"

    config = ResumableUploadConfig(response_type=UploadMediaResponse)
    session = ResumableUploadSession(
        upload_url=initial_url,
        config=config,
        transport=client.transport._session,
    )

    response = session.upload(
        stream=payload,
        request_body='{"name": "raw_bytes_session.txt"}',
    )

    assert isinstance(response, UploadMediaResponse)
    assert response.name == "raw_bytes_session.txt"
    assert response.size == len(payload)
    assert session.response == response
