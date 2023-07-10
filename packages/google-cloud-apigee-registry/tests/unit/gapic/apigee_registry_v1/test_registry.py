# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.api import httpbody_pb2  # type: ignore
from google.api_core import gapic_v1, grpc_helpers, grpc_helpers_async, path_template
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.location import locations_pb2
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import options_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import json_format
from google.protobuf import timestamp_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.apigee_registry_v1.services.registry import (
    RegistryAsyncClient,
    RegistryClient,
    pagers,
    transports,
)
from google.cloud.apigee_registry_v1.types import registry_models, registry_service


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


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert RegistryClient._get_default_mtls_endpoint(None) is None
    assert RegistryClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert (
        RegistryClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        RegistryClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        RegistryClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert RegistryClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (RegistryClient, "grpc"),
        (RegistryAsyncClient, "grpc_asyncio"),
        (RegistryClient, "rest"),
    ],
)
def test_registry_client_from_service_account_info(client_class, transport_name):
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
            "apigeeregistry.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://apigeeregistry.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.RegistryGrpcTransport, "grpc"),
        (transports.RegistryGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.RegistryRestTransport, "rest"),
    ],
)
def test_registry_client_service_account_always_use_jwt(
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
        (RegistryClient, "grpc"),
        (RegistryAsyncClient, "grpc_asyncio"),
        (RegistryClient, "rest"),
    ],
)
def test_registry_client_from_service_account_file(client_class, transport_name):
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
            "apigeeregistry.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://apigeeregistry.googleapis.com"
        )


