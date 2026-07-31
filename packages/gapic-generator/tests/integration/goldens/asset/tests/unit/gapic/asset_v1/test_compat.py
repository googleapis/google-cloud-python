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

from google.cloud.asset_v1 import _compat as universe

from google.auth.exceptions import MutualTLSChannelError
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


def test_use_client_cert_effective_true():
    mock_mtls = mock.Mock(spec=["should_use_client_cert"])
    mock_mtls.should_use_client_cert.return_value = True
    with mock.patch("google.api_core.gapic_v1.config.mtls", mock_mtls):
        assert config.use_client_cert_effective() is True


def test_use_client_cert_effective_false():
    mock_mtls = mock.Mock(spec=["should_use_client_cert"])
    mock_mtls.should_use_client_cert.return_value = False
    with mock.patch("google.api_core.gapic_v1.config.mtls", mock_mtls):
        assert config.use_client_cert_effective() is False


def test_use_client_cert_effective_fallback_env_true():
    mock_mtls = mock.Mock(spec=[])
    with mock.patch("google.api_core.gapic_v1.config.mtls", mock_mtls):
        with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
            assert config.use_client_cert_effective() is True


def test_use_client_cert_effective_fallback_env_false():
    mock_mtls = mock.Mock(spec=[])
    with mock.patch("google.api_core.gapic_v1.config.mtls", mock_mtls):
        with mock.patch.dict(
            os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}
        ):
            assert config.use_client_cert_effective() is False


def test_use_client_cert_effective_fallback_env_invalid():
    mock_mtls = mock.Mock(spec=[])
    with mock.patch("google.api_core.gapic_v1.config.mtls", mock_mtls):
        with mock.patch.dict(
            os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "invalid"}
        ):
            with pytest.raises(
                ValueError,
                match="Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`",
            ):
                config.use_client_cert_effective()


def test_get_client_cert_source_provided():
    source = mock.Mock()
    assert config.get_client_cert_source(source, True) == source


def test_get_client_cert_source_default():
    mock_mtls = mock.Mock(
        spec=["has_default_client_cert_source", "default_client_cert_source"]
    )
    mock_mtls.has_default_client_cert_source.return_value = True
    mock_source = mock.Mock()
    mock_mtls.default_client_cert_source.return_value = mock_source
    with mock.patch("google.api_core.gapic_v1.config.mtls", mock_mtls):
        assert config.get_client_cert_source(None, True) == mock_source


def test_get_client_cert_source_none():
    mock_mtls = mock.Mock(
        spec=["has_default_client_cert_source", "default_client_cert_source"]
    )
    mock_mtls.has_default_client_cert_source.return_value = False
    with mock.patch("google.api_core.gapic_v1.config.mtls", mock_mtls):
        with pytest.raises(
            ValueError,
            match="Client certificate is required for mTLS, but no client certificate source was provided or found.",
        ):
            config.get_client_cert_source(None, True)


def test_get_client_cert_source_use_cert_flag_false():
    assert config.get_client_cert_source(None, False) is None
    source = mock.Mock()
    assert config.get_client_cert_source(source, False) is None


def test_read_environment_variables():
    with mock.patch(
        "google.api_core.gapic_v1.config.use_client_cert_effective", return_value=True
    ):
        with mock.patch.dict(
            os.environ,
            {
                "GOOGLE_API_USE_MTLS_ENDPOINT": "always",
                "GOOGLE_CLOUD_UNIVERSE_DOMAIN": "my-universe.com",
            },
        ):
            use_cert, use_mtls, universe = config.read_environment_variables()
            assert use_cert is True
            assert use_mtls == "always"
            assert universe == "my-universe.com"


def test_read_environment_variables_invalid_mtls():
    with mock.patch(
        "google.api_core.gapic_v1.config.use_client_cert_effective", return_value=True
    ):
        with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "invalid"}):
            with pytest.raises(MutualTLSChannelError):
                config.read_environment_variables()
