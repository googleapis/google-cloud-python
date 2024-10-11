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

from google.api_core import gapic_v1, grpc_helpers, grpc_helpers_async, path_template
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.oauth2 import service_account

from google.ads.marketingplatform_admin_v1alpha.services.marketingplatform_admin_service import (
    MarketingplatformAdminServiceAsyncClient,
    MarketingplatformAdminServiceClient,
    pagers,
    transports,
)
from google.ads.marketingplatform_admin_v1alpha.types import (
    marketingplatform_admin,
    resources,
)


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

    assert MarketingplatformAdminServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        MarketingplatformAdminServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        MarketingplatformAdminServiceClient._get_default_mtls_endpoint(
            api_mtls_endpoint
        )
        == api_mtls_endpoint
    )
    assert (
        MarketingplatformAdminServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        MarketingplatformAdminServiceClient._get_default_mtls_endpoint(
            sandbox_mtls_endpoint
        )
        == sandbox_mtls_endpoint
    )
    assert (
        MarketingplatformAdminServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


def test__read_environment_variables():
    assert MarketingplatformAdminServiceClient._read_environment_variables() == (
        False,
        "auto",
        None,
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert MarketingplatformAdminServiceClient._read_environment_variables() == (
            True,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert MarketingplatformAdminServiceClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            MarketingplatformAdminServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert MarketingplatformAdminServiceClient._read_environment_variables() == (
            False,
            "never",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert MarketingplatformAdminServiceClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert MarketingplatformAdminServiceClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            MarketingplatformAdminServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert MarketingplatformAdminServiceClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert (
        MarketingplatformAdminServiceClient._get_client_cert_source(None, False) is None
    )
    assert (
        MarketingplatformAdminServiceClient._get_client_cert_source(
            mock_provided_cert_source, False
        )
        is None
    )
    assert (
        MarketingplatformAdminServiceClient._get_client_cert_source(
            mock_provided_cert_source, True
        )
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
                MarketingplatformAdminServiceClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                MarketingplatformAdminServiceClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    MarketingplatformAdminServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(MarketingplatformAdminServiceClient),
)
@mock.patch.object(
    MarketingplatformAdminServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(MarketingplatformAdminServiceAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = MarketingplatformAdminServiceClient._DEFAULT_UNIVERSE
    default_endpoint = (
        MarketingplatformAdminServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
            UNIVERSE_DOMAIN=default_universe
        )
    )
    mock_universe = "bar.com"
    mock_endpoint = (
        MarketingplatformAdminServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
            UNIVERSE_DOMAIN=mock_universe
        )
    )

    assert (
        MarketingplatformAdminServiceClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        MarketingplatformAdminServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == MarketingplatformAdminServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        MarketingplatformAdminServiceClient._get_api_endpoint(
            None, None, default_universe, "auto"
        )
        == default_endpoint
    )
    assert (
        MarketingplatformAdminServiceClient._get_api_endpoint(
            None, None, default_universe, "always"
        )
        == MarketingplatformAdminServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        MarketingplatformAdminServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == MarketingplatformAdminServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        MarketingplatformAdminServiceClient._get_api_endpoint(
            None, None, mock_universe, "never"
        )
        == mock_endpoint
    )
    assert (
        MarketingplatformAdminServiceClient._get_api_endpoint(
            None, None, default_universe, "never"
        )
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        MarketingplatformAdminServiceClient._get_api_endpoint(
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
        MarketingplatformAdminServiceClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        MarketingplatformAdminServiceClient._get_universe_domain(
            None, universe_domain_env
        )
        == universe_domain_env
    )
    assert (
        MarketingplatformAdminServiceClient._get_universe_domain(None, None)
        == MarketingplatformAdminServiceClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        MarketingplatformAdminServiceClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            MarketingplatformAdminServiceClient,
            transports.MarketingplatformAdminServiceGrpcTransport,
            "grpc",
        ),
        (
            MarketingplatformAdminServiceClient,
            transports.MarketingplatformAdminServiceRestTransport,
            "rest",
        ),
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
        (MarketingplatformAdminServiceClient, "grpc"),
        (MarketingplatformAdminServiceAsyncClient, "grpc_asyncio"),
        (MarketingplatformAdminServiceClient, "rest"),
    ],
)
def test_marketingplatform_admin_service_client_from_service_account_info(
    client_class, transport_name
):
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
            "marketingplatformadmin.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://marketingplatformadmin.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.MarketingplatformAdminServiceGrpcTransport, "grpc"),
        (transports.MarketingplatformAdminServiceGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.MarketingplatformAdminServiceRestTransport, "rest"),
    ],
)
def test_marketingplatform_admin_service_client_service_account_always_use_jwt(
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
        (MarketingplatformAdminServiceClient, "grpc"),
        (MarketingplatformAdminServiceAsyncClient, "grpc_asyncio"),
        (MarketingplatformAdminServiceClient, "rest"),
    ],
)
def test_marketingplatform_admin_service_client_from_service_account_file(
    client_class, transport_name
):
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
            "marketingplatformadmin.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://marketingplatformadmin.googleapis.com"
        )


