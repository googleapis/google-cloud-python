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
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation_async  # type: ignore
from google.api_core import operations_v1
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.firestore_admin_v1.services.firestore_admin import (
    FirestoreAdminAsyncClient,
)
from google.cloud.firestore_admin_v1.services.firestore_admin import (
    FirestoreAdminClient,
)
from google.cloud.firestore_admin_v1.services.firestore_admin import pagers
from google.cloud.firestore_admin_v1.services.firestore_admin import transports
from google.cloud.firestore_admin_v1.types import field
from google.cloud.firestore_admin_v1.types import field as gfa_field
from google.cloud.firestore_admin_v1.types import firestore_admin
from google.cloud.firestore_admin_v1.types import index
from google.cloud.firestore_admin_v1.types import index as gfa_index
from google.cloud.firestore_admin_v1.types import operation as gfa_operation
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore


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

    assert FirestoreAdminClient._get_default_mtls_endpoint(None) is None
    assert (
        FirestoreAdminClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        FirestoreAdminClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        FirestoreAdminClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        FirestoreAdminClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        FirestoreAdminClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [FirestoreAdminClient, FirestoreAdminAsyncClient]
)
def test_firestore_admin_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "firestore.googleapis.com:443"


def test_firestore_admin_client_get_transport_class():
    transport = FirestoreAdminClient.get_transport_class()
    assert transport == transports.FirestoreAdminGrpcTransport

    transport = FirestoreAdminClient.get_transport_class("grpc")
    assert transport == transports.FirestoreAdminGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (FirestoreAdminClient, transports.FirestoreAdminGrpcTransport, "grpc"),
        (
            FirestoreAdminAsyncClient,
            transports.FirestoreAdminGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    FirestoreAdminClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(FirestoreAdminClient),
)
@mock.patch.object(
    FirestoreAdminAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(FirestoreAdminAsyncClient),
)
def test_firestore_admin_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(FirestoreAdminClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(FirestoreAdminClient, "get_transport_class") as gtc:
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
        (FirestoreAdminClient, transports.FirestoreAdminGrpcTransport, "grpc", "true"),
        (
            FirestoreAdminAsyncClient,
            transports.FirestoreAdminGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (FirestoreAdminClient, transports.FirestoreAdminGrpcTransport, "grpc", "false"),
        (
            FirestoreAdminAsyncClient,
            transports.FirestoreAdminGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    FirestoreAdminClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(FirestoreAdminClient),
)
@mock.patch.object(
    FirestoreAdminAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(FirestoreAdminAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_firestore_admin_client_mtls_env_auto(
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
        (FirestoreAdminClient, transports.FirestoreAdminGrpcTransport, "grpc"),
        (
            FirestoreAdminAsyncClient,
            transports.FirestoreAdminGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_firestore_admin_client_client_options_scopes(
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
        (FirestoreAdminClient, transports.FirestoreAdminGrpcTransport, "grpc"),
        (
            FirestoreAdminAsyncClient,
            transports.FirestoreAdminGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_firestore_admin_client_client_options_credentials_file(
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


def test_firestore_admin_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.firestore_admin_v1.services.firestore_admin.transports.FirestoreAdminGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = FirestoreAdminClient(
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


def test_create_index(
    transport: str = "grpc", request_type=firestore_admin.CreateIndexRequest
):
    client = FirestoreAdminClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_index), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.create_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == firestore_admin.CreateIndexRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_index_from_dict():
    test_create_index(request_type=dict)


@pytest.mark.asyncio
async def test_create_index_async(transport: str = "grpc_asyncio"):
    client = FirestoreAdminAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = firestore_admin.CreateIndexRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_index), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.create_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_index_field_headers():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore_admin.CreateIndexRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_index), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")

        client.create_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_index_field_headers_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore_admin.CreateIndexRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_index), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )

        await client.create_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_index_flattened():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_index), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_index(
            parent="parent_value", index=gfa_index.Index(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].index == gfa_index.Index(name="name_value")


def test_create_index_flattened_error():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_index(
            firestore_admin.CreateIndexRequest(),
            parent="parent_value",
            index=gfa_index.Index(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_index_flattened_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_index), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_index(
            parent="parent_value", index=gfa_index.Index(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].index == gfa_index.Index(name="name_value")


@pytest.mark.asyncio
async def test_create_index_flattened_error_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_index(
            firestore_admin.CreateIndexRequest(),
            parent="parent_value",
            index=gfa_index.Index(name="name_value"),
        )


def test_list_indexes(
    transport: str = "grpc", request_type=firestore_admin.ListIndexesRequest
):
    client = FirestoreAdminClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_indexes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = firestore_admin.ListIndexesResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_indexes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == firestore_admin.ListIndexesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListIndexesPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_indexes_from_dict():
    test_list_indexes(request_type=dict)


@pytest.mark.asyncio
async def test_list_indexes_async(transport: str = "grpc_asyncio"):
    client = FirestoreAdminAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = firestore_admin.ListIndexesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_indexes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firestore_admin.ListIndexesResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_indexes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListIndexesAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_indexes_field_headers():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore_admin.ListIndexesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_indexes), "__call__") as call:
        call.return_value = firestore_admin.ListIndexesResponse()

        client.list_indexes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_indexes_field_headers_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore_admin.ListIndexesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_indexes), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firestore_admin.ListIndexesResponse()
        )

        await client.list_indexes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_indexes_flattened():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_indexes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = firestore_admin.ListIndexesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_indexes(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_indexes_flattened_error():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_indexes(
            firestore_admin.ListIndexesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_indexes_flattened_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_indexes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = firestore_admin.ListIndexesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firestore_admin.ListIndexesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_indexes(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_indexes_flattened_error_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_indexes(
            firestore_admin.ListIndexesRequest(), parent="parent_value",
        )


def test_list_indexes_pager():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_indexes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            firestore_admin.ListIndexesResponse(
                indexes=[index.Index(), index.Index(), index.Index(),],
                next_page_token="abc",
            ),
            firestore_admin.ListIndexesResponse(indexes=[], next_page_token="def",),
            firestore_admin.ListIndexesResponse(
                indexes=[index.Index(),], next_page_token="ghi",
            ),
            firestore_admin.ListIndexesResponse(
                indexes=[index.Index(), index.Index(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_indexes(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, index.Index) for i in results)


def test_list_indexes_pages():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_indexes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            firestore_admin.ListIndexesResponse(
                indexes=[index.Index(), index.Index(), index.Index(),],
                next_page_token="abc",
            ),
            firestore_admin.ListIndexesResponse(indexes=[], next_page_token="def",),
            firestore_admin.ListIndexesResponse(
                indexes=[index.Index(),], next_page_token="ghi",
            ),
            firestore_admin.ListIndexesResponse(
                indexes=[index.Index(), index.Index(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_indexes(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_indexes_async_pager():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_indexes),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            firestore_admin.ListIndexesResponse(
                indexes=[index.Index(), index.Index(), index.Index(),],
                next_page_token="abc",
            ),
            firestore_admin.ListIndexesResponse(indexes=[], next_page_token="def",),
            firestore_admin.ListIndexesResponse(
                indexes=[index.Index(),], next_page_token="ghi",
            ),
            firestore_admin.ListIndexesResponse(
                indexes=[index.Index(), index.Index(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_indexes(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, index.Index) for i in responses)


@pytest.mark.asyncio
async def test_list_indexes_async_pages():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_indexes),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            firestore_admin.ListIndexesResponse(
                indexes=[index.Index(), index.Index(), index.Index(),],
                next_page_token="abc",
            ),
            firestore_admin.ListIndexesResponse(indexes=[], next_page_token="def",),
            firestore_admin.ListIndexesResponse(
                indexes=[index.Index(),], next_page_token="ghi",
            ),
            firestore_admin.ListIndexesResponse(
                indexes=[index.Index(), index.Index(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_indexes(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_index(
    transport: str = "grpc", request_type=firestore_admin.GetIndexRequest
):
    client = FirestoreAdminClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_index), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = index.Index(
            name="name_value",
            query_scope=index.Index.QueryScope.COLLECTION,
            state=index.Index.State.CREATING,
        )

        response = client.get_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == firestore_admin.GetIndexRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, index.Index)

    assert response.name == "name_value"

    assert response.query_scope == index.Index.QueryScope.COLLECTION

    assert response.state == index.Index.State.CREATING


def test_get_index_from_dict():
    test_get_index(request_type=dict)


@pytest.mark.asyncio
async def test_get_index_async(transport: str = "grpc_asyncio"):
    client = FirestoreAdminAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = firestore_admin.GetIndexRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_index), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            index.Index(
                name="name_value",
                query_scope=index.Index.QueryScope.COLLECTION,
                state=index.Index.State.CREATING,
            )
        )

        response = await client.get_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, index.Index)

    assert response.name == "name_value"

    assert response.query_scope == index.Index.QueryScope.COLLECTION

    assert response.state == index.Index.State.CREATING


def test_get_index_field_headers():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore_admin.GetIndexRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_index), "__call__") as call:
        call.return_value = index.Index()

        client.get_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_index_field_headers_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore_admin.GetIndexRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_index), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(index.Index())

        await client.get_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_index_flattened():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_index), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = index.Index()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_index(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_index_flattened_error():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_index(
            firestore_admin.GetIndexRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_index_flattened_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_index), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = index.Index()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(index.Index())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_index(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_index_flattened_error_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_index(
            firestore_admin.GetIndexRequest(), name="name_value",
        )


def test_delete_index(
    transport: str = "grpc", request_type=firestore_admin.DeleteIndexRequest
):
    client = FirestoreAdminClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_index), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == firestore_admin.DeleteIndexRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_index_from_dict():
    test_delete_index(request_type=dict)


@pytest.mark.asyncio
async def test_delete_index_async(transport: str = "grpc_asyncio"):
    client = FirestoreAdminAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = firestore_admin.DeleteIndexRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_index), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_index_field_headers():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore_admin.DeleteIndexRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_index), "__call__") as call:
        call.return_value = None

        client.delete_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_index_field_headers_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore_admin.DeleteIndexRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_index), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_index_flattened():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_index), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_index(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_index_flattened_error():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_index(
            firestore_admin.DeleteIndexRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_index_flattened_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_index), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_index(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_index_flattened_error_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_index(
            firestore_admin.DeleteIndexRequest(), name="name_value",
        )


def test_get_field(
    transport: str = "grpc", request_type=firestore_admin.GetFieldRequest
):
    client = FirestoreAdminClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_field), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = field.Field(name="name_value",)

        response = client.get_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == firestore_admin.GetFieldRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, field.Field)

    assert response.name == "name_value"


def test_get_field_from_dict():
    test_get_field(request_type=dict)


@pytest.mark.asyncio
async def test_get_field_async(transport: str = "grpc_asyncio"):
    client = FirestoreAdminAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = firestore_admin.GetFieldRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            field.Field(name="name_value",)
        )

        response = await client.get_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, field.Field)

    assert response.name == "name_value"


def test_get_field_field_headers():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore_admin.GetFieldRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_field), "__call__") as call:
        call.return_value = field.Field()

        client.get_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_field_field_headers_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore_admin.GetFieldRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_field), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(field.Field())

        await client.get_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_field_flattened():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_field), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = field.Field()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_field(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_field_flattened_error():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_field(
            firestore_admin.GetFieldRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_field_flattened_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = field.Field()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(field.Field())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_field(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_field_flattened_error_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_field(
            firestore_admin.GetFieldRequest(), name="name_value",
        )


def test_update_field(
    transport: str = "grpc", request_type=firestore_admin.UpdateFieldRequest
):
    client = FirestoreAdminClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_field), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.update_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == firestore_admin.UpdateFieldRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_field_from_dict():
    test_update_field(request_type=dict)


@pytest.mark.asyncio
async def test_update_field_async(transport: str = "grpc_asyncio"):
    client = FirestoreAdminAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = firestore_admin.UpdateFieldRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.update_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_field_field_headers():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore_admin.UpdateFieldRequest()
    request.field.name = "field.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_field), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")

        client.update_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "field.name=field.name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_field_field_headers_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore_admin.UpdateFieldRequest()
    request.field.name = "field.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_field), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )

        await client.update_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "field.name=field.name/value",) in kw["metadata"]


