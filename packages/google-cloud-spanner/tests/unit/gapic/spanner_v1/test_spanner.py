# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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

from google import auth
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.spanner_v1.services.spanner import SpannerAsyncClient
from google.cloud.spanner_v1.services.spanner import SpannerClient
from google.cloud.spanner_v1.services.spanner import pagers
from google.cloud.spanner_v1.services.spanner import transports
from google.cloud.spanner_v1.types import keys
from google.cloud.spanner_v1.types import mutation
from google.cloud.spanner_v1.types import result_set
from google.cloud.spanner_v1.types import spanner
from google.cloud.spanner_v1.types import transaction
from google.cloud.spanner_v1.types import type as gs_type
from google.oauth2 import service_account
from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import struct_pb2 as struct  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.rpc import status_pb2 as status  # type: ignore


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

    assert SpannerClient._get_default_mtls_endpoint(None) is None
    assert SpannerClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert (
        SpannerClient._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    )
    assert (
        SpannerClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        SpannerClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert SpannerClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [SpannerClient, SpannerAsyncClient])
def test_spanner_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds

        assert client.transport._host == "spanner.googleapis.com:443"


def test_spanner_client_get_transport_class():
    transport = SpannerClient.get_transport_class()
    assert transport == transports.SpannerGrpcTransport

    transport = SpannerClient.get_transport_class("grpc")
    assert transport == transports.SpannerGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (SpannerClient, transports.SpannerGrpcTransport, "grpc"),
        (SpannerAsyncClient, transports.SpannerGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
@mock.patch.object(
    SpannerClient, "DEFAULT_ENDPOINT", modify_default_endpoint(SpannerClient)
)
@mock.patch.object(
    SpannerAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(SpannerAsyncClient)
)
def test_spanner_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(SpannerClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(SpannerClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                ssl_channel_credentials=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                ssl_channel_credentials=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class()

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class()

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (SpannerClient, transports.SpannerGrpcTransport, "grpc", "true"),
        (
            SpannerAsyncClient,
            transports.SpannerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (SpannerClient, transports.SpannerGrpcTransport, "grpc", "false"),
        (
            SpannerAsyncClient,
            transports.SpannerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    SpannerClient, "DEFAULT_ENDPOINT", modify_default_endpoint(SpannerClient)
)
@mock.patch.object(
    SpannerAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(SpannerAsyncClient)
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_spanner_client_mtls_env_auto(
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
            ssl_channel_creds = mock.Mock()
            with mock.patch(
                "grpc.ssl_channel_credentials", return_value=ssl_channel_creds
            ):
                patched.return_value = None
                client = client_class(client_options=options)

                if use_client_cert_env == "false":
                    expected_ssl_channel_creds = None
                    expected_host = client.DEFAULT_ENDPOINT
                else:
                    expected_ssl_channel_creds = ssl_channel_creds
                    expected_host = client.DEFAULT_MTLS_ENDPOINT

                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=expected_host,
                    scopes=None,
                    ssl_channel_credentials=expected_ssl_channel_creds,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    with mock.patch(
                        "google.auth.transport.grpc.SslCredentials.ssl_credentials",
                        new_callable=mock.PropertyMock,
                    ) as ssl_credentials_mock:
                        if use_client_cert_env == "false":
                            is_mtls_mock.return_value = False
                            ssl_credentials_mock.return_value = None
                            expected_host = client.DEFAULT_ENDPOINT
                            expected_ssl_channel_creds = None
                        else:
                            is_mtls_mock.return_value = True
                            ssl_credentials_mock.return_value = mock.Mock()
                            expected_host = client.DEFAULT_MTLS_ENDPOINT
                            expected_ssl_channel_creds = (
                                ssl_credentials_mock.return_value
                            )

                        patched.return_value = None
                        client = client_class()
                        patched.assert_called_once_with(
                            credentials=None,
                            credentials_file=None,
                            host=expected_host,
                            scopes=None,
                            ssl_channel_credentials=expected_ssl_channel_creds,
                            quota_project_id=None,
                            client_info=transports.base.DEFAULT_CLIENT_INFO,
                        )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    is_mtls_mock.return_value = False
                    patched.return_value = None
                    client = client_class()
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=client.DEFAULT_ENDPOINT,
                        scopes=None,
                        ssl_channel_credentials=None,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                    )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (SpannerClient, transports.SpannerGrpcTransport, "grpc"),
        (SpannerAsyncClient, transports.SpannerGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_spanner_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (SpannerClient, transports.SpannerGrpcTransport, "grpc"),
        (SpannerAsyncClient, transports.SpannerGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_spanner_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_spanner_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.spanner_v1.services.spanner.transports.SpannerGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = SpannerClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_create_session(
    transport: str = "grpc", request_type=spanner.CreateSessionRequest
):
    client = SpannerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_session), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = spanner.Session(name="name_value",)

        response = client.create_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.CreateSessionRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, spanner.Session)

    assert response.name == "name_value"


def test_create_session_from_dict():
    test_create_session(request_type=dict)


@pytest.mark.asyncio
async def test_create_session_async(
    transport: str = "grpc_asyncio", request_type=spanner.CreateSessionRequest
):
    client = SpannerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_session), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            spanner.Session(name="name_value",)
        )

        response = await client.create_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.CreateSessionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, spanner.Session)

    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_create_session_async_from_dict():
    await test_create_session_async(request_type=dict)


def test_create_session_field_headers():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.CreateSessionRequest()
    request.database = "database/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_session), "__call__") as call:
        call.return_value = spanner.Session()

        client.create_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "database=database/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_session_field_headers_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.CreateSessionRequest()
    request.database = "database/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_session), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(spanner.Session())

        await client.create_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "database=database/value",) in kw["metadata"]


def test_create_session_flattened():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_session), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = spanner.Session()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_session(database="database_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].database == "database_value"


def test_create_session_flattened_error():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_session(
            spanner.CreateSessionRequest(), database="database_value",
        )


@pytest.mark.asyncio
async def test_create_session_flattened_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_session), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = spanner.Session()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(spanner.Session())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_session(database="database_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].database == "database_value"


@pytest.mark.asyncio
async def test_create_session_flattened_error_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_session(
            spanner.CreateSessionRequest(), database="database_value",
        )


def test_batch_create_sessions(
    transport: str = "grpc", request_type=spanner.BatchCreateSessionsRequest
):
    client = SpannerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_sessions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = spanner.BatchCreateSessionsResponse()

        response = client.batch_create_sessions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.BatchCreateSessionsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, spanner.BatchCreateSessionsResponse)