def test_marketingplatform_admin_service_client_get_transport_class():
    transport = MarketingplatformAdminServiceClient.get_transport_class()
    available_transports = [
        transports.MarketingplatformAdminServiceGrpcTransport,
        transports.MarketingplatformAdminServiceRestTransport,
    ]
    assert transport in available_transports

    transport = MarketingplatformAdminServiceClient.get_transport_class("grpc")
    assert transport == transports.MarketingplatformAdminServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            MarketingplatformAdminServiceClient,
            transports.MarketingplatformAdminServiceGrpcTransport,
            "grpc",
        ),
        (
            MarketingplatformAdminServiceAsyncClient,
            transports.MarketingplatformAdminServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            MarketingplatformAdminServiceClient,
            transports.MarketingplatformAdminServiceRestTransport,
            "rest",
        ),
    ],
)
@mock.patch.object(
    MarketingplatformAdminServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(MarketingplatformAdminServiceClient),
)
@mock.patch.object(
    MarketingplatformAdminServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(MarketingplatformAdminServiceAsyncClient),
)
def test_marketingplatform_admin_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(
        MarketingplatformAdminServiceClient, "get_transport_class"
    ) as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(
        MarketingplatformAdminServiceClient, "get_transport_class"
    ) as gtc:
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
        (
            MarketingplatformAdminServiceClient,
            transports.MarketingplatformAdminServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            MarketingplatformAdminServiceAsyncClient,
            transports.MarketingplatformAdminServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            MarketingplatformAdminServiceClient,
            transports.MarketingplatformAdminServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            MarketingplatformAdminServiceAsyncClient,
            transports.MarketingplatformAdminServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            MarketingplatformAdminServiceClient,
            transports.MarketingplatformAdminServiceRestTransport,
            "rest",
            "true",
        ),
        (
            MarketingplatformAdminServiceClient,
            transports.MarketingplatformAdminServiceRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    MarketingplatformAdminServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(MarketingplatformAdminServiceClient),
)
@mock.patch.object(
    MarketingplatformAdminServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(MarketingplatformAdminServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_marketingplatform_admin_service_client_mtls_env_auto(
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


@pytest.mark.parametrize(
    "client_class",
    [MarketingplatformAdminServiceClient, MarketingplatformAdminServiceAsyncClient],
)
@mock.patch.object(
    MarketingplatformAdminServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MarketingplatformAdminServiceClient),
)
@mock.patch.object(
    MarketingplatformAdminServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MarketingplatformAdminServiceAsyncClient),
)
def test_marketingplatform_admin_service_client_get_mtls_endpoint_and_cert_source(
    client_class,
):
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


@pytest.mark.parametrize(
    "client_class",
    [MarketingplatformAdminServiceClient, MarketingplatformAdminServiceAsyncClient],
)
@mock.patch.object(
    MarketingplatformAdminServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(MarketingplatformAdminServiceClient),
)
@mock.patch.object(
    MarketingplatformAdminServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(MarketingplatformAdminServiceAsyncClient),
)
def test_marketingplatform_admin_service_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = MarketingplatformAdminServiceClient._DEFAULT_UNIVERSE
    default_endpoint = (
        MarketingplatformAdminServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
            UNIVERSE_DOMAIN=default_universe
        )
    )
    mock_universe = "bar.com"
    mock_endpoint = (
        MarketingplatformAdminServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
            UNIVERSE_DOMAIN=mock_universe
        )
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
        (
            MarketingplatformAdminServiceClient,
            transports.MarketingplatformAdminServiceGrpcTransport,
            "grpc",
        ),
        (
            MarketingplatformAdminServiceAsyncClient,
            transports.MarketingplatformAdminServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            MarketingplatformAdminServiceClient,
            transports.MarketingplatformAdminServiceRestTransport,
            "rest",
        ),
    ],
)
def test_marketingplatform_admin_service_client_client_options_scopes(
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
        (
            MarketingplatformAdminServiceClient,
            transports.MarketingplatformAdminServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            MarketingplatformAdminServiceAsyncClient,
            transports.MarketingplatformAdminServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (
            MarketingplatformAdminServiceClient,
            transports.MarketingplatformAdminServiceRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_marketingplatform_admin_service_client_client_options_credentials_file(
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


def test_marketingplatform_admin_service_client_client_options_from_dict():
    with mock.patch(
        "google.ads.marketingplatform_admin_v1alpha.services.marketingplatform_admin_service.transports.MarketingplatformAdminServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = MarketingplatformAdminServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
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


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            MarketingplatformAdminServiceClient,
            transports.MarketingplatformAdminServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            MarketingplatformAdminServiceAsyncClient,
            transports.MarketingplatformAdminServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_marketingplatform_admin_service_client_create_channel_credentials_file(
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

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "marketingplatformadmin.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                "https://www.googleapis.com/auth/marketingplatformadmin.analytics.read",
                "https://www.googleapis.com/auth/marketingplatformadmin.analytics.update",
            ),
            scopes=None,
            default_host="marketingplatformadmin.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        marketingplatform_admin.GetOrganizationRequest,
        dict,
    ],
)
def test_get_organization(request_type, transport: str = "grpc"):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_organization), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Organization(
            name="name_value",
            display_name="display_name_value",
        )
        response = client.get_organization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = marketingplatform_admin.GetOrganizationRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Organization)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


def test_get_organization_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = marketingplatform_admin.GetOrganizationRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_organization), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_organization(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == marketingplatform_admin.GetOrganizationRequest(
            name="name_value",
        )


def test_get_organization_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = MarketingplatformAdminServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_organization in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_organization
        ] = mock_rpc
        request = {}
        client.get_organization(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_organization(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_organization_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = MarketingplatformAdminServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_organization
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_organization
        ] = mock_rpc

        request = {}
        await client.get_organization(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_organization(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_organization_async(
    transport: str = "grpc_asyncio",
    request_type=marketingplatform_admin.GetOrganizationRequest,
):
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_organization), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Organization(
                name="name_value",
                display_name="display_name_value",
            )
        )
        response = await client.get_organization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = marketingplatform_admin.GetOrganizationRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Organization)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_get_organization_async_from_dict():
    await test_get_organization_async(request_type=dict)


