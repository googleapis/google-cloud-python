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
from google.cloud.container_v1.services.cluster_manager import ClusterManagerAsyncClient
from google.cloud.container_v1.services.cluster_manager import ClusterManagerClient
from google.cloud.container_v1.services.cluster_manager import pagers
from google.cloud.container_v1.services.cluster_manager import transports
from google.cloud.container_v1.types import cluster_service
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

    assert ClusterManagerClient._get_default_mtls_endpoint(None) is None
    assert (
        ClusterManagerClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ClusterManagerClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ClusterManagerClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ClusterManagerClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ClusterManagerClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [ClusterManagerClient, ClusterManagerAsyncClient]
)
def test_cluster_manager_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds

        assert client.transport._host == "container.googleapis.com:443"


def test_cluster_manager_client_get_transport_class():
    transport = ClusterManagerClient.get_transport_class()
    assert transport == transports.ClusterManagerGrpcTransport

    transport = ClusterManagerClient.get_transport_class("grpc")
    assert transport == transports.ClusterManagerGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ClusterManagerClient, transports.ClusterManagerGrpcTransport, "grpc"),
        (
            ClusterManagerAsyncClient,
            transports.ClusterManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    ClusterManagerClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ClusterManagerClient),
)
@mock.patch.object(
    ClusterManagerAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ClusterManagerAsyncClient),
)
def test_cluster_manager_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(ClusterManagerClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(ClusterManagerClient, "get_transport_class") as gtc:
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
        (ClusterManagerClient, transports.ClusterManagerGrpcTransport, "grpc", "true"),
        (
            ClusterManagerAsyncClient,
            transports.ClusterManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (ClusterManagerClient, transports.ClusterManagerGrpcTransport, "grpc", "false"),
        (
            ClusterManagerAsyncClient,
            transports.ClusterManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    ClusterManagerClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ClusterManagerClient),
)
@mock.patch.object(
    ClusterManagerAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ClusterManagerAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_cluster_manager_client_mtls_env_auto(
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
        (ClusterManagerClient, transports.ClusterManagerGrpcTransport, "grpc"),
        (
            ClusterManagerAsyncClient,
            transports.ClusterManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_cluster_manager_client_client_options_scopes(
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
        (ClusterManagerClient, transports.ClusterManagerGrpcTransport, "grpc"),
        (
            ClusterManagerAsyncClient,
            transports.ClusterManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_cluster_manager_client_client_options_credentials_file(
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


def test_cluster_manager_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.container_v1.services.cluster_manager.transports.ClusterManagerGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ClusterManagerClient(
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


def test_list_clusters(
    transport: str = "grpc", request_type=cluster_service.ListClustersRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListClustersResponse(
            missing_zones=["missing_zones_value"],
        )

        response = client.list_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.ListClustersRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.ListClustersResponse)

    assert response.missing_zones == ["missing_zones_value"]


def test_list_clusters_from_dict():
    test_list_clusters(request_type=dict)


@pytest.mark.asyncio
async def test_list_clusters_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.ListClustersRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListClustersResponse(missing_zones=["missing_zones_value"],)
        )

        response = await client.list_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.ListClustersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.ListClustersResponse)

    assert response.missing_zones == ["missing_zones_value"]


@pytest.mark.asyncio
async def test_list_clusters_async_from_dict():
    await test_list_clusters_async(request_type=dict)


def test_list_clusters_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListClustersRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        call.return_value = cluster_service.ListClustersResponse()

        client.list_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_clusters_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListClustersRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListClustersResponse()
        )

        await client.list_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_clusters_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListClustersResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_clusters(
            project_id="project_id_value", zone="zone_value", parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].parent == "parent_value"


def test_list_clusters_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_clusters(
            cluster_service.ListClustersRequest(),
            project_id="project_id_value",
            zone="zone_value",
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_clusters_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListClustersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListClustersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_clusters(
            project_id="project_id_value", zone="zone_value", parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_clusters_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_clusters(
            cluster_service.ListClustersRequest(),
            project_id="project_id_value",
            zone="zone_value",
            parent="parent_value",
        )


def test_get_cluster(
    transport: str = "grpc", request_type=cluster_service.GetClusterRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Cluster(
            name="name_value",
            description="description_value",
            initial_node_count=1911,
            logging_service="logging_service_value",
            monitoring_service="monitoring_service_value",
            network="network_value",
            cluster_ipv4_cidr="cluster_ipv4_cidr_value",
            subnetwork="subnetwork_value",
            locations=["locations_value"],
            enable_kubernetes_alpha=True,
            label_fingerprint="label_fingerprint_value",
            self_link="self_link_value",
            zone="zone_value",
            endpoint="endpoint_value",
            initial_cluster_version="initial_cluster_version_value",
            current_master_version="current_master_version_value",
            current_node_version="current_node_version_value",
            create_time="create_time_value",
            status=cluster_service.Cluster.Status.PROVISIONING,
            status_message="status_message_value",
            node_ipv4_cidr_size=1955,
            services_ipv4_cidr="services_ipv4_cidr_value",
            instance_group_urls=["instance_group_urls_value"],
            current_node_count=1936,
            expire_time="expire_time_value",
            location="location_value",
            enable_tpu=True,
            tpu_ipv4_cidr_block="tpu_ipv4_cidr_block_value",
        )

        response = client.get_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.GetClusterRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Cluster)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.initial_node_count == 1911

    assert response.logging_service == "logging_service_value"

    assert response.monitoring_service == "monitoring_service_value"

    assert response.network == "network_value"

    assert response.cluster_ipv4_cidr == "cluster_ipv4_cidr_value"

    assert response.subnetwork == "subnetwork_value"

    assert response.locations == ["locations_value"]

    assert response.enable_kubernetes_alpha is True

    assert response.label_fingerprint == "label_fingerprint_value"

    assert response.self_link == "self_link_value"

    assert response.zone == "zone_value"

    assert response.endpoint == "endpoint_value"

    assert response.initial_cluster_version == "initial_cluster_version_value"

    assert response.current_master_version == "current_master_version_value"

    assert response.current_node_version == "current_node_version_value"

    assert response.create_time == "create_time_value"

    assert response.status == cluster_service.Cluster.Status.PROVISIONING

    assert response.status_message == "status_message_value"

    assert response.node_ipv4_cidr_size == 1955

    assert response.services_ipv4_cidr == "services_ipv4_cidr_value"

    assert response.instance_group_urls == ["instance_group_urls_value"]

    assert response.current_node_count == 1936

    assert response.expire_time == "expire_time_value"

    assert response.location == "location_value"

    assert response.enable_tpu is True

    assert response.tpu_ipv4_cidr_block == "tpu_ipv4_cidr_block_value"


def test_get_cluster_from_dict():
    test_get_cluster(request_type=dict)


@pytest.mark.asyncio
async def test_get_cluster_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.GetClusterRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Cluster(
                name="name_value",
                description="description_value",
                initial_node_count=1911,
                logging_service="logging_service_value",
                monitoring_service="monitoring_service_value",
                network="network_value",
                cluster_ipv4_cidr="cluster_ipv4_cidr_value",
                subnetwork="subnetwork_value",
                locations=["locations_value"],
                enable_kubernetes_alpha=True,
                label_fingerprint="label_fingerprint_value",
                self_link="self_link_value",
                zone="zone_value",
                endpoint="endpoint_value",
                initial_cluster_version="initial_cluster_version_value",
                current_master_version="current_master_version_value",
                current_node_version="current_node_version_value",
                create_time="create_time_value",
                status=cluster_service.Cluster.Status.PROVISIONING,
                status_message="status_message_value",
                node_ipv4_cidr_size=1955,
                services_ipv4_cidr="services_ipv4_cidr_value",
                instance_group_urls=["instance_group_urls_value"],
                current_node_count=1936,
                expire_time="expire_time_value",
                location="location_value",
                enable_tpu=True,
                tpu_ipv4_cidr_block="tpu_ipv4_cidr_block_value",
            )
        )

        response = await client.get_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.GetClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Cluster)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.initial_node_count == 1911

    assert response.logging_service == "logging_service_value"

    assert response.monitoring_service == "monitoring_service_value"

    assert response.network == "network_value"

    assert response.cluster_ipv4_cidr == "cluster_ipv4_cidr_value"

    assert response.subnetwork == "subnetwork_value"

    assert response.locations == ["locations_value"]

    assert response.enable_kubernetes_alpha is True

    assert response.label_fingerprint == "label_fingerprint_value"

    assert response.self_link == "self_link_value"

    assert response.zone == "zone_value"

    assert response.endpoint == "endpoint_value"

    assert response.initial_cluster_version == "initial_cluster_version_value"

    assert response.current_master_version == "current_master_version_value"

    assert response.current_node_version == "current_node_version_value"

    assert response.create_time == "create_time_value"

    assert response.status == cluster_service.Cluster.Status.PROVISIONING

    assert response.status_message == "status_message_value"

    assert response.node_ipv4_cidr_size == 1955

    assert response.services_ipv4_cidr == "services_ipv4_cidr_value"

    assert response.instance_group_urls == ["instance_group_urls_value"]

    assert response.current_node_count == 1936

    assert response.expire_time == "expire_time_value"

    assert response.location == "location_value"

    assert response.enable_tpu is True

    assert response.tpu_ipv4_cidr_block == "tpu_ipv4_cidr_block_value"


@pytest.mark.asyncio
async def test_get_cluster_async_from_dict():
    await test_get_cluster_async(request_type=dict)


def test_get_cluster_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetClusterRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        call.return_value = cluster_service.Cluster()

        client.get_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_cluster_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetClusterRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Cluster()
        )

        await client.get_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_cluster_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Cluster()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_cluster(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].name == "name_value"


def test_get_cluster_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_cluster(
            cluster_service.GetClusterRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_cluster_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Cluster()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Cluster()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_cluster(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_cluster_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_cluster(
            cluster_service.GetClusterRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )


def test_create_cluster(
    transport: str = "grpc", request_type=cluster_service.CreateClusterRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.create_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.CreateClusterRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_create_cluster_from_dict():
    test_create_cluster(request_type=dict)


@pytest.mark.asyncio
async def test_create_cluster_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.CreateClusterRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.create_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.CreateClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_create_cluster_async_from_dict():
    await test_create_cluster_async(request_type=dict)


def test_create_cluster_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.CreateClusterRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        call.return_value = cluster_service.Operation()

        client.create_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_cluster_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.CreateClusterRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.create_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_cluster_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_cluster(
            project_id="project_id_value",
            zone="zone_value",
            cluster=cluster_service.Cluster(name="name_value"),
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster == cluster_service.Cluster(name="name_value")

        assert args[0].parent == "parent_value"


def test_create_cluster_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_cluster(
            cluster_service.CreateClusterRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster=cluster_service.Cluster(name="name_value"),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_create_cluster_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_cluster(
            project_id="project_id_value",
            zone="zone_value",
            cluster=cluster_service.Cluster(name="name_value"),
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster == cluster_service.Cluster(name="name_value")

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_create_cluster_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_cluster(
            cluster_service.CreateClusterRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster=cluster_service.Cluster(name="name_value"),
            parent="parent_value",
        )


def test_update_cluster(
    transport: str = "grpc", request_type=cluster_service.UpdateClusterRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.update_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.UpdateClusterRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_update_cluster_from_dict():
    test_update_cluster(request_type=dict)


@pytest.mark.asyncio
async def test_update_cluster_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.UpdateClusterRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.update_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.UpdateClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_update_cluster_async_from_dict():
    await test_update_cluster_async(request_type=dict)


def test_update_cluster_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.UpdateClusterRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        call.return_value = cluster_service.Operation()

        client.update_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_cluster_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.UpdateClusterRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.update_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_update_cluster_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_cluster(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            update=cluster_service.ClusterUpdate(
                desired_node_version="desired_node_version_value"
            ),
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].update == cluster_service.ClusterUpdate(
            desired_node_version="desired_node_version_value"
        )

        assert args[0].name == "name_value"


def test_update_cluster_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_cluster(
            cluster_service.UpdateClusterRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            update=cluster_service.ClusterUpdate(
                desired_node_version="desired_node_version_value"
            ),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_update_cluster_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_cluster(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            update=cluster_service.ClusterUpdate(
                desired_node_version="desired_node_version_value"
            ),
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].update == cluster_service.ClusterUpdate(
            desired_node_version="desired_node_version_value"
        )

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_update_cluster_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_cluster(
            cluster_service.UpdateClusterRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            update=cluster_service.ClusterUpdate(
                desired_node_version="desired_node_version_value"
            ),
            name="name_value",
        )


def test_update_node_pool(
    transport: str = "grpc", request_type=cluster_service.UpdateNodePoolRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.update_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.UpdateNodePoolRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_update_node_pool_from_dict():
    test_update_node_pool(request_type=dict)


@pytest.mark.asyncio
async def test_update_node_pool_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.UpdateNodePoolRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.update_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.UpdateNodePoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_update_node_pool_async_from_dict():
    await test_update_node_pool_async(request_type=dict)


def test_update_node_pool_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.UpdateNodePoolRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_node_pool), "__call__") as call:
        call.return_value = cluster_service.Operation()

        client.update_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_node_pool_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.UpdateNodePoolRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_node_pool), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.update_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_set_node_pool_autoscaling(
    transport: str = "grpc", request_type=cluster_service.SetNodePoolAutoscalingRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_autoscaling), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.set_node_pool_autoscaling(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetNodePoolAutoscalingRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_set_node_pool_autoscaling_from_dict():
    test_set_node_pool_autoscaling(request_type=dict)


@pytest.mark.asyncio
async def test_set_node_pool_autoscaling_async(
    transport: str = "grpc_asyncio",
    request_type=cluster_service.SetNodePoolAutoscalingRequest,
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_autoscaling), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.set_node_pool_autoscaling(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetNodePoolAutoscalingRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_node_pool_autoscaling_async_from_dict():
    await test_set_node_pool_autoscaling_async(request_type=dict)


def test_set_node_pool_autoscaling_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetNodePoolAutoscalingRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_autoscaling), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()

        client.set_node_pool_autoscaling(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_node_pool_autoscaling_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetNodePoolAutoscalingRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_autoscaling), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.set_node_pool_autoscaling(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_set_logging_service(
    transport: str = "grpc", request_type=cluster_service.SetLoggingServiceRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_logging_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.set_logging_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetLoggingServiceRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_set_logging_service_from_dict():
    test_set_logging_service(request_type=dict)


@pytest.mark.asyncio
async def test_set_logging_service_async(
    transport: str = "grpc_asyncio",
    request_type=cluster_service.SetLoggingServiceRequest,
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_logging_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.set_logging_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetLoggingServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_logging_service_async_from_dict():
    await test_set_logging_service_async(request_type=dict)


def test_set_logging_service_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetLoggingServiceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_logging_service), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()

        client.set_logging_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_logging_service_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetLoggingServiceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_logging_service), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.set_logging_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_set_logging_service_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_logging_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_logging_service(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            logging_service="logging_service_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].logging_service == "logging_service_value"

        assert args[0].name == "name_value"


def test_set_logging_service_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_logging_service(
            cluster_service.SetLoggingServiceRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            logging_service="logging_service_value",
            name="name_value",
        )


@pytest.mark.asyncio
async def test_set_logging_service_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_logging_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_logging_service(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            logging_service="logging_service_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].logging_service == "logging_service_value"

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_set_logging_service_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_logging_service(
            cluster_service.SetLoggingServiceRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            logging_service="logging_service_value",
            name="name_value",
        )


def test_set_monitoring_service(
    transport: str = "grpc", request_type=cluster_service.SetMonitoringServiceRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_monitoring_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.set_monitoring_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetMonitoringServiceRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_set_monitoring_service_from_dict():
    test_set_monitoring_service(request_type=dict)


@pytest.mark.asyncio
async def test_set_monitoring_service_async(
    transport: str = "grpc_asyncio",
    request_type=cluster_service.SetMonitoringServiceRequest,
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_monitoring_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.set_monitoring_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetMonitoringServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_monitoring_service_async_from_dict():
    await test_set_monitoring_service_async(request_type=dict)


def test_set_monitoring_service_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetMonitoringServiceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_monitoring_service), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()

        client.set_monitoring_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_monitoring_service_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetMonitoringServiceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_monitoring_service), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.set_monitoring_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_set_monitoring_service_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_monitoring_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_monitoring_service(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            monitoring_service="monitoring_service_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].monitoring_service == "monitoring_service_value"

        assert args[0].name == "name_value"


def test_set_monitoring_service_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_monitoring_service(
            cluster_service.SetMonitoringServiceRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            monitoring_service="monitoring_service_value",
            name="name_value",
        )


@pytest.mark.asyncio
async def test_set_monitoring_service_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_monitoring_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_monitoring_service(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            monitoring_service="monitoring_service_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].monitoring_service == "monitoring_service_value"

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_set_monitoring_service_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_monitoring_service(
            cluster_service.SetMonitoringServiceRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            monitoring_service="monitoring_service_value",
            name="name_value",
        )


def test_set_addons_config(
    transport: str = "grpc", request_type=cluster_service.SetAddonsConfigRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_addons_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.set_addons_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetAddonsConfigRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_set_addons_config_from_dict():
    test_set_addons_config(request_type=dict)


@pytest.mark.asyncio
async def test_set_addons_config_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.SetAddonsConfigRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_addons_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.set_addons_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetAddonsConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_addons_config_async_from_dict():
    await test_set_addons_config_async(request_type=dict)


def test_set_addons_config_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetAddonsConfigRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_addons_config), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()

        client.set_addons_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_addons_config_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetAddonsConfigRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_addons_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.set_addons_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_set_addons_config_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_addons_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_addons_config(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            addons_config=cluster_service.AddonsConfig(
                http_load_balancing=cluster_service.HttpLoadBalancing(disabled=True)
            ),
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].addons_config == cluster_service.AddonsConfig(
            http_load_balancing=cluster_service.HttpLoadBalancing(disabled=True)
        )

        assert args[0].name == "name_value"


def test_set_addons_config_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_addons_config(
            cluster_service.SetAddonsConfigRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            addons_config=cluster_service.AddonsConfig(
                http_load_balancing=cluster_service.HttpLoadBalancing(disabled=True)
            ),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_set_addons_config_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_addons_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_addons_config(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            addons_config=cluster_service.AddonsConfig(
                http_load_balancing=cluster_service.HttpLoadBalancing(disabled=True)
            ),
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].addons_config == cluster_service.AddonsConfig(
            http_load_balancing=cluster_service.HttpLoadBalancing(disabled=True)
        )

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_set_addons_config_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_addons_config(
            cluster_service.SetAddonsConfigRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            addons_config=cluster_service.AddonsConfig(
                http_load_balancing=cluster_service.HttpLoadBalancing(disabled=True)
            ),
            name="name_value",
        )


def test_set_locations(
    transport: str = "grpc", request_type=cluster_service.SetLocationsRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.set_locations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetLocationsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_set_locations_from_dict():
    test_set_locations(request_type=dict)


@pytest.mark.asyncio
async def test_set_locations_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.SetLocationsRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.set_locations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetLocationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_locations_async_from_dict():
    await test_set_locations_async(request_type=dict)


def test_set_locations_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetLocationsRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_locations), "__call__") as call:
        call.return_value = cluster_service.Operation()

        client.set_locations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_locations_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetLocationsRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_locations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.set_locations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_set_locations_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_locations(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            locations=["locations_value"],
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].locations == ["locations_value"]

        assert args[0].name == "name_value"


def test_set_locations_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_locations(
            cluster_service.SetLocationsRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            locations=["locations_value"],
            name="name_value",
        )


@pytest.mark.asyncio
async def test_set_locations_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_locations(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            locations=["locations_value"],
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].locations == ["locations_value"]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_set_locations_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_locations(
            cluster_service.SetLocationsRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            locations=["locations_value"],
            name="name_value",
        )


def test_update_master(
    transport: str = "grpc", request_type=cluster_service.UpdateMasterRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_master), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.update_master(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.UpdateMasterRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_update_master_from_dict():
    test_update_master(request_type=dict)


@pytest.mark.asyncio
async def test_update_master_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.UpdateMasterRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_master), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.update_master(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.UpdateMasterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_update_master_async_from_dict():
    await test_update_master_async(request_type=dict)


def test_update_master_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.UpdateMasterRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_master), "__call__") as call:
        call.return_value = cluster_service.Operation()

        client.update_master(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_master_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.UpdateMasterRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_master), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.update_master(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_update_master_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_master), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_master(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            master_version="master_version_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].master_version == "master_version_value"

        assert args[0].name == "name_value"


def test_update_master_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_master(
            cluster_service.UpdateMasterRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            master_version="master_version_value",
            name="name_value",
        )


@pytest.mark.asyncio
async def test_update_master_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_master), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_master(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            master_version="master_version_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].master_version == "master_version_value"

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_update_master_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_master(
            cluster_service.UpdateMasterRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            master_version="master_version_value",
            name="name_value",
        )


def test_set_master_auth(
    transport: str = "grpc", request_type=cluster_service.SetMasterAuthRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_master_auth), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.set_master_auth(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetMasterAuthRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_set_master_auth_from_dict():
    test_set_master_auth(request_type=dict)


@pytest.mark.asyncio
async def test_set_master_auth_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.SetMasterAuthRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_master_auth), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.set_master_auth(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetMasterAuthRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_master_auth_async_from_dict():
    await test_set_master_auth_async(request_type=dict)


def test_set_master_auth_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetMasterAuthRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_master_auth), "__call__") as call:
        call.return_value = cluster_service.Operation()

        client.set_master_auth(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_master_auth_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetMasterAuthRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_master_auth), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.set_master_auth(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_cluster(
    transport: str = "grpc", request_type=cluster_service.DeleteClusterRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.delete_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.DeleteClusterRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_delete_cluster_from_dict():
    test_delete_cluster(request_type=dict)


@pytest.mark.asyncio
async def test_delete_cluster_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.DeleteClusterRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.delete_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.DeleteClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_delete_cluster_async_from_dict():
    await test_delete_cluster_async(request_type=dict)


def test_delete_cluster_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.DeleteClusterRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        call.return_value = cluster_service.Operation()

        client.delete_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_cluster_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.DeleteClusterRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.delete_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_cluster_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_cluster(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].name == "name_value"


def test_delete_cluster_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_cluster(
            cluster_service.DeleteClusterRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_cluster_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_cluster(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_cluster_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_cluster(
            cluster_service.DeleteClusterRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )


def test_list_operations(
    transport: str = "grpc", request_type=cluster_service.ListOperationsRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListOperationsResponse(
            missing_zones=["missing_zones_value"],
        )

        response = client.list_operations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.ListOperationsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.ListOperationsResponse)

    assert response.missing_zones == ["missing_zones_value"]


def test_list_operations_from_dict():
    test_list_operations(request_type=dict)


@pytest.mark.asyncio
async def test_list_operations_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.ListOperationsRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListOperationsResponse(
                missing_zones=["missing_zones_value"],
            )
        )

        response = await client.list_operations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.ListOperationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.ListOperationsResponse)

    assert response.missing_zones == ["missing_zones_value"]


@pytest.mark.asyncio
async def test_list_operations_async_from_dict():
    await test_list_operations_async(request_type=dict)


def test_list_operations_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListOperationsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = cluster_service.ListOperationsResponse()

        client.list_operations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_operations_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListOperationsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListOperationsResponse()
        )

        await client.list_operations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_operations_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListOperationsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_operations(
            project_id="project_id_value", zone="zone_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"


def test_list_operations_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_operations(
            cluster_service.ListOperationsRequest(),
            project_id="project_id_value",
            zone="zone_value",
        )


@pytest.mark.asyncio
async def test_list_operations_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListOperationsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListOperationsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_operations(
            project_id="project_id_value", zone="zone_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"


@pytest.mark.asyncio
async def test_list_operations_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_operations(
            cluster_service.ListOperationsRequest(),
            project_id="project_id_value",
            zone="zone_value",
        )


def test_get_operation(
    transport: str = "grpc", request_type=cluster_service.GetOperationRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.get_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.GetOperationRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_get_operation_from_dict():
    test_get_operation(request_type=dict)


@pytest.mark.asyncio
async def test_get_operation_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.GetOperationRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.get_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.GetOperationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_get_operation_async_from_dict():
    await test_get_operation_async(request_type=dict)


def test_get_operation_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetOperationRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = cluster_service.Operation()

        client.get_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_operation_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetOperationRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.get_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_operation_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_operation(
            project_id="project_id_value",
            zone="zone_value",
            operation_id="operation_id_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].operation_id == "operation_id_value"

        assert args[0].name == "name_value"


def test_get_operation_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_operation(
            cluster_service.GetOperationRequest(),
            project_id="project_id_value",
            zone="zone_value",
            operation_id="operation_id_value",
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_operation_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_operation(
            project_id="project_id_value",
            zone="zone_value",
            operation_id="operation_id_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].operation_id == "operation_id_value"

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_operation_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_operation(
            cluster_service.GetOperationRequest(),
            project_id="project_id_value",
            zone="zone_value",
            operation_id="operation_id_value",
            name="name_value",
        )


def test_cancel_operation(
    transport: str = "grpc", request_type=cluster_service.CancelOperationRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.cancel_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.CancelOperationRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_cancel_operation_from_dict():
    test_cancel_operation(request_type=dict)


@pytest.mark.asyncio
async def test_cancel_operation_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.CancelOperationRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.cancel_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.CancelOperationRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_cancel_operation_async_from_dict():
    await test_cancel_operation_async(request_type=dict)


def test_cancel_operation_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.CancelOperationRequest()
    request.name = "name/value"

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
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_cancel_operation_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.CancelOperationRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.cancel_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_cancel_operation_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.cancel_operation(
            project_id="project_id_value",
            zone="zone_value",
            operation_id="operation_id_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].operation_id == "operation_id_value"

        assert args[0].name == "name_value"


def test_cancel_operation_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.cancel_operation(
            cluster_service.CancelOperationRequest(),
            project_id="project_id_value",
            zone="zone_value",
            operation_id="operation_id_value",
            name="name_value",
        )


@pytest.mark.asyncio
async def test_cancel_operation_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.cancel_operation(
            project_id="project_id_value",
            zone="zone_value",
            operation_id="operation_id_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].operation_id == "operation_id_value"

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_cancel_operation_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.cancel_operation(
            cluster_service.CancelOperationRequest(),
            project_id="project_id_value",
            zone="zone_value",
            operation_id="operation_id_value",
            name="name_value",
        )


def test_get_server_config(
    transport: str = "grpc", request_type=cluster_service.GetServerConfigRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ServerConfig(
            default_cluster_version="default_cluster_version_value",
            valid_node_versions=["valid_node_versions_value"],
            default_image_type="default_image_type_value",
            valid_image_types=["valid_image_types_value"],
            valid_master_versions=["valid_master_versions_value"],
        )

        response = client.get_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.GetServerConfigRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.ServerConfig)

    assert response.default_cluster_version == "default_cluster_version_value"

    assert response.valid_node_versions == ["valid_node_versions_value"]

    assert response.default_image_type == "default_image_type_value"

    assert response.valid_image_types == ["valid_image_types_value"]

    assert response.valid_master_versions == ["valid_master_versions_value"]


def test_get_server_config_from_dict():
    test_get_server_config(request_type=dict)


@pytest.mark.asyncio
async def test_get_server_config_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.GetServerConfigRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ServerConfig(
                default_cluster_version="default_cluster_version_value",
                valid_node_versions=["valid_node_versions_value"],
                default_image_type="default_image_type_value",
                valid_image_types=["valid_image_types_value"],
                valid_master_versions=["valid_master_versions_value"],
            )
        )

        response = await client.get_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.GetServerConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.ServerConfig)

    assert response.default_cluster_version == "default_cluster_version_value"

    assert response.valid_node_versions == ["valid_node_versions_value"]

    assert response.default_image_type == "default_image_type_value"

    assert response.valid_image_types == ["valid_image_types_value"]

    assert response.valid_master_versions == ["valid_master_versions_value"]


@pytest.mark.asyncio
async def test_get_server_config_async_from_dict():
    await test_get_server_config_async(request_type=dict)


def test_get_server_config_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetServerConfigRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        call.return_value = cluster_service.ServerConfig()

        client.get_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_server_config_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetServerConfigRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ServerConfig()
        )

        await client.get_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_server_config_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ServerConfig()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_server_config(
            project_id="project_id_value", zone="zone_value", name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].name == "name_value"


def test_get_server_config_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_server_config(
            cluster_service.GetServerConfigRequest(),
            project_id="project_id_value",
            zone="zone_value",
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_server_config_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ServerConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ServerConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_server_config(
            project_id="project_id_value", zone="zone_value", name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_server_config_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_server_config(
            cluster_service.GetServerConfigRequest(),
            project_id="project_id_value",
            zone="zone_value",
            name="name_value",
        )


def test_get_json_web_keys(
    transport: str = "grpc", request_type=cluster_service.GetJSONWebKeysRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_json_web_keys), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.GetJSONWebKeysResponse()

        response = client.get_json_web_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.GetJSONWebKeysRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.GetJSONWebKeysResponse)


def test_get_json_web_keys_from_dict():
    test_get_json_web_keys(request_type=dict)


@pytest.mark.asyncio
async def test_get_json_web_keys_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.GetJSONWebKeysRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_json_web_keys), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.GetJSONWebKeysResponse()
        )

        response = await client.get_json_web_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.GetJSONWebKeysRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.GetJSONWebKeysResponse)


@pytest.mark.asyncio
async def test_get_json_web_keys_async_from_dict():
    await test_get_json_web_keys_async(request_type=dict)


def test_get_json_web_keys_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetJSONWebKeysRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_json_web_keys), "__call__"
    ) as call:
        call.return_value = cluster_service.GetJSONWebKeysResponse()

        client.get_json_web_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_json_web_keys_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetJSONWebKeysRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_json_web_keys), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.GetJSONWebKeysResponse()
        )

        await client.get_json_web_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_node_pools(
    transport: str = "grpc", request_type=cluster_service.ListNodePoolsRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListNodePoolsResponse()

        response = client.list_node_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.ListNodePoolsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.ListNodePoolsResponse)


def test_list_node_pools_from_dict():
    test_list_node_pools(request_type=dict)


@pytest.mark.asyncio
async def test_list_node_pools_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.ListNodePoolsRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListNodePoolsResponse()
        )

        response = await client.list_node_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.ListNodePoolsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.ListNodePoolsResponse)


@pytest.mark.asyncio
async def test_list_node_pools_async_from_dict():
    await test_list_node_pools_async(request_type=dict)


def test_list_node_pools_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListNodePoolsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        call.return_value = cluster_service.ListNodePoolsResponse()

        client.list_node_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_node_pools_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListNodePoolsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListNodePoolsResponse()
        )

        await client.list_node_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_node_pools_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListNodePoolsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_node_pools(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].parent == "parent_value"


def test_list_node_pools_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_node_pools(
            cluster_service.ListNodePoolsRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_node_pools_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListNodePoolsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListNodePoolsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_node_pools(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_node_pools_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_node_pools(
            cluster_service.ListNodePoolsRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            parent="parent_value",
        )


def test_get_node_pool(
    transport: str = "grpc", request_type=cluster_service.GetNodePoolRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.NodePool(
            name="name_value",
            initial_node_count=1911,
            locations=["locations_value"],
            self_link="self_link_value",
            version="version_value",
            instance_group_urls=["instance_group_urls_value"],
            status=cluster_service.NodePool.Status.PROVISIONING,
            status_message="status_message_value",
            pod_ipv4_cidr_size=1856,
        )

        response = client.get_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.GetNodePoolRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.NodePool)

    assert response.name == "name_value"

    assert response.initial_node_count == 1911

    assert response.locations == ["locations_value"]

    assert response.self_link == "self_link_value"

    assert response.version == "version_value"

    assert response.instance_group_urls == ["instance_group_urls_value"]

    assert response.status == cluster_service.NodePool.Status.PROVISIONING

    assert response.status_message == "status_message_value"

    assert response.pod_ipv4_cidr_size == 1856


def test_get_node_pool_from_dict():
    test_get_node_pool(request_type=dict)


@pytest.mark.asyncio
async def test_get_node_pool_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.GetNodePoolRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.NodePool(
                name="name_value",
                initial_node_count=1911,
                locations=["locations_value"],
                self_link="self_link_value",
                version="version_value",
                instance_group_urls=["instance_group_urls_value"],
                status=cluster_service.NodePool.Status.PROVISIONING,
                status_message="status_message_value",
                pod_ipv4_cidr_size=1856,
            )
        )

        response = await client.get_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.GetNodePoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.NodePool)

    assert response.name == "name_value"

    assert response.initial_node_count == 1911

    assert response.locations == ["locations_value"]

    assert response.self_link == "self_link_value"

    assert response.version == "version_value"

    assert response.instance_group_urls == ["instance_group_urls_value"]

    assert response.status == cluster_service.NodePool.Status.PROVISIONING

    assert response.status_message == "status_message_value"

    assert response.pod_ipv4_cidr_size == 1856


@pytest.mark.asyncio
async def test_get_node_pool_async_from_dict():
    await test_get_node_pool_async(request_type=dict)


def test_get_node_pool_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetNodePoolRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        call.return_value = cluster_service.NodePool()

        client.get_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_node_pool_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetNodePoolRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.NodePool()
        )

        await client.get_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_node_pool_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.NodePool()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_node_pool(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].node_pool_id == "node_pool_id_value"

        assert args[0].name == "name_value"


def test_get_node_pool_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_node_pool(
            cluster_service.GetNodePoolRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_node_pool_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.NodePool()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.NodePool()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_node_pool(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].node_pool_id == "node_pool_id_value"

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_node_pool_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_node_pool(
            cluster_service.GetNodePoolRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            name="name_value",
        )


def test_create_node_pool(
    transport: str = "grpc", request_type=cluster_service.CreateNodePoolRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.create_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.CreateNodePoolRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_create_node_pool_from_dict():
    test_create_node_pool(request_type=dict)


@pytest.mark.asyncio
async def test_create_node_pool_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.CreateNodePoolRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.create_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.CreateNodePoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_create_node_pool_async_from_dict():
    await test_create_node_pool_async(request_type=dict)


def test_create_node_pool_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.CreateNodePoolRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        call.return_value = cluster_service.Operation()

        client.create_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_node_pool_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.CreateNodePoolRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.create_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_node_pool_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_node_pool(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool=cluster_service.NodePool(name="name_value"),
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].node_pool == cluster_service.NodePool(name="name_value")

        assert args[0].parent == "parent_value"


def test_create_node_pool_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_node_pool(
            cluster_service.CreateNodePoolRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool=cluster_service.NodePool(name="name_value"),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_create_node_pool_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_node_pool(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool=cluster_service.NodePool(name="name_value"),
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].node_pool == cluster_service.NodePool(name="name_value")

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_create_node_pool_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_node_pool(
            cluster_service.CreateNodePoolRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool=cluster_service.NodePool(name="name_value"),
            parent="parent_value",
        )


def test_delete_node_pool(
    transport: str = "grpc", request_type=cluster_service.DeleteNodePoolRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.delete_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.DeleteNodePoolRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_delete_node_pool_from_dict():
    test_delete_node_pool(request_type=dict)


@pytest.mark.asyncio
async def test_delete_node_pool_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.DeleteNodePoolRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.delete_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.DeleteNodePoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_delete_node_pool_async_from_dict():
    await test_delete_node_pool_async(request_type=dict)


def test_delete_node_pool_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.DeleteNodePoolRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        call.return_value = cluster_service.Operation()

        client.delete_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_node_pool_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.DeleteNodePoolRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.delete_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_node_pool_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_node_pool(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].node_pool_id == "node_pool_id_value"

        assert args[0].name == "name_value"


def test_delete_node_pool_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_node_pool(
            cluster_service.DeleteNodePoolRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_node_pool_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_node_pool(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].node_pool_id == "node_pool_id_value"

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_node_pool_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_node_pool(
            cluster_service.DeleteNodePoolRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            name="name_value",
        )


def test_rollback_node_pool_upgrade(
    transport: str = "grpc", request_type=cluster_service.RollbackNodePoolUpgradeRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_node_pool_upgrade), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.rollback_node_pool_upgrade(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.RollbackNodePoolUpgradeRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_rollback_node_pool_upgrade_from_dict():
    test_rollback_node_pool_upgrade(request_type=dict)


@pytest.mark.asyncio
async def test_rollback_node_pool_upgrade_async(
    transport: str = "grpc_asyncio",
    request_type=cluster_service.RollbackNodePoolUpgradeRequest,
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_node_pool_upgrade), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.rollback_node_pool_upgrade(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.RollbackNodePoolUpgradeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_rollback_node_pool_upgrade_async_from_dict():
    await test_rollback_node_pool_upgrade_async(request_type=dict)


def test_rollback_node_pool_upgrade_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.RollbackNodePoolUpgradeRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_node_pool_upgrade), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()

        client.rollback_node_pool_upgrade(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_rollback_node_pool_upgrade_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.RollbackNodePoolUpgradeRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_node_pool_upgrade), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.rollback_node_pool_upgrade(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_rollback_node_pool_upgrade_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_node_pool_upgrade), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.rollback_node_pool_upgrade(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].node_pool_id == "node_pool_id_value"

        assert args[0].name == "name_value"


def test_rollback_node_pool_upgrade_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.rollback_node_pool_upgrade(
            cluster_service.RollbackNodePoolUpgradeRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            name="name_value",
        )


@pytest.mark.asyncio
async def test_rollback_node_pool_upgrade_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_node_pool_upgrade), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.rollback_node_pool_upgrade(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].node_pool_id == "node_pool_id_value"

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_rollback_node_pool_upgrade_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.rollback_node_pool_upgrade(
            cluster_service.RollbackNodePoolUpgradeRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            node_pool_id="node_pool_id_value",
            name="name_value",
        )


def test_set_node_pool_management(
    transport: str = "grpc", request_type=cluster_service.SetNodePoolManagementRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_management), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.set_node_pool_management(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetNodePoolManagementRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_set_node_pool_management_from_dict():
    test_set_node_pool_management(request_type=dict)


@pytest.mark.asyncio
async def test_set_node_pool_management_async(
    transport: str = "grpc_asyncio",
    request_type=cluster_service.SetNodePoolManagementRequest,
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_management), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.set_node_pool_management(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetNodePoolManagementRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_node_pool_management_async_from_dict():
    await test_set_node_pool_management_async(request_type=dict)


def test_set_node_pool_management_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetNodePoolManagementRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_management), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()

        client.set_node_pool_management(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_node_pool_management_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetNodePoolManagementRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_management), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.set_node_pool_management(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_set_labels(
    transport: str = "grpc", request_type=cluster_service.SetLabelsRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_labels), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.set_labels(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetLabelsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_set_labels_from_dict():
    test_set_labels(request_type=dict)


@pytest.mark.asyncio
async def test_set_labels_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.SetLabelsRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_labels), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.set_labels(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetLabelsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_labels_async_from_dict():
    await test_set_labels_async(request_type=dict)


def test_set_labels_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetLabelsRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_labels), "__call__") as call:
        call.return_value = cluster_service.Operation()

        client.set_labels(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_labels_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetLabelsRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_labels), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.set_labels(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_set_legacy_abac(
    transport: str = "grpc", request_type=cluster_service.SetLegacyAbacRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_legacy_abac), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.set_legacy_abac(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetLegacyAbacRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_set_legacy_abac_from_dict():
    test_set_legacy_abac(request_type=dict)


@pytest.mark.asyncio
async def test_set_legacy_abac_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.SetLegacyAbacRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_legacy_abac), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.set_legacy_abac(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetLegacyAbacRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_legacy_abac_async_from_dict():
    await test_set_legacy_abac_async(request_type=dict)


def test_set_legacy_abac_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetLegacyAbacRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_legacy_abac), "__call__") as call:
        call.return_value = cluster_service.Operation()

        client.set_legacy_abac(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_legacy_abac_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetLegacyAbacRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_legacy_abac), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.set_legacy_abac(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_set_legacy_abac_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_legacy_abac), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_legacy_abac(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            enabled=True,
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].enabled == True

        assert args[0].name == "name_value"


def test_set_legacy_abac_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_legacy_abac(
            cluster_service.SetLegacyAbacRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            enabled=True,
            name="name_value",
        )


@pytest.mark.asyncio
async def test_set_legacy_abac_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_legacy_abac), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_legacy_abac(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            enabled=True,
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].enabled == True

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_set_legacy_abac_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_legacy_abac(
            cluster_service.SetLegacyAbacRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            enabled=True,
            name="name_value",
        )


def test_start_ip_rotation(
    transport: str = "grpc", request_type=cluster_service.StartIPRotationRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_ip_rotation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.start_ip_rotation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.StartIPRotationRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_start_ip_rotation_from_dict():
    test_start_ip_rotation(request_type=dict)


@pytest.mark.asyncio
async def test_start_ip_rotation_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.StartIPRotationRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_ip_rotation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.start_ip_rotation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.StartIPRotationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_start_ip_rotation_async_from_dict():
    await test_start_ip_rotation_async(request_type=dict)


def test_start_ip_rotation_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.StartIPRotationRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_ip_rotation), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()

        client.start_ip_rotation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_start_ip_rotation_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.StartIPRotationRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_ip_rotation), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.start_ip_rotation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_start_ip_rotation_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_ip_rotation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.start_ip_rotation(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].name == "name_value"


def test_start_ip_rotation_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.start_ip_rotation(
            cluster_service.StartIPRotationRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )


@pytest.mark.asyncio
async def test_start_ip_rotation_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_ip_rotation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.start_ip_rotation(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_start_ip_rotation_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.start_ip_rotation(
            cluster_service.StartIPRotationRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )


def test_complete_ip_rotation(
    transport: str = "grpc", request_type=cluster_service.CompleteIPRotationRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_ip_rotation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.complete_ip_rotation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.CompleteIPRotationRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_complete_ip_rotation_from_dict():
    test_complete_ip_rotation(request_type=dict)


@pytest.mark.asyncio
async def test_complete_ip_rotation_async(
    transport: str = "grpc_asyncio",
    request_type=cluster_service.CompleteIPRotationRequest,
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_ip_rotation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.complete_ip_rotation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.CompleteIPRotationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_complete_ip_rotation_async_from_dict():
    await test_complete_ip_rotation_async(request_type=dict)


def test_complete_ip_rotation_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.CompleteIPRotationRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_ip_rotation), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()

        client.complete_ip_rotation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_complete_ip_rotation_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.CompleteIPRotationRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_ip_rotation), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.complete_ip_rotation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_complete_ip_rotation_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_ip_rotation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.complete_ip_rotation(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].name == "name_value"


def test_complete_ip_rotation_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.complete_ip_rotation(
            cluster_service.CompleteIPRotationRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )


@pytest.mark.asyncio
async def test_complete_ip_rotation_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_ip_rotation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.complete_ip_rotation(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_complete_ip_rotation_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.complete_ip_rotation(
            cluster_service.CompleteIPRotationRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            name="name_value",
        )


def test_set_node_pool_size(
    transport: str = "grpc", request_type=cluster_service.SetNodePoolSizeRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_size), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.set_node_pool_size(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetNodePoolSizeRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_set_node_pool_size_from_dict():
    test_set_node_pool_size(request_type=dict)


@pytest.mark.asyncio
async def test_set_node_pool_size_async(
    transport: str = "grpc_asyncio", request_type=cluster_service.SetNodePoolSizeRequest
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_size), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.set_node_pool_size(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetNodePoolSizeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_node_pool_size_async_from_dict():
    await test_set_node_pool_size_async(request_type=dict)


def test_set_node_pool_size_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetNodePoolSizeRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_size), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()

        client.set_node_pool_size(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_node_pool_size_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetNodePoolSizeRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_node_pool_size), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.set_node_pool_size(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_set_network_policy(
    transport: str = "grpc", request_type=cluster_service.SetNetworkPolicyRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_network_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.set_network_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetNetworkPolicyRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_set_network_policy_from_dict():
    test_set_network_policy(request_type=dict)


@pytest.mark.asyncio
async def test_set_network_policy_async(
    transport: str = "grpc_asyncio",
    request_type=cluster_service.SetNetworkPolicyRequest,
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_network_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.set_network_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetNetworkPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_network_policy_async_from_dict():
    await test_set_network_policy_async(request_type=dict)


def test_set_network_policy_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetNetworkPolicyRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_network_policy), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()

        client.set_network_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_network_policy_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetNetworkPolicyRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_network_policy), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.set_network_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_set_network_policy_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_network_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_network_policy(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            network_policy=cluster_service.NetworkPolicy(
                provider=cluster_service.NetworkPolicy.Provider.CALICO
            ),
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].network_policy == cluster_service.NetworkPolicy(
            provider=cluster_service.NetworkPolicy.Provider.CALICO
        )

        assert args[0].name == "name_value"


def test_set_network_policy_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_network_policy(
            cluster_service.SetNetworkPolicyRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            network_policy=cluster_service.NetworkPolicy(
                provider=cluster_service.NetworkPolicy.Provider.CALICO
            ),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_set_network_policy_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_network_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_network_policy(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            network_policy=cluster_service.NetworkPolicy(
                provider=cluster_service.NetworkPolicy.Provider.CALICO
            ),
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].network_policy == cluster_service.NetworkPolicy(
            provider=cluster_service.NetworkPolicy.Provider.CALICO
        )

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_set_network_policy_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_network_policy(
            cluster_service.SetNetworkPolicyRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            network_policy=cluster_service.NetworkPolicy(
                provider=cluster_service.NetworkPolicy.Provider.CALICO
            ),
            name="name_value",
        )


def test_set_maintenance_policy(
    transport: str = "grpc", request_type=cluster_service.SetMaintenancePolicyRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_maintenance_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name="name_value",
            zone="zone_value",
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail="detail_value",
            status_message="status_message_value",
            self_link="self_link_value",
            target_link="target_link_value",
            location="location_value",
            start_time="start_time_value",
            end_time="end_time_value",
        )

        response = client.set_maintenance_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetMaintenancePolicyRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


def test_set_maintenance_policy_from_dict():
    test_set_maintenance_policy(request_type=dict)


@pytest.mark.asyncio
async def test_set_maintenance_policy_async(
    transport: str = "grpc_asyncio",
    request_type=cluster_service.SetMaintenancePolicyRequest,
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_maintenance_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation(
                name="name_value",
                zone="zone_value",
                operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
                status=cluster_service.Operation.Status.PENDING,
                detail="detail_value",
                status_message="status_message_value",
                self_link="self_link_value",
                target_link="target_link_value",
                location="location_value",
                start_time="start_time_value",
                end_time="end_time_value",
            )
        )

        response = await client.set_maintenance_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.SetMaintenancePolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)

    assert response.name == "name_value"

    assert response.zone == "zone_value"

    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER

    assert response.status == cluster_service.Operation.Status.PENDING

    assert response.detail == "detail_value"

    assert response.status_message == "status_message_value"

    assert response.self_link == "self_link_value"

    assert response.target_link == "target_link_value"

    assert response.location == "location_value"

    assert response.start_time == "start_time_value"

    assert response.end_time == "end_time_value"


@pytest.mark.asyncio
async def test_set_maintenance_policy_async_from_dict():
    await test_set_maintenance_policy_async(request_type=dict)


def test_set_maintenance_policy_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetMaintenancePolicyRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_maintenance_policy), "__call__"
    ) as call:
        call.return_value = cluster_service.Operation()

        client.set_maintenance_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_maintenance_policy_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.SetMaintenancePolicyRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_maintenance_policy), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )

        await client.set_maintenance_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_set_maintenance_policy_flattened():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_maintenance_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_maintenance_policy(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            maintenance_policy=cluster_service.MaintenancePolicy(
                window=cluster_service.MaintenanceWindow(
                    daily_maintenance_window=cluster_service.DailyMaintenanceWindow(
                        start_time="start_time_value"
                    )
                )
            ),
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].maintenance_policy == cluster_service.MaintenancePolicy(
            window=cluster_service.MaintenanceWindow(
                daily_maintenance_window=cluster_service.DailyMaintenanceWindow(
                    start_time="start_time_value"
                )
            )
        )

        assert args[0].name == "name_value"


def test_set_maintenance_policy_flattened_error():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_maintenance_policy(
            cluster_service.SetMaintenancePolicyRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            maintenance_policy=cluster_service.MaintenancePolicy(
                window=cluster_service.MaintenanceWindow(
                    daily_maintenance_window=cluster_service.DailyMaintenanceWindow(
                        start_time="start_time_value"
                    )
                )
            ),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_set_maintenance_policy_flattened_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_maintenance_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.Operation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_maintenance_policy(
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            maintenance_policy=cluster_service.MaintenancePolicy(
                window=cluster_service.MaintenanceWindow(
                    daily_maintenance_window=cluster_service.DailyMaintenanceWindow(
                        start_time="start_time_value"
                    )
                )
            ),
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].zone == "zone_value"

        assert args[0].cluster_id == "cluster_id_value"

        assert args[0].maintenance_policy == cluster_service.MaintenancePolicy(
            window=cluster_service.MaintenanceWindow(
                daily_maintenance_window=cluster_service.DailyMaintenanceWindow(
                    start_time="start_time_value"
                )
            )
        )

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_set_maintenance_policy_flattened_error_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_maintenance_policy(
            cluster_service.SetMaintenancePolicyRequest(),
            project_id="project_id_value",
            zone="zone_value",
            cluster_id="cluster_id_value",
            maintenance_policy=cluster_service.MaintenancePolicy(
                window=cluster_service.MaintenanceWindow(
                    daily_maintenance_window=cluster_service.DailyMaintenanceWindow(
                        start_time="start_time_value"
                    )
                )
            ),
            name="name_value",
        )


def test_list_usable_subnetworks(
    transport: str = "grpc", request_type=cluster_service.ListUsableSubnetworksRequest
):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_usable_subnetworks), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListUsableSubnetworksResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_usable_subnetworks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.ListUsableSubnetworksRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pagers.ListUsableSubnetworksPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_usable_subnetworks_from_dict():
    test_list_usable_subnetworks(request_type=dict)


@pytest.mark.asyncio
async def test_list_usable_subnetworks_async(
    transport: str = "grpc_asyncio",
    request_type=cluster_service.ListUsableSubnetworksRequest,
):
    client = ClusterManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_usable_subnetworks), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListUsableSubnetworksResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_usable_subnetworks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cluster_service.ListUsableSubnetworksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListUsableSubnetworksAsyncPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_usable_subnetworks_async_from_dict():
    await test_list_usable_subnetworks_async(request_type=dict)


def test_list_usable_subnetworks_field_headers():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListUsableSubnetworksRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_usable_subnetworks), "__call__"
    ) as call:
        call.return_value = cluster_service.ListUsableSubnetworksResponse()

        client.list_usable_subnetworks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_usable_subnetworks_field_headers_async():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListUsableSubnetworksRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_usable_subnetworks), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cluster_service.ListUsableSubnetworksResponse()
        )

        await client.list_usable_subnetworks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_usable_subnetworks_pager():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_usable_subnetworks), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                ],
                next_page_token="abc",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[], next_page_token="def",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[cluster_service.UsableSubnetwork(),],
                next_page_token="ghi",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_usable_subnetworks(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, cluster_service.UsableSubnetwork) for i in results)


def test_list_usable_subnetworks_pages():
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_usable_subnetworks), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                ],
                next_page_token="abc",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[], next_page_token="def",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[cluster_service.UsableSubnetwork(),],
                next_page_token="ghi",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_usable_subnetworks(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_usable_subnetworks_async_pager():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_usable_subnetworks),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                ],
                next_page_token="abc",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[], next_page_token="def",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[cluster_service.UsableSubnetwork(),],
                next_page_token="ghi",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_usable_subnetworks(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cluster_service.UsableSubnetwork) for i in responses)


@pytest.mark.asyncio
async def test_list_usable_subnetworks_async_pages():
    client = ClusterManagerAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_usable_subnetworks),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                ],
                next_page_token="abc",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[], next_page_token="def",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[cluster_service.UsableSubnetwork(),],
                next_page_token="ghi",
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_usable_subnetworks(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ClusterManagerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ClusterManagerClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.ClusterManagerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ClusterManagerClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.ClusterManagerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ClusterManagerClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ClusterManagerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = ClusterManagerClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ClusterManagerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.ClusterManagerGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ClusterManagerGrpcTransport,
        transports.ClusterManagerGrpcAsyncIOTransport,
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
    client = ClusterManagerClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.ClusterManagerGrpcTransport,)


def test_cluster_manager_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.ClusterManagerTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_cluster_manager_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.container_v1.services.cluster_manager.transports.ClusterManagerTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.ClusterManagerTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_clusters",
        "get_cluster",
        "create_cluster",
        "update_cluster",
        "update_node_pool",
        "set_node_pool_autoscaling",
        "set_logging_service",
        "set_monitoring_service",
        "set_addons_config",
        "set_locations",
        "update_master",
        "set_master_auth",
        "delete_cluster",
        "list_operations",
        "get_operation",
        "cancel_operation",
        "get_server_config",
        "get_json_web_keys",
        "list_node_pools",
        "get_node_pool",
        "create_node_pool",
        "delete_node_pool",
        "rollback_node_pool_upgrade",
        "set_node_pool_management",
        "set_labels",
        "set_legacy_abac",
        "start_ip_rotation",
        "complete_ip_rotation",
        "set_node_pool_size",
        "set_network_policy",
        "set_maintenance_policy",
        "list_usable_subnetworks",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_cluster_manager_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.container_v1.services.cluster_manager.transports.ClusterManagerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.ClusterManagerTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_cluster_manager_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.container_v1.services.cluster_manager.transports.ClusterManagerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.ClusterManagerTransport()
        adc.assert_called_once()


def test_cluster_manager_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        ClusterManagerClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


def test_cluster_manager_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.ClusterManagerGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_cluster_manager_host_no_port():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="container.googleapis.com"
        ),
    )
    assert client.transport._host == "container.googleapis.com:443"


