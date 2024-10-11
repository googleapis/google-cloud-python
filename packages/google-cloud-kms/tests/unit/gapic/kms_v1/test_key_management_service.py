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
from google.cloud.location import locations_pb2
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import options_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore

from google.cloud.kms_v1.services.key_management_service import (
    KeyManagementServiceAsyncClient,
    KeyManagementServiceClient,
    pagers,
    transports,
)
from google.cloud.kms_v1.types import resources, service


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

    assert KeyManagementServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        KeyManagementServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        KeyManagementServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        KeyManagementServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        KeyManagementServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        KeyManagementServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


def test__read_environment_variables():
    assert KeyManagementServiceClient._read_environment_variables() == (
        False,
        "auto",
        None,
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert KeyManagementServiceClient._read_environment_variables() == (
            True,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert KeyManagementServiceClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            KeyManagementServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert KeyManagementServiceClient._read_environment_variables() == (
            False,
            "never",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert KeyManagementServiceClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert KeyManagementServiceClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            KeyManagementServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert KeyManagementServiceClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert KeyManagementServiceClient._get_client_cert_source(None, False) is None
    assert (
        KeyManagementServiceClient._get_client_cert_source(
            mock_provided_cert_source, False
        )
        is None
    )
    assert (
        KeyManagementServiceClient._get_client_cert_source(
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
                KeyManagementServiceClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                KeyManagementServiceClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    KeyManagementServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(KeyManagementServiceClient),
)
@mock.patch.object(
    KeyManagementServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(KeyManagementServiceAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = KeyManagementServiceClient._DEFAULT_UNIVERSE
    default_endpoint = KeyManagementServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = KeyManagementServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        KeyManagementServiceClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        KeyManagementServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == KeyManagementServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        KeyManagementServiceClient._get_api_endpoint(
            None, None, default_universe, "auto"
        )
        == default_endpoint
    )
    assert (
        KeyManagementServiceClient._get_api_endpoint(
            None, None, default_universe, "always"
        )
        == KeyManagementServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        KeyManagementServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == KeyManagementServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        KeyManagementServiceClient._get_api_endpoint(None, None, mock_universe, "never")
        == mock_endpoint
    )
    assert (
        KeyManagementServiceClient._get_api_endpoint(
            None, None, default_universe, "never"
        )
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        KeyManagementServiceClient._get_api_endpoint(
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
        KeyManagementServiceClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        KeyManagementServiceClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        KeyManagementServiceClient._get_universe_domain(None, None)
        == KeyManagementServiceClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        KeyManagementServiceClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            KeyManagementServiceClient,
            transports.KeyManagementServiceGrpcTransport,
            "grpc",
        ),
        (
            KeyManagementServiceClient,
            transports.KeyManagementServiceRestTransport,
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
        (KeyManagementServiceClient, "grpc"),
        (KeyManagementServiceAsyncClient, "grpc_asyncio"),
        (KeyManagementServiceClient, "rest"),
    ],
)
def test_key_management_service_client_from_service_account_info(
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
            "cloudkms.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://cloudkms.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.KeyManagementServiceGrpcTransport, "grpc"),
        (transports.KeyManagementServiceGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.KeyManagementServiceRestTransport, "rest"),
    ],
)
def test_key_management_service_client_service_account_always_use_jwt(
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
        (KeyManagementServiceClient, "grpc"),
        (KeyManagementServiceAsyncClient, "grpc_asyncio"),
        (KeyManagementServiceClient, "rest"),
    ],
)
def test_key_management_service_client_from_service_account_file(
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
            "cloudkms.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://cloudkms.googleapis.com"
        )


def test_key_management_service_client_get_transport_class():
    transport = KeyManagementServiceClient.get_transport_class()
    available_transports = [
        transports.KeyManagementServiceGrpcTransport,
        transports.KeyManagementServiceRestTransport,
    ]
    assert transport in available_transports

    transport = KeyManagementServiceClient.get_transport_class("grpc")
    assert transport == transports.KeyManagementServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            KeyManagementServiceClient,
            transports.KeyManagementServiceGrpcTransport,
            "grpc",
        ),
        (
            KeyManagementServiceAsyncClient,
            transports.KeyManagementServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            KeyManagementServiceClient,
            transports.KeyManagementServiceRestTransport,
            "rest",
        ),
    ],
)
@mock.patch.object(
    KeyManagementServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(KeyManagementServiceClient),
)
@mock.patch.object(
    KeyManagementServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(KeyManagementServiceAsyncClient),
)
def test_key_management_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(KeyManagementServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(KeyManagementServiceClient, "get_transport_class") as gtc:
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
            KeyManagementServiceClient,
            transports.KeyManagementServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            KeyManagementServiceAsyncClient,
            transports.KeyManagementServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            KeyManagementServiceClient,
            transports.KeyManagementServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            KeyManagementServiceAsyncClient,
            transports.KeyManagementServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            KeyManagementServiceClient,
            transports.KeyManagementServiceRestTransport,
            "rest",
            "true",
        ),
        (
            KeyManagementServiceClient,
            transports.KeyManagementServiceRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    KeyManagementServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(KeyManagementServiceClient),
)
@mock.patch.object(
    KeyManagementServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(KeyManagementServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_key_management_service_client_mtls_env_auto(
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
    "client_class", [KeyManagementServiceClient, KeyManagementServiceAsyncClient]
)
@mock.patch.object(
    KeyManagementServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(KeyManagementServiceClient),
)
@mock.patch.object(
    KeyManagementServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(KeyManagementServiceAsyncClient),
)
def test_key_management_service_client_get_mtls_endpoint_and_cert_source(client_class):
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
    "client_class", [KeyManagementServiceClient, KeyManagementServiceAsyncClient]
)
@mock.patch.object(
    KeyManagementServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(KeyManagementServiceClient),
)
@mock.patch.object(
    KeyManagementServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(KeyManagementServiceAsyncClient),
)
def test_key_management_service_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = KeyManagementServiceClient._DEFAULT_UNIVERSE
    default_endpoint = KeyManagementServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = KeyManagementServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        (
            KeyManagementServiceClient,
            transports.KeyManagementServiceGrpcTransport,
            "grpc",
        ),
        (
            KeyManagementServiceAsyncClient,
            transports.KeyManagementServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            KeyManagementServiceClient,
            transports.KeyManagementServiceRestTransport,
            "rest",
        ),
    ],
)
def test_key_management_service_client_client_options_scopes(
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
            KeyManagementServiceClient,
            transports.KeyManagementServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            KeyManagementServiceAsyncClient,
            transports.KeyManagementServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (
            KeyManagementServiceClient,
            transports.KeyManagementServiceRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_key_management_service_client_client_options_credentials_file(
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


def test_key_management_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.kms_v1.services.key_management_service.transports.KeyManagementServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = KeyManagementServiceClient(
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
            KeyManagementServiceClient,
            transports.KeyManagementServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            KeyManagementServiceAsyncClient,
            transports.KeyManagementServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_key_management_service_client_create_channel_credentials_file(
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
            "cloudkms.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloudkms",
            ),
            scopes=None,
            default_host="cloudkms.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListKeyRingsRequest,
        dict,
    ],
)
def test_list_key_rings(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_key_rings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListKeyRingsResponse(
            next_page_token="next_page_token_value",
            total_size=1086,
        )
        response = client.list_key_rings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.ListKeyRingsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListKeyRingsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


def test_list_key_rings_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.ListKeyRingsRequest(
        parent="parent_value",
        page_token="page_token_value",
        filter="filter_value",
        order_by="order_by_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_key_rings), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_key_rings(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListKeyRingsRequest(
            parent="parent_value",
            page_token="page_token_value",
            filter="filter_value",
            order_by="order_by_value",
        )


def test_list_key_rings_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_key_rings in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_key_rings] = mock_rpc
        request = {}
        client.list_key_rings(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_key_rings(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_key_rings_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_key_rings
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_key_rings
        ] = mock_rpc

        request = {}
        await client.list_key_rings(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_key_rings(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_key_rings_async(
    transport: str = "grpc_asyncio", request_type=service.ListKeyRingsRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_key_rings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListKeyRingsResponse(
                next_page_token="next_page_token_value",
                total_size=1086,
            )
        )
        response = await client.list_key_rings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.ListKeyRingsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListKeyRingsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


@pytest.mark.asyncio
async def test_list_key_rings_async_from_dict():
    await test_list_key_rings_async(request_type=dict)


def test_list_key_rings_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListKeyRingsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_key_rings), "__call__") as call:
        call.return_value = service.ListKeyRingsResponse()
        client.list_key_rings(request)

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
async def test_list_key_rings_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListKeyRingsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_key_rings), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListKeyRingsResponse()
        )
        await client.list_key_rings(request)

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


def test_list_key_rings_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_key_rings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListKeyRingsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_key_rings(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_key_rings_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_key_rings(
            service.ListKeyRingsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_key_rings_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_key_rings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListKeyRingsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListKeyRingsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_key_rings(
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
async def test_list_key_rings_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_key_rings(
            service.ListKeyRingsRequest(),
            parent="parent_value",
        )


def test_list_key_rings_pager(transport_name: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_key_rings), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListKeyRingsResponse(
                key_rings=[
                    resources.KeyRing(),
                    resources.KeyRing(),
                    resources.KeyRing(),
                ],
                next_page_token="abc",
            ),
            service.ListKeyRingsResponse(
                key_rings=[],
                next_page_token="def",
            ),
            service.ListKeyRingsResponse(
                key_rings=[
                    resources.KeyRing(),
                ],
                next_page_token="ghi",
            ),
            service.ListKeyRingsResponse(
                key_rings=[
                    resources.KeyRing(),
                    resources.KeyRing(),
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
        pager = client.list_key_rings(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.KeyRing) for i in results)


def test_list_key_rings_pages(transport_name: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_key_rings), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListKeyRingsResponse(
                key_rings=[
                    resources.KeyRing(),
                    resources.KeyRing(),
                    resources.KeyRing(),
                ],
                next_page_token="abc",
            ),
            service.ListKeyRingsResponse(
                key_rings=[],
                next_page_token="def",
            ),
            service.ListKeyRingsResponse(
                key_rings=[
                    resources.KeyRing(),
                ],
                next_page_token="ghi",
            ),
            service.ListKeyRingsResponse(
                key_rings=[
                    resources.KeyRing(),
                    resources.KeyRing(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_key_rings(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_key_rings_async_pager():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_key_rings), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListKeyRingsResponse(
                key_rings=[
                    resources.KeyRing(),
                    resources.KeyRing(),
                    resources.KeyRing(),
                ],
                next_page_token="abc",
            ),
            service.ListKeyRingsResponse(
                key_rings=[],
                next_page_token="def",
            ),
            service.ListKeyRingsResponse(
                key_rings=[
                    resources.KeyRing(),
                ],
                next_page_token="ghi",
            ),
            service.ListKeyRingsResponse(
                key_rings=[
                    resources.KeyRing(),
                    resources.KeyRing(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_key_rings(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.KeyRing) for i in responses)


@pytest.mark.asyncio
async def test_list_key_rings_async_pages():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_key_rings), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListKeyRingsResponse(
                key_rings=[
                    resources.KeyRing(),
                    resources.KeyRing(),
                    resources.KeyRing(),
                ],
                next_page_token="abc",
            ),
            service.ListKeyRingsResponse(
                key_rings=[],
                next_page_token="def",
            ),
            service.ListKeyRingsResponse(
                key_rings=[
                    resources.KeyRing(),
                ],
                next_page_token="ghi",
            ),
            service.ListKeyRingsResponse(
                key_rings=[
                    resources.KeyRing(),
                    resources.KeyRing(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_key_rings(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListCryptoKeysRequest,
        dict,
    ],
)
def test_list_crypto_keys(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_crypto_keys), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCryptoKeysResponse(
            next_page_token="next_page_token_value",
            total_size=1086,
        )
        response = client.list_crypto_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.ListCryptoKeysRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCryptoKeysPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


def test_list_crypto_keys_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.ListCryptoKeysRequest(
        parent="parent_value",
        page_token="page_token_value",
        filter="filter_value",
        order_by="order_by_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_crypto_keys), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_crypto_keys(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListCryptoKeysRequest(
            parent="parent_value",
            page_token="page_token_value",
            filter="filter_value",
            order_by="order_by_value",
        )


def test_list_crypto_keys_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_crypto_keys in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_crypto_keys
        ] = mock_rpc
        request = {}
        client.list_crypto_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_crypto_keys(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_crypto_keys_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_crypto_keys
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_crypto_keys
        ] = mock_rpc

        request = {}
        await client.list_crypto_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_crypto_keys(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_crypto_keys_async(
    transport: str = "grpc_asyncio", request_type=service.ListCryptoKeysRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_crypto_keys), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCryptoKeysResponse(
                next_page_token="next_page_token_value",
                total_size=1086,
            )
        )
        response = await client.list_crypto_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.ListCryptoKeysRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCryptoKeysAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


@pytest.mark.asyncio
async def test_list_crypto_keys_async_from_dict():
    await test_list_crypto_keys_async(request_type=dict)


def test_list_crypto_keys_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListCryptoKeysRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_crypto_keys), "__call__") as call:
        call.return_value = service.ListCryptoKeysResponse()
        client.list_crypto_keys(request)

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
async def test_list_crypto_keys_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListCryptoKeysRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_crypto_keys), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCryptoKeysResponse()
        )
        await client.list_crypto_keys(request)

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


def test_list_crypto_keys_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_crypto_keys), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCryptoKeysResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_crypto_keys(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_crypto_keys_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_crypto_keys(
            service.ListCryptoKeysRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_crypto_keys_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_crypto_keys), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCryptoKeysResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCryptoKeysResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_crypto_keys(
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
async def test_list_crypto_keys_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_crypto_keys(
            service.ListCryptoKeysRequest(),
            parent="parent_value",
        )


def test_list_crypto_keys_pager(transport_name: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_crypto_keys), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCryptoKeysResponse(
                crypto_keys=[
                    resources.CryptoKey(),
                    resources.CryptoKey(),
                    resources.CryptoKey(),
                ],
                next_page_token="abc",
            ),
            service.ListCryptoKeysResponse(
                crypto_keys=[],
                next_page_token="def",
            ),
            service.ListCryptoKeysResponse(
                crypto_keys=[
                    resources.CryptoKey(),
                ],
                next_page_token="ghi",
            ),
            service.ListCryptoKeysResponse(
                crypto_keys=[
                    resources.CryptoKey(),
                    resources.CryptoKey(),
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
        pager = client.list_crypto_keys(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.CryptoKey) for i in results)


def test_list_crypto_keys_pages(transport_name: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_crypto_keys), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCryptoKeysResponse(
                crypto_keys=[
                    resources.CryptoKey(),
                    resources.CryptoKey(),
                    resources.CryptoKey(),
                ],
                next_page_token="abc",
            ),
            service.ListCryptoKeysResponse(
                crypto_keys=[],
                next_page_token="def",
            ),
            service.ListCryptoKeysResponse(
                crypto_keys=[
                    resources.CryptoKey(),
                ],
                next_page_token="ghi",
            ),
            service.ListCryptoKeysResponse(
                crypto_keys=[
                    resources.CryptoKey(),
                    resources.CryptoKey(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_crypto_keys(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_crypto_keys_async_pager():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crypto_keys), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCryptoKeysResponse(
                crypto_keys=[
                    resources.CryptoKey(),
                    resources.CryptoKey(),
                    resources.CryptoKey(),
                ],
                next_page_token="abc",
            ),
            service.ListCryptoKeysResponse(
                crypto_keys=[],
                next_page_token="def",
            ),
            service.ListCryptoKeysResponse(
                crypto_keys=[
                    resources.CryptoKey(),
                ],
                next_page_token="ghi",
            ),
            service.ListCryptoKeysResponse(
                crypto_keys=[
                    resources.CryptoKey(),
                    resources.CryptoKey(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_crypto_keys(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.CryptoKey) for i in responses)


@pytest.mark.asyncio
async def test_list_crypto_keys_async_pages():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crypto_keys), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCryptoKeysResponse(
                crypto_keys=[
                    resources.CryptoKey(),
                    resources.CryptoKey(),
                    resources.CryptoKey(),
                ],
                next_page_token="abc",
            ),
            service.ListCryptoKeysResponse(
                crypto_keys=[],
                next_page_token="def",
            ),
            service.ListCryptoKeysResponse(
                crypto_keys=[
                    resources.CryptoKey(),
                ],
                next_page_token="ghi",
            ),
            service.ListCryptoKeysResponse(
                crypto_keys=[
                    resources.CryptoKey(),
                    resources.CryptoKey(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_crypto_keys(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListCryptoKeyVersionsRequest,
        dict,
    ],
)
def test_list_crypto_key_versions(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crypto_key_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCryptoKeyVersionsResponse(
            next_page_token="next_page_token_value",
            total_size=1086,
        )
        response = client.list_crypto_key_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.ListCryptoKeyVersionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCryptoKeyVersionsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


def test_list_crypto_key_versions_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.ListCryptoKeyVersionsRequest(
        parent="parent_value",
        page_token="page_token_value",
        filter="filter_value",
        order_by="order_by_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crypto_key_versions), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_crypto_key_versions(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListCryptoKeyVersionsRequest(
            parent="parent_value",
            page_token="page_token_value",
            filter="filter_value",
            order_by="order_by_value",
        )


def test_list_crypto_key_versions_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_crypto_key_versions
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_crypto_key_versions
        ] = mock_rpc
        request = {}
        client.list_crypto_key_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_crypto_key_versions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_crypto_key_versions_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_crypto_key_versions
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_crypto_key_versions
        ] = mock_rpc

        request = {}
        await client.list_crypto_key_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_crypto_key_versions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_crypto_key_versions_async(
    transport: str = "grpc_asyncio", request_type=service.ListCryptoKeyVersionsRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crypto_key_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCryptoKeyVersionsResponse(
                next_page_token="next_page_token_value",
                total_size=1086,
            )
        )
        response = await client.list_crypto_key_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.ListCryptoKeyVersionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCryptoKeyVersionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


@pytest.mark.asyncio
async def test_list_crypto_key_versions_async_from_dict():
    await test_list_crypto_key_versions_async(request_type=dict)


def test_list_crypto_key_versions_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListCryptoKeyVersionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crypto_key_versions), "__call__"
    ) as call:
        call.return_value = service.ListCryptoKeyVersionsResponse()
        client.list_crypto_key_versions(request)

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
async def test_list_crypto_key_versions_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListCryptoKeyVersionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crypto_key_versions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCryptoKeyVersionsResponse()
        )
        await client.list_crypto_key_versions(request)

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


def test_list_crypto_key_versions_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crypto_key_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCryptoKeyVersionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_crypto_key_versions(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_crypto_key_versions_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_crypto_key_versions(
            service.ListCryptoKeyVersionsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_crypto_key_versions_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crypto_key_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCryptoKeyVersionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCryptoKeyVersionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_crypto_key_versions(
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
async def test_list_crypto_key_versions_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_crypto_key_versions(
            service.ListCryptoKeyVersionsRequest(),
            parent="parent_value",
        )


def test_list_crypto_key_versions_pager(transport_name: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crypto_key_versions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[
                    resources.CryptoKeyVersion(),
                    resources.CryptoKeyVersion(),
                    resources.CryptoKeyVersion(),
                ],
                next_page_token="abc",
            ),
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[],
                next_page_token="def",
            ),
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[
                    resources.CryptoKeyVersion(),
                ],
                next_page_token="ghi",
            ),
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[
                    resources.CryptoKeyVersion(),
                    resources.CryptoKeyVersion(),
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
        pager = client.list_crypto_key_versions(
            request={}, retry=retry, timeout=timeout
        )

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.CryptoKeyVersion) for i in results)


def test_list_crypto_key_versions_pages(transport_name: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crypto_key_versions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[
                    resources.CryptoKeyVersion(),
                    resources.CryptoKeyVersion(),
                    resources.CryptoKeyVersion(),
                ],
                next_page_token="abc",
            ),
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[],
                next_page_token="def",
            ),
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[
                    resources.CryptoKeyVersion(),
                ],
                next_page_token="ghi",
            ),
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[
                    resources.CryptoKeyVersion(),
                    resources.CryptoKeyVersion(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_crypto_key_versions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_crypto_key_versions_async_pager():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crypto_key_versions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[
                    resources.CryptoKeyVersion(),
                    resources.CryptoKeyVersion(),
                    resources.CryptoKeyVersion(),
                ],
                next_page_token="abc",
            ),
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[],
                next_page_token="def",
            ),
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[
                    resources.CryptoKeyVersion(),
                ],
                next_page_token="ghi",
            ),
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[
                    resources.CryptoKeyVersion(),
                    resources.CryptoKeyVersion(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_crypto_key_versions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.CryptoKeyVersion) for i in responses)


@pytest.mark.asyncio
async def test_list_crypto_key_versions_async_pages():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crypto_key_versions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[
                    resources.CryptoKeyVersion(),
                    resources.CryptoKeyVersion(),
                    resources.CryptoKeyVersion(),
                ],
                next_page_token="abc",
            ),
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[],
                next_page_token="def",
            ),
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[
                    resources.CryptoKeyVersion(),
                ],
                next_page_token="ghi",
            ),
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[
                    resources.CryptoKeyVersion(),
                    resources.CryptoKeyVersion(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_crypto_key_versions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListImportJobsRequest,
        dict,
    ],
)
def test_list_import_jobs(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_import_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListImportJobsResponse(
            next_page_token="next_page_token_value",
            total_size=1086,
        )
        response = client.list_import_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.ListImportJobsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListImportJobsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


def test_list_import_jobs_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.ListImportJobsRequest(
        parent="parent_value",
        page_token="page_token_value",
        filter="filter_value",
        order_by="order_by_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_import_jobs), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_import_jobs(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListImportJobsRequest(
            parent="parent_value",
            page_token="page_token_value",
            filter="filter_value",
            order_by="order_by_value",
        )


def test_list_import_jobs_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_import_jobs in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_import_jobs
        ] = mock_rpc
        request = {}
        client.list_import_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_import_jobs(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_import_jobs_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_import_jobs
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_import_jobs
        ] = mock_rpc

        request = {}
        await client.list_import_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_import_jobs(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_import_jobs_async(
    transport: str = "grpc_asyncio", request_type=service.ListImportJobsRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_import_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListImportJobsResponse(
                next_page_token="next_page_token_value",
                total_size=1086,
            )
        )
        response = await client.list_import_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.ListImportJobsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListImportJobsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


@pytest.mark.asyncio
async def test_list_import_jobs_async_from_dict():
    await test_list_import_jobs_async(request_type=dict)


def test_list_import_jobs_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListImportJobsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_import_jobs), "__call__") as call:
        call.return_value = service.ListImportJobsResponse()
        client.list_import_jobs(request)

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
async def test_list_import_jobs_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListImportJobsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_import_jobs), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListImportJobsResponse()
        )
        await client.list_import_jobs(request)

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


def test_list_import_jobs_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_import_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListImportJobsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_import_jobs(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_import_jobs_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_import_jobs(
            service.ListImportJobsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_import_jobs_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_import_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListImportJobsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListImportJobsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_import_jobs(
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
async def test_list_import_jobs_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_import_jobs(
            service.ListImportJobsRequest(),
            parent="parent_value",
        )


def test_list_import_jobs_pager(transport_name: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_import_jobs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListImportJobsResponse(
                import_jobs=[
                    resources.ImportJob(),
                    resources.ImportJob(),
                    resources.ImportJob(),
                ],
                next_page_token="abc",
            ),
            service.ListImportJobsResponse(
                import_jobs=[],
                next_page_token="def",
            ),
            service.ListImportJobsResponse(
                import_jobs=[
                    resources.ImportJob(),
                ],
                next_page_token="ghi",
            ),
            service.ListImportJobsResponse(
                import_jobs=[
                    resources.ImportJob(),
                    resources.ImportJob(),
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
        pager = client.list_import_jobs(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.ImportJob) for i in results)


def test_list_import_jobs_pages(transport_name: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_import_jobs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListImportJobsResponse(
                import_jobs=[
                    resources.ImportJob(),
                    resources.ImportJob(),
                    resources.ImportJob(),
                ],
                next_page_token="abc",
            ),
            service.ListImportJobsResponse(
                import_jobs=[],
                next_page_token="def",
            ),
            service.ListImportJobsResponse(
                import_jobs=[
                    resources.ImportJob(),
                ],
                next_page_token="ghi",
            ),
            service.ListImportJobsResponse(
                import_jobs=[
                    resources.ImportJob(),
                    resources.ImportJob(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_import_jobs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_import_jobs_async_pager():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_import_jobs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListImportJobsResponse(
                import_jobs=[
                    resources.ImportJob(),
                    resources.ImportJob(),
                    resources.ImportJob(),
                ],
                next_page_token="abc",
            ),
            service.ListImportJobsResponse(
                import_jobs=[],
                next_page_token="def",
            ),
            service.ListImportJobsResponse(
                import_jobs=[
                    resources.ImportJob(),
                ],
                next_page_token="ghi",
            ),
            service.ListImportJobsResponse(
                import_jobs=[
                    resources.ImportJob(),
                    resources.ImportJob(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_import_jobs(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.ImportJob) for i in responses)


@pytest.mark.asyncio
async def test_list_import_jobs_async_pages():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_import_jobs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListImportJobsResponse(
                import_jobs=[
                    resources.ImportJob(),
                    resources.ImportJob(),
                    resources.ImportJob(),
                ],
                next_page_token="abc",
            ),
            service.ListImportJobsResponse(
                import_jobs=[],
                next_page_token="def",
            ),
            service.ListImportJobsResponse(
                import_jobs=[
                    resources.ImportJob(),
                ],
                next_page_token="ghi",
            ),
            service.ListImportJobsResponse(
                import_jobs=[
                    resources.ImportJob(),
                    resources.ImportJob(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_import_jobs(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetKeyRingRequest,
        dict,
    ],
)
def test_get_key_ring(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_key_ring), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.KeyRing(
            name="name_value",
        )
        response = client.get_key_ring(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.GetKeyRingRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.KeyRing)
    assert response.name == "name_value"


def test_get_key_ring_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.GetKeyRingRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_key_ring), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_key_ring(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetKeyRingRequest(
            name="name_value",
        )


def test_get_key_ring_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_key_ring in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_key_ring] = mock_rpc
        request = {}
        client.get_key_ring(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_key_ring(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_key_ring_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_key_ring
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_key_ring
        ] = mock_rpc

        request = {}
        await client.get_key_ring(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_key_ring(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_key_ring_async(
    transport: str = "grpc_asyncio", request_type=service.GetKeyRingRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_key_ring), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.KeyRing(
                name="name_value",
            )
        )
        response = await client.get_key_ring(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.GetKeyRingRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.KeyRing)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_get_key_ring_async_from_dict():
    await test_get_key_ring_async(request_type=dict)


def test_get_key_ring_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetKeyRingRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_key_ring), "__call__") as call:
        call.return_value = resources.KeyRing()
        client.get_key_ring(request)

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
async def test_get_key_ring_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetKeyRingRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_key_ring), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.KeyRing())
        await client.get_key_ring(request)

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


def test_get_key_ring_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_key_ring), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.KeyRing()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_key_ring(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_key_ring_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_key_ring(
            service.GetKeyRingRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_key_ring_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_key_ring), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.KeyRing()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.KeyRing())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_key_ring(
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
async def test_get_key_ring_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_key_ring(
            service.GetKeyRingRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetCryptoKeyRequest,
        dict,
    ],
)
def test_get_crypto_key(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_crypto_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKey(
            name="name_value",
            purpose=resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
            import_only=True,
            crypto_key_backend="crypto_key_backend_value",
        )
        response = client.get_crypto_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.GetCryptoKeyRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKey)
    assert response.name == "name_value"
    assert response.purpose == resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
    assert response.import_only is True
    assert response.crypto_key_backend == "crypto_key_backend_value"


def test_get_crypto_key_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.GetCryptoKeyRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_crypto_key), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_crypto_key(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetCryptoKeyRequest(
            name="name_value",
        )


def test_get_crypto_key_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_crypto_key in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_crypto_key] = mock_rpc
        request = {}
        client.get_crypto_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_crypto_key(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_crypto_key_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_crypto_key
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_crypto_key
        ] = mock_rpc

        request = {}
        await client.get_crypto_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_crypto_key(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_crypto_key_async(
    transport: str = "grpc_asyncio", request_type=service.GetCryptoKeyRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_crypto_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKey(
                name="name_value",
                purpose=resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
                import_only=True,
                crypto_key_backend="crypto_key_backend_value",
            )
        )
        response = await client.get_crypto_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.GetCryptoKeyRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKey)
    assert response.name == "name_value"
    assert response.purpose == resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
    assert response.import_only is True
    assert response.crypto_key_backend == "crypto_key_backend_value"


@pytest.mark.asyncio
async def test_get_crypto_key_async_from_dict():
    await test_get_crypto_key_async(request_type=dict)


def test_get_crypto_key_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetCryptoKeyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_crypto_key), "__call__") as call:
        call.return_value = resources.CryptoKey()
        client.get_crypto_key(request)

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
async def test_get_crypto_key_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetCryptoKeyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_crypto_key), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.CryptoKey())
        await client.get_crypto_key(request)

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


def test_get_crypto_key_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_crypto_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKey()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_crypto_key(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_crypto_key_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_crypto_key(
            service.GetCryptoKeyRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_crypto_key_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_crypto_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKey()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.CryptoKey())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_crypto_key(
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
async def test_get_crypto_key_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_crypto_key(
            service.GetCryptoKeyRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetCryptoKeyVersionRequest,
        dict,
    ],
)
def test_get_crypto_key_version(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion(
            name="name_value",
            state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
            import_job="import_job_value",
            import_failure_reason="import_failure_reason_value",
            generation_failure_reason="generation_failure_reason_value",
            external_destruction_failure_reason="external_destruction_failure_reason_value",
            reimport_eligible=True,
        )
        response = client.get_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.GetCryptoKeyVersionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == "name_value"
    assert (
        response.state
        == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert (
        response.algorithm
        == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert response.import_job == "import_job_value"
    assert response.import_failure_reason == "import_failure_reason_value"
    assert response.generation_failure_reason == "generation_failure_reason_value"
    assert (
        response.external_destruction_failure_reason
        == "external_destruction_failure_reason_value"
    )
    assert response.reimport_eligible is True


def test_get_crypto_key_version_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.GetCryptoKeyVersionRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_crypto_key_version), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_crypto_key_version(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetCryptoKeyVersionRequest(
            name="name_value",
        )


def test_get_crypto_key_version_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_crypto_key_version
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_crypto_key_version
        ] = mock_rpc
        request = {}
        client.get_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_crypto_key_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_crypto_key_version_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_crypto_key_version
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_crypto_key_version
        ] = mock_rpc

        request = {}
        await client.get_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_crypto_key_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_crypto_key_version_async(
    transport: str = "grpc_asyncio", request_type=service.GetCryptoKeyVersionRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion(
                name="name_value",
                state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
                protection_level=resources.ProtectionLevel.SOFTWARE,
                algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
                import_job="import_job_value",
                import_failure_reason="import_failure_reason_value",
                generation_failure_reason="generation_failure_reason_value",
                external_destruction_failure_reason="external_destruction_failure_reason_value",
                reimport_eligible=True,
            )
        )
        response = await client.get_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.GetCryptoKeyVersionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == "name_value"
    assert (
        response.state
        == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert (
        response.algorithm
        == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert response.import_job == "import_job_value"
    assert response.import_failure_reason == "import_failure_reason_value"
    assert response.generation_failure_reason == "generation_failure_reason_value"
    assert (
        response.external_destruction_failure_reason
        == "external_destruction_failure_reason_value"
    )
    assert response.reimport_eligible is True


@pytest.mark.asyncio
async def test_get_crypto_key_version_async_from_dict():
    await test_get_crypto_key_version_async(request_type=dict)


def test_get_crypto_key_version_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetCryptoKeyVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_crypto_key_version), "__call__"
    ) as call:
        call.return_value = resources.CryptoKeyVersion()
        client.get_crypto_key_version(request)

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
async def test_get_crypto_key_version_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetCryptoKeyVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_crypto_key_version), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion()
        )
        await client.get_crypto_key_version(request)

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


def test_get_crypto_key_version_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_crypto_key_version(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_crypto_key_version_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_crypto_key_version(
            service.GetCryptoKeyVersionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_crypto_key_version_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_crypto_key_version(
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
async def test_get_crypto_key_version_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_crypto_key_version(
            service.GetCryptoKeyVersionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetPublicKeyRequest,
        dict,
    ],
)
def test_get_public_key(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_public_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.PublicKey(
            pem="pem_value",
            algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
            name="name_value",
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )
        response = client.get_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.GetPublicKeyRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.PublicKey)
    assert response.pem == "pem_value"
    assert (
        response.algorithm
        == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert response.name == "name_value"
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


def test_get_public_key_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.GetPublicKeyRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_public_key), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_public_key(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetPublicKeyRequest(
            name="name_value",
        )


def test_get_public_key_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_public_key in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_public_key] = mock_rpc
        request = {}
        client.get_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_public_key(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_public_key_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_public_key
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_public_key
        ] = mock_rpc

        request = {}
        await client.get_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_public_key(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_public_key_async(
    transport: str = "grpc_asyncio", request_type=service.GetPublicKeyRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_public_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.PublicKey(
                pem="pem_value",
                algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
                name="name_value",
                protection_level=resources.ProtectionLevel.SOFTWARE,
            )
        )
        response = await client.get_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.GetPublicKeyRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.PublicKey)
    assert response.pem == "pem_value"
    assert (
        response.algorithm
        == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert response.name == "name_value"
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


@pytest.mark.asyncio
async def test_get_public_key_async_from_dict():
    await test_get_public_key_async(request_type=dict)


def test_get_public_key_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetPublicKeyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_public_key), "__call__") as call:
        call.return_value = resources.PublicKey()
        client.get_public_key(request)

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
async def test_get_public_key_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetPublicKeyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_public_key), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.PublicKey())
        await client.get_public_key(request)

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


def test_get_public_key_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_public_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.PublicKey()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_public_key(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_public_key_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_public_key(
            service.GetPublicKeyRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_public_key_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_public_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.PublicKey()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.PublicKey())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_public_key(
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
async def test_get_public_key_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_public_key(
            service.GetPublicKeyRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetImportJobRequest,
        dict,
    ],
)
def test_get_import_job(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_import_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ImportJob(
            name="name_value",
            import_method=resources.ImportJob.ImportMethod.RSA_OAEP_3072_SHA1_AES_256,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            state=resources.ImportJob.ImportJobState.PENDING_GENERATION,
        )
        response = client.get_import_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.GetImportJobRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.ImportJob)
    assert response.name == "name_value"
    assert (
        response.import_method
        == resources.ImportJob.ImportMethod.RSA_OAEP_3072_SHA1_AES_256
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert response.state == resources.ImportJob.ImportJobState.PENDING_GENERATION


def test_get_import_job_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.GetImportJobRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_import_job), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_import_job(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetImportJobRequest(
            name="name_value",
        )


def test_get_import_job_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_import_job in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_import_job] = mock_rpc
        request = {}
        client.get_import_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_import_job(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_import_job_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_import_job
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_import_job
        ] = mock_rpc

        request = {}
        await client.get_import_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_import_job(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_import_job_async(
    transport: str = "grpc_asyncio", request_type=service.GetImportJobRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_import_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ImportJob(
                name="name_value",
                import_method=resources.ImportJob.ImportMethod.RSA_OAEP_3072_SHA1_AES_256,
                protection_level=resources.ProtectionLevel.SOFTWARE,
                state=resources.ImportJob.ImportJobState.PENDING_GENERATION,
            )
        )
        response = await client.get_import_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.GetImportJobRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.ImportJob)
    assert response.name == "name_value"
    assert (
        response.import_method
        == resources.ImportJob.ImportMethod.RSA_OAEP_3072_SHA1_AES_256
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert response.state == resources.ImportJob.ImportJobState.PENDING_GENERATION


@pytest.mark.asyncio
async def test_get_import_job_async_from_dict():
    await test_get_import_job_async(request_type=dict)


def test_get_import_job_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetImportJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_import_job), "__call__") as call:
        call.return_value = resources.ImportJob()
        client.get_import_job(request)

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
async def test_get_import_job_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetImportJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_import_job), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.ImportJob())
        await client.get_import_job(request)

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


def test_get_import_job_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_import_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ImportJob()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_import_job(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_import_job_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_import_job(
            service.GetImportJobRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_import_job_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_import_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ImportJob()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.ImportJob())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_import_job(
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
async def test_get_import_job_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_import_job(
            service.GetImportJobRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.CreateKeyRingRequest,
        dict,
    ],
)
def test_create_key_ring(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_key_ring), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.KeyRing(
            name="name_value",
        )
        response = client.create_key_ring(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.CreateKeyRingRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.KeyRing)
    assert response.name == "name_value"


def test_create_key_ring_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.CreateKeyRingRequest(
        parent="parent_value",
        key_ring_id="key_ring_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_key_ring), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_key_ring(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateKeyRingRequest(
            parent="parent_value",
            key_ring_id="key_ring_id_value",
        )


def test_create_key_ring_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_key_ring in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.create_key_ring] = mock_rpc
        request = {}
        client.create_key_ring(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_key_ring(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_key_ring_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_key_ring
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_key_ring
        ] = mock_rpc

        request = {}
        await client.create_key_ring(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.create_key_ring(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_key_ring_async(
    transport: str = "grpc_asyncio", request_type=service.CreateKeyRingRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_key_ring), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.KeyRing(
                name="name_value",
            )
        )
        response = await client.create_key_ring(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.CreateKeyRingRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.KeyRing)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_create_key_ring_async_from_dict():
    await test_create_key_ring_async(request_type=dict)


def test_create_key_ring_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateKeyRingRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_key_ring), "__call__") as call:
        call.return_value = resources.KeyRing()
        client.create_key_ring(request)

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
async def test_create_key_ring_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateKeyRingRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_key_ring), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.KeyRing())
        await client.create_key_ring(request)

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