def test_get_organization_field_headers():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = marketingplatform_admin.GetOrganizationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_organization), "__call__") as call:
        call.return_value = resources.Organization()
        client.get_organization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_organization_field_headers_async():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = marketingplatform_admin.GetOrganizationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_organization), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Organization()
        )
        await client.get_organization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_organization_flattened():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_organization), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Organization()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_organization(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_organization_flattened_error():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_organization(
            marketingplatform_admin.GetOrganizationRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_organization_flattened_async():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_organization), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Organization()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Organization()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_organization(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_organization_flattened_error_async():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_organization(
            marketingplatform_admin.GetOrganizationRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        marketingplatform_admin.ListAnalyticsAccountLinksRequest,
        dict,
    ],
)
def test_list_analytics_account_links(request_type, transport: str = "grpc"):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_analytics_account_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = marketingplatform_admin.ListAnalyticsAccountLinksResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_analytics_account_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = marketingplatform_admin.ListAnalyticsAccountLinksRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAnalyticsAccountLinksPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_analytics_account_links_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = marketingplatform_admin.ListAnalyticsAccountLinksRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_analytics_account_links), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_analytics_account_links(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == marketingplatform_admin.ListAnalyticsAccountLinksRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_analytics_account_links_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = MarketingplatformAdminServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_analytics_account_links
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_analytics_account_links
        ] = mock_rpc
        request = {}
        client.list_analytics_account_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_analytics_account_links(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_analytics_account_links_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = MarketingplatformAdminServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_analytics_account_links
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_analytics_account_links
        ] = mock_rpc

        request = {}
        await client.list_analytics_account_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_analytics_account_links(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_analytics_account_links_async(
    transport: str = "grpc_asyncio",
    request_type=marketingplatform_admin.ListAnalyticsAccountLinksRequest,
):
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_analytics_account_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_analytics_account_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = marketingplatform_admin.ListAnalyticsAccountLinksRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAnalyticsAccountLinksAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_analytics_account_links_async_from_dict():
    await test_list_analytics_account_links_async(request_type=dict)


def test_list_analytics_account_links_field_headers():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = marketingplatform_admin.ListAnalyticsAccountLinksRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_analytics_account_links), "__call__"
    ) as call:
        call.return_value = marketingplatform_admin.ListAnalyticsAccountLinksResponse()
        client.list_analytics_account_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_analytics_account_links_field_headers_async():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = marketingplatform_admin.ListAnalyticsAccountLinksRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_analytics_account_links), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            marketingplatform_admin.ListAnalyticsAccountLinksResponse()
        )
        await client.list_analytics_account_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_analytics_account_links_flattened():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_analytics_account_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = marketingplatform_admin.ListAnalyticsAccountLinksResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_analytics_account_links(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_analytics_account_links_flattened_error():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_analytics_account_links(
            marketingplatform_admin.ListAnalyticsAccountLinksRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_analytics_account_links_flattened_async():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_analytics_account_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = marketingplatform_admin.ListAnalyticsAccountLinksResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            marketingplatform_admin.ListAnalyticsAccountLinksResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_analytics_account_links(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_analytics_account_links_flattened_error_async():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_analytics_account_links(
            marketingplatform_admin.ListAnalyticsAccountLinksRequest(),
            parent="parent_value",
        )


def test_list_analytics_account_links_pager(transport_name: str = "grpc"):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_analytics_account_links), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                analytics_account_links=[
                    resources.AnalyticsAccountLink(),
                    resources.AnalyticsAccountLink(),
                    resources.AnalyticsAccountLink(),
                ],
                next_page_token="abc",
            ),
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                analytics_account_links=[],
                next_page_token="def",
            ),
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                analytics_account_links=[
                    resources.AnalyticsAccountLink(),
                ],
                next_page_token="ghi",
            ),
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                analytics_account_links=[
                    resources.AnalyticsAccountLink(),
                    resources.AnalyticsAccountLink(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        expected_metadata = tuple(expected_metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_analytics_account_links(
            request={}, retry=retry, timeout=timeout
        )

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.AnalyticsAccountLink) for i in results)


def test_list_analytics_account_links_pages(transport_name: str = "grpc"):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_analytics_account_links), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                analytics_account_links=[
                    resources.AnalyticsAccountLink(),
                    resources.AnalyticsAccountLink(),
                    resources.AnalyticsAccountLink(),
                ],
                next_page_token="abc",
            ),
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                analytics_account_links=[],
                next_page_token="def",
            ),
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                analytics_account_links=[
                    resources.AnalyticsAccountLink(),
                ],
                next_page_token="ghi",
            ),
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                analytics_account_links=[
                    resources.AnalyticsAccountLink(),
                    resources.AnalyticsAccountLink(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_analytics_account_links(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_analytics_account_links_async_pager():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_analytics_account_links),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                analytics_account_links=[
                    resources.AnalyticsAccountLink(),
                    resources.AnalyticsAccountLink(),
                    resources.AnalyticsAccountLink(),
                ],
                next_page_token="abc",
            ),
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                analytics_account_links=[],
                next_page_token="def",
            ),
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                analytics_account_links=[
                    resources.AnalyticsAccountLink(),
                ],
                next_page_token="ghi",
            ),
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                analytics_account_links=[
                    resources.AnalyticsAccountLink(),
                    resources.AnalyticsAccountLink(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_analytics_account_links(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.AnalyticsAccountLink) for i in responses)


@pytest.mark.asyncio
async def test_list_analytics_account_links_async_pages():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_analytics_account_links),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                analytics_account_links=[
                    resources.AnalyticsAccountLink(),
                    resources.AnalyticsAccountLink(),
                    resources.AnalyticsAccountLink(),
                ],
                next_page_token="abc",
            ),
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                analytics_account_links=[],
                next_page_token="def",
            ),
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                analytics_account_links=[
                    resources.AnalyticsAccountLink(),
                ],
                next_page_token="ghi",
            ),
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                analytics_account_links=[
                    resources.AnalyticsAccountLink(),
                    resources.AnalyticsAccountLink(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_analytics_account_links(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        marketingplatform_admin.CreateAnalyticsAccountLinkRequest,
        dict,
    ],
)
def test_create_analytics_account_link(request_type, transport: str = "grpc"):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_analytics_account_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.AnalyticsAccountLink(
            name="name_value",
            analytics_account="analytics_account_value",
            display_name="display_name_value",
            link_verification_state=resources.LinkVerificationState.LINK_VERIFICATION_STATE_VERIFIED,
        )
        response = client.create_analytics_account_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = marketingplatform_admin.CreateAnalyticsAccountLinkRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.AnalyticsAccountLink)
    assert response.name == "name_value"
    assert response.analytics_account == "analytics_account_value"
    assert response.display_name == "display_name_value"
    assert (
        response.link_verification_state
        == resources.LinkVerificationState.LINK_VERIFICATION_STATE_VERIFIED
    )


def test_create_analytics_account_link_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = marketingplatform_admin.CreateAnalyticsAccountLinkRequest(
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_analytics_account_link), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_analytics_account_link(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == marketingplatform_admin.CreateAnalyticsAccountLinkRequest(
            parent="parent_value",
        )


def test_create_analytics_account_link_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = MarketingplatformAdminServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_analytics_account_link
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_analytics_account_link
        ] = mock_rpc
        request = {}
        client.create_analytics_account_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_analytics_account_link(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_analytics_account_link_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = MarketingplatformAdminServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_analytics_account_link
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_analytics_account_link
        ] = mock_rpc

        request = {}
        await client.create_analytics_account_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.create_analytics_account_link(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_analytics_account_link_async(
    transport: str = "grpc_asyncio",
    request_type=marketingplatform_admin.CreateAnalyticsAccountLinkRequest,
):
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_analytics_account_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.AnalyticsAccountLink(
                name="name_value",
                analytics_account="analytics_account_value",
                display_name="display_name_value",
                link_verification_state=resources.LinkVerificationState.LINK_VERIFICATION_STATE_VERIFIED,
            )
        )
        response = await client.create_analytics_account_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = marketingplatform_admin.CreateAnalyticsAccountLinkRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.AnalyticsAccountLink)
    assert response.name == "name_value"
    assert response.analytics_account == "analytics_account_value"
    assert response.display_name == "display_name_value"
    assert (
        response.link_verification_state
        == resources.LinkVerificationState.LINK_VERIFICATION_STATE_VERIFIED
    )


@pytest.mark.asyncio
async def test_create_analytics_account_link_async_from_dict():
    await test_create_analytics_account_link_async(request_type=dict)