def test_batch_create_sessions_from_dict():
    test_batch_create_sessions(request_type=dict)


@pytest.mark.asyncio
async def test_batch_create_sessions_async(
    transport: str = "grpc_asyncio", request_type=spanner.BatchCreateSessionsRequest
):
    client = SpannerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_sessions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            spanner.BatchCreateSessionsResponse()
        )

        response = await client.batch_create_sessions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.BatchCreateSessionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, spanner.BatchCreateSessionsResponse)


@pytest.mark.asyncio
async def test_batch_create_sessions_async_from_dict():
    await test_batch_create_sessions_async(request_type=dict)


def test_batch_create_sessions_field_headers():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.BatchCreateSessionsRequest()
    request.database = "database/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_sessions), "__call__"
    ) as call:
        call.return_value = spanner.BatchCreateSessionsResponse()

        client.batch_create_sessions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "database=database/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_create_sessions_field_headers_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.BatchCreateSessionsRequest()
    request.database = "database/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_sessions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            spanner.BatchCreateSessionsResponse()
        )

        await client.batch_create_sessions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "database=database/value",) in kw["metadata"]


def test_batch_create_sessions_flattened():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_sessions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = spanner.BatchCreateSessionsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.batch_create_sessions(
            database="database_value", session_count=1420,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].database == "database_value"

        assert args[0].session_count == 1420


def test_batch_create_sessions_flattened_error():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.batch_create_sessions(
            spanner.BatchCreateSessionsRequest(),
            database="database_value",
            session_count=1420,
        )


@pytest.mark.asyncio
async def test_batch_create_sessions_flattened_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_sessions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = spanner.BatchCreateSessionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            spanner.BatchCreateSessionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.batch_create_sessions(
            database="database_value", session_count=1420,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].database == "database_value"

        assert args[0].session_count == 1420


