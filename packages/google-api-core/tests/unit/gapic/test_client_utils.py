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

from google.api_core.gapic_v1.client_utils import (
    get_api_endpoint,
    get_default_mtls_endpoint,
    get_universe_domain,
    resolve_credentials_and_host,
    resolve_grpc_channel,
    resolve_rest_session,
)


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
            get_api_endpoint(
                api_override,
                universe_domain,
                default_universe,
                default_mtls_endpoint,
                default_endpoint_template,
                use_mtls,
            )
    else:
        assert (
            get_api_endpoint(
                api_override,
                universe_domain,
                default_universe,
                default_mtls_endpoint,
                default_endpoint_template,
                use_mtls,
            )
            == expected
        )


def test_get_universe_domain():
    # When universe_domain is provided
    assert get_universe_domain("foo.com", "default.com") == "foo.com"
    assert get_universe_domain("  foo.com  ", "default.com") == "foo.com"

    # When universe_domain is None, falls back to default_universe
    assert get_universe_domain(None, "default.com") == "default.com"

    # ValueError raised when resolved value is empty string
    with pytest.raises(ValueError) as excinfo:
        get_universe_domain("", "default.com")
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."

    with pytest.raises(ValueError) as excinfo:
        get_universe_domain("   ", "default.com")
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


def test_resolve_credentials_and_host():
    mock_creds = mock.Mock()
    # Host with port formatting
    creds, host = resolve_credentials_and_host(
        host="foo.com",
        credentials=mock_creds,
        ignore_credentials=True,
    )
    assert creds is mock_creds
    assert host == "foo.com:443"

    # Host with existing port
    _, host_with_port = resolve_credentials_and_host(
        host="foo.com:80",
        credentials=mock_creds,
        ignore_credentials=True,
    )
    assert host_with_port == "foo.com:80"

    # Duplicate credential args check
    from google.api_core import exceptions as core_exceptions
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        resolve_credentials_and_host(
            host="foo.com",
            credentials=mock_creds,
            credentials_file="path/to/file",
        )


def test_resolve_grpc_channel():
    import grpc

    # Sync channel reuse
    mock_channel = mock.create_autospec(grpc.Channel)
    channel, ssl_creds, ignore_creds, host = resolve_grpc_channel(
        host="foo.com",
        channel=mock_channel,
    )
    assert channel is mock_channel
    assert ssl_creds is None
    assert ignore_creds is True
    assert host == "foo.com"


def test_resolve_rest_session():
    mock_creds = mock.Mock()
    with mock.patch("google.auth.transport.requests.AuthorizedSession") as mock_session_class:
        mock_session = mock_session_class.return_value
        session = resolve_rest_session(
            credentials=mock_creds,
            default_host="foo.com",
            client_cert_source_for_mtls=lambda: (b"cert", b"key"),
        )
        assert session is mock_session
        mock_session.configure_mtls_channel.assert_called_once()
