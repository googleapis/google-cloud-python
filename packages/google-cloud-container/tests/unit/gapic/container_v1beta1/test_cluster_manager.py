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

import math

from google.api_core import api_core_version
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest

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
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.rpc import code_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore

from google.cloud.container_v1beta1.services.cluster_manager import (
    ClusterManagerAsyncClient,
    ClusterManagerClient,
    pagers,
    transports,
)
from google.cloud.container_v1beta1.types import cluster_service


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

    assert ClusterManagerClient._get_default_mtls_endpoint(None) is None
    assert (
        ClusterManagerClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ClusterManagerClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ClusterManagerClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ClusterManagerClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ClusterManagerClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


def test__read_environment_variables():
    assert ClusterManagerClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert ClusterManagerClient._read_environment_variables() == (
            True,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert ClusterManagerClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            ClusterManagerClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert ClusterManagerClient._read_environment_variables() == (
            False,
            "never",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert ClusterManagerClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert ClusterManagerClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            ClusterManagerClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert ClusterManagerClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert ClusterManagerClient._get_client_cert_source(None, False) is None
    assert (
        ClusterManagerClient._get_client_cert_source(mock_provided_cert_source, False)
        is None
    )
    assert (
        ClusterManagerClient._get_client_cert_source(mock_provided_cert_source, True)
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
                ClusterManagerClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                ClusterManagerClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    ClusterManagerClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ClusterManagerClient),
)
@mock.patch.object(
    ClusterManagerAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ClusterManagerAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = ClusterManagerClient._DEFAULT_UNIVERSE
    default_endpoint = ClusterManagerClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = ClusterManagerClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        ClusterManagerClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        ClusterManagerClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == ClusterManagerClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        ClusterManagerClient._get_api_endpoint(None, None, default_universe, "auto")
        == default_endpoint
    )
    assert (
        ClusterManagerClient._get_api_endpoint(None, None, default_universe, "always")
        == ClusterManagerClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        ClusterManagerClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == ClusterManagerClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        ClusterManagerClient._get_api_endpoint(None, None, mock_universe, "never")
        == mock_endpoint
    )
    assert (
        ClusterManagerClient._get_api_endpoint(None, None, default_universe, "never")
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        ClusterManagerClient._get_api_endpoint(
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
        ClusterManagerClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        ClusterManagerClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        ClusterManagerClient._get_universe_domain(None, None)
        == ClusterManagerClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        ClusterManagerClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ClusterManagerClient, transports.ClusterManagerGrpcTransport, "grpc"),
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
        (ClusterManagerClient, "grpc"),
        (ClusterManagerAsyncClient, "grpc_asyncio"),
    ],
)
def test_cluster_manager_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("container.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.ClusterManagerGrpcTransport, "grpc"),
        (transports.ClusterManagerGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_cluster_manager_client_service_account_always_use_jwt(
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
        (ClusterManagerClient, "grpc"),
        (ClusterManagerAsyncClient, "grpc_asyncio"),
    ],
)
def test_cluster_manager_client_from_service_account_file(client_class, transport_name):
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

        assert client.transport._host == ("container.googleapis.com:443")


def test_cluster_manager_client_get_transport_class():
    transport = ClusterManagerClient.get_transport_class()
    available_transports = [
        transports.ClusterManagerGrpcTransport,
    ]
    assert transport in available_transports

    transport = ClusterManagerClient.get_transport_class("grpc")
    assert transport == transports.ClusterManagerGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ClusterManagerClient, transports.ClusterManagerGrpcTransport, "grpc"),
        (
            ClusterManagerAsyncClient,
            transports.ClusterManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    ClusterManagerClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ClusterManagerClient),
)
@mock.patch.object(
    ClusterManagerAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ClusterManagerAsyncClient),
)
def test_cluster_manager_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(ClusterManagerClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(ClusterManagerClient, "get_transport_class") as gtc:
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
        (ClusterManagerClient, transports.ClusterManagerGrpcTransport, "grpc", "true"),
        (
            ClusterManagerAsyncClient,
            transports.ClusterManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (ClusterManagerClient, transports.ClusterManagerGrpcTransport, "grpc", "false"),
        (
            ClusterManagerAsyncClient,
            transports.ClusterManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    ClusterManagerClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ClusterManagerClient),
)
@mock.patch.object(
    ClusterManagerAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ClusterManagerAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_cluster_manager_client_mtls_env_auto(
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
    "client_class", [ClusterManagerClient, ClusterManagerAsyncClient]
)
@mock.patch.object(
    ClusterManagerClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ClusterManagerClient),
)
@mock.patch.object(
    ClusterManagerAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ClusterManagerAsyncClient),
)
def test_cluster_manager_client_get_mtls_endpoint_and_cert_source(client_class):
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
    "client_class", [ClusterManagerClient, ClusterManagerAsyncClient]
)
@mock.patch.object(
    ClusterManagerClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ClusterManagerClient),
)
@mock.patch.object(
    ClusterManagerAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ClusterManagerAsyncClient),
)
def test_cluster_manager_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = ClusterManagerClient._DEFAULT_UNIVERSE
    default_endpoint = ClusterManagerClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = ClusterManagerClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        (ClusterManagerClient, transports.ClusterManagerGrpcTransport, "grpc"),
        (
            ClusterManagerAsyncClient,
            transports.ClusterManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_cluster_manager_client_client_options_scopes(
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
            ClusterManagerClient,
            transports.ClusterManagerGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            ClusterManagerAsyncClient,
            transports.ClusterManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_cluster_manager_client_client_options_credentials_file(
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


def test_cluster_manager_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.container_v1beta1.services.cluster_manager.transports.ClusterManagerGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ClusterManagerClient(
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
            ClusterManagerClient,
            transports.ClusterManagerGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            ClusterManagerAsyncClient,
            transports.ClusterManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_cluster_manager_client_create_channel_credentials_file(
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
            "container.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="container.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.ListClustersRequest,
        dict,
    ],
)
def test_list_clusters(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListClustersResponse(
            missing_zones=["missing_zones_value"],
        )
        response = client.list_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.ListClustersRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.ListClustersResponse)
    assert response.missing_zones == ["missing_zones_value"]


def test_list_clusters_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.ListClustersRequest(
        project_id="project_id_value",
        zone="zone_value",
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_clusters(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.ListClustersRequest(
            project_id="project_id_value",
            zone="zone_value",
            parent="parent_value",
        )


def test_list_clusters_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_clusters in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_clusters] = mock_rpc
        request = {}
        client.list_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_clusters(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_clusters_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_clusters
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_clusters
        ] = mock_rpc

        request = {}
        await client.list_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_clusters(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_clusters_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.ListClustersRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListClustersResponse(
                missing_zones=["missing_zones_value"],
            )
        )
        response = await client.list_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.ListClustersRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.ListClustersResponse)
    assert response.missing_zones == ["missing_zones_value"]


@pytest.mark.asyncio
async def test_list_clusters_async_from_dict():
    await test_list_clusters_async(request_type=dict)


def test_list_clusters_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListClustersRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        call.return_value = cluster_service.ListClustersResponse()
        client.list_clusters(request)

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
async def test_list_clusters_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListClustersRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListClustersResponse()
        )
        await client.list_clusters(request)

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


def test_list_clusters_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListClustersResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_clusters(
            project_id="project_id_value",
            zone="zone_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val


def test_list_clusters_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_clusters(
            cluster_service.ListClustersRequest(),
            project_id="project_id_value",
            zone="zone_value",
        )


@pytest.mark.asyncio
async def test_list_clusters_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListClustersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListClustersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_clusters(
            project_id="project_id_value",
            zone="zone_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_clusters_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_clusters(
            cluster_service.ListClustersRequest(),
            project_id="project_id_value",
            zone="zone_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.GetClusterRequest,
        dict,
    ],
)
def test_get_cluster(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Cluster(
            name="name_value",
            description="description_value",
            initial_node_count=1911,
            logging_service="logging_service_value",
            monitoring_service="monitoring_service_value",
            network="network_value",
            cluster_ipv4_cidr="cluster_ipv4_cidr_value",
            subnetwork="subnetwork_value",
            locations=["locations_value"],
            enable_kubernetes_alpha=True,
            label_fingerprint="label_fingerprint_value",
            private_cluster=True,
            master_ipv4_cidr_block="master_ipv4_cidr_block_value",
            self_link="self_link_value",
            zone="zone_value",
            endpoint="endpoint_value",
            initial_cluster_version="initial_cluster_version_value",
            current_master_version="current_master_version_value",
            current_node_version="current_node_version_value",
            create_time="create_time_value",
            status=cluster_service.Cluster.Status.PROVISIONING,
            status_message="status_message_value",
            node_ipv4_cidr_size=1955,
            services_ipv4_cidr="services_ipv4_cidr_value",
            instance_group_urls=["instance_group_urls_value"],
            current_node_count=1936,
            expire_time="expire_time_value",
            location="location_value",
            enable_tpu=True,
            tpu_ipv4_cidr_block="tpu_ipv4_cidr_block_value",
            id="id_value",
            etag="etag_value",
            satisfies_pzs=True,
            satisfies_pzi=True,
        )
        response = client.get_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.GetClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Cluster)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.initial_node_count == 1911
    assert response.logging_service == "logging_service_value"
    assert response.monitoring_service == "monitoring_service_value"
    assert response.network == "network_value"
    assert response.cluster_ipv4_cidr == "cluster_ipv4_cidr_value"
    assert response.subnetwork == "subnetwork_value"
    assert response.locations == ["locations_value"]
    assert response.enable_kubernetes_alpha is True
    assert response.label_fingerprint == "label_fingerprint_value"
    assert response.private_cluster is True
    assert response.master_ipv4_cidr_block == "master_ipv4_cidr_block_value"
    assert response.self_link == "self_link_value"
    assert response.zone == "zone_value"
    assert response.endpoint == "endpoint_value"
    assert response.initial_cluster_version == "initial_cluster_version_value"
    assert response.current_master_version == "current_master_version_value"
    assert response.current_node_version == "current_node_version_value"
    assert response.create_time == "create_time_value"
    assert response.status == cluster_service.Cluster.Status.PROVISIONING
    assert response.status_message == "status_message_value"
    assert response.node_ipv4_cidr_size == 1955
    assert response.services_ipv4_cidr == "services_ipv4_cidr_value"
    assert response.instance_group_urls == ["instance_group_urls_value"]
    assert response.current_node_count == 1936
    assert response.expire_time == "expire_time_value"
    assert response.location == "location_value"
    assert response.enable_tpu is True
    assert response.tpu_ipv4_cidr_block == "tpu_ipv4_cidr_block_value"
    assert response.id == "id_value"
    assert response.etag == "etag_value"
    assert response.satisfies_pzs is True
    assert response.satisfies_pzi is True


def test_get_cluster_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.GetClusterRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_cluster(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.GetClusterRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )


def test_get_cluster_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_cluster in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_cluster] = mock_rpc
        request = {}
        client.get_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_cluster_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_cluster
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_cluster
        ] = mock_rpc

        request = {}
        await client.get_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_cluster_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.GetClusterRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Cluster(
                name="name_value",
                description="description_value",
                initial_node_count=1911,
                logging_service="logging_service_value",
                monitoring_service="monitoring_service_value",
                network="network_value",
                cluster_ipv4_cidr="cluster_ipv4_cidr_value",
                subnetwork="subnetwork_value",
                locations=["locations_value"],
                enable_kubernetes_alpha=True,
                label_fingerprint="label_fingerprint_value",
                private_cluster=True,
                master_ipv4_cidr_block="master_ipv4_cidr_block_value",
                self_link="self_link_value",
                zone="zone_value",
                endpoint="endpoint_value",
                initial_cluster_version="initial_cluster_version_value",
                current_master_version="current_master_version_value",
                current_node_version="current_node_version_value",
                create_time="create_time_value",
                status=cluster_service.Cluster.Status.PROVISIONING,
                status_message="status_message_value",
                node_ipv4_cidr_size=1955,
                services_ipv4_cidr="services_ipv4_cidr_value",
                instance_group_urls=["instance_group_urls_value"],
                current_node_count=1936,
                expire_time="expire_time_value",
                location="location_value",
                enable_tpu=True,
                tpu_ipv4_cidr_block="tpu_ipv4_cidr_block_value",
                id="id_value",
                etag="etag_value",
                satisfies_pzs=True,
                satisfies_pzi=True,
            )
        )
        response = await client.get_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.GetClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Cluster)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.initial_node_count == 1911
    assert response.logging_service == "logging_service_value"
    assert response.monitoring_service == "monitoring_service_value"
    assert response.network == "network_value"
    assert response.cluster_ipv4_cidr == "cluster_ipv4_cidr_value"
    assert response.subnetwork == "subnetwork_value"
    assert response.locations == ["locations_value"]
    assert response.enable_kubernetes_alpha is True
    assert response.label_fingerprint == "label_fingerprint_value"
    assert response.private_cluster is True
    assert response.master_ipv4_cidr_block == "master_ipv4_cidr_block_value"
    assert response.self_link == "self_link_value"
    assert response.zone == "zone_value"
    assert response.endpoint == "endpoint_value"
    assert response.initial_cluster_version == "initial_cluster_version_value"
    assert response.current_master_version == "current_master_version_value"
    assert response.current_node_version == "current_node_version_value"
    assert response.create_time == "create_time_value"
    assert response.status == cluster_service.Cluster.Status.PROVISIONING
    assert response.status_message == "status_message_value"
    assert response.node_ipv4_cidr_size == 1955
    assert response.services_ipv4_cidr == "services_ipv4_cidr_value"
    assert response.instance_group_urls == ["instance_group_urls_value"]
    assert response.current_node_count == 1936
    assert response.expire_time == "expire_time_value"
    assert response.location == "location_value"
    assert response.enable_tpu is True
    assert response.tpu_ipv4_cidr_block == "tpu_ipv4_cidr_block_value"
    assert response.id == "id_value"
    assert response.etag == "etag_value"
    assert response.satisfies_pzs is True
    assert response.satisfies_pzi is True


