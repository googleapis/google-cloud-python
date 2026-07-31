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
#
"""Tests for the compatibility module for older versions of google-api-core."""

import re
import pytest
import os

from google.cloud.redis_v1 import _compat as universe

from google.auth.exceptions import MutualTLSChannelError
import google.auth.transport.mtls
from unittest import mock


def test_get_universe_domain():
    # When universe_domain is provided
    assert (
        universe.get_universe_domain("foo.com", default_universe="default.com")
        == "foo.com"
    )
    assert (
        universe.get_universe_domain("  foo.com  ", default_universe="default.com")
        == "foo.com"
    )

    # When universe_domain is None, falls back to default_universe
    assert (
        universe.get_universe_domain(None, default_universe="default.com")
        == "default.com"
    )

    # When multiple potential universes are provided, resolves in order of preference
    assert (
        universe.get_universe_domain(
            "foo.com", "bar.com", default_universe="default.com"
        )
        == "foo.com"
    )
    assert (
        universe.get_universe_domain(None, "bar.com", default_universe="default.com")
        == "bar.com"
    )
    assert (
        universe.get_universe_domain(None, None, default_universe="default.com")
        == "default.com"
    )

    # EmptyUniverseError raised when resolved value is empty string
    with pytest.raises(universe.EmptyUniverseError) as excinfo:
        universe.get_universe_domain("", default_universe="default.com")
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."

    with pytest.raises(universe.EmptyUniverseError) as excinfo:
        universe.get_universe_domain("   ", default_universe="default.com")
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."

    with pytest.raises(universe.EmptyUniverseError) as excinfo:
        universe.get_universe_domain(None, "", default_universe="default.com")
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


def test_get_default_mtls_endpoint():
    # Test valid API endpoints
    assert (
        universe.get_default_mtls_endpoint("foo.googleapis.com")
        == "foo.mtls.googleapis.com"
    )
    assert (
        universe.get_default_mtls_endpoint("foo.sandbox.googleapis.com")
        == "foo.mtls.sandbox.googleapis.com"
    )
    # Test case-insensitivity
    assert (
        universe.get_default_mtls_endpoint("foo.GoogleAPIs.com")
        == "foo.mtls.googleapis.com"
    )
    assert (
        universe.get_default_mtls_endpoint("foo.Sandbox.GoogleAPIs.com")
        == "foo.mtls.sandbox.googleapis.com"
    )

    # Test valid API endpoints with schemes
    assert (
        universe.get_default_mtls_endpoint("https://foo.googleapis.com")
        == "https://foo.mtls.googleapis.com"
    )
    assert (
        universe.get_default_mtls_endpoint("http://foo.googleapis.com:8080/v1")
        == "http://foo.mtls.googleapis.com:8080/v1"
    )

    # Test valid API endpoints with ports
    assert (
        universe.get_default_mtls_endpoint("foo.googleapis.com:443")
        == "foo.mtls.googleapis.com:443"
    )
    assert (
        universe.get_default_mtls_endpoint("foo.sandbox.googleapis.com:443")
        == "foo.mtls.sandbox.googleapis.com:443"
    )
    # Test case-insensitivity with ports
    assert (
        universe.get_default_mtls_endpoint("foo.GoogleAPIs.com:443")
        == "foo.mtls.googleapis.com:443"
    )
    assert (
        universe.get_default_mtls_endpoint("foo.Sandbox.GoogleAPIs.com:443")
        == "foo.mtls.sandbox.googleapis.com:443"
    )

    # Test endpoints that shouldn't be converted
    assert (
        universe.get_default_mtls_endpoint("foo.mtls.googleapis.com")
        == "foo.mtls.googleapis.com"
    )
    assert universe.get_default_mtls_endpoint("foo.com") == "foo.com"
    assert universe.get_default_mtls_endpoint("foo.com:8080") == "foo.com:8080"

    # Test empty/None endpoints
    assert universe.get_default_mtls_endpoint("") == ""
    assert universe.get_default_mtls_endpoint(None) is None

    # Test endpoints without host
    assert universe.get_default_mtls_endpoint("http://") == "http://"
    assert universe.get_default_mtls_endpoint("https://") == "https://"


@pytest.mark.parametrize(
    "api_override,universe_domain,default_universe,default_mtls_endpoint,default_endpoint_template,use_mtls,expected",
    [
        (
            "foo.com",
            "googleapis.com",
            "googleapis.com",
            "foo.mtls.googleapis.com",
            "foo.{UNIVERSE_DOMAIN}",
            True,
            "foo.com",
        ),
        (
            None,
            "googleapis.com",
            "googleapis.com",
            "foo.mtls.googleapis.com",
            "foo.{UNIVERSE_DOMAIN}",
            True,
            "foo.mtls.googleapis.com",
        ),
        (
            None,
            "googleapis.com",
            "googleapis.com",
            "foo.mtls.googleapis.com",
            "foo.{UNIVERSE_DOMAIN}",
            False,
            "foo.googleapis.com",
        ),
        (
            None,
            "bar.com",
            "googleapis.com",
            "foo.mtls.googleapis.com",
            "foo.{UNIVERSE_DOMAIN}",
            True,
            MutualTLSChannelError,
        ),
        (
            None,
            "googleapis.com",
            "googleapis.com",
            None,
            "foo.{UNIVERSE_DOMAIN}",
            True,
            ValueError,
        ),
    ],
)
def test_get_api_endpoint(
    api_override,
    universe_domain,
    default_universe,
    default_mtls_endpoint,
    default_endpoint_template,
    use_mtls,
    expected,
):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            universe.get_api_endpoint(
                api_override,
                universe_domain,
                default_universe,
                default_mtls_endpoint,
                default_endpoint_template,
                use_mtls,
            )
    else:
        assert (
            universe.get_api_endpoint(
                api_override,
                universe_domain,
                default_universe,
                default_mtls_endpoint,
                default_endpoint_template,
                use_mtls,
            )
            == expected
        )


def test_should_use_client_cert_with_should_use_client_cert():
    mock_mtls = mock.Mock()
    mock_mtls.should_use_client_cert.return_value = True
    with mock.patch(f"{universe.__name__}.mtls", mock_mtls):
        assert universe.should_use_client_cert() is True

    mock_mtls.should_use_client_cert.return_value = False
    with mock.patch(f"{universe.__name__}.mtls", mock_mtls):
        assert universe.should_use_client_cert() is False


def test_should_use_client_cert_fallback_env():
    mock_mtls = mock.Mock(spec=[])
    with mock.patch(f"{universe.__name__}.mtls", mock_mtls):
        with mock.patch.dict(os.environ, {"CLOUDSDK_CONTEXT_AWARE_USE_CLIENT_CERTIFICATE": "true"}, clear=True):
            assert universe.should_use_client_cert() is True

        with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}, clear=True):
            assert universe.should_use_client_cert() is False

        with mock.patch.dict(os.environ, {}, clear=True):
            assert universe.should_use_client_cert() is None
