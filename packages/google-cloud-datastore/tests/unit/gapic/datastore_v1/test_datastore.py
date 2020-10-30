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
from google.cloud.datastore_v1.services.datastore import DatastoreAsyncClient
from google.cloud.datastore_v1.services.datastore import DatastoreClient
from google.cloud.datastore_v1.services.datastore import transports
from google.cloud.datastore_v1.types import datastore
from google.cloud.datastore_v1.types import entity
from google.cloud.datastore_v1.types import query
from google.oauth2 import service_account
from google.protobuf import struct_pb2 as struct  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore
from google.type import latlng_pb2 as latlng  # type: ignore


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

    assert DatastoreClient._get_default_mtls_endpoint(None) is None
    assert DatastoreClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert (
        DatastoreClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        DatastoreClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DatastoreClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert DatastoreClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [DatastoreClient, DatastoreAsyncClient])
def test_datastore_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds

        assert client.transport._host == "datastore.googleapis.com:443"


def test_datastore_client_get_transport_class():
    transport = DatastoreClient.get_transport_class()
    assert transport == transports.DatastoreGrpcTransport

    transport = DatastoreClient.get_transport_class("grpc")
    assert transport == transports.DatastoreGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (DatastoreClient, transports.DatastoreGrpcTransport, "grpc"),
        (
            DatastoreAsyncClient,
            transports.DatastoreGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    DatastoreClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DatastoreClient)
)
@mock.patch.object(
    DatastoreAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DatastoreAsyncClient),
)
def test_datastore_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(DatastoreClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(DatastoreClient, "get_transport_class") as gtc:
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
        (DatastoreClient, transports.DatastoreGrpcTransport, "grpc", "true"),
        (
            DatastoreAsyncClient,
            transports.DatastoreGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (DatastoreClient, transports.DatastoreGrpcTransport, "grpc", "false"),
        (
            DatastoreAsyncClient,
            transports.DatastoreGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    DatastoreClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DatastoreClient)
)
@mock.patch.object(
    DatastoreAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DatastoreAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_datastore_client_mtls_env_auto(
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
        (DatastoreClient, transports.DatastoreGrpcTransport, "grpc"),
        (
            DatastoreAsyncClient,
            transports.DatastoreGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_datastore_client_client_options_scopes(
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
        (DatastoreClient, transports.DatastoreGrpcTransport, "grpc"),
        (
            DatastoreAsyncClient,
            transports.DatastoreGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_datastore_client_client_options_credentials_file(
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


def test_datastore_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.datastore_v1.services.datastore.transports.DatastoreGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = DatastoreClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_lookup(transport: str = "grpc", request_type=datastore.LookupRequest):
    client = DatastoreClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.lookup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastore.LookupResponse()

        response = client.lookup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datastore.LookupRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, datastore.LookupResponse)


def test_lookup_from_dict():
    test_lookup(request_type=dict)


@pytest.mark.asyncio
async def test_lookup_async(
    transport: str = "grpc_asyncio", request_type=datastore.LookupRequest
):
    client = DatastoreAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.lookup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastore.LookupResponse()
        )

        response = await client.lookup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datastore.LookupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastore.LookupResponse)


@pytest.mark.asyncio
async def test_lookup_async_from_dict():
    await test_lookup_async(request_type=dict)


def test_lookup_flattened():
    client = DatastoreClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.lookup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastore.LookupResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.lookup(
            project_id="project_id_value",
            read_options=datastore.ReadOptions(
                read_consistency=datastore.ReadOptions.ReadConsistency.STRONG
            ),
            keys=[
                entity.Key(
                    partition_id=entity.PartitionId(project_id="project_id_value")
                )
            ],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].read_options == datastore.ReadOptions(
            read_consistency=datastore.ReadOptions.ReadConsistency.STRONG
        )

        assert args[0].keys == [
            entity.Key(partition_id=entity.PartitionId(project_id="project_id_value"))
        ]


def test_lookup_flattened_error():
    client = DatastoreClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.lookup(
            datastore.LookupRequest(),
            project_id="project_id_value",
            read_options=datastore.ReadOptions(
                read_consistency=datastore.ReadOptions.ReadConsistency.STRONG
            ),
            keys=[
                entity.Key(
                    partition_id=entity.PartitionId(project_id="project_id_value")
                )
            ],
        )


@pytest.mark.asyncio
async def test_lookup_flattened_async():
    client = DatastoreAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.lookup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastore.LookupResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastore.LookupResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.lookup(
            project_id="project_id_value",
            read_options=datastore.ReadOptions(
                read_consistency=datastore.ReadOptions.ReadConsistency.STRONG
            ),
            keys=[
                entity.Key(
                    partition_id=entity.PartitionId(project_id="project_id_value")
                )
            ],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].read_options == datastore.ReadOptions(
            read_consistency=datastore.ReadOptions.ReadConsistency.STRONG
        )

        assert args[0].keys == [
            entity.Key(partition_id=entity.PartitionId(project_id="project_id_value"))
        ]


@pytest.mark.asyncio
async def test_lookup_flattened_error_async():
    client = DatastoreAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.lookup(
            datastore.LookupRequest(),
            project_id="project_id_value",
            read_options=datastore.ReadOptions(
                read_consistency=datastore.ReadOptions.ReadConsistency.STRONG
            ),
            keys=[
                entity.Key(
                    partition_id=entity.PartitionId(project_id="project_id_value")
                )
            ],
        )


def test_run_query(transport: str = "grpc", request_type=datastore.RunQueryRequest):
    client = DatastoreClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_query), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastore.RunQueryResponse()

        response = client.run_query(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datastore.RunQueryRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, datastore.RunQueryResponse)


def test_run_query_from_dict():
    test_run_query(request_type=dict)


@pytest.mark.asyncio
async def test_run_query_async(
    transport: str = "grpc_asyncio", request_type=datastore.RunQueryRequest
):
    client = DatastoreAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_query), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastore.RunQueryResponse()
        )

        response = await client.run_query(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datastore.RunQueryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastore.RunQueryResponse)


@pytest.mark.asyncio
async def test_run_query_async_from_dict():
    await test_run_query_async(request_type=dict)


def test_begin_transaction(
    transport: str = "grpc", request_type=datastore.BeginTransactionRequest
):
    client = DatastoreClient(
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
        call.return_value = datastore.BeginTransactionResponse(
            transaction=b"transaction_blob",
        )

        response = client.begin_transaction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datastore.BeginTransactionRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, datastore.BeginTransactionResponse)

    assert response.transaction == b"transaction_blob"


def test_begin_transaction_from_dict():
    test_begin_transaction(request_type=dict)


@pytest.mark.asyncio
async def test_begin_transaction_async(
    transport: str = "grpc_asyncio", request_type=datastore.BeginTransactionRequest
):
    client = DatastoreAsyncClient(
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
            datastore.BeginTransactionResponse(transaction=b"transaction_blob",)
        )

        response = await client.begin_transaction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datastore.BeginTransactionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastore.BeginTransactionResponse)

    assert response.transaction == b"transaction_blob"


