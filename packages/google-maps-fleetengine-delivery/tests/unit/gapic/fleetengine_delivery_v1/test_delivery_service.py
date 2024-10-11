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
from google.geo.type.types import viewport
from google.oauth2 import service_account
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.type import latlng_pb2  # type: ignore

from google.maps.fleetengine_delivery_v1.services.delivery_service import (
    DeliveryServiceAsyncClient,
    DeliveryServiceClient,
    pagers,
    transports,
)
from google.maps.fleetengine_delivery_v1.types import (
    common,
    delivery_api,
    delivery_vehicles,
    header,
    task_tracking_info,
    tasks,
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

    assert DeliveryServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        DeliveryServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        DeliveryServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        DeliveryServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DeliveryServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DeliveryServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


def test__read_environment_variables():
    assert DeliveryServiceClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert DeliveryServiceClient._read_environment_variables() == (
            True,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert DeliveryServiceClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            DeliveryServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert DeliveryServiceClient._read_environment_variables() == (
            False,
            "never",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert DeliveryServiceClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert DeliveryServiceClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            DeliveryServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert DeliveryServiceClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert DeliveryServiceClient._get_client_cert_source(None, False) is None
    assert (
        DeliveryServiceClient._get_client_cert_source(mock_provided_cert_source, False)
        is None
    )
    assert (
        DeliveryServiceClient._get_client_cert_source(mock_provided_cert_source, True)
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
                DeliveryServiceClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                DeliveryServiceClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    DeliveryServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(DeliveryServiceClient),
)
@mock.patch.object(
    DeliveryServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(DeliveryServiceAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = DeliveryServiceClient._DEFAULT_UNIVERSE
    default_endpoint = DeliveryServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = DeliveryServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        DeliveryServiceClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        DeliveryServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == DeliveryServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        DeliveryServiceClient._get_api_endpoint(None, None, default_universe, "auto")
        == default_endpoint
    )
    assert (
        DeliveryServiceClient._get_api_endpoint(None, None, default_universe, "always")
        == DeliveryServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        DeliveryServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == DeliveryServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        DeliveryServiceClient._get_api_endpoint(None, None, mock_universe, "never")
        == mock_endpoint
    )
    assert (
        DeliveryServiceClient._get_api_endpoint(None, None, default_universe, "never")
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        DeliveryServiceClient._get_api_endpoint(
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
        DeliveryServiceClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        DeliveryServiceClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        DeliveryServiceClient._get_universe_domain(None, None)
        == DeliveryServiceClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        DeliveryServiceClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (DeliveryServiceClient, transports.DeliveryServiceGrpcTransport, "grpc"),
        (DeliveryServiceClient, transports.DeliveryServiceRestTransport, "rest"),
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
        (DeliveryServiceClient, "grpc"),
        (DeliveryServiceAsyncClient, "grpc_asyncio"),
        (DeliveryServiceClient, "rest"),
    ],
)
def test_delivery_service_client_from_service_account_info(
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
            "fleetengine.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://fleetengine.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.DeliveryServiceGrpcTransport, "grpc"),
        (transports.DeliveryServiceGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.DeliveryServiceRestTransport, "rest"),
    ],
)
def test_delivery_service_client_service_account_always_use_jwt(
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
        (DeliveryServiceClient, "grpc"),
        (DeliveryServiceAsyncClient, "grpc_asyncio"),
        (DeliveryServiceClient, "rest"),
    ],
)
def test_delivery_service_client_from_service_account_file(
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
            "fleetengine.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://fleetengine.googleapis.com"
        )


def test_delivery_service_client_get_transport_class():
    transport = DeliveryServiceClient.get_transport_class()
    available_transports = [
        transports.DeliveryServiceGrpcTransport,
        transports.DeliveryServiceRestTransport,
    ]
    assert transport in available_transports

    transport = DeliveryServiceClient.get_transport_class("grpc")
    assert transport == transports.DeliveryServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (DeliveryServiceClient, transports.DeliveryServiceGrpcTransport, "grpc"),
        (
            DeliveryServiceAsyncClient,
            transports.DeliveryServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (DeliveryServiceClient, transports.DeliveryServiceRestTransport, "rest"),
    ],
)
@mock.patch.object(
    DeliveryServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(DeliveryServiceClient),
)
@mock.patch.object(
    DeliveryServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(DeliveryServiceAsyncClient),
)
def test_delivery_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(DeliveryServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(DeliveryServiceClient, "get_transport_class") as gtc:
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
            DeliveryServiceClient,
            transports.DeliveryServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            DeliveryServiceAsyncClient,
            transports.DeliveryServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            DeliveryServiceClient,
            transports.DeliveryServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            DeliveryServiceAsyncClient,
            transports.DeliveryServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            DeliveryServiceClient,
            transports.DeliveryServiceRestTransport,
            "rest",
            "true",
        ),
        (
            DeliveryServiceClient,
            transports.DeliveryServiceRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    DeliveryServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(DeliveryServiceClient),
)
@mock.patch.object(
    DeliveryServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(DeliveryServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_delivery_service_client_mtls_env_auto(
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
    "client_class", [DeliveryServiceClient, DeliveryServiceAsyncClient]
)
@mock.patch.object(
    DeliveryServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DeliveryServiceClient),
)
@mock.patch.object(
    DeliveryServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DeliveryServiceAsyncClient),
)
def test_delivery_service_client_get_mtls_endpoint_and_cert_source(client_class):
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
    "client_class", [DeliveryServiceClient, DeliveryServiceAsyncClient]
)
@mock.patch.object(
    DeliveryServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(DeliveryServiceClient),
)
@mock.patch.object(
    DeliveryServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(DeliveryServiceAsyncClient),
)
def test_delivery_service_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = DeliveryServiceClient._DEFAULT_UNIVERSE
    default_endpoint = DeliveryServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = DeliveryServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        (DeliveryServiceClient, transports.DeliveryServiceGrpcTransport, "grpc"),
        (
            DeliveryServiceAsyncClient,
            transports.DeliveryServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (DeliveryServiceClient, transports.DeliveryServiceRestTransport, "rest"),
    ],
)
def test_delivery_service_client_client_options_scopes(
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
            DeliveryServiceClient,
            transports.DeliveryServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            DeliveryServiceAsyncClient,
            transports.DeliveryServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (DeliveryServiceClient, transports.DeliveryServiceRestTransport, "rest", None),
    ],
)
def test_delivery_service_client_client_options_credentials_file(
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


def test_delivery_service_client_client_options_from_dict():
    with mock.patch(
        "google.maps.fleetengine_delivery_v1.services.delivery_service.transports.DeliveryServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = DeliveryServiceClient(
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
            DeliveryServiceClient,
            transports.DeliveryServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            DeliveryServiceAsyncClient,
            transports.DeliveryServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_delivery_service_client_create_channel_credentials_file(
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
            "fleetengine.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="fleetengine.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        delivery_api.CreateDeliveryVehicleRequest,
        dict,
    ],
)
def test_create_delivery_vehicle(request_type, transport: str = "grpc"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_delivery_vehicle), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = delivery_vehicles.DeliveryVehicle(
            name="name_value",
            navigation_status=common.DeliveryVehicleNavigationStatus.NO_GUIDANCE,
            current_route_segment=b"current_route_segment_blob",
            type_=delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO,
        )
        response = client.create_delivery_vehicle(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = delivery_api.CreateDeliveryVehicleRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, delivery_vehicles.DeliveryVehicle)
    assert response.name == "name_value"
    assert (
        response.navigation_status == common.DeliveryVehicleNavigationStatus.NO_GUIDANCE
    )
    assert response.current_route_segment == b"current_route_segment_blob"
    assert response.type_ == delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO


def test_create_delivery_vehicle_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = delivery_api.CreateDeliveryVehicleRequest(
        parent="parent_value",
        delivery_vehicle_id="delivery_vehicle_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_delivery_vehicle), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_delivery_vehicle(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == delivery_api.CreateDeliveryVehicleRequest(
            parent="parent_value",
            delivery_vehicle_id="delivery_vehicle_id_value",
        )


def test_create_delivery_vehicle_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_delivery_vehicle
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_delivery_vehicle
        ] = mock_rpc
        request = {}
        client.create_delivery_vehicle(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_delivery_vehicle(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_delivery_vehicle_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = DeliveryServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_delivery_vehicle
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_delivery_vehicle
        ] = mock_rpc

        request = {}
        await client.create_delivery_vehicle(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.create_delivery_vehicle(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_delivery_vehicle_async(
    transport: str = "grpc_asyncio",
    request_type=delivery_api.CreateDeliveryVehicleRequest,
):
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_delivery_vehicle), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_vehicles.DeliveryVehicle(
                name="name_value",
                navigation_status=common.DeliveryVehicleNavigationStatus.NO_GUIDANCE,
                current_route_segment=b"current_route_segment_blob",
                type_=delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO,
            )
        )
        response = await client.create_delivery_vehicle(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = delivery_api.CreateDeliveryVehicleRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, delivery_vehicles.DeliveryVehicle)
    assert response.name == "name_value"
    assert (
        response.navigation_status == common.DeliveryVehicleNavigationStatus.NO_GUIDANCE
    )
    assert response.current_route_segment == b"current_route_segment_blob"
    assert response.type_ == delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO


@pytest.mark.asyncio
async def test_create_delivery_vehicle_async_from_dict():
    await test_create_delivery_vehicle_async(request_type=dict)


def test_create_delivery_vehicle_flattened():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_delivery_vehicle), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = delivery_vehicles.DeliveryVehicle()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_delivery_vehicle(
            parent="parent_value",
            delivery_vehicle=delivery_vehicles.DeliveryVehicle(name="name_value"),
            delivery_vehicle_id="delivery_vehicle_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].delivery_vehicle
        mock_val = delivery_vehicles.DeliveryVehicle(name="name_value")
        assert arg == mock_val
        arg = args[0].delivery_vehicle_id
        mock_val = "delivery_vehicle_id_value"
        assert arg == mock_val


def test_create_delivery_vehicle_flattened_error():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_delivery_vehicle(
            delivery_api.CreateDeliveryVehicleRequest(),
            parent="parent_value",
            delivery_vehicle=delivery_vehicles.DeliveryVehicle(name="name_value"),
            delivery_vehicle_id="delivery_vehicle_id_value",
        )


@pytest.mark.asyncio
async def test_create_delivery_vehicle_flattened_async():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_delivery_vehicle), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = delivery_vehicles.DeliveryVehicle()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_vehicles.DeliveryVehicle()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_delivery_vehicle(
            parent="parent_value",
            delivery_vehicle=delivery_vehicles.DeliveryVehicle(name="name_value"),
            delivery_vehicle_id="delivery_vehicle_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].delivery_vehicle
        mock_val = delivery_vehicles.DeliveryVehicle(name="name_value")
        assert arg == mock_val
        arg = args[0].delivery_vehicle_id
        mock_val = "delivery_vehicle_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_delivery_vehicle_flattened_error_async():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_delivery_vehicle(
            delivery_api.CreateDeliveryVehicleRequest(),
            parent="parent_value",
            delivery_vehicle=delivery_vehicles.DeliveryVehicle(name="name_value"),
            delivery_vehicle_id="delivery_vehicle_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        delivery_api.GetDeliveryVehicleRequest,
        dict,
    ],
)
def test_get_delivery_vehicle(request_type, transport: str = "grpc"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_delivery_vehicle), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = delivery_vehicles.DeliveryVehicle(
            name="name_value",
            navigation_status=common.DeliveryVehicleNavigationStatus.NO_GUIDANCE,
            current_route_segment=b"current_route_segment_blob",
            type_=delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO,
        )
        response = client.get_delivery_vehicle(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = delivery_api.GetDeliveryVehicleRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, delivery_vehicles.DeliveryVehicle)
    assert response.name == "name_value"
    assert (
        response.navigation_status == common.DeliveryVehicleNavigationStatus.NO_GUIDANCE
    )
    assert response.current_route_segment == b"current_route_segment_blob"
    assert response.type_ == delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO


