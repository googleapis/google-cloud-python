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

from google.api_core import gapic_v1, grpc_helpers, grpc_helpers_async, path_template
from google.api_core import api_core_version, client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.location import locations_pb2
from google.iam.v1 import policy_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import json_format
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import expr_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.securitycentermanagement_v1.services.security_center_management import (
    SecurityCenterManagementAsyncClient,
    SecurityCenterManagementClient,
    pagers,
    transports,
)
from google.cloud.securitycentermanagement_v1.types import security_center_management


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

    assert SecurityCenterManagementClient._get_default_mtls_endpoint(None) is None
    assert (
        SecurityCenterManagementClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        SecurityCenterManagementClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        SecurityCenterManagementClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        SecurityCenterManagementClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        SecurityCenterManagementClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


def test__read_environment_variables():
    assert SecurityCenterManagementClient._read_environment_variables() == (
        False,
        "auto",
        None,
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert SecurityCenterManagementClient._read_environment_variables() == (
            True,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert SecurityCenterManagementClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            SecurityCenterManagementClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert SecurityCenterManagementClient._read_environment_variables() == (
            False,
            "never",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert SecurityCenterManagementClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert SecurityCenterManagementClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            SecurityCenterManagementClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert SecurityCenterManagementClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert SecurityCenterManagementClient._get_client_cert_source(None, False) is None
    assert (
        SecurityCenterManagementClient._get_client_cert_source(
            mock_provided_cert_source, False
        )
        is None
    )
    assert (
        SecurityCenterManagementClient._get_client_cert_source(
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
                SecurityCenterManagementClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                SecurityCenterManagementClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    SecurityCenterManagementClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(SecurityCenterManagementClient),
)
@mock.patch.object(
    SecurityCenterManagementAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(SecurityCenterManagementAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = SecurityCenterManagementClient._DEFAULT_UNIVERSE
    default_endpoint = SecurityCenterManagementClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = SecurityCenterManagementClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        SecurityCenterManagementClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        SecurityCenterManagementClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == SecurityCenterManagementClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        SecurityCenterManagementClient._get_api_endpoint(
            None, None, default_universe, "auto"
        )
        == default_endpoint
    )
    assert (
        SecurityCenterManagementClient._get_api_endpoint(
            None, None, default_universe, "always"
        )
        == SecurityCenterManagementClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        SecurityCenterManagementClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == SecurityCenterManagementClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        SecurityCenterManagementClient._get_api_endpoint(
            None, None, mock_universe, "never"
        )
        == mock_endpoint
    )
    assert (
        SecurityCenterManagementClient._get_api_endpoint(
            None, None, default_universe, "never"
        )
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        SecurityCenterManagementClient._get_api_endpoint(
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
        SecurityCenterManagementClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        SecurityCenterManagementClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        SecurityCenterManagementClient._get_universe_domain(None, None)
        == SecurityCenterManagementClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        SecurityCenterManagementClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            SecurityCenterManagementClient,
            transports.SecurityCenterManagementGrpcTransport,
            "grpc",
        ),
        (
            SecurityCenterManagementClient,
            transports.SecurityCenterManagementRestTransport,
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
        (SecurityCenterManagementClient, "grpc"),
        (SecurityCenterManagementAsyncClient, "grpc_asyncio"),
        (SecurityCenterManagementClient, "rest"),
    ],
)
def test_security_center_management_client_from_service_account_info(
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
            "securitycentermanagement.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://securitycentermanagement.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.SecurityCenterManagementGrpcTransport, "grpc"),
        (transports.SecurityCenterManagementGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.SecurityCenterManagementRestTransport, "rest"),
    ],
)
def test_security_center_management_client_service_account_always_use_jwt(
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
        (SecurityCenterManagementClient, "grpc"),
        (SecurityCenterManagementAsyncClient, "grpc_asyncio"),
        (SecurityCenterManagementClient, "rest"),
    ],
)
def test_security_center_management_client_from_service_account_file(
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
            "securitycentermanagement.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://securitycentermanagement.googleapis.com"
        )


def test_security_center_management_client_get_transport_class():
    transport = SecurityCenterManagementClient.get_transport_class()
    available_transports = [
        transports.SecurityCenterManagementGrpcTransport,
        transports.SecurityCenterManagementRestTransport,
    ]
    assert transport in available_transports

    transport = SecurityCenterManagementClient.get_transport_class("grpc")
    assert transport == transports.SecurityCenterManagementGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            SecurityCenterManagementClient,
            transports.SecurityCenterManagementGrpcTransport,
            "grpc",
        ),
        (
            SecurityCenterManagementAsyncClient,
            transports.SecurityCenterManagementGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            SecurityCenterManagementClient,
            transports.SecurityCenterManagementRestTransport,
            "rest",
        ),
    ],
)
@mock.patch.object(
    SecurityCenterManagementClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(SecurityCenterManagementClient),
)
@mock.patch.object(
    SecurityCenterManagementAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(SecurityCenterManagementAsyncClient),
)
def test_security_center_management_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(
        SecurityCenterManagementClient, "get_transport_class"
    ) as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(
        SecurityCenterManagementClient, "get_transport_class"
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
            SecurityCenterManagementClient,
            transports.SecurityCenterManagementGrpcTransport,
            "grpc",
            "true",
        ),
        (
            SecurityCenterManagementAsyncClient,
            transports.SecurityCenterManagementGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            SecurityCenterManagementClient,
            transports.SecurityCenterManagementGrpcTransport,
            "grpc",
            "false",
        ),
        (
            SecurityCenterManagementAsyncClient,
            transports.SecurityCenterManagementGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            SecurityCenterManagementClient,
            transports.SecurityCenterManagementRestTransport,
            "rest",
            "true",
        ),
        (
            SecurityCenterManagementClient,
            transports.SecurityCenterManagementRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    SecurityCenterManagementClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(SecurityCenterManagementClient),
)
@mock.patch.object(
    SecurityCenterManagementAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(SecurityCenterManagementAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_security_center_management_client_mtls_env_auto(
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
    [SecurityCenterManagementClient, SecurityCenterManagementAsyncClient],
)
@mock.patch.object(
    SecurityCenterManagementClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(SecurityCenterManagementClient),
)
@mock.patch.object(
    SecurityCenterManagementAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(SecurityCenterManagementAsyncClient),
)
def test_security_center_management_client_get_mtls_endpoint_and_cert_source(
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
    [SecurityCenterManagementClient, SecurityCenterManagementAsyncClient],
)
@mock.patch.object(
    SecurityCenterManagementClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(SecurityCenterManagementClient),
)
@mock.patch.object(
    SecurityCenterManagementAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(SecurityCenterManagementAsyncClient),
)
def test_security_center_management_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = SecurityCenterManagementClient._DEFAULT_UNIVERSE
    default_endpoint = SecurityCenterManagementClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = SecurityCenterManagementClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
            SecurityCenterManagementClient,
            transports.SecurityCenterManagementGrpcTransport,
            "grpc",
        ),
        (
            SecurityCenterManagementAsyncClient,
            transports.SecurityCenterManagementGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            SecurityCenterManagementClient,
            transports.SecurityCenterManagementRestTransport,
            "rest",
        ),
    ],
)
def test_security_center_management_client_client_options_scopes(
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
            SecurityCenterManagementClient,
            transports.SecurityCenterManagementGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            SecurityCenterManagementAsyncClient,
            transports.SecurityCenterManagementGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (
            SecurityCenterManagementClient,
            transports.SecurityCenterManagementRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_security_center_management_client_client_options_credentials_file(
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


def test_security_center_management_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.securitycentermanagement_v1.services.security_center_management.transports.SecurityCenterManagementGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = SecurityCenterManagementClient(
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
            SecurityCenterManagementClient,
            transports.SecurityCenterManagementGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            SecurityCenterManagementAsyncClient,
            transports.SecurityCenterManagementGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_security_center_management_client_create_channel_credentials_file(
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
            "securitycentermanagement.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="securitycentermanagement.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest,
        dict,
    ],
)
def test_list_effective_security_health_analytics_custom_modules(
    request_type, transport: str = "grpc"
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_effective_security_health_analytics_custom_modules(
            request
        )

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, pagers.ListEffectiveSecurityHealthAnalyticsCustomModulesPager
    )
    assert response.next_page_token == "next_page_token_value"


def test_list_effective_security_health_analytics_custom_modules_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_effective_security_health_analytics_custom_modules()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest()
        )


def test_list_effective_security_health_analytics_custom_modules_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_effective_security_health_analytics_custom_modules(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ] == security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_effective_security_health_analytics_custom_modules_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_effective_security_health_analytics_custom_modules
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_effective_security_health_analytics_custom_modules
        ] = mock_rpc
        request = {}
        client.list_effective_security_health_analytics_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_effective_security_health_analytics_custom_modules(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_effective_security_health_analytics_custom_modules_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = (
            await client.list_effective_security_health_analytics_custom_modules()
        )
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest()
        )


@pytest.mark.asyncio
async def test_list_effective_security_health_analytics_custom_modules_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_effective_security_health_analytics_custom_modules
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_effective_security_health_analytics_custom_modules
        ] = mock_object

        request = {}
        await client.list_effective_security_health_analytics_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_effective_security_health_analytics_custom_modules(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_effective_security_health_analytics_custom_modules_async(
    transport: str = "grpc_asyncio",
    request_type=security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest,
):
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_effective_security_health_analytics_custom_modules(
            request
        )

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, pagers.ListEffectiveSecurityHealthAnalyticsCustomModulesAsyncPager
    )
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_effective_security_health_analytics_custom_modules_async_from_dict():
    await test_list_effective_security_health_analytics_custom_modules_async(
        request_type=dict
    )


def test_list_effective_security_health_analytics_custom_modules_field_headers():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest()
    )

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        call.return_value = (
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse()
        )
        client.list_effective_security_health_analytics_custom_modules(request)

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
async def test_list_effective_security_health_analytics_custom_modules_field_headers_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest()
    )

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse()
        )
        await client.list_effective_security_health_analytics_custom_modules(request)

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


def test_list_effective_security_health_analytics_custom_modules_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_effective_security_health_analytics_custom_modules(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_effective_security_health_analytics_custom_modules_flattened_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_effective_security_health_analytics_custom_modules(
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_effective_security_health_analytics_custom_modules_flattened_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_effective_security_health_analytics_custom_modules(
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
async def test_list_effective_security_health_analytics_custom_modules_flattened_error_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_effective_security_health_analytics_custom_modules(
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest(),
            parent="parent_value",
        )


def test_list_effective_security_health_analytics_custom_modules_pager(
    transport_name: str = "grpc",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                effective_security_health_analytics_custom_modules=[
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                effective_security_health_analytics_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                effective_security_health_analytics_custom_modules=[
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                effective_security_health_analytics_custom_modules=[
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
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
        pager = client.list_effective_security_health_analytics_custom_modules(
            request={}, retry=retry, timeout=timeout
        )

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(
                i,
                security_center_management.EffectiveSecurityHealthAnalyticsCustomModule,
            )
            for i in results
        )


def test_list_effective_security_health_analytics_custom_modules_pages(
    transport_name: str = "grpc",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                effective_security_health_analytics_custom_modules=[
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                effective_security_health_analytics_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                effective_security_health_analytics_custom_modules=[
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                effective_security_health_analytics_custom_modules=[
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                ],
            ),
            RuntimeError,
        )
        pages = list(
            client.list_effective_security_health_analytics_custom_modules(
                request={}
            ).pages
        )
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_effective_security_health_analytics_custom_modules_async_pager():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_security_health_analytics_custom_modules),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                effective_security_health_analytics_custom_modules=[
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                effective_security_health_analytics_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                effective_security_health_analytics_custom_modules=[
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                effective_security_health_analytics_custom_modules=[
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                ],
            ),
            RuntimeError,
        )
        async_pager = (
            await client.list_effective_security_health_analytics_custom_modules(
                request={},
            )
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(
                i,
                security_center_management.EffectiveSecurityHealthAnalyticsCustomModule,
            )
            for i in responses
        )


@pytest.mark.asyncio
async def test_list_effective_security_health_analytics_custom_modules_async_pages():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_security_health_analytics_custom_modules),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                effective_security_health_analytics_custom_modules=[
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                effective_security_health_analytics_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                effective_security_health_analytics_custom_modules=[
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                effective_security_health_analytics_custom_modules=[
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_effective_security_health_analytics_custom_modules(
                request={}
            )
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest,
        dict,
    ],
)
def test_get_effective_security_health_analytics_custom_module(
    request_type, transport: str = "grpc"
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(
            name="name_value",
            enablement_state=security_center_management.EffectiveSecurityHealthAnalyticsCustomModule.EnablementState.ENABLED,
            display_name="display_name_value",
        )
        response = client.get_effective_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response,
        security_center_management.EffectiveSecurityHealthAnalyticsCustomModule,
    )
    assert response.name == "name_value"
    assert (
        response.enablement_state
        == security_center_management.EffectiveSecurityHealthAnalyticsCustomModule.EnablementState.ENABLED
    )
    assert response.display_name == "display_name_value"


def test_get_effective_security_health_analytics_custom_module_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_effective_security_health_analytics_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest()
        )


def test_get_effective_security_health_analytics_custom_module_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_effective_security_health_analytics_custom_module(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ] == security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest(
            name="name_value",
        )


def test_get_effective_security_health_analytics_custom_module_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_effective_security_health_analytics_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_effective_security_health_analytics_custom_module
        ] = mock_rpc
        request = {}
        client.get_effective_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_effective_security_health_analytics_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_effective_security_health_analytics_custom_module_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(
                name="name_value",
                enablement_state=security_center_management.EffectiveSecurityHealthAnalyticsCustomModule.EnablementState.ENABLED,
                display_name="display_name_value",
            )
        )
        response = await client.get_effective_security_health_analytics_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest()
        )


@pytest.mark.asyncio
async def test_get_effective_security_health_analytics_custom_module_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_effective_security_health_analytics_custom_module
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_effective_security_health_analytics_custom_module
        ] = mock_object

        request = {}
        await client.get_effective_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_effective_security_health_analytics_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_effective_security_health_analytics_custom_module_async(
    transport: str = "grpc_asyncio",
    request_type=security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest,
):
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(
                name="name_value",
                enablement_state=security_center_management.EffectiveSecurityHealthAnalyticsCustomModule.EnablementState.ENABLED,
                display_name="display_name_value",
            )
        )
        response = await client.get_effective_security_health_analytics_custom_module(
            request
        )

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response,
        security_center_management.EffectiveSecurityHealthAnalyticsCustomModule,
    )
    assert response.name == "name_value"
    assert (
        response.enablement_state
        == security_center_management.EffectiveSecurityHealthAnalyticsCustomModule.EnablementState.ENABLED
    )
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_get_effective_security_health_analytics_custom_module_async_from_dict():
    await test_get_effective_security_health_analytics_custom_module_async(
        request_type=dict
    )


def test_get_effective_security_health_analytics_custom_module_field_headers():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest()
    )

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        call.return_value = (
            security_center_management.EffectiveSecurityHealthAnalyticsCustomModule()
        )
        client.get_effective_security_health_analytics_custom_module(request)

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
async def test_get_effective_security_health_analytics_custom_module_field_headers_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest()
    )

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.EffectiveSecurityHealthAnalyticsCustomModule()
        )
        await client.get_effective_security_health_analytics_custom_module(request)

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


def test_get_effective_security_health_analytics_custom_module_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.EffectiveSecurityHealthAnalyticsCustomModule()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_effective_security_health_analytics_custom_module(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_effective_security_health_analytics_custom_module_flattened_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_effective_security_health_analytics_custom_module(
            security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_effective_security_health_analytics_custom_module_flattened_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.EffectiveSecurityHealthAnalyticsCustomModule()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.EffectiveSecurityHealthAnalyticsCustomModule()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_effective_security_health_analytics_custom_module(
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
async def test_get_effective_security_health_analytics_custom_module_flattened_error_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_effective_security_health_analytics_custom_module(
            security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest,
        dict,
    ],
)
def test_list_security_health_analytics_custom_modules(
    request_type, transport: str = "grpc"
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_health_analytics_custom_modules), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = client.list_security_health_analytics_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSecurityHealthAnalyticsCustomModulesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_security_health_analytics_custom_modules_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_health_analytics_custom_modules), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_security_health_analytics_custom_modules()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest()
        )


def test_list_security_health_analytics_custom_modules_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = (
        security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest(
            parent="parent_value",
            page_token="page_token_value",
        )
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_health_analytics_custom_modules), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_security_health_analytics_custom_modules(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ] == security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_security_health_analytics_custom_modules_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_security_health_analytics_custom_modules
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_security_health_analytics_custom_modules
        ] = mock_rpc
        request = {}
        client.list_security_health_analytics_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_security_health_analytics_custom_modules(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_security_health_analytics_custom_modules_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_health_analytics_custom_modules), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_security_health_analytics_custom_modules()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest()
        )


@pytest.mark.asyncio
async def test_list_security_health_analytics_custom_modules_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_security_health_analytics_custom_modules
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_security_health_analytics_custom_modules
        ] = mock_object

        request = {}
        await client.list_security_health_analytics_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_security_health_analytics_custom_modules(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_security_health_analytics_custom_modules_async(
    transport: str = "grpc_asyncio",
    request_type=security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest,
):
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_health_analytics_custom_modules), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_security_health_analytics_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, pagers.ListSecurityHealthAnalyticsCustomModulesAsyncPager
    )
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_security_health_analytics_custom_modules_async_from_dict():
    await test_list_security_health_analytics_custom_modules_async(request_type=dict)


def test_list_security_health_analytics_custom_modules_field_headers():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest()
    )

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_health_analytics_custom_modules), "__call__"
    ) as call:
        call.return_value = (
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse()
        )
        client.list_security_health_analytics_custom_modules(request)

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
async def test_list_security_health_analytics_custom_modules_field_headers_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest()
    )

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_health_analytics_custom_modules), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse()
        )
        await client.list_security_health_analytics_custom_modules(request)

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


def test_list_security_health_analytics_custom_modules_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_health_analytics_custom_modules), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_security_health_analytics_custom_modules(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_security_health_analytics_custom_modules_flattened_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_security_health_analytics_custom_modules(
            security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_security_health_analytics_custom_modules_flattened_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_health_analytics_custom_modules), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_security_health_analytics_custom_modules(
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
async def test_list_security_health_analytics_custom_modules_flattened_error_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_security_health_analytics_custom_modules(
            security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest(),
            parent="parent_value",
        )


def test_list_security_health_analytics_custom_modules_pager(
    transport_name: str = "grpc",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_health_analytics_custom_modules), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
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
        pager = client.list_security_health_analytics_custom_modules(
            request={}, retry=retry, timeout=timeout
        )

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(
                i, security_center_management.SecurityHealthAnalyticsCustomModule
            )
            for i in results
        )


def test_list_security_health_analytics_custom_modules_pages(
    transport_name: str = "grpc",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_health_analytics_custom_modules), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
            ),
            RuntimeError,
        )
        pages = list(
            client.list_security_health_analytics_custom_modules(request={}).pages
        )
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_security_health_analytics_custom_modules_async_pager():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_health_analytics_custom_modules),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_security_health_analytics_custom_modules(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(
                i, security_center_management.SecurityHealthAnalyticsCustomModule
            )
            for i in responses
        )


@pytest.mark.asyncio
async def test_list_security_health_analytics_custom_modules_async_pages():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_health_analytics_custom_modules),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_security_health_analytics_custom_modules(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest,
        dict,
    ],
)
def test_list_descendant_security_health_analytics_custom_modules(
    request_type, transport: str = "grpc"
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_descendant_security_health_analytics_custom_modules(
            request
        )

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, pagers.ListDescendantSecurityHealthAnalyticsCustomModulesPager
    )
    assert response.next_page_token == "next_page_token_value"


def test_list_descendant_security_health_analytics_custom_modules_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_descendant_security_health_analytics_custom_modules()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest()
        )


def test_list_descendant_security_health_analytics_custom_modules_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_descendant_security_health_analytics_custom_modules(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ] == security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_descendant_security_health_analytics_custom_modules_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_descendant_security_health_analytics_custom_modules
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_descendant_security_health_analytics_custom_modules
        ] = mock_rpc
        request = {}
        client.list_descendant_security_health_analytics_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_descendant_security_health_analytics_custom_modules(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_descendant_security_health_analytics_custom_modules_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = (
            await client.list_descendant_security_health_analytics_custom_modules()
        )
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest()
        )


@pytest.mark.asyncio
async def test_list_descendant_security_health_analytics_custom_modules_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_descendant_security_health_analytics_custom_modules
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_descendant_security_health_analytics_custom_modules
        ] = mock_object

        request = {}
        await client.list_descendant_security_health_analytics_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_descendant_security_health_analytics_custom_modules(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_descendant_security_health_analytics_custom_modules_async(
    transport: str = "grpc_asyncio",
    request_type=security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest,
):
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = (
            await client.list_descendant_security_health_analytics_custom_modules(
                request
            )
        )

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, pagers.ListDescendantSecurityHealthAnalyticsCustomModulesAsyncPager
    )
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_descendant_security_health_analytics_custom_modules_async_from_dict():
    await test_list_descendant_security_health_analytics_custom_modules_async(
        request_type=dict
    )


def test_list_descendant_security_health_analytics_custom_modules_field_headers():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest()
    )

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        call.return_value = (
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse()
        )
        client.list_descendant_security_health_analytics_custom_modules(request)

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
async def test_list_descendant_security_health_analytics_custom_modules_field_headers_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest()
    )

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse()
        )
        await client.list_descendant_security_health_analytics_custom_modules(request)

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