@pytest.mark.asyncio
async def test_get_cluster_async_from_dict():
    await test_get_cluster_async(request_type=dict)


def test_get_cluster_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        call.return_value = cluster_service.Cluster()
        client.get_cluster(request)

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
async def test_get_cluster_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Cluster()
        )
        await client.get_cluster(request)

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


def test_get_cluster_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Cluster()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_cluster(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val


def test_get_cluster_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_cluster(
            cluster_service.GetClusterRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
        )


@pytest.mark.asyncio
async def test_get_cluster_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Cluster()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Cluster()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_cluster(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_cluster_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_cluster(
            cluster_service.GetClusterRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.CreateClusterRequest,
        dict,
    ],
)
def test_create_cluster(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.create_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.CreateClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_create_cluster_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.CreateClusterRequest(
        project_id="project_id_value",
        zone="zone_value",
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_cluster(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.CreateClusterRequest(
            project_id="project_id_value",
            zone="zone_value",
            parent="parent_value",
        )


def test_create_cluster_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_cluster in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.create_cluster] = mock_rpc
        request = {}
        client.create_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_cluster_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_cluster
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_cluster
        ] = mock_rpc

        request = {}
        await client.create_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.create_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_cluster_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.CreateClusterRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.create_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.CreateClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_create_cluster_async_from_dict():
    await test_create_cluster_async(request_type=dict)


def test_create_cluster_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.CreateClusterRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.create_cluster(request)

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
async def test_create_cluster_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.CreateClusterRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.create_cluster(request)

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


def test_create_cluster_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_cluster(
            project_id="project_id_value",
            zone="zone_value",
            cluster=cluster_service.Cluster(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster
        mock_val = cluster_service.Cluster(name="name_value")
        assert arg == mock_val


def test_create_cluster_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_cluster(
            cluster_service.CreateClusterRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster=cluster_service.Cluster(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_cluster_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_cluster(
            project_id="project_id_value",
            zone="zone_value",
            cluster=cluster_service.Cluster(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster
        mock_val = cluster_service.Cluster(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_cluster_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_cluster(
            cluster_service.CreateClusterRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster=cluster_service.Cluster(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.UpdateClusterRequest,
        dict,
    ],
)
def test_update_cluster(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.update_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.UpdateClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_update_cluster_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.UpdateClusterRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_cluster(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.UpdateClusterRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )


def test_update_cluster_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.update_cluster in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.update_cluster] = mock_rpc
        request = {}
        client.update_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_cluster_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_cluster
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_cluster
        ] = mock_rpc

        request = {}
        await client.update_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.update_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_cluster_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.UpdateClusterRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.update_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.UpdateClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_update_cluster_async_from_dict():
    await test_update_cluster_async(request_type=dict)


def test_update_cluster_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.UpdateClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.update_cluster(request)

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
async def test_update_cluster_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.UpdateClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.update_cluster(request)

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


def test_update_cluster_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_cluster(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            update=cluster_service.ClusterUpdate(
                desired_node_version="desired_node_version_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].update
        mock_val = cluster_service.ClusterUpdate(
            desired_node_version="desired_node_version_value"
        )
        assert arg == mock_val


def test_update_cluster_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_cluster(
            cluster_service.UpdateClusterRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            update=cluster_service.ClusterUpdate(
                desired_node_version="desired_node_version_value"
            ),
        )


@pytest.mark.asyncio
async def test_update_cluster_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_cluster(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            update=cluster_service.ClusterUpdate(
                desired_node_version="desired_node_version_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].update
        mock_val = cluster_service.ClusterUpdate(
            desired_node_version="desired_node_version_value"
        )
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_cluster_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_cluster(
            cluster_service.UpdateClusterRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            update=cluster_service.ClusterUpdate(
                desired_node_version="desired_node_version_value"
            ),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.UpdateNodePoolRequest,
        dict,
    ],
)
def test_update_node_pool(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.update_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.UpdateNodePoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_update_node_pool_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.UpdateNodePoolRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        node_pool_id="node_pool_id_value",
        node_version="node_version_value",
        image_type="image_type_value",
        name="name_value",
        etag="etag_value",
        machine_type="machine_type_value",
        disk_type="disk_type_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_node_pool), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_node_pool(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.UpdateNodePoolRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            node_version="node_version_value",
            image_type="image_type_value",
            name="name_value",
            etag="etag_value",
            machine_type="machine_type_value",
            disk_type="disk_type_value",
        )


def test_update_node_pool_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.update_node_pool in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_node_pool
        ] = mock_rpc
        request = {}
        client.update_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_node_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_node_pool_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_node_pool
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_node_pool
        ] = mock_rpc

        request = {}
        await client.update_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.update_node_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_node_pool_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.UpdateNodePoolRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.update_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.UpdateNodePoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_update_node_pool_async_from_dict():
    await test_update_node_pool_async(request_type=dict)


def test_update_node_pool_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.UpdateNodePoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_node_pool), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.update_node_pool(request)

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
async def test_update_node_pool_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.UpdateNodePoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_node_pool), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.update_node_pool(request)

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


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.SetNodePoolAutoscalingRequest,
        dict,
    ],
)
def test_set_node_pool_autoscaling(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_autoscaling), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.set_node_pool_autoscaling(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetNodePoolAutoscalingRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_set_node_pool_autoscaling_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.SetNodePoolAutoscalingRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        node_pool_id="node_pool_id_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_autoscaling), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.set_node_pool_autoscaling(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.SetNodePoolAutoscalingRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            name="name_value",
        )


def test_set_node_pool_autoscaling_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.set_node_pool_autoscaling
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.set_node_pool_autoscaling
        ] = mock_rpc
        request = {}
        client.set_node_pool_autoscaling(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.set_node_pool_autoscaling(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_node_pool_autoscaling_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.set_node_pool_autoscaling
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.set_node_pool_autoscaling
        ] = mock_rpc

        request = {}
        await client.set_node_pool_autoscaling(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.set_node_pool_autoscaling(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_node_pool_autoscaling_async(
    transport: str = "grpc_asyncio",
    request_type=cluster_service.SetNodePoolAutoscalingRequest,
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_autoscaling), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.set_node_pool_autoscaling(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetNodePoolAutoscalingRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_node_pool_autoscaling_async_from_dict():
    await test_set_node_pool_autoscaling_async(request_type=dict)


def test_set_node_pool_autoscaling_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetNodePoolAutoscalingRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_autoscaling), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.set_node_pool_autoscaling(request)

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
async def test_set_node_pool_autoscaling_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetNodePoolAutoscalingRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_autoscaling), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.set_node_pool_autoscaling(request)

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


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.SetLoggingServiceRequest,
        dict,
    ],
)
def test_set_logging_service(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_logging_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.set_logging_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetLoggingServiceRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_set_logging_service_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.SetLoggingServiceRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        logging_service="logging_service_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_logging_service), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.set_logging_service(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.SetLoggingServiceRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            logging_service="logging_service_value",
            name="name_value",
        )


def test_set_logging_service_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.set_logging_service in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.set_logging_service
        ] = mock_rpc
        request = {}
        client.set_logging_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.set_logging_service(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_logging_service_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.set_logging_service
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.set_logging_service
        ] = mock_rpc

        request = {}
        await client.set_logging_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.set_logging_service(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_logging_service_async(
    transport: str = "grpc_asyncio",
    request_type=cluster_service.SetLoggingServiceRequest,
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_logging_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.set_logging_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetLoggingServiceRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_logging_service_async_from_dict():
    await test_set_logging_service_async(request_type=dict)


def test_set_logging_service_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetLoggingServiceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_logging_service), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.set_logging_service(request)

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
async def test_set_logging_service_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetLoggingServiceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_logging_service), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.set_logging_service(request)

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


def test_set_logging_service_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_logging_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_logging_service(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            logging_service="logging_service_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].logging_service
        mock_val = "logging_service_value"
        assert arg == mock_val


def test_set_logging_service_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_logging_service(
            cluster_service.SetLoggingServiceRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            logging_service="logging_service_value",
        )


@pytest.mark.asyncio
async def test_set_logging_service_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_logging_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_logging_service(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            logging_service="logging_service_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].logging_service
        mock_val = "logging_service_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_set_logging_service_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_logging_service(
            cluster_service.SetLoggingServiceRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            logging_service="logging_service_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.SetMonitoringServiceRequest,
        dict,
    ],
)
def test_set_monitoring_service(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_monitoring_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.set_monitoring_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetMonitoringServiceRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_set_monitoring_service_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.SetMonitoringServiceRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        monitoring_service="monitoring_service_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_monitoring_service), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.set_monitoring_service(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.SetMonitoringServiceRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            monitoring_service="monitoring_service_value",
            name="name_value",
        )


def test_set_monitoring_service_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.set_monitoring_service
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.set_monitoring_service
        ] = mock_rpc
        request = {}
        client.set_monitoring_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.set_monitoring_service(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_monitoring_service_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.set_monitoring_service
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.set_monitoring_service
        ] = mock_rpc

        request = {}
        await client.set_monitoring_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.set_monitoring_service(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_monitoring_service_async(
    transport: str = "grpc_asyncio",
    request_type=cluster_service.SetMonitoringServiceRequest,
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_monitoring_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.set_monitoring_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetMonitoringServiceRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_monitoring_service_async_from_dict():
    await test_set_monitoring_service_async(request_type=dict)


def test_set_monitoring_service_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetMonitoringServiceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_monitoring_service), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.set_monitoring_service(request)

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
async def test_set_monitoring_service_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetMonitoringServiceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_monitoring_service), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.set_monitoring_service(request)

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


def test_set_monitoring_service_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_monitoring_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_monitoring_service(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            monitoring_service="monitoring_service_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].monitoring_service
        mock_val = "monitoring_service_value"
        assert arg == mock_val


def test_set_monitoring_service_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_monitoring_service(
            cluster_service.SetMonitoringServiceRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            monitoring_service="monitoring_service_value",
        )


@pytest.mark.asyncio
async def test_set_monitoring_service_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_monitoring_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_monitoring_service(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            monitoring_service="monitoring_service_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].monitoring_service
        mock_val = "monitoring_service_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_set_monitoring_service_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_monitoring_service(
            cluster_service.SetMonitoringServiceRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            monitoring_service="monitoring_service_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.SetAddonsConfigRequest,
        dict,
    ],
)
def test_set_addons_config(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_addons_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.set_addons_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetAddonsConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_set_addons_config_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.SetAddonsConfigRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_addons_config), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.set_addons_config(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.SetAddonsConfigRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )


def test_set_addons_config_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.set_addons_config in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.set_addons_config
        ] = mock_rpc
        request = {}
        client.set_addons_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.set_addons_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_addons_config_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.set_addons_config
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.set_addons_config
        ] = mock_rpc

        request = {}
        await client.set_addons_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.set_addons_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_addons_config_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.SetAddonsConfigRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_addons_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.set_addons_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetAddonsConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_addons_config_async_from_dict():
    await test_set_addons_config_async(request_type=dict)


