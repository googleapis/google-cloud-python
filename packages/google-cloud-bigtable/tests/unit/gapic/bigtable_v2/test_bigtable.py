# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule


from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.bigtable_v2.services.bigtable import BigtableAsyncClient
from google.cloud.bigtable_v2.services.bigtable import BigtableClient
from google.cloud.bigtable_v2.services.bigtable import transports
from google.cloud.bigtable_v2.types import bigtable
from google.cloud.bigtable_v2.types import data
from google.oauth2 import service_account
import google.auth


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

    assert BigtableClient._get_default_mtls_endpoint(None) is None
    assert BigtableClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert (
        BigtableClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        BigtableClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        BigtableClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert BigtableClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize(
    "client_class",
    [
        BigtableClient,
        BigtableAsyncClient,
    ],
)
def test_bigtable_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "bigtable.googleapis.com:443"


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.BigtableGrpcTransport, "grpc"),
        (transports.BigtableGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_bigtable_client_service_account_always_use_jwt(
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
    "client_class",
    [
        BigtableClient,
        BigtableAsyncClient,
    ],
)
def test_bigtable_client_from_service_account_file(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "bigtable.googleapis.com:443"


def test_bigtable_client_get_transport_class():
    transport = BigtableClient.get_transport_class()
    available_transports = [
        transports.BigtableGrpcTransport,
    ]
    assert transport in available_transports

    transport = BigtableClient.get_transport_class("grpc")
    assert transport == transports.BigtableGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (BigtableClient, transports.BigtableGrpcTransport, "grpc"),
        (BigtableAsyncClient, transports.BigtableGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
@mock.patch.object(
    BigtableClient, "DEFAULT_ENDPOINT", modify_default_endpoint(BigtableClient)
)
@mock.patch.object(
    BigtableAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BigtableAsyncClient),
)
def test_bigtable_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(BigtableClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(BigtableClient, "get_transport_class") as gtc:
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
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (BigtableClient, transports.BigtableGrpcTransport, "grpc", "true"),
        (
            BigtableAsyncClient,
            transports.BigtableGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (BigtableClient, transports.BigtableGrpcTransport, "grpc", "false"),
        (
            BigtableAsyncClient,
            transports.BigtableGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    BigtableClient, "DEFAULT_ENDPOINT", modify_default_endpoint(BigtableClient)
)
@mock.patch.object(
    BigtableAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BigtableAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_bigtable_client_mtls_env_auto(
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
                )


@pytest.mark.parametrize("client_class", [BigtableClient, BigtableAsyncClient])
@mock.patch.object(
    BigtableClient, "DEFAULT_ENDPOINT", modify_default_endpoint(BigtableClient)
)
@mock.patch.object(
    BigtableAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BigtableAsyncClient),
)
def test_bigtable_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (BigtableClient, transports.BigtableGrpcTransport, "grpc"),
        (BigtableAsyncClient, transports.BigtableGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_bigtable_client_client_options_scopes(
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
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (BigtableClient, transports.BigtableGrpcTransport, "grpc", grpc_helpers),
        (
            BigtableAsyncClient,
            transports.BigtableGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_bigtable_client_client_options_credentials_file(
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
        )


def test_bigtable_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.bigtable_v2.services.bigtable.transports.BigtableGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = BigtableClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (BigtableClient, transports.BigtableGrpcTransport, "grpc", grpc_helpers),
        (
            BigtableAsyncClient,
            transports.BigtableGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_bigtable_client_create_channel_credentials_file(
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
            "bigtable.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                "https://www.googleapis.com/auth/bigtable.data",
                "https://www.googleapis.com/auth/bigtable.data.readonly",
                "https://www.googleapis.com/auth/cloud-bigtable.data",
                "https://www.googleapis.com/auth/cloud-bigtable.data.readonly",
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            scopes=None,
            default_host="bigtable.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable.ReadRowsRequest,
        dict,
    ],
)
def test_read_rows(request_type, transport: str = "grpc"):
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_rows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([bigtable.ReadRowsResponse()])
        response = client.read_rows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable.ReadRowsRequest()

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, bigtable.ReadRowsResponse)


def test_read_rows_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_rows), "__call__") as call:
        client.read_rows()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable.ReadRowsRequest()


@pytest.mark.asyncio
async def test_read_rows_async(
    transport: str = "grpc_asyncio", request_type=bigtable.ReadRowsRequest
):
    client = BigtableAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_rows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[bigtable.ReadRowsResponse()]
        )
        response = await client.read_rows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable.ReadRowsRequest()

    # Establish that the response is the type that we expect.
    message = await response.read()
    assert isinstance(message, bigtable.ReadRowsResponse)


@pytest.mark.asyncio
async def test_read_rows_async_from_dict():
    await test_read_rows_async(request_type=dict)


def test_read_rows_routing_parameters():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable.ReadRowsRequest(
        {"table_name": "projects/sample1/instances/sample2/tables/sample3"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_rows), "__call__") as call:
        call.return_value = iter([bigtable.ReadRowsResponse()])
        client.read_rows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]
    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable.ReadRowsRequest({"app_profile_id": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_rows), "__call__") as call:
        call.return_value = iter([bigtable.ReadRowsResponse()])
        client.read_rows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_read_rows_flattened():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_rows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([bigtable.ReadRowsResponse()])
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.read_rows(
            table_name="table_name_value",
            app_profile_id="app_profile_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].table_name
        mock_val = "table_name_value"
        assert arg == mock_val
        arg = args[0].app_profile_id
        mock_val = "app_profile_id_value"
        assert arg == mock_val


def test_read_rows_flattened_error():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.read_rows(
            bigtable.ReadRowsRequest(),
            table_name="table_name_value",
            app_profile_id="app_profile_id_value",
        )


@pytest.mark.asyncio
async def test_read_rows_flattened_async():
    client = BigtableAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_rows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([bigtable.ReadRowsResponse()])

        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.read_rows(
            table_name="table_name_value",
            app_profile_id="app_profile_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].table_name
        mock_val = "table_name_value"
        assert arg == mock_val
        arg = args[0].app_profile_id
        mock_val = "app_profile_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_read_rows_flattened_error_async():
    client = BigtableAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.read_rows(
            bigtable.ReadRowsRequest(),
            table_name="table_name_value",
            app_profile_id="app_profile_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable.SampleRowKeysRequest,
        dict,
    ],
)
def test_sample_row_keys(request_type, transport: str = "grpc"):
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.sample_row_keys), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([bigtable.SampleRowKeysResponse()])
        response = client.sample_row_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable.SampleRowKeysRequest()

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, bigtable.SampleRowKeysResponse)


def test_sample_row_keys_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.sample_row_keys), "__call__") as call:
        client.sample_row_keys()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable.SampleRowKeysRequest()