def test_get_delivery_vehicle_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = delivery_api.GetDeliveryVehicleRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_delivery_vehicle), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_delivery_vehicle(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == delivery_api.GetDeliveryVehicleRequest(
            name="name_value",
        )


def test_get_delivery_vehicle_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_delivery_vehicle in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_delivery_vehicle
        ] = mock_rpc
        request = {}
        client.get_delivery_vehicle(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_delivery_vehicle(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_delivery_vehicle_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = DeliveryServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_delivery_vehicle
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_delivery_vehicle
        ] = mock_rpc

        request = {}
        await client.get_delivery_vehicle(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_delivery_vehicle(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_delivery_vehicle_async(
    transport: str = "grpc_asyncio", request_type=delivery_api.GetDeliveryVehicleRequest
):
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_delivery_vehicle), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_vehicles.DeliveryVehicle(
                name="name_value",
                navigation_status=common.DeliveryVehicleNavigationStatus.NO_GUIDANCE,
                current_route_segment=b"current_route_segment_blob",
                type_=delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO,
            )
        )
        response = await client.get_delivery_vehicle(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = delivery_api.GetDeliveryVehicleRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, delivery_vehicles.DeliveryVehicle)
    assert response.name == "name_value"
    assert (
        response.navigation_status == common.DeliveryVehicleNavigationStatus.NO_GUIDANCE
    )
    assert response.current_route_segment == b"current_route_segment_blob"
    assert response.type_ == delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO


@pytest.mark.asyncio
async def test_get_delivery_vehicle_async_from_dict():
    await test_get_delivery_vehicle_async(request_type=dict)


def test_get_delivery_vehicle_flattened():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_delivery_vehicle), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = delivery_vehicles.DeliveryVehicle()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_delivery_vehicle(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_delivery_vehicle_flattened_error():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_delivery_vehicle(
            delivery_api.GetDeliveryVehicleRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_delivery_vehicle_flattened_async():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_delivery_vehicle), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = delivery_vehicles.DeliveryVehicle()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_vehicles.DeliveryVehicle()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_delivery_vehicle(
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
async def test_get_delivery_vehicle_flattened_error_async():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_delivery_vehicle(
            delivery_api.GetDeliveryVehicleRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        delivery_api.UpdateDeliveryVehicleRequest,
        dict,
    ],
)
def test_update_delivery_vehicle(request_type, transport: str = "grpc"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_delivery_vehicle), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = delivery_vehicles.DeliveryVehicle(
            name="name_value",
            navigation_status=common.DeliveryVehicleNavigationStatus.NO_GUIDANCE,
            current_route_segment=b"current_route_segment_blob",
            type_=delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO,
        )
        response = client.update_delivery_vehicle(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = delivery_api.UpdateDeliveryVehicleRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, delivery_vehicles.DeliveryVehicle)
    assert response.name == "name_value"
    assert (
        response.navigation_status == common.DeliveryVehicleNavigationStatus.NO_GUIDANCE
    )
    assert response.current_route_segment == b"current_route_segment_blob"
    assert response.type_ == delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO


def test_update_delivery_vehicle_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = delivery_api.UpdateDeliveryVehicleRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_delivery_vehicle), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_delivery_vehicle(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == delivery_api.UpdateDeliveryVehicleRequest()


def test_update_delivery_vehicle_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_delivery_vehicle
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_delivery_vehicle
        ] = mock_rpc
        request = {}
        client.update_delivery_vehicle(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_delivery_vehicle(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_delivery_vehicle_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = DeliveryServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_delivery_vehicle
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_delivery_vehicle
        ] = mock_rpc

        request = {}
        await client.update_delivery_vehicle(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.update_delivery_vehicle(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_delivery_vehicle_async(
    transport: str = "grpc_asyncio",
    request_type=delivery_api.UpdateDeliveryVehicleRequest,
):
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_delivery_vehicle), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_vehicles.DeliveryVehicle(
                name="name_value",
                navigation_status=common.DeliveryVehicleNavigationStatus.NO_GUIDANCE,
                current_route_segment=b"current_route_segment_blob",
                type_=delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO,
            )
        )
        response = await client.update_delivery_vehicle(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = delivery_api.UpdateDeliveryVehicleRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, delivery_vehicles.DeliveryVehicle)
    assert response.name == "name_value"
    assert (
        response.navigation_status == common.DeliveryVehicleNavigationStatus.NO_GUIDANCE
    )
    assert response.current_route_segment == b"current_route_segment_blob"
    assert response.type_ == delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO


@pytest.mark.asyncio
async def test_update_delivery_vehicle_async_from_dict():
    await test_update_delivery_vehicle_async(request_type=dict)


def test_update_delivery_vehicle_flattened():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_delivery_vehicle), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = delivery_vehicles.DeliveryVehicle()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_delivery_vehicle(
            delivery_vehicle=delivery_vehicles.DeliveryVehicle(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].delivery_vehicle
        mock_val = delivery_vehicles.DeliveryVehicle(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_delivery_vehicle_flattened_error():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_delivery_vehicle(
            delivery_api.UpdateDeliveryVehicleRequest(),
            delivery_vehicle=delivery_vehicles.DeliveryVehicle(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_delivery_vehicle_flattened_async():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_delivery_vehicle), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = delivery_vehicles.DeliveryVehicle()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_vehicles.DeliveryVehicle()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_delivery_vehicle(
            delivery_vehicle=delivery_vehicles.DeliveryVehicle(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].delivery_vehicle
        mock_val = delivery_vehicles.DeliveryVehicle(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_delivery_vehicle_flattened_error_async():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_delivery_vehicle(
            delivery_api.UpdateDeliveryVehicleRequest(),
            delivery_vehicle=delivery_vehicles.DeliveryVehicle(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        delivery_api.BatchCreateTasksRequest,
        dict,
    ],
)
def test_batch_create_tasks(request_type, transport: str = "grpc"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tasks), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = delivery_api.BatchCreateTasksResponse()
        response = client.batch_create_tasks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = delivery_api.BatchCreateTasksRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, delivery_api.BatchCreateTasksResponse)


def test_batch_create_tasks_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = delivery_api.BatchCreateTasksRequest(
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tasks), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.batch_create_tasks(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == delivery_api.BatchCreateTasksRequest(
            parent="parent_value",
        )


def test_batch_create_tasks_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.batch_create_tasks in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.batch_create_tasks
        ] = mock_rpc
        request = {}
        client.batch_create_tasks(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.batch_create_tasks(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_batch_create_tasks_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = DeliveryServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.batch_create_tasks
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.batch_create_tasks
        ] = mock_rpc

        request = {}
        await client.batch_create_tasks(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.batch_create_tasks(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_batch_create_tasks_async(
    transport: str = "grpc_asyncio", request_type=delivery_api.BatchCreateTasksRequest
):
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tasks), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_api.BatchCreateTasksResponse()
        )
        response = await client.batch_create_tasks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = delivery_api.BatchCreateTasksRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, delivery_api.BatchCreateTasksResponse)


@pytest.mark.asyncio
async def test_batch_create_tasks_async_from_dict():
    await test_batch_create_tasks_async(request_type=dict)


@pytest.mark.parametrize(
    "request_type",
    [
        delivery_api.CreateTaskRequest,
        dict,
    ],
)
def test_create_task(request_type, transport: str = "grpc"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tasks.Task(
            name="name_value",
            type_=tasks.Task.Type.PICKUP,
            state=tasks.Task.State.OPEN,
            task_outcome=tasks.Task.TaskOutcome.SUCCEEDED,
            task_outcome_location_source=tasks.Task.TaskOutcomeLocationSource.PROVIDER,
            tracking_id="tracking_id_value",
            delivery_vehicle_id="delivery_vehicle_id_value",
        )
        response = client.create_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = delivery_api.CreateTaskRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, tasks.Task)
    assert response.name == "name_value"
    assert response.type_ == tasks.Task.Type.PICKUP
    assert response.state == tasks.Task.State.OPEN
    assert response.task_outcome == tasks.Task.TaskOutcome.SUCCEEDED
    assert (
        response.task_outcome_location_source
        == tasks.Task.TaskOutcomeLocationSource.PROVIDER
    )
    assert response.tracking_id == "tracking_id_value"
    assert response.delivery_vehicle_id == "delivery_vehicle_id_value"


def test_create_task_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = delivery_api.CreateTaskRequest(
        parent="parent_value",
        task_id="task_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_task), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_task(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == delivery_api.CreateTaskRequest(
            parent="parent_value",
            task_id="task_id_value",
        )


def test_create_task_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_task in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.create_task] = mock_rpc
        request = {}
        client.create_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_task(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_task_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = DeliveryServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_task
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_task
        ] = mock_rpc

        request = {}
        await client.create_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.create_task(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_task_async(
    transport: str = "grpc_asyncio", request_type=delivery_api.CreateTaskRequest
):
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tasks.Task(
                name="name_value",
                type_=tasks.Task.Type.PICKUP,
                state=tasks.Task.State.OPEN,
                task_outcome=tasks.Task.TaskOutcome.SUCCEEDED,
                task_outcome_location_source=tasks.Task.TaskOutcomeLocationSource.PROVIDER,
                tracking_id="tracking_id_value",
                delivery_vehicle_id="delivery_vehicle_id_value",
            )
        )
        response = await client.create_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = delivery_api.CreateTaskRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, tasks.Task)
    assert response.name == "name_value"
    assert response.type_ == tasks.Task.Type.PICKUP
    assert response.state == tasks.Task.State.OPEN
    assert response.task_outcome == tasks.Task.TaskOutcome.SUCCEEDED
    assert (
        response.task_outcome_location_source
        == tasks.Task.TaskOutcomeLocationSource.PROVIDER
    )
    assert response.tracking_id == "tracking_id_value"
    assert response.delivery_vehicle_id == "delivery_vehicle_id_value"


@pytest.mark.asyncio
async def test_create_task_async_from_dict():
    await test_create_task_async(request_type=dict)


def test_create_task_flattened():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tasks.Task()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_task(
            parent="parent_value",
            task=tasks.Task(name="name_value"),
            task_id="task_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].task
        mock_val = tasks.Task(name="name_value")
        assert arg == mock_val
        arg = args[0].task_id
        mock_val = "task_id_value"
        assert arg == mock_val


def test_create_task_flattened_error():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_task(
            delivery_api.CreateTaskRequest(),
            parent="parent_value",
            task=tasks.Task(name="name_value"),
            task_id="task_id_value",
        )


@pytest.mark.asyncio
async def test_create_task_flattened_async():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tasks.Task()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tasks.Task())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_task(
            parent="parent_value",
            task=tasks.Task(name="name_value"),
            task_id="task_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].task
        mock_val = tasks.Task(name="name_value")
        assert arg == mock_val
        arg = args[0].task_id
        mock_val = "task_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_task_flattened_error_async():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_task(
            delivery_api.CreateTaskRequest(),
            parent="parent_value",
            task=tasks.Task(name="name_value"),
            task_id="task_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        delivery_api.GetTaskRequest,
        dict,
    ],
)
def test_get_task(request_type, transport: str = "grpc"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tasks.Task(
            name="name_value",
            type_=tasks.Task.Type.PICKUP,
            state=tasks.Task.State.OPEN,
            task_outcome=tasks.Task.TaskOutcome.SUCCEEDED,
            task_outcome_location_source=tasks.Task.TaskOutcomeLocationSource.PROVIDER,
            tracking_id="tracking_id_value",
            delivery_vehicle_id="delivery_vehicle_id_value",
        )
        response = client.get_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = delivery_api.GetTaskRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, tasks.Task)
    assert response.name == "name_value"
    assert response.type_ == tasks.Task.Type.PICKUP
    assert response.state == tasks.Task.State.OPEN
    assert response.task_outcome == tasks.Task.TaskOutcome.SUCCEEDED
    assert (
        response.task_outcome_location_source
        == tasks.Task.TaskOutcomeLocationSource.PROVIDER
    )
    assert response.tracking_id == "tracking_id_value"
    assert response.delivery_vehicle_id == "delivery_vehicle_id_value"


def test_get_task_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = delivery_api.GetTaskRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_task), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_task(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == delivery_api.GetTaskRequest(
            name="name_value",
        )


def test_get_task_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_task in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_task] = mock_rpc
        request = {}
        client.get_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_task(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_task_async_use_cached_wrapped_rpc(transport: str = "grpc_asyncio"):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = DeliveryServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_task
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_task
        ] = mock_rpc

        request = {}
        await client.get_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_task(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_task_async(
    transport: str = "grpc_asyncio", request_type=delivery_api.GetTaskRequest
):
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tasks.Task(
                name="name_value",
                type_=tasks.Task.Type.PICKUP,
                state=tasks.Task.State.OPEN,
                task_outcome=tasks.Task.TaskOutcome.SUCCEEDED,
                task_outcome_location_source=tasks.Task.TaskOutcomeLocationSource.PROVIDER,
                tracking_id="tracking_id_value",
                delivery_vehicle_id="delivery_vehicle_id_value",
            )
        )
        response = await client.get_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = delivery_api.GetTaskRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, tasks.Task)
    assert response.name == "name_value"
    assert response.type_ == tasks.Task.Type.PICKUP
    assert response.state == tasks.Task.State.OPEN
    assert response.task_outcome == tasks.Task.TaskOutcome.SUCCEEDED
    assert (
        response.task_outcome_location_source
        == tasks.Task.TaskOutcomeLocationSource.PROVIDER
    )
    assert response.tracking_id == "tracking_id_value"
    assert response.delivery_vehicle_id == "delivery_vehicle_id_value"


@pytest.mark.asyncio
async def test_get_task_async_from_dict():
    await test_get_task_async(request_type=dict)


