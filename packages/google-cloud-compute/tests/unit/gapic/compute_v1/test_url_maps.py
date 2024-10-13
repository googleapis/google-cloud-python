# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
import os

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

from collections.abc import AsyncIterable, Iterable
import json
import math

from google.api_core import api_core_version
from google.protobuf import json_format
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

try:
    from google.auth.aio import credentials as ga_credentials_async

    HAS_GOOGLE_AUTH_AIO = True
except ImportError:  # pragma: NO COVER
    HAS_GOOGLE_AUTH_AIO = False

from google.api_core import (
    future,
    gapic_v1,
    grpc_helpers,
    grpc_helpers_async,
    path_template,
)
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import extended_operation  # type: ignore
from google.api_core import retry as retries
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.oauth2 import service_account

from google.cloud.compute_v1.services.url_maps import UrlMapsClient, pagers, transports
from google.cloud.compute_v1.types import compute


async def mock_async_gen(data, chunk_size=1):
    for i in range(0, len(data)):  # pragma: NO COVER
        chunk = data[i : i + chunk_size]
        yield chunk.encode("utf-8")


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# TODO: use async auth anon credentials by default once the minimum version of google-auth is upgraded.
# See related issue: https://github.com/googleapis/gapic-generator-python/issues/2107.
def async_anonymous_credentials():
    if HAS_GOOGLE_AUTH_AIO:
        return ga_credentials_async.AnonymousCredentials()
    return ga_credentials.AnonymousCredentials()


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


# If default endpoint template is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint template so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint_template(client):
    return (
        "test.{UNIVERSE_DOMAIN}"
        if ("localhost" in client._DEFAULT_ENDPOINT_TEMPLATE)
        else client._DEFAULT_ENDPOINT_TEMPLATE
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert UrlMapsClient._get_default_mtls_endpoint(None) is None
    assert UrlMapsClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert (
        UrlMapsClient._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    )
    assert (
        UrlMapsClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        UrlMapsClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert UrlMapsClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


def test__read_environment_variables():
    assert UrlMapsClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert UrlMapsClient._read_environment_variables() == (True, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert UrlMapsClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            UrlMapsClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert UrlMapsClient._read_environment_variables() == (False, "never", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert UrlMapsClient._read_environment_variables() == (False, "always", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert UrlMapsClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            UrlMapsClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert UrlMapsClient._read_environment_variables() == (False, "auto", "foo.com")


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert UrlMapsClient._get_client_cert_source(None, False) is None
    assert (
        UrlMapsClient._get_client_cert_source(mock_provided_cert_source, False) is None
    )
    assert (
        UrlMapsClient._get_client_cert_source(mock_provided_cert_source, True)
        == mock_provided_cert_source
    )

    with mock.patch(
        "google.auth.transport.mtls.has_default_client_cert_source", return_value=True
    ):
        with mock.patch(
            "google.auth.transport.mtls.default_client_cert_source",
            return_value=mock_default_cert_source,
        ):
            assert (
                UrlMapsClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                UrlMapsClient._get_client_cert_source(mock_provided_cert_source, "true")
                is mock_provided_cert_source
            )


@mock.patch.object(
    UrlMapsClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(UrlMapsClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = UrlMapsClient._DEFAULT_UNIVERSE
    default_endpoint = UrlMapsClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = UrlMapsClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        UrlMapsClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        UrlMapsClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == UrlMapsClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        UrlMapsClient._get_api_endpoint(None, None, default_universe, "auto")
        == default_endpoint
    )
    assert (
        UrlMapsClient._get_api_endpoint(None, None, default_universe, "always")
        == UrlMapsClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        UrlMapsClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == UrlMapsClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        UrlMapsClient._get_api_endpoint(None, None, mock_universe, "never")
        == mock_endpoint
    )
    assert (
        UrlMapsClient._get_api_endpoint(None, None, default_universe, "never")
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        UrlMapsClient._get_api_endpoint(
            None, mock_client_cert_source, mock_universe, "auto"
        )
    assert (
        str(excinfo.value)
        == "mTLS is not supported in any universe other than googleapis.com."
    )


def test__get_universe_domain():
    client_universe_domain = "foo.com"
    universe_domain_env = "bar.com"

    assert (
        UrlMapsClient._get_universe_domain(client_universe_domain, universe_domain_env)
        == client_universe_domain
    )
    assert (
        UrlMapsClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        UrlMapsClient._get_universe_domain(None, None)
        == UrlMapsClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        UrlMapsClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (UrlMapsClient, transports.UrlMapsRestTransport, "rest"),
    ],
)
def test__validate_universe_domain(client_class, transport_class, transport_name):
    client = client_class(
        transport=transport_class(credentials=ga_credentials.AnonymousCredentials())
    )
    assert client._validate_universe_domain() == True

    # Test the case when universe is already validated.
    assert client._validate_universe_domain() == True

    if transport_name == "grpc":
        # Test the case where credentials are provided by the
        # `local_channel_credentials`. The default universes in both match.
        channel = grpc.secure_channel(
            "http://localhost/", grpc.local_channel_credentials()
        )
        client = client_class(transport=transport_class(channel=channel))
        assert client._validate_universe_domain() == True

        # Test the case where credentials do not exist: e.g. a transport is provided
        # with no credentials. Validation should still succeed because there is no
        # mismatch with non-existent credentials.
        channel = grpc.secure_channel(
            "http://localhost/", grpc.local_channel_credentials()
        )
        transport = transport_class(channel=channel)
        transport._credentials = None
        client = client_class(transport=transport)
        assert client._validate_universe_domain() == True

    # TODO: This is needed to cater for older versions of google-auth
    # Make this test unconditional once the minimum supported version of
    # google-auth becomes 2.23.0 or higher.
    google_auth_major, google_auth_minor = [
        int(part) for part in google.auth.__version__.split(".")[0:2]
    ]
    if google_auth_major > 2 or (google_auth_major == 2 and google_auth_minor >= 23):
        credentials = ga_credentials.AnonymousCredentials()
        credentials._universe_domain = "foo.com"
        # Test the case when there is a universe mismatch from the credentials.
        client = client_class(transport=transport_class(credentials=credentials))
        with pytest.raises(ValueError) as excinfo:
            client._validate_universe_domain()
        assert (
            str(excinfo.value)
            == "The configured universe domain (googleapis.com) does not match the universe domain found in the credentials (foo.com). If you haven't configured the universe domain explicitly, `googleapis.com` is the default."
        )

        # Test the case when there is a universe mismatch from the client.
        #
        # TODO: Make this test unconditional once the minimum supported version of
        # google-api-core becomes 2.15.0 or higher.
        api_core_major, api_core_minor = [
            int(part) for part in api_core_version.__version__.split(".")[0:2]
        ]
        if api_core_major > 2 or (api_core_major == 2 and api_core_minor >= 15):
            client = client_class(
                client_options={"universe_domain": "bar.com"},
                transport=transport_class(
                    credentials=ga_credentials.AnonymousCredentials(),
                ),
            )
            with pytest.raises(ValueError) as excinfo:
                client._validate_universe_domain()
            assert (
                str(excinfo.value)
                == "The configured universe domain (bar.com) does not match the universe domain found in the credentials (googleapis.com). If you haven't configured the universe domain explicitly, `googleapis.com` is the default."
            )

    # Test that ValueError is raised if universe_domain is provided via client options and credentials is None
    with pytest.raises(ValueError):
        client._compare_universes("foo.bar", None)


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (UrlMapsClient, "rest"),
    ],
)
def test_url_maps_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "compute.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://compute.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.UrlMapsRestTransport, "rest"),
    ],
)
def test_url_maps_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (UrlMapsClient, "rest"),
    ],
)
def test_url_maps_client_from_service_account_file(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "compute.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://compute.googleapis.com"
        )


