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
from google.cloud.devtools.cloudbuild_v1.services.cloud_build import (
    CloudBuildAsyncClient,
)
from google.cloud.devtools.cloudbuild_v1.services.cloud_build import CloudBuildClient
from google.cloud.devtools.cloudbuild_v1.services.cloud_build import pagers
from google.cloud.devtools.cloudbuild_v1.services.cloud_build import transports
from google.cloud.devtools.cloudbuild_v1.types import cloudbuild
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert CloudBuildClient._get_default_mtls_endpoint(None) is None
    assert (
        CloudBuildClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        CloudBuildClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CloudBuildClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CloudBuildClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert CloudBuildClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [CloudBuildClient, CloudBuildAsyncClient])
def test_cloud_build_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "cloudbuild.googleapis.com:443"


def test_cloud_build_client_get_transport_class():
    transport = CloudBuildClient.get_transport_class()
    assert transport == transports.CloudBuildGrpcTransport

    transport = CloudBuildClient.get_transport_class("grpc")
    assert transport == transports.CloudBuildGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CloudBuildClient, transports.CloudBuildGrpcTransport, "grpc"),
        (
            CloudBuildAsyncClient,
            transports.CloudBuildGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_cloud_build_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(CloudBuildClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(CloudBuildClient, "get_transport_class") as gtc:
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
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "never".
    os.environ["GOOGLE_API_USE_MTLS"] = "never"
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
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "always".
    os.environ["GOOGLE_API_USE_MTLS"] = "always"
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
        )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and client_cert_source is provided.
    os.environ["GOOGLE_API_USE_MTLS"] = "auto"
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
        )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and default_client_cert_source is provided.
    os.environ["GOOGLE_API_USE_MTLS"] = "auto"
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
            )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", but client_cert_source and default_client_cert_source are None.
    os.environ["GOOGLE_API_USE_MTLS"] = "auto"
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
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS has
    # unsupported value.
    os.environ["GOOGLE_API_USE_MTLS"] = "Unsupported"
    with pytest.raises(MutualTLSChannelError):
        client = client_class()

    del os.environ["GOOGLE_API_USE_MTLS"]


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CloudBuildClient, transports.CloudBuildGrpcTransport, "grpc"),
        (
            CloudBuildAsyncClient,
            transports.CloudBuildGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_cloud_build_client_client_options_scopes(
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
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CloudBuildClient, transports.CloudBuildGrpcTransport, "grpc"),
        (
            CloudBuildAsyncClient,
            transports.CloudBuildGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_cloud_build_client_client_options_credentials_file(
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
        )


def test_cloud_build_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.devtools.cloudbuild_v1.services.cloud_build.transports.CloudBuildGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = CloudBuildClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
        )


def test_create_build(transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.CreateBuildRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.create_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_build_async(transport: str = "grpc_asyncio"):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.CreateBuildRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_build), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.create_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_build_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_build(
            project_id="project_id_value", build=cloudbuild.Build(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].build == cloudbuild.Build(id="id_value")


def test_create_build_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_build(
            cloudbuild.CreateBuildRequest(),
            project_id="project_id_value",
            build=cloudbuild.Build(id="id_value"),
        )


@pytest.mark.asyncio
async def test_create_build_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_build), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_build(
            project_id="project_id_value", build=cloudbuild.Build(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].build == cloudbuild.Build(id="id_value")


@pytest.mark.asyncio
async def test_create_build_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_build(
            cloudbuild.CreateBuildRequest(),
            project_id="project_id_value",
            build=cloudbuild.Build(id="id_value"),
        )


def test_get_build(transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.GetBuildRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build(
            id="id_value",
            project_id="project_id_value",
            status=cloudbuild.Build.Status.QUEUED,
            status_detail="status_detail_value",
            images=["images_value"],
            logs_bucket="logs_bucket_value",
            build_trigger_id="build_trigger_id_value",
            log_url="log_url_value",
            tags=["tags_value"],
        )

        response = client.get_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.Build)

    assert response.id == "id_value"

    assert response.project_id == "project_id_value"

    assert response.status == cloudbuild.Build.Status.QUEUED

    assert response.status_detail == "status_detail_value"

    assert response.images == ["images_value"]

    assert response.logs_bucket == "logs_bucket_value"

    assert response.build_trigger_id == "build_trigger_id_value"

    assert response.log_url == "log_url_value"

    assert response.tags == ["tags_value"]


@pytest.mark.asyncio
async def test_get_build_async(transport: str = "grpc_asyncio"):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.GetBuildRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_build), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.Build(
                id="id_value",
                project_id="project_id_value",
                status=cloudbuild.Build.Status.QUEUED,
                status_detail="status_detail_value",
                images=["images_value"],
                logs_bucket="logs_bucket_value",
                build_trigger_id="build_trigger_id_value",
                log_url="log_url_value",
                tags=["tags_value"],
            )
        )

        response = await client.get_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.Build)

    assert response.id == "id_value"

    assert response.project_id == "project_id_value"

    assert response.status == cloudbuild.Build.Status.QUEUED

    assert response.status_detail == "status_detail_value"

    assert response.images == ["images_value"]

    assert response.logs_bucket == "logs_bucket_value"

    assert response.build_trigger_id == "build_trigger_id_value"

    assert response.log_url == "log_url_value"

    assert response.tags == ["tags_value"]


