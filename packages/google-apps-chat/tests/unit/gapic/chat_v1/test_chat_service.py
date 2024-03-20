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
from google.apps.card_v1.types import card
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import json_format
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.rpc import code_pb2  # type: ignore
from google.type import color_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.apps.chat_v1.services.chat_service import (
    ChatServiceAsyncClient,
    ChatServiceClient,
    pagers,
    transports,
)
from google.apps.chat_v1.types import (
    action_status,
    annotation,
    attachment,
    contextual_addon,
    deletion_metadata,
    group,
    history_state,
    matched_url,
)
from google.apps.chat_v1.types import membership
from google.apps.chat_v1.types import membership as gc_membership
from google.apps.chat_v1.types import message
from google.apps.chat_v1.types import message as gc_message
from google.apps.chat_v1.types import reaction
from google.apps.chat_v1.types import reaction as gc_reaction
from google.apps.chat_v1.types import slash_command
from google.apps.chat_v1.types import space
from google.apps.chat_v1.types import space as gc_space
from google.apps.chat_v1.types import space_setup, user, widgets


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

    assert ChatServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        ChatServiceClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        ChatServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ChatServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ChatServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert ChatServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


def test__read_environment_variables():
    assert ChatServiceClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert ChatServiceClient._read_environment_variables() == (True, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert ChatServiceClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            ChatServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert ChatServiceClient._read_environment_variables() == (False, "never", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert ChatServiceClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert ChatServiceClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            ChatServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert ChatServiceClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert ChatServiceClient._get_client_cert_source(None, False) is None
    assert (
        ChatServiceClient._get_client_cert_source(mock_provided_cert_source, False)
        is None
    )
    assert (
        ChatServiceClient._get_client_cert_source(mock_provided_cert_source, True)
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
                ChatServiceClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                ChatServiceClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    ChatServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ChatServiceClient),
)
@mock.patch.object(
    ChatServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ChatServiceAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = ChatServiceClient._DEFAULT_UNIVERSE
    default_endpoint = ChatServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = ChatServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        ChatServiceClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        ChatServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == ChatServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        ChatServiceClient._get_api_endpoint(None, None, default_universe, "auto")
        == default_endpoint
    )
    assert (
        ChatServiceClient._get_api_endpoint(None, None, default_universe, "always")
        == ChatServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        ChatServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == ChatServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        ChatServiceClient._get_api_endpoint(None, None, mock_universe, "never")
        == mock_endpoint
    )
    assert (
        ChatServiceClient._get_api_endpoint(None, None, default_universe, "never")
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        ChatServiceClient._get_api_endpoint(
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
        ChatServiceClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        ChatServiceClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        ChatServiceClient._get_universe_domain(None, None)
        == ChatServiceClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        ChatServiceClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ChatServiceClient, transports.ChatServiceGrpcTransport, "grpc"),
        (ChatServiceClient, transports.ChatServiceRestTransport, "rest"),
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
        (ChatServiceClient, "grpc"),
        (ChatServiceAsyncClient, "grpc_asyncio"),
        (ChatServiceClient, "rest"),
    ],
)
def test_chat_service_client_from_service_account_info(client_class, transport_name):
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
            "chat.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://chat.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.ChatServiceGrpcTransport, "grpc"),
        (transports.ChatServiceGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.ChatServiceRestTransport, "rest"),
    ],
)
def test_chat_service_client_service_account_always_use_jwt(
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
        (ChatServiceClient, "grpc"),
        (ChatServiceAsyncClient, "grpc_asyncio"),
        (ChatServiceClient, "rest"),
    ],
)
def test_chat_service_client_from_service_account_file(client_class, transport_name):
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
            "chat.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://chat.googleapis.com"
        )


def test_chat_service_client_get_transport_class():
    transport = ChatServiceClient.get_transport_class()
    available_transports = [
        transports.ChatServiceGrpcTransport,
        transports.ChatServiceRestTransport,
    ]
    assert transport in available_transports

    transport = ChatServiceClient.get_transport_class("grpc")
    assert transport == transports.ChatServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ChatServiceClient, transports.ChatServiceGrpcTransport, "grpc"),
        (
            ChatServiceAsyncClient,
            transports.ChatServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (ChatServiceClient, transports.ChatServiceRestTransport, "rest"),
    ],
)
@mock.patch.object(
    ChatServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ChatServiceClient),
)
@mock.patch.object(
    ChatServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ChatServiceAsyncClient),
)
def test_chat_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(ChatServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(ChatServiceClient, "get_transport_class") as gtc:
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
        (ChatServiceClient, transports.ChatServiceGrpcTransport, "grpc", "true"),
        (
            ChatServiceAsyncClient,
            transports.ChatServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (ChatServiceClient, transports.ChatServiceGrpcTransport, "grpc", "false"),
        (
            ChatServiceAsyncClient,
            transports.ChatServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (ChatServiceClient, transports.ChatServiceRestTransport, "rest", "true"),
        (ChatServiceClient, transports.ChatServiceRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    ChatServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ChatServiceClient),
)
@mock.patch.object(
    ChatServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ChatServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_chat_service_client_mtls_env_auto(
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


@pytest.mark.parametrize("client_class", [ChatServiceClient, ChatServiceAsyncClient])
@mock.patch.object(
    ChatServiceClient, "DEFAULT_ENDPOINT", modify_default_endpoint(ChatServiceClient)
)
@mock.patch.object(
    ChatServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ChatServiceAsyncClient),
)
def test_chat_service_client_get_mtls_endpoint_and_cert_source(client_class):
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


@pytest.mark.parametrize("client_class", [ChatServiceClient, ChatServiceAsyncClient])
@mock.patch.object(
    ChatServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ChatServiceClient),
)
@mock.patch.object(
    ChatServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ChatServiceAsyncClient),
)
def test_chat_service_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = ChatServiceClient._DEFAULT_UNIVERSE
    default_endpoint = ChatServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = ChatServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        (ChatServiceClient, transports.ChatServiceGrpcTransport, "grpc"),
        (
            ChatServiceAsyncClient,
            transports.ChatServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (ChatServiceClient, transports.ChatServiceRestTransport, "rest"),
    ],
)
def test_chat_service_client_client_options_scopes(
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
        (ChatServiceClient, transports.ChatServiceGrpcTransport, "grpc", grpc_helpers),
        (
            ChatServiceAsyncClient,
            transports.ChatServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (ChatServiceClient, transports.ChatServiceRestTransport, "rest", None),
    ],
)
def test_chat_service_client_client_options_credentials_file(
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


def test_chat_service_client_client_options_from_dict():
    with mock.patch(
        "google.apps.chat_v1.services.chat_service.transports.ChatServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ChatServiceClient(client_options={"api_endpoint": "squid.clam.whelk"})
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
        (ChatServiceClient, transports.ChatServiceGrpcTransport, "grpc", grpc_helpers),
        (
            ChatServiceAsyncClient,
            transports.ChatServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_chat_service_client_create_channel_credentials_file(
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
            "chat.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                "https://www.googleapis.com/auth/chat.bot",
                "https://www.googleapis.com/auth/chat.delete",
                "https://www.googleapis.com/auth/chat.import",
                "https://www.googleapis.com/auth/chat.memberships",
                "https://www.googleapis.com/auth/chat.memberships.app",
                "https://www.googleapis.com/auth/chat.memberships.readonly",
                "https://www.googleapis.com/auth/chat.messages",
                "https://www.googleapis.com/auth/chat.messages.create",
                "https://www.googleapis.com/auth/chat.messages.reactions",
                "https://www.googleapis.com/auth/chat.messages.reactions.create",
                "https://www.googleapis.com/auth/chat.messages.reactions.readonly",
                "https://www.googleapis.com/auth/chat.messages.readonly",
                "https://www.googleapis.com/auth/chat.spaces",
                "https://www.googleapis.com/auth/chat.spaces.create",
                "https://www.googleapis.com/auth/chat.spaces.readonly",
            ),
            scopes=None,
            default_host="chat.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gc_message.CreateMessageRequest,
        dict,
    ],
)
def test_create_message(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_message), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gc_message.Message(
            name="name_value",
            text="text_value",
            formatted_text="formatted_text_value",
            fallback_text="fallback_text_value",
            argument_text="argument_text_value",
            thread_reply=True,
            client_assigned_message_id="client_assigned_message_id_value",
        )
        response = client.create_message(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gc_message.CreateMessageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gc_message.Message)
    assert response.name == "name_value"
    assert response.text == "text_value"
    assert response.formatted_text == "formatted_text_value"
    assert response.fallback_text == "fallback_text_value"
    assert response.argument_text == "argument_text_value"
    assert response.thread_reply is True
    assert response.client_assigned_message_id == "client_assigned_message_id_value"


def test_create_message_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_message), "__call__") as call:
        client.create_message()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gc_message.CreateMessageRequest()


@pytest.mark.asyncio
async def test_create_message_async(
    transport: str = "grpc_asyncio", request_type=gc_message.CreateMessageRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_message), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gc_message.Message(
                name="name_value",
                text="text_value",
                formatted_text="formatted_text_value",
                fallback_text="fallback_text_value",
                argument_text="argument_text_value",
                thread_reply=True,
                client_assigned_message_id="client_assigned_message_id_value",
            )
        )
        response = await client.create_message(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gc_message.CreateMessageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gc_message.Message)
    assert response.name == "name_value"
    assert response.text == "text_value"
    assert response.formatted_text == "formatted_text_value"
    assert response.fallback_text == "fallback_text_value"
    assert response.argument_text == "argument_text_value"
    assert response.thread_reply is True
    assert response.client_assigned_message_id == "client_assigned_message_id_value"


@pytest.mark.asyncio
async def test_create_message_async_from_dict():
    await test_create_message_async(request_type=dict)


def test_create_message_field_headers():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gc_message.CreateMessageRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_message), "__call__") as call:
        call.return_value = gc_message.Message()
        client.create_message(request)

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
async def test_create_message_field_headers_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gc_message.CreateMessageRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_message), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gc_message.Message())
        await client.create_message(request)

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


def test_create_message_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_message), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gc_message.Message()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_message(
            parent="parent_value",
            message=gc_message.Message(name="name_value"),
            message_id="message_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].message
        mock_val = gc_message.Message(name="name_value")
        assert arg == mock_val
        arg = args[0].message_id
        mock_val = "message_id_value"
        assert arg == mock_val


def test_create_message_flattened_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_message(
            gc_message.CreateMessageRequest(),
            parent="parent_value",
            message=gc_message.Message(name="name_value"),
            message_id="message_id_value",
        )


@pytest.mark.asyncio
async def test_create_message_flattened_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_message), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gc_message.Message()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gc_message.Message())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_message(
            parent="parent_value",
            message=gc_message.Message(name="name_value"),
            message_id="message_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].message
        mock_val = gc_message.Message(name="name_value")
        assert arg == mock_val
        arg = args[0].message_id
        mock_val = "message_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_message_flattened_error_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_message(
            gc_message.CreateMessageRequest(),
            parent="parent_value",
            message=gc_message.Message(name="name_value"),
            message_id="message_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        message.ListMessagesRequest,
        dict,
    ],
)
def test_list_messages(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_messages), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = message.ListMessagesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_messages(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == message.ListMessagesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMessagesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_messages_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_messages), "__call__") as call:
        client.list_messages()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == message.ListMessagesRequest()


@pytest.mark.asyncio
async def test_list_messages_async(
    transport: str = "grpc_asyncio", request_type=message.ListMessagesRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_messages), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            message.ListMessagesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_messages(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == message.ListMessagesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMessagesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_messages_async_from_dict():
    await test_list_messages_async(request_type=dict)


def test_list_messages_field_headers():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = message.ListMessagesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_messages), "__call__") as call:
        call.return_value = message.ListMessagesResponse()
        client.list_messages(request)

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
async def test_list_messages_field_headers_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = message.ListMessagesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_messages), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            message.ListMessagesResponse()
        )
        await client.list_messages(request)

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