def test_set_addons_config_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetAddonsConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_addons_config), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.set_addons_config(request)

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
async def test_set_addons_config_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetAddonsConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_addons_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.set_addons_config(request)

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


def test_set_addons_config_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_addons_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_addons_config(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            addons_config=cluster_service.AddonsConfig(
                http_load_balancing=cluster_service.HttpLoadBalancing(disabled=True)
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].addons_config
        mock_val = cluster_service.AddonsConfig(
            http_load_balancing=cluster_service.HttpLoadBalancing(disabled=True)
        )
        assert arg == mock_val


def test_set_addons_config_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_addons_config(
            cluster_service.SetAddonsConfigRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            addons_config=cluster_service.AddonsConfig(
                http_load_balancing=cluster_service.HttpLoadBalancing(disabled=True)
            ),
        )


@pytest.mark.asyncio
async def test_set_addons_config_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_addons_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_addons_config(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            addons_config=cluster_service.AddonsConfig(
                http_load_balancing=cluster_service.HttpLoadBalancing(disabled=True)
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].addons_config
        mock_val = cluster_service.AddonsConfig(
            http_load_balancing=cluster_service.HttpLoadBalancing(disabled=True)
        )
        assert arg == mock_val


@pytest.mark.asyncio
async def test_set_addons_config_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_addons_config(
            cluster_service.SetAddonsConfigRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            addons_config=cluster_service.AddonsConfig(
                http_load_balancing=cluster_service.HttpLoadBalancing(disabled=True)
            ),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.SetLocationsRequest,
        dict,
    ],
)
def test_set_locations(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.set_locations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetLocationsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_set_locations_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.SetLocationsRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_locations), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.set_locations(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.SetLocationsRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )


def test_set_locations_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.set_locations in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.set_locations] = mock_rpc
        request = {}
        client.set_locations(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.set_locations(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_locations_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.set_locations
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.set_locations
        ] = mock_rpc

        request = {}
        await client.set_locations(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.set_locations(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_locations_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.SetLocationsRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.set_locations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetLocationsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_locations_async_from_dict():
    await test_set_locations_async(request_type=dict)


def test_set_locations_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetLocationsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_locations), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.set_locations(request)

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
async def test_set_locations_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetLocationsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_locations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.set_locations(request)

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


def test_set_locations_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_locations(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            locations=["locations_value"],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].locations
        mock_val = ["locations_value"]
        assert arg == mock_val


def test_set_locations_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_locations(
            cluster_service.SetLocationsRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            locations=["locations_value"],
        )


@pytest.mark.asyncio
async def test_set_locations_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_locations(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            locations=["locations_value"],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].locations
        mock_val = ["locations_value"]
        assert arg == mock_val


@pytest.mark.asyncio
async def test_set_locations_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_locations(
            cluster_service.SetLocationsRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            locations=["locations_value"],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.UpdateMasterRequest,
        dict,
    ],
)
def test_update_master(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_master), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.update_master(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.UpdateMasterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_update_master_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.UpdateMasterRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        master_version="master_version_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_master), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_master(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.UpdateMasterRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            master_version="master_version_value",
            name="name_value",
        )


def test_update_master_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.update_master in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.update_master] = mock_rpc
        request = {}
        client.update_master(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_master(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_master_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_master
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_master
        ] = mock_rpc

        request = {}
        await client.update_master(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.update_master(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_master_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.UpdateMasterRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_master), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.update_master(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.UpdateMasterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_update_master_async_from_dict():
    await test_update_master_async(request_type=dict)


def test_update_master_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.UpdateMasterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_master), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.update_master(request)

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
async def test_update_master_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.UpdateMasterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_master), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.update_master(request)

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


def test_update_master_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_master), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_master(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            master_version="master_version_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].master_version
        mock_val = "master_version_value"
        assert arg == mock_val


def test_update_master_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_master(
            cluster_service.UpdateMasterRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            master_version="master_version_value",
        )


@pytest.mark.asyncio
async def test_update_master_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_master), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_master(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            master_version="master_version_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].master_version
        mock_val = "master_version_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_master_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_master(
            cluster_service.UpdateMasterRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            master_version="master_version_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.SetMasterAuthRequest,
        dict,
    ],
)
def test_set_master_auth(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_master_auth), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.set_master_auth(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetMasterAuthRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_set_master_auth_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.SetMasterAuthRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_master_auth), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.set_master_auth(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.SetMasterAuthRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )


def test_set_master_auth_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.set_master_auth in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.set_master_auth] = mock_rpc
        request = {}
        client.set_master_auth(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.set_master_auth(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_master_auth_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.set_master_auth
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.set_master_auth
        ] = mock_rpc

        request = {}
        await client.set_master_auth(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.set_master_auth(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_master_auth_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.SetMasterAuthRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_master_auth), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.set_master_auth(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetMasterAuthRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_master_auth_async_from_dict():
    await test_set_master_auth_async(request_type=dict)


def test_set_master_auth_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetMasterAuthRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_master_auth), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.set_master_auth(request)

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
async def test_set_master_auth_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetMasterAuthRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_master_auth), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.set_master_auth(request)

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


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.DeleteClusterRequest,
        dict,
    ],
)
def test_delete_cluster(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.delete_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.DeleteClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_delete_cluster_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.DeleteClusterRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_cluster(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.DeleteClusterRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )


def test_delete_cluster_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.delete_cluster in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.delete_cluster] = mock_rpc
        request = {}
        client.delete_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_cluster_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_cluster
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_cluster
        ] = mock_rpc

        request = {}
        await client.delete_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.delete_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_cluster_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.DeleteClusterRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.delete_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.DeleteClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_delete_cluster_async_from_dict():
    await test_delete_cluster_async(request_type=dict)


def test_delete_cluster_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.DeleteClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.delete_cluster(request)

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
async def test_delete_cluster_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.DeleteClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.delete_cluster(request)

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