def test_get_build_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_build(
            project_id="project_id_value", id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].id == "id_value"


def test_get_build_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_build(
            cloudbuild.GetBuildRequest(), project_id="project_id_value", id="id_value",
        )


@pytest.mark.asyncio
async def test_get_build_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_build), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cloudbuild.Build())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_build(project_id="project_id_value", id="id_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].id == "id_value"


@pytest.mark.asyncio
async def test_get_build_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_build(
            cloudbuild.GetBuildRequest(), project_id="project_id_value", id="id_value",
        )


def test_list_builds(transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.ListBuildsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_builds), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_builds(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBuildsPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_builds_async(transport: str = "grpc_asyncio"):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.ListBuildsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_builds), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListBuildsResponse(next_page_token="next_page_token_value",)
        )

        response = await client.list_builds(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBuildsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_builds_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_builds), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_builds(
            project_id="project_id_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].filter == "filter_value"


def test_list_builds_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_builds(
            cloudbuild.ListBuildsRequest(),
            project_id="project_id_value",
            filter="filter_value",
        )


@pytest.mark.asyncio
async def test_list_builds_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_builds), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListBuildsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_builds(
            project_id="project_id_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].filter == "filter_value"


@pytest.mark.asyncio
async def test_list_builds_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_builds(
            cloudbuild.ListBuildsRequest(),
            project_id="project_id_value",
            filter="filter_value",
        )


def test_list_builds_pager():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_builds), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(), cloudbuild.Build(), cloudbuild.Build(),],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildsResponse(builds=[], next_page_token="def",),
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(),], next_page_token="ghi",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(), cloudbuild.Build(),],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_builds(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, cloudbuild.Build) for i in results)


def test_list_builds_pages():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_builds), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(), cloudbuild.Build(), cloudbuild.Build(),],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildsResponse(builds=[], next_page_token="def",),
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(),], next_page_token="ghi",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(), cloudbuild.Build(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_builds(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_builds_async_pager():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_builds),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(), cloudbuild.Build(), cloudbuild.Build(),],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildsResponse(builds=[], next_page_token="def",),
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(),], next_page_token="ghi",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(), cloudbuild.Build(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_builds(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloudbuild.Build) for i in responses)


