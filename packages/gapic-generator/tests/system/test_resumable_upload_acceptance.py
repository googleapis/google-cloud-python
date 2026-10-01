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

"""Manual live Google Ads acceptance tests for GAPIC Resumable Upload client libraries.

Skipped by default in CI unless `RUN_GOOGLE_ADS_ACCEPTANCE=true` is set.
Dynamically generates the `YouTubeVideoUploadService` GAPIC library via
`gapic-generator` and exercises `YouTubeVideoUploadServiceClient` and
`YouTubeVideoUploadServiceAsyncClient` (with `grpc`/`grpc_asyncio` and
`rest`/`rest_asyncio` transports) against `https://googleads.googleapis.com`
using two-tier service account impersonation.

To run the manual live Google Ads acceptance suite:
    RUN_GOOGLE_ADS_ACCEPTANCE=true \\
    GOOGLE_ADS_DEVELOPER_TOKEN="<developer-token>" \\
    GOOGLE_ADS_LOGIN_CUSTOMER_ID="7568249731" \\
    GOOGLE_ADS_CUSTOMER_ID="6040249544" \\
    GOOGLE_ADS_TARGET_SERVICE_ACCOUNT="<target-sa>@<project>.iam.gserviceaccount.com" \\
    GOOGLE_ADS_SOURCE_SERVICE_ACCOUNT="<source-sa>@<project>.iam.gserviceaccount.com" \\
    GOOGLE_ADS_VIDEO_PATH="~/Downloads/video.mp4" \\
    pytest tests/system/test_resumable_upload_acceptance.py
"""

from datetime import datetime, timezone
import io
import logging
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, List, Sequence, Tuple
import uuid

import grpc
import pytest

import google.auth
from google.auth import credentials as ga_credentials
from google.auth import impersonated_credentials
import google.auth.transport.requests
from google.oauth2 import service_account
from google.api_core import exceptions
from google.api_core.resumable_transfer import (
    ProgressState,
    ResumableUploadConfig,
    UploadProgress,
)


class _ClientPauseError(Exception):
    """Client-side exception raised inside progress loop to simulate user pause."""

    def __init__(self, message: str, upload_url: str, chunk_size: int) -> None:
        super().__init__(message)
        self.upload_url = upload_url
        self.chunk_size = chunk_size


# =============================================================================
# Manual Live Google Ads (YouTubeVideoUploadService) Acceptance Tests
# =============================================================================


ADWORDS_SCOPE = "https://www.googleapis.com/auth/adwords"
SOURCE_SCOPES = (
    "https://www.googleapis.com/auth/iam",
    "https://www.googleapis.com/auth/cloud-platform",
)

YOUTUBE_VIDEO_UPLOAD_PROTO = """\
syntax = "proto3";

package google.ads.googleads.v23.services;

import "google/api/annotations.proto";
import "google/api/client.proto";

enum YouTubeVideoPrivacy {
  UNSPECIFIED = 0;
  UNKNOWN = 1;
  PUBLIC = 2;
  UNLISTED = 3;
}

message YouTubeVideoUpload {
  string resource_name = 1;
  int64 video_upload_id = 2;
  string channel_id = 3;
  string video_id = 4;
  string video_title = 6;
  string video_description = 7;
  YouTubeVideoPrivacy video_privacy = 8;
}

message CreateYouTubeVideoUploadRequest {
  string customer_id = 1;
  YouTubeVideoUpload you_tube_video_upload = 2;
}

message CreateYouTubeVideoUploadResponse {
  string resource_name = 1;
}

service YouTubeVideoUploadService {
  option (google.api.default_host) = "googleads.googleapis.com";
  option (google.api.oauth_scopes) = "https://www.googleapis.com/auth/adwords";

  rpc CreateYouTubeVideoUpload(CreateYouTubeVideoUploadRequest)
      returns (CreateYouTubeVideoUploadResponse) {
    option (google.api.http) = {
      post: "/v23/customers/{customer_id=*}/youTubeVideoUploads:create"
      body: "*"
    };
  }
}
"""