def test_delete_cluster_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_cluster(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val


def test_delete_cluster_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_cluster(
            cluster_service.DeleteClusterRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
        )


@pytest.mark.asyncio
async def test_delete_cluster_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_cluster(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_cluster_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_cluster(
            cluster_service.DeleteClusterRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.ListOperationsRequest,
        dict,
    ],
)
def test_list_operations(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListOperationsResponse(
            missing_zones=["missing_zones_value"],
        )
        response = client.list_operations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.ListOperationsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.ListOperationsResponse)
    assert response.missing_zones == ["missing_zones_value"]


def test_list_operations_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.ListOperationsRequest(
        project_id="project_id_value",
        zone="zone_value",
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_operations(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.ListOperationsRequest(
            project_id="project_id_value",
            zone="zone_value",
            parent="parent_value",
        )


def test_list_operations_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_operations in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_operations] = mock_rpc
        request = {}
        client.list_operations(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_operations(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_operations_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_operations
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_operations
        ] = mock_rpc

        request = {}
        await client.list_operations(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_operations(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_operations_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.ListOperationsRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListOperationsResponse(
                missing_zones=["missing_zones_value"],
            )
        )
        response = await client.list_operations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.ListOperationsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.ListOperationsResponse)
    assert response.missing_zones == ["missing_zones_value"]


@pytest.mark.asyncio
async def test_list_operations_async_from_dict():
    await test_list_operations_async(request_type=dict)


def test_list_operations_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListOperationsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = cluster_service.ListOperationsResponse()
        client.list_operations(request)

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
async def test_list_operations_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListOperationsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListOperationsResponse()
        )
        await client.list_operations(request)

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


def test_list_operations_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListOperationsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_operations(
            project_id="project_id_value",
            zone="zone_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val


def test_list_operations_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_operations(
            cluster_service.ListOperationsRequest(),
            project_id="project_id_value",
            zone="zone_value",
        )


@pytest.mark.asyncio
async def test_list_operations_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListOperationsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListOperationsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_operations(
            project_id="project_id_value",
            zone="zone_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_operations_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_operations(
            cluster_service.ListOperationsRequest(),
            project_id="project_id_value",
            zone="zone_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.GetOperationRequest,
        dict,
    ],
)
def test_get_operation(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.get_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.GetOperationRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_get_operation_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.GetOperationRequest(
        project_id="project_id_value",
        zone="zone_value",
        operation_id="operation_id_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_operation(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.GetOperationRequest(
            project_id="project_id_value",
            zone="zone_value",
            operation_id="operation_id_value",
            name="name_value",
        )


def test_get_operation_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_operation in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_operation] = mock_rpc
        request = {}
        client.get_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_operation(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_operation_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_operation
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_operation
        ] = mock_rpc

        request = {}
        await client.get_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_operation(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_operation_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.GetOperationRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.get_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.GetOperationRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_get_operation_async_from_dict():
    await test_get_operation_async(request_type=dict)


def test_get_operation_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetOperationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.get_operation(request)

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
async def test_get_operation_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetOperationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.get_operation(request)

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


def test_get_operation_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_operation(
            project_id="project_id_value",
            zone="zone_value",
            operation_id="operation_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].operation_id
        mock_val = "operation_id_value"
        assert arg == mock_val


def test_get_operation_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_operation(
            cluster_service.GetOperationRequest(),
            project_id="project_id_value",
            zone="zone_value",
            operation_id="operation_id_value",
        )


@pytest.mark.asyncio
async def test_get_operation_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_operation(
            project_id="project_id_value",
            zone="zone_value",
            operation_id="operation_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].operation_id
        mock_val = "operation_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_operation_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_operation(
            cluster_service.GetOperationRequest(),
            project_id="project_id_value",
            zone="zone_value",
            operation_id="operation_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.CancelOperationRequest,
        dict,
    ],
)
def test_cancel_operation(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.cancel_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.CancelOperationRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_cancel_operation_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.CancelOperationRequest(
        project_id="project_id_value",
        zone="zone_value",
        operation_id="operation_id_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.cancel_operation(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.CancelOperationRequest(
            project_id="project_id_value",
            zone="zone_value",
            operation_id="operation_id_value",
            name="name_value",
        )


def test_cancel_operation_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.cancel_operation in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.cancel_operation
        ] = mock_rpc
        request = {}
        client.cancel_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.cancel_operation(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_cancel_operation_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.cancel_operation
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.cancel_operation
        ] = mock_rpc

        request = {}
        await client.cancel_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.cancel_operation(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_cancel_operation_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.CancelOperationRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.CancelOperationRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_cancel_operation_async_from_dict():
    await test_cancel_operation_async(request_type=dict)


def test_cancel_operation_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.CancelOperationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = None
        client.cancel_operation(request)

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
async def test_cancel_operation_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.CancelOperationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.cancel_operation(request)

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


def test_cancel_operation_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.cancel_operation(
            project_id="project_id_value",
            zone="zone_value",
            operation_id="operation_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].operation_id
        mock_val = "operation_id_value"
        assert arg == mock_val


def test_cancel_operation_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.cancel_operation(
            cluster_service.CancelOperationRequest(),
            project_id="project_id_value",
            zone="zone_value",
            operation_id="operation_id_value",
        )


@pytest.mark.asyncio
async def test_cancel_operation_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.cancel_operation(
            project_id="project_id_value",
            zone="zone_value",
            operation_id="operation_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].operation_id
        mock_val = "operation_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_cancel_operation_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.cancel_operation(
            cluster_service.CancelOperationRequest(),
            project_id="project_id_value",
            zone="zone_value",
            operation_id="operation_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.GetServerConfigRequest,
        dict,
    ],
)
def test_get_server_config(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ServerConfig(
            default_cluster_version="default_cluster_version_value",
            valid_node_versions=["valid_node_versions_value"],
            default_image_type="default_image_type_value",
            valid_image_types=["valid_image_types_value"],
            valid_master_versions=["valid_master_versions_value"],
        )
        response = client.get_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.GetServerConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.ServerConfig)
    assert response.default_cluster_version == "default_cluster_version_value"
    assert response.valid_node_versions == ["valid_node_versions_value"]
    assert response.default_image_type == "default_image_type_value"
    assert response.valid_image_types == ["valid_image_types_value"]
    assert response.valid_master_versions == ["valid_master_versions_value"]


def test_get_server_config_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.GetServerConfigRequest(
        project_id="project_id_value",
        zone="zone_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_server_config(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.GetServerConfigRequest(
            project_id="project_id_value",
            zone="zone_value",
            name="name_value",
        )


def test_get_server_config_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_server_config in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_server_config
        ] = mock_rpc
        request = {}
        client.get_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_server_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_server_config_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_server_config
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_server_config
        ] = mock_rpc

        request = {}
        await client.get_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_server_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_server_config_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.GetServerConfigRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ServerConfig(
                default_cluster_version="default_cluster_version_value",
                valid_node_versions=["valid_node_versions_value"],
                default_image_type="default_image_type_value",
                valid_image_types=["valid_image_types_value"],
                valid_master_versions=["valid_master_versions_value"],
            )
        )
        response = await client.get_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.GetServerConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.ServerConfig)
    assert response.default_cluster_version == "default_cluster_version_value"
    assert response.valid_node_versions == ["valid_node_versions_value"]
    assert response.default_image_type == "default_image_type_value"
    assert response.valid_image_types == ["valid_image_types_value"]
    assert response.valid_master_versions == ["valid_master_versions_value"]


@pytest.mark.asyncio
async def test_get_server_config_async_from_dict():
    await test_get_server_config_async(request_type=dict)


def test_get_server_config_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetServerConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        call.return_value = cluster_service.ServerConfig()
        client.get_server_config(request)

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
async def test_get_server_config_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetServerConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ServerConfig()
        )
        await client.get_server_config(request)

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


def test_get_server_config_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ServerConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_server_config(
            project_id="project_id_value",
            zone="zone_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val


def test_get_server_config_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_server_config(
            cluster_service.GetServerConfigRequest(),
            project_id="project_id_value",
            zone="zone_value",
        )


@pytest.mark.asyncio
async def test_get_server_config_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ServerConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ServerConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_server_config(
            project_id="project_id_value",
            zone="zone_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_server_config_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_server_config(
            cluster_service.GetServerConfigRequest(),
            project_id="project_id_value",
            zone="zone_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.GetJSONWebKeysRequest,
        dict,
    ],
)
def test_get_json_web_keys(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_json_web_keys), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.GetJSONWebKeysResponse()
        response = client.get_json_web_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.GetJSONWebKeysRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.GetJSONWebKeysResponse)


def test_get_json_web_keys_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.GetJSONWebKeysRequest(
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_json_web_keys), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_json_web_keys(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.GetJSONWebKeysRequest(
            parent="parent_value",
        )


def test_get_json_web_keys_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_json_web_keys in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_json_web_keys
        ] = mock_rpc
        request = {}
        client.get_json_web_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_json_web_keys(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_json_web_keys_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_json_web_keys
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_json_web_keys
        ] = mock_rpc

        request = {}
        await client.get_json_web_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_json_web_keys(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_json_web_keys_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.GetJSONWebKeysRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_json_web_keys), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.GetJSONWebKeysResponse()
        )
        response = await client.get_json_web_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.GetJSONWebKeysRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.GetJSONWebKeysResponse)


@pytest.mark.asyncio
async def test_get_json_web_keys_async_from_dict():
    await test_get_json_web_keys_async(request_type=dict)


def test_get_json_web_keys_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetJSONWebKeysRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_json_web_keys), "__call__"
    ) as call:
        call.return_value = cluster_service.GetJSONWebKeysResponse()
        client.get_json_web_keys(request)

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
async def test_get_json_web_keys_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetJSONWebKeysRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_json_web_keys), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.GetJSONWebKeysResponse()
        )
        await client.get_json_web_keys(request)

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


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.ListNodePoolsRequest,
        dict,
    ],
)
def test_list_node_pools(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListNodePoolsResponse()
        response = client.list_node_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.ListNodePoolsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.ListNodePoolsResponse)


def test_list_node_pools_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.ListNodePoolsRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_node_pools(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.ListNodePoolsRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            parent="parent_value",
        )


def test_list_node_pools_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_node_pools in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_node_pools] = mock_rpc
        request = {}
        client.list_node_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_node_pools(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_node_pools_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_node_pools
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_node_pools
        ] = mock_rpc

        request = {}
        await client.list_node_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_node_pools(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_node_pools_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.ListNodePoolsRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListNodePoolsResponse()
        )
        response = await client.list_node_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.ListNodePoolsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.ListNodePoolsResponse)


@pytest.mark.asyncio
async def test_list_node_pools_async_from_dict():
    await test_list_node_pools_async(request_type=dict)


def test_list_node_pools_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListNodePoolsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        call.return_value = cluster_service.ListNodePoolsResponse()
        client.list_node_pools(request)

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
async def test_list_node_pools_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListNodePoolsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListNodePoolsResponse()
        )
        await client.list_node_pools(request)

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


def test_list_node_pools_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListNodePoolsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_node_pools(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val


def test_list_node_pools_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_node_pools(
            cluster_service.ListNodePoolsRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
        )


@pytest.mark.asyncio
async def test_list_node_pools_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListNodePoolsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListNodePoolsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_node_pools(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_node_pools_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_node_pools(
            cluster_service.ListNodePoolsRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.GetNodePoolRequest,
        dict,
    ],
)
def test_get_node_pool(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.NodePool(
            name="name_value",
            initial_node_count=1911,
            locations=["locations_value"],
            self_link="self_link_value",
            version="version_value",
            instance_group_urls=["instance_group_urls_value"],
            status=cluster_service.NodePool.Status.PROVISIONING,
            status_message="status_message_value",
            pod_ipv4_cidr_size=1856,
            etag="etag_value",
        )
        response = client.get_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.GetNodePoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.NodePool)
    assert response.name == "name_value"
    assert response.initial_node_count == 1911
    assert response.locations == ["locations_value"]
    assert response.self_link == "self_link_value"
    assert response.version == "version_value"
    assert response.instance_group_urls == ["instance_group_urls_value"]
    assert response.status == cluster_service.NodePool.Status.PROVISIONING
    assert response.status_message == "status_message_value"
    assert response.pod_ipv4_cidr_size == 1856
    assert response.etag == "etag_value"


def test_get_node_pool_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.GetNodePoolRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        node_pool_id="node_pool_id_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_node_pool(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.GetNodePoolRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            name="name_value",
        )


def test_get_node_pool_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_node_pool in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_node_pool] = mock_rpc
        request = {}
        client.get_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_node_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_node_pool_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_node_pool
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_node_pool
        ] = mock_rpc

        request = {}
        await client.get_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_node_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_node_pool_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.GetNodePoolRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.NodePool(
                name="name_value",
                initial_node_count=1911,
                locations=["locations_value"],
                self_link="self_link_value",
                version="version_value",
                instance_group_urls=["instance_group_urls_value"],
                status=cluster_service.NodePool.Status.PROVISIONING,
                status_message="status_message_value",
                pod_ipv4_cidr_size=1856,
                etag="etag_value",
            )
        )
        response = await client.get_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.GetNodePoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.NodePool)
    assert response.name == "name_value"
    assert response.initial_node_count == 1911
    assert response.locations == ["locations_value"]
    assert response.self_link == "self_link_value"
    assert response.version == "version_value"
    assert response.instance_group_urls == ["instance_group_urls_value"]
    assert response.status == cluster_service.NodePool.Status.PROVISIONING
    assert response.status_message == "status_message_value"
    assert response.pod_ipv4_cidr_size == 1856
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_get_node_pool_async_from_dict():
    await test_get_node_pool_async(request_type=dict)


def test_get_node_pool_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetNodePoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        call.return_value = cluster_service.NodePool()
        client.get_node_pool(request)

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
async def test_get_node_pool_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetNodePoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.NodePool()
        )
        await client.get_node_pool(request)

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


def test_get_node_pool_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.NodePool()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_node_pool(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].node_pool_id
        mock_val = "node_pool_id_value"
        assert arg == mock_val


def test_get_node_pool_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_node_pool(
            cluster_service.GetNodePoolRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
        )