def test_update_field_flattened():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_field), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_field(field=gfa_field.Field(name="name_value"),)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].field == gfa_field.Field(name="name_value")


def test_update_field_flattened_error():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_field(
            firestore_admin.UpdateFieldRequest(),
            field=gfa_field.Field(name="name_value"),
        )


@pytest.mark.asyncio
async def test_update_field_flattened_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_field(field=gfa_field.Field(name="name_value"),)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].field == gfa_field.Field(name="name_value")


@pytest.mark.asyncio
async def test_update_field_flattened_error_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_field(
            firestore_admin.UpdateFieldRequest(),
            field=gfa_field.Field(name="name_value"),
        )


def test_list_fields(
    transport: str = "grpc", request_type=firestore_admin.ListFieldsRequest
):
    client = FirestoreAdminClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_fields), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = firestore_admin.ListFieldsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_fields(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == firestore_admin.ListFieldsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListFieldsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_fields_from_dict():
    test_list_fields(request_type=dict)


@pytest.mark.asyncio
async def test_list_fields_async(transport: str = "grpc_asyncio"):
    client = FirestoreAdminAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = firestore_admin.ListFieldsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_fields), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firestore_admin.ListFieldsResponse(next_page_token="next_page_token_value",)
        )

        response = await client.list_fields(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListFieldsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_fields_field_headers():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore_admin.ListFieldsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_fields), "__call__") as call:
        call.return_value = firestore_admin.ListFieldsResponse()

        client.list_fields(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_fields_field_headers_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore_admin.ListFieldsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_fields), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firestore_admin.ListFieldsResponse()
        )

        await client.list_fields(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_fields_flattened():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_fields), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = firestore_admin.ListFieldsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_fields(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_fields_flattened_error():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_fields(
            firestore_admin.ListFieldsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_fields_flattened_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_fields), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = firestore_admin.ListFieldsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firestore_admin.ListFieldsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_fields(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_fields_flattened_error_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_fields(
            firestore_admin.ListFieldsRequest(), parent="parent_value",
        )


def test_list_fields_pager():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_fields), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            firestore_admin.ListFieldsResponse(
                fields=[field.Field(), field.Field(), field.Field(),],
                next_page_token="abc",
            ),
            firestore_admin.ListFieldsResponse(fields=[], next_page_token="def",),
            firestore_admin.ListFieldsResponse(
                fields=[field.Field(),], next_page_token="ghi",
            ),
            firestore_admin.ListFieldsResponse(fields=[field.Field(), field.Field(),],),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_fields(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, field.Field) for i in results)


