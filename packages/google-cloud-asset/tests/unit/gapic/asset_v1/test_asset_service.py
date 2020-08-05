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
from google.api_core import operation_async
from google.api_core import operations_v1
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.asset_v1.services.asset_service import AssetServiceAsyncClient
from google.cloud.asset_v1.services.asset_service import AssetServiceClient
from google.cloud.asset_v1.services.asset_service import pagers
from google.cloud.asset_v1.services.asset_service import transports
from google.cloud.asset_v1.types import asset_service
from google.cloud.asset_v1.types import assets
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.type import expr_pb2 as expr  # type: ignore


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

    assert AssetServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        AssetServiceClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        AssetServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        AssetServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        AssetServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert AssetServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [AssetServiceClient, AssetServiceAsyncClient])
def test_asset_service_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "cloudasset.googleapis.com:443"


def test_asset_service_client_get_transport_class():
    transport = AssetServiceClient.get_transport_class()
    assert transport == transports.AssetServiceGrpcTransport

    transport = AssetServiceClient.get_transport_class("grpc")
    assert transport == transports.AssetServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (AssetServiceClient, transports.AssetServiceGrpcTransport, "grpc"),
        (
            AssetServiceAsyncClient,
            transports.AssetServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    AssetServiceClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AssetServiceClient)
)
@mock.patch.object(
    AssetServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AssetServiceAsyncClient),
)
def test_asset_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(AssetServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(AssetServiceClient, "get_transport_class") as gtc:
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
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
            quota_project_id=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_ENDPOINT,
                client_cert_source=None,
                quota_project_id=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                client_cert_source=None,
                quota_project_id=None,
            )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and client_cert_source is provided.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "auto"}):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                client_cert_source=client_cert_source_callback,
                quota_project_id=None,
            )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and default_client_cert_source is provided.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "auto"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                patched.return_value = None
                client = client_class()
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_MTLS_ENDPOINT,
                    scopes=None,
                    api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                    client_cert_source=None,
                    quota_project_id=None,
                )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", but client_cert_source and default_client_cert_source are None.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "auto"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class()
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    api_mtls_endpoint=client.DEFAULT_ENDPOINT,
                    client_cert_source=None,
                    quota_project_id=None,
                )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
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
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (AssetServiceClient, transports.AssetServiceGrpcTransport, "grpc"),
        (
            AssetServiceAsyncClient,
            transports.AssetServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_asset_service_client_client_options_scopes(
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
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (AssetServiceClient, transports.AssetServiceGrpcTransport, "grpc"),
        (
            AssetServiceAsyncClient,
            transports.AssetServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_asset_service_client_client_options_credentials_file(
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
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            quota_project_id=None,
        )


def test_asset_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.asset_v1.services.asset_service.transports.AssetServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = AssetServiceClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
            quota_project_id=None,
        )


def test_export_assets(
    transport: str = "grpc", request_type=asset_service.ExportAssetsRequest
):
    client = AssetServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.export_assets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.export_assets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == asset_service.ExportAssetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_export_assets_from_dict():
    test_export_assets(request_type=dict)


@pytest.mark.asyncio
async def test_export_assets_async(transport: str = "grpc_asyncio"):
    client = AssetServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = asset_service.ExportAssetsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.export_assets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.export_assets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_export_assets_field_headers():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.ExportAssetsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.export_assets), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")

        client.export_assets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_export_assets_field_headers_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.ExportAssetsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.export_assets), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )

        await client.export_assets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_batch_get_assets_history(
    transport: str = "grpc", request_type=asset_service.BatchGetAssetsHistoryRequest
):
    client = AssetServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_get_assets_history), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.BatchGetAssetsHistoryResponse()

        response = client.batch_get_assets_history(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == asset_service.BatchGetAssetsHistoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.BatchGetAssetsHistoryResponse)


def test_batch_get_assets_history_from_dict():
    test_batch_get_assets_history(request_type=dict)


