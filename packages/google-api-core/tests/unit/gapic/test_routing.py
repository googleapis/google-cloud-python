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

from google.api_core.gapic_v1.routing import (
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

    # Test endpoints that shouldn't be converted
    assert (
        get_default_mtls_endpoint("foo.mtls.googleapis.com")
        == "foo.mtls.googleapis.com"
    )
    assert get_default_mtls_endpoint("foo.com") == "foo.com"

    # Test empty/None endpoints
    assert get_default_mtls_endpoint("") == ""
    assert get_default_mtls_endpoint(None) is None


def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = MockClient._DEFAULT_UNIVERSE
    default_endpoint = MockClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = MockClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        get_api_endpoint(
            api_override,
            mock_client_cert_source,
            default_universe,
            "always",
            MockClient._DEFAULT_UNIVERSE,
            MockClient.DEFAULT_MTLS_ENDPOINT,
            MockClient._DEFAULT_ENDPOINT_TEMPLATE,
        )
        == api_override
    )
    assert (
        get_api_endpoint(
            None,
            mock_client_cert_source,
            default_universe,
            "auto",
            MockClient._DEFAULT_UNIVERSE,
            MockClient.DEFAULT_MTLS_ENDPOINT,
            MockClient._DEFAULT_ENDPOINT_TEMPLATE,
        )
        == MockClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        get_api_endpoint(
            None,
            None,
            default_universe,
            "auto",
            MockClient._DEFAULT_UNIVERSE,
            MockClient.DEFAULT_MTLS_ENDPOINT,
            MockClient._DEFAULT_ENDPOINT_TEMPLATE,
        )
        == default_endpoint
    )
    assert (
        get_api_endpoint(
            None,
            None,
            default_universe,
            "always",
            MockClient._DEFAULT_UNIVERSE,
            MockClient.DEFAULT_MTLS_ENDPOINT,
            MockClient._DEFAULT_ENDPOINT_TEMPLATE,
        )
        == MockClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        get_api_endpoint(
            None,
            mock_client_cert_source,
            default_universe,
            "always",
            MockClient._DEFAULT_UNIVERSE,
            MockClient.DEFAULT_MTLS_ENDPOINT,
            MockClient._DEFAULT_ENDPOINT_TEMPLATE,
        )
        == MockClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        get_api_endpoint(
            None,
            None,
            mock_universe,
            "never",
            MockClient._DEFAULT_UNIVERSE,
            MockClient.DEFAULT_MTLS_ENDPOINT,
            MockClient._DEFAULT_ENDPOINT_TEMPLATE,
        )
        == mock_endpoint
    )
    assert (
        get_api_endpoint(
            None,
            None,
            default_universe,
            "never",
            MockClient._DEFAULT_UNIVERSE,
            MockClient.DEFAULT_MTLS_ENDPOINT,
            MockClient._DEFAULT_ENDPOINT_TEMPLATE,
        )
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        get_api_endpoint(
            None,
            mock_client_cert_source,
            mock_universe,
            "auto",
            MockClient._DEFAULT_UNIVERSE,
            MockClient.DEFAULT_MTLS_ENDPOINT,
            MockClient._DEFAULT_ENDPOINT_TEMPLATE,
        )
    assert (
        str(excinfo.value)
        == "mTLS is not supported in any universe other than googleapis.com."
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
