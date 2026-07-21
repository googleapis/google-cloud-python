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
from google.auth.transport import mtls
from google.api_core.gapic_v1.client_utils import (
    get_api_endpoint,
    get_default_mtls_endpoint,
    get_universe_domain,
    get_client_cert_source,
    use_client_cert_effective,
    read_environment_variables,
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

    with pytest.raises(ValueError) as excinfo:
        get_api_endpoint(
            None,
            mock_client_cert_source,
            default_universe,
            "always",
            MockClient._DEFAULT_UNIVERSE,
            None,
            MockClient._DEFAULT_ENDPOINT_TEMPLATE,
        )
    assert str(excinfo.value) == "mTLS endpoint is not available."


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


@pytest.mark.parametrize(
    "has_method, method_val, env_val, expected",
    [
        # should_use_client_cert is available cases
        (True, True, None, "true"),
        (True, False, None, "false"),
        (True, False, "unsupported", "false"),
        # should_use_client_cert is unavailable cases
        (False, None, "true", "true"),
        (False, None, "false", "false"),
        (False, None, "True", "true"),
        (False, None, "False", "false"),
        (False, None, "TRUE", "true"),
        (False, None, "FALSE", "false"),
        (False, None, None, "false"),
        (False, None, "unsupported", "value_error"),
    ],
    ids=[
        "google_auth_true",
        "google_auth_false",
        "google_auth_false_env_unsupported",
        "fallback_env_true_lowercase",
        "fallback_env_false_lowercase",
        "fallback_env_true_titlecase",
        "fallback_env_false_titlecase",
        "fallback_env_true_uppercase",
        "fallback_env_false_uppercase",
        "fallback_env_unset",
        "fallback_env_unsupported",
    ],
)
def test_use_client_cert_effective(has_method, method_val, env_val, expected):
    # Mock hasattr to control whether should_use_client_cert exists
    original_hasattr = hasattr

    def custom_hasattr(obj, name):
        if obj is mtls and name == "should_use_client_cert":
            return has_method
        return original_hasattr(obj, name)

    with mock.patch("google.api_core.gapic_v1.client_utils.hasattr", custom_hasattr):
        with mock.patch(
            "google.auth.transport.mtls.should_use_client_cert",
            create=True,
            return_value=method_val,
        ):
            env = {}
            if env_val is not None:
                env["GOOGLE_API_USE_CLIENT_CERTIFICATE"] = env_val
            with mock.patch.dict(os.environ, env, clear=True):
                if expected == "value_error":
                    with pytest.raises(
                        ValueError, match="must be either `true` or `false`"
                    ):
                        use_client_cert_effective()
                else:
                    assert use_client_cert_effective() is (expected == "true")


@pytest.mark.parametrize(
    "provided, use_cert, has_default_avail, default_val, expected",
    [
        (None, False, True, b"default", None),
        (b"provided", False, True, b"default", None),
        (b"provided", True, True, b"default", b"provided"),
        (None, True, True, b"default", b"default"),
        (None, True, False, b"default", None),
    ],
    ids=[
        "use_cert_false_no_provided",
        "use_cert_false_with_provided",
        "use_cert_true_with_provided",
        "use_cert_true_no_provided_default_avail",
        "use_cert_true_no_provided_default_unavail",
    ],
)
def test_get_client_cert_source(
    provided, use_cert, has_default_avail, default_val, expected
):
    original_hasattr = hasattr

    def custom_hasattr(obj, name):
        if obj is mtls and name == "has_default_client_cert_source":
            return has_default_avail
        return original_hasattr(obj, name)

    with mock.patch("google.api_core.gapic_v1.client_utils.hasattr", custom_hasattr):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            create=True,
            return_value=has_default_avail,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                create=True,
                return_value=default_val,
            ):
                if expected == "value_error":
                    with pytest.raises(
                        ValueError, match="Client certificate is required for mTLS"
                    ):
                        get_client_cert_source(provided, use_cert)
                else:
                    assert get_client_cert_source(provided, use_cert) == expected


@pytest.mark.parametrize(
    "env, mock_cert_val, expected",
    [
        ({}, False, (False, "auto", None)),
        ({}, True, (True, "auto", None)),
        ({"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}, False, (False, "never", None)),
        ({"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}, False, (False, "always", None)),
        ({"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}, False, (False, "auto", None)),
        ({"GOOGLE_API_USE_MTLS_ENDPOINT": "invalid"}, False, "mutual_tls_error"),
        (
            {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"},
            False,
            (False, "auto", "foo.com"),
        ),
    ],
    ids=[
        "default_env",
        "client_cert_true",
        "mtls_never",
        "mtls_always",
        "mtls_auto",
        "mtls_invalid",
        "universe_domain",
    ],
)
def test_read_environment_variables(env, mock_cert_val, expected):
    with mock.patch(
        "google.api_core.gapic_v1.client_utils.use_client_cert_effective",
        return_value=mock_cert_val,
    ):
        with mock.patch.dict(os.environ, env, clear=True):
            if expected == "mutual_tls_error":
                with pytest.raises(
                    MutualTLSChannelError, match="must be `never`, `auto` or `always`"
                ):
                    read_environment_variables()
            else:
                assert read_environment_variables() == expected