@pytest.mark.asyncio
async def test_batch_create_sessions_flattened_error_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.batch_create_sessions(
            spanner.BatchCreateSessionsRequest(),
            database="database_value",
            session_count=1420,
        )


def test_get_session(transport: str = "grpc", request_type=spanner.GetSessionRequest):
    client = SpannerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_session), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = spanner.Session(name="name_value",)

        response = client.get_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.GetSessionRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, spanner.Session)

    assert response.name == "name_value"


def test_get_session_from_dict():
    test_get_session(request_type=dict)


@pytest.mark.asyncio
async def test_get_session_async(
    transport: str = "grpc_asyncio", request_type=spanner.GetSessionRequest
):
    client = SpannerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_session), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            spanner.Session(name="name_value",)
        )

        response = await client.get_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.GetSessionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, spanner.Session)

    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_get_session_async_from_dict():
    await test_get_session_async(request_type=dict)


def test_get_session_field_headers():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.GetSessionRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_session), "__call__") as call:
        call.return_value = spanner.Session()

        client.get_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_session_field_headers_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.GetSessionRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_session), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(spanner.Session())

        await client.get_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_session_flattened():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_session), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = spanner.Session()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_session(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_session_flattened_error():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_session(
            spanner.GetSessionRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_session_flattened_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_session), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = spanner.Session()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(spanner.Session())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_session(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_session_flattened_error_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_session(
            spanner.GetSessionRequest(), name="name_value",
        )


def test_list_sessions(
    transport: str = "grpc", request_type=spanner.ListSessionsRequest
):
    client = SpannerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sessions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = spanner.ListSessionsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_sessions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.ListSessionsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pagers.ListSessionsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_sessions_from_dict():
    test_list_sessions(request_type=dict)


@pytest.mark.asyncio
async def test_list_sessions_async(
    transport: str = "grpc_asyncio", request_type=spanner.ListSessionsRequest
):
    client = SpannerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sessions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            spanner.ListSessionsResponse(next_page_token="next_page_token_value",)
        )

        response = await client.list_sessions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.ListSessionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSessionsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_sessions_async_from_dict():
    await test_list_sessions_async(request_type=dict)


def test_list_sessions_field_headers():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.ListSessionsRequest()
    request.database = "database/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sessions), "__call__") as call:
        call.return_value = spanner.ListSessionsResponse()

        client.list_sessions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "database=database/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_sessions_field_headers_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.ListSessionsRequest()
    request.database = "database/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sessions), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            spanner.ListSessionsResponse()
        )

        await client.list_sessions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "database=database/value",) in kw["metadata"]


def test_list_sessions_flattened():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sessions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = spanner.ListSessionsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_sessions(database="database_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].database == "database_value"


def test_list_sessions_flattened_error():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_sessions(
            spanner.ListSessionsRequest(), database="database_value",
        )


@pytest.mark.asyncio
async def test_list_sessions_flattened_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sessions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = spanner.ListSessionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            spanner.ListSessionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_sessions(database="database_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].database == "database_value"


@pytest.mark.asyncio
async def test_list_sessions_flattened_error_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_sessions(
            spanner.ListSessionsRequest(), database="database_value",
        )


def test_list_sessions_pager():
    client = SpannerClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sessions), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            spanner.ListSessionsResponse(
                sessions=[spanner.Session(), spanner.Session(), spanner.Session(),],
                next_page_token="abc",
            ),
            spanner.ListSessionsResponse(sessions=[], next_page_token="def",),
            spanner.ListSessionsResponse(
                sessions=[spanner.Session(),], next_page_token="ghi",
            ),
            spanner.ListSessionsResponse(
                sessions=[spanner.Session(), spanner.Session(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("database", ""),)),
        )
        pager = client.list_sessions(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, spanner.Session) for i in results)