def test_list_messages_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_messages), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = message.ListMessagesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_messages(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_messages_flattened_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_messages(
            message.ListMessagesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_messages_flattened_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_messages), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = message.ListMessagesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            message.ListMessagesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_messages(
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
async def test_list_messages_flattened_error_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_messages(
            message.ListMessagesRequest(),
            parent="parent_value",
        )


def test_list_messages_pager(transport_name: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_messages), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            message.ListMessagesResponse(
                messages=[
                    message.Message(),
                    message.Message(),
                    message.Message(),
                ],
                next_page_token="abc",
            ),
            message.ListMessagesResponse(
                messages=[],
                next_page_token="def",
            ),
            message.ListMessagesResponse(
                messages=[
                    message.Message(),
                ],
                next_page_token="ghi",
            ),
            message.ListMessagesResponse(
                messages=[
                    message.Message(),
                    message.Message(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_messages(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, message.Message) for i in results)


def test_list_messages_pages(transport_name: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_messages), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            message.ListMessagesResponse(
                messages=[
                    message.Message(),
                    message.Message(),
                    message.Message(),
                ],
                next_page_token="abc",
            ),
            message.ListMessagesResponse(
                messages=[],
                next_page_token="def",
            ),
            message.ListMessagesResponse(
                messages=[
                    message.Message(),
                ],
                next_page_token="ghi",
            ),
            message.ListMessagesResponse(
                messages=[
                    message.Message(),
                    message.Message(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_messages(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_messages_async_pager():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_messages), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            message.ListMessagesResponse(
                messages=[
                    message.Message(),
                    message.Message(),
                    message.Message(),
                ],
                next_page_token="abc",
            ),
            message.ListMessagesResponse(
                messages=[],
                next_page_token="def",
            ),
            message.ListMessagesResponse(
                messages=[
                    message.Message(),
                ],
                next_page_token="ghi",
            ),
            message.ListMessagesResponse(
                messages=[
                    message.Message(),
                    message.Message(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_messages(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, message.Message) for i in responses)


@pytest.mark.asyncio
async def test_list_messages_async_pages():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_messages), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            message.ListMessagesResponse(
                messages=[
                    message.Message(),
                    message.Message(),
                    message.Message(),
                ],
                next_page_token="abc",
            ),
            message.ListMessagesResponse(
                messages=[],
                next_page_token="def",
            ),
            message.ListMessagesResponse(
                messages=[
                    message.Message(),
                ],
                next_page_token="ghi",
            ),
            message.ListMessagesResponse(
                messages=[
                    message.Message(),
                    message.Message(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_messages(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        membership.ListMembershipsRequest,
        dict,
    ],
)
def test_list_memberships(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_memberships), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = membership.ListMembershipsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_memberships(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == membership.ListMembershipsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMembershipsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_memberships_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_memberships), "__call__") as call:
        client.list_memberships()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == membership.ListMembershipsRequest()


@pytest.mark.asyncio
async def test_list_memberships_async(
    transport: str = "grpc_asyncio", request_type=membership.ListMembershipsRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_memberships), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            membership.ListMembershipsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_memberships(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == membership.ListMembershipsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMembershipsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_memberships_async_from_dict():
    await test_list_memberships_async(request_type=dict)


def test_list_memberships_field_headers():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = membership.ListMembershipsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_memberships), "__call__") as call:
        call.return_value = membership.ListMembershipsResponse()
        client.list_memberships(request)

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
async def test_list_memberships_field_headers_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = membership.ListMembershipsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_memberships), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            membership.ListMembershipsResponse()
        )
        await client.list_memberships(request)

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


def test_list_memberships_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_memberships), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = membership.ListMembershipsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_memberships(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_memberships_flattened_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_memberships(
            membership.ListMembershipsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_memberships_flattened_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_memberships), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = membership.ListMembershipsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            membership.ListMembershipsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_memberships(
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
async def test_list_memberships_flattened_error_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_memberships(
            membership.ListMembershipsRequest(),
            parent="parent_value",
        )


def test_list_memberships_pager(transport_name: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_memberships), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            membership.ListMembershipsResponse(
                memberships=[
                    membership.Membership(),
                    membership.Membership(),
                    membership.Membership(),
                ],
                next_page_token="abc",
            ),
            membership.ListMembershipsResponse(
                memberships=[],
                next_page_token="def",
            ),
            membership.ListMembershipsResponse(
                memberships=[
                    membership.Membership(),
                ],
                next_page_token="ghi",
            ),
            membership.ListMembershipsResponse(
                memberships=[
                    membership.Membership(),
                    membership.Membership(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_memberships(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, membership.Membership) for i in results)


def test_list_memberships_pages(transport_name: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_memberships), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            membership.ListMembershipsResponse(
                memberships=[
                    membership.Membership(),
                    membership.Membership(),
                    membership.Membership(),
                ],
                next_page_token="abc",
            ),
            membership.ListMembershipsResponse(
                memberships=[],
                next_page_token="def",
            ),
            membership.ListMembershipsResponse(
                memberships=[
                    membership.Membership(),
                ],
                next_page_token="ghi",
            ),
            membership.ListMembershipsResponse(
                memberships=[
                    membership.Membership(),
                    membership.Membership(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_memberships(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_memberships_async_pager():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_memberships), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            membership.ListMembershipsResponse(
                memberships=[
                    membership.Membership(),
                    membership.Membership(),
                    membership.Membership(),
                ],
                next_page_token="abc",
            ),
            membership.ListMembershipsResponse(
                memberships=[],
                next_page_token="def",
            ),
            membership.ListMembershipsResponse(
                memberships=[
                    membership.Membership(),
                ],
                next_page_token="ghi",
            ),
            membership.ListMembershipsResponse(
                memberships=[
                    membership.Membership(),
                    membership.Membership(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_memberships(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, membership.Membership) for i in responses)


@pytest.mark.asyncio
async def test_list_memberships_async_pages():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_memberships), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            membership.ListMembershipsResponse(
                memberships=[
                    membership.Membership(),
                    membership.Membership(),
                    membership.Membership(),
                ],
                next_page_token="abc",
            ),
            membership.ListMembershipsResponse(
                memberships=[],
                next_page_token="def",
            ),
            membership.ListMembershipsResponse(
                memberships=[
                    membership.Membership(),
                ],
                next_page_token="ghi",
            ),
            membership.ListMembershipsResponse(
                memberships=[
                    membership.Membership(),
                    membership.Membership(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_memberships(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        membership.GetMembershipRequest,
        dict,
    ],
)
def test_get_membership(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_membership), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = membership.Membership(
            name="name_value",
            state=membership.Membership.MembershipState.JOINED,
            role=membership.Membership.MembershipRole.ROLE_MEMBER,
        )
        response = client.get_membership(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == membership.GetMembershipRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, membership.Membership)
    assert response.name == "name_value"
    assert response.state == membership.Membership.MembershipState.JOINED
    assert response.role == membership.Membership.MembershipRole.ROLE_MEMBER


def test_get_membership_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_membership), "__call__") as call:
        client.get_membership()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == membership.GetMembershipRequest()


@pytest.mark.asyncio
async def test_get_membership_async(
    transport: str = "grpc_asyncio", request_type=membership.GetMembershipRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_membership), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            membership.Membership(
                name="name_value",
                state=membership.Membership.MembershipState.JOINED,
                role=membership.Membership.MembershipRole.ROLE_MEMBER,
            )
        )
        response = await client.get_membership(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == membership.GetMembershipRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, membership.Membership)
    assert response.name == "name_value"
    assert response.state == membership.Membership.MembershipState.JOINED
    assert response.role == membership.Membership.MembershipRole.ROLE_MEMBER


@pytest.mark.asyncio
async def test_get_membership_async_from_dict():
    await test_get_membership_async(request_type=dict)


def test_get_membership_field_headers():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = membership.GetMembershipRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_membership), "__call__") as call:
        call.return_value = membership.Membership()
        client.get_membership(request)

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
async def test_get_membership_field_headers_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = membership.GetMembershipRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_membership), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            membership.Membership()
        )
        await client.get_membership(request)

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


def test_get_membership_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_membership), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = membership.Membership()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_membership(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_membership_flattened_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_membership(
            membership.GetMembershipRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_membership_flattened_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_membership), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = membership.Membership()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            membership.Membership()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_membership(
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
async def test_get_membership_flattened_error_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_membership(
            membership.GetMembershipRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        message.GetMessageRequest,
        dict,
    ],
)
def test_get_message(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_message), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = message.Message(
            name="name_value",
            text="text_value",
            formatted_text="formatted_text_value",
            fallback_text="fallback_text_value",
            argument_text="argument_text_value",
            thread_reply=True,
            client_assigned_message_id="client_assigned_message_id_value",
        )
        response = client.get_message(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == message.GetMessageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, message.Message)
    assert response.name == "name_value"
    assert response.text == "text_value"
    assert response.formatted_text == "formatted_text_value"
    assert response.fallback_text == "fallback_text_value"
    assert response.argument_text == "argument_text_value"
    assert response.thread_reply is True
    assert response.client_assigned_message_id == "client_assigned_message_id_value"


def test_get_message_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_message), "__call__") as call:
        client.get_message()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == message.GetMessageRequest()


@pytest.mark.asyncio
async def test_get_message_async(
    transport: str = "grpc_asyncio", request_type=message.GetMessageRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_message), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            message.Message(
                name="name_value",
                text="text_value",
                formatted_text="formatted_text_value",
                fallback_text="fallback_text_value",
                argument_text="argument_text_value",
                thread_reply=True,
                client_assigned_message_id="client_assigned_message_id_value",
            )
        )
        response = await client.get_message(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == message.GetMessageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, message.Message)
    assert response.name == "name_value"
    assert response.text == "text_value"
    assert response.formatted_text == "formatted_text_value"
    assert response.fallback_text == "fallback_text_value"
    assert response.argument_text == "argument_text_value"
    assert response.thread_reply is True
    assert response.client_assigned_message_id == "client_assigned_message_id_value"


@pytest.mark.asyncio
async def test_get_message_async_from_dict():
    await test_get_message_async(request_type=dict)


def test_get_message_field_headers():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = message.GetMessageRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_message), "__call__") as call:
        call.return_value = message.Message()
        client.get_message(request)

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
async def test_get_message_field_headers_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = message.GetMessageRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_message), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(message.Message())
        await client.get_message(request)

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


def test_get_message_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_message), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = message.Message()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_message(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_message_flattened_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_message(
            message.GetMessageRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_message_flattened_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_message), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = message.Message()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(message.Message())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_message(
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
async def test_get_message_flattened_error_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_message(
            message.GetMessageRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gc_message.UpdateMessageRequest,
        dict,
    ],
)
def test_update_message(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_message), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gc_message.Message(
            name="name_value",
            text="text_value",
            formatted_text="formatted_text_value",
            fallback_text="fallback_text_value",
            argument_text="argument_text_value",
            thread_reply=True,
            client_assigned_message_id="client_assigned_message_id_value",
        )
        response = client.update_message(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gc_message.UpdateMessageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gc_message.Message)
    assert response.name == "name_value"
    assert response.text == "text_value"
    assert response.formatted_text == "formatted_text_value"
    assert response.fallback_text == "fallback_text_value"
    assert response.argument_text == "argument_text_value"
    assert response.thread_reply is True
    assert response.client_assigned_message_id == "client_assigned_message_id_value"


def test_update_message_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_message), "__call__") as call:
        client.update_message()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gc_message.UpdateMessageRequest()


@pytest.mark.asyncio
async def test_update_message_async(
    transport: str = "grpc_asyncio", request_type=gc_message.UpdateMessageRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_message), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gc_message.Message(
                name="name_value",
                text="text_value",
                formatted_text="formatted_text_value",
                fallback_text="fallback_text_value",
                argument_text="argument_text_value",
                thread_reply=True,
                client_assigned_message_id="client_assigned_message_id_value",
            )
        )
        response = await client.update_message(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gc_message.UpdateMessageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gc_message.Message)
    assert response.name == "name_value"
    assert response.text == "text_value"
    assert response.formatted_text == "formatted_text_value"
    assert response.fallback_text == "fallback_text_value"
    assert response.argument_text == "argument_text_value"
    assert response.thread_reply is True
    assert response.client_assigned_message_id == "client_assigned_message_id_value"


@pytest.mark.asyncio
async def test_update_message_async_from_dict():
    await test_update_message_async(request_type=dict)


def test_update_message_field_headers():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gc_message.UpdateMessageRequest()

    request.message.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_message), "__call__") as call:
        call.return_value = gc_message.Message()
        client.update_message(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "message.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_message_field_headers_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gc_message.UpdateMessageRequest()

    request.message.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_message), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gc_message.Message())
        await client.update_message(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "message.name=name_value",
    ) in kw["metadata"]


def test_update_message_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_message), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gc_message.Message()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_message(
            message=gc_message.Message(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].message
        mock_val = gc_message.Message(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_message_flattened_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_message(
            gc_message.UpdateMessageRequest(),
            message=gc_message.Message(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_message_flattened_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_message), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gc_message.Message()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gc_message.Message())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_message(
            message=gc_message.Message(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].message
        mock_val = gc_message.Message(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_message_flattened_error_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_message(
            gc_message.UpdateMessageRequest(),
            message=gc_message.Message(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        message.DeleteMessageRequest,
        dict,
    ],
)
def test_delete_message(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_message), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_message(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == message.DeleteMessageRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_message_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_message), "__call__") as call:
        client.delete_message()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == message.DeleteMessageRequest()


@pytest.mark.asyncio
async def test_delete_message_async(
    transport: str = "grpc_asyncio", request_type=message.DeleteMessageRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_message), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_message(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == message.DeleteMessageRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_message_async_from_dict():
    await test_delete_message_async(request_type=dict)


def test_delete_message_field_headers():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = message.DeleteMessageRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_message), "__call__") as call:
        call.return_value = None
        client.delete_message(request)

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
async def test_delete_message_field_headers_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = message.DeleteMessageRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_message), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_message(request)

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


def test_delete_message_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_message), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_message(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_message_flattened_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_message(
            message.DeleteMessageRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_message_flattened_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_message), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_message(
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
async def test_delete_message_flattened_error_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_message(
            message.DeleteMessageRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        attachment.GetAttachmentRequest,
        dict,
    ],
)
def test_get_attachment(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_attachment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = attachment.Attachment(
            name="name_value",
            content_name="content_name_value",
            content_type="content_type_value",
            thumbnail_uri="thumbnail_uri_value",
            download_uri="download_uri_value",
            source=attachment.Attachment.Source.DRIVE_FILE,
        )
        response = client.get_attachment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == attachment.GetAttachmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, attachment.Attachment)
    assert response.name == "name_value"
    assert response.content_name == "content_name_value"
    assert response.content_type == "content_type_value"
    assert response.thumbnail_uri == "thumbnail_uri_value"
    assert response.download_uri == "download_uri_value"
    assert response.source == attachment.Attachment.Source.DRIVE_FILE


def test_get_attachment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_attachment), "__call__") as call:
        client.get_attachment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attachment.GetAttachmentRequest()


@pytest.mark.asyncio
async def test_get_attachment_async(
    transport: str = "grpc_asyncio", request_type=attachment.GetAttachmentRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_attachment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attachment.Attachment(
                name="name_value",
                content_name="content_name_value",
                content_type="content_type_value",
                thumbnail_uri="thumbnail_uri_value",
                download_uri="download_uri_value",
                source=attachment.Attachment.Source.DRIVE_FILE,
            )
        )
        response = await client.get_attachment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == attachment.GetAttachmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, attachment.Attachment)
    assert response.name == "name_value"
    assert response.content_name == "content_name_value"
    assert response.content_type == "content_type_value"
    assert response.thumbnail_uri == "thumbnail_uri_value"
    assert response.download_uri == "download_uri_value"
    assert response.source == attachment.Attachment.Source.DRIVE_FILE


@pytest.mark.asyncio
async def test_get_attachment_async_from_dict():
    await test_get_attachment_async(request_type=dict)


def test_get_attachment_field_headers():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attachment.GetAttachmentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_attachment), "__call__") as call:
        call.return_value = attachment.Attachment()
        client.get_attachment(request)

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
async def test_get_attachment_field_headers_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attachment.GetAttachmentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_attachment), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attachment.Attachment()
        )
        await client.get_attachment(request)

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


def test_get_attachment_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_attachment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = attachment.Attachment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_attachment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_attachment_flattened_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_attachment(
            attachment.GetAttachmentRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_attachment_flattened_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_attachment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = attachment.Attachment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attachment.Attachment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_attachment(
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
async def test_get_attachment_flattened_error_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_attachment(
            attachment.GetAttachmentRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        attachment.UploadAttachmentRequest,
        dict,
    ],
)
def test_upload_attachment(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.upload_attachment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = attachment.UploadAttachmentResponse()
        response = client.upload_attachment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == attachment.UploadAttachmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, attachment.UploadAttachmentResponse)


def test_upload_attachment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.upload_attachment), "__call__"
    ) as call:
        client.upload_attachment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attachment.UploadAttachmentRequest()


@pytest.mark.asyncio
async def test_upload_attachment_async(
    transport: str = "grpc_asyncio", request_type=attachment.UploadAttachmentRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.upload_attachment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attachment.UploadAttachmentResponse()
        )
        response = await client.upload_attachment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == attachment.UploadAttachmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, attachment.UploadAttachmentResponse)


@pytest.mark.asyncio
async def test_upload_attachment_async_from_dict():
    await test_upload_attachment_async(request_type=dict)


def test_upload_attachment_field_headers():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attachment.UploadAttachmentRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.upload_attachment), "__call__"
    ) as call:
        call.return_value = attachment.UploadAttachmentResponse()
        client.upload_attachment(request)

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
async def test_upload_attachment_field_headers_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attachment.UploadAttachmentRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.upload_attachment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attachment.UploadAttachmentResponse()
        )
        await client.upload_attachment(request)

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
        space.ListSpacesRequest,
        dict,
    ],
)
def test_list_spaces(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_spaces), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = space.ListSpacesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_spaces(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == space.ListSpacesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSpacesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_spaces_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_spaces), "__call__") as call:
        client.list_spaces()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == space.ListSpacesRequest()


@pytest.mark.asyncio
async def test_list_spaces_async(
    transport: str = "grpc_asyncio", request_type=space.ListSpacesRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_spaces), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            space.ListSpacesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_spaces(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == space.ListSpacesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSpacesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_spaces_async_from_dict():
    await test_list_spaces_async(request_type=dict)


def test_list_spaces_pager(transport_name: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_spaces), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            space.ListSpacesResponse(
                spaces=[
                    space.Space(),
                    space.Space(),
                    space.Space(),
                ],
                next_page_token="abc",
            ),
            space.ListSpacesResponse(
                spaces=[],
                next_page_token="def",
            ),
            space.ListSpacesResponse(
                spaces=[
                    space.Space(),
                ],
                next_page_token="ghi",
            ),
            space.ListSpacesResponse(
                spaces=[
                    space.Space(),
                    space.Space(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_spaces(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, space.Space) for i in results)


def test_list_spaces_pages(transport_name: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_spaces), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            space.ListSpacesResponse(
                spaces=[
                    space.Space(),
                    space.Space(),
                    space.Space(),
                ],
                next_page_token="abc",
            ),
            space.ListSpacesResponse(
                spaces=[],
                next_page_token="def",
            ),
            space.ListSpacesResponse(
                spaces=[
                    space.Space(),
                ],
                next_page_token="ghi",
            ),
            space.ListSpacesResponse(
                spaces=[
                    space.Space(),
                    space.Space(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_spaces(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_spaces_async_pager():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_spaces), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            space.ListSpacesResponse(
                spaces=[
                    space.Space(),
                    space.Space(),
                    space.Space(),
                ],
                next_page_token="abc",
            ),
            space.ListSpacesResponse(
                spaces=[],
                next_page_token="def",
            ),
            space.ListSpacesResponse(
                spaces=[
                    space.Space(),
                ],
                next_page_token="ghi",
            ),
            space.ListSpacesResponse(
                spaces=[
                    space.Space(),
                    space.Space(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_spaces(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, space.Space) for i in responses)


@pytest.mark.asyncio
async def test_list_spaces_async_pages():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_spaces), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            space.ListSpacesResponse(
                spaces=[
                    space.Space(),
                    space.Space(),
                    space.Space(),
                ],
                next_page_token="abc",
            ),
            space.ListSpacesResponse(
                spaces=[],
                next_page_token="def",
            ),
            space.ListSpacesResponse(
                spaces=[
                    space.Space(),
                ],
                next_page_token="ghi",
            ),
            space.ListSpacesResponse(
                spaces=[
                    space.Space(),
                    space.Space(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_spaces(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        space.GetSpaceRequest,
        dict,
    ],
)
def test_get_space(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_space), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = space.Space(
            name="name_value",
            type_=space.Space.Type.ROOM,
            space_type=space.Space.SpaceType.SPACE,
            single_user_bot_dm=True,
            threaded=True,
            display_name="display_name_value",
            external_user_allowed=True,
            space_threading_state=space.Space.SpaceThreadingState.THREADED_MESSAGES,
            space_history_state=history_state.HistoryState.HISTORY_OFF,
            import_mode=True,
            admin_installed=True,
        )
        response = client.get_space(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == space.GetSpaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, space.Space)
    assert response.name == "name_value"
    assert response.type_ == space.Space.Type.ROOM
    assert response.space_type == space.Space.SpaceType.SPACE
    assert response.single_user_bot_dm is True
    assert response.threaded is True
    assert response.display_name == "display_name_value"
    assert response.external_user_allowed is True
    assert (
        response.space_threading_state
        == space.Space.SpaceThreadingState.THREADED_MESSAGES
    )
    assert response.space_history_state == history_state.HistoryState.HISTORY_OFF
    assert response.import_mode is True
    assert response.admin_installed is True


def test_get_space_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_space), "__call__") as call:
        client.get_space()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == space.GetSpaceRequest()


@pytest.mark.asyncio
async def test_get_space_async(
    transport: str = "grpc_asyncio", request_type=space.GetSpaceRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_space), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            space.Space(
                name="name_value",
                type_=space.Space.Type.ROOM,
                space_type=space.Space.SpaceType.SPACE,
                single_user_bot_dm=True,
                threaded=True,
                display_name="display_name_value",
                external_user_allowed=True,
                space_threading_state=space.Space.SpaceThreadingState.THREADED_MESSAGES,
                space_history_state=history_state.HistoryState.HISTORY_OFF,
                import_mode=True,
                admin_installed=True,
            )
        )
        response = await client.get_space(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == space.GetSpaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, space.Space)
    assert response.name == "name_value"
    assert response.type_ == space.Space.Type.ROOM
    assert response.space_type == space.Space.SpaceType.SPACE
    assert response.single_user_bot_dm is True
    assert response.threaded is True
    assert response.display_name == "display_name_value"
    assert response.external_user_allowed is True
    assert (
        response.space_threading_state
        == space.Space.SpaceThreadingState.THREADED_MESSAGES
    )
    assert response.space_history_state == history_state.HistoryState.HISTORY_OFF
    assert response.import_mode is True
    assert response.admin_installed is True


@pytest.mark.asyncio
async def test_get_space_async_from_dict():
    await test_get_space_async(request_type=dict)


def test_get_space_field_headers():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = space.GetSpaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_space), "__call__") as call:
        call.return_value = space.Space()
        client.get_space(request)

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
async def test_get_space_field_headers_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = space.GetSpaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_space), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(space.Space())
        await client.get_space(request)

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


def test_get_space_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_space), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = space.Space()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_space(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_space_flattened_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_space(
            space.GetSpaceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_space_flattened_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_space), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = space.Space()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(space.Space())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_space(
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
async def test_get_space_flattened_error_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_space(
            space.GetSpaceRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gc_space.CreateSpaceRequest,
        dict,
    ],
)
def test_create_space(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_space), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gc_space.Space(
            name="name_value",
            type_=gc_space.Space.Type.ROOM,
            space_type=gc_space.Space.SpaceType.SPACE,
            single_user_bot_dm=True,
            threaded=True,
            display_name="display_name_value",
            external_user_allowed=True,
            space_threading_state=gc_space.Space.SpaceThreadingState.THREADED_MESSAGES,
            space_history_state=history_state.HistoryState.HISTORY_OFF,
            import_mode=True,
            admin_installed=True,
        )
        response = client.create_space(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gc_space.CreateSpaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gc_space.Space)
    assert response.name == "name_value"
    assert response.type_ == gc_space.Space.Type.ROOM
    assert response.space_type == gc_space.Space.SpaceType.SPACE
    assert response.single_user_bot_dm is True
    assert response.threaded is True
    assert response.display_name == "display_name_value"
    assert response.external_user_allowed is True
    assert (
        response.space_threading_state
        == gc_space.Space.SpaceThreadingState.THREADED_MESSAGES
    )
    assert response.space_history_state == history_state.HistoryState.HISTORY_OFF
    assert response.import_mode is True
    assert response.admin_installed is True


def test_create_space_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_space), "__call__") as call:
        client.create_space()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gc_space.CreateSpaceRequest()


@pytest.mark.asyncio
async def test_create_space_async(
    transport: str = "grpc_asyncio", request_type=gc_space.CreateSpaceRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_space), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gc_space.Space(
                name="name_value",
                type_=gc_space.Space.Type.ROOM,
                space_type=gc_space.Space.SpaceType.SPACE,
                single_user_bot_dm=True,
                threaded=True,
                display_name="display_name_value",
                external_user_allowed=True,
                space_threading_state=gc_space.Space.SpaceThreadingState.THREADED_MESSAGES,
                space_history_state=history_state.HistoryState.HISTORY_OFF,
                import_mode=True,
                admin_installed=True,
            )
        )
        response = await client.create_space(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gc_space.CreateSpaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gc_space.Space)
    assert response.name == "name_value"
    assert response.type_ == gc_space.Space.Type.ROOM
    assert response.space_type == gc_space.Space.SpaceType.SPACE
    assert response.single_user_bot_dm is True
    assert response.threaded is True
    assert response.display_name == "display_name_value"
    assert response.external_user_allowed is True
    assert (
        response.space_threading_state
        == gc_space.Space.SpaceThreadingState.THREADED_MESSAGES
    )
    assert response.space_history_state == history_state.HistoryState.HISTORY_OFF
    assert response.import_mode is True
    assert response.admin_installed is True