def test_url_maps_client_get_transport_class():
    transport = UrlMapsClient.get_transport_class()
    available_transports = [
        transports.UrlMapsRestTransport,
    ]
    assert transport in available_transports

    transport = UrlMapsClient.get_transport_class("rest")
    assert transport == transports.UrlMapsRestTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (UrlMapsClient, transports.UrlMapsRestTransport, "rest"),
    ],
)
@mock.patch.object(
    UrlMapsClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(UrlMapsClient),
)
def test_url_maps_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(UrlMapsClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(UrlMapsClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (UrlMapsClient, transports.UrlMapsRestTransport, "rest", "true"),
        (UrlMapsClient, transports.UrlMapsRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    UrlMapsClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(UrlMapsClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_url_maps_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                )
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                            UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                        )
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                        UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                    ),
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize("client_class", [UrlMapsClient])
@mock.patch.object(
    UrlMapsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(UrlMapsClient)
)
def test_url_maps_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
        )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
        )


@pytest.mark.parametrize("client_class", [UrlMapsClient])
@mock.patch.object(
    UrlMapsClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(UrlMapsClient),
)
def test_url_maps_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = UrlMapsClient._DEFAULT_UNIVERSE
    default_endpoint = UrlMapsClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = UrlMapsClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    # If ClientOptions.api_endpoint is set and GOOGLE_API_USE_CLIENT_CERTIFICATE="true",
    # use ClientOptions.api_endpoint as the api endpoint regardless.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
        ):
            options = client_options.ClientOptions(
                client_cert_source=mock_client_cert_source, api_endpoint=api_override
            )
            client = client_class(
                client_options=options,
                credentials=ga_credentials.AnonymousCredentials(),
            )
            assert client.api_endpoint == api_override

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == default_endpoint

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="always",
    # use the DEFAULT_MTLS_ENDPOINT as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT

    # If ClientOptions.api_endpoint is not set, GOOGLE_API_USE_MTLS_ENDPOINT="auto" (default),
    # GOOGLE_API_USE_CLIENT_CERTIFICATE="false" (default), default cert source doesn't exist,
    # and ClientOptions.universe_domain="bar.com",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with universe domain as the api endpoint.
    options = client_options.ClientOptions()
    universe_exists = hasattr(options, "universe_domain")
    if universe_exists:
        options = client_options.ClientOptions(universe_domain=mock_universe)
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    else:
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    assert client.api_endpoint == (
        mock_endpoint if universe_exists else default_endpoint
    )
    assert client.universe_domain == (
        mock_universe if universe_exists else default_universe
    )

    # If ClientOptions does not have a universe domain attribute and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    options = client_options.ClientOptions()
    if hasattr(options, "universe_domain"):
        delattr(options, "universe_domain")
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
        assert client.api_endpoint == default_endpoint


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (UrlMapsClient, transports.UrlMapsRestTransport, "rest"),
    ],
)
def test_url_maps_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (UrlMapsClient, transports.UrlMapsRestTransport, "rest", None),
    ],
)
def test_url_maps_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_aggregated_list_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = UrlMapsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.aggregated_list in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.aggregated_list] = mock_rpc

        request = {}
        client.aggregated_list(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.aggregated_list(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_aggregated_list_rest_required_fields(
    request_type=compute.AggregatedListUrlMapsRequest,
):
    transport_class = transports.UrlMapsRestTransport

    request_init = {}
    request_init["project"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).aggregated_list._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).aggregated_list._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "include_all_scopes",
            "max_results",
            "order_by",
            "page_token",
            "return_partial_success",
            "service_project_number",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"

    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.UrlMapsAggregatedList()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.UrlMapsAggregatedList.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.aggregated_list(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_aggregated_list_rest_unset_required_fields():
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.aggregated_list._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "includeAllScopes",
                "maxResults",
                "orderBy",
                "pageToken",
                "returnPartialSuccess",
                "serviceProjectNumber",
            )
        )
        & set(("project",))
    )


def test_aggregated_list_rest_flattened():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.UrlMapsAggregatedList()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.UrlMapsAggregatedList.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.aggregated_list(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/aggregated/urlMaps"
            % client.transport._host,
            args[1],
        )


def test_aggregated_list_rest_flattened_error(transport: str = "rest"):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.aggregated_list(
            compute.AggregatedListUrlMapsRequest(),
            project="project_value",
        )


def test_aggregated_list_rest_pager(transport: str = "rest"):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            compute.UrlMapsAggregatedList(
                items={
                    "a": compute.UrlMapsScopedList(),
                    "b": compute.UrlMapsScopedList(),
                    "c": compute.UrlMapsScopedList(),
                },
                next_page_token="abc",
            ),
            compute.UrlMapsAggregatedList(
                items={},
                next_page_token="def",
            ),
            compute.UrlMapsAggregatedList(
                items={
                    "g": compute.UrlMapsScopedList(),
                },
                next_page_token="ghi",
            ),
            compute.UrlMapsAggregatedList(
                items={
                    "h": compute.UrlMapsScopedList(),
                    "i": compute.UrlMapsScopedList(),
                },
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(compute.UrlMapsAggregatedList.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"project": "sample1"}

        pager = client.aggregated_list(request=sample_request)

        assert isinstance(pager.get("a"), compute.UrlMapsScopedList)
        assert pager.get("h") is None

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tuple) for i in results)
        for result in results:
            assert isinstance(result, tuple)
            assert tuple(type(t) for t in result) == (str, compute.UrlMapsScopedList)

        assert pager.get("a") is None
        assert isinstance(pager.get("h"), compute.UrlMapsScopedList)

        pages = list(client.aggregated_list(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_delete_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = UrlMapsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.delete in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.delete] = mock_rpc

        request = {}
        client.delete(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.delete(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_rest_required_fields(request_type=compute.DeleteUrlMapRequest):
    transport_class = transports.UrlMapsRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["url_map"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["urlMap"] = "url_map_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "urlMap" in jsonified_request
    assert jsonified_request["urlMap"] == "url_map_value"

    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_rest_unset_required_fields():
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "project",
                "urlMap",
            )
        )
    )


def test_delete_rest_flattened():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "url_map": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            url_map="url_map_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/global/urlMaps/{url_map}"
            % client.transport._host,
            args[1],
        )


def test_delete_rest_flattened_error(transport: str = "rest"):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete(
            compute.DeleteUrlMapRequest(),
            project="project_value",
            url_map="url_map_value",
        )


def test_delete_unary_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = UrlMapsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.delete in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.delete] = mock_rpc

        request = {}
        client.delete_unary(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.delete_unary(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_unary_rest_required_fields(request_type=compute.DeleteUrlMapRequest):
    transport_class = transports.UrlMapsRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["url_map"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["urlMap"] = "url_map_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "urlMap" in jsonified_request
    assert jsonified_request["urlMap"] == "url_map_value"

    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_unary_rest_unset_required_fields():
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "project",
                "urlMap",
            )
        )
    )


def test_delete_unary_rest_flattened():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "url_map": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            url_map="url_map_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/global/urlMaps/{url_map}"
            % client.transport._host,
            args[1],
        )


def test_delete_unary_rest_flattened_error(transport: str = "rest"):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_unary(
            compute.DeleteUrlMapRequest(),
            project="project_value",
            url_map="url_map_value",
        )


def test_get_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = UrlMapsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get] = mock_rpc

        request = {}
        client.get(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_rest_required_fields(request_type=compute.GetUrlMapRequest):
    transport_class = transports.UrlMapsRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["url_map"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["urlMap"] = "url_map_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "urlMap" in jsonified_request
    assert jsonified_request["urlMap"] == "url_map_value"

    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.UrlMap()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.UrlMap.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_rest_unset_required_fields():
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "project",
                "urlMap",
            )
        )
    )


def test_get_rest_flattened():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.UrlMap()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "url_map": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            url_map="url_map_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.UrlMap.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/global/urlMaps/{url_map}"
            % client.transport._host,
            args[1],
        )