@pytest.mark.asyncio
async def test_begin_transaction_async_from_dict():
    await test_begin_transaction_async(request_type=dict)


def test_begin_transaction_flattened():
    client = DatastoreClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.begin_transaction), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastore.BeginTransactionResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.begin_transaction(project_id="project_id_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"


def test_begin_transaction_flattened_error():
    client = DatastoreClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.begin_transaction(
            datastore.BeginTransactionRequest(), project_id="project_id_value",
        )


@pytest.mark.asyncio
async def test_begin_transaction_flattened_async():
    client = DatastoreAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.begin_transaction), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastore.BeginTransactionResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastore.BeginTransactionResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.begin_transaction(project_id="project_id_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"


@pytest.mark.asyncio
async def test_begin_transaction_flattened_error_async():
    client = DatastoreAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.begin_transaction(
            datastore.BeginTransactionRequest(), project_id="project_id_value",
        )


def test_commit(transport: str = "grpc", request_type=datastore.CommitRequest):
    client = DatastoreClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastore.CommitResponse(index_updates=1389,)

        response = client.commit(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datastore.CommitRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, datastore.CommitResponse)

    assert response.index_updates == 1389


def test_commit_from_dict():
    test_commit(request_type=dict)


@pytest.mark.asyncio
async def test_commit_async(
    transport: str = "grpc_asyncio", request_type=datastore.CommitRequest
):
    client = DatastoreAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastore.CommitResponse(index_updates=1389,)
        )

        response = await client.commit(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datastore.CommitRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastore.CommitResponse)

    assert response.index_updates == 1389


