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

from google.api_core.gapic_v1 import client_helpers
from google.auth.exceptions import MutualTLSChannelError


def test_get_default_mtls_endpoint():
    # Test valid API endpoints
    assert (
        client_helpers.get_default_mtls_endpoint("foo.googleapis.com")
        == "foo.mtls.googleapis.com"
    )
    assert (
        client_helpers.get_default_mtls_endpoint("foo.sandbox.googleapis.com")
        == "foo.mtls.sandbox.googleapis.com"
    )

    # Test endpoints that shouldn't be converted
    assert (
        client_helpers.get_default_mtls_endpoint("foo.mtls.googleapis.com")
        == "foo.mtls.googleapis.com"
    )
    assert client_helpers.get_default_mtls_endpoint("foo.com") == "foo.com"

    # Test empty/None endpoints
    assert client_helpers.get_default_mtls_endpoint("") == ""
    assert client_helpers.get_default_mtls_endpoint(None) is None


@mock.patch("google.auth.transport.mtls.should_use_client_cert", autospec=True)
def test_use_client_cert_effective_with_google_auth(mock_method):
    # Test when google-auth supports the method
    mock_method.return_value = True
    assert client_helpers.use_client_cert_effective() is True

    mock_method.return_value = False
    assert client_helpers.use_client_cert_effective() is False


@mock.patch.dict(os.environ, {}, clear=True)
def test_use_client_cert_effective_fallback():
    # We must patch hasattr to simulate google-auth lacking the method
    with mock.patch(
        "google.api_core.gapic_v1.client_helpers.hasattr", return_value=False
    ):
        # Default is false
        assert client_helpers.use_client_cert_effective() is False

        env_true = {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}
        with mock.patch.dict(os.environ, env_true):
            assert client_helpers.use_client_cert_effective() is True

        with mock.patch.dict(
            os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}
        ):
            assert client_helpers.use_client_cert_effective() is False

        with mock.patch.dict(
            os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "invalid"}
        ):
            match_str = "must be either `true` or `false`"
            with pytest.raises(ValueError, match=match_str):
                client_helpers.use_client_cert_effective()


def test_get_api_endpoint_override():
    # If api_override is provided, it should be returned
    # regardless of other args
    endpoint = client_helpers.get_api_endpoint(
        api_override="custom.endpoint.com",
        client_cert_source=None,
        universe_domain="googleapis.com",
        use_mtls_endpoint="auto",
        default_universe="googleapis.com",
        default_mtls_endpoint="foo.mtls.googleapis.com",
        default_endpoint_template="foo.{UNIVERSE_DOMAIN}",
    )
    assert endpoint == "custom.endpoint.com"


def test_get_api_endpoint_mtls_always():
    # use_mtls_endpoint == "always" should use the default mtls endpoint
    endpoint = client_helpers.get_api_endpoint(
        api_override=None,
        client_cert_source=None,
        universe_domain="googleapis.com",
        use_mtls_endpoint="always",
        default_universe="googleapis.com",
        default_mtls_endpoint="foo.mtls.googleapis.com",
        default_endpoint_template="foo.{UNIVERSE_DOMAIN}",
    )
    assert endpoint == "foo.mtls.googleapis.com"


def test_get_api_endpoint_mtls_auto_with_cert():
    # "auto" with client_cert_source should use mtls
    endpoint = client_helpers.get_api_endpoint(
        api_override=None,
        client_cert_source=mock.Mock(),
        universe_domain="googleapis.com",
        use_mtls_endpoint="auto",
        default_universe="googleapis.com",
        default_mtls_endpoint="foo.mtls.googleapis.com",
        default_endpoint_template="foo.{UNIVERSE_DOMAIN}",
    )
    assert endpoint == "foo.mtls.googleapis.com"