def test_list_sessions_pages():
    client = SpannerClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sessions), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            spanner.ListSessionsResponse(
                sessions=[spanner.Session(), spanner.Session(), spanner.Session(),],
                next_page_token="abc",
            ),
            spanner.ListSessionsResponse(sessions=[], next_page_token="def",),
            spanner.ListSessionsResponse(
                sessions=[spanner.Session(),], next_page_token="ghi",
            ),
            spanner.ListSessionsResponse(
                sessions=[spanner.Session(), spanner.Session(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_sessions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_sessions_async_pager():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_sessions), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            spanner.ListSessionsResponse(
                sessions=[spanner.Session(), spanner.Session(), spanner.Session(),],
                next_page_token="abc",
            ),
            spanner.ListSessionsResponse(sessions=[], next_page_token="def",),
            spanner.ListSessionsResponse(
                sessions=[spanner.Session(),], next_page_token="ghi",
            ),
            spanner.ListSessionsResponse(
                sessions=[spanner.Session(), spanner.Session(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_sessions(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, spanner.Session) for i in responses)


@pytest.mark.asyncio
async def test_list_sessions_async_pages():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_sessions), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            spanner.ListSessionsResponse(
                sessions=[spanner.Session(), spanner.Session(), spanner.Session(),],
                next_page_token="abc",
            ),
            spanner.ListSessionsResponse(sessions=[], next_page_token="def",),
            spanner.ListSessionsResponse(
                sessions=[spanner.Session(),], next_page_token="ghi",
            ),
            spanner.ListSessionsResponse(
                sessions=[spanner.Session(), spanner.Session(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_sessions(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_delete_session(
    transport: str = "grpc", request_type=spanner.DeleteSessionRequest
):
    client = SpannerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_session), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.DeleteSessionRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_session_from_dict():
    test_delete_session(request_type=dict)


@pytest.mark.asyncio
async def test_delete_session_async(
    transport: str = "grpc_asyncio", request_type=spanner.DeleteSessionRequest
):
    client = SpannerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_session), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.DeleteSessionRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_session_async_from_dict():
    await test_delete_session_async(request_type=dict)


def test_delete_session_field_headers():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.DeleteSessionRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_session), "__call__") as call:
        call.return_value = None

        client.delete_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_session_field_headers_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.DeleteSessionRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_session), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_session_flattened():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_session), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_session(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_session_flattened_error():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_session(
            spanner.DeleteSessionRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_session_flattened_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_session), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_session(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_session_flattened_error_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_session(
            spanner.DeleteSessionRequest(), name="name_value",
        )


def test_execute_sql(transport: str = "grpc", request_type=spanner.ExecuteSqlRequest):
    client = SpannerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.execute_sql), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = result_set.ResultSet()

        response = client.execute_sql(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.ExecuteSqlRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, result_set.ResultSet)


def test_execute_sql_from_dict():
    test_execute_sql(request_type=dict)


@pytest.mark.asyncio
async def test_execute_sql_async(
    transport: str = "grpc_asyncio", request_type=spanner.ExecuteSqlRequest
):
    client = SpannerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.execute_sql), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            result_set.ResultSet()
        )

        response = await client.execute_sql(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.ExecuteSqlRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, result_set.ResultSet)


@pytest.mark.asyncio
async def test_execute_sql_async_from_dict():
    await test_execute_sql_async(request_type=dict)


def test_execute_sql_field_headers():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.ExecuteSqlRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.execute_sql), "__call__") as call:
        call.return_value = result_set.ResultSet()

        client.execute_sql(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_execute_sql_field_headers_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.ExecuteSqlRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.execute_sql), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            result_set.ResultSet()
        )

        await client.execute_sql(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


def test_execute_streaming_sql(
    transport: str = "grpc", request_type=spanner.ExecuteSqlRequest
):
    client = SpannerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.execute_streaming_sql), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([result_set.PartialResultSet()])

        response = client.execute_streaming_sql(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.ExecuteSqlRequest()

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, result_set.PartialResultSet)


def test_execute_streaming_sql_from_dict():
    test_execute_streaming_sql(request_type=dict)