def test_get_task_flattened():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tasks.Task()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_task(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_task_flattened_error():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_task(
            delivery_api.GetTaskRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_task_flattened_async():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tasks.Task()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tasks.Task())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_task(
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
async def test_get_task_flattened_error_async():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_task(
            delivery_api.GetTaskRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        delivery_api.UpdateTaskRequest,
        dict,
    ],
)
def test_update_task(request_type, transport: str = "grpc"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tasks.Task(
            name="name_value",
            type_=tasks.Task.Type.PICKUP,
            state=tasks.Task.State.OPEN,
            task_outcome=tasks.Task.TaskOutcome.SUCCEEDED,
            task_outcome_location_source=tasks.Task.TaskOutcomeLocationSource.PROVIDER,
            tracking_id="tracking_id_value",
            delivery_vehicle_id="delivery_vehicle_id_value",
        )
        response = client.update_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = delivery_api.UpdateTaskRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, tasks.Task)
    assert response.name == "name_value"
    assert response.type_ == tasks.Task.Type.PICKUP
    assert response.state == tasks.Task.State.OPEN
    assert response.task_outcome == tasks.Task.TaskOutcome.SUCCEEDED
    assert (
        response.task_outcome_location_source
        == tasks.Task.TaskOutcomeLocationSource.PROVIDER
    )
    assert response.tracking_id == "tracking_id_value"
    assert response.delivery_vehicle_id == "delivery_vehicle_id_value"


def test_update_task_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = delivery_api.UpdateTaskRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_task), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_task(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == delivery_api.UpdateTaskRequest()


def test_update_task_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.update_task in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.update_task] = mock_rpc
        request = {}
        client.update_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_task(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_task_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = DeliveryServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_task
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_task
        ] = mock_rpc

        request = {}
        await client.update_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.update_task(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_task_async(
    transport: str = "grpc_asyncio", request_type=delivery_api.UpdateTaskRequest
):
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tasks.Task(
                name="name_value",
                type_=tasks.Task.Type.PICKUP,
                state=tasks.Task.State.OPEN,
                task_outcome=tasks.Task.TaskOutcome.SUCCEEDED,
                task_outcome_location_source=tasks.Task.TaskOutcomeLocationSource.PROVIDER,
                tracking_id="tracking_id_value",
                delivery_vehicle_id="delivery_vehicle_id_value",
            )
        )
        response = await client.update_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = delivery_api.UpdateTaskRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, tasks.Task)
    assert response.name == "name_value"
    assert response.type_ == tasks.Task.Type.PICKUP
    assert response.state == tasks.Task.State.OPEN
    assert response.task_outcome == tasks.Task.TaskOutcome.SUCCEEDED
    assert (
        response.task_outcome_location_source
        == tasks.Task.TaskOutcomeLocationSource.PROVIDER
    )
    assert response.tracking_id == "tracking_id_value"
    assert response.delivery_vehicle_id == "delivery_vehicle_id_value"


@pytest.mark.asyncio
async def test_update_task_async_from_dict():
    await test_update_task_async(request_type=dict)


def test_update_task_flattened():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tasks.Task()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_task(
            task=tasks.Task(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].task
        mock_val = tasks.Task(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_task_flattened_error():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_task(
            delivery_api.UpdateTaskRequest(),
            task=tasks.Task(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_task_flattened_async():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tasks.Task()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tasks.Task())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_task(
            task=tasks.Task(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].task
        mock_val = tasks.Task(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_task_flattened_error_async():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_task(
            delivery_api.UpdateTaskRequest(),
            task=tasks.Task(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        delivery_api.ListTasksRequest,
        dict,
    ],
)
def test_list_tasks(request_type, transport: str = "grpc"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = delivery_api.ListTasksResponse(
            next_page_token="next_page_token_value",
            total_size=1086,
        )
        response = client.list_tasks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = delivery_api.ListTasksRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTasksPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


def test_list_tasks_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = delivery_api.ListTasksRequest(
        parent="parent_value",
        page_token="page_token_value",
        filter="filter_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_tasks(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == delivery_api.ListTasksRequest(
            parent="parent_value",
            page_token="page_token_value",
            filter="filter_value",
        )


def test_list_tasks_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_tasks in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_tasks] = mock_rpc
        request = {}
        client.list_tasks(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_tasks(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_tasks_async_use_cached_wrapped_rpc(transport: str = "grpc_asyncio"):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = DeliveryServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_tasks
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_tasks
        ] = mock_rpc

        request = {}
        await client.list_tasks(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_tasks(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_tasks_async(
    transport: str = "grpc_asyncio", request_type=delivery_api.ListTasksRequest
):
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_api.ListTasksResponse(
                next_page_token="next_page_token_value",
                total_size=1086,
            )
        )
        response = await client.list_tasks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = delivery_api.ListTasksRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTasksAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


@pytest.mark.asyncio
async def test_list_tasks_async_from_dict():
    await test_list_tasks_async(request_type=dict)


def test_list_tasks_flattened():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = delivery_api.ListTasksResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_tasks(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_tasks_flattened_error():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tasks(
            delivery_api.ListTasksRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_tasks_flattened_async():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = delivery_api.ListTasksResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_api.ListTasksResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_tasks(
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
async def test_list_tasks_flattened_error_async():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_tasks(
            delivery_api.ListTasksRequest(),
            parent="parent_value",
        )


def test_list_tasks_pager(transport_name: str = "grpc"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            delivery_api.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                    tasks.Task(),
                    tasks.Task(),
                ],
                next_page_token="abc",
            ),
            delivery_api.ListTasksResponse(
                tasks=[],
                next_page_token="def",
            ),
            delivery_api.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                ],
                next_page_token="ghi",
            ),
            delivery_api.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                    tasks.Task(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        pager = client.list_tasks(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tasks.Task) for i in results)


def test_list_tasks_pages(transport_name: str = "grpc"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            delivery_api.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                    tasks.Task(),
                    tasks.Task(),
                ],
                next_page_token="abc",
            ),
            delivery_api.ListTasksResponse(
                tasks=[],
                next_page_token="def",
            ),
            delivery_api.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                ],
                next_page_token="ghi",
            ),
            delivery_api.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                    tasks.Task(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_tasks(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_tasks_async_pager():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tasks), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            delivery_api.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                    tasks.Task(),
                    tasks.Task(),
                ],
                next_page_token="abc",
            ),
            delivery_api.ListTasksResponse(
                tasks=[],
                next_page_token="def",
            ),
            delivery_api.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                ],
                next_page_token="ghi",
            ),
            delivery_api.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                    tasks.Task(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_tasks(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, tasks.Task) for i in responses)


@pytest.mark.asyncio
async def test_list_tasks_async_pages():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tasks), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            delivery_api.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                    tasks.Task(),
                    tasks.Task(),
                ],
                next_page_token="abc",
            ),
            delivery_api.ListTasksResponse(
                tasks=[],
                next_page_token="def",
            ),
            delivery_api.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                ],
                next_page_token="ghi",
            ),
            delivery_api.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                    tasks.Task(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_tasks(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        delivery_api.GetTaskTrackingInfoRequest,
        dict,
    ],
)
def test_get_task_tracking_info(request_type, transport: str = "grpc"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_task_tracking_info), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = task_tracking_info.TaskTrackingInfo(
            name="name_value",
            tracking_id="tracking_id_value",
            state=tasks.Task.State.OPEN,
            task_outcome=tasks.Task.TaskOutcome.SUCCEEDED,
        )
        response = client.get_task_tracking_info(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = delivery_api.GetTaskTrackingInfoRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, task_tracking_info.TaskTrackingInfo)
    assert response.name == "name_value"
    assert response.tracking_id == "tracking_id_value"
    assert response.state == tasks.Task.State.OPEN
    assert response.task_outcome == tasks.Task.TaskOutcome.SUCCEEDED