@pytest.mark.asyncio
async def test_sample_row_keys_async(
    transport: str = "grpc_asyncio", request_type=bigtable.SampleRowKeysRequest
):
    client = BigtableAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.sample_row_keys), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[bigtable.SampleRowKeysResponse()]
        )
        response = await client.sample_row_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable.SampleRowKeysRequest()

    # Establish that the response is the type that we expect.
    message = await response.read()
    assert isinstance(message, bigtable.SampleRowKeysResponse)


@pytest.mark.asyncio
async def test_sample_row_keys_async_from_dict():
    await test_sample_row_keys_async(request_type=dict)


def test_sample_row_keys_routing_parameters():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable.SampleRowKeysRequest(
        {"table_name": "projects/sample1/instances/sample2/tables/sample3"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.sample_row_keys), "__call__") as call:
        call.return_value = iter([bigtable.SampleRowKeysResponse()])
        client.sample_row_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]
    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable.SampleRowKeysRequest({"app_profile_id": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.sample_row_keys), "__call__") as call:
        call.return_value = iter([bigtable.SampleRowKeysResponse()])
        client.sample_row_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_sample_row_keys_flattened():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.sample_row_keys), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([bigtable.SampleRowKeysResponse()])
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.sample_row_keys(
            table_name="table_name_value",
            app_profile_id="app_profile_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].table_name
        mock_val = "table_name_value"
        assert arg == mock_val
        arg = args[0].app_profile_id
        mock_val = "app_profile_id_value"
        assert arg == mock_val


def test_sample_row_keys_flattened_error():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.sample_row_keys(
            bigtable.SampleRowKeysRequest(),
            table_name="table_name_value",
            app_profile_id="app_profile_id_value",
        )


@pytest.mark.asyncio
async def test_sample_row_keys_flattened_async():
    client = BigtableAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.sample_row_keys), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([bigtable.SampleRowKeysResponse()])

        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.sample_row_keys(
            table_name="table_name_value",
            app_profile_id="app_profile_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].table_name
        mock_val = "table_name_value"
        assert arg == mock_val
        arg = args[0].app_profile_id
        mock_val = "app_profile_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_sample_row_keys_flattened_error_async():
    client = BigtableAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.sample_row_keys(
            bigtable.SampleRowKeysRequest(),
            table_name="table_name_value",
            app_profile_id="app_profile_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable.MutateRowRequest,
        dict,
    ],
)
def test_mutate_row(request_type, transport: str = "grpc"):
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mutate_row), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable.MutateRowResponse()
        response = client.mutate_row(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable.MutateRowRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, bigtable.MutateRowResponse)