def test_registry_client_get_transport_class():
    transport = RegistryClient.get_transport_class()
    available_transports = [
        transports.RegistryGrpcTransport,
        transports.RegistryRestTransport,
    ]
    assert transport in available_transports

    transport = RegistryClient.get_transport_class("grpc")
    assert transport == transports.RegistryGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (RegistryClient, transports.RegistryGrpcTransport, "grpc"),
        (RegistryAsyncClient, transports.RegistryGrpcAsyncIOTransport, "grpc_asyncio"),
        (RegistryClient, transports.RegistryRestTransport, "rest"),
    ],
)
@mock.patch.object(
    RegistryClient, "DEFAULT_ENDPOINT", modify_default_endpoint(RegistryClient)
)
@mock.patch.object(
    RegistryAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(RegistryAsyncClient),
)
def test_registry_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(RegistryClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(RegistryClient, "get_transport_class") as gtc:
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
                host=client.DEFAULT_ENDPOINT,
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
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
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
            host=client.DEFAULT_ENDPOINT,
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
        (RegistryClient, transports.RegistryGrpcTransport, "grpc", "true"),
        (
            RegistryAsyncClient,
            transports.RegistryGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (RegistryClient, transports.RegistryGrpcTransport, "grpc", "false"),
        (
            RegistryAsyncClient,
            transports.RegistryGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (RegistryClient, transports.RegistryRestTransport, "rest", "true"),
        (RegistryClient, transports.RegistryRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    RegistryClient, "DEFAULT_ENDPOINT", modify_default_endpoint(RegistryClient)
)
@mock.patch.object(
    RegistryAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(RegistryAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_registry_client_mtls_env_auto(
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
                expected_host = client.DEFAULT_ENDPOINT
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
                        expected_host = client.DEFAULT_ENDPOINT
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
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize("client_class", [RegistryClient, RegistryAsyncClient])
@mock.patch.object(
    RegistryClient, "DEFAULT_ENDPOINT", modify_default_endpoint(RegistryClient)
)
@mock.patch.object(
    RegistryAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(RegistryAsyncClient),
)
def test_registry_client_get_mtls_endpoint_and_cert_source(client_class):
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


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (RegistryClient, transports.RegistryGrpcTransport, "grpc"),
        (RegistryAsyncClient, transports.RegistryGrpcAsyncIOTransport, "grpc_asyncio"),
        (RegistryClient, transports.RegistryRestTransport, "rest"),
    ],
)
def test_registry_client_client_options_scopes(
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
            host=client.DEFAULT_ENDPOINT,
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
        (RegistryClient, transports.RegistryGrpcTransport, "grpc", grpc_helpers),
        (
            RegistryAsyncClient,
            transports.RegistryGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (RegistryClient, transports.RegistryRestTransport, "rest", None),
    ],
)
def test_registry_client_client_options_credentials_file(
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
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_registry_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.apigee_registry_v1.services.registry.transports.RegistryGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = RegistryClient(client_options={"api_endpoint": "squid.clam.whelk"})
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
        (RegistryClient, transports.RegistryGrpcTransport, "grpc", grpc_helpers),
        (
            RegistryAsyncClient,
            transports.RegistryGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_registry_client_create_channel_credentials_file(
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
            host=client.DEFAULT_ENDPOINT,
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
            "apigeeregistry.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="apigeeregistry.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.ListApisRequest,
        dict,
    ],
)
def test_list_apis(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_apis), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_service.ListApisResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_apis(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ListApisRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApisPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_apis_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_apis), "__call__") as call:
        client.list_apis()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ListApisRequest()


@pytest.mark.asyncio
async def test_list_apis_async(
    transport: str = "grpc_asyncio", request_type=registry_service.ListApisRequest
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_apis), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_service.ListApisResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_apis(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ListApisRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApisAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_apis_async_from_dict():
    await test_list_apis_async(request_type=dict)


def test_list_apis_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.ListApisRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_apis), "__call__") as call:
        call.return_value = registry_service.ListApisResponse()
        client.list_apis(request)

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
async def test_list_apis_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.ListApisRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_apis), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_service.ListApisResponse()
        )
        await client.list_apis(request)

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


def test_list_apis_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_apis), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_service.ListApisResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_apis(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_apis_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_apis(
            registry_service.ListApisRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_apis_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_apis), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_service.ListApisResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_service.ListApisResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_apis(
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
async def test_list_apis_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_apis(
            registry_service.ListApisRequest(),
            parent="parent_value",
        )


def test_list_apis_pager(transport_name: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_apis), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApisResponse(
                apis=[
                    registry_models.Api(),
                    registry_models.Api(),
                    registry_models.Api(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApisResponse(
                apis=[],
                next_page_token="def",
            ),
            registry_service.ListApisResponse(
                apis=[
                    registry_models.Api(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApisResponse(
                apis=[
                    registry_models.Api(),
                    registry_models.Api(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_apis(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, registry_models.Api) for i in results)


def test_list_apis_pages(transport_name: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_apis), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApisResponse(
                apis=[
                    registry_models.Api(),
                    registry_models.Api(),
                    registry_models.Api(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApisResponse(
                apis=[],
                next_page_token="def",
            ),
            registry_service.ListApisResponse(
                apis=[
                    registry_models.Api(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApisResponse(
                apis=[
                    registry_models.Api(),
                    registry_models.Api(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_apis(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_apis_async_pager():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_apis), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApisResponse(
                apis=[
                    registry_models.Api(),
                    registry_models.Api(),
                    registry_models.Api(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApisResponse(
                apis=[],
                next_page_token="def",
            ),
            registry_service.ListApisResponse(
                apis=[
                    registry_models.Api(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApisResponse(
                apis=[
                    registry_models.Api(),
                    registry_models.Api(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_apis(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, registry_models.Api) for i in responses)


@pytest.mark.asyncio
async def test_list_apis_async_pages():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_apis), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApisResponse(
                apis=[
                    registry_models.Api(),
                    registry_models.Api(),
                    registry_models.Api(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApisResponse(
                apis=[],
                next_page_token="def",
            ),
            registry_service.ListApisResponse(
                apis=[
                    registry_models.Api(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApisResponse(
                apis=[
                    registry_models.Api(),
                    registry_models.Api(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_apis(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.GetApiRequest,
        dict,
    ],
)
def test_get_api(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_api), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.Api(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            availability="availability_value",
            recommended_version="recommended_version_value",
            recommended_deployment="recommended_deployment_value",
        )
        response = client.get_api(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.GetApiRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.Api)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.availability == "availability_value"
    assert response.recommended_version == "recommended_version_value"
    assert response.recommended_deployment == "recommended_deployment_value"


def test_get_api_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_api), "__call__") as call:
        client.get_api()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.GetApiRequest()


@pytest.mark.asyncio
async def test_get_api_async(
    transport: str = "grpc_asyncio", request_type=registry_service.GetApiRequest
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_api), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.Api(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                availability="availability_value",
                recommended_version="recommended_version_value",
                recommended_deployment="recommended_deployment_value",
            )
        )
        response = await client.get_api(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.GetApiRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.Api)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.availability == "availability_value"
    assert response.recommended_version == "recommended_version_value"
    assert response.recommended_deployment == "recommended_deployment_value"


@pytest.mark.asyncio
async def test_get_api_async_from_dict():
    await test_get_api_async(request_type=dict)


def test_get_api_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.GetApiRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_api), "__call__") as call:
        call.return_value = registry_models.Api()
        client.get_api(request)

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
async def test_get_api_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.GetApiRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_api), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(registry_models.Api())
        await client.get_api(request)

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


def test_get_api_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_api), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.Api()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_api(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_api_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_api(
            registry_service.GetApiRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_api_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_api), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.Api()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(registry_models.Api())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_api(
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
async def test_get_api_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_api(
            registry_service.GetApiRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.CreateApiRequest,
        dict,
    ],
)
def test_create_api(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_api), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.Api(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            availability="availability_value",
            recommended_version="recommended_version_value",
            recommended_deployment="recommended_deployment_value",
        )
        response = client.create_api(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.CreateApiRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.Api)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.availability == "availability_value"
    assert response.recommended_version == "recommended_version_value"
    assert response.recommended_deployment == "recommended_deployment_value"


def test_create_api_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_api), "__call__") as call:
        client.create_api()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.CreateApiRequest()


@pytest.mark.asyncio
async def test_create_api_async(
    transport: str = "grpc_asyncio", request_type=registry_service.CreateApiRequest
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_api), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.Api(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                availability="availability_value",
                recommended_version="recommended_version_value",
                recommended_deployment="recommended_deployment_value",
            )
        )
        response = await client.create_api(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.CreateApiRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.Api)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.availability == "availability_value"
    assert response.recommended_version == "recommended_version_value"
    assert response.recommended_deployment == "recommended_deployment_value"


@pytest.mark.asyncio
async def test_create_api_async_from_dict():
    await test_create_api_async(request_type=dict)


def test_create_api_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.CreateApiRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_api), "__call__") as call:
        call.return_value = registry_models.Api()
        client.create_api(request)

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
async def test_create_api_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.CreateApiRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_api), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(registry_models.Api())
        await client.create_api(request)

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


def test_create_api_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_api), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.Api()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_api(
            parent="parent_value",
            api=registry_models.Api(name="name_value"),
            api_id="api_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].api
        mock_val = registry_models.Api(name="name_value")
        assert arg == mock_val
        arg = args[0].api_id
        mock_val = "api_id_value"
        assert arg == mock_val


def test_create_api_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_api(
            registry_service.CreateApiRequest(),
            parent="parent_value",
            api=registry_models.Api(name="name_value"),
            api_id="api_id_value",
        )


@pytest.mark.asyncio
async def test_create_api_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_api), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.Api()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(registry_models.Api())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_api(
            parent="parent_value",
            api=registry_models.Api(name="name_value"),
            api_id="api_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].api
        mock_val = registry_models.Api(name="name_value")
        assert arg == mock_val
        arg = args[0].api_id
        mock_val = "api_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_api_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_api(
            registry_service.CreateApiRequest(),
            parent="parent_value",
            api=registry_models.Api(name="name_value"),
            api_id="api_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.UpdateApiRequest,
        dict,
    ],
)
def test_update_api(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_api), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.Api(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            availability="availability_value",
            recommended_version="recommended_version_value",
            recommended_deployment="recommended_deployment_value",
        )
        response = client.update_api(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.UpdateApiRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.Api)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.availability == "availability_value"
    assert response.recommended_version == "recommended_version_value"
    assert response.recommended_deployment == "recommended_deployment_value"


def test_update_api_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_api), "__call__") as call:
        client.update_api()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.UpdateApiRequest()


@pytest.mark.asyncio
async def test_update_api_async(
    transport: str = "grpc_asyncio", request_type=registry_service.UpdateApiRequest
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_api), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.Api(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                availability="availability_value",
                recommended_version="recommended_version_value",
                recommended_deployment="recommended_deployment_value",
            )
        )
        response = await client.update_api(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.UpdateApiRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.Api)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.availability == "availability_value"
    assert response.recommended_version == "recommended_version_value"
    assert response.recommended_deployment == "recommended_deployment_value"


@pytest.mark.asyncio
async def test_update_api_async_from_dict():
    await test_update_api_async(request_type=dict)


def test_update_api_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.UpdateApiRequest()

    request.api.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_api), "__call__") as call:
        call.return_value = registry_models.Api()
        client.update_api(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "api.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_api_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.UpdateApiRequest()

    request.api.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_api), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(registry_models.Api())
        await client.update_api(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "api.name=name_value",
    ) in kw["metadata"]


def test_update_api_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_api), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.Api()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_api(
            api=registry_models.Api(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].api
        mock_val = registry_models.Api(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_api_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_api(
            registry_service.UpdateApiRequest(),
            api=registry_models.Api(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_api_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_api), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.Api()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(registry_models.Api())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_api(
            api=registry_models.Api(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].api
        mock_val = registry_models.Api(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_api_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_api(
            registry_service.UpdateApiRequest(),
            api=registry_models.Api(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.DeleteApiRequest,
        dict,
    ],
)
def test_delete_api(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_api), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_api(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.DeleteApiRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_api_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_api), "__call__") as call:
        client.delete_api()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.DeleteApiRequest()


@pytest.mark.asyncio
async def test_delete_api_async(
    transport: str = "grpc_asyncio", request_type=registry_service.DeleteApiRequest
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_api), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_api(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.DeleteApiRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_api_async_from_dict():
    await test_delete_api_async(request_type=dict)


def test_delete_api_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.DeleteApiRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_api), "__call__") as call:
        call.return_value = None
        client.delete_api(request)

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
async def test_delete_api_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.DeleteApiRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_api), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_api(request)

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


def test_delete_api_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_api), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_api(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_api_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_api(
            registry_service.DeleteApiRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_api_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_api), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_api(
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
async def test_delete_api_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_api(
            registry_service.DeleteApiRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.ListApiVersionsRequest,
        dict,
    ],
)
def test_list_api_versions(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_service.ListApiVersionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_api_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ListApiVersionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApiVersionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_api_versions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_versions), "__call__"
    ) as call:
        client.list_api_versions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ListApiVersionsRequest()


@pytest.mark.asyncio
async def test_list_api_versions_async(
    transport: str = "grpc_asyncio",
    request_type=registry_service.ListApiVersionsRequest,
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_service.ListApiVersionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_api_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ListApiVersionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApiVersionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_api_versions_async_from_dict():
    await test_list_api_versions_async(request_type=dict)


def test_list_api_versions_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.ListApiVersionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_versions), "__call__"
    ) as call:
        call.return_value = registry_service.ListApiVersionsResponse()
        client.list_api_versions(request)

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
async def test_list_api_versions_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.ListApiVersionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_versions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_service.ListApiVersionsResponse()
        )
        await client.list_api_versions(request)

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


def test_list_api_versions_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_service.ListApiVersionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_api_versions(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_api_versions_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_api_versions(
            registry_service.ListApiVersionsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_api_versions_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_service.ListApiVersionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_service.ListApiVersionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_api_versions(
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
async def test_list_api_versions_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_api_versions(
            registry_service.ListApiVersionsRequest(),
            parent="parent_value",
        )


def test_list_api_versions_pager(transport_name: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_versions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApiVersionsResponse(
                api_versions=[
                    registry_models.ApiVersion(),
                    registry_models.ApiVersion(),
                    registry_models.ApiVersion(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiVersionsResponse(
                api_versions=[],
                next_page_token="def",
            ),
            registry_service.ListApiVersionsResponse(
                api_versions=[
                    registry_models.ApiVersion(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiVersionsResponse(
                api_versions=[
                    registry_models.ApiVersion(),
                    registry_models.ApiVersion(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_api_versions(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, registry_models.ApiVersion) for i in results)


def test_list_api_versions_pages(transport_name: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_versions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApiVersionsResponse(
                api_versions=[
                    registry_models.ApiVersion(),
                    registry_models.ApiVersion(),
                    registry_models.ApiVersion(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiVersionsResponse(
                api_versions=[],
                next_page_token="def",
            ),
            registry_service.ListApiVersionsResponse(
                api_versions=[
                    registry_models.ApiVersion(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiVersionsResponse(
                api_versions=[
                    registry_models.ApiVersion(),
                    registry_models.ApiVersion(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_api_versions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_api_versions_async_pager():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_versions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApiVersionsResponse(
                api_versions=[
                    registry_models.ApiVersion(),
                    registry_models.ApiVersion(),
                    registry_models.ApiVersion(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiVersionsResponse(
                api_versions=[],
                next_page_token="def",
            ),
            registry_service.ListApiVersionsResponse(
                api_versions=[
                    registry_models.ApiVersion(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiVersionsResponse(
                api_versions=[
                    registry_models.ApiVersion(),
                    registry_models.ApiVersion(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_api_versions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, registry_models.ApiVersion) for i in responses)


@pytest.mark.asyncio
async def test_list_api_versions_async_pages():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_versions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApiVersionsResponse(
                api_versions=[
                    registry_models.ApiVersion(),
                    registry_models.ApiVersion(),
                    registry_models.ApiVersion(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiVersionsResponse(
                api_versions=[],
                next_page_token="def",
            ),
            registry_service.ListApiVersionsResponse(
                api_versions=[
                    registry_models.ApiVersion(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiVersionsResponse(
                api_versions=[
                    registry_models.ApiVersion(),
                    registry_models.ApiVersion(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_api_versions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.GetApiVersionRequest,
        dict,
    ],
)
def test_get_api_version(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_api_version), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiVersion(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            state="state_value",
        )
        response = client.get_api_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.GetApiVersionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiVersion)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.state == "state_value"


def test_get_api_version_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_api_version), "__call__") as call:
        client.get_api_version()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.GetApiVersionRequest()


@pytest.mark.asyncio
async def test_get_api_version_async(
    transport: str = "grpc_asyncio", request_type=registry_service.GetApiVersionRequest
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_api_version), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiVersion(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                state="state_value",
            )
        )
        response = await client.get_api_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.GetApiVersionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiVersion)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.state == "state_value"


@pytest.mark.asyncio
async def test_get_api_version_async_from_dict():
    await test_get_api_version_async(request_type=dict)


def test_get_api_version_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.GetApiVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_api_version), "__call__") as call:
        call.return_value = registry_models.ApiVersion()
        client.get_api_version(request)

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
async def test_get_api_version_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.GetApiVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_api_version), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiVersion()
        )
        await client.get_api_version(request)

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


def test_get_api_version_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_api_version), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiVersion()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_api_version(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_api_version_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_api_version(
            registry_service.GetApiVersionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_api_version_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_api_version), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiVersion()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiVersion()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_api_version(
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
async def test_get_api_version_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_api_version(
            registry_service.GetApiVersionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.CreateApiVersionRequest,
        dict,
    ],
)
def test_create_api_version(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_api_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiVersion(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            state="state_value",
        )
        response = client.create_api_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.CreateApiVersionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiVersion)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.state == "state_value"


def test_create_api_version_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_api_version), "__call__"
    ) as call:
        client.create_api_version()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.CreateApiVersionRequest()


@pytest.mark.asyncio
async def test_create_api_version_async(
    transport: str = "grpc_asyncio",
    request_type=registry_service.CreateApiVersionRequest,
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_api_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiVersion(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                state="state_value",
            )
        )
        response = await client.create_api_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.CreateApiVersionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiVersion)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.state == "state_value"


@pytest.mark.asyncio
async def test_create_api_version_async_from_dict():
    await test_create_api_version_async(request_type=dict)


def test_create_api_version_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.CreateApiVersionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_api_version), "__call__"
    ) as call:
        call.return_value = registry_models.ApiVersion()
        client.create_api_version(request)

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
async def test_create_api_version_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.CreateApiVersionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_api_version), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiVersion()
        )
        await client.create_api_version(request)

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


def test_create_api_version_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_api_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiVersion()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_api_version(
            parent="parent_value",
            api_version=registry_models.ApiVersion(name="name_value"),
            api_version_id="api_version_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].api_version
        mock_val = registry_models.ApiVersion(name="name_value")
        assert arg == mock_val
        arg = args[0].api_version_id
        mock_val = "api_version_id_value"
        assert arg == mock_val


def test_create_api_version_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_api_version(
            registry_service.CreateApiVersionRequest(),
            parent="parent_value",
            api_version=registry_models.ApiVersion(name="name_value"),
            api_version_id="api_version_id_value",
        )


@pytest.mark.asyncio
async def test_create_api_version_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_api_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiVersion()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiVersion()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_api_version(
            parent="parent_value",
            api_version=registry_models.ApiVersion(name="name_value"),
            api_version_id="api_version_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].api_version
        mock_val = registry_models.ApiVersion(name="name_value")
        assert arg == mock_val
        arg = args[0].api_version_id
        mock_val = "api_version_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_api_version_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_api_version(
            registry_service.CreateApiVersionRequest(),
            parent="parent_value",
            api_version=registry_models.ApiVersion(name="name_value"),
            api_version_id="api_version_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.UpdateApiVersionRequest,
        dict,
    ],
)
def test_update_api_version(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_api_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiVersion(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            state="state_value",
        )
        response = client.update_api_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.UpdateApiVersionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiVersion)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.state == "state_value"


def test_update_api_version_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_api_version), "__call__"
    ) as call:
        client.update_api_version()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.UpdateApiVersionRequest()


@pytest.mark.asyncio
async def test_update_api_version_async(
    transport: str = "grpc_asyncio",
    request_type=registry_service.UpdateApiVersionRequest,
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_api_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiVersion(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                state="state_value",
            )
        )
        response = await client.update_api_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.UpdateApiVersionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiVersion)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.state == "state_value"


@pytest.mark.asyncio
async def test_update_api_version_async_from_dict():
    await test_update_api_version_async(request_type=dict)


def test_update_api_version_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.UpdateApiVersionRequest()

    request.api_version.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_api_version), "__call__"
    ) as call:
        call.return_value = registry_models.ApiVersion()
        client.update_api_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "api_version.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_api_version_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.UpdateApiVersionRequest()

    request.api_version.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_api_version), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiVersion()
        )
        await client.update_api_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "api_version.name=name_value",
    ) in kw["metadata"]


def test_update_api_version_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_api_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiVersion()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_api_version(
            api_version=registry_models.ApiVersion(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].api_version
        mock_val = registry_models.ApiVersion(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_api_version_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_api_version(
            registry_service.UpdateApiVersionRequest(),
            api_version=registry_models.ApiVersion(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_api_version_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_api_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiVersion()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiVersion()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_api_version(
            api_version=registry_models.ApiVersion(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].api_version
        mock_val = registry_models.ApiVersion(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_api_version_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_api_version(
            registry_service.UpdateApiVersionRequest(),
            api_version=registry_models.ApiVersion(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.DeleteApiVersionRequest,
        dict,
    ],
)
def test_delete_api_version(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_api_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.DeleteApiVersionRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_api_version_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_version), "__call__"
    ) as call:
        client.delete_api_version()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.DeleteApiVersionRequest()


@pytest.mark.asyncio
async def test_delete_api_version_async(
    transport: str = "grpc_asyncio",
    request_type=registry_service.DeleteApiVersionRequest,
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_api_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.DeleteApiVersionRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_api_version_async_from_dict():
    await test_delete_api_version_async(request_type=dict)


def test_delete_api_version_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.DeleteApiVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_version), "__call__"
    ) as call:
        call.return_value = None
        client.delete_api_version(request)

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
async def test_delete_api_version_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.DeleteApiVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_version), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_api_version(request)

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


def test_delete_api_version_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_api_version(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_api_version_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_api_version(
            registry_service.DeleteApiVersionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_api_version_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_api_version(
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
async def test_delete_api_version_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_api_version(
            registry_service.DeleteApiVersionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.ListApiSpecsRequest,
        dict,
    ],
)
def test_list_api_specs(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_api_specs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_service.ListApiSpecsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_api_specs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ListApiSpecsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApiSpecsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_api_specs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_api_specs), "__call__") as call:
        client.list_api_specs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ListApiSpecsRequest()


@pytest.mark.asyncio
async def test_list_api_specs_async(
    transport: str = "grpc_asyncio", request_type=registry_service.ListApiSpecsRequest
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_api_specs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_service.ListApiSpecsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_api_specs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ListApiSpecsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApiSpecsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_api_specs_async_from_dict():
    await test_list_api_specs_async(request_type=dict)


def test_list_api_specs_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.ListApiSpecsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_api_specs), "__call__") as call:
        call.return_value = registry_service.ListApiSpecsResponse()
        client.list_api_specs(request)

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
async def test_list_api_specs_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.ListApiSpecsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_api_specs), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_service.ListApiSpecsResponse()
        )
        await client.list_api_specs(request)

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


def test_list_api_specs_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_api_specs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_service.ListApiSpecsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_api_specs(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_api_specs_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_api_specs(
            registry_service.ListApiSpecsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_api_specs_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_api_specs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_service.ListApiSpecsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_service.ListApiSpecsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_api_specs(
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
async def test_list_api_specs_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_api_specs(
            registry_service.ListApiSpecsRequest(),
            parent="parent_value",
        )


def test_list_api_specs_pager(transport_name: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_api_specs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApiSpecsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiSpecsResponse(
                api_specs=[],
                next_page_token="def",
            ),
            registry_service.ListApiSpecsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiSpecsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_api_specs(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, registry_models.ApiSpec) for i in results)


def test_list_api_specs_pages(transport_name: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_api_specs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApiSpecsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiSpecsResponse(
                api_specs=[],
                next_page_token="def",
            ),
            registry_service.ListApiSpecsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiSpecsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_api_specs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_api_specs_async_pager():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_specs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApiSpecsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiSpecsResponse(
                api_specs=[],
                next_page_token="def",
            ),
            registry_service.ListApiSpecsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiSpecsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_api_specs(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, registry_models.ApiSpec) for i in responses)


@pytest.mark.asyncio
async def test_list_api_specs_async_pages():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_specs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApiSpecsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiSpecsResponse(
                api_specs=[],
                next_page_token="def",
            ),
            registry_service.ListApiSpecsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiSpecsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_api_specs(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.GetApiSpecRequest,
        dict,
    ],
)
def test_get_api_spec(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_api_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiSpec(
            name="name_value",
            filename="filename_value",
            description="description_value",
            revision_id="revision_id_value",
            mime_type="mime_type_value",
            size_bytes=1089,
            hash_="hash__value",
            source_uri="source_uri_value",
            contents=b"contents_blob",
        )
        response = client.get_api_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.GetApiSpecRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiSpec)
    assert response.name == "name_value"
    assert response.filename == "filename_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.source_uri == "source_uri_value"
    assert response.contents == b"contents_blob"


def test_get_api_spec_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_api_spec), "__call__") as call:
        client.get_api_spec()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.GetApiSpecRequest()


@pytest.mark.asyncio
async def test_get_api_spec_async(
    transport: str = "grpc_asyncio", request_type=registry_service.GetApiSpecRequest
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_api_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiSpec(
                name="name_value",
                filename="filename_value",
                description="description_value",
                revision_id="revision_id_value",
                mime_type="mime_type_value",
                size_bytes=1089,
                hash_="hash__value",
                source_uri="source_uri_value",
                contents=b"contents_blob",
            )
        )
        response = await client.get_api_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.GetApiSpecRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiSpec)
    assert response.name == "name_value"
    assert response.filename == "filename_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.source_uri == "source_uri_value"
    assert response.contents == b"contents_blob"


@pytest.mark.asyncio
async def test_get_api_spec_async_from_dict():
    await test_get_api_spec_async(request_type=dict)


def test_get_api_spec_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.GetApiSpecRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_api_spec), "__call__") as call:
        call.return_value = registry_models.ApiSpec()
        client.get_api_spec(request)

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
async def test_get_api_spec_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.GetApiSpecRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_api_spec), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiSpec()
        )
        await client.get_api_spec(request)

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


def test_get_api_spec_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_api_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiSpec()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_api_spec(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_api_spec_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_api_spec(
            registry_service.GetApiSpecRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_api_spec_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_api_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiSpec()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiSpec()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_api_spec(
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
async def test_get_api_spec_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_api_spec(
            registry_service.GetApiSpecRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.GetApiSpecContentsRequest,
        dict,
    ],
)
def test_get_api_spec_contents(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_api_spec_contents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = httpbody_pb2.HttpBody(
            content_type="content_type_value",
            data=b"data_blob",
        )
        response = client.get_api_spec_contents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.GetApiSpecContentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, httpbody_pb2.HttpBody)
    assert response.content_type == "content_type_value"
    assert response.data == b"data_blob"


def test_get_api_spec_contents_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_api_spec_contents), "__call__"
    ) as call:
        client.get_api_spec_contents()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.GetApiSpecContentsRequest()


@pytest.mark.asyncio
async def test_get_api_spec_contents_async(
    transport: str = "grpc_asyncio",
    request_type=registry_service.GetApiSpecContentsRequest,
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_api_spec_contents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            httpbody_pb2.HttpBody(
                content_type="content_type_value",
                data=b"data_blob",
            )
        )
        response = await client.get_api_spec_contents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.GetApiSpecContentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, httpbody_pb2.HttpBody)
    assert response.content_type == "content_type_value"
    assert response.data == b"data_blob"


@pytest.mark.asyncio
async def test_get_api_spec_contents_async_from_dict():
    await test_get_api_spec_contents_async(request_type=dict)


def test_get_api_spec_contents_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.GetApiSpecContentsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_api_spec_contents), "__call__"
    ) as call:
        call.return_value = httpbody_pb2.HttpBody()
        client.get_api_spec_contents(request)

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
async def test_get_api_spec_contents_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.GetApiSpecContentsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_api_spec_contents), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            httpbody_pb2.HttpBody()
        )
        await client.get_api_spec_contents(request)

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


def test_get_api_spec_contents_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_api_spec_contents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = httpbody_pb2.HttpBody()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_api_spec_contents(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_api_spec_contents_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_api_spec_contents(
            registry_service.GetApiSpecContentsRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_api_spec_contents_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_api_spec_contents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = httpbody_pb2.HttpBody()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            httpbody_pb2.HttpBody()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_api_spec_contents(
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
async def test_get_api_spec_contents_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_api_spec_contents(
            registry_service.GetApiSpecContentsRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.CreateApiSpecRequest,
        dict,
    ],
)
def test_create_api_spec(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_api_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiSpec(
            name="name_value",
            filename="filename_value",
            description="description_value",
            revision_id="revision_id_value",
            mime_type="mime_type_value",
            size_bytes=1089,
            hash_="hash__value",
            source_uri="source_uri_value",
            contents=b"contents_blob",
        )
        response = client.create_api_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.CreateApiSpecRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiSpec)
    assert response.name == "name_value"
    assert response.filename == "filename_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.source_uri == "source_uri_value"
    assert response.contents == b"contents_blob"


def test_create_api_spec_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_api_spec), "__call__") as call:
        client.create_api_spec()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.CreateApiSpecRequest()


@pytest.mark.asyncio
async def test_create_api_spec_async(
    transport: str = "grpc_asyncio", request_type=registry_service.CreateApiSpecRequest
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_api_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiSpec(
                name="name_value",
                filename="filename_value",
                description="description_value",
                revision_id="revision_id_value",
                mime_type="mime_type_value",
                size_bytes=1089,
                hash_="hash__value",
                source_uri="source_uri_value",
                contents=b"contents_blob",
            )
        )
        response = await client.create_api_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.CreateApiSpecRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiSpec)
    assert response.name == "name_value"
    assert response.filename == "filename_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.source_uri == "source_uri_value"
    assert response.contents == b"contents_blob"


@pytest.mark.asyncio
async def test_create_api_spec_async_from_dict():
    await test_create_api_spec_async(request_type=dict)


def test_create_api_spec_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.CreateApiSpecRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_api_spec), "__call__") as call:
        call.return_value = registry_models.ApiSpec()
        client.create_api_spec(request)

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
async def test_create_api_spec_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.CreateApiSpecRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_api_spec), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiSpec()
        )
        await client.create_api_spec(request)

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


def test_create_api_spec_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_api_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiSpec()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_api_spec(
            parent="parent_value",
            api_spec=registry_models.ApiSpec(name="name_value"),
            api_spec_id="api_spec_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].api_spec
        mock_val = registry_models.ApiSpec(name="name_value")
        assert arg == mock_val
        arg = args[0].api_spec_id
        mock_val = "api_spec_id_value"
        assert arg == mock_val


def test_create_api_spec_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_api_spec(
            registry_service.CreateApiSpecRequest(),
            parent="parent_value",
            api_spec=registry_models.ApiSpec(name="name_value"),
            api_spec_id="api_spec_id_value",
        )


@pytest.mark.asyncio
async def test_create_api_spec_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_api_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiSpec()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiSpec()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_api_spec(
            parent="parent_value",
            api_spec=registry_models.ApiSpec(name="name_value"),
            api_spec_id="api_spec_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].api_spec
        mock_val = registry_models.ApiSpec(name="name_value")
        assert arg == mock_val
        arg = args[0].api_spec_id
        mock_val = "api_spec_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_api_spec_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_api_spec(
            registry_service.CreateApiSpecRequest(),
            parent="parent_value",
            api_spec=registry_models.ApiSpec(name="name_value"),
            api_spec_id="api_spec_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.UpdateApiSpecRequest,
        dict,
    ],
)
def test_update_api_spec(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_api_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiSpec(
            name="name_value",
            filename="filename_value",
            description="description_value",
            revision_id="revision_id_value",
            mime_type="mime_type_value",
            size_bytes=1089,
            hash_="hash__value",
            source_uri="source_uri_value",
            contents=b"contents_blob",
        )
        response = client.update_api_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.UpdateApiSpecRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiSpec)
    assert response.name == "name_value"
    assert response.filename == "filename_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.source_uri == "source_uri_value"
    assert response.contents == b"contents_blob"


def test_update_api_spec_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_api_spec), "__call__") as call:
        client.update_api_spec()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.UpdateApiSpecRequest()


@pytest.mark.asyncio
async def test_update_api_spec_async(
    transport: str = "grpc_asyncio", request_type=registry_service.UpdateApiSpecRequest
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_api_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiSpec(
                name="name_value",
                filename="filename_value",
                description="description_value",
                revision_id="revision_id_value",
                mime_type="mime_type_value",
                size_bytes=1089,
                hash_="hash__value",
                source_uri="source_uri_value",
                contents=b"contents_blob",
            )
        )
        response = await client.update_api_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.UpdateApiSpecRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiSpec)
    assert response.name == "name_value"
    assert response.filename == "filename_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.source_uri == "source_uri_value"
    assert response.contents == b"contents_blob"


@pytest.mark.asyncio
async def test_update_api_spec_async_from_dict():
    await test_update_api_spec_async(request_type=dict)


def test_update_api_spec_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.UpdateApiSpecRequest()

    request.api_spec.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_api_spec), "__call__") as call:
        call.return_value = registry_models.ApiSpec()
        client.update_api_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "api_spec.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_api_spec_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.UpdateApiSpecRequest()

    request.api_spec.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_api_spec), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiSpec()
        )
        await client.update_api_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "api_spec.name=name_value",
    ) in kw["metadata"]


def test_update_api_spec_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_api_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiSpec()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_api_spec(
            api_spec=registry_models.ApiSpec(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].api_spec
        mock_val = registry_models.ApiSpec(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_api_spec_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_api_spec(
            registry_service.UpdateApiSpecRequest(),
            api_spec=registry_models.ApiSpec(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_api_spec_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_api_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiSpec()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiSpec()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_api_spec(
            api_spec=registry_models.ApiSpec(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].api_spec
        mock_val = registry_models.ApiSpec(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_api_spec_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_api_spec(
            registry_service.UpdateApiSpecRequest(),
            api_spec=registry_models.ApiSpec(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.DeleteApiSpecRequest,
        dict,
    ],
)
def test_delete_api_spec(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_api_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_api_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.DeleteApiSpecRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_api_spec_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_api_spec), "__call__") as call:
        client.delete_api_spec()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.DeleteApiSpecRequest()


@pytest.mark.asyncio
async def test_delete_api_spec_async(
    transport: str = "grpc_asyncio", request_type=registry_service.DeleteApiSpecRequest
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_api_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_api_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.DeleteApiSpecRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_api_spec_async_from_dict():
    await test_delete_api_spec_async(request_type=dict)


def test_delete_api_spec_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.DeleteApiSpecRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_api_spec), "__call__") as call:
        call.return_value = None
        client.delete_api_spec(request)

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
async def test_delete_api_spec_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.DeleteApiSpecRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_api_spec), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_api_spec(request)

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


def test_delete_api_spec_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_api_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_api_spec(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_api_spec_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_api_spec(
            registry_service.DeleteApiSpecRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_api_spec_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_api_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_api_spec(
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
async def test_delete_api_spec_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_api_spec(
            registry_service.DeleteApiSpecRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.TagApiSpecRevisionRequest,
        dict,
    ],
)
def test_tag_api_spec_revision(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.tag_api_spec_revision), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiSpec(
            name="name_value",
            filename="filename_value",
            description="description_value",
            revision_id="revision_id_value",
            mime_type="mime_type_value",
            size_bytes=1089,
            hash_="hash__value",
            source_uri="source_uri_value",
            contents=b"contents_blob",
        )
        response = client.tag_api_spec_revision(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.TagApiSpecRevisionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiSpec)
    assert response.name == "name_value"
    assert response.filename == "filename_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.source_uri == "source_uri_value"
    assert response.contents == b"contents_blob"


def test_tag_api_spec_revision_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.tag_api_spec_revision), "__call__"
    ) as call:
        client.tag_api_spec_revision()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.TagApiSpecRevisionRequest()


@pytest.mark.asyncio
async def test_tag_api_spec_revision_async(
    transport: str = "grpc_asyncio",
    request_type=registry_service.TagApiSpecRevisionRequest,
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.tag_api_spec_revision), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiSpec(
                name="name_value",
                filename="filename_value",
                description="description_value",
                revision_id="revision_id_value",
                mime_type="mime_type_value",
                size_bytes=1089,
                hash_="hash__value",
                source_uri="source_uri_value",
                contents=b"contents_blob",
            )
        )
        response = await client.tag_api_spec_revision(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.TagApiSpecRevisionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiSpec)
    assert response.name == "name_value"
    assert response.filename == "filename_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.source_uri == "source_uri_value"
    assert response.contents == b"contents_blob"


@pytest.mark.asyncio
async def test_tag_api_spec_revision_async_from_dict():
    await test_tag_api_spec_revision_async(request_type=dict)


def test_tag_api_spec_revision_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.TagApiSpecRevisionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.tag_api_spec_revision), "__call__"
    ) as call:
        call.return_value = registry_models.ApiSpec()
        client.tag_api_spec_revision(request)

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
async def test_tag_api_spec_revision_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.TagApiSpecRevisionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.tag_api_spec_revision), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiSpec()
        )
        await client.tag_api_spec_revision(request)

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
        registry_service.ListApiSpecRevisionsRequest,
        dict,
    ],
)
def test_list_api_spec_revisions(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_spec_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_service.ListApiSpecRevisionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_api_spec_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ListApiSpecRevisionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApiSpecRevisionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_api_spec_revisions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_spec_revisions), "__call__"
    ) as call:
        client.list_api_spec_revisions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ListApiSpecRevisionsRequest()


@pytest.mark.asyncio
async def test_list_api_spec_revisions_async(
    transport: str = "grpc_asyncio",
    request_type=registry_service.ListApiSpecRevisionsRequest,
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_spec_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_service.ListApiSpecRevisionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_api_spec_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ListApiSpecRevisionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApiSpecRevisionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_api_spec_revisions_async_from_dict():
    await test_list_api_spec_revisions_async(request_type=dict)


def test_list_api_spec_revisions_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.ListApiSpecRevisionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_spec_revisions), "__call__"
    ) as call:
        call.return_value = registry_service.ListApiSpecRevisionsResponse()
        client.list_api_spec_revisions(request)

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
async def test_list_api_spec_revisions_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.ListApiSpecRevisionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_spec_revisions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_service.ListApiSpecRevisionsResponse()
        )
        await client.list_api_spec_revisions(request)

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


def test_list_api_spec_revisions_pager(transport_name: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_spec_revisions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApiSpecRevisionsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiSpecRevisionsResponse(
                api_specs=[],
                next_page_token="def",
            ),
            registry_service.ListApiSpecRevisionsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiSpecRevisionsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", ""),)),
        )
        pager = client.list_api_spec_revisions(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, registry_models.ApiSpec) for i in results)