@pytest.mark.asyncio
async def test_execute_streaming_sql_async(
    transport: str = "grpc_asyncio", request_type=spanner.ExecuteSqlRequest
):
    client = SpannerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.execute_streaming_sql), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[result_set.PartialResultSet()]
        )

        response = await client.execute_streaming_sql(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.ExecuteSqlRequest()

    # Establish that the response is the type that we expect.
    message = await response.read()
    assert isinstance(message, result_set.PartialResultSet)


@pytest.mark.asyncio
async def test_execute_streaming_sql_async_from_dict():
    await test_execute_streaming_sql_async(request_type=dict)


def test_execute_streaming_sql_field_headers():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.ExecuteSqlRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.execute_streaming_sql), "__call__"
    ) as call:
        call.return_value = iter([result_set.PartialResultSet()])

        client.execute_streaming_sql(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_execute_streaming_sql_field_headers_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.ExecuteSqlRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.execute_streaming_sql), "__call__"
    ) as call:
        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[result_set.PartialResultSet()]
        )

        await client.execute_streaming_sql(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


def test_execute_batch_dml(
    transport: str = "grpc", request_type=spanner.ExecuteBatchDmlRequest
):
    client = SpannerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.execute_batch_dml), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = spanner.ExecuteBatchDmlResponse()

        response = client.execute_batch_dml(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.ExecuteBatchDmlRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, spanner.ExecuteBatchDmlResponse)


def test_execute_batch_dml_from_dict():
    test_execute_batch_dml(request_type=dict)


@pytest.mark.asyncio
async def test_execute_batch_dml_async(
    transport: str = "grpc_asyncio", request_type=spanner.ExecuteBatchDmlRequest
):
    client = SpannerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.execute_batch_dml), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            spanner.ExecuteBatchDmlResponse()
        )

        response = await client.execute_batch_dml(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.ExecuteBatchDmlRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, spanner.ExecuteBatchDmlResponse)


@pytest.mark.asyncio
async def test_execute_batch_dml_async_from_dict():
    await test_execute_batch_dml_async(request_type=dict)


def test_execute_batch_dml_field_headers():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.ExecuteBatchDmlRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.execute_batch_dml), "__call__"
    ) as call:
        call.return_value = spanner.ExecuteBatchDmlResponse()

        client.execute_batch_dml(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_execute_batch_dml_field_headers_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.ExecuteBatchDmlRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.execute_batch_dml), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            spanner.ExecuteBatchDmlResponse()
        )

        await client.execute_batch_dml(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


def test_read(transport: str = "grpc", request_type=spanner.ReadRequest):
    client = SpannerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = result_set.ResultSet()

        response = client.read(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.ReadRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, result_set.ResultSet)


def test_read_from_dict():
    test_read(request_type=dict)


@pytest.mark.asyncio
async def test_read_async(
    transport: str = "grpc_asyncio", request_type=spanner.ReadRequest
):
    client = SpannerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            result_set.ResultSet()
        )

        response = await client.read(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.ReadRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, result_set.ResultSet)


@pytest.mark.asyncio
async def test_read_async_from_dict():
    await test_read_async(request_type=dict)


def test_read_field_headers():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.ReadRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read), "__call__") as call:
        call.return_value = result_set.ResultSet()

        client.read(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_read_field_headers_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.ReadRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            result_set.ResultSet()
        )

        await client.read(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


def test_streaming_read(transport: str = "grpc", request_type=spanner.ReadRequest):
    client = SpannerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.streaming_read), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([result_set.PartialResultSet()])

        response = client.streaming_read(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.ReadRequest()

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, result_set.PartialResultSet)


def test_streaming_read_from_dict():
    test_streaming_read(request_type=dict)


@pytest.mark.asyncio
async def test_streaming_read_async(
    transport: str = "grpc_asyncio", request_type=spanner.ReadRequest
):
    client = SpannerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.streaming_read), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[result_set.PartialResultSet()]
        )

        response = await client.streaming_read(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.ReadRequest()

    # Establish that the response is the type that we expect.
    message = await response.read()
    assert isinstance(message, result_set.PartialResultSet)


@pytest.mark.asyncio
async def test_streaming_read_async_from_dict():
    await test_streaming_read_async(request_type=dict)


def test_streaming_read_field_headers():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.ReadRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.streaming_read), "__call__") as call:
        call.return_value = iter([result_set.PartialResultSet()])

        client.streaming_read(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_streaming_read_field_headers_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.ReadRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.streaming_read), "__call__") as call:
        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[result_set.PartialResultSet()]
        )

        await client.streaming_read(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


def test_begin_transaction(
    transport: str = "grpc", request_type=spanner.BeginTransactionRequest
):
    client = SpannerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.begin_transaction), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = transaction.Transaction(id=b"id_blob",)

        response = client.begin_transaction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.BeginTransactionRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, transaction.Transaction)

    assert response.id == b"id_blob"