def test_mutate_row_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mutate_row), "__call__") as call:
        client.mutate_row()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable.MutateRowRequest()


@pytest.mark.asyncio
async def test_mutate_row_async(
    transport: str = "grpc_asyncio", request_type=bigtable.MutateRowRequest
):
    client = BigtableAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mutate_row), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable.MutateRowResponse()
        )
        response = await client.mutate_row(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable.MutateRowRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, bigtable.MutateRowResponse)


@pytest.mark.asyncio
async def test_mutate_row_async_from_dict():
    await test_mutate_row_async(request_type=dict)


def test_mutate_row_routing_parameters():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable.MutateRowRequest(
        {"table_name": "projects/sample1/instances/sample2/tables/sample3"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mutate_row), "__call__") as call:
        call.return_value = bigtable.MutateRowResponse()
        client.mutate_row(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]
    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable.MutateRowRequest({"app_profile_id": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mutate_row), "__call__") as call:
        call.return_value = bigtable.MutateRowResponse()
        client.mutate_row(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_mutate_row_flattened():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mutate_row), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable.MutateRowResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.mutate_row(
            table_name="table_name_value",
            row_key=b"row_key_blob",
            mutations=[
                data.Mutation(
                    set_cell=data.Mutation.SetCell(family_name="family_name_value")
                )
            ],
            app_profile_id="app_profile_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].table_name
        mock_val = "table_name_value"
        assert arg == mock_val
        arg = args[0].row_key
        mock_val = b"row_key_blob"
        assert arg == mock_val
        arg = args[0].mutations
        mock_val = [
            data.Mutation(
                set_cell=data.Mutation.SetCell(family_name="family_name_value")
            )
        ]
        assert arg == mock_val
        arg = args[0].app_profile_id
        mock_val = "app_profile_id_value"
        assert arg == mock_val


def test_mutate_row_flattened_error():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.mutate_row(
            bigtable.MutateRowRequest(),
            table_name="table_name_value",
            row_key=b"row_key_blob",
            mutations=[
                data.Mutation(
                    set_cell=data.Mutation.SetCell(family_name="family_name_value")
                )
            ],
            app_profile_id="app_profile_id_value",
        )


@pytest.mark.asyncio
async def test_mutate_row_flattened_async():
    client = BigtableAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mutate_row), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable.MutateRowResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable.MutateRowResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.mutate_row(
            table_name="table_name_value",
            row_key=b"row_key_blob",
            mutations=[
                data.Mutation(
                    set_cell=data.Mutation.SetCell(family_name="family_name_value")
                )
            ],
            app_profile_id="app_profile_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].table_name
        mock_val = "table_name_value"
        assert arg == mock_val
        arg = args[0].row_key
        mock_val = b"row_key_blob"
        assert arg == mock_val
        arg = args[0].mutations
        mock_val = [
            data.Mutation(
                set_cell=data.Mutation.SetCell(family_name="family_name_value")
            )
        ]
        assert arg == mock_val
        arg = args[0].app_profile_id
        mock_val = "app_profile_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_mutate_row_flattened_error_async():
    client = BigtableAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.mutate_row(
            bigtable.MutateRowRequest(),
            table_name="table_name_value",
            row_key=b"row_key_blob",
            mutations=[
                data.Mutation(
                    set_cell=data.Mutation.SetCell(family_name="family_name_value")
                )
            ],
            app_profile_id="app_profile_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable.MutateRowsRequest,
        dict,
    ],
)
def test_mutate_rows(request_type, transport: str = "grpc"):
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mutate_rows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([bigtable.MutateRowsResponse()])
        response = client.mutate_rows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable.MutateRowsRequest()

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, bigtable.MutateRowsResponse)