@pytest.mark.asyncio
async def test_list_builds_async_pages():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_builds),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(), cloudbuild.Build(), cloudbuild.Build(),],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildsResponse(builds=[], next_page_token="def",),
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(),], next_page_token="ghi",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(), cloudbuild.Build(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.list_builds(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_cancel_build(transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.CancelBuildRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.cancel_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build(
            id="id_value",
            project_id="project_id_value",
            status=cloudbuild.Build.Status.QUEUED,
            status_detail="status_detail_value",
            images=["images_value"],
            logs_bucket="logs_bucket_value",
            build_trigger_id="build_trigger_id_value",
            log_url="log_url_value",
            tags=["tags_value"],
        )

        response = client.cancel_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.Build)

    assert response.id == "id_value"

    assert response.project_id == "project_id_value"

    assert response.status == cloudbuild.Build.Status.QUEUED

    assert response.status_detail == "status_detail_value"

    assert response.images == ["images_value"]

    assert response.logs_bucket == "logs_bucket_value"

    assert response.build_trigger_id == "build_trigger_id_value"

    assert response.log_url == "log_url_value"

    assert response.tags == ["tags_value"]


@pytest.mark.asyncio
async def test_cancel_build_async(transport: str = "grpc_asyncio"):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.CancelBuildRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.cancel_build), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.Build(
                id="id_value",
                project_id="project_id_value",
                status=cloudbuild.Build.Status.QUEUED,
                status_detail="status_detail_value",
                images=["images_value"],
                logs_bucket="logs_bucket_value",
                build_trigger_id="build_trigger_id_value",
                log_url="log_url_value",
                tags=["tags_value"],
            )
        )

        response = await client.cancel_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.Build)

    assert response.id == "id_value"

    assert response.project_id == "project_id_value"

    assert response.status == cloudbuild.Build.Status.QUEUED

    assert response.status_detail == "status_detail_value"

    assert response.images == ["images_value"]

    assert response.logs_bucket == "logs_bucket_value"

    assert response.build_trigger_id == "build_trigger_id_value"

    assert response.log_url == "log_url_value"

    assert response.tags == ["tags_value"]


def test_cancel_build_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.cancel_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.cancel_build(
            project_id="project_id_value", id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].id == "id_value"


def test_cancel_build_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.cancel_build(
            cloudbuild.CancelBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


@pytest.mark.asyncio
async def test_cancel_build_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.cancel_build), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cloudbuild.Build())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.cancel_build(
            project_id="project_id_value", id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].id == "id_value"


@pytest.mark.asyncio
async def test_cancel_build_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.cancel_build(
            cloudbuild.CancelBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


def test_retry_build(transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.RetryBuildRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.retry_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.retry_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_retry_build_async(transport: str = "grpc_asyncio"):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.RetryBuildRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.retry_build), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.retry_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_retry_build_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.retry_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.retry_build(
            project_id="project_id_value", id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].id == "id_value"


def test_retry_build_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.retry_build(
            cloudbuild.RetryBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


@pytest.mark.asyncio
async def test_retry_build_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.retry_build), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.retry_build(
            project_id="project_id_value", id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].id == "id_value"


@pytest.mark.asyncio
async def test_retry_build_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.retry_build(
            cloudbuild.RetryBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


def test_create_build_trigger(transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.CreateBuildTriggerRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger(
            id="id_value",
            description="description_value",
            name="name_value",
            tags=["tags_value"],
            disabled=True,
            ignored_files=["ignored_files_value"],
            included_files=["included_files_value"],
            build=cloudbuild.Build(id="id_value"),
        )

        response = client.create_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)

    assert response.id == "id_value"

    assert response.description == "description_value"

    assert response.name == "name_value"

    assert response.tags == ["tags_value"]

    assert response.disabled is True

    assert response.ignored_files == ["ignored_files_value"]

    assert response.included_files == ["included_files_value"]


@pytest.mark.asyncio
async def test_create_build_trigger_async(transport: str = "grpc_asyncio"):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.CreateBuildTriggerRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger(
                id="id_value",
                description="description_value",
                name="name_value",
                tags=["tags_value"],
                disabled=True,
                ignored_files=["ignored_files_value"],
                included_files=["included_files_value"],
            )
        )

        response = await client.create_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)

    assert response.id == "id_value"

    assert response.description == "description_value"

    assert response.name == "name_value"

    assert response.tags == ["tags_value"]

    assert response.disabled is True

    assert response.ignored_files == ["ignored_files_value"]

    assert response.included_files == ["included_files_value"]


