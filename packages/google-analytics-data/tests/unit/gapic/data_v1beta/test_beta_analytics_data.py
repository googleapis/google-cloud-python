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

from collections.abc import Iterable
import json
import math

from google.api_core import (
    future,
    gapic_v1,
    grpc_helpers,
    grpc_helpers_async,
    operation,
    operations_v1,
    path_template,
)
from google.api_core import api_core_version, client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import operation_async  # type: ignore
from google.api_core import retry as retries
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import json_format
from google.protobuf import timestamp_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.analytics.data_v1beta.services.beta_analytics_data import (
    BetaAnalyticsDataAsyncClient,
    BetaAnalyticsDataClient,
    pagers,
    transports,
)
from google.analytics.data_v1beta.types import analytics_data_api, data


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


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

    assert BetaAnalyticsDataClient._get_default_mtls_endpoint(None) is None
    assert (
        BetaAnalyticsDataClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        BetaAnalyticsDataClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        BetaAnalyticsDataClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        BetaAnalyticsDataClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        BetaAnalyticsDataClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


def test__read_environment_variables():
    assert BetaAnalyticsDataClient._read_environment_variables() == (
        False,
        "auto",
        None,
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert BetaAnalyticsDataClient._read_environment_variables() == (
            True,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert BetaAnalyticsDataClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            BetaAnalyticsDataClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert BetaAnalyticsDataClient._read_environment_variables() == (
            False,
            "never",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert BetaAnalyticsDataClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert BetaAnalyticsDataClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            BetaAnalyticsDataClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert BetaAnalyticsDataClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert BetaAnalyticsDataClient._get_client_cert_source(None, False) is None
    assert (
        BetaAnalyticsDataClient._get_client_cert_source(
            mock_provided_cert_source, False
        )
        is None
    )
    assert (
        BetaAnalyticsDataClient._get_client_cert_source(mock_provided_cert_source, True)
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
                BetaAnalyticsDataClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                BetaAnalyticsDataClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    BetaAnalyticsDataClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(BetaAnalyticsDataClient),
)
@mock.patch.object(
    BetaAnalyticsDataAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(BetaAnalyticsDataAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = BetaAnalyticsDataClient._DEFAULT_UNIVERSE
    default_endpoint = BetaAnalyticsDataClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = BetaAnalyticsDataClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        BetaAnalyticsDataClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        BetaAnalyticsDataClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == BetaAnalyticsDataClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        BetaAnalyticsDataClient._get_api_endpoint(None, None, default_universe, "auto")
        == default_endpoint
    )
    assert (
        BetaAnalyticsDataClient._get_api_endpoint(
            None, None, default_universe, "always"
        )
        == BetaAnalyticsDataClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        BetaAnalyticsDataClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == BetaAnalyticsDataClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        BetaAnalyticsDataClient._get_api_endpoint(None, None, mock_universe, "never")
        == mock_endpoint
    )
    assert (
        BetaAnalyticsDataClient._get_api_endpoint(None, None, default_universe, "never")
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        BetaAnalyticsDataClient._get_api_endpoint(
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
        BetaAnalyticsDataClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        BetaAnalyticsDataClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        BetaAnalyticsDataClient._get_universe_domain(None, None)
        == BetaAnalyticsDataClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        BetaAnalyticsDataClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (BetaAnalyticsDataClient, transports.BetaAnalyticsDataGrpcTransport, "grpc"),
        (BetaAnalyticsDataClient, transports.BetaAnalyticsDataRestTransport, "rest"),
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
        (BetaAnalyticsDataClient, "grpc"),
        (BetaAnalyticsDataAsyncClient, "grpc_asyncio"),
        (BetaAnalyticsDataClient, "rest"),
    ],
)
def test_beta_analytics_data_client_from_service_account_info(
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
            "analyticsdata.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://analyticsdata.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.BetaAnalyticsDataGrpcTransport, "grpc"),
        (transports.BetaAnalyticsDataGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.BetaAnalyticsDataRestTransport, "rest"),
    ],
)
def test_beta_analytics_data_client_service_account_always_use_jwt(
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
        (BetaAnalyticsDataClient, "grpc"),
        (BetaAnalyticsDataAsyncClient, "grpc_asyncio"),
        (BetaAnalyticsDataClient, "rest"),
    ],
)
def test_beta_analytics_data_client_from_service_account_file(
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
            "analyticsdata.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://analyticsdata.googleapis.com"
        )


def test_beta_analytics_data_client_get_transport_class():
    transport = BetaAnalyticsDataClient.get_transport_class()
    available_transports = [
        transports.BetaAnalyticsDataGrpcTransport,
        transports.BetaAnalyticsDataRestTransport,
    ]
    assert transport in available_transports

    transport = BetaAnalyticsDataClient.get_transport_class("grpc")
    assert transport == transports.BetaAnalyticsDataGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (BetaAnalyticsDataClient, transports.BetaAnalyticsDataGrpcTransport, "grpc"),
        (
            BetaAnalyticsDataAsyncClient,
            transports.BetaAnalyticsDataGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (BetaAnalyticsDataClient, transports.BetaAnalyticsDataRestTransport, "rest"),
    ],
)
@mock.patch.object(
    BetaAnalyticsDataClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(BetaAnalyticsDataClient),
)
@mock.patch.object(
    BetaAnalyticsDataAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(BetaAnalyticsDataAsyncClient),
)
def test_beta_analytics_data_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(BetaAnalyticsDataClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(BetaAnalyticsDataClient, "get_transport_class") as gtc:
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
            BetaAnalyticsDataClient,
            transports.BetaAnalyticsDataGrpcTransport,
            "grpc",
            "true",
        ),
        (
            BetaAnalyticsDataAsyncClient,
            transports.BetaAnalyticsDataGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            BetaAnalyticsDataClient,
            transports.BetaAnalyticsDataGrpcTransport,
            "grpc",
            "false",
        ),
        (
            BetaAnalyticsDataAsyncClient,
            transports.BetaAnalyticsDataGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            BetaAnalyticsDataClient,
            transports.BetaAnalyticsDataRestTransport,
            "rest",
            "true",
        ),
        (
            BetaAnalyticsDataClient,
            transports.BetaAnalyticsDataRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    BetaAnalyticsDataClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(BetaAnalyticsDataClient),
)
@mock.patch.object(
    BetaAnalyticsDataAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(BetaAnalyticsDataAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_beta_analytics_data_client_mtls_env_auto(
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
    "client_class", [BetaAnalyticsDataClient, BetaAnalyticsDataAsyncClient]
)
@mock.patch.object(
    BetaAnalyticsDataClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BetaAnalyticsDataClient),
)
@mock.patch.object(
    BetaAnalyticsDataAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BetaAnalyticsDataAsyncClient),
)
def test_beta_analytics_data_client_get_mtls_endpoint_and_cert_source(client_class):
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
    "client_class", [BetaAnalyticsDataClient, BetaAnalyticsDataAsyncClient]
)
@mock.patch.object(
    BetaAnalyticsDataClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(BetaAnalyticsDataClient),
)
@mock.patch.object(
    BetaAnalyticsDataAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(BetaAnalyticsDataAsyncClient),
)
def test_beta_analytics_data_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = BetaAnalyticsDataClient._DEFAULT_UNIVERSE
    default_endpoint = BetaAnalyticsDataClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = BetaAnalyticsDataClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        (BetaAnalyticsDataClient, transports.BetaAnalyticsDataGrpcTransport, "grpc"),
        (
            BetaAnalyticsDataAsyncClient,
            transports.BetaAnalyticsDataGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (BetaAnalyticsDataClient, transports.BetaAnalyticsDataRestTransport, "rest"),
    ],
)
def test_beta_analytics_data_client_client_options_scopes(
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
            BetaAnalyticsDataClient,
            transports.BetaAnalyticsDataGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            BetaAnalyticsDataAsyncClient,
            transports.BetaAnalyticsDataGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (
            BetaAnalyticsDataClient,
            transports.BetaAnalyticsDataRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_beta_analytics_data_client_client_options_credentials_file(
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


def test_beta_analytics_data_client_client_options_from_dict():
    with mock.patch(
        "google.analytics.data_v1beta.services.beta_analytics_data.transports.BetaAnalyticsDataGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = BetaAnalyticsDataClient(
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
            BetaAnalyticsDataClient,
            transports.BetaAnalyticsDataGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            BetaAnalyticsDataAsyncClient,
            transports.BetaAnalyticsDataGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_beta_analytics_data_client_create_channel_credentials_file(
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
            "analyticsdata.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                "https://www.googleapis.com/auth/analytics",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            scopes=None,
            default_host="analyticsdata.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.RunReportRequest,
        dict,
    ],
)
def test_run_report(request_type, transport: str = "grpc"):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_report), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.RunReportResponse(
            row_count=992,
            kind="kind_value",
        )
        response = client.run_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.RunReportRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.RunReportResponse)
    assert response.row_count == 992
    assert response.kind == "kind_value"


def test_run_report_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_report), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.run_report()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.RunReportRequest()