def test_mutate_rows_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mutate_rows), "__call__") as call:
        client.mutate_rows()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable.MutateRowsRequest()


@pytest.mark.asyncio
async def test_mutate_rows_async(
    transport: str = "grpc_asyncio", request_type=bigtable.MutateRowsRequest
):
    client = BigtableAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mutate_rows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[bigtable.MutateRowsResponse()]
        )
        response = await client.mutate_rows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable.MutateRowsRequest()

    # Establish that the response is the type that we expect.
    message = await response.read()
    assert isinstance(message, bigtable.MutateRowsResponse)


@pytest.mark.asyncio
async def test_mutate_rows_async_from_dict():
    await test_mutate_rows_async(request_type=dict)


def test_mutate_rows_routing_parameters():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable.MutateRowsRequest(
        {"table_name": "projects/sample1/instances/sample2/tables/sample3"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mutate_rows), "__call__") as call:
        call.return_value = iter([bigtable.MutateRowsResponse()])
        client.mutate_rows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]
    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable.MutateRowsRequest({"app_profile_id": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mutate_rows), "__call__") as call:
        call.return_value = iter([bigtable.MutateRowsResponse()])
        client.mutate_rows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_mutate_rows_flattened():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mutate_rows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([bigtable.MutateRowsResponse()])
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.mutate_rows(
            table_name="table_name_value",
            entries=[bigtable.MutateRowsRequest.Entry(row_key=b"row_key_blob")],
            app_profile_id="app_profile_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].table_name
        mock_val = "table_name_value"
        assert arg == mock_val
        arg = args[0].entries
        mock_val = [bigtable.MutateRowsRequest.Entry(row_key=b"row_key_blob")]
        assert arg == mock_val
        arg = args[0].app_profile_id
        mock_val = "app_profile_id_value"
        assert arg == mock_val


def test_mutate_rows_flattened_error():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.mutate_rows(
            bigtable.MutateRowsRequest(),
            table_name="table_name_value",
            entries=[bigtable.MutateRowsRequest.Entry(row_key=b"row_key_blob")],
            app_profile_id="app_profile_id_value",
        )


@pytest.mark.asyncio
async def test_mutate_rows_flattened_async():
    client = BigtableAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.mutate_rows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([bigtable.MutateRowsResponse()])

        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.mutate_rows(
            table_name="table_name_value",
            entries=[bigtable.MutateRowsRequest.Entry(row_key=b"row_key_blob")],
            app_profile_id="app_profile_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].table_name
        mock_val = "table_name_value"
        assert arg == mock_val
        arg = args[0].entries
        mock_val = [bigtable.MutateRowsRequest.Entry(row_key=b"row_key_blob")]
        assert arg == mock_val
        arg = args[0].app_profile_id
        mock_val = "app_profile_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_mutate_rows_flattened_error_async():
    client = BigtableAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.mutate_rows(
            bigtable.MutateRowsRequest(),
            table_name="table_name_value",
            entries=[bigtable.MutateRowsRequest.Entry(row_key=b"row_key_blob")],
            app_profile_id="app_profile_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable.CheckAndMutateRowRequest,
        dict,
    ],
)
def test_check_and_mutate_row(request_type, transport: str = "grpc"):
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_and_mutate_row), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable.CheckAndMutateRowResponse(
            predicate_matched=True,
        )
        response = client.check_and_mutate_row(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable.CheckAndMutateRowRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, bigtable.CheckAndMutateRowResponse)
    assert response.predicate_matched is True


def test_check_and_mutate_row_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_and_mutate_row), "__call__"
    ) as call:
        client.check_and_mutate_row()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable.CheckAndMutateRowRequest()


@pytest.mark.asyncio
async def test_check_and_mutate_row_async(
    transport: str = "grpc_asyncio", request_type=bigtable.CheckAndMutateRowRequest
):
    client = BigtableAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_and_mutate_row), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable.CheckAndMutateRowResponse(
                predicate_matched=True,
            )
        )
        response = await client.check_and_mutate_row(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable.CheckAndMutateRowRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, bigtable.CheckAndMutateRowResponse)
    assert response.predicate_matched is True