def test_create_analytics_account_link_field_headers():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = marketingplatform_admin.CreateAnalyticsAccountLinkRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_analytics_account_link), "__call__"
    ) as call:
        call.return_value = resources.AnalyticsAccountLink()
        client.create_analytics_account_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_analytics_account_link_field_headers_async():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = marketingplatform_admin.CreateAnalyticsAccountLinkRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_analytics_account_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.AnalyticsAccountLink()
        )
        await client.create_analytics_account_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_analytics_account_link_flattened():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_analytics_account_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.AnalyticsAccountLink()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_analytics_account_link(
            parent="parent_value",
            analytics_account_link=resources.AnalyticsAccountLink(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].analytics_account_link
        mock_val = resources.AnalyticsAccountLink(name="name_value")
        assert arg == mock_val


def test_create_analytics_account_link_flattened_error():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_analytics_account_link(
            marketingplatform_admin.CreateAnalyticsAccountLinkRequest(),
            parent="parent_value",
            analytics_account_link=resources.AnalyticsAccountLink(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_analytics_account_link_flattened_async():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_analytics_account_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.AnalyticsAccountLink()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.AnalyticsAccountLink()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_analytics_account_link(
            parent="parent_value",
            analytics_account_link=resources.AnalyticsAccountLink(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].analytics_account_link
        mock_val = resources.AnalyticsAccountLink(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_analytics_account_link_flattened_error_async():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_analytics_account_link(
            marketingplatform_admin.CreateAnalyticsAccountLinkRequest(),
            parent="parent_value",
            analytics_account_link=resources.AnalyticsAccountLink(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        marketingplatform_admin.DeleteAnalyticsAccountLinkRequest,
        dict,
    ],
)
def test_delete_analytics_account_link(request_type, transport: str = "grpc"):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_analytics_account_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_analytics_account_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = marketingplatform_admin.DeleteAnalyticsAccountLinkRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_analytics_account_link_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = marketingplatform_admin.DeleteAnalyticsAccountLinkRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_analytics_account_link), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_analytics_account_link(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == marketingplatform_admin.DeleteAnalyticsAccountLinkRequest(
            name="name_value",
        )


def test_delete_analytics_account_link_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = MarketingplatformAdminServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_analytics_account_link
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_analytics_account_link
        ] = mock_rpc
        request = {}
        client.delete_analytics_account_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_analytics_account_link(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_analytics_account_link_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = MarketingplatformAdminServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_analytics_account_link
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_analytics_account_link
        ] = mock_rpc

        request = {}
        await client.delete_analytics_account_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.delete_analytics_account_link(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_analytics_account_link_async(
    transport: str = "grpc_asyncio",
    request_type=marketingplatform_admin.DeleteAnalyticsAccountLinkRequest,
):
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_analytics_account_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_analytics_account_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = marketingplatform_admin.DeleteAnalyticsAccountLinkRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_analytics_account_link_async_from_dict():
    await test_delete_analytics_account_link_async(request_type=dict)


def test_delete_analytics_account_link_field_headers():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = marketingplatform_admin.DeleteAnalyticsAccountLinkRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_analytics_account_link), "__call__"
    ) as call:
        call.return_value = None
        client.delete_analytics_account_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_analytics_account_link_field_headers_async():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = marketingplatform_admin.DeleteAnalyticsAccountLinkRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_analytics_account_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_analytics_account_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_analytics_account_link_flattened():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_analytics_account_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_analytics_account_link(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_analytics_account_link_flattened_error():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_analytics_account_link(
            marketingplatform_admin.DeleteAnalyticsAccountLinkRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_analytics_account_link_flattened_async():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_analytics_account_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_analytics_account_link(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_analytics_account_link_flattened_error_async():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_analytics_account_link(
            marketingplatform_admin.DeleteAnalyticsAccountLinkRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        marketingplatform_admin.SetPropertyServiceLevelRequest,
        dict,
    ],
)
def test_set_property_service_level(request_type, transport: str = "grpc"):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_property_service_level), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = marketingplatform_admin.SetPropertyServiceLevelResponse()
        response = client.set_property_service_level(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = marketingplatform_admin.SetPropertyServiceLevelRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, marketingplatform_admin.SetPropertyServiceLevelResponse)


def test_set_property_service_level_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = marketingplatform_admin.SetPropertyServiceLevelRequest(
        analytics_account_link="analytics_account_link_value",
        analytics_property="analytics_property_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_property_service_level), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.set_property_service_level(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == marketingplatform_admin.SetPropertyServiceLevelRequest(
            analytics_account_link="analytics_account_link_value",
            analytics_property="analytics_property_value",
        )


def test_set_property_service_level_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = MarketingplatformAdminServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.set_property_service_level
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.set_property_service_level
        ] = mock_rpc
        request = {}
        client.set_property_service_level(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.set_property_service_level(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_property_service_level_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = MarketingplatformAdminServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.set_property_service_level
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.set_property_service_level
        ] = mock_rpc

        request = {}
        await client.set_property_service_level(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.set_property_service_level(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_property_service_level_async(
    transport: str = "grpc_asyncio",
    request_type=marketingplatform_admin.SetPropertyServiceLevelRequest,
):
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_property_service_level), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            marketingplatform_admin.SetPropertyServiceLevelResponse()
        )
        response = await client.set_property_service_level(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = marketingplatform_admin.SetPropertyServiceLevelRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, marketingplatform_admin.SetPropertyServiceLevelResponse)


@pytest.mark.asyncio
async def test_set_property_service_level_async_from_dict():
    await test_set_property_service_level_async(request_type=dict)


def test_set_property_service_level_field_headers():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = marketingplatform_admin.SetPropertyServiceLevelRequest()

    request.analytics_account_link = "analytics_account_link_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_property_service_level), "__call__"
    ) as call:
        call.return_value = marketingplatform_admin.SetPropertyServiceLevelResponse()
        client.set_property_service_level(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "analytics_account_link=analytics_account_link_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_property_service_level_field_headers_async():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = marketingplatform_admin.SetPropertyServiceLevelRequest()

    request.analytics_account_link = "analytics_account_link_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_property_service_level), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            marketingplatform_admin.SetPropertyServiceLevelResponse()
        )
        await client.set_property_service_level(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "analytics_account_link=analytics_account_link_value",
    ) in kw["metadata"]


def test_set_property_service_level_flattened():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_property_service_level), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = marketingplatform_admin.SetPropertyServiceLevelResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_property_service_level(
            analytics_account_link="analytics_account_link_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].analytics_account_link
        mock_val = "analytics_account_link_value"
        assert arg == mock_val


def test_set_property_service_level_flattened_error():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_property_service_level(
            marketingplatform_admin.SetPropertyServiceLevelRequest(),
            analytics_account_link="analytics_account_link_value",
        )


@pytest.mark.asyncio
async def test_set_property_service_level_flattened_async():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_property_service_level), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = marketingplatform_admin.SetPropertyServiceLevelResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            marketingplatform_admin.SetPropertyServiceLevelResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_property_service_level(
            analytics_account_link="analytics_account_link_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].analytics_account_link
        mock_val = "analytics_account_link_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_set_property_service_level_flattened_error_async():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_property_service_level(
            marketingplatform_admin.SetPropertyServiceLevelRequest(),
            analytics_account_link="analytics_account_link_value",
        )


def test_get_organization_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = MarketingplatformAdminServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_organization in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_organization
        ] = mock_rpc

        request = {}
        client.get_organization(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_organization(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_organization_rest_required_fields(
    request_type=marketingplatform_admin.GetOrganizationRequest,
):
    transport_class = transports.MarketingplatformAdminServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_organization._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_organization._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.Organization()
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
            return_value = resources.Organization.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_organization(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_organization_rest_unset_required_fields():
    transport = transports.MarketingplatformAdminServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_organization._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_get_organization_rest_flattened():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.Organization()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "organizations/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.Organization.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_organization(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{name=organizations/*}" % client.transport._host, args[1]
        )


def test_get_organization_rest_flattened_error(transport: str = "rest"):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_organization(
            marketingplatform_admin.GetOrganizationRequest(),
            name="name_value",
        )


def test_list_analytics_account_links_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = MarketingplatformAdminServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_analytics_account_links
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_analytics_account_links
        ] = mock_rpc

        request = {}
        client.list_analytics_account_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_analytics_account_links(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_analytics_account_links_rest_required_fields(
    request_type=marketingplatform_admin.ListAnalyticsAccountLinksRequest,
):
    transport_class = transports.MarketingplatformAdminServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_analytics_account_links._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_analytics_account_links._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = marketingplatform_admin.ListAnalyticsAccountLinksResponse()
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
            return_value = marketingplatform_admin.ListAnalyticsAccountLinksResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_analytics_account_links(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_analytics_account_links_rest_unset_required_fields():
    transport = transports.MarketingplatformAdminServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_analytics_account_links._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


def test_list_analytics_account_links_rest_flattened():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = marketingplatform_admin.ListAnalyticsAccountLinksResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "organizations/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = marketingplatform_admin.ListAnalyticsAccountLinksResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_analytics_account_links(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{parent=organizations/*}/analyticsAccountLinks"
            % client.transport._host,
            args[1],
        )


def test_list_analytics_account_links_rest_flattened_error(transport: str = "rest"):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_analytics_account_links(
            marketingplatform_admin.ListAnalyticsAccountLinksRequest(),
            parent="parent_value",
        )


def test_list_analytics_account_links_rest_pager(transport: str = "rest"):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                analytics_account_links=[
                    resources.AnalyticsAccountLink(),
                    resources.AnalyticsAccountLink(),
                    resources.AnalyticsAccountLink(),
                ],
                next_page_token="abc",
            ),
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                analytics_account_links=[],
                next_page_token="def",
            ),
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                analytics_account_links=[
                    resources.AnalyticsAccountLink(),
                ],
                next_page_token="ghi",
            ),
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                analytics_account_links=[
                    resources.AnalyticsAccountLink(),
                    resources.AnalyticsAccountLink(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            marketingplatform_admin.ListAnalyticsAccountLinksResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "organizations/sample1"}

        pager = client.list_analytics_account_links(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.AnalyticsAccountLink) for i in results)

        pages = list(client.list_analytics_account_links(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_create_analytics_account_link_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = MarketingplatformAdminServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_analytics_account_link
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_analytics_account_link
        ] = mock_rpc

        request = {}
        client.create_analytics_account_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_analytics_account_link(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_analytics_account_link_rest_required_fields(
    request_type=marketingplatform_admin.CreateAnalyticsAccountLinkRequest,
):
    transport_class = transports.MarketingplatformAdminServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_analytics_account_link._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_analytics_account_link._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.AnalyticsAccountLink()
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
            return_value = resources.AnalyticsAccountLink.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_analytics_account_link(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_analytics_account_link_rest_unset_required_fields():
    transport = transports.MarketingplatformAdminServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_analytics_account_link._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "analyticsAccountLink",
            )
        )
    )