def test_run_report_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = analytics_data_api.RunReportRequest(
        property="property_value",
        currency_code="currency_code_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_report), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.run_report(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.RunReportRequest(
            property="property_value",
            currency_code="currency_code_value",
        )


def test_run_report_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.run_report in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.run_report] = mock_rpc
        request = {}
        client.run_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.run_report(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_run_report_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_report), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.RunReportResponse(
                row_count=992,
                kind="kind_value",
            )
        )
        response = await client.run_report()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.RunReportRequest()


@pytest.mark.asyncio
async def test_run_report_async_use_cached_wrapped_rpc(transport: str = "grpc_asyncio"):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.run_report
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.run_report
        ] = mock_object

        request = {}
        await client.run_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.run_report(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_run_report_async(
    transport: str = "grpc_asyncio", request_type=analytics_data_api.RunReportRequest
):
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_report), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.RunReportResponse(
                row_count=992,
                kind="kind_value",
            )
        )
        response = await client.run_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.RunReportRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.RunReportResponse)
    assert response.row_count == 992
    assert response.kind == "kind_value"


@pytest.mark.asyncio
async def test_run_report_async_from_dict():
    await test_run_report_async(request_type=dict)


def test_run_report_field_headers():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.RunReportRequest()

    request.property = "property_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_report), "__call__") as call:
        call.return_value = analytics_data_api.RunReportResponse()
        client.run_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "property=property_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_run_report_field_headers_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.RunReportRequest()

    request.property = "property_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_report), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.RunReportResponse()
        )
        await client.run_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "property=property_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.RunPivotReportRequest,
        dict,
    ],
)
def test_run_pivot_report(request_type, transport: str = "grpc"):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_pivot_report), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.RunPivotReportResponse(
            kind="kind_value",
        )
        response = client.run_pivot_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.RunPivotReportRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.RunPivotReportResponse)
    assert response.kind == "kind_value"


def test_run_pivot_report_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_pivot_report), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.run_pivot_report()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.RunPivotReportRequest()


def test_run_pivot_report_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = analytics_data_api.RunPivotReportRequest(
        property="property_value",
        currency_code="currency_code_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_pivot_report), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.run_pivot_report(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.RunPivotReportRequest(
            property="property_value",
            currency_code="currency_code_value",
        )


def test_run_pivot_report_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.run_pivot_report in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.run_pivot_report
        ] = mock_rpc
        request = {}
        client.run_pivot_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.run_pivot_report(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_run_pivot_report_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_pivot_report), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.RunPivotReportResponse(
                kind="kind_value",
            )
        )
        response = await client.run_pivot_report()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.RunPivotReportRequest()


@pytest.mark.asyncio
async def test_run_pivot_report_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.run_pivot_report
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.run_pivot_report
        ] = mock_object

        request = {}
        await client.run_pivot_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.run_pivot_report(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_run_pivot_report_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_data_api.RunPivotReportRequest,
):
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_pivot_report), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.RunPivotReportResponse(
                kind="kind_value",
            )
        )
        response = await client.run_pivot_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.RunPivotReportRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.RunPivotReportResponse)
    assert response.kind == "kind_value"


@pytest.mark.asyncio
async def test_run_pivot_report_async_from_dict():
    await test_run_pivot_report_async(request_type=dict)


def test_run_pivot_report_field_headers():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.RunPivotReportRequest()

    request.property = "property_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_pivot_report), "__call__") as call:
        call.return_value = analytics_data_api.RunPivotReportResponse()
        client.run_pivot_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "property=property_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_run_pivot_report_field_headers_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.RunPivotReportRequest()

    request.property = "property_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_pivot_report), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.RunPivotReportResponse()
        )
        await client.run_pivot_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "property=property_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.BatchRunReportsRequest,
        dict,
    ],
)
def test_batch_run_reports(request_type, transport: str = "grpc"):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_reports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.BatchRunReportsResponse(
            kind="kind_value",
        )
        response = client.batch_run_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.BatchRunReportsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.BatchRunReportsResponse)
    assert response.kind == "kind_value"


def test_batch_run_reports_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_reports), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.batch_run_reports()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.BatchRunReportsRequest()


def test_batch_run_reports_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = analytics_data_api.BatchRunReportsRequest(
        property="property_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_reports), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.batch_run_reports(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.BatchRunReportsRequest(
            property="property_value",
        )


def test_batch_run_reports_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.batch_run_reports in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.batch_run_reports
        ] = mock_rpc
        request = {}
        client.batch_run_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.batch_run_reports(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_batch_run_reports_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_reports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.BatchRunReportsResponse(
                kind="kind_value",
            )
        )
        response = await client.batch_run_reports()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.BatchRunReportsRequest()


@pytest.mark.asyncio
async def test_batch_run_reports_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.batch_run_reports
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.batch_run_reports
        ] = mock_object

        request = {}
        await client.batch_run_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.batch_run_reports(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_batch_run_reports_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_data_api.BatchRunReportsRequest,
):
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_reports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.BatchRunReportsResponse(
                kind="kind_value",
            )
        )
        response = await client.batch_run_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.BatchRunReportsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.BatchRunReportsResponse)
    assert response.kind == "kind_value"


@pytest.mark.asyncio
async def test_batch_run_reports_async_from_dict():
    await test_batch_run_reports_async(request_type=dict)


def test_batch_run_reports_field_headers():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.BatchRunReportsRequest()

    request.property = "property_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_reports), "__call__"
    ) as call:
        call.return_value = analytics_data_api.BatchRunReportsResponse()
        client.batch_run_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "property=property_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_run_reports_field_headers_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.BatchRunReportsRequest()

    request.property = "property_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_reports), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.BatchRunReportsResponse()
        )
        await client.batch_run_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "property=property_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.BatchRunPivotReportsRequest,
        dict,
    ],
)
def test_batch_run_pivot_reports(request_type, transport: str = "grpc"):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_pivot_reports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.BatchRunPivotReportsResponse(
            kind="kind_value",
        )
        response = client.batch_run_pivot_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.BatchRunPivotReportsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.BatchRunPivotReportsResponse)
    assert response.kind == "kind_value"


def test_batch_run_pivot_reports_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_pivot_reports), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.batch_run_pivot_reports()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.BatchRunPivotReportsRequest()


def test_batch_run_pivot_reports_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = analytics_data_api.BatchRunPivotReportsRequest(
        property="property_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_pivot_reports), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.batch_run_pivot_reports(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.BatchRunPivotReportsRequest(
            property="property_value",
        )


def test_batch_run_pivot_reports_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.batch_run_pivot_reports
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.batch_run_pivot_reports
        ] = mock_rpc
        request = {}
        client.batch_run_pivot_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.batch_run_pivot_reports(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_batch_run_pivot_reports_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_pivot_reports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.BatchRunPivotReportsResponse(
                kind="kind_value",
            )
        )
        response = await client.batch_run_pivot_reports()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.BatchRunPivotReportsRequest()


@pytest.mark.asyncio
async def test_batch_run_pivot_reports_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.batch_run_pivot_reports
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.batch_run_pivot_reports
        ] = mock_object

        request = {}
        await client.batch_run_pivot_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.batch_run_pivot_reports(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_batch_run_pivot_reports_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_data_api.BatchRunPivotReportsRequest,
):
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_pivot_reports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.BatchRunPivotReportsResponse(
                kind="kind_value",
            )
        )
        response = await client.batch_run_pivot_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.BatchRunPivotReportsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.BatchRunPivotReportsResponse)
    assert response.kind == "kind_value"