def test_list_fields_pages():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_fields), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            firestore_admin.ListFieldsResponse(
                fields=[field.Field(), field.Field(), field.Field(),],
                next_page_token="abc",
            ),
            firestore_admin.ListFieldsResponse(fields=[], next_page_token="def",),
            firestore_admin.ListFieldsResponse(
                fields=[field.Field(),], next_page_token="ghi",
            ),
            firestore_admin.ListFieldsResponse(fields=[field.Field(), field.Field(),],),
            RuntimeError,
        )
        pages = list(client.list_fields(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_fields_async_pager():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_fields),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            firestore_admin.ListFieldsResponse(
                fields=[field.Field(), field.Field(), field.Field(),],
                next_page_token="abc",
            ),
            firestore_admin.ListFieldsResponse(fields=[], next_page_token="def",),
            firestore_admin.ListFieldsResponse(
                fields=[field.Field(),], next_page_token="ghi",
            ),
            firestore_admin.ListFieldsResponse(fields=[field.Field(), field.Field(),],),
            RuntimeError,
        )
        async_pager = await client.list_fields(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, field.Field) for i in responses)


@pytest.mark.asyncio
async def test_list_fields_async_pages():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_fields),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            firestore_admin.ListFieldsResponse(
                fields=[field.Field(), field.Field(), field.Field(),],
                next_page_token="abc",
            ),
            firestore_admin.ListFieldsResponse(fields=[], next_page_token="def",),
            firestore_admin.ListFieldsResponse(
                fields=[field.Field(),], next_page_token="ghi",
            ),
            firestore_admin.ListFieldsResponse(fields=[field.Field(), field.Field(),],),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_fields(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_export_documents(
    transport: str = "grpc", request_type=firestore_admin.ExportDocumentsRequest
):
    client = FirestoreAdminClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.export_documents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.export_documents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == firestore_admin.ExportDocumentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_export_documents_from_dict():
    test_export_documents(request_type=dict)


@pytest.mark.asyncio
async def test_export_documents_async(transport: str = "grpc_asyncio"):
    client = FirestoreAdminAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = firestore_admin.ExportDocumentsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.export_documents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.export_documents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_export_documents_field_headers():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore_admin.ExportDocumentsRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.export_documents), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")

        client.export_documents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_export_documents_field_headers_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore_admin.ExportDocumentsRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.export_documents), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )

        await client.export_documents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_export_documents_flattened():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.export_documents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.export_documents(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_export_documents_flattened_error():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.export_documents(
            firestore_admin.ExportDocumentsRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_export_documents_flattened_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.export_documents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.export_documents(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_export_documents_flattened_error_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.export_documents(
            firestore_admin.ExportDocumentsRequest(), name="name_value",
        )


def test_import_documents(
    transport: str = "grpc", request_type=firestore_admin.ImportDocumentsRequest
):
    client = FirestoreAdminClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.import_documents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.import_documents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == firestore_admin.ImportDocumentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_import_documents_from_dict():
    test_import_documents(request_type=dict)


@pytest.mark.asyncio
async def test_import_documents_async(transport: str = "grpc_asyncio"):
    client = FirestoreAdminAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = firestore_admin.ImportDocumentsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.import_documents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.import_documents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_import_documents_field_headers():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore_admin.ImportDocumentsRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.import_documents), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")

        client.import_documents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_import_documents_field_headers_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore_admin.ImportDocumentsRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.import_documents), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )

        await client.import_documents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_import_documents_flattened():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.import_documents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.import_documents(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_import_documents_flattened_error():
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.import_documents(
            firestore_admin.ImportDocumentsRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_import_documents_flattened_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.import_documents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.import_documents(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_import_documents_flattened_error_async():
    client = FirestoreAdminAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.import_documents(
            firestore_admin.ImportDocumentsRequest(), name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.FirestoreAdminGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = FirestoreAdminClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.FirestoreAdminGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = FirestoreAdminClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.FirestoreAdminGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = FirestoreAdminClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.FirestoreAdminGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = FirestoreAdminClient(transport=transport)
    assert client._transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.FirestoreAdminGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.FirestoreAdminGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.FirestoreAdminGrpcTransport,
        transports.FirestoreAdminGrpcAsyncIOTransport,
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
    client = FirestoreAdminClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client._transport, transports.FirestoreAdminGrpcTransport,)


def test_firestore_admin_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.FirestoreAdminTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_firestore_admin_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.firestore_admin_v1.services.firestore_admin.transports.FirestoreAdminTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.FirestoreAdminTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_index",
        "list_indexes",
        "get_index",
        "delete_index",
        "get_field",
        "update_field",
        "list_fields",
        "export_documents",
        "import_documents",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


def test_firestore_admin_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.firestore_admin_v1.services.firestore_admin.transports.FirestoreAdminTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.FirestoreAdminTransport(
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


def test_firestore_admin_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.firestore_admin_v1.services.firestore_admin.transports.FirestoreAdminTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.FirestoreAdminTransport()
        adc.assert_called_once()


def test_firestore_admin_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        FirestoreAdminClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/datastore",
            ),
            quota_project_id=None,
        )


def test_firestore_admin_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.FirestoreAdminGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/datastore",
            ),
            quota_project_id="octopus",
        )