@pytest.mark.asyncio
async def test_batch_get_assets_history_async(transport: str = "grpc_asyncio"):
    client = AssetServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = asset_service.BatchGetAssetsHistoryRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.batch_get_assets_history), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            asset_service.BatchGetAssetsHistoryResponse()
        )

        response = await client.batch_get_assets_history(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.BatchGetAssetsHistoryResponse)


def test_batch_get_assets_history_field_headers():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.BatchGetAssetsHistoryRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_get_assets_history), "__call__"
    ) as call:
        call.return_value = asset_service.BatchGetAssetsHistoryResponse()

        client.batch_get_assets_history(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_get_assets_history_field_headers_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.BatchGetAssetsHistoryRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.batch_get_assets_history), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            asset_service.BatchGetAssetsHistoryResponse()
        )

        await client.batch_get_assets_history(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_feed(
    transport: str = "grpc", request_type=asset_service.CreateFeedRequest
):
    client = AssetServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_feed), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.Feed(
            name="name_value",
            asset_names=["asset_names_value"],
            asset_types=["asset_types_value"],
            content_type=asset_service.ContentType.RESOURCE,
        )

        response = client.create_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == asset_service.CreateFeedRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.Feed)

    assert response.name == "name_value"

    assert response.asset_names == ["asset_names_value"]

    assert response.asset_types == ["asset_types_value"]

    assert response.content_type == asset_service.ContentType.RESOURCE


def test_create_feed_from_dict():
    test_create_feed(request_type=dict)


@pytest.mark.asyncio
async def test_create_feed_async(transport: str = "grpc_asyncio"):
    client = AssetServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = asset_service.CreateFeedRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_feed), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            asset_service.Feed(
                name="name_value",
                asset_names=["asset_names_value"],
                asset_types=["asset_types_value"],
                content_type=asset_service.ContentType.RESOURCE,
            )
        )

        response = await client.create_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.Feed)

    assert response.name == "name_value"

    assert response.asset_names == ["asset_names_value"]

    assert response.asset_types == ["asset_types_value"]

    assert response.content_type == asset_service.ContentType.RESOURCE


def test_create_feed_field_headers():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.CreateFeedRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_feed), "__call__") as call:
        call.return_value = asset_service.Feed()

        client.create_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_feed_field_headers_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.CreateFeedRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_feed), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.Feed())

        await client.create_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_feed_flattened():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_feed), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.Feed()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_feed(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_create_feed_flattened_error():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_feed(
            asset_service.CreateFeedRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_create_feed_flattened_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_feed), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.Feed()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.Feed())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_feed(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_create_feed_flattened_error_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_feed(
            asset_service.CreateFeedRequest(), parent="parent_value",
        )


def test_get_feed(transport: str = "grpc", request_type=asset_service.GetFeedRequest):
    client = AssetServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_feed), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.Feed(
            name="name_value",
            asset_names=["asset_names_value"],
            asset_types=["asset_types_value"],
            content_type=asset_service.ContentType.RESOURCE,
        )

        response = client.get_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == asset_service.GetFeedRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.Feed)

    assert response.name == "name_value"

    assert response.asset_names == ["asset_names_value"]

    assert response.asset_types == ["asset_types_value"]

    assert response.content_type == asset_service.ContentType.RESOURCE


def test_get_feed_from_dict():
    test_get_feed(request_type=dict)


@pytest.mark.asyncio
async def test_get_feed_async(transport: str = "grpc_asyncio"):
    client = AssetServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = asset_service.GetFeedRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_feed), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            asset_service.Feed(
                name="name_value",
                asset_names=["asset_names_value"],
                asset_types=["asset_types_value"],
                content_type=asset_service.ContentType.RESOURCE,
            )
        )

        response = await client.get_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.Feed)

    assert response.name == "name_value"

    assert response.asset_names == ["asset_names_value"]

    assert response.asset_types == ["asset_types_value"]

    assert response.content_type == asset_service.ContentType.RESOURCE


