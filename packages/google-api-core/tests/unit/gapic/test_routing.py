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

from unittest import mock

import pytest

from google.auth.exceptions import MutualTLSChannelError

from google.api_core.gapic_v1._routing import (
    _get_api_endpoint,
    _get_default_mtls_endpoint,
    _get_universe_domain,
)


def test_get_default_mtls_endpoint():
    # Test valid API endpoints
    assert _get_default_mtls_endpoint("foo.googleapis.com") == "foo.mtls.googleapis.com"
    assert (
        _get_default_mtls_endpoint("foo.sandbox.googleapis.com")
        == "foo.mtls.sandbox.googleapis.com"
    )

    # Test endpoints that shouldn't be converted
    assert (
        _get_default_mtls_endpoint("foo.mtls.googleapis.com")
        == "foo.mtls.googleapis.com"
    )
    assert _get_default_mtls_endpoint("foo.com") == "foo.com"

    # Test empty/None endpoints
    assert _get_default_mtls_endpoint("") == ""
    assert _get_default_mtls_endpoint(None) is None


def test_get_api_endpoint_override():
    # If api_override is provided, it should be returned
    # regardless of other args
    endpoint = _get_api_endpoint(
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
    endpoint = _get_api_endpoint(
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
    endpoint = _get_api_endpoint(
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
    endpoint = _get_api_endpoint(
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
        _get_api_endpoint(
            api_override=None,
            client_cert_source=mock.Mock(),
            universe_domain="custom-universe.com",
            use_mtls_endpoint="auto",
            default_universe="googleapis.com",
            default_mtls_endpoint="foo.mtls.googleapis.com",
            default_endpoint_template="foo.{UNIVERSE_DOMAIN}",
        )


def test_get_api_endpoint_mtls_case_insensitive():
    # mTLS universe check should be case insensitive
    endpoint = _get_api_endpoint(
        api_override=None,
        client_cert_source=mock.Mock(),
        universe_domain="GOOGLEAPIS.COM",
        use_mtls_endpoint="auto",
        default_universe="googleapis.com",
        default_mtls_endpoint="foo.mtls.googleapis.com",
        default_endpoint_template="foo.{UNIVERSE_DOMAIN}",
    )
    assert endpoint == "foo.mtls.googleapis.com"


def test_get_universe_domain():
    # client_universe_domain takes precedence
    assert (
        _get_universe_domain("client.com", "env.com", "default.com")  # noqa: E501
        == "client.com"
    )

    # env takes precedence over default
    assert (
        _get_universe_domain(None, "env.com", "default.com") == "env.com"  # noqa: E501
    )

    # fallback to default
    assert (
        _get_universe_domain(None, None, "default.com") == "default.com"
    )  # noqa: E501


def test_get_universe_domain_strip():
    # check that whitespace is stripped
    assert (
        _get_universe_domain("  client.com  ", "env.com", "default.com") == "client.com"
    )
    assert _get_universe_domain(None, "  env.com  ", "default.com") == "env.com"


def test_get_universe_domain_empty():
    with pytest.raises(ValueError, match="cannot be an empty string"):
        _get_universe_domain("", None, "default.com")
    with pytest.raises(ValueError, match="cannot be an empty string"):
        _get_universe_domain("   ", None, "default.com")


def test_get_api_endpoint_none_template():
    endpoint = _get_api_endpoint(
        api_override=None,
        client_cert_source=None,
        universe_domain="googleapis.com",
        use_mtls_endpoint="never",
        default_universe="googleapis.com",
        default_mtls_endpoint=None,
        default_endpoint_template=None,
    )
    assert endpoint is None