def test_list_descendant_security_health_analytics_custom_modules_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_descendant_security_health_analytics_custom_modules(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_descendant_security_health_analytics_custom_modules_flattened_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_descendant_security_health_analytics_custom_modules(
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_descendant_security_health_analytics_custom_modules_flattened_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = (
            await client.list_descendant_security_health_analytics_custom_modules(
                parent="parent_value",
            )
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_descendant_security_health_analytics_custom_modules_flattened_error_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_descendant_security_health_analytics_custom_modules(
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest(),
            parent="parent_value",
        )


def test_list_descendant_security_health_analytics_custom_modules_pager(
    transport_name: str = "grpc",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
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
        pager = client.list_descendant_security_health_analytics_custom_modules(
            request={}, retry=retry, timeout=timeout
        )

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(
                i, security_center_management.SecurityHealthAnalyticsCustomModule
            )
            for i in results
        )


def test_list_descendant_security_health_analytics_custom_modules_pages(
    transport_name: str = "grpc",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_security_health_analytics_custom_modules),
        "__call__",
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
            ),
            RuntimeError,
        )
        pages = list(
            client.list_descendant_security_health_analytics_custom_modules(
                request={}
            ).pages
        )
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_descendant_security_health_analytics_custom_modules_async_pager():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_security_health_analytics_custom_modules),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
            ),
            RuntimeError,
        )
        async_pager = (
            await client.list_descendant_security_health_analytics_custom_modules(
                request={},
            )
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(
                i, security_center_management.SecurityHealthAnalyticsCustomModule
            )
            for i in responses
        )


@pytest.mark.asyncio
async def test_list_descendant_security_health_analytics_custom_modules_async_pages():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_security_health_analytics_custom_modules),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_descendant_security_health_analytics_custom_modules(
                request={}
            )
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest,
        dict,
    ],
)
def test_get_security_health_analytics_custom_module(
    request_type, transport: str = "grpc"
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_security_health_analytics_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = security_center_management.SecurityHealthAnalyticsCustomModule(
            name="name_value",
            display_name="display_name_value",
            enablement_state=security_center_management.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED,
            last_editor="last_editor_value",
            ancestor_module="ancestor_module_value",
        )
        response = client.get_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, security_center_management.SecurityHealthAnalyticsCustomModule
    )
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert (
        response.enablement_state
        == security_center_management.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED
    )
    assert response.last_editor == "last_editor_value"
    assert response.ancestor_module == "ancestor_module_value"


def test_get_security_health_analytics_custom_module_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_security_health_analytics_custom_module), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_security_health_analytics_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest()
        )


def test_get_security_health_analytics_custom_module_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_security_health_analytics_custom_module), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_security_health_analytics_custom_module(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ] == security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest(
            name="name_value",
        )


def test_get_security_health_analytics_custom_module_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_security_health_analytics_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_security_health_analytics_custom_module
        ] = mock_rpc
        request = {}
        client.get_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_security_health_analytics_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_security_health_analytics_custom_module_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_security_health_analytics_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SecurityHealthAnalyticsCustomModule(
                name="name_value",
                display_name="display_name_value",
                enablement_state=security_center_management.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED,
                last_editor="last_editor_value",
                ancestor_module="ancestor_module_value",
            )
        )
        response = await client.get_security_health_analytics_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest()
        )


@pytest.mark.asyncio
async def test_get_security_health_analytics_custom_module_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_security_health_analytics_custom_module
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_security_health_analytics_custom_module
        ] = mock_object

        request = {}
        await client.get_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_security_health_analytics_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_security_health_analytics_custom_module_async(
    transport: str = "grpc_asyncio",
    request_type=security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest,
):
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_security_health_analytics_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SecurityHealthAnalyticsCustomModule(
                name="name_value",
                display_name="display_name_value",
                enablement_state=security_center_management.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED,
                last_editor="last_editor_value",
                ancestor_module="ancestor_module_value",
            )
        )
        response = await client.get_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, security_center_management.SecurityHealthAnalyticsCustomModule
    )
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert (
        response.enablement_state
        == security_center_management.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED
    )
    assert response.last_editor == "last_editor_value"
    assert response.ancestor_module == "ancestor_module_value"


@pytest.mark.asyncio
async def test_get_security_health_analytics_custom_module_async_from_dict():
    await test_get_security_health_analytics_custom_module_async(request_type=dict)


def test_get_security_health_analytics_custom_module_field_headers():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_security_health_analytics_custom_module), "__call__"
    ) as call:
        call.return_value = (
            security_center_management.SecurityHealthAnalyticsCustomModule()
        )
        client.get_security_health_analytics_custom_module(request)

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
async def test_get_security_health_analytics_custom_module_field_headers_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_security_health_analytics_custom_module), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SecurityHealthAnalyticsCustomModule()
        )
        await client.get_security_health_analytics_custom_module(request)

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


def test_get_security_health_analytics_custom_module_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_security_health_analytics_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.SecurityHealthAnalyticsCustomModule()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_security_health_analytics_custom_module(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_security_health_analytics_custom_module_flattened_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_security_health_analytics_custom_module(
            security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_security_health_analytics_custom_module_flattened_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_security_health_analytics_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.SecurityHealthAnalyticsCustomModule()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SecurityHealthAnalyticsCustomModule()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_security_health_analytics_custom_module(
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
async def test_get_security_health_analytics_custom_module_flattened_error_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_security_health_analytics_custom_module(
            security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest,
        dict,
    ],
)
def test_create_security_health_analytics_custom_module(
    request_type, transport: str = "grpc"
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = security_center_management.SecurityHealthAnalyticsCustomModule(
            name="name_value",
            display_name="display_name_value",
            enablement_state=security_center_management.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED,
            last_editor="last_editor_value",
            ancestor_module="ancestor_module_value",
        )
        response = client.create_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, security_center_management.SecurityHealthAnalyticsCustomModule
    )
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert (
        response.enablement_state
        == security_center_management.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED
    )
    assert response.last_editor == "last_editor_value"
    assert response.ancestor_module == "ancestor_module_value"


def test_create_security_health_analytics_custom_module_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_security_health_analytics_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest()
        )


def test_create_security_health_analytics_custom_module_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = (
        security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest(
            parent="parent_value",
        )
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_security_health_analytics_custom_module(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ] == security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest(
            parent="parent_value",
        )


def test_create_security_health_analytics_custom_module_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_security_health_analytics_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_security_health_analytics_custom_module
        ] = mock_rpc
        request = {}
        client.create_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_security_health_analytics_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_security_health_analytics_custom_module_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SecurityHealthAnalyticsCustomModule(
                name="name_value",
                display_name="display_name_value",
                enablement_state=security_center_management.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED,
                last_editor="last_editor_value",
                ancestor_module="ancestor_module_value",
            )
        )
        response = await client.create_security_health_analytics_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest()
        )


@pytest.mark.asyncio
async def test_create_security_health_analytics_custom_module_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_security_health_analytics_custom_module
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_security_health_analytics_custom_module
        ] = mock_object

        request = {}
        await client.create_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.create_security_health_analytics_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_create_security_health_analytics_custom_module_async(
    transport: str = "grpc_asyncio",
    request_type=security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest,
):
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SecurityHealthAnalyticsCustomModule(
                name="name_value",
                display_name="display_name_value",
                enablement_state=security_center_management.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED,
                last_editor="last_editor_value",
                ancestor_module="ancestor_module_value",
            )
        )
        response = await client.create_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, security_center_management.SecurityHealthAnalyticsCustomModule
    )
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert (
        response.enablement_state
        == security_center_management.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED
    )
    assert response.last_editor == "last_editor_value"
    assert response.ancestor_module == "ancestor_module_value"


@pytest.mark.asyncio
async def test_create_security_health_analytics_custom_module_async_from_dict():
    await test_create_security_health_analytics_custom_module_async(request_type=dict)


def test_create_security_health_analytics_custom_module_field_headers():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest()
    )

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        call.return_value = (
            security_center_management.SecurityHealthAnalyticsCustomModule()
        )
        client.create_security_health_analytics_custom_module(request)

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
async def test_create_security_health_analytics_custom_module_field_headers_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest()
    )

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SecurityHealthAnalyticsCustomModule()
        )
        await client.create_security_health_analytics_custom_module(request)

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


def test_create_security_health_analytics_custom_module_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.SecurityHealthAnalyticsCustomModule()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_security_health_analytics_custom_module(
            parent="parent_value",
            security_health_analytics_custom_module=security_center_management.SecurityHealthAnalyticsCustomModule(
                name="name_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].security_health_analytics_custom_module
        mock_val = security_center_management.SecurityHealthAnalyticsCustomModule(
            name="name_value"
        )
        assert arg == mock_val


def test_create_security_health_analytics_custom_module_flattened_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_security_health_analytics_custom_module(
            security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest(),
            parent="parent_value",
            security_health_analytics_custom_module=security_center_management.SecurityHealthAnalyticsCustomModule(
                name="name_value"
            ),
        )


@pytest.mark.asyncio
async def test_create_security_health_analytics_custom_module_flattened_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.SecurityHealthAnalyticsCustomModule()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SecurityHealthAnalyticsCustomModule()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_security_health_analytics_custom_module(
            parent="parent_value",
            security_health_analytics_custom_module=security_center_management.SecurityHealthAnalyticsCustomModule(
                name="name_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].security_health_analytics_custom_module
        mock_val = security_center_management.SecurityHealthAnalyticsCustomModule(
            name="name_value"
        )
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_security_health_analytics_custom_module_flattened_error_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_security_health_analytics_custom_module(
            security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest(),
            parent="parent_value",
            security_health_analytics_custom_module=security_center_management.SecurityHealthAnalyticsCustomModule(
                name="name_value"
            ),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest,
        dict,
    ],
)
def test_update_security_health_analytics_custom_module(
    request_type, transport: str = "grpc"
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = security_center_management.SecurityHealthAnalyticsCustomModule(
            name="name_value",
            display_name="display_name_value",
            enablement_state=security_center_management.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED,
            last_editor="last_editor_value",
            ancestor_module="ancestor_module_value",
        )
        response = client.update_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, security_center_management.SecurityHealthAnalyticsCustomModule
    )
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert (
        response.enablement_state
        == security_center_management.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED
    )
    assert response.last_editor == "last_editor_value"
    assert response.ancestor_module == "ancestor_module_value"


def test_update_security_health_analytics_custom_module_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_security_health_analytics_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest()
        )


def test_update_security_health_analytics_custom_module_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = (
        security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest()
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_security_health_analytics_custom_module(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest()
        )


def test_update_security_health_analytics_custom_module_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_security_health_analytics_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_security_health_analytics_custom_module
        ] = mock_rpc
        request = {}
        client.update_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_security_health_analytics_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_security_health_analytics_custom_module_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SecurityHealthAnalyticsCustomModule(
                name="name_value",
                display_name="display_name_value",
                enablement_state=security_center_management.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED,
                last_editor="last_editor_value",
                ancestor_module="ancestor_module_value",
            )
        )
        response = await client.update_security_health_analytics_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest()
        )


@pytest.mark.asyncio
async def test_update_security_health_analytics_custom_module_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_security_health_analytics_custom_module
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_security_health_analytics_custom_module
        ] = mock_object

        request = {}
        await client.update_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.update_security_health_analytics_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_update_security_health_analytics_custom_module_async(
    transport: str = "grpc_asyncio",
    request_type=security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest,
):
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SecurityHealthAnalyticsCustomModule(
                name="name_value",
                display_name="display_name_value",
                enablement_state=security_center_management.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED,
                last_editor="last_editor_value",
                ancestor_module="ancestor_module_value",
            )
        )
        response = await client.update_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, security_center_management.SecurityHealthAnalyticsCustomModule
    )
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert (
        response.enablement_state
        == security_center_management.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED
    )
    assert response.last_editor == "last_editor_value"
    assert response.ancestor_module == "ancestor_module_value"


@pytest.mark.asyncio
async def test_update_security_health_analytics_custom_module_async_from_dict():
    await test_update_security_health_analytics_custom_module_async(request_type=dict)


def test_update_security_health_analytics_custom_module_field_headers():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest()
    )

    request.security_health_analytics_custom_module.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        call.return_value = (
            security_center_management.SecurityHealthAnalyticsCustomModule()
        )
        client.update_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "security_health_analytics_custom_module.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_security_health_analytics_custom_module_field_headers_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest()
    )

    request.security_health_analytics_custom_module.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SecurityHealthAnalyticsCustomModule()
        )
        await client.update_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "security_health_analytics_custom_module.name=name_value",
    ) in kw["metadata"]


def test_update_security_health_analytics_custom_module_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.SecurityHealthAnalyticsCustomModule()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_security_health_analytics_custom_module(
            security_health_analytics_custom_module=security_center_management.SecurityHealthAnalyticsCustomModule(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].security_health_analytics_custom_module
        mock_val = security_center_management.SecurityHealthAnalyticsCustomModule(
            name="name_value"
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_security_health_analytics_custom_module_flattened_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_security_health_analytics_custom_module(
            security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest(),
            security_health_analytics_custom_module=security_center_management.SecurityHealthAnalyticsCustomModule(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_security_health_analytics_custom_module_flattened_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.SecurityHealthAnalyticsCustomModule()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SecurityHealthAnalyticsCustomModule()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_security_health_analytics_custom_module(
            security_health_analytics_custom_module=security_center_management.SecurityHealthAnalyticsCustomModule(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].security_health_analytics_custom_module
        mock_val = security_center_management.SecurityHealthAnalyticsCustomModule(
            name="name_value"
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_security_health_analytics_custom_module_flattened_error_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_security_health_analytics_custom_module(
            security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest(),
            security_health_analytics_custom_module=security_center_management.SecurityHealthAnalyticsCustomModule(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest,
        dict,
    ],
)
def test_delete_security_health_analytics_custom_module(
    request_type, transport: str = "grpc"
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_security_health_analytics_custom_module_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_security_health_analytics_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest()
        )


def test_delete_security_health_analytics_custom_module_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = (
        security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest(
            name="name_value",
        )
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_security_health_analytics_custom_module(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ] == security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest(
            name="name_value",
        )


def test_delete_security_health_analytics_custom_module_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_security_health_analytics_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_security_health_analytics_custom_module
        ] = mock_rpc
        request = {}
        client.delete_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_security_health_analytics_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_security_health_analytics_custom_module_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_security_health_analytics_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest()
        )


@pytest.mark.asyncio
async def test_delete_security_health_analytics_custom_module_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_security_health_analytics_custom_module
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_security_health_analytics_custom_module
        ] = mock_object

        request = {}
        await client.delete_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.delete_security_health_analytics_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_delete_security_health_analytics_custom_module_async(
    transport: str = "grpc_asyncio",
    request_type=security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest,
):
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_security_health_analytics_custom_module_async_from_dict():
    await test_delete_security_health_analytics_custom_module_async(request_type=dict)


def test_delete_security_health_analytics_custom_module_field_headers():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest()
    )

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        call.return_value = None
        client.delete_security_health_analytics_custom_module(request)

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
async def test_delete_security_health_analytics_custom_module_field_headers_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest()
    )

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_security_health_analytics_custom_module(request)

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


def test_delete_security_health_analytics_custom_module_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_security_health_analytics_custom_module(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_security_health_analytics_custom_module_flattened_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_security_health_analytics_custom_module(
            security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_security_health_analytics_custom_module_flattened_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_security_health_analytics_custom_module(
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
async def test_delete_security_health_analytics_custom_module_flattened_error_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_security_health_analytics_custom_module(
            security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest,
        dict,
    ],
)
def test_simulate_security_health_analytics_custom_module(
    request_type, transport: str = "grpc"
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.simulate_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse()
        )
        response = client.simulate_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response,
        security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse,
    )


def test_simulate_security_health_analytics_custom_module_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.simulate_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.simulate_security_health_analytics_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest()
        )


def test_simulate_security_health_analytics_custom_module_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = (
        security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest(
            parent="parent_value",
        )
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.simulate_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.simulate_security_health_analytics_custom_module(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ] == security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest(
            parent="parent_value",
        )


def test_simulate_security_health_analytics_custom_module_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.simulate_security_health_analytics_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.simulate_security_health_analytics_custom_module
        ] = mock_rpc
        request = {}
        client.simulate_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.simulate_security_health_analytics_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_simulate_security_health_analytics_custom_module_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.simulate_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse()
        )
        response = await client.simulate_security_health_analytics_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest()
        )


@pytest.mark.asyncio
async def test_simulate_security_health_analytics_custom_module_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.simulate_security_health_analytics_custom_module
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.simulate_security_health_analytics_custom_module
        ] = mock_object

        request = {}
        await client.simulate_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.simulate_security_health_analytics_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_simulate_security_health_analytics_custom_module_async(
    transport: str = "grpc_asyncio",
    request_type=security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest,
):
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.simulate_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse()
        )
        response = await client.simulate_security_health_analytics_custom_module(
            request
        )

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response,
        security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse,
    )


@pytest.mark.asyncio
async def test_simulate_security_health_analytics_custom_module_async_from_dict():
    await test_simulate_security_health_analytics_custom_module_async(request_type=dict)


def test_simulate_security_health_analytics_custom_module_field_headers():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest()
    )

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.simulate_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        call.return_value = (
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse()
        )
        client.simulate_security_health_analytics_custom_module(request)

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
async def test_simulate_security_health_analytics_custom_module_field_headers_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest()
    )

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.simulate_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse()
        )
        await client.simulate_security_health_analytics_custom_module(request)

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


def test_simulate_security_health_analytics_custom_module_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.simulate_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.simulate_security_health_analytics_custom_module(
            parent="parent_value",
            custom_config=security_center_management.CustomConfig(
                predicate=expr_pb2.Expr(expression="expression_value")
            ),
            resource=security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest.SimulatedResource(
                resource_type="resource_type_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].custom_config
        mock_val = security_center_management.CustomConfig(
            predicate=expr_pb2.Expr(expression="expression_value")
        )
        assert arg == mock_val
        arg = args[0].resource
        mock_val = security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest.SimulatedResource(
            resource_type="resource_type_value"
        )
        assert arg == mock_val


def test_simulate_security_health_analytics_custom_module_flattened_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.simulate_security_health_analytics_custom_module(
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest(),
            parent="parent_value",
            custom_config=security_center_management.CustomConfig(
                predicate=expr_pb2.Expr(expression="expression_value")
            ),
            resource=security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest.SimulatedResource(
                resource_type="resource_type_value"
            ),
        )


@pytest.mark.asyncio
async def test_simulate_security_health_analytics_custom_module_flattened_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.simulate_security_health_analytics_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.simulate_security_health_analytics_custom_module(
            parent="parent_value",
            custom_config=security_center_management.CustomConfig(
                predicate=expr_pb2.Expr(expression="expression_value")
            ),
            resource=security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest.SimulatedResource(
                resource_type="resource_type_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].custom_config
        mock_val = security_center_management.CustomConfig(
            predicate=expr_pb2.Expr(expression="expression_value")
        )
        assert arg == mock_val
        arg = args[0].resource
        mock_val = security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest.SimulatedResource(
            resource_type="resource_type_value"
        )
        assert arg == mock_val


@pytest.mark.asyncio
async def test_simulate_security_health_analytics_custom_module_flattened_error_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.simulate_security_health_analytics_custom_module(
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest(),
            parent="parent_value",
            custom_config=security_center_management.CustomConfig(
                predicate=expr_pb2.Expr(expression="expression_value")
            ),
            resource=security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest.SimulatedResource(
                resource_type="resource_type_value"
            ),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest,
        dict,
    ],
)
def test_list_effective_event_threat_detection_custom_modules(
    request_type, transport: str = "grpc"
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_effective_event_threat_detection_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, pagers.ListEffectiveEventThreatDetectionCustomModulesPager
    )
    assert response.next_page_token == "next_page_token_value"


def test_list_effective_event_threat_detection_custom_modules_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_effective_event_threat_detection_custom_modules()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest()
        )


def test_list_effective_event_threat_detection_custom_modules_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_effective_event_threat_detection_custom_modules(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ] == security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_effective_event_threat_detection_custom_modules_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_effective_event_threat_detection_custom_modules
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_effective_event_threat_detection_custom_modules
        ] = mock_rpc
        request = {}
        client.list_effective_event_threat_detection_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_effective_event_threat_detection_custom_modules(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_effective_event_threat_detection_custom_modules_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_effective_event_threat_detection_custom_modules()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest()
        )


@pytest.mark.asyncio
async def test_list_effective_event_threat_detection_custom_modules_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_effective_event_threat_detection_custom_modules
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_effective_event_threat_detection_custom_modules
        ] = mock_object

        request = {}
        await client.list_effective_event_threat_detection_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_effective_event_threat_detection_custom_modules(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_effective_event_threat_detection_custom_modules_async(
    transport: str = "grpc_asyncio",
    request_type=security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest,
):
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_effective_event_threat_detection_custom_modules(
            request
        )

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, pagers.ListEffectiveEventThreatDetectionCustomModulesAsyncPager
    )
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_effective_event_threat_detection_custom_modules_async_from_dict():
    await test_list_effective_event_threat_detection_custom_modules_async(
        request_type=dict
    )


def test_list_effective_event_threat_detection_custom_modules_field_headers():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest()
    )

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        call.return_value = (
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse()
        )
        client.list_effective_event_threat_detection_custom_modules(request)

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
async def test_list_effective_event_threat_detection_custom_modules_field_headers_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest()
    )

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse()
        )
        await client.list_effective_event_threat_detection_custom_modules(request)

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