@pytest.mark.asyncio
async def test_get_node_pool_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.NodePool()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.NodePool()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_node_pool(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].node_pool_id
        mock_val = "node_pool_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_node_pool_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_node_pool(
            cluster_service.GetNodePoolRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.CreateNodePoolRequest,
        dict,
    ],
)
def test_create_node_pool(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.create_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.CreateNodePoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_create_node_pool_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.CreateNodePoolRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_node_pool(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.CreateNodePoolRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            parent="parent_value",
        )


def test_create_node_pool_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_node_pool in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_node_pool
        ] = mock_rpc
        request = {}
        client.create_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_node_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_node_pool_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_node_pool
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_node_pool
        ] = mock_rpc

        request = {}
        await client.create_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.create_node_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_node_pool_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.CreateNodePoolRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.create_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.CreateNodePoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_create_node_pool_async_from_dict():
    await test_create_node_pool_async(request_type=dict)


def test_create_node_pool_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.CreateNodePoolRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.create_node_pool(request)

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
async def test_create_node_pool_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.CreateNodePoolRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.create_node_pool(request)

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


def test_create_node_pool_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_node_pool(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool=cluster_service.NodePool(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].node_pool
        mock_val = cluster_service.NodePool(name="name_value")
        assert arg == mock_val


def test_create_node_pool_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_node_pool(
            cluster_service.CreateNodePoolRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool=cluster_service.NodePool(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_node_pool_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_node_pool(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool=cluster_service.NodePool(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].node_pool
        mock_val = cluster_service.NodePool(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_node_pool_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_node_pool(
            cluster_service.CreateNodePoolRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool=cluster_service.NodePool(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.DeleteNodePoolRequest,
        dict,
    ],
)
def test_delete_node_pool(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.delete_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.DeleteNodePoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_delete_node_pool_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.DeleteNodePoolRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        node_pool_id="node_pool_id_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_node_pool(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.DeleteNodePoolRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            name="name_value",
        )


def test_delete_node_pool_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.delete_node_pool in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_node_pool
        ] = mock_rpc
        request = {}
        client.delete_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_node_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_node_pool_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_node_pool
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_node_pool
        ] = mock_rpc

        request = {}
        await client.delete_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.delete_node_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_node_pool_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.DeleteNodePoolRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.delete_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.DeleteNodePoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_delete_node_pool_async_from_dict():
    await test_delete_node_pool_async(request_type=dict)


def test_delete_node_pool_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.DeleteNodePoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.delete_node_pool(request)

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
async def test_delete_node_pool_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.DeleteNodePoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.delete_node_pool(request)

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


def test_delete_node_pool_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_node_pool(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].node_pool_id
        mock_val = "node_pool_id_value"
        assert arg == mock_val


def test_delete_node_pool_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_node_pool(
            cluster_service.DeleteNodePoolRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
        )


@pytest.mark.asyncio
async def test_delete_node_pool_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_node_pool(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].node_pool_id
        mock_val = "node_pool_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_node_pool_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_node_pool(
            cluster_service.DeleteNodePoolRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.CompleteNodePoolUpgradeRequest,
        dict,
    ],
)
def test_complete_node_pool_upgrade(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_node_pool_upgrade), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.complete_node_pool_upgrade(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.CompleteNodePoolUpgradeRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_complete_node_pool_upgrade_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.CompleteNodePoolUpgradeRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_node_pool_upgrade), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.complete_node_pool_upgrade(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.CompleteNodePoolUpgradeRequest(
            name="name_value",
        )


def test_complete_node_pool_upgrade_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.complete_node_pool_upgrade
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.complete_node_pool_upgrade
        ] = mock_rpc
        request = {}
        client.complete_node_pool_upgrade(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.complete_node_pool_upgrade(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_complete_node_pool_upgrade_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.complete_node_pool_upgrade
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.complete_node_pool_upgrade
        ] = mock_rpc

        request = {}
        await client.complete_node_pool_upgrade(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.complete_node_pool_upgrade(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_complete_node_pool_upgrade_async(
    transport: str = "grpc_asyncio",
    request_type=cluster_service.CompleteNodePoolUpgradeRequest,
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_node_pool_upgrade), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.complete_node_pool_upgrade(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.CompleteNodePoolUpgradeRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_complete_node_pool_upgrade_async_from_dict():
    await test_complete_node_pool_upgrade_async(request_type=dict)


def test_complete_node_pool_upgrade_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.CompleteNodePoolUpgradeRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_node_pool_upgrade), "__call__"
    ) as call:
        call.return_value = None
        client.complete_node_pool_upgrade(request)

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
async def test_complete_node_pool_upgrade_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.CompleteNodePoolUpgradeRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_node_pool_upgrade), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.complete_node_pool_upgrade(request)

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


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.RollbackNodePoolUpgradeRequest,
        dict,
    ],
)
def test_rollback_node_pool_upgrade(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_node_pool_upgrade), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.rollback_node_pool_upgrade(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.RollbackNodePoolUpgradeRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_rollback_node_pool_upgrade_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.RollbackNodePoolUpgradeRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        node_pool_id="node_pool_id_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_node_pool_upgrade), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.rollback_node_pool_upgrade(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.RollbackNodePoolUpgradeRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            name="name_value",
        )


def test_rollback_node_pool_upgrade_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.rollback_node_pool_upgrade
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.rollback_node_pool_upgrade
        ] = mock_rpc
        request = {}
        client.rollback_node_pool_upgrade(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.rollback_node_pool_upgrade(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_rollback_node_pool_upgrade_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.rollback_node_pool_upgrade
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.rollback_node_pool_upgrade
        ] = mock_rpc

        request = {}
        await client.rollback_node_pool_upgrade(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.rollback_node_pool_upgrade(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_rollback_node_pool_upgrade_async(
    transport: str = "grpc_asyncio",
    request_type=cluster_service.RollbackNodePoolUpgradeRequest,
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_node_pool_upgrade), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.rollback_node_pool_upgrade(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.RollbackNodePoolUpgradeRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_rollback_node_pool_upgrade_async_from_dict():
    await test_rollback_node_pool_upgrade_async(request_type=dict)


def test_rollback_node_pool_upgrade_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.RollbackNodePoolUpgradeRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_node_pool_upgrade), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.rollback_node_pool_upgrade(request)

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
async def test_rollback_node_pool_upgrade_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.RollbackNodePoolUpgradeRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_node_pool_upgrade), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.rollback_node_pool_upgrade(request)

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


def test_rollback_node_pool_upgrade_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_node_pool_upgrade), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.rollback_node_pool_upgrade(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].node_pool_id
        mock_val = "node_pool_id_value"
        assert arg == mock_val


def test_rollback_node_pool_upgrade_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.rollback_node_pool_upgrade(
            cluster_service.RollbackNodePoolUpgradeRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
        )


@pytest.mark.asyncio
async def test_rollback_node_pool_upgrade_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_node_pool_upgrade), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.rollback_node_pool_upgrade(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].node_pool_id
        mock_val = "node_pool_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_rollback_node_pool_upgrade_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.rollback_node_pool_upgrade(
            cluster_service.RollbackNodePoolUpgradeRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.SetNodePoolManagementRequest,
        dict,
    ],
)
def test_set_node_pool_management(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_management), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.set_node_pool_management(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetNodePoolManagementRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_set_node_pool_management_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.SetNodePoolManagementRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        node_pool_id="node_pool_id_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_management), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.set_node_pool_management(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.SetNodePoolManagementRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            name="name_value",
        )


def test_set_node_pool_management_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.set_node_pool_management
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.set_node_pool_management
        ] = mock_rpc
        request = {}
        client.set_node_pool_management(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.set_node_pool_management(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_node_pool_management_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.set_node_pool_management
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.set_node_pool_management
        ] = mock_rpc

        request = {}
        await client.set_node_pool_management(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.set_node_pool_management(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_node_pool_management_async(
    transport: str = "grpc_asyncio",
    request_type=cluster_service.SetNodePoolManagementRequest,
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_management), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.set_node_pool_management(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetNodePoolManagementRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_node_pool_management_async_from_dict():
    await test_set_node_pool_management_async(request_type=dict)


def test_set_node_pool_management_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetNodePoolManagementRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_management), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.set_node_pool_management(request)

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
async def test_set_node_pool_management_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetNodePoolManagementRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_management), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.set_node_pool_management(request)

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


def test_set_node_pool_management_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_management), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_node_pool_management(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            management=cluster_service.NodeManagement(auto_upgrade=True),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].node_pool_id
        mock_val = "node_pool_id_value"
        assert arg == mock_val
        arg = args[0].management
        mock_val = cluster_service.NodeManagement(auto_upgrade=True)
        assert arg == mock_val


def test_set_node_pool_management_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_node_pool_management(
            cluster_service.SetNodePoolManagementRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            management=cluster_service.NodeManagement(auto_upgrade=True),
        )


@pytest.mark.asyncio
async def test_set_node_pool_management_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_management), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_node_pool_management(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            management=cluster_service.NodeManagement(auto_upgrade=True),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].node_pool_id
        mock_val = "node_pool_id_value"
        assert arg == mock_val
        arg = args[0].management
        mock_val = cluster_service.NodeManagement(auto_upgrade=True)
        assert arg == mock_val


@pytest.mark.asyncio
async def test_set_node_pool_management_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_node_pool_management(
            cluster_service.SetNodePoolManagementRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            management=cluster_service.NodeManagement(auto_upgrade=True),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.SetLabelsRequest,
        dict,
    ],
)
def test_set_labels(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_labels), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.set_labels(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetLabelsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_set_labels_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.SetLabelsRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        label_fingerprint="label_fingerprint_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_labels), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.set_labels(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.SetLabelsRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            label_fingerprint="label_fingerprint_value",
            name="name_value",
        )


def test_set_labels_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.set_labels in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.set_labels] = mock_rpc
        request = {}
        client.set_labels(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.set_labels(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_labels_async_use_cached_wrapped_rpc(transport: str = "grpc_asyncio"):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.set_labels
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.set_labels
        ] = mock_rpc

        request = {}
        await client.set_labels(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.set_labels(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_labels_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.SetLabelsRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_labels), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.set_labels(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetLabelsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_labels_async_from_dict():
    await test_set_labels_async(request_type=dict)


def test_set_labels_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetLabelsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_labels), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.set_labels(request)

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
async def test_set_labels_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetLabelsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_labels), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.set_labels(request)

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


def test_set_labels_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_labels), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_labels(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            resource_labels={"key_value": "value_value"},
            label_fingerprint="label_fingerprint_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].resource_labels
        mock_val = {"key_value": "value_value"}
        assert arg == mock_val
        arg = args[0].label_fingerprint
        mock_val = "label_fingerprint_value"
        assert arg == mock_val


def test_set_labels_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_labels(
            cluster_service.SetLabelsRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            resource_labels={"key_value": "value_value"},
            label_fingerprint="label_fingerprint_value",
        )


@pytest.mark.asyncio
async def test_set_labels_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_labels), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_labels(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            resource_labels={"key_value": "value_value"},
            label_fingerprint="label_fingerprint_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].resource_labels
        mock_val = {"key_value": "value_value"}
        assert arg == mock_val
        arg = args[0].label_fingerprint
        mock_val = "label_fingerprint_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_set_labels_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_labels(
            cluster_service.SetLabelsRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            resource_labels={"key_value": "value_value"},
            label_fingerprint="label_fingerprint_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.SetLegacyAbacRequest,
        dict,
    ],
)
def test_set_legacy_abac(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_legacy_abac), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.set_legacy_abac(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetLegacyAbacRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_set_legacy_abac_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.SetLegacyAbacRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_legacy_abac), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.set_legacy_abac(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.SetLegacyAbacRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )


def test_set_legacy_abac_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.set_legacy_abac in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.set_legacy_abac] = mock_rpc
        request = {}
        client.set_legacy_abac(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.set_legacy_abac(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_legacy_abac_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.set_legacy_abac
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.set_legacy_abac
        ] = mock_rpc

        request = {}
        await client.set_legacy_abac(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.set_legacy_abac(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_legacy_abac_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.SetLegacyAbacRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_legacy_abac), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.set_legacy_abac(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetLegacyAbacRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_legacy_abac_async_from_dict():
    await test_set_legacy_abac_async(request_type=dict)


def test_set_legacy_abac_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetLegacyAbacRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_legacy_abac), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.set_legacy_abac(request)

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
async def test_set_legacy_abac_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetLegacyAbacRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_legacy_abac), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.set_legacy_abac(request)

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


def test_set_legacy_abac_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_legacy_abac), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_legacy_abac(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            enabled=True,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].enabled
        mock_val = True
        assert arg == mock_val


def test_set_legacy_abac_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_legacy_abac(
            cluster_service.SetLegacyAbacRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            enabled=True,
        )


@pytest.mark.asyncio
async def test_set_legacy_abac_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_legacy_abac), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_legacy_abac(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            enabled=True,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].enabled
        mock_val = True
        assert arg == mock_val


@pytest.mark.asyncio
async def test_set_legacy_abac_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_legacy_abac(
            cluster_service.SetLegacyAbacRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            enabled=True,
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.StartIPRotationRequest,
        dict,
    ],
)
def test_start_ip_rotation(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_ip_rotation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.start_ip_rotation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.StartIPRotationRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_start_ip_rotation_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.StartIPRotationRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_ip_rotation), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.start_ip_rotation(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.StartIPRotationRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )


def test_start_ip_rotation_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.start_ip_rotation in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.start_ip_rotation
        ] = mock_rpc
        request = {}
        client.start_ip_rotation(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.start_ip_rotation(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_start_ip_rotation_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.start_ip_rotation
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.start_ip_rotation
        ] = mock_rpc

        request = {}
        await client.start_ip_rotation(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.start_ip_rotation(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_start_ip_rotation_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.StartIPRotationRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_ip_rotation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.start_ip_rotation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.StartIPRotationRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_start_ip_rotation_async_from_dict():
    await test_start_ip_rotation_async(request_type=dict)


def test_start_ip_rotation_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.StartIPRotationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_ip_rotation), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.start_ip_rotation(request)

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
async def test_start_ip_rotation_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.StartIPRotationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_ip_rotation), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.start_ip_rotation(request)

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


def test_start_ip_rotation_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_ip_rotation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.start_ip_rotation(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val


def test_start_ip_rotation_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.start_ip_rotation(
            cluster_service.StartIPRotationRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
        )


@pytest.mark.asyncio
async def test_start_ip_rotation_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_ip_rotation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.start_ip_rotation(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_start_ip_rotation_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.start_ip_rotation(
            cluster_service.StartIPRotationRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.CompleteIPRotationRequest,
        dict,
    ],
)
def test_complete_ip_rotation(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_ip_rotation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.complete_ip_rotation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.CompleteIPRotationRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_complete_ip_rotation_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.CompleteIPRotationRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_ip_rotation), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.complete_ip_rotation(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.CompleteIPRotationRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )


def test_complete_ip_rotation_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.complete_ip_rotation in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.complete_ip_rotation
        ] = mock_rpc
        request = {}
        client.complete_ip_rotation(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.complete_ip_rotation(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_complete_ip_rotation_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.complete_ip_rotation
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.complete_ip_rotation
        ] = mock_rpc

        request = {}
        await client.complete_ip_rotation(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.complete_ip_rotation(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_complete_ip_rotation_async(
    transport: str = "grpc_asyncio",
    request_type=cluster_service.CompleteIPRotationRequest,
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_ip_rotation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.complete_ip_rotation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.CompleteIPRotationRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_complete_ip_rotation_async_from_dict():
    await test_complete_ip_rotation_async(request_type=dict)


def test_complete_ip_rotation_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.CompleteIPRotationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_ip_rotation), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.complete_ip_rotation(request)

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
async def test_complete_ip_rotation_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.CompleteIPRotationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_ip_rotation), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.complete_ip_rotation(request)

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


def test_complete_ip_rotation_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_ip_rotation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.complete_ip_rotation(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val


def test_complete_ip_rotation_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.complete_ip_rotation(
            cluster_service.CompleteIPRotationRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
        )


@pytest.mark.asyncio
async def test_complete_ip_rotation_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_ip_rotation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.complete_ip_rotation(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_complete_ip_rotation_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.complete_ip_rotation(
            cluster_service.CompleteIPRotationRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.SetNodePoolSizeRequest,
        dict,
    ],
)
def test_set_node_pool_size(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_size), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.set_node_pool_size(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetNodePoolSizeRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_set_node_pool_size_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.SetNodePoolSizeRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        node_pool_id="node_pool_id_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_size), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.set_node_pool_size(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.SetNodePoolSizeRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            name="name_value",
        )


def test_set_node_pool_size_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.set_node_pool_size in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.set_node_pool_size
        ] = mock_rpc
        request = {}
        client.set_node_pool_size(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.set_node_pool_size(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_node_pool_size_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.set_node_pool_size
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.set_node_pool_size
        ] = mock_rpc

        request = {}
        await client.set_node_pool_size(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.set_node_pool_size(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_node_pool_size_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.SetNodePoolSizeRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_size), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.set_node_pool_size(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetNodePoolSizeRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_node_pool_size_async_from_dict():
    await test_set_node_pool_size_async(request_type=dict)


def test_set_node_pool_size_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetNodePoolSizeRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_size), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.set_node_pool_size(request)

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
async def test_set_node_pool_size_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetNodePoolSizeRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_size), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.set_node_pool_size(request)

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


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.SetNetworkPolicyRequest,
        dict,
    ],
)
def test_set_network_policy(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_network_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.set_network_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetNetworkPolicyRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_set_network_policy_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.SetNetworkPolicyRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_network_policy), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.set_network_policy(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.SetNetworkPolicyRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )


def test_set_network_policy_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.set_network_policy in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.set_network_policy
        ] = mock_rpc
        request = {}
        client.set_network_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.set_network_policy(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_network_policy_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.set_network_policy
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.set_network_policy
        ] = mock_rpc

        request = {}
        await client.set_network_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.set_network_policy(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_network_policy_async(
    transport: str = "grpc_asyncio",
    request_type=cluster_service.SetNetworkPolicyRequest,
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_network_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.set_network_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetNetworkPolicyRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_network_policy_async_from_dict():
    await test_set_network_policy_async(request_type=dict)


def test_set_network_policy_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetNetworkPolicyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_network_policy), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.set_network_policy(request)

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
async def test_set_network_policy_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetNetworkPolicyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_network_policy), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.set_network_policy(request)

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


def test_set_network_policy_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_network_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_network_policy(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            network_policy=cluster_service.NetworkPolicy(
                provider=cluster_service.NetworkPolicy.Provider.CALICO
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].network_policy
        mock_val = cluster_service.NetworkPolicy(
            provider=cluster_service.NetworkPolicy.Provider.CALICO
        )
        assert arg == mock_val


def test_set_network_policy_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_network_policy(
            cluster_service.SetNetworkPolicyRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            network_policy=cluster_service.NetworkPolicy(
                provider=cluster_service.NetworkPolicy.Provider.CALICO
            ),
        )


@pytest.mark.asyncio
async def test_set_network_policy_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_network_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_network_policy(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            network_policy=cluster_service.NetworkPolicy(
                provider=cluster_service.NetworkPolicy.Provider.CALICO
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].network_policy
        mock_val = cluster_service.NetworkPolicy(
            provider=cluster_service.NetworkPolicy.Provider.CALICO
        )
        assert arg == mock_val


@pytest.mark.asyncio
async def test_set_network_policy_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_network_policy(
            cluster_service.SetNetworkPolicyRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            network_policy=cluster_service.NetworkPolicy(
                provider=cluster_service.NetworkPolicy.Provider.CALICO
            ),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.SetMaintenancePolicyRequest,
        dict,
    ],
)
def test_set_maintenance_policy(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_maintenance_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )
        response = client.set_maintenance_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetMaintenancePolicyRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


def test_set_maintenance_policy_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.SetMaintenancePolicyRequest(
        project_id="project_id_value",
        zone="zone_value",
        cluster_id="cluster_id_value",
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_maintenance_policy), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.set_maintenance_policy(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.SetMaintenancePolicyRequest(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )


def test_set_maintenance_policy_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.set_maintenance_policy
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.set_maintenance_policy
        ] = mock_rpc
        request = {}
        client.set_maintenance_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.set_maintenance_policy(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_maintenance_policy_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.set_maintenance_policy
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.set_maintenance_policy
        ] = mock_rpc

        request = {}
        await client.set_maintenance_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.set_maintenance_policy(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_set_maintenance_policy_async(
    transport: str = "grpc_asyncio",
    request_type=cluster_service.SetMaintenancePolicyRequest,
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_maintenance_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        response = await client.set_maintenance_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.SetMaintenancePolicyRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == "detail_value"
    assert response.status_message == "status_message_value"
    assert response.self_link == "self_link_value"
    assert response.target_link == "target_link_value"
    assert response.location == "location_value"
    assert response.start_time == "start_time_value"
    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_maintenance_policy_async_from_dict():
    await test_set_maintenance_policy_async(request_type=dict)


def test_set_maintenance_policy_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetMaintenancePolicyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_maintenance_policy), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.set_maintenance_policy(request)

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
async def test_set_maintenance_policy_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetMaintenancePolicyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_maintenance_policy), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        await client.set_maintenance_policy(request)

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


def test_set_maintenance_policy_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_maintenance_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_maintenance_policy(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            maintenance_policy=cluster_service.MaintenancePolicy(
                window=cluster_service.MaintenanceWindow(
                    daily_maintenance_window=cluster_service.DailyMaintenanceWindow(
                        start_time="start_time_value"
                    )
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].maintenance_policy
        mock_val = cluster_service.MaintenancePolicy(
            window=cluster_service.MaintenanceWindow(
                daily_maintenance_window=cluster_service.DailyMaintenanceWindow(
                    start_time="start_time_value"
                )
            )
        )
        assert arg == mock_val


def test_set_maintenance_policy_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_maintenance_policy(
            cluster_service.SetMaintenancePolicyRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            maintenance_policy=cluster_service.MaintenancePolicy(
                window=cluster_service.MaintenanceWindow(
                    daily_maintenance_window=cluster_service.DailyMaintenanceWindow(
                        start_time="start_time_value"
                    )
                )
            ),
        )


@pytest.mark.asyncio
async def test_set_maintenance_policy_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_maintenance_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_maintenance_policy(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            maintenance_policy=cluster_service.MaintenancePolicy(
                window=cluster_service.MaintenanceWindow(
                    daily_maintenance_window=cluster_service.DailyMaintenanceWindow(
                        start_time="start_time_value"
                    )
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = "zone_value"
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val
        arg = args[0].maintenance_policy
        mock_val = cluster_service.MaintenancePolicy(
            window=cluster_service.MaintenanceWindow(
                daily_maintenance_window=cluster_service.DailyMaintenanceWindow(
                    start_time="start_time_value"
                )
            )
        )
        assert arg == mock_val


@pytest.mark.asyncio
async def test_set_maintenance_policy_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_maintenance_policy(
            cluster_service.SetMaintenancePolicyRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            maintenance_policy=cluster_service.MaintenancePolicy(
                window=cluster_service.MaintenanceWindow(
                    daily_maintenance_window=cluster_service.DailyMaintenanceWindow(
                        start_time="start_time_value"
                    )
                )
            ),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.ListUsableSubnetworksRequest,
        dict,
    ],
)
def test_list_usable_subnetworks(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_usable_subnetworks), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListUsableSubnetworksResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_usable_subnetworks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.ListUsableSubnetworksRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListUsableSubnetworksPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_usable_subnetworks_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.ListUsableSubnetworksRequest(
        parent="parent_value",
        filter="filter_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_usable_subnetworks), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_usable_subnetworks(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.ListUsableSubnetworksRequest(
            parent="parent_value",
            filter="filter_value",
            page_token="page_token_value",
        )


def test_list_usable_subnetworks_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_usable_subnetworks
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_usable_subnetworks
        ] = mock_rpc
        request = {}
        client.list_usable_subnetworks(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_usable_subnetworks(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_usable_subnetworks_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_usable_subnetworks
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_usable_subnetworks
        ] = mock_rpc

        request = {}
        await client.list_usable_subnetworks(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_usable_subnetworks(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_usable_subnetworks_async(
    transport: str = "grpc_asyncio",
    request_type=cluster_service.ListUsableSubnetworksRequest,
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_usable_subnetworks), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListUsableSubnetworksResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_usable_subnetworks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.ListUsableSubnetworksRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListUsableSubnetworksAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_usable_subnetworks_async_from_dict():
    await test_list_usable_subnetworks_async(request_type=dict)


def test_list_usable_subnetworks_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListUsableSubnetworksRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_usable_subnetworks), "__call__"
    ) as call:
        call.return_value = cluster_service.ListUsableSubnetworksResponse()
        client.list_usable_subnetworks(request)

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
async def test_list_usable_subnetworks_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListUsableSubnetworksRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_usable_subnetworks), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListUsableSubnetworksResponse()
        )
        await client.list_usable_subnetworks(request)

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


def test_list_usable_subnetworks_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_usable_subnetworks), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListUsableSubnetworksResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_usable_subnetworks(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_usable_subnetworks_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_usable_subnetworks(
            cluster_service.ListUsableSubnetworksRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_usable_subnetworks_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_usable_subnetworks), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListUsableSubnetworksResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListUsableSubnetworksResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_usable_subnetworks(
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
async def test_list_usable_subnetworks_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_usable_subnetworks(
            cluster_service.ListUsableSubnetworksRequest(),
            parent="parent_value",
        )


def test_list_usable_subnetworks_pager(transport_name: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_usable_subnetworks), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                ],
                next_page_token="abc",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[],
                next_page_token="def",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                ],
                next_page_token="ghi",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
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
        pager = client.list_usable_subnetworks(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cluster_service.UsableSubnetwork) for i in results)


def test_list_usable_subnetworks_pages(transport_name: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_usable_subnetworks), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                ],
                next_page_token="abc",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[],
                next_page_token="def",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                ],
                next_page_token="ghi",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_usable_subnetworks(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_usable_subnetworks_async_pager():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_usable_subnetworks),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                ],
                next_page_token="abc",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[],
                next_page_token="def",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                ],
                next_page_token="ghi",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_usable_subnetworks(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cluster_service.UsableSubnetwork) for i in responses)