@pytest.mark.asyncio
async def test_batch_run_pivot_reports_async_from_dict():
    await test_batch_run_pivot_reports_async(request_type=dict)


def test_batch_run_pivot_reports_field_headers():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.BatchRunPivotReportsRequest()

    request.property = "property_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_pivot_reports), "__call__"
    ) as call:
        call.return_value = analytics_data_api.BatchRunPivotReportsResponse()
        client.batch_run_pivot_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "property=property_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_run_pivot_reports_field_headers_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.BatchRunPivotReportsRequest()

    request.property = "property_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_pivot_reports), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.BatchRunPivotReportsResponse()
        )
        await client.batch_run_pivot_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "property=property_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.GetMetadataRequest,
        dict,
    ],
)
def test_get_metadata(request_type, transport: str = "grpc"):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metadata), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.Metadata(
            name="name_value",
        )
        response = client.get_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.GetMetadataRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.Metadata)
    assert response.name == "name_value"


def test_get_metadata_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metadata), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_metadata()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.GetMetadataRequest()


def test_get_metadata_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = analytics_data_api.GetMetadataRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metadata), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_metadata(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.GetMetadataRequest(
            name="name_value",
        )


def test_get_metadata_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_metadata in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_metadata] = mock_rpc
        request = {}
        client.get_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_metadata(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_metadata_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metadata), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.Metadata(
                name="name_value",
            )
        )
        response = await client.get_metadata()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.GetMetadataRequest()


@pytest.mark.asyncio
async def test_get_metadata_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_metadata
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_metadata
        ] = mock_object

        request = {}
        await client.get_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_metadata(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_metadata_async(
    transport: str = "grpc_asyncio", request_type=analytics_data_api.GetMetadataRequest
):
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metadata), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.Metadata(
                name="name_value",
            )
        )
        response = await client.get_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.GetMetadataRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.Metadata)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_get_metadata_async_from_dict():
    await test_get_metadata_async(request_type=dict)


def test_get_metadata_field_headers():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.GetMetadataRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metadata), "__call__") as call:
        call.return_value = analytics_data_api.Metadata()
        client.get_metadata(request)

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
async def test_get_metadata_field_headers_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.GetMetadataRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metadata), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.Metadata()
        )
        await client.get_metadata(request)

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


def test_get_metadata_flattened():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metadata), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.Metadata()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_metadata(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_metadata_flattened_error():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_metadata(
            analytics_data_api.GetMetadataRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_metadata_flattened_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metadata), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.Metadata()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.Metadata()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_metadata(
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
async def test_get_metadata_flattened_error_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_metadata(
            analytics_data_api.GetMetadataRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.RunRealtimeReportRequest,
        dict,
    ],
)
def test_run_realtime_report(request_type, transport: str = "grpc"):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_realtime_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.RunRealtimeReportResponse(
            row_count=992,
            kind="kind_value",
        )
        response = client.run_realtime_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.RunRealtimeReportRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.RunRealtimeReportResponse)
    assert response.row_count == 992
    assert response.kind == "kind_value"


def test_run_realtime_report_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_realtime_report), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.run_realtime_report()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.RunRealtimeReportRequest()


def test_run_realtime_report_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = analytics_data_api.RunRealtimeReportRequest(
        property="property_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_realtime_report), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.run_realtime_report(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.RunRealtimeReportRequest(
            property="property_value",
        )


def test_run_realtime_report_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.run_realtime_report in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.run_realtime_report
        ] = mock_rpc
        request = {}
        client.run_realtime_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.run_realtime_report(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_run_realtime_report_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_realtime_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.RunRealtimeReportResponse(
                row_count=992,
                kind="kind_value",
            )
        )
        response = await client.run_realtime_report()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.RunRealtimeReportRequest()


@pytest.mark.asyncio
async def test_run_realtime_report_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.run_realtime_report
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.run_realtime_report
        ] = mock_object

        request = {}
        await client.run_realtime_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.run_realtime_report(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_run_realtime_report_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_data_api.RunRealtimeReportRequest,
):
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_realtime_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.RunRealtimeReportResponse(
                row_count=992,
                kind="kind_value",
            )
        )
        response = await client.run_realtime_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.RunRealtimeReportRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.RunRealtimeReportResponse)
    assert response.row_count == 992
    assert response.kind == "kind_value"


@pytest.mark.asyncio
async def test_run_realtime_report_async_from_dict():
    await test_run_realtime_report_async(request_type=dict)


def test_run_realtime_report_field_headers():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.RunRealtimeReportRequest()

    request.property = "property_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_realtime_report), "__call__"
    ) as call:
        call.return_value = analytics_data_api.RunRealtimeReportResponse()
        client.run_realtime_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "property=property_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_run_realtime_report_field_headers_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.RunRealtimeReportRequest()

    request.property = "property_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_realtime_report), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.RunRealtimeReportResponse()
        )
        await client.run_realtime_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "property=property_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.CheckCompatibilityRequest,
        dict,
    ],
)
def test_check_compatibility(request_type, transport: str = "grpc"):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_compatibility), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.CheckCompatibilityResponse()
        response = client.check_compatibility(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.CheckCompatibilityRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.CheckCompatibilityResponse)


def test_check_compatibility_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_compatibility), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.check_compatibility()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.CheckCompatibilityRequest()


def test_check_compatibility_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = analytics_data_api.CheckCompatibilityRequest(
        property="property_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_compatibility), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.check_compatibility(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.CheckCompatibilityRequest(
            property="property_value",
        )


def test_check_compatibility_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.check_compatibility in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.check_compatibility
        ] = mock_rpc
        request = {}
        client.check_compatibility(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.check_compatibility(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_check_compatibility_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_compatibility), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.CheckCompatibilityResponse()
        )
        response = await client.check_compatibility()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.CheckCompatibilityRequest()


@pytest.mark.asyncio
async def test_check_compatibility_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.check_compatibility
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.check_compatibility
        ] = mock_object

        request = {}
        await client.check_compatibility(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.check_compatibility(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_check_compatibility_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_data_api.CheckCompatibilityRequest,
):
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_compatibility), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.CheckCompatibilityResponse()
        )
        response = await client.check_compatibility(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.CheckCompatibilityRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.CheckCompatibilityResponse)


@pytest.mark.asyncio
async def test_check_compatibility_async_from_dict():
    await test_check_compatibility_async(request_type=dict)


def test_check_compatibility_field_headers():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.CheckCompatibilityRequest()

    request.property = "property_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_compatibility), "__call__"
    ) as call:
        call.return_value = analytics_data_api.CheckCompatibilityResponse()
        client.check_compatibility(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "property=property_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_check_compatibility_field_headers_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.CheckCompatibilityRequest()

    request.property = "property_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_compatibility), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.CheckCompatibilityResponse()
        )
        await client.check_compatibility(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "property=property_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.CreateAudienceExportRequest,
        dict,
    ],
)
def test_create_audience_export(request_type, transport: str = "grpc"):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_audience_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_audience_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.CreateAudienceExportRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_audience_export_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_audience_export), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_audience_export()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.CreateAudienceExportRequest()


def test_create_audience_export_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = analytics_data_api.CreateAudienceExportRequest(
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_audience_export), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_audience_export(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.CreateAudienceExportRequest(
            parent="parent_value",
        )


def test_create_audience_export_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_audience_export
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_audience_export
        ] = mock_rpc
        request = {}
        client.create_audience_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_audience_export(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_audience_export_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_audience_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_audience_export()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.CreateAudienceExportRequest()


@pytest.mark.asyncio
async def test_create_audience_export_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_audience_export
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_audience_export
        ] = mock_object

        request = {}
        await client.create_audience_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.create_audience_export(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_create_audience_export_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_data_api.CreateAudienceExportRequest,
):
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_audience_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_audience_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.CreateAudienceExportRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_audience_export_async_from_dict():
    await test_create_audience_export_async(request_type=dict)


def test_create_audience_export_field_headers():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.CreateAudienceExportRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_audience_export), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_audience_export(request)

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
async def test_create_audience_export_field_headers_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.CreateAudienceExportRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_audience_export), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_audience_export(request)

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