@pytest.mark.asyncio
async def test_create_space_async_from_dict():
    await test_create_space_async(request_type=dict)


def test_create_space_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_space), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gc_space.Space()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_space(
            space=gc_space.Space(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].space
        mock_val = gc_space.Space(name="name_value")
        assert arg == mock_val


def test_create_space_flattened_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_space(
            gc_space.CreateSpaceRequest(),
            space=gc_space.Space(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_space_flattened_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_space), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gc_space.Space()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gc_space.Space())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_space(
            space=gc_space.Space(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].space
        mock_val = gc_space.Space(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_space_flattened_error_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_space(
            gc_space.CreateSpaceRequest(),
            space=gc_space.Space(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        space_setup.SetUpSpaceRequest,
        dict,
    ],
)
def test_set_up_space(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_up_space), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = space.Space(
            name="name_value",
            type_=space.Space.Type.ROOM,
            space_type=space.Space.SpaceType.SPACE,
            single_user_bot_dm=True,
            threaded=True,
            display_name="display_name_value",
            external_user_allowed=True,
            space_threading_state=space.Space.SpaceThreadingState.THREADED_MESSAGES,
            space_history_state=history_state.HistoryState.HISTORY_OFF,
            import_mode=True,
            admin_installed=True,
        )
        response = client.set_up_space(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == space_setup.SetUpSpaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, space.Space)
    assert response.name == "name_value"
    assert response.type_ == space.Space.Type.ROOM
    assert response.space_type == space.Space.SpaceType.SPACE
    assert response.single_user_bot_dm is True
    assert response.threaded is True
    assert response.display_name == "display_name_value"
    assert response.external_user_allowed is True
    assert (
        response.space_threading_state
        == space.Space.SpaceThreadingState.THREADED_MESSAGES
    )
    assert response.space_history_state == history_state.HistoryState.HISTORY_OFF
    assert response.import_mode is True
    assert response.admin_installed is True


def test_set_up_space_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_up_space), "__call__") as call:
        client.set_up_space()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == space_setup.SetUpSpaceRequest()


@pytest.mark.asyncio
async def test_set_up_space_async(
    transport: str = "grpc_asyncio", request_type=space_setup.SetUpSpaceRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_up_space), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            space.Space(
                name="name_value",
                type_=space.Space.Type.ROOM,
                space_type=space.Space.SpaceType.SPACE,
                single_user_bot_dm=True,
                threaded=True,
                display_name="display_name_value",
                external_user_allowed=True,
                space_threading_state=space.Space.SpaceThreadingState.THREADED_MESSAGES,
                space_history_state=history_state.HistoryState.HISTORY_OFF,
                import_mode=True,
                admin_installed=True,
            )
        )
        response = await client.set_up_space(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == space_setup.SetUpSpaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, space.Space)
    assert response.name == "name_value"
    assert response.type_ == space.Space.Type.ROOM
    assert response.space_type == space.Space.SpaceType.SPACE
    assert response.single_user_bot_dm is True
    assert response.threaded is True
    assert response.display_name == "display_name_value"
    assert response.external_user_allowed is True
    assert (
        response.space_threading_state
        == space.Space.SpaceThreadingState.THREADED_MESSAGES
    )
    assert response.space_history_state == history_state.HistoryState.HISTORY_OFF
    assert response.import_mode is True
    assert response.admin_installed is True


@pytest.mark.asyncio
async def test_set_up_space_async_from_dict():
    await test_set_up_space_async(request_type=dict)


@pytest.mark.parametrize(
    "request_type",
    [
        gc_space.UpdateSpaceRequest,
        dict,
    ],
)
def test_update_space(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_space), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gc_space.Space(
            name="name_value",
            type_=gc_space.Space.Type.ROOM,
            space_type=gc_space.Space.SpaceType.SPACE,
            single_user_bot_dm=True,
            threaded=True,
            display_name="display_name_value",
            external_user_allowed=True,
            space_threading_state=gc_space.Space.SpaceThreadingState.THREADED_MESSAGES,
            space_history_state=history_state.HistoryState.HISTORY_OFF,
            import_mode=True,
            admin_installed=True,
        )
        response = client.update_space(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gc_space.UpdateSpaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gc_space.Space)
    assert response.name == "name_value"
    assert response.type_ == gc_space.Space.Type.ROOM
    assert response.space_type == gc_space.Space.SpaceType.SPACE
    assert response.single_user_bot_dm is True
    assert response.threaded is True
    assert response.display_name == "display_name_value"
    assert response.external_user_allowed is True
    assert (
        response.space_threading_state
        == gc_space.Space.SpaceThreadingState.THREADED_MESSAGES
    )
    assert response.space_history_state == history_state.HistoryState.HISTORY_OFF
    assert response.import_mode is True
    assert response.admin_installed is True


def test_update_space_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_space), "__call__") as call:
        client.update_space()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gc_space.UpdateSpaceRequest()


@pytest.mark.asyncio
async def test_update_space_async(
    transport: str = "grpc_asyncio", request_type=gc_space.UpdateSpaceRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_space), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gc_space.Space(
                name="name_value",
                type_=gc_space.Space.Type.ROOM,
                space_type=gc_space.Space.SpaceType.SPACE,
                single_user_bot_dm=True,
                threaded=True,
                display_name="display_name_value",
                external_user_allowed=True,
                space_threading_state=gc_space.Space.SpaceThreadingState.THREADED_MESSAGES,
                space_history_state=history_state.HistoryState.HISTORY_OFF,
                import_mode=True,
                admin_installed=True,
            )
        )
        response = await client.update_space(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gc_space.UpdateSpaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gc_space.Space)
    assert response.name == "name_value"
    assert response.type_ == gc_space.Space.Type.ROOM
    assert response.space_type == gc_space.Space.SpaceType.SPACE
    assert response.single_user_bot_dm is True
    assert response.threaded is True
    assert response.display_name == "display_name_value"
    assert response.external_user_allowed is True
    assert (
        response.space_threading_state
        == gc_space.Space.SpaceThreadingState.THREADED_MESSAGES
    )
    assert response.space_history_state == history_state.HistoryState.HISTORY_OFF
    assert response.import_mode is True
    assert response.admin_installed is True


@pytest.mark.asyncio
async def test_update_space_async_from_dict():
    await test_update_space_async(request_type=dict)


def test_update_space_field_headers():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gc_space.UpdateSpaceRequest()

    request.space.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_space), "__call__") as call:
        call.return_value = gc_space.Space()
        client.update_space(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "space.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_space_field_headers_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gc_space.UpdateSpaceRequest()

    request.space.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_space), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gc_space.Space())
        await client.update_space(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "space.name=name_value",
    ) in kw["metadata"]


def test_update_space_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_space), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gc_space.Space()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_space(
            space=gc_space.Space(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].space
        mock_val = gc_space.Space(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_space_flattened_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_space(
            gc_space.UpdateSpaceRequest(),
            space=gc_space.Space(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_space_flattened_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_space), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gc_space.Space()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gc_space.Space())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_space(
            space=gc_space.Space(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].space
        mock_val = gc_space.Space(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_space_flattened_error_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_space(
            gc_space.UpdateSpaceRequest(),
            space=gc_space.Space(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        space.DeleteSpaceRequest,
        dict,
    ],
)
def test_delete_space(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_space), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_space(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == space.DeleteSpaceRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_space_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_space), "__call__") as call:
        client.delete_space()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == space.DeleteSpaceRequest()


@pytest.mark.asyncio
async def test_delete_space_async(
    transport: str = "grpc_asyncio", request_type=space.DeleteSpaceRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_space), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_space(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == space.DeleteSpaceRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_space_async_from_dict():
    await test_delete_space_async(request_type=dict)


def test_delete_space_field_headers():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = space.DeleteSpaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_space), "__call__") as call:
        call.return_value = None
        client.delete_space(request)

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
async def test_delete_space_field_headers_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = space.DeleteSpaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_space), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_space(request)

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


def test_delete_space_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_space), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_space(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_space_flattened_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_space(
            space.DeleteSpaceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_space_flattened_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_space), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_space(
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
async def test_delete_space_flattened_error_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_space(
            space.DeleteSpaceRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        space.CompleteImportSpaceRequest,
        dict,
    ],
)
def test_complete_import_space(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_import_space), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = space.CompleteImportSpaceResponse()
        response = client.complete_import_space(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == space.CompleteImportSpaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, space.CompleteImportSpaceResponse)


def test_complete_import_space_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_import_space), "__call__"
    ) as call:
        client.complete_import_space()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == space.CompleteImportSpaceRequest()


@pytest.mark.asyncio
async def test_complete_import_space_async(
    transport: str = "grpc_asyncio", request_type=space.CompleteImportSpaceRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_import_space), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            space.CompleteImportSpaceResponse()
        )
        response = await client.complete_import_space(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == space.CompleteImportSpaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, space.CompleteImportSpaceResponse)


@pytest.mark.asyncio
async def test_complete_import_space_async_from_dict():
    await test_complete_import_space_async(request_type=dict)


def test_complete_import_space_field_headers():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = space.CompleteImportSpaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_import_space), "__call__"
    ) as call:
        call.return_value = space.CompleteImportSpaceResponse()
        client.complete_import_space(request)

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
async def test_complete_import_space_field_headers_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = space.CompleteImportSpaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_import_space), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            space.CompleteImportSpaceResponse()
        )
        await client.complete_import_space(request)

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
        space.FindDirectMessageRequest,
        dict,
    ],
)
def test_find_direct_message(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.find_direct_message), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = space.Space(
            name="name_value",
            type_=space.Space.Type.ROOM,
            space_type=space.Space.SpaceType.SPACE,
            single_user_bot_dm=True,
            threaded=True,
            display_name="display_name_value",
            external_user_allowed=True,
            space_threading_state=space.Space.SpaceThreadingState.THREADED_MESSAGES,
            space_history_state=history_state.HistoryState.HISTORY_OFF,
            import_mode=True,
            admin_installed=True,
        )
        response = client.find_direct_message(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == space.FindDirectMessageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, space.Space)
    assert response.name == "name_value"
    assert response.type_ == space.Space.Type.ROOM
    assert response.space_type == space.Space.SpaceType.SPACE
    assert response.single_user_bot_dm is True
    assert response.threaded is True
    assert response.display_name == "display_name_value"
    assert response.external_user_allowed is True
    assert (
        response.space_threading_state
        == space.Space.SpaceThreadingState.THREADED_MESSAGES
    )
    assert response.space_history_state == history_state.HistoryState.HISTORY_OFF
    assert response.import_mode is True
    assert response.admin_installed is True


def test_find_direct_message_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.find_direct_message), "__call__"
    ) as call:
        client.find_direct_message()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == space.FindDirectMessageRequest()


@pytest.mark.asyncio
async def test_find_direct_message_async(
    transport: str = "grpc_asyncio", request_type=space.FindDirectMessageRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.find_direct_message), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            space.Space(
                name="name_value",
                type_=space.Space.Type.ROOM,
                space_type=space.Space.SpaceType.SPACE,
                single_user_bot_dm=True,
                threaded=True,
                display_name="display_name_value",
                external_user_allowed=True,
                space_threading_state=space.Space.SpaceThreadingState.THREADED_MESSAGES,
                space_history_state=history_state.HistoryState.HISTORY_OFF,
                import_mode=True,
                admin_installed=True,
            )
        )
        response = await client.find_direct_message(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == space.FindDirectMessageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, space.Space)
    assert response.name == "name_value"
    assert response.type_ == space.Space.Type.ROOM
    assert response.space_type == space.Space.SpaceType.SPACE
    assert response.single_user_bot_dm is True
    assert response.threaded is True
    assert response.display_name == "display_name_value"
    assert response.external_user_allowed is True
    assert (
        response.space_threading_state
        == space.Space.SpaceThreadingState.THREADED_MESSAGES
    )
    assert response.space_history_state == history_state.HistoryState.HISTORY_OFF
    assert response.import_mode is True
    assert response.admin_installed is True


@pytest.mark.asyncio
async def test_find_direct_message_async_from_dict():
    await test_find_direct_message_async(request_type=dict)


@pytest.mark.parametrize(
    "request_type",
    [
        gc_membership.CreateMembershipRequest,
        dict,
    ],
)
def test_create_membership(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_membership), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gc_membership.Membership(
            name="name_value",
            state=gc_membership.Membership.MembershipState.JOINED,
            role=gc_membership.Membership.MembershipRole.ROLE_MEMBER,
        )
        response = client.create_membership(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gc_membership.CreateMembershipRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gc_membership.Membership)
    assert response.name == "name_value"
    assert response.state == gc_membership.Membership.MembershipState.JOINED
    assert response.role == gc_membership.Membership.MembershipRole.ROLE_MEMBER


def test_create_membership_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_membership), "__call__"
    ) as call:
        client.create_membership()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gc_membership.CreateMembershipRequest()


@pytest.mark.asyncio
async def test_create_membership_async(
    transport: str = "grpc_asyncio", request_type=gc_membership.CreateMembershipRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_membership), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gc_membership.Membership(
                name="name_value",
                state=gc_membership.Membership.MembershipState.JOINED,
                role=gc_membership.Membership.MembershipRole.ROLE_MEMBER,
            )
        )
        response = await client.create_membership(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gc_membership.CreateMembershipRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gc_membership.Membership)
    assert response.name == "name_value"
    assert response.state == gc_membership.Membership.MembershipState.JOINED
    assert response.role == gc_membership.Membership.MembershipRole.ROLE_MEMBER


@pytest.mark.asyncio
async def test_create_membership_async_from_dict():
    await test_create_membership_async(request_type=dict)