@pytest.mark.asyncio
async def test_list_usable_subnetworks_async_pages():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_usable_subnetworks),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                ],
                next_page_token="abc",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[],
                next_page_token="def",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                ],
                next_page_token="ghi",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_usable_subnetworks(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.CheckAutopilotCompatibilityRequest,
        dict,
    ],
)
def test_check_autopilot_compatibility(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_autopilot_compatibility), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.CheckAutopilotCompatibilityResponse(
            summary="summary_value",
        )
        response = client.check_autopilot_compatibility(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.CheckAutopilotCompatibilityRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.CheckAutopilotCompatibilityResponse)
    assert response.summary == "summary_value"


def test_check_autopilot_compatibility_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.CheckAutopilotCompatibilityRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_autopilot_compatibility), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.check_autopilot_compatibility(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.CheckAutopilotCompatibilityRequest(
            name="name_value",
        )


def test_check_autopilot_compatibility_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.check_autopilot_compatibility
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.check_autopilot_compatibility
        ] = mock_rpc
        request = {}
        client.check_autopilot_compatibility(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.check_autopilot_compatibility(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_check_autopilot_compatibility_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.check_autopilot_compatibility
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.check_autopilot_compatibility
        ] = mock_rpc

        request = {}
        await client.check_autopilot_compatibility(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.check_autopilot_compatibility(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_check_autopilot_compatibility_async(
    transport: str = "grpc_asyncio",
    request_type=cluster_service.CheckAutopilotCompatibilityRequest,
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_autopilot_compatibility), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.CheckAutopilotCompatibilityResponse(
                summary="summary_value",
            )
        )
        response = await client.check_autopilot_compatibility(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.CheckAutopilotCompatibilityRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.CheckAutopilotCompatibilityResponse)
    assert response.summary == "summary_value"


@pytest.mark.asyncio
async def test_check_autopilot_compatibility_async_from_dict():
    await test_check_autopilot_compatibility_async(request_type=dict)


def test_check_autopilot_compatibility_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.CheckAutopilotCompatibilityRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_autopilot_compatibility), "__call__"
    ) as call:
        call.return_value = cluster_service.CheckAutopilotCompatibilityResponse()
        client.check_autopilot_compatibility(request)

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
async def test_check_autopilot_compatibility_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.CheckAutopilotCompatibilityRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_autopilot_compatibility), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.CheckAutopilotCompatibilityResponse()
        )
        await client.check_autopilot_compatibility(request)

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


@pytest.mark.parametrize(
    "request_type",
    [
        cluster_service.ListLocationsRequest,
        dict,
    ],
)
def test_list_locations(request_type, transport: str = "grpc"):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListLocationsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_locations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cluster_service.ListLocationsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response.raw_page is response
    assert isinstance(response, cluster_service.ListLocationsResponse)
    assert response.next_page_token == "next_page_token_value"


