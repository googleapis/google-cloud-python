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
from google.cloud.bigquery_storage_v1beta2.services.big_query_read import (
    BigQueryReadAsyncClient,
)
from google.cloud.bigquery_storage_v1beta2.services.big_query_read import (
    BigQueryReadClient,
)
from google.cloud.bigquery_storage_v1beta2.services.big_query_read import transports
from google.cloud.bigquery_storage_v1beta2.types import arrow
from google.cloud.bigquery_storage_v1beta2.types import avro
from google.cloud.bigquery_storage_v1beta2.types import storage
from google.cloud.bigquery_storage_v1beta2.types import stream
from google.oauth2 import service_account
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


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

    assert BigQueryReadClient._get_default_mtls_endpoint(None) is None
    assert (
        BigQueryReadClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        BigQueryReadClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        BigQueryReadClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        BigQueryReadClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert BigQueryReadClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


def test_big_query_read_client_from_service_account_info():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = BigQueryReadClient.from_service_account_info(info)
        assert client.transport._credentials == creds

        assert client.transport._host == "bigquerystorage.googleapis.com:443"


@pytest.mark.parametrize("client_class", [BigQueryReadClient, BigQueryReadAsyncClient,])
def test_big_query_read_client_from_service_account_file(client_class):
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


def test_big_query_read_client_get_transport_class():
    transport = BigQueryReadClient.get_transport_class()
    available_transports = [
        transports.BigQueryReadGrpcTransport,
    ]
    assert transport in available_transports

    transport = BigQueryReadClient.get_transport_class("grpc")
    assert transport == transports.BigQueryReadGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (BigQueryReadClient, transports.BigQueryReadGrpcTransport, "grpc"),
        (
            BigQueryReadAsyncClient,
            transports.BigQueryReadGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    BigQueryReadClient, "DEFAULT_ENDPOINT", modify_default_endpoint(BigQueryReadClient)
)
@mock.patch.object(
    BigQueryReadAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BigQueryReadAsyncClient),
)
def test_big_query_read_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(BigQueryReadClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(BigQueryReadClient, "get_transport_class") as gtc:
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
        (BigQueryReadClient, transports.BigQueryReadGrpcTransport, "grpc", "true"),
        (
            BigQueryReadAsyncClient,
            transports.BigQueryReadGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (BigQueryReadClient, transports.BigQueryReadGrpcTransport, "grpc", "false"),
        (
            BigQueryReadAsyncClient,
            transports.BigQueryReadGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    BigQueryReadClient, "DEFAULT_ENDPOINT", modify_default_endpoint(BigQueryReadClient)
)
@mock.patch.object(
    BigQueryReadAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BigQueryReadAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_big_query_read_client_mtls_env_auto(
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
        (BigQueryReadClient, transports.BigQueryReadGrpcTransport, "grpc"),
        (
            BigQueryReadAsyncClient,
            transports.BigQueryReadGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_big_query_read_client_client_options_scopes(
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
        (BigQueryReadClient, transports.BigQueryReadGrpcTransport, "grpc"),
        (
            BigQueryReadAsyncClient,
            transports.BigQueryReadGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_big_query_read_client_client_options_credentials_file(
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


def test_big_query_read_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.bigquery_storage_v1beta2.services.big_query_read.transports.BigQueryReadGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = BigQueryReadClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_create_read_session(
    transport: str = "grpc", request_type=storage.CreateReadSessionRequest
):
    client = BigQueryReadClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_read_session), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = stream.ReadSession(
            name="name_value",
            data_format=stream.DataFormat.AVRO,
            table="table_value",
            avro_schema=avro.AvroSchema(schema="schema_value"),
        )

        response = client.create_read_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == storage.CreateReadSessionRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, stream.ReadSession)

    assert response.name == "name_value"

    assert response.data_format == stream.DataFormat.AVRO

    assert response.table == "table_value"


def test_create_read_session_from_dict():
    test_create_read_session(request_type=dict)


@pytest.mark.asyncio
async def test_create_read_session_async(
    transport: str = "grpc_asyncio", request_type=storage.CreateReadSessionRequest
):
    client = BigQueryReadAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_read_session), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            stream.ReadSession(
                name="name_value",
                data_format=stream.DataFormat.AVRO,
                table="table_value",
            )
        )

        response = await client.create_read_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == storage.CreateReadSessionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, stream.ReadSession)

    assert response.name == "name_value"

    assert response.data_format == stream.DataFormat.AVRO

    assert response.table == "table_value"


@pytest.mark.asyncio
async def test_create_read_session_async_from_dict():
    await test_create_read_session_async(request_type=dict)


def test_create_read_session_field_headers():
    client = BigQueryReadClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.CreateReadSessionRequest()
    request.read_session.table = "read_session.table/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_read_session), "__call__"
    ) as call:
        call.return_value = stream.ReadSession()

        client.create_read_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "read_session.table=read_session.table/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_read_session_field_headers_async():
    client = BigQueryReadAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.CreateReadSessionRequest()
    request.read_session.table = "read_session.table/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_read_session), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(stream.ReadSession())

        await client.create_read_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "read_session.table=read_session.table/value",
    ) in kw["metadata"]


def test_create_read_session_flattened():
    client = BigQueryReadClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_read_session), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = stream.ReadSession()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_read_session(
            parent="parent_value",
            read_session=stream.ReadSession(name="name_value"),
            max_stream_count=1721,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].read_session == stream.ReadSession(name="name_value")

        assert args[0].max_stream_count == 1721


