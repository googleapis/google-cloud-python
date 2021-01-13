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
from google.cloud.bigquery_storage_v1beta2.services.big_query_write import (
    BigQueryWriteAsyncClient,
)
from google.cloud.bigquery_storage_v1beta2.services.big_query_write import (
    BigQueryWriteClient,
)
from google.cloud.bigquery_storage_v1beta2.services.big_query_write import transports
from google.cloud.bigquery_storage_v1beta2.types import protobuf
from google.cloud.bigquery_storage_v1beta2.types import storage
from google.cloud.bigquery_storage_v1beta2.types import stream
from google.cloud.bigquery_storage_v1beta2.types import table
from google.oauth2 import service_account
from google.protobuf import descriptor_pb2 as descriptor  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore
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

    assert BigQueryWriteClient._get_default_mtls_endpoint(None) is None
    assert (
        BigQueryWriteClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        BigQueryWriteClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        BigQueryWriteClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        BigQueryWriteClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        BigQueryWriteClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


def test_big_query_write_client_from_service_account_info():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = BigQueryWriteClient.from_service_account_info(info)
        assert client.transport._credentials == creds

        assert client.transport._host == "bigquerystorage.googleapis.com:443"


@pytest.mark.parametrize(
    "client_class", [BigQueryWriteClient, BigQueryWriteAsyncClient,]
)
def test_big_query_write_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds

        assert client.transport._host == "bigquerystorage.googleapis.com:443"


def test_big_query_write_client_get_transport_class():
    transport = BigQueryWriteClient.get_transport_class()
    available_transports = [
        transports.BigQueryWriteGrpcTransport,
    ]
    assert transport in available_transports

    transport = BigQueryWriteClient.get_transport_class("grpc")
    assert transport == transports.BigQueryWriteGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (BigQueryWriteClient, transports.BigQueryWriteGrpcTransport, "grpc"),
        (
            BigQueryWriteAsyncClient,
            transports.BigQueryWriteGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    BigQueryWriteClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BigQueryWriteClient),
)
@mock.patch.object(
    BigQueryWriteAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BigQueryWriteAsyncClient),
)
def test_big_query_write_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(BigQueryWriteClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(BigQueryWriteClient, "get_transport_class") as gtc:
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
        (BigQueryWriteClient, transports.BigQueryWriteGrpcTransport, "grpc", "true"),
        (
            BigQueryWriteAsyncClient,
            transports.BigQueryWriteGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (BigQueryWriteClient, transports.BigQueryWriteGrpcTransport, "grpc", "false"),
        (
            BigQueryWriteAsyncClient,
            transports.BigQueryWriteGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    BigQueryWriteClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BigQueryWriteClient),
)
@mock.patch.object(
    BigQueryWriteAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BigQueryWriteAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_big_query_write_client_mtls_env_auto(
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
        (BigQueryWriteClient, transports.BigQueryWriteGrpcTransport, "grpc"),
        (
            BigQueryWriteAsyncClient,
            transports.BigQueryWriteGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_big_query_write_client_client_options_scopes(
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
        (BigQueryWriteClient, transports.BigQueryWriteGrpcTransport, "grpc"),
        (
            BigQueryWriteAsyncClient,
            transports.BigQueryWriteGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_big_query_write_client_client_options_credentials_file(
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


def test_big_query_write_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.bigquery_storage_v1beta2.services.big_query_write.transports.BigQueryWriteGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = BigQueryWriteClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_create_write_stream(
    transport: str = "grpc", request_type=storage.CreateWriteStreamRequest
):
    client = BigQueryWriteClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_write_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = stream.WriteStream(
            name="name_value", type_=stream.WriteStream.Type.COMMITTED,
        )

        response = client.create_write_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == storage.CreateWriteStreamRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, stream.WriteStream)

    assert response.name == "name_value"

    assert response.type_ == stream.WriteStream.Type.COMMITTED


def test_create_write_stream_from_dict():
    test_create_write_stream(request_type=dict)


@pytest.mark.asyncio
async def test_create_write_stream_async(
    transport: str = "grpc_asyncio", request_type=storage.CreateWriteStreamRequest
):
    client = BigQueryWriteAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_write_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            stream.WriteStream(
                name="name_value", type_=stream.WriteStream.Type.COMMITTED,
            )
        )

        response = await client.create_write_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == storage.CreateWriteStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, stream.WriteStream)

    assert response.name == "name_value"

    assert response.type_ == stream.WriteStream.Type.COMMITTED


@pytest.mark.asyncio
async def test_create_write_stream_async_from_dict():
    await test_create_write_stream_async(request_type=dict)


def test_create_write_stream_field_headers():
    client = BigQueryWriteClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.CreateWriteStreamRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_write_stream), "__call__"
    ) as call:
        call.return_value = stream.WriteStream()

        client.create_write_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_write_stream_field_headers_async():
    client = BigQueryWriteAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.CreateWriteStreamRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_write_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(stream.WriteStream())

        await client.create_write_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_write_stream_flattened():
    client = BigQueryWriteClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_write_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = stream.WriteStream()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_write_stream(
            parent="parent_value", write_stream=stream.WriteStream(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].write_stream == stream.WriteStream(name="name_value")


def test_create_write_stream_flattened_error():
    client = BigQueryWriteClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_write_stream(
            storage.CreateWriteStreamRequest(),
            parent="parent_value",
            write_stream=stream.WriteStream(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_write_stream_flattened_async():
    client = BigQueryWriteAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_write_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = stream.WriteStream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(stream.WriteStream())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_write_stream(
            parent="parent_value", write_stream=stream.WriteStream(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].write_stream == stream.WriteStream(name="name_value")


@pytest.mark.asyncio
async def test_create_write_stream_flattened_error_async():
    client = BigQueryWriteAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_write_stream(
            storage.CreateWriteStreamRequest(),
            parent="parent_value",
            write_stream=stream.WriteStream(name="name_value"),
        )


def test_append_rows(transport: str = "grpc", request_type=storage.AppendRowsRequest):
    client = BigQueryWriteClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.append_rows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([storage.AppendRowsResponse()])

        response = client.append_rows(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, storage.AppendRowsResponse)


def test_append_rows_from_dict():
    test_append_rows(request_type=dict)


@pytest.mark.asyncio
async def test_append_rows_async(
    transport: str = "grpc_asyncio", request_type=storage.AppendRowsRequest
):
    client = BigQueryWriteAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.append_rows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = mock.Mock(aio.StreamStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[storage.AppendRowsResponse()]
        )

        response = await client.append_rows(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    message = await response.read()
    assert isinstance(message, storage.AppendRowsResponse)


@pytest.mark.asyncio
async def test_append_rows_async_from_dict():
    await test_append_rows_async(request_type=dict)


def test_get_write_stream(
    transport: str = "grpc", request_type=storage.GetWriteStreamRequest
):
    client = BigQueryWriteClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_write_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = stream.WriteStream(
            name="name_value", type_=stream.WriteStream.Type.COMMITTED,
        )

        response = client.get_write_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == storage.GetWriteStreamRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, stream.WriteStream)

    assert response.name == "name_value"

    assert response.type_ == stream.WriteStream.Type.COMMITTED


def test_get_write_stream_from_dict():
    test_get_write_stream(request_type=dict)


@pytest.mark.asyncio
async def test_get_write_stream_async(
    transport: str = "grpc_asyncio", request_type=storage.GetWriteStreamRequest
):
    client = BigQueryWriteAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_write_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            stream.WriteStream(
                name="name_value", type_=stream.WriteStream.Type.COMMITTED,
            )
        )

        response = await client.get_write_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == storage.GetWriteStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, stream.WriteStream)

    assert response.name == "name_value"

    assert response.type_ == stream.WriteStream.Type.COMMITTED


@pytest.mark.asyncio
async def test_get_write_stream_async_from_dict():
    await test_get_write_stream_async(request_type=dict)


def test_get_write_stream_field_headers():
    client = BigQueryWriteClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.GetWriteStreamRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_write_stream), "__call__") as call:
        call.return_value = stream.WriteStream()

        client.get_write_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_write_stream_field_headers_async():
    client = BigQueryWriteAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.GetWriteStreamRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_write_stream), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(stream.WriteStream())

        await client.get_write_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_write_stream_flattened():
    client = BigQueryWriteClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_write_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = stream.WriteStream()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_write_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_write_stream_flattened_error():
    client = BigQueryWriteClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_write_stream(
            storage.GetWriteStreamRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_write_stream_flattened_async():
    client = BigQueryWriteAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_write_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = stream.WriteStream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(stream.WriteStream())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_write_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_write_stream_flattened_error_async():
    client = BigQueryWriteAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_write_stream(
            storage.GetWriteStreamRequest(), name="name_value",
        )


def test_finalize_write_stream(
    transport: str = "grpc", request_type=storage.FinalizeWriteStreamRequest
):
    client = BigQueryWriteClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.finalize_write_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.FinalizeWriteStreamResponse(row_count=992,)

        response = client.finalize_write_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == storage.FinalizeWriteStreamRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, storage.FinalizeWriteStreamResponse)

    assert response.row_count == 992


def test_finalize_write_stream_from_dict():
    test_finalize_write_stream(request_type=dict)


@pytest.mark.asyncio
async def test_finalize_write_stream_async(
    transport: str = "grpc_asyncio", request_type=storage.FinalizeWriteStreamRequest
):
    client = BigQueryWriteAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.finalize_write_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.FinalizeWriteStreamResponse(row_count=992,)
        )

        response = await client.finalize_write_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == storage.FinalizeWriteStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.FinalizeWriteStreamResponse)

    assert response.row_count == 992