GOOGLEADS_SERVICE_YAML = """\
type: google.api.Service
config_version: 3
name: googleads.googleapis.com
title: Google Ads API
apis:
- name: google.ads.googleads.v23.services.YouTubeVideoUploadService
publishing:
  library_settings:
  - version: google.ads.googleads.v23.services
    python_settings:
      experimental_features:
        rest_async_io_enabled: true
"""


def _load_source_credentials() -> ga_credentials.Credentials:
    creds, _ = google.auth.default(scopes=list(SOURCE_SCOPES))
    return creds


def _load_impersonated_credentials() -> impersonated_credentials.Credentials:
    target_principal = os.environ.get("GOOGLE_ADS_TARGET_SERVICE_ACCOUNT", "")
    if not target_principal:
        pytest.skip("GOOGLE_ADS_TARGET_SERVICE_ACCOUNT is not set.")
    source_creds = _load_source_credentials()
    return impersonated_credentials.Credentials(
        source_credentials=source_creds,
        target_principal=target_principal,
        target_scopes=[ADWORDS_SCOPE],
        lifetime=3600,
    )


def _google_ads_metadata() -> Sequence[Tuple[str, str]]:
    developer_token = os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN", "")
    login_customer_id = os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID", "")
    if not developer_token or not login_customer_id:
        pytest.skip(
            "GOOGLE_ADS_DEVELOPER_TOKEN and GOOGLE_ADS_LOGIN_CUSTOMER_ID are required."
        )
    return (
        ("developer-token", developer_token),
        ("login-customer-id", login_customer_id),
    )


def _google_ads_customer_id() -> str:
    customer_id = os.environ.get(
        "GOOGLE_ADS_CUSTOMER_ID",
        os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID", ""),
    )
    if not customer_id:
        pytest.skip("GOOGLE_ADS_CUSTOMER_ID is required.")
    return customer_id


def _open_upload_file() -> Tuple[io.BufferedReader, int]:
    raw_path = os.environ.get("GOOGLE_ADS_VIDEO_PATH", "~/Downloads/video.mp4")
    expanded = Path(os.path.expanduser(raw_path)).resolve()
    if not expanded.is_file():
        pytest.skip(f"Test media file not found at {expanded}")
    f = open(expanded, "rb")
    return f, expanded.stat().st_size


def _extract_detail_type_names(err_or_details: Any) -> List[str]:
    details = (
        getattr(err_or_details, "details", None)
        if isinstance(err_or_details, Exception)
        else err_or_details
    )
    if not details and isinstance(err_or_details, Exception):
        import json

        try:
            payload = json.loads(getattr(err_or_details, "message", "") or "")
            if isinstance(payload, dict):
                details = payload.get("error", {}).get("details", [])
        except ValueError:
            details = []
    if not details:
        return []
    names: List[str] = []
    for detail in details:
        if isinstance(detail, dict) and "@type" in detail:
            names.append(
                str(detail["@type"]).removeprefix("type.googleapis.com/")
            )
        elif hasattr(detail, "DESCRIPTOR"):
            full_name = detail.DESCRIPTOR.full_name
            if (
                full_name == "google.rpc.ResourceInfo"
                and getattr(detail, "resource_type", "").startswith(
                    "type.googleapis.com/"
                )
            ):
                names.append(
                    detail.resource_type.removeprefix("type.googleapis.com/")
                )
            else:
                names.append(full_name)
        elif hasattr(detail, "type_url") and detail.type_url:
            names.append(
                str(detail.type_url).removeprefix("type.googleapis.com/")
            )
        else:
            names.append(type(detail).__name__)
    return names