def test_create_analytics_account_link_rest_flattened():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.AnalyticsAccountLink()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "organizations/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            analytics_account_link=resources.AnalyticsAccountLink(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.AnalyticsAccountLink.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_analytics_account_link(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{parent=organizations/*}/analyticsAccountLinks"
            % client.transport._host,
            args[1],
        )


def test_create_analytics_account_link_rest_flattened_error(transport: str = "rest"):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_analytics_account_link(
            marketingplatform_admin.CreateAnalyticsAccountLinkRequest(),
            parent="parent_value",
            analytics_account_link=resources.AnalyticsAccountLink(name="name_value"),
        )


def test_delete_analytics_account_link_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = MarketingplatformAdminServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_analytics_account_link
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_analytics_account_link
        ] = mock_rpc

        request = {}
        client.delete_analytics_account_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_analytics_account_link(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_analytics_account_link_rest_required_fields(
    request_type=marketingplatform_admin.DeleteAnalyticsAccountLinkRequest,
):
    transport_class = transports.MarketingplatformAdminServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_analytics_account_link._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_analytics_account_link._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
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
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_analytics_account_link(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_analytics_account_link_rest_unset_required_fields():
    transport = transports.MarketingplatformAdminServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_analytics_account_link._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_delete_analytics_account_link_rest_flattened():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "organizations/sample1/analyticsAccountLinks/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_analytics_account_link(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{name=organizations/*/analyticsAccountLinks/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_analytics_account_link_rest_flattened_error(transport: str = "rest"):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_analytics_account_link(
            marketingplatform_admin.DeleteAnalyticsAccountLinkRequest(),
            name="name_value",
        )


def test_set_property_service_level_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = MarketingplatformAdminServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.set_property_service_level
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.set_property_service_level
        ] = mock_rpc

        request = {}
        client.set_property_service_level(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.set_property_service_level(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_set_property_service_level_rest_required_fields(
    request_type=marketingplatform_admin.SetPropertyServiceLevelRequest,
):
    transport_class = transports.MarketingplatformAdminServiceRestTransport

    request_init = {}
    request_init["analytics_account_link"] = ""
    request_init["analytics_property"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).set_property_service_level._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["analyticsAccountLink"] = "analytics_account_link_value"
    jsonified_request["analyticsProperty"] = "analytics_property_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).set_property_service_level._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "analyticsAccountLink" in jsonified_request
    assert jsonified_request["analyticsAccountLink"] == "analytics_account_link_value"
    assert "analyticsProperty" in jsonified_request
    assert jsonified_request["analyticsProperty"] == "analytics_property_value"

    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = marketingplatform_admin.SetPropertyServiceLevelResponse()
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
            return_value = marketingplatform_admin.SetPropertyServiceLevelResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.set_property_service_level(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_set_property_service_level_rest_unset_required_fields():
    transport = transports.MarketingplatformAdminServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.set_property_service_level._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "analyticsAccountLink",
                "analyticsProperty",
                "serviceLevel",
            )
        )
    )


def test_set_property_service_level_rest_flattened():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = marketingplatform_admin.SetPropertyServiceLevelResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "analytics_account_link": "organizations/sample1/analyticsAccountLinks/sample2"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            analytics_account_link="analytics_account_link_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = marketingplatform_admin.SetPropertyServiceLevelResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.set_property_service_level(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{analytics_account_link=organizations/*/analyticsAccountLinks/*}:setPropertyServiceLevel"
            % client.transport._host,
            args[1],
        )