@pytest.mark.asyncio
async def test_finalize_write_stream_async_from_dict():
    await test_finalize_write_stream_async(request_type=dict)


def test_finalize_write_stream_field_headers():
    client = BigQueryWriteClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.FinalizeWriteStreamRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.finalize_write_stream), "__call__"
    ) as call:
        call.return_value = storage.FinalizeWriteStreamResponse()

        client.finalize_write_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_finalize_write_stream_field_headers_async():
    client = BigQueryWriteAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.FinalizeWriteStreamRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.finalize_write_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.FinalizeWriteStreamResponse()
        )

        await client.finalize_write_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_finalize_write_stream_flattened():
    client = BigQueryWriteClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.finalize_write_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.FinalizeWriteStreamResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.finalize_write_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_finalize_write_stream_flattened_error():
    client = BigQueryWriteClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.finalize_write_stream(
            storage.FinalizeWriteStreamRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_finalize_write_stream_flattened_async():
    client = BigQueryWriteAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.finalize_write_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.FinalizeWriteStreamResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.FinalizeWriteStreamResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.finalize_write_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_finalize_write_stream_flattened_error_async():
    client = BigQueryWriteAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.finalize_write_stream(
            storage.FinalizeWriteStreamRequest(), name="name_value",
        )


def test_batch_commit_write_streams(
    transport: str = "grpc", request_type=storage.BatchCommitWriteStreamsRequest
):
    client = BigQueryWriteClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_commit_write_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.BatchCommitWriteStreamsResponse()

        response = client.batch_commit_write_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == storage.BatchCommitWriteStreamsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, storage.BatchCommitWriteStreamsResponse)