def test_create_build_trigger_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_build_trigger(
            project_id="project_id_value",
            trigger=cloudbuild.BuildTrigger(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].trigger == cloudbuild.BuildTrigger(id="id_value")


def test_create_build_trigger_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_build_trigger(
            cloudbuild.CreateBuildTriggerRequest(),
            project_id="project_id_value",
            trigger=cloudbuild.BuildTrigger(id="id_value"),
        )


@pytest.mark.asyncio
async def test_create_build_trigger_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_build_trigger(
            project_id="project_id_value",
            trigger=cloudbuild.BuildTrigger(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].trigger == cloudbuild.BuildTrigger(id="id_value")


@pytest.mark.asyncio
async def test_create_build_trigger_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_build_trigger(
            cloudbuild.CreateBuildTriggerRequest(),
            project_id="project_id_value",
            trigger=cloudbuild.BuildTrigger(id="id_value"),
        )


def test_get_build_trigger(transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.GetBuildTriggerRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger(
            id="id_value",
            description="description_value",
            name="name_value",
            tags=["tags_value"],
            disabled=True,
            ignored_files=["ignored_files_value"],
            included_files=["included_files_value"],
            build=cloudbuild.Build(id="id_value"),
        )

        response = client.get_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)

    assert response.id == "id_value"

    assert response.description == "description_value"

    assert response.name == "name_value"

    assert response.tags == ["tags_value"]

    assert response.disabled is True

    assert response.ignored_files == ["ignored_files_value"]

    assert response.included_files == ["included_files_value"]


@pytest.mark.asyncio
async def test_get_build_trigger_async(transport: str = "grpc_asyncio"):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.GetBuildTriggerRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger(
                id="id_value",
                description="description_value",
                name="name_value",
                tags=["tags_value"],
                disabled=True,
                ignored_files=["ignored_files_value"],
                included_files=["included_files_value"],
            )
        )

        response = await client.get_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)

    assert response.id == "id_value"

    assert response.description == "description_value"

    assert response.name == "name_value"

    assert response.tags == ["tags_value"]

    assert response.disabled is True

    assert response.ignored_files == ["ignored_files_value"]

    assert response.included_files == ["included_files_value"]