@pytest.fixture(scope="module")
def generated_google_ads_module(tmp_path_factory):
    """Dynamically generates the Google Ads YouTubeVideoUploadService GAPIC client."""
    from google.api import annotations_pb2
    import grpc_tools

    tmp_dir = tmp_path_factory.mktemp("googleads_gapic")
    proto_rel = Path(
        "google", "ads", "googleads", "v23", "services", "you_tube_video_upload_service.proto"
    )
    proto_path = tmp_dir / proto_rel
    proto_path.parent.mkdir(parents=True, exist_ok=True)
    proto_path.write_text(YOUTUBE_VIDEO_UPLOAD_PROTO, encoding="utf-8")

    yaml_path = tmp_dir / "googleads_v23.yaml"
    yaml_path.write_text(GOOGLEADS_SERVICE_YAML, encoding="utf-8")

    googleapis_include = str(Path(annotations_pb2.__file__).resolve().parents[2])
    grpc_tools_include = str(Path(grpc_tools.__file__).resolve().parent / "_proto")

    cmd = [
        sys.executable,
        "-m",
        "grpc_tools.protoc",
        f"-I{tmp_dir}",
        f"-I{googleapis_include}",
        f"-I{grpc_tools_include}",
        "--experimental_allow_proto3_optional",
        (
            "--python_gapic_opt="
            f"transport=grpc+rest,service-yaml={yaml_path}"
        ),
        f"--python_gapic_out={tmp_dir}",
        str(proto_rel),
    ]
    env = os.environ.copy()
    bin_dir = str(Path(sys.executable).resolve().parent)
    env["PATH"] = f"{bin_dir}{os.pathsep}{env.get('PATH', '')}"
    repo_root = str(Path(__file__).resolve().parents[2])
    existing_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        f"{repo_root}{os.pathsep}{existing_pythonpath}"
        if existing_pythonpath
        else repo_root
    )
    subprocess.run(cmd, check=True, env=env)

    sys.path.insert(0, str(tmp_dir))
    import importlib

    if "google" in sys.modules and hasattr(sys.modules["google"], "__path__"):
        google_pkg_dir = str(tmp_dir / "google")
        if google_pkg_dir not in sys.modules["google"].__path__:
            sys.modules["google"].__path__.append(google_pkg_dir)

    module = importlib.import_module(
        "google.ads.googleads_v23.services.you_tube_video_upload_service"
    )
    return module