def test_batch_commit_write_streams_from_dict():
    test_batch_commit_write_streams(request_type=dict)


@pytest.mark.asyncio
async def test_batch_commit_write_streams_async(
    transport: str = "grpc_asyncio", request_type=storage.BatchCommitWriteStreamsRequest
):
    client = BigQueryWriteAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_commit_write_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.BatchCommitWriteStreamsResponse()
        )

        response = await client.batch_commit_write_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == storage.BatchCommitWriteStreamsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.BatchCommitWriteStreamsResponse)


@pytest.mark.asyncio
async def test_batch_commit_write_streams_async_from_dict():
    await test_batch_commit_write_streams_async(request_type=dict)


def test_batch_commit_write_streams_field_headers():
    client = BigQueryWriteClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.BatchCommitWriteStreamsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_commit_write_streams), "__call__"
    ) as call:
        call.return_value = storage.BatchCommitWriteStreamsResponse()

        client.batch_commit_write_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_commit_write_streams_field_headers_async():
    client = BigQueryWriteAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.BatchCommitWriteStreamsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_commit_write_streams), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.BatchCommitWriteStreamsResponse()
        )

        await client.batch_commit_write_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_batch_commit_write_streams_flattened():
    client = BigQueryWriteClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_commit_write_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.BatchCommitWriteStreamsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.batch_commit_write_streams(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_batch_commit_write_streams_flattened_error():
    client = BigQueryWriteClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.batch_commit_write_streams(
            storage.BatchCommitWriteStreamsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_batch_commit_write_streams_flattened_async():
    client = BigQueryWriteAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_commit_write_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.BatchCommitWriteStreamsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.BatchCommitWriteStreamsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.batch_commit_write_streams(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_batch_commit_write_streams_flattened_error_async():
    client = BigQueryWriteAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.batch_commit_write_streams(
            storage.BatchCommitWriteStreamsRequest(), parent="parent_value",
        )


def test_flush_rows(transport: str = "grpc", request_type=storage.FlushRowsRequest):
    client = BigQueryWriteClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.flush_rows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.FlushRowsResponse(offset=647,)

        response = client.flush_rows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == storage.FlushRowsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, storage.FlushRowsResponse)

    assert response.offset == 647


def test_flush_rows_from_dict():
    test_flush_rows(request_type=dict)


@pytest.mark.asyncio
async def test_flush_rows_async(
    transport: str = "grpc_asyncio", request_type=storage.FlushRowsRequest
):
    client = BigQueryWriteAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.flush_rows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.FlushRowsResponse(offset=647,)
        )

        response = await client.flush_rows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == storage.FlushRowsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.FlushRowsResponse)

    assert response.offset == 647