def test_list_effective_event_threat_detection_custom_modules_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_effective_event_threat_detection_custom_modules(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_effective_event_threat_detection_custom_modules_flattened_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_effective_event_threat_detection_custom_modules(
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_effective_event_threat_detection_custom_modules_flattened_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_effective_event_threat_detection_custom_modules(
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
async def test_list_effective_event_threat_detection_custom_modules_flattened_error_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_effective_event_threat_detection_custom_modules(
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest(),
            parent="parent_value",
        )


def test_list_effective_event_threat_detection_custom_modules_pager(
    transport_name: str = "grpc",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                effective_event_threat_detection_custom_modules=[
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                effective_event_threat_detection_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                effective_event_threat_detection_custom_modules=[
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                effective_event_threat_detection_custom_modules=[
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
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
        pager = client.list_effective_event_threat_detection_custom_modules(
            request={}, retry=retry, timeout=timeout
        )

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(
                i, security_center_management.EffectiveEventThreatDetectionCustomModule
            )
            for i in results
        )


def test_list_effective_event_threat_detection_custom_modules_pages(
    transport_name: str = "grpc",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                effective_event_threat_detection_custom_modules=[
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                effective_event_threat_detection_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                effective_event_threat_detection_custom_modules=[
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                effective_event_threat_detection_custom_modules=[
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                ],
            ),
            RuntimeError,
        )
        pages = list(
            client.list_effective_event_threat_detection_custom_modules(
                request={}
            ).pages
        )
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_effective_event_threat_detection_custom_modules_async_pager():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_event_threat_detection_custom_modules),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                effective_event_threat_detection_custom_modules=[
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                effective_event_threat_detection_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                effective_event_threat_detection_custom_modules=[
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                effective_event_threat_detection_custom_modules=[
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_effective_event_threat_detection_custom_modules(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(
                i, security_center_management.EffectiveEventThreatDetectionCustomModule
            )
            for i in responses
        )


@pytest.mark.asyncio
async def test_list_effective_event_threat_detection_custom_modules_async_pages():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_effective_event_threat_detection_custom_modules),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                effective_event_threat_detection_custom_modules=[
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                effective_event_threat_detection_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                effective_event_threat_detection_custom_modules=[
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                effective_event_threat_detection_custom_modules=[
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_effective_event_threat_detection_custom_modules(
                request={}
            )
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest,
        dict,
    ],
)
def test_get_effective_event_threat_detection_custom_module(
    request_type, transport: str = "grpc"
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_event_threat_detection_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = security_center_management.EffectiveEventThreatDetectionCustomModule(
            name="name_value",
            enablement_state=security_center_management.EffectiveEventThreatDetectionCustomModule.EnablementState.ENABLED,
            type_="type__value",
            display_name="display_name_value",
            description="description_value",
        )
        response = client.get_effective_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, security_center_management.EffectiveEventThreatDetectionCustomModule
    )
    assert response.name == "name_value"
    assert (
        response.enablement_state
        == security_center_management.EffectiveEventThreatDetectionCustomModule.EnablementState.ENABLED
    )
    assert response.type_ == "type__value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_get_effective_event_threat_detection_custom_module_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_event_threat_detection_custom_module),
        "__call__",
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_effective_event_threat_detection_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest()
        )


def test_get_effective_event_threat_detection_custom_module_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = (
        security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest(
            name="name_value",
        )
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_event_threat_detection_custom_module),
        "__call__",
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_effective_event_threat_detection_custom_module(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ] == security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest(
            name="name_value",
        )


def test_get_effective_event_threat_detection_custom_module_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_effective_event_threat_detection_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_effective_event_threat_detection_custom_module
        ] = mock_rpc
        request = {}
        client.get_effective_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_effective_event_threat_detection_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_effective_event_threat_detection_custom_module_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_event_threat_detection_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.EffectiveEventThreatDetectionCustomModule(
                name="name_value",
                enablement_state=security_center_management.EffectiveEventThreatDetectionCustomModule.EnablementState.ENABLED,
                type_="type__value",
                display_name="display_name_value",
                description="description_value",
            )
        )
        response = await client.get_effective_event_threat_detection_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest()
        )


@pytest.mark.asyncio
async def test_get_effective_event_threat_detection_custom_module_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_effective_event_threat_detection_custom_module
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_effective_event_threat_detection_custom_module
        ] = mock_object

        request = {}
        await client.get_effective_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_effective_event_threat_detection_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_effective_event_threat_detection_custom_module_async(
    transport: str = "grpc_asyncio",
    request_type=security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest,
):
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_event_threat_detection_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.EffectiveEventThreatDetectionCustomModule(
                name="name_value",
                enablement_state=security_center_management.EffectiveEventThreatDetectionCustomModule.EnablementState.ENABLED,
                type_="type__value",
                display_name="display_name_value",
                description="description_value",
            )
        )
        response = await client.get_effective_event_threat_detection_custom_module(
            request
        )

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, security_center_management.EffectiveEventThreatDetectionCustomModule
    )
    assert response.name == "name_value"
    assert (
        response.enablement_state
        == security_center_management.EffectiveEventThreatDetectionCustomModule.EnablementState.ENABLED
    )
    assert response.type_ == "type__value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_get_effective_event_threat_detection_custom_module_async_from_dict():
    await test_get_effective_event_threat_detection_custom_module_async(
        request_type=dict
    )


def test_get_effective_event_threat_detection_custom_module_field_headers():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest()
    )

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_event_threat_detection_custom_module),
        "__call__",
    ) as call:
        call.return_value = (
            security_center_management.EffectiveEventThreatDetectionCustomModule()
        )
        client.get_effective_event_threat_detection_custom_module(request)

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
async def test_get_effective_event_threat_detection_custom_module_field_headers_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest()
    )

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_event_threat_detection_custom_module),
        "__call__",
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.EffectiveEventThreatDetectionCustomModule()
        )
        await client.get_effective_event_threat_detection_custom_module(request)

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


def test_get_effective_event_threat_detection_custom_module_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_event_threat_detection_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.EffectiveEventThreatDetectionCustomModule()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_effective_event_threat_detection_custom_module(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_effective_event_threat_detection_custom_module_flattened_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_effective_event_threat_detection_custom_module(
            security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_effective_event_threat_detection_custom_module_flattened_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_event_threat_detection_custom_module),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.EffectiveEventThreatDetectionCustomModule()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.EffectiveEventThreatDetectionCustomModule()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_effective_event_threat_detection_custom_module(
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
async def test_get_effective_event_threat_detection_custom_module_flattened_error_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_effective_event_threat_detection_custom_module(
            security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.ListEventThreatDetectionCustomModulesRequest,
        dict,
    ],
)
def test_list_event_threat_detection_custom_modules(
    request_type, transport: str = "grpc"
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_event_threat_detection_custom_modules), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = client.list_event_threat_detection_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.ListEventThreatDetectionCustomModulesRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEventThreatDetectionCustomModulesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_event_threat_detection_custom_modules_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_event_threat_detection_custom_modules), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_event_threat_detection_custom_modules()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.ListEventThreatDetectionCustomModulesRequest()
        )


def test_list_event_threat_detection_custom_modules_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = security_center_management.ListEventThreatDetectionCustomModulesRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_event_threat_detection_custom_modules), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_event_threat_detection_custom_modules(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ] == security_center_management.ListEventThreatDetectionCustomModulesRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_event_threat_detection_custom_modules_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_event_threat_detection_custom_modules
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_event_threat_detection_custom_modules
        ] = mock_rpc
        request = {}
        client.list_event_threat_detection_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_event_threat_detection_custom_modules(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_event_threat_detection_custom_modules_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_event_threat_detection_custom_modules), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_event_threat_detection_custom_modules()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.ListEventThreatDetectionCustomModulesRequest()
        )


@pytest.mark.asyncio
async def test_list_event_threat_detection_custom_modules_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_event_threat_detection_custom_modules
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_event_threat_detection_custom_modules
        ] = mock_object

        request = {}
        await client.list_event_threat_detection_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_event_threat_detection_custom_modules(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_event_threat_detection_custom_modules_async(
    transport: str = "grpc_asyncio",
    request_type=security_center_management.ListEventThreatDetectionCustomModulesRequest,
):
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_event_threat_detection_custom_modules), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_event_threat_detection_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.ListEventThreatDetectionCustomModulesRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEventThreatDetectionCustomModulesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_event_threat_detection_custom_modules_async_from_dict():
    await test_list_event_threat_detection_custom_modules_async(request_type=dict)


def test_list_event_threat_detection_custom_modules_field_headers():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = security_center_management.ListEventThreatDetectionCustomModulesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_event_threat_detection_custom_modules), "__call__"
    ) as call:
        call.return_value = (
            security_center_management.ListEventThreatDetectionCustomModulesResponse()
        )
        client.list_event_threat_detection_custom_modules(request)

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
async def test_list_event_threat_detection_custom_modules_field_headers_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = security_center_management.ListEventThreatDetectionCustomModulesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_event_threat_detection_custom_modules), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListEventThreatDetectionCustomModulesResponse()
        )
        await client.list_event_threat_detection_custom_modules(request)

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


def test_list_event_threat_detection_custom_modules_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_event_threat_detection_custom_modules), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.ListEventThreatDetectionCustomModulesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_event_threat_detection_custom_modules(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_event_threat_detection_custom_modules_flattened_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_event_threat_detection_custom_modules(
            security_center_management.ListEventThreatDetectionCustomModulesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_event_threat_detection_custom_modules_flattened_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_event_threat_detection_custom_modules), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.ListEventThreatDetectionCustomModulesResponse()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListEventThreatDetectionCustomModulesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_event_threat_detection_custom_modules(
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
async def test_list_event_threat_detection_custom_modules_flattened_error_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_event_threat_detection_custom_modules(
            security_center_management.ListEventThreatDetectionCustomModulesRequest(),
            parent="parent_value",
        )


def test_list_event_threat_detection_custom_modules_pager(transport_name: str = "grpc"):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_event_threat_detection_custom_modules), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
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
        pager = client.list_event_threat_detection_custom_modules(
            request={}, retry=retry, timeout=timeout
        )

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, security_center_management.EventThreatDetectionCustomModule)
            for i in results
        )


def test_list_event_threat_detection_custom_modules_pages(transport_name: str = "grpc"):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_event_threat_detection_custom_modules), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
            ),
            RuntimeError,
        )
        pages = list(
            client.list_event_threat_detection_custom_modules(request={}).pages
        )
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_event_threat_detection_custom_modules_async_pager():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_event_threat_detection_custom_modules),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_event_threat_detection_custom_modules(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, security_center_management.EventThreatDetectionCustomModule)
            for i in responses
        )


@pytest.mark.asyncio
async def test_list_event_threat_detection_custom_modules_async_pages():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_event_threat_detection_custom_modules),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_event_threat_detection_custom_modules(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest,
        dict,
    ],
)
def test_list_descendant_event_threat_detection_custom_modules(
    request_type, transport: str = "grpc"
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_descendant_event_threat_detection_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, pagers.ListDescendantEventThreatDetectionCustomModulesPager
    )
    assert response.next_page_token == "next_page_token_value"


def test_list_descendant_event_threat_detection_custom_modules_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_descendant_event_threat_detection_custom_modules()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest()
        )


def test_list_descendant_event_threat_detection_custom_modules_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_descendant_event_threat_detection_custom_modules(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ] == security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_descendant_event_threat_detection_custom_modules_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_descendant_event_threat_detection_custom_modules
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_descendant_event_threat_detection_custom_modules
        ] = mock_rpc
        request = {}
        client.list_descendant_event_threat_detection_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_descendant_event_threat_detection_custom_modules(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_descendant_event_threat_detection_custom_modules_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_descendant_event_threat_detection_custom_modules()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest()
        )


@pytest.mark.asyncio
async def test_list_descendant_event_threat_detection_custom_modules_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_descendant_event_threat_detection_custom_modules
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_descendant_event_threat_detection_custom_modules
        ] = mock_object

        request = {}
        await client.list_descendant_event_threat_detection_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_descendant_event_threat_detection_custom_modules(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_descendant_event_threat_detection_custom_modules_async(
    transport: str = "grpc_asyncio",
    request_type=security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest,
):
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_descendant_event_threat_detection_custom_modules(
            request
        )

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, pagers.ListDescendantEventThreatDetectionCustomModulesAsyncPager
    )
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_descendant_event_threat_detection_custom_modules_async_from_dict():
    await test_list_descendant_event_threat_detection_custom_modules_async(
        request_type=dict
    )


def test_list_descendant_event_threat_detection_custom_modules_field_headers():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest()
    )

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        call.return_value = (
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse()
        )
        client.list_descendant_event_threat_detection_custom_modules(request)

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
async def test_list_descendant_event_threat_detection_custom_modules_field_headers_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest()
    )

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse()
        )
        await client.list_descendant_event_threat_detection_custom_modules(request)

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


def test_list_descendant_event_threat_detection_custom_modules_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_descendant_event_threat_detection_custom_modules(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_descendant_event_threat_detection_custom_modules_flattened_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_descendant_event_threat_detection_custom_modules(
            security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_descendant_event_threat_detection_custom_modules_flattened_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_descendant_event_threat_detection_custom_modules(
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
async def test_list_descendant_event_threat_detection_custom_modules_flattened_error_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_descendant_event_threat_detection_custom_modules(
            security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest(),
            parent="parent_value",
        )


def test_list_descendant_event_threat_detection_custom_modules_pager(
    transport_name: str = "grpc",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
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
        pager = client.list_descendant_event_threat_detection_custom_modules(
            request={}, retry=retry, timeout=timeout
        )

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, security_center_management.EventThreatDetectionCustomModule)
            for i in results
        )


def test_list_descendant_event_threat_detection_custom_modules_pages(
    transport_name: str = "grpc",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_event_threat_detection_custom_modules),
        "__call__",
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
            ),
            RuntimeError,
        )
        pages = list(
            client.list_descendant_event_threat_detection_custom_modules(
                request={}
            ).pages
        )
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_descendant_event_threat_detection_custom_modules_async_pager():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_event_threat_detection_custom_modules),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
            ),
            RuntimeError,
        )
        async_pager = (
            await client.list_descendant_event_threat_detection_custom_modules(
                request={},
            )
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, security_center_management.EventThreatDetectionCustomModule)
            for i in responses
        )


@pytest.mark.asyncio
async def test_list_descendant_event_threat_detection_custom_modules_async_pages():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_descendant_event_threat_detection_custom_modules),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_descendant_event_threat_detection_custom_modules(
                request={}
            )
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.GetEventThreatDetectionCustomModuleRequest,
        dict,
    ],
)
def test_get_event_threat_detection_custom_module(
    request_type, transport: str = "grpc"
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = security_center_management.EventThreatDetectionCustomModule(
            name="name_value",
            ancestor_module="ancestor_module_value",
            enablement_state=security_center_management.EventThreatDetectionCustomModule.EnablementState.ENABLED,
            type_="type__value",
            display_name="display_name_value",
            description="description_value",
            last_editor="last_editor_value",
        )
        response = client.get_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.GetEventThreatDetectionCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, security_center_management.EventThreatDetectionCustomModule
    )
    assert response.name == "name_value"
    assert response.ancestor_module == "ancestor_module_value"
    assert (
        response.enablement_state
        == security_center_management.EventThreatDetectionCustomModule.EnablementState.ENABLED
    )
    assert response.type_ == "type__value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.last_editor == "last_editor_value"


def test_get_event_threat_detection_custom_module_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_event_threat_detection_custom_module), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_event_threat_detection_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.GetEventThreatDetectionCustomModuleRequest()
        )


def test_get_event_threat_detection_custom_module_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = security_center_management.GetEventThreatDetectionCustomModuleRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_event_threat_detection_custom_module), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_event_threat_detection_custom_module(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ] == security_center_management.GetEventThreatDetectionCustomModuleRequest(
            name="name_value",
        )


def test_get_event_threat_detection_custom_module_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_event_threat_detection_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_event_threat_detection_custom_module
        ] = mock_rpc
        request = {}
        client.get_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_event_threat_detection_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_event_threat_detection_custom_module_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.EventThreatDetectionCustomModule(
                name="name_value",
                ancestor_module="ancestor_module_value",
                enablement_state=security_center_management.EventThreatDetectionCustomModule.EnablementState.ENABLED,
                type_="type__value",
                display_name="display_name_value",
                description="description_value",
                last_editor="last_editor_value",
            )
        )
        response = await client.get_event_threat_detection_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.GetEventThreatDetectionCustomModuleRequest()
        )


@pytest.mark.asyncio
async def test_get_event_threat_detection_custom_module_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_event_threat_detection_custom_module
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_event_threat_detection_custom_module
        ] = mock_object

        request = {}
        await client.get_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_event_threat_detection_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_event_threat_detection_custom_module_async(
    transport: str = "grpc_asyncio",
    request_type=security_center_management.GetEventThreatDetectionCustomModuleRequest,
):
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.EventThreatDetectionCustomModule(
                name="name_value",
                ancestor_module="ancestor_module_value",
                enablement_state=security_center_management.EventThreatDetectionCustomModule.EnablementState.ENABLED,
                type_="type__value",
                display_name="display_name_value",
                description="description_value",
                last_editor="last_editor_value",
            )
        )
        response = await client.get_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.GetEventThreatDetectionCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, security_center_management.EventThreatDetectionCustomModule
    )
    assert response.name == "name_value"
    assert response.ancestor_module == "ancestor_module_value"
    assert (
        response.enablement_state
        == security_center_management.EventThreatDetectionCustomModule.EnablementState.ENABLED
    )
    assert response.type_ == "type__value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.last_editor == "last_editor_value"


@pytest.mark.asyncio
async def test_get_event_threat_detection_custom_module_async_from_dict():
    await test_get_event_threat_detection_custom_module_async(request_type=dict)


def test_get_event_threat_detection_custom_module_field_headers():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = security_center_management.GetEventThreatDetectionCustomModuleRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_event_threat_detection_custom_module), "__call__"
    ) as call:
        call.return_value = (
            security_center_management.EventThreatDetectionCustomModule()
        )
        client.get_event_threat_detection_custom_module(request)

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
async def test_get_event_threat_detection_custom_module_field_headers_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = security_center_management.GetEventThreatDetectionCustomModuleRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_event_threat_detection_custom_module), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.EventThreatDetectionCustomModule()
        )
        await client.get_event_threat_detection_custom_module(request)

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


def test_get_event_threat_detection_custom_module_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.EventThreatDetectionCustomModule()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_event_threat_detection_custom_module(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_event_threat_detection_custom_module_flattened_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_event_threat_detection_custom_module(
            security_center_management.GetEventThreatDetectionCustomModuleRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_event_threat_detection_custom_module_flattened_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.EventThreatDetectionCustomModule()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.EventThreatDetectionCustomModule()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_event_threat_detection_custom_module(
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
async def test_get_event_threat_detection_custom_module_flattened_error_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_event_threat_detection_custom_module(
            security_center_management.GetEventThreatDetectionCustomModuleRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.CreateEventThreatDetectionCustomModuleRequest,
        dict,
    ],
)
def test_create_event_threat_detection_custom_module(
    request_type, transport: str = "grpc"
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = security_center_management.EventThreatDetectionCustomModule(
            name="name_value",
            ancestor_module="ancestor_module_value",
            enablement_state=security_center_management.EventThreatDetectionCustomModule.EnablementState.ENABLED,
            type_="type__value",
            display_name="display_name_value",
            description="description_value",
            last_editor="last_editor_value",
        )
        response = client.create_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.CreateEventThreatDetectionCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, security_center_management.EventThreatDetectionCustomModule
    )
    assert response.name == "name_value"
    assert response.ancestor_module == "ancestor_module_value"
    assert (
        response.enablement_state
        == security_center_management.EventThreatDetectionCustomModule.EnablementState.ENABLED
    )
    assert response.type_ == "type__value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.last_editor == "last_editor_value"


def test_create_event_threat_detection_custom_module_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_event_threat_detection_custom_module), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_event_threat_detection_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.CreateEventThreatDetectionCustomModuleRequest()
        )


def test_create_event_threat_detection_custom_module_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = security_center_management.CreateEventThreatDetectionCustomModuleRequest(
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_event_threat_detection_custom_module), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_event_threat_detection_custom_module(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ] == security_center_management.CreateEventThreatDetectionCustomModuleRequest(
            parent="parent_value",
        )


def test_create_event_threat_detection_custom_module_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_event_threat_detection_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_event_threat_detection_custom_module
        ] = mock_rpc
        request = {}
        client.create_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_event_threat_detection_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_event_threat_detection_custom_module_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.EventThreatDetectionCustomModule(
                name="name_value",
                ancestor_module="ancestor_module_value",
                enablement_state=security_center_management.EventThreatDetectionCustomModule.EnablementState.ENABLED,
                type_="type__value",
                display_name="display_name_value",
                description="description_value",
                last_editor="last_editor_value",
            )
        )
        response = await client.create_event_threat_detection_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.CreateEventThreatDetectionCustomModuleRequest()
        )


@pytest.mark.asyncio
async def test_create_event_threat_detection_custom_module_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_event_threat_detection_custom_module
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_event_threat_detection_custom_module
        ] = mock_object

        request = {}
        await client.create_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.create_event_threat_detection_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_create_event_threat_detection_custom_module_async(
    transport: str = "grpc_asyncio",
    request_type=security_center_management.CreateEventThreatDetectionCustomModuleRequest,
):
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.EventThreatDetectionCustomModule(
                name="name_value",
                ancestor_module="ancestor_module_value",
                enablement_state=security_center_management.EventThreatDetectionCustomModule.EnablementState.ENABLED,
                type_="type__value",
                display_name="display_name_value",
                description="description_value",
                last_editor="last_editor_value",
            )
        )
        response = await client.create_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.CreateEventThreatDetectionCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, security_center_management.EventThreatDetectionCustomModule
    )
    assert response.name == "name_value"
    assert response.ancestor_module == "ancestor_module_value"
    assert (
        response.enablement_state
        == security_center_management.EventThreatDetectionCustomModule.EnablementState.ENABLED
    )
    assert response.type_ == "type__value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.last_editor == "last_editor_value"