@pytest.mark.asyncio
async def test_commit_async_from_dict():
    await test_commit_async(request_type=dict)


def test_commit_flattened():
    client = DatastoreClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastore.CommitResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.commit(
            project_id="project_id_value",
            mode=datastore.CommitRequest.Mode.TRANSACTIONAL,
            transaction=b"transaction_blob",
            mutations=[
                datastore.Mutation(
                    insert=entity.Entity(
                        key=entity.Key(
                            partition_id=entity.PartitionId(
                                project_id="project_id_value"
                            )
                        )
                    )
                )
            ],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].mode == datastore.CommitRequest.Mode.TRANSACTIONAL

        assert args[0].mutations == [
            datastore.Mutation(
                insert=entity.Entity(
                    key=entity.Key(
                        partition_id=entity.PartitionId(project_id="project_id_value")
                    )
                )
            )
        ]

        assert args[0].transaction == b"transaction_blob"


def test_commit_flattened_error():
    client = DatastoreClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.commit(
            datastore.CommitRequest(),
            project_id="project_id_value",
            mode=datastore.CommitRequest.Mode.TRANSACTIONAL,
            transaction=b"transaction_blob",
            mutations=[
                datastore.Mutation(
                    insert=entity.Entity(
                        key=entity.Key(
                            partition_id=entity.PartitionId(
                                project_id="project_id_value"
                            )
                        )
                    )
                )
            ],
        )


@pytest.mark.asyncio
async def test_commit_flattened_async():
    client = DatastoreAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastore.CommitResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastore.CommitResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.commit(
            project_id="project_id_value",
            mode=datastore.CommitRequest.Mode.TRANSACTIONAL,
            transaction=b"transaction_blob",
            mutations=[
                datastore.Mutation(
                    insert=entity.Entity(
                        key=entity.Key(
                            partition_id=entity.PartitionId(
                                project_id="project_id_value"
                            )
                        )
                    )
                )
            ],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].mode == datastore.CommitRequest.Mode.TRANSACTIONAL

        assert args[0].mutations == [
            datastore.Mutation(
                insert=entity.Entity(
                    key=entity.Key(
                        partition_id=entity.PartitionId(project_id="project_id_value")
                    )
                )
            )
        ]

        assert args[0].transaction == b"transaction_blob"


@pytest.mark.asyncio
async def test_commit_flattened_error_async():
    client = DatastoreAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.commit(
            datastore.CommitRequest(),
            project_id="project_id_value",
            mode=datastore.CommitRequest.Mode.TRANSACTIONAL,
            transaction=b"transaction_blob",
            mutations=[
                datastore.Mutation(
                    insert=entity.Entity(
                        key=entity.Key(
                            partition_id=entity.PartitionId(
                                project_id="project_id_value"
                            )
                        )
                    )
                )
            ],
        )


def test_rollback(transport: str = "grpc", request_type=datastore.RollbackRequest):
    client = DatastoreClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastore.RollbackResponse()

        response = client.rollback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datastore.RollbackRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, datastore.RollbackResponse)


def test_rollback_from_dict():
    test_rollback(request_type=dict)


@pytest.mark.asyncio
async def test_rollback_async(
    transport: str = "grpc_asyncio", request_type=datastore.RollbackRequest
):
    client = DatastoreAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastore.RollbackResponse()
        )

        response = await client.rollback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datastore.RollbackRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastore.RollbackResponse)


@pytest.mark.asyncio
async def test_rollback_async_from_dict():
    await test_rollback_async(request_type=dict)