def test_cluster_manager_host_with_port():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="container.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "container.googleapis.com:8000"


def test_cluster_manager_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.ClusterManagerGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_cluster_manager_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.ClusterManagerGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ClusterManagerGrpcTransport,
        transports.ClusterManagerGrpcAsyncIOTransport,
    ],
)
def test_cluster_manager_transport_channel_mtls_with_client_cert_source(
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
                scopes=("https://www.googleapis.com/auth/cloud-platform",),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ClusterManagerGrpcTransport,
        transports.ClusterManagerGrpcAsyncIOTransport,
    ],
)
def test_cluster_manager_transport_channel_mtls_with_adc(transport_class):
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
                scopes=("https://www.googleapis.com/auth/cloud-platform",),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_common_billing_account_path():
    billing_account = "squid"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = ClusterManagerClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = ClusterManagerClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = ClusterManagerClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"

    expected = "folders/{folder}".format(folder=folder,)
    actual = ClusterManagerClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = ClusterManagerClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = ClusterManagerClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = ClusterManagerClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = ClusterManagerClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = ClusterManagerClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"

    expected = "projects/{project}".format(project=project,)
    actual = ClusterManagerClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = ClusterManagerClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = ClusterManagerClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = ClusterManagerClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = ClusterManagerClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = ClusterManagerClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.ClusterManagerTransport, "_prep_wrapped_messages"
    ) as prep:
        client = ClusterManagerClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.ClusterManagerTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = ClusterManagerClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