def test_begin_transaction_from_dict():
    test_begin_transaction(request_type=dict)


@pytest.mark.asyncio
async def test_begin_transaction_async(
    transport: str = "grpc_asyncio", request_type=spanner.BeginTransactionRequest
):
    client = SpannerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.begin_transaction), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transaction.Transaction(id=b"id_blob",)
        )

        response = await client.begin_transaction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.BeginTransactionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, transaction.Transaction)

    assert response.id == b"id_blob"


@pytest.mark.asyncio
async def test_begin_transaction_async_from_dict():
    await test_begin_transaction_async(request_type=dict)


def test_begin_transaction_field_headers():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.BeginTransactionRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.begin_transaction), "__call__"
    ) as call:
        call.return_value = transaction.Transaction()

        client.begin_transaction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_begin_transaction_field_headers_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.BeginTransactionRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.begin_transaction), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transaction.Transaction()
        )

        await client.begin_transaction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


def test_begin_transaction_flattened():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.begin_transaction), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = transaction.Transaction()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.begin_transaction(
            session="session_value",
            options=transaction.TransactionOptions(read_write=None),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].session == "session_value"

        assert args[0].options == transaction.TransactionOptions(read_write=None)


def test_begin_transaction_flattened_error():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.begin_transaction(
            spanner.BeginTransactionRequest(),
            session="session_value",
            options=transaction.TransactionOptions(read_write=None),
        )


@pytest.mark.asyncio
async def test_begin_transaction_flattened_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.begin_transaction), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = transaction.Transaction()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transaction.Transaction()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.begin_transaction(
            session="session_value",
            options=transaction.TransactionOptions(read_write=None),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].session == "session_value"

        assert args[0].options == transaction.TransactionOptions(read_write=None)


@pytest.mark.asyncio
async def test_begin_transaction_flattened_error_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.begin_transaction(
            spanner.BeginTransactionRequest(),
            session="session_value",
            options=transaction.TransactionOptions(read_write=None),
        )


def test_commit(transport: str = "grpc", request_type=spanner.CommitRequest):
    client = SpannerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = spanner.CommitResponse()

        response = client.commit(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.CommitRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, spanner.CommitResponse)


def test_commit_from_dict():
    test_commit(request_type=dict)


@pytest.mark.asyncio
async def test_commit_async(
    transport: str = "grpc_asyncio", request_type=spanner.CommitRequest
):
    client = SpannerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            spanner.CommitResponse()
        )

        response = await client.commit(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.CommitRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, spanner.CommitResponse)


@pytest.mark.asyncio
async def test_commit_async_from_dict():
    await test_commit_async(request_type=dict)


