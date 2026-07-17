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
from google.auth.exceptions import MutualTLSChannelError

from google.api_core.gapic_v1.client_utils import (
    get_api_endpoint,
    get_default_mtls_endpoint,
    get_universe_domain,
)


class MockClient:
    _DEFAULT_UNIVERSE = "googleapis.com"
    DEFAULT_MTLS_ENDPOINT = "foo.mtls.googleapis.com"
    _DEFAULT_ENDPOINT_TEMPLATE = "foo.{UNIVERSE_DOMAIN}"


def test_get_default_mtls_endpoint():
    # Test valid API endpoints
    assert get_default_mtls_endpoint("foo.googleapis.com") == "foo.mtls.googleapis.com"
    assert (
        get_default_mtls_endpoint("foo.sandbox.googleapis.com")
        == "foo.mtls.sandbox.googleapis.com"
    )
    # Test case-insensitivity
    assert get_default_mtls_endpoint("foo.GoogleAPIs.com") == "foo.mtls.googleapis.com"
    assert (
        get_default_mtls_endpoint("foo.Sandbox.GoogleAPIs.com")
        == "foo.mtls.sandbox.googleapis.com"
    )

    # Test valid API endpoints with schemes
    assert (
        get_default_mtls_endpoint("https://foo.googleapis.com")
        == "https://foo.mtls.googleapis.com"
    )
    assert (
        get_default_mtls_endpoint("http://foo.googleapis.com:8080/v1")
        == "http://foo.mtls.googleapis.com:8080/v1"
    )

    # Test valid API endpoints with ports
    assert (
        get_default_mtls_endpoint("foo.googleapis.com:443")
        == "foo.mtls.googleapis.com:443"
    )
    assert (
        get_default_mtls_endpoint("foo.sandbox.googleapis.com:443")
        == "foo.mtls.sandbox.googleapis.com:443"
    )
    # Test case-insensitivity with ports
    assert (
        get_default_mtls_endpoint("foo.GoogleAPIs.com:443")
        == "foo.mtls.googleapis.com:443"
    )
    assert (
        get_default_mtls_endpoint("foo.Sandbox.GoogleAPIs.com:443")
        == "foo.mtls.sandbox.googleapis.com:443"
    )

    # Test endpoints that shouldn't be converted
    assert (
        get_default_mtls_endpoint("foo.mtls.googleapis.com")
        == "foo.mtls.googleapis.com"
    )
    assert get_default_mtls_endpoint("foo.com") == "foo.com"
    assert get_default_mtls_endpoint("foo.com:8080") == "foo.com:8080"

    # Test empty/None endpoints
    assert get_default_mtls_endpoint("") == ""
    assert get_default_mtls_endpoint(None) is None


@pytest.mark.parametrize(
    "api_override,client_cert_source,universe_domain,use_mtls_endpoint,default_universe,default_mtls_endpoint,default_endpoint_template,expected",
    [
        (
            "foo.com",
            mock.Mock(),
            "googleapis.com",
            "always",
            "googleapis.com",
            "foo.mtls.googleapis.com",
            "foo.{UNIVERSE_DOMAIN}",
            "foo.com",
        ),
        (
            None,
            mock.Mock(),
            "googleapis.com",
            "auto",
            "googleapis.com",
            "foo.mtls.googleapis.com",
            "foo.{UNIVERSE_DOMAIN}",
            "foo.mtls.googleapis.com",
        ),
        (
            None,
            None,
            "googleapis.com",
            "auto",
            "googleapis.com",
            "foo.mtls.googleapis.com",
            "foo.{UNIVERSE_DOMAIN}",
            "foo.googleapis.com",
        ),
        (
            None,
            None,
            "googleapis.com",
            "always",
            "googleapis.com",
            "foo.mtls.googleapis.com",
            "foo.{UNIVERSE_DOMAIN}",
            "foo.mtls.googleapis.com",
        ),
        (
            None,
            mock.Mock(),
            "googleapis.com",
            "always",
            "googleapis.com",
            "foo.mtls.googleapis.com",
            "foo.{UNIVERSE_DOMAIN}",
            "foo.mtls.googleapis.com",
        ),
        (
            None,
            None,
            "bar.com",
            "never",
            "googleapis.com",
            "foo.mtls.googleapis.com",
            "foo.{UNIVERSE_DOMAIN}",
            "foo.bar.com",
        ),
        (
            None,
            None,
            "googleapis.com",
            "never",
            "googleapis.com",
            "foo.mtls.googleapis.com",
            "foo.{UNIVERSE_DOMAIN}",
            "foo.googleapis.com",
        ),
        (
            None,
            mock.Mock(),
            "bar.com",
            "auto",
            "googleapis.com",
            "foo.mtls.googleapis.com",
            "foo.{UNIVERSE_DOMAIN}",
            MutualTLSChannelError,
        ),
        (
            None,
            mock.Mock(),
            "googleapis.com",
            "always",
            "googleapis.com",
            None,
            "foo.{UNIVERSE_DOMAIN}",
            ValueError,
        ),
    ],
)
def test_get_api_endpoint(
    api_override,
    client_cert_source,
    universe_domain,
    use_mtls_endpoint,
    default_universe,
    default_mtls_endpoint,
    default_endpoint_template,
    expected,
):
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": use_mtls_endpoint}):
        if isinstance(expected, type) and issubclass(expected, Exception):
            with pytest.raises(expected):
                get_api_endpoint(
                    api_override,
                    client_cert_source,
                    universe_domain,
                    default_universe,
                    default_mtls_endpoint,
                    default_endpoint_template,
                )
        else:
            assert (
                get_api_endpoint(
                    api_override,
                    client_cert_source,
                    universe_domain,
                    default_universe,
                    default_mtls_endpoint,
                    default_endpoint_template,
                )
                == expected
            )


def test__get_universe_domain():
    client_universe_domain = "foo.com"
    universe_domain_env = "bar.com"

    assert (
        get_universe_domain(
            client_universe_domain, universe_domain_env, MockClient._DEFAULT_UNIVERSE
        )
        == client_universe_domain
    )
    assert (
        get_universe_domain(None, universe_domain_env, MockClient._DEFAULT_UNIVERSE)
        == universe_domain_env
    )
    assert (
        get_universe_domain(None, None, MockClient._DEFAULT_UNIVERSE)
        == MockClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        get_universe_domain("", None, MockClient._DEFAULT_UNIVERSE)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."