def test_set_property_service_level_rest_flattened_error(transport: str = "rest"):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_property_service_level(
            marketingplatform_admin.SetPropertyServiceLevelRequest(),
            analytics_account_link="analytics_account_link_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.MarketingplatformAdminServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = MarketingplatformAdminServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.MarketingplatformAdminServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = MarketingplatformAdminServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.MarketingplatformAdminServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = MarketingplatformAdminServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = MarketingplatformAdminServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.MarketingplatformAdminServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = MarketingplatformAdminServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.MarketingplatformAdminServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = MarketingplatformAdminServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.MarketingplatformAdminServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.MarketingplatformAdminServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MarketingplatformAdminServiceGrpcTransport,
        transports.MarketingplatformAdminServiceGrpcAsyncIOTransport,
        transports.MarketingplatformAdminServiceRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_kind_grpc():
    transport = MarketingplatformAdminServiceClient.get_transport_class("grpc")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "grpc"


def test_initialize_client_w_grpc():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_organization_empty_call_grpc():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_organization), "__call__") as call:
        call.return_value = resources.Organization()
        client.get_organization(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = marketingplatform_admin.GetOrganizationRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_analytics_account_links_empty_call_grpc():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_analytics_account_links), "__call__"
    ) as call:
        call.return_value = marketingplatform_admin.ListAnalyticsAccountLinksResponse()
        client.list_analytics_account_links(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = marketingplatform_admin.ListAnalyticsAccountLinksRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_analytics_account_link_empty_call_grpc():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_analytics_account_link), "__call__"
    ) as call:
        call.return_value = resources.AnalyticsAccountLink()
        client.create_analytics_account_link(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = marketingplatform_admin.CreateAnalyticsAccountLinkRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_analytics_account_link_empty_call_grpc():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_analytics_account_link), "__call__"
    ) as call:
        call.return_value = None
        client.delete_analytics_account_link(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = marketingplatform_admin.DeleteAnalyticsAccountLinkRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_set_property_service_level_empty_call_grpc():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.set_property_service_level), "__call__"
    ) as call:
        call.return_value = marketingplatform_admin.SetPropertyServiceLevelResponse()
        client.set_property_service_level(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = marketingplatform_admin.SetPropertyServiceLevelRequest()

        assert args[0] == request_msg


def test_transport_kind_grpc_asyncio():
    transport = MarketingplatformAdminServiceAsyncClient.get_transport_class(
        "grpc_asyncio"
    )(credentials=async_anonymous_credentials())
    assert transport.kind == "grpc_asyncio"


def test_initialize_client_w_grpc_asyncio():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_organization_empty_call_grpc_asyncio():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_organization), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Organization(
                name="name_value",
                display_name="display_name_value",
            )
        )
        await client.get_organization(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = marketingplatform_admin.GetOrganizationRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_analytics_account_links_empty_call_grpc_asyncio():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_analytics_account_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            marketingplatform_admin.ListAnalyticsAccountLinksResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_analytics_account_links(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = marketingplatform_admin.ListAnalyticsAccountLinksRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_analytics_account_link_empty_call_grpc_asyncio():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_analytics_account_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.AnalyticsAccountLink(
                name="name_value",
                analytics_account="analytics_account_value",
                display_name="display_name_value",
                link_verification_state=resources.LinkVerificationState.LINK_VERIFICATION_STATE_VERIFIED,
            )
        )
        await client.create_analytics_account_link(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = marketingplatform_admin.CreateAnalyticsAccountLinkRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_delete_analytics_account_link_empty_call_grpc_asyncio():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_analytics_account_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_analytics_account_link(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = marketingplatform_admin.DeleteAnalyticsAccountLinkRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_set_property_service_level_empty_call_grpc_asyncio():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.set_property_service_level), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            marketingplatform_admin.SetPropertyServiceLevelResponse()
        )
        await client.set_property_service_level(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = marketingplatform_admin.SetPropertyServiceLevelRequest()

        assert args[0] == request_msg


def test_transport_kind_rest():
    transport = MarketingplatformAdminServiceClient.get_transport_class("rest")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "rest"


def test_get_organization_rest_bad_request(
    request_type=marketingplatform_admin.GetOrganizationRequest,
):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"name": "organizations/sample1"}
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
        client.get_organization(request)


@pytest.mark.parametrize(
    "request_type",
    [
        marketingplatform_admin.GetOrganizationRequest,
        dict,
    ],
)
def test_get_organization_rest_call_success(request_type):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "organizations/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.Organization(
            name="name_value",
            display_name="display_name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = resources.Organization.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_organization(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Organization)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_organization_rest_interceptors(null_interceptor):
    transport = transports.MarketingplatformAdminServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MarketingplatformAdminServiceRestInterceptor(),
    )
    client = MarketingplatformAdminServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MarketingplatformAdminServiceRestInterceptor, "post_get_organization"
    ) as post, mock.patch.object(
        transports.MarketingplatformAdminServiceRestInterceptor, "pre_get_organization"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = marketingplatform_admin.GetOrganizationRequest.pb(
            marketingplatform_admin.GetOrganizationRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = resources.Organization.to_json(resources.Organization())
        req.return_value.content = return_value

        request = marketingplatform_admin.GetOrganizationRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.Organization()

        client.get_organization(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_analytics_account_links_rest_bad_request(
    request_type=marketingplatform_admin.ListAnalyticsAccountLinksRequest,
):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "organizations/sample1"}
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
        client.list_analytics_account_links(request)


@pytest.mark.parametrize(
    "request_type",
    [
        marketingplatform_admin.ListAnalyticsAccountLinksRequest,
        dict,
    ],
)
def test_list_analytics_account_links_rest_call_success(request_type):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "organizations/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = marketingplatform_admin.ListAnalyticsAccountLinksResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = marketingplatform_admin.ListAnalyticsAccountLinksResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_analytics_account_links(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAnalyticsAccountLinksPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_analytics_account_links_rest_interceptors(null_interceptor):
    transport = transports.MarketingplatformAdminServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MarketingplatformAdminServiceRestInterceptor(),
    )
    client = MarketingplatformAdminServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MarketingplatformAdminServiceRestInterceptor,
        "post_list_analytics_account_links",
    ) as post, mock.patch.object(
        transports.MarketingplatformAdminServiceRestInterceptor,
        "pre_list_analytics_account_links",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = marketingplatform_admin.ListAnalyticsAccountLinksRequest.pb(
            marketingplatform_admin.ListAnalyticsAccountLinksRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = (
            marketingplatform_admin.ListAnalyticsAccountLinksResponse.to_json(
                marketingplatform_admin.ListAnalyticsAccountLinksResponse()
            )
        )
        req.return_value.content = return_value

        request = marketingplatform_admin.ListAnalyticsAccountLinksRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = marketingplatform_admin.ListAnalyticsAccountLinksResponse()

        client.list_analytics_account_links(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_analytics_account_link_rest_bad_request(
    request_type=marketingplatform_admin.CreateAnalyticsAccountLinkRequest,
):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "organizations/sample1"}
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
        client.create_analytics_account_link(request)


@pytest.mark.parametrize(
    "request_type",
    [
        marketingplatform_admin.CreateAnalyticsAccountLinkRequest,
        dict,
    ],
)
def test_create_analytics_account_link_rest_call_success(request_type):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "organizations/sample1"}
    request_init["analytics_account_link"] = {
        "name": "name_value",
        "analytics_account": "analytics_account_value",
        "display_name": "display_name_value",
        "link_verification_state": 1,
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = marketingplatform_admin.CreateAnalyticsAccountLinkRequest.meta.fields[
        "analytics_account_link"
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
        "analytics_account_link"
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
                for i in range(0, len(request_init["analytics_account_link"][field])):
                    del request_init["analytics_account_link"][field][i][subfield]
            else:
                del request_init["analytics_account_link"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.AnalyticsAccountLink(
            name="name_value",
            analytics_account="analytics_account_value",
            display_name="display_name_value",
            link_verification_state=resources.LinkVerificationState.LINK_VERIFICATION_STATE_VERIFIED,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = resources.AnalyticsAccountLink.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_analytics_account_link(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.AnalyticsAccountLink)
    assert response.name == "name_value"
    assert response.analytics_account == "analytics_account_value"
    assert response.display_name == "display_name_value"
    assert (
        response.link_verification_state
        == resources.LinkVerificationState.LINK_VERIFICATION_STATE_VERIFIED
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_analytics_account_link_rest_interceptors(null_interceptor):
    transport = transports.MarketingplatformAdminServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MarketingplatformAdminServiceRestInterceptor(),
    )
    client = MarketingplatformAdminServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MarketingplatformAdminServiceRestInterceptor,
        "post_create_analytics_account_link",
    ) as post, mock.patch.object(
        transports.MarketingplatformAdminServiceRestInterceptor,
        "pre_create_analytics_account_link",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = marketingplatform_admin.CreateAnalyticsAccountLinkRequest.pb(
            marketingplatform_admin.CreateAnalyticsAccountLinkRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = resources.AnalyticsAccountLink.to_json(
            resources.AnalyticsAccountLink()
        )
        req.return_value.content = return_value

        request = marketingplatform_admin.CreateAnalyticsAccountLinkRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.AnalyticsAccountLink()

        client.create_analytics_account_link(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_analytics_account_link_rest_bad_request(
    request_type=marketingplatform_admin.DeleteAnalyticsAccountLinkRequest,
):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"name": "organizations/sample1/analyticsAccountLinks/sample2"}
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
        client.delete_analytics_account_link(request)


@pytest.mark.parametrize(
    "request_type",
    [
        marketingplatform_admin.DeleteAnalyticsAccountLinkRequest,
        dict,
    ],
)
def test_delete_analytics_account_link_rest_call_success(request_type):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "organizations/sample1/analyticsAccountLinks/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = ""
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_analytics_account_link(request)

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_analytics_account_link_rest_interceptors(null_interceptor):
    transport = transports.MarketingplatformAdminServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MarketingplatformAdminServiceRestInterceptor(),
    )
    client = MarketingplatformAdminServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MarketingplatformAdminServiceRestInterceptor,
        "pre_delete_analytics_account_link",
    ) as pre:
        pre.assert_not_called()
        pb_message = marketingplatform_admin.DeleteAnalyticsAccountLinkRequest.pb(
            marketingplatform_admin.DeleteAnalyticsAccountLinkRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200

        request = marketingplatform_admin.DeleteAnalyticsAccountLinkRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_analytics_account_link(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_set_property_service_level_rest_bad_request(
    request_type=marketingplatform_admin.SetPropertyServiceLevelRequest,
):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "analytics_account_link": "organizations/sample1/analyticsAccountLinks/sample2"
    }
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
        client.set_property_service_level(request)


@pytest.mark.parametrize(
    "request_type",
    [
        marketingplatform_admin.SetPropertyServiceLevelRequest,
        dict,
    ],
)
def test_set_property_service_level_rest_call_success(request_type):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "analytics_account_link": "organizations/sample1/analyticsAccountLinks/sample2"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = marketingplatform_admin.SetPropertyServiceLevelResponse()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = marketingplatform_admin.SetPropertyServiceLevelResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_property_service_level(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, marketingplatform_admin.SetPropertyServiceLevelResponse)


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_set_property_service_level_rest_interceptors(null_interceptor):
    transport = transports.MarketingplatformAdminServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MarketingplatformAdminServiceRestInterceptor(),
    )
    client = MarketingplatformAdminServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MarketingplatformAdminServiceRestInterceptor,
        "post_set_property_service_level",
    ) as post, mock.patch.object(
        transports.MarketingplatformAdminServiceRestInterceptor,
        "pre_set_property_service_level",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = marketingplatform_admin.SetPropertyServiceLevelRequest.pb(
            marketingplatform_admin.SetPropertyServiceLevelRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = marketingplatform_admin.SetPropertyServiceLevelResponse.to_json(
            marketingplatform_admin.SetPropertyServiceLevelResponse()
        )
        req.return_value.content = return_value

        request = marketingplatform_admin.SetPropertyServiceLevelRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = marketingplatform_admin.SetPropertyServiceLevelResponse()

        client.set_property_service_level(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_initialize_client_w_rest():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_organization_empty_call_rest():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_organization), "__call__") as call:
        client.get_organization(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = marketingplatform_admin.GetOrganizationRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_analytics_account_links_empty_call_rest():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_analytics_account_links), "__call__"
    ) as call:
        client.list_analytics_account_links(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = marketingplatform_admin.ListAnalyticsAccountLinksRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_analytics_account_link_empty_call_rest():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_analytics_account_link), "__call__"
    ) as call:
        client.create_analytics_account_link(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = marketingplatform_admin.CreateAnalyticsAccountLinkRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_analytics_account_link_empty_call_rest():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_analytics_account_link), "__call__"
    ) as call:
        client.delete_analytics_account_link(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = marketingplatform_admin.DeleteAnalyticsAccountLinkRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_set_property_service_level_empty_call_rest():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.set_property_service_level), "__call__"
    ) as call:
        client.set_property_service_level(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = marketingplatform_admin.SetPropertyServiceLevelRequest()

        assert args[0] == request_msg


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.MarketingplatformAdminServiceGrpcTransport,
    )