def test_list_locations_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cluster_service.ListLocationsRequest(
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_locations(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cluster_service.ListLocationsRequest(
            parent="parent_value",
        )


def test_list_locations_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_locations in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_locations] = mock_rpc
        request = {}
        client.list_locations(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_locations(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_locations_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ClusterManagerAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_locations
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_locations
        ] = mock_rpc

        request = {}
        await client.list_locations(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_locations(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_locations_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.ListLocationsRequest
):
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListLocationsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_locations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cluster_service.ListLocationsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.ListLocationsResponse)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_locations_async_from_dict():
    await test_list_locations_async(request_type=dict)


def test_list_locations_field_headers():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListLocationsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value = cluster_service.ListLocationsResponse()
        client.list_locations(request)

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
async def test_list_locations_field_headers_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListLocationsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListLocationsResponse()
        )
        await client.list_locations(request)

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


def test_list_locations_flattened():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListLocationsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_locations(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_locations_flattened_error():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_locations(
            cluster_service.ListLocationsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_locations_flattened_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListLocationsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListLocationsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_locations(
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
async def test_list_locations_flattened_error_async():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_locations(
            cluster_service.ListLocationsRequest(),
            parent="parent_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ClusterManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.ClusterManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ClusterManagerClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.ClusterManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = ClusterManagerClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = ClusterManagerClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.ClusterManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ClusterManagerClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ClusterManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = ClusterManagerClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ClusterManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.ClusterManagerGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ClusterManagerGrpcTransport,
        transports.ClusterManagerGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_kind_grpc():
    transport = ClusterManagerClient.get_transport_class("grpc")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "grpc"


def test_initialize_client_w_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_clusters_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        call.return_value = cluster_service.ListClustersResponse()
        client.list_clusters(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.ListClustersRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_cluster_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        call.return_value = cluster_service.Cluster()
        client.get_cluster(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.GetClusterRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_cluster_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.create_cluster(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.CreateClusterRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_cluster_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.update_cluster(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.UpdateClusterRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_node_pool_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.update_node_pool), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.update_node_pool(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.UpdateNodePoolRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_set_node_pool_autoscaling_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_autoscaling), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.set_node_pool_autoscaling(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetNodePoolAutoscalingRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_set_logging_service_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.set_logging_service), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.set_logging_service(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetLoggingServiceRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_set_monitoring_service_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.set_monitoring_service), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.set_monitoring_service(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetMonitoringServiceRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_set_addons_config_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.set_addons_config), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.set_addons_config(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetAddonsConfigRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_set_locations_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.set_locations), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.set_locations(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetLocationsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_master_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.update_master), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.update_master(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.UpdateMasterRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_set_master_auth_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.set_master_auth), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.set_master_auth(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetMasterAuthRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_cluster_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.delete_cluster(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.DeleteClusterRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_operations_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = cluster_service.ListOperationsResponse()
        client.list_operations(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.ListOperationsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_operation_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.get_operation(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.GetOperationRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_cancel_operation_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = None
        client.cancel_operation(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.CancelOperationRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_server_config_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        call.return_value = cluster_service.ServerConfig()
        client.get_server_config(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.GetServerConfigRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_json_web_keys_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_json_web_keys), "__call__"
    ) as call:
        call.return_value = cluster_service.GetJSONWebKeysResponse()
        client.get_json_web_keys(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.GetJSONWebKeysRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_node_pools_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        call.return_value = cluster_service.ListNodePoolsResponse()
        client.list_node_pools(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.ListNodePoolsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_node_pool_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        call.return_value = cluster_service.NodePool()
        client.get_node_pool(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.GetNodePoolRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_node_pool_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.create_node_pool(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.CreateNodePoolRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_node_pool_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.delete_node_pool(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.DeleteNodePoolRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_complete_node_pool_upgrade_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_node_pool_upgrade), "__call__"
    ) as call:
        call.return_value = None
        client.complete_node_pool_upgrade(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.CompleteNodePoolUpgradeRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_rollback_node_pool_upgrade_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_node_pool_upgrade), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.rollback_node_pool_upgrade(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.RollbackNodePoolUpgradeRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_set_node_pool_management_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_management), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.set_node_pool_management(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetNodePoolManagementRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_set_labels_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.set_labels), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.set_labels(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetLabelsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_set_legacy_abac_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.set_legacy_abac), "__call__") as call:
        call.return_value = cluster_service.Operation()
        client.set_legacy_abac(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetLegacyAbacRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_start_ip_rotation_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.start_ip_rotation), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.start_ip_rotation(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.StartIPRotationRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_complete_ip_rotation_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_ip_rotation), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.complete_ip_rotation(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.CompleteIPRotationRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_set_node_pool_size_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_size), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.set_node_pool_size(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetNodePoolSizeRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_set_network_policy_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.set_network_policy), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.set_network_policy(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetNetworkPolicyRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_set_maintenance_policy_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.set_maintenance_policy), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()
        client.set_maintenance_policy(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetMaintenancePolicyRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_usable_subnetworks_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_usable_subnetworks), "__call__"
    ) as call:
        call.return_value = cluster_service.ListUsableSubnetworksResponse()
        client.list_usable_subnetworks(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.ListUsableSubnetworksRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_check_autopilot_compatibility_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.check_autopilot_compatibility), "__call__"
    ) as call:
        call.return_value = cluster_service.CheckAutopilotCompatibilityResponse()
        client.check_autopilot_compatibility(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.CheckAutopilotCompatibilityRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_locations_empty_call_grpc():
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value = cluster_service.ListLocationsResponse()
        client.list_locations(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.ListLocationsRequest()

        assert args[0] == request_msg


def test_transport_kind_grpc_asyncio():
    transport = ClusterManagerAsyncClient.get_transport_class("grpc_asyncio")(
        credentials=async_anonymous_credentials()
    )
    assert transport.kind == "grpc_asyncio"


def test_initialize_client_w_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_clusters_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListClustersResponse(
                missing_zones=["missing_zones_value"],
            )
        )
        await client.list_clusters(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.ListClustersRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_cluster_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Cluster(
                name="name_value",
                description="description_value",
                initial_node_count=1911,
                logging_service="logging_service_value",
                monitoring_service="monitoring_service_value",
                network="network_value",
                cluster_ipv4_cidr="cluster_ipv4_cidr_value",
                subnetwork="subnetwork_value",
                locations=["locations_value"],
                enable_kubernetes_alpha=True,
                label_fingerprint="label_fingerprint_value",
                private_cluster=True,
                master_ipv4_cidr_block="master_ipv4_cidr_block_value",
                self_link="self_link_value",
                zone="zone_value",
                endpoint="endpoint_value",
                initial_cluster_version="initial_cluster_version_value",
                current_master_version="current_master_version_value",
                current_node_version="current_node_version_value",
                create_time="create_time_value",
                status=cluster_service.Cluster.Status.PROVISIONING,
                status_message="status_message_value",
                node_ipv4_cidr_size=1955,
                services_ipv4_cidr="services_ipv4_cidr_value",
                instance_group_urls=["instance_group_urls_value"],
                current_node_count=1936,
                expire_time="expire_time_value",
                location="location_value",
                enable_tpu=True,
                tpu_ipv4_cidr_block="tpu_ipv4_cidr_block_value",
                id="id_value",
                etag="etag_value",
                satisfies_pzs=True,
                satisfies_pzi=True,
            )
        )
        await client.get_cluster(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.GetClusterRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_cluster_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.create_cluster(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.CreateClusterRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_update_cluster_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.update_cluster(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.UpdateClusterRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_update_node_pool_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.update_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.update_node_pool(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.UpdateNodePoolRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_set_node_pool_autoscaling_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_autoscaling), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.set_node_pool_autoscaling(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetNodePoolAutoscalingRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_set_logging_service_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.set_logging_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.set_logging_service(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetLoggingServiceRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_set_monitoring_service_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.set_monitoring_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.set_monitoring_service(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetMonitoringServiceRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_set_addons_config_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.set_addons_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.set_addons_config(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetAddonsConfigRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_set_locations_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.set_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.set_locations(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetLocationsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_update_master_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.update_master), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.update_master(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.UpdateMasterRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_set_master_auth_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.set_master_auth), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.set_master_auth(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetMasterAuthRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_delete_cluster_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.delete_cluster(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.DeleteClusterRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_operations_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListOperationsResponse(
                missing_zones=["missing_zones_value"],
            )
        )
        await client.list_operations(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.ListOperationsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_operation_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.get_operation(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.GetOperationRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_cancel_operation_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.cancel_operation(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.CancelOperationRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_server_config_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ServerConfig(
                default_cluster_version="default_cluster_version_value",
                valid_node_versions=["valid_node_versions_value"],
                default_image_type="default_image_type_value",
                valid_image_types=["valid_image_types_value"],
                valid_master_versions=["valid_master_versions_value"],
            )
        )
        await client.get_server_config(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.GetServerConfigRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_json_web_keys_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_json_web_keys), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.GetJSONWebKeysResponse()
        )
        await client.get_json_web_keys(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.GetJSONWebKeysRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_node_pools_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListNodePoolsResponse()
        )
        await client.list_node_pools(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.ListNodePoolsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_node_pool_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.NodePool(
                name="name_value",
                initial_node_count=1911,
                locations=["locations_value"],
                self_link="self_link_value",
                version="version_value",
                instance_group_urls=["instance_group_urls_value"],
                status=cluster_service.NodePool.Status.PROVISIONING,
                status_message="status_message_value",
                pod_ipv4_cidr_size=1856,
                etag="etag_value",
            )
        )
        await client.get_node_pool(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.GetNodePoolRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_node_pool_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.create_node_pool(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.CreateNodePoolRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_delete_node_pool_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.delete_node_pool(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.DeleteNodePoolRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_complete_node_pool_upgrade_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_node_pool_upgrade), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.complete_node_pool_upgrade(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.CompleteNodePoolUpgradeRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_rollback_node_pool_upgrade_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_node_pool_upgrade), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.rollback_node_pool_upgrade(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.RollbackNodePoolUpgradeRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_set_node_pool_management_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_management), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.set_node_pool_management(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetNodePoolManagementRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_set_labels_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.set_labels), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.set_labels(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetLabelsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_set_legacy_abac_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.set_legacy_abac), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.set_legacy_abac(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetLegacyAbacRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_start_ip_rotation_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.start_ip_rotation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.start_ip_rotation(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.StartIPRotationRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_complete_ip_rotation_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_ip_rotation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.complete_ip_rotation(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.CompleteIPRotationRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_set_node_pool_size_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_size), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.set_node_pool_size(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetNodePoolSizeRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_set_network_policy_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.set_network_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.set_network_policy(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetNetworkPolicyRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_set_maintenance_policy_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.set_maintenance_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )
        await client.set_maintenance_policy(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.SetMaintenancePolicyRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_usable_subnetworks_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_usable_subnetworks), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListUsableSubnetworksResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_usable_subnetworks(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.ListUsableSubnetworksRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_check_autopilot_compatibility_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.check_autopilot_compatibility), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.CheckAutopilotCompatibilityResponse(
                summary="summary_value",
            )
        )
        await client.check_autopilot_compatibility(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.CheckAutopilotCompatibilityRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_locations_empty_call_grpc_asyncio():
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListLocationsResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_locations(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = cluster_service.ListLocationsRequest()

        assert args[0] == request_msg


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.ClusterManagerGrpcTransport,
    )


def test_cluster_manager_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.ClusterManagerTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_cluster_manager_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.container_v1beta1.services.cluster_manager.transports.ClusterManagerTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.ClusterManagerTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_clusters",
        "get_cluster",
        "create_cluster",
        "update_cluster",
        "update_node_pool",
        "set_node_pool_autoscaling",
        "set_logging_service",
        "set_monitoring_service",
        "set_addons_config",
        "set_locations",
        "update_master",
        "set_master_auth",
        "delete_cluster",
        "list_operations",
        "get_operation",
        "cancel_operation",
        "get_server_config",
        "get_json_web_keys",
        "list_node_pools",
        "get_node_pool",
        "create_node_pool",
        "delete_node_pool",
        "complete_node_pool_upgrade",
        "rollback_node_pool_upgrade",
        "set_node_pool_management",
        "set_labels",
        "set_legacy_abac",
        "start_ip_rotation",
        "complete_ip_rotation",
        "set_node_pool_size",
        "set_network_policy",
        "set_maintenance_policy",
        "list_usable_subnetworks",
        "check_autopilot_compatibility",
        "list_locations",
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


def test_cluster_manager_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.container_v1beta1.services.cluster_manager.transports.ClusterManagerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ClusterManagerTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_cluster_manager_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.container_v1beta1.services.cluster_manager.transports.ClusterManagerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ClusterManagerTransport()
        adc.assert_called_once()


def test_cluster_manager_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        ClusterManagerClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ClusterManagerGrpcTransport,
        transports.ClusterManagerGrpcAsyncIOTransport,
    ],
)
def test_cluster_manager_transport_auth_adc(transport_class):
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
        transports.ClusterManagerGrpcTransport,
        transports.ClusterManagerGrpcAsyncIOTransport,
    ],
)
def test_cluster_manager_transport_auth_gdch_credentials(transport_class):
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
        (transports.ClusterManagerGrpcTransport, grpc_helpers),
        (transports.ClusterManagerGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_cluster_manager_transport_create_channel(transport_class, grpc_helpers):
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
            "container.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="container.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ClusterManagerGrpcTransport,
        transports.ClusterManagerGrpcAsyncIOTransport,
    ],
)
def test_cluster_manager_grpc_transport_client_cert_source_for_mtls(transport_class):
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


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_cluster_manager_host_no_port(transport_name):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="container.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("container.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_cluster_manager_host_with_port(transport_name):
    client = ClusterManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="container.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("container.googleapis.com:8000")


def test_cluster_manager_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ClusterManagerGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_cluster_manager_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ClusterManagerGrpcAsyncIOTransport(
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
        transports.ClusterManagerGrpcTransport,
        transports.ClusterManagerGrpcAsyncIOTransport,
    ],
)
def test_cluster_manager_transport_channel_mtls_with_client_cert_source(
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
        transports.ClusterManagerGrpcTransport,
        transports.ClusterManagerGrpcAsyncIOTransport,
    ],
)
def test_cluster_manager_transport_channel_mtls_with_adc(transport_class):
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


def test_topic_path():
    project = "squid"
    topic = "clam"
    expected = "projects/{project}/topics/{topic}".format(
        project=project,
        topic=topic,
    )
    actual = ClusterManagerClient.topic_path(project, topic)
    assert expected == actual


def test_parse_topic_path():
    expected = {
        "project": "whelk",
        "topic": "octopus",
    }
    path = ClusterManagerClient.topic_path(**expected)

    # Check that the path construction is reversible.
    actual = ClusterManagerClient.parse_topic_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "oyster"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = ClusterManagerClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = ClusterManagerClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = ClusterManagerClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "cuttlefish"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = ClusterManagerClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = ClusterManagerClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = ClusterManagerClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "winkle"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = ClusterManagerClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = ClusterManagerClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = ClusterManagerClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "scallop"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = ClusterManagerClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = ClusterManagerClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = ClusterManagerClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = ClusterManagerClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = ClusterManagerClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = ClusterManagerClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.ClusterManagerTransport, "_prep_wrapped_messages"
    ) as prep:
        client = ClusterManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.ClusterManagerTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = ClusterManagerClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_transport_close_grpc():
    client = ClusterManagerClient(
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
    client = ClusterManagerAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_client_ctx():
    transports = [
        "grpc",
    ]
    for transport in transports:
        client = ClusterManagerClient(
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
        (ClusterManagerClient, transports.ClusterManagerGrpcTransport),
        (ClusterManagerAsyncClient, transports.ClusterManagerGrpcAsyncIOTransport),
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