@pytest.mark.skipif(
    os.environ.get("RUN_GOOGLE_ADS_ACCEPTANCE", "").lower() != "true",
    reason=(
        "Manual acceptance test against live Google Ads YouTubeVideoUploadService. "
        "Set RUN_GOOGLE_ADS_ACCEPTANCE=true to run."
    ),
)
class TestGoogleAdsLiveAcceptance:
    """Manual live acceptance tests against Google Ads YouTubeVideoUploadService."""

    @pytest.fixture(autouse=True)
    def _disable_mtls(self, monkeypatch):
        monkeypatch.setenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")

    @pytest.fixture(autouse=True)
    def _capture_diagnostic_trace(self, request):
        log_buffer = io.StringIO()
        handler = logging.StreamHandler(log_buffer)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(
            logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
        )
        root_logger = logging.getLogger()
        prev_level = root_logger.level
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(handler)
        yield
        root_logger.removeHandler(handler)
        root_logger.setLevel(prev_level)
        contents = log_buffer.getvalue()
        if contents:
            safe_name = re.sub(r"[^a-zA-Z0-9_-]+", "_", request.node.name)
            ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            log_path = Path(f"/tmp/googleads_acceptance_{safe_name}_{ts}.log")
            log_path.write_text(contents, encoding="utf-8")

    def test_adc_source_credentials_are_service_account(self):
        """Test Case 1: ADC Source Credential Validation."""
        creds = _load_source_credentials()
        assert isinstance(creds, service_account.Credentials)
        expected_source_sa = os.environ.get("GOOGLE_ADS_SOURCE_SERVICE_ACCOUNT")
        if expected_source_sa:
            assert creds.service_account_email == expected_source_sa

    def test_impersonated_credentials_fetch_access_token(self):
        """Test Case 2: Impersonated Access Token Generation."""
        creds = _load_impersonated_credentials()
        creds.refresh(google.auth.transport.requests.Request())
        headers = {}
        creds.apply(headers)

        assert creds.token is not None
        assert len(creds.token) > 0
        auth_header = headers.get("authorization") or headers.get("Authorization")
        assert auth_header is not None
        assert auth_header.startswith("Bearer ")
        assert creds.expiry is not None
        now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
        assert creds.expiry > now_utc

    @pytest.mark.parametrize("transport", ["grpc", "rest"])
    def test_upload_with_impersonated_credentials(
        self, generated_google_ads_module, transport
    ):
        """Test Case 4: Complete Resumable Media Upload."""
        client_cls = generated_google_ads_module.YouTubeVideoUploadServiceClient
        client = client_cls(
            credentials=_load_impersonated_credentials(),
            transport=transport,
        )
        stream, upload_size = _open_upload_file()
        try:
            upload_session = client.create_you_tube_video_upload(
                request={
                    "customer_id": _google_ads_customer_id(),
                    "you_tube_video_upload": {
                        "video_title": "Test video",
                        "video_description": "Testing defaults",
                        "video_privacy": "UNLISTED",
                    },
                },
                metadata=_google_ads_metadata(),
            )
            progress_records: List[UploadProgress] = []
            for progress in upload_session.iter_upload(
                stream, size=upload_size, content_type="video/mp4"
            ):
                progress_records.append(progress)

            response = upload_session.response
            assert response is not None
            assert re.match(
                r"^customers/\d+/youTubeVideoUploads/\d+$",
                response.resource_name,
            )
            assert len(progress_records) >= 2
            assert progress_records[0].state == ProgressState.STARTED
            assert progress_records[-1].state == ProgressState.FINALIZED
            assert progress_records[-1].bytes_uploaded == upload_size
        finally:
            stream.close()

    @pytest.mark.parametrize("transport", ["grpc", "rest"])
    def test_golden_user_style_resume_seekable(
        self, generated_google_ads_module, transport
    ):
        """Test Case 5: Mid-Stream Interruption & Seekable Resumption."""
        client_cls = generated_google_ads_module.YouTubeVideoUploadServiceClient
        client = client_cls(
            credentials=_load_impersonated_credentials(),
            transport=transport,
        )
        stream, upload_size = _open_upload_file()
        chunk_size = 512 * 1024  # 512 KiB
        request_payload = {
            "customer_id": _google_ads_customer_id(),
            "you_tube_video_upload": {
                "video_title": "Test video",
                "video_description": "Testing defaults",
                "video_privacy": "UNLISTED",
            },
        }
        try:
            session1 = client.create_you_tube_video_upload(
                request=request_payload,
                config=ResumableUploadConfig(chunk_size=chunk_size),
                metadata=_google_ads_metadata(),
            )
            with pytest.raises(_ClientPauseError) as exc_info:
                for progress in session1.iter_upload(
                    stream, size=upload_size, content_type="video/mp4"
                ):
                    if (
                        progress.state == ProgressState.UPLOADING
                        and progress.bytes_uploaded >= chunk_size
                    ):
                        raise _ClientPauseError(
                            "User paused upload",
                            upload_url=progress.upload_url,
                            chunk_size=session1.chunk_size,
                        )

            saved_url = exc_info.value.upload_url
            saved_chunk_size = exc_info.value.chunk_size
            assert saved_url
            assert saved_chunk_size >= chunk_size
            assert session1.bytes_uploaded >= chunk_size

            stream.seek(0)
            session2 = client.create_you_tube_video_upload(
                request=request_payload,
                metadata=_google_ads_metadata(),
            )
            progress_records_2: List[UploadProgress] = []
            for progress in session2.iter_resume(
                saved_url,
                stream,
                size=upload_size,
                chunk_size=saved_chunk_size,
            ):
                progress_records_2.append(progress)

            response = session2.response
            assert response is not None
            assert re.match(
                r"^customers/\d+/youTubeVideoUploads/\d+$",
                response.resource_name,
            )
            assert len(progress_records_2) >= 2
            assert progress_records_2[0].state == ProgressState.OFFSET_RECEIVED
            assert progress_records_2[0].bytes_uploaded >= chunk_size
            assert progress_records_2[-1].state == ProgressState.FINALIZED
            assert progress_records_2[-1].bytes_uploaded == upload_size
        finally:
            stream.close()

    if os.environ.get("GAPIC_PYTHON_ASYNC", "true") == "true":


        @pytest.mark.asyncio
        @pytest.mark.parametrize("transport", ["grpc_asyncio", "rest_asyncio"])
        async def test_async_upload_with_impersonated_credentials(
            self, generated_google_ads_module, transport
        ):
            """Async Test Case 4: Complete Resumable Media Upload."""
            client_cls = (
                generated_google_ads_module.YouTubeVideoUploadServiceAsyncClient
            )
            client = client_cls(
                credentials=_load_impersonated_credentials(),
                transport=transport,
            )
            stream, upload_size = _open_upload_file()
            try:
                upload_session = await client.create_you_tube_video_upload(
                    request={
                        "customer_id": _google_ads_customer_id(),
                        "you_tube_video_upload": {
                            "video_title": "Test video",
                            "video_description": "Testing defaults",
                            "video_privacy": "UNLISTED",
                        },
                    },
                    metadata=_google_ads_metadata(),
                )
                progress_records: List[UploadProgress] = []
                async for progress in upload_session.upload(
                    stream, size=upload_size, content_type="video/mp4"
                ):
                    progress_records.append(progress)

                response = upload_session.response
                assert response is not None
                assert re.match(
                    r"^customers/\d+/youTubeVideoUploads/\d+$",
                    response.resource_name,
                )
                assert len(progress_records) >= 2
                assert progress_records[0].state == ProgressState.STARTED
                assert progress_records[-1].state == ProgressState.FINALIZED
                assert progress_records[-1].bytes_uploaded == upload_size
            finally:
                stream.close()

        @pytest.mark.asyncio
        @pytest.mark.parametrize("transport", ["grpc_asyncio", "rest_asyncio"])
        async def test_async_golden_user_style_resume_seekable(
            self, generated_google_ads_module, transport
        ):
            """Async Test Case 5: Mid-Stream Interruption & Seekable Resumption."""
            client_cls = (
                generated_google_ads_module.YouTubeVideoUploadServiceAsyncClient
            )
            client = client_cls(
                credentials=_load_impersonated_credentials(),
                transport=transport,
            )
            stream, upload_size = _open_upload_file()
            chunk_size = 512 * 1024  # 512 KiB
            request_payload = {
                "customer_id": _google_ads_customer_id(),
                "you_tube_video_upload": {
                    "video_title": "Test video",
                    "video_description": "Testing defaults",
                    "video_privacy": "UNLISTED",
                },
            }
            try:
                session1 = await client.create_you_tube_video_upload(
                    request=request_payload,
                    config=ResumableUploadConfig(chunk_size=chunk_size),
                    metadata=_google_ads_metadata(),
                )
                with pytest.raises(_ClientPauseError) as exc_info:
                    async for progress in session1.upload(
                        stream, size=upload_size, content_type="video/mp4"
                    ):
                        if (
                            progress.state == ProgressState.UPLOADING
                            and progress.bytes_uploaded >= chunk_size
                        ):
                            raise _ClientPauseError(
                                "User paused upload",
                                upload_url=progress.upload_url,
                                chunk_size=session1.chunk_size,
                            )

                saved_url = exc_info.value.upload_url
                saved_chunk_size = exc_info.value.chunk_size
                assert saved_url
                assert saved_chunk_size >= chunk_size
                assert session1.bytes_uploaded >= chunk_size

                stream.seek(0)
                session2 = await client.create_you_tube_video_upload(
                    request=request_payload,
                    metadata=_google_ads_metadata(),
                )
                progress_records_2: List[UploadProgress] = []
                async for progress in session2.resume(
                    saved_url,
                    stream,
                    size=upload_size,
                    chunk_size=saved_chunk_size,
                ):
                    progress_records_2.append(progress)

                response = session2.response
                assert response is not None
                assert re.match(
                    r"^customers/\d+/youTubeVideoUploads/\d+$",
                    response.resource_name,
                )
                assert len(progress_records_2) >= 2
                assert progress_records_2[0].state == ProgressState.OFFSET_RECEIVED
                assert progress_records_2[0].bytes_uploaded >= chunk_size
                assert progress_records_2[-1].state == ProgressState.FINALIZED
                assert progress_records_2[-1].bytes_uploaded == upload_size
            finally:
                stream.close()