def test_get_api_endpoint_mtls_auto_no_cert():
    # "auto" without client_cert_source should use the default template
    endpoint = client_helpers.get_api_endpoint(
        api_override=None,
        client_cert_source=None,
        universe_domain="googleapis.com",
        use_mtls_endpoint="auto",
        default_universe="googleapis.com",
        default_mtls_endpoint="foo.mtls.googleapis.com",
        default_endpoint_template="foo.{UNIVERSE_DOMAIN}",
    )
    assert endpoint == "foo.googleapis.com"


def test_get_api_endpoint_mtls_universe_mismatch():
    # mTLS is only supported in the default universe
    with pytest.raises(MutualTLSChannelError, match="mTLS is not supported"):
        client_helpers.get_api_endpoint(
            api_override=None,
            client_cert_source=mock.Mock(),
            universe_domain="custom-universe.com",
            use_mtls_endpoint="auto",
            default_universe="googleapis.com",
            default_mtls_endpoint="foo.mtls.googleapis.com",
            default_endpoint_template="foo.{UNIVERSE_DOMAIN}",
        )


@mock.patch(
    "google.api_core.gapic_v1.client_helpers.use_client_cert_effective"
)  # noqa: E501
@mock.patch.dict(os.environ, clear=True)
def test_read_environment_variables(mock_effective):
    mock_effective.return_value = True
    os.environ["GOOGLE_API_USE_MTLS_ENDPOINT"] = "always"
    os.environ["GOOGLE_CLOUD_UNIVERSE_DOMAIN"] = "custom.com"

    cert, mtls, domain = client_helpers.read_environment_variables()
    assert cert is True
    assert mtls == "always"
    assert domain == "custom.com"


@mock.patch.dict(os.environ, clear=True)
def test_read_environment_variables_invalid_mtls():
    os.environ["GOOGLE_API_USE_MTLS_ENDPOINT"] = "invalid"
    with pytest.raises(
        MutualTLSChannelError, match="must be `never`, `auto` or `always`"
    ):
        client_helpers.read_environment_variables()


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
    assert client_helpers.get_client_cert_source(b"provided", False) is None

    # When provided_cert_source is given, return provided
    assert (
        client_helpers.get_client_cert_source(b"provided", True) == b"provided"
    )  # noqa: E501

    # When no provided cert but default is available
    assert client_helpers.get_client_cert_source(None, True) == b"default_cert"


def test_get_universe_domain():
    # client_universe_domain takes precedence
    assert (
        client_helpers.get_universe_domain(
            "client.com", "env.com", "default.com"
        )  # noqa: E501
        == "client.com"
    )

    # env takes precedence over default
    assert (
        client_helpers.get_universe_domain(None, "env.com", "default.com")
        == "env.com"  # noqa: E501
    )

    # fallback to default
    assert (
        client_helpers.get_universe_domain(None, None, "default.com")
        == "default.com"  # noqa: E501
    )


def test_get_universe_domain_empty():
    with pytest.raises(ValueError, match="cannot be an empty string"):
        client_helpers.get_universe_domain("", None, "default.com")


def test_setup_request_id():
    import uuid

    # test dict request
    req = {}
    client_helpers.setup_request_id(req, "request_id", True)
    assert "request_id" in req
    uuid_str = req["request_id"]
    uuid.UUID(uuid_str)  # verify it is a valid UUID

    # test dict request when already set
    req = {"request_id": "existing"}
    client_helpers.setup_request_id(req, "request_id", True)
    assert req["request_id"] == "existing"

    class DummyRequest:
        def __init__(self):
            self.request_id = ""

        def HasField(self, field_name):
            if not hasattr(self, field_name):
                raise ValueError()
            return bool(getattr(self, field_name))

    # test object request proto3 optional true
    req_obj = DummyRequest()
    client_helpers.setup_request_id(req_obj, "request_id", True)
    assert req_obj.request_id != ""
    uuid.UUID(req_obj.request_id)

    # test object request proto3 optional false
    req_obj2 = DummyRequest()
    client_helpers.setup_request_id(req_obj2, "request_id", False)
    assert req_obj2.request_id != ""
    uuid.UUID(req_obj2.request_id)