def test_create_key_ring_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_key_ring), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.KeyRing()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_key_ring(
            parent="parent_value",
            key_ring_id="key_ring_id_value",
            key_ring=resources.KeyRing(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].key_ring_id
        mock_val = "key_ring_id_value"
        assert arg == mock_val
        arg = args[0].key_ring
        mock_val = resources.KeyRing(name="name_value")
        assert arg == mock_val


def test_create_key_ring_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_key_ring(
            service.CreateKeyRingRequest(),
            parent="parent_value",
            key_ring_id="key_ring_id_value",
            key_ring=resources.KeyRing(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_key_ring_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_key_ring), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.KeyRing()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.KeyRing())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_key_ring(
            parent="parent_value",
            key_ring_id="key_ring_id_value",
            key_ring=resources.KeyRing(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].key_ring_id
        mock_val = "key_ring_id_value"
        assert arg == mock_val
        arg = args[0].key_ring
        mock_val = resources.KeyRing(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_key_ring_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_key_ring(
            service.CreateKeyRingRequest(),
            parent="parent_value",
            key_ring_id="key_ring_id_value",
            key_ring=resources.KeyRing(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.CreateCryptoKeyRequest,
        dict,
    ],
)
def test_create_crypto_key(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_crypto_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKey(
            name="name_value",
            purpose=resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
            import_only=True,
            crypto_key_backend="crypto_key_backend_value",
        )
        response = client.create_crypto_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.CreateCryptoKeyRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKey)
    assert response.name == "name_value"
    assert response.purpose == resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
    assert response.import_only is True
    assert response.crypto_key_backend == "crypto_key_backend_value"


def test_create_crypto_key_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.CreateCryptoKeyRequest(
        parent="parent_value",
        crypto_key_id="crypto_key_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_crypto_key), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_crypto_key(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateCryptoKeyRequest(
            parent="parent_value",
            crypto_key_id="crypto_key_id_value",
        )


def test_create_crypto_key_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_crypto_key in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_crypto_key
        ] = mock_rpc
        request = {}
        client.create_crypto_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_crypto_key(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_crypto_key_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_crypto_key
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_crypto_key
        ] = mock_rpc

        request = {}
        await client.create_crypto_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.create_crypto_key(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_crypto_key_async(
    transport: str = "grpc_asyncio", request_type=service.CreateCryptoKeyRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_crypto_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKey(
                name="name_value",
                purpose=resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
                import_only=True,
                crypto_key_backend="crypto_key_backend_value",
            )
        )
        response = await client.create_crypto_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.CreateCryptoKeyRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKey)
    assert response.name == "name_value"
    assert response.purpose == resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
    assert response.import_only is True
    assert response.crypto_key_backend == "crypto_key_backend_value"


@pytest.mark.asyncio
async def test_create_crypto_key_async_from_dict():
    await test_create_crypto_key_async(request_type=dict)


def test_create_crypto_key_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateCryptoKeyRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_crypto_key), "__call__"
    ) as call:
        call.return_value = resources.CryptoKey()
        client.create_crypto_key(request)

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
async def test_create_crypto_key_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateCryptoKeyRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_crypto_key), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.CryptoKey())
        await client.create_crypto_key(request)

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