def test_rollback_flattened():
    client = DatastoreClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastore.RollbackResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.rollback(
            project_id="project_id_value", transaction=b"transaction_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].transaction == b"transaction_blob"


def test_rollback_flattened_error():
    client = DatastoreClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.rollback(
            datastore.RollbackRequest(),
            project_id="project_id_value",
            transaction=b"transaction_blob",
        )


@pytest.mark.asyncio
async def test_rollback_flattened_async():
    client = DatastoreAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastore.RollbackResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastore.RollbackResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.rollback(
            project_id="project_id_value", transaction=b"transaction_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].transaction == b"transaction_blob"


@pytest.mark.asyncio
async def test_rollback_flattened_error_async():
    client = DatastoreAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.rollback(
            datastore.RollbackRequest(),
            project_id="project_id_value",
            transaction=b"transaction_blob",
        )


def test_allocate_ids(
    transport: str = "grpc", request_type=datastore.AllocateIdsRequest
):
    client = DatastoreClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.allocate_ids), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastore.AllocateIdsResponse()

        response = client.allocate_ids(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datastore.AllocateIdsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, datastore.AllocateIdsResponse)


def test_allocate_ids_from_dict():
    test_allocate_ids(request_type=dict)


@pytest.mark.asyncio
async def test_allocate_ids_async(
    transport: str = "grpc_asyncio", request_type=datastore.AllocateIdsRequest
):
    client = DatastoreAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.allocate_ids), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastore.AllocateIdsResponse()
        )

        response = await client.allocate_ids(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datastore.AllocateIdsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastore.AllocateIdsResponse)


@pytest.mark.asyncio
async def test_allocate_ids_async_from_dict():
    await test_allocate_ids_async(request_type=dict)


def test_allocate_ids_flattened():
    client = DatastoreClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.allocate_ids), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastore.AllocateIdsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.allocate_ids(
            project_id="project_id_value",
            keys=[
                entity.Key(
                    partition_id=entity.PartitionId(project_id="project_id_value")
                )
            ],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].keys == [
            entity.Key(partition_id=entity.PartitionId(project_id="project_id_value"))
        ]


def test_allocate_ids_flattened_error():
    client = DatastoreClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.allocate_ids(
            datastore.AllocateIdsRequest(),
            project_id="project_id_value",
            keys=[
                entity.Key(
                    partition_id=entity.PartitionId(project_id="project_id_value")
                )
            ],
        )


@pytest.mark.asyncio
async def test_allocate_ids_flattened_async():
    client = DatastoreAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.allocate_ids), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastore.AllocateIdsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastore.AllocateIdsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.allocate_ids(
            project_id="project_id_value",
            keys=[
                entity.Key(
                    partition_id=entity.PartitionId(project_id="project_id_value")
                )
            ],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].keys == [
            entity.Key(partition_id=entity.PartitionId(project_id="project_id_value"))
        ]


@pytest.mark.asyncio
async def test_allocate_ids_flattened_error_async():
    client = DatastoreAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.allocate_ids(
            datastore.AllocateIdsRequest(),
            project_id="project_id_value",
            keys=[
                entity.Key(
                    partition_id=entity.PartitionId(project_id="project_id_value")
                )
            ],
        )


def test_reserve_ids(transport: str = "grpc", request_type=datastore.ReserveIdsRequest):
    client = DatastoreClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reserve_ids), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastore.ReserveIdsResponse()

        response = client.reserve_ids(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datastore.ReserveIdsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, datastore.ReserveIdsResponse)


def test_reserve_ids_from_dict():
    test_reserve_ids(request_type=dict)


@pytest.mark.asyncio
async def test_reserve_ids_async(
    transport: str = "grpc_asyncio", request_type=datastore.ReserveIdsRequest
):
    client = DatastoreAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reserve_ids), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastore.ReserveIdsResponse()
        )

        response = await client.reserve_ids(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datastore.ReserveIdsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastore.ReserveIdsResponse)


@pytest.mark.asyncio
async def test_reserve_ids_async_from_dict():
    await test_reserve_ids_async(request_type=dict)