def test_get_rest_flattened_error(transport: str = "rest"):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get(
            compute.GetUrlMapRequest(),
            project="project_value",
            url_map="url_map_value",
        )


def test_insert_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = UrlMapsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.insert in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.insert] = mock_rpc

        request = {}
        client.insert(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.insert(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_insert_rest_required_fields(request_type=compute.InsertUrlMapRequest):
    transport_class = transports.UrlMapsRestTransport

    request_init = {}
    request_init["project"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).insert._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).insert._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"

    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.insert(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_insert_rest_unset_required_fields():
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.insert._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "project",
                "urlMapResource",
            )
        )
    )


def test_insert_rest_flattened():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            url_map_resource=compute.UrlMap(
                creation_timestamp="creation_timestamp_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.insert(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/global/urlMaps" % client.transport._host,
            args[1],
        )


def test_insert_rest_flattened_error(transport: str = "rest"):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.insert(
            compute.InsertUrlMapRequest(),
            project="project_value",
            url_map_resource=compute.UrlMap(
                creation_timestamp="creation_timestamp_value"
            ),
        )


def test_insert_unary_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = UrlMapsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.insert in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.insert] = mock_rpc

        request = {}
        client.insert_unary(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.insert_unary(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_insert_unary_rest_required_fields(request_type=compute.InsertUrlMapRequest):
    transport_class = transports.UrlMapsRestTransport

    request_init = {}
    request_init["project"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).insert._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).insert._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"

    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.insert_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_insert_unary_rest_unset_required_fields():
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.insert._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "project",
                "urlMapResource",
            )
        )
    )


def test_insert_unary_rest_flattened():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            url_map_resource=compute.UrlMap(
                creation_timestamp="creation_timestamp_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.insert_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/global/urlMaps" % client.transport._host,
            args[1],
        )


def test_insert_unary_rest_flattened_error(transport: str = "rest"):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.insert_unary(
            compute.InsertUrlMapRequest(),
            project="project_value",
            url_map_resource=compute.UrlMap(
                creation_timestamp="creation_timestamp_value"
            ),
        )


def test_invalidate_cache_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = UrlMapsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.invalidate_cache in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.invalidate_cache
        ] = mock_rpc

        request = {}
        client.invalidate_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.invalidate_cache(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_invalidate_cache_rest_required_fields(
    request_type=compute.InvalidateCacheUrlMapRequest,
):
    transport_class = transports.UrlMapsRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["url_map"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).invalidate_cache._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["urlMap"] = "url_map_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).invalidate_cache._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "urlMap" in jsonified_request
    assert jsonified_request["urlMap"] == "url_map_value"

    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.invalidate_cache(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_invalidate_cache_rest_unset_required_fields():
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.invalidate_cache._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "cacheInvalidationRuleResource",
                "project",
                "urlMap",
            )
        )
    )


def test_invalidate_cache_rest_flattened():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "url_map": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            url_map="url_map_value",
            cache_invalidation_rule_resource=compute.CacheInvalidationRule(
                host="host_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.invalidate_cache(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/global/urlMaps/{url_map}/invalidateCache"
            % client.transport._host,
            args[1],
        )


def test_invalidate_cache_rest_flattened_error(transport: str = "rest"):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.invalidate_cache(
            compute.InvalidateCacheUrlMapRequest(),
            project="project_value",
            url_map="url_map_value",
            cache_invalidation_rule_resource=compute.CacheInvalidationRule(
                host="host_value"
            ),
        )


def test_invalidate_cache_unary_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = UrlMapsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.invalidate_cache in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.invalidate_cache
        ] = mock_rpc

        request = {}
        client.invalidate_cache_unary(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.invalidate_cache_unary(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_invalidate_cache_unary_rest_required_fields(
    request_type=compute.InvalidateCacheUrlMapRequest,
):
    transport_class = transports.UrlMapsRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["url_map"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).invalidate_cache._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["urlMap"] = "url_map_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).invalidate_cache._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "urlMap" in jsonified_request
    assert jsonified_request["urlMap"] == "url_map_value"

    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.invalidate_cache_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_invalidate_cache_unary_rest_unset_required_fields():
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.invalidate_cache._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "cacheInvalidationRuleResource",
                "project",
                "urlMap",
            )
        )
    )


def test_invalidate_cache_unary_rest_flattened():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "url_map": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            url_map="url_map_value",
            cache_invalidation_rule_resource=compute.CacheInvalidationRule(
                host="host_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.invalidate_cache_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/global/urlMaps/{url_map}/invalidateCache"
            % client.transport._host,
            args[1],
        )


def test_invalidate_cache_unary_rest_flattened_error(transport: str = "rest"):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.invalidate_cache_unary(
            compute.InvalidateCacheUrlMapRequest(),
            project="project_value",
            url_map="url_map_value",
            cache_invalidation_rule_resource=compute.CacheInvalidationRule(
                host="host_value"
            ),
        )


def test_list_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = UrlMapsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list] = mock_rpc

        request = {}
        client.list(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_rest_required_fields(request_type=compute.ListUrlMapsRequest):
    transport_class = transports.UrlMapsRestTransport

    request_init = {}
    request_init["project"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "max_results",
            "order_by",
            "page_token",
            "return_partial_success",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"

    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.UrlMapList()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.UrlMapList.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_rest_unset_required_fields():
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "maxResults",
                "orderBy",
                "pageToken",
                "returnPartialSuccess",
            )
        )
        & set(("project",))
    )


def test_list_rest_flattened():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.UrlMapList()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.UrlMapList.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/global/urlMaps" % client.transport._host,
            args[1],
        )


def test_list_rest_flattened_error(transport: str = "rest"):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list(
            compute.ListUrlMapsRequest(),
            project="project_value",
        )


def test_list_rest_pager(transport: str = "rest"):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            compute.UrlMapList(
                items=[
                    compute.UrlMap(),
                    compute.UrlMap(),
                    compute.UrlMap(),
                ],
                next_page_token="abc",
            ),
            compute.UrlMapList(
                items=[],
                next_page_token="def",
            ),
            compute.UrlMapList(
                items=[
                    compute.UrlMap(),
                ],
                next_page_token="ghi",
            ),
            compute.UrlMapList(
                items=[
                    compute.UrlMap(),
                    compute.UrlMap(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(compute.UrlMapList.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"project": "sample1"}

        pager = client.list(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, compute.UrlMap) for i in results)

        pages = list(client.list(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_patch_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = UrlMapsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.patch in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.patch] = mock_rpc

        request = {}
        client.patch(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.patch(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_patch_rest_required_fields(request_type=compute.PatchUrlMapRequest):
    transport_class = transports.UrlMapsRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["url_map"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).patch._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["urlMap"] = "url_map_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).patch._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "urlMap" in jsonified_request
    assert jsonified_request["urlMap"] == "url_map_value"

    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.patch(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_patch_rest_unset_required_fields():
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.patch._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "project",
                "urlMap",
                "urlMapResource",
            )
        )
    )


def test_patch_rest_flattened():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "url_map": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            url_map="url_map_value",
            url_map_resource=compute.UrlMap(
                creation_timestamp="creation_timestamp_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.patch(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/global/urlMaps/{url_map}"
            % client.transport._host,
            args[1],
        )


def test_patch_rest_flattened_error(transport: str = "rest"):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.patch(
            compute.PatchUrlMapRequest(),
            project="project_value",
            url_map="url_map_value",
            url_map_resource=compute.UrlMap(
                creation_timestamp="creation_timestamp_value"
            ),
        )


def test_patch_unary_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = UrlMapsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.patch in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.patch] = mock_rpc

        request = {}
        client.patch_unary(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.patch_unary(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_patch_unary_rest_required_fields(request_type=compute.PatchUrlMapRequest):
    transport_class = transports.UrlMapsRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["url_map"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).patch._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["urlMap"] = "url_map_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).patch._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "urlMap" in jsonified_request
    assert jsonified_request["urlMap"] == "url_map_value"

    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.patch_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_patch_unary_rest_unset_required_fields():
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.patch._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "project",
                "urlMap",
                "urlMapResource",
            )
        )
    )


def test_patch_unary_rest_flattened():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "url_map": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            url_map="url_map_value",
            url_map_resource=compute.UrlMap(
                creation_timestamp="creation_timestamp_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.patch_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/global/urlMaps/{url_map}"
            % client.transport._host,
            args[1],
        )


def test_patch_unary_rest_flattened_error(transport: str = "rest"):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.patch_unary(
            compute.PatchUrlMapRequest(),
            project="project_value",
            url_map="url_map_value",
            url_map_resource=compute.UrlMap(
                creation_timestamp="creation_timestamp_value"
            ),
        )


def test_update_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = UrlMapsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.update in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.update] = mock_rpc

        request = {}
        client.update(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.update(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_update_rest_required_fields(request_type=compute.UpdateUrlMapRequest):
    transport_class = transports.UrlMapsRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["url_map"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["urlMap"] = "url_map_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "urlMap" in jsonified_request
    assert jsonified_request["urlMap"] == "url_map_value"

    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "put",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_rest_unset_required_fields():
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "project",
                "urlMap",
                "urlMapResource",
            )
        )
    )