def test_commit_field_headers():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.CommitRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit), "__call__") as call:
        call.return_value = spanner.CommitResponse()

        client.commit(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_commit_field_headers_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.CommitRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            spanner.CommitResponse()
        )

        await client.commit(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


def test_commit_flattened():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = spanner.CommitResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.commit(
            session="session_value",
            transaction_id=b"transaction_id_blob",
            mutations=[
                mutation.Mutation(insert=mutation.Mutation.Write(table="table_value"))
            ],
            single_use_transaction=transaction.TransactionOptions(read_write=None),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].session == "session_value"

        assert args[0].mutations == [
            mutation.Mutation(insert=mutation.Mutation.Write(table="table_value"))
        ]

        assert args[0].single_use_transaction == transaction.TransactionOptions(
            read_write=None
        )


def test_commit_flattened_error():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.commit(
            spanner.CommitRequest(),
            session="session_value",
            transaction_id=b"transaction_id_blob",
            mutations=[
                mutation.Mutation(insert=mutation.Mutation.Write(table="table_value"))
            ],
            single_use_transaction=transaction.TransactionOptions(read_write=None),
        )


@pytest.mark.asyncio
async def test_commit_flattened_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = spanner.CommitResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            spanner.CommitResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.commit(
            session="session_value",
            transaction_id=b"transaction_id_blob",
            mutations=[
                mutation.Mutation(insert=mutation.Mutation.Write(table="table_value"))
            ],
            single_use_transaction=transaction.TransactionOptions(read_write=None),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].session == "session_value"

        assert args[0].mutations == [
            mutation.Mutation(insert=mutation.Mutation.Write(table="table_value"))
        ]

        assert args[0].single_use_transaction == transaction.TransactionOptions(
            read_write=None
        )


@pytest.mark.asyncio
async def test_commit_flattened_error_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.commit(
            spanner.CommitRequest(),
            session="session_value",
            transaction_id=b"transaction_id_blob",
            mutations=[
                mutation.Mutation(insert=mutation.Mutation.Write(table="table_value"))
            ],
            single_use_transaction=transaction.TransactionOptions(read_write=None),
        )


def test_rollback(transport: str = "grpc", request_type=spanner.RollbackRequest):
    client = SpannerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.rollback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.RollbackRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_rollback_from_dict():
    test_rollback(request_type=dict)


@pytest.mark.asyncio
async def test_rollback_async(
    transport: str = "grpc_asyncio", request_type=spanner.RollbackRequest
):
    client = SpannerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.rollback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.RollbackRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_rollback_async_from_dict():
    await test_rollback_async(request_type=dict)


def test_rollback_field_headers():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.RollbackRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback), "__call__") as call:
        call.return_value = None

        client.rollback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_rollback_field_headers_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.RollbackRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.rollback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


def test_rollback_flattened():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.rollback(
            session="session_value", transaction_id=b"transaction_id_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].session == "session_value"

        assert args[0].transaction_id == b"transaction_id_blob"


def test_rollback_flattened_error():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.rollback(
            spanner.RollbackRequest(),
            session="session_value",
            transaction_id=b"transaction_id_blob",
        )


@pytest.mark.asyncio
async def test_rollback_flattened_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.rollback(
            session="session_value", transaction_id=b"transaction_id_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].session == "session_value"

        assert args[0].transaction_id == b"transaction_id_blob"


@pytest.mark.asyncio
async def test_rollback_flattened_error_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.rollback(
            spanner.RollbackRequest(),
            session="session_value",
            transaction_id=b"transaction_id_blob",
        )


def test_partition_query(
    transport: str = "grpc", request_type=spanner.PartitionQueryRequest
):
    client = SpannerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.partition_query), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = spanner.PartitionResponse()

        response = client.partition_query(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.PartitionQueryRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, spanner.PartitionResponse)


def test_partition_query_from_dict():
    test_partition_query(request_type=dict)


@pytest.mark.asyncio
async def test_partition_query_async(
    transport: str = "grpc_asyncio", request_type=spanner.PartitionQueryRequest
):
    client = SpannerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.partition_query), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            spanner.PartitionResponse()
        )

        response = await client.partition_query(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.PartitionQueryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, spanner.PartitionResponse)


@pytest.mark.asyncio
async def test_partition_query_async_from_dict():
    await test_partition_query_async(request_type=dict)


def test_partition_query_field_headers():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.PartitionQueryRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.partition_query), "__call__") as call:
        call.return_value = spanner.PartitionResponse()

        client.partition_query(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_partition_query_field_headers_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.PartitionQueryRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.partition_query), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            spanner.PartitionResponse()
        )

        await client.partition_query(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


def test_partition_read(
    transport: str = "grpc", request_type=spanner.PartitionReadRequest
):
    client = SpannerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.partition_read), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = spanner.PartitionResponse()

        response = client.partition_read(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.PartitionReadRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, spanner.PartitionResponse)


def test_partition_read_from_dict():
    test_partition_read(request_type=dict)


@pytest.mark.asyncio
async def test_partition_read_async(
    transport: str = "grpc_asyncio", request_type=spanner.PartitionReadRequest
):
    client = SpannerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.partition_read), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            spanner.PartitionResponse()
        )

        response = await client.partition_read(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == spanner.PartitionReadRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, spanner.PartitionResponse)


@pytest.mark.asyncio
async def test_partition_read_async_from_dict():
    await test_partition_read_async(request_type=dict)