def test_reserve_ids_flattened():
    client = DatastoreClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reserve_ids), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastore.ReserveIdsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.reserve_ids(
            project_id="project_id_value",
            keys=[
                entity.Key(
                    partition_id=entity.PartitionId(project_id="project_id_value")
                )
            ],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].keys == [
            entity.Key(partition_id=entity.PartitionId(project_id="project_id_value"))
        ]


def test_reserve_ids_flattened_error():
    client = DatastoreClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.reserve_ids(
            datastore.ReserveIdsRequest(),
            project_id="project_id_value",
            keys=[
                entity.Key(
                    partition_id=entity.PartitionId(project_id="project_id_value")
                )
            ],
        )


@pytest.mark.asyncio
async def test_reserve_ids_flattened_async():
    client = DatastoreAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reserve_ids), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastore.ReserveIdsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastore.ReserveIdsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.reserve_ids(
            project_id="project_id_value",
            keys=[
                entity.Key(
                    partition_id=entity.PartitionId(project_id="project_id_value")
                )
            ],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].keys == [
            entity.Key(partition_id=entity.PartitionId(project_id="project_id_value"))
        ]


@pytest.mark.asyncio
async def test_reserve_ids_flattened_error_async():
    client = DatastoreAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.reserve_ids(
            datastore.ReserveIdsRequest(),
            project_id="project_id_value",
            keys=[
                entity.Key(
                    partition_id=entity.PartitionId(project_id="project_id_value")
                )
            ],
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.DatastoreGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DatastoreClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.DatastoreGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DatastoreClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.DatastoreGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DatastoreClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DatastoreGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = DatastoreClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DatastoreGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.DatastoreGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.DatastoreGrpcTransport, transports.DatastoreGrpcAsyncIOTransport],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = DatastoreClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.DatastoreGrpcTransport,)


def test_datastore_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.DatastoreTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_datastore_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.datastore_v1.services.datastore.transports.DatastoreTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.DatastoreTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "lookup",
        "run_query",
        "begin_transaction",
        "commit",
        "rollback",
        "allocate_ids",
        "reserve_ids",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_datastore_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.datastore_v1.services.datastore.transports.DatastoreTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.DatastoreTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/datastore",
            ),
            quota_project_id="octopus",
        )


def test_datastore_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.datastore_v1.services.datastore.transports.DatastoreTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.DatastoreTransport()
        adc.assert_called_once()


def test_datastore_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        DatastoreClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/datastore",
            ),
            quota_project_id=None,
        )


def test_datastore_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.DatastoreGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/datastore",
            ),
            quota_project_id="octopus",
        )


def test_datastore_host_no_port():
    client = DatastoreClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="datastore.googleapis.com"
        ),
    )
    assert client.transport._host == "datastore.googleapis.com:443"


def test_datastore_host_with_port():
    client = DatastoreClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="datastore.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "datastore.googleapis.com:8000"


def test_datastore_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.DatastoreGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_datastore_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.DatastoreGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


@pytest.mark.parametrize(
    "transport_class",
    [transports.DatastoreGrpcTransport, transports.DatastoreGrpcAsyncIOTransport],
)
def test_datastore_transport_channel_mtls_with_client_cert_source(transport_class):
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
                    "https://www.googleapis.com/auth/datastore",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


@pytest.mark.parametrize(
    "transport_class",
    [transports.DatastoreGrpcTransport, transports.DatastoreGrpcAsyncIOTransport],
)
def test_datastore_transport_channel_mtls_with_adc(transport_class):
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
                    "https://www.googleapis.com/auth/datastore",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_common_billing_account_path():
    billing_account = "squid"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = DatastoreClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = DatastoreClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = DatastoreClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"

    expected = "folders/{folder}".format(folder=folder,)
    actual = DatastoreClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = DatastoreClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = DatastoreClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = DatastoreClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = DatastoreClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = DatastoreClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"

    expected = "projects/{project}".format(project=project,)
    actual = DatastoreClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = DatastoreClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = DatastoreClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = DatastoreClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = DatastoreClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = DatastoreClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.DatastoreTransport, "_prep_wrapped_messages"
    ) as prep:
        client = DatastoreClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.DatastoreTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = DatastoreClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