@pytest.mark.asyncio
async def test_check_and_mutate_row_async_from_dict():
    await test_check_and_mutate_row_async(request_type=dict)


def test_check_and_mutate_row_routing_parameters():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable.CheckAndMutateRowRequest(
        {"table_name": "projects/sample1/instances/sample2/tables/sample3"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_and_mutate_row), "__call__"
    ) as call:
        call.return_value = bigtable.CheckAndMutateRowResponse()
        client.check_and_mutate_row(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]
    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable.CheckAndMutateRowRequest({"app_profile_id": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_and_mutate_row), "__call__"
    ) as call:
        call.return_value = bigtable.CheckAndMutateRowResponse()
        client.check_and_mutate_row(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_check_and_mutate_row_flattened():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_and_mutate_row), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable.CheckAndMutateRowResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.check_and_mutate_row(
            table_name="table_name_value",
            row_key=b"row_key_blob",
            predicate_filter=data.RowFilter(
                chain=data.RowFilter.Chain(
                    filters=[
                        data.RowFilter(
                            chain=data.RowFilter.Chain(
                                filters=[data.RowFilter(chain=None)]
                            )
                        )
                    ]
                )
            ),
            true_mutations=[
                data.Mutation(
                    set_cell=data.Mutation.SetCell(family_name="family_name_value")
                )
            ],
            false_mutations=[
                data.Mutation(
                    set_cell=data.Mutation.SetCell(family_name="family_name_value")
                )
            ],
            app_profile_id="app_profile_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].table_name
        mock_val = "table_name_value"
        assert arg == mock_val
        arg = args[0].row_key
        mock_val = b"row_key_blob"
        assert arg == mock_val
        arg = args[0].predicate_filter
        mock_val = data.RowFilter(
            chain=data.RowFilter.Chain(
                filters=[
                    data.RowFilter(
                        chain=data.RowFilter.Chain(filters=[data.RowFilter(chain=None)])
                    )
                ]
            )
        )
        assert arg == mock_val
        arg = args[0].true_mutations
        mock_val = [
            data.Mutation(
                set_cell=data.Mutation.SetCell(family_name="family_name_value")
            )
        ]
        assert arg == mock_val
        arg = args[0].false_mutations
        mock_val = [
            data.Mutation(
                set_cell=data.Mutation.SetCell(family_name="family_name_value")
            )
        ]
        assert arg == mock_val
        arg = args[0].app_profile_id
        mock_val = "app_profile_id_value"
        assert arg == mock_val


def test_check_and_mutate_row_flattened_error():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.check_and_mutate_row(
            bigtable.CheckAndMutateRowRequest(),
            table_name="table_name_value",
            row_key=b"row_key_blob",
            predicate_filter=data.RowFilter(
                chain=data.RowFilter.Chain(
                    filters=[
                        data.RowFilter(
                            chain=data.RowFilter.Chain(
                                filters=[data.RowFilter(chain=None)]
                            )
                        )
                    ]
                )
            ),
            true_mutations=[
                data.Mutation(
                    set_cell=data.Mutation.SetCell(family_name="family_name_value")
                )
            ],
            false_mutations=[
                data.Mutation(
                    set_cell=data.Mutation.SetCell(family_name="family_name_value")
                )
            ],
            app_profile_id="app_profile_id_value",
        )


@pytest.mark.asyncio
async def test_check_and_mutate_row_flattened_async():
    client = BigtableAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_and_mutate_row), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable.CheckAndMutateRowResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable.CheckAndMutateRowResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.check_and_mutate_row(
            table_name="table_name_value",
            row_key=b"row_key_blob",
            predicate_filter=data.RowFilter(
                chain=data.RowFilter.Chain(
                    filters=[
                        data.RowFilter(
                            chain=data.RowFilter.Chain(
                                filters=[data.RowFilter(chain=None)]
                            )
                        )
                    ]
                )
            ),
            true_mutations=[
                data.Mutation(
                    set_cell=data.Mutation.SetCell(family_name="family_name_value")
                )
            ],
            false_mutations=[
                data.Mutation(
                    set_cell=data.Mutation.SetCell(family_name="family_name_value")
                )
            ],
            app_profile_id="app_profile_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].table_name
        mock_val = "table_name_value"
        assert arg == mock_val
        arg = args[0].row_key
        mock_val = b"row_key_blob"
        assert arg == mock_val
        arg = args[0].predicate_filter
        mock_val = data.RowFilter(
            chain=data.RowFilter.Chain(
                filters=[
                    data.RowFilter(
                        chain=data.RowFilter.Chain(filters=[data.RowFilter(chain=None)])
                    )
                ]
            )
        )
        assert arg == mock_val
        arg = args[0].true_mutations
        mock_val = [
            data.Mutation(
                set_cell=data.Mutation.SetCell(family_name="family_name_value")
            )
        ]
        assert arg == mock_val
        arg = args[0].false_mutations
        mock_val = [
            data.Mutation(
                set_cell=data.Mutation.SetCell(family_name="family_name_value")
            )
        ]
        assert arg == mock_val
        arg = args[0].app_profile_id
        mock_val = "app_profile_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_check_and_mutate_row_flattened_error_async():
    client = BigtableAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.check_and_mutate_row(
            bigtable.CheckAndMutateRowRequest(),
            table_name="table_name_value",
            row_key=b"row_key_blob",
            predicate_filter=data.RowFilter(
                chain=data.RowFilter.Chain(
                    filters=[
                        data.RowFilter(
                            chain=data.RowFilter.Chain(
                                filters=[data.RowFilter(chain=None)]
                            )
                        )
                    ]
                )
            ),
            true_mutations=[
                data.Mutation(
                    set_cell=data.Mutation.SetCell(family_name="family_name_value")
                )
            ],
            false_mutations=[
                data.Mutation(
                    set_cell=data.Mutation.SetCell(family_name="family_name_value")
                )
            ],
            app_profile_id="app_profile_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable.PingAndWarmRequest,
        dict,
    ],
)
def test_ping_and_warm(request_type, transport: str = "grpc"):
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.ping_and_warm), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable.PingAndWarmResponse()
        response = client.ping_and_warm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable.PingAndWarmRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, bigtable.PingAndWarmResponse)


