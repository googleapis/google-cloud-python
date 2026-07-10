# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from unittest import mock

import pytest

try:
    import grpc  # noqa: F401
except ImportError:
    pytest.skip("No GRPC", allow_module_level=True)

from google.api_core.gapic_v1._client_cert import (
    get_client_cert_source,
    use_client_cert_effective,
)


@mock.patch("google.auth.transport.mtls.should_use_client_cert", create=True)
def test_use_client_cert_effective_with_google_auth(mock_method):
    # Test when google-auth supports the method
    mock_method.return_value = True
    assert use_client_cert_effective() is True

    mock_method.return_value = False
    assert use_client_cert_effective() is False


@mock.patch.dict(os.environ, {}, clear=True)
def test_use_client_cert_effective_fallback():
    # We must patch hasattr to simulate google-auth lacking the method
    with mock.patch(
        "google.api_core.gapic_v1._client_cert.hasattr", return_value=False
    ):
        # Default is false
        assert use_client_cert_effective() is False

        env_true = {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}
        with mock.patch.dict(os.environ, env_true):
            assert use_client_cert_effective() is True

        with mock.patch.dict(
            os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}
        ):
            assert use_client_cert_effective() is False

        with mock.patch.dict(
            os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "invalid"}
        ):
            match_str = "must be either `true` or `false`"
            with pytest.raises(ValueError, match=match_str):
                use_client_cert_effective()


@mock.patch(
    "google.auth.transport.mtls.has_default_client_cert_source", create=True
)  # noqa: E501
@mock.patch(
    "google.auth.transport.mtls.default_client_cert_source", create=True
)  # noqa: E501
def test_get_client_cert_source(mock_default, mock_has_default):
    mock_default.return_value = b"default_cert"
    mock_has_default.return_value = True

    # When use_cert_flag is False, return None
    assert get_client_cert_source(b"provided", False) is None

    # When provided_cert_source is given, return provided
    assert get_client_cert_source(b"provided", True) == b"provided"  # noqa: E501

    # When no provided cert but default is available
    assert get_client_cert_source(None, True) == b"default_cert"