@pytest.mark.asyncio
async def test_flush_rows_async_from_dict():
    await test_flush_rows_async(request_type=dict)


def test_flush_rows_field_headers():
    client = BigQueryWriteClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.FlushRowsRequest()
    request.write_stream = "write_stream/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.flush_rows), "__call__") as call:
        call.return_value = storage.FlushRowsResponse()

        client.flush_rows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "write_stream=write_stream/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_flush_rows_field_headers_async():
    client = BigQueryWriteAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.FlushRowsRequest()
    request.write_stream = "write_stream/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.flush_rows), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.FlushRowsResponse()
        )

        await client.flush_rows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "write_stream=write_stream/value",) in kw[
        "metadata"
    ]


def test_flush_rows_flattened():
    client = BigQueryWriteClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.flush_rows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.FlushRowsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.flush_rows(write_stream="write_stream_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].write_stream == "write_stream_value"


def test_flush_rows_flattened_error():
    client = BigQueryWriteClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.flush_rows(
            storage.FlushRowsRequest(), write_stream="write_stream_value",
        )


@pytest.mark.asyncio
async def test_flush_rows_flattened_async():
    client = BigQueryWriteAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.flush_rows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.FlushRowsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.FlushRowsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.flush_rows(write_stream="write_stream_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].write_stream == "write_stream_value"


@pytest.mark.asyncio
async def test_flush_rows_flattened_error_async():
    client = BigQueryWriteAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.flush_rows(
            storage.FlushRowsRequest(), write_stream="write_stream_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.BigQueryWriteGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BigQueryWriteClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.BigQueryWriteGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BigQueryWriteClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.BigQueryWriteGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BigQueryWriteClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.BigQueryWriteGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = BigQueryWriteClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.BigQueryWriteGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.BigQueryWriteGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.BigQueryWriteGrpcTransport,
        transports.BigQueryWriteGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = BigQueryWriteClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.BigQueryWriteGrpcTransport,)


def test_big_query_write_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.BigQueryWriteTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_big_query_write_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.bigquery_storage_v1beta2.services.big_query_write.transports.BigQueryWriteTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.BigQueryWriteTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_write_stream",
        "append_rows",
        "get_write_stream",
        "finalize_write_stream",
        "batch_commit_write_streams",
        "flush_rows",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_big_query_write_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.bigquery_storage_v1beta2.services.big_query_write.transports.BigQueryWriteTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.BigQueryWriteTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/bigquery.insertdata",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


def test_big_query_write_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.bigquery_storage_v1beta2.services.big_query_write.transports.BigQueryWriteTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.BigQueryWriteTransport()
        adc.assert_called_once()


def test_big_query_write_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        BigQueryWriteClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/bigquery.insertdata",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id=None,
        )


def test_big_query_write_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.BigQueryWriteGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/bigquery.insertdata",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


def test_big_query_write_host_no_port():
    client = BigQueryWriteClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="bigquerystorage.googleapis.com"
        ),
    )
    assert client.transport._host == "bigquerystorage.googleapis.com:443"