def test_get_feed_field_headers():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.GetFeedRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_feed), "__call__") as call:
        call.return_value = asset_service.Feed()

        client.get_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_feed_field_headers_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.GetFeedRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_feed), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.Feed())

        await client.get_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_feed_flattened():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_feed), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.Feed()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_feed(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_feed_flattened_error():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_feed(
            asset_service.GetFeedRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_feed_flattened_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_feed), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.Feed()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.Feed())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_feed(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_feed_flattened_error_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_feed(
            asset_service.GetFeedRequest(), name="name_value",
        )


def test_list_feeds(
    transport: str = "grpc", request_type=asset_service.ListFeedsRequest
):
    client = AssetServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_feeds), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.ListFeedsResponse()

        response = client.list_feeds(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == asset_service.ListFeedsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.ListFeedsResponse)


def test_list_feeds_from_dict():
    test_list_feeds(request_type=dict)


@pytest.mark.asyncio
async def test_list_feeds_async(transport: str = "grpc_asyncio"):
    client = AssetServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = asset_service.ListFeedsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_feeds), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            asset_service.ListFeedsResponse()
        )

        response = await client.list_feeds(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.ListFeedsResponse)


def test_list_feeds_field_headers():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.ListFeedsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_feeds), "__call__") as call:
        call.return_value = asset_service.ListFeedsResponse()

        client.list_feeds(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_feeds_field_headers_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.ListFeedsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_feeds), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            asset_service.ListFeedsResponse()
        )

        await client.list_feeds(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_feeds_flattened():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_feeds), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.ListFeedsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_feeds(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_feeds_flattened_error():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_feeds(
            asset_service.ListFeedsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_feeds_flattened_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_feeds), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.ListFeedsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            asset_service.ListFeedsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_feeds(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_feeds_flattened_error_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_feeds(
            asset_service.ListFeedsRequest(), parent="parent_value",
        )


def test_update_feed(
    transport: str = "grpc", request_type=asset_service.UpdateFeedRequest
):
    client = AssetServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_feed), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.Feed(
            name="name_value",
            asset_names=["asset_names_value"],
            asset_types=["asset_types_value"],
            content_type=asset_service.ContentType.RESOURCE,
        )

        response = client.update_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == asset_service.UpdateFeedRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.Feed)

    assert response.name == "name_value"

    assert response.asset_names == ["asset_names_value"]

    assert response.asset_types == ["asset_types_value"]

    assert response.content_type == asset_service.ContentType.RESOURCE


def test_update_feed_from_dict():
    test_update_feed(request_type=dict)


@pytest.mark.asyncio
async def test_update_feed_async(transport: str = "grpc_asyncio"):
    client = AssetServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = asset_service.UpdateFeedRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_feed), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            asset_service.Feed(
                name="name_value",
                asset_names=["asset_names_value"],
                asset_types=["asset_types_value"],
                content_type=asset_service.ContentType.RESOURCE,
            )
        )

        response = await client.update_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.Feed)

    assert response.name == "name_value"

    assert response.asset_names == ["asset_names_value"]

    assert response.asset_types == ["asset_types_value"]

    assert response.content_type == asset_service.ContentType.RESOURCE


def test_update_feed_field_headers():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.UpdateFeedRequest()
    request.feed.name = "feed.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_feed), "__call__") as call:
        call.return_value = asset_service.Feed()

        client.update_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "feed.name=feed.name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_feed_field_headers_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.UpdateFeedRequest()
    request.feed.name = "feed.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_feed), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.Feed())

        await client.update_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "feed.name=feed.name/value",) in kw["metadata"]


def test_update_feed_flattened():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_feed), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.Feed()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_feed(feed=asset_service.Feed(name="name_value"),)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].feed == asset_service.Feed(name="name_value")


def test_update_feed_flattened_error():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_feed(
            asset_service.UpdateFeedRequest(),
            feed=asset_service.Feed(name="name_value"),
        )


@pytest.mark.asyncio
async def test_update_feed_flattened_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_feed), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.Feed()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.Feed())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_feed(feed=asset_service.Feed(name="name_value"),)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].feed == asset_service.Feed(name="name_value")


@pytest.mark.asyncio
async def test_update_feed_flattened_error_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_feed(
            asset_service.UpdateFeedRequest(),
            feed=asset_service.Feed(name="name_value"),
        )


def test_delete_feed(
    transport: str = "grpc", request_type=asset_service.DeleteFeedRequest
):
    client = AssetServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_feed), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == asset_service.DeleteFeedRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_feed_from_dict():
    test_delete_feed(request_type=dict)