def test_get_task_tracking_info_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = delivery_api.GetTaskTrackingInfoRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_task_tracking_info), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_task_tracking_info(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == delivery_api.GetTaskTrackingInfoRequest(
            name="name_value",
        )


def test_get_task_tracking_info_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_task_tracking_info
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_task_tracking_info
        ] = mock_rpc
        request = {}
        client.get_task_tracking_info(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_task_tracking_info(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_task_tracking_info_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = DeliveryServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_task_tracking_info
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_task_tracking_info
        ] = mock_rpc

        request = {}
        await client.get_task_tracking_info(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_task_tracking_info(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_task_tracking_info_async(
    transport: str = "grpc_asyncio",
    request_type=delivery_api.GetTaskTrackingInfoRequest,
):
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_task_tracking_info), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            task_tracking_info.TaskTrackingInfo(
                name="name_value",
                tracking_id="tracking_id_value",
                state=tasks.Task.State.OPEN,
                task_outcome=tasks.Task.TaskOutcome.SUCCEEDED,
            )
        )
        response = await client.get_task_tracking_info(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = delivery_api.GetTaskTrackingInfoRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, task_tracking_info.TaskTrackingInfo)
    assert response.name == "name_value"
    assert response.tracking_id == "tracking_id_value"
    assert response.state == tasks.Task.State.OPEN
    assert response.task_outcome == tasks.Task.TaskOutcome.SUCCEEDED


@pytest.mark.asyncio
async def test_get_task_tracking_info_async_from_dict():
    await test_get_task_tracking_info_async(request_type=dict)


def test_get_task_tracking_info_flattened():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_task_tracking_info), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = task_tracking_info.TaskTrackingInfo()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_task_tracking_info(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_task_tracking_info_flattened_error():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_task_tracking_info(
            delivery_api.GetTaskTrackingInfoRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_task_tracking_info_flattened_async():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_task_tracking_info), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = task_tracking_info.TaskTrackingInfo()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            task_tracking_info.TaskTrackingInfo()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_task_tracking_info(
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
async def test_get_task_tracking_info_flattened_error_async():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_task_tracking_info(
            delivery_api.GetTaskTrackingInfoRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        delivery_api.ListDeliveryVehiclesRequest,
        dict,
    ],
)
def test_list_delivery_vehicles(request_type, transport: str = "grpc"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_vehicles), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = delivery_api.ListDeliveryVehiclesResponse(
            next_page_token="next_page_token_value",
            total_size=1086,
        )
        response = client.list_delivery_vehicles(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = delivery_api.ListDeliveryVehiclesRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDeliveryVehiclesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


def test_list_delivery_vehicles_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = delivery_api.ListDeliveryVehiclesRequest(
        parent="parent_value",
        page_token="page_token_value",
        filter="filter_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_vehicles), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_delivery_vehicles(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == delivery_api.ListDeliveryVehiclesRequest(
            parent="parent_value",
            page_token="page_token_value",
            filter="filter_value",
        )


def test_list_delivery_vehicles_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_delivery_vehicles
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_delivery_vehicles
        ] = mock_rpc
        request = {}
        client.list_delivery_vehicles(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_delivery_vehicles(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_delivery_vehicles_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = DeliveryServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_delivery_vehicles
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_delivery_vehicles
        ] = mock_rpc

        request = {}
        await client.list_delivery_vehicles(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_delivery_vehicles(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_delivery_vehicles_async(
    transport: str = "grpc_asyncio",
    request_type=delivery_api.ListDeliveryVehiclesRequest,
):
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_vehicles), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_api.ListDeliveryVehiclesResponse(
                next_page_token="next_page_token_value",
                total_size=1086,
            )
        )
        response = await client.list_delivery_vehicles(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = delivery_api.ListDeliveryVehiclesRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDeliveryVehiclesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


@pytest.mark.asyncio
async def test_list_delivery_vehicles_async_from_dict():
    await test_list_delivery_vehicles_async(request_type=dict)


def test_list_delivery_vehicles_flattened():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_vehicles), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = delivery_api.ListDeliveryVehiclesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_delivery_vehicles(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_delivery_vehicles_flattened_error():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_delivery_vehicles(
            delivery_api.ListDeliveryVehiclesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_delivery_vehicles_flattened_async():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_vehicles), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = delivery_api.ListDeliveryVehiclesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_api.ListDeliveryVehiclesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_delivery_vehicles(
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
async def test_list_delivery_vehicles_flattened_error_async():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_delivery_vehicles(
            delivery_api.ListDeliveryVehiclesRequest(),
            parent="parent_value",
        )


def test_list_delivery_vehicles_pager(transport_name: str = "grpc"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_vehicles), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            delivery_api.ListDeliveryVehiclesResponse(
                delivery_vehicles=[
                    delivery_vehicles.DeliveryVehicle(),
                    delivery_vehicles.DeliveryVehicle(),
                    delivery_vehicles.DeliveryVehicle(),
                ],
                next_page_token="abc",
            ),
            delivery_api.ListDeliveryVehiclesResponse(
                delivery_vehicles=[],
                next_page_token="def",
            ),
            delivery_api.ListDeliveryVehiclesResponse(
                delivery_vehicles=[
                    delivery_vehicles.DeliveryVehicle(),
                ],
                next_page_token="ghi",
            ),
            delivery_api.ListDeliveryVehiclesResponse(
                delivery_vehicles=[
                    delivery_vehicles.DeliveryVehicle(),
                    delivery_vehicles.DeliveryVehicle(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        pager = client.list_delivery_vehicles(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, delivery_vehicles.DeliveryVehicle) for i in results)


def test_list_delivery_vehicles_pages(transport_name: str = "grpc"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_vehicles), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            delivery_api.ListDeliveryVehiclesResponse(
                delivery_vehicles=[
                    delivery_vehicles.DeliveryVehicle(),
                    delivery_vehicles.DeliveryVehicle(),
                    delivery_vehicles.DeliveryVehicle(),
                ],
                next_page_token="abc",
            ),
            delivery_api.ListDeliveryVehiclesResponse(
                delivery_vehicles=[],
                next_page_token="def",
            ),
            delivery_api.ListDeliveryVehiclesResponse(
                delivery_vehicles=[
                    delivery_vehicles.DeliveryVehicle(),
                ],
                next_page_token="ghi",
            ),
            delivery_api.ListDeliveryVehiclesResponse(
                delivery_vehicles=[
                    delivery_vehicles.DeliveryVehicle(),
                    delivery_vehicles.DeliveryVehicle(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_delivery_vehicles(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_delivery_vehicles_async_pager():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_vehicles),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            delivery_api.ListDeliveryVehiclesResponse(
                delivery_vehicles=[
                    delivery_vehicles.DeliveryVehicle(),
                    delivery_vehicles.DeliveryVehicle(),
                    delivery_vehicles.DeliveryVehicle(),
                ],
                next_page_token="abc",
            ),
            delivery_api.ListDeliveryVehiclesResponse(
                delivery_vehicles=[],
                next_page_token="def",
            ),
            delivery_api.ListDeliveryVehiclesResponse(
                delivery_vehicles=[
                    delivery_vehicles.DeliveryVehicle(),
                ],
                next_page_token="ghi",
            ),
            delivery_api.ListDeliveryVehiclesResponse(
                delivery_vehicles=[
                    delivery_vehicles.DeliveryVehicle(),
                    delivery_vehicles.DeliveryVehicle(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_delivery_vehicles(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, delivery_vehicles.DeliveryVehicle) for i in responses)


@pytest.mark.asyncio
async def test_list_delivery_vehicles_async_pages():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_vehicles),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            delivery_api.ListDeliveryVehiclesResponse(
                delivery_vehicles=[
                    delivery_vehicles.DeliveryVehicle(),
                    delivery_vehicles.DeliveryVehicle(),
                    delivery_vehicles.DeliveryVehicle(),
                ],
                next_page_token="abc",
            ),
            delivery_api.ListDeliveryVehiclesResponse(
                delivery_vehicles=[],
                next_page_token="def",
            ),
            delivery_api.ListDeliveryVehiclesResponse(
                delivery_vehicles=[
                    delivery_vehicles.DeliveryVehicle(),
                ],
                next_page_token="ghi",
            ),
            delivery_api.ListDeliveryVehiclesResponse(
                delivery_vehicles=[
                    delivery_vehicles.DeliveryVehicle(),
                    delivery_vehicles.DeliveryVehicle(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_delivery_vehicles(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_create_delivery_vehicle_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_delivery_vehicle
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_delivery_vehicle
        ] = mock_rpc

        request = {}
        client.create_delivery_vehicle(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_delivery_vehicle(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_delivery_vehicle_rest_required_fields(
    request_type=delivery_api.CreateDeliveryVehicleRequest,
):
    transport_class = transports.DeliveryServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["delivery_vehicle_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped
    assert "deliveryVehicleId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_delivery_vehicle._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "deliveryVehicleId" in jsonified_request
    assert jsonified_request["deliveryVehicleId"] == request_init["delivery_vehicle_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["deliveryVehicleId"] = "delivery_vehicle_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_delivery_vehicle._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "delivery_vehicle_id",
            "header",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "deliveryVehicleId" in jsonified_request
    assert jsonified_request["deliveryVehicleId"] == "delivery_vehicle_id_value"

    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = delivery_vehicles.DeliveryVehicle()
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
            return_value = delivery_vehicles.DeliveryVehicle.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_delivery_vehicle(request)

            expected_params = [
                (
                    "deliveryVehicleId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_delivery_vehicle_rest_unset_required_fields():
    transport = transports.DeliveryServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_delivery_vehicle._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "deliveryVehicleId",
                "header",
            )
        )
        & set(
            (
                "parent",
                "deliveryVehicleId",
                "deliveryVehicle",
            )
        )
    )


def test_create_delivery_vehicle_rest_flattened():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = delivery_vehicles.DeliveryVehicle()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "providers/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            delivery_vehicle=delivery_vehicles.DeliveryVehicle(name="name_value"),
            delivery_vehicle_id="delivery_vehicle_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = delivery_vehicles.DeliveryVehicle.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_delivery_vehicle(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=providers/*}/deliveryVehicles" % client.transport._host,
            args[1],
        )


def test_create_delivery_vehicle_rest_flattened_error(transport: str = "rest"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_delivery_vehicle(
            delivery_api.CreateDeliveryVehicleRequest(),
            parent="parent_value",
            delivery_vehicle=delivery_vehicles.DeliveryVehicle(name="name_value"),
            delivery_vehicle_id="delivery_vehicle_id_value",
        )


def test_get_delivery_vehicle_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_delivery_vehicle in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_delivery_vehicle
        ] = mock_rpc

        request = {}
        client.get_delivery_vehicle(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_delivery_vehicle(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_delivery_vehicle_rest_required_fields(
    request_type=delivery_api.GetDeliveryVehicleRequest,
):
    transport_class = transports.DeliveryServiceRestTransport

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
    ).get_delivery_vehicle._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_delivery_vehicle._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("header",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = delivery_vehicles.DeliveryVehicle()
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
            return_value = delivery_vehicles.DeliveryVehicle.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_delivery_vehicle(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_delivery_vehicle_rest_unset_required_fields():
    transport = transports.DeliveryServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_delivery_vehicle._get_unset_required_fields({})
    assert set(unset_fields) == (set(("header",)) & set(("name",)))


def test_get_delivery_vehicle_rest_flattened():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = delivery_vehicles.DeliveryVehicle()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "providers/sample1/deliveryVehicles/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = delivery_vehicles.DeliveryVehicle.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_delivery_vehicle(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=providers/*/deliveryVehicles/*}" % client.transport._host,
            args[1],
        )


def test_get_delivery_vehicle_rest_flattened_error(transport: str = "rest"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_delivery_vehicle(
            delivery_api.GetDeliveryVehicleRequest(),
            name="name_value",
        )


def test_update_delivery_vehicle_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_delivery_vehicle
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_delivery_vehicle
        ] = mock_rpc

        request = {}
        client.update_delivery_vehicle(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_delivery_vehicle(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_update_delivery_vehicle_rest_required_fields(
    request_type=delivery_api.UpdateDeliveryVehicleRequest,
):
    transport_class = transports.DeliveryServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_delivery_vehicle._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_delivery_vehicle._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "header",
            "update_mask",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = delivery_vehicles.DeliveryVehicle()
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
            return_value = delivery_vehicles.DeliveryVehicle.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_delivery_vehicle(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_delivery_vehicle_rest_unset_required_fields():
    transport = transports.DeliveryServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_delivery_vehicle._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "header",
                "updateMask",
            )
        )
        & set(
            (
                "deliveryVehicle",
                "updateMask",
            )
        )
    )


def test_update_delivery_vehicle_rest_flattened():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = delivery_vehicles.DeliveryVehicle()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "delivery_vehicle": {"name": "providers/sample1/deliveryVehicles/sample2"}
        }

        # get truthy value for each flattened field
        mock_args = dict(
            delivery_vehicle=delivery_vehicles.DeliveryVehicle(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = delivery_vehicles.DeliveryVehicle.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_delivery_vehicle(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{delivery_vehicle.name=providers/*/deliveryVehicles/*}"
            % client.transport._host,
            args[1],
        )


def test_update_delivery_vehicle_rest_flattened_error(transport: str = "rest"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_delivery_vehicle(
            delivery_api.UpdateDeliveryVehicleRequest(),
            delivery_vehicle=delivery_vehicles.DeliveryVehicle(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_batch_create_tasks_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.batch_create_tasks in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.batch_create_tasks
        ] = mock_rpc

        request = {}
        client.batch_create_tasks(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.batch_create_tasks(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_batch_create_tasks_rest_required_fields(
    request_type=delivery_api.BatchCreateTasksRequest,
):
    transport_class = transports.DeliveryServiceRestTransport

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
    ).batch_create_tasks._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).batch_create_tasks._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = delivery_api.BatchCreateTasksResponse()
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
            return_value = delivery_api.BatchCreateTasksResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.batch_create_tasks(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_batch_create_tasks_rest_unset_required_fields():
    transport = transports.DeliveryServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.batch_create_tasks._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "requests",
            )
        )
    )


def test_create_task_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_task in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.create_task] = mock_rpc

        request = {}
        client.create_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_task(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_task_rest_required_fields(request_type=delivery_api.CreateTaskRequest):
    transport_class = transports.DeliveryServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["task_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped
    assert "taskId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_task._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "taskId" in jsonified_request
    assert jsonified_request["taskId"] == request_init["task_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["taskId"] = "task_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_task._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "header",
            "task_id",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "taskId" in jsonified_request
    assert jsonified_request["taskId"] == "task_id_value"

    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tasks.Task()
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
            return_value = tasks.Task.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_task(request)

            expected_params = [
                (
                    "taskId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_task_rest_unset_required_fields():
    transport = transports.DeliveryServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_task._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "header",
                "taskId",
            )
        )
        & set(
            (
                "parent",
                "taskId",
                "task",
            )
        )
    )


def test_create_task_rest_flattened():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tasks.Task()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "providers/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            task=tasks.Task(name="name_value"),
            task_id="task_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tasks.Task.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_task(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=providers/*}/tasks" % client.transport._host, args[1]
        )


def test_create_task_rest_flattened_error(transport: str = "rest"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_task(
            delivery_api.CreateTaskRequest(),
            parent="parent_value",
            task=tasks.Task(name="name_value"),
            task_id="task_id_value",
        )


def test_get_task_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_task in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_task] = mock_rpc

        request = {}
        client.get_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_task(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_task_rest_required_fields(request_type=delivery_api.GetTaskRequest):
    transport_class = transports.DeliveryServiceRestTransport

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
    ).get_task._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_task._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("header",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tasks.Task()
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
            return_value = tasks.Task.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_task(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_task_rest_unset_required_fields():
    transport = transports.DeliveryServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_task._get_unset_required_fields({})
    assert set(unset_fields) == (set(("header",)) & set(("name",)))


def test_get_task_rest_flattened():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tasks.Task()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "providers/sample1/tasks/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tasks.Task.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_task(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=providers/*/tasks/*}" % client.transport._host, args[1]
        )


def test_get_task_rest_flattened_error(transport: str = "rest"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_task(
            delivery_api.GetTaskRequest(),
            name="name_value",
        )


def test_update_task_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.update_task in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.update_task] = mock_rpc

        request = {}
        client.update_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_task(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_update_task_rest_required_fields(request_type=delivery_api.UpdateTaskRequest):
    transport_class = transports.DeliveryServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_task._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_task._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "header",
            "update_mask",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tasks.Task()
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
            return_value = tasks.Task.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_task(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_task_rest_unset_required_fields():
    transport = transports.DeliveryServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_task._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "header",
                "updateMask",
            )
        )
        & set(
            (
                "task",
                "updateMask",
            )
        )
    )


def test_update_task_rest_flattened():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tasks.Task()

        # get arguments that satisfy an http rule for this method
        sample_request = {"task": {"name": "providers/sample1/tasks/sample2"}}

        # get truthy value for each flattened field
        mock_args = dict(
            task=tasks.Task(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tasks.Task.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_task(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{task.name=providers/*/tasks/*}" % client.transport._host, args[1]
        )


def test_update_task_rest_flattened_error(transport: str = "rest"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_task(
            delivery_api.UpdateTaskRequest(),
            task=tasks.Task(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_list_tasks_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_tasks in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_tasks] = mock_rpc

        request = {}
        client.list_tasks(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_tasks(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_tasks_rest_required_fields(request_type=delivery_api.ListTasksRequest):
    transport_class = transports.DeliveryServiceRestTransport

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
    ).list_tasks._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_tasks._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "header",
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = delivery_api.ListTasksResponse()
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
            return_value = delivery_api.ListTasksResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_tasks(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_tasks_rest_unset_required_fields():
    transport = transports.DeliveryServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_tasks._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "header",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


def test_list_tasks_rest_flattened():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = delivery_api.ListTasksResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "providers/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = delivery_api.ListTasksResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_tasks(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=providers/*}/tasks" % client.transport._host, args[1]
        )


def test_list_tasks_rest_flattened_error(transport: str = "rest"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tasks(
            delivery_api.ListTasksRequest(),
            parent="parent_value",
        )


def test_list_tasks_rest_pager(transport: str = "rest"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            delivery_api.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                    tasks.Task(),
                    tasks.Task(),
                ],
                next_page_token="abc",
            ),
            delivery_api.ListTasksResponse(
                tasks=[],
                next_page_token="def",
            ),
            delivery_api.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                ],
                next_page_token="ghi",
            ),
            delivery_api.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                    tasks.Task(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(delivery_api.ListTasksResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "providers/sample1"}

        pager = client.list_tasks(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tasks.Task) for i in results)

        pages = list(client.list_tasks(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_task_tracking_info_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_task_tracking_info
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_task_tracking_info
        ] = mock_rpc

        request = {}
        client.get_task_tracking_info(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_task_tracking_info(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_task_tracking_info_rest_required_fields(
    request_type=delivery_api.GetTaskTrackingInfoRequest,
):
    transport_class = transports.DeliveryServiceRestTransport

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
    ).get_task_tracking_info._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_task_tracking_info._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("header",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = task_tracking_info.TaskTrackingInfo()
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
            return_value = task_tracking_info.TaskTrackingInfo.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_task_tracking_info(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_task_tracking_info_rest_unset_required_fields():
    transport = transports.DeliveryServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_task_tracking_info._get_unset_required_fields({})
    assert set(unset_fields) == (set(("header",)) & set(("name",)))


def test_get_task_tracking_info_rest_flattened():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = task_tracking_info.TaskTrackingInfo()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "providers/sample1/taskTrackingInfo/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = task_tracking_info.TaskTrackingInfo.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_task_tracking_info(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=providers/*/taskTrackingInfo/*}" % client.transport._host,
            args[1],
        )


def test_get_task_tracking_info_rest_flattened_error(transport: str = "rest"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_task_tracking_info(
            delivery_api.GetTaskTrackingInfoRequest(),
            name="name_value",
        )


def test_list_delivery_vehicles_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_delivery_vehicles
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_delivery_vehicles
        ] = mock_rpc

        request = {}
        client.list_delivery_vehicles(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_delivery_vehicles(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_delivery_vehicles_rest_required_fields(
    request_type=delivery_api.ListDeliveryVehiclesRequest,
):
    transport_class = transports.DeliveryServiceRestTransport

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
    ).list_delivery_vehicles._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_delivery_vehicles._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "header",
            "page_size",
            "page_token",
            "viewport",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = delivery_api.ListDeliveryVehiclesResponse()
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
            return_value = delivery_api.ListDeliveryVehiclesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_delivery_vehicles(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_delivery_vehicles_rest_unset_required_fields():
    transport = transports.DeliveryServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_delivery_vehicles._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "header",
                "pageSize",
                "pageToken",
                "viewport",
            )
        )
        & set(("parent",))
    )


def test_list_delivery_vehicles_rest_flattened():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = delivery_api.ListDeliveryVehiclesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "providers/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = delivery_api.ListDeliveryVehiclesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_delivery_vehicles(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=providers/*}/deliveryVehicles" % client.transport._host,
            args[1],
        )


def test_list_delivery_vehicles_rest_flattened_error(transport: str = "rest"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_delivery_vehicles(
            delivery_api.ListDeliveryVehiclesRequest(),
            parent="parent_value",
        )


def test_list_delivery_vehicles_rest_pager(transport: str = "rest"):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            delivery_api.ListDeliveryVehiclesResponse(
                delivery_vehicles=[
                    delivery_vehicles.DeliveryVehicle(),
                    delivery_vehicles.DeliveryVehicle(),
                    delivery_vehicles.DeliveryVehicle(),
                ],
                next_page_token="abc",
            ),
            delivery_api.ListDeliveryVehiclesResponse(
                delivery_vehicles=[],
                next_page_token="def",
            ),
            delivery_api.ListDeliveryVehiclesResponse(
                delivery_vehicles=[
                    delivery_vehicles.DeliveryVehicle(),
                ],
                next_page_token="ghi",
            ),
            delivery_api.ListDeliveryVehiclesResponse(
                delivery_vehicles=[
                    delivery_vehicles.DeliveryVehicle(),
                    delivery_vehicles.DeliveryVehicle(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            delivery_api.ListDeliveryVehiclesResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "providers/sample1"}

        pager = client.list_delivery_vehicles(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, delivery_vehicles.DeliveryVehicle) for i in results)

        pages = list(client.list_delivery_vehicles(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.DeliveryServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.DeliveryServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DeliveryServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.DeliveryServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = DeliveryServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = DeliveryServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.DeliveryServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DeliveryServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DeliveryServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = DeliveryServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DeliveryServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.DeliveryServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DeliveryServiceGrpcTransport,
        transports.DeliveryServiceGrpcAsyncIOTransport,
        transports.DeliveryServiceRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_kind_grpc():
    transport = DeliveryServiceClient.get_transport_class("grpc")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "grpc"


def test_initialize_client_w_grpc():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_delivery_vehicle_empty_call_grpc():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_delivery_vehicle), "__call__"
    ) as call:
        call.return_value = delivery_vehicles.DeliveryVehicle()
        client.create_delivery_vehicle(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.CreateDeliveryVehicleRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_delivery_vehicle_empty_call_grpc():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_delivery_vehicle), "__call__"
    ) as call:
        call.return_value = delivery_vehicles.DeliveryVehicle()
        client.get_delivery_vehicle(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.GetDeliveryVehicleRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_delivery_vehicle_empty_call_grpc():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_delivery_vehicle), "__call__"
    ) as call:
        call.return_value = delivery_vehicles.DeliveryVehicle()
        client.update_delivery_vehicle(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.UpdateDeliveryVehicleRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_batch_create_tasks_empty_call_grpc():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tasks), "__call__"
    ) as call:
        call.return_value = delivery_api.BatchCreateTasksResponse()
        client.batch_create_tasks(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.BatchCreateTasksRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_task_empty_call_grpc():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_task), "__call__") as call:
        call.return_value = tasks.Task()
        client.create_task(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.CreateTaskRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_task_empty_call_grpc():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_task), "__call__") as call:
        call.return_value = tasks.Task()
        client.get_task(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.GetTaskRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_task_empty_call_grpc():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.update_task), "__call__") as call:
        call.return_value = tasks.Task()
        client.update_task(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.UpdateTaskRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_tasks_empty_call_grpc():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        call.return_value = delivery_api.ListTasksResponse()
        client.list_tasks(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.ListTasksRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_task_tracking_info_empty_call_grpc():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_task_tracking_info), "__call__"
    ) as call:
        call.return_value = task_tracking_info.TaskTrackingInfo()
        client.get_task_tracking_info(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.GetTaskTrackingInfoRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_delivery_vehicles_empty_call_grpc():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_vehicles), "__call__"
    ) as call:
        call.return_value = delivery_api.ListDeliveryVehiclesResponse()
        client.list_delivery_vehicles(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.ListDeliveryVehiclesRequest()

        assert args[0] == request_msg


def test_create_delivery_vehicle_routing_parameters_request_1_grpc():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_delivery_vehicle), "__call__"
    ) as call:
        call.return_value = delivery_vehicles.DeliveryVehicle()
        client.create_delivery_vehicle(request={"parent": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.CreateDeliveryVehicleRequest(
            **{"parent": "providers/sample1"}
        )

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_get_delivery_vehicle_routing_parameters_request_1_grpc():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_delivery_vehicle), "__call__"
    ) as call:
        call.return_value = delivery_vehicles.DeliveryVehicle()
        client.get_delivery_vehicle(request={"name": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.GetDeliveryVehicleRequest(
            **{"name": "providers/sample1"}
        )

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_update_delivery_vehicle_routing_parameters_request_1_grpc():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_delivery_vehicle), "__call__"
    ) as call:
        call.return_value = delivery_vehicles.DeliveryVehicle()
        client.update_delivery_vehicle(
            request={"delivery_vehicle": {"name": "providers/sample1"}}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.UpdateDeliveryVehicleRequest(
            **{"delivery_vehicle": {"name": "providers/sample1"}}
        )

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_batch_create_tasks_routing_parameters_request_1_grpc():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tasks), "__call__"
    ) as call:
        call.return_value = delivery_api.BatchCreateTasksResponse()
        client.batch_create_tasks(request={"parent": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.BatchCreateTasksRequest(
            **{"parent": "providers/sample1"}
        )

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_create_task_routing_parameters_request_1_grpc():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_task), "__call__") as call:
        call.return_value = tasks.Task()
        client.create_task(request={"parent": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.CreateTaskRequest(**{"parent": "providers/sample1"})

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_get_task_routing_parameters_request_1_grpc():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_task), "__call__") as call:
        call.return_value = tasks.Task()
        client.get_task(request={"name": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.GetTaskRequest(**{"name": "providers/sample1"})

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_update_task_routing_parameters_request_1_grpc():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.update_task), "__call__") as call:
        call.return_value = tasks.Task()
        client.update_task(request={"task": {"name": "providers/sample1"}})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.UpdateTaskRequest(
            **{"task": {"name": "providers/sample1"}}
        )

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_list_tasks_routing_parameters_request_1_grpc():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        call.return_value = delivery_api.ListTasksResponse()
        client.list_tasks(request={"parent": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.ListTasksRequest(**{"parent": "providers/sample1"})

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_get_task_tracking_info_routing_parameters_request_1_grpc():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_task_tracking_info), "__call__"
    ) as call:
        call.return_value = task_tracking_info.TaskTrackingInfo()
        client.get_task_tracking_info(request={"name": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.GetTaskTrackingInfoRequest(
            **{"name": "providers/sample1"}
        )

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_list_delivery_vehicles_routing_parameters_request_1_grpc():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_vehicles), "__call__"
    ) as call:
        call.return_value = delivery_api.ListDeliveryVehiclesResponse()
        client.list_delivery_vehicles(request={"parent": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.ListDeliveryVehiclesRequest(
            **{"parent": "providers/sample1"}
        )

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_transport_kind_grpc_asyncio():
    transport = DeliveryServiceAsyncClient.get_transport_class("grpc_asyncio")(
        credentials=async_anonymous_credentials()
    )
    assert transport.kind == "grpc_asyncio"


def test_initialize_client_w_grpc_asyncio():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_delivery_vehicle_empty_call_grpc_asyncio():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_delivery_vehicle), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_vehicles.DeliveryVehicle(
                name="name_value",
                navigation_status=common.DeliveryVehicleNavigationStatus.NO_GUIDANCE,
                current_route_segment=b"current_route_segment_blob",
                type_=delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO,
            )
        )
        await client.create_delivery_vehicle(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.CreateDeliveryVehicleRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_delivery_vehicle_empty_call_grpc_asyncio():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_delivery_vehicle), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_vehicles.DeliveryVehicle(
                name="name_value",
                navigation_status=common.DeliveryVehicleNavigationStatus.NO_GUIDANCE,
                current_route_segment=b"current_route_segment_blob",
                type_=delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO,
            )
        )
        await client.get_delivery_vehicle(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.GetDeliveryVehicleRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_update_delivery_vehicle_empty_call_grpc_asyncio():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_delivery_vehicle), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_vehicles.DeliveryVehicle(
                name="name_value",
                navigation_status=common.DeliveryVehicleNavigationStatus.NO_GUIDANCE,
                current_route_segment=b"current_route_segment_blob",
                type_=delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO,
            )
        )
        await client.update_delivery_vehicle(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.UpdateDeliveryVehicleRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_batch_create_tasks_empty_call_grpc_asyncio():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tasks), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_api.BatchCreateTasksResponse()
        )
        await client.batch_create_tasks(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.BatchCreateTasksRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_task_empty_call_grpc_asyncio():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tasks.Task(
                name="name_value",
                type_=tasks.Task.Type.PICKUP,
                state=tasks.Task.State.OPEN,
                task_outcome=tasks.Task.TaskOutcome.SUCCEEDED,
                task_outcome_location_source=tasks.Task.TaskOutcomeLocationSource.PROVIDER,
                tracking_id="tracking_id_value",
                delivery_vehicle_id="delivery_vehicle_id_value",
            )
        )
        await client.create_task(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.CreateTaskRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_task_empty_call_grpc_asyncio():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tasks.Task(
                name="name_value",
                type_=tasks.Task.Type.PICKUP,
                state=tasks.Task.State.OPEN,
                task_outcome=tasks.Task.TaskOutcome.SUCCEEDED,
                task_outcome_location_source=tasks.Task.TaskOutcomeLocationSource.PROVIDER,
                tracking_id="tracking_id_value",
                delivery_vehicle_id="delivery_vehicle_id_value",
            )
        )
        await client.get_task(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.GetTaskRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_update_task_empty_call_grpc_asyncio():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.update_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tasks.Task(
                name="name_value",
                type_=tasks.Task.Type.PICKUP,
                state=tasks.Task.State.OPEN,
                task_outcome=tasks.Task.TaskOutcome.SUCCEEDED,
                task_outcome_location_source=tasks.Task.TaskOutcomeLocationSource.PROVIDER,
                tracking_id="tracking_id_value",
                delivery_vehicle_id="delivery_vehicle_id_value",
            )
        )
        await client.update_task(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.UpdateTaskRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_tasks_empty_call_grpc_asyncio():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_api.ListTasksResponse(
                next_page_token="next_page_token_value",
                total_size=1086,
            )
        )
        await client.list_tasks(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.ListTasksRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_task_tracking_info_empty_call_grpc_asyncio():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_task_tracking_info), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            task_tracking_info.TaskTrackingInfo(
                name="name_value",
                tracking_id="tracking_id_value",
                state=tasks.Task.State.OPEN,
                task_outcome=tasks.Task.TaskOutcome.SUCCEEDED,
            )
        )
        await client.get_task_tracking_info(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.GetTaskTrackingInfoRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_delivery_vehicles_empty_call_grpc_asyncio():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_vehicles), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_api.ListDeliveryVehiclesResponse(
                next_page_token="next_page_token_value",
                total_size=1086,
            )
        )
        await client.list_delivery_vehicles(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.ListDeliveryVehiclesRequest()

        assert args[0] == request_msg


@pytest.mark.asyncio
async def test_create_delivery_vehicle_routing_parameters_request_1_grpc_asyncio():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_delivery_vehicle), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_vehicles.DeliveryVehicle(
                name="name_value",
                navigation_status=common.DeliveryVehicleNavigationStatus.NO_GUIDANCE,
                current_route_segment=b"current_route_segment_blob",
                type_=delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO,
            )
        )
        await client.create_delivery_vehicle(request={"parent": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.CreateDeliveryVehicleRequest(
            **{"parent": "providers/sample1"}
        )

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_get_delivery_vehicle_routing_parameters_request_1_grpc_asyncio():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_delivery_vehicle), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_vehicles.DeliveryVehicle(
                name="name_value",
                navigation_status=common.DeliveryVehicleNavigationStatus.NO_GUIDANCE,
                current_route_segment=b"current_route_segment_blob",
                type_=delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO,
            )
        )
        await client.get_delivery_vehicle(request={"name": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.GetDeliveryVehicleRequest(
            **{"name": "providers/sample1"}
        )

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_update_delivery_vehicle_routing_parameters_request_1_grpc_asyncio():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_delivery_vehicle), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_vehicles.DeliveryVehicle(
                name="name_value",
                navigation_status=common.DeliveryVehicleNavigationStatus.NO_GUIDANCE,
                current_route_segment=b"current_route_segment_blob",
                type_=delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO,
            )
        )
        await client.update_delivery_vehicle(
            request={"delivery_vehicle": {"name": "providers/sample1"}}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.UpdateDeliveryVehicleRequest(
            **{"delivery_vehicle": {"name": "providers/sample1"}}
        )

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_batch_create_tasks_routing_parameters_request_1_grpc_asyncio():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tasks), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_api.BatchCreateTasksResponse()
        )
        await client.batch_create_tasks(request={"parent": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.BatchCreateTasksRequest(
            **{"parent": "providers/sample1"}
        )

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_create_task_routing_parameters_request_1_grpc_asyncio():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tasks.Task(
                name="name_value",
                type_=tasks.Task.Type.PICKUP,
                state=tasks.Task.State.OPEN,
                task_outcome=tasks.Task.TaskOutcome.SUCCEEDED,
                task_outcome_location_source=tasks.Task.TaskOutcomeLocationSource.PROVIDER,
                tracking_id="tracking_id_value",
                delivery_vehicle_id="delivery_vehicle_id_value",
            )
        )
        await client.create_task(request={"parent": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.CreateTaskRequest(**{"parent": "providers/sample1"})

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_get_task_routing_parameters_request_1_grpc_asyncio():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tasks.Task(
                name="name_value",
                type_=tasks.Task.Type.PICKUP,
                state=tasks.Task.State.OPEN,
                task_outcome=tasks.Task.TaskOutcome.SUCCEEDED,
                task_outcome_location_source=tasks.Task.TaskOutcomeLocationSource.PROVIDER,
                tracking_id="tracking_id_value",
                delivery_vehicle_id="delivery_vehicle_id_value",
            )
        )
        await client.get_task(request={"name": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.GetTaskRequest(**{"name": "providers/sample1"})

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_update_task_routing_parameters_request_1_grpc_asyncio():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.update_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tasks.Task(
                name="name_value",
                type_=tasks.Task.Type.PICKUP,
                state=tasks.Task.State.OPEN,
                task_outcome=tasks.Task.TaskOutcome.SUCCEEDED,
                task_outcome_location_source=tasks.Task.TaskOutcomeLocationSource.PROVIDER,
                tracking_id="tracking_id_value",
                delivery_vehicle_id="delivery_vehicle_id_value",
            )
        )
        await client.update_task(request={"task": {"name": "providers/sample1"}})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.UpdateTaskRequest(
            **{"task": {"name": "providers/sample1"}}
        )

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_list_tasks_routing_parameters_request_1_grpc_asyncio():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_api.ListTasksResponse(
                next_page_token="next_page_token_value",
                total_size=1086,
            )
        )
        await client.list_tasks(request={"parent": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.ListTasksRequest(**{"parent": "providers/sample1"})

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_get_task_tracking_info_routing_parameters_request_1_grpc_asyncio():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_task_tracking_info), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            task_tracking_info.TaskTrackingInfo(
                name="name_value",
                tracking_id="tracking_id_value",
                state=tasks.Task.State.OPEN,
                task_outcome=tasks.Task.TaskOutcome.SUCCEEDED,
            )
        )
        await client.get_task_tracking_info(request={"name": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.GetTaskTrackingInfoRequest(
            **{"name": "providers/sample1"}
        )

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_list_delivery_vehicles_routing_parameters_request_1_grpc_asyncio():
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_vehicles), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            delivery_api.ListDeliveryVehiclesResponse(
                next_page_token="next_page_token_value",
                total_size=1086,
            )
        )
        await client.list_delivery_vehicles(request={"parent": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.ListDeliveryVehiclesRequest(
            **{"parent": "providers/sample1"}
        )

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_transport_kind_rest():
    transport = DeliveryServiceClient.get_transport_class("rest")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "rest"


def test_create_delivery_vehicle_rest_bad_request(
    request_type=delivery_api.CreateDeliveryVehicleRequest,
):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "providers/sample1"}
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
        client.create_delivery_vehicle(request)


@pytest.mark.parametrize(
    "request_type",
    [
        delivery_api.CreateDeliveryVehicleRequest,
        dict,
    ],
)
def test_create_delivery_vehicle_rest_call_success(request_type):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "providers/sample1"}
    request_init["delivery_vehicle"] = {
        "name": "name_value",
        "last_location": {
            "location": {"latitude": 0.86, "longitude": 0.971},
            "horizontal_accuracy": {"value": 0.541},
            "latlng_accuracy": {},
            "heading": {"value": 541},
            "bearing_accuracy": {},
            "heading_accuracy": {},
            "altitude": {},
            "vertical_accuracy": {},
            "altitude_accuracy": {},
            "speed_kmph": {},
            "speed": {},
            "speed_accuracy": {},
            "update_time": {"seconds": 751, "nanos": 543},
            "server_time": {},
            "location_sensor": 1,
            "is_road_snapped": {"value": True},
            "is_gps_sensor_enabled": {},
            "time_since_update": {},
            "num_stale_updates": {},
            "raw_location": {},
            "raw_location_time": {},
            "raw_location_sensor": 1,
            "raw_location_accuracy": {},
            "supplemental_location": {},
            "supplemental_location_time": {},
            "supplemental_location_sensor": 1,
            "supplemental_location_accuracy": {},
            "road_snapped": True,
        },
        "navigation_status": 1,
        "current_route_segment": b"current_route_segment_blob",
        "current_route_segment_end_point": {},
        "remaining_distance_meters": {},
        "remaining_duration": {"seconds": 751, "nanos": 543},
        "remaining_vehicle_journey_segments": [
            {
                "stop": {
                    "planned_location": {"point": {}},
                    "tasks": [
                        {
                            "task_id": "task_id_value",
                            "task_duration": {},
                            "target_time_window": {"start_time": {}, "end_time": {}},
                        }
                    ],
                    "state": 1,
                },
                "driving_distance_meters": {},
                "driving_duration": {},
                "path": {},
            }
        ],
        "attributes": [
            {
                "key": "key_value",
                "value": "value_value",
                "string_value": "string_value_value",
                "bool_value": True,
                "number_value": 0.1285,
            }
        ],
        "type_": 1,
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = delivery_api.CreateDeliveryVehicleRequest.meta.fields[
        "delivery_vehicle"
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
    for field, value in request_init["delivery_vehicle"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["delivery_vehicle"][field])):
                    del request_init["delivery_vehicle"][field][i][subfield]
            else:
                del request_init["delivery_vehicle"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = delivery_vehicles.DeliveryVehicle(
            name="name_value",
            navigation_status=common.DeliveryVehicleNavigationStatus.NO_GUIDANCE,
            current_route_segment=b"current_route_segment_blob",
            type_=delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = delivery_vehicles.DeliveryVehicle.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_delivery_vehicle(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, delivery_vehicles.DeliveryVehicle)
    assert response.name == "name_value"
    assert (
        response.navigation_status == common.DeliveryVehicleNavigationStatus.NO_GUIDANCE
    )
    assert response.current_route_segment == b"current_route_segment_blob"
    assert response.type_ == delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_delivery_vehicle_rest_interceptors(null_interceptor):
    transport = transports.DeliveryServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeliveryServiceRestInterceptor(),
    )
    client = DeliveryServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeliveryServiceRestInterceptor, "post_create_delivery_vehicle"
    ) as post, mock.patch.object(
        transports.DeliveryServiceRestInterceptor, "pre_create_delivery_vehicle"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = delivery_api.CreateDeliveryVehicleRequest.pb(
            delivery_api.CreateDeliveryVehicleRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = delivery_vehicles.DeliveryVehicle.to_json(
            delivery_vehicles.DeliveryVehicle()
        )
        req.return_value.content = return_value

        request = delivery_api.CreateDeliveryVehicleRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = delivery_vehicles.DeliveryVehicle()

        client.create_delivery_vehicle(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_delivery_vehicle_rest_bad_request(
    request_type=delivery_api.GetDeliveryVehicleRequest,
):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"name": "providers/sample1/deliveryVehicles/sample2"}
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
        client.get_delivery_vehicle(request)


@pytest.mark.parametrize(
    "request_type",
    [
        delivery_api.GetDeliveryVehicleRequest,
        dict,
    ],
)
def test_get_delivery_vehicle_rest_call_success(request_type):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "providers/sample1/deliveryVehicles/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = delivery_vehicles.DeliveryVehicle(
            name="name_value",
            navigation_status=common.DeliveryVehicleNavigationStatus.NO_GUIDANCE,
            current_route_segment=b"current_route_segment_blob",
            type_=delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = delivery_vehicles.DeliveryVehicle.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_delivery_vehicle(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, delivery_vehicles.DeliveryVehicle)
    assert response.name == "name_value"
    assert (
        response.navigation_status == common.DeliveryVehicleNavigationStatus.NO_GUIDANCE
    )
    assert response.current_route_segment == b"current_route_segment_blob"
    assert response.type_ == delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_delivery_vehicle_rest_interceptors(null_interceptor):
    transport = transports.DeliveryServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeliveryServiceRestInterceptor(),
    )
    client = DeliveryServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeliveryServiceRestInterceptor, "post_get_delivery_vehicle"
    ) as post, mock.patch.object(
        transports.DeliveryServiceRestInterceptor, "pre_get_delivery_vehicle"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = delivery_api.GetDeliveryVehicleRequest.pb(
            delivery_api.GetDeliveryVehicleRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = delivery_vehicles.DeliveryVehicle.to_json(
            delivery_vehicles.DeliveryVehicle()
        )
        req.return_value.content = return_value

        request = delivery_api.GetDeliveryVehicleRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = delivery_vehicles.DeliveryVehicle()

        client.get_delivery_vehicle(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_delivery_vehicle_rest_bad_request(
    request_type=delivery_api.UpdateDeliveryVehicleRequest,
):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "delivery_vehicle": {"name": "providers/sample1/deliveryVehicles/sample2"}
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
        client.update_delivery_vehicle(request)


@pytest.mark.parametrize(
    "request_type",
    [
        delivery_api.UpdateDeliveryVehicleRequest,
        dict,
    ],
)
def test_update_delivery_vehicle_rest_call_success(request_type):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "delivery_vehicle": {"name": "providers/sample1/deliveryVehicles/sample2"}
    }
    request_init["delivery_vehicle"] = {
        "name": "providers/sample1/deliveryVehicles/sample2",
        "last_location": {
            "location": {"latitude": 0.86, "longitude": 0.971},
            "horizontal_accuracy": {"value": 0.541},
            "latlng_accuracy": {},
            "heading": {"value": 541},
            "bearing_accuracy": {},
            "heading_accuracy": {},
            "altitude": {},
            "vertical_accuracy": {},
            "altitude_accuracy": {},
            "speed_kmph": {},
            "speed": {},
            "speed_accuracy": {},
            "update_time": {"seconds": 751, "nanos": 543},
            "server_time": {},
            "location_sensor": 1,
            "is_road_snapped": {"value": True},
            "is_gps_sensor_enabled": {},
            "time_since_update": {},
            "num_stale_updates": {},
            "raw_location": {},
            "raw_location_time": {},
            "raw_location_sensor": 1,
            "raw_location_accuracy": {},
            "supplemental_location": {},
            "supplemental_location_time": {},
            "supplemental_location_sensor": 1,
            "supplemental_location_accuracy": {},
            "road_snapped": True,
        },
        "navigation_status": 1,
        "current_route_segment": b"current_route_segment_blob",
        "current_route_segment_end_point": {},
        "remaining_distance_meters": {},
        "remaining_duration": {"seconds": 751, "nanos": 543},
        "remaining_vehicle_journey_segments": [
            {
                "stop": {
                    "planned_location": {"point": {}},
                    "tasks": [
                        {
                            "task_id": "task_id_value",
                            "task_duration": {},
                            "target_time_window": {"start_time": {}, "end_time": {}},
                        }
                    ],
                    "state": 1,
                },
                "driving_distance_meters": {},
                "driving_duration": {},
                "path": {},
            }
        ],
        "attributes": [
            {
                "key": "key_value",
                "value": "value_value",
                "string_value": "string_value_value",
                "bool_value": True,
                "number_value": 0.1285,
            }
        ],
        "type_": 1,
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = delivery_api.UpdateDeliveryVehicleRequest.meta.fields[
        "delivery_vehicle"
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
    for field, value in request_init["delivery_vehicle"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["delivery_vehicle"][field])):
                    del request_init["delivery_vehicle"][field][i][subfield]
            else:
                del request_init["delivery_vehicle"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = delivery_vehicles.DeliveryVehicle(
            name="name_value",
            navigation_status=common.DeliveryVehicleNavigationStatus.NO_GUIDANCE,
            current_route_segment=b"current_route_segment_blob",
            type_=delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = delivery_vehicles.DeliveryVehicle.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_delivery_vehicle(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, delivery_vehicles.DeliveryVehicle)
    assert response.name == "name_value"
    assert (
        response.navigation_status == common.DeliveryVehicleNavigationStatus.NO_GUIDANCE
    )
    assert response.current_route_segment == b"current_route_segment_blob"
    assert response.type_ == delivery_vehicles.DeliveryVehicle.DeliveryVehicleType.AUTO


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_delivery_vehicle_rest_interceptors(null_interceptor):
    transport = transports.DeliveryServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeliveryServiceRestInterceptor(),
    )
    client = DeliveryServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeliveryServiceRestInterceptor, "post_update_delivery_vehicle"
    ) as post, mock.patch.object(
        transports.DeliveryServiceRestInterceptor, "pre_update_delivery_vehicle"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = delivery_api.UpdateDeliveryVehicleRequest.pb(
            delivery_api.UpdateDeliveryVehicleRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = delivery_vehicles.DeliveryVehicle.to_json(
            delivery_vehicles.DeliveryVehicle()
        )
        req.return_value.content = return_value

        request = delivery_api.UpdateDeliveryVehicleRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = delivery_vehicles.DeliveryVehicle()

        client.update_delivery_vehicle(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_batch_create_tasks_rest_bad_request(
    request_type=delivery_api.BatchCreateTasksRequest,
):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "providers/sample1"}
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
        client.batch_create_tasks(request)


@pytest.mark.parametrize(
    "request_type",
    [
        delivery_api.BatchCreateTasksRequest,
        dict,
    ],
)
def test_batch_create_tasks_rest_call_success(request_type):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "providers/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = delivery_api.BatchCreateTasksResponse()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = delivery_api.BatchCreateTasksResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.batch_create_tasks(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, delivery_api.BatchCreateTasksResponse)


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_batch_create_tasks_rest_interceptors(null_interceptor):
    transport = transports.DeliveryServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeliveryServiceRestInterceptor(),
    )
    client = DeliveryServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeliveryServiceRestInterceptor, "post_batch_create_tasks"
    ) as post, mock.patch.object(
        transports.DeliveryServiceRestInterceptor, "pre_batch_create_tasks"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = delivery_api.BatchCreateTasksRequest.pb(
            delivery_api.BatchCreateTasksRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = delivery_api.BatchCreateTasksResponse.to_json(
            delivery_api.BatchCreateTasksResponse()
        )
        req.return_value.content = return_value

        request = delivery_api.BatchCreateTasksRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = delivery_api.BatchCreateTasksResponse()

        client.batch_create_tasks(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_task_rest_bad_request(request_type=delivery_api.CreateTaskRequest):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "providers/sample1"}
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
        client.create_task(request)


@pytest.mark.parametrize(
    "request_type",
    [
        delivery_api.CreateTaskRequest,
        dict,
    ],
)
def test_create_task_rest_call_success(request_type):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "providers/sample1"}
    request_init["task"] = {
        "name": "name_value",
        "type_": 1,
        "state": 1,
        "task_outcome": 1,
        "task_outcome_time": {"seconds": 751, "nanos": 543},
        "task_outcome_location": {"point": {"latitude": 0.86, "longitude": 0.971}},
        "task_outcome_location_source": 2,
        "tracking_id": "tracking_id_value",
        "delivery_vehicle_id": "delivery_vehicle_id_value",
        "planned_location": {},
        "task_duration": {"seconds": 751, "nanos": 543},
        "target_time_window": {"start_time": {}, "end_time": {}},
        "journey_sharing_info": {
            "remaining_vehicle_journey_segments": [
                {
                    "stop": {
                        "planned_location": {},
                        "tasks": [
                            {
                                "task_id": "task_id_value",
                                "task_duration": {},
                                "target_time_window": {},
                            }
                        ],
                        "state": 1,
                    },
                    "driving_distance_meters": {"value": 541},
                    "driving_duration": {},
                    "path": {},
                }
            ],
            "last_location": {
                "location": {},
                "horizontal_accuracy": {"value": 0.541},
                "latlng_accuracy": {},
                "heading": {},
                "bearing_accuracy": {},
                "heading_accuracy": {},
                "altitude": {},
                "vertical_accuracy": {},
                "altitude_accuracy": {},
                "speed_kmph": {},
                "speed": {},
                "speed_accuracy": {},
                "update_time": {},
                "server_time": {},
                "location_sensor": 1,
                "is_road_snapped": {"value": True},
                "is_gps_sensor_enabled": {},
                "time_since_update": {},
                "num_stale_updates": {},
                "raw_location": {},
                "raw_location_time": {},
                "raw_location_sensor": 1,
                "raw_location_accuracy": {},
                "supplemental_location": {},
                "supplemental_location_time": {},
                "supplemental_location_sensor": 1,
                "supplemental_location_accuracy": {},
                "road_snapped": True,
            },
            "last_location_snappable": True,
        },
        "task_tracking_view_config": {
            "route_polyline_points_visibility": {
                "remaining_stop_count_threshold": 3219,
                "duration_until_estimated_arrival_time_threshold": {},
                "remaining_driving_distance_meters_threshold": 4561,
                "always": True,
                "never": True,
            },
            "estimated_arrival_time_visibility": {},
            "estimated_task_completion_time_visibility": {},
            "remaining_driving_distance_visibility": {},
            "remaining_stop_count_visibility": {},
            "vehicle_location_visibility": {},
        },
        "attributes": [
            {
                "key": "key_value",
                "string_value": "string_value_value",
                "bool_value": True,
                "number_value": 0.1285,
            }
        ],
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = delivery_api.CreateTaskRequest.meta.fields["task"]

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
    for field, value in request_init["task"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["task"][field])):
                    del request_init["task"][field][i][subfield]
            else:
                del request_init["task"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tasks.Task(
            name="name_value",
            type_=tasks.Task.Type.PICKUP,
            state=tasks.Task.State.OPEN,
            task_outcome=tasks.Task.TaskOutcome.SUCCEEDED,
            task_outcome_location_source=tasks.Task.TaskOutcomeLocationSource.PROVIDER,
            tracking_id="tracking_id_value",
            delivery_vehicle_id="delivery_vehicle_id_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = tasks.Task.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_task(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, tasks.Task)
    assert response.name == "name_value"
    assert response.type_ == tasks.Task.Type.PICKUP
    assert response.state == tasks.Task.State.OPEN
    assert response.task_outcome == tasks.Task.TaskOutcome.SUCCEEDED
    assert (
        response.task_outcome_location_source
        == tasks.Task.TaskOutcomeLocationSource.PROVIDER
    )
    assert response.tracking_id == "tracking_id_value"
    assert response.delivery_vehicle_id == "delivery_vehicle_id_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_task_rest_interceptors(null_interceptor):
    transport = transports.DeliveryServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeliveryServiceRestInterceptor(),
    )
    client = DeliveryServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeliveryServiceRestInterceptor, "post_create_task"
    ) as post, mock.patch.object(
        transports.DeliveryServiceRestInterceptor, "pre_create_task"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = delivery_api.CreateTaskRequest.pb(delivery_api.CreateTaskRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = tasks.Task.to_json(tasks.Task())
        req.return_value.content = return_value

        request = delivery_api.CreateTaskRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tasks.Task()

        client.create_task(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_task_rest_bad_request(request_type=delivery_api.GetTaskRequest):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"name": "providers/sample1/tasks/sample2"}
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
        client.get_task(request)


@pytest.mark.parametrize(
    "request_type",
    [
        delivery_api.GetTaskRequest,
        dict,
    ],
)
def test_get_task_rest_call_success(request_type):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "providers/sample1/tasks/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tasks.Task(
            name="name_value",
            type_=tasks.Task.Type.PICKUP,
            state=tasks.Task.State.OPEN,
            task_outcome=tasks.Task.TaskOutcome.SUCCEEDED,
            task_outcome_location_source=tasks.Task.TaskOutcomeLocationSource.PROVIDER,
            tracking_id="tracking_id_value",
            delivery_vehicle_id="delivery_vehicle_id_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = tasks.Task.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_task(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, tasks.Task)
    assert response.name == "name_value"
    assert response.type_ == tasks.Task.Type.PICKUP
    assert response.state == tasks.Task.State.OPEN
    assert response.task_outcome == tasks.Task.TaskOutcome.SUCCEEDED
    assert (
        response.task_outcome_location_source
        == tasks.Task.TaskOutcomeLocationSource.PROVIDER
    )
    assert response.tracking_id == "tracking_id_value"
    assert response.delivery_vehicle_id == "delivery_vehicle_id_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_task_rest_interceptors(null_interceptor):
    transport = transports.DeliveryServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeliveryServiceRestInterceptor(),
    )
    client = DeliveryServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeliveryServiceRestInterceptor, "post_get_task"
    ) as post, mock.patch.object(
        transports.DeliveryServiceRestInterceptor, "pre_get_task"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = delivery_api.GetTaskRequest.pb(delivery_api.GetTaskRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = tasks.Task.to_json(tasks.Task())
        req.return_value.content = return_value

        request = delivery_api.GetTaskRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tasks.Task()

        client.get_task(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_task_rest_bad_request(request_type=delivery_api.UpdateTaskRequest):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"task": {"name": "providers/sample1/tasks/sample2"}}
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
        client.update_task(request)


@pytest.mark.parametrize(
    "request_type",
    [
        delivery_api.UpdateTaskRequest,
        dict,
    ],
)
def test_update_task_rest_call_success(request_type):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"task": {"name": "providers/sample1/tasks/sample2"}}
    request_init["task"] = {
        "name": "providers/sample1/tasks/sample2",
        "type_": 1,
        "state": 1,
        "task_outcome": 1,
        "task_outcome_time": {"seconds": 751, "nanos": 543},
        "task_outcome_location": {"point": {"latitude": 0.86, "longitude": 0.971}},
        "task_outcome_location_source": 2,
        "tracking_id": "tracking_id_value",
        "delivery_vehicle_id": "delivery_vehicle_id_value",
        "planned_location": {},
        "task_duration": {"seconds": 751, "nanos": 543},
        "target_time_window": {"start_time": {}, "end_time": {}},
        "journey_sharing_info": {
            "remaining_vehicle_journey_segments": [
                {
                    "stop": {
                        "planned_location": {},
                        "tasks": [
                            {
                                "task_id": "task_id_value",
                                "task_duration": {},
                                "target_time_window": {},
                            }
                        ],
                        "state": 1,
                    },
                    "driving_distance_meters": {"value": 541},
                    "driving_duration": {},
                    "path": {},
                }
            ],
            "last_location": {
                "location": {},
                "horizontal_accuracy": {"value": 0.541},
                "latlng_accuracy": {},
                "heading": {},
                "bearing_accuracy": {},
                "heading_accuracy": {},
                "altitude": {},
                "vertical_accuracy": {},
                "altitude_accuracy": {},
                "speed_kmph": {},
                "speed": {},
                "speed_accuracy": {},
                "update_time": {},
                "server_time": {},
                "location_sensor": 1,
                "is_road_snapped": {"value": True},
                "is_gps_sensor_enabled": {},
                "time_since_update": {},
                "num_stale_updates": {},
                "raw_location": {},
                "raw_location_time": {},
                "raw_location_sensor": 1,
                "raw_location_accuracy": {},
                "supplemental_location": {},
                "supplemental_location_time": {},
                "supplemental_location_sensor": 1,
                "supplemental_location_accuracy": {},
                "road_snapped": True,
            },
            "last_location_snappable": True,
        },
        "task_tracking_view_config": {
            "route_polyline_points_visibility": {
                "remaining_stop_count_threshold": 3219,
                "duration_until_estimated_arrival_time_threshold": {},
                "remaining_driving_distance_meters_threshold": 4561,
                "always": True,
                "never": True,
            },
            "estimated_arrival_time_visibility": {},
            "estimated_task_completion_time_visibility": {},
            "remaining_driving_distance_visibility": {},
            "remaining_stop_count_visibility": {},
            "vehicle_location_visibility": {},
        },
        "attributes": [
            {
                "key": "key_value",
                "string_value": "string_value_value",
                "bool_value": True,
                "number_value": 0.1285,
            }
        ],
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = delivery_api.UpdateTaskRequest.meta.fields["task"]

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
    for field, value in request_init["task"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["task"][field])):
                    del request_init["task"][field][i][subfield]
            else:
                del request_init["task"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tasks.Task(
            name="name_value",
            type_=tasks.Task.Type.PICKUP,
            state=tasks.Task.State.OPEN,
            task_outcome=tasks.Task.TaskOutcome.SUCCEEDED,
            task_outcome_location_source=tasks.Task.TaskOutcomeLocationSource.PROVIDER,
            tracking_id="tracking_id_value",
            delivery_vehicle_id="delivery_vehicle_id_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = tasks.Task.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_task(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, tasks.Task)
    assert response.name == "name_value"
    assert response.type_ == tasks.Task.Type.PICKUP
    assert response.state == tasks.Task.State.OPEN
    assert response.task_outcome == tasks.Task.TaskOutcome.SUCCEEDED
    assert (
        response.task_outcome_location_source
        == tasks.Task.TaskOutcomeLocationSource.PROVIDER
    )
    assert response.tracking_id == "tracking_id_value"
    assert response.delivery_vehicle_id == "delivery_vehicle_id_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_task_rest_interceptors(null_interceptor):
    transport = transports.DeliveryServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeliveryServiceRestInterceptor(),
    )
    client = DeliveryServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeliveryServiceRestInterceptor, "post_update_task"
    ) as post, mock.patch.object(
        transports.DeliveryServiceRestInterceptor, "pre_update_task"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = delivery_api.UpdateTaskRequest.pb(delivery_api.UpdateTaskRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = tasks.Task.to_json(tasks.Task())
        req.return_value.content = return_value

        request = delivery_api.UpdateTaskRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tasks.Task()

        client.update_task(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_tasks_rest_bad_request(request_type=delivery_api.ListTasksRequest):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "providers/sample1"}
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
        client.list_tasks(request)


@pytest.mark.parametrize(
    "request_type",
    [
        delivery_api.ListTasksRequest,
        dict,
    ],
)
def test_list_tasks_rest_call_success(request_type):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "providers/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = delivery_api.ListTasksResponse(
            next_page_token="next_page_token_value",
            total_size=1086,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = delivery_api.ListTasksResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_tasks(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTasksPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_tasks_rest_interceptors(null_interceptor):
    transport = transports.DeliveryServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeliveryServiceRestInterceptor(),
    )
    client = DeliveryServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeliveryServiceRestInterceptor, "post_list_tasks"
    ) as post, mock.patch.object(
        transports.DeliveryServiceRestInterceptor, "pre_list_tasks"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = delivery_api.ListTasksRequest.pb(delivery_api.ListTasksRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = delivery_api.ListTasksResponse.to_json(
            delivery_api.ListTasksResponse()
        )
        req.return_value.content = return_value

        request = delivery_api.ListTasksRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = delivery_api.ListTasksResponse()

        client.list_tasks(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_task_tracking_info_rest_bad_request(
    request_type=delivery_api.GetTaskTrackingInfoRequest,
):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"name": "providers/sample1/taskTrackingInfo/sample2"}
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
        client.get_task_tracking_info(request)


@pytest.mark.parametrize(
    "request_type",
    [
        delivery_api.GetTaskTrackingInfoRequest,
        dict,
    ],
)
def test_get_task_tracking_info_rest_call_success(request_type):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "providers/sample1/taskTrackingInfo/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = task_tracking_info.TaskTrackingInfo(
            name="name_value",
            tracking_id="tracking_id_value",
            state=tasks.Task.State.OPEN,
            task_outcome=tasks.Task.TaskOutcome.SUCCEEDED,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = task_tracking_info.TaskTrackingInfo.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_task_tracking_info(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, task_tracking_info.TaskTrackingInfo)
    assert response.name == "name_value"
    assert response.tracking_id == "tracking_id_value"
    assert response.state == tasks.Task.State.OPEN
    assert response.task_outcome == tasks.Task.TaskOutcome.SUCCEEDED


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_task_tracking_info_rest_interceptors(null_interceptor):
    transport = transports.DeliveryServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeliveryServiceRestInterceptor(),
    )
    client = DeliveryServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeliveryServiceRestInterceptor, "post_get_task_tracking_info"
    ) as post, mock.patch.object(
        transports.DeliveryServiceRestInterceptor, "pre_get_task_tracking_info"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = delivery_api.GetTaskTrackingInfoRequest.pb(
            delivery_api.GetTaskTrackingInfoRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = task_tracking_info.TaskTrackingInfo.to_json(
            task_tracking_info.TaskTrackingInfo()
        )
        req.return_value.content = return_value

        request = delivery_api.GetTaskTrackingInfoRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = task_tracking_info.TaskTrackingInfo()

        client.get_task_tracking_info(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_delivery_vehicles_rest_bad_request(
    request_type=delivery_api.ListDeliveryVehiclesRequest,
):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "providers/sample1"}
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
        client.list_delivery_vehicles(request)


@pytest.mark.parametrize(
    "request_type",
    [
        delivery_api.ListDeliveryVehiclesRequest,
        dict,
    ],
)
def test_list_delivery_vehicles_rest_call_success(request_type):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "providers/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = delivery_api.ListDeliveryVehiclesResponse(
            next_page_token="next_page_token_value",
            total_size=1086,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = delivery_api.ListDeliveryVehiclesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_delivery_vehicles(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDeliveryVehiclesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_delivery_vehicles_rest_interceptors(null_interceptor):
    transport = transports.DeliveryServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeliveryServiceRestInterceptor(),
    )
    client = DeliveryServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeliveryServiceRestInterceptor, "post_list_delivery_vehicles"
    ) as post, mock.patch.object(
        transports.DeliveryServiceRestInterceptor, "pre_list_delivery_vehicles"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = delivery_api.ListDeliveryVehiclesRequest.pb(
            delivery_api.ListDeliveryVehiclesRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = delivery_api.ListDeliveryVehiclesResponse.to_json(
            delivery_api.ListDeliveryVehiclesResponse()
        )
        req.return_value.content = return_value

        request = delivery_api.ListDeliveryVehiclesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = delivery_api.ListDeliveryVehiclesResponse()

        client.list_delivery_vehicles(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_initialize_client_w_rest():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_delivery_vehicle_empty_call_rest():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_delivery_vehicle), "__call__"
    ) as call:
        client.create_delivery_vehicle(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.CreateDeliveryVehicleRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_delivery_vehicle_empty_call_rest():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_delivery_vehicle), "__call__"
    ) as call:
        client.get_delivery_vehicle(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.GetDeliveryVehicleRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_delivery_vehicle_empty_call_rest():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_delivery_vehicle), "__call__"
    ) as call:
        client.update_delivery_vehicle(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.UpdateDeliveryVehicleRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_batch_create_tasks_empty_call_rest():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tasks), "__call__"
    ) as call:
        client.batch_create_tasks(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.BatchCreateTasksRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_task_empty_call_rest():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_task), "__call__") as call:
        client.create_task(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.CreateTaskRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_task_empty_call_rest():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_task), "__call__") as call:
        client.get_task(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.GetTaskRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_task_empty_call_rest():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.update_task), "__call__") as call:
        client.update_task(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.UpdateTaskRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_tasks_empty_call_rest():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        client.list_tasks(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.ListTasksRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_task_tracking_info_empty_call_rest():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_task_tracking_info), "__call__"
    ) as call:
        client.get_task_tracking_info(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.GetTaskTrackingInfoRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_delivery_vehicles_empty_call_rest():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_vehicles), "__call__"
    ) as call:
        client.list_delivery_vehicles(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = delivery_api.ListDeliveryVehiclesRequest()

        assert args[0] == request_msg


def test_create_delivery_vehicle_routing_parameters_request_1_rest():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_delivery_vehicle), "__call__"
    ) as call:
        client.create_delivery_vehicle(request={"parent": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.CreateDeliveryVehicleRequest(
            **{"parent": "providers/sample1"}
        )

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_get_delivery_vehicle_routing_parameters_request_1_rest():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_delivery_vehicle), "__call__"
    ) as call:
        client.get_delivery_vehicle(request={"name": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.GetDeliveryVehicleRequest(
            **{"name": "providers/sample1"}
        )

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_update_delivery_vehicle_routing_parameters_request_1_rest():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_delivery_vehicle), "__call__"
    ) as call:
        client.update_delivery_vehicle(
            request={"delivery_vehicle": {"name": "providers/sample1"}}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.UpdateDeliveryVehicleRequest(
            **{"delivery_vehicle": {"name": "providers/sample1"}}
        )

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_batch_create_tasks_routing_parameters_request_1_rest():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tasks), "__call__"
    ) as call:
        client.batch_create_tasks(request={"parent": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.BatchCreateTasksRequest(
            **{"parent": "providers/sample1"}
        )

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_create_task_routing_parameters_request_1_rest():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_task), "__call__") as call:
        client.create_task(request={"parent": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.CreateTaskRequest(**{"parent": "providers/sample1"})

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_get_task_routing_parameters_request_1_rest():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_task), "__call__") as call:
        client.get_task(request={"name": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.GetTaskRequest(**{"name": "providers/sample1"})

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_update_task_routing_parameters_request_1_rest():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.update_task), "__call__") as call:
        client.update_task(request={"task": {"name": "providers/sample1"}})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.UpdateTaskRequest(
            **{"task": {"name": "providers/sample1"}}
        )

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_list_tasks_routing_parameters_request_1_rest():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        client.list_tasks(request={"parent": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.ListTasksRequest(**{"parent": "providers/sample1"})

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_get_task_tracking_info_routing_parameters_request_1_rest():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_task_tracking_info), "__call__"
    ) as call:
        client.get_task_tracking_info(request={"name": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.GetTaskTrackingInfoRequest(
            **{"name": "providers/sample1"}
        )

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_list_delivery_vehicles_routing_parameters_request_1_rest():
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_vehicles), "__call__"
    ) as call:
        client.list_delivery_vehicles(request={"parent": "providers/sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = delivery_api.ListDeliveryVehiclesRequest(
            **{"parent": "providers/sample1"}
        )

        assert args[0] == request_msg

        expected_headers = {"provider_id": "providers/sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.DeliveryServiceGrpcTransport,
    )


def test_delivery_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.DeliveryServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_delivery_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.maps.fleetengine_delivery_v1.services.delivery_service.transports.DeliveryServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.DeliveryServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_delivery_vehicle",
        "get_delivery_vehicle",
        "update_delivery_vehicle",
        "batch_create_tasks",
        "create_task",
        "get_task",
        "update_task",
        "list_tasks",
        "get_task_tracking_info",
        "list_delivery_vehicles",
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


def test_delivery_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.maps.fleetengine_delivery_v1.services.delivery_service.transports.DeliveryServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DeliveryServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_delivery_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.maps.fleetengine_delivery_v1.services.delivery_service.transports.DeliveryServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DeliveryServiceTransport()
        adc.assert_called_once()


def test_delivery_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        DeliveryServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DeliveryServiceGrpcTransport,
        transports.DeliveryServiceGrpcAsyncIOTransport,
    ],
)
def test_delivery_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DeliveryServiceGrpcTransport,
        transports.DeliveryServiceGrpcAsyncIOTransport,
        transports.DeliveryServiceRestTransport,
    ],
)
def test_delivery_service_transport_auth_gdch_credentials(transport_class):
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
        (transports.DeliveryServiceGrpcTransport, grpc_helpers),
        (transports.DeliveryServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_delivery_service_transport_create_channel(transport_class, grpc_helpers):
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
            "fleetengine.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="fleetengine.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DeliveryServiceGrpcTransport,
        transports.DeliveryServiceGrpcAsyncIOTransport,
    ],
)
def test_delivery_service_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_delivery_service_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.DeliveryServiceRestTransport(
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
def test_delivery_service_host_no_port(transport_name):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="fleetengine.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "fleetengine.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://fleetengine.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_delivery_service_host_with_port(transport_name):
    client = DeliveryServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="fleetengine.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "fleetengine.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://fleetengine.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_delivery_service_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = DeliveryServiceClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = DeliveryServiceClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.create_delivery_vehicle._session
    session2 = client2.transport.create_delivery_vehicle._session
    assert session1 != session2
    session1 = client1.transport.get_delivery_vehicle._session
    session2 = client2.transport.get_delivery_vehicle._session
    assert session1 != session2
    session1 = client1.transport.update_delivery_vehicle._session
    session2 = client2.transport.update_delivery_vehicle._session
    assert session1 != session2
    session1 = client1.transport.batch_create_tasks._session
    session2 = client2.transport.batch_create_tasks._session
    assert session1 != session2
    session1 = client1.transport.create_task._session
    session2 = client2.transport.create_task._session
    assert session1 != session2
    session1 = client1.transport.get_task._session
    session2 = client2.transport.get_task._session
    assert session1 != session2
    session1 = client1.transport.update_task._session
    session2 = client2.transport.update_task._session
    assert session1 != session2
    session1 = client1.transport.list_tasks._session
    session2 = client2.transport.list_tasks._session
    assert session1 != session2
    session1 = client1.transport.get_task_tracking_info._session
    session2 = client2.transport.get_task_tracking_info._session
    assert session1 != session2
    session1 = client1.transport.list_delivery_vehicles._session
    session2 = client2.transport.list_delivery_vehicles._session
    assert session1 != session2


def test_delivery_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DeliveryServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_delivery_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DeliveryServiceGrpcAsyncIOTransport(
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
        transports.DeliveryServiceGrpcTransport,
        transports.DeliveryServiceGrpcAsyncIOTransport,
    ],
)
def test_delivery_service_transport_channel_mtls_with_client_cert_source(
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
        transports.DeliveryServiceGrpcTransport,
        transports.DeliveryServiceGrpcAsyncIOTransport,
    ],
)
def test_delivery_service_transport_channel_mtls_with_adc(transport_class):
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


def test_delivery_vehicle_path():
    provider = "squid"
    vehicle = "clam"
    expected = "providers/{provider}/deliveryVehicles/{vehicle}".format(
        provider=provider,
        vehicle=vehicle,
    )
    actual = DeliveryServiceClient.delivery_vehicle_path(provider, vehicle)
    assert expected == actual


def test_parse_delivery_vehicle_path():
    expected = {
        "provider": "whelk",
        "vehicle": "octopus",
    }
    path = DeliveryServiceClient.delivery_vehicle_path(**expected)

    # Check that the path construction is reversible.
    actual = DeliveryServiceClient.parse_delivery_vehicle_path(path)
    assert expected == actual


def test_task_path():
    provider = "oyster"
    task = "nudibranch"
    expected = "providers/{provider}/tasks/{task}".format(
        provider=provider,
        task=task,
    )
    actual = DeliveryServiceClient.task_path(provider, task)
    assert expected == actual


def test_parse_task_path():
    expected = {
        "provider": "cuttlefish",
        "task": "mussel",
    }
    path = DeliveryServiceClient.task_path(**expected)

    # Check that the path construction is reversible.
    actual = DeliveryServiceClient.parse_task_path(path)
    assert expected == actual


def test_task_tracking_info_path():
    provider = "winkle"
    tracking = "nautilus"
    expected = "providers/{provider}/taskTrackingInfo/{tracking}".format(
        provider=provider,
        tracking=tracking,
    )
    actual = DeliveryServiceClient.task_tracking_info_path(provider, tracking)
    assert expected == actual


def test_parse_task_tracking_info_path():
    expected = {
        "provider": "scallop",
        "tracking": "abalone",
    }
    path = DeliveryServiceClient.task_tracking_info_path(**expected)

    # Check that the path construction is reversible.
    actual = DeliveryServiceClient.parse_task_tracking_info_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = DeliveryServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = DeliveryServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = DeliveryServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = DeliveryServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = DeliveryServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = DeliveryServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = DeliveryServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = DeliveryServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = DeliveryServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = DeliveryServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = DeliveryServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = DeliveryServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = DeliveryServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = DeliveryServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = DeliveryServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.DeliveryServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = DeliveryServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.DeliveryServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = DeliveryServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_transport_close_grpc():
    client = DeliveryServiceClient(
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
    client = DeliveryServiceAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close_rest():
    client = DeliveryServiceClient(
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
        client = DeliveryServiceClient(
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
        (DeliveryServiceClient, transports.DeliveryServiceGrpcTransport),
        (DeliveryServiceAsyncClient, transports.DeliveryServiceGrpcAsyncIOTransport),
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