def test_ping_and_warm_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.ping_and_warm), "__call__") as call:
        client.ping_and_warm()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable.PingAndWarmRequest()


@pytest.mark.asyncio
async def test_ping_and_warm_async(
    transport: str = "grpc_asyncio", request_type=bigtable.PingAndWarmRequest
):
    client = BigtableAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.ping_and_warm), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable.PingAndWarmResponse()
        )
        response = await client.ping_and_warm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable.PingAndWarmRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, bigtable.PingAndWarmResponse)


@pytest.mark.asyncio
async def test_ping_and_warm_async_from_dict():
    await test_ping_and_warm_async(request_type=dict)


def test_ping_and_warm_routing_parameters():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable.PingAndWarmRequest(
        {"name": "projects/sample1/instances/sample2"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.ping_and_warm), "__call__") as call:
        call.return_value = bigtable.PingAndWarmResponse()
        client.ping_and_warm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]
    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable.PingAndWarmRequest({"app_profile_id": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.ping_and_warm), "__call__") as call:
        call.return_value = bigtable.PingAndWarmResponse()
        client.ping_and_warm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_ping_and_warm_flattened():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.ping_and_warm), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable.PingAndWarmResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.ping_and_warm(
            name="name_value",
            app_profile_id="app_profile_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].app_profile_id
        mock_val = "app_profile_id_value"
        assert arg == mock_val


def test_ping_and_warm_flattened_error():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.ping_and_warm(
            bigtable.PingAndWarmRequest(),
            name="name_value",
            app_profile_id="app_profile_id_value",
        )


@pytest.mark.asyncio
async def test_ping_and_warm_flattened_async():
    client = BigtableAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.ping_and_warm), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable.PingAndWarmResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable.PingAndWarmResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.ping_and_warm(
            name="name_value",
            app_profile_id="app_profile_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].app_profile_id
        mock_val = "app_profile_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_ping_and_warm_flattened_error_async():
    client = BigtableAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.ping_and_warm(
            bigtable.PingAndWarmRequest(),
            name="name_value",
            app_profile_id="app_profile_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable.ReadModifyWriteRowRequest,
        dict,
    ],
)
def test_read_modify_write_row(request_type, transport: str = "grpc"):
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_modify_write_row), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable.ReadModifyWriteRowResponse()
        response = client.read_modify_write_row(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable.ReadModifyWriteRowRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, bigtable.ReadModifyWriteRowResponse)