def test_get_build_trigger_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_build_trigger(
            project_id="project_id_value", trigger_id="trigger_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].trigger_id == "trigger_id_value"


def test_get_build_trigger_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_build_trigger(
            cloudbuild.GetBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


@pytest.mark.asyncio
async def test_get_build_trigger_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_build_trigger(
            project_id="project_id_value", trigger_id="trigger_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].trigger_id == "trigger_id_value"


@pytest.mark.asyncio
async def test_get_build_trigger_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_build_trigger(
            cloudbuild.GetBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


def test_list_build_triggers(transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.ListBuildTriggersRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_build_triggers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildTriggersResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_build_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBuildTriggersPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_build_triggers_async(transport: str = "grpc_asyncio"):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.ListBuildTriggersRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_build_triggers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListBuildTriggersResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_build_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBuildTriggersAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_build_triggers_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_build_triggers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildTriggersResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_build_triggers(project_id="project_id_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"


def test_list_build_triggers_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_build_triggers(
            cloudbuild.ListBuildTriggersRequest(), project_id="project_id_value",
        )


@pytest.mark.asyncio
async def test_list_build_triggers_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_build_triggers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildTriggersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListBuildTriggersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_build_triggers(project_id="project_id_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"


@pytest.mark.asyncio
async def test_list_build_triggers_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_build_triggers(
            cloudbuild.ListBuildTriggersRequest(), project_id="project_id_value",
        )


def test_list_build_triggers_pager():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_build_triggers), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildTriggersResponse(triggers=[], next_page_token="def",),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[cloudbuild.BuildTrigger(),], next_page_token="ghi",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[cloudbuild.BuildTrigger(), cloudbuild.BuildTrigger(),],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_build_triggers(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, cloudbuild.BuildTrigger) for i in results)


def test_list_build_triggers_pages():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_build_triggers), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildTriggersResponse(triggers=[], next_page_token="def",),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[cloudbuild.BuildTrigger(),], next_page_token="ghi",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[cloudbuild.BuildTrigger(), cloudbuild.BuildTrigger(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_build_triggers(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_build_triggers_async_pager():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_build_triggers),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildTriggersResponse(triggers=[], next_page_token="def",),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[cloudbuild.BuildTrigger(),], next_page_token="ghi",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[cloudbuild.BuildTrigger(), cloudbuild.BuildTrigger(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_build_triggers(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloudbuild.BuildTrigger) for i in responses)


@pytest.mark.asyncio
async def test_list_build_triggers_async_pages():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_build_triggers),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildTriggersResponse(triggers=[], next_page_token="def",),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[cloudbuild.BuildTrigger(),], next_page_token="ghi",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[cloudbuild.BuildTrigger(), cloudbuild.BuildTrigger(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.list_build_triggers(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_delete_build_trigger(transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.DeleteBuildTriggerRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_build_trigger_async(transport: str = "grpc_asyncio"):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.DeleteBuildTriggerRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_build_trigger_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_build_trigger(
            project_id="project_id_value", trigger_id="trigger_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].trigger_id == "trigger_id_value"


def test_delete_build_trigger_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_build_trigger(
            cloudbuild.DeleteBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


@pytest.mark.asyncio
async def test_delete_build_trigger_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_build_trigger(
            project_id="project_id_value", trigger_id="trigger_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].trigger_id == "trigger_id_value"


@pytest.mark.asyncio
async def test_delete_build_trigger_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_build_trigger(
            cloudbuild.DeleteBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


def test_update_build_trigger(transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.UpdateBuildTriggerRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger(
            id="id_value",
            description="description_value",
            name="name_value",
            tags=["tags_value"],
            disabled=True,
            ignored_files=["ignored_files_value"],
            included_files=["included_files_value"],
            build=cloudbuild.Build(id="id_value"),
        )

        response = client.update_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)

    assert response.id == "id_value"

    assert response.description == "description_value"

    assert response.name == "name_value"

    assert response.tags == ["tags_value"]

    assert response.disabled is True

    assert response.ignored_files == ["ignored_files_value"]

    assert response.included_files == ["included_files_value"]


@pytest.mark.asyncio
async def test_update_build_trigger_async(transport: str = "grpc_asyncio"):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.UpdateBuildTriggerRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger(
                id="id_value",
                description="description_value",
                name="name_value",
                tags=["tags_value"],
                disabled=True,
                ignored_files=["ignored_files_value"],
                included_files=["included_files_value"],
            )
        )

        response = await client.update_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)

    assert response.id == "id_value"

    assert response.description == "description_value"

    assert response.name == "name_value"

    assert response.tags == ["tags_value"]

    assert response.disabled is True

    assert response.ignored_files == ["ignored_files_value"]

    assert response.included_files == ["included_files_value"]


def test_update_build_trigger_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            trigger=cloudbuild.BuildTrigger(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].trigger_id == "trigger_id_value"

        assert args[0].trigger == cloudbuild.BuildTrigger(id="id_value")


def test_update_build_trigger_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_build_trigger(
            cloudbuild.UpdateBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            trigger=cloudbuild.BuildTrigger(id="id_value"),
        )


@pytest.mark.asyncio
async def test_update_build_trigger_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            trigger=cloudbuild.BuildTrigger(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].trigger_id == "trigger_id_value"

        assert args[0].trigger == cloudbuild.BuildTrigger(id="id_value")


@pytest.mark.asyncio
async def test_update_build_trigger_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_build_trigger(
            cloudbuild.UpdateBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            trigger=cloudbuild.BuildTrigger(id="id_value"),
        )


def test_run_build_trigger(transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.RunBuildTriggerRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.run_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.run_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_run_build_trigger_async(transport: str = "grpc_asyncio"):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.RunBuildTriggerRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.run_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.run_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_run_build_trigger_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.run_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.run_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            source=cloudbuild.RepoSource(project_id="project_id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].trigger_id == "trigger_id_value"

        assert args[0].source == cloudbuild.RepoSource(project_id="project_id_value")


def test_run_build_trigger_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.run_build_trigger(
            cloudbuild.RunBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            source=cloudbuild.RepoSource(project_id="project_id_value"),
        )


@pytest.mark.asyncio
async def test_run_build_trigger_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.run_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.run_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            source=cloudbuild.RepoSource(project_id="project_id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].trigger_id == "trigger_id_value"

        assert args[0].source == cloudbuild.RepoSource(project_id="project_id_value")


@pytest.mark.asyncio
async def test_run_build_trigger_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.run_build_trigger(
            cloudbuild.RunBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            source=cloudbuild.RepoSource(project_id="project_id_value"),
        )


def test_create_worker_pool(transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.CreateWorkerPoolRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.WorkerPool(
            name="name_value",
            project_id="project_id_value",
            service_account_email="service_account_email_value",
            worker_count=1314,
            regions=[cloudbuild.WorkerPool.Region.US_CENTRAL1],
            status=cloudbuild.WorkerPool.Status.CREATING,
        )

        response = client.create_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.WorkerPool)

    assert response.name == "name_value"

    assert response.project_id == "project_id_value"

    assert response.service_account_email == "service_account_email_value"

    assert response.worker_count == 1314

    assert response.regions == [cloudbuild.WorkerPool.Region.US_CENTRAL1]

    assert response.status == cloudbuild.WorkerPool.Status.CREATING


@pytest.mark.asyncio
async def test_create_worker_pool_async(transport: str = "grpc_asyncio"):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.CreateWorkerPoolRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.WorkerPool(
                name="name_value",
                project_id="project_id_value",
                service_account_email="service_account_email_value",
                worker_count=1314,
                regions=[cloudbuild.WorkerPool.Region.US_CENTRAL1],
                status=cloudbuild.WorkerPool.Status.CREATING,
            )
        )

        response = await client.create_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.WorkerPool)

    assert response.name == "name_value"

    assert response.project_id == "project_id_value"

    assert response.service_account_email == "service_account_email_value"

    assert response.worker_count == 1314

    assert response.regions == [cloudbuild.WorkerPool.Region.US_CENTRAL1]

    assert response.status == cloudbuild.WorkerPool.Status.CREATING


def test_get_worker_pool(transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.GetWorkerPoolRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_worker_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.WorkerPool(
            name="name_value",
            project_id="project_id_value",
            service_account_email="service_account_email_value",
            worker_count=1314,
            regions=[cloudbuild.WorkerPool.Region.US_CENTRAL1],
            status=cloudbuild.WorkerPool.Status.CREATING,
        )

        response = client.get_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.WorkerPool)

    assert response.name == "name_value"

    assert response.project_id == "project_id_value"

    assert response.service_account_email == "service_account_email_value"

    assert response.worker_count == 1314

    assert response.regions == [cloudbuild.WorkerPool.Region.US_CENTRAL1]

    assert response.status == cloudbuild.WorkerPool.Status.CREATING


@pytest.mark.asyncio
async def test_get_worker_pool_async(transport: str = "grpc_asyncio"):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.GetWorkerPoolRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.WorkerPool(
                name="name_value",
                project_id="project_id_value",
                service_account_email="service_account_email_value",
                worker_count=1314,
                regions=[cloudbuild.WorkerPool.Region.US_CENTRAL1],
                status=cloudbuild.WorkerPool.Status.CREATING,
            )
        )

        response = await client.get_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.WorkerPool)

    assert response.name == "name_value"

    assert response.project_id == "project_id_value"

    assert response.service_account_email == "service_account_email_value"

    assert response.worker_count == 1314

    assert response.regions == [cloudbuild.WorkerPool.Region.US_CENTRAL1]

    assert response.status == cloudbuild.WorkerPool.Status.CREATING


def test_delete_worker_pool(transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.DeleteWorkerPoolRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_worker_pool_async(transport: str = "grpc_asyncio"):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.DeleteWorkerPoolRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_update_worker_pool(transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.UpdateWorkerPoolRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.WorkerPool(
            name="name_value",
            project_id="project_id_value",
            service_account_email="service_account_email_value",
            worker_count=1314,
            regions=[cloudbuild.WorkerPool.Region.US_CENTRAL1],
            status=cloudbuild.WorkerPool.Status.CREATING,
        )

        response = client.update_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.WorkerPool)

    assert response.name == "name_value"

    assert response.project_id == "project_id_value"

    assert response.service_account_email == "service_account_email_value"

    assert response.worker_count == 1314

    assert response.regions == [cloudbuild.WorkerPool.Region.US_CENTRAL1]

    assert response.status == cloudbuild.WorkerPool.Status.CREATING


@pytest.mark.asyncio
async def test_update_worker_pool_async(transport: str = "grpc_asyncio"):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.UpdateWorkerPoolRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.WorkerPool(
                name="name_value",
                project_id="project_id_value",
                service_account_email="service_account_email_value",
                worker_count=1314,
                regions=[cloudbuild.WorkerPool.Region.US_CENTRAL1],
                status=cloudbuild.WorkerPool.Status.CREATING,
            )
        )

        response = await client.update_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.WorkerPool)

    assert response.name == "name_value"

    assert response.project_id == "project_id_value"

    assert response.service_account_email == "service_account_email_value"

    assert response.worker_count == 1314

    assert response.regions == [cloudbuild.WorkerPool.Region.US_CENTRAL1]

    assert response.status == cloudbuild.WorkerPool.Status.CREATING


def test_list_worker_pools(transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.ListWorkerPoolsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_worker_pools), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListWorkerPoolsResponse()

        response = client.list_worker_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.ListWorkerPoolsResponse)


@pytest.mark.asyncio
async def test_list_worker_pools_async(transport: str = "grpc_asyncio"):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloudbuild.ListWorkerPoolsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_worker_pools), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListWorkerPoolsResponse()
        )

        response = await client.list_worker_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.ListWorkerPoolsResponse)


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudBuildClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudBuildClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudBuildClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = CloudBuildClient(transport=transport)
    assert client._transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.CloudBuildGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client._transport, transports.CloudBuildGrpcTransport,)


def test_cloud_build_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.CloudBuildTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_cloud_build_base_transport():
    # Instantiate the base transport.
    transport = transports.CloudBuildTransport(
        credentials=credentials.AnonymousCredentials(),
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_build",
        "get_build",
        "list_builds",
        "cancel_build",
        "retry_build",
        "create_build_trigger",
        "get_build_trigger",
        "list_build_triggers",
        "delete_build_trigger",
        "update_build_trigger",
        "run_build_trigger",
        "create_worker_pool",
        "get_worker_pool",
        "delete_worker_pool",
        "update_worker_pool",
        "list_worker_pools",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


def test_cloud_build_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(auth, "load_credentials_from_file") as load_creds:
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.CloudBuildTransport(credentials_file="credentials.json",)
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
        )


def test_cloud_build_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        CloudBuildClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",)
        )


def test_cloud_build_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.CloudBuildGrpcTransport(host="squid.clam.whelk")
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",)
        )


def test_cloud_build_host_no_port():
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudbuild.googleapis.com"
        ),
    )
    assert client._transport._host == "cloudbuild.googleapis.com:443"


def test_cloud_build_host_with_port():
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudbuild.googleapis.com:8000"
        ),
    )
    assert client._transport._host == "cloudbuild.googleapis.com:8000"


def test_cloud_build_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.CloudBuildGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


def test_cloud_build_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.CloudBuildGrpcAsyncIOTransport(
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
def test_cloud_build_grpc_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.CloudBuildGrpcTransport(
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
    )
    assert transport.grpc_channel == mock_grpc_channel


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers_async.create_channel", autospec=True)
def test_cloud_build_grpc_asyncio_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.CloudBuildGrpcAsyncIOTransport(
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
    )
    assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_cloud_build_grpc_transport_channel_mtls_with_adc(
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
        transport = transports.CloudBuildGrpcTransport(
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
        )
        assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers_async.create_channel", autospec=True)
def test_cloud_build_grpc_asyncio_transport_channel_mtls_with_adc(
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
        transport = transports.CloudBuildGrpcAsyncIOTransport(
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
        )
        assert transport.grpc_channel == mock_grpc_channel


def test_cloud_build_grpc_lro_client():
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )
    transport = client._transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_cloud_build_grpc_lro_async_client():
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    transport = client._client._transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsAsyncClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client