@pytest.mark.asyncio
async def test_delete_feed_async(transport: str = "grpc_asyncio"):
    client = AssetServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = asset_service.DeleteFeedRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_feed), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_feed_field_headers():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.DeleteFeedRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_feed), "__call__") as call:
        call.return_value = None

        client.delete_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_feed_field_headers_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.DeleteFeedRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_feed), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_feed_flattened():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_feed), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_feed(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_feed_flattened_error():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_feed(
            asset_service.DeleteFeedRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_feed_flattened_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_feed), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_feed(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_feed_flattened_error_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_feed(
            asset_service.DeleteFeedRequest(), name="name_value",
        )


def test_search_all_resources(
    transport: str = "grpc", request_type=asset_service.SearchAllResourcesRequest
):
    client = AssetServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.search_all_resources), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.SearchAllResourcesResponse(
            next_page_token="next_page_token_value",
        )

        response = client.search_all_resources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == asset_service.SearchAllResourcesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchAllResourcesPager)

    assert response.next_page_token == "next_page_token_value"


def test_search_all_resources_from_dict():
    test_search_all_resources(request_type=dict)


@pytest.mark.asyncio
async def test_search_all_resources_async(transport: str = "grpc_asyncio"):
    client = AssetServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = asset_service.SearchAllResourcesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_all_resources), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            asset_service.SearchAllResourcesResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.search_all_resources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchAllResourcesAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_search_all_resources_field_headers():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.SearchAllResourcesRequest()
    request.scope = "scope/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.search_all_resources), "__call__"
    ) as call:
        call.return_value = asset_service.SearchAllResourcesResponse()

        client.search_all_resources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "scope=scope/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_search_all_resources_field_headers_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.SearchAllResourcesRequest()
    request.scope = "scope/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_all_resources), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            asset_service.SearchAllResourcesResponse()
        )

        await client.search_all_resources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "scope=scope/value",) in kw["metadata"]


def test_search_all_resources_flattened():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.search_all_resources), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.SearchAllResourcesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.search_all_resources(
            scope="scope_value", query="query_value", asset_types=["asset_types_value"],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].scope == "scope_value"

        assert args[0].query == "query_value"

        assert args[0].asset_types == ["asset_types_value"]


def test_search_all_resources_flattened_error():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.search_all_resources(
            asset_service.SearchAllResourcesRequest(),
            scope="scope_value",
            query="query_value",
            asset_types=["asset_types_value"],
        )


@pytest.mark.asyncio
async def test_search_all_resources_flattened_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_all_resources), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.SearchAllResourcesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            asset_service.SearchAllResourcesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.search_all_resources(
            scope="scope_value", query="query_value", asset_types=["asset_types_value"],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].scope == "scope_value"

        assert args[0].query == "query_value"

        assert args[0].asset_types == ["asset_types_value"]


@pytest.mark.asyncio
async def test_search_all_resources_flattened_error_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.search_all_resources(
            asset_service.SearchAllResourcesRequest(),
            scope="scope_value",
            query="query_value",
            asset_types=["asset_types_value"],
        )


def test_search_all_resources_pager():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.search_all_resources), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            asset_service.SearchAllResourcesResponse(
                results=[
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                ],
                next_page_token="abc",
            ),
            asset_service.SearchAllResourcesResponse(
                results=[], next_page_token="def",
            ),
            asset_service.SearchAllResourcesResponse(
                results=[assets.ResourceSearchResult(),], next_page_token="ghi",
            ),
            asset_service.SearchAllResourcesResponse(
                results=[assets.ResourceSearchResult(), assets.ResourceSearchResult(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("scope", ""),)),
        )
        pager = client.search_all_resources(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, assets.ResourceSearchResult) for i in results)