@pytest.mark.asyncio
async def test_create_event_threat_detection_custom_module_async_from_dict():
    await test_create_event_threat_detection_custom_module_async(request_type=dict)


def test_create_event_threat_detection_custom_module_field_headers():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = security_center_management.CreateEventThreatDetectionCustomModuleRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_event_threat_detection_custom_module), "__call__"
    ) as call:
        call.return_value = (
            security_center_management.EventThreatDetectionCustomModule()
        )
        client.create_event_threat_detection_custom_module(request)

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
async def test_create_event_threat_detection_custom_module_field_headers_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = security_center_management.CreateEventThreatDetectionCustomModuleRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_event_threat_detection_custom_module), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.EventThreatDetectionCustomModule()
        )
        await client.create_event_threat_detection_custom_module(request)

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


def test_create_event_threat_detection_custom_module_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.EventThreatDetectionCustomModule()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_event_threat_detection_custom_module(
            parent="parent_value",
            event_threat_detection_custom_module=security_center_management.EventThreatDetectionCustomModule(
                name="name_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].event_threat_detection_custom_module
        mock_val = security_center_management.EventThreatDetectionCustomModule(
            name="name_value"
        )
        assert arg == mock_val


def test_create_event_threat_detection_custom_module_flattened_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_event_threat_detection_custom_module(
            security_center_management.CreateEventThreatDetectionCustomModuleRequest(),
            parent="parent_value",
            event_threat_detection_custom_module=security_center_management.EventThreatDetectionCustomModule(
                name="name_value"
            ),
        )


@pytest.mark.asyncio
async def test_create_event_threat_detection_custom_module_flattened_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.EventThreatDetectionCustomModule()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.EventThreatDetectionCustomModule()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_event_threat_detection_custom_module(
            parent="parent_value",
            event_threat_detection_custom_module=security_center_management.EventThreatDetectionCustomModule(
                name="name_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].event_threat_detection_custom_module
        mock_val = security_center_management.EventThreatDetectionCustomModule(
            name="name_value"
        )
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_event_threat_detection_custom_module_flattened_error_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_event_threat_detection_custom_module(
            security_center_management.CreateEventThreatDetectionCustomModuleRequest(),
            parent="parent_value",
            event_threat_detection_custom_module=security_center_management.EventThreatDetectionCustomModule(
                name="name_value"
            ),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.UpdateEventThreatDetectionCustomModuleRequest,
        dict,
    ],
)
def test_update_event_threat_detection_custom_module(
    request_type, transport: str = "grpc"
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = security_center_management.EventThreatDetectionCustomModule(
            name="name_value",
            ancestor_module="ancestor_module_value",
            enablement_state=security_center_management.EventThreatDetectionCustomModule.EnablementState.ENABLED,
            type_="type__value",
            display_name="display_name_value",
            description="description_value",
            last_editor="last_editor_value",
        )
        response = client.update_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.UpdateEventThreatDetectionCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, security_center_management.EventThreatDetectionCustomModule
    )
    assert response.name == "name_value"
    assert response.ancestor_module == "ancestor_module_value"
    assert (
        response.enablement_state
        == security_center_management.EventThreatDetectionCustomModule.EnablementState.ENABLED
    )
    assert response.type_ == "type__value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.last_editor == "last_editor_value"


def test_update_event_threat_detection_custom_module_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_event_threat_detection_custom_module), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_event_threat_detection_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.UpdateEventThreatDetectionCustomModuleRequest()
        )


def test_update_event_threat_detection_custom_module_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = security_center_management.UpdateEventThreatDetectionCustomModuleRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_event_threat_detection_custom_module), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_event_threat_detection_custom_module(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.UpdateEventThreatDetectionCustomModuleRequest()
        )


def test_update_event_threat_detection_custom_module_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_event_threat_detection_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_event_threat_detection_custom_module
        ] = mock_rpc
        request = {}
        client.update_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_event_threat_detection_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_event_threat_detection_custom_module_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.EventThreatDetectionCustomModule(
                name="name_value",
                ancestor_module="ancestor_module_value",
                enablement_state=security_center_management.EventThreatDetectionCustomModule.EnablementState.ENABLED,
                type_="type__value",
                display_name="display_name_value",
                description="description_value",
                last_editor="last_editor_value",
            )
        )
        response = await client.update_event_threat_detection_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.UpdateEventThreatDetectionCustomModuleRequest()
        )


@pytest.mark.asyncio
async def test_update_event_threat_detection_custom_module_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_event_threat_detection_custom_module
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_event_threat_detection_custom_module
        ] = mock_object

        request = {}
        await client.update_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.update_event_threat_detection_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_update_event_threat_detection_custom_module_async(
    transport: str = "grpc_asyncio",
    request_type=security_center_management.UpdateEventThreatDetectionCustomModuleRequest,
):
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.EventThreatDetectionCustomModule(
                name="name_value",
                ancestor_module="ancestor_module_value",
                enablement_state=security_center_management.EventThreatDetectionCustomModule.EnablementState.ENABLED,
                type_="type__value",
                display_name="display_name_value",
                description="description_value",
                last_editor="last_editor_value",
            )
        )
        response = await client.update_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.UpdateEventThreatDetectionCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, security_center_management.EventThreatDetectionCustomModule
    )
    assert response.name == "name_value"
    assert response.ancestor_module == "ancestor_module_value"
    assert (
        response.enablement_state
        == security_center_management.EventThreatDetectionCustomModule.EnablementState.ENABLED
    )
    assert response.type_ == "type__value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.last_editor == "last_editor_value"


@pytest.mark.asyncio
async def test_update_event_threat_detection_custom_module_async_from_dict():
    await test_update_event_threat_detection_custom_module_async(request_type=dict)


def test_update_event_threat_detection_custom_module_field_headers():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = security_center_management.UpdateEventThreatDetectionCustomModuleRequest()

    request.event_threat_detection_custom_module.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_event_threat_detection_custom_module), "__call__"
    ) as call:
        call.return_value = (
            security_center_management.EventThreatDetectionCustomModule()
        )
        client.update_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "event_threat_detection_custom_module.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_event_threat_detection_custom_module_field_headers_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = security_center_management.UpdateEventThreatDetectionCustomModuleRequest()

    request.event_threat_detection_custom_module.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_event_threat_detection_custom_module), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.EventThreatDetectionCustomModule()
        )
        await client.update_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "event_threat_detection_custom_module.name=name_value",
    ) in kw["metadata"]


def test_update_event_threat_detection_custom_module_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.EventThreatDetectionCustomModule()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_event_threat_detection_custom_module(
            event_threat_detection_custom_module=security_center_management.EventThreatDetectionCustomModule(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].event_threat_detection_custom_module
        mock_val = security_center_management.EventThreatDetectionCustomModule(
            name="name_value"
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_event_threat_detection_custom_module_flattened_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_event_threat_detection_custom_module(
            security_center_management.UpdateEventThreatDetectionCustomModuleRequest(),
            event_threat_detection_custom_module=security_center_management.EventThreatDetectionCustomModule(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_event_threat_detection_custom_module_flattened_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.EventThreatDetectionCustomModule()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.EventThreatDetectionCustomModule()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_event_threat_detection_custom_module(
            event_threat_detection_custom_module=security_center_management.EventThreatDetectionCustomModule(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].event_threat_detection_custom_module
        mock_val = security_center_management.EventThreatDetectionCustomModule(
            name="name_value"
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_event_threat_detection_custom_module_flattened_error_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_event_threat_detection_custom_module(
            security_center_management.UpdateEventThreatDetectionCustomModuleRequest(),
            event_threat_detection_custom_module=security_center_management.EventThreatDetectionCustomModule(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.DeleteEventThreatDetectionCustomModuleRequest,
        dict,
    ],
)
def test_delete_event_threat_detection_custom_module(
    request_type, transport: str = "grpc"
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.DeleteEventThreatDetectionCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_event_threat_detection_custom_module_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_event_threat_detection_custom_module), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_event_threat_detection_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.DeleteEventThreatDetectionCustomModuleRequest()
        )


def test_delete_event_threat_detection_custom_module_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = security_center_management.DeleteEventThreatDetectionCustomModuleRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_event_threat_detection_custom_module), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_event_threat_detection_custom_module(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ] == security_center_management.DeleteEventThreatDetectionCustomModuleRequest(
            name="name_value",
        )


def test_delete_event_threat_detection_custom_module_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_event_threat_detection_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_event_threat_detection_custom_module
        ] = mock_rpc
        request = {}
        client.delete_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_event_threat_detection_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_event_threat_detection_custom_module_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_event_threat_detection_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.DeleteEventThreatDetectionCustomModuleRequest()
        )


@pytest.mark.asyncio
async def test_delete_event_threat_detection_custom_module_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_event_threat_detection_custom_module
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_event_threat_detection_custom_module
        ] = mock_object

        request = {}
        await client.delete_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.delete_event_threat_detection_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_delete_event_threat_detection_custom_module_async(
    transport: str = "grpc_asyncio",
    request_type=security_center_management.DeleteEventThreatDetectionCustomModuleRequest,
):
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.DeleteEventThreatDetectionCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_event_threat_detection_custom_module_async_from_dict():
    await test_delete_event_threat_detection_custom_module_async(request_type=dict)


def test_delete_event_threat_detection_custom_module_field_headers():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = security_center_management.DeleteEventThreatDetectionCustomModuleRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_event_threat_detection_custom_module), "__call__"
    ) as call:
        call.return_value = None
        client.delete_event_threat_detection_custom_module(request)

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
async def test_delete_event_threat_detection_custom_module_field_headers_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = security_center_management.DeleteEventThreatDetectionCustomModuleRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_event_threat_detection_custom_module), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_event_threat_detection_custom_module(request)

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


def test_delete_event_threat_detection_custom_module_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_event_threat_detection_custom_module(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_event_threat_detection_custom_module_flattened_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_event_threat_detection_custom_module(
            security_center_management.DeleteEventThreatDetectionCustomModuleRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_event_threat_detection_custom_module_flattened_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_event_threat_detection_custom_module(
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
async def test_delete_event_threat_detection_custom_module_flattened_error_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_event_threat_detection_custom_module(
            security_center_management.DeleteEventThreatDetectionCustomModuleRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.ValidateEventThreatDetectionCustomModuleRequest,
        dict,
    ],
)
def test_validate_event_threat_detection_custom_module(
    request_type, transport: str = "grpc"
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.validate_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.ValidateEventThreatDetectionCustomModuleResponse()
        )
        response = client.validate_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.ValidateEventThreatDetectionCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response,
        security_center_management.ValidateEventThreatDetectionCustomModuleResponse,
    )


def test_validate_event_threat_detection_custom_module_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.validate_event_threat_detection_custom_module), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.validate_event_threat_detection_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.ValidateEventThreatDetectionCustomModuleRequest()
        )


def test_validate_event_threat_detection_custom_module_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = (
        security_center_management.ValidateEventThreatDetectionCustomModuleRequest(
            parent="parent_value",
            raw_text="raw_text_value",
            type_="type__value",
        )
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.validate_event_threat_detection_custom_module), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.validate_event_threat_detection_custom_module(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ] == security_center_management.ValidateEventThreatDetectionCustomModuleRequest(
            parent="parent_value",
            raw_text="raw_text_value",
            type_="type__value",
        )


def test_validate_event_threat_detection_custom_module_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.validate_event_threat_detection_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.validate_event_threat_detection_custom_module
        ] = mock_rpc
        request = {}
        client.validate_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.validate_event_threat_detection_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_validate_event_threat_detection_custom_module_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.validate_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ValidateEventThreatDetectionCustomModuleResponse()
        )
        response = await client.validate_event_threat_detection_custom_module()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == security_center_management.ValidateEventThreatDetectionCustomModuleRequest()
        )


@pytest.mark.asyncio
async def test_validate_event_threat_detection_custom_module_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.validate_event_threat_detection_custom_module
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.validate_event_threat_detection_custom_module
        ] = mock_object

        request = {}
        await client.validate_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.validate_event_threat_detection_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_validate_event_threat_detection_custom_module_async(
    transport: str = "grpc_asyncio",
    request_type=security_center_management.ValidateEventThreatDetectionCustomModuleRequest,
):
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.validate_event_threat_detection_custom_module), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ValidateEventThreatDetectionCustomModuleResponse()
        )
        response = await client.validate_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = (
            security_center_management.ValidateEventThreatDetectionCustomModuleRequest()
        )
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response,
        security_center_management.ValidateEventThreatDetectionCustomModuleResponse,
    )


@pytest.mark.asyncio
async def test_validate_event_threat_detection_custom_module_async_from_dict():
    await test_validate_event_threat_detection_custom_module_async(request_type=dict)


def test_validate_event_threat_detection_custom_module_field_headers():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.ValidateEventThreatDetectionCustomModuleRequest()
    )

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.validate_event_threat_detection_custom_module), "__call__"
    ) as call:
        call.return_value = (
            security_center_management.ValidateEventThreatDetectionCustomModuleResponse()
        )
        client.validate_event_threat_detection_custom_module(request)

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
async def test_validate_event_threat_detection_custom_module_field_headers_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = (
        security_center_management.ValidateEventThreatDetectionCustomModuleRequest()
    )

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.validate_event_threat_detection_custom_module), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ValidateEventThreatDetectionCustomModuleResponse()
        )
        await client.validate_event_threat_detection_custom_module(request)

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
        security_center_management.GetSecurityCenterServiceRequest,
        dict,
    ],
)
def test_get_security_center_service(request_type, transport: str = "grpc"):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_security_center_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = security_center_management.SecurityCenterService(
            name="name_value",
            intended_enablement_state=security_center_management.SecurityCenterService.EnablementState.INHERITED,
            effective_enablement_state=security_center_management.SecurityCenterService.EnablementState.INHERITED,
        )
        response = client.get_security_center_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = security_center_management.GetSecurityCenterServiceRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, security_center_management.SecurityCenterService)
    assert response.name == "name_value"
    assert (
        response.intended_enablement_state
        == security_center_management.SecurityCenterService.EnablementState.INHERITED
    )
    assert (
        response.effective_enablement_state
        == security_center_management.SecurityCenterService.EnablementState.INHERITED
    )


def test_get_security_center_service_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_security_center_service), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_security_center_service()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == security_center_management.GetSecurityCenterServiceRequest()


def test_get_security_center_service_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = security_center_management.GetSecurityCenterServiceRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_security_center_service), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_security_center_service(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == security_center_management.GetSecurityCenterServiceRequest(
            name="name_value",
        )


def test_get_security_center_service_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_security_center_service
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_security_center_service
        ] = mock_rpc
        request = {}
        client.get_security_center_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_security_center_service(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_security_center_service_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_security_center_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SecurityCenterService(
                name="name_value",
                intended_enablement_state=security_center_management.SecurityCenterService.EnablementState.INHERITED,
                effective_enablement_state=security_center_management.SecurityCenterService.EnablementState.INHERITED,
            )
        )
        response = await client.get_security_center_service()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == security_center_management.GetSecurityCenterServiceRequest()


@pytest.mark.asyncio
async def test_get_security_center_service_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_security_center_service
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_security_center_service
        ] = mock_object

        request = {}
        await client.get_security_center_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_security_center_service(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_security_center_service_async(
    transport: str = "grpc_asyncio",
    request_type=security_center_management.GetSecurityCenterServiceRequest,
):
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_security_center_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SecurityCenterService(
                name="name_value",
                intended_enablement_state=security_center_management.SecurityCenterService.EnablementState.INHERITED,
                effective_enablement_state=security_center_management.SecurityCenterService.EnablementState.INHERITED,
            )
        )
        response = await client.get_security_center_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = security_center_management.GetSecurityCenterServiceRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, security_center_management.SecurityCenterService)
    assert response.name == "name_value"
    assert (
        response.intended_enablement_state
        == security_center_management.SecurityCenterService.EnablementState.INHERITED
    )
    assert (
        response.effective_enablement_state
        == security_center_management.SecurityCenterService.EnablementState.INHERITED
    )


@pytest.mark.asyncio
async def test_get_security_center_service_async_from_dict():
    await test_get_security_center_service_async(request_type=dict)


def test_get_security_center_service_field_headers():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = security_center_management.GetSecurityCenterServiceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_security_center_service), "__call__"
    ) as call:
        call.return_value = security_center_management.SecurityCenterService()
        client.get_security_center_service(request)

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
async def test_get_security_center_service_field_headers_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = security_center_management.GetSecurityCenterServiceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_security_center_service), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SecurityCenterService()
        )
        await client.get_security_center_service(request)

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


def test_get_security_center_service_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_security_center_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = security_center_management.SecurityCenterService()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_security_center_service(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_security_center_service_flattened_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_security_center_service(
            security_center_management.GetSecurityCenterServiceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_security_center_service_flattened_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_security_center_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = security_center_management.SecurityCenterService()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SecurityCenterService()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_security_center_service(
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
async def test_get_security_center_service_flattened_error_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_security_center_service(
            security_center_management.GetSecurityCenterServiceRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.ListSecurityCenterServicesRequest,
        dict,
    ],
)
def test_list_security_center_services(request_type, transport: str = "grpc"):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_center_services), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.ListSecurityCenterServicesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = client.list_security_center_services(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = security_center_management.ListSecurityCenterServicesRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSecurityCenterServicesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_security_center_services_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_center_services), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_security_center_services()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == security_center_management.ListSecurityCenterServicesRequest()


def test_list_security_center_services_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = security_center_management.ListSecurityCenterServicesRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_center_services), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_security_center_services(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == security_center_management.ListSecurityCenterServicesRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_security_center_services_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_security_center_services
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_security_center_services
        ] = mock_rpc
        request = {}
        client.list_security_center_services(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_security_center_services(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_security_center_services_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_center_services), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListSecurityCenterServicesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_security_center_services()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == security_center_management.ListSecurityCenterServicesRequest()


@pytest.mark.asyncio
async def test_list_security_center_services_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_security_center_services
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_security_center_services
        ] = mock_object

        request = {}
        await client.list_security_center_services(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_security_center_services(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_security_center_services_async(
    transport: str = "grpc_asyncio",
    request_type=security_center_management.ListSecurityCenterServicesRequest,
):
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_center_services), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListSecurityCenterServicesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_security_center_services(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = security_center_management.ListSecurityCenterServicesRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSecurityCenterServicesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_security_center_services_async_from_dict():
    await test_list_security_center_services_async(request_type=dict)


def test_list_security_center_services_field_headers():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = security_center_management.ListSecurityCenterServicesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_center_services), "__call__"
    ) as call:
        call.return_value = (
            security_center_management.ListSecurityCenterServicesResponse()
        )
        client.list_security_center_services(request)

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
async def test_list_security_center_services_field_headers_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = security_center_management.ListSecurityCenterServicesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_center_services), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListSecurityCenterServicesResponse()
        )
        await client.list_security_center_services(request)

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