def test_marketingplatform_admin_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.MarketingplatformAdminServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_marketingplatform_admin_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.ads.marketingplatform_admin_v1alpha.services.marketingplatform_admin_service.transports.MarketingplatformAdminServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.MarketingplatformAdminServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "get_organization",
        "list_analytics_account_links",
        "create_analytics_account_link",
        "delete_analytics_account_link",
        "set_property_service_level",
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


def test_marketingplatform_admin_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.ads.marketingplatform_admin_v1alpha.services.marketingplatform_admin_service.transports.MarketingplatformAdminServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.MarketingplatformAdminServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/marketingplatformadmin.analytics.read",
                "https://www.googleapis.com/auth/marketingplatformadmin.analytics.update",
            ),
            quota_project_id="octopus",
        )


def test_marketingplatform_admin_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.ads.marketingplatform_admin_v1alpha.services.marketingplatform_admin_service.transports.MarketingplatformAdminServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.MarketingplatformAdminServiceTransport()
        adc.assert_called_once()


def test_marketingplatform_admin_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        MarketingplatformAdminServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/marketingplatformadmin.analytics.read",
                "https://www.googleapis.com/auth/marketingplatformadmin.analytics.update",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MarketingplatformAdminServiceGrpcTransport,
        transports.MarketingplatformAdminServiceGrpcAsyncIOTransport,
    ],
)
def test_marketingplatform_admin_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/marketingplatformadmin.analytics.read",
                "https://www.googleapis.com/auth/marketingplatformadmin.analytics.update",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MarketingplatformAdminServiceGrpcTransport,
        transports.MarketingplatformAdminServiceGrpcAsyncIOTransport,
        transports.MarketingplatformAdminServiceRestTransport,
    ],
)
def test_marketingplatform_admin_service_transport_auth_gdch_credentials(
    transport_class,
):
    host = "https://language.com"
    api_audience_tests = [None, "https://language2.com"]
    api_audience_expect = [host, "https://language2.com"]
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, "default", autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(
                return_value=gdch_mock
            )
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(e)


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.MarketingplatformAdminServiceGrpcTransport, grpc_helpers),
        (
            transports.MarketingplatformAdminServiceGrpcAsyncIOTransport,
            grpc_helpers_async,
        ),
    ],
)
def test_marketingplatform_admin_service_transport_create_channel(
    transport_class, grpc_helpers
):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "marketingplatformadmin.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/marketingplatformadmin.analytics.read",
                "https://www.googleapis.com/auth/marketingplatformadmin.analytics.update",
            ),
            scopes=["1", "2"],
            default_host="marketingplatformadmin.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MarketingplatformAdminServiceGrpcTransport,
        transports.MarketingplatformAdminServiceGrpcAsyncIOTransport,
    ],
)
def test_marketingplatform_admin_service_grpc_transport_client_cert_source_for_mtls(
    transport_class,
):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