def test_read_modify_write_row_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_modify_write_row), "__call__"
    ) as call:
        client.read_modify_write_row()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable.ReadModifyWriteRowRequest()


@pytest.mark.asyncio
async def test_read_modify_write_row_async(
    transport: str = "grpc_asyncio", request_type=bigtable.ReadModifyWriteRowRequest
):
    client = BigtableAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_modify_write_row), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable.ReadModifyWriteRowResponse()
        )
        response = await client.read_modify_write_row(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable.ReadModifyWriteRowRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, bigtable.ReadModifyWriteRowResponse)


@pytest.mark.asyncio
async def test_read_modify_write_row_async_from_dict():
    await test_read_modify_write_row_async(request_type=dict)


def test_read_modify_write_row_routing_parameters():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable.ReadModifyWriteRowRequest(
        {"table_name": "projects/sample1/instances/sample2/tables/sample3"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_modify_write_row), "__call__"
    ) as call:
        call.return_value = bigtable.ReadModifyWriteRowResponse()
        client.read_modify_write_row(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]
    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable.ReadModifyWriteRowRequest({"app_profile_id": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_modify_write_row), "__call__"
    ) as call:
        call.return_value = bigtable.ReadModifyWriteRowResponse()
        client.read_modify_write_row(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_read_modify_write_row_flattened():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_modify_write_row), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable.ReadModifyWriteRowResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.read_modify_write_row(
            table_name="table_name_value",
            row_key=b"row_key_blob",
            rules=[data.ReadModifyWriteRule(family_name="family_name_value")],
            app_profile_id="app_profile_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].table_name
        mock_val = "table_name_value"
        assert arg == mock_val
        arg = args[0].row_key
        mock_val = b"row_key_blob"
        assert arg == mock_val
        arg = args[0].rules
        mock_val = [data.ReadModifyWriteRule(family_name="family_name_value")]
        assert arg == mock_val
        arg = args[0].app_profile_id
        mock_val = "app_profile_id_value"
        assert arg == mock_val


def test_read_modify_write_row_flattened_error():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.read_modify_write_row(
            bigtable.ReadModifyWriteRowRequest(),
            table_name="table_name_value",
            row_key=b"row_key_blob",
            rules=[data.ReadModifyWriteRule(family_name="family_name_value")],
            app_profile_id="app_profile_id_value",
        )


@pytest.mark.asyncio
async def test_read_modify_write_row_flattened_async():
    client = BigtableAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_modify_write_row), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable.ReadModifyWriteRowResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable.ReadModifyWriteRowResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.read_modify_write_row(
            table_name="table_name_value",
            row_key=b"row_key_blob",
            rules=[data.ReadModifyWriteRule(family_name="family_name_value")],
            app_profile_id="app_profile_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].table_name
        mock_val = "table_name_value"
        assert arg == mock_val
        arg = args[0].row_key
        mock_val = b"row_key_blob"
        assert arg == mock_val
        arg = args[0].rules
        mock_val = [data.ReadModifyWriteRule(family_name="family_name_value")]
        assert arg == mock_val
        arg = args[0].app_profile_id
        mock_val = "app_profile_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_read_modify_write_row_flattened_error_async():
    client = BigtableAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.read_modify_write_row(
            bigtable.ReadModifyWriteRowRequest(),
            table_name="table_name_value",
            row_key=b"row_key_blob",
            rules=[data.ReadModifyWriteRule(family_name="family_name_value")],
            app_profile_id="app_profile_id_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.BigtableGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BigtableClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.BigtableGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BigtableClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.BigtableGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = BigtableClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = BigtableClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.BigtableGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BigtableClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.BigtableGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = BigtableClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.BigtableGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.BigtableGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.BigtableGrpcTransport,
        transports.BigtableGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.BigtableGrpcTransport,
    )


def test_bigtable_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.BigtableTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_bigtable_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.bigtable_v2.services.bigtable.transports.BigtableTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.BigtableTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "read_rows",
        "sample_row_keys",
        "mutate_row",
        "mutate_rows",
        "check_and_mutate_row",
        "ping_and_warm",
        "read_modify_write_row",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()


def test_bigtable_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.bigtable_v2.services.bigtable.transports.BigtableTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.BigtableTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/bigtable.data",
                "https://www.googleapis.com/auth/bigtable.data.readonly",
                "https://www.googleapis.com/auth/cloud-bigtable.data",
                "https://www.googleapis.com/auth/cloud-bigtable.data.readonly",
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            quota_project_id="octopus",
        )