def test_update_rest_flattened():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "url_map": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            url_map="url_map_value",
            url_map_resource=compute.UrlMap(
                creation_timestamp="creation_timestamp_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/global/urlMaps/{url_map}"
            % client.transport._host,
            args[1],
        )


def test_update_rest_flattened_error(transport: str = "rest"):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update(
            compute.UpdateUrlMapRequest(),
            project="project_value",
            url_map="url_map_value",
            url_map_resource=compute.UrlMap(
                creation_timestamp="creation_timestamp_value"
            ),
        )


def test_update_unary_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = UrlMapsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.update in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.update] = mock_rpc

        request = {}
        client.update_unary(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.update_unary(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_update_unary_rest_required_fields(request_type=compute.UpdateUrlMapRequest):
    transport_class = transports.UrlMapsRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["url_map"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["urlMap"] = "url_map_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "urlMap" in jsonified_request
    assert jsonified_request["urlMap"] == "url_map_value"

    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "put",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_unary_rest_unset_required_fields():
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "project",
                "urlMap",
                "urlMapResource",
            )
        )
    )


def test_update_unary_rest_flattened():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "url_map": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            url_map="url_map_value",
            url_map_resource=compute.UrlMap(
                creation_timestamp="creation_timestamp_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/global/urlMaps/{url_map}"
            % client.transport._host,
            args[1],
        )


def test_update_unary_rest_flattened_error(transport: str = "rest"):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_unary(
            compute.UpdateUrlMapRequest(),
            project="project_value",
            url_map="url_map_value",
            url_map_resource=compute.UrlMap(
                creation_timestamp="creation_timestamp_value"
            ),
        )


def test_validate_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = UrlMapsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.validate in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.validate] = mock_rpc

        request = {}
        client.validate(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.validate(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_validate_rest_required_fields(request_type=compute.ValidateUrlMapRequest):
    transport_class = transports.UrlMapsRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["url_map"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).validate._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["urlMap"] = "url_map_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).validate._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "urlMap" in jsonified_request
    assert jsonified_request["urlMap"] == "url_map_value"

    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.UrlMapsValidateResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.UrlMapsValidateResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.validate(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_validate_rest_unset_required_fields():
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.validate._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "project",
                "urlMap",
                "urlMapsValidateRequestResource",
            )
        )
    )


