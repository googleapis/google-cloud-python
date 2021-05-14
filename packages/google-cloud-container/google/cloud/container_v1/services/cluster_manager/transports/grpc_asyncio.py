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
import warnings
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import gapic_v1  # type: ignore
from google.api_core import grpc_helpers_async  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
import packaging.version

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.container_v1.types import cluster_service
from google.protobuf import empty_pb2  # type: ignore
from .base import ClusterManagerTransport, DEFAULT_CLIENT_INFO
from .grpc import ClusterManagerGrpcTransport


class ClusterManagerGrpcAsyncIOTransport(ClusterManagerTransport):
    """gRPC AsyncIO backend transport for ClusterManager.

    Google Kubernetes Engine Cluster Manager v1

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "container.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """

        self_signed_jwt_kwargs = cls._get_self_signed_jwt_kwargs(host, scopes)

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            **self_signed_jwt_kwargs,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "container.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id=None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None
        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                credentials=self._credentials,
                credentials_file=credentials_file,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def list_clusters(
        self,
    ) -> Callable[
        [cluster_service.ListClustersRequest],
        Awaitable[cluster_service.ListClustersResponse],
    ]:
        r"""Return a callable for the list clusters method over gRPC.

        Lists all clusters owned by a project in either the
        specified zone or all zones.

        Returns:
            Callable[[~.ListClustersRequest],
                    Awaitable[~.ListClustersResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_clusters" not in self._stubs:
            self._stubs["list_clusters"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/ListClusters",
                request_serializer=cluster_service.ListClustersRequest.serialize,
                response_deserializer=cluster_service.ListClustersResponse.deserialize,
            )
        return self._stubs["list_clusters"]

    @property
    def get_cluster(
        self,
    ) -> Callable[
        [cluster_service.GetClusterRequest], Awaitable[cluster_service.Cluster]
    ]:
        r"""Return a callable for the get cluster method over gRPC.

        Gets the details of a specific cluster.

        Returns:
            Callable[[~.GetClusterRequest],
                    Awaitable[~.Cluster]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_cluster" not in self._stubs:
            self._stubs["get_cluster"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/GetCluster",
                request_serializer=cluster_service.GetClusterRequest.serialize,
                response_deserializer=cluster_service.Cluster.deserialize,
            )
        return self._stubs["get_cluster"]

    @property
    def create_cluster(
        self,
    ) -> Callable[
        [cluster_service.CreateClusterRequest], Awaitable[cluster_service.Operation]
    ]:
        r"""Return a callable for the create cluster method over gRPC.

        Creates a cluster, consisting of the specified number and type
        of Google Compute Engine instances.

        By default, the cluster is created in the project's `default
        network <https://cloud.google.com/compute/docs/networks-and-firewalls#networks>`__.

        One firewall is added for the cluster. After cluster creation,
        the Kubelet creates routes for each node to allow the containers
        on that node to communicate with all other instances in the
        cluster.

        Finally, an entry is added to the project's global metadata
        indicating which CIDR range the cluster is using.

        Returns:
            Callable[[~.CreateClusterRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_cluster" not in self._stubs:
            self._stubs["create_cluster"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/CreateCluster",
                request_serializer=cluster_service.CreateClusterRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["create_cluster"]

    @property
    def update_cluster(
        self,
    ) -> Callable[
        [cluster_service.UpdateClusterRequest], Awaitable[cluster_service.Operation]
    ]:
        r"""Return a callable for the update cluster method over gRPC.

        Updates the settings of a specific cluster.

        Returns:
            Callable[[~.UpdateClusterRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_cluster" not in self._stubs:
            self._stubs["update_cluster"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/UpdateCluster",
                request_serializer=cluster_service.UpdateClusterRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["update_cluster"]

    @property
    def update_node_pool(
        self,
    ) -> Callable[
        [cluster_service.UpdateNodePoolRequest], Awaitable[cluster_service.Operation]
    ]:
        r"""Return a callable for the update node pool method over gRPC.

        Updates the version and/or image type for the
        specified node pool.

        Returns:
            Callable[[~.UpdateNodePoolRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_node_pool" not in self._stubs:
            self._stubs["update_node_pool"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/UpdateNodePool",
                request_serializer=cluster_service.UpdateNodePoolRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["update_node_pool"]

    @property
    def set_node_pool_autoscaling(
        self,
    ) -> Callable[
        [cluster_service.SetNodePoolAutoscalingRequest],
        Awaitable[cluster_service.Operation],
    ]:
        r"""Return a callable for the set node pool autoscaling method over gRPC.

        Sets the autoscaling settings for the specified node
        pool.

        Returns:
            Callable[[~.SetNodePoolAutoscalingRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_node_pool_autoscaling" not in self._stubs:
            self._stubs["set_node_pool_autoscaling"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/SetNodePoolAutoscaling",
                request_serializer=cluster_service.SetNodePoolAutoscalingRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["set_node_pool_autoscaling"]

    @property
    def set_logging_service(
        self,
    ) -> Callable[
        [cluster_service.SetLoggingServiceRequest], Awaitable[cluster_service.Operation]
    ]:
        r"""Return a callable for the set logging service method over gRPC.

        Sets the logging service for a specific cluster.

        Returns:
            Callable[[~.SetLoggingServiceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_logging_service" not in self._stubs:
            self._stubs["set_logging_service"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/SetLoggingService",
                request_serializer=cluster_service.SetLoggingServiceRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["set_logging_service"]

    @property
    def set_monitoring_service(
        self,
    ) -> Callable[
        [cluster_service.SetMonitoringServiceRequest],
        Awaitable[cluster_service.Operation],
    ]:
        r"""Return a callable for the set monitoring service method over gRPC.

        Sets the monitoring service for a specific cluster.

        Returns:
            Callable[[~.SetMonitoringServiceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_monitoring_service" not in self._stubs:
            self._stubs["set_monitoring_service"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/SetMonitoringService",
                request_serializer=cluster_service.SetMonitoringServiceRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["set_monitoring_service"]

    @property
    def set_addons_config(
        self,
    ) -> Callable[
        [cluster_service.SetAddonsConfigRequest], Awaitable[cluster_service.Operation]
    ]:
        r"""Return a callable for the set addons config method over gRPC.

        Sets the addons for a specific cluster.

        Returns:
            Callable[[~.SetAddonsConfigRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_addons_config" not in self._stubs:
            self._stubs["set_addons_config"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/SetAddonsConfig",
                request_serializer=cluster_service.SetAddonsConfigRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["set_addons_config"]

    @property
    def set_locations(
        self,
    ) -> Callable[
        [cluster_service.SetLocationsRequest], Awaitable[cluster_service.Operation]
    ]:
        r"""Return a callable for the set locations method over gRPC.

        Sets the locations for a specific cluster. Deprecated. Use
        `projects.locations.clusters.update <https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters/update>`__
        instead.

        Returns:
            Callable[[~.SetLocationsRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_locations" not in self._stubs:
            self._stubs["set_locations"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/SetLocations",
                request_serializer=cluster_service.SetLocationsRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["set_locations"]

    @property
    def update_master(
        self,
    ) -> Callable[
        [cluster_service.UpdateMasterRequest], Awaitable[cluster_service.Operation]
    ]:
        r"""Return a callable for the update master method over gRPC.

        Updates the master for a specific cluster.

        Returns:
            Callable[[~.UpdateMasterRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_master" not in self._stubs:
            self._stubs["update_master"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/UpdateMaster",
                request_serializer=cluster_service.UpdateMasterRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["update_master"]

    @property
    def set_master_auth(
        self,
    ) -> Callable[
        [cluster_service.SetMasterAuthRequest], Awaitable[cluster_service.Operation]
    ]:
        r"""Return a callable for the set master auth method over gRPC.

        Sets master auth materials. Currently supports
        changing the admin password or a specific cluster,
        either via password generation or explicitly setting the
        password.

        Returns:
            Callable[[~.SetMasterAuthRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_master_auth" not in self._stubs:
            self._stubs["set_master_auth"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/SetMasterAuth",
                request_serializer=cluster_service.SetMasterAuthRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["set_master_auth"]

    @property
    def delete_cluster(
        self,
    ) -> Callable[
        [cluster_service.DeleteClusterRequest], Awaitable[cluster_service.Operation]
    ]:
        r"""Return a callable for the delete cluster method over gRPC.

        Deletes the cluster, including the Kubernetes
        endpoint and all worker nodes.

        Firewalls and routes that were configured during cluster
        creation are also deleted.

        Other Google Compute Engine resources that might be in
        use by the cluster, such as load balancer resources, are
        not deleted if they weren't present when the cluster was
        initially created.

        Returns:
            Callable[[~.DeleteClusterRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_cluster" not in self._stubs:
            self._stubs["delete_cluster"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/DeleteCluster",
                request_serializer=cluster_service.DeleteClusterRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["delete_cluster"]

    @property
    def list_operations(
        self,
    ) -> Callable[
        [cluster_service.ListOperationsRequest],
        Awaitable[cluster_service.ListOperationsResponse],
    ]:
        r"""Return a callable for the list operations method over gRPC.

        Lists all operations in a project in a specific zone
        or all zones.

        Returns:
            Callable[[~.ListOperationsRequest],
                    Awaitable[~.ListOperationsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_operations" not in self._stubs:
            self._stubs["list_operations"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/ListOperations",
                request_serializer=cluster_service.ListOperationsRequest.serialize,
                response_deserializer=cluster_service.ListOperationsResponse.deserialize,
            )
        return self._stubs["list_operations"]

    @property
    def get_operation(
        self,
    ) -> Callable[
        [cluster_service.GetOperationRequest], Awaitable[cluster_service.Operation]
    ]:
        r"""Return a callable for the get operation method over gRPC.

        Gets the specified operation.

        Returns:
            Callable[[~.GetOperationRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_operation" not in self._stubs:
            self._stubs["get_operation"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/GetOperation",
                request_serializer=cluster_service.GetOperationRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["get_operation"]

    @property
    def cancel_operation(
        self,
    ) -> Callable[[cluster_service.CancelOperationRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the cancel operation method over gRPC.

        Cancels the specified operation.

        Returns:
            Callable[[~.CancelOperationRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_operation" not in self._stubs:
            self._stubs["cancel_operation"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/CancelOperation",
                request_serializer=cluster_service.CancelOperationRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["cancel_operation"]

    @property
    def get_server_config(
        self,
    ) -> Callable[
        [cluster_service.GetServerConfigRequest],
        Awaitable[cluster_service.ServerConfig],
    ]:
        r"""Return a callable for the get server config method over gRPC.

        Returns configuration info about the Google
        Kubernetes Engine service.

        Returns:
            Callable[[~.GetServerConfigRequest],
                    Awaitable[~.ServerConfig]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_server_config" not in self._stubs:
            self._stubs["get_server_config"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/GetServerConfig",
                request_serializer=cluster_service.GetServerConfigRequest.serialize,
                response_deserializer=cluster_service.ServerConfig.deserialize,
            )
        return self._stubs["get_server_config"]

    @property
    def get_json_web_keys(
        self,
    ) -> Callable[
        [cluster_service.GetJSONWebKeysRequest],
        Awaitable[cluster_service.GetJSONWebKeysResponse],
    ]:
        r"""Return a callable for the get json web keys method over gRPC.

        Gets the public component of the cluster signing keys
        in JSON Web Key format.
        This API is not yet intended for general use, and is not
        available for all clusters.

        Returns:
            Callable[[~.GetJSONWebKeysRequest],
                    Awaitable[~.GetJSONWebKeysResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_json_web_keys" not in self._stubs:
            self._stubs["get_json_web_keys"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/GetJSONWebKeys",
                request_serializer=cluster_service.GetJSONWebKeysRequest.serialize,
                response_deserializer=cluster_service.GetJSONWebKeysResponse.deserialize,
            )
        return self._stubs["get_json_web_keys"]

    @property
    def list_node_pools(
        self,
    ) -> Callable[
        [cluster_service.ListNodePoolsRequest],
        Awaitable[cluster_service.ListNodePoolsResponse],
    ]:
        r"""Return a callable for the list node pools method over gRPC.

        Lists the node pools for a cluster.

        Returns:
            Callable[[~.ListNodePoolsRequest],
                    Awaitable[~.ListNodePoolsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_node_pools" not in self._stubs:
            self._stubs["list_node_pools"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/ListNodePools",
                request_serializer=cluster_service.ListNodePoolsRequest.serialize,
                response_deserializer=cluster_service.ListNodePoolsResponse.deserialize,
            )
        return self._stubs["list_node_pools"]

    @property
    def get_node_pool(
        self,
    ) -> Callable[
        [cluster_service.GetNodePoolRequest], Awaitable[cluster_service.NodePool]
    ]:
        r"""Return a callable for the get node pool method over gRPC.

        Retrieves the requested node pool.

        Returns:
            Callable[[~.GetNodePoolRequest],
                    Awaitable[~.NodePool]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_node_pool" not in self._stubs:
            self._stubs["get_node_pool"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/GetNodePool",
                request_serializer=cluster_service.GetNodePoolRequest.serialize,
                response_deserializer=cluster_service.NodePool.deserialize,
            )
        return self._stubs["get_node_pool"]

    @property
    def create_node_pool(
        self,
    ) -> Callable[
        [cluster_service.CreateNodePoolRequest], Awaitable[cluster_service.Operation]
    ]:
        r"""Return a callable for the create node pool method over gRPC.

        Creates a node pool for a cluster.

        Returns:
            Callable[[~.CreateNodePoolRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_node_pool" not in self._stubs:
            self._stubs["create_node_pool"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/CreateNodePool",
                request_serializer=cluster_service.CreateNodePoolRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["create_node_pool"]

    @property
    def delete_node_pool(
        self,
    ) -> Callable[
        [cluster_service.DeleteNodePoolRequest], Awaitable[cluster_service.Operation]
    ]:
        r"""Return a callable for the delete node pool method over gRPC.

        Deletes a node pool from a cluster.

        Returns:
            Callable[[~.DeleteNodePoolRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_node_pool" not in self._stubs:
            self._stubs["delete_node_pool"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/DeleteNodePool",
                request_serializer=cluster_service.DeleteNodePoolRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["delete_node_pool"]

    @property
    def rollback_node_pool_upgrade(
        self,
    ) -> Callable[
        [cluster_service.RollbackNodePoolUpgradeRequest],
        Awaitable[cluster_service.Operation],
    ]:
        r"""Return a callable for the rollback node pool upgrade method over gRPC.

        Rolls back a previously Aborted or Failed NodePool
        upgrade. This makes no changes if the last upgrade
        successfully completed.

        Returns:
            Callable[[~.RollbackNodePoolUpgradeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "rollback_node_pool_upgrade" not in self._stubs:
            self._stubs["rollback_node_pool_upgrade"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/RollbackNodePoolUpgrade",
                request_serializer=cluster_service.RollbackNodePoolUpgradeRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["rollback_node_pool_upgrade"]

    @property
    def set_node_pool_management(
        self,
    ) -> Callable[
        [cluster_service.SetNodePoolManagementRequest],
        Awaitable[cluster_service.Operation],
    ]:
        r"""Return a callable for the set node pool management method over gRPC.

        Sets the NodeManagement options for a node pool.

        Returns:
            Callable[[~.SetNodePoolManagementRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_node_pool_management" not in self._stubs:
            self._stubs["set_node_pool_management"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/SetNodePoolManagement",
                request_serializer=cluster_service.SetNodePoolManagementRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["set_node_pool_management"]

    @property
    def set_labels(
        self,
    ) -> Callable[
        [cluster_service.SetLabelsRequest], Awaitable[cluster_service.Operation]
    ]:
        r"""Return a callable for the set labels method over gRPC.

        Sets labels on a cluster.

        Returns:
            Callable[[~.SetLabelsRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_labels" not in self._stubs:
            self._stubs["set_labels"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/SetLabels",
                request_serializer=cluster_service.SetLabelsRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["set_labels"]

    @property
    def set_legacy_abac(
        self,
    ) -> Callable[
        [cluster_service.SetLegacyAbacRequest], Awaitable[cluster_service.Operation]
    ]:
        r"""Return a callable for the set legacy abac method over gRPC.

        Enables or disables the ABAC authorization mechanism
        on a cluster.

        Returns:
            Callable[[~.SetLegacyAbacRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_legacy_abac" not in self._stubs:
            self._stubs["set_legacy_abac"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/SetLegacyAbac",
                request_serializer=cluster_service.SetLegacyAbacRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["set_legacy_abac"]

    @property
    def start_ip_rotation(
        self,
    ) -> Callable[
        [cluster_service.StartIPRotationRequest], Awaitable[cluster_service.Operation]
    ]:
        r"""Return a callable for the start ip rotation method over gRPC.

        Starts master IP rotation.

        Returns:
            Callable[[~.StartIPRotationRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "start_ip_rotation" not in self._stubs:
            self._stubs["start_ip_rotation"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/StartIPRotation",
                request_serializer=cluster_service.StartIPRotationRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["start_ip_rotation"]

    @property
    def complete_ip_rotation(
        self,
    ) -> Callable[
        [cluster_service.CompleteIPRotationRequest],
        Awaitable[cluster_service.Operation],
    ]:
        r"""Return a callable for the complete ip rotation method over gRPC.

        Completes master IP rotation.

        Returns:
            Callable[[~.CompleteIPRotationRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "complete_ip_rotation" not in self._stubs:
            self._stubs["complete_ip_rotation"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/CompleteIPRotation",
                request_serializer=cluster_service.CompleteIPRotationRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["complete_ip_rotation"]

    @property
    def set_node_pool_size(
        self,
    ) -> Callable[
        [cluster_service.SetNodePoolSizeRequest], Awaitable[cluster_service.Operation]
    ]:
        r"""Return a callable for the set node pool size method over gRPC.

        Sets the size for a specific node pool.

        Returns:
            Callable[[~.SetNodePoolSizeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_node_pool_size" not in self._stubs:
            self._stubs["set_node_pool_size"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/SetNodePoolSize",
                request_serializer=cluster_service.SetNodePoolSizeRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["set_node_pool_size"]

    @property
    def set_network_policy(
        self,
    ) -> Callable[
        [cluster_service.SetNetworkPolicyRequest], Awaitable[cluster_service.Operation]
    ]:
        r"""Return a callable for the set network policy method over gRPC.

        Enables or disables Network Policy for a cluster.

        Returns:
            Callable[[~.SetNetworkPolicyRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_network_policy" not in self._stubs:
            self._stubs["set_network_policy"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/SetNetworkPolicy",
                request_serializer=cluster_service.SetNetworkPolicyRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["set_network_policy"]

    @property
    def set_maintenance_policy(
        self,
    ) -> Callable[
        [cluster_service.SetMaintenancePolicyRequest],
        Awaitable[cluster_service.Operation],
    ]:
        r"""Return a callable for the set maintenance policy method over gRPC.

        Sets the maintenance policy for a cluster.

        Returns:
            Callable[[~.SetMaintenancePolicyRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_maintenance_policy" not in self._stubs:
            self._stubs["set_maintenance_policy"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/SetMaintenancePolicy",
                request_serializer=cluster_service.SetMaintenancePolicyRequest.serialize,
                response_deserializer=cluster_service.Operation.deserialize,
            )
        return self._stubs["set_maintenance_policy"]

    @property
    def list_usable_subnetworks(
        self,
    ) -> Callable[
        [cluster_service.ListUsableSubnetworksRequest],
        Awaitable[cluster_service.ListUsableSubnetworksResponse],
    ]:
        r"""Return a callable for the list usable subnetworks method over gRPC.

        Lists subnetworks that are usable for creating
        clusters in a project.

        Returns:
            Callable[[~.ListUsableSubnetworksRequest],
                    Awaitable[~.ListUsableSubnetworksResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_usable_subnetworks" not in self._stubs:
            self._stubs["list_usable_subnetworks"] = self.grpc_channel.unary_unary(
                "/google.container.v1.ClusterManager/ListUsableSubnetworks",
                request_serializer=cluster_service.ListUsableSubnetworksRequest.serialize,
                response_deserializer=cluster_service.ListUsableSubnetworksResponse.deserialize,
            )
        return self._stubs["list_usable_subnetworks"]


__all__ = ("ClusterManagerGrpcAsyncIOTransport",)