def test_bigtable_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.bigtable_v2.services.bigtable.transports.BigtableTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.BigtableTransport()
        adc.assert_called_once()


def test_bigtable_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        BigtableClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/bigtable.data",
                "https://www.googleapis.com/auth/bigtable.data.readonly",
                "https://www.googleapis.com/auth/cloud-bigtable.data",
                "https://www.googleapis.com/auth/cloud-bigtable.data.readonly",
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.BigtableGrpcTransport,
        transports.BigtableGrpcAsyncIOTransport,
    ],
)
def test_bigtable_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/bigtable.data",
                "https://www.googleapis.com/auth/bigtable.data.readonly",
                "https://www.googleapis.com/auth/cloud-bigtable.data",
                "https://www.googleapis.com/auth/cloud-bigtable.data.readonly",
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.BigtableGrpcTransport, grpc_helpers),
        (transports.BigtableGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_bigtable_transport_create_channel(transport_class, grpc_helpers):
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
            "bigtable.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/bigtable.data",
                "https://www.googleapis.com/auth/bigtable.data.readonly",
                "https://www.googleapis.com/auth/cloud-bigtable.data",
                "https://www.googleapis.com/auth/cloud-bigtable.data.readonly",
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            scopes=["1", "2"],
            default_host="bigtable.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.BigtableGrpcTransport, transports.BigtableGrpcAsyncIOTransport],
)
def test_bigtable_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_bigtable_host_no_port():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="bigtable.googleapis.com"
        ),
    )
    assert client.transport._host == "bigtable.googleapis.com:443"


def test_bigtable_host_with_port():
    client = BigtableClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="bigtable.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "bigtable.googleapis.com:8000"


def test_bigtable_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.BigtableGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_bigtable_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.BigtableGrpcAsyncIOTransport(
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
    [transports.BigtableGrpcTransport, transports.BigtableGrpcAsyncIOTransport],
)
def test_bigtable_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.BigtableGrpcTransport, transports.BigtableGrpcAsyncIOTransport],
)
def test_bigtable_transport_channel_mtls_with_adc(transport_class):
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


def test_instance_path():
    project = "squid"
    instance = "clam"
    expected = "projects/{project}/instances/{instance}".format(
        project=project,
        instance=instance,
    )
    actual = BigtableClient.instance_path(project, instance)
    assert expected == actual


def test_parse_instance_path():
    expected = {
        "project": "whelk",
        "instance": "octopus",
    }
    path = BigtableClient.instance_path(**expected)

    # Check that the path construction is reversible.
    actual = BigtableClient.parse_instance_path(path)
    assert expected == actual


def test_table_path():
    project = "oyster"
    instance = "nudibranch"
    table = "cuttlefish"
    expected = "projects/{project}/instances/{instance}/tables/{table}".format(
        project=project,
        instance=instance,
        table=table,
    )
    actual = BigtableClient.table_path(project, instance, table)
    assert expected == actual


def test_parse_table_path():
    expected = {
        "project": "mussel",
        "instance": "winkle",
        "table": "nautilus",
    }
    path = BigtableClient.table_path(**expected)

    # Check that the path construction is reversible.
    actual = BigtableClient.parse_table_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "scallop"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = BigtableClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "abalone",
    }
    path = BigtableClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = BigtableClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "squid"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = BigtableClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "clam",
    }
    path = BigtableClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = BigtableClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "whelk"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = BigtableClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "octopus",
    }
    path = BigtableClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = BigtableClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "oyster"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = BigtableClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nudibranch",
    }
    path = BigtableClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = BigtableClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "cuttlefish"
    location = "mussel"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = BigtableClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
    }
    path = BigtableClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = BigtableClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.BigtableTransport, "_prep_wrapped_messages"
    ) as prep:
        client = BigtableClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.BigtableTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = BigtableClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = BigtableAsyncClient(
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
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = BigtableClient(
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
        "grpc",
    ]
    for transport in transports:
        client = BigtableClient(
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
        (BigtableClient, transports.BigtableGrpcTransport),
        (BigtableAsyncClient, transports.BigtableGrpcAsyncIOTransport),
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
            )