def test_validate_rest_flattened():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.UrlMapsValidateResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "url_map": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            url_map="url_map_value",
            url_maps_validate_request_resource=compute.UrlMapsValidateRequest(
                load_balancing_schemes=["load_balancing_schemes_value"]
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.UrlMapsValidateResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.validate(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/global/urlMaps/{url_map}/validate"
            % client.transport._host,
            args[1],
        )


def test_validate_rest_flattened_error(transport: str = "rest"):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.validate(
            compute.ValidateUrlMapRequest(),
            project="project_value",
            url_map="url_map_value",
            url_maps_validate_request_resource=compute.UrlMapsValidateRequest(
                load_balancing_schemes=["load_balancing_schemes_value"]
            ),
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = UrlMapsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = UrlMapsClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = UrlMapsClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = UrlMapsClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = UrlMapsClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = UrlMapsClient(transport=transport)
    assert client.transport is transport


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.UrlMapsRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_kind_rest():
    transport = UrlMapsClient.get_transport_class("rest")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "rest"


def test_aggregated_list_rest_bad_request(
    request_type=compute.AggregatedListUrlMapsRequest,
):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"project": "sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        client.aggregated_list(request)


@pytest.mark.parametrize(
    "request_type",
    [
        compute.AggregatedListUrlMapsRequest,
        dict,
    ],
)
def test_aggregated_list_rest_call_success(request_type):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.UrlMapsAggregatedList(
            id="id_value",
            kind="kind_value",
            next_page_token="next_page_token_value",
            self_link="self_link_value",
            unreachables=["unreachables_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = compute.UrlMapsAggregatedList.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.aggregated_list(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.AggregatedListPager)
    assert response.id == "id_value"
    assert response.kind == "kind_value"
    assert response.next_page_token == "next_page_token_value"
    assert response.self_link == "self_link_value"
    assert response.unreachables == ["unreachables_value"]


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_aggregated_list_rest_interceptors(null_interceptor):
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.UrlMapsRestInterceptor(),
    )
    client = UrlMapsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.UrlMapsRestInterceptor, "post_aggregated_list"
    ) as post, mock.patch.object(
        transports.UrlMapsRestInterceptor, "pre_aggregated_list"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.AggregatedListUrlMapsRequest.pb(
            compute.AggregatedListUrlMapsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = compute.UrlMapsAggregatedList.to_json(
            compute.UrlMapsAggregatedList()
        )
        req.return_value.content = return_value

        request = compute.AggregatedListUrlMapsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.UrlMapsAggregatedList()

        client.aggregated_list(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_rest_bad_request(request_type=compute.DeleteUrlMapRequest):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "url_map": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        client.delete(request)


@pytest.mark.parametrize(
    "request_type",
    [
        compute.DeleteUrlMapRequest,
        dict,
    ],
)
def test_delete_rest_call_success(request_type):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "url_map": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_rest_interceptors(null_interceptor):
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.UrlMapsRestInterceptor(),
    )
    client = UrlMapsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.UrlMapsRestInterceptor, "post_delete"
    ) as post, mock.patch.object(
        transports.UrlMapsRestInterceptor, "pre_delete"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.DeleteUrlMapRequest.pb(compute.DeleteUrlMapRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = compute.Operation.to_json(compute.Operation())
        req.return_value.content = return_value

        request = compute.DeleteUrlMapRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation()

        client.delete(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_rest_bad_request(request_type=compute.GetUrlMapRequest):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "url_map": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        client.get(request)


@pytest.mark.parametrize(
    "request_type",
    [
        compute.GetUrlMapRequest,
        dict,
    ],
)
def test_get_rest_call_success(request_type):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "url_map": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.UrlMap(
            creation_timestamp="creation_timestamp_value",
            default_service="default_service_value",
            description="description_value",
            fingerprint="fingerprint_value",
            id=205,
            kind="kind_value",
            name="name_value",
            region="region_value",
            self_link="self_link_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = compute.UrlMap.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.UrlMap)
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.default_service == "default_service_value"
    assert response.description == "description_value"
    assert response.fingerprint == "fingerprint_value"
    assert response.id == 205
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_rest_interceptors(null_interceptor):
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.UrlMapsRestInterceptor(),
    )
    client = UrlMapsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.UrlMapsRestInterceptor, "post_get"
    ) as post, mock.patch.object(
        transports.UrlMapsRestInterceptor, "pre_get"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.GetUrlMapRequest.pb(compute.GetUrlMapRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = compute.UrlMap.to_json(compute.UrlMap())
        req.return_value.content = return_value

        request = compute.GetUrlMapRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.UrlMap()

        client.get(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_insert_rest_bad_request(request_type=compute.InsertUrlMapRequest):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"project": "sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        client.insert(request)


@pytest.mark.parametrize(
    "request_type",
    [
        compute.InsertUrlMapRequest,
        dict,
    ],
)
def test_insert_rest_call_success(request_type):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1"}
    request_init["url_map_resource"] = {
        "creation_timestamp": "creation_timestamp_value",
        "default_route_action": {
            "cors_policy": {
                "allow_credentials": True,
                "allow_headers": ["allow_headers_value1", "allow_headers_value2"],
                "allow_methods": ["allow_methods_value1", "allow_methods_value2"],
                "allow_origin_regexes": [
                    "allow_origin_regexes_value1",
                    "allow_origin_regexes_value2",
                ],
                "allow_origins": ["allow_origins_value1", "allow_origins_value2"],
                "disabled": True,
                "expose_headers": ["expose_headers_value1", "expose_headers_value2"],
                "max_age": 722,
            },
            "fault_injection_policy": {
                "abort": {"http_status": 1219, "percentage": 0.10540000000000001},
                "delay": {
                    "fixed_delay": {"nanos": 543, "seconds": 751},
                    "percentage": 0.10540000000000001,
                },
            },
            "max_stream_duration": {},
            "request_mirror_policy": {"backend_service": "backend_service_value"},
            "retry_policy": {
                "num_retries": 1197,
                "per_try_timeout": {},
                "retry_conditions": [
                    "retry_conditions_value1",
                    "retry_conditions_value2",
                ],
            },
            "timeout": {},
            "url_rewrite": {
                "host_rewrite": "host_rewrite_value",
                "path_prefix_rewrite": "path_prefix_rewrite_value",
                "path_template_rewrite": "path_template_rewrite_value",
            },
            "weighted_backend_services": [
                {
                    "backend_service": "backend_service_value",
                    "header_action": {
                        "request_headers_to_add": [
                            {
                                "header_name": "header_name_value",
                                "header_value": "header_value_value",
                                "replace": True,
                            }
                        ],
                        "request_headers_to_remove": [
                            "request_headers_to_remove_value1",
                            "request_headers_to_remove_value2",
                        ],
                        "response_headers_to_add": {},
                        "response_headers_to_remove": [
                            "response_headers_to_remove_value1",
                            "response_headers_to_remove_value2",
                        ],
                    },
                    "weight": 648,
                }
            ],
        },
        "default_service": "default_service_value",
        "default_url_redirect": {
            "host_redirect": "host_redirect_value",
            "https_redirect": True,
            "path_redirect": "path_redirect_value",
            "prefix_redirect": "prefix_redirect_value",
            "redirect_response_code": "redirect_response_code_value",
            "strip_query": True,
        },
        "description": "description_value",
        "fingerprint": "fingerprint_value",
        "header_action": {},
        "host_rules": [
            {
                "description": "description_value",
                "hosts": ["hosts_value1", "hosts_value2"],
                "path_matcher": "path_matcher_value",
            }
        ],
        "id": 205,
        "kind": "kind_value",
        "name": "name_value",
        "path_matchers": [
            {
                "default_route_action": {},
                "default_service": "default_service_value",
                "default_url_redirect": {},
                "description": "description_value",
                "header_action": {},
                "name": "name_value",
                "path_rules": [
                    {
                        "paths": ["paths_value1", "paths_value2"],
                        "route_action": {},
                        "service": "service_value",
                        "url_redirect": {},
                    }
                ],
                "route_rules": [
                    {
                        "description": "description_value",
                        "header_action": {},
                        "match_rules": [
                            {
                                "full_path_match": "full_path_match_value",
                                "header_matches": [
                                    {
                                        "exact_match": "exact_match_value",
                                        "header_name": "header_name_value",
                                        "invert_match": True,
                                        "prefix_match": "prefix_match_value",
                                        "present_match": True,
                                        "range_match": {
                                            "range_end": 931,
                                            "range_start": 1178,
                                        },
                                        "regex_match": "regex_match_value",
                                        "suffix_match": "suffix_match_value",
                                    }
                                ],
                                "ignore_case": True,
                                "metadata_filters": [
                                    {
                                        "filter_labels": [
                                            {
                                                "name": "name_value",
                                                "value": "value_value",
                                            }
                                        ],
                                        "filter_match_criteria": "filter_match_criteria_value",
                                    }
                                ],
                                "path_template_match": "path_template_match_value",
                                "prefix_match": "prefix_match_value",
                                "query_parameter_matches": [
                                    {
                                        "exact_match": "exact_match_value",
                                        "name": "name_value",
                                        "present_match": True,
                                        "regex_match": "regex_match_value",
                                    }
                                ],
                                "regex_match": "regex_match_value",
                            }
                        ],
                        "priority": 898,
                        "route_action": {},
                        "service": "service_value",
                        "url_redirect": {},
                    }
                ],
            }
        ],
        "region": "region_value",
        "self_link": "self_link_value",
        "tests": [
            {
                "description": "description_value",
                "expected_output_url": "expected_output_url_value",
                "expected_redirect_response_code": 3275,
                "headers": [{"name": "name_value", "value": "value_value"}],
                "host": "host_value",
                "path": "path_value",
                "service": "service_value",
            }
        ],
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = compute.InsertUrlMapRequest.meta.fields["url_map_resource"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["url_map_resource"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["url_map_resource"][field])):
                    del request_init["url_map_resource"][field][i][subfield]
            else:
                del request_init["url_map_resource"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.insert(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_insert_rest_interceptors(null_interceptor):
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.UrlMapsRestInterceptor(),
    )
    client = UrlMapsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.UrlMapsRestInterceptor, "post_insert"
    ) as post, mock.patch.object(
        transports.UrlMapsRestInterceptor, "pre_insert"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.InsertUrlMapRequest.pb(compute.InsertUrlMapRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = compute.Operation.to_json(compute.Operation())
        req.return_value.content = return_value

        request = compute.InsertUrlMapRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation()

        client.insert(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_invalidate_cache_rest_bad_request(
    request_type=compute.InvalidateCacheUrlMapRequest,
):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "url_map": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        client.invalidate_cache(request)


@pytest.mark.parametrize(
    "request_type",
    [
        compute.InvalidateCacheUrlMapRequest,
        dict,
    ],
)
def test_invalidate_cache_rest_call_success(request_type):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "url_map": "sample2"}
    request_init["cache_invalidation_rule_resource"] = {
        "host": "host_value",
        "path": "path_value",
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = compute.InvalidateCacheUrlMapRequest.meta.fields[
        "cache_invalidation_rule_resource"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init[
        "cache_invalidation_rule_resource"
    ].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(
                    0, len(request_init["cache_invalidation_rule_resource"][field])
                ):
                    del request_init["cache_invalidation_rule_resource"][field][i][
                        subfield
                    ]
            else:
                del request_init["cache_invalidation_rule_resource"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.invalidate_cache(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_invalidate_cache_rest_interceptors(null_interceptor):
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.UrlMapsRestInterceptor(),
    )
    client = UrlMapsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.UrlMapsRestInterceptor, "post_invalidate_cache"
    ) as post, mock.patch.object(
        transports.UrlMapsRestInterceptor, "pre_invalidate_cache"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.InvalidateCacheUrlMapRequest.pb(
            compute.InvalidateCacheUrlMapRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = compute.Operation.to_json(compute.Operation())
        req.return_value.content = return_value

        request = compute.InvalidateCacheUrlMapRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation()

        client.invalidate_cache(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_rest_bad_request(request_type=compute.ListUrlMapsRequest):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"project": "sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        client.list(request)


@pytest.mark.parametrize(
    "request_type",
    [
        compute.ListUrlMapsRequest,
        dict,
    ],
)
def test_list_rest_call_success(request_type):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.UrlMapList(
            id="id_value",
            kind="kind_value",
            next_page_token="next_page_token_value",
            self_link="self_link_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = compute.UrlMapList.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPager)
    assert response.id == "id_value"
    assert response.kind == "kind_value"
    assert response.next_page_token == "next_page_token_value"
    assert response.self_link == "self_link_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_rest_interceptors(null_interceptor):
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.UrlMapsRestInterceptor(),
    )
    client = UrlMapsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.UrlMapsRestInterceptor, "post_list"
    ) as post, mock.patch.object(
        transports.UrlMapsRestInterceptor, "pre_list"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.ListUrlMapsRequest.pb(compute.ListUrlMapsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = compute.UrlMapList.to_json(compute.UrlMapList())
        req.return_value.content = return_value

        request = compute.ListUrlMapsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.UrlMapList()

        client.list(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_patch_rest_bad_request(request_type=compute.PatchUrlMapRequest):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "url_map": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        client.patch(request)


@pytest.mark.parametrize(
    "request_type",
    [
        compute.PatchUrlMapRequest,
        dict,
    ],
)
def test_patch_rest_call_success(request_type):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "url_map": "sample2"}
    request_init["url_map_resource"] = {
        "creation_timestamp": "creation_timestamp_value",
        "default_route_action": {
            "cors_policy": {
                "allow_credentials": True,
                "allow_headers": ["allow_headers_value1", "allow_headers_value2"],
                "allow_methods": ["allow_methods_value1", "allow_methods_value2"],
                "allow_origin_regexes": [
                    "allow_origin_regexes_value1",
                    "allow_origin_regexes_value2",
                ],
                "allow_origins": ["allow_origins_value1", "allow_origins_value2"],
                "disabled": True,
                "expose_headers": ["expose_headers_value1", "expose_headers_value2"],
                "max_age": 722,
            },
            "fault_injection_policy": {
                "abort": {"http_status": 1219, "percentage": 0.10540000000000001},
                "delay": {
                    "fixed_delay": {"nanos": 543, "seconds": 751},
                    "percentage": 0.10540000000000001,
                },
            },
            "max_stream_duration": {},
            "request_mirror_policy": {"backend_service": "backend_service_value"},
            "retry_policy": {
                "num_retries": 1197,
                "per_try_timeout": {},
                "retry_conditions": [
                    "retry_conditions_value1",
                    "retry_conditions_value2",
                ],
            },
            "timeout": {},
            "url_rewrite": {
                "host_rewrite": "host_rewrite_value",
                "path_prefix_rewrite": "path_prefix_rewrite_value",
                "path_template_rewrite": "path_template_rewrite_value",
            },
            "weighted_backend_services": [
                {
                    "backend_service": "backend_service_value",
                    "header_action": {
                        "request_headers_to_add": [
                            {
                                "header_name": "header_name_value",
                                "header_value": "header_value_value",
                                "replace": True,
                            }
                        ],
                        "request_headers_to_remove": [
                            "request_headers_to_remove_value1",
                            "request_headers_to_remove_value2",
                        ],
                        "response_headers_to_add": {},
                        "response_headers_to_remove": [
                            "response_headers_to_remove_value1",
                            "response_headers_to_remove_value2",
                        ],
                    },
                    "weight": 648,
                }
            ],
        },
        "default_service": "default_service_value",
        "default_url_redirect": {
            "host_redirect": "host_redirect_value",
            "https_redirect": True,
            "path_redirect": "path_redirect_value",
            "prefix_redirect": "prefix_redirect_value",
            "redirect_response_code": "redirect_response_code_value",
            "strip_query": True,
        },
        "description": "description_value",
        "fingerprint": "fingerprint_value",
        "header_action": {},
        "host_rules": [
            {
                "description": "description_value",
                "hosts": ["hosts_value1", "hosts_value2"],
                "path_matcher": "path_matcher_value",
            }
        ],
        "id": 205,
        "kind": "kind_value",
        "name": "name_value",
        "path_matchers": [
            {
                "default_route_action": {},
                "default_service": "default_service_value",
                "default_url_redirect": {},
                "description": "description_value",
                "header_action": {},
                "name": "name_value",
                "path_rules": [
                    {
                        "paths": ["paths_value1", "paths_value2"],
                        "route_action": {},
                        "service": "service_value",
                        "url_redirect": {},
                    }
                ],
                "route_rules": [
                    {
                        "description": "description_value",
                        "header_action": {},
                        "match_rules": [
                            {
                                "full_path_match": "full_path_match_value",
                                "header_matches": [
                                    {
                                        "exact_match": "exact_match_value",
                                        "header_name": "header_name_value",
                                        "invert_match": True,
                                        "prefix_match": "prefix_match_value",
                                        "present_match": True,
                                        "range_match": {
                                            "range_end": 931,
                                            "range_start": 1178,
                                        },
                                        "regex_match": "regex_match_value",
                                        "suffix_match": "suffix_match_value",
                                    }
                                ],
                                "ignore_case": True,
                                "metadata_filters": [
                                    {
                                        "filter_labels": [
                                            {
                                                "name": "name_value",
                                                "value": "value_value",
                                            }
                                        ],
                                        "filter_match_criteria": "filter_match_criteria_value",
                                    }
                                ],
                                "path_template_match": "path_template_match_value",
                                "prefix_match": "prefix_match_value",
                                "query_parameter_matches": [
                                    {
                                        "exact_match": "exact_match_value",
                                        "name": "name_value",
                                        "present_match": True,
                                        "regex_match": "regex_match_value",
                                    }
                                ],
                                "regex_match": "regex_match_value",
                            }
                        ],
                        "priority": 898,
                        "route_action": {},
                        "service": "service_value",
                        "url_redirect": {},
                    }
                ],
            }
        ],
        "region": "region_value",
        "self_link": "self_link_value",
        "tests": [
            {
                "description": "description_value",
                "expected_output_url": "expected_output_url_value",
                "expected_redirect_response_code": 3275,
                "headers": [{"name": "name_value", "value": "value_value"}],
                "host": "host_value",
                "path": "path_value",
                "service": "service_value",
            }
        ],
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = compute.PatchUrlMapRequest.meta.fields["url_map_resource"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["url_map_resource"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["url_map_resource"][field])):
                    del request_init["url_map_resource"][field][i][subfield]
            else:
                del request_init["url_map_resource"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.patch(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_patch_rest_interceptors(null_interceptor):
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.UrlMapsRestInterceptor(),
    )
    client = UrlMapsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.UrlMapsRestInterceptor, "post_patch"
    ) as post, mock.patch.object(
        transports.UrlMapsRestInterceptor, "pre_patch"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.PatchUrlMapRequest.pb(compute.PatchUrlMapRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = compute.Operation.to_json(compute.Operation())
        req.return_value.content = return_value

        request = compute.PatchUrlMapRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation()

        client.patch(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_rest_bad_request(request_type=compute.UpdateUrlMapRequest):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "url_map": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        client.update(request)


@pytest.mark.parametrize(
    "request_type",
    [
        compute.UpdateUrlMapRequest,
        dict,
    ],
)
def test_update_rest_call_success(request_type):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "url_map": "sample2"}
    request_init["url_map_resource"] = {
        "creation_timestamp": "creation_timestamp_value",
        "default_route_action": {
            "cors_policy": {
                "allow_credentials": True,
                "allow_headers": ["allow_headers_value1", "allow_headers_value2"],
                "allow_methods": ["allow_methods_value1", "allow_methods_value2"],
                "allow_origin_regexes": [
                    "allow_origin_regexes_value1",
                    "allow_origin_regexes_value2",
                ],
                "allow_origins": ["allow_origins_value1", "allow_origins_value2"],
                "disabled": True,
                "expose_headers": ["expose_headers_value1", "expose_headers_value2"],
                "max_age": 722,
            },
            "fault_injection_policy": {
                "abort": {"http_status": 1219, "percentage": 0.10540000000000001},
                "delay": {
                    "fixed_delay": {"nanos": 543, "seconds": 751},
                    "percentage": 0.10540000000000001,
                },
            },
            "max_stream_duration": {},
            "request_mirror_policy": {"backend_service": "backend_service_value"},
            "retry_policy": {
                "num_retries": 1197,
                "per_try_timeout": {},
                "retry_conditions": [
                    "retry_conditions_value1",
                    "retry_conditions_value2",
                ],
            },
            "timeout": {},
            "url_rewrite": {
                "host_rewrite": "host_rewrite_value",
                "path_prefix_rewrite": "path_prefix_rewrite_value",
                "path_template_rewrite": "path_template_rewrite_value",
            },
            "weighted_backend_services": [
                {
                    "backend_service": "backend_service_value",
                    "header_action": {
                        "request_headers_to_add": [
                            {
                                "header_name": "header_name_value",
                                "header_value": "header_value_value",
                                "replace": True,
                            }
                        ],
                        "request_headers_to_remove": [
                            "request_headers_to_remove_value1",
                            "request_headers_to_remove_value2",
                        ],
                        "response_headers_to_add": {},
                        "response_headers_to_remove": [
                            "response_headers_to_remove_value1",
                            "response_headers_to_remove_value2",
                        ],
                    },
                    "weight": 648,
                }
            ],
        },
        "default_service": "default_service_value",
        "default_url_redirect": {
            "host_redirect": "host_redirect_value",
            "https_redirect": True,
            "path_redirect": "path_redirect_value",
            "prefix_redirect": "prefix_redirect_value",
            "redirect_response_code": "redirect_response_code_value",
            "strip_query": True,
        },
        "description": "description_value",
        "fingerprint": "fingerprint_value",
        "header_action": {},
        "host_rules": [
            {
                "description": "description_value",
                "hosts": ["hosts_value1", "hosts_value2"],
                "path_matcher": "path_matcher_value",
            }
        ],
        "id": 205,
        "kind": "kind_value",
        "name": "name_value",
        "path_matchers": [
            {
                "default_route_action": {},
                "default_service": "default_service_value",
                "default_url_redirect": {},
                "description": "description_value",
                "header_action": {},
                "name": "name_value",
                "path_rules": [
                    {
                        "paths": ["paths_value1", "paths_value2"],
                        "route_action": {},
                        "service": "service_value",
                        "url_redirect": {},
                    }
                ],
                "route_rules": [
                    {
                        "description": "description_value",
                        "header_action": {},
                        "match_rules": [
                            {
                                "full_path_match": "full_path_match_value",
                                "header_matches": [
                                    {
                                        "exact_match": "exact_match_value",
                                        "header_name": "header_name_value",
                                        "invert_match": True,
                                        "prefix_match": "prefix_match_value",
                                        "present_match": True,
                                        "range_match": {
                                            "range_end": 931,
                                            "range_start": 1178,
                                        },
                                        "regex_match": "regex_match_value",
                                        "suffix_match": "suffix_match_value",
                                    }
                                ],
                                "ignore_case": True,
                                "metadata_filters": [
                                    {
                                        "filter_labels": [
                                            {
                                                "name": "name_value",
                                                "value": "value_value",
                                            }
                                        ],
                                        "filter_match_criteria": "filter_match_criteria_value",
                                    }
                                ],
                                "path_template_match": "path_template_match_value",
                                "prefix_match": "prefix_match_value",
                                "query_parameter_matches": [
                                    {
                                        "exact_match": "exact_match_value",
                                        "name": "name_value",
                                        "present_match": True,
                                        "regex_match": "regex_match_value",
                                    }
                                ],
                                "regex_match": "regex_match_value",
                            }
                        ],
                        "priority": 898,
                        "route_action": {},
                        "service": "service_value",
                        "url_redirect": {},
                    }
                ],
            }
        ],
        "region": "region_value",
        "self_link": "self_link_value",
        "tests": [
            {
                "description": "description_value",
                "expected_output_url": "expected_output_url_value",
                "expected_redirect_response_code": 3275,
                "headers": [{"name": "name_value", "value": "value_value"}],
                "host": "host_value",
                "path": "path_value",
                "service": "service_value",
            }
        ],
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = compute.UpdateUrlMapRequest.meta.fields["url_map_resource"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["url_map_resource"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["url_map_resource"][field])):
                    del request_init["url_map_resource"][field][i][subfield]
            else:
                del request_init["url_map_resource"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_rest_interceptors(null_interceptor):
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.UrlMapsRestInterceptor(),
    )
    client = UrlMapsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.UrlMapsRestInterceptor, "post_update"
    ) as post, mock.patch.object(
        transports.UrlMapsRestInterceptor, "pre_update"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.UpdateUrlMapRequest.pb(compute.UpdateUrlMapRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = compute.Operation.to_json(compute.Operation())
        req.return_value.content = return_value

        request = compute.UpdateUrlMapRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation()

        client.update(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_validate_rest_bad_request(request_type=compute.ValidateUrlMapRequest):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "url_map": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        client.validate(request)


@pytest.mark.parametrize(
    "request_type",
    [
        compute.ValidateUrlMapRequest,
        dict,
    ],
)
def test_validate_rest_call_success(request_type):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "url_map": "sample2"}
    request_init["url_maps_validate_request_resource"] = {
        "load_balancing_schemes": [
            "load_balancing_schemes_value1",
            "load_balancing_schemes_value2",
        ],
        "resource": {
            "creation_timestamp": "creation_timestamp_value",
            "default_route_action": {
                "cors_policy": {
                    "allow_credentials": True,
                    "allow_headers": ["allow_headers_value1", "allow_headers_value2"],
                    "allow_methods": ["allow_methods_value1", "allow_methods_value2"],
                    "allow_origin_regexes": [
                        "allow_origin_regexes_value1",
                        "allow_origin_regexes_value2",
                    ],
                    "allow_origins": ["allow_origins_value1", "allow_origins_value2"],
                    "disabled": True,
                    "expose_headers": [
                        "expose_headers_value1",
                        "expose_headers_value2",
                    ],
                    "max_age": 722,
                },
                "fault_injection_policy": {
                    "abort": {"http_status": 1219, "percentage": 0.10540000000000001},
                    "delay": {
                        "fixed_delay": {"nanos": 543, "seconds": 751},
                        "percentage": 0.10540000000000001,
                    },
                },
                "max_stream_duration": {},
                "request_mirror_policy": {"backend_service": "backend_service_value"},
                "retry_policy": {
                    "num_retries": 1197,
                    "per_try_timeout": {},
                    "retry_conditions": [
                        "retry_conditions_value1",
                        "retry_conditions_value2",
                    ],
                },
                "timeout": {},
                "url_rewrite": {
                    "host_rewrite": "host_rewrite_value",
                    "path_prefix_rewrite": "path_prefix_rewrite_value",
                    "path_template_rewrite": "path_template_rewrite_value",
                },
                "weighted_backend_services": [
                    {
                        "backend_service": "backend_service_value",
                        "header_action": {
                            "request_headers_to_add": [
                                {
                                    "header_name": "header_name_value",
                                    "header_value": "header_value_value",
                                    "replace": True,
                                }
                            ],
                            "request_headers_to_remove": [
                                "request_headers_to_remove_value1",
                                "request_headers_to_remove_value2",
                            ],
                            "response_headers_to_add": {},
                            "response_headers_to_remove": [
                                "response_headers_to_remove_value1",
                                "response_headers_to_remove_value2",
                            ],
                        },
                        "weight": 648,
                    }
                ],
            },
            "default_service": "default_service_value",
            "default_url_redirect": {
                "host_redirect": "host_redirect_value",
                "https_redirect": True,
                "path_redirect": "path_redirect_value",
                "prefix_redirect": "prefix_redirect_value",
                "redirect_response_code": "redirect_response_code_value",
                "strip_query": True,
            },
            "description": "description_value",
            "fingerprint": "fingerprint_value",
            "header_action": {},
            "host_rules": [
                {
                    "description": "description_value",
                    "hosts": ["hosts_value1", "hosts_value2"],
                    "path_matcher": "path_matcher_value",
                }
            ],
            "id": 205,
            "kind": "kind_value",
            "name": "name_value",
            "path_matchers": [
                {
                    "default_route_action": {},
                    "default_service": "default_service_value",
                    "default_url_redirect": {},
                    "description": "description_value",
                    "header_action": {},
                    "name": "name_value",
                    "path_rules": [
                        {
                            "paths": ["paths_value1", "paths_value2"],
                            "route_action": {},
                            "service": "service_value",
                            "url_redirect": {},
                        }
                    ],
                    "route_rules": [
                        {
                            "description": "description_value",
                            "header_action": {},
                            "match_rules": [
                                {
                                    "full_path_match": "full_path_match_value",
                                    "header_matches": [
                                        {
                                            "exact_match": "exact_match_value",
                                            "header_name": "header_name_value",
                                            "invert_match": True,
                                            "prefix_match": "prefix_match_value",
                                            "present_match": True,
                                            "range_match": {
                                                "range_end": 931,
                                                "range_start": 1178,
                                            },
                                            "regex_match": "regex_match_value",
                                            "suffix_match": "suffix_match_value",
                                        }
                                    ],
                                    "ignore_case": True,
                                    "metadata_filters": [
                                        {
                                            "filter_labels": [
                                                {
                                                    "name": "name_value",
                                                    "value": "value_value",
                                                }
                                            ],
                                            "filter_match_criteria": "filter_match_criteria_value",
                                        }
                                    ],
                                    "path_template_match": "path_template_match_value",
                                    "prefix_match": "prefix_match_value",
                                    "query_parameter_matches": [
                                        {
                                            "exact_match": "exact_match_value",
                                            "name": "name_value",
                                            "present_match": True,
                                            "regex_match": "regex_match_value",
                                        }
                                    ],
                                    "regex_match": "regex_match_value",
                                }
                            ],
                            "priority": 898,
                            "route_action": {},
                            "service": "service_value",
                            "url_redirect": {},
                        }
                    ],
                }
            ],
            "region": "region_value",
            "self_link": "self_link_value",
            "tests": [
                {
                    "description": "description_value",
                    "expected_output_url": "expected_output_url_value",
                    "expected_redirect_response_code": 3275,
                    "headers": [{"name": "name_value", "value": "value_value"}],
                    "host": "host_value",
                    "path": "path_value",
                    "service": "service_value",
                }
            ],
        },
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = compute.ValidateUrlMapRequest.meta.fields[
        "url_maps_validate_request_resource"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init[
        "url_maps_validate_request_resource"
    ].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(
                    0, len(request_init["url_maps_validate_request_resource"][field])
                ):
                    del request_init["url_maps_validate_request_resource"][field][i][
                        subfield
                    ]
            else:
                del request_init["url_maps_validate_request_resource"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.UrlMapsValidateResponse()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = compute.UrlMapsValidateResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.validate(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.UrlMapsValidateResponse)


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_validate_rest_interceptors(null_interceptor):
    transport = transports.UrlMapsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.UrlMapsRestInterceptor(),
    )
    client = UrlMapsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.UrlMapsRestInterceptor, "post_validate"
    ) as post, mock.patch.object(
        transports.UrlMapsRestInterceptor, "pre_validate"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.ValidateUrlMapRequest.pb(compute.ValidateUrlMapRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = compute.UrlMapsValidateResponse.to_json(
            compute.UrlMapsValidateResponse()
        )
        req.return_value.content = return_value

        request = compute.ValidateUrlMapRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.UrlMapsValidateResponse()

        client.validate(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_initialize_client_w_rest():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_aggregated_list_empty_call_rest():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.aggregated_list), "__call__") as call:
        client.aggregated_list(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = compute.AggregatedListUrlMapsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_unary_empty_call_rest():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.delete), "__call__") as call:
        client.delete_unary(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = compute.DeleteUrlMapRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_empty_call_rest():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get), "__call__") as call:
        client.get(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = compute.GetUrlMapRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_insert_unary_empty_call_rest():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.insert), "__call__") as call:
        client.insert_unary(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = compute.InsertUrlMapRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_invalidate_cache_unary_empty_call_rest():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.invalidate_cache), "__call__") as call:
        client.invalidate_cache_unary(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = compute.InvalidateCacheUrlMapRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_empty_call_rest():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list), "__call__") as call:
        client.list(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = compute.ListUrlMapsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_patch_unary_empty_call_rest():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.patch), "__call__") as call:
        client.patch_unary(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = compute.PatchUrlMapRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_unary_empty_call_rest():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.update), "__call__") as call:
        client.update_unary(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = compute.UpdateUrlMapRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_validate_empty_call_rest():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.validate), "__call__") as call:
        client.validate(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = compute.ValidateUrlMapRequest()

        assert args[0] == request_msg


def test_url_maps_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.UrlMapsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_url_maps_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.compute_v1.services.url_maps.transports.UrlMapsTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.UrlMapsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "aggregated_list",
        "delete",
        "get",
        "insert",
        "invalidate_cache",
        "list",
        "patch",
        "update",
        "validate",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_url_maps_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.compute_v1.services.url_maps.transports.UrlMapsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.UrlMapsTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


def test_url_maps_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.compute_v1.services.url_maps.transports.UrlMapsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.UrlMapsTransport()
        adc.assert_called_once()


def test_url_maps_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        UrlMapsClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id=None,
        )


def test_url_maps_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.UrlMapsRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_url_maps_host_no_port(transport_name):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="compute.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "compute.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://compute.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_url_maps_host_with_port(transport_name):
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="compute.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "compute.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://compute.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_url_maps_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = UrlMapsClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = UrlMapsClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.aggregated_list._session
    session2 = client2.transport.aggregated_list._session
    assert session1 != session2
    session1 = client1.transport.delete._session
    session2 = client2.transport.delete._session
    assert session1 != session2
    session1 = client1.transport.get._session
    session2 = client2.transport.get._session
    assert session1 != session2
    session1 = client1.transport.insert._session
    session2 = client2.transport.insert._session
    assert session1 != session2
    session1 = client1.transport.invalidate_cache._session
    session2 = client2.transport.invalidate_cache._session
    assert session1 != session2
    session1 = client1.transport.list._session
    session2 = client2.transport.list._session
    assert session1 != session2
    session1 = client1.transport.patch._session
    session2 = client2.transport.patch._session
    assert session1 != session2
    session1 = client1.transport.update._session
    session2 = client2.transport.update._session
    assert session1 != session2
    session1 = client1.transport.validate._session
    session2 = client2.transport.validate._session
    assert session1 != session2


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = UrlMapsClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = UrlMapsClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = UrlMapsClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = UrlMapsClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = UrlMapsClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = UrlMapsClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = UrlMapsClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = UrlMapsClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = UrlMapsClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = UrlMapsClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = UrlMapsClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = UrlMapsClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = UrlMapsClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = UrlMapsClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = UrlMapsClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.UrlMapsTransport, "_prep_wrapped_messages"
    ) as prep:
        client = UrlMapsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.UrlMapsTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = UrlMapsClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_transport_close_rest():
    client = UrlMapsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_session")), "close"
    ) as close:
        with client:
            close.assert_not_called()
        close.assert_called_once()


def test_client_ctx():
    transports = [
        "rest",
    ]
    for transport in transports:
        client = UrlMapsClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (UrlMapsClient, transports.UrlMapsRestTransport),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