def test_big_query_write_host_with_port():
    client = BigQueryWriteClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="bigquerystorage.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "bigquerystorage.googleapis.com:8000"


def test_big_query_write_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.BigQueryWriteGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_big_query_write_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.BigQueryWriteGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.BigQueryWriteGrpcTransport,
        transports.BigQueryWriteGrpcAsyncIOTransport,
    ],
)
def test_big_query_write_transport_channel_mtls_with_client_cert_source(
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
                    "https://www.googleapis.com/auth/bigquery",
                    "https://www.googleapis.com/auth/bigquery.insertdata",
                    "https://www.googleapis.com/auth/cloud-platform",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.BigQueryWriteGrpcTransport,
        transports.BigQueryWriteGrpcAsyncIOTransport,
    ],
)
def test_big_query_write_transport_channel_mtls_with_adc(transport_class):
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
                scopes=(
                    "https://www.googleapis.com/auth/bigquery",
                    "https://www.googleapis.com/auth/bigquery.insertdata",
                    "https://www.googleapis.com/auth/cloud-platform",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_table_path():
    project = "squid"
    dataset = "clam"
    table = "whelk"

    expected = "projects/{project}/datasets/{dataset}/tables/{table}".format(
        project=project, dataset=dataset, table=table,
    )
    actual = BigQueryWriteClient.table_path(project, dataset, table)
    assert expected == actual


def test_parse_table_path():
    expected = {
        "project": "octopus",
        "dataset": "oyster",
        "table": "nudibranch",
    }
    path = BigQueryWriteClient.table_path(**expected)

    # Check that the path construction is reversible.
    actual = BigQueryWriteClient.parse_table_path(path)
    assert expected == actual


def test_write_stream_path():
    project = "cuttlefish"
    dataset = "mussel"
    table = "winkle"
    stream = "nautilus"

    expected = "projects/{project}/datasets/{dataset}/tables/{table}/streams/{stream}".format(
        project=project, dataset=dataset, table=table, stream=stream,
    )
    actual = BigQueryWriteClient.write_stream_path(project, dataset, table, stream)
    assert expected == actual


def test_parse_write_stream_path():
    expected = {
        "project": "scallop",
        "dataset": "abalone",
        "table": "squid",
        "stream": "clam",
    }
    path = BigQueryWriteClient.write_stream_path(**expected)

    # Check that the path construction is reversible.
    actual = BigQueryWriteClient.parse_write_stream_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = BigQueryWriteClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = BigQueryWriteClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = BigQueryWriteClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"

    expected = "folders/{folder}".format(folder=folder,)
    actual = BigQueryWriteClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = BigQueryWriteClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = BigQueryWriteClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = BigQueryWriteClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = BigQueryWriteClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = BigQueryWriteClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"

    expected = "projects/{project}".format(project=project,)
    actual = BigQueryWriteClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = BigQueryWriteClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = BigQueryWriteClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = BigQueryWriteClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = BigQueryWriteClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = BigQueryWriteClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.BigQueryWriteTransport, "_prep_wrapped_messages"
    ) as prep:
        client = BigQueryWriteClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.BigQueryWriteTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = BigQueryWriteClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