def test_partition_read_field_headers():
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.PartitionReadRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.partition_read), "__call__") as call:
        call.return_value = spanner.PartitionResponse()

        client.partition_read(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_partition_read_field_headers_async():
    client = SpannerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = spanner.PartitionReadRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.partition_read), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            spanner.PartitionResponse()
        )

        await client.partition_read(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.SpannerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SpannerClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.SpannerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SpannerClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.SpannerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SpannerClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.SpannerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = SpannerClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.SpannerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.SpannerGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.SpannerGrpcTransport, transports.SpannerGrpcAsyncIOTransport],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = SpannerClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.SpannerGrpcTransport,)


def test_spanner_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.SpannerTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_spanner_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.spanner_v1.services.spanner.transports.SpannerTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.SpannerTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_session",
        "batch_create_sessions",
        "get_session",
        "list_sessions",
        "delete_session",
        "execute_sql",
        "execute_streaming_sql",
        "execute_batch_dml",
        "read",
        "streaming_read",
        "begin_transaction",
        "commit",
        "rollback",
        "partition_query",
        "partition_read",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_spanner_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.spanner_v1.services.spanner.transports.SpannerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.SpannerTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/spanner.data",
            ),
            quota_project_id="octopus",
        )


def test_spanner_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.spanner_v1.services.spanner.transports.SpannerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.SpannerTransport()
        adc.assert_called_once()


def test_spanner_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        SpannerClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/spanner.data",
            ),
            quota_project_id=None,
        )


def test_spanner_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.SpannerGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/spanner.data",
            ),
            quota_project_id="octopus",
        )


def test_spanner_host_no_port():
    client = SpannerClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="spanner.googleapis.com"
        ),
    )
    assert client.transport._host == "spanner.googleapis.com:443"


def test_spanner_host_with_port():
    client = SpannerClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="spanner.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "spanner.googleapis.com:8000"


def test_spanner_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.SpannerGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"


def test_spanner_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.SpannerGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"


@pytest.mark.parametrize(
    "transport_class",
    [transports.SpannerGrpcTransport, transports.SpannerGrpcAsyncIOTransport],
)
def test_spanner_transport_channel_mtls_with_client_cert_source(transport_class):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(auth, "default") as adc:
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
                scopes=(
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/spanner.data",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.SpannerGrpcTransport, transports.SpannerGrpcAsyncIOTransport],
)
def test_spanner_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
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
                scopes=(
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/spanner.data",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_database_path():
    project = "squid"
    instance = "clam"
    database = "whelk"

    expected = "projects/{project}/instances/{instance}/databases/{database}".format(
        project=project, instance=instance, database=database,
    )
    actual = SpannerClient.database_path(project, instance, database)
    assert expected == actual


def test_parse_database_path():
    expected = {
        "project": "octopus",
        "instance": "oyster",
        "database": "nudibranch",
    }
    path = SpannerClient.database_path(**expected)

    # Check that the path construction is reversible.
    actual = SpannerClient.parse_database_path(path)
    assert expected == actual


def test_session_path():
    project = "cuttlefish"
    instance = "mussel"
    database = "winkle"
    session = "nautilus"

    expected = "projects/{project}/instances/{instance}/databases/{database}/sessions/{session}".format(
        project=project, instance=instance, database=database, session=session,
    )
    actual = SpannerClient.session_path(project, instance, database, session)
    assert expected == actual


def test_parse_session_path():
    expected = {
        "project": "scallop",
        "instance": "abalone",
        "database": "squid",
        "session": "clam",
    }
    path = SpannerClient.session_path(**expected)

    # Check that the path construction is reversible.
    actual = SpannerClient.parse_session_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = SpannerClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = SpannerClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = SpannerClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"

    expected = "folders/{folder}".format(folder=folder,)
    actual = SpannerClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = SpannerClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = SpannerClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = SpannerClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = SpannerClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = SpannerClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"

    expected = "projects/{project}".format(project=project,)
    actual = SpannerClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = SpannerClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = SpannerClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = SpannerClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = SpannerClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = SpannerClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.SpannerTransport, "_prep_wrapped_messages"
    ) as prep:
        client = SpannerClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.SpannerTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = SpannerClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