def test_create_audience_export_flattened():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_audience_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_audience_export(
            parent="parent_value",
            audience_export=analytics_data_api.AudienceExport(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].audience_export
        mock_val = analytics_data_api.AudienceExport(name="name_value")
        assert arg == mock_val


def test_create_audience_export_flattened_error():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_audience_export(
            analytics_data_api.CreateAudienceExportRequest(),
            parent="parent_value",
            audience_export=analytics_data_api.AudienceExport(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_audience_export_flattened_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_audience_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_audience_export(
            parent="parent_value",
            audience_export=analytics_data_api.AudienceExport(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].audience_export
        mock_val = analytics_data_api.AudienceExport(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_audience_export_flattened_error_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_audience_export(
            analytics_data_api.CreateAudienceExportRequest(),
            parent="parent_value",
            audience_export=analytics_data_api.AudienceExport(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.QueryAudienceExportRequest,
        dict,
    ],
)
def test_query_audience_export(request_type, transport: str = "grpc"):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_audience_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.QueryAudienceExportResponse(
            row_count=992,
        )
        response = client.query_audience_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.QueryAudienceExportRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.QueryAudienceExportResponse)
    assert response.row_count == 992


def test_query_audience_export_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_audience_export), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.query_audience_export()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.QueryAudienceExportRequest()


def test_query_audience_export_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = analytics_data_api.QueryAudienceExportRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_audience_export), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.query_audience_export(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.QueryAudienceExportRequest(
            name="name_value",
        )


def test_query_audience_export_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.query_audience_export
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.query_audience_export
        ] = mock_rpc
        request = {}
        client.query_audience_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.query_audience_export(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_query_audience_export_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_audience_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.QueryAudienceExportResponse(
                row_count=992,
            )
        )
        response = await client.query_audience_export()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.QueryAudienceExportRequest()


@pytest.mark.asyncio
async def test_query_audience_export_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.query_audience_export
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.query_audience_export
        ] = mock_object

        request = {}
        await client.query_audience_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.query_audience_export(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_query_audience_export_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_data_api.QueryAudienceExportRequest,
):
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_audience_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.QueryAudienceExportResponse(
                row_count=992,
            )
        )
        response = await client.query_audience_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.QueryAudienceExportRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.QueryAudienceExportResponse)
    assert response.row_count == 992


@pytest.mark.asyncio
async def test_query_audience_export_async_from_dict():
    await test_query_audience_export_async(request_type=dict)


def test_query_audience_export_field_headers():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.QueryAudienceExportRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_audience_export), "__call__"
    ) as call:
        call.return_value = analytics_data_api.QueryAudienceExportResponse()
        client.query_audience_export(request)

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
async def test_query_audience_export_field_headers_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.QueryAudienceExportRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_audience_export), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.QueryAudienceExportResponse()
        )
        await client.query_audience_export(request)

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


def test_query_audience_export_flattened():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_audience_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.QueryAudienceExportResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.query_audience_export(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_query_audience_export_flattened_error():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.query_audience_export(
            analytics_data_api.QueryAudienceExportRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_query_audience_export_flattened_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_audience_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.QueryAudienceExportResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.QueryAudienceExportResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.query_audience_export(
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
async def test_query_audience_export_flattened_error_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.query_audience_export(
            analytics_data_api.QueryAudienceExportRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.GetAudienceExportRequest,
        dict,
    ],
)
def test_get_audience_export(request_type, transport: str = "grpc"):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_audience_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.AudienceExport(
            name="name_value",
            audience="audience_value",
            audience_display_name="audience_display_name_value",
            state=analytics_data_api.AudienceExport.State.CREATING,
            creation_quota_tokens_charged=3070,
            row_count=992,
            error_message="error_message_value",
            percentage_completed=0.2106,
        )
        response = client.get_audience_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.GetAudienceExportRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.AudienceExport)
    assert response.name == "name_value"
    assert response.audience == "audience_value"
    assert response.audience_display_name == "audience_display_name_value"
    assert response.state == analytics_data_api.AudienceExport.State.CREATING
    assert response.creation_quota_tokens_charged == 3070
    assert response.row_count == 992
    assert response.error_message == "error_message_value"
    assert math.isclose(response.percentage_completed, 0.2106, rel_tol=1e-6)


def test_get_audience_export_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_audience_export), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_audience_export()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.GetAudienceExportRequest()


def test_get_audience_export_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = analytics_data_api.GetAudienceExportRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_audience_export), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_audience_export(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.GetAudienceExportRequest(
            name="name_value",
        )


def test_get_audience_export_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_audience_export in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_audience_export
        ] = mock_rpc
        request = {}
        client.get_audience_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_audience_export(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_audience_export_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_audience_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.AudienceExport(
                name="name_value",
                audience="audience_value",
                audience_display_name="audience_display_name_value",
                state=analytics_data_api.AudienceExport.State.CREATING,
                creation_quota_tokens_charged=3070,
                row_count=992,
                error_message="error_message_value",
                percentage_completed=0.2106,
            )
        )
        response = await client.get_audience_export()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.GetAudienceExportRequest()


@pytest.mark.asyncio
async def test_get_audience_export_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_audience_export
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_audience_export
        ] = mock_object

        request = {}
        await client.get_audience_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_audience_export(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_audience_export_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_data_api.GetAudienceExportRequest,
):
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_audience_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.AudienceExport(
                name="name_value",
                audience="audience_value",
                audience_display_name="audience_display_name_value",
                state=analytics_data_api.AudienceExport.State.CREATING,
                creation_quota_tokens_charged=3070,
                row_count=992,
                error_message="error_message_value",
                percentage_completed=0.2106,
            )
        )
        response = await client.get_audience_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.GetAudienceExportRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.AudienceExport)
    assert response.name == "name_value"
    assert response.audience == "audience_value"
    assert response.audience_display_name == "audience_display_name_value"
    assert response.state == analytics_data_api.AudienceExport.State.CREATING
    assert response.creation_quota_tokens_charged == 3070
    assert response.row_count == 992
    assert response.error_message == "error_message_value"
    assert math.isclose(response.percentage_completed, 0.2106, rel_tol=1e-6)


@pytest.mark.asyncio
async def test_get_audience_export_async_from_dict():
    await test_get_audience_export_async(request_type=dict)


def test_get_audience_export_field_headers():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.GetAudienceExportRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_audience_export), "__call__"
    ) as call:
        call.return_value = analytics_data_api.AudienceExport()
        client.get_audience_export(request)

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
async def test_get_audience_export_field_headers_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.GetAudienceExportRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_audience_export), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.AudienceExport()
        )
        await client.get_audience_export(request)

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


def test_get_audience_export_flattened():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_audience_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.AudienceExport()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_audience_export(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_audience_export_flattened_error():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_audience_export(
            analytics_data_api.GetAudienceExportRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_audience_export_flattened_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_audience_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.AudienceExport()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.AudienceExport()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_audience_export(
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
async def test_get_audience_export_flattened_error_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_audience_export(
            analytics_data_api.GetAudienceExportRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.ListAudienceExportsRequest,
        dict,
    ],
)
def test_list_audience_exports(request_type, transport: str = "grpc"):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_audience_exports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.ListAudienceExportsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_audience_exports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.ListAudienceExportsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAudienceExportsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_audience_exports_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_audience_exports), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_audience_exports()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.ListAudienceExportsRequest()


def test_list_audience_exports_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = analytics_data_api.ListAudienceExportsRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_audience_exports), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_audience_exports(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.ListAudienceExportsRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_audience_exports_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_audience_exports
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_audience_exports
        ] = mock_rpc
        request = {}
        client.list_audience_exports(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_audience_exports(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_audience_exports_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_audience_exports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.ListAudienceExportsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_audience_exports()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_data_api.ListAudienceExportsRequest()


@pytest.mark.asyncio
async def test_list_audience_exports_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_audience_exports
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_audience_exports
        ] = mock_object

        request = {}
        await client.list_audience_exports(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_audience_exports(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_audience_exports_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_data_api.ListAudienceExportsRequest,
):
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_audience_exports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.ListAudienceExportsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_audience_exports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = analytics_data_api.ListAudienceExportsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAudienceExportsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_audience_exports_async_from_dict():
    await test_list_audience_exports_async(request_type=dict)


def test_list_audience_exports_field_headers():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.ListAudienceExportsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_audience_exports), "__call__"
    ) as call:
        call.return_value = analytics_data_api.ListAudienceExportsResponse()
        client.list_audience_exports(request)

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
async def test_list_audience_exports_field_headers_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.ListAudienceExportsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_audience_exports), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.ListAudienceExportsResponse()
        )
        await client.list_audience_exports(request)

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