def test_create_crypto_key_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_crypto_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKey()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_crypto_key(
            parent="parent_value",
            crypto_key_id="crypto_key_id_value",
            crypto_key=resources.CryptoKey(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].crypto_key_id
        mock_val = "crypto_key_id_value"
        assert arg == mock_val
        arg = args[0].crypto_key
        mock_val = resources.CryptoKey(name="name_value")
        assert arg == mock_val


def test_create_crypto_key_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_crypto_key(
            service.CreateCryptoKeyRequest(),
            parent="parent_value",
            crypto_key_id="crypto_key_id_value",
            crypto_key=resources.CryptoKey(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_crypto_key_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_crypto_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKey()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.CryptoKey())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_crypto_key(
            parent="parent_value",
            crypto_key_id="crypto_key_id_value",
            crypto_key=resources.CryptoKey(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].crypto_key_id
        mock_val = "crypto_key_id_value"
        assert arg == mock_val
        arg = args[0].crypto_key
        mock_val = resources.CryptoKey(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_crypto_key_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_crypto_key(
            service.CreateCryptoKeyRequest(),
            parent="parent_value",
            crypto_key_id="crypto_key_id_value",
            crypto_key=resources.CryptoKey(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.CreateCryptoKeyVersionRequest,
        dict,
    ],
)
def test_create_crypto_key_version(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion(
            name="name_value",
            state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
            import_job="import_job_value",
            import_failure_reason="import_failure_reason_value",
            generation_failure_reason="generation_failure_reason_value",
            external_destruction_failure_reason="external_destruction_failure_reason_value",
            reimport_eligible=True,
        )
        response = client.create_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.CreateCryptoKeyVersionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == "name_value"
    assert (
        response.state
        == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert (
        response.algorithm
        == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert response.import_job == "import_job_value"
    assert response.import_failure_reason == "import_failure_reason_value"
    assert response.generation_failure_reason == "generation_failure_reason_value"
    assert (
        response.external_destruction_failure_reason
        == "external_destruction_failure_reason_value"
    )
    assert response.reimport_eligible is True


def test_create_crypto_key_version_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.CreateCryptoKeyVersionRequest(
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_crypto_key_version), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_crypto_key_version(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateCryptoKeyVersionRequest(
            parent="parent_value",
        )


def test_create_crypto_key_version_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_crypto_key_version
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_crypto_key_version
        ] = mock_rpc
        request = {}
        client.create_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_crypto_key_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_crypto_key_version_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_crypto_key_version
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_crypto_key_version
        ] = mock_rpc

        request = {}
        await client.create_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.create_crypto_key_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_crypto_key_version_async(
    transport: str = "grpc_asyncio", request_type=service.CreateCryptoKeyVersionRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion(
                name="name_value",
                state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
                protection_level=resources.ProtectionLevel.SOFTWARE,
                algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
                import_job="import_job_value",
                import_failure_reason="import_failure_reason_value",
                generation_failure_reason="generation_failure_reason_value",
                external_destruction_failure_reason="external_destruction_failure_reason_value",
                reimport_eligible=True,
            )
        )
        response = await client.create_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.CreateCryptoKeyVersionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == "name_value"
    assert (
        response.state
        == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert (
        response.algorithm
        == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert response.import_job == "import_job_value"
    assert response.import_failure_reason == "import_failure_reason_value"
    assert response.generation_failure_reason == "generation_failure_reason_value"
    assert (
        response.external_destruction_failure_reason
        == "external_destruction_failure_reason_value"
    )
    assert response.reimport_eligible is True


@pytest.mark.asyncio
async def test_create_crypto_key_version_async_from_dict():
    await test_create_crypto_key_version_async(request_type=dict)


def test_create_crypto_key_version_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateCryptoKeyVersionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_crypto_key_version), "__call__"
    ) as call:
        call.return_value = resources.CryptoKeyVersion()
        client.create_crypto_key_version(request)

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
async def test_create_crypto_key_version_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateCryptoKeyVersionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_crypto_key_version), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion()
        )
        await client.create_crypto_key_version(request)

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


def test_create_crypto_key_version_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_crypto_key_version(
            parent="parent_value",
            crypto_key_version=resources.CryptoKeyVersion(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].crypto_key_version
        mock_val = resources.CryptoKeyVersion(name="name_value")
        assert arg == mock_val


def test_create_crypto_key_version_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_crypto_key_version(
            service.CreateCryptoKeyVersionRequest(),
            parent="parent_value",
            crypto_key_version=resources.CryptoKeyVersion(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_crypto_key_version_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_crypto_key_version(
            parent="parent_value",
            crypto_key_version=resources.CryptoKeyVersion(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].crypto_key_version
        mock_val = resources.CryptoKeyVersion(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_crypto_key_version_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_crypto_key_version(
            service.CreateCryptoKeyVersionRequest(),
            parent="parent_value",
            crypto_key_version=resources.CryptoKeyVersion(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.ImportCryptoKeyVersionRequest,
        dict,
    ],
)
def test_import_crypto_key_version(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion(
            name="name_value",
            state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
            import_job="import_job_value",
            import_failure_reason="import_failure_reason_value",
            generation_failure_reason="generation_failure_reason_value",
            external_destruction_failure_reason="external_destruction_failure_reason_value",
            reimport_eligible=True,
        )
        response = client.import_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.ImportCryptoKeyVersionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == "name_value"
    assert (
        response.state
        == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert (
        response.algorithm
        == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert response.import_job == "import_job_value"
    assert response.import_failure_reason == "import_failure_reason_value"
    assert response.generation_failure_reason == "generation_failure_reason_value"
    assert (
        response.external_destruction_failure_reason
        == "external_destruction_failure_reason_value"
    )
    assert response.reimport_eligible is True


def test_import_crypto_key_version_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.ImportCryptoKeyVersionRequest(
        parent="parent_value",
        crypto_key_version="crypto_key_version_value",
        import_job="import_job_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_crypto_key_version), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.import_crypto_key_version(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ImportCryptoKeyVersionRequest(
            parent="parent_value",
            crypto_key_version="crypto_key_version_value",
            import_job="import_job_value",
        )


def test_import_crypto_key_version_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.import_crypto_key_version
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.import_crypto_key_version
        ] = mock_rpc
        request = {}
        client.import_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.import_crypto_key_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_import_crypto_key_version_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.import_crypto_key_version
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.import_crypto_key_version
        ] = mock_rpc

        request = {}
        await client.import_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.import_crypto_key_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_import_crypto_key_version_async(
    transport: str = "grpc_asyncio", request_type=service.ImportCryptoKeyVersionRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion(
                name="name_value",
                state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
                protection_level=resources.ProtectionLevel.SOFTWARE,
                algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
                import_job="import_job_value",
                import_failure_reason="import_failure_reason_value",
                generation_failure_reason="generation_failure_reason_value",
                external_destruction_failure_reason="external_destruction_failure_reason_value",
                reimport_eligible=True,
            )
        )
        response = await client.import_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.ImportCryptoKeyVersionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == "name_value"
    assert (
        response.state
        == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert (
        response.algorithm
        == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert response.import_job == "import_job_value"
    assert response.import_failure_reason == "import_failure_reason_value"
    assert response.generation_failure_reason == "generation_failure_reason_value"
    assert (
        response.external_destruction_failure_reason
        == "external_destruction_failure_reason_value"
    )
    assert response.reimport_eligible is True


@pytest.mark.asyncio
async def test_import_crypto_key_version_async_from_dict():
    await test_import_crypto_key_version_async(request_type=dict)


def test_import_crypto_key_version_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ImportCryptoKeyVersionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_crypto_key_version), "__call__"
    ) as call:
        call.return_value = resources.CryptoKeyVersion()
        client.import_crypto_key_version(request)

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
async def test_import_crypto_key_version_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ImportCryptoKeyVersionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_crypto_key_version), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion()
        )
        await client.import_crypto_key_version(request)

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
        service.CreateImportJobRequest,
        dict,
    ],
)
def test_create_import_job(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_import_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ImportJob(
            name="name_value",
            import_method=resources.ImportJob.ImportMethod.RSA_OAEP_3072_SHA1_AES_256,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            state=resources.ImportJob.ImportJobState.PENDING_GENERATION,
        )
        response = client.create_import_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.CreateImportJobRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.ImportJob)
    assert response.name == "name_value"
    assert (
        response.import_method
        == resources.ImportJob.ImportMethod.RSA_OAEP_3072_SHA1_AES_256
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert response.state == resources.ImportJob.ImportJobState.PENDING_GENERATION


def test_create_import_job_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.CreateImportJobRequest(
        parent="parent_value",
        import_job_id="import_job_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_import_job), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_import_job(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateImportJobRequest(
            parent="parent_value",
            import_job_id="import_job_id_value",
        )


def test_create_import_job_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_import_job in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_import_job
        ] = mock_rpc
        request = {}
        client.create_import_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_import_job(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_import_job_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_import_job
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_import_job
        ] = mock_rpc

        request = {}
        await client.create_import_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.create_import_job(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_import_job_async(
    transport: str = "grpc_asyncio", request_type=service.CreateImportJobRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_import_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ImportJob(
                name="name_value",
                import_method=resources.ImportJob.ImportMethod.RSA_OAEP_3072_SHA1_AES_256,
                protection_level=resources.ProtectionLevel.SOFTWARE,
                state=resources.ImportJob.ImportJobState.PENDING_GENERATION,
            )
        )
        response = await client.create_import_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.CreateImportJobRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.ImportJob)
    assert response.name == "name_value"
    assert (
        response.import_method
        == resources.ImportJob.ImportMethod.RSA_OAEP_3072_SHA1_AES_256
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert response.state == resources.ImportJob.ImportJobState.PENDING_GENERATION


@pytest.mark.asyncio
async def test_create_import_job_async_from_dict():
    await test_create_import_job_async(request_type=dict)


def test_create_import_job_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateImportJobRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_import_job), "__call__"
    ) as call:
        call.return_value = resources.ImportJob()
        client.create_import_job(request)

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
async def test_create_import_job_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateImportJobRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_import_job), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.ImportJob())
        await client.create_import_job(request)

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


def test_create_import_job_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_import_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ImportJob()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_import_job(
            parent="parent_value",
            import_job_id="import_job_id_value",
            import_job=resources.ImportJob(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].import_job_id
        mock_val = "import_job_id_value"
        assert arg == mock_val
        arg = args[0].import_job
        mock_val = resources.ImportJob(name="name_value")
        assert arg == mock_val


def test_create_import_job_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_import_job(
            service.CreateImportJobRequest(),
            parent="parent_value",
            import_job_id="import_job_id_value",
            import_job=resources.ImportJob(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_import_job_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_import_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ImportJob()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.ImportJob())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_import_job(
            parent="parent_value",
            import_job_id="import_job_id_value",
            import_job=resources.ImportJob(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].import_job_id
        mock_val = "import_job_id_value"
        assert arg == mock_val
        arg = args[0].import_job
        mock_val = resources.ImportJob(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_import_job_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_import_job(
            service.CreateImportJobRequest(),
            parent="parent_value",
            import_job_id="import_job_id_value",
            import_job=resources.ImportJob(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.UpdateCryptoKeyRequest,
        dict,
    ],
)
def test_update_crypto_key(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKey(
            name="name_value",
            purpose=resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
            import_only=True,
            crypto_key_backend="crypto_key_backend_value",
        )
        response = client.update_crypto_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.UpdateCryptoKeyRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKey)
    assert response.name == "name_value"
    assert response.purpose == resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
    assert response.import_only is True
    assert response.crypto_key_backend == "crypto_key_backend_value"


def test_update_crypto_key_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.UpdateCryptoKeyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_crypto_key(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateCryptoKeyRequest()


def test_update_crypto_key_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.update_crypto_key in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_crypto_key
        ] = mock_rpc
        request = {}
        client.update_crypto_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_crypto_key(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_crypto_key_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_crypto_key
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_crypto_key
        ] = mock_rpc

        request = {}
        await client.update_crypto_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.update_crypto_key(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_crypto_key_async(
    transport: str = "grpc_asyncio", request_type=service.UpdateCryptoKeyRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKey(
                name="name_value",
                purpose=resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
                import_only=True,
                crypto_key_backend="crypto_key_backend_value",
            )
        )
        response = await client.update_crypto_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.UpdateCryptoKeyRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKey)
    assert response.name == "name_value"
    assert response.purpose == resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
    assert response.import_only is True
    assert response.crypto_key_backend == "crypto_key_backend_value"


@pytest.mark.asyncio
async def test_update_crypto_key_async_from_dict():
    await test_update_crypto_key_async(request_type=dict)


def test_update_crypto_key_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateCryptoKeyRequest()

    request.crypto_key.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key), "__call__"
    ) as call:
        call.return_value = resources.CryptoKey()
        client.update_crypto_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "crypto_key.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_crypto_key_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateCryptoKeyRequest()

    request.crypto_key.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.CryptoKey())
        await client.update_crypto_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "crypto_key.name=name_value",
    ) in kw["metadata"]


def test_update_crypto_key_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKey()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_crypto_key(
            crypto_key=resources.CryptoKey(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].crypto_key
        mock_val = resources.CryptoKey(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_crypto_key_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_crypto_key(
            service.UpdateCryptoKeyRequest(),
            crypto_key=resources.CryptoKey(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_crypto_key_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKey()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.CryptoKey())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_crypto_key(
            crypto_key=resources.CryptoKey(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].crypto_key
        mock_val = resources.CryptoKey(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_crypto_key_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_crypto_key(
            service.UpdateCryptoKeyRequest(),
            crypto_key=resources.CryptoKey(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.UpdateCryptoKeyVersionRequest,
        dict,
    ],
)
def test_update_crypto_key_version(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion(
            name="name_value",
            state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
            import_job="import_job_value",
            import_failure_reason="import_failure_reason_value",
            generation_failure_reason="generation_failure_reason_value",
            external_destruction_failure_reason="external_destruction_failure_reason_value",
            reimport_eligible=True,
        )
        response = client.update_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.UpdateCryptoKeyVersionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == "name_value"
    assert (
        response.state
        == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert (
        response.algorithm
        == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert response.import_job == "import_job_value"
    assert response.import_failure_reason == "import_failure_reason_value"
    assert response.generation_failure_reason == "generation_failure_reason_value"
    assert (
        response.external_destruction_failure_reason
        == "external_destruction_failure_reason_value"
    )
    assert response.reimport_eligible is True


def test_update_crypto_key_version_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.UpdateCryptoKeyVersionRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key_version), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_crypto_key_version(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateCryptoKeyVersionRequest()


def test_update_crypto_key_version_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_crypto_key_version
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_crypto_key_version
        ] = mock_rpc
        request = {}
        client.update_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_crypto_key_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_crypto_key_version_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_crypto_key_version
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_crypto_key_version
        ] = mock_rpc

        request = {}
        await client.update_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.update_crypto_key_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_crypto_key_version_async(
    transport: str = "grpc_asyncio", request_type=service.UpdateCryptoKeyVersionRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion(
                name="name_value",
                state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
                protection_level=resources.ProtectionLevel.SOFTWARE,
                algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
                import_job="import_job_value",
                import_failure_reason="import_failure_reason_value",
                generation_failure_reason="generation_failure_reason_value",
                external_destruction_failure_reason="external_destruction_failure_reason_value",
                reimport_eligible=True,
            )
        )
        response = await client.update_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.UpdateCryptoKeyVersionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == "name_value"
    assert (
        response.state
        == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert (
        response.algorithm
        == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert response.import_job == "import_job_value"
    assert response.import_failure_reason == "import_failure_reason_value"
    assert response.generation_failure_reason == "generation_failure_reason_value"
    assert (
        response.external_destruction_failure_reason
        == "external_destruction_failure_reason_value"
    )
    assert response.reimport_eligible is True


@pytest.mark.asyncio
async def test_update_crypto_key_version_async_from_dict():
    await test_update_crypto_key_version_async(request_type=dict)


def test_update_crypto_key_version_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateCryptoKeyVersionRequest()

    request.crypto_key_version.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key_version), "__call__"
    ) as call:
        call.return_value = resources.CryptoKeyVersion()
        client.update_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "crypto_key_version.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_crypto_key_version_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateCryptoKeyVersionRequest()

    request.crypto_key_version.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key_version), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion()
        )
        await client.update_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "crypto_key_version.name=name_value",
    ) in kw["metadata"]


def test_update_crypto_key_version_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_crypto_key_version(
            crypto_key_version=resources.CryptoKeyVersion(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].crypto_key_version
        mock_val = resources.CryptoKeyVersion(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_crypto_key_version_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_crypto_key_version(
            service.UpdateCryptoKeyVersionRequest(),
            crypto_key_version=resources.CryptoKeyVersion(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_crypto_key_version_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_crypto_key_version(
            crypto_key_version=resources.CryptoKeyVersion(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].crypto_key_version
        mock_val = resources.CryptoKeyVersion(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_crypto_key_version_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_crypto_key_version(
            service.UpdateCryptoKeyVersionRequest(),
            crypto_key_version=resources.CryptoKeyVersion(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.UpdateCryptoKeyPrimaryVersionRequest,
        dict,
    ],
)
def test_update_crypto_key_primary_version(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key_primary_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKey(
            name="name_value",
            purpose=resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
            import_only=True,
            crypto_key_backend="crypto_key_backend_value",
        )
        response = client.update_crypto_key_primary_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.UpdateCryptoKeyPrimaryVersionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKey)
    assert response.name == "name_value"
    assert response.purpose == resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
    assert response.import_only is True
    assert response.crypto_key_backend == "crypto_key_backend_value"


def test_update_crypto_key_primary_version_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.UpdateCryptoKeyPrimaryVersionRequest(
        name="name_value",
        crypto_key_version_id="crypto_key_version_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key_primary_version), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_crypto_key_primary_version(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateCryptoKeyPrimaryVersionRequest(
            name="name_value",
            crypto_key_version_id="crypto_key_version_id_value",
        )


def test_update_crypto_key_primary_version_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_crypto_key_primary_version
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_crypto_key_primary_version
        ] = mock_rpc
        request = {}
        client.update_crypto_key_primary_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_crypto_key_primary_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_crypto_key_primary_version_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_crypto_key_primary_version
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_crypto_key_primary_version
        ] = mock_rpc

        request = {}
        await client.update_crypto_key_primary_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.update_crypto_key_primary_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_crypto_key_primary_version_async(
    transport: str = "grpc_asyncio",
    request_type=service.UpdateCryptoKeyPrimaryVersionRequest,
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key_primary_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKey(
                name="name_value",
                purpose=resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
                import_only=True,
                crypto_key_backend="crypto_key_backend_value",
            )
        )
        response = await client.update_crypto_key_primary_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.UpdateCryptoKeyPrimaryVersionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKey)
    assert response.name == "name_value"
    assert response.purpose == resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
    assert response.import_only is True
    assert response.crypto_key_backend == "crypto_key_backend_value"


@pytest.mark.asyncio
async def test_update_crypto_key_primary_version_async_from_dict():
    await test_update_crypto_key_primary_version_async(request_type=dict)


def test_update_crypto_key_primary_version_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateCryptoKeyPrimaryVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key_primary_version), "__call__"
    ) as call:
        call.return_value = resources.CryptoKey()
        client.update_crypto_key_primary_version(request)

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
async def test_update_crypto_key_primary_version_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateCryptoKeyPrimaryVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key_primary_version), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.CryptoKey())
        await client.update_crypto_key_primary_version(request)

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


def test_update_crypto_key_primary_version_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key_primary_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKey()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_crypto_key_primary_version(
            name="name_value",
            crypto_key_version_id="crypto_key_version_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].crypto_key_version_id
        mock_val = "crypto_key_version_id_value"
        assert arg == mock_val


def test_update_crypto_key_primary_version_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_crypto_key_primary_version(
            service.UpdateCryptoKeyPrimaryVersionRequest(),
            name="name_value",
            crypto_key_version_id="crypto_key_version_id_value",
        )


@pytest.mark.asyncio
async def test_update_crypto_key_primary_version_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key_primary_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKey()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.CryptoKey())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_crypto_key_primary_version(
            name="name_value",
            crypto_key_version_id="crypto_key_version_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].crypto_key_version_id
        mock_val = "crypto_key_version_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_crypto_key_primary_version_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_crypto_key_primary_version(
            service.UpdateCryptoKeyPrimaryVersionRequest(),
            name="name_value",
            crypto_key_version_id="crypto_key_version_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.DestroyCryptoKeyVersionRequest,
        dict,
    ],
)
def test_destroy_crypto_key_version(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.destroy_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion(
            name="name_value",
            state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
            import_job="import_job_value",
            import_failure_reason="import_failure_reason_value",
            generation_failure_reason="generation_failure_reason_value",
            external_destruction_failure_reason="external_destruction_failure_reason_value",
            reimport_eligible=True,
        )
        response = client.destroy_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.DestroyCryptoKeyVersionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == "name_value"
    assert (
        response.state
        == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert (
        response.algorithm
        == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert response.import_job == "import_job_value"
    assert response.import_failure_reason == "import_failure_reason_value"
    assert response.generation_failure_reason == "generation_failure_reason_value"
    assert (
        response.external_destruction_failure_reason
        == "external_destruction_failure_reason_value"
    )
    assert response.reimport_eligible is True


def test_destroy_crypto_key_version_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.DestroyCryptoKeyVersionRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.destroy_crypto_key_version), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.destroy_crypto_key_version(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DestroyCryptoKeyVersionRequest(
            name="name_value",
        )


def test_destroy_crypto_key_version_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.destroy_crypto_key_version
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.destroy_crypto_key_version
        ] = mock_rpc
        request = {}
        client.destroy_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.destroy_crypto_key_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_destroy_crypto_key_version_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.destroy_crypto_key_version
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.destroy_crypto_key_version
        ] = mock_rpc

        request = {}
        await client.destroy_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.destroy_crypto_key_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_destroy_crypto_key_version_async(
    transport: str = "grpc_asyncio", request_type=service.DestroyCryptoKeyVersionRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.destroy_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion(
                name="name_value",
                state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
                protection_level=resources.ProtectionLevel.SOFTWARE,
                algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
                import_job="import_job_value",
                import_failure_reason="import_failure_reason_value",
                generation_failure_reason="generation_failure_reason_value",
                external_destruction_failure_reason="external_destruction_failure_reason_value",
                reimport_eligible=True,
            )
        )
        response = await client.destroy_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.DestroyCryptoKeyVersionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == "name_value"
    assert (
        response.state
        == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert (
        response.algorithm
        == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert response.import_job == "import_job_value"
    assert response.import_failure_reason == "import_failure_reason_value"
    assert response.generation_failure_reason == "generation_failure_reason_value"
    assert (
        response.external_destruction_failure_reason
        == "external_destruction_failure_reason_value"
    )
    assert response.reimport_eligible is True


@pytest.mark.asyncio
async def test_destroy_crypto_key_version_async_from_dict():
    await test_destroy_crypto_key_version_async(request_type=dict)


def test_destroy_crypto_key_version_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DestroyCryptoKeyVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.destroy_crypto_key_version), "__call__"
    ) as call:
        call.return_value = resources.CryptoKeyVersion()
        client.destroy_crypto_key_version(request)

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
async def test_destroy_crypto_key_version_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DestroyCryptoKeyVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.destroy_crypto_key_version), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion()
        )
        await client.destroy_crypto_key_version(request)

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


def test_destroy_crypto_key_version_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.destroy_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.destroy_crypto_key_version(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_destroy_crypto_key_version_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.destroy_crypto_key_version(
            service.DestroyCryptoKeyVersionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_destroy_crypto_key_version_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.destroy_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.destroy_crypto_key_version(
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
async def test_destroy_crypto_key_version_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.destroy_crypto_key_version(
            service.DestroyCryptoKeyVersionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.RestoreCryptoKeyVersionRequest,
        dict,
    ],
)
def test_restore_crypto_key_version(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restore_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion(
            name="name_value",
            state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
            import_job="import_job_value",
            import_failure_reason="import_failure_reason_value",
            generation_failure_reason="generation_failure_reason_value",
            external_destruction_failure_reason="external_destruction_failure_reason_value",
            reimport_eligible=True,
        )
        response = client.restore_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.RestoreCryptoKeyVersionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == "name_value"
    assert (
        response.state
        == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert (
        response.algorithm
        == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert response.import_job == "import_job_value"
    assert response.import_failure_reason == "import_failure_reason_value"
    assert response.generation_failure_reason == "generation_failure_reason_value"
    assert (
        response.external_destruction_failure_reason
        == "external_destruction_failure_reason_value"
    )
    assert response.reimport_eligible is True


def test_restore_crypto_key_version_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.RestoreCryptoKeyVersionRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restore_crypto_key_version), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.restore_crypto_key_version(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.RestoreCryptoKeyVersionRequest(
            name="name_value",
        )


def test_restore_crypto_key_version_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.restore_crypto_key_version
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.restore_crypto_key_version
        ] = mock_rpc
        request = {}
        client.restore_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.restore_crypto_key_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_restore_crypto_key_version_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.restore_crypto_key_version
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.restore_crypto_key_version
        ] = mock_rpc

        request = {}
        await client.restore_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.restore_crypto_key_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_restore_crypto_key_version_async(
    transport: str = "grpc_asyncio", request_type=service.RestoreCryptoKeyVersionRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restore_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion(
                name="name_value",
                state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
                protection_level=resources.ProtectionLevel.SOFTWARE,
                algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
                import_job="import_job_value",
                import_failure_reason="import_failure_reason_value",
                generation_failure_reason="generation_failure_reason_value",
                external_destruction_failure_reason="external_destruction_failure_reason_value",
                reimport_eligible=True,
            )
        )
        response = await client.restore_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.RestoreCryptoKeyVersionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == "name_value"
    assert (
        response.state
        == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert (
        response.algorithm
        == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert response.import_job == "import_job_value"
    assert response.import_failure_reason == "import_failure_reason_value"
    assert response.generation_failure_reason == "generation_failure_reason_value"
    assert (
        response.external_destruction_failure_reason
        == "external_destruction_failure_reason_value"
    )
    assert response.reimport_eligible is True


@pytest.mark.asyncio
async def test_restore_crypto_key_version_async_from_dict():
    await test_restore_crypto_key_version_async(request_type=dict)


def test_restore_crypto_key_version_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.RestoreCryptoKeyVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restore_crypto_key_version), "__call__"
    ) as call:
        call.return_value = resources.CryptoKeyVersion()
        client.restore_crypto_key_version(request)

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
async def test_restore_crypto_key_version_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.RestoreCryptoKeyVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restore_crypto_key_version), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion()
        )
        await client.restore_crypto_key_version(request)

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


def test_restore_crypto_key_version_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restore_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.restore_crypto_key_version(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_restore_crypto_key_version_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.restore_crypto_key_version(
            service.RestoreCryptoKeyVersionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_restore_crypto_key_version_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restore_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.restore_crypto_key_version(
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
async def test_restore_crypto_key_version_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.restore_crypto_key_version(
            service.RestoreCryptoKeyVersionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.EncryptRequest,
        dict,
    ],
)
def test_encrypt(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.encrypt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.EncryptResponse(
            name="name_value",
            ciphertext=b"ciphertext_blob",
            verified_plaintext_crc32c=True,
            verified_additional_authenticated_data_crc32c=True,
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )
        response = client.encrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.EncryptRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.EncryptResponse)
    assert response.name == "name_value"
    assert response.ciphertext == b"ciphertext_blob"
    assert response.verified_plaintext_crc32c is True
    assert response.verified_additional_authenticated_data_crc32c is True
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


def test_encrypt_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.EncryptRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.encrypt), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.encrypt(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.EncryptRequest(
            name="name_value",
        )


def test_encrypt_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.encrypt in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.encrypt] = mock_rpc
        request = {}
        client.encrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.encrypt(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_encrypt_async_use_cached_wrapped_rpc(transport: str = "grpc_asyncio"):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.encrypt
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.encrypt
        ] = mock_rpc

        request = {}
        await client.encrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.encrypt(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_encrypt_async(
    transport: str = "grpc_asyncio", request_type=service.EncryptRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.encrypt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.EncryptResponse(
                name="name_value",
                ciphertext=b"ciphertext_blob",
                verified_plaintext_crc32c=True,
                verified_additional_authenticated_data_crc32c=True,
                protection_level=resources.ProtectionLevel.SOFTWARE,
            )
        )
        response = await client.encrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.EncryptRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.EncryptResponse)
    assert response.name == "name_value"
    assert response.ciphertext == b"ciphertext_blob"
    assert response.verified_plaintext_crc32c is True
    assert response.verified_additional_authenticated_data_crc32c is True
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


@pytest.mark.asyncio
async def test_encrypt_async_from_dict():
    await test_encrypt_async(request_type=dict)


def test_encrypt_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.EncryptRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.encrypt), "__call__") as call:
        call.return_value = service.EncryptResponse()
        client.encrypt(request)

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
async def test_encrypt_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.EncryptRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.encrypt), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.EncryptResponse()
        )
        await client.encrypt(request)

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


def test_encrypt_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.encrypt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.EncryptResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.encrypt(
            name="name_value",
            plaintext=b"plaintext_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].plaintext
        mock_val = b"plaintext_blob"
        assert arg == mock_val


def test_encrypt_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.encrypt(
            service.EncryptRequest(),
            name="name_value",
            plaintext=b"plaintext_blob",
        )


@pytest.mark.asyncio
async def test_encrypt_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.encrypt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.EncryptResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.EncryptResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.encrypt(
            name="name_value",
            plaintext=b"plaintext_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].plaintext
        mock_val = b"plaintext_blob"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_encrypt_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.encrypt(
            service.EncryptRequest(),
            name="name_value",
            plaintext=b"plaintext_blob",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.DecryptRequest,
        dict,
    ],
)
def test_decrypt(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.decrypt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.DecryptResponse(
            plaintext=b"plaintext_blob",
            used_primary=True,
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )
        response = client.decrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.DecryptRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.DecryptResponse)
    assert response.plaintext == b"plaintext_blob"
    assert response.used_primary is True
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


def test_decrypt_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.DecryptRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.decrypt), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.decrypt(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DecryptRequest(
            name="name_value",
        )


def test_decrypt_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.decrypt in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.decrypt] = mock_rpc
        request = {}
        client.decrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.decrypt(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_decrypt_async_use_cached_wrapped_rpc(transport: str = "grpc_asyncio"):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.decrypt
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.decrypt
        ] = mock_rpc

        request = {}
        await client.decrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.decrypt(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_decrypt_async(
    transport: str = "grpc_asyncio", request_type=service.DecryptRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.decrypt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.DecryptResponse(
                plaintext=b"plaintext_blob",
                used_primary=True,
                protection_level=resources.ProtectionLevel.SOFTWARE,
            )
        )
        response = await client.decrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.DecryptRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.DecryptResponse)
    assert response.plaintext == b"plaintext_blob"
    assert response.used_primary is True
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


@pytest.mark.asyncio
async def test_decrypt_async_from_dict():
    await test_decrypt_async(request_type=dict)


def test_decrypt_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DecryptRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.decrypt), "__call__") as call:
        call.return_value = service.DecryptResponse()
        client.decrypt(request)

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
async def test_decrypt_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DecryptRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.decrypt), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.DecryptResponse()
        )
        await client.decrypt(request)

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