def test_search_all_resources_pages():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.search_all_resources), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            asset_service.SearchAllResourcesResponse(
                results=[
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                ],
                next_page_token="abc",
            ),
            asset_service.SearchAllResourcesResponse(
                results=[], next_page_token="def",
            ),
            asset_service.SearchAllResourcesResponse(
                results=[assets.ResourceSearchResult(),], next_page_token="ghi",
            ),
            asset_service.SearchAllResourcesResponse(
                results=[assets.ResourceSearchResult(), assets.ResourceSearchResult(),],
            ),
            RuntimeError,
        )
        pages = list(client.search_all_resources(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_search_all_resources_async_pager():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_all_resources),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            asset_service.SearchAllResourcesResponse(
                results=[
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                ],
                next_page_token="abc",
            ),
            asset_service.SearchAllResourcesResponse(
                results=[], next_page_token="def",
            ),
            asset_service.SearchAllResourcesResponse(
                results=[assets.ResourceSearchResult(),], next_page_token="ghi",
            ),
            asset_service.SearchAllResourcesResponse(
                results=[assets.ResourceSearchResult(), assets.ResourceSearchResult(),],
            ),
            RuntimeError,
        )
        async_pager = await client.search_all_resources(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, assets.ResourceSearchResult) for i in responses)


@pytest.mark.asyncio
async def test_search_all_resources_async_pages():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_all_resources),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            asset_service.SearchAllResourcesResponse(
                results=[
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                ],
                next_page_token="abc",
            ),
            asset_service.SearchAllResourcesResponse(
                results=[], next_page_token="def",
            ),
            asset_service.SearchAllResourcesResponse(
                results=[assets.ResourceSearchResult(),], next_page_token="ghi",
            ),
            asset_service.SearchAllResourcesResponse(
                results=[assets.ResourceSearchResult(), assets.ResourceSearchResult(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.search_all_resources(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_search_all_iam_policies(
    transport: str = "grpc", request_type=asset_service.SearchAllIamPoliciesRequest
):
    client = AssetServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.search_all_iam_policies), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.SearchAllIamPoliciesResponse(
            next_page_token="next_page_token_value",
        )

        response = client.search_all_iam_policies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == asset_service.SearchAllIamPoliciesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchAllIamPoliciesPager)

    assert response.next_page_token == "next_page_token_value"


def test_search_all_iam_policies_from_dict():
    test_search_all_iam_policies(request_type=dict)


@pytest.mark.asyncio
async def test_search_all_iam_policies_async(transport: str = "grpc_asyncio"):
    client = AssetServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = asset_service.SearchAllIamPoliciesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_all_iam_policies), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            asset_service.SearchAllIamPoliciesResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.search_all_iam_policies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchAllIamPoliciesAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_search_all_iam_policies_field_headers():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.SearchAllIamPoliciesRequest()
    request.scope = "scope/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.search_all_iam_policies), "__call__"
    ) as call:
        call.return_value = asset_service.SearchAllIamPoliciesResponse()

        client.search_all_iam_policies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "scope=scope/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_search_all_iam_policies_field_headers_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.SearchAllIamPoliciesRequest()
    request.scope = "scope/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_all_iam_policies), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            asset_service.SearchAllIamPoliciesResponse()
        )

        await client.search_all_iam_policies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "scope=scope/value",) in kw["metadata"]


def test_search_all_iam_policies_flattened():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.search_all_iam_policies), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.SearchAllIamPoliciesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.search_all_iam_policies(
            scope="scope_value", query="query_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].scope == "scope_value"

        assert args[0].query == "query_value"


def test_search_all_iam_policies_flattened_error():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.search_all_iam_policies(
            asset_service.SearchAllIamPoliciesRequest(),
            scope="scope_value",
            query="query_value",
        )


@pytest.mark.asyncio
async def test_search_all_iam_policies_flattened_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_all_iam_policies), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.SearchAllIamPoliciesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            asset_service.SearchAllIamPoliciesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.search_all_iam_policies(
            scope="scope_value", query="query_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].scope == "scope_value"

        assert args[0].query == "query_value"


@pytest.mark.asyncio
async def test_search_all_iam_policies_flattened_error_async():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.search_all_iam_policies(
            asset_service.SearchAllIamPoliciesRequest(),
            scope="scope_value",
            query="query_value",
        )


def test_search_all_iam_policies_pager():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.search_all_iam_policies), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                ],
                next_page_token="abc",
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[], next_page_token="def",
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[assets.IamPolicySearchResult(),], next_page_token="ghi",
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("scope", ""),)),
        )
        pager = client.search_all_iam_policies(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, assets.IamPolicySearchResult) for i in results)