def test_create_read_session_flattened_error():
    client = BigQueryReadClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_read_session(
            storage.CreateReadSessionRequest(),
            parent="parent_value",
            read_session=stream.ReadSession(name="name_value"),
            max_stream_count=1721,
        )


@pytest.mark.asyncio
async def test_create_read_session_flattened_async():
    client = BigQueryReadAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_read_session), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = stream.ReadSession()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(stream.ReadSession())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_read_session(
            parent="parent_value",
            read_session=stream.ReadSession(name="name_value"),
            max_stream_count=1721,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].read_session == stream.ReadSession(name="name_value")

        assert args[0].max_stream_count == 1721


@pytest.mark.asyncio
async def test_create_read_session_flattened_error_async():
    client = BigQueryReadAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_read_session(
            storage.CreateReadSessionRequest(),
            parent="parent_value",
            read_session=stream.ReadSession(name="name_value"),
            max_stream_count=1721,
        )


def test_read_rows(transport: str = "grpc", request_type=storage.ReadRowsRequest):
    client = BigQueryReadClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_rows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([storage.ReadRowsResponse()])

        response = client.read_rows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == storage.ReadRowsRequest()

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, storage.ReadRowsResponse)


def test_read_rows_from_dict():
    test_read_rows(request_type=dict)


@pytest.mark.asyncio
async def test_read_rows_async(
    transport: str = "grpc_asyncio", request_type=storage.ReadRowsRequest
):
    client = BigQueryReadAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_rows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[storage.ReadRowsResponse()]
        )

        response = await client.read_rows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == storage.ReadRowsRequest()

    # Establish that the response is the type that we expect.
    message = await response.read()
    assert isinstance(message, storage.ReadRowsResponse)


@pytest.mark.asyncio
async def test_read_rows_async_from_dict():
    await test_read_rows_async(request_type=dict)


def test_read_rows_field_headers():
    client = BigQueryReadClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.ReadRowsRequest()
    request.read_stream = "read_stream/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_rows), "__call__") as call:
        call.return_value = iter([storage.ReadRowsResponse()])

        client.read_rows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "read_stream=read_stream/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_read_rows_field_headers_async():
    client = BigQueryReadAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.ReadRowsRequest()
    request.read_stream = "read_stream/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_rows), "__call__") as call:
        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[storage.ReadRowsResponse()]
        )

        await client.read_rows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "read_stream=read_stream/value",) in kw["metadata"]


def test_read_rows_flattened():
    client = BigQueryReadClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_rows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([storage.ReadRowsResponse()])

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.read_rows(
            read_stream="read_stream_value", offset=647,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].read_stream == "read_stream_value"

        assert args[0].offset == 647


def test_read_rows_flattened_error():
    client = BigQueryReadClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.read_rows(
            storage.ReadRowsRequest(), read_stream="read_stream_value", offset=647,
        )


@pytest.mark.asyncio
async def test_read_rows_flattened_async():
    client = BigQueryReadAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_rows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([storage.ReadRowsResponse()])

        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.read_rows(read_stream="read_stream_value", offset=647,)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].read_stream == "read_stream_value"

        assert args[0].offset == 647


@pytest.mark.asyncio
async def test_read_rows_flattened_error_async():
    client = BigQueryReadAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.read_rows(
            storage.ReadRowsRequest(), read_stream="read_stream_value", offset=647,
        )


def test_split_read_stream(
    transport: str = "grpc", request_type=storage.SplitReadStreamRequest
):
    client = BigQueryReadClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.split_read_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.SplitReadStreamResponse()

        response = client.split_read_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == storage.SplitReadStreamRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, storage.SplitReadStreamResponse)


def test_split_read_stream_from_dict():
    test_split_read_stream(request_type=dict)


@pytest.mark.asyncio
async def test_split_read_stream_async(
    transport: str = "grpc_asyncio", request_type=storage.SplitReadStreamRequest
):
    client = BigQueryReadAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.split_read_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.SplitReadStreamResponse()
        )

        response = await client.split_read_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == storage.SplitReadStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.SplitReadStreamResponse)


@pytest.mark.asyncio
async def test_split_read_stream_async_from_dict():
    await test_split_read_stream_async(request_type=dict)