def test_decrypt_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.decrypt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.DecryptResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.decrypt(
            name="name_value",
            ciphertext=b"ciphertext_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].ciphertext
        mock_val = b"ciphertext_blob"
        assert arg == mock_val


def test_decrypt_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.decrypt(
            service.DecryptRequest(),
            name="name_value",
            ciphertext=b"ciphertext_blob",
        )


@pytest.mark.asyncio
async def test_decrypt_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.decrypt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.DecryptResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.DecryptResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.decrypt(
            name="name_value",
            ciphertext=b"ciphertext_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].ciphertext
        mock_val = b"ciphertext_blob"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_decrypt_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.decrypt(
            service.DecryptRequest(),
            name="name_value",
            ciphertext=b"ciphertext_blob",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.RawEncryptRequest,
        dict,
    ],
)
def test_raw_encrypt(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.raw_encrypt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.RawEncryptResponse(
            ciphertext=b"ciphertext_blob",
            initialization_vector=b"initialization_vector_blob",
            tag_length=1053,
            verified_plaintext_crc32c=True,
            verified_additional_authenticated_data_crc32c=True,
            verified_initialization_vector_crc32c=True,
            name="name_value",
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )
        response = client.raw_encrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.RawEncryptRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.RawEncryptResponse)
    assert response.ciphertext == b"ciphertext_blob"
    assert response.initialization_vector == b"initialization_vector_blob"
    assert response.tag_length == 1053
    assert response.verified_plaintext_crc32c is True
    assert response.verified_additional_authenticated_data_crc32c is True
    assert response.verified_initialization_vector_crc32c is True
    assert response.name == "name_value"
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


def test_raw_encrypt_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.RawEncryptRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.raw_encrypt), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.raw_encrypt(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.RawEncryptRequest(
            name="name_value",
        )


def test_raw_encrypt_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.raw_encrypt in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.raw_encrypt] = mock_rpc
        request = {}
        client.raw_encrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.raw_encrypt(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_raw_encrypt_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.raw_encrypt
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.raw_encrypt
        ] = mock_rpc

        request = {}
        await client.raw_encrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.raw_encrypt(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_raw_encrypt_async(
    transport: str = "grpc_asyncio", request_type=service.RawEncryptRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.raw_encrypt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.RawEncryptResponse(
                ciphertext=b"ciphertext_blob",
                initialization_vector=b"initialization_vector_blob",
                tag_length=1053,
                verified_plaintext_crc32c=True,
                verified_additional_authenticated_data_crc32c=True,
                verified_initialization_vector_crc32c=True,
                name="name_value",
                protection_level=resources.ProtectionLevel.SOFTWARE,
            )
        )
        response = await client.raw_encrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.RawEncryptRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.RawEncryptResponse)
    assert response.ciphertext == b"ciphertext_blob"
    assert response.initialization_vector == b"initialization_vector_blob"
    assert response.tag_length == 1053
    assert response.verified_plaintext_crc32c is True
    assert response.verified_additional_authenticated_data_crc32c is True
    assert response.verified_initialization_vector_crc32c is True
    assert response.name == "name_value"
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


@pytest.mark.asyncio
async def test_raw_encrypt_async_from_dict():
    await test_raw_encrypt_async(request_type=dict)


def test_raw_encrypt_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.RawEncryptRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.raw_encrypt), "__call__") as call:
        call.return_value = service.RawEncryptResponse()
        client.raw_encrypt(request)

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
async def test_raw_encrypt_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.RawEncryptRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.raw_encrypt), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.RawEncryptResponse()
        )
        await client.raw_encrypt(request)

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
        service.RawDecryptRequest,
        dict,
    ],
)
def test_raw_decrypt(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.raw_decrypt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.RawDecryptResponse(
            plaintext=b"plaintext_blob",
            protection_level=resources.ProtectionLevel.SOFTWARE,
            verified_ciphertext_crc32c=True,
            verified_additional_authenticated_data_crc32c=True,
            verified_initialization_vector_crc32c=True,
        )
        response = client.raw_decrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.RawDecryptRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.RawDecryptResponse)
    assert response.plaintext == b"plaintext_blob"
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert response.verified_ciphertext_crc32c is True
    assert response.verified_additional_authenticated_data_crc32c is True
    assert response.verified_initialization_vector_crc32c is True


def test_raw_decrypt_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.RawDecryptRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.raw_decrypt), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.raw_decrypt(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.RawDecryptRequest(
            name="name_value",
        )


def test_raw_decrypt_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.raw_decrypt in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.raw_decrypt] = mock_rpc
        request = {}
        client.raw_decrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.raw_decrypt(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_raw_decrypt_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.raw_decrypt
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.raw_decrypt
        ] = mock_rpc

        request = {}
        await client.raw_decrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.raw_decrypt(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_raw_decrypt_async(
    transport: str = "grpc_asyncio", request_type=service.RawDecryptRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.raw_decrypt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.RawDecryptResponse(
                plaintext=b"plaintext_blob",
                protection_level=resources.ProtectionLevel.SOFTWARE,
                verified_ciphertext_crc32c=True,
                verified_additional_authenticated_data_crc32c=True,
                verified_initialization_vector_crc32c=True,
            )
        )
        response = await client.raw_decrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.RawDecryptRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.RawDecryptResponse)
    assert response.plaintext == b"plaintext_blob"
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert response.verified_ciphertext_crc32c is True
    assert response.verified_additional_authenticated_data_crc32c is True
    assert response.verified_initialization_vector_crc32c is True


@pytest.mark.asyncio
async def test_raw_decrypt_async_from_dict():
    await test_raw_decrypt_async(request_type=dict)


def test_raw_decrypt_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.RawDecryptRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.raw_decrypt), "__call__") as call:
        call.return_value = service.RawDecryptResponse()
        client.raw_decrypt(request)

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
async def test_raw_decrypt_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.RawDecryptRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.raw_decrypt), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.RawDecryptResponse()
        )
        await client.raw_decrypt(request)

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
        service.AsymmetricSignRequest,
        dict,
    ],
)
def test_asymmetric_sign(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.asymmetric_sign), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.AsymmetricSignResponse(
            signature=b"signature_blob",
            verified_digest_crc32c=True,
            name="name_value",
            verified_data_crc32c=True,
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )
        response = client.asymmetric_sign(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.AsymmetricSignRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.AsymmetricSignResponse)
    assert response.signature == b"signature_blob"
    assert response.verified_digest_crc32c is True
    assert response.name == "name_value"
    assert response.verified_data_crc32c is True
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


def test_asymmetric_sign_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.AsymmetricSignRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.asymmetric_sign), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.asymmetric_sign(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.AsymmetricSignRequest(
            name="name_value",
        )


def test_asymmetric_sign_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.asymmetric_sign in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.asymmetric_sign] = mock_rpc
        request = {}
        client.asymmetric_sign(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.asymmetric_sign(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_asymmetric_sign_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.asymmetric_sign
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.asymmetric_sign
        ] = mock_rpc

        request = {}
        await client.asymmetric_sign(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.asymmetric_sign(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_asymmetric_sign_async(
    transport: str = "grpc_asyncio", request_type=service.AsymmetricSignRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.asymmetric_sign), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.AsymmetricSignResponse(
                signature=b"signature_blob",
                verified_digest_crc32c=True,
                name="name_value",
                verified_data_crc32c=True,
                protection_level=resources.ProtectionLevel.SOFTWARE,
            )
        )
        response = await client.asymmetric_sign(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.AsymmetricSignRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.AsymmetricSignResponse)
    assert response.signature == b"signature_blob"
    assert response.verified_digest_crc32c is True
    assert response.name == "name_value"
    assert response.verified_data_crc32c is True
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


@pytest.mark.asyncio
async def test_asymmetric_sign_async_from_dict():
    await test_asymmetric_sign_async(request_type=dict)


def test_asymmetric_sign_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.AsymmetricSignRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.asymmetric_sign), "__call__") as call:
        call.return_value = service.AsymmetricSignResponse()
        client.asymmetric_sign(request)

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
async def test_asymmetric_sign_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.AsymmetricSignRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.asymmetric_sign), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.AsymmetricSignResponse()
        )
        await client.asymmetric_sign(request)

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


def test_asymmetric_sign_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.asymmetric_sign), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.AsymmetricSignResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.asymmetric_sign(
            name="name_value",
            digest=service.Digest(sha256=b"sha256_blob"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].digest
        mock_val = service.Digest(sha256=b"sha256_blob")
        assert arg == mock_val


def test_asymmetric_sign_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.asymmetric_sign(
            service.AsymmetricSignRequest(),
            name="name_value",
            digest=service.Digest(sha256=b"sha256_blob"),
        )


@pytest.mark.asyncio
async def test_asymmetric_sign_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.asymmetric_sign), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.AsymmetricSignResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.AsymmetricSignResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.asymmetric_sign(
            name="name_value",
            digest=service.Digest(sha256=b"sha256_blob"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].digest
        mock_val = service.Digest(sha256=b"sha256_blob")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_asymmetric_sign_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.asymmetric_sign(
            service.AsymmetricSignRequest(),
            name="name_value",
            digest=service.Digest(sha256=b"sha256_blob"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.AsymmetricDecryptRequest,
        dict,
    ],
)
def test_asymmetric_decrypt(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.asymmetric_decrypt), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.AsymmetricDecryptResponse(
            plaintext=b"plaintext_blob",
            verified_ciphertext_crc32c=True,
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )
        response = client.asymmetric_decrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.AsymmetricDecryptRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.AsymmetricDecryptResponse)
    assert response.plaintext == b"plaintext_blob"
    assert response.verified_ciphertext_crc32c is True
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


def test_asymmetric_decrypt_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.AsymmetricDecryptRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.asymmetric_decrypt), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.asymmetric_decrypt(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.AsymmetricDecryptRequest(
            name="name_value",
        )


def test_asymmetric_decrypt_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.asymmetric_decrypt in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.asymmetric_decrypt
        ] = mock_rpc
        request = {}
        client.asymmetric_decrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.asymmetric_decrypt(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_asymmetric_decrypt_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.asymmetric_decrypt
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.asymmetric_decrypt
        ] = mock_rpc

        request = {}
        await client.asymmetric_decrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.asymmetric_decrypt(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_asymmetric_decrypt_async(
    transport: str = "grpc_asyncio", request_type=service.AsymmetricDecryptRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.asymmetric_decrypt), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.AsymmetricDecryptResponse(
                plaintext=b"plaintext_blob",
                verified_ciphertext_crc32c=True,
                protection_level=resources.ProtectionLevel.SOFTWARE,
            )
        )
        response = await client.asymmetric_decrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.AsymmetricDecryptRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.AsymmetricDecryptResponse)
    assert response.plaintext == b"plaintext_blob"
    assert response.verified_ciphertext_crc32c is True
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


@pytest.mark.asyncio
async def test_asymmetric_decrypt_async_from_dict():
    await test_asymmetric_decrypt_async(request_type=dict)


def test_asymmetric_decrypt_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.AsymmetricDecryptRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.asymmetric_decrypt), "__call__"
    ) as call:
        call.return_value = service.AsymmetricDecryptResponse()
        client.asymmetric_decrypt(request)

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
async def test_asymmetric_decrypt_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.AsymmetricDecryptRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.asymmetric_decrypt), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.AsymmetricDecryptResponse()
        )
        await client.asymmetric_decrypt(request)

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


def test_asymmetric_decrypt_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.asymmetric_decrypt), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.AsymmetricDecryptResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.asymmetric_decrypt(
            name="name_value",
            ciphertext=b"ciphertext_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].ciphertext
        mock_val = b"ciphertext_blob"
        assert arg == mock_val


def test_asymmetric_decrypt_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.asymmetric_decrypt(
            service.AsymmetricDecryptRequest(),
            name="name_value",
            ciphertext=b"ciphertext_blob",
        )


@pytest.mark.asyncio
async def test_asymmetric_decrypt_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.asymmetric_decrypt), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.AsymmetricDecryptResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.AsymmetricDecryptResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.asymmetric_decrypt(
            name="name_value",
            ciphertext=b"ciphertext_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].ciphertext
        mock_val = b"ciphertext_blob"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_asymmetric_decrypt_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.asymmetric_decrypt(
            service.AsymmetricDecryptRequest(),
            name="name_value",
            ciphertext=b"ciphertext_blob",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.MacSignRequest,
        dict,
    ],
)
def test_mac_sign(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mac_sign), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.MacSignResponse(
            name="name_value",
            mac=b"mac_blob",
            verified_data_crc32c=True,
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )
        response = client.mac_sign(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.MacSignRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.MacSignResponse)
    assert response.name == "name_value"
    assert response.mac == b"mac_blob"
    assert response.verified_data_crc32c is True
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


def test_mac_sign_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.MacSignRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mac_sign), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.mac_sign(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.MacSignRequest(
            name="name_value",
        )


def test_mac_sign_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.mac_sign in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.mac_sign] = mock_rpc
        request = {}
        client.mac_sign(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.mac_sign(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_mac_sign_async_use_cached_wrapped_rpc(transport: str = "grpc_asyncio"):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.mac_sign
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.mac_sign
        ] = mock_rpc

        request = {}
        await client.mac_sign(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.mac_sign(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_mac_sign_async(
    transport: str = "grpc_asyncio", request_type=service.MacSignRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mac_sign), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.MacSignResponse(
                name="name_value",
                mac=b"mac_blob",
                verified_data_crc32c=True,
                protection_level=resources.ProtectionLevel.SOFTWARE,
            )
        )
        response = await client.mac_sign(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.MacSignRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.MacSignResponse)
    assert response.name == "name_value"
    assert response.mac == b"mac_blob"
    assert response.verified_data_crc32c is True
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


@pytest.mark.asyncio
async def test_mac_sign_async_from_dict():
    await test_mac_sign_async(request_type=dict)


def test_mac_sign_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.MacSignRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mac_sign), "__call__") as call:
        call.return_value = service.MacSignResponse()
        client.mac_sign(request)

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
async def test_mac_sign_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.MacSignRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mac_sign), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.MacSignResponse()
        )
        await client.mac_sign(request)

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


def test_mac_sign_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mac_sign), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.MacSignResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.mac_sign(
            name="name_value",
            data=b"data_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].data
        mock_val = b"data_blob"
        assert arg == mock_val


def test_mac_sign_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.mac_sign(
            service.MacSignRequest(),
            name="name_value",
            data=b"data_blob",
        )


@pytest.mark.asyncio
async def test_mac_sign_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mac_sign), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.MacSignResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.MacSignResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.mac_sign(
            name="name_value",
            data=b"data_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].data
        mock_val = b"data_blob"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_mac_sign_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.mac_sign(
            service.MacSignRequest(),
            name="name_value",
            data=b"data_blob",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.MacVerifyRequest,
        dict,
    ],
)
def test_mac_verify(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mac_verify), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.MacVerifyResponse(
            name="name_value",
            success=True,
            verified_data_crc32c=True,
            verified_mac_crc32c=True,
            verified_success_integrity=True,
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )
        response = client.mac_verify(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.MacVerifyRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.MacVerifyResponse)
    assert response.name == "name_value"
    assert response.success is True
    assert response.verified_data_crc32c is True
    assert response.verified_mac_crc32c is True
    assert response.verified_success_integrity is True
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


def test_mac_verify_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.MacVerifyRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mac_verify), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.mac_verify(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.MacVerifyRequest(
            name="name_value",
        )


def test_mac_verify_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.mac_verify in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.mac_verify] = mock_rpc
        request = {}
        client.mac_verify(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.mac_verify(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_mac_verify_async_use_cached_wrapped_rpc(transport: str = "grpc_asyncio"):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.mac_verify
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.mac_verify
        ] = mock_rpc

        request = {}
        await client.mac_verify(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.mac_verify(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_mac_verify_async(
    transport: str = "grpc_asyncio", request_type=service.MacVerifyRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mac_verify), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.MacVerifyResponse(
                name="name_value",
                success=True,
                verified_data_crc32c=True,
                verified_mac_crc32c=True,
                verified_success_integrity=True,
                protection_level=resources.ProtectionLevel.SOFTWARE,
            )
        )
        response = await client.mac_verify(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.MacVerifyRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.MacVerifyResponse)
    assert response.name == "name_value"
    assert response.success is True
    assert response.verified_data_crc32c is True
    assert response.verified_mac_crc32c is True
    assert response.verified_success_integrity is True
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


@pytest.mark.asyncio
async def test_mac_verify_async_from_dict():
    await test_mac_verify_async(request_type=dict)


def test_mac_verify_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.MacVerifyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mac_verify), "__call__") as call:
        call.return_value = service.MacVerifyResponse()
        client.mac_verify(request)

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
async def test_mac_verify_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.MacVerifyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mac_verify), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.MacVerifyResponse()
        )
        await client.mac_verify(request)

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


def test_mac_verify_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mac_verify), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.MacVerifyResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.mac_verify(
            name="name_value",
            data=b"data_blob",
            mac=b"mac_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].data
        mock_val = b"data_blob"
        assert arg == mock_val
        arg = args[0].mac
        mock_val = b"mac_blob"
        assert arg == mock_val


def test_mac_verify_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.mac_verify(
            service.MacVerifyRequest(),
            name="name_value",
            data=b"data_blob",
            mac=b"mac_blob",
        )


@pytest.mark.asyncio
async def test_mac_verify_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mac_verify), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.MacVerifyResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.MacVerifyResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.mac_verify(
            name="name_value",
            data=b"data_blob",
            mac=b"mac_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].data
        mock_val = b"data_blob"
        assert arg == mock_val
        arg = args[0].mac
        mock_val = b"mac_blob"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_mac_verify_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.mac_verify(
            service.MacVerifyRequest(),
            name="name_value",
            data=b"data_blob",
            mac=b"mac_blob",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.GenerateRandomBytesRequest,
        dict,
    ],
)
def test_generate_random_bytes(request_type, transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_random_bytes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.GenerateRandomBytesResponse(
            data=b"data_blob",
        )
        response = client.generate_random_bytes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.GenerateRandomBytesRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.GenerateRandomBytesResponse)
    assert response.data == b"data_blob"


def test_generate_random_bytes_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.GenerateRandomBytesRequest(
        location="location_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_random_bytes), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.generate_random_bytes(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GenerateRandomBytesRequest(
            location="location_value",
        )


def test_generate_random_bytes_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.generate_random_bytes
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.generate_random_bytes
        ] = mock_rpc
        request = {}
        client.generate_random_bytes(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.generate_random_bytes(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_generate_random_bytes_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = KeyManagementServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.generate_random_bytes
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.generate_random_bytes
        ] = mock_rpc

        request = {}
        await client.generate_random_bytes(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.generate_random_bytes(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_generate_random_bytes_async(
    transport: str = "grpc_asyncio", request_type=service.GenerateRandomBytesRequest
):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_random_bytes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.GenerateRandomBytesResponse(
                data=b"data_blob",
            )
        )
        response = await client.generate_random_bytes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.GenerateRandomBytesRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.GenerateRandomBytesResponse)
    assert response.data == b"data_blob"


@pytest.mark.asyncio
async def test_generate_random_bytes_async_from_dict():
    await test_generate_random_bytes_async(request_type=dict)


def test_generate_random_bytes_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GenerateRandomBytesRequest()

    request.location = "location_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_random_bytes), "__call__"
    ) as call:
        call.return_value = service.GenerateRandomBytesResponse()
        client.generate_random_bytes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "location=location_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_generate_random_bytes_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GenerateRandomBytesRequest()

    request.location = "location_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_random_bytes), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.GenerateRandomBytesResponse()
        )
        await client.generate_random_bytes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "location=location_value",
    ) in kw["metadata"]


def test_generate_random_bytes_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_random_bytes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.GenerateRandomBytesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.generate_random_bytes(
            location="location_value",
            length_bytes=1288,
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].location
        mock_val = "location_value"
        assert arg == mock_val
        arg = args[0].length_bytes
        mock_val = 1288
        assert arg == mock_val
        arg = args[0].protection_level
        mock_val = resources.ProtectionLevel.SOFTWARE
        assert arg == mock_val


def test_generate_random_bytes_flattened_error():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.generate_random_bytes(
            service.GenerateRandomBytesRequest(),
            location="location_value",
            length_bytes=1288,
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )


@pytest.mark.asyncio
async def test_generate_random_bytes_flattened_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_random_bytes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.GenerateRandomBytesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.GenerateRandomBytesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.generate_random_bytes(
            location="location_value",
            length_bytes=1288,
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].location
        mock_val = "location_value"
        assert arg == mock_val
        arg = args[0].length_bytes
        mock_val = 1288
        assert arg == mock_val
        arg = args[0].protection_level
        mock_val = resources.ProtectionLevel.SOFTWARE
        assert arg == mock_val


@pytest.mark.asyncio
async def test_generate_random_bytes_flattened_error_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.generate_random_bytes(
            service.GenerateRandomBytesRequest(),
            location="location_value",
            length_bytes=1288,
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )


def test_list_key_rings_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_key_rings in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_key_rings] = mock_rpc

        request = {}
        client.list_key_rings(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_key_rings(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_key_rings_rest_required_fields(request_type=service.ListKeyRingsRequest):
    transport_class = transports.KeyManagementServiceRestTransport

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
    ).list_key_rings._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_key_rings._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "order_by",
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = service.ListKeyRingsResponse()
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
            return_value = service.ListKeyRingsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_key_rings(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_key_rings_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_key_rings._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "orderBy",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


def test_list_key_rings_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.ListKeyRingsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.ListKeyRingsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_key_rings(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/keyRings" % client.transport._host,
            args[1],
        )


def test_list_key_rings_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_key_rings(
            service.ListKeyRingsRequest(),
            parent="parent_value",
        )


def test_list_key_rings_rest_pager(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            service.ListKeyRingsResponse(
                key_rings=[
                    resources.KeyRing(),
                    resources.KeyRing(),
                    resources.KeyRing(),
                ],
                next_page_token="abc",
            ),
            service.ListKeyRingsResponse(
                key_rings=[],
                next_page_token="def",
            ),
            service.ListKeyRingsResponse(
                key_rings=[
                    resources.KeyRing(),
                ],
                next_page_token="ghi",
            ),
            service.ListKeyRingsResponse(
                key_rings=[
                    resources.KeyRing(),
                    resources.KeyRing(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(service.ListKeyRingsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_key_rings(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.KeyRing) for i in results)

        pages = list(client.list_key_rings(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_crypto_keys_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_crypto_keys in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_crypto_keys
        ] = mock_rpc

        request = {}
        client.list_crypto_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_crypto_keys(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_crypto_keys_rest_required_fields(
    request_type=service.ListCryptoKeysRequest,
):
    transport_class = transports.KeyManagementServiceRestTransport

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
    ).list_crypto_keys._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_crypto_keys._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "order_by",
            "page_size",
            "page_token",
            "version_view",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = service.ListCryptoKeysResponse()
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
            return_value = service.ListCryptoKeysResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_crypto_keys(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_crypto_keys_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_crypto_keys._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "orderBy",
                "pageSize",
                "pageToken",
                "versionView",
            )
        )
        & set(("parent",))
    )


def test_list_crypto_keys_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.ListCryptoKeysResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/keyRings/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.ListCryptoKeysResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_crypto_keys(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/keyRings/*}/cryptoKeys"
            % client.transport._host,
            args[1],
        )


def test_list_crypto_keys_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_crypto_keys(
            service.ListCryptoKeysRequest(),
            parent="parent_value",
        )


def test_list_crypto_keys_rest_pager(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            service.ListCryptoKeysResponse(
                crypto_keys=[
                    resources.CryptoKey(),
                    resources.CryptoKey(),
                    resources.CryptoKey(),
                ],
                next_page_token="abc",
            ),
            service.ListCryptoKeysResponse(
                crypto_keys=[],
                next_page_token="def",
            ),
            service.ListCryptoKeysResponse(
                crypto_keys=[
                    resources.CryptoKey(),
                ],
                next_page_token="ghi",
            ),
            service.ListCryptoKeysResponse(
                crypto_keys=[
                    resources.CryptoKey(),
                    resources.CryptoKey(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(service.ListCryptoKeysResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/keyRings/sample3"
        }

        pager = client.list_crypto_keys(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.CryptoKey) for i in results)

        pages = list(client.list_crypto_keys(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_crypto_key_versions_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_crypto_key_versions
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_crypto_key_versions
        ] = mock_rpc

        request = {}
        client.list_crypto_key_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_crypto_key_versions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_crypto_key_versions_rest_required_fields(
    request_type=service.ListCryptoKeyVersionsRequest,
):
    transport_class = transports.KeyManagementServiceRestTransport

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
    ).list_crypto_key_versions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_crypto_key_versions._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "order_by",
            "page_size",
            "page_token",
            "view",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = service.ListCryptoKeyVersionsResponse()
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
            return_value = service.ListCryptoKeyVersionsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_crypto_key_versions(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_crypto_key_versions_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_crypto_key_versions._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "orderBy",
                "pageSize",
                "pageToken",
                "view",
            )
        )
        & set(("parent",))
    )


def test_list_crypto_key_versions_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.ListCryptoKeyVersionsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.ListCryptoKeyVersionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_crypto_key_versions(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/keyRings/*/cryptoKeys/*}/cryptoKeyVersions"
            % client.transport._host,
            args[1],
        )


def test_list_crypto_key_versions_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_crypto_key_versions(
            service.ListCryptoKeyVersionsRequest(),
            parent="parent_value",
        )


def test_list_crypto_key_versions_rest_pager(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[
                    resources.CryptoKeyVersion(),
                    resources.CryptoKeyVersion(),
                    resources.CryptoKeyVersion(),
                ],
                next_page_token="abc",
            ),
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[],
                next_page_token="def",
            ),
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[
                    resources.CryptoKeyVersion(),
                ],
                next_page_token="ghi",
            ),
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[
                    resources.CryptoKeyVersion(),
                    resources.CryptoKeyVersion(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            service.ListCryptoKeyVersionsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
        }

        pager = client.list_crypto_key_versions(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.CryptoKeyVersion) for i in results)

        pages = list(client.list_crypto_key_versions(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_import_jobs_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_import_jobs in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_import_jobs
        ] = mock_rpc

        request = {}
        client.list_import_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_import_jobs(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_import_jobs_rest_required_fields(
    request_type=service.ListImportJobsRequest,
):
    transport_class = transports.KeyManagementServiceRestTransport

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
    ).list_import_jobs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_import_jobs._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "order_by",
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = service.ListImportJobsResponse()
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
            return_value = service.ListImportJobsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_import_jobs(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_import_jobs_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_import_jobs._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "orderBy",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


def test_list_import_jobs_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.ListImportJobsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/keyRings/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.ListImportJobsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_import_jobs(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/keyRings/*}/importJobs"
            % client.transport._host,
            args[1],
        )


def test_list_import_jobs_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_import_jobs(
            service.ListImportJobsRequest(),
            parent="parent_value",
        )


def test_list_import_jobs_rest_pager(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            service.ListImportJobsResponse(
                import_jobs=[
                    resources.ImportJob(),
                    resources.ImportJob(),
                    resources.ImportJob(),
                ],
                next_page_token="abc",
            ),
            service.ListImportJobsResponse(
                import_jobs=[],
                next_page_token="def",
            ),
            service.ListImportJobsResponse(
                import_jobs=[
                    resources.ImportJob(),
                ],
                next_page_token="ghi",
            ),
            service.ListImportJobsResponse(
                import_jobs=[
                    resources.ImportJob(),
                    resources.ImportJob(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(service.ListImportJobsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/keyRings/sample3"
        }

        pager = client.list_import_jobs(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.ImportJob) for i in results)

        pages = list(client.list_import_jobs(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_key_ring_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_key_ring in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_key_ring] = mock_rpc

        request = {}
        client.get_key_ring(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_key_ring(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_key_ring_rest_required_fields(request_type=service.GetKeyRingRequest):
    transport_class = transports.KeyManagementServiceRestTransport

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
    ).get_key_ring._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_key_ring._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.KeyRing()
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
            return_value = resources.KeyRing.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_key_ring(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_key_ring_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_key_ring._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_get_key_ring_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.KeyRing()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/keyRings/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.KeyRing.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_key_ring(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/keyRings/*}" % client.transport._host,
            args[1],
        )


def test_get_key_ring_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_key_ring(
            service.GetKeyRingRequest(),
            name="name_value",
        )


def test_get_crypto_key_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_crypto_key in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_crypto_key] = mock_rpc

        request = {}
        client.get_crypto_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_crypto_key(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_crypto_key_rest_required_fields(request_type=service.GetCryptoKeyRequest):
    transport_class = transports.KeyManagementServiceRestTransport

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
    ).get_crypto_key._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_crypto_key._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.CryptoKey()
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
            return_value = resources.CryptoKey.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_crypto_key(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_crypto_key_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_crypto_key._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_get_crypto_key_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.CryptoKey()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.CryptoKey.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_crypto_key(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*}"
            % client.transport._host,
            args[1],
        )


def test_get_crypto_key_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_crypto_key(
            service.GetCryptoKeyRequest(),
            name="name_value",
        )


def test_get_crypto_key_version_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_crypto_key_version
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_crypto_key_version
        ] = mock_rpc

        request = {}
        client.get_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_crypto_key_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_crypto_key_version_rest_required_fields(
    request_type=service.GetCryptoKeyVersionRequest,
):
    transport_class = transports.KeyManagementServiceRestTransport

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
    ).get_crypto_key_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_crypto_key_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.CryptoKeyVersion()
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
            return_value = resources.CryptoKeyVersion.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_crypto_key_version(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_crypto_key_version_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_crypto_key_version._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_get_crypto_key_version_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.CryptoKeyVersion()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.CryptoKeyVersion.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_crypto_key_version(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*}"
            % client.transport._host,
            args[1],
        )


def test_get_crypto_key_version_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_crypto_key_version(
            service.GetCryptoKeyVersionRequest(),
            name="name_value",
        )


def test_get_public_key_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_public_key in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_public_key] = mock_rpc

        request = {}
        client.get_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_public_key(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_public_key_rest_required_fields(request_type=service.GetPublicKeyRequest):
    transport_class = transports.KeyManagementServiceRestTransport

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
    ).get_public_key._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_public_key._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.PublicKey()
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
            return_value = resources.PublicKey.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_public_key(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_public_key_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_public_key._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_get_public_key_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.PublicKey()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.PublicKey.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_public_key(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*}/publicKey"
            % client.transport._host,
            args[1],
        )


def test_get_public_key_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_public_key(
            service.GetPublicKeyRequest(),
            name="name_value",
        )


def test_get_import_job_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_import_job in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_import_job] = mock_rpc

        request = {}
        client.get_import_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_import_job(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_import_job_rest_required_fields(request_type=service.GetImportJobRequest):
    transport_class = transports.KeyManagementServiceRestTransport

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
    ).get_import_job._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_import_job._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.ImportJob()
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
            return_value = resources.ImportJob.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_import_job(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_import_job_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_import_job._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_get_import_job_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.ImportJob()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/keyRings/sample3/importJobs/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.ImportJob.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_import_job(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/keyRings/*/importJobs/*}"
            % client.transport._host,
            args[1],
        )


def test_get_import_job_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_import_job(
            service.GetImportJobRequest(),
            name="name_value",
        )


def test_create_key_ring_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_key_ring in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.create_key_ring] = mock_rpc

        request = {}
        client.create_key_ring(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_key_ring(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_key_ring_rest_required_fields(
    request_type=service.CreateKeyRingRequest,
):
    transport_class = transports.KeyManagementServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["key_ring_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped
    assert "keyRingId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_key_ring._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "keyRingId" in jsonified_request
    assert jsonified_request["keyRingId"] == request_init["key_ring_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["keyRingId"] = "key_ring_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_key_ring._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("key_ring_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "keyRingId" in jsonified_request
    assert jsonified_request["keyRingId"] == "key_ring_id_value"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.KeyRing()
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
            return_value = resources.KeyRing.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_key_ring(request)

            expected_params = [
                (
                    "keyRingId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_key_ring_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_key_ring._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("keyRingId",))
        & set(
            (
                "parent",
                "keyRingId",
                "keyRing",
            )
        )
    )


def test_create_key_ring_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.KeyRing()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            key_ring_id="key_ring_id_value",
            key_ring=resources.KeyRing(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.KeyRing.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_key_ring(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/keyRings" % client.transport._host,
            args[1],
        )


def test_create_key_ring_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_key_ring(
            service.CreateKeyRingRequest(),
            parent="parent_value",
            key_ring_id="key_ring_id_value",
            key_ring=resources.KeyRing(name="name_value"),
        )


def test_create_crypto_key_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_crypto_key in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_crypto_key
        ] = mock_rpc

        request = {}
        client.create_crypto_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_crypto_key(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_crypto_key_rest_required_fields(
    request_type=service.CreateCryptoKeyRequest,
):
    transport_class = transports.KeyManagementServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["crypto_key_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped
    assert "cryptoKeyId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_crypto_key._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "cryptoKeyId" in jsonified_request
    assert jsonified_request["cryptoKeyId"] == request_init["crypto_key_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["cryptoKeyId"] = "crypto_key_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_crypto_key._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "crypto_key_id",
            "skip_initial_version_creation",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "cryptoKeyId" in jsonified_request
    assert jsonified_request["cryptoKeyId"] == "crypto_key_id_value"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.CryptoKey()
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
            return_value = resources.CryptoKey.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_crypto_key(request)

            expected_params = [
                (
                    "cryptoKeyId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_crypto_key_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_crypto_key._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "cryptoKeyId",
                "skipInitialVersionCreation",
            )
        )
        & set(
            (
                "parent",
                "cryptoKeyId",
                "cryptoKey",
            )
        )
    )


def test_create_crypto_key_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.CryptoKey()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/keyRings/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            crypto_key_id="crypto_key_id_value",
            crypto_key=resources.CryptoKey(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.CryptoKey.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_crypto_key(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/keyRings/*}/cryptoKeys"
            % client.transport._host,
            args[1],
        )


def test_create_crypto_key_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_crypto_key(
            service.CreateCryptoKeyRequest(),
            parent="parent_value",
            crypto_key_id="crypto_key_id_value",
            crypto_key=resources.CryptoKey(name="name_value"),
        )


def test_create_crypto_key_version_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_crypto_key_version
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_crypto_key_version
        ] = mock_rpc

        request = {}
        client.create_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_crypto_key_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_crypto_key_version_rest_required_fields(
    request_type=service.CreateCryptoKeyVersionRequest,
):
    transport_class = transports.KeyManagementServiceRestTransport

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
    ).create_crypto_key_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_crypto_key_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.CryptoKeyVersion()
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
            return_value = resources.CryptoKeyVersion.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_crypto_key_version(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_crypto_key_version_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_crypto_key_version._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "cryptoKeyVersion",
            )
        )
    )


def test_create_crypto_key_version_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.CryptoKeyVersion()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            crypto_key_version=resources.CryptoKeyVersion(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.CryptoKeyVersion.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_crypto_key_version(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/keyRings/*/cryptoKeys/*}/cryptoKeyVersions"
            % client.transport._host,
            args[1],
        )


def test_create_crypto_key_version_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_crypto_key_version(
            service.CreateCryptoKeyVersionRequest(),
            parent="parent_value",
            crypto_key_version=resources.CryptoKeyVersion(name="name_value"),
        )


def test_import_crypto_key_version_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.import_crypto_key_version
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.import_crypto_key_version
        ] = mock_rpc

        request = {}
        client.import_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.import_crypto_key_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_import_crypto_key_version_rest_required_fields(
    request_type=service.ImportCryptoKeyVersionRequest,
):
    transport_class = transports.KeyManagementServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["import_job"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).import_crypto_key_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"
    jsonified_request["importJob"] = "import_job_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).import_crypto_key_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "importJob" in jsonified_request
    assert jsonified_request["importJob"] == "import_job_value"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.CryptoKeyVersion()
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
            return_value = resources.CryptoKeyVersion.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.import_crypto_key_version(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_import_crypto_key_version_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.import_crypto_key_version._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "algorithm",
                "importJob",
            )
        )
    )


def test_create_import_job_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_import_job in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_import_job
        ] = mock_rpc

        request = {}
        client.create_import_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_import_job(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_import_job_rest_required_fields(
    request_type=service.CreateImportJobRequest,
):
    transport_class = transports.KeyManagementServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["import_job_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped
    assert "importJobId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_import_job._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "importJobId" in jsonified_request
    assert jsonified_request["importJobId"] == request_init["import_job_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["importJobId"] = "import_job_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_import_job._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("import_job_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "importJobId" in jsonified_request
    assert jsonified_request["importJobId"] == "import_job_id_value"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.ImportJob()
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
            return_value = resources.ImportJob.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_import_job(request)

            expected_params = [
                (
                    "importJobId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_import_job_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_import_job._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("importJobId",))
        & set(
            (
                "parent",
                "importJobId",
                "importJob",
            )
        )
    )


def test_create_import_job_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.ImportJob()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/keyRings/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            import_job_id="import_job_id_value",
            import_job=resources.ImportJob(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.ImportJob.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_import_job(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/keyRings/*}/importJobs"
            % client.transport._host,
            args[1],
        )


def test_create_import_job_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_import_job(
            service.CreateImportJobRequest(),
            parent="parent_value",
            import_job_id="import_job_id_value",
            import_job=resources.ImportJob(name="name_value"),
        )


def test_update_crypto_key_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.update_crypto_key in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_crypto_key
        ] = mock_rpc

        request = {}
        client.update_crypto_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_crypto_key(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_update_crypto_key_rest_required_fields(
    request_type=service.UpdateCryptoKeyRequest,
):
    transport_class = transports.KeyManagementServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_crypto_key._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_crypto_key._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.CryptoKey()
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
            return_value = resources.CryptoKey.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_crypto_key(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_crypto_key_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_crypto_key._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "cryptoKey",
                "updateMask",
            )
        )
    )


def test_update_crypto_key_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.CryptoKey()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "crypto_key": {
                "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            crypto_key=resources.CryptoKey(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.CryptoKey.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_crypto_key(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{crypto_key.name=projects/*/locations/*/keyRings/*/cryptoKeys/*}"
            % client.transport._host,
            args[1],
        )


def test_update_crypto_key_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_crypto_key(
            service.UpdateCryptoKeyRequest(),
            crypto_key=resources.CryptoKey(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_crypto_key_version_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_crypto_key_version
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_crypto_key_version
        ] = mock_rpc

        request = {}
        client.update_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_crypto_key_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_update_crypto_key_version_rest_required_fields(
    request_type=service.UpdateCryptoKeyVersionRequest,
):
    transport_class = transports.KeyManagementServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_crypto_key_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_crypto_key_version._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.CryptoKeyVersion()
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
            return_value = resources.CryptoKeyVersion.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_crypto_key_version(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_crypto_key_version_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_crypto_key_version._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "cryptoKeyVersion",
                "updateMask",
            )
        )
    )


def test_update_crypto_key_version_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.CryptoKeyVersion()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "crypto_key_version": {
                "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            crypto_key_version=resources.CryptoKeyVersion(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.CryptoKeyVersion.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_crypto_key_version(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{crypto_key_version.name=projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*}"
            % client.transport._host,
            args[1],
        )


def test_update_crypto_key_version_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_crypto_key_version(
            service.UpdateCryptoKeyVersionRequest(),
            crypto_key_version=resources.CryptoKeyVersion(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_crypto_key_primary_version_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_crypto_key_primary_version
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_crypto_key_primary_version
        ] = mock_rpc

        request = {}
        client.update_crypto_key_primary_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_crypto_key_primary_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_update_crypto_key_primary_version_rest_required_fields(
    request_type=service.UpdateCryptoKeyPrimaryVersionRequest,
):
    transport_class = transports.KeyManagementServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["crypto_key_version_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_crypto_key_primary_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"
    jsonified_request["cryptoKeyVersionId"] = "crypto_key_version_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_crypto_key_primary_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"
    assert "cryptoKeyVersionId" in jsonified_request
    assert jsonified_request["cryptoKeyVersionId"] == "crypto_key_version_id_value"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.CryptoKey()
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
            return_value = resources.CryptoKey.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_crypto_key_primary_version(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_crypto_key_primary_version_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.update_crypto_key_primary_version._get_unset_required_fields({})
    )
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "cryptoKeyVersionId",
            )
        )
    )


def test_update_crypto_key_primary_version_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.CryptoKey()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            crypto_key_version_id="crypto_key_version_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.CryptoKey.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_crypto_key_primary_version(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*}:updatePrimaryVersion"
            % client.transport._host,
            args[1],
        )


def test_update_crypto_key_primary_version_rest_flattened_error(
    transport: str = "rest",
):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_crypto_key_primary_version(
            service.UpdateCryptoKeyPrimaryVersionRequest(),
            name="name_value",
            crypto_key_version_id="crypto_key_version_id_value",
        )


def test_destroy_crypto_key_version_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.destroy_crypto_key_version
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.destroy_crypto_key_version
        ] = mock_rpc

        request = {}
        client.destroy_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.destroy_crypto_key_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_destroy_crypto_key_version_rest_required_fields(
    request_type=service.DestroyCryptoKeyVersionRequest,
):
    transport_class = transports.KeyManagementServiceRestTransport

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
    ).destroy_crypto_key_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).destroy_crypto_key_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.CryptoKeyVersion()
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
            return_value = resources.CryptoKeyVersion.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.destroy_crypto_key_version(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_destroy_crypto_key_version_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.destroy_crypto_key_version._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_destroy_crypto_key_version_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.CryptoKeyVersion()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.CryptoKeyVersion.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.destroy_crypto_key_version(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*}:destroy"
            % client.transport._host,
            args[1],
        )


def test_destroy_crypto_key_version_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.destroy_crypto_key_version(
            service.DestroyCryptoKeyVersionRequest(),
            name="name_value",
        )


def test_restore_crypto_key_version_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.restore_crypto_key_version
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.restore_crypto_key_version
        ] = mock_rpc

        request = {}
        client.restore_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.restore_crypto_key_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_restore_crypto_key_version_rest_required_fields(
    request_type=service.RestoreCryptoKeyVersionRequest,
):
    transport_class = transports.KeyManagementServiceRestTransport

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
    ).restore_crypto_key_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).restore_crypto_key_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.CryptoKeyVersion()
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
            return_value = resources.CryptoKeyVersion.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.restore_crypto_key_version(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_restore_crypto_key_version_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.restore_crypto_key_version._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_restore_crypto_key_version_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.CryptoKeyVersion()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.CryptoKeyVersion.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.restore_crypto_key_version(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*}:restore"
            % client.transport._host,
            args[1],
        )


def test_restore_crypto_key_version_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.restore_crypto_key_version(
            service.RestoreCryptoKeyVersionRequest(),
            name="name_value",
        )


def test_encrypt_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.encrypt in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.encrypt] = mock_rpc

        request = {}
        client.encrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.encrypt(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_encrypt_rest_required_fields(request_type=service.EncryptRequest):
    transport_class = transports.KeyManagementServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["plaintext"] = b""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).encrypt._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"
    jsonified_request["plaintext"] = b"plaintext_blob"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).encrypt._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"
    assert "plaintext" in jsonified_request
    assert jsonified_request["plaintext"] == b"plaintext_blob"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = service.EncryptResponse()
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
            return_value = service.EncryptResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.encrypt(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_encrypt_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.encrypt._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "plaintext",
            )
        )
    )


def test_encrypt_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.EncryptResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            plaintext=b"plaintext_blob",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.EncryptResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.encrypt(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/**}:encrypt"
            % client.transport._host,
            args[1],
        )


def test_encrypt_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.encrypt(
            service.EncryptRequest(),
            name="name_value",
            plaintext=b"plaintext_blob",
        )


def test_decrypt_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.decrypt in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.decrypt] = mock_rpc

        request = {}
        client.decrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.decrypt(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_decrypt_rest_required_fields(request_type=service.DecryptRequest):
    transport_class = transports.KeyManagementServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["ciphertext"] = b""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).decrypt._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"
    jsonified_request["ciphertext"] = b"ciphertext_blob"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).decrypt._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"
    assert "ciphertext" in jsonified_request
    assert jsonified_request["ciphertext"] == b"ciphertext_blob"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = service.DecryptResponse()
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
            return_value = service.DecryptResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.decrypt(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_decrypt_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.decrypt._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "ciphertext",
            )
        )
    )


def test_decrypt_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.DecryptResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            ciphertext=b"ciphertext_blob",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.DecryptResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.decrypt(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*}:decrypt"
            % client.transport._host,
            args[1],
        )


def test_decrypt_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.decrypt(
            service.DecryptRequest(),
            name="name_value",
            ciphertext=b"ciphertext_blob",
        )


def test_raw_encrypt_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.raw_encrypt in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.raw_encrypt] = mock_rpc

        request = {}
        client.raw_encrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.raw_encrypt(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_raw_encrypt_rest_required_fields(request_type=service.RawEncryptRequest):
    transport_class = transports.KeyManagementServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["plaintext"] = b""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).raw_encrypt._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"
    jsonified_request["plaintext"] = b"plaintext_blob"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).raw_encrypt._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"
    assert "plaintext" in jsonified_request
    assert jsonified_request["plaintext"] == b"plaintext_blob"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = service.RawEncryptResponse()
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
            return_value = service.RawEncryptResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.raw_encrypt(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_raw_encrypt_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.raw_encrypt._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "plaintext",
            )
        )
    )


def test_raw_decrypt_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.raw_decrypt in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.raw_decrypt] = mock_rpc

        request = {}
        client.raw_decrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.raw_decrypt(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_raw_decrypt_rest_required_fields(request_type=service.RawDecryptRequest):
    transport_class = transports.KeyManagementServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["ciphertext"] = b""
    request_init["initialization_vector"] = b""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).raw_decrypt._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"
    jsonified_request["ciphertext"] = b"ciphertext_blob"
    jsonified_request["initializationVector"] = b"initialization_vector_blob"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).raw_decrypt._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"
    assert "ciphertext" in jsonified_request
    assert jsonified_request["ciphertext"] == b"ciphertext_blob"
    assert "initializationVector" in jsonified_request
    assert jsonified_request["initializationVector"] == b"initialization_vector_blob"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = service.RawDecryptResponse()
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
            return_value = service.RawDecryptResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.raw_decrypt(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_raw_decrypt_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.raw_decrypt._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "ciphertext",
                "initializationVector",
            )
        )
    )


def test_asymmetric_sign_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.asymmetric_sign in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.asymmetric_sign] = mock_rpc

        request = {}
        client.asymmetric_sign(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.asymmetric_sign(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_asymmetric_sign_rest_required_fields(
    request_type=service.AsymmetricSignRequest,
):
    transport_class = transports.KeyManagementServiceRestTransport

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
    ).asymmetric_sign._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).asymmetric_sign._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = service.AsymmetricSignResponse()
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
            return_value = service.AsymmetricSignResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.asymmetric_sign(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_asymmetric_sign_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.asymmetric_sign._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_asymmetric_sign_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.AsymmetricSignResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            digest=service.Digest(sha256=b"sha256_blob"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.AsymmetricSignResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.asymmetric_sign(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*}:asymmetricSign"
            % client.transport._host,
            args[1],
        )


def test_asymmetric_sign_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.asymmetric_sign(
            service.AsymmetricSignRequest(),
            name="name_value",
            digest=service.Digest(sha256=b"sha256_blob"),
        )


def test_asymmetric_decrypt_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.asymmetric_decrypt in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.asymmetric_decrypt
        ] = mock_rpc

        request = {}
        client.asymmetric_decrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.asymmetric_decrypt(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_asymmetric_decrypt_rest_required_fields(
    request_type=service.AsymmetricDecryptRequest,
):
    transport_class = transports.KeyManagementServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["ciphertext"] = b""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).asymmetric_decrypt._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"
    jsonified_request["ciphertext"] = b"ciphertext_blob"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).asymmetric_decrypt._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"
    assert "ciphertext" in jsonified_request
    assert jsonified_request["ciphertext"] == b"ciphertext_blob"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = service.AsymmetricDecryptResponse()
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
            return_value = service.AsymmetricDecryptResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.asymmetric_decrypt(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_asymmetric_decrypt_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.asymmetric_decrypt._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "ciphertext",
            )
        )
    )


def test_asymmetric_decrypt_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.AsymmetricDecryptResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            ciphertext=b"ciphertext_blob",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.AsymmetricDecryptResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.asymmetric_decrypt(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*}:asymmetricDecrypt"
            % client.transport._host,
            args[1],
        )


def test_asymmetric_decrypt_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.asymmetric_decrypt(
            service.AsymmetricDecryptRequest(),
            name="name_value",
            ciphertext=b"ciphertext_blob",
        )


def test_mac_sign_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.mac_sign in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.mac_sign] = mock_rpc

        request = {}
        client.mac_sign(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.mac_sign(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_mac_sign_rest_required_fields(request_type=service.MacSignRequest):
    transport_class = transports.KeyManagementServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["data"] = b""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).mac_sign._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"
    jsonified_request["data"] = b"data_blob"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).mac_sign._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"
    assert "data" in jsonified_request
    assert jsonified_request["data"] == b"data_blob"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = service.MacSignResponse()
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
            return_value = service.MacSignResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.mac_sign(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_mac_sign_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.mac_sign._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "data",
            )
        )
    )


def test_mac_sign_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.MacSignResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            data=b"data_blob",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.MacSignResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.mac_sign(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*}:macSign"
            % client.transport._host,
            args[1],
        )


def test_mac_sign_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.mac_sign(
            service.MacSignRequest(),
            name="name_value",
            data=b"data_blob",
        )


def test_mac_verify_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.mac_verify in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.mac_verify] = mock_rpc

        request = {}
        client.mac_verify(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.mac_verify(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_mac_verify_rest_required_fields(request_type=service.MacVerifyRequest):
    transport_class = transports.KeyManagementServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["data"] = b""
    request_init["mac"] = b""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).mac_verify._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"
    jsonified_request["data"] = b"data_blob"
    jsonified_request["mac"] = b"mac_blob"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).mac_verify._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"
    assert "data" in jsonified_request
    assert jsonified_request["data"] == b"data_blob"
    assert "mac" in jsonified_request
    assert jsonified_request["mac"] == b"mac_blob"

    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = service.MacVerifyResponse()
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
            return_value = service.MacVerifyResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.mac_verify(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_mac_verify_rest_unset_required_fields():
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.mac_verify._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "data",
                "mac",
            )
        )
    )


def test_mac_verify_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.MacVerifyResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            data=b"data_blob",
            mac=b"mac_blob",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.MacVerifyResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.mac_verify(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*}:macVerify"
            % client.transport._host,
            args[1],
        )


def test_mac_verify_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.mac_verify(
            service.MacVerifyRequest(),
            name="name_value",
            data=b"data_blob",
            mac=b"mac_blob",
        )


def test_generate_random_bytes_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.generate_random_bytes
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.generate_random_bytes
        ] = mock_rpc

        request = {}
        client.generate_random_bytes(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.generate_random_bytes(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_generate_random_bytes_rest_flattened():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.GenerateRandomBytesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"location": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            location="location_value",
            length_bytes=1288,
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.GenerateRandomBytesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.generate_random_bytes(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{location=projects/*/locations/*}:generateRandomBytes"
            % client.transport._host,
            args[1],
        )


def test_generate_random_bytes_rest_flattened_error(transport: str = "rest"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.generate_random_bytes(
            service.GenerateRandomBytesRequest(),
            location="location_value",
            length_bytes=1288,
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.KeyManagementServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.KeyManagementServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = KeyManagementServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.KeyManagementServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = KeyManagementServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = KeyManagementServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.KeyManagementServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = KeyManagementServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.KeyManagementServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = KeyManagementServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.KeyManagementServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.KeyManagementServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.KeyManagementServiceGrpcTransport,
        transports.KeyManagementServiceGrpcAsyncIOTransport,
        transports.KeyManagementServiceRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_kind_grpc():
    transport = KeyManagementServiceClient.get_transport_class("grpc")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "grpc"


def test_initialize_client_w_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_key_rings_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_key_rings), "__call__") as call:
        call.return_value = service.ListKeyRingsResponse()
        client.list_key_rings(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.ListKeyRingsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_crypto_keys_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_crypto_keys), "__call__") as call:
        call.return_value = service.ListCryptoKeysResponse()
        client.list_crypto_keys(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.ListCryptoKeysRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_crypto_key_versions_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crypto_key_versions), "__call__"
    ) as call:
        call.return_value = service.ListCryptoKeyVersionsResponse()
        client.list_crypto_key_versions(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.ListCryptoKeyVersionsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_import_jobs_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_import_jobs), "__call__") as call:
        call.return_value = service.ListImportJobsResponse()
        client.list_import_jobs(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.ListImportJobsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_key_ring_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_key_ring), "__call__") as call:
        call.return_value = resources.KeyRing()
        client.get_key_ring(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.GetKeyRingRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_crypto_key_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_crypto_key), "__call__") as call:
        call.return_value = resources.CryptoKey()
        client.get_crypto_key(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.GetCryptoKeyRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_crypto_key_version_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_crypto_key_version), "__call__"
    ) as call:
        call.return_value = resources.CryptoKeyVersion()
        client.get_crypto_key_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.GetCryptoKeyVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_public_key_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_public_key), "__call__") as call:
        call.return_value = resources.PublicKey()
        client.get_public_key(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.GetPublicKeyRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_import_job_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_import_job), "__call__") as call:
        call.return_value = resources.ImportJob()
        client.get_import_job(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.GetImportJobRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_key_ring_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_key_ring), "__call__") as call:
        call.return_value = resources.KeyRing()
        client.create_key_ring(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.CreateKeyRingRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_crypto_key_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_crypto_key), "__call__"
    ) as call:
        call.return_value = resources.CryptoKey()
        client.create_crypto_key(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.CreateCryptoKeyRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_crypto_key_version_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_crypto_key_version), "__call__"
    ) as call:
        call.return_value = resources.CryptoKeyVersion()
        client.create_crypto_key_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.CreateCryptoKeyVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_import_crypto_key_version_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.import_crypto_key_version), "__call__"
    ) as call:
        call.return_value = resources.CryptoKeyVersion()
        client.import_crypto_key_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.ImportCryptoKeyVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_import_job_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_import_job), "__call__"
    ) as call:
        call.return_value = resources.ImportJob()
        client.create_import_job(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.CreateImportJobRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_crypto_key_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key), "__call__"
    ) as call:
        call.return_value = resources.CryptoKey()
        client.update_crypto_key(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.UpdateCryptoKeyRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_crypto_key_version_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key_version), "__call__"
    ) as call:
        call.return_value = resources.CryptoKeyVersion()
        client.update_crypto_key_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.UpdateCryptoKeyVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_crypto_key_primary_version_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key_primary_version), "__call__"
    ) as call:
        call.return_value = resources.CryptoKey()
        client.update_crypto_key_primary_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.UpdateCryptoKeyPrimaryVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_destroy_crypto_key_version_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.destroy_crypto_key_version), "__call__"
    ) as call:
        call.return_value = resources.CryptoKeyVersion()
        client.destroy_crypto_key_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.DestroyCryptoKeyVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_restore_crypto_key_version_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.restore_crypto_key_version), "__call__"
    ) as call:
        call.return_value = resources.CryptoKeyVersion()
        client.restore_crypto_key_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.RestoreCryptoKeyVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_encrypt_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.encrypt), "__call__") as call:
        call.return_value = service.EncryptResponse()
        client.encrypt(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.EncryptRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_decrypt_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.decrypt), "__call__") as call:
        call.return_value = service.DecryptResponse()
        client.decrypt(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.DecryptRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_raw_encrypt_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.raw_encrypt), "__call__") as call:
        call.return_value = service.RawEncryptResponse()
        client.raw_encrypt(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.RawEncryptRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_raw_decrypt_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.raw_decrypt), "__call__") as call:
        call.return_value = service.RawDecryptResponse()
        client.raw_decrypt(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.RawDecryptRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_asymmetric_sign_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.asymmetric_sign), "__call__") as call:
        call.return_value = service.AsymmetricSignResponse()
        client.asymmetric_sign(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.AsymmetricSignRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_asymmetric_decrypt_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.asymmetric_decrypt), "__call__"
    ) as call:
        call.return_value = service.AsymmetricDecryptResponse()
        client.asymmetric_decrypt(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.AsymmetricDecryptRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_mac_sign_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.mac_sign), "__call__") as call:
        call.return_value = service.MacSignResponse()
        client.mac_sign(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.MacSignRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_mac_verify_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.mac_verify), "__call__") as call:
        call.return_value = service.MacVerifyResponse()
        client.mac_verify(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.MacVerifyRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_generate_random_bytes_empty_call_grpc():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_random_bytes), "__call__"
    ) as call:
        call.return_value = service.GenerateRandomBytesResponse()
        client.generate_random_bytes(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.GenerateRandomBytesRequest()

        assert args[0] == request_msg


def test_transport_kind_grpc_asyncio():
    transport = KeyManagementServiceAsyncClient.get_transport_class("grpc_asyncio")(
        credentials=async_anonymous_credentials()
    )
    assert transport.kind == "grpc_asyncio"


def test_initialize_client_w_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_key_rings_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_key_rings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListKeyRingsResponse(
                next_page_token="next_page_token_value",
                total_size=1086,
            )
        )
        await client.list_key_rings(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.ListKeyRingsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_crypto_keys_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_crypto_keys), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCryptoKeysResponse(
                next_page_token="next_page_token_value",
                total_size=1086,
            )
        )
        await client.list_crypto_keys(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.ListCryptoKeysRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_crypto_key_versions_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crypto_key_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCryptoKeyVersionsResponse(
                next_page_token="next_page_token_value",
                total_size=1086,
            )
        )
        await client.list_crypto_key_versions(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.ListCryptoKeyVersionsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_import_jobs_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_import_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListImportJobsResponse(
                next_page_token="next_page_token_value",
                total_size=1086,
            )
        )
        await client.list_import_jobs(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.ListImportJobsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_key_ring_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_key_ring), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.KeyRing(
                name="name_value",
            )
        )
        await client.get_key_ring(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.GetKeyRingRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_crypto_key_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_crypto_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKey(
                name="name_value",
                purpose=resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
                import_only=True,
                crypto_key_backend="crypto_key_backend_value",
            )
        )
        await client.get_crypto_key(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.GetCryptoKeyRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_crypto_key_version_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion(
                name="name_value",
                state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
                protection_level=resources.ProtectionLevel.SOFTWARE,
                algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
                import_job="import_job_value",
                import_failure_reason="import_failure_reason_value",
                generation_failure_reason="generation_failure_reason_value",
                external_destruction_failure_reason="external_destruction_failure_reason_value",
                reimport_eligible=True,
            )
        )
        await client.get_crypto_key_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.GetCryptoKeyVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_public_key_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_public_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.PublicKey(
                pem="pem_value",
                algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
                name="name_value",
                protection_level=resources.ProtectionLevel.SOFTWARE,
            )
        )
        await client.get_public_key(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.GetPublicKeyRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_import_job_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_import_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ImportJob(
                name="name_value",
                import_method=resources.ImportJob.ImportMethod.RSA_OAEP_3072_SHA1_AES_256,
                protection_level=resources.ProtectionLevel.SOFTWARE,
                state=resources.ImportJob.ImportJobState.PENDING_GENERATION,
            )
        )
        await client.get_import_job(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.GetImportJobRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_key_ring_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_key_ring), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.KeyRing(
                name="name_value",
            )
        )
        await client.create_key_ring(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.CreateKeyRingRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_crypto_key_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_crypto_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKey(
                name="name_value",
                purpose=resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
                import_only=True,
                crypto_key_backend="crypto_key_backend_value",
            )
        )
        await client.create_crypto_key(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.CreateCryptoKeyRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_crypto_key_version_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion(
                name="name_value",
                state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
                protection_level=resources.ProtectionLevel.SOFTWARE,
                algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
                import_job="import_job_value",
                import_failure_reason="import_failure_reason_value",
                generation_failure_reason="generation_failure_reason_value",
                external_destruction_failure_reason="external_destruction_failure_reason_value",
                reimport_eligible=True,
            )
        )
        await client.create_crypto_key_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.CreateCryptoKeyVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_import_crypto_key_version_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.import_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion(
                name="name_value",
                state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
                protection_level=resources.ProtectionLevel.SOFTWARE,
                algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
                import_job="import_job_value",
                import_failure_reason="import_failure_reason_value",
                generation_failure_reason="generation_failure_reason_value",
                external_destruction_failure_reason="external_destruction_failure_reason_value",
                reimport_eligible=True,
            )
        )
        await client.import_crypto_key_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.ImportCryptoKeyVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_import_job_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_import_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ImportJob(
                name="name_value",
                import_method=resources.ImportJob.ImportMethod.RSA_OAEP_3072_SHA1_AES_256,
                protection_level=resources.ProtectionLevel.SOFTWARE,
                state=resources.ImportJob.ImportJobState.PENDING_GENERATION,
            )
        )
        await client.create_import_job(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.CreateImportJobRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_update_crypto_key_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKey(
                name="name_value",
                purpose=resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
                import_only=True,
                crypto_key_backend="crypto_key_backend_value",
            )
        )
        await client.update_crypto_key(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.UpdateCryptoKeyRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_update_crypto_key_version_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion(
                name="name_value",
                state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
                protection_level=resources.ProtectionLevel.SOFTWARE,
                algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
                import_job="import_job_value",
                import_failure_reason="import_failure_reason_value",
                generation_failure_reason="generation_failure_reason_value",
                external_destruction_failure_reason="external_destruction_failure_reason_value",
                reimport_eligible=True,
            )
        )
        await client.update_crypto_key_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.UpdateCryptoKeyVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_update_crypto_key_primary_version_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key_primary_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKey(
                name="name_value",
                purpose=resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
                import_only=True,
                crypto_key_backend="crypto_key_backend_value",
            )
        )
        await client.update_crypto_key_primary_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.UpdateCryptoKeyPrimaryVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_destroy_crypto_key_version_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.destroy_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion(
                name="name_value",
                state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
                protection_level=resources.ProtectionLevel.SOFTWARE,
                algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
                import_job="import_job_value",
                import_failure_reason="import_failure_reason_value",
                generation_failure_reason="generation_failure_reason_value",
                external_destruction_failure_reason="external_destruction_failure_reason_value",
                reimport_eligible=True,
            )
        )
        await client.destroy_crypto_key_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.DestroyCryptoKeyVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_restore_crypto_key_version_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.restore_crypto_key_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CryptoKeyVersion(
                name="name_value",
                state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
                protection_level=resources.ProtectionLevel.SOFTWARE,
                algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
                import_job="import_job_value",
                import_failure_reason="import_failure_reason_value",
                generation_failure_reason="generation_failure_reason_value",
                external_destruction_failure_reason="external_destruction_failure_reason_value",
                reimport_eligible=True,
            )
        )
        await client.restore_crypto_key_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.RestoreCryptoKeyVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_encrypt_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.encrypt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.EncryptResponse(
                name="name_value",
                ciphertext=b"ciphertext_blob",
                verified_plaintext_crc32c=True,
                verified_additional_authenticated_data_crc32c=True,
                protection_level=resources.ProtectionLevel.SOFTWARE,
            )
        )
        await client.encrypt(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.EncryptRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_decrypt_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.decrypt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.DecryptResponse(
                plaintext=b"plaintext_blob",
                used_primary=True,
                protection_level=resources.ProtectionLevel.SOFTWARE,
            )
        )
        await client.decrypt(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.DecryptRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_raw_encrypt_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.raw_encrypt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.RawEncryptResponse(
                ciphertext=b"ciphertext_blob",
                initialization_vector=b"initialization_vector_blob",
                tag_length=1053,
                verified_plaintext_crc32c=True,
                verified_additional_authenticated_data_crc32c=True,
                verified_initialization_vector_crc32c=True,
                name="name_value",
                protection_level=resources.ProtectionLevel.SOFTWARE,
            )
        )
        await client.raw_encrypt(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.RawEncryptRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_raw_decrypt_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.raw_decrypt), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.RawDecryptResponse(
                plaintext=b"plaintext_blob",
                protection_level=resources.ProtectionLevel.SOFTWARE,
                verified_ciphertext_crc32c=True,
                verified_additional_authenticated_data_crc32c=True,
                verified_initialization_vector_crc32c=True,
            )
        )
        await client.raw_decrypt(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.RawDecryptRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_asymmetric_sign_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.asymmetric_sign), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.AsymmetricSignResponse(
                signature=b"signature_blob",
                verified_digest_crc32c=True,
                name="name_value",
                verified_data_crc32c=True,
                protection_level=resources.ProtectionLevel.SOFTWARE,
            )
        )
        await client.asymmetric_sign(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.AsymmetricSignRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_asymmetric_decrypt_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.asymmetric_decrypt), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.AsymmetricDecryptResponse(
                plaintext=b"plaintext_blob",
                verified_ciphertext_crc32c=True,
                protection_level=resources.ProtectionLevel.SOFTWARE,
            )
        )
        await client.asymmetric_decrypt(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.AsymmetricDecryptRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_mac_sign_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.mac_sign), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.MacSignResponse(
                name="name_value",
                mac=b"mac_blob",
                verified_data_crc32c=True,
                protection_level=resources.ProtectionLevel.SOFTWARE,
            )
        )
        await client.mac_sign(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.MacSignRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_mac_verify_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.mac_verify), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.MacVerifyResponse(
                name="name_value",
                success=True,
                verified_data_crc32c=True,
                verified_mac_crc32c=True,
                verified_success_integrity=True,
                protection_level=resources.ProtectionLevel.SOFTWARE,
            )
        )
        await client.mac_verify(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.MacVerifyRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_generate_random_bytes_empty_call_grpc_asyncio():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_random_bytes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.GenerateRandomBytesResponse(
                data=b"data_blob",
            )
        )
        await client.generate_random_bytes(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.GenerateRandomBytesRequest()

        assert args[0] == request_msg


def test_transport_kind_rest():
    transport = KeyManagementServiceClient.get_transport_class("rest")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "rest"


def test_list_key_rings_rest_bad_request(request_type=service.ListKeyRingsRequest):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_key_rings(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListKeyRingsRequest,
        dict,
    ],
)
def test_list_key_rings_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.ListKeyRingsResponse(
            next_page_token="next_page_token_value",
            total_size=1086,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = service.ListKeyRingsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_key_rings(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListKeyRingsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_key_rings_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_list_key_rings"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_list_key_rings"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.ListKeyRingsRequest.pb(service.ListKeyRingsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = service.ListKeyRingsResponse.to_json(
            service.ListKeyRingsResponse()
        )
        req.return_value.content = return_value

        request = service.ListKeyRingsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = service.ListKeyRingsResponse()

        client.list_key_rings(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_crypto_keys_rest_bad_request(request_type=service.ListCryptoKeysRequest):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/keyRings/sample3"}
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
        client.list_crypto_keys(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListCryptoKeysRequest,
        dict,
    ],
)
def test_list_crypto_keys_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/keyRings/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.ListCryptoKeysResponse(
            next_page_token="next_page_token_value",
            total_size=1086,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = service.ListCryptoKeysResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_crypto_keys(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCryptoKeysPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_crypto_keys_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_list_crypto_keys"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_list_crypto_keys"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.ListCryptoKeysRequest.pb(service.ListCryptoKeysRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = service.ListCryptoKeysResponse.to_json(
            service.ListCryptoKeysResponse()
        )
        req.return_value.content = return_value

        request = service.ListCryptoKeysRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = service.ListCryptoKeysResponse()

        client.list_crypto_keys(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_crypto_key_versions_rest_bad_request(
    request_type=service.ListCryptoKeyVersionsRequest,
):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
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
        client.list_crypto_key_versions(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListCryptoKeyVersionsRequest,
        dict,
    ],
)
def test_list_crypto_key_versions_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.ListCryptoKeyVersionsResponse(
            next_page_token="next_page_token_value",
            total_size=1086,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = service.ListCryptoKeyVersionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_crypto_key_versions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCryptoKeyVersionsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_crypto_key_versions_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_list_crypto_key_versions"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_list_crypto_key_versions"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.ListCryptoKeyVersionsRequest.pb(
            service.ListCryptoKeyVersionsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = service.ListCryptoKeyVersionsResponse.to_json(
            service.ListCryptoKeyVersionsResponse()
        )
        req.return_value.content = return_value

        request = service.ListCryptoKeyVersionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = service.ListCryptoKeyVersionsResponse()

        client.list_crypto_key_versions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_import_jobs_rest_bad_request(request_type=service.ListImportJobsRequest):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/keyRings/sample3"}
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
        client.list_import_jobs(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListImportJobsRequest,
        dict,
    ],
)
def test_list_import_jobs_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/keyRings/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.ListImportJobsResponse(
            next_page_token="next_page_token_value",
            total_size=1086,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = service.ListImportJobsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_import_jobs(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListImportJobsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_import_jobs_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_list_import_jobs"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_list_import_jobs"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.ListImportJobsRequest.pb(service.ListImportJobsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = service.ListImportJobsResponse.to_json(
            service.ListImportJobsResponse()
        )
        req.return_value.content = return_value

        request = service.ListImportJobsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = service.ListImportJobsResponse()

        client.list_import_jobs(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_key_ring_rest_bad_request(request_type=service.GetKeyRingRequest):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/keyRings/sample3"}
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
        client.get_key_ring(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetKeyRingRequest,
        dict,
    ],
)
def test_get_key_ring_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/keyRings/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.KeyRing(
            name="name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = resources.KeyRing.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_key_ring(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.KeyRing)
    assert response.name == "name_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_key_ring_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_get_key_ring"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_get_key_ring"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.GetKeyRingRequest.pb(service.GetKeyRingRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = resources.KeyRing.to_json(resources.KeyRing())
        req.return_value.content = return_value

        request = service.GetKeyRingRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.KeyRing()

        client.get_key_ring(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_crypto_key_rest_bad_request(request_type=service.GetCryptoKeyRequest):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
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
        client.get_crypto_key(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetCryptoKeyRequest,
        dict,
    ],
)
def test_get_crypto_key_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.CryptoKey(
            name="name_value",
            purpose=resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
            import_only=True,
            crypto_key_backend="crypto_key_backend_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = resources.CryptoKey.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_crypto_key(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKey)
    assert response.name == "name_value"
    assert response.purpose == resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
    assert response.import_only is True
    assert response.crypto_key_backend == "crypto_key_backend_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_crypto_key_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_get_crypto_key"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_get_crypto_key"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.GetCryptoKeyRequest.pb(service.GetCryptoKeyRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = resources.CryptoKey.to_json(resources.CryptoKey())
        req.return_value.content = return_value

        request = service.GetCryptoKeyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.CryptoKey()

        client.get_crypto_key(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_crypto_key_version_rest_bad_request(
    request_type=service.GetCryptoKeyVersionRequest,
):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
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
        client.get_crypto_key_version(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetCryptoKeyVersionRequest,
        dict,
    ],
)
def test_get_crypto_key_version_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.CryptoKeyVersion(
            name="name_value",
            state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
            import_job="import_job_value",
            import_failure_reason="import_failure_reason_value",
            generation_failure_reason="generation_failure_reason_value",
            external_destruction_failure_reason="external_destruction_failure_reason_value",
            reimport_eligible=True,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = resources.CryptoKeyVersion.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_crypto_key_version(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == "name_value"
    assert (
        response.state
        == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert (
        response.algorithm
        == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert response.import_job == "import_job_value"
    assert response.import_failure_reason == "import_failure_reason_value"
    assert response.generation_failure_reason == "generation_failure_reason_value"
    assert (
        response.external_destruction_failure_reason
        == "external_destruction_failure_reason_value"
    )
    assert response.reimport_eligible is True


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_crypto_key_version_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_get_crypto_key_version"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_get_crypto_key_version"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.GetCryptoKeyVersionRequest.pb(
            service.GetCryptoKeyVersionRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = resources.CryptoKeyVersion.to_json(resources.CryptoKeyVersion())
        req.return_value.content = return_value

        request = service.GetCryptoKeyVersionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.CryptoKeyVersion()

        client.get_crypto_key_version(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_public_key_rest_bad_request(request_type=service.GetPublicKeyRequest):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
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
        client.get_public_key(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetPublicKeyRequest,
        dict,
    ],
)
def test_get_public_key_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.PublicKey(
            pem="pem_value",
            algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
            name="name_value",
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = resources.PublicKey.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_public_key(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.PublicKey)
    assert response.pem == "pem_value"
    assert (
        response.algorithm
        == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert response.name == "name_value"
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_public_key_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_get_public_key"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_get_public_key"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.GetPublicKeyRequest.pb(service.GetPublicKeyRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = resources.PublicKey.to_json(resources.PublicKey())
        req.return_value.content = return_value

        request = service.GetPublicKeyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.PublicKey()

        client.get_public_key(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_import_job_rest_bad_request(request_type=service.GetImportJobRequest):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/importJobs/sample4"
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
        client.get_import_job(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetImportJobRequest,
        dict,
    ],
)
def test_get_import_job_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/importJobs/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.ImportJob(
            name="name_value",
            import_method=resources.ImportJob.ImportMethod.RSA_OAEP_3072_SHA1_AES_256,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            state=resources.ImportJob.ImportJobState.PENDING_GENERATION,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = resources.ImportJob.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_import_job(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.ImportJob)
    assert response.name == "name_value"
    assert (
        response.import_method
        == resources.ImportJob.ImportMethod.RSA_OAEP_3072_SHA1_AES_256
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert response.state == resources.ImportJob.ImportJobState.PENDING_GENERATION


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_import_job_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_get_import_job"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_get_import_job"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.GetImportJobRequest.pb(service.GetImportJobRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = resources.ImportJob.to_json(resources.ImportJob())
        req.return_value.content = return_value

        request = service.GetImportJobRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.ImportJob()

        client.get_import_job(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_key_ring_rest_bad_request(request_type=service.CreateKeyRingRequest):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.create_key_ring(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.CreateKeyRingRequest,
        dict,
    ],
)
def test_create_key_ring_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["key_ring"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = service.CreateKeyRingRequest.meta.fields["key_ring"]

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
    for field, value in request_init["key_ring"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["key_ring"][field])):
                    del request_init["key_ring"][field][i][subfield]
            else:
                del request_init["key_ring"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.KeyRing(
            name="name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = resources.KeyRing.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_key_ring(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.KeyRing)
    assert response.name == "name_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_key_ring_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_create_key_ring"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_create_key_ring"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.CreateKeyRingRequest.pb(service.CreateKeyRingRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = resources.KeyRing.to_json(resources.KeyRing())
        req.return_value.content = return_value

        request = service.CreateKeyRingRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.KeyRing()

        client.create_key_ring(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_crypto_key_rest_bad_request(
    request_type=service.CreateCryptoKeyRequest,
):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/keyRings/sample3"}
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
        client.create_crypto_key(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.CreateCryptoKeyRequest,
        dict,
    ],
)
def test_create_crypto_key_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/keyRings/sample3"}
    request_init["crypto_key"] = {
        "name": "name_value",
        "primary": {
            "name": "name_value",
            "state": 5,
            "protection_level": 1,
            "algorithm": 1,
            "attestation": {
                "format": 3,
                "content": b"content_blob",
                "cert_chains": {
                    "cavium_certs": ["cavium_certs_value1", "cavium_certs_value2"],
                    "google_card_certs": [
                        "google_card_certs_value1",
                        "google_card_certs_value2",
                    ],
                    "google_partition_certs": [
                        "google_partition_certs_value1",
                        "google_partition_certs_value2",
                    ],
                },
            },
            "create_time": {"seconds": 751, "nanos": 543},
            "generate_time": {},
            "destroy_time": {},
            "destroy_event_time": {},
            "import_job": "import_job_value",
            "import_time": {},
            "import_failure_reason": "import_failure_reason_value",
            "generation_failure_reason": "generation_failure_reason_value",
            "external_destruction_failure_reason": "external_destruction_failure_reason_value",
            "external_protection_level_options": {
                "external_key_uri": "external_key_uri_value",
                "ekm_connection_key_path": "ekm_connection_key_path_value",
            },
            "reimport_eligible": True,
        },
        "purpose": 1,
        "create_time": {},
        "next_rotation_time": {},
        "rotation_period": {"seconds": 751, "nanos": 543},
        "version_template": {"protection_level": 1, "algorithm": 1},
        "labels": {},
        "import_only": True,
        "destroy_scheduled_duration": {},
        "crypto_key_backend": "crypto_key_backend_value",
        "key_access_justifications_policy": {"allowed_access_reasons": [1]},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = service.CreateCryptoKeyRequest.meta.fields["crypto_key"]

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
    for field, value in request_init["crypto_key"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["crypto_key"][field])):
                    del request_init["crypto_key"][field][i][subfield]
            else:
                del request_init["crypto_key"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.CryptoKey(
            name="name_value",
            purpose=resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
            import_only=True,
            crypto_key_backend="crypto_key_backend_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = resources.CryptoKey.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_crypto_key(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKey)
    assert response.name == "name_value"
    assert response.purpose == resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
    assert response.import_only is True
    assert response.crypto_key_backend == "crypto_key_backend_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_crypto_key_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_create_crypto_key"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_create_crypto_key"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.CreateCryptoKeyRequest.pb(service.CreateCryptoKeyRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = resources.CryptoKey.to_json(resources.CryptoKey())
        req.return_value.content = return_value

        request = service.CreateCryptoKeyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.CryptoKey()

        client.create_crypto_key(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_crypto_key_version_rest_bad_request(
    request_type=service.CreateCryptoKeyVersionRequest,
):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
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
        client.create_crypto_key_version(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.CreateCryptoKeyVersionRequest,
        dict,
    ],
)
def test_create_crypto_key_version_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
    }
    request_init["crypto_key_version"] = {
        "name": "name_value",
        "state": 5,
        "protection_level": 1,
        "algorithm": 1,
        "attestation": {
            "format": 3,
            "content": b"content_blob",
            "cert_chains": {
                "cavium_certs": ["cavium_certs_value1", "cavium_certs_value2"],
                "google_card_certs": [
                    "google_card_certs_value1",
                    "google_card_certs_value2",
                ],
                "google_partition_certs": [
                    "google_partition_certs_value1",
                    "google_partition_certs_value2",
                ],
            },
        },
        "create_time": {"seconds": 751, "nanos": 543},
        "generate_time": {},
        "destroy_time": {},
        "destroy_event_time": {},
        "import_job": "import_job_value",
        "import_time": {},
        "import_failure_reason": "import_failure_reason_value",
        "generation_failure_reason": "generation_failure_reason_value",
        "external_destruction_failure_reason": "external_destruction_failure_reason_value",
        "external_protection_level_options": {
            "external_key_uri": "external_key_uri_value",
            "ekm_connection_key_path": "ekm_connection_key_path_value",
        },
        "reimport_eligible": True,
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = service.CreateCryptoKeyVersionRequest.meta.fields["crypto_key_version"]

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
    for field, value in request_init["crypto_key_version"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["crypto_key_version"][field])):
                    del request_init["crypto_key_version"][field][i][subfield]
            else:
                del request_init["crypto_key_version"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.CryptoKeyVersion(
            name="name_value",
            state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
            import_job="import_job_value",
            import_failure_reason="import_failure_reason_value",
            generation_failure_reason="generation_failure_reason_value",
            external_destruction_failure_reason="external_destruction_failure_reason_value",
            reimport_eligible=True,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = resources.CryptoKeyVersion.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_crypto_key_version(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == "name_value"
    assert (
        response.state
        == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert (
        response.algorithm
        == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert response.import_job == "import_job_value"
    assert response.import_failure_reason == "import_failure_reason_value"
    assert response.generation_failure_reason == "generation_failure_reason_value"
    assert (
        response.external_destruction_failure_reason
        == "external_destruction_failure_reason_value"
    )
    assert response.reimport_eligible is True


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_crypto_key_version_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_create_crypto_key_version"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_create_crypto_key_version"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.CreateCryptoKeyVersionRequest.pb(
            service.CreateCryptoKeyVersionRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = resources.CryptoKeyVersion.to_json(resources.CryptoKeyVersion())
        req.return_value.content = return_value

        request = service.CreateCryptoKeyVersionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.CryptoKeyVersion()

        client.create_crypto_key_version(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_import_crypto_key_version_rest_bad_request(
    request_type=service.ImportCryptoKeyVersionRequest,
):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
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
        client.import_crypto_key_version(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.ImportCryptoKeyVersionRequest,
        dict,
    ],
)
def test_import_crypto_key_version_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.CryptoKeyVersion(
            name="name_value",
            state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
            import_job="import_job_value",
            import_failure_reason="import_failure_reason_value",
            generation_failure_reason="generation_failure_reason_value",
            external_destruction_failure_reason="external_destruction_failure_reason_value",
            reimport_eligible=True,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = resources.CryptoKeyVersion.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.import_crypto_key_version(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == "name_value"
    assert (
        response.state
        == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert (
        response.algorithm
        == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert response.import_job == "import_job_value"
    assert response.import_failure_reason == "import_failure_reason_value"
    assert response.generation_failure_reason == "generation_failure_reason_value"
    assert (
        response.external_destruction_failure_reason
        == "external_destruction_failure_reason_value"
    )
    assert response.reimport_eligible is True


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_import_crypto_key_version_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_import_crypto_key_version"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_import_crypto_key_version"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.ImportCryptoKeyVersionRequest.pb(
            service.ImportCryptoKeyVersionRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = resources.CryptoKeyVersion.to_json(resources.CryptoKeyVersion())
        req.return_value.content = return_value

        request = service.ImportCryptoKeyVersionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.CryptoKeyVersion()

        client.import_crypto_key_version(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_import_job_rest_bad_request(
    request_type=service.CreateImportJobRequest,
):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/keyRings/sample3"}
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
        client.create_import_job(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.CreateImportJobRequest,
        dict,
    ],
)
def test_create_import_job_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/keyRings/sample3"}
    request_init["import_job"] = {
        "name": "name_value",
        "import_method": 1,
        "protection_level": 1,
        "create_time": {"seconds": 751, "nanos": 543},
        "generate_time": {},
        "expire_time": {},
        "expire_event_time": {},
        "state": 1,
        "public_key": {"pem": "pem_value"},
        "attestation": {
            "format": 3,
            "content": b"content_blob",
            "cert_chains": {
                "cavium_certs": ["cavium_certs_value1", "cavium_certs_value2"],
                "google_card_certs": [
                    "google_card_certs_value1",
                    "google_card_certs_value2",
                ],
                "google_partition_certs": [
                    "google_partition_certs_value1",
                    "google_partition_certs_value2",
                ],
            },
        },
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = service.CreateImportJobRequest.meta.fields["import_job"]

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
    for field, value in request_init["import_job"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["import_job"][field])):
                    del request_init["import_job"][field][i][subfield]
            else:
                del request_init["import_job"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.ImportJob(
            name="name_value",
            import_method=resources.ImportJob.ImportMethod.RSA_OAEP_3072_SHA1_AES_256,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            state=resources.ImportJob.ImportJobState.PENDING_GENERATION,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = resources.ImportJob.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_import_job(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.ImportJob)
    assert response.name == "name_value"
    assert (
        response.import_method
        == resources.ImportJob.ImportMethod.RSA_OAEP_3072_SHA1_AES_256
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert response.state == resources.ImportJob.ImportJobState.PENDING_GENERATION


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_import_job_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_create_import_job"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_create_import_job"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.CreateImportJobRequest.pb(service.CreateImportJobRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = resources.ImportJob.to_json(resources.ImportJob())
        req.return_value.content = return_value

        request = service.CreateImportJobRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.ImportJob()

        client.create_import_job(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_crypto_key_rest_bad_request(
    request_type=service.UpdateCryptoKeyRequest,
):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "crypto_key": {
            "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
        }
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
        client.update_crypto_key(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.UpdateCryptoKeyRequest,
        dict,
    ],
)
def test_update_crypto_key_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "crypto_key": {
            "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
        }
    }
    request_init["crypto_key"] = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4",
        "primary": {
            "name": "name_value",
            "state": 5,
            "protection_level": 1,
            "algorithm": 1,
            "attestation": {
                "format": 3,
                "content": b"content_blob",
                "cert_chains": {
                    "cavium_certs": ["cavium_certs_value1", "cavium_certs_value2"],
                    "google_card_certs": [
                        "google_card_certs_value1",
                        "google_card_certs_value2",
                    ],
                    "google_partition_certs": [
                        "google_partition_certs_value1",
                        "google_partition_certs_value2",
                    ],
                },
            },
            "create_time": {"seconds": 751, "nanos": 543},
            "generate_time": {},
            "destroy_time": {},
            "destroy_event_time": {},
            "import_job": "import_job_value",
            "import_time": {},
            "import_failure_reason": "import_failure_reason_value",
            "generation_failure_reason": "generation_failure_reason_value",
            "external_destruction_failure_reason": "external_destruction_failure_reason_value",
            "external_protection_level_options": {
                "external_key_uri": "external_key_uri_value",
                "ekm_connection_key_path": "ekm_connection_key_path_value",
            },
            "reimport_eligible": True,
        },
        "purpose": 1,
        "create_time": {},
        "next_rotation_time": {},
        "rotation_period": {"seconds": 751, "nanos": 543},
        "version_template": {"protection_level": 1, "algorithm": 1},
        "labels": {},
        "import_only": True,
        "destroy_scheduled_duration": {},
        "crypto_key_backend": "crypto_key_backend_value",
        "key_access_justifications_policy": {"allowed_access_reasons": [1]},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = service.UpdateCryptoKeyRequest.meta.fields["crypto_key"]

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
    for field, value in request_init["crypto_key"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["crypto_key"][field])):
                    del request_init["crypto_key"][field][i][subfield]
            else:
                del request_init["crypto_key"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.CryptoKey(
            name="name_value",
            purpose=resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
            import_only=True,
            crypto_key_backend="crypto_key_backend_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = resources.CryptoKey.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_crypto_key(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKey)
    assert response.name == "name_value"
    assert response.purpose == resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
    assert response.import_only is True
    assert response.crypto_key_backend == "crypto_key_backend_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_crypto_key_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_update_crypto_key"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_update_crypto_key"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.UpdateCryptoKeyRequest.pb(service.UpdateCryptoKeyRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = resources.CryptoKey.to_json(resources.CryptoKey())
        req.return_value.content = return_value

        request = service.UpdateCryptoKeyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.CryptoKey()

        client.update_crypto_key(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_crypto_key_version_rest_bad_request(
    request_type=service.UpdateCryptoKeyVersionRequest,
):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "crypto_key_version": {
            "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
        }
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
        client.update_crypto_key_version(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.UpdateCryptoKeyVersionRequest,
        dict,
    ],
)
def test_update_crypto_key_version_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "crypto_key_version": {
            "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
        }
    }
    request_init["crypto_key_version"] = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5",
        "state": 5,
        "protection_level": 1,
        "algorithm": 1,
        "attestation": {
            "format": 3,
            "content": b"content_blob",
            "cert_chains": {
                "cavium_certs": ["cavium_certs_value1", "cavium_certs_value2"],
                "google_card_certs": [
                    "google_card_certs_value1",
                    "google_card_certs_value2",
                ],
                "google_partition_certs": [
                    "google_partition_certs_value1",
                    "google_partition_certs_value2",
                ],
            },
        },
        "create_time": {"seconds": 751, "nanos": 543},
        "generate_time": {},
        "destroy_time": {},
        "destroy_event_time": {},
        "import_job": "import_job_value",
        "import_time": {},
        "import_failure_reason": "import_failure_reason_value",
        "generation_failure_reason": "generation_failure_reason_value",
        "external_destruction_failure_reason": "external_destruction_failure_reason_value",
        "external_protection_level_options": {
            "external_key_uri": "external_key_uri_value",
            "ekm_connection_key_path": "ekm_connection_key_path_value",
        },
        "reimport_eligible": True,
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = service.UpdateCryptoKeyVersionRequest.meta.fields["crypto_key_version"]

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
    for field, value in request_init["crypto_key_version"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["crypto_key_version"][field])):
                    del request_init["crypto_key_version"][field][i][subfield]
            else:
                del request_init["crypto_key_version"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.CryptoKeyVersion(
            name="name_value",
            state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
            import_job="import_job_value",
            import_failure_reason="import_failure_reason_value",
            generation_failure_reason="generation_failure_reason_value",
            external_destruction_failure_reason="external_destruction_failure_reason_value",
            reimport_eligible=True,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = resources.CryptoKeyVersion.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_crypto_key_version(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == "name_value"
    assert (
        response.state
        == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert (
        response.algorithm
        == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert response.import_job == "import_job_value"
    assert response.import_failure_reason == "import_failure_reason_value"
    assert response.generation_failure_reason == "generation_failure_reason_value"
    assert (
        response.external_destruction_failure_reason
        == "external_destruction_failure_reason_value"
    )
    assert response.reimport_eligible is True


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_crypto_key_version_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_update_crypto_key_version"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_update_crypto_key_version"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.UpdateCryptoKeyVersionRequest.pb(
            service.UpdateCryptoKeyVersionRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = resources.CryptoKeyVersion.to_json(resources.CryptoKeyVersion())
        req.return_value.content = return_value

        request = service.UpdateCryptoKeyVersionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.CryptoKeyVersion()

        client.update_crypto_key_version(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_crypto_key_primary_version_rest_bad_request(
    request_type=service.UpdateCryptoKeyPrimaryVersionRequest,
):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
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
        client.update_crypto_key_primary_version(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.UpdateCryptoKeyPrimaryVersionRequest,
        dict,
    ],
)
def test_update_crypto_key_primary_version_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.CryptoKey(
            name="name_value",
            purpose=resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
            import_only=True,
            crypto_key_backend="crypto_key_backend_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = resources.CryptoKey.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_crypto_key_primary_version(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKey)
    assert response.name == "name_value"
    assert response.purpose == resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
    assert response.import_only is True
    assert response.crypto_key_backend == "crypto_key_backend_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_crypto_key_primary_version_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor,
        "post_update_crypto_key_primary_version",
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor,
        "pre_update_crypto_key_primary_version",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.UpdateCryptoKeyPrimaryVersionRequest.pb(
            service.UpdateCryptoKeyPrimaryVersionRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = resources.CryptoKey.to_json(resources.CryptoKey())
        req.return_value.content = return_value

        request = service.UpdateCryptoKeyPrimaryVersionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.CryptoKey()

        client.update_crypto_key_primary_version(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_destroy_crypto_key_version_rest_bad_request(
    request_type=service.DestroyCryptoKeyVersionRequest,
):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
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
        client.destroy_crypto_key_version(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.DestroyCryptoKeyVersionRequest,
        dict,
    ],
)
def test_destroy_crypto_key_version_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.CryptoKeyVersion(
            name="name_value",
            state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
            import_job="import_job_value",
            import_failure_reason="import_failure_reason_value",
            generation_failure_reason="generation_failure_reason_value",
            external_destruction_failure_reason="external_destruction_failure_reason_value",
            reimport_eligible=True,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = resources.CryptoKeyVersion.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.destroy_crypto_key_version(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == "name_value"
    assert (
        response.state
        == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert (
        response.algorithm
        == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert response.import_job == "import_job_value"
    assert response.import_failure_reason == "import_failure_reason_value"
    assert response.generation_failure_reason == "generation_failure_reason_value"
    assert (
        response.external_destruction_failure_reason
        == "external_destruction_failure_reason_value"
    )
    assert response.reimport_eligible is True


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_destroy_crypto_key_version_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor,
        "post_destroy_crypto_key_version",
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_destroy_crypto_key_version"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.DestroyCryptoKeyVersionRequest.pb(
            service.DestroyCryptoKeyVersionRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = resources.CryptoKeyVersion.to_json(resources.CryptoKeyVersion())
        req.return_value.content = return_value

        request = service.DestroyCryptoKeyVersionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.CryptoKeyVersion()

        client.destroy_crypto_key_version(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_restore_crypto_key_version_rest_bad_request(
    request_type=service.RestoreCryptoKeyVersionRequest,
):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
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
        client.restore_crypto_key_version(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.RestoreCryptoKeyVersionRequest,
        dict,
    ],
)
def test_restore_crypto_key_version_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.CryptoKeyVersion(
            name="name_value",
            state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
            import_job="import_job_value",
            import_failure_reason="import_failure_reason_value",
            generation_failure_reason="generation_failure_reason_value",
            external_destruction_failure_reason="external_destruction_failure_reason_value",
            reimport_eligible=True,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = resources.CryptoKeyVersion.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.restore_crypto_key_version(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == "name_value"
    assert (
        response.state
        == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    )
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert (
        response.algorithm
        == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert response.import_job == "import_job_value"
    assert response.import_failure_reason == "import_failure_reason_value"
    assert response.generation_failure_reason == "generation_failure_reason_value"
    assert (
        response.external_destruction_failure_reason
        == "external_destruction_failure_reason_value"
    )
    assert response.reimport_eligible is True


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_restore_crypto_key_version_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor,
        "post_restore_crypto_key_version",
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_restore_crypto_key_version"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.RestoreCryptoKeyVersionRequest.pb(
            service.RestoreCryptoKeyVersionRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = resources.CryptoKeyVersion.to_json(resources.CryptoKeyVersion())
        req.return_value.content = return_value

        request = service.RestoreCryptoKeyVersionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.CryptoKeyVersion()

        client.restore_crypto_key_version(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_encrypt_rest_bad_request(request_type=service.EncryptRequest):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
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
        client.encrypt(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.EncryptRequest,
        dict,
    ],
)
def test_encrypt_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.EncryptResponse(
            name="name_value",
            ciphertext=b"ciphertext_blob",
            verified_plaintext_crc32c=True,
            verified_additional_authenticated_data_crc32c=True,
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = service.EncryptResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.encrypt(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.EncryptResponse)
    assert response.name == "name_value"
    assert response.ciphertext == b"ciphertext_blob"
    assert response.verified_plaintext_crc32c is True
    assert response.verified_additional_authenticated_data_crc32c is True
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_encrypt_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_encrypt"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_encrypt"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.EncryptRequest.pb(service.EncryptRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = service.EncryptResponse.to_json(service.EncryptResponse())
        req.return_value.content = return_value

        request = service.EncryptRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = service.EncryptResponse()

        client.encrypt(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_decrypt_rest_bad_request(request_type=service.DecryptRequest):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
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
        client.decrypt(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.DecryptRequest,
        dict,
    ],
)
def test_decrypt_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.DecryptResponse(
            plaintext=b"plaintext_blob",
            used_primary=True,
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = service.DecryptResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.decrypt(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.DecryptResponse)
    assert response.plaintext == b"plaintext_blob"
    assert response.used_primary is True
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_decrypt_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_decrypt"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_decrypt"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.DecryptRequest.pb(service.DecryptRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = service.DecryptResponse.to_json(service.DecryptResponse())
        req.return_value.content = return_value

        request = service.DecryptRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = service.DecryptResponse()

        client.decrypt(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_raw_encrypt_rest_bad_request(request_type=service.RawEncryptRequest):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
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
        client.raw_encrypt(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.RawEncryptRequest,
        dict,
    ],
)
def test_raw_encrypt_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.RawEncryptResponse(
            ciphertext=b"ciphertext_blob",
            initialization_vector=b"initialization_vector_blob",
            tag_length=1053,
            verified_plaintext_crc32c=True,
            verified_additional_authenticated_data_crc32c=True,
            verified_initialization_vector_crc32c=True,
            name="name_value",
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = service.RawEncryptResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.raw_encrypt(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.RawEncryptResponse)
    assert response.ciphertext == b"ciphertext_blob"
    assert response.initialization_vector == b"initialization_vector_blob"
    assert response.tag_length == 1053
    assert response.verified_plaintext_crc32c is True
    assert response.verified_additional_authenticated_data_crc32c is True
    assert response.verified_initialization_vector_crc32c is True
    assert response.name == "name_value"
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_raw_encrypt_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_raw_encrypt"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_raw_encrypt"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.RawEncryptRequest.pb(service.RawEncryptRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = service.RawEncryptResponse.to_json(service.RawEncryptResponse())
        req.return_value.content = return_value

        request = service.RawEncryptRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = service.RawEncryptResponse()

        client.raw_encrypt(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_raw_decrypt_rest_bad_request(request_type=service.RawDecryptRequest):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
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
        client.raw_decrypt(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.RawDecryptRequest,
        dict,
    ],
)
def test_raw_decrypt_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.RawDecryptResponse(
            plaintext=b"plaintext_blob",
            protection_level=resources.ProtectionLevel.SOFTWARE,
            verified_ciphertext_crc32c=True,
            verified_additional_authenticated_data_crc32c=True,
            verified_initialization_vector_crc32c=True,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = service.RawDecryptResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.raw_decrypt(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.RawDecryptResponse)
    assert response.plaintext == b"plaintext_blob"
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert response.verified_ciphertext_crc32c is True
    assert response.verified_additional_authenticated_data_crc32c is True
    assert response.verified_initialization_vector_crc32c is True


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_raw_decrypt_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_raw_decrypt"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_raw_decrypt"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.RawDecryptRequest.pb(service.RawDecryptRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = service.RawDecryptResponse.to_json(service.RawDecryptResponse())
        req.return_value.content = return_value

        request = service.RawDecryptRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = service.RawDecryptResponse()

        client.raw_decrypt(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_asymmetric_sign_rest_bad_request(request_type=service.AsymmetricSignRequest):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
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
        client.asymmetric_sign(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.AsymmetricSignRequest,
        dict,
    ],
)
def test_asymmetric_sign_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.AsymmetricSignResponse(
            signature=b"signature_blob",
            verified_digest_crc32c=True,
            name="name_value",
            verified_data_crc32c=True,
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = service.AsymmetricSignResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.asymmetric_sign(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.AsymmetricSignResponse)
    assert response.signature == b"signature_blob"
    assert response.verified_digest_crc32c is True
    assert response.name == "name_value"
    assert response.verified_data_crc32c is True
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_asymmetric_sign_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_asymmetric_sign"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_asymmetric_sign"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.AsymmetricSignRequest.pb(service.AsymmetricSignRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = service.AsymmetricSignResponse.to_json(
            service.AsymmetricSignResponse()
        )
        req.return_value.content = return_value

        request = service.AsymmetricSignRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = service.AsymmetricSignResponse()

        client.asymmetric_sign(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_asymmetric_decrypt_rest_bad_request(
    request_type=service.AsymmetricDecryptRequest,
):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
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
        client.asymmetric_decrypt(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.AsymmetricDecryptRequest,
        dict,
    ],
)
def test_asymmetric_decrypt_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.AsymmetricDecryptResponse(
            plaintext=b"plaintext_blob",
            verified_ciphertext_crc32c=True,
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = service.AsymmetricDecryptResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.asymmetric_decrypt(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.AsymmetricDecryptResponse)
    assert response.plaintext == b"plaintext_blob"
    assert response.verified_ciphertext_crc32c is True
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_asymmetric_decrypt_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_asymmetric_decrypt"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_asymmetric_decrypt"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.AsymmetricDecryptRequest.pb(
            service.AsymmetricDecryptRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = service.AsymmetricDecryptResponse.to_json(
            service.AsymmetricDecryptResponse()
        )
        req.return_value.content = return_value

        request = service.AsymmetricDecryptRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = service.AsymmetricDecryptResponse()

        client.asymmetric_decrypt(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_mac_sign_rest_bad_request(request_type=service.MacSignRequest):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
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
        client.mac_sign(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.MacSignRequest,
        dict,
    ],
)
def test_mac_sign_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.MacSignResponse(
            name="name_value",
            mac=b"mac_blob",
            verified_data_crc32c=True,
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = service.MacSignResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.mac_sign(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.MacSignResponse)
    assert response.name == "name_value"
    assert response.mac == b"mac_blob"
    assert response.verified_data_crc32c is True
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_mac_sign_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_mac_sign"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_mac_sign"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.MacSignRequest.pb(service.MacSignRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = service.MacSignResponse.to_json(service.MacSignResponse())
        req.return_value.content = return_value

        request = service.MacSignRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = service.MacSignResponse()

        client.mac_sign(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_mac_verify_rest_bad_request(request_type=service.MacVerifyRequest):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
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
        client.mac_verify(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.MacVerifyRequest,
        dict,
    ],
)
def test_mac_verify_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/keyRings/sample3/cryptoKeys/sample4/cryptoKeyVersions/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.MacVerifyResponse(
            name="name_value",
            success=True,
            verified_data_crc32c=True,
            verified_mac_crc32c=True,
            verified_success_integrity=True,
            protection_level=resources.ProtectionLevel.SOFTWARE,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = service.MacVerifyResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.mac_verify(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.MacVerifyResponse)
    assert response.name == "name_value"
    assert response.success is True
    assert response.verified_data_crc32c is True
    assert response.verified_mac_crc32c is True
    assert response.verified_success_integrity is True
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_mac_verify_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_mac_verify"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_mac_verify"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.MacVerifyRequest.pb(service.MacVerifyRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = service.MacVerifyResponse.to_json(service.MacVerifyResponse())
        req.return_value.content = return_value

        request = service.MacVerifyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = service.MacVerifyResponse()

        client.mac_verify(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_generate_random_bytes_rest_bad_request(
    request_type=service.GenerateRandomBytesRequest,
):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"location": "projects/sample1/locations/sample2"}
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
        client.generate_random_bytes(request)


@pytest.mark.parametrize(
    "request_type",
    [
        service.GenerateRandomBytesRequest,
        dict,
    ],
)
def test_generate_random_bytes_rest_call_success(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"location": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.GenerateRandomBytesResponse(
            data=b"data_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = service.GenerateRandomBytesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.generate_random_bytes(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.GenerateRandomBytesResponse)
    assert response.data == b"data_blob"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_generate_random_bytes_rest_interceptors(null_interceptor):
    transport = transports.KeyManagementServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.KeyManagementServiceRestInterceptor(),
    )
    client = KeyManagementServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "post_generate_random_bytes"
    ) as post, mock.patch.object(
        transports.KeyManagementServiceRestInterceptor, "pre_generate_random_bytes"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.GenerateRandomBytesRequest.pb(
            service.GenerateRandomBytesRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = service.GenerateRandomBytesResponse.to_json(
            service.GenerateRandomBytesResponse()
        )
        req.return_value.content = return_value

        request = service.GenerateRandomBytesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = service.GenerateRandomBytesResponse()

        client.generate_random_bytes(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_location_rest_bad_request(request_type=locations_pb2.GetLocationRequest):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_location(request)


@pytest.mark.parametrize(
    "request_type",
    [
        locations_pb2.GetLocationRequest,
        dict,
    ],
)
def test_get_location_rest(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"name": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.Location()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value

        response = client.get_location(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


def test_list_locations_rest_bad_request(
    request_type=locations_pb2.ListLocationsRequest,
):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict({"name": "projects/sample1"}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_locations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        locations_pb2.ListLocationsRequest,
        dict,
    ],
)
def test_list_locations_rest(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"name": "projects/sample1"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.ListLocationsResponse()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value

        response = client.list_locations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


def test_get_iam_policy_rest_bad_request(
    request_type=iam_policy_pb2.GetIamPolicyRequest,
):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict(
        {"resource": "projects/sample1/locations/sample2/keyRings/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_iam_policy(request)


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.GetIamPolicyRequest,
        dict,
    ],
)
def test_get_iam_policy_rest(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"resource": "projects/sample1/locations/sample2/keyRings/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = policy_pb2.Policy()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value

        response = client.get_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)


def test_set_iam_policy_rest_bad_request(
    request_type=iam_policy_pb2.SetIamPolicyRequest,
):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict(
        {"resource": "projects/sample1/locations/sample2/keyRings/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_iam_policy(request)


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.SetIamPolicyRequest,
        dict,
    ],
)
def test_set_iam_policy_rest(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"resource": "projects/sample1/locations/sample2/keyRings/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = policy_pb2.Policy()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value

        response = client.set_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)


def test_test_iam_permissions_rest_bad_request(
    request_type=iam_policy_pb2.TestIamPermissionsRequest,
):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict(
        {"resource": "projects/sample1/locations/sample2/keyRings/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.test_iam_permissions(request)


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.TestIamPermissionsRequest,
        dict,
    ],
)
def test_test_iam_permissions_rest(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"resource": "projects/sample1/locations/sample2/keyRings/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = iam_policy_pb2.TestIamPermissionsResponse()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value

        response = client.test_iam_permissions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)


def test_get_operation_rest_bad_request(
    request_type=operations_pb2.GetOperationRequest,
):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.GetOperationRequest,
        dict,
    ],
)
def test_get_operation_rest(request_type):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value

        response = client.get_operation(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_initialize_client_w_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_key_rings_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_key_rings), "__call__") as call:
        client.list_key_rings(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.ListKeyRingsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_crypto_keys_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_crypto_keys), "__call__") as call:
        client.list_crypto_keys(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.ListCryptoKeysRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_crypto_key_versions_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crypto_key_versions), "__call__"
    ) as call:
        client.list_crypto_key_versions(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.ListCryptoKeyVersionsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_import_jobs_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_import_jobs), "__call__") as call:
        client.list_import_jobs(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.ListImportJobsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_key_ring_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_key_ring), "__call__") as call:
        client.get_key_ring(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.GetKeyRingRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_crypto_key_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_crypto_key), "__call__") as call:
        client.get_crypto_key(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.GetCryptoKeyRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_crypto_key_version_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_crypto_key_version), "__call__"
    ) as call:
        client.get_crypto_key_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.GetCryptoKeyVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_public_key_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_public_key), "__call__") as call:
        client.get_public_key(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.GetPublicKeyRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_import_job_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_import_job), "__call__") as call:
        client.get_import_job(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.GetImportJobRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_key_ring_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_key_ring), "__call__") as call:
        client.create_key_ring(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.CreateKeyRingRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_crypto_key_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_crypto_key), "__call__"
    ) as call:
        client.create_crypto_key(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.CreateCryptoKeyRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_crypto_key_version_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_crypto_key_version), "__call__"
    ) as call:
        client.create_crypto_key_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.CreateCryptoKeyVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_import_crypto_key_version_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.import_crypto_key_version), "__call__"
    ) as call:
        client.import_crypto_key_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.ImportCryptoKeyVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_import_job_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_import_job), "__call__"
    ) as call:
        client.create_import_job(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.CreateImportJobRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_crypto_key_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key), "__call__"
    ) as call:
        client.update_crypto_key(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.UpdateCryptoKeyRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_crypto_key_version_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key_version), "__call__"
    ) as call:
        client.update_crypto_key_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.UpdateCryptoKeyVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_crypto_key_primary_version_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_crypto_key_primary_version), "__call__"
    ) as call:
        client.update_crypto_key_primary_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.UpdateCryptoKeyPrimaryVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_destroy_crypto_key_version_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.destroy_crypto_key_version), "__call__"
    ) as call:
        client.destroy_crypto_key_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.DestroyCryptoKeyVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_restore_crypto_key_version_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.restore_crypto_key_version), "__call__"
    ) as call:
        client.restore_crypto_key_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.RestoreCryptoKeyVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_encrypt_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.encrypt), "__call__") as call:
        client.encrypt(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.EncryptRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_decrypt_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.decrypt), "__call__") as call:
        client.decrypt(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.DecryptRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_raw_encrypt_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.raw_encrypt), "__call__") as call:
        client.raw_encrypt(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.RawEncryptRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_raw_decrypt_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.raw_decrypt), "__call__") as call:
        client.raw_decrypt(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.RawDecryptRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_asymmetric_sign_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.asymmetric_sign), "__call__") as call:
        client.asymmetric_sign(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.AsymmetricSignRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_asymmetric_decrypt_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.asymmetric_decrypt), "__call__"
    ) as call:
        client.asymmetric_decrypt(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.AsymmetricDecryptRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_mac_sign_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.mac_sign), "__call__") as call:
        client.mac_sign(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.MacSignRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_mac_verify_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.mac_verify), "__call__") as call:
        client.mac_verify(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.MacVerifyRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_generate_random_bytes_empty_call_rest():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_random_bytes), "__call__"
    ) as call:
        client.generate_random_bytes(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = service.GenerateRandomBytesRequest()

        assert args[0] == request_msg


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.KeyManagementServiceGrpcTransport,
    )


def test_key_management_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.KeyManagementServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_key_management_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.kms_v1.services.key_management_service.transports.KeyManagementServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.KeyManagementServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_key_rings",
        "list_crypto_keys",
        "list_crypto_key_versions",
        "list_import_jobs",
        "get_key_ring",
        "get_crypto_key",
        "get_crypto_key_version",
        "get_public_key",
        "get_import_job",
        "create_key_ring",
        "create_crypto_key",
        "create_crypto_key_version",
        "import_crypto_key_version",
        "create_import_job",
        "update_crypto_key",
        "update_crypto_key_version",
        "update_crypto_key_primary_version",
        "destroy_crypto_key_version",
        "restore_crypto_key_version",
        "encrypt",
        "decrypt",
        "raw_encrypt",
        "raw_decrypt",
        "asymmetric_sign",
        "asymmetric_decrypt",
        "mac_sign",
        "mac_verify",
        "generate_random_bytes",
        "set_iam_policy",
        "get_iam_policy",
        "test_iam_permissions",
        "get_location",
        "list_locations",
        "get_operation",
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


def test_key_management_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.kms_v1.services.key_management_service.transports.KeyManagementServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.KeyManagementServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloudkms",
            ),
            quota_project_id="octopus",
        )


def test_key_management_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.kms_v1.services.key_management_service.transports.KeyManagementServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.KeyManagementServiceTransport()
        adc.assert_called_once()


def test_key_management_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        KeyManagementServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloudkms",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.KeyManagementServiceGrpcTransport,
        transports.KeyManagementServiceGrpcAsyncIOTransport,
    ],
)
def test_key_management_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloudkms",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.KeyManagementServiceGrpcTransport,
        transports.KeyManagementServiceGrpcAsyncIOTransport,
        transports.KeyManagementServiceRestTransport,
    ],
)
def test_key_management_service_transport_auth_gdch_credentials(transport_class):
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
        (transports.KeyManagementServiceGrpcTransport, grpc_helpers),
        (transports.KeyManagementServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_key_management_service_transport_create_channel(transport_class, grpc_helpers):
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
            "cloudkms.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloudkms",
            ),
            scopes=["1", "2"],
            default_host="cloudkms.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.KeyManagementServiceGrpcTransport,
        transports.KeyManagementServiceGrpcAsyncIOTransport,
    ],
)
def test_key_management_service_grpc_transport_client_cert_source_for_mtls(
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


def test_key_management_service_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.KeyManagementServiceRestTransport(
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
def test_key_management_service_host_no_port(transport_name):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudkms.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "cloudkms.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://cloudkms.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_key_management_service_host_with_port(transport_name):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudkms.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "cloudkms.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://cloudkms.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_key_management_service_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = KeyManagementServiceClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = KeyManagementServiceClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.list_key_rings._session
    session2 = client2.transport.list_key_rings._session
    assert session1 != session2
    session1 = client1.transport.list_crypto_keys._session
    session2 = client2.transport.list_crypto_keys._session
    assert session1 != session2
    session1 = client1.transport.list_crypto_key_versions._session
    session2 = client2.transport.list_crypto_key_versions._session
    assert session1 != session2
    session1 = client1.transport.list_import_jobs._session
    session2 = client2.transport.list_import_jobs._session
    assert session1 != session2
    session1 = client1.transport.get_key_ring._session
    session2 = client2.transport.get_key_ring._session
    assert session1 != session2
    session1 = client1.transport.get_crypto_key._session
    session2 = client2.transport.get_crypto_key._session
    assert session1 != session2
    session1 = client1.transport.get_crypto_key_version._session
    session2 = client2.transport.get_crypto_key_version._session
    assert session1 != session2
    session1 = client1.transport.get_public_key._session
    session2 = client2.transport.get_public_key._session
    assert session1 != session2
    session1 = client1.transport.get_import_job._session
    session2 = client2.transport.get_import_job._session
    assert session1 != session2
    session1 = client1.transport.create_key_ring._session
    session2 = client2.transport.create_key_ring._session
    assert session1 != session2
    session1 = client1.transport.create_crypto_key._session
    session2 = client2.transport.create_crypto_key._session
    assert session1 != session2
    session1 = client1.transport.create_crypto_key_version._session
    session2 = client2.transport.create_crypto_key_version._session
    assert session1 != session2
    session1 = client1.transport.import_crypto_key_version._session
    session2 = client2.transport.import_crypto_key_version._session
    assert session1 != session2
    session1 = client1.transport.create_import_job._session
    session2 = client2.transport.create_import_job._session
    assert session1 != session2
    session1 = client1.transport.update_crypto_key._session
    session2 = client2.transport.update_crypto_key._session
    assert session1 != session2
    session1 = client1.transport.update_crypto_key_version._session
    session2 = client2.transport.update_crypto_key_version._session
    assert session1 != session2
    session1 = client1.transport.update_crypto_key_primary_version._session
    session2 = client2.transport.update_crypto_key_primary_version._session
    assert session1 != session2
    session1 = client1.transport.destroy_crypto_key_version._session
    session2 = client2.transport.destroy_crypto_key_version._session
    assert session1 != session2
    session1 = client1.transport.restore_crypto_key_version._session
    session2 = client2.transport.restore_crypto_key_version._session
    assert session1 != session2
    session1 = client1.transport.encrypt._session
    session2 = client2.transport.encrypt._session
    assert session1 != session2
    session1 = client1.transport.decrypt._session
    session2 = client2.transport.decrypt._session
    assert session1 != session2
    session1 = client1.transport.raw_encrypt._session
    session2 = client2.transport.raw_encrypt._session
    assert session1 != session2
    session1 = client1.transport.raw_decrypt._session
    session2 = client2.transport.raw_decrypt._session
    assert session1 != session2
    session1 = client1.transport.asymmetric_sign._session
    session2 = client2.transport.asymmetric_sign._session
    assert session1 != session2
    session1 = client1.transport.asymmetric_decrypt._session
    session2 = client2.transport.asymmetric_decrypt._session
    assert session1 != session2
    session1 = client1.transport.mac_sign._session
    session2 = client2.transport.mac_sign._session
    assert session1 != session2
    session1 = client1.transport.mac_verify._session
    session2 = client2.transport.mac_verify._session
    assert session1 != session2
    session1 = client1.transport.generate_random_bytes._session
    session2 = client2.transport.generate_random_bytes._session
    assert session1 != session2


def test_key_management_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.KeyManagementServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_key_management_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.KeyManagementServiceGrpcAsyncIOTransport(
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
        transports.KeyManagementServiceGrpcTransport,
        transports.KeyManagementServiceGrpcAsyncIOTransport,
    ],
)
def test_key_management_service_transport_channel_mtls_with_client_cert_source(
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
        transports.KeyManagementServiceGrpcTransport,
        transports.KeyManagementServiceGrpcAsyncIOTransport,
    ],
)
def test_key_management_service_transport_channel_mtls_with_adc(transport_class):
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


def test_crypto_key_path():
    project = "squid"
    location = "clam"
    key_ring = "whelk"
    crypto_key = "octopus"
    expected = "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}".format(
        project=project,
        location=location,
        key_ring=key_ring,
        crypto_key=crypto_key,
    )
    actual = KeyManagementServiceClient.crypto_key_path(
        project, location, key_ring, crypto_key
    )
    assert expected == actual


def test_parse_crypto_key_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "key_ring": "cuttlefish",
        "crypto_key": "mussel",
    }
    path = KeyManagementServiceClient.crypto_key_path(**expected)

    # Check that the path construction is reversible.
    actual = KeyManagementServiceClient.parse_crypto_key_path(path)
    assert expected == actual


def test_crypto_key_version_path():
    project = "winkle"
    location = "nautilus"
    key_ring = "scallop"
    crypto_key = "abalone"
    crypto_key_version = "squid"
    expected = "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}/cryptoKeyVersions/{crypto_key_version}".format(
        project=project,
        location=location,
        key_ring=key_ring,
        crypto_key=crypto_key,
        crypto_key_version=crypto_key_version,
    )
    actual = KeyManagementServiceClient.crypto_key_version_path(
        project, location, key_ring, crypto_key, crypto_key_version
    )
    assert expected == actual


def test_parse_crypto_key_version_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "key_ring": "octopus",
        "crypto_key": "oyster",
        "crypto_key_version": "nudibranch",
    }
    path = KeyManagementServiceClient.crypto_key_version_path(**expected)

    # Check that the path construction is reversible.
    actual = KeyManagementServiceClient.parse_crypto_key_version_path(path)
    assert expected == actual


def test_import_job_path():
    project = "cuttlefish"
    location = "mussel"
    key_ring = "winkle"
    import_job = "nautilus"
    expected = "projects/{project}/locations/{location}/keyRings/{key_ring}/importJobs/{import_job}".format(
        project=project,
        location=location,
        key_ring=key_ring,
        import_job=import_job,
    )
    actual = KeyManagementServiceClient.import_job_path(
        project, location, key_ring, import_job
    )
    assert expected == actual


def test_parse_import_job_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "key_ring": "squid",
        "import_job": "clam",
    }
    path = KeyManagementServiceClient.import_job_path(**expected)

    # Check that the path construction is reversible.
    actual = KeyManagementServiceClient.parse_import_job_path(path)
    assert expected == actual


def test_key_ring_path():
    project = "whelk"
    location = "octopus"
    key_ring = "oyster"
    expected = "projects/{project}/locations/{location}/keyRings/{key_ring}".format(
        project=project,
        location=location,
        key_ring=key_ring,
    )
    actual = KeyManagementServiceClient.key_ring_path(project, location, key_ring)
    assert expected == actual


def test_parse_key_ring_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "key_ring": "mussel",
    }
    path = KeyManagementServiceClient.key_ring_path(**expected)

    # Check that the path construction is reversible.
    actual = KeyManagementServiceClient.parse_key_ring_path(path)
    assert expected == actual


def test_public_key_path():
    project = "winkle"
    location = "nautilus"
    key_ring = "scallop"
    crypto_key = "abalone"
    crypto_key_version = "squid"
    expected = "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}/cryptoKeyVersions/{crypto_key_version}/publicKey".format(
        project=project,
        location=location,
        key_ring=key_ring,
        crypto_key=crypto_key,
        crypto_key_version=crypto_key_version,
    )
    actual = KeyManagementServiceClient.public_key_path(
        project, location, key_ring, crypto_key, crypto_key_version
    )
    assert expected == actual


def test_parse_public_key_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "key_ring": "octopus",
        "crypto_key": "oyster",
        "crypto_key_version": "nudibranch",
    }
    path = KeyManagementServiceClient.public_key_path(**expected)

    # Check that the path construction is reversible.
    actual = KeyManagementServiceClient.parse_public_key_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "cuttlefish"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = KeyManagementServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "mussel",
    }
    path = KeyManagementServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = KeyManagementServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "winkle"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = KeyManagementServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nautilus",
    }
    path = KeyManagementServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = KeyManagementServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "scallop"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = KeyManagementServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "abalone",
    }
    path = KeyManagementServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = KeyManagementServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "squid"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = KeyManagementServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "clam",
    }
    path = KeyManagementServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = KeyManagementServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "whelk"
    location = "octopus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = KeyManagementServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
    }
    path = KeyManagementServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = KeyManagementServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.KeyManagementServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = KeyManagementServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.KeyManagementServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = KeyManagementServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_get_operation(transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()
        response = client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


@pytest.mark.asyncio
async def test_get_operation_async(transport: str = "grpc_asyncio"):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_get_operation_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = operations_pb2.Operation()

        client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_operation_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_get_operation_from_dict():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()

        response = client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_operation_from_dict_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_locations(transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.ListLocationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.ListLocationsResponse()
        response = client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


@pytest.mark.asyncio
async def test_list_locations_async(transport: str = "grpc_asyncio"):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.ListLocationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        response = await client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


def test_list_locations_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.ListLocationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value = locations_pb2.ListLocationsResponse()

        client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_locations_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.ListLocationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        await client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_list_locations_from_dict():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.ListLocationsResponse()

        response = client.list_locations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_locations_from_dict_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        response = await client.list_locations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_location(transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.GetLocationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.Location()
        response = client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


@pytest.mark.asyncio
async def test_get_location_async(transport: str = "grpc_asyncio"):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.GetLocationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        response = await client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


def test_get_location_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials()
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.GetLocationRequest()
    request.name = "locations/abc"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        call.return_value = locations_pb2.Location()

        client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations/abc",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_location_field_headers_async():
    client = KeyManagementServiceAsyncClient(credentials=async_anonymous_credentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.GetLocationRequest()
    request.name = "locations/abc"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        await client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations/abc",
    ) in kw["metadata"]


def test_get_location_from_dict():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.Location()

        response = client.get_location(
            request={
                "name": "locations/abc",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_location_from_dict_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        response = await client.get_location(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_set_iam_policy(transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy(
            version=774,
            etag=b"etag_blob",
        )
        response = client.set_iam_policy(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_set_iam_policy_async(transport: str = "grpc_asyncio"):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy(
                version=774,
                etag=b"etag_blob",
            )
        )
        response = await client.set_iam_policy(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_set_iam_policy_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = policy_pb2.Policy()

        client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_iam_policy_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


def test_set_iam_policy_from_dict():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()

        response = client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy_pb2.Policy(version=774),
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_set_iam_policy_from_dict_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        response = await client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy_pb2.Policy(version=774),
            }
        )
        call.assert_called()


def test_get_iam_policy(transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy(
            version=774,
            etag=b"etag_blob",
        )

        response = client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_get_iam_policy_async(transport: str = "grpc_asyncio"):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy(
                version=774,
                etag=b"etag_blob",
            )
        )

        response = await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_get_iam_policy_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        call.return_value = policy_pb2.Policy()

        client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_iam_policy_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


def test_get_iam_policy_from_dict():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()

        response = client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options_pb2.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_iam_policy_from_dict_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        response = await client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options_pb2.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


def test_test_iam_permissions(transport: str = "grpc"):
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.TestIamPermissionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse(
            permissions=["permissions_value"],
        )

        response = client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)

    assert response.permissions == ["permissions_value"]


@pytest.mark.asyncio
async def test_test_iam_permissions_async(transport: str = "grpc_asyncio"):
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.TestIamPermissionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse(
                permissions=["permissions_value"],
            )
        )

        response = await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)

    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_field_headers():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()

        client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_test_iam_permissions_field_headers_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse()
        )

        await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


def test_test_iam_permissions_from_dict():
    client = KeyManagementServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()

        response = client.test_iam_permissions(
            request={
                "resource": "resource_value",
                "permissions": ["permissions_value"],
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_test_iam_permissions_from_dict_async():
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse()
        )

        response = await client.test_iam_permissions(
            request={
                "resource": "resource_value",
                "permissions": ["permissions_value"],
            }
        )
        call.assert_called()


def test_transport_close_grpc():
    client = KeyManagementServiceClient(
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
    client = KeyManagementServiceAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close_rest():
    client = KeyManagementServiceClient(
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
        client = KeyManagementServiceClient(
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
        (KeyManagementServiceClient, transports.KeyManagementServiceGrpcTransport),
        (
            KeyManagementServiceAsyncClient,
            transports.KeyManagementServiceGrpcAsyncIOTransport,
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