def test_create_membership_field_headers():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gc_membership.CreateMembershipRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_membership), "__call__"
    ) as call:
        call.return_value = gc_membership.Membership()
        client.create_membership(request)

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
async def test_create_membership_field_headers_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gc_membership.CreateMembershipRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_membership), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gc_membership.Membership()
        )
        await client.create_membership(request)

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


def test_create_membership_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_membership), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gc_membership.Membership()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_membership(
            parent="parent_value",
            membership=gc_membership.Membership(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].membership
        mock_val = gc_membership.Membership(name="name_value")
        assert arg == mock_val


def test_create_membership_flattened_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_membership(
            gc_membership.CreateMembershipRequest(),
            parent="parent_value",
            membership=gc_membership.Membership(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_membership_flattened_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_membership), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gc_membership.Membership()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gc_membership.Membership()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_membership(
            parent="parent_value",
            membership=gc_membership.Membership(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].membership
        mock_val = gc_membership.Membership(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_membership_flattened_error_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_membership(
            gc_membership.CreateMembershipRequest(),
            parent="parent_value",
            membership=gc_membership.Membership(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        membership.DeleteMembershipRequest,
        dict,
    ],
)
def test_delete_membership(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_membership), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = membership.Membership(
            name="name_value",
            state=membership.Membership.MembershipState.JOINED,
            role=membership.Membership.MembershipRole.ROLE_MEMBER,
        )
        response = client.delete_membership(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == membership.DeleteMembershipRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, membership.Membership)
    assert response.name == "name_value"
    assert response.state == membership.Membership.MembershipState.JOINED
    assert response.role == membership.Membership.MembershipRole.ROLE_MEMBER


def test_delete_membership_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_membership), "__call__"
    ) as call:
        client.delete_membership()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == membership.DeleteMembershipRequest()


@pytest.mark.asyncio
async def test_delete_membership_async(
    transport: str = "grpc_asyncio", request_type=membership.DeleteMembershipRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_membership), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            membership.Membership(
                name="name_value",
                state=membership.Membership.MembershipState.JOINED,
                role=membership.Membership.MembershipRole.ROLE_MEMBER,
            )
        )
        response = await client.delete_membership(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == membership.DeleteMembershipRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, membership.Membership)
    assert response.name == "name_value"
    assert response.state == membership.Membership.MembershipState.JOINED
    assert response.role == membership.Membership.MembershipRole.ROLE_MEMBER


@pytest.mark.asyncio
async def test_delete_membership_async_from_dict():
    await test_delete_membership_async(request_type=dict)


def test_delete_membership_field_headers():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = membership.DeleteMembershipRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_membership), "__call__"
    ) as call:
        call.return_value = membership.Membership()
        client.delete_membership(request)

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
async def test_delete_membership_field_headers_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = membership.DeleteMembershipRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_membership), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            membership.Membership()
        )
        await client.delete_membership(request)

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


def test_delete_membership_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_membership), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = membership.Membership()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_membership(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_membership_flattened_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_membership(
            membership.DeleteMembershipRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_membership_flattened_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_membership), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = membership.Membership()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            membership.Membership()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_membership(
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
async def test_delete_membership_flattened_error_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_membership(
            membership.DeleteMembershipRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gc_reaction.CreateReactionRequest,
        dict,
    ],
)
def test_create_reaction(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_reaction), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gc_reaction.Reaction(
            name="name_value",
        )
        response = client.create_reaction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gc_reaction.CreateReactionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gc_reaction.Reaction)
    assert response.name == "name_value"


def test_create_reaction_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_reaction), "__call__") as call:
        client.create_reaction()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gc_reaction.CreateReactionRequest()


@pytest.mark.asyncio
async def test_create_reaction_async(
    transport: str = "grpc_asyncio", request_type=gc_reaction.CreateReactionRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_reaction), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gc_reaction.Reaction(
                name="name_value",
            )
        )
        response = await client.create_reaction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gc_reaction.CreateReactionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gc_reaction.Reaction)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_create_reaction_async_from_dict():
    await test_create_reaction_async(request_type=dict)


def test_create_reaction_field_headers():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gc_reaction.CreateReactionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_reaction), "__call__") as call:
        call.return_value = gc_reaction.Reaction()
        client.create_reaction(request)

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
async def test_create_reaction_field_headers_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gc_reaction.CreateReactionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_reaction), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gc_reaction.Reaction()
        )
        await client.create_reaction(request)

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


def test_create_reaction_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_reaction), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gc_reaction.Reaction()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_reaction(
            parent="parent_value",
            reaction=gc_reaction.Reaction(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].reaction
        mock_val = gc_reaction.Reaction(name="name_value")
        assert arg == mock_val


def test_create_reaction_flattened_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_reaction(
            gc_reaction.CreateReactionRequest(),
            parent="parent_value",
            reaction=gc_reaction.Reaction(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_reaction_flattened_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_reaction), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gc_reaction.Reaction()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gc_reaction.Reaction()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_reaction(
            parent="parent_value",
            reaction=gc_reaction.Reaction(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].reaction
        mock_val = gc_reaction.Reaction(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_reaction_flattened_error_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_reaction(
            gc_reaction.CreateReactionRequest(),
            parent="parent_value",
            reaction=gc_reaction.Reaction(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        reaction.ListReactionsRequest,
        dict,
    ],
)
def test_list_reactions(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_reactions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = reaction.ListReactionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_reactions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == reaction.ListReactionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListReactionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_reactions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_reactions), "__call__") as call:
        client.list_reactions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == reaction.ListReactionsRequest()


@pytest.mark.asyncio
async def test_list_reactions_async(
    transport: str = "grpc_asyncio", request_type=reaction.ListReactionsRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_reactions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            reaction.ListReactionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_reactions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == reaction.ListReactionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListReactionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_reactions_async_from_dict():
    await test_list_reactions_async(request_type=dict)


def test_list_reactions_field_headers():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = reaction.ListReactionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_reactions), "__call__") as call:
        call.return_value = reaction.ListReactionsResponse()
        client.list_reactions(request)

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
async def test_list_reactions_field_headers_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = reaction.ListReactionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_reactions), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            reaction.ListReactionsResponse()
        )
        await client.list_reactions(request)

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


def test_list_reactions_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_reactions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = reaction.ListReactionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_reactions(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_reactions_flattened_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_reactions(
            reaction.ListReactionsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_reactions_flattened_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_reactions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = reaction.ListReactionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            reaction.ListReactionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_reactions(
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
async def test_list_reactions_flattened_error_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_reactions(
            reaction.ListReactionsRequest(),
            parent="parent_value",
        )


def test_list_reactions_pager(transport_name: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_reactions), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            reaction.ListReactionsResponse(
                reactions=[
                    reaction.Reaction(),
                    reaction.Reaction(),
                    reaction.Reaction(),
                ],
                next_page_token="abc",
            ),
            reaction.ListReactionsResponse(
                reactions=[],
                next_page_token="def",
            ),
            reaction.ListReactionsResponse(
                reactions=[
                    reaction.Reaction(),
                ],
                next_page_token="ghi",
            ),
            reaction.ListReactionsResponse(
                reactions=[
                    reaction.Reaction(),
                    reaction.Reaction(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_reactions(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, reaction.Reaction) for i in results)


def test_list_reactions_pages(transport_name: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_reactions), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            reaction.ListReactionsResponse(
                reactions=[
                    reaction.Reaction(),
                    reaction.Reaction(),
                    reaction.Reaction(),
                ],
                next_page_token="abc",
            ),
            reaction.ListReactionsResponse(
                reactions=[],
                next_page_token="def",
            ),
            reaction.ListReactionsResponse(
                reactions=[
                    reaction.Reaction(),
                ],
                next_page_token="ghi",
            ),
            reaction.ListReactionsResponse(
                reactions=[
                    reaction.Reaction(),
                    reaction.Reaction(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_reactions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_reactions_async_pager():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_reactions), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            reaction.ListReactionsResponse(
                reactions=[
                    reaction.Reaction(),
                    reaction.Reaction(),
                    reaction.Reaction(),
                ],
                next_page_token="abc",
            ),
            reaction.ListReactionsResponse(
                reactions=[],
                next_page_token="def",
            ),
            reaction.ListReactionsResponse(
                reactions=[
                    reaction.Reaction(),
                ],
                next_page_token="ghi",
            ),
            reaction.ListReactionsResponse(
                reactions=[
                    reaction.Reaction(),
                    reaction.Reaction(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_reactions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, reaction.Reaction) for i in responses)


@pytest.mark.asyncio
async def test_list_reactions_async_pages():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_reactions), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            reaction.ListReactionsResponse(
                reactions=[
                    reaction.Reaction(),
                    reaction.Reaction(),
                    reaction.Reaction(),
                ],
                next_page_token="abc",
            ),
            reaction.ListReactionsResponse(
                reactions=[],
                next_page_token="def",
            ),
            reaction.ListReactionsResponse(
                reactions=[
                    reaction.Reaction(),
                ],
                next_page_token="ghi",
            ),
            reaction.ListReactionsResponse(
                reactions=[
                    reaction.Reaction(),
                    reaction.Reaction(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_reactions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        reaction.DeleteReactionRequest,
        dict,
    ],
)
def test_delete_reaction(request_type, transport: str = "grpc"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_reaction), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_reaction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == reaction.DeleteReactionRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_reaction_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_reaction), "__call__") as call:
        client.delete_reaction()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == reaction.DeleteReactionRequest()


@pytest.mark.asyncio
async def test_delete_reaction_async(
    transport: str = "grpc_asyncio", request_type=reaction.DeleteReactionRequest
):
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_reaction), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_reaction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == reaction.DeleteReactionRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_reaction_async_from_dict():
    await test_delete_reaction_async(request_type=dict)


def test_delete_reaction_field_headers():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = reaction.DeleteReactionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_reaction), "__call__") as call:
        call.return_value = None
        client.delete_reaction(request)

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
async def test_delete_reaction_field_headers_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = reaction.DeleteReactionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_reaction), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_reaction(request)

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


def test_delete_reaction_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_reaction), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_reaction(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_reaction_flattened_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_reaction(
            reaction.DeleteReactionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_reaction_flattened_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_reaction), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_reaction(
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
async def test_delete_reaction_flattened_error_async():
    client = ChatServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_reaction(
            reaction.DeleteReactionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gc_message.CreateMessageRequest,
        dict,
    ],
)
def test_create_message_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "spaces/sample1"}
    request_init["message"] = {
        "name": "name_value",
        "sender": {
            "name": "name_value",
            "display_name": "display_name_value",
            "domain_id": "domain_id_value",
            "type_": 1,
            "is_anonymous": True,
        },
        "create_time": {"seconds": 751, "nanos": 543},
        "last_update_time": {},
        "delete_time": {},
        "text": "text_value",
        "formatted_text": "formatted_text_value",
        "cards": [
            {
                "header": {
                    "title": "title_value",
                    "subtitle": "subtitle_value",
                    "image_style": 1,
                    "image_url": "image_url_value",
                },
                "sections": [
                    {
                        "header": "header_value",
                        "widgets": [
                            {
                                "text_paragraph": {"text": "text_value"},
                                "image": {
                                    "image_url": "image_url_value",
                                    "on_click": {
                                        "action": {
                                            "action_method_name": "action_method_name_value",
                                            "parameters": [
                                                {
                                                    "key": "key_value",
                                                    "value": "value_value",
                                                }
                                            ],
                                        },
                                        "open_link": {"url": "url_value"},
                                    },
                                    "aspect_ratio": 0.1278,
                                },
                                "key_value": {
                                    "icon": 1,
                                    "icon_url": "icon_url_value",
                                    "top_label": "top_label_value",
                                    "content": "content_value",
                                    "content_multiline": True,
                                    "bottom_label": "bottom_label_value",
                                    "on_click": {},
                                    "button": {
                                        "text_button": {
                                            "text": "text_value",
                                            "on_click": {},
                                        },
                                        "image_button": {
                                            "icon": 1,
                                            "icon_url": "icon_url_value",
                                            "on_click": {},
                                            "name": "name_value",
                                        },
                                    },
                                },
                                "buttons": {},
                            }
                        ],
                    }
                ],
                "card_actions": [
                    {"action_label": "action_label_value", "on_click": {}}
                ],
                "name": "name_value",
            }
        ],
        "cards_v2": [
            {
                "card_id": "card_id_value",
                "card": {
                    "header": {
                        "title": "title_value",
                        "subtitle": "subtitle_value",
                        "image_type": 1,
                        "image_url": "image_url_value",
                        "image_alt_text": "image_alt_text_value",
                    },
                    "sections": [
                        {
                            "header": "header_value",
                            "widgets": [
                                {
                                    "text_paragraph": {"text": "text_value"},
                                    "image": {
                                        "image_url": "image_url_value",
                                        "on_click": {
                                            "action": {
                                                "function": "function_value",
                                                "parameters": [
                                                    {
                                                        "key": "key_value",
                                                        "value": "value_value",
                                                    }
                                                ],
                                                "load_indicator": 1,
                                                "persist_values": True,
                                                "interaction": 1,
                                            },
                                            "open_link": {
                                                "url": "url_value",
                                                "open_as": 1,
                                                "on_close": 1,
                                            },
                                            "open_dynamic_link_action": {},
                                            "card": {},
                                        },
                                        "alt_text": "alt_text_value",
                                    },
                                    "decorated_text": {
                                        "icon": {
                                            "known_icon": "known_icon_value",
                                            "icon_url": "icon_url_value",
                                            "alt_text": "alt_text_value",
                                            "image_type": 1,
                                        },
                                        "start_icon": {},
                                        "top_label": "top_label_value",
                                        "text": "text_value",
                                        "wrap_text": True,
                                        "bottom_label": "bottom_label_value",
                                        "on_click": {},
                                        "button": {
                                            "text": "text_value",
                                            "icon": {},
                                            "color": {
                                                "red": 0.315,
                                                "green": 0.529,
                                                "blue": 0.424,
                                                "alpha": {"value": 0.541},
                                            },
                                            "on_click": {},
                                            "disabled": True,
                                            "alt_text": "alt_text_value",
                                        },
                                        "switch_control": {
                                            "name": "name_value",
                                            "value": "value_value",
                                            "selected": True,
                                            "on_change_action": {},
                                            "control_type": 1,
                                        },
                                        "end_icon": {},
                                    },
                                    "button_list": {"buttons": {}},
                                    "text_input": {
                                        "name": "name_value",
                                        "label": "label_value",
                                        "hint_text": "hint_text_value",
                                        "value": "value_value",
                                        "type_": 1,
                                        "on_change_action": {},
                                        "initial_suggestions": {
                                            "items": [{"text": "text_value"}]
                                        },
                                        "auto_complete_action": {},
                                        "placeholder_text": "placeholder_text_value",
                                    },
                                    "selection_input": {
                                        "name": "name_value",
                                        "label": "label_value",
                                        "type_": 1,
                                        "items": [
                                            {
                                                "text": "text_value",
                                                "value": "value_value",
                                                "selected": True,
                                                "start_icon_uri": "start_icon_uri_value",
                                                "bottom_text": "bottom_text_value",
                                            }
                                        ],
                                        "on_change_action": {},
                                        "multi_select_max_selected_items": 3288,
                                        "multi_select_min_query_length": 3107,
                                        "external_data_source": {},
                                        "platform_data_source": {
                                            "common_data_source": 1
                                        },
                                    },
                                    "date_time_picker": {
                                        "name": "name_value",
                                        "label": "label_value",
                                        "type_": 1,
                                        "value_ms_epoch": 1482,
                                        "timezone_offset_date": 2126,
                                        "on_change_action": {},
                                    },
                                    "divider": {},
                                    "grid": {
                                        "title": "title_value",
                                        "items": [
                                            {
                                                "id": "id_value",
                                                "image": {
                                                    "image_uri": "image_uri_value",
                                                    "alt_text": "alt_text_value",
                                                    "crop_style": {
                                                        "type_": 1,
                                                        "aspect_ratio": 0.1278,
                                                    },
                                                    "border_style": {
                                                        "type_": 1,
                                                        "stroke_color": {},
                                                        "corner_radius": 1392,
                                                    },
                                                },
                                                "title": "title_value",
                                                "subtitle": "subtitle_value",
                                                "layout": 1,
                                            }
                                        ],
                                        "border_style": {},
                                        "column_count": 1302,
                                        "on_click": {},
                                    },
                                    "columns": {
                                        "column_items": [
                                            {
                                                "horizontal_size_style": 1,
                                                "horizontal_alignment": 1,
                                                "vertical_alignment": 1,
                                                "widgets": [
                                                    {
                                                        "text_paragraph": {},
                                                        "image": {},
                                                        "decorated_text": {},
                                                        "button_list": {},
                                                        "text_input": {},
                                                        "selection_input": {},
                                                        "date_time_picker": {},
                                                    }
                                                ],
                                            }
                                        ]
                                    },
                                    "horizontal_alignment": 1,
                                }
                            ],
                            "collapsible": True,
                            "uncollapsible_widgets_count": 2891,
                        }
                    ],
                    "section_divider_style": 1,
                    "card_actions": [
                        {"action_label": "action_label_value", "on_click": {}}
                    ],
                    "name": "name_value",
                    "fixed_footer": {"primary_button": {}, "secondary_button": {}},
                    "display_style": 1,
                    "peek_card_header": {},
                },
            }
        ],
        "annotations": [
            {
                "type_": 1,
                "start_index": 1189,
                "length": 642,
                "user_mention": {"user": {}, "type_": 1},
                "slash_command": {
                    "bot": {},
                    "type_": 1,
                    "command_name": "command_name_value",
                    "command_id": 1035,
                    "triggers_dialog": True,
                },
                "rich_link_metadata": {
                    "uri": "uri_value",
                    "rich_link_type": 1,
                    "drive_link_data": {
                        "drive_data_ref": {"drive_file_id": "drive_file_id_value"},
                        "mime_type": "mime_type_value",
                    },
                },
            }
        ],
        "thread": {"name": "name_value", "thread_key": "thread_key_value"},
        "space": {
            "name": "name_value",
            "type_": 1,
            "space_type": 1,
            "single_user_bot_dm": True,
            "threaded": True,
            "display_name": "display_name_value",
            "external_user_allowed": True,
            "space_threading_state": 2,
            "space_details": {
                "description": "description_value",
                "guidelines": "guidelines_value",
            },
            "space_history_state": 1,
            "import_mode": True,
            "create_time": {},
            "admin_installed": True,
        },
        "fallback_text": "fallback_text_value",
        "action_response": {
            "type_": 1,
            "url": "url_value",
            "dialog_action": {
                "dialog": {"body": {}},
                "action_status": {
                    "status_code": 1,
                    "user_facing_message": "user_facing_message_value",
                },
            },
            "updated_widget": {"suggestions": {"items": {}}, "widget": "widget_value"},
        },
        "argument_text": "argument_text_value",
        "slash_command": {"command_id": 1035},
        "attachment": [
            {
                "name": "name_value",
                "content_name": "content_name_value",
                "content_type": "content_type_value",
                "attachment_data_ref": {
                    "resource_name": "resource_name_value",
                    "attachment_upload_token": "attachment_upload_token_value",
                },
                "drive_data_ref": {},
                "thumbnail_uri": "thumbnail_uri_value",
                "download_uri": "download_uri_value",
                "source": 1,
            }
        ],
        "matched_url": {"url": "url_value"},
        "thread_reply": True,
        "client_assigned_message_id": "client_assigned_message_id_value",
        "emoji_reaction_summaries": [
            {
                "emoji": {
                    "unicode": "unicode_value",
                    "custom_emoji": {"uid": "uid_value"},
                },
                "reaction_count": 1501,
            }
        ],
        "private_message_viewer": {},
        "deletion_metadata": {"deletion_type": 1},
        "quoted_message_metadata": {"name": "name_value", "last_update_time": {}},
        "attached_gifs": [{"uri": "uri_value"}],
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = gc_message.CreateMessageRequest.meta.fields["message"]

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
    for field, value in request_init["message"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["message"][field])):
                    del request_init["message"][field][i][subfield]
            else:
                del request_init["message"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gc_message.Message(
            name="name_value",
            text="text_value",
            formatted_text="formatted_text_value",
            fallback_text="fallback_text_value",
            argument_text="argument_text_value",
            thread_reply=True,
            client_assigned_message_id="client_assigned_message_id_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gc_message.Message.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_message(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gc_message.Message)
    assert response.name == "name_value"
    assert response.text == "text_value"
    assert response.formatted_text == "formatted_text_value"
    assert response.fallback_text == "fallback_text_value"
    assert response.argument_text == "argument_text_value"
    assert response.thread_reply is True
    assert response.client_assigned_message_id == "client_assigned_message_id_value"


def test_create_message_rest_required_fields(
    request_type=gc_message.CreateMessageRequest,
):
    transport_class = transports.ChatServiceRestTransport

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
    ).create_message._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_message._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "message_id",
            "message_reply_option",
            "request_id",
            "thread_key",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gc_message.Message()
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
            return_value = gc_message.Message.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_message(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_message_rest_unset_required_fields():
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_message._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "messageId",
                "messageReplyOption",
                "requestId",
                "threadKey",
            )
        )
        & set(
            (
                "parent",
                "message",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_message_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "post_create_message"
    ) as post, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_create_message"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gc_message.CreateMessageRequest.pb(
            gc_message.CreateMessageRequest()
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
        req.return_value._content = gc_message.Message.to_json(gc_message.Message())

        request = gc_message.CreateMessageRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gc_message.Message()

        client.create_message(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_message_rest_bad_request(
    transport: str = "rest", request_type=gc_message.CreateMessageRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "spaces/sample1"}
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
        client.create_message(request)


def test_create_message_rest_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gc_message.Message()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "spaces/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            message=gc_message.Message(name="name_value"),
            message_id="message_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gc_message.Message.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_message(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=spaces/*}/messages" % client.transport._host, args[1]
        )


def test_create_message_rest_flattened_error(transport: str = "rest"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_message(
            gc_message.CreateMessageRequest(),
            parent="parent_value",
            message=gc_message.Message(name="name_value"),
            message_id="message_id_value",
        )


def test_create_message_rest_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        message.ListMessagesRequest,
        dict,
    ],
)
def test_list_messages_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "spaces/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = message.ListMessagesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = message.ListMessagesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_messages(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMessagesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_messages_rest_required_fields(request_type=message.ListMessagesRequest):
    transport_class = transports.ChatServiceRestTransport

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
    ).list_messages._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_messages._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "order_by",
            "page_size",
            "page_token",
            "show_deleted",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = message.ListMessagesResponse()
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
            return_value = message.ListMessagesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_messages(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_messages_rest_unset_required_fields():
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_messages._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "orderBy",
                "pageSize",
                "pageToken",
                "showDeleted",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_messages_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "post_list_messages"
    ) as post, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_list_messages"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = message.ListMessagesRequest.pb(message.ListMessagesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = message.ListMessagesResponse.to_json(
            message.ListMessagesResponse()
        )

        request = message.ListMessagesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = message.ListMessagesResponse()

        client.list_messages(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_messages_rest_bad_request(
    transport: str = "rest", request_type=message.ListMessagesRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "spaces/sample1"}
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
        client.list_messages(request)


def test_list_messages_rest_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = message.ListMessagesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "spaces/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = message.ListMessagesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_messages(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=spaces/*}/messages" % client.transport._host, args[1]
        )


