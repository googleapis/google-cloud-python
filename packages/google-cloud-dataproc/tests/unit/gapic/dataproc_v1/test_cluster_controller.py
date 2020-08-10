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
from google.cloud.dataproc_v1.services.cluster_controller import (
    ClusterControllerAsyncClient,
)
from google.cloud.dataproc_v1.services.cluster_controller import ClusterControllerClient
from google.cloud.dataproc_v1.services.cluster_controller import pagers
from google.cloud.dataproc_v1.services.cluster_controller import transports
from google.cloud.dataproc_v1.types import clusters
from google.cloud.dataproc_v1.types import clusters as gcd_clusters
from google.cloud.dataproc_v1.types import operations
from google.cloud.dataproc_v1.types import shared
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
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

    assert ClusterControllerClient._get_default_mtls_endpoint(None) is None
    assert (
        ClusterControllerClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ClusterControllerClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ClusterControllerClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ClusterControllerClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ClusterControllerClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [ClusterControllerClient, ClusterControllerAsyncClient]
)
def test_cluster_controller_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "dataproc.googleapis.com:443"


def test_cluster_controller_client_get_transport_class():
    transport = ClusterControllerClient.get_transport_class()
    assert transport == transports.ClusterControllerGrpcTransport

    transport = ClusterControllerClient.get_transport_class("grpc")
    assert transport == transports.ClusterControllerGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ClusterControllerClient, transports.ClusterControllerGrpcTransport, "grpc"),
        (
            ClusterControllerAsyncClient,
            transports.ClusterControllerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    ClusterControllerClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ClusterControllerClient),
)
@mock.patch.object(
    ClusterControllerAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ClusterControllerAsyncClient),
)
def test_cluster_controller_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(ClusterControllerClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(ClusterControllerClient, "get_transport_class") as gtc:
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
        (ClusterControllerClient, transports.ClusterControllerGrpcTransport, "grpc"),
        (
            ClusterControllerAsyncClient,
            transports.ClusterControllerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_cluster_controller_client_client_options_scopes(
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
        (ClusterControllerClient, transports.ClusterControllerGrpcTransport, "grpc"),
        (
            ClusterControllerAsyncClient,
            transports.ClusterControllerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_cluster_controller_client_client_options_credentials_file(
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


def test_cluster_controller_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.dataproc_v1.services.cluster_controller.transports.ClusterControllerGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ClusterControllerClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
            quota_project_id=None,
        )


def test_create_cluster(
    transport: str = "grpc", request_type=clusters.CreateClusterRequest
):
    client = ClusterControllerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.create_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == clusters.CreateClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_cluster_from_dict():
    test_create_cluster(request_type=dict)


@pytest.mark.asyncio
async def test_create_cluster_async(transport: str = "grpc_asyncio"):
    client = ClusterControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = clusters.CreateClusterRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.create_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_cluster_flattened():
    client = ClusterControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_cluster(
            project_id="project_id_value",
            region="region_value",
            cluster=clusters.Cluster(project_id="project_id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].cluster == clusters.Cluster(project_id="project_id_value")


def test_create_cluster_flattened_error():
    client = ClusterControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_cluster(
            clusters.CreateClusterRequest(),
            project_id="project_id_value",
            region="region_value",
            cluster=clusters.Cluster(project_id="project_id_value"),
        )


@pytest.mark.asyncio
async def test_create_cluster_flattened_async():
    client = ClusterControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_cluster(
            project_id="project_id_value",
            region="region_value",
            cluster=clusters.Cluster(project_id="project_id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].cluster == clusters.Cluster(project_id="project_id_value")


@pytest.mark.asyncio
async def test_create_cluster_flattened_error_async():
    client = ClusterControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_cluster(
            clusters.CreateClusterRequest(),
            project_id="project_id_value",
            region="region_value",
            cluster=clusters.Cluster(project_id="project_id_value"),
        )


def test_update_cluster(
    transport: str = "grpc", request_type=clusters.UpdateClusterRequest
):
    client = ClusterControllerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.update_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == clusters.UpdateClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_cluster_from_dict():
    test_update_cluster(request_type=dict)


@pytest.mark.asyncio
async def test_update_cluster_async(transport: str = "grpc_asyncio"):
    client = ClusterControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = clusters.UpdateClusterRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.update_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_cluster_flattened():
    client = ClusterControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_cluster(
            project_id="project_id_value",
            region="region_value",
            cluster_name="cluster_name_value",
            cluster=clusters.Cluster(project_id="project_id_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].cluster_name == "cluster_name_value"

        assert args[0].cluster == clusters.Cluster(project_id="project_id_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_cluster_flattened_error():
    client = ClusterControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_cluster(
            clusters.UpdateClusterRequest(),
            project_id="project_id_value",
            region="region_value",
            cluster_name="cluster_name_value",
            cluster=clusters.Cluster(project_id="project_id_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_cluster_flattened_async():
    client = ClusterControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_cluster(
            project_id="project_id_value",
            region="region_value",
            cluster_name="cluster_name_value",
            cluster=clusters.Cluster(project_id="project_id_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].cluster_name == "cluster_name_value"

        assert args[0].cluster == clusters.Cluster(project_id="project_id_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_cluster_flattened_error_async():
    client = ClusterControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_cluster(
            clusters.UpdateClusterRequest(),
            project_id="project_id_value",
            region="region_value",
            cluster_name="cluster_name_value",
            cluster=clusters.Cluster(project_id="project_id_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_delete_cluster(
    transport: str = "grpc", request_type=clusters.DeleteClusterRequest
):
    client = ClusterControllerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.delete_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == clusters.DeleteClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_cluster_from_dict():
    test_delete_cluster(request_type=dict)


@pytest.mark.asyncio
async def test_delete_cluster_async(transport: str = "grpc_asyncio"):
    client = ClusterControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = clusters.DeleteClusterRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.delete_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_cluster_flattened():
    client = ClusterControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_cluster(
            project_id="project_id_value",
            region="region_value",
            cluster_name="cluster_name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].cluster_name == "cluster_name_value"


def test_delete_cluster_flattened_error():
    client = ClusterControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_cluster(
            clusters.DeleteClusterRequest(),
            project_id="project_id_value",
            region="region_value",
            cluster_name="cluster_name_value",
        )


@pytest.mark.asyncio
async def test_delete_cluster_flattened_async():
    client = ClusterControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_cluster(
            project_id="project_id_value",
            region="region_value",
            cluster_name="cluster_name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].cluster_name == "cluster_name_value"


@pytest.mark.asyncio
async def test_delete_cluster_flattened_error_async():
    client = ClusterControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_cluster(
            clusters.DeleteClusterRequest(),
            project_id="project_id_value",
            region="region_value",
            cluster_name="cluster_name_value",
        )


def test_get_cluster(transport: str = "grpc", request_type=clusters.GetClusterRequest):
    client = ClusterControllerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = clusters.Cluster(
            project_id="project_id_value",
            cluster_name="cluster_name_value",
            cluster_uuid="cluster_uuid_value",
        )

        response = client.get_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == clusters.GetClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, clusters.Cluster)

    assert response.project_id == "project_id_value"

    assert response.cluster_name == "cluster_name_value"

    assert response.cluster_uuid == "cluster_uuid_value"


def test_get_cluster_from_dict():
    test_get_cluster(request_type=dict)


@pytest.mark.asyncio
async def test_get_cluster_async(transport: str = "grpc_asyncio"):
    client = ClusterControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = clusters.GetClusterRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clusters.Cluster(
                project_id="project_id_value",
                cluster_name="cluster_name_value",
                cluster_uuid="cluster_uuid_value",
            )
        )

        response = await client.get_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, clusters.Cluster)

    assert response.project_id == "project_id_value"

    assert response.cluster_name == "cluster_name_value"

    assert response.cluster_uuid == "cluster_uuid_value"


def test_get_cluster_flattened():
    client = ClusterControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = clusters.Cluster()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_cluster(
            project_id="project_id_value",
            region="region_value",
            cluster_name="cluster_name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].cluster_name == "cluster_name_value"


def test_get_cluster_flattened_error():
    client = ClusterControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_cluster(
            clusters.GetClusterRequest(),
            project_id="project_id_value",
            region="region_value",
            cluster_name="cluster_name_value",
        )


@pytest.mark.asyncio
async def test_get_cluster_flattened_async():
    client = ClusterControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clusters.Cluster()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(clusters.Cluster())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_cluster(
            project_id="project_id_value",
            region="region_value",
            cluster_name="cluster_name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].cluster_name == "cluster_name_value"


@pytest.mark.asyncio
async def test_get_cluster_flattened_error_async():
    client = ClusterControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_cluster(
            clusters.GetClusterRequest(),
            project_id="project_id_value",
            region="region_value",
            cluster_name="cluster_name_value",
        )


def test_list_clusters(
    transport: str = "grpc", request_type=clusters.ListClustersRequest
):
    client = ClusterControllerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_clusters), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = clusters.ListClustersResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == clusters.ListClustersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListClustersPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_clusters_from_dict():
    test_list_clusters(request_type=dict)


@pytest.mark.asyncio
async def test_list_clusters_async(transport: str = "grpc_asyncio"):
    client = ClusterControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = clusters.ListClustersRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_clusters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clusters.ListClustersResponse(next_page_token="next_page_token_value",)
        )

        response = await client.list_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListClustersAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_clusters_flattened():
    client = ClusterControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_clusters), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = clusters.ListClustersResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_clusters(
            project_id="project_id_value", region="region_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].filter == "filter_value"


def test_list_clusters_flattened_error():
    client = ClusterControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_clusters(
            clusters.ListClustersRequest(),
            project_id="project_id_value",
            region="region_value",
            filter="filter_value",
        )


@pytest.mark.asyncio
async def test_list_clusters_flattened_async():
    client = ClusterControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_clusters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clusters.ListClustersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clusters.ListClustersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_clusters(
            project_id="project_id_value", region="region_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].filter == "filter_value"


@pytest.mark.asyncio
async def test_list_clusters_flattened_error_async():
    client = ClusterControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_clusters(
            clusters.ListClustersRequest(),
            project_id="project_id_value",
            region="region_value",
            filter="filter_value",
        )


def test_list_clusters_pager():
    client = ClusterControllerClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_clusters), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clusters.ListClustersResponse(
                clusters=[clusters.Cluster(), clusters.Cluster(), clusters.Cluster(),],
                next_page_token="abc",
            ),
            clusters.ListClustersResponse(clusters=[], next_page_token="def",),
            clusters.ListClustersResponse(
                clusters=[clusters.Cluster(),], next_page_token="ghi",
            ),
            clusters.ListClustersResponse(
                clusters=[clusters.Cluster(), clusters.Cluster(),],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_clusters(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, clusters.Cluster) for i in results)


def test_list_clusters_pages():
    client = ClusterControllerClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_clusters), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clusters.ListClustersResponse(
                clusters=[clusters.Cluster(), clusters.Cluster(), clusters.Cluster(),],
                next_page_token="abc",
            ),
            clusters.ListClustersResponse(clusters=[], next_page_token="def",),
            clusters.ListClustersResponse(
                clusters=[clusters.Cluster(),], next_page_token="ghi",
            ),
            clusters.ListClustersResponse(
                clusters=[clusters.Cluster(), clusters.Cluster(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_clusters(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_clusters_async_pager():
    client = ClusterControllerAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_clusters),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clusters.ListClustersResponse(
                clusters=[clusters.Cluster(), clusters.Cluster(), clusters.Cluster(),],
                next_page_token="abc",
            ),
            clusters.ListClustersResponse(clusters=[], next_page_token="def",),
            clusters.ListClustersResponse(
                clusters=[clusters.Cluster(),], next_page_token="ghi",
            ),
            clusters.ListClustersResponse(
                clusters=[clusters.Cluster(), clusters.Cluster(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_clusters(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, clusters.Cluster) for i in responses)


@pytest.mark.asyncio
async def test_list_clusters_async_pages():
    client = ClusterControllerAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_clusters),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clusters.ListClustersResponse(
                clusters=[clusters.Cluster(), clusters.Cluster(), clusters.Cluster(),],
                next_page_token="abc",
            ),
            clusters.ListClustersResponse(clusters=[], next_page_token="def",),
            clusters.ListClustersResponse(
                clusters=[clusters.Cluster(),], next_page_token="ghi",
            ),
            clusters.ListClustersResponse(
                clusters=[clusters.Cluster(), clusters.Cluster(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.list_clusters(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_diagnose_cluster(
    transport: str = "grpc", request_type=clusters.DiagnoseClusterRequest
):
    client = ClusterControllerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.diagnose_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.diagnose_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == clusters.DiagnoseClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_diagnose_cluster_from_dict():
    test_diagnose_cluster(request_type=dict)


@pytest.mark.asyncio
async def test_diagnose_cluster_async(transport: str = "grpc_asyncio"):
    client = ClusterControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = clusters.DiagnoseClusterRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.diagnose_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.diagnose_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_diagnose_cluster_flattened():
    client = ClusterControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.diagnose_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.diagnose_cluster(
            project_id="project_id_value",
            region="region_value",
            cluster_name="cluster_name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].cluster_name == "cluster_name_value"


def test_diagnose_cluster_flattened_error():
    client = ClusterControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.diagnose_cluster(
            clusters.DiagnoseClusterRequest(),
            project_id="project_id_value",
            region="region_value",
            cluster_name="cluster_name_value",
        )


@pytest.mark.asyncio
async def test_diagnose_cluster_flattened_async():
    client = ClusterControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.diagnose_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.diagnose_cluster(
            project_id="project_id_value",
            region="region_value",
            cluster_name="cluster_name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].cluster_name == "cluster_name_value"


@pytest.mark.asyncio
async def test_diagnose_cluster_flattened_error_async():
    client = ClusterControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.diagnose_cluster(
            clusters.DiagnoseClusterRequest(),
            project_id="project_id_value",
            region="region_value",
            cluster_name="cluster_name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ClusterControllerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ClusterControllerClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.ClusterControllerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ClusterControllerClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.ClusterControllerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ClusterControllerClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ClusterControllerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = ClusterControllerClient(transport=transport)
    assert client._transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ClusterControllerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.ClusterControllerGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = ClusterControllerClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client._transport, transports.ClusterControllerGrpcTransport,)


def test_cluster_controller_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.ClusterControllerTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_cluster_controller_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.dataproc_v1.services.cluster_controller.transports.ClusterControllerTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.ClusterControllerTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_cluster",
        "update_cluster",
        "delete_cluster",
        "get_cluster",
        "list_clusters",
        "diagnose_cluster",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


def test_cluster_controller_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.dataproc_v1.services.cluster_controller.transports.ClusterControllerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.ClusterControllerTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_cluster_controller_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        ClusterControllerClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


def test_cluster_controller_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.ClusterControllerGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_cluster_controller_host_no_port():
    client = ClusterControllerClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dataproc.googleapis.com"
        ),
    )
    assert client._transport._host == "dataproc.googleapis.com:443"


def test_cluster_controller_host_with_port():
    client = ClusterControllerClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dataproc.googleapis.com:8000"
        ),
    )
    assert client._transport._host == "dataproc.googleapis.com:8000"


def test_cluster_controller_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.ClusterControllerGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


def test_cluster_controller_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.ClusterControllerGrpcAsyncIOTransport(
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
def test_cluster_controller_grpc_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.ClusterControllerGrpcTransport(
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
def test_cluster_controller_grpc_asyncio_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.ClusterControllerGrpcAsyncIOTransport(
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
def test_cluster_controller_grpc_transport_channel_mtls_with_adc(
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
        transport = transports.ClusterControllerGrpcTransport(
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
def test_cluster_controller_grpc_asyncio_transport_channel_mtls_with_adc(
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
        transport = transports.ClusterControllerGrpcAsyncIOTransport(
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


def test_cluster_controller_grpc_lro_client():
    client = ClusterControllerClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )
    transport = client._transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_cluster_controller_grpc_lro_async_client():
    client = ClusterControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    transport = client._client._transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsAsyncClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client