def test_search_all_iam_policies_pages():
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.search_all_iam_policies), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                ],
                next_page_token="abc",
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[], next_page_token="def",
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[assets.IamPolicySearchResult(),], next_page_token="ghi",
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.search_all_iam_policies(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_search_all_iam_policies_async_pager():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_all_iam_policies),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                ],
                next_page_token="abc",
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[], next_page_token="def",
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[assets.IamPolicySearchResult(),], next_page_token="ghi",
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.search_all_iam_policies(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, assets.IamPolicySearchResult) for i in responses)


@pytest.mark.asyncio
async def test_search_all_iam_policies_async_pages():
    client = AssetServiceAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_all_iam_policies),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                ],
                next_page_token="abc",
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[], next_page_token="def",
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[assets.IamPolicySearchResult(),], next_page_token="ghi",
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.search_all_iam_policies(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.AssetServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AssetServiceClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.AssetServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AssetServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.AssetServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AssetServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AssetServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = AssetServiceClient(transport=transport)
    assert client._transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AssetServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.AssetServiceGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = AssetServiceClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client._transport, transports.AssetServiceGrpcTransport,)


def test_asset_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.AssetServiceTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_asset_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.asset_v1.services.asset_service.transports.AssetServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.AssetServiceTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "export_assets",
        "batch_get_assets_history",
        "create_feed",
        "get_feed",
        "list_feeds",
        "update_feed",
        "delete_feed",
        "search_all_resources",
        "search_all_iam_policies",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


def test_asset_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.asset_v1.services.asset_service.transports.AssetServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.AssetServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_asset_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        AssetServiceClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


def test_asset_service_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.AssetServiceGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_asset_service_host_no_port():
    client = AssetServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudasset.googleapis.com"
        ),
    )
    assert client._transport._host == "cloudasset.googleapis.com:443"


def test_asset_service_host_with_port():
    client = AssetServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudasset.googleapis.com:8000"
        ),
    )
    assert client._transport._host == "cloudasset.googleapis.com:8000"


def test_asset_service_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.AssetServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


def test_asset_service_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.AssetServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_asset_service_grpc_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.AssetServiceGrpcTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        credentials_file=None,
        scopes=("https://www.googleapis.com/auth/cloud-platform",),
        ssl_credentials=mock_ssl_cred,
        quota_project_id=None,
    )
    assert transport.grpc_channel == mock_grpc_channel


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers_async.create_channel", autospec=True)
def test_asset_service_grpc_asyncio_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.AssetServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        credentials_file=None,
        scopes=("https://www.googleapis.com/auth/cloud-platform",),
        ssl_credentials=mock_ssl_cred,
        quota_project_id=None,
    )
    assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_asset_service_grpc_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.AssetServiceGrpcTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            credentials_file=None,
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            ssl_credentials=mock_ssl_cred,
            quota_project_id=None,
        )
        assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers_async.create_channel", autospec=True)
def test_asset_service_grpc_asyncio_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.AssetServiceGrpcAsyncIOTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            credentials_file=None,
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            ssl_credentials=mock_ssl_cred,
            quota_project_id=None,
        )
        assert transport.grpc_channel == mock_grpc_channel


def test_asset_service_grpc_lro_client():
    client = AssetServiceClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )
    transport = client._transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_asset_service_grpc_lro_async_client():
    client = AssetServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    transport = client._client._transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsAsyncClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_feed_path():
    project = "squid"
    feed = "clam"

    expected = "projects/{project}/feeds/{feed}".format(project=project, feed=feed,)
    actual = AssetServiceClient.feed_path(project, feed)
    assert expected == actual


def test_parse_feed_path():
    expected = {
        "project": "whelk",
        "feed": "octopus",
    }
    path = AssetServiceClient.feed_path(**expected)

    # Check that the path construction is reversible.
    actual = AssetServiceClient.parse_feed_path(path)
    assert expected == actual