def test_list_audience_exports_flattened():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_audience_exports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.ListAudienceExportsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_audience_exports(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_audience_exports_flattened_error():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_audience_exports(
            analytics_data_api.ListAudienceExportsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_audience_exports_flattened_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_audience_exports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.ListAudienceExportsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.ListAudienceExportsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_audience_exports(
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
async def test_list_audience_exports_flattened_error_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_audience_exports(
            analytics_data_api.ListAudienceExportsRequest(),
            parent="parent_value",
        )


def test_list_audience_exports_pager(transport_name: str = "grpc"):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_audience_exports), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_data_api.ListAudienceExportsResponse(
                audience_exports=[
                    analytics_data_api.AudienceExport(),
                    analytics_data_api.AudienceExport(),
                    analytics_data_api.AudienceExport(),
                ],
                next_page_token="abc",
            ),
            analytics_data_api.ListAudienceExportsResponse(
                audience_exports=[],
                next_page_token="def",
            ),
            analytics_data_api.ListAudienceExportsResponse(
                audience_exports=[
                    analytics_data_api.AudienceExport(),
                ],
                next_page_token="ghi",
            ),
            analytics_data_api.ListAudienceExportsResponse(
                audience_exports=[
                    analytics_data_api.AudienceExport(),
                    analytics_data_api.AudienceExport(),
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
        pager = client.list_audience_exports(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, analytics_data_api.AudienceExport) for i in results)


def test_list_audience_exports_pages(transport_name: str = "grpc"):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_audience_exports), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_data_api.ListAudienceExportsResponse(
                audience_exports=[
                    analytics_data_api.AudienceExport(),
                    analytics_data_api.AudienceExport(),
                    analytics_data_api.AudienceExport(),
                ],
                next_page_token="abc",
            ),
            analytics_data_api.ListAudienceExportsResponse(
                audience_exports=[],
                next_page_token="def",
            ),
            analytics_data_api.ListAudienceExportsResponse(
                audience_exports=[
                    analytics_data_api.AudienceExport(),
                ],
                next_page_token="ghi",
            ),
            analytics_data_api.ListAudienceExportsResponse(
                audience_exports=[
                    analytics_data_api.AudienceExport(),
                    analytics_data_api.AudienceExport(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_audience_exports(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_audience_exports_async_pager():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_audience_exports),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_data_api.ListAudienceExportsResponse(
                audience_exports=[
                    analytics_data_api.AudienceExport(),
                    analytics_data_api.AudienceExport(),
                    analytics_data_api.AudienceExport(),
                ],
                next_page_token="abc",
            ),
            analytics_data_api.ListAudienceExportsResponse(
                audience_exports=[],
                next_page_token="def",
            ),
            analytics_data_api.ListAudienceExportsResponse(
                audience_exports=[
                    analytics_data_api.AudienceExport(),
                ],
                next_page_token="ghi",
            ),
            analytics_data_api.ListAudienceExportsResponse(
                audience_exports=[
                    analytics_data_api.AudienceExport(),
                    analytics_data_api.AudienceExport(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_audience_exports(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, analytics_data_api.AudienceExport) for i in responses)


@pytest.mark.asyncio
async def test_list_audience_exports_async_pages():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_audience_exports),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_data_api.ListAudienceExportsResponse(
                audience_exports=[
                    analytics_data_api.AudienceExport(),
                    analytics_data_api.AudienceExport(),
                    analytics_data_api.AudienceExport(),
                ],
                next_page_token="abc",
            ),
            analytics_data_api.ListAudienceExportsResponse(
                audience_exports=[],
                next_page_token="def",
            ),
            analytics_data_api.ListAudienceExportsResponse(
                audience_exports=[
                    analytics_data_api.AudienceExport(),
                ],
                next_page_token="ghi",
            ),
            analytics_data_api.ListAudienceExportsResponse(
                audience_exports=[
                    analytics_data_api.AudienceExport(),
                    analytics_data_api.AudienceExport(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_audience_exports(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.RunReportRequest,
        dict,
    ],
)
def test_run_report_rest(request_type):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"property": "properties/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = analytics_data_api.RunReportResponse(
            row_count=992,
            kind="kind_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = analytics_data_api.RunReportResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.run_report(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.RunReportResponse)
    assert response.row_count == 992
    assert response.kind == "kind_value"


def test_run_report_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.run_report in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.run_report] = mock_rpc

        request = {}
        client.run_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.run_report(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_run_report_rest_interceptors(null_interceptor):
    transport = transports.BetaAnalyticsDataRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BetaAnalyticsDataRestInterceptor(),
    )
    client = BetaAnalyticsDataClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "post_run_report"
    ) as post, mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "pre_run_report"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = analytics_data_api.RunReportRequest.pb(
            analytics_data_api.RunReportRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = analytics_data_api.RunReportResponse.to_json(
            analytics_data_api.RunReportResponse()
        )

        request = analytics_data_api.RunReportRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = analytics_data_api.RunReportResponse()

        client.run_report(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_run_report_rest_bad_request(
    transport: str = "rest", request_type=analytics_data_api.RunReportRequest
):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"property": "properties/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.run_report(request)


def test_run_report_rest_error():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.RunPivotReportRequest,
        dict,
    ],
)
def test_run_pivot_report_rest(request_type):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"property": "properties/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = analytics_data_api.RunPivotReportResponse(
            kind="kind_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = analytics_data_api.RunPivotReportResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.run_pivot_report(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.RunPivotReportResponse)
    assert response.kind == "kind_value"


def test_run_pivot_report_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.run_pivot_report in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.run_pivot_report
        ] = mock_rpc

        request = {}
        client.run_pivot_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.run_pivot_report(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_run_pivot_report_rest_interceptors(null_interceptor):
    transport = transports.BetaAnalyticsDataRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BetaAnalyticsDataRestInterceptor(),
    )
    client = BetaAnalyticsDataClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "post_run_pivot_report"
    ) as post, mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "pre_run_pivot_report"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = analytics_data_api.RunPivotReportRequest.pb(
            analytics_data_api.RunPivotReportRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = analytics_data_api.RunPivotReportResponse.to_json(
            analytics_data_api.RunPivotReportResponse()
        )

        request = analytics_data_api.RunPivotReportRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = analytics_data_api.RunPivotReportResponse()

        client.run_pivot_report(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_run_pivot_report_rest_bad_request(
    transport: str = "rest", request_type=analytics_data_api.RunPivotReportRequest
):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"property": "properties/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.run_pivot_report(request)


def test_run_pivot_report_rest_error():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.BatchRunReportsRequest,
        dict,
    ],
)
def test_batch_run_reports_rest(request_type):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"property": "properties/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = analytics_data_api.BatchRunReportsResponse(
            kind="kind_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = analytics_data_api.BatchRunReportsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.batch_run_reports(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.BatchRunReportsResponse)
    assert response.kind == "kind_value"


def test_batch_run_reports_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.batch_run_reports in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.batch_run_reports
        ] = mock_rpc

        request = {}
        client.batch_run_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.batch_run_reports(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_batch_run_reports_rest_interceptors(null_interceptor):
    transport = transports.BetaAnalyticsDataRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BetaAnalyticsDataRestInterceptor(),
    )
    client = BetaAnalyticsDataClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "post_batch_run_reports"
    ) as post, mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "pre_batch_run_reports"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = analytics_data_api.BatchRunReportsRequest.pb(
            analytics_data_api.BatchRunReportsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = analytics_data_api.BatchRunReportsResponse.to_json(
            analytics_data_api.BatchRunReportsResponse()
        )

        request = analytics_data_api.BatchRunReportsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = analytics_data_api.BatchRunReportsResponse()

        client.batch_run_reports(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_batch_run_reports_rest_bad_request(
    transport: str = "rest", request_type=analytics_data_api.BatchRunReportsRequest
):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"property": "properties/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.batch_run_reports(request)


def test_batch_run_reports_rest_error():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.BatchRunPivotReportsRequest,
        dict,
    ],
)
def test_batch_run_pivot_reports_rest(request_type):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"property": "properties/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = analytics_data_api.BatchRunPivotReportsResponse(
            kind="kind_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = analytics_data_api.BatchRunPivotReportsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.batch_run_pivot_reports(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.BatchRunPivotReportsResponse)
    assert response.kind == "kind_value"


def test_batch_run_pivot_reports_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.batch_run_pivot_reports
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.batch_run_pivot_reports
        ] = mock_rpc

        request = {}
        client.batch_run_pivot_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.batch_run_pivot_reports(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_batch_run_pivot_reports_rest_interceptors(null_interceptor):
    transport = transports.BetaAnalyticsDataRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BetaAnalyticsDataRestInterceptor(),
    )
    client = BetaAnalyticsDataClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "post_batch_run_pivot_reports"
    ) as post, mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "pre_batch_run_pivot_reports"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = analytics_data_api.BatchRunPivotReportsRequest.pb(
            analytics_data_api.BatchRunPivotReportsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            analytics_data_api.BatchRunPivotReportsResponse.to_json(
                analytics_data_api.BatchRunPivotReportsResponse()
            )
        )

        request = analytics_data_api.BatchRunPivotReportsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = analytics_data_api.BatchRunPivotReportsResponse()

        client.batch_run_pivot_reports(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_batch_run_pivot_reports_rest_bad_request(
    transport: str = "rest", request_type=analytics_data_api.BatchRunPivotReportsRequest
):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"property": "properties/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.batch_run_pivot_reports(request)


def test_batch_run_pivot_reports_rest_error():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.GetMetadataRequest,
        dict,
    ],
)
def test_get_metadata_rest(request_type):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "properties/sample1/metadata"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = analytics_data_api.Metadata(
            name="name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = analytics_data_api.Metadata.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_metadata(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.Metadata)
    assert response.name == "name_value"


def test_get_metadata_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_metadata in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_metadata] = mock_rpc

        request = {}
        client.get_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_metadata(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_metadata_rest_required_fields(
    request_type=analytics_data_api.GetMetadataRequest,
):
    transport_class = transports.BetaAnalyticsDataRestTransport

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
    ).get_metadata._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_metadata._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = analytics_data_api.Metadata()
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
            return_value = analytics_data_api.Metadata.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_metadata(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_metadata_rest_unset_required_fields():
    transport = transports.BetaAnalyticsDataRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_metadata._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_metadata_rest_interceptors(null_interceptor):
    transport = transports.BetaAnalyticsDataRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BetaAnalyticsDataRestInterceptor(),
    )
    client = BetaAnalyticsDataClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "post_get_metadata"
    ) as post, mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "pre_get_metadata"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = analytics_data_api.GetMetadataRequest.pb(
            analytics_data_api.GetMetadataRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = analytics_data_api.Metadata.to_json(
            analytics_data_api.Metadata()
        )

        request = analytics_data_api.GetMetadataRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = analytics_data_api.Metadata()

        client.get_metadata(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_metadata_rest_bad_request(
    transport: str = "rest", request_type=analytics_data_api.GetMetadataRequest
):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "properties/sample1/metadata"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_metadata(request)


def test_get_metadata_rest_flattened():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = analytics_data_api.Metadata()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "properties/sample1/metadata"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = analytics_data_api.Metadata.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_metadata(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta/{name=properties/*/metadata}" % client.transport._host, args[1]
        )


def test_get_metadata_rest_flattened_error(transport: str = "rest"):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_metadata(
            analytics_data_api.GetMetadataRequest(),
            name="name_value",
        )


def test_get_metadata_rest_error():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.RunRealtimeReportRequest,
        dict,
    ],
)
def test_run_realtime_report_rest(request_type):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"property": "properties/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = analytics_data_api.RunRealtimeReportResponse(
            row_count=992,
            kind="kind_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = analytics_data_api.RunRealtimeReportResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.run_realtime_report(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.RunRealtimeReportResponse)
    assert response.row_count == 992
    assert response.kind == "kind_value"


def test_run_realtime_report_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.run_realtime_report in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.run_realtime_report
        ] = mock_rpc

        request = {}
        client.run_realtime_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.run_realtime_report(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_run_realtime_report_rest_interceptors(null_interceptor):
    transport = transports.BetaAnalyticsDataRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BetaAnalyticsDataRestInterceptor(),
    )
    client = BetaAnalyticsDataClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "post_run_realtime_report"
    ) as post, mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "pre_run_realtime_report"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = analytics_data_api.RunRealtimeReportRequest.pb(
            analytics_data_api.RunRealtimeReportRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            analytics_data_api.RunRealtimeReportResponse.to_json(
                analytics_data_api.RunRealtimeReportResponse()
            )
        )

        request = analytics_data_api.RunRealtimeReportRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = analytics_data_api.RunRealtimeReportResponse()

        client.run_realtime_report(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_run_realtime_report_rest_bad_request(
    transport: str = "rest", request_type=analytics_data_api.RunRealtimeReportRequest
):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"property": "properties/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.run_realtime_report(request)


def test_run_realtime_report_rest_error():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.CheckCompatibilityRequest,
        dict,
    ],
)
def test_check_compatibility_rest(request_type):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"property": "properties/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = analytics_data_api.CheckCompatibilityResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = analytics_data_api.CheckCompatibilityResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.check_compatibility(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.CheckCompatibilityResponse)


def test_check_compatibility_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.check_compatibility in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.check_compatibility
        ] = mock_rpc

        request = {}
        client.check_compatibility(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.check_compatibility(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_check_compatibility_rest_interceptors(null_interceptor):
    transport = transports.BetaAnalyticsDataRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BetaAnalyticsDataRestInterceptor(),
    )
    client = BetaAnalyticsDataClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "post_check_compatibility"
    ) as post, mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "pre_check_compatibility"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = analytics_data_api.CheckCompatibilityRequest.pb(
            analytics_data_api.CheckCompatibilityRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            analytics_data_api.CheckCompatibilityResponse.to_json(
                analytics_data_api.CheckCompatibilityResponse()
            )
        )

        request = analytics_data_api.CheckCompatibilityRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = analytics_data_api.CheckCompatibilityResponse()

        client.check_compatibility(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_check_compatibility_rest_bad_request(
    transport: str = "rest", request_type=analytics_data_api.CheckCompatibilityRequest
):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"property": "properties/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.check_compatibility(request)


def test_check_compatibility_rest_error():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.CreateAudienceExportRequest,
        dict,
    ],
)
def test_create_audience_export_rest(request_type):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "properties/sample1"}
    request_init["audience_export"] = {
        "name": "name_value",
        "audience": "audience_value",
        "audience_display_name": "audience_display_name_value",
        "dimensions": [{"dimension_name": "dimension_name_value"}],
        "state": 1,
        "begin_creating_time": {"seconds": 751, "nanos": 543},
        "creation_quota_tokens_charged": 3070,
        "row_count": 992,
        "error_message": "error_message_value",
        "percentage_completed": 0.2106,
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = analytics_data_api.CreateAudienceExportRequest.meta.fields[
        "audience_export"
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
    for field, value in request_init["audience_export"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["audience_export"][field])):
                    del request_init["audience_export"][field][i][subfield]
            else:
                del request_init["audience_export"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_audience_export(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_audience_export_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_audience_export
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_audience_export
        ] = mock_rpc

        request = {}
        client.create_audience_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_audience_export(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_audience_export_rest_required_fields(
    request_type=analytics_data_api.CreateAudienceExportRequest,
):
    transport_class = transports.BetaAnalyticsDataRestTransport

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
    ).create_audience_export._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_audience_export._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
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
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_audience_export(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_audience_export_rest_unset_required_fields():
    transport = transports.BetaAnalyticsDataRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_audience_export._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "audienceExport",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_audience_export_rest_interceptors(null_interceptor):
    transport = transports.BetaAnalyticsDataRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BetaAnalyticsDataRestInterceptor(),
    )
    client = BetaAnalyticsDataClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "post_create_audience_export"
    ) as post, mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "pre_create_audience_export"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = analytics_data_api.CreateAudienceExportRequest.pb(
            analytics_data_api.CreateAudienceExportRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = analytics_data_api.CreateAudienceExportRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_audience_export(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_audience_export_rest_bad_request(
    transport: str = "rest", request_type=analytics_data_api.CreateAudienceExportRequest
):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "properties/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_audience_export(request)


def test_create_audience_export_rest_flattened():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "properties/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            audience_export=analytics_data_api.AudienceExport(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_audience_export(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta/{parent=properties/*}/audienceExports" % client.transport._host,
            args[1],
        )


def test_create_audience_export_rest_flattened_error(transport: str = "rest"):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_audience_export(
            analytics_data_api.CreateAudienceExportRequest(),
            parent="parent_value",
            audience_export=analytics_data_api.AudienceExport(name="name_value"),
        )


def test_create_audience_export_rest_error():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.QueryAudienceExportRequest,
        dict,
    ],
)
def test_query_audience_export_rest(request_type):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "properties/sample1/audienceExports/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = analytics_data_api.QueryAudienceExportResponse(
            row_count=992,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = analytics_data_api.QueryAudienceExportResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.query_audience_export(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.QueryAudienceExportResponse)
    assert response.row_count == 992


def test_query_audience_export_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.query_audience_export
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.query_audience_export
        ] = mock_rpc

        request = {}
        client.query_audience_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.query_audience_export(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_query_audience_export_rest_required_fields(
    request_type=analytics_data_api.QueryAudienceExportRequest,
):
    transport_class = transports.BetaAnalyticsDataRestTransport

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
    ).query_audience_export._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).query_audience_export._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = analytics_data_api.QueryAudienceExportResponse()
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
            return_value = analytics_data_api.QueryAudienceExportResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.query_audience_export(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_query_audience_export_rest_unset_required_fields():
    transport = transports.BetaAnalyticsDataRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.query_audience_export._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_query_audience_export_rest_interceptors(null_interceptor):
    transport = transports.BetaAnalyticsDataRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BetaAnalyticsDataRestInterceptor(),
    )
    client = BetaAnalyticsDataClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "post_query_audience_export"
    ) as post, mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "pre_query_audience_export"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = analytics_data_api.QueryAudienceExportRequest.pb(
            analytics_data_api.QueryAudienceExportRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            analytics_data_api.QueryAudienceExportResponse.to_json(
                analytics_data_api.QueryAudienceExportResponse()
            )
        )

        request = analytics_data_api.QueryAudienceExportRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = analytics_data_api.QueryAudienceExportResponse()

        client.query_audience_export(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_query_audience_export_rest_bad_request(
    transport: str = "rest", request_type=analytics_data_api.QueryAudienceExportRequest
):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "properties/sample1/audienceExports/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.query_audience_export(request)


def test_query_audience_export_rest_flattened():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = analytics_data_api.QueryAudienceExportResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "properties/sample1/audienceExports/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = analytics_data_api.QueryAudienceExportResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.query_audience_export(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta/{name=properties/*/audienceExports/*}:query"
            % client.transport._host,
            args[1],
        )


def test_query_audience_export_rest_flattened_error(transport: str = "rest"):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.query_audience_export(
            analytics_data_api.QueryAudienceExportRequest(),
            name="name_value",
        )


def test_query_audience_export_rest_error():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.GetAudienceExportRequest,
        dict,
    ],
)
def test_get_audience_export_rest(request_type):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "properties/sample1/audienceExports/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = analytics_data_api.AudienceExport(
            name="name_value",
            audience="audience_value",
            audience_display_name="audience_display_name_value",
            state=analytics_data_api.AudienceExport.State.CREATING,
            creation_quota_tokens_charged=3070,
            row_count=992,
            error_message="error_message_value",
            percentage_completed=0.2106,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = analytics_data_api.AudienceExport.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_audience_export(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.AudienceExport)
    assert response.name == "name_value"
    assert response.audience == "audience_value"
    assert response.audience_display_name == "audience_display_name_value"
    assert response.state == analytics_data_api.AudienceExport.State.CREATING
    assert response.creation_quota_tokens_charged == 3070
    assert response.row_count == 992
    assert response.error_message == "error_message_value"
    assert math.isclose(response.percentage_completed, 0.2106, rel_tol=1e-6)


def test_get_audience_export_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_audience_export in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_audience_export
        ] = mock_rpc

        request = {}
        client.get_audience_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_audience_export(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_audience_export_rest_required_fields(
    request_type=analytics_data_api.GetAudienceExportRequest,
):
    transport_class = transports.BetaAnalyticsDataRestTransport

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
    ).get_audience_export._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_audience_export._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = analytics_data_api.AudienceExport()
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
            return_value = analytics_data_api.AudienceExport.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_audience_export(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_audience_export_rest_unset_required_fields():
    transport = transports.BetaAnalyticsDataRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_audience_export._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_audience_export_rest_interceptors(null_interceptor):
    transport = transports.BetaAnalyticsDataRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BetaAnalyticsDataRestInterceptor(),
    )
    client = BetaAnalyticsDataClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "post_get_audience_export"
    ) as post, mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "pre_get_audience_export"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = analytics_data_api.GetAudienceExportRequest.pb(
            analytics_data_api.GetAudienceExportRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = analytics_data_api.AudienceExport.to_json(
            analytics_data_api.AudienceExport()
        )

        request = analytics_data_api.GetAudienceExportRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = analytics_data_api.AudienceExport()

        client.get_audience_export(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_audience_export_rest_bad_request(
    transport: str = "rest", request_type=analytics_data_api.GetAudienceExportRequest
):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "properties/sample1/audienceExports/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_audience_export(request)


def test_get_audience_export_rest_flattened():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = analytics_data_api.AudienceExport()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "properties/sample1/audienceExports/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = analytics_data_api.AudienceExport.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_audience_export(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta/{name=properties/*/audienceExports/*}" % client.transport._host,
            args[1],
        )


def test_get_audience_export_rest_flattened_error(transport: str = "rest"):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_audience_export(
            analytics_data_api.GetAudienceExportRequest(),
            name="name_value",
        )


def test_get_audience_export_rest_error():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_data_api.ListAudienceExportsRequest,
        dict,
    ],
)
def test_list_audience_exports_rest(request_type):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "properties/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = analytics_data_api.ListAudienceExportsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = analytics_data_api.ListAudienceExportsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_audience_exports(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAudienceExportsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_audience_exports_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_audience_exports
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_audience_exports
        ] = mock_rpc

        request = {}
        client.list_audience_exports(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_audience_exports(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_audience_exports_rest_required_fields(
    request_type=analytics_data_api.ListAudienceExportsRequest,
):
    transport_class = transports.BetaAnalyticsDataRestTransport

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
    ).list_audience_exports._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_audience_exports._get_unset_required_fields(jsonified_request)
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

    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = analytics_data_api.ListAudienceExportsResponse()
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
            return_value = analytics_data_api.ListAudienceExportsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_audience_exports(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_audience_exports_rest_unset_required_fields():
    transport = transports.BetaAnalyticsDataRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_audience_exports._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_audience_exports_rest_interceptors(null_interceptor):
    transport = transports.BetaAnalyticsDataRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BetaAnalyticsDataRestInterceptor(),
    )
    client = BetaAnalyticsDataClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "post_list_audience_exports"
    ) as post, mock.patch.object(
        transports.BetaAnalyticsDataRestInterceptor, "pre_list_audience_exports"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = analytics_data_api.ListAudienceExportsRequest.pb(
            analytics_data_api.ListAudienceExportsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            analytics_data_api.ListAudienceExportsResponse.to_json(
                analytics_data_api.ListAudienceExportsResponse()
            )
        )

        request = analytics_data_api.ListAudienceExportsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = analytics_data_api.ListAudienceExportsResponse()

        client.list_audience_exports(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_audience_exports_rest_bad_request(
    transport: str = "rest", request_type=analytics_data_api.ListAudienceExportsRequest
):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "properties/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_audience_exports(request)


def test_list_audience_exports_rest_flattened():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = analytics_data_api.ListAudienceExportsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "properties/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = analytics_data_api.ListAudienceExportsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_audience_exports(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta/{parent=properties/*}/audienceExports" % client.transport._host,
            args[1],
        )


def test_list_audience_exports_rest_flattened_error(transport: str = "rest"):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_audience_exports(
            analytics_data_api.ListAudienceExportsRequest(),
            parent="parent_value",
        )


def test_list_audience_exports_rest_pager(transport: str = "rest"):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            analytics_data_api.ListAudienceExportsResponse(
                audience_exports=[
                    analytics_data_api.AudienceExport(),
                    analytics_data_api.AudienceExport(),
                    analytics_data_api.AudienceExport(),
                ],
                next_page_token="abc",
            ),
            analytics_data_api.ListAudienceExportsResponse(
                audience_exports=[],
                next_page_token="def",
            ),
            analytics_data_api.ListAudienceExportsResponse(
                audience_exports=[
                    analytics_data_api.AudienceExport(),
                ],
                next_page_token="ghi",
            ),
            analytics_data_api.ListAudienceExportsResponse(
                audience_exports=[
                    analytics_data_api.AudienceExport(),
                    analytics_data_api.AudienceExport(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            analytics_data_api.ListAudienceExportsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "properties/sample1"}

        pager = client.list_audience_exports(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, analytics_data_api.AudienceExport) for i in results)

        pages = list(client.list_audience_exports(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.BetaAnalyticsDataGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.BetaAnalyticsDataGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BetaAnalyticsDataClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.BetaAnalyticsDataGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = BetaAnalyticsDataClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = BetaAnalyticsDataClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.BetaAnalyticsDataGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BetaAnalyticsDataClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.BetaAnalyticsDataGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = BetaAnalyticsDataClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.BetaAnalyticsDataGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.BetaAnalyticsDataGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.BetaAnalyticsDataGrpcTransport,
        transports.BetaAnalyticsDataGrpcAsyncIOTransport,
        transports.BetaAnalyticsDataRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "rest",
    ],
)
def test_transport_kind(transport_name):
    transport = BetaAnalyticsDataClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.BetaAnalyticsDataGrpcTransport,
    )


def test_beta_analytics_data_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.BetaAnalyticsDataTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_beta_analytics_data_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.analytics.data_v1beta.services.beta_analytics_data.transports.BetaAnalyticsDataTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.BetaAnalyticsDataTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "run_report",
        "run_pivot_report",
        "batch_run_reports",
        "batch_run_pivot_reports",
        "get_metadata",
        "run_realtime_report",
        "check_compatibility",
        "create_audience_export",
        "query_audience_export",
        "get_audience_export",
        "list_audience_exports",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_beta_analytics_data_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.analytics.data_v1beta.services.beta_analytics_data.transports.BetaAnalyticsDataTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.BetaAnalyticsDataTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/analytics",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            quota_project_id="octopus",
        )


def test_beta_analytics_data_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.analytics.data_v1beta.services.beta_analytics_data.transports.BetaAnalyticsDataTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.BetaAnalyticsDataTransport()
        adc.assert_called_once()


def test_beta_analytics_data_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        BetaAnalyticsDataClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/analytics",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.BetaAnalyticsDataGrpcTransport,
        transports.BetaAnalyticsDataGrpcAsyncIOTransport,
    ],
)
def test_beta_analytics_data_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/analytics",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.BetaAnalyticsDataGrpcTransport,
        transports.BetaAnalyticsDataGrpcAsyncIOTransport,
        transports.BetaAnalyticsDataRestTransport,
    ],
)
def test_beta_analytics_data_transport_auth_gdch_credentials(transport_class):
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
        (transports.BetaAnalyticsDataGrpcTransport, grpc_helpers),
        (transports.BetaAnalyticsDataGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_beta_analytics_data_transport_create_channel(transport_class, grpc_helpers):
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
            "analyticsdata.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/analytics",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            scopes=["1", "2"],
            default_host="analyticsdata.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.BetaAnalyticsDataGrpcTransport,
        transports.BetaAnalyticsDataGrpcAsyncIOTransport,
    ],
)
def test_beta_analytics_data_grpc_transport_client_cert_source_for_mtls(
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


def test_beta_analytics_data_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.BetaAnalyticsDataRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_beta_analytics_data_rest_lro_client():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.AbstractOperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_beta_analytics_data_host_no_port(transport_name):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="analyticsdata.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "analyticsdata.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://analyticsdata.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_beta_analytics_data_host_with_port(transport_name):
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="analyticsdata.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "analyticsdata.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://analyticsdata.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_beta_analytics_data_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = BetaAnalyticsDataClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = BetaAnalyticsDataClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.run_report._session
    session2 = client2.transport.run_report._session
    assert session1 != session2
    session1 = client1.transport.run_pivot_report._session
    session2 = client2.transport.run_pivot_report._session
    assert session1 != session2
    session1 = client1.transport.batch_run_reports._session
    session2 = client2.transport.batch_run_reports._session
    assert session1 != session2
    session1 = client1.transport.batch_run_pivot_reports._session
    session2 = client2.transport.batch_run_pivot_reports._session
    assert session1 != session2
    session1 = client1.transport.get_metadata._session
    session2 = client2.transport.get_metadata._session
    assert session1 != session2
    session1 = client1.transport.run_realtime_report._session
    session2 = client2.transport.run_realtime_report._session
    assert session1 != session2
    session1 = client1.transport.check_compatibility._session
    session2 = client2.transport.check_compatibility._session
    assert session1 != session2
    session1 = client1.transport.create_audience_export._session
    session2 = client2.transport.create_audience_export._session
    assert session1 != session2
    session1 = client1.transport.query_audience_export._session
    session2 = client2.transport.query_audience_export._session
    assert session1 != session2
    session1 = client1.transport.get_audience_export._session
    session2 = client2.transport.get_audience_export._session
    assert session1 != session2
    session1 = client1.transport.list_audience_exports._session
    session2 = client2.transport.list_audience_exports._session
    assert session1 != session2


def test_beta_analytics_data_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.BetaAnalyticsDataGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_beta_analytics_data_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.BetaAnalyticsDataGrpcAsyncIOTransport(
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
        transports.BetaAnalyticsDataGrpcTransport,
        transports.BetaAnalyticsDataGrpcAsyncIOTransport,
    ],
)
def test_beta_analytics_data_transport_channel_mtls_with_client_cert_source(
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
        transports.BetaAnalyticsDataGrpcTransport,
        transports.BetaAnalyticsDataGrpcAsyncIOTransport,
    ],
)
def test_beta_analytics_data_transport_channel_mtls_with_adc(transport_class):
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


def test_beta_analytics_data_grpc_lro_client():
    client = BetaAnalyticsDataClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_beta_analytics_data_grpc_lro_async_client():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsAsyncClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_audience_export_path():
    property = "squid"
    audience_export = "clam"
    expected = "properties/{property}/audienceExports/{audience_export}".format(
        property=property,
        audience_export=audience_export,
    )
    actual = BetaAnalyticsDataClient.audience_export_path(property, audience_export)
    assert expected == actual


def test_parse_audience_export_path():
    expected = {
        "property": "whelk",
        "audience_export": "octopus",
    }
    path = BetaAnalyticsDataClient.audience_export_path(**expected)

    # Check that the path construction is reversible.
    actual = BetaAnalyticsDataClient.parse_audience_export_path(path)
    assert expected == actual


def test_metadata_path():
    property = "oyster"
    expected = "properties/{property}/metadata".format(
        property=property,
    )
    actual = BetaAnalyticsDataClient.metadata_path(property)
    assert expected == actual


def test_parse_metadata_path():
    expected = {
        "property": "nudibranch",
    }
    path = BetaAnalyticsDataClient.metadata_path(**expected)

    # Check that the path construction is reversible.
    actual = BetaAnalyticsDataClient.parse_metadata_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "cuttlefish"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = BetaAnalyticsDataClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "mussel",
    }
    path = BetaAnalyticsDataClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = BetaAnalyticsDataClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "winkle"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = BetaAnalyticsDataClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nautilus",
    }
    path = BetaAnalyticsDataClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = BetaAnalyticsDataClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "scallop"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = BetaAnalyticsDataClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "abalone",
    }
    path = BetaAnalyticsDataClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = BetaAnalyticsDataClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "squid"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = BetaAnalyticsDataClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "clam",
    }
    path = BetaAnalyticsDataClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = BetaAnalyticsDataClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "whelk"
    location = "octopus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = BetaAnalyticsDataClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
    }
    path = BetaAnalyticsDataClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = BetaAnalyticsDataClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.BetaAnalyticsDataTransport, "_prep_wrapped_messages"
    ) as prep:
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.BetaAnalyticsDataTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = BetaAnalyticsDataClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = BetaAnalyticsDataAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = BetaAnalyticsDataClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
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
        client = BetaAnalyticsDataClient(
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
        (BetaAnalyticsDataClient, transports.BetaAnalyticsDataGrpcTransport),
        (
            BetaAnalyticsDataAsyncClient,
            transports.BetaAnalyticsDataGrpcAsyncIOTransport,
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