def test_marketingplatform_admin_service_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.MarketingplatformAdminServiceRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_marketingplatform_admin_service_host_no_port(transport_name):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="marketingplatformadmin.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "marketingplatformadmin.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://marketingplatformadmin.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_marketingplatform_admin_service_host_with_port(transport_name):
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="marketingplatformadmin.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "marketingplatformadmin.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://marketingplatformadmin.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_marketingplatform_admin_service_client_transport_session_collision(
    transport_name,
):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = MarketingplatformAdminServiceClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = MarketingplatformAdminServiceClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.get_organization._session
    session2 = client2.transport.get_organization._session
    assert session1 != session2
    session1 = client1.transport.list_analytics_account_links._session
    session2 = client2.transport.list_analytics_account_links._session
    assert session1 != session2
    session1 = client1.transport.create_analytics_account_link._session
    session2 = client2.transport.create_analytics_account_link._session
    assert session1 != session2
    session1 = client1.transport.delete_analytics_account_link._session
    session2 = client2.transport.delete_analytics_account_link._session
    assert session1 != session2
    session1 = client1.transport.set_property_service_level._session
    session2 = client2.transport.set_property_service_level._session
    assert session1 != session2


def test_marketingplatform_admin_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.MarketingplatformAdminServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_marketingplatform_admin_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.MarketingplatformAdminServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MarketingplatformAdminServiceGrpcTransport,
        transports.MarketingplatformAdminServiceGrpcAsyncIOTransport,
    ],
)
def test_marketingplatform_admin_service_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MarketingplatformAdminServiceGrpcTransport,
        transports.MarketingplatformAdminServiceGrpcAsyncIOTransport,
    ],
)
def test_marketingplatform_admin_service_transport_channel_mtls_with_adc(
    transport_class,
):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_account_path():
    account = "squid"
    expected = "accounts/{account}".format(
        account=account,
    )
    actual = MarketingplatformAdminServiceClient.account_path(account)
    assert expected == actual


def test_parse_account_path():
    expected = {
        "account": "clam",
    }
    path = MarketingplatformAdminServiceClient.account_path(**expected)

    # Check that the path construction is reversible.
    actual = MarketingplatformAdminServiceClient.parse_account_path(path)
    assert expected == actual


def test_analytics_account_link_path():
    organization = "whelk"
    analytics_account_link = "octopus"
    expected = "organizations/{organization}/analyticsAccountLinks/{analytics_account_link}".format(
        organization=organization,
        analytics_account_link=analytics_account_link,
    )
    actual = MarketingplatformAdminServiceClient.analytics_account_link_path(
        organization, analytics_account_link
    )
    assert expected == actual


def test_parse_analytics_account_link_path():
    expected = {
        "organization": "oyster",
        "analytics_account_link": "nudibranch",
    }
    path = MarketingplatformAdminServiceClient.analytics_account_link_path(**expected)

    # Check that the path construction is reversible.
    actual = MarketingplatformAdminServiceClient.parse_analytics_account_link_path(path)
    assert expected == actual


def test_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = MarketingplatformAdminServiceClient.organization_path(organization)
    assert expected == actual


def test_parse_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = MarketingplatformAdminServiceClient.organization_path(**expected)

    # Check that the path construction is reversible.
    actual = MarketingplatformAdminServiceClient.parse_organization_path(path)
    assert expected == actual


def test_property_path():
    property = "winkle"
    expected = "properties/{property}".format(
        property=property,
    )
    actual = MarketingplatformAdminServiceClient.property_path(property)
    assert expected == actual


def test_parse_property_path():
    expected = {
        "property": "nautilus",
    }
    path = MarketingplatformAdminServiceClient.property_path(**expected)

    # Check that the path construction is reversible.
    actual = MarketingplatformAdminServiceClient.parse_property_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "scallop"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = MarketingplatformAdminServiceClient.common_billing_account_path(
        billing_account
    )
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "abalone",
    }
    path = MarketingplatformAdminServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = MarketingplatformAdminServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "squid"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = MarketingplatformAdminServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "clam",
    }
    path = MarketingplatformAdminServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = MarketingplatformAdminServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "whelk"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = MarketingplatformAdminServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "octopus",
    }
    path = MarketingplatformAdminServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = MarketingplatformAdminServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "oyster"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = MarketingplatformAdminServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nudibranch",
    }
    path = MarketingplatformAdminServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = MarketingplatformAdminServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "cuttlefish"
    location = "mussel"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = MarketingplatformAdminServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
    }
    path = MarketingplatformAdminServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = MarketingplatformAdminServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.MarketingplatformAdminServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = MarketingplatformAdminServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.MarketingplatformAdminServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = MarketingplatformAdminServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_transport_close_grpc():
    client = MarketingplatformAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_grpc_channel")), "close"
    ) as close:
        with client:
            close.assert_not_called()
        close.assert_called_once()


@pytest.mark.asyncio
async def test_transport_close_grpc_asyncio():
    client = MarketingplatformAdminServiceAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close_rest():
    client = MarketingplatformAdminServiceClient(
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
        "grpc",
    ]
    for transport in transports:
        client = MarketingplatformAdminServiceClient(
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
        (
            MarketingplatformAdminServiceClient,
            transports.MarketingplatformAdminServiceGrpcTransport,
        ),
        (
            MarketingplatformAdminServiceAsyncClient,
            transports.MarketingplatformAdminServiceGrpcAsyncIOTransport,
        ),
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