def test_list_api_spec_revisions_pages(transport_name: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_spec_revisions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApiSpecRevisionsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiSpecRevisionsResponse(
                api_specs=[],
                next_page_token="def",
            ),
            registry_service.ListApiSpecRevisionsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiSpecRevisionsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_api_spec_revisions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_api_spec_revisions_async_pager():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_spec_revisions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApiSpecRevisionsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiSpecRevisionsResponse(
                api_specs=[],
                next_page_token="def",
            ),
            registry_service.ListApiSpecRevisionsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiSpecRevisionsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_api_spec_revisions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, registry_models.ApiSpec) for i in responses)


@pytest.mark.asyncio
async def test_list_api_spec_revisions_async_pages():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_spec_revisions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApiSpecRevisionsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiSpecRevisionsResponse(
                api_specs=[],
                next_page_token="def",
            ),
            registry_service.ListApiSpecRevisionsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiSpecRevisionsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_api_spec_revisions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.RollbackApiSpecRequest,
        dict,
    ],
)
def test_rollback_api_spec(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_api_spec), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiSpec(
            name="name_value",
            filename="filename_value",
            description="description_value",
            revision_id="revision_id_value",
            mime_type="mime_type_value",
            size_bytes=1089,
            hash_="hash__value",
            source_uri="source_uri_value",
            contents=b"contents_blob",
        )
        response = client.rollback_api_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.RollbackApiSpecRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiSpec)
    assert response.name == "name_value"
    assert response.filename == "filename_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.source_uri == "source_uri_value"
    assert response.contents == b"contents_blob"


def test_rollback_api_spec_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_api_spec), "__call__"
    ) as call:
        client.rollback_api_spec()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.RollbackApiSpecRequest()


@pytest.mark.asyncio
async def test_rollback_api_spec_async(
    transport: str = "grpc_asyncio",
    request_type=registry_service.RollbackApiSpecRequest,
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_api_spec), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiSpec(
                name="name_value",
                filename="filename_value",
                description="description_value",
                revision_id="revision_id_value",
                mime_type="mime_type_value",
                size_bytes=1089,
                hash_="hash__value",
                source_uri="source_uri_value",
                contents=b"contents_blob",
            )
        )
        response = await client.rollback_api_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.RollbackApiSpecRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiSpec)
    assert response.name == "name_value"
    assert response.filename == "filename_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.source_uri == "source_uri_value"
    assert response.contents == b"contents_blob"


@pytest.mark.asyncio
async def test_rollback_api_spec_async_from_dict():
    await test_rollback_api_spec_async(request_type=dict)


def test_rollback_api_spec_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.RollbackApiSpecRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_api_spec), "__call__"
    ) as call:
        call.return_value = registry_models.ApiSpec()
        client.rollback_api_spec(request)

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
async def test_rollback_api_spec_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.RollbackApiSpecRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_api_spec), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiSpec()
        )
        await client.rollback_api_spec(request)

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
        registry_service.DeleteApiSpecRevisionRequest,
        dict,
    ],
)
def test_delete_api_spec_revision(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_spec_revision), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiSpec(
            name="name_value",
            filename="filename_value",
            description="description_value",
            revision_id="revision_id_value",
            mime_type="mime_type_value",
            size_bytes=1089,
            hash_="hash__value",
            source_uri="source_uri_value",
            contents=b"contents_blob",
        )
        response = client.delete_api_spec_revision(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.DeleteApiSpecRevisionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiSpec)
    assert response.name == "name_value"
    assert response.filename == "filename_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.source_uri == "source_uri_value"
    assert response.contents == b"contents_blob"


def test_delete_api_spec_revision_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_spec_revision), "__call__"
    ) as call:
        client.delete_api_spec_revision()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.DeleteApiSpecRevisionRequest()


@pytest.mark.asyncio
async def test_delete_api_spec_revision_async(
    transport: str = "grpc_asyncio",
    request_type=registry_service.DeleteApiSpecRevisionRequest,
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_spec_revision), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiSpec(
                name="name_value",
                filename="filename_value",
                description="description_value",
                revision_id="revision_id_value",
                mime_type="mime_type_value",
                size_bytes=1089,
                hash_="hash__value",
                source_uri="source_uri_value",
                contents=b"contents_blob",
            )
        )
        response = await client.delete_api_spec_revision(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.DeleteApiSpecRevisionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiSpec)
    assert response.name == "name_value"
    assert response.filename == "filename_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.source_uri == "source_uri_value"
    assert response.contents == b"contents_blob"


@pytest.mark.asyncio
async def test_delete_api_spec_revision_async_from_dict():
    await test_delete_api_spec_revision_async(request_type=dict)


def test_delete_api_spec_revision_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.DeleteApiSpecRevisionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_spec_revision), "__call__"
    ) as call:
        call.return_value = registry_models.ApiSpec()
        client.delete_api_spec_revision(request)

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
async def test_delete_api_spec_revision_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.DeleteApiSpecRevisionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_spec_revision), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiSpec()
        )
        await client.delete_api_spec_revision(request)

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


def test_delete_api_spec_revision_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_spec_revision), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiSpec()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_api_spec_revision(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_api_spec_revision_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_api_spec_revision(
            registry_service.DeleteApiSpecRevisionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_api_spec_revision_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_spec_revision), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiSpec()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiSpec()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_api_spec_revision(
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
async def test_delete_api_spec_revision_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_api_spec_revision(
            registry_service.DeleteApiSpecRevisionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.ListApiDeploymentsRequest,
        dict,
    ],
)
def test_list_api_deployments(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_deployments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_service.ListApiDeploymentsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_api_deployments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ListApiDeploymentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApiDeploymentsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_api_deployments_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_deployments), "__call__"
    ) as call:
        client.list_api_deployments()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ListApiDeploymentsRequest()


@pytest.mark.asyncio
async def test_list_api_deployments_async(
    transport: str = "grpc_asyncio",
    request_type=registry_service.ListApiDeploymentsRequest,
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_deployments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_service.ListApiDeploymentsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_api_deployments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ListApiDeploymentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApiDeploymentsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_api_deployments_async_from_dict():
    await test_list_api_deployments_async(request_type=dict)


def test_list_api_deployments_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.ListApiDeploymentsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_deployments), "__call__"
    ) as call:
        call.return_value = registry_service.ListApiDeploymentsResponse()
        client.list_api_deployments(request)

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
async def test_list_api_deployments_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.ListApiDeploymentsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_deployments), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_service.ListApiDeploymentsResponse()
        )
        await client.list_api_deployments(request)

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


def test_list_api_deployments_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_deployments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_service.ListApiDeploymentsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_api_deployments(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_api_deployments_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_api_deployments(
            registry_service.ListApiDeploymentsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_api_deployments_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_deployments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_service.ListApiDeploymentsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_service.ListApiDeploymentsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_api_deployments(
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
async def test_list_api_deployments_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_api_deployments(
            registry_service.ListApiDeploymentsRequest(),
            parent="parent_value",
        )


def test_list_api_deployments_pager(transport_name: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_deployments), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApiDeploymentsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiDeploymentsResponse(
                api_deployments=[],
                next_page_token="def",
            ),
            registry_service.ListApiDeploymentsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiDeploymentsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_api_deployments(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, registry_models.ApiDeployment) for i in results)


def test_list_api_deployments_pages(transport_name: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_deployments), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApiDeploymentsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiDeploymentsResponse(
                api_deployments=[],
                next_page_token="def",
            ),
            registry_service.ListApiDeploymentsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiDeploymentsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_api_deployments(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_api_deployments_async_pager():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_deployments),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApiDeploymentsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiDeploymentsResponse(
                api_deployments=[],
                next_page_token="def",
            ),
            registry_service.ListApiDeploymentsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiDeploymentsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_api_deployments(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, registry_models.ApiDeployment) for i in responses)


@pytest.mark.asyncio
async def test_list_api_deployments_async_pages():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_deployments),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApiDeploymentsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiDeploymentsResponse(
                api_deployments=[],
                next_page_token="def",
            ),
            registry_service.ListApiDeploymentsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiDeploymentsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_api_deployments(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.GetApiDeploymentRequest,
        dict,
    ],
)
def test_get_api_deployment(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_api_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiDeployment(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            revision_id="revision_id_value",
            api_spec_revision="api_spec_revision_value",
            endpoint_uri="endpoint_uri_value",
            external_channel_uri="external_channel_uri_value",
            intended_audience="intended_audience_value",
            access_guidance="access_guidance_value",
        )
        response = client.get_api_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.GetApiDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiDeployment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.api_spec_revision == "api_spec_revision_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.external_channel_uri == "external_channel_uri_value"
    assert response.intended_audience == "intended_audience_value"
    assert response.access_guidance == "access_guidance_value"


def test_get_api_deployment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_api_deployment), "__call__"
    ) as call:
        client.get_api_deployment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.GetApiDeploymentRequest()


@pytest.mark.asyncio
async def test_get_api_deployment_async(
    transport: str = "grpc_asyncio",
    request_type=registry_service.GetApiDeploymentRequest,
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_api_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiDeployment(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                revision_id="revision_id_value",
                api_spec_revision="api_spec_revision_value",
                endpoint_uri="endpoint_uri_value",
                external_channel_uri="external_channel_uri_value",
                intended_audience="intended_audience_value",
                access_guidance="access_guidance_value",
            )
        )
        response = await client.get_api_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.GetApiDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiDeployment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.api_spec_revision == "api_spec_revision_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.external_channel_uri == "external_channel_uri_value"
    assert response.intended_audience == "intended_audience_value"
    assert response.access_guidance == "access_guidance_value"


@pytest.mark.asyncio
async def test_get_api_deployment_async_from_dict():
    await test_get_api_deployment_async(request_type=dict)


def test_get_api_deployment_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.GetApiDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_api_deployment), "__call__"
    ) as call:
        call.return_value = registry_models.ApiDeployment()
        client.get_api_deployment(request)

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
async def test_get_api_deployment_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.GetApiDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_api_deployment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiDeployment()
        )
        await client.get_api_deployment(request)

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


def test_get_api_deployment_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_api_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiDeployment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_api_deployment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_api_deployment_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_api_deployment(
            registry_service.GetApiDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_api_deployment_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_api_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiDeployment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiDeployment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_api_deployment(
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
async def test_get_api_deployment_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_api_deployment(
            registry_service.GetApiDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.CreateApiDeploymentRequest,
        dict,
    ],
)
def test_create_api_deployment(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_api_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiDeployment(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            revision_id="revision_id_value",
            api_spec_revision="api_spec_revision_value",
            endpoint_uri="endpoint_uri_value",
            external_channel_uri="external_channel_uri_value",
            intended_audience="intended_audience_value",
            access_guidance="access_guidance_value",
        )
        response = client.create_api_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.CreateApiDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiDeployment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.api_spec_revision == "api_spec_revision_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.external_channel_uri == "external_channel_uri_value"
    assert response.intended_audience == "intended_audience_value"
    assert response.access_guidance == "access_guidance_value"


def test_create_api_deployment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_api_deployment), "__call__"
    ) as call:
        client.create_api_deployment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.CreateApiDeploymentRequest()


@pytest.mark.asyncio
async def test_create_api_deployment_async(
    transport: str = "grpc_asyncio",
    request_type=registry_service.CreateApiDeploymentRequest,
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_api_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiDeployment(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                revision_id="revision_id_value",
                api_spec_revision="api_spec_revision_value",
                endpoint_uri="endpoint_uri_value",
                external_channel_uri="external_channel_uri_value",
                intended_audience="intended_audience_value",
                access_guidance="access_guidance_value",
            )
        )
        response = await client.create_api_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.CreateApiDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiDeployment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.api_spec_revision == "api_spec_revision_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.external_channel_uri == "external_channel_uri_value"
    assert response.intended_audience == "intended_audience_value"
    assert response.access_guidance == "access_guidance_value"


@pytest.mark.asyncio
async def test_create_api_deployment_async_from_dict():
    await test_create_api_deployment_async(request_type=dict)


def test_create_api_deployment_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.CreateApiDeploymentRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_api_deployment), "__call__"
    ) as call:
        call.return_value = registry_models.ApiDeployment()
        client.create_api_deployment(request)

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
async def test_create_api_deployment_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.CreateApiDeploymentRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_api_deployment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiDeployment()
        )
        await client.create_api_deployment(request)

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


def test_create_api_deployment_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_api_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiDeployment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_api_deployment(
            parent="parent_value",
            api_deployment=registry_models.ApiDeployment(name="name_value"),
            api_deployment_id="api_deployment_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].api_deployment
        mock_val = registry_models.ApiDeployment(name="name_value")
        assert arg == mock_val
        arg = args[0].api_deployment_id
        mock_val = "api_deployment_id_value"
        assert arg == mock_val


def test_create_api_deployment_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_api_deployment(
            registry_service.CreateApiDeploymentRequest(),
            parent="parent_value",
            api_deployment=registry_models.ApiDeployment(name="name_value"),
            api_deployment_id="api_deployment_id_value",
        )


@pytest.mark.asyncio
async def test_create_api_deployment_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_api_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiDeployment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiDeployment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_api_deployment(
            parent="parent_value",
            api_deployment=registry_models.ApiDeployment(name="name_value"),
            api_deployment_id="api_deployment_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].api_deployment
        mock_val = registry_models.ApiDeployment(name="name_value")
        assert arg == mock_val
        arg = args[0].api_deployment_id
        mock_val = "api_deployment_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_api_deployment_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_api_deployment(
            registry_service.CreateApiDeploymentRequest(),
            parent="parent_value",
            api_deployment=registry_models.ApiDeployment(name="name_value"),
            api_deployment_id="api_deployment_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.UpdateApiDeploymentRequest,
        dict,
    ],
)
def test_update_api_deployment(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_api_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiDeployment(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            revision_id="revision_id_value",
            api_spec_revision="api_spec_revision_value",
            endpoint_uri="endpoint_uri_value",
            external_channel_uri="external_channel_uri_value",
            intended_audience="intended_audience_value",
            access_guidance="access_guidance_value",
        )
        response = client.update_api_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.UpdateApiDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiDeployment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.api_spec_revision == "api_spec_revision_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.external_channel_uri == "external_channel_uri_value"
    assert response.intended_audience == "intended_audience_value"
    assert response.access_guidance == "access_guidance_value"


def test_update_api_deployment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_api_deployment), "__call__"
    ) as call:
        client.update_api_deployment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.UpdateApiDeploymentRequest()


@pytest.mark.asyncio
async def test_update_api_deployment_async(
    transport: str = "grpc_asyncio",
    request_type=registry_service.UpdateApiDeploymentRequest,
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_api_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiDeployment(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                revision_id="revision_id_value",
                api_spec_revision="api_spec_revision_value",
                endpoint_uri="endpoint_uri_value",
                external_channel_uri="external_channel_uri_value",
                intended_audience="intended_audience_value",
                access_guidance="access_guidance_value",
            )
        )
        response = await client.update_api_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.UpdateApiDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiDeployment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.api_spec_revision == "api_spec_revision_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.external_channel_uri == "external_channel_uri_value"
    assert response.intended_audience == "intended_audience_value"
    assert response.access_guidance == "access_guidance_value"


@pytest.mark.asyncio
async def test_update_api_deployment_async_from_dict():
    await test_update_api_deployment_async(request_type=dict)


def test_update_api_deployment_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.UpdateApiDeploymentRequest()

    request.api_deployment.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_api_deployment), "__call__"
    ) as call:
        call.return_value = registry_models.ApiDeployment()
        client.update_api_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "api_deployment.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_api_deployment_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.UpdateApiDeploymentRequest()

    request.api_deployment.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_api_deployment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiDeployment()
        )
        await client.update_api_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "api_deployment.name=name_value",
    ) in kw["metadata"]


def test_update_api_deployment_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_api_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiDeployment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_api_deployment(
            api_deployment=registry_models.ApiDeployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].api_deployment
        mock_val = registry_models.ApiDeployment(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_api_deployment_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_api_deployment(
            registry_service.UpdateApiDeploymentRequest(),
            api_deployment=registry_models.ApiDeployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_api_deployment_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_api_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiDeployment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiDeployment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_api_deployment(
            api_deployment=registry_models.ApiDeployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].api_deployment
        mock_val = registry_models.ApiDeployment(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_api_deployment_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_api_deployment(
            registry_service.UpdateApiDeploymentRequest(),
            api_deployment=registry_models.ApiDeployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.DeleteApiDeploymentRequest,
        dict,
    ],
)
def test_delete_api_deployment(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_api_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.DeleteApiDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_api_deployment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_deployment), "__call__"
    ) as call:
        client.delete_api_deployment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.DeleteApiDeploymentRequest()


@pytest.mark.asyncio
async def test_delete_api_deployment_async(
    transport: str = "grpc_asyncio",
    request_type=registry_service.DeleteApiDeploymentRequest,
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_api_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.DeleteApiDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_api_deployment_async_from_dict():
    await test_delete_api_deployment_async(request_type=dict)


def test_delete_api_deployment_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.DeleteApiDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_deployment), "__call__"
    ) as call:
        call.return_value = None
        client.delete_api_deployment(request)

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
async def test_delete_api_deployment_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.DeleteApiDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_deployment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_api_deployment(request)

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


def test_delete_api_deployment_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_api_deployment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_api_deployment_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_api_deployment(
            registry_service.DeleteApiDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_api_deployment_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_api_deployment(
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
async def test_delete_api_deployment_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_api_deployment(
            registry_service.DeleteApiDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.TagApiDeploymentRevisionRequest,
        dict,
    ],
)
def test_tag_api_deployment_revision(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.tag_api_deployment_revision), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiDeployment(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            revision_id="revision_id_value",
            api_spec_revision="api_spec_revision_value",
            endpoint_uri="endpoint_uri_value",
            external_channel_uri="external_channel_uri_value",
            intended_audience="intended_audience_value",
            access_guidance="access_guidance_value",
        )
        response = client.tag_api_deployment_revision(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.TagApiDeploymentRevisionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiDeployment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.api_spec_revision == "api_spec_revision_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.external_channel_uri == "external_channel_uri_value"
    assert response.intended_audience == "intended_audience_value"
    assert response.access_guidance == "access_guidance_value"


def test_tag_api_deployment_revision_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.tag_api_deployment_revision), "__call__"
    ) as call:
        client.tag_api_deployment_revision()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.TagApiDeploymentRevisionRequest()


@pytest.mark.asyncio
async def test_tag_api_deployment_revision_async(
    transport: str = "grpc_asyncio",
    request_type=registry_service.TagApiDeploymentRevisionRequest,
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.tag_api_deployment_revision), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiDeployment(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                revision_id="revision_id_value",
                api_spec_revision="api_spec_revision_value",
                endpoint_uri="endpoint_uri_value",
                external_channel_uri="external_channel_uri_value",
                intended_audience="intended_audience_value",
                access_guidance="access_guidance_value",
            )
        )
        response = await client.tag_api_deployment_revision(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.TagApiDeploymentRevisionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiDeployment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.api_spec_revision == "api_spec_revision_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.external_channel_uri == "external_channel_uri_value"
    assert response.intended_audience == "intended_audience_value"
    assert response.access_guidance == "access_guidance_value"


@pytest.mark.asyncio
async def test_tag_api_deployment_revision_async_from_dict():
    await test_tag_api_deployment_revision_async(request_type=dict)


def test_tag_api_deployment_revision_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.TagApiDeploymentRevisionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.tag_api_deployment_revision), "__call__"
    ) as call:
        call.return_value = registry_models.ApiDeployment()
        client.tag_api_deployment_revision(request)

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
async def test_tag_api_deployment_revision_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.TagApiDeploymentRevisionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.tag_api_deployment_revision), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiDeployment()
        )
        await client.tag_api_deployment_revision(request)

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
        registry_service.ListApiDeploymentRevisionsRequest,
        dict,
    ],
)
def test_list_api_deployment_revisions(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_deployment_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_service.ListApiDeploymentRevisionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_api_deployment_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ListApiDeploymentRevisionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApiDeploymentRevisionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_api_deployment_revisions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_deployment_revisions), "__call__"
    ) as call:
        client.list_api_deployment_revisions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ListApiDeploymentRevisionsRequest()