def test_list_security_center_services_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_center_services), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.ListSecurityCenterServicesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_security_center_services(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_security_center_services_flattened_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_security_center_services(
            security_center_management.ListSecurityCenterServicesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_security_center_services_flattened_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_center_services), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            security_center_management.ListSecurityCenterServicesResponse()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.ListSecurityCenterServicesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_security_center_services(
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
async def test_list_security_center_services_flattened_error_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_security_center_services(
            security_center_management.ListSecurityCenterServicesRequest(),
            parent="parent_value",
        )


def test_list_security_center_services_pager(transport_name: str = "grpc"):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_center_services), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListSecurityCenterServicesResponse(
                security_center_services=[
                    security_center_management.SecurityCenterService(),
                    security_center_management.SecurityCenterService(),
                    security_center_management.SecurityCenterService(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListSecurityCenterServicesResponse(
                security_center_services=[],
                next_page_token="def",
            ),
            security_center_management.ListSecurityCenterServicesResponse(
                security_center_services=[
                    security_center_management.SecurityCenterService(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListSecurityCenterServicesResponse(
                security_center_services=[
                    security_center_management.SecurityCenterService(),
                    security_center_management.SecurityCenterService(),
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
        pager = client.list_security_center_services(
            request={}, retry=retry, timeout=timeout
        )

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, security_center_management.SecurityCenterService)
            for i in results
        )


def test_list_security_center_services_pages(transport_name: str = "grpc"):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_center_services), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListSecurityCenterServicesResponse(
                security_center_services=[
                    security_center_management.SecurityCenterService(),
                    security_center_management.SecurityCenterService(),
                    security_center_management.SecurityCenterService(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListSecurityCenterServicesResponse(
                security_center_services=[],
                next_page_token="def",
            ),
            security_center_management.ListSecurityCenterServicesResponse(
                security_center_services=[
                    security_center_management.SecurityCenterService(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListSecurityCenterServicesResponse(
                security_center_services=[
                    security_center_management.SecurityCenterService(),
                    security_center_management.SecurityCenterService(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_security_center_services(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_security_center_services_async_pager():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_center_services),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListSecurityCenterServicesResponse(
                security_center_services=[
                    security_center_management.SecurityCenterService(),
                    security_center_management.SecurityCenterService(),
                    security_center_management.SecurityCenterService(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListSecurityCenterServicesResponse(
                security_center_services=[],
                next_page_token="def",
            ),
            security_center_management.ListSecurityCenterServicesResponse(
                security_center_services=[
                    security_center_management.SecurityCenterService(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListSecurityCenterServicesResponse(
                security_center_services=[
                    security_center_management.SecurityCenterService(),
                    security_center_management.SecurityCenterService(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_security_center_services(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, security_center_management.SecurityCenterService)
            for i in responses
        )


@pytest.mark.asyncio
async def test_list_security_center_services_async_pages():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_security_center_services),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            security_center_management.ListSecurityCenterServicesResponse(
                security_center_services=[
                    security_center_management.SecurityCenterService(),
                    security_center_management.SecurityCenterService(),
                    security_center_management.SecurityCenterService(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListSecurityCenterServicesResponse(
                security_center_services=[],
                next_page_token="def",
            ),
            security_center_management.ListSecurityCenterServicesResponse(
                security_center_services=[
                    security_center_management.SecurityCenterService(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListSecurityCenterServicesResponse(
                security_center_services=[
                    security_center_management.SecurityCenterService(),
                    security_center_management.SecurityCenterService(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_security_center_services(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.UpdateSecurityCenterServiceRequest,
        dict,
    ],
)
def test_update_security_center_service(request_type, transport: str = "grpc"):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_center_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = security_center_management.SecurityCenterService(
            name="name_value",
            intended_enablement_state=security_center_management.SecurityCenterService.EnablementState.INHERITED,
            effective_enablement_state=security_center_management.SecurityCenterService.EnablementState.INHERITED,
        )
        response = client.update_security_center_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = security_center_management.UpdateSecurityCenterServiceRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, security_center_management.SecurityCenterService)
    assert response.name == "name_value"
    assert (
        response.intended_enablement_state
        == security_center_management.SecurityCenterService.EnablementState.INHERITED
    )
    assert (
        response.effective_enablement_state
        == security_center_management.SecurityCenterService.EnablementState.INHERITED
    )


def test_update_security_center_service_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_center_service), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_security_center_service()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0] == security_center_management.UpdateSecurityCenterServiceRequest()
        )


def test_update_security_center_service_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = security_center_management.UpdateSecurityCenterServiceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_center_service), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_security_center_service(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0] == security_center_management.UpdateSecurityCenterServiceRequest()
        )


def test_update_security_center_service_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_security_center_service
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_security_center_service
        ] = mock_rpc
        request = {}
        client.update_security_center_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_security_center_service(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_security_center_service_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_center_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SecurityCenterService(
                name="name_value",
                intended_enablement_state=security_center_management.SecurityCenterService.EnablementState.INHERITED,
                effective_enablement_state=security_center_management.SecurityCenterService.EnablementState.INHERITED,
            )
        )
        response = await client.update_security_center_service()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0] == security_center_management.UpdateSecurityCenterServiceRequest()
        )


@pytest.mark.asyncio
async def test_update_security_center_service_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_security_center_service
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_security_center_service
        ] = mock_object

        request = {}
        await client.update_security_center_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.update_security_center_service(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_update_security_center_service_async(
    transport: str = "grpc_asyncio",
    request_type=security_center_management.UpdateSecurityCenterServiceRequest,
):
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_center_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SecurityCenterService(
                name="name_value",
                intended_enablement_state=security_center_management.SecurityCenterService.EnablementState.INHERITED,
                effective_enablement_state=security_center_management.SecurityCenterService.EnablementState.INHERITED,
            )
        )
        response = await client.update_security_center_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = security_center_management.UpdateSecurityCenterServiceRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, security_center_management.SecurityCenterService)
    assert response.name == "name_value"
    assert (
        response.intended_enablement_state
        == security_center_management.SecurityCenterService.EnablementState.INHERITED
    )
    assert (
        response.effective_enablement_state
        == security_center_management.SecurityCenterService.EnablementState.INHERITED
    )


@pytest.mark.asyncio
async def test_update_security_center_service_async_from_dict():
    await test_update_security_center_service_async(request_type=dict)


def test_update_security_center_service_field_headers():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = security_center_management.UpdateSecurityCenterServiceRequest()

    request.security_center_service.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_center_service), "__call__"
    ) as call:
        call.return_value = security_center_management.SecurityCenterService()
        client.update_security_center_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "security_center_service.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_security_center_service_field_headers_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = security_center_management.UpdateSecurityCenterServiceRequest()

    request.security_center_service.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_center_service), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SecurityCenterService()
        )
        await client.update_security_center_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "security_center_service.name=name_value",
    ) in kw["metadata"]


def test_update_security_center_service_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_center_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = security_center_management.SecurityCenterService()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_security_center_service(
            security_center_service=security_center_management.SecurityCenterService(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].security_center_service
        mock_val = security_center_management.SecurityCenterService(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_security_center_service_flattened_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_security_center_service(
            security_center_management.UpdateSecurityCenterServiceRequest(),
            security_center_service=security_center_management.SecurityCenterService(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_security_center_service_flattened_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_center_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = security_center_management.SecurityCenterService()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            security_center_management.SecurityCenterService()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_security_center_service(
            security_center_service=security_center_management.SecurityCenterService(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].security_center_service
        mock_val = security_center_management.SecurityCenterService(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_security_center_service_flattened_error_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_security_center_service(
            security_center_management.UpdateSecurityCenterServiceRequest(),
            security_center_service=security_center_management.SecurityCenterService(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest,
        dict,
    ],
)
def test_list_effective_security_health_analytics_custom_modules_rest(request_type):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_effective_security_health_analytics_custom_modules(
            request
        )

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, pagers.ListEffectiveSecurityHealthAnalyticsCustomModulesPager
    )
    assert response.next_page_token == "next_page_token_value"


def test_list_effective_security_health_analytics_custom_modules_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_effective_security_health_analytics_custom_modules
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_effective_security_health_analytics_custom_modules
        ] = mock_rpc

        request = {}
        client.list_effective_security_health_analytics_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_effective_security_health_analytics_custom_modules(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_effective_security_health_analytics_custom_modules_rest_required_fields(
    request_type=security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest,
):
    transport_class = transports.SecurityCenterManagementRestTransport

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
    ).list_effective_security_health_analytics_custom_modules._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_effective_security_health_analytics_custom_modules._get_unset_required_fields(
        jsonified_request
    )
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

    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = (
        security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse()
    )
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
            return_value = security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_effective_security_health_analytics_custom_modules(
                request
            )

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_effective_security_health_analytics_custom_modules_rest_unset_required_fields():
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_effective_security_health_analytics_custom_modules._get_unset_required_fields(
        {}
    )
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
def test_list_effective_security_health_analytics_custom_modules_rest_interceptors(
    null_interceptor,
):
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SecurityCenterManagementRestInterceptor(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "post_list_effective_security_health_analytics_custom_modules",
    ) as post, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "pre_list_effective_security_health_analytics_custom_modules",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest.pb(
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest()
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
        req.return_value._content = security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse.to_json(
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse()
        )

        request = (
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest()
        )
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse()
        )

        client.list_effective_security_health_analytics_custom_modules(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_effective_security_health_analytics_custom_modules_rest_bad_request(
    transport: str = "rest",
    request_type=security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest,
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_effective_security_health_analytics_custom_modules(request)


def test_list_effective_security_health_analytics_custom_modules_rest_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = (
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse()
        )

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
        return_value = security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_effective_security_health_analytics_custom_modules(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/effectiveSecurityHealthAnalyticsCustomModules"
            % client.transport._host,
            args[1],
        )


def test_list_effective_security_health_analytics_custom_modules_rest_flattened_error(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_effective_security_health_analytics_custom_modules(
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest(),
            parent="parent_value",
        )


def test_list_effective_security_health_analytics_custom_modules_rest_pager(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                effective_security_health_analytics_custom_modules=[
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                effective_security_health_analytics_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                effective_security_health_analytics_custom_modules=[
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(
                effective_security_health_analytics_custom_modules=[
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                    security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse.to_json(
                x
            )
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_effective_security_health_analytics_custom_modules(
            request=sample_request
        )

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(
                i,
                security_center_management.EffectiveSecurityHealthAnalyticsCustomModule,
            )
            for i in results
        )

        pages = list(
            client.list_effective_security_health_analytics_custom_modules(
                request=sample_request
            ).pages
        )
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest,
        dict,
    ],
)
def test_get_effective_security_health_analytics_custom_module_rest(request_type):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/effectiveSecurityHealthAnalyticsCustomModules/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.EffectiveSecurityHealthAnalyticsCustomModule(
            name="name_value",
            enablement_state=security_center_management.EffectiveSecurityHealthAnalyticsCustomModule.EnablementState.ENABLED,
            display_name="display_name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = (
            security_center_management.EffectiveSecurityHealthAnalyticsCustomModule.pb(
                return_value
            )
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_effective_security_health_analytics_custom_module(request)

    # Establish that the response is the type that we expect.
    assert isinstance(
        response,
        security_center_management.EffectiveSecurityHealthAnalyticsCustomModule,
    )
    assert response.name == "name_value"
    assert (
        response.enablement_state
        == security_center_management.EffectiveSecurityHealthAnalyticsCustomModule.EnablementState.ENABLED
    )
    assert response.display_name == "display_name_value"


def test_get_effective_security_health_analytics_custom_module_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_effective_security_health_analytics_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_effective_security_health_analytics_custom_module
        ] = mock_rpc

        request = {}
        client.get_effective_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_effective_security_health_analytics_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_effective_security_health_analytics_custom_module_rest_required_fields(
    request_type=security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest,
):
    transport_class = transports.SecurityCenterManagementRestTransport

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
    ).get_effective_security_health_analytics_custom_module._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_effective_security_health_analytics_custom_module._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = (
        security_center_management.EffectiveSecurityHealthAnalyticsCustomModule()
    )
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
            return_value = security_center_management.EffectiveSecurityHealthAnalyticsCustomModule.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_effective_security_health_analytics_custom_module(
                request
            )

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_effective_security_health_analytics_custom_module_rest_unset_required_fields():
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_effective_security_health_analytics_custom_module._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_effective_security_health_analytics_custom_module_rest_interceptors(
    null_interceptor,
):
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SecurityCenterManagementRestInterceptor(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "post_get_effective_security_health_analytics_custom_module",
    ) as post, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "pre_get_effective_security_health_analytics_custom_module",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest.pb(
            security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest()
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
        req.return_value._content = security_center_management.EffectiveSecurityHealthAnalyticsCustomModule.to_json(
            security_center_management.EffectiveSecurityHealthAnalyticsCustomModule()
        )

        request = (
            security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest()
        )
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            security_center_management.EffectiveSecurityHealthAnalyticsCustomModule()
        )

        client.get_effective_security_health_analytics_custom_module(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_effective_security_health_analytics_custom_module_rest_bad_request(
    transport: str = "rest",
    request_type=security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest,
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/effectiveSecurityHealthAnalyticsCustomModules/sample3"
    }
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
        client.get_effective_security_health_analytics_custom_module(request)


def test_get_effective_security_health_analytics_custom_module_rest_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = (
            security_center_management.EffectiveSecurityHealthAnalyticsCustomModule()
        )

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/effectiveSecurityHealthAnalyticsCustomModules/sample3"
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
        return_value = (
            security_center_management.EffectiveSecurityHealthAnalyticsCustomModule.pb(
                return_value
            )
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_effective_security_health_analytics_custom_module(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/effectiveSecurityHealthAnalyticsCustomModules/*}"
            % client.transport._host,
            args[1],
        )


def test_get_effective_security_health_analytics_custom_module_rest_flattened_error(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_effective_security_health_analytics_custom_module(
            security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest(),
            name="name_value",
        )


def test_get_effective_security_health_analytics_custom_module_rest_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest,
        dict,
    ],
)
def test_list_security_health_analytics_custom_modules_rest(request_type):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = (
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                next_page_token="next_page_token_value",
            )
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_security_health_analytics_custom_modules(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSecurityHealthAnalyticsCustomModulesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_security_health_analytics_custom_modules_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_security_health_analytics_custom_modules
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_security_health_analytics_custom_modules
        ] = mock_rpc

        request = {}
        client.list_security_health_analytics_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_security_health_analytics_custom_modules(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_security_health_analytics_custom_modules_rest_required_fields(
    request_type=security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest,
):
    transport_class = transports.SecurityCenterManagementRestTransport

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
    ).list_security_health_analytics_custom_modules._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_security_health_analytics_custom_modules._get_unset_required_fields(
        jsonified_request
    )
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

    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = (
        security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse()
    )
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
            return_value = security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_security_health_analytics_custom_modules(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_security_health_analytics_custom_modules_rest_unset_required_fields():
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_security_health_analytics_custom_modules._get_unset_required_fields(
        {}
    )
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
def test_list_security_health_analytics_custom_modules_rest_interceptors(
    null_interceptor,
):
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SecurityCenterManagementRestInterceptor(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "post_list_security_health_analytics_custom_modules",
    ) as post, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "pre_list_security_health_analytics_custom_modules",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest.pb(
            security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest()
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
        req.return_value._content = security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse.to_json(
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse()
        )

        request = (
            security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest()
        )
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse()
        )

        client.list_security_health_analytics_custom_modules(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_security_health_analytics_custom_modules_rest_bad_request(
    transport: str = "rest",
    request_type=security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest,
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_security_health_analytics_custom_modules(request)


def test_list_security_health_analytics_custom_modules_rest_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = (
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse()
        )

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
        return_value = security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_security_health_analytics_custom_modules(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/securityHealthAnalyticsCustomModules"
            % client.transport._host,
            args[1],
        )


def test_list_security_health_analytics_custom_modules_rest_flattened_error(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_security_health_analytics_custom_modules(
            security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest(),
            parent="parent_value",
        )


def test_list_security_health_analytics_custom_modules_rest_pager(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse.to_json(
                x
            )
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_security_health_analytics_custom_modules(
            request=sample_request
        )

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(
                i, security_center_management.SecurityHealthAnalyticsCustomModule
            )
            for i in results
        )

        pages = list(
            client.list_security_health_analytics_custom_modules(
                request=sample_request
            ).pages
        )
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest,
        dict,
    ],
)
def test_list_descendant_security_health_analytics_custom_modules_rest(request_type):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_descendant_security_health_analytics_custom_modules(
            request
        )

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, pagers.ListDescendantSecurityHealthAnalyticsCustomModulesPager
    )
    assert response.next_page_token == "next_page_token_value"


def test_list_descendant_security_health_analytics_custom_modules_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_descendant_security_health_analytics_custom_modules
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_descendant_security_health_analytics_custom_modules
        ] = mock_rpc

        request = {}
        client.list_descendant_security_health_analytics_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_descendant_security_health_analytics_custom_modules(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_descendant_security_health_analytics_custom_modules_rest_required_fields(
    request_type=security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest,
):
    transport_class = transports.SecurityCenterManagementRestTransport

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
    ).list_descendant_security_health_analytics_custom_modules._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_descendant_security_health_analytics_custom_modules._get_unset_required_fields(
        jsonified_request
    )
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

    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = (
        security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse()
    )
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
            return_value = security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_descendant_security_health_analytics_custom_modules(
                request
            )

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_descendant_security_health_analytics_custom_modules_rest_unset_required_fields():
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_descendant_security_health_analytics_custom_modules._get_unset_required_fields(
        {}
    )
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
def test_list_descendant_security_health_analytics_custom_modules_rest_interceptors(
    null_interceptor,
):
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SecurityCenterManagementRestInterceptor(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "post_list_descendant_security_health_analytics_custom_modules",
    ) as post, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "pre_list_descendant_security_health_analytics_custom_modules",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest.pb(
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest()
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
        req.return_value._content = security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse.to_json(
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse()
        )

        request = (
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest()
        )
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse()
        )

        client.list_descendant_security_health_analytics_custom_modules(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_descendant_security_health_analytics_custom_modules_rest_bad_request(
    transport: str = "rest",
    request_type=security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest,
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_descendant_security_health_analytics_custom_modules(request)


def test_list_descendant_security_health_analytics_custom_modules_rest_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = (
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse()
        )

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
        return_value = security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_descendant_security_health_analytics_custom_modules(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/securityHealthAnalyticsCustomModules:listDescendant"
            % client.transport._host,
            args[1],
        )


def test_list_descendant_security_health_analytics_custom_modules_rest_flattened_error(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_descendant_security_health_analytics_custom_modules(
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest(),
            parent="parent_value",
        )


def test_list_descendant_security_health_analytics_custom_modules_rest_pager(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse(
                security_health_analytics_custom_modules=[
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                    security_center_management.SecurityHealthAnalyticsCustomModule(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse.to_json(
                x
            )
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_descendant_security_health_analytics_custom_modules(
            request=sample_request
        )

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(
                i, security_center_management.SecurityHealthAnalyticsCustomModule
            )
            for i in results
        )

        pages = list(
            client.list_descendant_security_health_analytics_custom_modules(
                request=sample_request
            ).pages
        )
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest,
        dict,
    ],
)
def test_get_security_health_analytics_custom_module_rest(request_type):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/securityHealthAnalyticsCustomModules/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.SecurityHealthAnalyticsCustomModule(
            name="name_value",
            display_name="display_name_value",
            enablement_state=security_center_management.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED,
            last_editor="last_editor_value",
            ancestor_module="ancestor_module_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = (
            security_center_management.SecurityHealthAnalyticsCustomModule.pb(
                return_value
            )
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_security_health_analytics_custom_module(request)

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, security_center_management.SecurityHealthAnalyticsCustomModule
    )
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert (
        response.enablement_state
        == security_center_management.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED
    )
    assert response.last_editor == "last_editor_value"
    assert response.ancestor_module == "ancestor_module_value"


def test_get_security_health_analytics_custom_module_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_security_health_analytics_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_security_health_analytics_custom_module
        ] = mock_rpc

        request = {}
        client.get_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_security_health_analytics_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_security_health_analytics_custom_module_rest_required_fields(
    request_type=security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest,
):
    transport_class = transports.SecurityCenterManagementRestTransport

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
    ).get_security_health_analytics_custom_module._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_security_health_analytics_custom_module._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = security_center_management.SecurityHealthAnalyticsCustomModule()
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
            return_value = (
                security_center_management.SecurityHealthAnalyticsCustomModule.pb(
                    return_value
                )
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_security_health_analytics_custom_module(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_security_health_analytics_custom_module_rest_unset_required_fields():
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_security_health_analytics_custom_module._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_security_health_analytics_custom_module_rest_interceptors(
    null_interceptor,
):
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SecurityCenterManagementRestInterceptor(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "post_get_security_health_analytics_custom_module",
    ) as post, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "pre_get_security_health_analytics_custom_module",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest.pb(
            security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest()
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
            security_center_management.SecurityHealthAnalyticsCustomModule.to_json(
                security_center_management.SecurityHealthAnalyticsCustomModule()
            )
        )

        request = (
            security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest()
        )
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            security_center_management.SecurityHealthAnalyticsCustomModule()
        )

        client.get_security_health_analytics_custom_module(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_security_health_analytics_custom_module_rest_bad_request(
    transport: str = "rest",
    request_type=security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest,
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/securityHealthAnalyticsCustomModules/sample3"
    }
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
        client.get_security_health_analytics_custom_module(request)


def test_get_security_health_analytics_custom_module_rest_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.SecurityHealthAnalyticsCustomModule()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/securityHealthAnalyticsCustomModules/sample3"
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
        return_value = (
            security_center_management.SecurityHealthAnalyticsCustomModule.pb(
                return_value
            )
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_security_health_analytics_custom_module(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/securityHealthAnalyticsCustomModules/*}"
            % client.transport._host,
            args[1],
        )


def test_get_security_health_analytics_custom_module_rest_flattened_error(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_security_health_analytics_custom_module(
            security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest(),
            name="name_value",
        )


def test_get_security_health_analytics_custom_module_rest_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest,
        dict,
    ],
)
def test_create_security_health_analytics_custom_module_rest(request_type):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["security_health_analytics_custom_module"] = {
        "name": "name_value",
        "display_name": "display_name_value",
        "enablement_state": 1,
        "update_time": {"seconds": 751, "nanos": 543},
        "last_editor": "last_editor_value",
        "ancestor_module": "ancestor_module_value",
        "custom_config": {
            "predicate": {
                "expression": "expression_value",
                "title": "title_value",
                "description": "description_value",
                "location": "location_value",
            },
            "custom_output": {
                "properties": [{"name": "name_value", "value_expression": {}}]
            },
            "resource_selector": {
                "resource_types": ["resource_types_value1", "resource_types_value2"]
            },
            "severity": 1,
            "description": "description_value",
            "recommendation": "recommendation_value",
        },
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest.meta.fields[
        "security_health_analytics_custom_module"
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
        "security_health_analytics_custom_module"
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
                    0,
                    len(request_init["security_health_analytics_custom_module"][field]),
                ):
                    del request_init["security_health_analytics_custom_module"][field][
                        i
                    ][subfield]
            else:
                del request_init["security_health_analytics_custom_module"][field][
                    subfield
                ]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.SecurityHealthAnalyticsCustomModule(
            name="name_value",
            display_name="display_name_value",
            enablement_state=security_center_management.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED,
            last_editor="last_editor_value",
            ancestor_module="ancestor_module_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = (
            security_center_management.SecurityHealthAnalyticsCustomModule.pb(
                return_value
            )
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_security_health_analytics_custom_module(request)

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, security_center_management.SecurityHealthAnalyticsCustomModule
    )
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert (
        response.enablement_state
        == security_center_management.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED
    )
    assert response.last_editor == "last_editor_value"
    assert response.ancestor_module == "ancestor_module_value"


def test_create_security_health_analytics_custom_module_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_security_health_analytics_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_security_health_analytics_custom_module
        ] = mock_rpc

        request = {}
        client.create_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_security_health_analytics_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_security_health_analytics_custom_module_rest_required_fields(
    request_type=security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest,
):
    transport_class = transports.SecurityCenterManagementRestTransport

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
    ).create_security_health_analytics_custom_module._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_security_health_analytics_custom_module._get_unset_required_fields(
        jsonified_request
    )
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("validate_only",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = security_center_management.SecurityHealthAnalyticsCustomModule()
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
            return_value = (
                security_center_management.SecurityHealthAnalyticsCustomModule.pb(
                    return_value
                )
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_security_health_analytics_custom_module(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_security_health_analytics_custom_module_rest_unset_required_fields():
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_security_health_analytics_custom_module._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (
        set(("validateOnly",))
        & set(
            (
                "parent",
                "securityHealthAnalyticsCustomModule",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_security_health_analytics_custom_module_rest_interceptors(
    null_interceptor,
):
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SecurityCenterManagementRestInterceptor(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "post_create_security_health_analytics_custom_module",
    ) as post, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "pre_create_security_health_analytics_custom_module",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest.pb(
            security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest()
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
            security_center_management.SecurityHealthAnalyticsCustomModule.to_json(
                security_center_management.SecurityHealthAnalyticsCustomModule()
            )
        )

        request = (
            security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest()
        )
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            security_center_management.SecurityHealthAnalyticsCustomModule()
        )

        client.create_security_health_analytics_custom_module(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_security_health_analytics_custom_module_rest_bad_request(
    transport: str = "rest",
    request_type=security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest,
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.create_security_health_analytics_custom_module(request)


def test_create_security_health_analytics_custom_module_rest_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.SecurityHealthAnalyticsCustomModule()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            security_health_analytics_custom_module=security_center_management.SecurityHealthAnalyticsCustomModule(
                name="name_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = (
            security_center_management.SecurityHealthAnalyticsCustomModule.pb(
                return_value
            )
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_security_health_analytics_custom_module(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/securityHealthAnalyticsCustomModules"
            % client.transport._host,
            args[1],
        )


def test_create_security_health_analytics_custom_module_rest_flattened_error(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_security_health_analytics_custom_module(
            security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest(),
            parent="parent_value",
            security_health_analytics_custom_module=security_center_management.SecurityHealthAnalyticsCustomModule(
                name="name_value"
            ),
        )


def test_create_security_health_analytics_custom_module_rest_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest,
        dict,
    ],
)
def test_update_security_health_analytics_custom_module_rest(request_type):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "security_health_analytics_custom_module": {
            "name": "projects/sample1/locations/sample2/securityHealthAnalyticsCustomModules/sample3"
        }
    }
    request_init["security_health_analytics_custom_module"] = {
        "name": "projects/sample1/locations/sample2/securityHealthAnalyticsCustomModules/sample3",
        "display_name": "display_name_value",
        "enablement_state": 1,
        "update_time": {"seconds": 751, "nanos": 543},
        "last_editor": "last_editor_value",
        "ancestor_module": "ancestor_module_value",
        "custom_config": {
            "predicate": {
                "expression": "expression_value",
                "title": "title_value",
                "description": "description_value",
                "location": "location_value",
            },
            "custom_output": {
                "properties": [{"name": "name_value", "value_expression": {}}]
            },
            "resource_selector": {
                "resource_types": ["resource_types_value1", "resource_types_value2"]
            },
            "severity": 1,
            "description": "description_value",
            "recommendation": "recommendation_value",
        },
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest.meta.fields[
        "security_health_analytics_custom_module"
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
        "security_health_analytics_custom_module"
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
                    0,
                    len(request_init["security_health_analytics_custom_module"][field]),
                ):
                    del request_init["security_health_analytics_custom_module"][field][
                        i
                    ][subfield]
            else:
                del request_init["security_health_analytics_custom_module"][field][
                    subfield
                ]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.SecurityHealthAnalyticsCustomModule(
            name="name_value",
            display_name="display_name_value",
            enablement_state=security_center_management.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED,
            last_editor="last_editor_value",
            ancestor_module="ancestor_module_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = (
            security_center_management.SecurityHealthAnalyticsCustomModule.pb(
                return_value
            )
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_security_health_analytics_custom_module(request)

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, security_center_management.SecurityHealthAnalyticsCustomModule
    )
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert (
        response.enablement_state
        == security_center_management.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED
    )
    assert response.last_editor == "last_editor_value"
    assert response.ancestor_module == "ancestor_module_value"


def test_update_security_health_analytics_custom_module_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_security_health_analytics_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_security_health_analytics_custom_module
        ] = mock_rpc

        request = {}
        client.update_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_security_health_analytics_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_update_security_health_analytics_custom_module_rest_required_fields(
    request_type=security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest,
):
    transport_class = transports.SecurityCenterManagementRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_security_health_analytics_custom_module._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_security_health_analytics_custom_module._get_unset_required_fields(
        jsonified_request
    )
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "update_mask",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = security_center_management.SecurityHealthAnalyticsCustomModule()
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
            return_value = (
                security_center_management.SecurityHealthAnalyticsCustomModule.pb(
                    return_value
                )
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_security_health_analytics_custom_module(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_security_health_analytics_custom_module_rest_unset_required_fields():
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_security_health_analytics_custom_module._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (
        set(
            (
                "updateMask",
                "validateOnly",
            )
        )
        & set(
            (
                "updateMask",
                "securityHealthAnalyticsCustomModule",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_security_health_analytics_custom_module_rest_interceptors(
    null_interceptor,
):
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SecurityCenterManagementRestInterceptor(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "post_update_security_health_analytics_custom_module",
    ) as post, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "pre_update_security_health_analytics_custom_module",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest.pb(
            security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest()
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
            security_center_management.SecurityHealthAnalyticsCustomModule.to_json(
                security_center_management.SecurityHealthAnalyticsCustomModule()
            )
        )

        request = (
            security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest()
        )
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            security_center_management.SecurityHealthAnalyticsCustomModule()
        )

        client.update_security_health_analytics_custom_module(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_security_health_analytics_custom_module_rest_bad_request(
    transport: str = "rest",
    request_type=security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest,
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "security_health_analytics_custom_module": {
            "name": "projects/sample1/locations/sample2/securityHealthAnalyticsCustomModules/sample3"
        }
    }
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
        client.update_security_health_analytics_custom_module(request)


def test_update_security_health_analytics_custom_module_rest_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.SecurityHealthAnalyticsCustomModule()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "security_health_analytics_custom_module": {
                "name": "projects/sample1/locations/sample2/securityHealthAnalyticsCustomModules/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            security_health_analytics_custom_module=security_center_management.SecurityHealthAnalyticsCustomModule(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = (
            security_center_management.SecurityHealthAnalyticsCustomModule.pb(
                return_value
            )
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_security_health_analytics_custom_module(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{security_health_analytics_custom_module.name=projects/*/locations/*/securityHealthAnalyticsCustomModules/*}"
            % client.transport._host,
            args[1],
        )


def test_update_security_health_analytics_custom_module_rest_flattened_error(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_security_health_analytics_custom_module(
            security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest(),
            security_health_analytics_custom_module=security_center_management.SecurityHealthAnalyticsCustomModule(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_security_health_analytics_custom_module_rest_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest,
        dict,
    ],
)
def test_delete_security_health_analytics_custom_module_rest(request_type):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/securityHealthAnalyticsCustomModules/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_security_health_analytics_custom_module(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_security_health_analytics_custom_module_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_security_health_analytics_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_security_health_analytics_custom_module
        ] = mock_rpc

        request = {}
        client.delete_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_security_health_analytics_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_security_health_analytics_custom_module_rest_required_fields(
    request_type=security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest,
):
    transport_class = transports.SecurityCenterManagementRestTransport

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
    ).delete_security_health_analytics_custom_module._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_security_health_analytics_custom_module._get_unset_required_fields(
        jsonified_request
    )
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("validate_only",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SecurityCenterManagementClient(
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

            response = client.delete_security_health_analytics_custom_module(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_security_health_analytics_custom_module_rest_unset_required_fields():
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_security_health_analytics_custom_module._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (set(("validateOnly",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_security_health_analytics_custom_module_rest_interceptors(
    null_interceptor,
):
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SecurityCenterManagementRestInterceptor(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "pre_delete_security_health_analytics_custom_module",
    ) as pre:
        pre.assert_not_called()
        pb_message = security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest.pb(
            security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest()
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

        request = (
            security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest()
        )
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_security_health_analytics_custom_module(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_security_health_analytics_custom_module_rest_bad_request(
    transport: str = "rest",
    request_type=security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest,
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/securityHealthAnalyticsCustomModules/sample3"
    }
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
        client.delete_security_health_analytics_custom_module(request)


def test_delete_security_health_analytics_custom_module_rest_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/securityHealthAnalyticsCustomModules/sample3"
        }

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

        client.delete_security_health_analytics_custom_module(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/securityHealthAnalyticsCustomModules/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_security_health_analytics_custom_module_rest_flattened_error(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_security_health_analytics_custom_module(
            security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest(),
            name="name_value",
        )


def test_delete_security_health_analytics_custom_module_rest_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest,
        dict,
    ],
)
def test_simulate_security_health_analytics_custom_module_rest(request_type):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = (
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse()
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.simulate_security_health_analytics_custom_module(request)

    # Establish that the response is the type that we expect.
    assert isinstance(
        response,
        security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse,
    )


def test_simulate_security_health_analytics_custom_module_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.simulate_security_health_analytics_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.simulate_security_health_analytics_custom_module
        ] = mock_rpc

        request = {}
        client.simulate_security_health_analytics_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.simulate_security_health_analytics_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_simulate_security_health_analytics_custom_module_rest_required_fields(
    request_type=security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest,
):
    transport_class = transports.SecurityCenterManagementRestTransport

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
    ).simulate_security_health_analytics_custom_module._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).simulate_security_health_analytics_custom_module._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = (
        security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse()
    )
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
            return_value = security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.simulate_security_health_analytics_custom_module(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_simulate_security_health_analytics_custom_module_rest_unset_required_fields():
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.simulate_security_health_analytics_custom_module._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "customConfig",
                "resource",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_simulate_security_health_analytics_custom_module_rest_interceptors(
    null_interceptor,
):
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SecurityCenterManagementRestInterceptor(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "post_simulate_security_health_analytics_custom_module",
    ) as post, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "pre_simulate_security_health_analytics_custom_module",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest.pb(
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest()
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
        req.return_value._content = security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse.to_json(
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse()
        )

        request = (
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest()
        )
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse()
        )

        client.simulate_security_health_analytics_custom_module(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_simulate_security_health_analytics_custom_module_rest_bad_request(
    transport: str = "rest",
    request_type=security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest,
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.simulate_security_health_analytics_custom_module(request)


def test_simulate_security_health_analytics_custom_module_rest_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = (
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse()
        )

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            custom_config=security_center_management.CustomConfig(
                predicate=expr_pb2.Expr(expression="expression_value")
            ),
            resource=security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest.SimulatedResource(
                resource_type="resource_type_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.simulate_security_health_analytics_custom_module(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/securityHealthAnalyticsCustomModules:simulate"
            % client.transport._host,
            args[1],
        )


def test_simulate_security_health_analytics_custom_module_rest_flattened_error(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.simulate_security_health_analytics_custom_module(
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest(),
            parent="parent_value",
            custom_config=security_center_management.CustomConfig(
                predicate=expr_pb2.Expr(expression="expression_value")
            ),
            resource=security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest.SimulatedResource(
                resource_type="resource_type_value"
            ),
        )


def test_simulate_security_health_analytics_custom_module_rest_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest,
        dict,
    ],
)
def test_list_effective_event_threat_detection_custom_modules_rest(request_type):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_effective_event_threat_detection_custom_modules(request)

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, pagers.ListEffectiveEventThreatDetectionCustomModulesPager
    )
    assert response.next_page_token == "next_page_token_value"


def test_list_effective_event_threat_detection_custom_modules_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_effective_event_threat_detection_custom_modules
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_effective_event_threat_detection_custom_modules
        ] = mock_rpc

        request = {}
        client.list_effective_event_threat_detection_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_effective_event_threat_detection_custom_modules(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_effective_event_threat_detection_custom_modules_rest_required_fields(
    request_type=security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest,
):
    transport_class = transports.SecurityCenterManagementRestTransport

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
    ).list_effective_event_threat_detection_custom_modules._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_effective_event_threat_detection_custom_modules._get_unset_required_fields(
        jsonified_request
    )
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

    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = (
        security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse()
    )
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
            return_value = security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_effective_event_threat_detection_custom_modules(
                request
            )

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_effective_event_threat_detection_custom_modules_rest_unset_required_fields():
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_effective_event_threat_detection_custom_modules._get_unset_required_fields(
        {}
    )
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
def test_list_effective_event_threat_detection_custom_modules_rest_interceptors(
    null_interceptor,
):
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SecurityCenterManagementRestInterceptor(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "post_list_effective_event_threat_detection_custom_modules",
    ) as post, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "pre_list_effective_event_threat_detection_custom_modules",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest.pb(
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest()
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
        req.return_value._content = security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse.to_json(
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse()
        )

        request = (
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest()
        )
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse()
        )

        client.list_effective_event_threat_detection_custom_modules(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_effective_event_threat_detection_custom_modules_rest_bad_request(
    transport: str = "rest",
    request_type=security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest,
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_effective_event_threat_detection_custom_modules(request)


def test_list_effective_event_threat_detection_custom_modules_rest_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = (
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse()
        )

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
        return_value = security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_effective_event_threat_detection_custom_modules(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/effectiveEventThreatDetectionCustomModules"
            % client.transport._host,
            args[1],
        )


def test_list_effective_event_threat_detection_custom_modules_rest_flattened_error(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_effective_event_threat_detection_custom_modules(
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest(),
            parent="parent_value",
        )


def test_list_effective_event_threat_detection_custom_modules_rest_pager(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                effective_event_threat_detection_custom_modules=[
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                effective_event_threat_detection_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                effective_event_threat_detection_custom_modules=[
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse(
                effective_event_threat_detection_custom_modules=[
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                    security_center_management.EffectiveEventThreatDetectionCustomModule(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse.to_json(
                x
            )
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_effective_event_threat_detection_custom_modules(
            request=sample_request
        )

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(
                i, security_center_management.EffectiveEventThreatDetectionCustomModule
            )
            for i in results
        )

        pages = list(
            client.list_effective_event_threat_detection_custom_modules(
                request=sample_request
            ).pages
        )
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest,
        dict,
    ],
)
def test_get_effective_event_threat_detection_custom_module_rest(request_type):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/effectiveEventThreatDetectionCustomModules/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.EffectiveEventThreatDetectionCustomModule(
            name="name_value",
            enablement_state=security_center_management.EffectiveEventThreatDetectionCustomModule.EnablementState.ENABLED,
            type_="type__value",
            display_name="display_name_value",
            description="description_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = (
            security_center_management.EffectiveEventThreatDetectionCustomModule.pb(
                return_value
            )
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_effective_event_threat_detection_custom_module(request)

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, security_center_management.EffectiveEventThreatDetectionCustomModule
    )
    assert response.name == "name_value"
    assert (
        response.enablement_state
        == security_center_management.EffectiveEventThreatDetectionCustomModule.EnablementState.ENABLED
    )
    assert response.type_ == "type__value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_get_effective_event_threat_detection_custom_module_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_effective_event_threat_detection_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_effective_event_threat_detection_custom_module
        ] = mock_rpc

        request = {}
        client.get_effective_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_effective_event_threat_detection_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_effective_event_threat_detection_custom_module_rest_required_fields(
    request_type=security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest,
):
    transport_class = transports.SecurityCenterManagementRestTransport

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
    ).get_effective_event_threat_detection_custom_module._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_effective_event_threat_detection_custom_module._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = (
        security_center_management.EffectiveEventThreatDetectionCustomModule()
    )
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
            return_value = (
                security_center_management.EffectiveEventThreatDetectionCustomModule.pb(
                    return_value
                )
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_effective_event_threat_detection_custom_module(
                request
            )

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_effective_event_threat_detection_custom_module_rest_unset_required_fields():
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_effective_event_threat_detection_custom_module._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_effective_event_threat_detection_custom_module_rest_interceptors(
    null_interceptor,
):
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SecurityCenterManagementRestInterceptor(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "post_get_effective_event_threat_detection_custom_module",
    ) as post, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "pre_get_effective_event_threat_detection_custom_module",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest.pb(
            security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest()
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
        req.return_value._content = security_center_management.EffectiveEventThreatDetectionCustomModule.to_json(
            security_center_management.EffectiveEventThreatDetectionCustomModule()
        )

        request = (
            security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest()
        )
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            security_center_management.EffectiveEventThreatDetectionCustomModule()
        )

        client.get_effective_event_threat_detection_custom_module(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_effective_event_threat_detection_custom_module_rest_bad_request(
    transport: str = "rest",
    request_type=security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest,
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/effectiveEventThreatDetectionCustomModules/sample3"
    }
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
        client.get_effective_event_threat_detection_custom_module(request)


def test_get_effective_event_threat_detection_custom_module_rest_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = (
            security_center_management.EffectiveEventThreatDetectionCustomModule()
        )

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/effectiveEventThreatDetectionCustomModules/sample3"
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
        return_value = (
            security_center_management.EffectiveEventThreatDetectionCustomModule.pb(
                return_value
            )
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_effective_event_threat_detection_custom_module(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/effectiveEventThreatDetectionCustomModules/*}"
            % client.transport._host,
            args[1],
        )


def test_get_effective_event_threat_detection_custom_module_rest_flattened_error(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_effective_event_threat_detection_custom_module(
            security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest(),
            name="name_value",
        )


def test_get_effective_event_threat_detection_custom_module_rest_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.ListEventThreatDetectionCustomModulesRequest,
        dict,
    ],
)
def test_list_event_threat_detection_custom_modules_rest(request_type):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = (
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                next_page_token="next_page_token_value",
            )
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = (
            security_center_management.ListEventThreatDetectionCustomModulesResponse.pb(
                return_value
            )
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_event_threat_detection_custom_modules(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEventThreatDetectionCustomModulesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_event_threat_detection_custom_modules_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_event_threat_detection_custom_modules
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_event_threat_detection_custom_modules
        ] = mock_rpc

        request = {}
        client.list_event_threat_detection_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_event_threat_detection_custom_modules(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_event_threat_detection_custom_modules_rest_required_fields(
    request_type=security_center_management.ListEventThreatDetectionCustomModulesRequest,
):
    transport_class = transports.SecurityCenterManagementRestTransport

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
    ).list_event_threat_detection_custom_modules._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_event_threat_detection_custom_modules._get_unset_required_fields(
        jsonified_request
    )
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

    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = (
        security_center_management.ListEventThreatDetectionCustomModulesResponse()
    )
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
            return_value = security_center_management.ListEventThreatDetectionCustomModulesResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_event_threat_detection_custom_modules(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_event_threat_detection_custom_modules_rest_unset_required_fields():
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.list_event_threat_detection_custom_modules._get_unset_required_fields(
            {}
        )
    )
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
def test_list_event_threat_detection_custom_modules_rest_interceptors(null_interceptor):
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SecurityCenterManagementRestInterceptor(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "post_list_event_threat_detection_custom_modules",
    ) as post, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "pre_list_event_threat_detection_custom_modules",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = security_center_management.ListEventThreatDetectionCustomModulesRequest.pb(
            security_center_management.ListEventThreatDetectionCustomModulesRequest()
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
        req.return_value._content = security_center_management.ListEventThreatDetectionCustomModulesResponse.to_json(
            security_center_management.ListEventThreatDetectionCustomModulesResponse()
        )

        request = (
            security_center_management.ListEventThreatDetectionCustomModulesRequest()
        )
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            security_center_management.ListEventThreatDetectionCustomModulesResponse()
        )

        client.list_event_threat_detection_custom_modules(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_event_threat_detection_custom_modules_rest_bad_request(
    transport: str = "rest",
    request_type=security_center_management.ListEventThreatDetectionCustomModulesRequest,
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_event_threat_detection_custom_modules(request)


def test_list_event_threat_detection_custom_modules_rest_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = (
            security_center_management.ListEventThreatDetectionCustomModulesResponse()
        )

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
        return_value = (
            security_center_management.ListEventThreatDetectionCustomModulesResponse.pb(
                return_value
            )
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_event_threat_detection_custom_modules(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/eventThreatDetectionCustomModules"
            % client.transport._host,
            args[1],
        )


def test_list_event_threat_detection_custom_modules_rest_flattened_error(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_event_threat_detection_custom_modules(
            security_center_management.ListEventThreatDetectionCustomModulesRequest(),
            parent="parent_value",
        )


def test_list_event_threat_detection_custom_modules_rest_pager(transport: str = "rest"):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            security_center_management.ListEventThreatDetectionCustomModulesResponse.to_json(
                x
            )
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_event_threat_detection_custom_modules(
            request=sample_request
        )

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, security_center_management.EventThreatDetectionCustomModule)
            for i in results
        )

        pages = list(
            client.list_event_threat_detection_custom_modules(
                request=sample_request
            ).pages
        )
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest,
        dict,
    ],
)
def test_list_descendant_event_threat_detection_custom_modules_rest(request_type):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_descendant_event_threat_detection_custom_modules(request)

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, pagers.ListDescendantEventThreatDetectionCustomModulesPager
    )
    assert response.next_page_token == "next_page_token_value"


def test_list_descendant_event_threat_detection_custom_modules_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_descendant_event_threat_detection_custom_modules
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_descendant_event_threat_detection_custom_modules
        ] = mock_rpc

        request = {}
        client.list_descendant_event_threat_detection_custom_modules(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_descendant_event_threat_detection_custom_modules(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_descendant_event_threat_detection_custom_modules_rest_required_fields(
    request_type=security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest,
):
    transport_class = transports.SecurityCenterManagementRestTransport

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
    ).list_descendant_event_threat_detection_custom_modules._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_descendant_event_threat_detection_custom_modules._get_unset_required_fields(
        jsonified_request
    )
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

    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = (
        security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse()
    )
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
            return_value = security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_descendant_event_threat_detection_custom_modules(
                request
            )

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_descendant_event_threat_detection_custom_modules_rest_unset_required_fields():
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_descendant_event_threat_detection_custom_modules._get_unset_required_fields(
        {}
    )
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
def test_list_descendant_event_threat_detection_custom_modules_rest_interceptors(
    null_interceptor,
):
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SecurityCenterManagementRestInterceptor(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "post_list_descendant_event_threat_detection_custom_modules",
    ) as post, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "pre_list_descendant_event_threat_detection_custom_modules",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest.pb(
            security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest()
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
        req.return_value._content = security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse.to_json(
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse()
        )

        request = (
            security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest()
        )
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse()
        )

        client.list_descendant_event_threat_detection_custom_modules(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_descendant_event_threat_detection_custom_modules_rest_bad_request(
    transport: str = "rest",
    request_type=security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest,
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_descendant_event_threat_detection_custom_modules(request)


def test_list_descendant_event_threat_detection_custom_modules_rest_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = (
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse()
        )

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
        return_value = security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_descendant_event_threat_detection_custom_modules(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/eventThreatDetectionCustomModules:listDescendant"
            % client.transport._host,
            args[1],
        )


def test_list_descendant_event_threat_detection_custom_modules_rest_flattened_error(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_descendant_event_threat_detection_custom_modules(
            security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest(),
            parent="parent_value",
        )


def test_list_descendant_event_threat_detection_custom_modules_rest_pager(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[],
                next_page_token="def",
            ),
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse(
                event_threat_detection_custom_modules=[
                    security_center_management.EventThreatDetectionCustomModule(),
                    security_center_management.EventThreatDetectionCustomModule(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse.to_json(
                x
            )
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_descendant_event_threat_detection_custom_modules(
            request=sample_request
        )

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, security_center_management.EventThreatDetectionCustomModule)
            for i in results
        )

        pages = list(
            client.list_descendant_event_threat_detection_custom_modules(
                request=sample_request
            ).pages
        )
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.GetEventThreatDetectionCustomModuleRequest,
        dict,
    ],
)
def test_get_event_threat_detection_custom_module_rest(request_type):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/eventThreatDetectionCustomModules/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.EventThreatDetectionCustomModule(
            name="name_value",
            ancestor_module="ancestor_module_value",
            enablement_state=security_center_management.EventThreatDetectionCustomModule.EnablementState.ENABLED,
            type_="type__value",
            display_name="display_name_value",
            description="description_value",
            last_editor="last_editor_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = security_center_management.EventThreatDetectionCustomModule.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_event_threat_detection_custom_module(request)

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, security_center_management.EventThreatDetectionCustomModule
    )
    assert response.name == "name_value"
    assert response.ancestor_module == "ancestor_module_value"
    assert (
        response.enablement_state
        == security_center_management.EventThreatDetectionCustomModule.EnablementState.ENABLED
    )
    assert response.type_ == "type__value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.last_editor == "last_editor_value"


def test_get_event_threat_detection_custom_module_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_event_threat_detection_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_event_threat_detection_custom_module
        ] = mock_rpc

        request = {}
        client.get_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_event_threat_detection_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_event_threat_detection_custom_module_rest_required_fields(
    request_type=security_center_management.GetEventThreatDetectionCustomModuleRequest,
):
    transport_class = transports.SecurityCenterManagementRestTransport

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
    ).get_event_threat_detection_custom_module._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_event_threat_detection_custom_module._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = security_center_management.EventThreatDetectionCustomModule()
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
            return_value = (
                security_center_management.EventThreatDetectionCustomModule.pb(
                    return_value
                )
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_event_threat_detection_custom_module(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_event_threat_detection_custom_module_rest_unset_required_fields():
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.get_event_threat_detection_custom_module._get_unset_required_fields(
            {}
        )
    )
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_event_threat_detection_custom_module_rest_interceptors(null_interceptor):
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SecurityCenterManagementRestInterceptor(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "post_get_event_threat_detection_custom_module",
    ) as post, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "pre_get_event_threat_detection_custom_module",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = (
            security_center_management.GetEventThreatDetectionCustomModuleRequest.pb(
                security_center_management.GetEventThreatDetectionCustomModuleRequest()
            )
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
            security_center_management.EventThreatDetectionCustomModule.to_json(
                security_center_management.EventThreatDetectionCustomModule()
            )
        )

        request = (
            security_center_management.GetEventThreatDetectionCustomModuleRequest()
        )
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            security_center_management.EventThreatDetectionCustomModule()
        )

        client.get_event_threat_detection_custom_module(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_event_threat_detection_custom_module_rest_bad_request(
    transport: str = "rest",
    request_type=security_center_management.GetEventThreatDetectionCustomModuleRequest,
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/eventThreatDetectionCustomModules/sample3"
    }
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
        client.get_event_threat_detection_custom_module(request)


def test_get_event_threat_detection_custom_module_rest_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.EventThreatDetectionCustomModule()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/eventThreatDetectionCustomModules/sample3"
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
        return_value = security_center_management.EventThreatDetectionCustomModule.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_event_threat_detection_custom_module(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/eventThreatDetectionCustomModules/*}"
            % client.transport._host,
            args[1],
        )


def test_get_event_threat_detection_custom_module_rest_flattened_error(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_event_threat_detection_custom_module(
            security_center_management.GetEventThreatDetectionCustomModuleRequest(),
            name="name_value",
        )


def test_get_event_threat_detection_custom_module_rest_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.CreateEventThreatDetectionCustomModuleRequest,
        dict,
    ],
)
def test_create_event_threat_detection_custom_module_rest(request_type):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["event_threat_detection_custom_module"] = {
        "name": "name_value",
        "config": {"fields": {}},
        "ancestor_module": "ancestor_module_value",
        "enablement_state": 1,
        "type_": "type__value",
        "display_name": "display_name_value",
        "description": "description_value",
        "update_time": {"seconds": 751, "nanos": 543},
        "last_editor": "last_editor_value",
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = security_center_management.CreateEventThreatDetectionCustomModuleRequest.meta.fields[
        "event_threat_detection_custom_module"
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
        "event_threat_detection_custom_module"
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
                    0, len(request_init["event_threat_detection_custom_module"][field])
                ):
                    del request_init["event_threat_detection_custom_module"][field][i][
                        subfield
                    ]
            else:
                del request_init["event_threat_detection_custom_module"][field][
                    subfield
                ]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.EventThreatDetectionCustomModule(
            name="name_value",
            ancestor_module="ancestor_module_value",
            enablement_state=security_center_management.EventThreatDetectionCustomModule.EnablementState.ENABLED,
            type_="type__value",
            display_name="display_name_value",
            description="description_value",
            last_editor="last_editor_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = security_center_management.EventThreatDetectionCustomModule.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_event_threat_detection_custom_module(request)

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, security_center_management.EventThreatDetectionCustomModule
    )
    assert response.name == "name_value"
    assert response.ancestor_module == "ancestor_module_value"
    assert (
        response.enablement_state
        == security_center_management.EventThreatDetectionCustomModule.EnablementState.ENABLED
    )
    assert response.type_ == "type__value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.last_editor == "last_editor_value"


def test_create_event_threat_detection_custom_module_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_event_threat_detection_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_event_threat_detection_custom_module
        ] = mock_rpc

        request = {}
        client.create_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_event_threat_detection_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_event_threat_detection_custom_module_rest_required_fields(
    request_type=security_center_management.CreateEventThreatDetectionCustomModuleRequest,
):
    transport_class = transports.SecurityCenterManagementRestTransport

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
    ).create_event_threat_detection_custom_module._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_event_threat_detection_custom_module._get_unset_required_fields(
        jsonified_request
    )
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("validate_only",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = security_center_management.EventThreatDetectionCustomModule()
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
            return_value = (
                security_center_management.EventThreatDetectionCustomModule.pb(
                    return_value
                )
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_event_threat_detection_custom_module(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_event_threat_detection_custom_module_rest_unset_required_fields():
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_event_threat_detection_custom_module._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (
        set(("validateOnly",))
        & set(
            (
                "parent",
                "eventThreatDetectionCustomModule",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_event_threat_detection_custom_module_rest_interceptors(
    null_interceptor,
):
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SecurityCenterManagementRestInterceptor(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "post_create_event_threat_detection_custom_module",
    ) as post, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "pre_create_event_threat_detection_custom_module",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = security_center_management.CreateEventThreatDetectionCustomModuleRequest.pb(
            security_center_management.CreateEventThreatDetectionCustomModuleRequest()
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
            security_center_management.EventThreatDetectionCustomModule.to_json(
                security_center_management.EventThreatDetectionCustomModule()
            )
        )

        request = (
            security_center_management.CreateEventThreatDetectionCustomModuleRequest()
        )
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            security_center_management.EventThreatDetectionCustomModule()
        )

        client.create_event_threat_detection_custom_module(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_event_threat_detection_custom_module_rest_bad_request(
    transport: str = "rest",
    request_type=security_center_management.CreateEventThreatDetectionCustomModuleRequest,
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.create_event_threat_detection_custom_module(request)


def test_create_event_threat_detection_custom_module_rest_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.EventThreatDetectionCustomModule()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            event_threat_detection_custom_module=security_center_management.EventThreatDetectionCustomModule(
                name="name_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = security_center_management.EventThreatDetectionCustomModule.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_event_threat_detection_custom_module(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/eventThreatDetectionCustomModules"
            % client.transport._host,
            args[1],
        )


def test_create_event_threat_detection_custom_module_rest_flattened_error(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_event_threat_detection_custom_module(
            security_center_management.CreateEventThreatDetectionCustomModuleRequest(),
            parent="parent_value",
            event_threat_detection_custom_module=security_center_management.EventThreatDetectionCustomModule(
                name="name_value"
            ),
        )


def test_create_event_threat_detection_custom_module_rest_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.UpdateEventThreatDetectionCustomModuleRequest,
        dict,
    ],
)
def test_update_event_threat_detection_custom_module_rest(request_type):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "event_threat_detection_custom_module": {
            "name": "projects/sample1/locations/sample2/eventThreatDetectionCustomModules/sample3"
        }
    }
    request_init["event_threat_detection_custom_module"] = {
        "name": "projects/sample1/locations/sample2/eventThreatDetectionCustomModules/sample3",
        "config": {"fields": {}},
        "ancestor_module": "ancestor_module_value",
        "enablement_state": 1,
        "type_": "type__value",
        "display_name": "display_name_value",
        "description": "description_value",
        "update_time": {"seconds": 751, "nanos": 543},
        "last_editor": "last_editor_value",
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = security_center_management.UpdateEventThreatDetectionCustomModuleRequest.meta.fields[
        "event_threat_detection_custom_module"
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
        "event_threat_detection_custom_module"
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
                    0, len(request_init["event_threat_detection_custom_module"][field])
                ):
                    del request_init["event_threat_detection_custom_module"][field][i][
                        subfield
                    ]
            else:
                del request_init["event_threat_detection_custom_module"][field][
                    subfield
                ]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.EventThreatDetectionCustomModule(
            name="name_value",
            ancestor_module="ancestor_module_value",
            enablement_state=security_center_management.EventThreatDetectionCustomModule.EnablementState.ENABLED,
            type_="type__value",
            display_name="display_name_value",
            description="description_value",
            last_editor="last_editor_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = security_center_management.EventThreatDetectionCustomModule.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_event_threat_detection_custom_module(request)

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, security_center_management.EventThreatDetectionCustomModule
    )
    assert response.name == "name_value"
    assert response.ancestor_module == "ancestor_module_value"
    assert (
        response.enablement_state
        == security_center_management.EventThreatDetectionCustomModule.EnablementState.ENABLED
    )
    assert response.type_ == "type__value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.last_editor == "last_editor_value"


def test_update_event_threat_detection_custom_module_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_event_threat_detection_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_event_threat_detection_custom_module
        ] = mock_rpc

        request = {}
        client.update_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_event_threat_detection_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_update_event_threat_detection_custom_module_rest_required_fields(
    request_type=security_center_management.UpdateEventThreatDetectionCustomModuleRequest,
):
    transport_class = transports.SecurityCenterManagementRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_event_threat_detection_custom_module._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_event_threat_detection_custom_module._get_unset_required_fields(
        jsonified_request
    )
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "update_mask",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = security_center_management.EventThreatDetectionCustomModule()
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
            return_value = (
                security_center_management.EventThreatDetectionCustomModule.pb(
                    return_value
                )
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_event_threat_detection_custom_module(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_event_threat_detection_custom_module_rest_unset_required_fields():
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_event_threat_detection_custom_module._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (
        set(
            (
                "updateMask",
                "validateOnly",
            )
        )
        & set(
            (
                "updateMask",
                "eventThreatDetectionCustomModule",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_event_threat_detection_custom_module_rest_interceptors(
    null_interceptor,
):
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SecurityCenterManagementRestInterceptor(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "post_update_event_threat_detection_custom_module",
    ) as post, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "pre_update_event_threat_detection_custom_module",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = security_center_management.UpdateEventThreatDetectionCustomModuleRequest.pb(
            security_center_management.UpdateEventThreatDetectionCustomModuleRequest()
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
            security_center_management.EventThreatDetectionCustomModule.to_json(
                security_center_management.EventThreatDetectionCustomModule()
            )
        )

        request = (
            security_center_management.UpdateEventThreatDetectionCustomModuleRequest()
        )
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            security_center_management.EventThreatDetectionCustomModule()
        )

        client.update_event_threat_detection_custom_module(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_event_threat_detection_custom_module_rest_bad_request(
    transport: str = "rest",
    request_type=security_center_management.UpdateEventThreatDetectionCustomModuleRequest,
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "event_threat_detection_custom_module": {
            "name": "projects/sample1/locations/sample2/eventThreatDetectionCustomModules/sample3"
        }
    }
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
        client.update_event_threat_detection_custom_module(request)


def test_update_event_threat_detection_custom_module_rest_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.EventThreatDetectionCustomModule()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "event_threat_detection_custom_module": {
                "name": "projects/sample1/locations/sample2/eventThreatDetectionCustomModules/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            event_threat_detection_custom_module=security_center_management.EventThreatDetectionCustomModule(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = security_center_management.EventThreatDetectionCustomModule.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_event_threat_detection_custom_module(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{event_threat_detection_custom_module.name=projects/*/locations/*/eventThreatDetectionCustomModules/*}"
            % client.transport._host,
            args[1],
        )


def test_update_event_threat_detection_custom_module_rest_flattened_error(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_event_threat_detection_custom_module(
            security_center_management.UpdateEventThreatDetectionCustomModuleRequest(),
            event_threat_detection_custom_module=security_center_management.EventThreatDetectionCustomModule(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_event_threat_detection_custom_module_rest_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.DeleteEventThreatDetectionCustomModuleRequest,
        dict,
    ],
)
def test_delete_event_threat_detection_custom_module_rest(request_type):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/eventThreatDetectionCustomModules/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_event_threat_detection_custom_module(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_event_threat_detection_custom_module_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_event_threat_detection_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_event_threat_detection_custom_module
        ] = mock_rpc

        request = {}
        client.delete_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_event_threat_detection_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_event_threat_detection_custom_module_rest_required_fields(
    request_type=security_center_management.DeleteEventThreatDetectionCustomModuleRequest,
):
    transport_class = transports.SecurityCenterManagementRestTransport

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
    ).delete_event_threat_detection_custom_module._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_event_threat_detection_custom_module._get_unset_required_fields(
        jsonified_request
    )
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("validate_only",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SecurityCenterManagementClient(
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

            response = client.delete_event_threat_detection_custom_module(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_event_threat_detection_custom_module_rest_unset_required_fields():
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_event_threat_detection_custom_module._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (set(("validateOnly",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_event_threat_detection_custom_module_rest_interceptors(
    null_interceptor,
):
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SecurityCenterManagementRestInterceptor(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "pre_delete_event_threat_detection_custom_module",
    ) as pre:
        pre.assert_not_called()
        pb_message = security_center_management.DeleteEventThreatDetectionCustomModuleRequest.pb(
            security_center_management.DeleteEventThreatDetectionCustomModuleRequest()
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

        request = (
            security_center_management.DeleteEventThreatDetectionCustomModuleRequest()
        )
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_event_threat_detection_custom_module(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_event_threat_detection_custom_module_rest_bad_request(
    transport: str = "rest",
    request_type=security_center_management.DeleteEventThreatDetectionCustomModuleRequest,
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/eventThreatDetectionCustomModules/sample3"
    }
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
        client.delete_event_threat_detection_custom_module(request)


def test_delete_event_threat_detection_custom_module_rest_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/eventThreatDetectionCustomModules/sample3"
        }

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

        client.delete_event_threat_detection_custom_module(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/eventThreatDetectionCustomModules/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_event_threat_detection_custom_module_rest_flattened_error(
    transport: str = "rest",
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_event_threat_detection_custom_module(
            security_center_management.DeleteEventThreatDetectionCustomModuleRequest(),
            name="name_value",
        )


def test_delete_event_threat_detection_custom_module_rest_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.ValidateEventThreatDetectionCustomModuleRequest,
        dict,
    ],
)
def test_validate_event_threat_detection_custom_module_rest(request_type):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = (
            security_center_management.ValidateEventThreatDetectionCustomModuleResponse()
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = security_center_management.ValidateEventThreatDetectionCustomModuleResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.validate_event_threat_detection_custom_module(request)

    # Establish that the response is the type that we expect.
    assert isinstance(
        response,
        security_center_management.ValidateEventThreatDetectionCustomModuleResponse,
    )


def test_validate_event_threat_detection_custom_module_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.validate_event_threat_detection_custom_module
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.validate_event_threat_detection_custom_module
        ] = mock_rpc

        request = {}
        client.validate_event_threat_detection_custom_module(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.validate_event_threat_detection_custom_module(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_validate_event_threat_detection_custom_module_rest_required_fields(
    request_type=security_center_management.ValidateEventThreatDetectionCustomModuleRequest,
):
    transport_class = transports.SecurityCenterManagementRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["raw_text"] = ""
    request_init["type_"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).validate_event_threat_detection_custom_module._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"
    jsonified_request["rawText"] = "raw_text_value"
    jsonified_request["type"] = "type__value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).validate_event_threat_detection_custom_module._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "rawText" in jsonified_request
    assert jsonified_request["rawText"] == "raw_text_value"
    assert "type" in jsonified_request
    assert jsonified_request["type"] == "type__value"

    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = (
        security_center_management.ValidateEventThreatDetectionCustomModuleResponse()
    )
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
            return_value = security_center_management.ValidateEventThreatDetectionCustomModuleResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.validate_event_threat_detection_custom_module(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_validate_event_threat_detection_custom_module_rest_unset_required_fields():
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.validate_event_threat_detection_custom_module._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "rawText",
                "type",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_validate_event_threat_detection_custom_module_rest_interceptors(
    null_interceptor,
):
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SecurityCenterManagementRestInterceptor(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "post_validate_event_threat_detection_custom_module",
    ) as post, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "pre_validate_event_threat_detection_custom_module",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = security_center_management.ValidateEventThreatDetectionCustomModuleRequest.pb(
            security_center_management.ValidateEventThreatDetectionCustomModuleRequest()
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
        req.return_value._content = security_center_management.ValidateEventThreatDetectionCustomModuleResponse.to_json(
            security_center_management.ValidateEventThreatDetectionCustomModuleResponse()
        )

        request = (
            security_center_management.ValidateEventThreatDetectionCustomModuleRequest()
        )
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            security_center_management.ValidateEventThreatDetectionCustomModuleResponse()
        )

        client.validate_event_threat_detection_custom_module(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_validate_event_threat_detection_custom_module_rest_bad_request(
    transport: str = "rest",
    request_type=security_center_management.ValidateEventThreatDetectionCustomModuleRequest,
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.validate_event_threat_detection_custom_module(request)


def test_validate_event_threat_detection_custom_module_rest_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.GetSecurityCenterServiceRequest,
        dict,
    ],
)
def test_get_security_center_service_rest(request_type):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/securityCenterServices/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.SecurityCenterService(
            name="name_value",
            intended_enablement_state=security_center_management.SecurityCenterService.EnablementState.INHERITED,
            effective_enablement_state=security_center_management.SecurityCenterService.EnablementState.INHERITED,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = security_center_management.SecurityCenterService.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_security_center_service(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, security_center_management.SecurityCenterService)
    assert response.name == "name_value"
    assert (
        response.intended_enablement_state
        == security_center_management.SecurityCenterService.EnablementState.INHERITED
    )
    assert (
        response.effective_enablement_state
        == security_center_management.SecurityCenterService.EnablementState.INHERITED
    )


def test_get_security_center_service_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_security_center_service
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_security_center_service
        ] = mock_rpc

        request = {}
        client.get_security_center_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_security_center_service(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_security_center_service_rest_required_fields(
    request_type=security_center_management.GetSecurityCenterServiceRequest,
):
    transport_class = transports.SecurityCenterManagementRestTransport

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
    ).get_security_center_service._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_security_center_service._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("show_eligible_modules_only",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = security_center_management.SecurityCenterService()
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
            return_value = security_center_management.SecurityCenterService.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_security_center_service(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_security_center_service_rest_unset_required_fields():
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_security_center_service._get_unset_required_fields({})
    assert set(unset_fields) == (set(("showEligibleModulesOnly",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_security_center_service_rest_interceptors(null_interceptor):
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SecurityCenterManagementRestInterceptor(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "post_get_security_center_service",
    ) as post, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "pre_get_security_center_service",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = security_center_management.GetSecurityCenterServiceRequest.pb(
            security_center_management.GetSecurityCenterServiceRequest()
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
            security_center_management.SecurityCenterService.to_json(
                security_center_management.SecurityCenterService()
            )
        )

        request = security_center_management.GetSecurityCenterServiceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = security_center_management.SecurityCenterService()

        client.get_security_center_service(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_security_center_service_rest_bad_request(
    transport: str = "rest",
    request_type=security_center_management.GetSecurityCenterServiceRequest,
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/securityCenterServices/sample3"
    }
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
        client.get_security_center_service(request)


def test_get_security_center_service_rest_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.SecurityCenterService()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/securityCenterServices/sample3"
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
        return_value = security_center_management.SecurityCenterService.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_security_center_service(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/securityCenterServices/*}"
            % client.transport._host,
            args[1],
        )


def test_get_security_center_service_rest_flattened_error(transport: str = "rest"):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_security_center_service(
            security_center_management.GetSecurityCenterServiceRequest(),
            name="name_value",
        )


def test_get_security_center_service_rest_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.ListSecurityCenterServicesRequest,
        dict,
    ],
)
def test_list_security_center_services_rest(request_type):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.ListSecurityCenterServicesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = security_center_management.ListSecurityCenterServicesResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_security_center_services(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSecurityCenterServicesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_security_center_services_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_security_center_services
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_security_center_services
        ] = mock_rpc

        request = {}
        client.list_security_center_services(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_security_center_services(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_security_center_services_rest_required_fields(
    request_type=security_center_management.ListSecurityCenterServicesRequest,
):
    transport_class = transports.SecurityCenterManagementRestTransport

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
    ).list_security_center_services._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_security_center_services._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
            "show_eligible_modules_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = security_center_management.ListSecurityCenterServicesResponse()
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
            return_value = (
                security_center_management.ListSecurityCenterServicesResponse.pb(
                    return_value
                )
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_security_center_services(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_security_center_services_rest_unset_required_fields():
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_security_center_services._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
                "showEligibleModulesOnly",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_security_center_services_rest_interceptors(null_interceptor):
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SecurityCenterManagementRestInterceptor(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "post_list_security_center_services",
    ) as post, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "pre_list_security_center_services",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = security_center_management.ListSecurityCenterServicesRequest.pb(
            security_center_management.ListSecurityCenterServicesRequest()
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
            security_center_management.ListSecurityCenterServicesResponse.to_json(
                security_center_management.ListSecurityCenterServicesResponse()
            )
        )

        request = security_center_management.ListSecurityCenterServicesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            security_center_management.ListSecurityCenterServicesResponse()
        )

        client.list_security_center_services(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_security_center_services_rest_bad_request(
    transport: str = "rest",
    request_type=security_center_management.ListSecurityCenterServicesRequest,
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_security_center_services(request)


def test_list_security_center_services_rest_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.ListSecurityCenterServicesResponse()

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
        return_value = security_center_management.ListSecurityCenterServicesResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_security_center_services(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/securityCenterServices"
            % client.transport._host,
            args[1],
        )


def test_list_security_center_services_rest_flattened_error(transport: str = "rest"):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_security_center_services(
            security_center_management.ListSecurityCenterServicesRequest(),
            parent="parent_value",
        )


def test_list_security_center_services_rest_pager(transport: str = "rest"):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            security_center_management.ListSecurityCenterServicesResponse(
                security_center_services=[
                    security_center_management.SecurityCenterService(),
                    security_center_management.SecurityCenterService(),
                    security_center_management.SecurityCenterService(),
                ],
                next_page_token="abc",
            ),
            security_center_management.ListSecurityCenterServicesResponse(
                security_center_services=[],
                next_page_token="def",
            ),
            security_center_management.ListSecurityCenterServicesResponse(
                security_center_services=[
                    security_center_management.SecurityCenterService(),
                ],
                next_page_token="ghi",
            ),
            security_center_management.ListSecurityCenterServicesResponse(
                security_center_services=[
                    security_center_management.SecurityCenterService(),
                    security_center_management.SecurityCenterService(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            security_center_management.ListSecurityCenterServicesResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_security_center_services(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, security_center_management.SecurityCenterService)
            for i in results
        )

        pages = list(client.list_security_center_services(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        security_center_management.UpdateSecurityCenterServiceRequest,
        dict,
    ],
)
def test_update_security_center_service_rest(request_type):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "security_center_service": {
            "name": "projects/sample1/locations/sample2/securityCenterServices/sample3"
        }
    }
    request_init["security_center_service"] = {
        "name": "projects/sample1/locations/sample2/securityCenterServices/sample3",
        "intended_enablement_state": 1,
        "effective_enablement_state": 1,
        "modules": {},
        "update_time": {"seconds": 751, "nanos": 543},
        "service_config": {"fields": {}},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = (
        security_center_management.UpdateSecurityCenterServiceRequest.meta.fields[
            "security_center_service"
        ]
    )

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
        "security_center_service"
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
                for i in range(0, len(request_init["security_center_service"][field])):
                    del request_init["security_center_service"][field][i][subfield]
            else:
                del request_init["security_center_service"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.SecurityCenterService(
            name="name_value",
            intended_enablement_state=security_center_management.SecurityCenterService.EnablementState.INHERITED,
            effective_enablement_state=security_center_management.SecurityCenterService.EnablementState.INHERITED,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = security_center_management.SecurityCenterService.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_security_center_service(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, security_center_management.SecurityCenterService)
    assert response.name == "name_value"
    assert (
        response.intended_enablement_state
        == security_center_management.SecurityCenterService.EnablementState.INHERITED
    )
    assert (
        response.effective_enablement_state
        == security_center_management.SecurityCenterService.EnablementState.INHERITED
    )


def test_update_security_center_service_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_security_center_service
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_security_center_service
        ] = mock_rpc

        request = {}
        client.update_security_center_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_security_center_service(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_update_security_center_service_rest_required_fields(
    request_type=security_center_management.UpdateSecurityCenterServiceRequest,
):
    transport_class = transports.SecurityCenterManagementRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_security_center_service._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_security_center_service._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "update_mask",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = security_center_management.SecurityCenterService()
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
            return_value = security_center_management.SecurityCenterService.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_security_center_service(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_security_center_service_rest_unset_required_fields():
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_security_center_service._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (
        set(
            (
                "updateMask",
                "validateOnly",
            )
        )
        & set(
            (
                "securityCenterService",
                "updateMask",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_security_center_service_rest_interceptors(null_interceptor):
    transport = transports.SecurityCenterManagementRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SecurityCenterManagementRestInterceptor(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "post_update_security_center_service",
    ) as post, mock.patch.object(
        transports.SecurityCenterManagementRestInterceptor,
        "pre_update_security_center_service",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = security_center_management.UpdateSecurityCenterServiceRequest.pb(
            security_center_management.UpdateSecurityCenterServiceRequest()
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
            security_center_management.SecurityCenterService.to_json(
                security_center_management.SecurityCenterService()
            )
        )

        request = security_center_management.UpdateSecurityCenterServiceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = security_center_management.SecurityCenterService()

        client.update_security_center_service(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_security_center_service_rest_bad_request(
    transport: str = "rest",
    request_type=security_center_management.UpdateSecurityCenterServiceRequest,
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "security_center_service": {
            "name": "projects/sample1/locations/sample2/securityCenterServices/sample3"
        }
    }
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
        client.update_security_center_service(request)


def test_update_security_center_service_rest_flattened():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = security_center_management.SecurityCenterService()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "security_center_service": {
                "name": "projects/sample1/locations/sample2/securityCenterServices/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            security_center_service=security_center_management.SecurityCenterService(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = security_center_management.SecurityCenterService.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_security_center_service(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{security_center_service.name=projects/*/locations/*/securityCenterServices/*}"
            % client.transport._host,
            args[1],
        )


def test_update_security_center_service_rest_flattened_error(transport: str = "rest"):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_security_center_service(
            security_center_management.UpdateSecurityCenterServiceRequest(),
            security_center_service=security_center_management.SecurityCenterService(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_security_center_service_rest_error():
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.SecurityCenterManagementGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.SecurityCenterManagementGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SecurityCenterManagementClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.SecurityCenterManagementGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = SecurityCenterManagementClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = SecurityCenterManagementClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.SecurityCenterManagementGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SecurityCenterManagementClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.SecurityCenterManagementGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = SecurityCenterManagementClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.SecurityCenterManagementGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.SecurityCenterManagementGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.SecurityCenterManagementGrpcTransport,
        transports.SecurityCenterManagementGrpcAsyncIOTransport,
        transports.SecurityCenterManagementRestTransport,
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
    transport = SecurityCenterManagementClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.SecurityCenterManagementGrpcTransport,
    )


def test_security_center_management_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.SecurityCenterManagementTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_security_center_management_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.securitycentermanagement_v1.services.security_center_management.transports.SecurityCenterManagementTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.SecurityCenterManagementTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_effective_security_health_analytics_custom_modules",
        "get_effective_security_health_analytics_custom_module",
        "list_security_health_analytics_custom_modules",
        "list_descendant_security_health_analytics_custom_modules",
        "get_security_health_analytics_custom_module",
        "create_security_health_analytics_custom_module",
        "update_security_health_analytics_custom_module",
        "delete_security_health_analytics_custom_module",
        "simulate_security_health_analytics_custom_module",
        "list_effective_event_threat_detection_custom_modules",
        "get_effective_event_threat_detection_custom_module",
        "list_event_threat_detection_custom_modules",
        "list_descendant_event_threat_detection_custom_modules",
        "get_event_threat_detection_custom_module",
        "create_event_threat_detection_custom_module",
        "update_event_threat_detection_custom_module",
        "delete_event_threat_detection_custom_module",
        "validate_event_threat_detection_custom_module",
        "get_security_center_service",
        "list_security_center_services",
        "update_security_center_service",
        "get_location",
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


def test_security_center_management_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.securitycentermanagement_v1.services.security_center_management.transports.SecurityCenterManagementTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.SecurityCenterManagementTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_security_center_management_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.securitycentermanagement_v1.services.security_center_management.transports.SecurityCenterManagementTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.SecurityCenterManagementTransport()
        adc.assert_called_once()


def test_security_center_management_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        SecurityCenterManagementClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.SecurityCenterManagementGrpcTransport,
        transports.SecurityCenterManagementGrpcAsyncIOTransport,
    ],
)
def test_security_center_management_transport_auth_adc(transport_class):
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
        transports.SecurityCenterManagementGrpcTransport,
        transports.SecurityCenterManagementGrpcAsyncIOTransport,
        transports.SecurityCenterManagementRestTransport,
    ],
)
def test_security_center_management_transport_auth_gdch_credentials(transport_class):
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
        (transports.SecurityCenterManagementGrpcTransport, grpc_helpers),
        (transports.SecurityCenterManagementGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_security_center_management_transport_create_channel(
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
            "securitycentermanagement.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="securitycentermanagement.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.SecurityCenterManagementGrpcTransport,
        transports.SecurityCenterManagementGrpcAsyncIOTransport,
    ],
)
def test_security_center_management_grpc_transport_client_cert_source_for_mtls(
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


def test_security_center_management_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.SecurityCenterManagementRestTransport(
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
def test_security_center_management_host_no_port(transport_name):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="securitycentermanagement.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "securitycentermanagement.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://securitycentermanagement.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_security_center_management_host_with_port(transport_name):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="securitycentermanagement.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "securitycentermanagement.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://securitycentermanagement.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_security_center_management_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = SecurityCenterManagementClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = SecurityCenterManagementClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = (
        client1.transport.list_effective_security_health_analytics_custom_modules._session
    )
    session2 = (
        client2.transport.list_effective_security_health_analytics_custom_modules._session
    )
    assert session1 != session2
    session1 = (
        client1.transport.get_effective_security_health_analytics_custom_module._session
    )
    session2 = (
        client2.transport.get_effective_security_health_analytics_custom_module._session
    )
    assert session1 != session2
    session1 = client1.transport.list_security_health_analytics_custom_modules._session
    session2 = client2.transport.list_security_health_analytics_custom_modules._session
    assert session1 != session2
    session1 = (
        client1.transport.list_descendant_security_health_analytics_custom_modules._session
    )
    session2 = (
        client2.transport.list_descendant_security_health_analytics_custom_modules._session
    )
    assert session1 != session2
    session1 = client1.transport.get_security_health_analytics_custom_module._session
    session2 = client2.transport.get_security_health_analytics_custom_module._session
    assert session1 != session2
    session1 = client1.transport.create_security_health_analytics_custom_module._session
    session2 = client2.transport.create_security_health_analytics_custom_module._session
    assert session1 != session2
    session1 = client1.transport.update_security_health_analytics_custom_module._session
    session2 = client2.transport.update_security_health_analytics_custom_module._session
    assert session1 != session2
    session1 = client1.transport.delete_security_health_analytics_custom_module._session
    session2 = client2.transport.delete_security_health_analytics_custom_module._session
    assert session1 != session2
    session1 = (
        client1.transport.simulate_security_health_analytics_custom_module._session
    )
    session2 = (
        client2.transport.simulate_security_health_analytics_custom_module._session
    )
    assert session1 != session2
    session1 = (
        client1.transport.list_effective_event_threat_detection_custom_modules._session
    )
    session2 = (
        client2.transport.list_effective_event_threat_detection_custom_modules._session
    )
    assert session1 != session2
    session1 = (
        client1.transport.get_effective_event_threat_detection_custom_module._session
    )
    session2 = (
        client2.transport.get_effective_event_threat_detection_custom_module._session
    )
    assert session1 != session2
    session1 = client1.transport.list_event_threat_detection_custom_modules._session
    session2 = client2.transport.list_event_threat_detection_custom_modules._session
    assert session1 != session2
    session1 = (
        client1.transport.list_descendant_event_threat_detection_custom_modules._session
    )
    session2 = (
        client2.transport.list_descendant_event_threat_detection_custom_modules._session
    )
    assert session1 != session2
    session1 = client1.transport.get_event_threat_detection_custom_module._session
    session2 = client2.transport.get_event_threat_detection_custom_module._session
    assert session1 != session2
    session1 = client1.transport.create_event_threat_detection_custom_module._session
    session2 = client2.transport.create_event_threat_detection_custom_module._session
    assert session1 != session2
    session1 = client1.transport.update_event_threat_detection_custom_module._session
    session2 = client2.transport.update_event_threat_detection_custom_module._session
    assert session1 != session2
    session1 = client1.transport.delete_event_threat_detection_custom_module._session
    session2 = client2.transport.delete_event_threat_detection_custom_module._session
    assert session1 != session2
    session1 = client1.transport.validate_event_threat_detection_custom_module._session
    session2 = client2.transport.validate_event_threat_detection_custom_module._session
    assert session1 != session2
    session1 = client1.transport.get_security_center_service._session
    session2 = client2.transport.get_security_center_service._session
    assert session1 != session2
    session1 = client1.transport.list_security_center_services._session
    session2 = client2.transport.list_security_center_services._session
    assert session1 != session2
    session1 = client1.transport.update_security_center_service._session
    session2 = client2.transport.update_security_center_service._session
    assert session1 != session2


def test_security_center_management_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.SecurityCenterManagementGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_security_center_management_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.SecurityCenterManagementGrpcAsyncIOTransport(
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
        transports.SecurityCenterManagementGrpcTransport,
        transports.SecurityCenterManagementGrpcAsyncIOTransport,
    ],
)
def test_security_center_management_transport_channel_mtls_with_client_cert_source(
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
        transports.SecurityCenterManagementGrpcTransport,
        transports.SecurityCenterManagementGrpcAsyncIOTransport,
    ],
)
def test_security_center_management_transport_channel_mtls_with_adc(transport_class):
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


def test_effective_event_threat_detection_custom_module_path():
    organization = "squid"
    location = "clam"
    effective_event_threat_detection_custom_module = "whelk"
    expected = "organizations/{organization}/locations/{location}/effectiveEventThreatDetectionCustomModules/{effective_event_threat_detection_custom_module}".format(
        organization=organization,
        location=location,
        effective_event_threat_detection_custom_module=effective_event_threat_detection_custom_module,
    )
    actual = SecurityCenterManagementClient.effective_event_threat_detection_custom_module_path(
        organization, location, effective_event_threat_detection_custom_module
    )
    assert expected == actual


def test_parse_effective_event_threat_detection_custom_module_path():
    expected = {
        "organization": "octopus",
        "location": "oyster",
        "effective_event_threat_detection_custom_module": "nudibranch",
    }
    path = SecurityCenterManagementClient.effective_event_threat_detection_custom_module_path(
        **expected
    )

    # Check that the path construction is reversible.
    actual = SecurityCenterManagementClient.parse_effective_event_threat_detection_custom_module_path(
        path
    )
    assert expected == actual


def test_effective_security_health_analytics_custom_module_path():
    organization = "cuttlefish"
    location = "mussel"
    effective_security_health_analytics_custom_module = "winkle"
    expected = "organizations/{organization}/locations/{location}/effectiveSecurityHealthAnalyticsCustomModules/{effective_security_health_analytics_custom_module}".format(
        organization=organization,
        location=location,
        effective_security_health_analytics_custom_module=effective_security_health_analytics_custom_module,
    )
    actual = SecurityCenterManagementClient.effective_security_health_analytics_custom_module_path(
        organization, location, effective_security_health_analytics_custom_module
    )
    assert expected == actual


def test_parse_effective_security_health_analytics_custom_module_path():
    expected = {
        "organization": "nautilus",
        "location": "scallop",
        "effective_security_health_analytics_custom_module": "abalone",
    }
    path = SecurityCenterManagementClient.effective_security_health_analytics_custom_module_path(
        **expected
    )

    # Check that the path construction is reversible.
    actual = SecurityCenterManagementClient.parse_effective_security_health_analytics_custom_module_path(
        path
    )
    assert expected == actual


def test_event_threat_detection_custom_module_path():
    organization = "squid"
    location = "clam"
    event_threat_detection_custom_module = "whelk"
    expected = "organizations/{organization}/locations/{location}/eventThreatDetectionCustomModules/{event_threat_detection_custom_module}".format(
        organization=organization,
        location=location,
        event_threat_detection_custom_module=event_threat_detection_custom_module,
    )
    actual = SecurityCenterManagementClient.event_threat_detection_custom_module_path(
        organization, location, event_threat_detection_custom_module
    )
    assert expected == actual


def test_parse_event_threat_detection_custom_module_path():
    expected = {
        "organization": "octopus",
        "location": "oyster",
        "event_threat_detection_custom_module": "nudibranch",
    }
    path = SecurityCenterManagementClient.event_threat_detection_custom_module_path(
        **expected
    )

    # Check that the path construction is reversible.
    actual = (
        SecurityCenterManagementClient.parse_event_threat_detection_custom_module_path(
            path
        )
    )
    assert expected == actual


def test_finding_path():
    organization = "cuttlefish"
    source = "mussel"
    finding = "winkle"
    expected = (
        "organizations/{organization}/sources/{source}/findings/{finding}".format(
            organization=organization,
            source=source,
            finding=finding,
        )
    )
    actual = SecurityCenterManagementClient.finding_path(organization, source, finding)
    assert expected == actual


def test_parse_finding_path():
    expected = {
        "organization": "nautilus",
        "source": "scallop",
        "finding": "abalone",
    }
    path = SecurityCenterManagementClient.finding_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterManagementClient.parse_finding_path(path)
    assert expected == actual


def test_security_center_service_path():
    project = "squid"
    location = "clam"
    service = "whelk"
    expected = "projects/{project}/locations/{location}/securityCenterServices/{service}".format(
        project=project,
        location=location,
        service=service,
    )
    actual = SecurityCenterManagementClient.security_center_service_path(
        project, location, service
    )
    assert expected == actual


def test_parse_security_center_service_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "service": "nudibranch",
    }
    path = SecurityCenterManagementClient.security_center_service_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterManagementClient.parse_security_center_service_path(path)
    assert expected == actual


def test_security_health_analytics_custom_module_path():
    organization = "cuttlefish"
    location = "mussel"
    security_health_analytics_custom_module = "winkle"
    expected = "organizations/{organization}/locations/{location}/securityHealthAnalyticsCustomModules/{security_health_analytics_custom_module}".format(
        organization=organization,
        location=location,
        security_health_analytics_custom_module=security_health_analytics_custom_module,
    )
    actual = (
        SecurityCenterManagementClient.security_health_analytics_custom_module_path(
            organization, location, security_health_analytics_custom_module
        )
    )
    assert expected == actual


def test_parse_security_health_analytics_custom_module_path():
    expected = {
        "organization": "nautilus",
        "location": "scallop",
        "security_health_analytics_custom_module": "abalone",
    }
    path = SecurityCenterManagementClient.security_health_analytics_custom_module_path(
        **expected
    )

    # Check that the path construction is reversible.
    actual = SecurityCenterManagementClient.parse_security_health_analytics_custom_module_path(
        path
    )
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = SecurityCenterManagementClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = SecurityCenterManagementClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterManagementClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = SecurityCenterManagementClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = SecurityCenterManagementClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterManagementClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = SecurityCenterManagementClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = SecurityCenterManagementClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterManagementClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = SecurityCenterManagementClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = SecurityCenterManagementClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterManagementClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = SecurityCenterManagementClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = SecurityCenterManagementClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterManagementClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.SecurityCenterManagementTransport, "_prep_wrapped_messages"
    ) as prep:
        client = SecurityCenterManagementClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.SecurityCenterManagementTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = SecurityCenterManagementClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_get_location_rest_bad_request(
    transport: str = "rest", request_type=locations_pb2.GetLocationRequest
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.Location()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_location(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


def test_list_locations_rest_bad_request(
    transport: str = "rest", request_type=locations_pb2.ListLocationsRequest
):
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict({"name": "projects/sample1"}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
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
    client = SecurityCenterManagementClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.ListLocationsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.list_locations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


def test_list_locations(transport: str = "grpc"):
    client = SecurityCenterManagementClient(
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
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = SecurityCenterManagementClient(
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
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = SecurityCenterManagementClient(
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
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = SecurityCenterManagementClient(
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
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = SecurityCenterManagementClient(
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
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials()
    )

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
    client = SecurityCenterManagementClient(
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
    client = SecurityCenterManagementAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = SecurityCenterManagementClient(
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
        client = SecurityCenterManagementClient(
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
            SecurityCenterManagementClient,
            transports.SecurityCenterManagementGrpcTransport,
        ),
        (
            SecurityCenterManagementAsyncClient,
            transports.SecurityCenterManagementGrpcAsyncIOTransport,
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