def test_split_read_stream_field_headers():
    client = BigQueryReadClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.SplitReadStreamRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.split_read_stream), "__call__"
    ) as call:
        call.return_value = storage.SplitReadStreamResponse()

        client.split_read_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_split_read_stream_field_headers_async():
    client = BigQueryReadAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.SplitReadStreamRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.split_read_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.SplitReadStreamResponse()
        )

        await client.split_read_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.BigQueryReadGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BigQueryReadClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.BigQueryReadGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BigQueryReadClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.BigQueryReadGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BigQueryReadClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.BigQueryReadGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = BigQueryReadClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.BigQueryReadGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.BigQueryReadGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.BigQueryReadGrpcTransport,
        transports.BigQueryReadGrpcAsyncIOTransport,
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
    client = BigQueryReadClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.BigQueryReadGrpcTransport,)


def test_big_query_read_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.BigQueryReadTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_big_query_read_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.bigquery_storage_v1beta2.services.big_query_read.transports.BigQueryReadTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.BigQueryReadTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_read_session",
        "read_rows",
        "split_read_stream",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_big_query_read_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.bigquery_storage_v1beta2.services.big_query_read.transports.BigQueryReadTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.BigQueryReadTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/bigquery.readonly",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


def test_big_query_read_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.bigquery_storage_v1beta2.services.big_query_read.transports.BigQueryReadTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.BigQueryReadTransport()
        adc.assert_called_once()


def test_big_query_read_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        BigQueryReadClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/bigquery.readonly",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id=None,
        )


def test_big_query_read_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.BigQueryReadGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/bigquery.readonly",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


def test_big_query_read_host_no_port():
    client = BigQueryReadClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="bigquerystorage.googleapis.com"
        ),
    )
    assert client.transport._host == "bigquerystorage.googleapis.com:443"


def test_big_query_read_host_with_port():
    client = BigQueryReadClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="bigquerystorage.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "bigquerystorage.googleapis.com:8000"


def test_big_query_read_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.BigQueryReadGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_big_query_read_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.BigQueryReadGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


@pytest.mark.parametrize(
    "transport_class",
    [transports.BigQueryReadGrpcTransport, transports.BigQueryReadGrpcAsyncIOTransport],
)
def test_big_query_read_transport_channel_mtls_with_client_cert_source(transport_class):
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
                    "https://www.googleapis.com/auth/bigquery.readonly",
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
    [transports.BigQueryReadGrpcTransport, transports.BigQueryReadGrpcAsyncIOTransport],
)
def test_big_query_read_transport_channel_mtls_with_adc(transport_class):
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
                    "https://www.googleapis.com/auth/bigquery.readonly",
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


def test_read_session_path():
    project = "squid"
    location = "clam"
    session = "whelk"

    expected = "projects/{project}/locations/{location}/sessions/{session}".format(
        project=project, location=location, session=session,
    )
    actual = BigQueryReadClient.read_session_path(project, location, session)
    assert expected == actual


def test_parse_read_session_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "session": "nudibranch",
    }
    path = BigQueryReadClient.read_session_path(**expected)

    # Check that the path construction is reversible.
    actual = BigQueryReadClient.parse_read_session_path(path)
    assert expected == actual


def test_read_stream_path():
    project = "cuttlefish"
    location = "mussel"
    session = "winkle"
    stream = "nautilus"

    expected = "projects/{project}/locations/{location}/sessions/{session}/streams/{stream}".format(
        project=project, location=location, session=session, stream=stream,
    )
    actual = BigQueryReadClient.read_stream_path(project, location, session, stream)
    assert expected == actual


def test_parse_read_stream_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "session": "squid",
        "stream": "clam",
    }
    path = BigQueryReadClient.read_stream_path(**expected)

    # Check that the path construction is reversible.
    actual = BigQueryReadClient.parse_read_stream_path(path)
    assert expected == actual


def test_table_path():
    project = "whelk"
    dataset = "octopus"
    table = "oyster"

    expected = "projects/{project}/datasets/{dataset}/tables/{table}".format(
        project=project, dataset=dataset, table=table,
    )
    actual = BigQueryReadClient.table_path(project, dataset, table)
    assert expected == actual


def test_parse_table_path():
    expected = {
        "project": "nudibranch",
        "dataset": "cuttlefish",
        "table": "mussel",
    }
    path = BigQueryReadClient.table_path(**expected)

    # Check that the path construction is reversible.
    actual = BigQueryReadClient.parse_table_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "winkle"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = BigQueryReadClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nautilus",
    }
    path = BigQueryReadClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = BigQueryReadClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "scallop"

    expected = "folders/{folder}".format(folder=folder,)
    actual = BigQueryReadClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "abalone",
    }
    path = BigQueryReadClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = BigQueryReadClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "squid"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = BigQueryReadClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "clam",
    }
    path = BigQueryReadClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = BigQueryReadClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "whelk"

    expected = "projects/{project}".format(project=project,)
    actual = BigQueryReadClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "octopus",
    }
    path = BigQueryReadClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = BigQueryReadClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "oyster"
    location = "nudibranch"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = BigQueryReadClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
    }
    path = BigQueryReadClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = BigQueryReadClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.BigQueryReadTransport, "_prep_wrapped_messages"
    ) as prep:
        client = BigQueryReadClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.BigQueryReadTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = BigQueryReadClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