def test_list_messages_rest_flattened_error(transport: str = "rest"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_messages(
            message.ListMessagesRequest(),
            parent="parent_value",
        )


def test_list_messages_rest_pager(transport: str = "rest"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            message.ListMessagesResponse(
                messages=[
                    message.Message(),
                    message.Message(),
                    message.Message(),
                ],
                next_page_token="abc",
            ),
            message.ListMessagesResponse(
                messages=[],
                next_page_token="def",
            ),
            message.ListMessagesResponse(
                messages=[
                    message.Message(),
                ],
                next_page_token="ghi",
            ),
            message.ListMessagesResponse(
                messages=[
                    message.Message(),
                    message.Message(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(message.ListMessagesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "spaces/sample1"}

        pager = client.list_messages(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, message.Message) for i in results)

        pages = list(client.list_messages(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        membership.ListMembershipsRequest,
        dict,
    ],
)
def test_list_memberships_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "spaces/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = membership.ListMembershipsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = membership.ListMembershipsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_memberships(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMembershipsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_memberships_rest_required_fields(
    request_type=membership.ListMembershipsRequest,
):
    transport_class = transports.ChatServiceRestTransport

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
    ).list_memberships._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_memberships._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "page_size",
            "page_token",
            "show_groups",
            "show_invited",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = membership.ListMembershipsResponse()
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
            return_value = membership.ListMembershipsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_memberships(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_memberships_rest_unset_required_fields():
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_memberships._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "pageSize",
                "pageToken",
                "showGroups",
                "showInvited",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_memberships_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "post_list_memberships"
    ) as post, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_list_memberships"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = membership.ListMembershipsRequest.pb(
            membership.ListMembershipsRequest()
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
        req.return_value._content = membership.ListMembershipsResponse.to_json(
            membership.ListMembershipsResponse()
        )

        request = membership.ListMembershipsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = membership.ListMembershipsResponse()

        client.list_memberships(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_memberships_rest_bad_request(
    transport: str = "rest", request_type=membership.ListMembershipsRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "spaces/sample1"}
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
        client.list_memberships(request)


def test_list_memberships_rest_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = membership.ListMembershipsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "spaces/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = membership.ListMembershipsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_memberships(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=spaces/*}/members" % client.transport._host, args[1]
        )


def test_list_memberships_rest_flattened_error(transport: str = "rest"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_memberships(
            membership.ListMembershipsRequest(),
            parent="parent_value",
        )


def test_list_memberships_rest_pager(transport: str = "rest"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            membership.ListMembershipsResponse(
                memberships=[
                    membership.Membership(),
                    membership.Membership(),
                    membership.Membership(),
                ],
                next_page_token="abc",
            ),
            membership.ListMembershipsResponse(
                memberships=[],
                next_page_token="def",
            ),
            membership.ListMembershipsResponse(
                memberships=[
                    membership.Membership(),
                ],
                next_page_token="ghi",
            ),
            membership.ListMembershipsResponse(
                memberships=[
                    membership.Membership(),
                    membership.Membership(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            membership.ListMembershipsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "spaces/sample1"}

        pager = client.list_memberships(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, membership.Membership) for i in results)

        pages = list(client.list_memberships(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        membership.GetMembershipRequest,
        dict,
    ],
)
def test_get_membership_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "spaces/sample1/members/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = membership.Membership(
            name="name_value",
            state=membership.Membership.MembershipState.JOINED,
            role=membership.Membership.MembershipRole.ROLE_MEMBER,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = membership.Membership.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_membership(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, membership.Membership)
    assert response.name == "name_value"
    assert response.state == membership.Membership.MembershipState.JOINED
    assert response.role == membership.Membership.MembershipRole.ROLE_MEMBER


def test_get_membership_rest_required_fields(
    request_type=membership.GetMembershipRequest,
):
    transport_class = transports.ChatServiceRestTransport

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
    ).get_membership._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_membership._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = membership.Membership()
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
            return_value = membership.Membership.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_membership(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_membership_rest_unset_required_fields():
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_membership._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_membership_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "post_get_membership"
    ) as post, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_get_membership"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = membership.GetMembershipRequest.pb(
            membership.GetMembershipRequest()
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
        req.return_value._content = membership.Membership.to_json(
            membership.Membership()
        )

        request = membership.GetMembershipRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = membership.Membership()

        client.get_membership(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_membership_rest_bad_request(
    transport: str = "rest", request_type=membership.GetMembershipRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "spaces/sample1/members/sample2"}
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
        client.get_membership(request)


def test_get_membership_rest_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = membership.Membership()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "spaces/sample1/members/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = membership.Membership.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_membership(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=spaces/*/members/*}" % client.transport._host, args[1]
        )


def test_get_membership_rest_flattened_error(transport: str = "rest"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_membership(
            membership.GetMembershipRequest(),
            name="name_value",
        )


def test_get_membership_rest_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        message.GetMessageRequest,
        dict,
    ],
)
def test_get_message_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "spaces/sample1/messages/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = message.Message(
            name="name_value",
            text="text_value",
            formatted_text="formatted_text_value",
            fallback_text="fallback_text_value",
            argument_text="argument_text_value",
            thread_reply=True,
            client_assigned_message_id="client_assigned_message_id_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = message.Message.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_message(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, message.Message)
    assert response.name == "name_value"
    assert response.text == "text_value"
    assert response.formatted_text == "formatted_text_value"
    assert response.fallback_text == "fallback_text_value"
    assert response.argument_text == "argument_text_value"
    assert response.thread_reply is True
    assert response.client_assigned_message_id == "client_assigned_message_id_value"


def test_get_message_rest_required_fields(request_type=message.GetMessageRequest):
    transport_class = transports.ChatServiceRestTransport

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
    ).get_message._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_message._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = message.Message()
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
            return_value = message.Message.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_message(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_message_rest_unset_required_fields():
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_message._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_message_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "post_get_message"
    ) as post, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_get_message"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = message.GetMessageRequest.pb(message.GetMessageRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = message.Message.to_json(message.Message())

        request = message.GetMessageRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = message.Message()

        client.get_message(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_message_rest_bad_request(
    transport: str = "rest", request_type=message.GetMessageRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "spaces/sample1/messages/sample2"}
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
        client.get_message(request)


def test_get_message_rest_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = message.Message()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "spaces/sample1/messages/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = message.Message.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_message(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=spaces/*/messages/*}" % client.transport._host, args[1]
        )


def test_get_message_rest_flattened_error(transport: str = "rest"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_message(
            message.GetMessageRequest(),
            name="name_value",
        )


def test_get_message_rest_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gc_message.UpdateMessageRequest,
        dict,
    ],
)
def test_update_message_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"message": {"name": "spaces/sample1/messages/sample2"}}
    request_init["message"] = {
        "name": "spaces/sample1/messages/sample2",
        "sender": {
            "name": "name_value",
            "display_name": "display_name_value",
            "domain_id": "domain_id_value",
            "type_": 1,
            "is_anonymous": True,
        },
        "create_time": {"seconds": 751, "nanos": 543},
        "last_update_time": {},
        "delete_time": {},
        "text": "text_value",
        "formatted_text": "formatted_text_value",
        "cards": [
            {
                "header": {
                    "title": "title_value",
                    "subtitle": "subtitle_value",
                    "image_style": 1,
                    "image_url": "image_url_value",
                },
                "sections": [
                    {
                        "header": "header_value",
                        "widgets": [
                            {
                                "text_paragraph": {"text": "text_value"},
                                "image": {
                                    "image_url": "image_url_value",
                                    "on_click": {
                                        "action": {
                                            "action_method_name": "action_method_name_value",
                                            "parameters": [
                                                {
                                                    "key": "key_value",
                                                    "value": "value_value",
                                                }
                                            ],
                                        },
                                        "open_link": {"url": "url_value"},
                                    },
                                    "aspect_ratio": 0.1278,
                                },
                                "key_value": {
                                    "icon": 1,
                                    "icon_url": "icon_url_value",
                                    "top_label": "top_label_value",
                                    "content": "content_value",
                                    "content_multiline": True,
                                    "bottom_label": "bottom_label_value",
                                    "on_click": {},
                                    "button": {
                                        "text_button": {
                                            "text": "text_value",
                                            "on_click": {},
                                        },
                                        "image_button": {
                                            "icon": 1,
                                            "icon_url": "icon_url_value",
                                            "on_click": {},
                                            "name": "name_value",
                                        },
                                    },
                                },
                                "buttons": {},
                            }
                        ],
                    }
                ],
                "card_actions": [
                    {"action_label": "action_label_value", "on_click": {}}
                ],
                "name": "name_value",
            }
        ],
        "cards_v2": [
            {
                "card_id": "card_id_value",
                "card": {
                    "header": {
                        "title": "title_value",
                        "subtitle": "subtitle_value",
                        "image_type": 1,
                        "image_url": "image_url_value",
                        "image_alt_text": "image_alt_text_value",
                    },
                    "sections": [
                        {
                            "header": "header_value",
                            "widgets": [
                                {
                                    "text_paragraph": {"text": "text_value"},
                                    "image": {
                                        "image_url": "image_url_value",
                                        "on_click": {
                                            "action": {
                                                "function": "function_value",
                                                "parameters": [
                                                    {
                                                        "key": "key_value",
                                                        "value": "value_value",
                                                    }
                                                ],
                                                "load_indicator": 1,
                                                "persist_values": True,
                                                "interaction": 1,
                                            },
                                            "open_link": {
                                                "url": "url_value",
                                                "open_as": 1,
                                                "on_close": 1,
                                            },
                                            "open_dynamic_link_action": {},
                                            "card": {},
                                        },
                                        "alt_text": "alt_text_value",
                                    },
                                    "decorated_text": {
                                        "icon": {
                                            "known_icon": "known_icon_value",
                                            "icon_url": "icon_url_value",
                                            "alt_text": "alt_text_value",
                                            "image_type": 1,
                                        },
                                        "start_icon": {},
                                        "top_label": "top_label_value",
                                        "text": "text_value",
                                        "wrap_text": True,
                                        "bottom_label": "bottom_label_value",
                                        "on_click": {},
                                        "button": {
                                            "text": "text_value",
                                            "icon": {},
                                            "color": {
                                                "red": 0.315,
                                                "green": 0.529,
                                                "blue": 0.424,
                                                "alpha": {"value": 0.541},
                                            },
                                            "on_click": {},
                                            "disabled": True,
                                            "alt_text": "alt_text_value",
                                        },
                                        "switch_control": {
                                            "name": "name_value",
                                            "value": "value_value",
                                            "selected": True,
                                            "on_change_action": {},
                                            "control_type": 1,
                                        },
                                        "end_icon": {},
                                    },
                                    "button_list": {"buttons": {}},
                                    "text_input": {
                                        "name": "name_value",
                                        "label": "label_value",
                                        "hint_text": "hint_text_value",
                                        "value": "value_value",
                                        "type_": 1,
                                        "on_change_action": {},
                                        "initial_suggestions": {
                                            "items": [{"text": "text_value"}]
                                        },
                                        "auto_complete_action": {},
                                        "placeholder_text": "placeholder_text_value",
                                    },
                                    "selection_input": {
                                        "name": "name_value",
                                        "label": "label_value",
                                        "type_": 1,
                                        "items": [
                                            {
                                                "text": "text_value",
                                                "value": "value_value",
                                                "selected": True,
                                                "start_icon_uri": "start_icon_uri_value",
                                                "bottom_text": "bottom_text_value",
                                            }
                                        ],
                                        "on_change_action": {},
                                        "multi_select_max_selected_items": 3288,
                                        "multi_select_min_query_length": 3107,
                                        "external_data_source": {},
                                        "platform_data_source": {
                                            "common_data_source": 1
                                        },
                                    },
                                    "date_time_picker": {
                                        "name": "name_value",
                                        "label": "label_value",
                                        "type_": 1,
                                        "value_ms_epoch": 1482,
                                        "timezone_offset_date": 2126,
                                        "on_change_action": {},
                                    },
                                    "divider": {},
                                    "grid": {
                                        "title": "title_value",
                                        "items": [
                                            {
                                                "id": "id_value",
                                                "image": {
                                                    "image_uri": "image_uri_value",
                                                    "alt_text": "alt_text_value",
                                                    "crop_style": {
                                                        "type_": 1,
                                                        "aspect_ratio": 0.1278,
                                                    },
                                                    "border_style": {
                                                        "type_": 1,
                                                        "stroke_color": {},
                                                        "corner_radius": 1392,
                                                    },
                                                },
                                                "title": "title_value",
                                                "subtitle": "subtitle_value",
                                                "layout": 1,
                                            }
                                        ],
                                        "border_style": {},
                                        "column_count": 1302,
                                        "on_click": {},
                                    },
                                    "columns": {
                                        "column_items": [
                                            {
                                                "horizontal_size_style": 1,
                                                "horizontal_alignment": 1,
                                                "vertical_alignment": 1,
                                                "widgets": [
                                                    {
                                                        "text_paragraph": {},
                                                        "image": {},
                                                        "decorated_text": {},
                                                        "button_list": {},
                                                        "text_input": {},
                                                        "selection_input": {},
                                                        "date_time_picker": {},
                                                    }
                                                ],
                                            }
                                        ]
                                    },
                                    "horizontal_alignment": 1,
                                }
                            ],
                            "collapsible": True,
                            "uncollapsible_widgets_count": 2891,
                        }
                    ],
                    "section_divider_style": 1,
                    "card_actions": [
                        {"action_label": "action_label_value", "on_click": {}}
                    ],
                    "name": "name_value",
                    "fixed_footer": {"primary_button": {}, "secondary_button": {}},
                    "display_style": 1,
                    "peek_card_header": {},
                },
            }
        ],
        "annotations": [
            {
                "type_": 1,
                "start_index": 1189,
                "length": 642,
                "user_mention": {"user": {}, "type_": 1},
                "slash_command": {
                    "bot": {},
                    "type_": 1,
                    "command_name": "command_name_value",
                    "command_id": 1035,
                    "triggers_dialog": True,
                },
                "rich_link_metadata": {
                    "uri": "uri_value",
                    "rich_link_type": 1,
                    "drive_link_data": {
                        "drive_data_ref": {"drive_file_id": "drive_file_id_value"},
                        "mime_type": "mime_type_value",
                    },
                },
            }
        ],
        "thread": {"name": "name_value", "thread_key": "thread_key_value"},
        "space": {
            "name": "name_value",
            "type_": 1,
            "space_type": 1,
            "single_user_bot_dm": True,
            "threaded": True,
            "display_name": "display_name_value",
            "external_user_allowed": True,
            "space_threading_state": 2,
            "space_details": {
                "description": "description_value",
                "guidelines": "guidelines_value",
            },
            "space_history_state": 1,
            "import_mode": True,
            "create_time": {},
            "admin_installed": True,
        },
        "fallback_text": "fallback_text_value",
        "action_response": {
            "type_": 1,
            "url": "url_value",
            "dialog_action": {
                "dialog": {"body": {}},
                "action_status": {
                    "status_code": 1,
                    "user_facing_message": "user_facing_message_value",
                },
            },
            "updated_widget": {"suggestions": {"items": {}}, "widget": "widget_value"},
        },
        "argument_text": "argument_text_value",
        "slash_command": {"command_id": 1035},
        "attachment": [
            {
                "name": "name_value",
                "content_name": "content_name_value",
                "content_type": "content_type_value",
                "attachment_data_ref": {
                    "resource_name": "resource_name_value",
                    "attachment_upload_token": "attachment_upload_token_value",
                },
                "drive_data_ref": {},
                "thumbnail_uri": "thumbnail_uri_value",
                "download_uri": "download_uri_value",
                "source": 1,
            }
        ],
        "matched_url": {"url": "url_value"},
        "thread_reply": True,
        "client_assigned_message_id": "client_assigned_message_id_value",
        "emoji_reaction_summaries": [
            {
                "emoji": {
                    "unicode": "unicode_value",
                    "custom_emoji": {"uid": "uid_value"},
                },
                "reaction_count": 1501,
            }
        ],
        "private_message_viewer": {},
        "deletion_metadata": {"deletion_type": 1},
        "quoted_message_metadata": {"name": "name_value", "last_update_time": {}},
        "attached_gifs": [{"uri": "uri_value"}],
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = gc_message.UpdateMessageRequest.meta.fields["message"]

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
    for field, value in request_init["message"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["message"][field])):
                    del request_init["message"][field][i][subfield]
            else:
                del request_init["message"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gc_message.Message(
            name="name_value",
            text="text_value",
            formatted_text="formatted_text_value",
            fallback_text="fallback_text_value",
            argument_text="argument_text_value",
            thread_reply=True,
            client_assigned_message_id="client_assigned_message_id_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gc_message.Message.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_message(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gc_message.Message)
    assert response.name == "name_value"
    assert response.text == "text_value"
    assert response.formatted_text == "formatted_text_value"
    assert response.fallback_text == "fallback_text_value"
    assert response.argument_text == "argument_text_value"
    assert response.thread_reply is True
    assert response.client_assigned_message_id == "client_assigned_message_id_value"


def test_update_message_rest_required_fields(
    request_type=gc_message.UpdateMessageRequest,
):
    transport_class = transports.ChatServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_message._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_message._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "allow_missing",
            "update_mask",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gc_message.Message()
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
            return_value = gc_message.Message.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_message(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_message_rest_unset_required_fields():
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_message._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "allowMissing",
                "updateMask",
            )
        )
        & set(("message",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_message_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "post_update_message"
    ) as post, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_update_message"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gc_message.UpdateMessageRequest.pb(
            gc_message.UpdateMessageRequest()
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
        req.return_value._content = gc_message.Message.to_json(gc_message.Message())

        request = gc_message.UpdateMessageRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gc_message.Message()

        client.update_message(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_message_rest_bad_request(
    transport: str = "rest", request_type=gc_message.UpdateMessageRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"message": {"name": "spaces/sample1/messages/sample2"}}
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
        client.update_message(request)


def test_update_message_rest_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gc_message.Message()

        # get arguments that satisfy an http rule for this method
        sample_request = {"message": {"name": "spaces/sample1/messages/sample2"}}

        # get truthy value for each flattened field
        mock_args = dict(
            message=gc_message.Message(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gc_message.Message.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_message(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{message.name=spaces/*/messages/*}" % client.transport._host, args[1]
        )


def test_update_message_rest_flattened_error(transport: str = "rest"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_message(
            gc_message.UpdateMessageRequest(),
            message=gc_message.Message(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_message_rest_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        message.DeleteMessageRequest,
        dict,
    ],
)
def test_delete_message_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "spaces/sample1/messages/sample2"}
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
        response = client.delete_message(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_message_rest_required_fields(request_type=message.DeleteMessageRequest):
    transport_class = transports.ChatServiceRestTransport

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
    ).delete_message._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_message._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("force",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ChatServiceClient(
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

            response = client.delete_message(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_message_rest_unset_required_fields():
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_message._get_unset_required_fields({})
    assert set(unset_fields) == (set(("force",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_message_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_delete_message"
    ) as pre:
        pre.assert_not_called()
        pb_message = message.DeleteMessageRequest.pb(message.DeleteMessageRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()

        request = message.DeleteMessageRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_message(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_message_rest_bad_request(
    transport: str = "rest", request_type=message.DeleteMessageRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "spaces/sample1/messages/sample2"}
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
        client.delete_message(request)


def test_delete_message_rest_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "spaces/sample1/messages/sample2"}

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

        client.delete_message(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=spaces/*/messages/*}" % client.transport._host, args[1]
        )


def test_delete_message_rest_flattened_error(transport: str = "rest"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_message(
            message.DeleteMessageRequest(),
            name="name_value",
        )


def test_delete_message_rest_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        attachment.GetAttachmentRequest,
        dict,
    ],
)
def test_get_attachment_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "spaces/sample1/messages/sample2/attachments/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = attachment.Attachment(
            name="name_value",
            content_name="content_name_value",
            content_type="content_type_value",
            thumbnail_uri="thumbnail_uri_value",
            download_uri="download_uri_value",
            source=attachment.Attachment.Source.DRIVE_FILE,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = attachment.Attachment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_attachment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, attachment.Attachment)
    assert response.name == "name_value"
    assert response.content_name == "content_name_value"
    assert response.content_type == "content_type_value"
    assert response.thumbnail_uri == "thumbnail_uri_value"
    assert response.download_uri == "download_uri_value"
    assert response.source == attachment.Attachment.Source.DRIVE_FILE


def test_get_attachment_rest_required_fields(
    request_type=attachment.GetAttachmentRequest,
):
    transport_class = transports.ChatServiceRestTransport

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
    ).get_attachment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_attachment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = attachment.Attachment()
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
            return_value = attachment.Attachment.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_attachment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_attachment_rest_unset_required_fields():
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_attachment._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_attachment_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "post_get_attachment"
    ) as post, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_get_attachment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = attachment.GetAttachmentRequest.pb(
            attachment.GetAttachmentRequest()
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
        req.return_value._content = attachment.Attachment.to_json(
            attachment.Attachment()
        )

        request = attachment.GetAttachmentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = attachment.Attachment()

        client.get_attachment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_attachment_rest_bad_request(
    transport: str = "rest", request_type=attachment.GetAttachmentRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "spaces/sample1/messages/sample2/attachments/sample3"}
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
        client.get_attachment(request)


def test_get_attachment_rest_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = attachment.Attachment()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "spaces/sample1/messages/sample2/attachments/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = attachment.Attachment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_attachment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=spaces/*/messages/*/attachments/*}" % client.transport._host,
            args[1],
        )


def test_get_attachment_rest_flattened_error(transport: str = "rest"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_attachment(
            attachment.GetAttachmentRequest(),
            name="name_value",
        )


def test_get_attachment_rest_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        attachment.UploadAttachmentRequest,
        dict,
    ],
)
def test_upload_attachment_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "spaces/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = attachment.UploadAttachmentResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = attachment.UploadAttachmentResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.upload_attachment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, attachment.UploadAttachmentResponse)


def test_upload_attachment_rest_required_fields(
    request_type=attachment.UploadAttachmentRequest,
):
    transport_class = transports.ChatServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["filename"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).upload_attachment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"
    jsonified_request["filename"] = "filename_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).upload_attachment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "filename" in jsonified_request
    assert jsonified_request["filename"] == "filename_value"

    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = attachment.UploadAttachmentResponse()
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
            return_value = attachment.UploadAttachmentResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.upload_attachment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_upload_attachment_rest_unset_required_fields():
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.upload_attachment._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "filename",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_upload_attachment_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "post_upload_attachment"
    ) as post, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_upload_attachment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = attachment.UploadAttachmentRequest.pb(
            attachment.UploadAttachmentRequest()
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
        req.return_value._content = attachment.UploadAttachmentResponse.to_json(
            attachment.UploadAttachmentResponse()
        )

        request = attachment.UploadAttachmentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = attachment.UploadAttachmentResponse()

        client.upload_attachment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_upload_attachment_rest_bad_request(
    transport: str = "rest", request_type=attachment.UploadAttachmentRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "spaces/sample1"}
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
        client.upload_attachment(request)


def test_upload_attachment_rest_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        space.ListSpacesRequest,
        dict,
    ],
)
def test_list_spaces_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = space.ListSpacesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = space.ListSpacesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_spaces(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSpacesPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_spaces_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "post_list_spaces"
    ) as post, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_list_spaces"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = space.ListSpacesRequest.pb(space.ListSpacesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = space.ListSpacesResponse.to_json(
            space.ListSpacesResponse()
        )

        request = space.ListSpacesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = space.ListSpacesResponse()

        client.list_spaces(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_spaces_rest_bad_request(
    transport: str = "rest", request_type=space.ListSpacesRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {}
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
        client.list_spaces(request)


def test_list_spaces_rest_pager(transport: str = "rest"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            space.ListSpacesResponse(
                spaces=[
                    space.Space(),
                    space.Space(),
                    space.Space(),
                ],
                next_page_token="abc",
            ),
            space.ListSpacesResponse(
                spaces=[],
                next_page_token="def",
            ),
            space.ListSpacesResponse(
                spaces=[
                    space.Space(),
                ],
                next_page_token="ghi",
            ),
            space.ListSpacesResponse(
                spaces=[
                    space.Space(),
                    space.Space(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(space.ListSpacesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {}

        pager = client.list_spaces(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, space.Space) for i in results)

        pages = list(client.list_spaces(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        space.GetSpaceRequest,
        dict,
    ],
)
def test_get_space_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "spaces/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = space.Space(
            name="name_value",
            type_=space.Space.Type.ROOM,
            space_type=space.Space.SpaceType.SPACE,
            single_user_bot_dm=True,
            threaded=True,
            display_name="display_name_value",
            external_user_allowed=True,
            space_threading_state=space.Space.SpaceThreadingState.THREADED_MESSAGES,
            space_history_state=history_state.HistoryState.HISTORY_OFF,
            import_mode=True,
            admin_installed=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = space.Space.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_space(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, space.Space)
    assert response.name == "name_value"
    assert response.type_ == space.Space.Type.ROOM
    assert response.space_type == space.Space.SpaceType.SPACE
    assert response.single_user_bot_dm is True
    assert response.threaded is True
    assert response.display_name == "display_name_value"
    assert response.external_user_allowed is True
    assert (
        response.space_threading_state
        == space.Space.SpaceThreadingState.THREADED_MESSAGES
    )
    assert response.space_history_state == history_state.HistoryState.HISTORY_OFF
    assert response.import_mode is True
    assert response.admin_installed is True


def test_get_space_rest_required_fields(request_type=space.GetSpaceRequest):
    transport_class = transports.ChatServiceRestTransport

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
    ).get_space._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_space._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = space.Space()
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
            return_value = space.Space.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_space(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_space_rest_unset_required_fields():
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_space._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_space_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "post_get_space"
    ) as post, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_get_space"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = space.GetSpaceRequest.pb(space.GetSpaceRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = space.Space.to_json(space.Space())

        request = space.GetSpaceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = space.Space()

        client.get_space(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_space_rest_bad_request(
    transport: str = "rest", request_type=space.GetSpaceRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "spaces/sample1"}
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
        client.get_space(request)


def test_get_space_rest_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = space.Space()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "spaces/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = space.Space.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_space(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=spaces/*}" % client.transport._host, args[1]
        )


def test_get_space_rest_flattened_error(transport: str = "rest"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_space(
            space.GetSpaceRequest(),
            name="name_value",
        )


def test_get_space_rest_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gc_space.CreateSpaceRequest,
        dict,
    ],
)
def test_create_space_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {}
    request_init["space"] = {
        "name": "name_value",
        "type_": 1,
        "space_type": 1,
        "single_user_bot_dm": True,
        "threaded": True,
        "display_name": "display_name_value",
        "external_user_allowed": True,
        "space_threading_state": 2,
        "space_details": {
            "description": "description_value",
            "guidelines": "guidelines_value",
        },
        "space_history_state": 1,
        "import_mode": True,
        "create_time": {"seconds": 751, "nanos": 543},
        "admin_installed": True,
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = gc_space.CreateSpaceRequest.meta.fields["space"]

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
    for field, value in request_init["space"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["space"][field])):
                    del request_init["space"][field][i][subfield]
            else:
                del request_init["space"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gc_space.Space(
            name="name_value",
            type_=gc_space.Space.Type.ROOM,
            space_type=gc_space.Space.SpaceType.SPACE,
            single_user_bot_dm=True,
            threaded=True,
            display_name="display_name_value",
            external_user_allowed=True,
            space_threading_state=gc_space.Space.SpaceThreadingState.THREADED_MESSAGES,
            space_history_state=history_state.HistoryState.HISTORY_OFF,
            import_mode=True,
            admin_installed=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gc_space.Space.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_space(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gc_space.Space)
    assert response.name == "name_value"
    assert response.type_ == gc_space.Space.Type.ROOM
    assert response.space_type == gc_space.Space.SpaceType.SPACE
    assert response.single_user_bot_dm is True
    assert response.threaded is True
    assert response.display_name == "display_name_value"
    assert response.external_user_allowed is True
    assert (
        response.space_threading_state
        == gc_space.Space.SpaceThreadingState.THREADED_MESSAGES
    )
    assert response.space_history_state == history_state.HistoryState.HISTORY_OFF
    assert response.import_mode is True
    assert response.admin_installed is True


def test_create_space_rest_required_fields(request_type=gc_space.CreateSpaceRequest):
    transport_class = transports.ChatServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_space._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_space._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gc_space.Space()
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
            return_value = gc_space.Space.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_space(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_space_rest_unset_required_fields():
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_space._get_unset_required_fields({})
    assert set(unset_fields) == (set(("requestId",)) & set(("space",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_space_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "post_create_space"
    ) as post, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_create_space"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gc_space.CreateSpaceRequest.pb(gc_space.CreateSpaceRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gc_space.Space.to_json(gc_space.Space())

        request = gc_space.CreateSpaceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gc_space.Space()

        client.create_space(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_space_rest_bad_request(
    transport: str = "rest", request_type=gc_space.CreateSpaceRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {}
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
        client.create_space(request)


def test_create_space_rest_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gc_space.Space()

        # get arguments that satisfy an http rule for this method
        sample_request = {}

        # get truthy value for each flattened field
        mock_args = dict(
            space=gc_space.Space(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gc_space.Space.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_space(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/spaces" % client.transport._host, args[1])


def test_create_space_rest_flattened_error(transport: str = "rest"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_space(
            gc_space.CreateSpaceRequest(),
            space=gc_space.Space(name="name_value"),
        )


def test_create_space_rest_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        space_setup.SetUpSpaceRequest,
        dict,
    ],
)
def test_set_up_space_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = space.Space(
            name="name_value",
            type_=space.Space.Type.ROOM,
            space_type=space.Space.SpaceType.SPACE,
            single_user_bot_dm=True,
            threaded=True,
            display_name="display_name_value",
            external_user_allowed=True,
            space_threading_state=space.Space.SpaceThreadingState.THREADED_MESSAGES,
            space_history_state=history_state.HistoryState.HISTORY_OFF,
            import_mode=True,
            admin_installed=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = space.Space.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_up_space(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, space.Space)
    assert response.name == "name_value"
    assert response.type_ == space.Space.Type.ROOM
    assert response.space_type == space.Space.SpaceType.SPACE
    assert response.single_user_bot_dm is True
    assert response.threaded is True
    assert response.display_name == "display_name_value"
    assert response.external_user_allowed is True
    assert (
        response.space_threading_state
        == space.Space.SpaceThreadingState.THREADED_MESSAGES
    )
    assert response.space_history_state == history_state.HistoryState.HISTORY_OFF
    assert response.import_mode is True
    assert response.admin_installed is True


def test_set_up_space_rest_required_fields(request_type=space_setup.SetUpSpaceRequest):
    transport_class = transports.ChatServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).set_up_space._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).set_up_space._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = space.Space()
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
            return_value = space.Space.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.set_up_space(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_set_up_space_rest_unset_required_fields():
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.set_up_space._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("space",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_set_up_space_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "post_set_up_space"
    ) as post, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_set_up_space"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = space_setup.SetUpSpaceRequest.pb(space_setup.SetUpSpaceRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = space.Space.to_json(space.Space())

        request = space_setup.SetUpSpaceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = space.Space()

        client.set_up_space(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_set_up_space_rest_bad_request(
    transport: str = "rest", request_type=space_setup.SetUpSpaceRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {}
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
        client.set_up_space(request)


def test_set_up_space_rest_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gc_space.UpdateSpaceRequest,
        dict,
    ],
)
def test_update_space_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"space": {"name": "spaces/sample1"}}
    request_init["space"] = {
        "name": "spaces/sample1",
        "type_": 1,
        "space_type": 1,
        "single_user_bot_dm": True,
        "threaded": True,
        "display_name": "display_name_value",
        "external_user_allowed": True,
        "space_threading_state": 2,
        "space_details": {
            "description": "description_value",
            "guidelines": "guidelines_value",
        },
        "space_history_state": 1,
        "import_mode": True,
        "create_time": {"seconds": 751, "nanos": 543},
        "admin_installed": True,
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = gc_space.UpdateSpaceRequest.meta.fields["space"]

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
    for field, value in request_init["space"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["space"][field])):
                    del request_init["space"][field][i][subfield]
            else:
                del request_init["space"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gc_space.Space(
            name="name_value",
            type_=gc_space.Space.Type.ROOM,
            space_type=gc_space.Space.SpaceType.SPACE,
            single_user_bot_dm=True,
            threaded=True,
            display_name="display_name_value",
            external_user_allowed=True,
            space_threading_state=gc_space.Space.SpaceThreadingState.THREADED_MESSAGES,
            space_history_state=history_state.HistoryState.HISTORY_OFF,
            import_mode=True,
            admin_installed=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gc_space.Space.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_space(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gc_space.Space)
    assert response.name == "name_value"
    assert response.type_ == gc_space.Space.Type.ROOM
    assert response.space_type == gc_space.Space.SpaceType.SPACE
    assert response.single_user_bot_dm is True
    assert response.threaded is True
    assert response.display_name == "display_name_value"
    assert response.external_user_allowed is True
    assert (
        response.space_threading_state
        == gc_space.Space.SpaceThreadingState.THREADED_MESSAGES
    )
    assert response.space_history_state == history_state.HistoryState.HISTORY_OFF
    assert response.import_mode is True
    assert response.admin_installed is True


def test_update_space_rest_required_fields(request_type=gc_space.UpdateSpaceRequest):
    transport_class = transports.ChatServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_space._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_space._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gc_space.Space()
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
            return_value = gc_space.Space.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_space(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_space_rest_unset_required_fields():
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_space._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("space",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_space_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "post_update_space"
    ) as post, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_update_space"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gc_space.UpdateSpaceRequest.pb(gc_space.UpdateSpaceRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gc_space.Space.to_json(gc_space.Space())

        request = gc_space.UpdateSpaceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gc_space.Space()

        client.update_space(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_space_rest_bad_request(
    transport: str = "rest", request_type=gc_space.UpdateSpaceRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"space": {"name": "spaces/sample1"}}
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
        client.update_space(request)


def test_update_space_rest_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gc_space.Space()

        # get arguments that satisfy an http rule for this method
        sample_request = {"space": {"name": "spaces/sample1"}}

        # get truthy value for each flattened field
        mock_args = dict(
            space=gc_space.Space(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gc_space.Space.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_space(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{space.name=spaces/*}" % client.transport._host, args[1]
        )


def test_update_space_rest_flattened_error(transport: str = "rest"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_space(
            gc_space.UpdateSpaceRequest(),
            space=gc_space.Space(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_space_rest_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        space.DeleteSpaceRequest,
        dict,
    ],
)
def test_delete_space_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "spaces/sample1"}
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
        response = client.delete_space(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_space_rest_required_fields(request_type=space.DeleteSpaceRequest):
    transport_class = transports.ChatServiceRestTransport

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
    ).delete_space._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_space._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ChatServiceClient(
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

            response = client.delete_space(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_space_rest_unset_required_fields():
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_space._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_space_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_delete_space"
    ) as pre:
        pre.assert_not_called()
        pb_message = space.DeleteSpaceRequest.pb(space.DeleteSpaceRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()

        request = space.DeleteSpaceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_space(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_space_rest_bad_request(
    transport: str = "rest", request_type=space.DeleteSpaceRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "spaces/sample1"}
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
        client.delete_space(request)


def test_delete_space_rest_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "spaces/sample1"}

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

        client.delete_space(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=spaces/*}" % client.transport._host, args[1]
        )


def test_delete_space_rest_flattened_error(transport: str = "rest"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_space(
            space.DeleteSpaceRequest(),
            name="name_value",
        )


def test_delete_space_rest_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        space.CompleteImportSpaceRequest,
        dict,
    ],
)
def test_complete_import_space_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "spaces/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = space.CompleteImportSpaceResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = space.CompleteImportSpaceResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.complete_import_space(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, space.CompleteImportSpaceResponse)


def test_complete_import_space_rest_required_fields(
    request_type=space.CompleteImportSpaceRequest,
):
    transport_class = transports.ChatServiceRestTransport

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
    ).complete_import_space._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).complete_import_space._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = space.CompleteImportSpaceResponse()
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
            return_value = space.CompleteImportSpaceResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.complete_import_space(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_complete_import_space_rest_unset_required_fields():
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.complete_import_space._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_complete_import_space_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "post_complete_import_space"
    ) as post, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_complete_import_space"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = space.CompleteImportSpaceRequest.pb(
            space.CompleteImportSpaceRequest()
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
        req.return_value._content = space.CompleteImportSpaceResponse.to_json(
            space.CompleteImportSpaceResponse()
        )

        request = space.CompleteImportSpaceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = space.CompleteImportSpaceResponse()

        client.complete_import_space(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_complete_import_space_rest_bad_request(
    transport: str = "rest", request_type=space.CompleteImportSpaceRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "spaces/sample1"}
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
        client.complete_import_space(request)


def test_complete_import_space_rest_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        space.FindDirectMessageRequest,
        dict,
    ],
)
def test_find_direct_message_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = space.Space(
            name="name_value",
            type_=space.Space.Type.ROOM,
            space_type=space.Space.SpaceType.SPACE,
            single_user_bot_dm=True,
            threaded=True,
            display_name="display_name_value",
            external_user_allowed=True,
            space_threading_state=space.Space.SpaceThreadingState.THREADED_MESSAGES,
            space_history_state=history_state.HistoryState.HISTORY_OFF,
            import_mode=True,
            admin_installed=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = space.Space.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.find_direct_message(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, space.Space)
    assert response.name == "name_value"
    assert response.type_ == space.Space.Type.ROOM
    assert response.space_type == space.Space.SpaceType.SPACE
    assert response.single_user_bot_dm is True
    assert response.threaded is True
    assert response.display_name == "display_name_value"
    assert response.external_user_allowed is True
    assert (
        response.space_threading_state
        == space.Space.SpaceThreadingState.THREADED_MESSAGES
    )
    assert response.space_history_state == history_state.HistoryState.HISTORY_OFF
    assert response.import_mode is True
    assert response.admin_installed is True


def test_find_direct_message_rest_required_fields(
    request_type=space.FindDirectMessageRequest,
):
    transport_class = transports.ChatServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped
    assert "name" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).find_direct_message._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "name" in jsonified_request
    assert jsonified_request["name"] == request_init["name"]

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).find_direct_message._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("name",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = space.Space()
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
            return_value = space.Space.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.find_direct_message(request)

            expected_params = [
                (
                    "name",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_find_direct_message_rest_unset_required_fields():
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.find_direct_message._get_unset_required_fields({})
    assert set(unset_fields) == (set(("name",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_find_direct_message_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "post_find_direct_message"
    ) as post, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_find_direct_message"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = space.FindDirectMessageRequest.pb(space.FindDirectMessageRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = space.Space.to_json(space.Space())

        request = space.FindDirectMessageRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = space.Space()

        client.find_direct_message(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_find_direct_message_rest_bad_request(
    transport: str = "rest", request_type=space.FindDirectMessageRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {}
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
        client.find_direct_message(request)


def test_find_direct_message_rest_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gc_membership.CreateMembershipRequest,
        dict,
    ],
)
def test_create_membership_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "spaces/sample1"}
    request_init["membership"] = {
        "name": "name_value",
        "state": 1,
        "role": 1,
        "member": {
            "name": "name_value",
            "display_name": "display_name_value",
            "domain_id": "domain_id_value",
            "type_": 1,
            "is_anonymous": True,
        },
        "group_member": {"name": "name_value"},
        "create_time": {"seconds": 751, "nanos": 543},
        "delete_time": {},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = gc_membership.CreateMembershipRequest.meta.fields["membership"]

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
    for field, value in request_init["membership"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["membership"][field])):
                    del request_init["membership"][field][i][subfield]
            else:
                del request_init["membership"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gc_membership.Membership(
            name="name_value",
            state=gc_membership.Membership.MembershipState.JOINED,
            role=gc_membership.Membership.MembershipRole.ROLE_MEMBER,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gc_membership.Membership.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_membership(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gc_membership.Membership)
    assert response.name == "name_value"
    assert response.state == gc_membership.Membership.MembershipState.JOINED
    assert response.role == gc_membership.Membership.MembershipRole.ROLE_MEMBER


def test_create_membership_rest_required_fields(
    request_type=gc_membership.CreateMembershipRequest,
):
    transport_class = transports.ChatServiceRestTransport

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
    ).create_membership._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_membership._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gc_membership.Membership()
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
            return_value = gc_membership.Membership.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_membership(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_membership_rest_unset_required_fields():
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_membership._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "membership",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_membership_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "post_create_membership"
    ) as post, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_create_membership"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gc_membership.CreateMembershipRequest.pb(
            gc_membership.CreateMembershipRequest()
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
        req.return_value._content = gc_membership.Membership.to_json(
            gc_membership.Membership()
        )

        request = gc_membership.CreateMembershipRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gc_membership.Membership()

        client.create_membership(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_membership_rest_bad_request(
    transport: str = "rest", request_type=gc_membership.CreateMembershipRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "spaces/sample1"}
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
        client.create_membership(request)


def test_create_membership_rest_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gc_membership.Membership()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "spaces/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            membership=gc_membership.Membership(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gc_membership.Membership.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_membership(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=spaces/*}/members" % client.transport._host, args[1]
        )


def test_create_membership_rest_flattened_error(transport: str = "rest"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_membership(
            gc_membership.CreateMembershipRequest(),
            parent="parent_value",
            membership=gc_membership.Membership(name="name_value"),
        )


def test_create_membership_rest_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        membership.DeleteMembershipRequest,
        dict,
    ],
)
def test_delete_membership_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "spaces/sample1/members/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = membership.Membership(
            name="name_value",
            state=membership.Membership.MembershipState.JOINED,
            role=membership.Membership.MembershipRole.ROLE_MEMBER,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = membership.Membership.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_membership(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, membership.Membership)
    assert response.name == "name_value"
    assert response.state == membership.Membership.MembershipState.JOINED
    assert response.role == membership.Membership.MembershipRole.ROLE_MEMBER


def test_delete_membership_rest_required_fields(
    request_type=membership.DeleteMembershipRequest,
):
    transport_class = transports.ChatServiceRestTransport

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
    ).delete_membership._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_membership._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = membership.Membership()
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
            return_value = membership.Membership.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_membership(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_membership_rest_unset_required_fields():
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_membership._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_membership_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "post_delete_membership"
    ) as post, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_delete_membership"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = membership.DeleteMembershipRequest.pb(
            membership.DeleteMembershipRequest()
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
        req.return_value._content = membership.Membership.to_json(
            membership.Membership()
        )

        request = membership.DeleteMembershipRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = membership.Membership()

        client.delete_membership(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_membership_rest_bad_request(
    transport: str = "rest", request_type=membership.DeleteMembershipRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "spaces/sample1/members/sample2"}
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
        client.delete_membership(request)


def test_delete_membership_rest_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = membership.Membership()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "spaces/sample1/members/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = membership.Membership.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_membership(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=spaces/*/members/*}" % client.transport._host, args[1]
        )


def test_delete_membership_rest_flattened_error(transport: str = "rest"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_membership(
            membership.DeleteMembershipRequest(),
            name="name_value",
        )


def test_delete_membership_rest_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gc_reaction.CreateReactionRequest,
        dict,
    ],
)
def test_create_reaction_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "spaces/sample1/messages/sample2"}
    request_init["reaction"] = {
        "name": "name_value",
        "user": {
            "name": "name_value",
            "display_name": "display_name_value",
            "domain_id": "domain_id_value",
            "type_": 1,
            "is_anonymous": True,
        },
        "emoji": {"unicode": "unicode_value", "custom_emoji": {"uid": "uid_value"}},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = gc_reaction.CreateReactionRequest.meta.fields["reaction"]

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
    for field, value in request_init["reaction"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["reaction"][field])):
                    del request_init["reaction"][field][i][subfield]
            else:
                del request_init["reaction"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gc_reaction.Reaction(
            name="name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gc_reaction.Reaction.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_reaction(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gc_reaction.Reaction)
    assert response.name == "name_value"


def test_create_reaction_rest_required_fields(
    request_type=gc_reaction.CreateReactionRequest,
):
    transport_class = transports.ChatServiceRestTransport

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
    ).create_reaction._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_reaction._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gc_reaction.Reaction()
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
            return_value = gc_reaction.Reaction.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_reaction(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_reaction_rest_unset_required_fields():
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_reaction._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "reaction",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_reaction_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "post_create_reaction"
    ) as post, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_create_reaction"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gc_reaction.CreateReactionRequest.pb(
            gc_reaction.CreateReactionRequest()
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
        req.return_value._content = gc_reaction.Reaction.to_json(gc_reaction.Reaction())

        request = gc_reaction.CreateReactionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gc_reaction.Reaction()

        client.create_reaction(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_reaction_rest_bad_request(
    transport: str = "rest", request_type=gc_reaction.CreateReactionRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "spaces/sample1/messages/sample2"}
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
        client.create_reaction(request)


def test_create_reaction_rest_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gc_reaction.Reaction()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "spaces/sample1/messages/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            reaction=gc_reaction.Reaction(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gc_reaction.Reaction.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_reaction(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=spaces/*/messages/*}/reactions" % client.transport._host,
            args[1],
        )


def test_create_reaction_rest_flattened_error(transport: str = "rest"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_reaction(
            gc_reaction.CreateReactionRequest(),
            parent="parent_value",
            reaction=gc_reaction.Reaction(name="name_value"),
        )


def test_create_reaction_rest_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        reaction.ListReactionsRequest,
        dict,
    ],
)
def test_list_reactions_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "spaces/sample1/messages/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = reaction.ListReactionsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = reaction.ListReactionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_reactions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListReactionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_reactions_rest_required_fields(
    request_type=reaction.ListReactionsRequest,
):
    transport_class = transports.ChatServiceRestTransport

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
    ).list_reactions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_reactions._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = reaction.ListReactionsResponse()
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
            return_value = reaction.ListReactionsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_reactions(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_reactions_rest_unset_required_fields():
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_reactions._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_reactions_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "post_list_reactions"
    ) as post, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_list_reactions"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = reaction.ListReactionsRequest.pb(reaction.ListReactionsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = reaction.ListReactionsResponse.to_json(
            reaction.ListReactionsResponse()
        )

        request = reaction.ListReactionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = reaction.ListReactionsResponse()

        client.list_reactions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_reactions_rest_bad_request(
    transport: str = "rest", request_type=reaction.ListReactionsRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "spaces/sample1/messages/sample2"}
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
        client.list_reactions(request)


def test_list_reactions_rest_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = reaction.ListReactionsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "spaces/sample1/messages/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = reaction.ListReactionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_reactions(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=spaces/*/messages/*}/reactions" % client.transport._host,
            args[1],
        )


def test_list_reactions_rest_flattened_error(transport: str = "rest"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_reactions(
            reaction.ListReactionsRequest(),
            parent="parent_value",
        )


def test_list_reactions_rest_pager(transport: str = "rest"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            reaction.ListReactionsResponse(
                reactions=[
                    reaction.Reaction(),
                    reaction.Reaction(),
                    reaction.Reaction(),
                ],
                next_page_token="abc",
            ),
            reaction.ListReactionsResponse(
                reactions=[],
                next_page_token="def",
            ),
            reaction.ListReactionsResponse(
                reactions=[
                    reaction.Reaction(),
                ],
                next_page_token="ghi",
            ),
            reaction.ListReactionsResponse(
                reactions=[
                    reaction.Reaction(),
                    reaction.Reaction(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(reaction.ListReactionsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "spaces/sample1/messages/sample2"}

        pager = client.list_reactions(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, reaction.Reaction) for i in results)

        pages = list(client.list_reactions(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        reaction.DeleteReactionRequest,
        dict,
    ],
)
def test_delete_reaction_rest(request_type):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "spaces/sample1/messages/sample2/reactions/sample3"}
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
        response = client.delete_reaction(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_reaction_rest_required_fields(
    request_type=reaction.DeleteReactionRequest,
):
    transport_class = transports.ChatServiceRestTransport

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
    ).delete_reaction._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_reaction._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ChatServiceClient(
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

            response = client.delete_reaction(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_reaction_rest_unset_required_fields():
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_reaction._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_reaction_rest_interceptors(null_interceptor):
    transport = transports.ChatServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ChatServiceRestInterceptor(),
    )
    client = ChatServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ChatServiceRestInterceptor, "pre_delete_reaction"
    ) as pre:
        pre.assert_not_called()
        pb_message = reaction.DeleteReactionRequest.pb(reaction.DeleteReactionRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()

        request = reaction.DeleteReactionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_reaction(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_reaction_rest_bad_request(
    transport: str = "rest", request_type=reaction.DeleteReactionRequest
):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "spaces/sample1/messages/sample2/reactions/sample3"}
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
        client.delete_reaction(request)


def test_delete_reaction_rest_flattened():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "spaces/sample1/messages/sample2/reactions/sample3"}

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

        client.delete_reaction(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=spaces/*/messages/*/reactions/*}" % client.transport._host,
            args[1],
        )


def test_delete_reaction_rest_flattened_error(transport: str = "rest"):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_reaction(
            reaction.DeleteReactionRequest(),
            name="name_value",
        )


def test_delete_reaction_rest_error():
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ChatServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ChatServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.ChatServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ChatServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.ChatServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = ChatServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = ChatServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.ChatServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ChatServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ChatServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = ChatServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ChatServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.ChatServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ChatServiceGrpcTransport,
        transports.ChatServiceGrpcAsyncIOTransport,
        transports.ChatServiceRestTransport,
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
    transport = ChatServiceClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.ChatServiceGrpcTransport,
    )


def test_chat_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.ChatServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_chat_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.apps.chat_v1.services.chat_service.transports.ChatServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.ChatServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_message",
        "list_messages",
        "list_memberships",
        "get_membership",
        "get_message",
        "update_message",
        "delete_message",
        "get_attachment",
        "upload_attachment",
        "list_spaces",
        "get_space",
        "create_space",
        "set_up_space",
        "update_space",
        "delete_space",
        "complete_import_space",
        "find_direct_message",
        "create_membership",
        "delete_membership",
        "create_reaction",
        "list_reactions",
        "delete_reaction",
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


def test_chat_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.apps.chat_v1.services.chat_service.transports.ChatServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ChatServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/chat.bot",
                "https://www.googleapis.com/auth/chat.delete",
                "https://www.googleapis.com/auth/chat.import",
                "https://www.googleapis.com/auth/chat.memberships",
                "https://www.googleapis.com/auth/chat.memberships.app",
                "https://www.googleapis.com/auth/chat.memberships.readonly",
                "https://www.googleapis.com/auth/chat.messages",
                "https://www.googleapis.com/auth/chat.messages.create",
                "https://www.googleapis.com/auth/chat.messages.reactions",
                "https://www.googleapis.com/auth/chat.messages.reactions.create",
                "https://www.googleapis.com/auth/chat.messages.reactions.readonly",
                "https://www.googleapis.com/auth/chat.messages.readonly",
                "https://www.googleapis.com/auth/chat.spaces",
                "https://www.googleapis.com/auth/chat.spaces.create",
                "https://www.googleapis.com/auth/chat.spaces.readonly",
            ),
            quota_project_id="octopus",
        )


def test_chat_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.apps.chat_v1.services.chat_service.transports.ChatServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ChatServiceTransport()
        adc.assert_called_once()


def test_chat_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        ChatServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/chat.bot",
                "https://www.googleapis.com/auth/chat.delete",
                "https://www.googleapis.com/auth/chat.import",
                "https://www.googleapis.com/auth/chat.memberships",
                "https://www.googleapis.com/auth/chat.memberships.app",
                "https://www.googleapis.com/auth/chat.memberships.readonly",
                "https://www.googleapis.com/auth/chat.messages",
                "https://www.googleapis.com/auth/chat.messages.create",
                "https://www.googleapis.com/auth/chat.messages.reactions",
                "https://www.googleapis.com/auth/chat.messages.reactions.create",
                "https://www.googleapis.com/auth/chat.messages.reactions.readonly",
                "https://www.googleapis.com/auth/chat.messages.readonly",
                "https://www.googleapis.com/auth/chat.spaces",
                "https://www.googleapis.com/auth/chat.spaces.create",
                "https://www.googleapis.com/auth/chat.spaces.readonly",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ChatServiceGrpcTransport,
        transports.ChatServiceGrpcAsyncIOTransport,
    ],
)
def test_chat_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/chat.bot",
                "https://www.googleapis.com/auth/chat.delete",
                "https://www.googleapis.com/auth/chat.import",
                "https://www.googleapis.com/auth/chat.memberships",
                "https://www.googleapis.com/auth/chat.memberships.app",
                "https://www.googleapis.com/auth/chat.memberships.readonly",
                "https://www.googleapis.com/auth/chat.messages",
                "https://www.googleapis.com/auth/chat.messages.create",
                "https://www.googleapis.com/auth/chat.messages.reactions",
                "https://www.googleapis.com/auth/chat.messages.reactions.create",
                "https://www.googleapis.com/auth/chat.messages.reactions.readonly",
                "https://www.googleapis.com/auth/chat.messages.readonly",
                "https://www.googleapis.com/auth/chat.spaces",
                "https://www.googleapis.com/auth/chat.spaces.create",
                "https://www.googleapis.com/auth/chat.spaces.readonly",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ChatServiceGrpcTransport,
        transports.ChatServiceGrpcAsyncIOTransport,
        transports.ChatServiceRestTransport,
    ],
)
def test_chat_service_transport_auth_gdch_credentials(transport_class):
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
        (transports.ChatServiceGrpcTransport, grpc_helpers),
        (transports.ChatServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_chat_service_transport_create_channel(transport_class, grpc_helpers):
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
            "chat.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/chat.bot",
                "https://www.googleapis.com/auth/chat.delete",
                "https://www.googleapis.com/auth/chat.import",
                "https://www.googleapis.com/auth/chat.memberships",
                "https://www.googleapis.com/auth/chat.memberships.app",
                "https://www.googleapis.com/auth/chat.memberships.readonly",
                "https://www.googleapis.com/auth/chat.messages",
                "https://www.googleapis.com/auth/chat.messages.create",
                "https://www.googleapis.com/auth/chat.messages.reactions",
                "https://www.googleapis.com/auth/chat.messages.reactions.create",
                "https://www.googleapis.com/auth/chat.messages.reactions.readonly",
                "https://www.googleapis.com/auth/chat.messages.readonly",
                "https://www.googleapis.com/auth/chat.spaces",
                "https://www.googleapis.com/auth/chat.spaces.create",
                "https://www.googleapis.com/auth/chat.spaces.readonly",
            ),
            scopes=["1", "2"],
            default_host="chat.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.ChatServiceGrpcTransport, transports.ChatServiceGrpcAsyncIOTransport],
)
def test_chat_service_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_chat_service_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.ChatServiceRestTransport(
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
def test_chat_service_host_no_port(transport_name):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint="chat.googleapis.com"),
        transport=transport_name,
    )
    assert client.transport._host == (
        "chat.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://chat.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_chat_service_host_with_port(transport_name):
    client = ChatServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="chat.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "chat.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://chat.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_chat_service_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = ChatServiceClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = ChatServiceClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.create_message._session
    session2 = client2.transport.create_message._session
    assert session1 != session2
    session1 = client1.transport.list_messages._session
    session2 = client2.transport.list_messages._session
    assert session1 != session2
    session1 = client1.transport.list_memberships._session
    session2 = client2.transport.list_memberships._session
    assert session1 != session2
    session1 = client1.transport.get_membership._session
    session2 = client2.transport.get_membership._session
    assert session1 != session2
    session1 = client1.transport.get_message._session
    session2 = client2.transport.get_message._session
    assert session1 != session2
    session1 = client1.transport.update_message._session
    session2 = client2.transport.update_message._session
    assert session1 != session2
    session1 = client1.transport.delete_message._session
    session2 = client2.transport.delete_message._session
    assert session1 != session2
    session1 = client1.transport.get_attachment._session
    session2 = client2.transport.get_attachment._session
    assert session1 != session2
    session1 = client1.transport.upload_attachment._session
    session2 = client2.transport.upload_attachment._session
    assert session1 != session2
    session1 = client1.transport.list_spaces._session
    session2 = client2.transport.list_spaces._session
    assert session1 != session2
    session1 = client1.transport.get_space._session
    session2 = client2.transport.get_space._session
    assert session1 != session2
    session1 = client1.transport.create_space._session
    session2 = client2.transport.create_space._session
    assert session1 != session2
    session1 = client1.transport.set_up_space._session
    session2 = client2.transport.set_up_space._session
    assert session1 != session2
    session1 = client1.transport.update_space._session
    session2 = client2.transport.update_space._session
    assert session1 != session2
    session1 = client1.transport.delete_space._session
    session2 = client2.transport.delete_space._session
    assert session1 != session2
    session1 = client1.transport.complete_import_space._session
    session2 = client2.transport.complete_import_space._session
    assert session1 != session2
    session1 = client1.transport.find_direct_message._session
    session2 = client2.transport.find_direct_message._session
    assert session1 != session2
    session1 = client1.transport.create_membership._session
    session2 = client2.transport.create_membership._session
    assert session1 != session2
    session1 = client1.transport.delete_membership._session
    session2 = client2.transport.delete_membership._session
    assert session1 != session2
    session1 = client1.transport.create_reaction._session
    session2 = client2.transport.create_reaction._session
    assert session1 != session2
    session1 = client1.transport.list_reactions._session
    session2 = client2.transport.list_reactions._session
    assert session1 != session2
    session1 = client1.transport.delete_reaction._session
    session2 = client2.transport.delete_reaction._session
    assert session1 != session2


def test_chat_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ChatServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_chat_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ChatServiceGrpcAsyncIOTransport(
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
    [transports.ChatServiceGrpcTransport, transports.ChatServiceGrpcAsyncIOTransport],
)
def test_chat_service_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.ChatServiceGrpcTransport, transports.ChatServiceGrpcAsyncIOTransport],
)
def test_chat_service_transport_channel_mtls_with_adc(transport_class):
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


def test_attachment_path():
    space = "squid"
    message = "clam"
    attachment = "whelk"
    expected = "spaces/{space}/messages/{message}/attachments/{attachment}".format(
        space=space,
        message=message,
        attachment=attachment,
    )
    actual = ChatServiceClient.attachment_path(space, message, attachment)
    assert expected == actual


def test_parse_attachment_path():
    expected = {
        "space": "octopus",
        "message": "oyster",
        "attachment": "nudibranch",
    }
    path = ChatServiceClient.attachment_path(**expected)

    # Check that the path construction is reversible.
    actual = ChatServiceClient.parse_attachment_path(path)
    assert expected == actual


def test_membership_path():
    space = "cuttlefish"
    member = "mussel"
    expected = "spaces/{space}/members/{member}".format(
        space=space,
        member=member,
    )
    actual = ChatServiceClient.membership_path(space, member)
    assert expected == actual


def test_parse_membership_path():
    expected = {
        "space": "winkle",
        "member": "nautilus",
    }
    path = ChatServiceClient.membership_path(**expected)

    # Check that the path construction is reversible.
    actual = ChatServiceClient.parse_membership_path(path)
    assert expected == actual


def test_message_path():
    space = "scallop"
    message = "abalone"
    expected = "spaces/{space}/messages/{message}".format(
        space=space,
        message=message,
    )
    actual = ChatServiceClient.message_path(space, message)
    assert expected == actual


def test_parse_message_path():
    expected = {
        "space": "squid",
        "message": "clam",
    }
    path = ChatServiceClient.message_path(**expected)

    # Check that the path construction is reversible.
    actual = ChatServiceClient.parse_message_path(path)
    assert expected == actual


def test_quoted_message_metadata_path():
    space = "whelk"
    message = "octopus"
    quoted_message_metadata = "oyster"
    expected = "spaces/{space}/messages/{message}/quotedMessageMetadata/{quoted_message_metadata}".format(
        space=space,
        message=message,
        quoted_message_metadata=quoted_message_metadata,
    )
    actual = ChatServiceClient.quoted_message_metadata_path(
        space, message, quoted_message_metadata
    )
    assert expected == actual


def test_parse_quoted_message_metadata_path():
    expected = {
        "space": "nudibranch",
        "message": "cuttlefish",
        "quoted_message_metadata": "mussel",
    }
    path = ChatServiceClient.quoted_message_metadata_path(**expected)

    # Check that the path construction is reversible.
    actual = ChatServiceClient.parse_quoted_message_metadata_path(path)
    assert expected == actual


def test_reaction_path():
    space = "winkle"
    message = "nautilus"
    reaction = "scallop"
    expected = "spaces/{space}/messages/{message}/reactions/{reaction}".format(
        space=space,
        message=message,
        reaction=reaction,
    )
    actual = ChatServiceClient.reaction_path(space, message, reaction)
    assert expected == actual


def test_parse_reaction_path():
    expected = {
        "space": "abalone",
        "message": "squid",
        "reaction": "clam",
    }
    path = ChatServiceClient.reaction_path(**expected)

    # Check that the path construction is reversible.
    actual = ChatServiceClient.parse_reaction_path(path)
    assert expected == actual


def test_space_path():
    space = "whelk"
    expected = "spaces/{space}".format(
        space=space,
    )
    actual = ChatServiceClient.space_path(space)
    assert expected == actual


def test_parse_space_path():
    expected = {
        "space": "octopus",
    }
    path = ChatServiceClient.space_path(**expected)

    # Check that the path construction is reversible.
    actual = ChatServiceClient.parse_space_path(path)
    assert expected == actual


def test_thread_path():
    space = "oyster"
    thread = "nudibranch"
    expected = "spaces/{space}/threads/{thread}".format(
        space=space,
        thread=thread,
    )
    actual = ChatServiceClient.thread_path(space, thread)
    assert expected == actual


def test_parse_thread_path():
    expected = {
        "space": "cuttlefish",
        "thread": "mussel",
    }
    path = ChatServiceClient.thread_path(**expected)

    # Check that the path construction is reversible.
    actual = ChatServiceClient.parse_thread_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "winkle"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = ChatServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nautilus",
    }
    path = ChatServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = ChatServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "scallop"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = ChatServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "abalone",
    }
    path = ChatServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = ChatServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "squid"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = ChatServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "clam",
    }
    path = ChatServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = ChatServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "whelk"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = ChatServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "octopus",
    }
    path = ChatServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = ChatServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "oyster"
    location = "nudibranch"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = ChatServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
    }
    path = ChatServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = ChatServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.ChatServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = ChatServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.ChatServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = ChatServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = ChatServiceAsyncClient(
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
        client = ChatServiceClient(
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
        client = ChatServiceClient(
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
        (ChatServiceClient, transports.ChatServiceGrpcTransport),
        (ChatServiceAsyncClient, transports.ChatServiceGrpcAsyncIOTransport),
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