def test_firestore_admin_host_no_port():
    client = FirestoreAdminClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="firestore.googleapis.com"
        ),
    )
    assert client._transport._host == "firestore.googleapis.com:443"


def test_firestore_admin_host_with_port():
    client = FirestoreAdminClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="firestore.googleapis.com:8000"
        ),
    )
    assert client._transport._host == "firestore.googleapis.com:8000"


def test_firestore_admin_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.FirestoreAdminGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"


def test_firestore_admin_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.FirestoreAdminGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.FirestoreAdminGrpcTransport,
        transports.FirestoreAdminGrpcAsyncIOTransport,
    ],
)
def test_firestore_admin_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
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


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.FirestoreAdminGrpcTransport,
        transports.FirestoreAdminGrpcAsyncIOTransport,
    ],
)
def test_firestore_admin_transport_channel_mtls_with_adc(transport_class):
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


def test_firestore_admin_grpc_lro_client():
    client = FirestoreAdminClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )
    transport = client._transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_firestore_admin_grpc_lro_async_client():
    client = FirestoreAdminAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    transport = client._client._transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsAsyncClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_field_path():
    project = "squid"
    database = "clam"
    collection = "whelk"
    field = "octopus"

    expected = "projects/{project}/databases/{database}/collectionGroups/{collection}/fields/{field}".format(
        project=project, database=database, collection=collection, field=field,
    )
    actual = FirestoreAdminClient.field_path(project, database, collection, field)
    assert expected == actual


def test_parse_field_path():
    expected = {
        "project": "oyster",
        "database": "nudibranch",
        "collection": "cuttlefish",
        "field": "mussel",
    }
    path = FirestoreAdminClient.field_path(**expected)

    # Check that the path construction is reversible.
    actual = FirestoreAdminClient.parse_field_path(path)
    assert expected == actual


def test_index_path():
    project = "squid"
    database = "clam"
    collection = "whelk"
    index = "octopus"

    expected = "projects/{project}/databases/{database}/collectionGroups/{collection}/indexes/{index}".format(
        project=project, database=database, collection=collection, index=index,
    )
    actual = FirestoreAdminClient.index_path(project, database, collection, index)
    assert expected == actual


def test_parse_index_path():
    expected = {
        "project": "oyster",
        "database": "nudibranch",
        "collection": "cuttlefish",
        "index": "mussel",
    }
    path = FirestoreAdminClient.index_path(**expected)

    # Check that the path construction is reversible.
    actual = FirestoreAdminClient.parse_index_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.FirestoreAdminTransport, "_prep_wrapped_messages"
    ) as prep:
        client = FirestoreAdminClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.FirestoreAdminTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = FirestoreAdminClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