@pytest.mark.asyncio
async def test_list_api_deployment_revisions_async(
    transport: str = "grpc_asyncio",
    request_type=registry_service.ListApiDeploymentRevisionsRequest,
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_deployment_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_service.ListApiDeploymentRevisionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_api_deployment_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ListApiDeploymentRevisionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApiDeploymentRevisionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_api_deployment_revisions_async_from_dict():
    await test_list_api_deployment_revisions_async(request_type=dict)


def test_list_api_deployment_revisions_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.ListApiDeploymentRevisionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_deployment_revisions), "__call__"
    ) as call:
        call.return_value = registry_service.ListApiDeploymentRevisionsResponse()
        client.list_api_deployment_revisions(request)

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
async def test_list_api_deployment_revisions_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.ListApiDeploymentRevisionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_deployment_revisions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_service.ListApiDeploymentRevisionsResponse()
        )
        await client.list_api_deployment_revisions(request)

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


def test_list_api_deployment_revisions_pager(transport_name: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_deployment_revisions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApiDeploymentRevisionsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiDeploymentRevisionsResponse(
                api_deployments=[],
                next_page_token="def",
            ),
            registry_service.ListApiDeploymentRevisionsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiDeploymentRevisionsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", ""),)),
        )
        pager = client.list_api_deployment_revisions(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, registry_models.ApiDeployment) for i in results)


def test_list_api_deployment_revisions_pages(transport_name: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_deployment_revisions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApiDeploymentRevisionsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiDeploymentRevisionsResponse(
                api_deployments=[],
                next_page_token="def",
            ),
            registry_service.ListApiDeploymentRevisionsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiDeploymentRevisionsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_api_deployment_revisions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_api_deployment_revisions_async_pager():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_deployment_revisions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApiDeploymentRevisionsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiDeploymentRevisionsResponse(
                api_deployments=[],
                next_page_token="def",
            ),
            registry_service.ListApiDeploymentRevisionsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiDeploymentRevisionsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_api_deployment_revisions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, registry_models.ApiDeployment) for i in responses)


@pytest.mark.asyncio
async def test_list_api_deployment_revisions_async_pages():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_api_deployment_revisions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListApiDeploymentRevisionsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiDeploymentRevisionsResponse(
                api_deployments=[],
                next_page_token="def",
            ),
            registry_service.ListApiDeploymentRevisionsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiDeploymentRevisionsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_api_deployment_revisions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.RollbackApiDeploymentRequest,
        dict,
    ],
)
def test_rollback_api_deployment(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_api_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiDeployment(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            revision_id="revision_id_value",
            api_spec_revision="api_spec_revision_value",
            endpoint_uri="endpoint_uri_value",
            external_channel_uri="external_channel_uri_value",
            intended_audience="intended_audience_value",
            access_guidance="access_guidance_value",
        )
        response = client.rollback_api_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.RollbackApiDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiDeployment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.api_spec_revision == "api_spec_revision_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.external_channel_uri == "external_channel_uri_value"
    assert response.intended_audience == "intended_audience_value"
    assert response.access_guidance == "access_guidance_value"


def test_rollback_api_deployment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_api_deployment), "__call__"
    ) as call:
        client.rollback_api_deployment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.RollbackApiDeploymentRequest()


@pytest.mark.asyncio
async def test_rollback_api_deployment_async(
    transport: str = "grpc_asyncio",
    request_type=registry_service.RollbackApiDeploymentRequest,
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_api_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiDeployment(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                revision_id="revision_id_value",
                api_spec_revision="api_spec_revision_value",
                endpoint_uri="endpoint_uri_value",
                external_channel_uri="external_channel_uri_value",
                intended_audience="intended_audience_value",
                access_guidance="access_guidance_value",
            )
        )
        response = await client.rollback_api_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.RollbackApiDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiDeployment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.api_spec_revision == "api_spec_revision_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.external_channel_uri == "external_channel_uri_value"
    assert response.intended_audience == "intended_audience_value"
    assert response.access_guidance == "access_guidance_value"


@pytest.mark.asyncio
async def test_rollback_api_deployment_async_from_dict():
    await test_rollback_api_deployment_async(request_type=dict)


def test_rollback_api_deployment_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.RollbackApiDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_api_deployment), "__call__"
    ) as call:
        call.return_value = registry_models.ApiDeployment()
        client.rollback_api_deployment(request)

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
async def test_rollback_api_deployment_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.RollbackApiDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_api_deployment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiDeployment()
        )
        await client.rollback_api_deployment(request)

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
        registry_service.DeleteApiDeploymentRevisionRequest,
        dict,
    ],
)
def test_delete_api_deployment_revision(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_deployment_revision), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiDeployment(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            revision_id="revision_id_value",
            api_spec_revision="api_spec_revision_value",
            endpoint_uri="endpoint_uri_value",
            external_channel_uri="external_channel_uri_value",
            intended_audience="intended_audience_value",
            access_guidance="access_guidance_value",
        )
        response = client.delete_api_deployment_revision(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.DeleteApiDeploymentRevisionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiDeployment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.api_spec_revision == "api_spec_revision_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.external_channel_uri == "external_channel_uri_value"
    assert response.intended_audience == "intended_audience_value"
    assert response.access_guidance == "access_guidance_value"


def test_delete_api_deployment_revision_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_deployment_revision), "__call__"
    ) as call:
        client.delete_api_deployment_revision()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.DeleteApiDeploymentRevisionRequest()


@pytest.mark.asyncio
async def test_delete_api_deployment_revision_async(
    transport: str = "grpc_asyncio",
    request_type=registry_service.DeleteApiDeploymentRevisionRequest,
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_deployment_revision), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiDeployment(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                revision_id="revision_id_value",
                api_spec_revision="api_spec_revision_value",
                endpoint_uri="endpoint_uri_value",
                external_channel_uri="external_channel_uri_value",
                intended_audience="intended_audience_value",
                access_guidance="access_guidance_value",
            )
        )
        response = await client.delete_api_deployment_revision(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.DeleteApiDeploymentRevisionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiDeployment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.api_spec_revision == "api_spec_revision_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.external_channel_uri == "external_channel_uri_value"
    assert response.intended_audience == "intended_audience_value"
    assert response.access_guidance == "access_guidance_value"


@pytest.mark.asyncio
async def test_delete_api_deployment_revision_async_from_dict():
    await test_delete_api_deployment_revision_async(request_type=dict)


def test_delete_api_deployment_revision_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.DeleteApiDeploymentRevisionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_deployment_revision), "__call__"
    ) as call:
        call.return_value = registry_models.ApiDeployment()
        client.delete_api_deployment_revision(request)

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
async def test_delete_api_deployment_revision_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.DeleteApiDeploymentRevisionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_deployment_revision), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiDeployment()
        )
        await client.delete_api_deployment_revision(request)

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


def test_delete_api_deployment_revision_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_deployment_revision), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiDeployment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_api_deployment_revision(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_api_deployment_revision_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_api_deployment_revision(
            registry_service.DeleteApiDeploymentRevisionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_api_deployment_revision_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_api_deployment_revision), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.ApiDeployment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.ApiDeployment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_api_deployment_revision(
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
async def test_delete_api_deployment_revision_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_api_deployment_revision(
            registry_service.DeleteApiDeploymentRevisionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.ListArtifactsRequest,
        dict,
    ],
)
def test_list_artifacts(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_artifacts), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_service.ListArtifactsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_artifacts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ListArtifactsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListArtifactsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_artifacts_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_artifacts), "__call__") as call:
        client.list_artifacts()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ListArtifactsRequest()


@pytest.mark.asyncio
async def test_list_artifacts_async(
    transport: str = "grpc_asyncio", request_type=registry_service.ListArtifactsRequest
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_artifacts), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_service.ListArtifactsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_artifacts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ListArtifactsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListArtifactsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_artifacts_async_from_dict():
    await test_list_artifacts_async(request_type=dict)


def test_list_artifacts_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.ListArtifactsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_artifacts), "__call__") as call:
        call.return_value = registry_service.ListArtifactsResponse()
        client.list_artifacts(request)

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
async def test_list_artifacts_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.ListArtifactsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_artifacts), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_service.ListArtifactsResponse()
        )
        await client.list_artifacts(request)

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


def test_list_artifacts_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_artifacts), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_service.ListArtifactsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_artifacts(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_artifacts_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_artifacts(
            registry_service.ListArtifactsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_artifacts_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_artifacts), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_service.ListArtifactsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_service.ListArtifactsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_artifacts(
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
async def test_list_artifacts_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_artifacts(
            registry_service.ListArtifactsRequest(),
            parent="parent_value",
        )


def test_list_artifacts_pager(transport_name: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_artifacts), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListArtifactsResponse(
                artifacts=[
                    registry_models.Artifact(),
                    registry_models.Artifact(),
                    registry_models.Artifact(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListArtifactsResponse(
                artifacts=[],
                next_page_token="def",
            ),
            registry_service.ListArtifactsResponse(
                artifacts=[
                    registry_models.Artifact(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListArtifactsResponse(
                artifacts=[
                    registry_models.Artifact(),
                    registry_models.Artifact(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_artifacts(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, registry_models.Artifact) for i in results)


def test_list_artifacts_pages(transport_name: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_artifacts), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListArtifactsResponse(
                artifacts=[
                    registry_models.Artifact(),
                    registry_models.Artifact(),
                    registry_models.Artifact(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListArtifactsResponse(
                artifacts=[],
                next_page_token="def",
            ),
            registry_service.ListArtifactsResponse(
                artifacts=[
                    registry_models.Artifact(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListArtifactsResponse(
                artifacts=[
                    registry_models.Artifact(),
                    registry_models.Artifact(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_artifacts(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_artifacts_async_pager():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_artifacts), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListArtifactsResponse(
                artifacts=[
                    registry_models.Artifact(),
                    registry_models.Artifact(),
                    registry_models.Artifact(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListArtifactsResponse(
                artifacts=[],
                next_page_token="def",
            ),
            registry_service.ListArtifactsResponse(
                artifacts=[
                    registry_models.Artifact(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListArtifactsResponse(
                artifacts=[
                    registry_models.Artifact(),
                    registry_models.Artifact(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_artifacts(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, registry_models.Artifact) for i in responses)


@pytest.mark.asyncio
async def test_list_artifacts_async_pages():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_artifacts), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registry_service.ListArtifactsResponse(
                artifacts=[
                    registry_models.Artifact(),
                    registry_models.Artifact(),
                    registry_models.Artifact(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListArtifactsResponse(
                artifacts=[],
                next_page_token="def",
            ),
            registry_service.ListArtifactsResponse(
                artifacts=[
                    registry_models.Artifact(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListArtifactsResponse(
                artifacts=[
                    registry_models.Artifact(),
                    registry_models.Artifact(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_artifacts(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.GetArtifactRequest,
        dict,
    ],
)
def test_get_artifact(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_artifact), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.Artifact(
            name="name_value",
            mime_type="mime_type_value",
            size_bytes=1089,
            hash_="hash__value",
            contents=b"contents_blob",
        )
        response = client.get_artifact(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.GetArtifactRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.Artifact)
    assert response.name == "name_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.contents == b"contents_blob"


def test_get_artifact_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_artifact), "__call__") as call:
        client.get_artifact()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.GetArtifactRequest()


@pytest.mark.asyncio
async def test_get_artifact_async(
    transport: str = "grpc_asyncio", request_type=registry_service.GetArtifactRequest
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_artifact), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.Artifact(
                name="name_value",
                mime_type="mime_type_value",
                size_bytes=1089,
                hash_="hash__value",
                contents=b"contents_blob",
            )
        )
        response = await client.get_artifact(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.GetArtifactRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.Artifact)
    assert response.name == "name_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.contents == b"contents_blob"


@pytest.mark.asyncio
async def test_get_artifact_async_from_dict():
    await test_get_artifact_async(request_type=dict)


def test_get_artifact_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.GetArtifactRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_artifact), "__call__") as call:
        call.return_value = registry_models.Artifact()
        client.get_artifact(request)

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
async def test_get_artifact_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.GetArtifactRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_artifact), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.Artifact()
        )
        await client.get_artifact(request)

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


def test_get_artifact_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_artifact), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.Artifact()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_artifact(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_artifact_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_artifact(
            registry_service.GetArtifactRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_artifact_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_artifact), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.Artifact()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.Artifact()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_artifact(
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
async def test_get_artifact_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_artifact(
            registry_service.GetArtifactRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.GetArtifactContentsRequest,
        dict,
    ],
)
def test_get_artifact_contents(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_artifact_contents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = httpbody_pb2.HttpBody(
            content_type="content_type_value",
            data=b"data_blob",
        )
        response = client.get_artifact_contents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.GetArtifactContentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, httpbody_pb2.HttpBody)
    assert response.content_type == "content_type_value"
    assert response.data == b"data_blob"


def test_get_artifact_contents_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_artifact_contents), "__call__"
    ) as call:
        client.get_artifact_contents()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.GetArtifactContentsRequest()


@pytest.mark.asyncio
async def test_get_artifact_contents_async(
    transport: str = "grpc_asyncio",
    request_type=registry_service.GetArtifactContentsRequest,
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_artifact_contents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            httpbody_pb2.HttpBody(
                content_type="content_type_value",
                data=b"data_blob",
            )
        )
        response = await client.get_artifact_contents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.GetArtifactContentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, httpbody_pb2.HttpBody)
    assert response.content_type == "content_type_value"
    assert response.data == b"data_blob"


@pytest.mark.asyncio
async def test_get_artifact_contents_async_from_dict():
    await test_get_artifact_contents_async(request_type=dict)


def test_get_artifact_contents_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.GetArtifactContentsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_artifact_contents), "__call__"
    ) as call:
        call.return_value = httpbody_pb2.HttpBody()
        client.get_artifact_contents(request)

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
async def test_get_artifact_contents_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.GetArtifactContentsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_artifact_contents), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            httpbody_pb2.HttpBody()
        )
        await client.get_artifact_contents(request)

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


def test_get_artifact_contents_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_artifact_contents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = httpbody_pb2.HttpBody()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_artifact_contents(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_artifact_contents_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_artifact_contents(
            registry_service.GetArtifactContentsRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_artifact_contents_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_artifact_contents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = httpbody_pb2.HttpBody()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            httpbody_pb2.HttpBody()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_artifact_contents(
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
async def test_get_artifact_contents_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_artifact_contents(
            registry_service.GetArtifactContentsRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.CreateArtifactRequest,
        dict,
    ],
)
def test_create_artifact(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_artifact), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.Artifact(
            name="name_value",
            mime_type="mime_type_value",
            size_bytes=1089,
            hash_="hash__value",
            contents=b"contents_blob",
        )
        response = client.create_artifact(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.CreateArtifactRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.Artifact)
    assert response.name == "name_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.contents == b"contents_blob"


def test_create_artifact_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_artifact), "__call__") as call:
        client.create_artifact()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.CreateArtifactRequest()


@pytest.mark.asyncio
async def test_create_artifact_async(
    transport: str = "grpc_asyncio", request_type=registry_service.CreateArtifactRequest
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_artifact), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.Artifact(
                name="name_value",
                mime_type="mime_type_value",
                size_bytes=1089,
                hash_="hash__value",
                contents=b"contents_blob",
            )
        )
        response = await client.create_artifact(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.CreateArtifactRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.Artifact)
    assert response.name == "name_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.contents == b"contents_blob"


@pytest.mark.asyncio
async def test_create_artifact_async_from_dict():
    await test_create_artifact_async(request_type=dict)


def test_create_artifact_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.CreateArtifactRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_artifact), "__call__") as call:
        call.return_value = registry_models.Artifact()
        client.create_artifact(request)

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
async def test_create_artifact_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.CreateArtifactRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_artifact), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.Artifact()
        )
        await client.create_artifact(request)

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


def test_create_artifact_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_artifact), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.Artifact()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_artifact(
            parent="parent_value",
            artifact=registry_models.Artifact(name="name_value"),
            artifact_id="artifact_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].artifact
        mock_val = registry_models.Artifact(name="name_value")
        assert arg == mock_val
        arg = args[0].artifact_id
        mock_val = "artifact_id_value"
        assert arg == mock_val


def test_create_artifact_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_artifact(
            registry_service.CreateArtifactRequest(),
            parent="parent_value",
            artifact=registry_models.Artifact(name="name_value"),
            artifact_id="artifact_id_value",
        )


@pytest.mark.asyncio
async def test_create_artifact_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_artifact), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.Artifact()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.Artifact()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_artifact(
            parent="parent_value",
            artifact=registry_models.Artifact(name="name_value"),
            artifact_id="artifact_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].artifact
        mock_val = registry_models.Artifact(name="name_value")
        assert arg == mock_val
        arg = args[0].artifact_id
        mock_val = "artifact_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_artifact_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_artifact(
            registry_service.CreateArtifactRequest(),
            parent="parent_value",
            artifact=registry_models.Artifact(name="name_value"),
            artifact_id="artifact_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.ReplaceArtifactRequest,
        dict,
    ],
)
def test_replace_artifact(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.replace_artifact), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.Artifact(
            name="name_value",
            mime_type="mime_type_value",
            size_bytes=1089,
            hash_="hash__value",
            contents=b"contents_blob",
        )
        response = client.replace_artifact(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ReplaceArtifactRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.Artifact)
    assert response.name == "name_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.contents == b"contents_blob"


def test_replace_artifact_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.replace_artifact), "__call__") as call:
        client.replace_artifact()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ReplaceArtifactRequest()


@pytest.mark.asyncio
async def test_replace_artifact_async(
    transport: str = "grpc_asyncio",
    request_type=registry_service.ReplaceArtifactRequest,
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.replace_artifact), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.Artifact(
                name="name_value",
                mime_type="mime_type_value",
                size_bytes=1089,
                hash_="hash__value",
                contents=b"contents_blob",
            )
        )
        response = await client.replace_artifact(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.ReplaceArtifactRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.Artifact)
    assert response.name == "name_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.contents == b"contents_blob"


@pytest.mark.asyncio
async def test_replace_artifact_async_from_dict():
    await test_replace_artifact_async(request_type=dict)


def test_replace_artifact_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.ReplaceArtifactRequest()

    request.artifact.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.replace_artifact), "__call__") as call:
        call.return_value = registry_models.Artifact()
        client.replace_artifact(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "artifact.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_replace_artifact_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.ReplaceArtifactRequest()

    request.artifact.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.replace_artifact), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.Artifact()
        )
        await client.replace_artifact(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "artifact.name=name_value",
    ) in kw["metadata"]


def test_replace_artifact_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.replace_artifact), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.Artifact()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.replace_artifact(
            artifact=registry_models.Artifact(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].artifact
        mock_val = registry_models.Artifact(name="name_value")
        assert arg == mock_val


def test_replace_artifact_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.replace_artifact(
            registry_service.ReplaceArtifactRequest(),
            artifact=registry_models.Artifact(name="name_value"),
        )


@pytest.mark.asyncio
async def test_replace_artifact_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.replace_artifact), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registry_models.Artifact()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            registry_models.Artifact()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.replace_artifact(
            artifact=registry_models.Artifact(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].artifact
        mock_val = registry_models.Artifact(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_replace_artifact_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.replace_artifact(
            registry_service.ReplaceArtifactRequest(),
            artifact=registry_models.Artifact(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.DeleteArtifactRequest,
        dict,
    ],
)
def test_delete_artifact(request_type, transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_artifact), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_artifact(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.DeleteArtifactRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_artifact_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_artifact), "__call__") as call:
        client.delete_artifact()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.DeleteArtifactRequest()


@pytest.mark.asyncio
async def test_delete_artifact_async(
    transport: str = "grpc_asyncio", request_type=registry_service.DeleteArtifactRequest
):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_artifact), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_artifact(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == registry_service.DeleteArtifactRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_artifact_async_from_dict():
    await test_delete_artifact_async(request_type=dict)


def test_delete_artifact_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.DeleteArtifactRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_artifact), "__call__") as call:
        call.return_value = None
        client.delete_artifact(request)

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
async def test_delete_artifact_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registry_service.DeleteArtifactRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_artifact), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_artifact(request)

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


def test_delete_artifact_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_artifact), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_artifact(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_artifact_flattened_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_artifact(
            registry_service.DeleteArtifactRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_artifact_flattened_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_artifact), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_artifact(
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
async def test_delete_artifact_flattened_error_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_artifact(
            registry_service.DeleteArtifactRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.ListApisRequest,
        dict,
    ],
)
def test_list_apis_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_service.ListApisResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_service.ListApisResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_apis(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApisPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_apis_rest_required_fields(request_type=registry_service.ListApisRequest):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_apis._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_apis._get_unset_required_fields(jsonified_request)
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

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_service.ListApisResponse()
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

            pb_return_value = registry_service.ListApisResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_apis(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_apis_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_apis._get_unset_required_fields({})
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
def test_list_apis_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_list_apis"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_list_apis"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.ListApisRequest.pb(
            registry_service.ListApisRequest()
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
        req.return_value._content = registry_service.ListApisResponse.to_json(
            registry_service.ListApisResponse()
        )

        request = registry_service.ListApisRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_service.ListApisResponse()

        client.list_apis(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_apis_rest_bad_request(
    transport: str = "rest", request_type=registry_service.ListApisRequest
):
    client = RegistryClient(
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
        client.list_apis(request)


def test_list_apis_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_service.ListApisResponse()

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
        pb_return_value = registry_service.ListApisResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_apis(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/apis" % client.transport._host,
            args[1],
        )


def test_list_apis_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_apis(
            registry_service.ListApisRequest(),
            parent="parent_value",
        )


def test_list_apis_rest_pager(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            registry_service.ListApisResponse(
                apis=[
                    registry_models.Api(),
                    registry_models.Api(),
                    registry_models.Api(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApisResponse(
                apis=[],
                next_page_token="def",
            ),
            registry_service.ListApisResponse(
                apis=[
                    registry_models.Api(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApisResponse(
                apis=[
                    registry_models.Api(),
                    registry_models.Api(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(registry_service.ListApisResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_apis(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, registry_models.Api) for i in results)

        pages = list(client.list_apis(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.GetApiRequest,
        dict,
    ],
)
def test_get_api_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/apis/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.Api(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            availability="availability_value",
            recommended_version="recommended_version_value",
            recommended_deployment="recommended_deployment_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.Api.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_api(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.Api)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.availability == "availability_value"
    assert response.recommended_version == "recommended_version_value"
    assert response.recommended_deployment == "recommended_deployment_value"


def test_get_api_rest_required_fields(request_type=registry_service.GetApiRequest):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_api._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_api._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_models.Api()
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

            pb_return_value = registry_models.Api.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_api(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_api_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_api._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_api_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_get_api"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_get_api"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.GetApiRequest.pb(registry_service.GetApiRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = registry_models.Api.to_json(registry_models.Api())

        request = registry_service.GetApiRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_models.Api()

        client.get_api(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_api_rest_bad_request(
    transport: str = "rest", request_type=registry_service.GetApiRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/apis/sample3"}
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
        client.get_api(request)


def test_get_api_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.Api()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/apis/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.Api.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_api(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/apis/*}" % client.transport._host,
            args[1],
        )


def test_get_api_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_api(
            registry_service.GetApiRequest(),
            name="name_value",
        )


def test_get_api_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.CreateApiRequest,
        dict,
    ],
)
def test_create_api_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["api"] = {
        "name": "name_value",
        "display_name": "display_name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "availability": "availability_value",
        "recommended_version": "recommended_version_value",
        "recommended_deployment": "recommended_deployment_value",
        "labels": {},
        "annotations": {},
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.Api(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            availability="availability_value",
            recommended_version="recommended_version_value",
            recommended_deployment="recommended_deployment_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.Api.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_api(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.Api)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.availability == "availability_value"
    assert response.recommended_version == "recommended_version_value"
    assert response.recommended_deployment == "recommended_deployment_value"


def test_create_api_rest_required_fields(
    request_type=registry_service.CreateApiRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["api_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped
    assert "apiId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_api._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "apiId" in jsonified_request
    assert jsonified_request["apiId"] == request_init["api_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["apiId"] = "api_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_api._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("api_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "apiId" in jsonified_request
    assert jsonified_request["apiId"] == "api_id_value"

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_models.Api()
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

            pb_return_value = registry_models.Api.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_api(request)

            expected_params = [
                (
                    "apiId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_api_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_api._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("apiId",))
        & set(
            (
                "parent",
                "api",
                "apiId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_api_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_create_api"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_create_api"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.CreateApiRequest.pb(
            registry_service.CreateApiRequest()
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
        req.return_value._content = registry_models.Api.to_json(registry_models.Api())

        request = registry_service.CreateApiRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_models.Api()

        client.create_api(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_api_rest_bad_request(
    transport: str = "rest", request_type=registry_service.CreateApiRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["api"] = {
        "name": "name_value",
        "display_name": "display_name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "availability": "availability_value",
        "recommended_version": "recommended_version_value",
        "recommended_deployment": "recommended_deployment_value",
        "labels": {},
        "annotations": {},
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
        client.create_api(request)


def test_create_api_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.Api()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            api=registry_models.Api(name="name_value"),
            api_id="api_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.Api.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_api(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/apis" % client.transport._host,
            args[1],
        )


def test_create_api_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_api(
            registry_service.CreateApiRequest(),
            parent="parent_value",
            api=registry_models.Api(name="name_value"),
            api_id="api_id_value",
        )


def test_create_api_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.UpdateApiRequest,
        dict,
    ],
)
def test_update_api_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"api": {"name": "projects/sample1/locations/sample2/apis/sample3"}}
    request_init["api"] = {
        "name": "projects/sample1/locations/sample2/apis/sample3",
        "display_name": "display_name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "availability": "availability_value",
        "recommended_version": "recommended_version_value",
        "recommended_deployment": "recommended_deployment_value",
        "labels": {},
        "annotations": {},
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.Api(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            availability="availability_value",
            recommended_version="recommended_version_value",
            recommended_deployment="recommended_deployment_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.Api.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_api(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.Api)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.availability == "availability_value"
    assert response.recommended_version == "recommended_version_value"
    assert response.recommended_deployment == "recommended_deployment_value"


def test_update_api_rest_required_fields(
    request_type=registry_service.UpdateApiRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_api._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_api._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "allow_missing",
            "update_mask",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_models.Api()
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

            pb_return_value = registry_models.Api.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_api(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_api_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_api._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "allowMissing",
                "updateMask",
            )
        )
        & set(("api",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_api_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_update_api"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_update_api"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.UpdateApiRequest.pb(
            registry_service.UpdateApiRequest()
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
        req.return_value._content = registry_models.Api.to_json(registry_models.Api())

        request = registry_service.UpdateApiRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_models.Api()

        client.update_api(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_api_rest_bad_request(
    transport: str = "rest", request_type=registry_service.UpdateApiRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"api": {"name": "projects/sample1/locations/sample2/apis/sample3"}}
    request_init["api"] = {
        "name": "projects/sample1/locations/sample2/apis/sample3",
        "display_name": "display_name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "availability": "availability_value",
        "recommended_version": "recommended_version_value",
        "recommended_deployment": "recommended_deployment_value",
        "labels": {},
        "annotations": {},
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
        client.update_api(request)


def test_update_api_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.Api()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "api": {"name": "projects/sample1/locations/sample2/apis/sample3"}
        }

        # get truthy value for each flattened field
        mock_args = dict(
            api=registry_models.Api(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.Api.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_api(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{api.name=projects/*/locations/*/apis/*}" % client.transport._host,
            args[1],
        )


def test_update_api_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_api(
            registry_service.UpdateApiRequest(),
            api=registry_models.Api(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_api_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.DeleteApiRequest,
        dict,
    ],
)
def test_delete_api_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/apis/sample3"}
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
        response = client.delete_api(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_api_rest_required_fields(
    request_type=registry_service.DeleteApiRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_api._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_api._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("force",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RegistryClient(
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

            response = client.delete_api(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_api_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_api._get_unset_required_fields({})
    assert set(unset_fields) == (set(("force",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_api_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_delete_api"
    ) as pre:
        pre.assert_not_called()
        pb_message = registry_service.DeleteApiRequest.pb(
            registry_service.DeleteApiRequest()
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

        request = registry_service.DeleteApiRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_api(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_api_rest_bad_request(
    transport: str = "rest", request_type=registry_service.DeleteApiRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/apis/sample3"}
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
        client.delete_api(request)


def test_delete_api_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/apis/sample3"}

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

        client.delete_api(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/apis/*}" % client.transport._host,
            args[1],
        )


def test_delete_api_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_api(
            registry_service.DeleteApiRequest(),
            name="name_value",
        )


def test_delete_api_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.ListApiVersionsRequest,
        dict,
    ],
)
def test_list_api_versions_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/apis/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_service.ListApiVersionsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_service.ListApiVersionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_api_versions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApiVersionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_api_versions_rest_required_fields(
    request_type=registry_service.ListApiVersionsRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_api_versions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_api_versions._get_unset_required_fields(jsonified_request)
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

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_service.ListApiVersionsResponse()
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

            pb_return_value = registry_service.ListApiVersionsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_api_versions(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_api_versions_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_api_versions._get_unset_required_fields({})
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
def test_list_api_versions_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_list_api_versions"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_list_api_versions"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.ListApiVersionsRequest.pb(
            registry_service.ListApiVersionsRequest()
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
        req.return_value._content = registry_service.ListApiVersionsResponse.to_json(
            registry_service.ListApiVersionsResponse()
        )

        request = registry_service.ListApiVersionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_service.ListApiVersionsResponse()

        client.list_api_versions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_api_versions_rest_bad_request(
    transport: str = "rest", request_type=registry_service.ListApiVersionsRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/apis/sample3"}
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
        client.list_api_versions(request)


def test_list_api_versions_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_service.ListApiVersionsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2/apis/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_service.ListApiVersionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_api_versions(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/apis/*}/versions"
            % client.transport._host,
            args[1],
        )


def test_list_api_versions_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_api_versions(
            registry_service.ListApiVersionsRequest(),
            parent="parent_value",
        )


def test_list_api_versions_rest_pager(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            registry_service.ListApiVersionsResponse(
                api_versions=[
                    registry_models.ApiVersion(),
                    registry_models.ApiVersion(),
                    registry_models.ApiVersion(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiVersionsResponse(
                api_versions=[],
                next_page_token="def",
            ),
            registry_service.ListApiVersionsResponse(
                api_versions=[
                    registry_models.ApiVersion(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiVersionsResponse(
                api_versions=[
                    registry_models.ApiVersion(),
                    registry_models.ApiVersion(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            registry_service.ListApiVersionsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2/apis/sample3"}

        pager = client.list_api_versions(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, registry_models.ApiVersion) for i in results)

        pages = list(client.list_api_versions(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.GetApiVersionRequest,
        dict,
    ],
)
def test_get_api_version_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiVersion(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            state="state_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiVersion.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_api_version(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiVersion)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.state == "state_value"


def test_get_api_version_rest_required_fields(
    request_type=registry_service.GetApiVersionRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_api_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_api_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_models.ApiVersion()
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

            pb_return_value = registry_models.ApiVersion.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_api_version(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_api_version_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_api_version._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_api_version_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_get_api_version"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_get_api_version"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.GetApiVersionRequest.pb(
            registry_service.GetApiVersionRequest()
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
        req.return_value._content = registry_models.ApiVersion.to_json(
            registry_models.ApiVersion()
        )

        request = registry_service.GetApiVersionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_models.ApiVersion()

        client.get_api_version(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_api_version_rest_bad_request(
    transport: str = "rest", request_type=registry_service.GetApiVersionRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4"
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
        client.get_api_version(request)


def test_get_api_version_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiVersion()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiVersion.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_api_version(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/apis/*/versions/*}"
            % client.transport._host,
            args[1],
        )


def test_get_api_version_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_api_version(
            registry_service.GetApiVersionRequest(),
            name="name_value",
        )


def test_get_api_version_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.CreateApiVersionRequest,
        dict,
    ],
)
def test_create_api_version_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/apis/sample3"}
    request_init["api_version"] = {
        "name": "name_value",
        "display_name": "display_name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "state": "state_value",
        "labels": {},
        "annotations": {},
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiVersion(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            state="state_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiVersion.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_api_version(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiVersion)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.state == "state_value"


def test_create_api_version_rest_required_fields(
    request_type=registry_service.CreateApiVersionRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["api_version_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped
    assert "apiVersionId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_api_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "apiVersionId" in jsonified_request
    assert jsonified_request["apiVersionId"] == request_init["api_version_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["apiVersionId"] = "api_version_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_api_version._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("api_version_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "apiVersionId" in jsonified_request
    assert jsonified_request["apiVersionId"] == "api_version_id_value"

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_models.ApiVersion()
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

            pb_return_value = registry_models.ApiVersion.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_api_version(request)

            expected_params = [
                (
                    "apiVersionId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_api_version_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_api_version._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("apiVersionId",))
        & set(
            (
                "parent",
                "apiVersion",
                "apiVersionId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_api_version_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_create_api_version"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_create_api_version"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.CreateApiVersionRequest.pb(
            registry_service.CreateApiVersionRequest()
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
        req.return_value._content = registry_models.ApiVersion.to_json(
            registry_models.ApiVersion()
        )

        request = registry_service.CreateApiVersionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_models.ApiVersion()

        client.create_api_version(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_api_version_rest_bad_request(
    transport: str = "rest", request_type=registry_service.CreateApiVersionRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/apis/sample3"}
    request_init["api_version"] = {
        "name": "name_value",
        "display_name": "display_name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "state": "state_value",
        "labels": {},
        "annotations": {},
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
        client.create_api_version(request)


def test_create_api_version_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiVersion()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2/apis/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            api_version=registry_models.ApiVersion(name="name_value"),
            api_version_id="api_version_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiVersion.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_api_version(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/apis/*}/versions"
            % client.transport._host,
            args[1],
        )


def test_create_api_version_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_api_version(
            registry_service.CreateApiVersionRequest(),
            parent="parent_value",
            api_version=registry_models.ApiVersion(name="name_value"),
            api_version_id="api_version_id_value",
        )


def test_create_api_version_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.UpdateApiVersionRequest,
        dict,
    ],
)
def test_update_api_version_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "api_version": {
            "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4"
        }
    }
    request_init["api_version"] = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4",
        "display_name": "display_name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "state": "state_value",
        "labels": {},
        "annotations": {},
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiVersion(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            state="state_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiVersion.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_api_version(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiVersion)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.state == "state_value"


def test_update_api_version_rest_required_fields(
    request_type=registry_service.UpdateApiVersionRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_api_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_api_version._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "allow_missing",
            "update_mask",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_models.ApiVersion()
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

            pb_return_value = registry_models.ApiVersion.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_api_version(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_api_version_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_api_version._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "allowMissing",
                "updateMask",
            )
        )
        & set(("apiVersion",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_api_version_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_update_api_version"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_update_api_version"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.UpdateApiVersionRequest.pb(
            registry_service.UpdateApiVersionRequest()
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
        req.return_value._content = registry_models.ApiVersion.to_json(
            registry_models.ApiVersion()
        )

        request = registry_service.UpdateApiVersionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_models.ApiVersion()

        client.update_api_version(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_api_version_rest_bad_request(
    transport: str = "rest", request_type=registry_service.UpdateApiVersionRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "api_version": {
            "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4"
        }
    }
    request_init["api_version"] = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4",
        "display_name": "display_name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "state": "state_value",
        "labels": {},
        "annotations": {},
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
        client.update_api_version(request)


def test_update_api_version_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiVersion()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "api_version": {
                "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            api_version=registry_models.ApiVersion(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiVersion.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_api_version(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{api_version.name=projects/*/locations/*/apis/*/versions/*}"
            % client.transport._host,
            args[1],
        )


def test_update_api_version_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_api_version(
            registry_service.UpdateApiVersionRequest(),
            api_version=registry_models.ApiVersion(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_api_version_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.DeleteApiVersionRequest,
        dict,
    ],
)
def test_delete_api_version_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4"
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
        response = client.delete_api_version(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_api_version_rest_required_fields(
    request_type=registry_service.DeleteApiVersionRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_api_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_api_version._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("force",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RegistryClient(
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

            response = client.delete_api_version(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_api_version_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_api_version._get_unset_required_fields({})
    assert set(unset_fields) == (set(("force",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_api_version_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_delete_api_version"
    ) as pre:
        pre.assert_not_called()
        pb_message = registry_service.DeleteApiVersionRequest.pb(
            registry_service.DeleteApiVersionRequest()
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

        request = registry_service.DeleteApiVersionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_api_version(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_api_version_rest_bad_request(
    transport: str = "rest", request_type=registry_service.DeleteApiVersionRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4"
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
        client.delete_api_version(request)


def test_delete_api_version_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4"
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

        client.delete_api_version(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/apis/*/versions/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_api_version_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_api_version(
            registry_service.DeleteApiVersionRequest(),
            name="name_value",
        )


def test_delete_api_version_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.ListApiSpecsRequest,
        dict,
    ],
)
def test_list_api_specs_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/apis/sample3/versions/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_service.ListApiSpecsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_service.ListApiSpecsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_api_specs(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApiSpecsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_api_specs_rest_required_fields(
    request_type=registry_service.ListApiSpecsRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_api_specs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_api_specs._get_unset_required_fields(jsonified_request)
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

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_service.ListApiSpecsResponse()
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

            pb_return_value = registry_service.ListApiSpecsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_api_specs(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_api_specs_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_api_specs._get_unset_required_fields({})
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
def test_list_api_specs_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_list_api_specs"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_list_api_specs"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.ListApiSpecsRequest.pb(
            registry_service.ListApiSpecsRequest()
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
        req.return_value._content = registry_service.ListApiSpecsResponse.to_json(
            registry_service.ListApiSpecsResponse()
        )

        request = registry_service.ListApiSpecsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_service.ListApiSpecsResponse()

        client.list_api_specs(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_api_specs_rest_bad_request(
    transport: str = "rest", request_type=registry_service.ListApiSpecsRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/apis/sample3/versions/sample4"
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
        client.list_api_specs(request)


def test_list_api_specs_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_service.ListApiSpecsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/apis/sample3/versions/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_service.ListApiSpecsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_api_specs(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/apis/*/versions/*}/specs"
            % client.transport._host,
            args[1],
        )


def test_list_api_specs_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_api_specs(
            registry_service.ListApiSpecsRequest(),
            parent="parent_value",
        )


def test_list_api_specs_rest_pager(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            registry_service.ListApiSpecsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiSpecsResponse(
                api_specs=[],
                next_page_token="def",
            ),
            registry_service.ListApiSpecsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiSpecsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            registry_service.ListApiSpecsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/apis/sample3/versions/sample4"
        }

        pager = client.list_api_specs(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, registry_models.ApiSpec) for i in results)

        pages = list(client.list_api_specs(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.GetApiSpecRequest,
        dict,
    ],
)
def test_get_api_spec_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiSpec(
            name="name_value",
            filename="filename_value",
            description="description_value",
            revision_id="revision_id_value",
            mime_type="mime_type_value",
            size_bytes=1089,
            hash_="hash__value",
            source_uri="source_uri_value",
            contents=b"contents_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiSpec.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_api_spec(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiSpec)
    assert response.name == "name_value"
    assert response.filename == "filename_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.source_uri == "source_uri_value"
    assert response.contents == b"contents_blob"


def test_get_api_spec_rest_required_fields(
    request_type=registry_service.GetApiSpecRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_api_spec._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_api_spec._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_models.ApiSpec()
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

            pb_return_value = registry_models.ApiSpec.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_api_spec(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_api_spec_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_api_spec._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_api_spec_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_get_api_spec"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_get_api_spec"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.GetApiSpecRequest.pb(
            registry_service.GetApiSpecRequest()
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
        req.return_value._content = registry_models.ApiSpec.to_json(
            registry_models.ApiSpec()
        )

        request = registry_service.GetApiSpecRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_models.ApiSpec()

        client.get_api_spec(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_api_spec_rest_bad_request(
    transport: str = "rest", request_type=registry_service.GetApiSpecRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
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
        client.get_api_spec(request)


def test_get_api_spec_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiSpec()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiSpec.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_api_spec(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/apis/*/versions/*/specs/*}"
            % client.transport._host,
            args[1],
        )


def test_get_api_spec_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_api_spec(
            registry_service.GetApiSpecRequest(),
            name="name_value",
        )


def test_get_api_spec_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.GetApiSpecContentsRequest,
        dict,
    ],
)
def test_get_api_spec_contents_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = httpbody_pb2.HttpBody(
            content_type="content_type_value",
            data=b"data_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = return_value
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_api_spec_contents(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, httpbody_pb2.HttpBody)
    assert response.content_type == "content_type_value"
    assert response.data == b"data_blob"


def test_get_api_spec_contents_rest_required_fields(
    request_type=registry_service.GetApiSpecContentsRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_api_spec_contents._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_api_spec_contents._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = httpbody_pb2.HttpBody()
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

            pb_return_value = return_value
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_api_spec_contents(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_api_spec_contents_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_api_spec_contents._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_api_spec_contents_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_get_api_spec_contents"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_get_api_spec_contents"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.GetApiSpecContentsRequest.pb(
            registry_service.GetApiSpecContentsRequest()
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
        req.return_value._content = json_format.MessageToJson(httpbody_pb2.HttpBody())

        request = registry_service.GetApiSpecContentsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = httpbody_pb2.HttpBody()

        client.get_api_spec_contents(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_api_spec_contents_rest_bad_request(
    transport: str = "rest", request_type=registry_service.GetApiSpecContentsRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
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
        client.get_api_spec_contents(request)


def test_get_api_spec_contents_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = httpbody_pb2.HttpBody()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = return_value
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_api_spec_contents(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/apis/*/versions/*/specs/*}:getContents"
            % client.transport._host,
            args[1],
        )


def test_get_api_spec_contents_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_api_spec_contents(
            registry_service.GetApiSpecContentsRequest(),
            name="name_value",
        )


def test_get_api_spec_contents_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.CreateApiSpecRequest,
        dict,
    ],
)
def test_create_api_spec_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/apis/sample3/versions/sample4"
    }
    request_init["api_spec"] = {
        "name": "name_value",
        "filename": "filename_value",
        "description": "description_value",
        "revision_id": "revision_id_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "revision_create_time": {},
        "revision_update_time": {},
        "mime_type": "mime_type_value",
        "size_bytes": 1089,
        "hash_": "hash__value",
        "source_uri": "source_uri_value",
        "contents": b"contents_blob",
        "labels": {},
        "annotations": {},
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiSpec(
            name="name_value",
            filename="filename_value",
            description="description_value",
            revision_id="revision_id_value",
            mime_type="mime_type_value",
            size_bytes=1089,
            hash_="hash__value",
            source_uri="source_uri_value",
            contents=b"contents_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiSpec.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_api_spec(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiSpec)
    assert response.name == "name_value"
    assert response.filename == "filename_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.source_uri == "source_uri_value"
    assert response.contents == b"contents_blob"


def test_create_api_spec_rest_required_fields(
    request_type=registry_service.CreateApiSpecRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["api_spec_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped
    assert "apiSpecId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_api_spec._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "apiSpecId" in jsonified_request
    assert jsonified_request["apiSpecId"] == request_init["api_spec_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["apiSpecId"] = "api_spec_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_api_spec._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("api_spec_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "apiSpecId" in jsonified_request
    assert jsonified_request["apiSpecId"] == "api_spec_id_value"

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_models.ApiSpec()
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

            pb_return_value = registry_models.ApiSpec.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_api_spec(request)

            expected_params = [
                (
                    "apiSpecId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_api_spec_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_api_spec._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("apiSpecId",))
        & set(
            (
                "parent",
                "apiSpec",
                "apiSpecId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_api_spec_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_create_api_spec"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_create_api_spec"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.CreateApiSpecRequest.pb(
            registry_service.CreateApiSpecRequest()
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
        req.return_value._content = registry_models.ApiSpec.to_json(
            registry_models.ApiSpec()
        )

        request = registry_service.CreateApiSpecRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_models.ApiSpec()

        client.create_api_spec(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_api_spec_rest_bad_request(
    transport: str = "rest", request_type=registry_service.CreateApiSpecRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/apis/sample3/versions/sample4"
    }
    request_init["api_spec"] = {
        "name": "name_value",
        "filename": "filename_value",
        "description": "description_value",
        "revision_id": "revision_id_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "revision_create_time": {},
        "revision_update_time": {},
        "mime_type": "mime_type_value",
        "size_bytes": 1089,
        "hash_": "hash__value",
        "source_uri": "source_uri_value",
        "contents": b"contents_blob",
        "labels": {},
        "annotations": {},
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
        client.create_api_spec(request)


def test_create_api_spec_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiSpec()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/apis/sample3/versions/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            api_spec=registry_models.ApiSpec(name="name_value"),
            api_spec_id="api_spec_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiSpec.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_api_spec(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/apis/*/versions/*}/specs"
            % client.transport._host,
            args[1],
        )


def test_create_api_spec_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_api_spec(
            registry_service.CreateApiSpecRequest(),
            parent="parent_value",
            api_spec=registry_models.ApiSpec(name="name_value"),
            api_spec_id="api_spec_id_value",
        )


def test_create_api_spec_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.UpdateApiSpecRequest,
        dict,
    ],
)
def test_update_api_spec_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "api_spec": {
            "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
        }
    }
    request_init["api_spec"] = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5",
        "filename": "filename_value",
        "description": "description_value",
        "revision_id": "revision_id_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "revision_create_time": {},
        "revision_update_time": {},
        "mime_type": "mime_type_value",
        "size_bytes": 1089,
        "hash_": "hash__value",
        "source_uri": "source_uri_value",
        "contents": b"contents_blob",
        "labels": {},
        "annotations": {},
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiSpec(
            name="name_value",
            filename="filename_value",
            description="description_value",
            revision_id="revision_id_value",
            mime_type="mime_type_value",
            size_bytes=1089,
            hash_="hash__value",
            source_uri="source_uri_value",
            contents=b"contents_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiSpec.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_api_spec(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiSpec)
    assert response.name == "name_value"
    assert response.filename == "filename_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.source_uri == "source_uri_value"
    assert response.contents == b"contents_blob"


def test_update_api_spec_rest_required_fields(
    request_type=registry_service.UpdateApiSpecRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_api_spec._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_api_spec._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "allow_missing",
            "update_mask",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_models.ApiSpec()
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

            pb_return_value = registry_models.ApiSpec.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_api_spec(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_api_spec_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_api_spec._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "allowMissing",
                "updateMask",
            )
        )
        & set(("apiSpec",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_api_spec_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_update_api_spec"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_update_api_spec"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.UpdateApiSpecRequest.pb(
            registry_service.UpdateApiSpecRequest()
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
        req.return_value._content = registry_models.ApiSpec.to_json(
            registry_models.ApiSpec()
        )

        request = registry_service.UpdateApiSpecRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_models.ApiSpec()

        client.update_api_spec(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_api_spec_rest_bad_request(
    transport: str = "rest", request_type=registry_service.UpdateApiSpecRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "api_spec": {
            "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
        }
    }
    request_init["api_spec"] = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5",
        "filename": "filename_value",
        "description": "description_value",
        "revision_id": "revision_id_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "revision_create_time": {},
        "revision_update_time": {},
        "mime_type": "mime_type_value",
        "size_bytes": 1089,
        "hash_": "hash__value",
        "source_uri": "source_uri_value",
        "contents": b"contents_blob",
        "labels": {},
        "annotations": {},
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
        client.update_api_spec(request)


def test_update_api_spec_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiSpec()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "api_spec": {
                "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            api_spec=registry_models.ApiSpec(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiSpec.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_api_spec(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{api_spec.name=projects/*/locations/*/apis/*/versions/*/specs/*}"
            % client.transport._host,
            args[1],
        )


def test_update_api_spec_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_api_spec(
            registry_service.UpdateApiSpecRequest(),
            api_spec=registry_models.ApiSpec(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_api_spec_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.DeleteApiSpecRequest,
        dict,
    ],
)
def test_delete_api_spec_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
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
        response = client.delete_api_spec(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_api_spec_rest_required_fields(
    request_type=registry_service.DeleteApiSpecRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_api_spec._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_api_spec._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("force",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RegistryClient(
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

            response = client.delete_api_spec(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_api_spec_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_api_spec._get_unset_required_fields({})
    assert set(unset_fields) == (set(("force",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_api_spec_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_delete_api_spec"
    ) as pre:
        pre.assert_not_called()
        pb_message = registry_service.DeleteApiSpecRequest.pb(
            registry_service.DeleteApiSpecRequest()
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

        request = registry_service.DeleteApiSpecRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_api_spec(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_api_spec_rest_bad_request(
    transport: str = "rest", request_type=registry_service.DeleteApiSpecRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
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
        client.delete_api_spec(request)


def test_delete_api_spec_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
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

        client.delete_api_spec(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/apis/*/versions/*/specs/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_api_spec_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_api_spec(
            registry_service.DeleteApiSpecRequest(),
            name="name_value",
        )


def test_delete_api_spec_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.TagApiSpecRevisionRequest,
        dict,
    ],
)
def test_tag_api_spec_revision_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiSpec(
            name="name_value",
            filename="filename_value",
            description="description_value",
            revision_id="revision_id_value",
            mime_type="mime_type_value",
            size_bytes=1089,
            hash_="hash__value",
            source_uri="source_uri_value",
            contents=b"contents_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiSpec.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.tag_api_spec_revision(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiSpec)
    assert response.name == "name_value"
    assert response.filename == "filename_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.source_uri == "source_uri_value"
    assert response.contents == b"contents_blob"


def test_tag_api_spec_revision_rest_required_fields(
    request_type=registry_service.TagApiSpecRevisionRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["tag"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).tag_api_spec_revision._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"
    jsonified_request["tag"] = "tag_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).tag_api_spec_revision._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"
    assert "tag" in jsonified_request
    assert jsonified_request["tag"] == "tag_value"

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_models.ApiSpec()
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

            pb_return_value = registry_models.ApiSpec.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.tag_api_spec_revision(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_tag_api_spec_revision_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.tag_api_spec_revision._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "tag",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_tag_api_spec_revision_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_tag_api_spec_revision"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_tag_api_spec_revision"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.TagApiSpecRevisionRequest.pb(
            registry_service.TagApiSpecRevisionRequest()
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
        req.return_value._content = registry_models.ApiSpec.to_json(
            registry_models.ApiSpec()
        )

        request = registry_service.TagApiSpecRevisionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_models.ApiSpec()

        client.tag_api_spec_revision(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_tag_api_spec_revision_rest_bad_request(
    transport: str = "rest", request_type=registry_service.TagApiSpecRevisionRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
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
        client.tag_api_spec_revision(request)


def test_tag_api_spec_revision_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.ListApiSpecRevisionsRequest,
        dict,
    ],
)
def test_list_api_spec_revisions_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_service.ListApiSpecRevisionsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_service.ListApiSpecRevisionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_api_spec_revisions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApiSpecRevisionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_api_spec_revisions_rest_required_fields(
    request_type=registry_service.ListApiSpecRevisionsRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_api_spec_revisions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_api_spec_revisions._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_service.ListApiSpecRevisionsResponse()
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

            pb_return_value = registry_service.ListApiSpecRevisionsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_api_spec_revisions(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_api_spec_revisions_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_api_spec_revisions._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("name",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_api_spec_revisions_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_list_api_spec_revisions"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_list_api_spec_revisions"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.ListApiSpecRevisionsRequest.pb(
            registry_service.ListApiSpecRevisionsRequest()
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
            registry_service.ListApiSpecRevisionsResponse.to_json(
                registry_service.ListApiSpecRevisionsResponse()
            )
        )

        request = registry_service.ListApiSpecRevisionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_service.ListApiSpecRevisionsResponse()

        client.list_api_spec_revisions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_api_spec_revisions_rest_bad_request(
    transport: str = "rest", request_type=registry_service.ListApiSpecRevisionsRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
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
        client.list_api_spec_revisions(request)


def test_list_api_spec_revisions_rest_pager(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            registry_service.ListApiSpecRevisionsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiSpecRevisionsResponse(
                api_specs=[],
                next_page_token="def",
            ),
            registry_service.ListApiSpecRevisionsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiSpecRevisionsResponse(
                api_specs=[
                    registry_models.ApiSpec(),
                    registry_models.ApiSpec(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            registry_service.ListApiSpecRevisionsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
        }

        pager = client.list_api_spec_revisions(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, registry_models.ApiSpec) for i in results)

        pages = list(client.list_api_spec_revisions(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.RollbackApiSpecRequest,
        dict,
    ],
)
def test_rollback_api_spec_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiSpec(
            name="name_value",
            filename="filename_value",
            description="description_value",
            revision_id="revision_id_value",
            mime_type="mime_type_value",
            size_bytes=1089,
            hash_="hash__value",
            source_uri="source_uri_value",
            contents=b"contents_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiSpec.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.rollback_api_spec(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiSpec)
    assert response.name == "name_value"
    assert response.filename == "filename_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.source_uri == "source_uri_value"
    assert response.contents == b"contents_blob"


def test_rollback_api_spec_rest_required_fields(
    request_type=registry_service.RollbackApiSpecRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["revision_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).rollback_api_spec._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"
    jsonified_request["revisionId"] = "revision_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).rollback_api_spec._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"
    assert "revisionId" in jsonified_request
    assert jsonified_request["revisionId"] == "revision_id_value"

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_models.ApiSpec()
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

            pb_return_value = registry_models.ApiSpec.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.rollback_api_spec(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_rollback_api_spec_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.rollback_api_spec._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "revisionId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_rollback_api_spec_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_rollback_api_spec"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_rollback_api_spec"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.RollbackApiSpecRequest.pb(
            registry_service.RollbackApiSpecRequest()
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
        req.return_value._content = registry_models.ApiSpec.to_json(
            registry_models.ApiSpec()
        )

        request = registry_service.RollbackApiSpecRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_models.ApiSpec()

        client.rollback_api_spec(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_rollback_api_spec_rest_bad_request(
    transport: str = "rest", request_type=registry_service.RollbackApiSpecRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
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
        client.rollback_api_spec(request)


def test_rollback_api_spec_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.DeleteApiSpecRevisionRequest,
        dict,
    ],
)
def test_delete_api_spec_revision_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiSpec(
            name="name_value",
            filename="filename_value",
            description="description_value",
            revision_id="revision_id_value",
            mime_type="mime_type_value",
            size_bytes=1089,
            hash_="hash__value",
            source_uri="source_uri_value",
            contents=b"contents_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiSpec.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_api_spec_revision(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiSpec)
    assert response.name == "name_value"
    assert response.filename == "filename_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.source_uri == "source_uri_value"
    assert response.contents == b"contents_blob"


def test_delete_api_spec_revision_rest_required_fields(
    request_type=registry_service.DeleteApiSpecRevisionRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_api_spec_revision._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_api_spec_revision._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_models.ApiSpec()
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

            pb_return_value = registry_models.ApiSpec.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_api_spec_revision(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_api_spec_revision_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_api_spec_revision._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_api_spec_revision_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_delete_api_spec_revision"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_delete_api_spec_revision"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.DeleteApiSpecRevisionRequest.pb(
            registry_service.DeleteApiSpecRevisionRequest()
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
        req.return_value._content = registry_models.ApiSpec.to_json(
            registry_models.ApiSpec()
        )

        request = registry_service.DeleteApiSpecRevisionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_models.ApiSpec()

        client.delete_api_spec_revision(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_api_spec_revision_rest_bad_request(
    transport: str = "rest", request_type=registry_service.DeleteApiSpecRevisionRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
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
        client.delete_api_spec_revision(request)


def test_delete_api_spec_revision_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiSpec()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/apis/sample3/versions/sample4/specs/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiSpec.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_api_spec_revision(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/apis/*/versions/*/specs/*}:deleteRevision"
            % client.transport._host,
            args[1],
        )


def test_delete_api_spec_revision_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_api_spec_revision(
            registry_service.DeleteApiSpecRevisionRequest(),
            name="name_value",
        )


def test_delete_api_spec_revision_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.ListApiDeploymentsRequest,
        dict,
    ],
)
def test_list_api_deployments_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/apis/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_service.ListApiDeploymentsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_service.ListApiDeploymentsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_api_deployments(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApiDeploymentsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_api_deployments_rest_required_fields(
    request_type=registry_service.ListApiDeploymentsRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_api_deployments._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_api_deployments._get_unset_required_fields(jsonified_request)
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

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_service.ListApiDeploymentsResponse()
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

            pb_return_value = registry_service.ListApiDeploymentsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_api_deployments(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_api_deployments_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_api_deployments._get_unset_required_fields({})
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
def test_list_api_deployments_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_list_api_deployments"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_list_api_deployments"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.ListApiDeploymentsRequest.pb(
            registry_service.ListApiDeploymentsRequest()
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
        req.return_value._content = registry_service.ListApiDeploymentsResponse.to_json(
            registry_service.ListApiDeploymentsResponse()
        )

        request = registry_service.ListApiDeploymentsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_service.ListApiDeploymentsResponse()

        client.list_api_deployments(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_api_deployments_rest_bad_request(
    transport: str = "rest", request_type=registry_service.ListApiDeploymentsRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/apis/sample3"}
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
        client.list_api_deployments(request)


def test_list_api_deployments_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_service.ListApiDeploymentsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2/apis/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_service.ListApiDeploymentsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_api_deployments(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/apis/*}/deployments"
            % client.transport._host,
            args[1],
        )


def test_list_api_deployments_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_api_deployments(
            registry_service.ListApiDeploymentsRequest(),
            parent="parent_value",
        )


def test_list_api_deployments_rest_pager(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            registry_service.ListApiDeploymentsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiDeploymentsResponse(
                api_deployments=[],
                next_page_token="def",
            ),
            registry_service.ListApiDeploymentsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiDeploymentsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            registry_service.ListApiDeploymentsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2/apis/sample3"}

        pager = client.list_api_deployments(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, registry_models.ApiDeployment) for i in results)

        pages = list(client.list_api_deployments(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.GetApiDeploymentRequest,
        dict,
    ],
)
def test_get_api_deployment_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/deployments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiDeployment(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            revision_id="revision_id_value",
            api_spec_revision="api_spec_revision_value",
            endpoint_uri="endpoint_uri_value",
            external_channel_uri="external_channel_uri_value",
            intended_audience="intended_audience_value",
            access_guidance="access_guidance_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiDeployment.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_api_deployment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiDeployment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.api_spec_revision == "api_spec_revision_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.external_channel_uri == "external_channel_uri_value"
    assert response.intended_audience == "intended_audience_value"
    assert response.access_guidance == "access_guidance_value"


def test_get_api_deployment_rest_required_fields(
    request_type=registry_service.GetApiDeploymentRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_api_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_api_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_models.ApiDeployment()
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

            pb_return_value = registry_models.ApiDeployment.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_api_deployment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_api_deployment_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_api_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_api_deployment_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_get_api_deployment"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_get_api_deployment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.GetApiDeploymentRequest.pb(
            registry_service.GetApiDeploymentRequest()
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
        req.return_value._content = registry_models.ApiDeployment.to_json(
            registry_models.ApiDeployment()
        )

        request = registry_service.GetApiDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_models.ApiDeployment()

        client.get_api_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_api_deployment_rest_bad_request(
    transport: str = "rest", request_type=registry_service.GetApiDeploymentRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/deployments/sample4"
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
        client.get_api_deployment(request)


def test_get_api_deployment_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiDeployment()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/apis/sample3/deployments/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiDeployment.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_api_deployment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/apis/*/deployments/*}"
            % client.transport._host,
            args[1],
        )


def test_get_api_deployment_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_api_deployment(
            registry_service.GetApiDeploymentRequest(),
            name="name_value",
        )


def test_get_api_deployment_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.CreateApiDeploymentRequest,
        dict,
    ],
)
def test_create_api_deployment_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/apis/sample3"}
    request_init["api_deployment"] = {
        "name": "name_value",
        "display_name": "display_name_value",
        "description": "description_value",
        "revision_id": "revision_id_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "revision_create_time": {},
        "revision_update_time": {},
        "api_spec_revision": "api_spec_revision_value",
        "endpoint_uri": "endpoint_uri_value",
        "external_channel_uri": "external_channel_uri_value",
        "intended_audience": "intended_audience_value",
        "access_guidance": "access_guidance_value",
        "labels": {},
        "annotations": {},
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiDeployment(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            revision_id="revision_id_value",
            api_spec_revision="api_spec_revision_value",
            endpoint_uri="endpoint_uri_value",
            external_channel_uri="external_channel_uri_value",
            intended_audience="intended_audience_value",
            access_guidance="access_guidance_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiDeployment.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_api_deployment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiDeployment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.api_spec_revision == "api_spec_revision_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.external_channel_uri == "external_channel_uri_value"
    assert response.intended_audience == "intended_audience_value"
    assert response.access_guidance == "access_guidance_value"


def test_create_api_deployment_rest_required_fields(
    request_type=registry_service.CreateApiDeploymentRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["api_deployment_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped
    assert "apiDeploymentId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_api_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "apiDeploymentId" in jsonified_request
    assert jsonified_request["apiDeploymentId"] == request_init["api_deployment_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["apiDeploymentId"] = "api_deployment_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_api_deployment._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("api_deployment_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "apiDeploymentId" in jsonified_request
    assert jsonified_request["apiDeploymentId"] == "api_deployment_id_value"

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_models.ApiDeployment()
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

            pb_return_value = registry_models.ApiDeployment.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_api_deployment(request)

            expected_params = [
                (
                    "apiDeploymentId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_api_deployment_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_api_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("apiDeploymentId",))
        & set(
            (
                "parent",
                "apiDeployment",
                "apiDeploymentId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_api_deployment_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_create_api_deployment"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_create_api_deployment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.CreateApiDeploymentRequest.pb(
            registry_service.CreateApiDeploymentRequest()
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
        req.return_value._content = registry_models.ApiDeployment.to_json(
            registry_models.ApiDeployment()
        )

        request = registry_service.CreateApiDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_models.ApiDeployment()

        client.create_api_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_api_deployment_rest_bad_request(
    transport: str = "rest", request_type=registry_service.CreateApiDeploymentRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/apis/sample3"}
    request_init["api_deployment"] = {
        "name": "name_value",
        "display_name": "display_name_value",
        "description": "description_value",
        "revision_id": "revision_id_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "revision_create_time": {},
        "revision_update_time": {},
        "api_spec_revision": "api_spec_revision_value",
        "endpoint_uri": "endpoint_uri_value",
        "external_channel_uri": "external_channel_uri_value",
        "intended_audience": "intended_audience_value",
        "access_guidance": "access_guidance_value",
        "labels": {},
        "annotations": {},
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
        client.create_api_deployment(request)


def test_create_api_deployment_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiDeployment()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2/apis/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            api_deployment=registry_models.ApiDeployment(name="name_value"),
            api_deployment_id="api_deployment_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiDeployment.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_api_deployment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/apis/*}/deployments"
            % client.transport._host,
            args[1],
        )


def test_create_api_deployment_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_api_deployment(
            registry_service.CreateApiDeploymentRequest(),
            parent="parent_value",
            api_deployment=registry_models.ApiDeployment(name="name_value"),
            api_deployment_id="api_deployment_id_value",
        )


def test_create_api_deployment_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.UpdateApiDeploymentRequest,
        dict,
    ],
)
def test_update_api_deployment_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "api_deployment": {
            "name": "projects/sample1/locations/sample2/apis/sample3/deployments/sample4"
        }
    }
    request_init["api_deployment"] = {
        "name": "projects/sample1/locations/sample2/apis/sample3/deployments/sample4",
        "display_name": "display_name_value",
        "description": "description_value",
        "revision_id": "revision_id_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "revision_create_time": {},
        "revision_update_time": {},
        "api_spec_revision": "api_spec_revision_value",
        "endpoint_uri": "endpoint_uri_value",
        "external_channel_uri": "external_channel_uri_value",
        "intended_audience": "intended_audience_value",
        "access_guidance": "access_guidance_value",
        "labels": {},
        "annotations": {},
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiDeployment(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            revision_id="revision_id_value",
            api_spec_revision="api_spec_revision_value",
            endpoint_uri="endpoint_uri_value",
            external_channel_uri="external_channel_uri_value",
            intended_audience="intended_audience_value",
            access_guidance="access_guidance_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiDeployment.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_api_deployment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiDeployment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.api_spec_revision == "api_spec_revision_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.external_channel_uri == "external_channel_uri_value"
    assert response.intended_audience == "intended_audience_value"
    assert response.access_guidance == "access_guidance_value"


def test_update_api_deployment_rest_required_fields(
    request_type=registry_service.UpdateApiDeploymentRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_api_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_api_deployment._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "allow_missing",
            "update_mask",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_models.ApiDeployment()
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

            pb_return_value = registry_models.ApiDeployment.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_api_deployment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_api_deployment_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_api_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "allowMissing",
                "updateMask",
            )
        )
        & set(("apiDeployment",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_api_deployment_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_update_api_deployment"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_update_api_deployment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.UpdateApiDeploymentRequest.pb(
            registry_service.UpdateApiDeploymentRequest()
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
        req.return_value._content = registry_models.ApiDeployment.to_json(
            registry_models.ApiDeployment()
        )

        request = registry_service.UpdateApiDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_models.ApiDeployment()

        client.update_api_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_api_deployment_rest_bad_request(
    transport: str = "rest", request_type=registry_service.UpdateApiDeploymentRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "api_deployment": {
            "name": "projects/sample1/locations/sample2/apis/sample3/deployments/sample4"
        }
    }
    request_init["api_deployment"] = {
        "name": "projects/sample1/locations/sample2/apis/sample3/deployments/sample4",
        "display_name": "display_name_value",
        "description": "description_value",
        "revision_id": "revision_id_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "revision_create_time": {},
        "revision_update_time": {},
        "api_spec_revision": "api_spec_revision_value",
        "endpoint_uri": "endpoint_uri_value",
        "external_channel_uri": "external_channel_uri_value",
        "intended_audience": "intended_audience_value",
        "access_guidance": "access_guidance_value",
        "labels": {},
        "annotations": {},
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
        client.update_api_deployment(request)


def test_update_api_deployment_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiDeployment()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "api_deployment": {
                "name": "projects/sample1/locations/sample2/apis/sample3/deployments/sample4"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            api_deployment=registry_models.ApiDeployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiDeployment.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_api_deployment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{api_deployment.name=projects/*/locations/*/apis/*/deployments/*}"
            % client.transport._host,
            args[1],
        )


def test_update_api_deployment_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_api_deployment(
            registry_service.UpdateApiDeploymentRequest(),
            api_deployment=registry_models.ApiDeployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_api_deployment_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.DeleteApiDeploymentRequest,
        dict,
    ],
)
def test_delete_api_deployment_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/deployments/sample4"
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
        response = client.delete_api_deployment(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_api_deployment_rest_required_fields(
    request_type=registry_service.DeleteApiDeploymentRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_api_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_api_deployment._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("force",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RegistryClient(
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

            response = client.delete_api_deployment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_api_deployment_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_api_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (set(("force",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_api_deployment_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_delete_api_deployment"
    ) as pre:
        pre.assert_not_called()
        pb_message = registry_service.DeleteApiDeploymentRequest.pb(
            registry_service.DeleteApiDeploymentRequest()
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

        request = registry_service.DeleteApiDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_api_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_api_deployment_rest_bad_request(
    transport: str = "rest", request_type=registry_service.DeleteApiDeploymentRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/deployments/sample4"
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
        client.delete_api_deployment(request)


def test_delete_api_deployment_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/apis/sample3/deployments/sample4"
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

        client.delete_api_deployment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/apis/*/deployments/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_api_deployment_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_api_deployment(
            registry_service.DeleteApiDeploymentRequest(),
            name="name_value",
        )


def test_delete_api_deployment_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.TagApiDeploymentRevisionRequest,
        dict,
    ],
)
def test_tag_api_deployment_revision_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/deployments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiDeployment(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            revision_id="revision_id_value",
            api_spec_revision="api_spec_revision_value",
            endpoint_uri="endpoint_uri_value",
            external_channel_uri="external_channel_uri_value",
            intended_audience="intended_audience_value",
            access_guidance="access_guidance_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiDeployment.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.tag_api_deployment_revision(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiDeployment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.api_spec_revision == "api_spec_revision_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.external_channel_uri == "external_channel_uri_value"
    assert response.intended_audience == "intended_audience_value"
    assert response.access_guidance == "access_guidance_value"


def test_tag_api_deployment_revision_rest_required_fields(
    request_type=registry_service.TagApiDeploymentRevisionRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["tag"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).tag_api_deployment_revision._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"
    jsonified_request["tag"] = "tag_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).tag_api_deployment_revision._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"
    assert "tag" in jsonified_request
    assert jsonified_request["tag"] == "tag_value"

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_models.ApiDeployment()
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

            pb_return_value = registry_models.ApiDeployment.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.tag_api_deployment_revision(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_tag_api_deployment_revision_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.tag_api_deployment_revision._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "tag",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_tag_api_deployment_revision_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_tag_api_deployment_revision"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_tag_api_deployment_revision"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.TagApiDeploymentRevisionRequest.pb(
            registry_service.TagApiDeploymentRevisionRequest()
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
        req.return_value._content = registry_models.ApiDeployment.to_json(
            registry_models.ApiDeployment()
        )

        request = registry_service.TagApiDeploymentRevisionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_models.ApiDeployment()

        client.tag_api_deployment_revision(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_tag_api_deployment_revision_rest_bad_request(
    transport: str = "rest",
    request_type=registry_service.TagApiDeploymentRevisionRequest,
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/deployments/sample4"
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
        client.tag_api_deployment_revision(request)


def test_tag_api_deployment_revision_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.ListApiDeploymentRevisionsRequest,
        dict,
    ],
)
def test_list_api_deployment_revisions_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/deployments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_service.ListApiDeploymentRevisionsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_service.ListApiDeploymentRevisionsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_api_deployment_revisions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApiDeploymentRevisionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_api_deployment_revisions_rest_required_fields(
    request_type=registry_service.ListApiDeploymentRevisionsRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_api_deployment_revisions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_api_deployment_revisions._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_service.ListApiDeploymentRevisionsResponse()
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

            pb_return_value = registry_service.ListApiDeploymentRevisionsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_api_deployment_revisions(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_api_deployment_revisions_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_api_deployment_revisions._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("name",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_api_deployment_revisions_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_list_api_deployment_revisions"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_list_api_deployment_revisions"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.ListApiDeploymentRevisionsRequest.pb(
            registry_service.ListApiDeploymentRevisionsRequest()
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
            registry_service.ListApiDeploymentRevisionsResponse.to_json(
                registry_service.ListApiDeploymentRevisionsResponse()
            )
        )

        request = registry_service.ListApiDeploymentRevisionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_service.ListApiDeploymentRevisionsResponse()

        client.list_api_deployment_revisions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_api_deployment_revisions_rest_bad_request(
    transport: str = "rest",
    request_type=registry_service.ListApiDeploymentRevisionsRequest,
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/deployments/sample4"
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
        client.list_api_deployment_revisions(request)


def test_list_api_deployment_revisions_rest_pager(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            registry_service.ListApiDeploymentRevisionsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListApiDeploymentRevisionsResponse(
                api_deployments=[],
                next_page_token="def",
            ),
            registry_service.ListApiDeploymentRevisionsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListApiDeploymentRevisionsResponse(
                api_deployments=[
                    registry_models.ApiDeployment(),
                    registry_models.ApiDeployment(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            registry_service.ListApiDeploymentRevisionsResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "name": "projects/sample1/locations/sample2/apis/sample3/deployments/sample4"
        }

        pager = client.list_api_deployment_revisions(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, registry_models.ApiDeployment) for i in results)

        pages = list(client.list_api_deployment_revisions(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.RollbackApiDeploymentRequest,
        dict,
    ],
)
def test_rollback_api_deployment_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/deployments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiDeployment(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            revision_id="revision_id_value",
            api_spec_revision="api_spec_revision_value",
            endpoint_uri="endpoint_uri_value",
            external_channel_uri="external_channel_uri_value",
            intended_audience="intended_audience_value",
            access_guidance="access_guidance_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiDeployment.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.rollback_api_deployment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiDeployment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.api_spec_revision == "api_spec_revision_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.external_channel_uri == "external_channel_uri_value"
    assert response.intended_audience == "intended_audience_value"
    assert response.access_guidance == "access_guidance_value"


def test_rollback_api_deployment_rest_required_fields(
    request_type=registry_service.RollbackApiDeploymentRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["revision_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).rollback_api_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"
    jsonified_request["revisionId"] = "revision_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).rollback_api_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"
    assert "revisionId" in jsonified_request
    assert jsonified_request["revisionId"] == "revision_id_value"

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_models.ApiDeployment()
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

            pb_return_value = registry_models.ApiDeployment.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.rollback_api_deployment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_rollback_api_deployment_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.rollback_api_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "revisionId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_rollback_api_deployment_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_rollback_api_deployment"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_rollback_api_deployment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.RollbackApiDeploymentRequest.pb(
            registry_service.RollbackApiDeploymentRequest()
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
        req.return_value._content = registry_models.ApiDeployment.to_json(
            registry_models.ApiDeployment()
        )

        request = registry_service.RollbackApiDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_models.ApiDeployment()

        client.rollback_api_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_rollback_api_deployment_rest_bad_request(
    transport: str = "rest", request_type=registry_service.RollbackApiDeploymentRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/deployments/sample4"
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
        client.rollback_api_deployment(request)


def test_rollback_api_deployment_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.DeleteApiDeploymentRevisionRequest,
        dict,
    ],
)
def test_delete_api_deployment_revision_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/deployments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiDeployment(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            revision_id="revision_id_value",
            api_spec_revision="api_spec_revision_value",
            endpoint_uri="endpoint_uri_value",
            external_channel_uri="external_channel_uri_value",
            intended_audience="intended_audience_value",
            access_guidance="access_guidance_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiDeployment.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_api_deployment_revision(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.ApiDeployment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert response.api_spec_revision == "api_spec_revision_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.external_channel_uri == "external_channel_uri_value"
    assert response.intended_audience == "intended_audience_value"
    assert response.access_guidance == "access_guidance_value"


def test_delete_api_deployment_revision_rest_required_fields(
    request_type=registry_service.DeleteApiDeploymentRevisionRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_api_deployment_revision._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_api_deployment_revision._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_models.ApiDeployment()
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

            pb_return_value = registry_models.ApiDeployment.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_api_deployment_revision(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_api_deployment_revision_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_api_deployment_revision._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_api_deployment_revision_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_delete_api_deployment_revision"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_delete_api_deployment_revision"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.DeleteApiDeploymentRevisionRequest.pb(
            registry_service.DeleteApiDeploymentRevisionRequest()
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
        req.return_value._content = registry_models.ApiDeployment.to_json(
            registry_models.ApiDeployment()
        )

        request = registry_service.DeleteApiDeploymentRevisionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_models.ApiDeployment()

        client.delete_api_deployment_revision(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_api_deployment_revision_rest_bad_request(
    transport: str = "rest",
    request_type=registry_service.DeleteApiDeploymentRevisionRequest,
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/apis/sample3/deployments/sample4"
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
        client.delete_api_deployment_revision(request)


def test_delete_api_deployment_revision_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.ApiDeployment()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/apis/sample3/deployments/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.ApiDeployment.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_api_deployment_revision(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/apis/*/deployments/*}:deleteRevision"
            % client.transport._host,
            args[1],
        )


def test_delete_api_deployment_revision_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_api_deployment_revision(
            registry_service.DeleteApiDeploymentRevisionRequest(),
            name="name_value",
        )


def test_delete_api_deployment_revision_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.ListArtifactsRequest,
        dict,
    ],
)
def test_list_artifacts_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_service.ListArtifactsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_service.ListArtifactsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_artifacts(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListArtifactsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_artifacts_rest_required_fields(
    request_type=registry_service.ListArtifactsRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_artifacts._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_artifacts._get_unset_required_fields(jsonified_request)
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

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_service.ListArtifactsResponse()
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

            pb_return_value = registry_service.ListArtifactsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_artifacts(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_artifacts_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_artifacts._get_unset_required_fields({})
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
def test_list_artifacts_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_list_artifacts"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_list_artifacts"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.ListArtifactsRequest.pb(
            registry_service.ListArtifactsRequest()
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
        req.return_value._content = registry_service.ListArtifactsResponse.to_json(
            registry_service.ListArtifactsResponse()
        )

        request = registry_service.ListArtifactsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_service.ListArtifactsResponse()

        client.list_artifacts(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_artifacts_rest_bad_request(
    transport: str = "rest", request_type=registry_service.ListArtifactsRequest
):
    client = RegistryClient(
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
        client.list_artifacts(request)


def test_list_artifacts_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_service.ListArtifactsResponse()

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
        pb_return_value = registry_service.ListArtifactsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_artifacts(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/artifacts" % client.transport._host,
            args[1],
        )


def test_list_artifacts_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_artifacts(
            registry_service.ListArtifactsRequest(),
            parent="parent_value",
        )


def test_list_artifacts_rest_pager(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            registry_service.ListArtifactsResponse(
                artifacts=[
                    registry_models.Artifact(),
                    registry_models.Artifact(),
                    registry_models.Artifact(),
                ],
                next_page_token="abc",
            ),
            registry_service.ListArtifactsResponse(
                artifacts=[],
                next_page_token="def",
            ),
            registry_service.ListArtifactsResponse(
                artifacts=[
                    registry_models.Artifact(),
                ],
                next_page_token="ghi",
            ),
            registry_service.ListArtifactsResponse(
                artifacts=[
                    registry_models.Artifact(),
                    registry_models.Artifact(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            registry_service.ListArtifactsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_artifacts(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, registry_models.Artifact) for i in results)

        pages = list(client.list_artifacts(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.GetArtifactRequest,
        dict,
    ],
)
def test_get_artifact_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/artifacts/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.Artifact(
            name="name_value",
            mime_type="mime_type_value",
            size_bytes=1089,
            hash_="hash__value",
            contents=b"contents_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.Artifact.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_artifact(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.Artifact)
    assert response.name == "name_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.contents == b"contents_blob"


def test_get_artifact_rest_required_fields(
    request_type=registry_service.GetArtifactRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_artifact._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_artifact._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_models.Artifact()
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

            pb_return_value = registry_models.Artifact.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_artifact(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_artifact_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_artifact._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_artifact_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_get_artifact"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_get_artifact"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.GetArtifactRequest.pb(
            registry_service.GetArtifactRequest()
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
        req.return_value._content = registry_models.Artifact.to_json(
            registry_models.Artifact()
        )

        request = registry_service.GetArtifactRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_models.Artifact()

        client.get_artifact(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_artifact_rest_bad_request(
    transport: str = "rest", request_type=registry_service.GetArtifactRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/artifacts/sample3"}
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
        client.get_artifact(request)


def test_get_artifact_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.Artifact()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/artifacts/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.Artifact.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_artifact(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/artifacts/*}" % client.transport._host,
            args[1],
        )


def test_get_artifact_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_artifact(
            registry_service.GetArtifactRequest(),
            name="name_value",
        )


def test_get_artifact_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.GetArtifactContentsRequest,
        dict,
    ],
)
def test_get_artifact_contents_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/artifacts/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = httpbody_pb2.HttpBody(
            content_type="content_type_value",
            data=b"data_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = return_value
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_artifact_contents(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, httpbody_pb2.HttpBody)
    assert response.content_type == "content_type_value"
    assert response.data == b"data_blob"


def test_get_artifact_contents_rest_required_fields(
    request_type=registry_service.GetArtifactContentsRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_artifact_contents._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_artifact_contents._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = httpbody_pb2.HttpBody()
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

            pb_return_value = return_value
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_artifact_contents(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_artifact_contents_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_artifact_contents._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_artifact_contents_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_get_artifact_contents"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_get_artifact_contents"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.GetArtifactContentsRequest.pb(
            registry_service.GetArtifactContentsRequest()
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
        req.return_value._content = json_format.MessageToJson(httpbody_pb2.HttpBody())

        request = registry_service.GetArtifactContentsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = httpbody_pb2.HttpBody()

        client.get_artifact_contents(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_artifact_contents_rest_bad_request(
    transport: str = "rest", request_type=registry_service.GetArtifactContentsRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/artifacts/sample3"}
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
        client.get_artifact_contents(request)


def test_get_artifact_contents_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = httpbody_pb2.HttpBody()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/artifacts/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = return_value
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_artifact_contents(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/artifacts/*}:getContents"
            % client.transport._host,
            args[1],
        )


def test_get_artifact_contents_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_artifact_contents(
            registry_service.GetArtifactContentsRequest(),
            name="name_value",
        )


def test_get_artifact_contents_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.CreateArtifactRequest,
        dict,
    ],
)
def test_create_artifact_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["artifact"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "mime_type": "mime_type_value",
        "size_bytes": 1089,
        "hash_": "hash__value",
        "contents": b"contents_blob",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.Artifact(
            name="name_value",
            mime_type="mime_type_value",
            size_bytes=1089,
            hash_="hash__value",
            contents=b"contents_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.Artifact.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_artifact(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.Artifact)
    assert response.name == "name_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.contents == b"contents_blob"


def test_create_artifact_rest_required_fields(
    request_type=registry_service.CreateArtifactRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["artifact_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped
    assert "artifactId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_artifact._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "artifactId" in jsonified_request
    assert jsonified_request["artifactId"] == request_init["artifact_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["artifactId"] = "artifact_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_artifact._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("artifact_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "artifactId" in jsonified_request
    assert jsonified_request["artifactId"] == "artifact_id_value"

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_models.Artifact()
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

            pb_return_value = registry_models.Artifact.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_artifact(request)

            expected_params = [
                (
                    "artifactId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_artifact_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_artifact._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("artifactId",))
        & set(
            (
                "parent",
                "artifact",
                "artifactId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_artifact_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_create_artifact"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_create_artifact"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.CreateArtifactRequest.pb(
            registry_service.CreateArtifactRequest()
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
        req.return_value._content = registry_models.Artifact.to_json(
            registry_models.Artifact()
        )

        request = registry_service.CreateArtifactRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_models.Artifact()

        client.create_artifact(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_artifact_rest_bad_request(
    transport: str = "rest", request_type=registry_service.CreateArtifactRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["artifact"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "mime_type": "mime_type_value",
        "size_bytes": 1089,
        "hash_": "hash__value",
        "contents": b"contents_blob",
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
        client.create_artifact(request)


def test_create_artifact_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.Artifact()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            artifact=registry_models.Artifact(name="name_value"),
            artifact_id="artifact_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.Artifact.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_artifact(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/artifacts" % client.transport._host,
            args[1],
        )


def test_create_artifact_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_artifact(
            registry_service.CreateArtifactRequest(),
            parent="parent_value",
            artifact=registry_models.Artifact(name="name_value"),
            artifact_id="artifact_id_value",
        )


def test_create_artifact_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.ReplaceArtifactRequest,
        dict,
    ],
)
def test_replace_artifact_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "artifact": {"name": "projects/sample1/locations/sample2/artifacts/sample3"}
    }
    request_init["artifact"] = {
        "name": "projects/sample1/locations/sample2/artifacts/sample3",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "mime_type": "mime_type_value",
        "size_bytes": 1089,
        "hash_": "hash__value",
        "contents": b"contents_blob",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.Artifact(
            name="name_value",
            mime_type="mime_type_value",
            size_bytes=1089,
            hash_="hash__value",
            contents=b"contents_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.Artifact.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.replace_artifact(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, registry_models.Artifact)
    assert response.name == "name_value"
    assert response.mime_type == "mime_type_value"
    assert response.size_bytes == 1089
    assert response.hash_ == "hash__value"
    assert response.contents == b"contents_blob"


def test_replace_artifact_rest_required_fields(
    request_type=registry_service.ReplaceArtifactRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).replace_artifact._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).replace_artifact._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = registry_models.Artifact()
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

            pb_return_value = registry_models.Artifact.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.replace_artifact(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_replace_artifact_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.replace_artifact._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("artifact",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_replace_artifact_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "post_replace_artifact"
    ) as post, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_replace_artifact"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = registry_service.ReplaceArtifactRequest.pb(
            registry_service.ReplaceArtifactRequest()
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
        req.return_value._content = registry_models.Artifact.to_json(
            registry_models.Artifact()
        )

        request = registry_service.ReplaceArtifactRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = registry_models.Artifact()

        client.replace_artifact(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_replace_artifact_rest_bad_request(
    transport: str = "rest", request_type=registry_service.ReplaceArtifactRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "artifact": {"name": "projects/sample1/locations/sample2/artifacts/sample3"}
    }
    request_init["artifact"] = {
        "name": "projects/sample1/locations/sample2/artifacts/sample3",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "mime_type": "mime_type_value",
        "size_bytes": 1089,
        "hash_": "hash__value",
        "contents": b"contents_blob",
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
        client.replace_artifact(request)


def test_replace_artifact_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = registry_models.Artifact()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "artifact": {"name": "projects/sample1/locations/sample2/artifacts/sample3"}
        }

        # get truthy value for each flattened field
        mock_args = dict(
            artifact=registry_models.Artifact(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = registry_models.Artifact.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.replace_artifact(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{artifact.name=projects/*/locations/*/artifacts/*}"
            % client.transport._host,
            args[1],
        )


def test_replace_artifact_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.replace_artifact(
            registry_service.ReplaceArtifactRequest(),
            artifact=registry_models.Artifact(name="name_value"),
        )


def test_replace_artifact_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        registry_service.DeleteArtifactRequest,
        dict,
    ],
)
def test_delete_artifact_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/artifacts/sample3"}
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
        response = client.delete_artifact(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_artifact_rest_required_fields(
    request_type=registry_service.DeleteArtifactRequest,
):
    transport_class = transports.RegistryRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_artifact._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_artifact._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RegistryClient(
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

            response = client.delete_artifact(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_artifact_rest_unset_required_fields():
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_artifact._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_artifact_rest_interceptors(null_interceptor):
    transport = transports.RegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.RegistryRestInterceptor(),
    )
    client = RegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegistryRestInterceptor, "pre_delete_artifact"
    ) as pre:
        pre.assert_not_called()
        pb_message = registry_service.DeleteArtifactRequest.pb(
            registry_service.DeleteArtifactRequest()
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

        request = registry_service.DeleteArtifactRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_artifact(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_artifact_rest_bad_request(
    transport: str = "rest", request_type=registry_service.DeleteArtifactRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/artifacts/sample3"}
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
        client.delete_artifact(request)


def test_delete_artifact_rest_flattened():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/artifacts/sample3"
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

        client.delete_artifact(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/artifacts/*}" % client.transport._host,
            args[1],
        )


def test_delete_artifact_rest_flattened_error(transport: str = "rest"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_artifact(
            registry_service.DeleteArtifactRequest(),
            name="name_value",
        )


def test_delete_artifact_rest_error():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.RegistryGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = RegistryClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.RegistryGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = RegistryClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.RegistryGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = RegistryClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = RegistryClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.RegistryGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = RegistryClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.RegistryGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = RegistryClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.RegistryGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.RegistryGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.RegistryGrpcTransport,
        transports.RegistryGrpcAsyncIOTransport,
        transports.RegistryRestTransport,
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
    transport = RegistryClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.RegistryGrpcTransport,
    )


def test_registry_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.RegistryTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_registry_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.apigee_registry_v1.services.registry.transports.RegistryTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.RegistryTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_apis",
        "get_api",
        "create_api",
        "update_api",
        "delete_api",
        "list_api_versions",
        "get_api_version",
        "create_api_version",
        "update_api_version",
        "delete_api_version",
        "list_api_specs",
        "get_api_spec",
        "get_api_spec_contents",
        "create_api_spec",
        "update_api_spec",
        "delete_api_spec",
        "tag_api_spec_revision",
        "list_api_spec_revisions",
        "rollback_api_spec",
        "delete_api_spec_revision",
        "list_api_deployments",
        "get_api_deployment",
        "create_api_deployment",
        "update_api_deployment",
        "delete_api_deployment",
        "tag_api_deployment_revision",
        "list_api_deployment_revisions",
        "rollback_api_deployment",
        "delete_api_deployment_revision",
        "list_artifacts",
        "get_artifact",
        "get_artifact_contents",
        "create_artifact",
        "replace_artifact",
        "delete_artifact",
        "set_iam_policy",
        "get_iam_policy",
        "test_iam_permissions",
        "get_location",
        "list_locations",
        "get_operation",
        "cancel_operation",
        "delete_operation",
        "list_operations",
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


def test_registry_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.apigee_registry_v1.services.registry.transports.RegistryTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.RegistryTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_registry_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.apigee_registry_v1.services.registry.transports.RegistryTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.RegistryTransport()
        adc.assert_called_once()


def test_registry_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        RegistryClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.RegistryGrpcTransport,
        transports.RegistryGrpcAsyncIOTransport,
    ],
)
def test_registry_transport_auth_adc(transport_class):
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
        transports.RegistryGrpcTransport,
        transports.RegistryGrpcAsyncIOTransport,
        transports.RegistryRestTransport,
    ],
)
def test_registry_transport_auth_gdch_credentials(transport_class):
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
        (transports.RegistryGrpcTransport, grpc_helpers),
        (transports.RegistryGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_registry_transport_create_channel(transport_class, grpc_helpers):
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
            "apigeeregistry.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="apigeeregistry.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.RegistryGrpcTransport, transports.RegistryGrpcAsyncIOTransport],
)
def test_registry_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_registry_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.RegistryRestTransport(
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
def test_registry_host_no_port(transport_name):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="apigeeregistry.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "apigeeregistry.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://apigeeregistry.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_registry_host_with_port(transport_name):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="apigeeregistry.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "apigeeregistry.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://apigeeregistry.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_registry_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = RegistryClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = RegistryClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.list_apis._session
    session2 = client2.transport.list_apis._session
    assert session1 != session2
    session1 = client1.transport.get_api._session
    session2 = client2.transport.get_api._session
    assert session1 != session2
    session1 = client1.transport.create_api._session
    session2 = client2.transport.create_api._session
    assert session1 != session2
    session1 = client1.transport.update_api._session
    session2 = client2.transport.update_api._session
    assert session1 != session2
    session1 = client1.transport.delete_api._session
    session2 = client2.transport.delete_api._session
    assert session1 != session2
    session1 = client1.transport.list_api_versions._session
    session2 = client2.transport.list_api_versions._session
    assert session1 != session2
    session1 = client1.transport.get_api_version._session
    session2 = client2.transport.get_api_version._session
    assert session1 != session2
    session1 = client1.transport.create_api_version._session
    session2 = client2.transport.create_api_version._session
    assert session1 != session2
    session1 = client1.transport.update_api_version._session
    session2 = client2.transport.update_api_version._session
    assert session1 != session2
    session1 = client1.transport.delete_api_version._session
    session2 = client2.transport.delete_api_version._session
    assert session1 != session2
    session1 = client1.transport.list_api_specs._session
    session2 = client2.transport.list_api_specs._session
    assert session1 != session2
    session1 = client1.transport.get_api_spec._session
    session2 = client2.transport.get_api_spec._session
    assert session1 != session2
    session1 = client1.transport.get_api_spec_contents._session
    session2 = client2.transport.get_api_spec_contents._session
    assert session1 != session2
    session1 = client1.transport.create_api_spec._session
    session2 = client2.transport.create_api_spec._session
    assert session1 != session2
    session1 = client1.transport.update_api_spec._session
    session2 = client2.transport.update_api_spec._session
    assert session1 != session2
    session1 = client1.transport.delete_api_spec._session
    session2 = client2.transport.delete_api_spec._session
    assert session1 != session2
    session1 = client1.transport.tag_api_spec_revision._session
    session2 = client2.transport.tag_api_spec_revision._session
    assert session1 != session2
    session1 = client1.transport.list_api_spec_revisions._session
    session2 = client2.transport.list_api_spec_revisions._session
    assert session1 != session2
    session1 = client1.transport.rollback_api_spec._session
    session2 = client2.transport.rollback_api_spec._session
    assert session1 != session2
    session1 = client1.transport.delete_api_spec_revision._session
    session2 = client2.transport.delete_api_spec_revision._session
    assert session1 != session2
    session1 = client1.transport.list_api_deployments._session
    session2 = client2.transport.list_api_deployments._session
    assert session1 != session2
    session1 = client1.transport.get_api_deployment._session
    session2 = client2.transport.get_api_deployment._session
    assert session1 != session2
    session1 = client1.transport.create_api_deployment._session
    session2 = client2.transport.create_api_deployment._session
    assert session1 != session2
    session1 = client1.transport.update_api_deployment._session
    session2 = client2.transport.update_api_deployment._session
    assert session1 != session2
    session1 = client1.transport.delete_api_deployment._session
    session2 = client2.transport.delete_api_deployment._session
    assert session1 != session2
    session1 = client1.transport.tag_api_deployment_revision._session
    session2 = client2.transport.tag_api_deployment_revision._session
    assert session1 != session2
    session1 = client1.transport.list_api_deployment_revisions._session
    session2 = client2.transport.list_api_deployment_revisions._session
    assert session1 != session2
    session1 = client1.transport.rollback_api_deployment._session
    session2 = client2.transport.rollback_api_deployment._session
    assert session1 != session2
    session1 = client1.transport.delete_api_deployment_revision._session
    session2 = client2.transport.delete_api_deployment_revision._session
    assert session1 != session2
    session1 = client1.transport.list_artifacts._session
    session2 = client2.transport.list_artifacts._session
    assert session1 != session2
    session1 = client1.transport.get_artifact._session
    session2 = client2.transport.get_artifact._session
    assert session1 != session2
    session1 = client1.transport.get_artifact_contents._session
    session2 = client2.transport.get_artifact_contents._session
    assert session1 != session2
    session1 = client1.transport.create_artifact._session
    session2 = client2.transport.create_artifact._session
    assert session1 != session2
    session1 = client1.transport.replace_artifact._session
    session2 = client2.transport.replace_artifact._session
    assert session1 != session2
    session1 = client1.transport.delete_artifact._session
    session2 = client2.transport.delete_artifact._session
    assert session1 != session2


def test_registry_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.RegistryGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_registry_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.RegistryGrpcAsyncIOTransport(
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
    [transports.RegistryGrpcTransport, transports.RegistryGrpcAsyncIOTransport],
)
def test_registry_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.RegistryGrpcTransport, transports.RegistryGrpcAsyncIOTransport],
)
def test_registry_transport_channel_mtls_with_adc(transport_class):
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


def test_api_path():
    project = "squid"
    location = "clam"
    api = "whelk"
    expected = "projects/{project}/locations/{location}/apis/{api}".format(
        project=project,
        location=location,
        api=api,
    )
    actual = RegistryClient.api_path(project, location, api)
    assert expected == actual


def test_parse_api_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "api": "nudibranch",
    }
    path = RegistryClient.api_path(**expected)

    # Check that the path construction is reversible.
    actual = RegistryClient.parse_api_path(path)
    assert expected == actual


def test_api_deployment_path():
    project = "cuttlefish"
    location = "mussel"
    api = "winkle"
    deployment = "nautilus"
    expected = "projects/{project}/locations/{location}/apis/{api}/deployments/{deployment}".format(
        project=project,
        location=location,
        api=api,
        deployment=deployment,
    )
    actual = RegistryClient.api_deployment_path(project, location, api, deployment)
    assert expected == actual


def test_parse_api_deployment_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "api": "squid",
        "deployment": "clam",
    }
    path = RegistryClient.api_deployment_path(**expected)

    # Check that the path construction is reversible.
    actual = RegistryClient.parse_api_deployment_path(path)
    assert expected == actual


def test_api_spec_path():
    project = "whelk"
    location = "octopus"
    api = "oyster"
    version = "nudibranch"
    spec = "cuttlefish"
    expected = "projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec}".format(
        project=project,
        location=location,
        api=api,
        version=version,
        spec=spec,
    )
    actual = RegistryClient.api_spec_path(project, location, api, version, spec)
    assert expected == actual


def test_parse_api_spec_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "api": "nautilus",
        "version": "scallop",
        "spec": "abalone",
    }
    path = RegistryClient.api_spec_path(**expected)

    # Check that the path construction is reversible.
    actual = RegistryClient.parse_api_spec_path(path)
    assert expected == actual


def test_api_version_path():
    project = "squid"
    location = "clam"
    api = "whelk"
    version = "octopus"
    expected = (
        "projects/{project}/locations/{location}/apis/{api}/versions/{version}".format(
            project=project,
            location=location,
            api=api,
            version=version,
        )
    )
    actual = RegistryClient.api_version_path(project, location, api, version)
    assert expected == actual


def test_parse_api_version_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "api": "cuttlefish",
        "version": "mussel",
    }
    path = RegistryClient.api_version_path(**expected)

    # Check that the path construction is reversible.
    actual = RegistryClient.parse_api_version_path(path)
    assert expected == actual


def test_artifact_path():
    project = "winkle"
    location = "nautilus"
    artifact = "scallop"
    expected = "projects/{project}/locations/{location}/artifacts/{artifact}".format(
        project=project,
        location=location,
        artifact=artifact,
    )
    actual = RegistryClient.artifact_path(project, location, artifact)
    assert expected == actual


def test_parse_artifact_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "artifact": "clam",
    }
    path = RegistryClient.artifact_path(**expected)

    # Check that the path construction is reversible.
    actual = RegistryClient.parse_artifact_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = RegistryClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = RegistryClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = RegistryClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = RegistryClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = RegistryClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = RegistryClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = RegistryClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = RegistryClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = RegistryClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = RegistryClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = RegistryClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = RegistryClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = RegistryClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = RegistryClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = RegistryClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.RegistryTransport, "_prep_wrapped_messages"
    ) as prep:
        client = RegistryClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.RegistryTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = RegistryClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = RegistryAsyncClient(
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
    client = RegistryClient(
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
    client = RegistryClient(
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
    client = RegistryClient(
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
    client = RegistryClient(
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


def test_get_iam_policy_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.GetIamPolicyRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"resource": "projects/sample1/locations/sample2/apis/sample3"}, request
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
        client.get_iam_policy(request)


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.GetIamPolicyRequest,
        dict,
    ],
)
def test_get_iam_policy_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"resource": "projects/sample1/locations/sample2/apis/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = policy_pb2.Policy()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)


def test_set_iam_policy_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.SetIamPolicyRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"resource": "projects/sample1/locations/sample2/apis/sample3"}, request
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
        client.set_iam_policy(request)


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.SetIamPolicyRequest,
        dict,
    ],
)
def test_set_iam_policy_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"resource": "projects/sample1/locations/sample2/apis/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = policy_pb2.Policy()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.set_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)


def test_test_iam_permissions_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.TestIamPermissionsRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"resource": "projects/sample1/locations/sample2/apis/sample3"}, request
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
        client.test_iam_permissions(request)


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.TestIamPermissionsRequest,
        dict,
    ],
)
def test_test_iam_permissions_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"resource": "projects/sample1/locations/sample2/apis/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = iam_policy_pb2.TestIamPermissionsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.test_iam_permissions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)


def test_cancel_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.CancelOperationRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.cancel_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.CancelOperationRequest,
        dict,
    ],
)
def test_cancel_operation_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = "{}"

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.cancel_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.DeleteOperationRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.DeleteOperationRequest,
        dict,
    ],
)
def test_delete_operation_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = "{}"

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.delete_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_get_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.GetOperationRequest
):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_operation(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_list_operations_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.ListOperationsRequest
):
    client = RegistryClient(
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
        client.list_operations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.ListOperationsRequest,
        dict,
    ],
)
def test_list_operations_rest(request_type):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.ListOperationsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.list_operations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_delete_operation(transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_operation_async(transport: str = "grpc"):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_operation_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = None

        client.delete_operation(request)
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
async def test_delete_operation_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_operation(request)
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


def test_delete_operation_from_dict():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_delete_operation_from_dict_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_cancel_operation(transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_cancel_operation_async(transport: str = "grpc"):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_cancel_operation_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

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
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_cancel_operation_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.cancel_operation(request)
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


def test_cancel_operation_from_dict():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_cancel_operation_from_dict_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_operation(transport: str = "grpc"):
    client = RegistryClient(
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
async def test_get_operation_async(transport: str = "grpc"):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = RegistryClient(
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
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = RegistryClient(
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
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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


def test_list_operations(transport: str = "grpc"):
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()
        response = client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


@pytest.mark.asyncio
async def test_list_operations_async(transport: str = "grpc"):
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_list_operations_field_headers():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = operations_pb2.ListOperationsResponse()

        client.list_operations(request)
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
async def test_list_operations_field_headers_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        await client.list_operations(request)
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


def test_list_operations_from_dict():
    client = RegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()

        response = client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_operations_from_dict_async():
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_locations(transport: str = "grpc"):
    client = RegistryClient(
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
async def test_list_locations_async(transport: str = "grpc"):
    client = RegistryAsyncClient(
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
    client = RegistryClient(
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
    client = RegistryAsyncClient(
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
    client = RegistryClient(
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
    client = RegistryAsyncClient(
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
    client = RegistryClient(
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
    client = RegistryAsyncClient(
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
    client = RegistryClient(credentials=ga_credentials.AnonymousCredentials())

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
    client = RegistryAsyncClient(credentials=ga_credentials.AnonymousCredentials())

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
    client = RegistryClient(
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
    client = RegistryAsyncClient(
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


def test_set_iam_policy(transport: str = "grpc"):
    client = RegistryClient(
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
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = RegistryClient(
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
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = RegistryClient(
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
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = RegistryClient(
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
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = RegistryClient(
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
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = RegistryClient(
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
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = RegistryClient(
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
    client = RegistryAsyncClient(
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
    client = RegistryClient(
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
    client = RegistryAsyncClient(
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
    client = RegistryClient(
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
    client = RegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = RegistryClient(
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
        client = RegistryClient(
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
        (RegistryClient, transports.RegistryGrpcTransport),
        (RegistryAsyncClient, transports.RegistryGrpcAsyncIOTransport),
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
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
