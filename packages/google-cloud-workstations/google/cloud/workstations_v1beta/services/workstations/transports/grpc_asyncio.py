# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers_async, operations_v1
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.workstations_v1beta.types import workstations

from .base import DEFAULT_CLIENT_INFO, WorkstationsTransport
from .grpc import WorkstationsGrpcTransport


class WorkstationsGrpcAsyncIOTransport(WorkstationsTransport):
    """gRPC AsyncIO backend transport for Workstations.

    Service for interacting with Cloud Workstations.

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
        host: str = "workstations.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
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

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "workstations.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[aio.Channel] = None,
        api_mtls_endpoint: Optional[str] = None,
        client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
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
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client: Optional[operations_v1.OperationsAsyncClient] = None

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
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
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
    def operations_client(self) -> operations_v1.OperationsAsyncClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsAsyncClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def get_workstation_cluster(
        self,
    ) -> Callable[
        [workstations.GetWorkstationClusterRequest],
        Awaitable[workstations.WorkstationCluster],
    ]:
        r"""Return a callable for the get workstation cluster method over gRPC.

        Returns the requested workstation cluster.

        Returns:
            Callable[[~.GetWorkstationClusterRequest],
                    Awaitable[~.WorkstationCluster]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_workstation_cluster" not in self._stubs:
            self._stubs["get_workstation_cluster"] = self.grpc_channel.unary_unary(
                "/google.cloud.workstations.v1beta.Workstations/GetWorkstationCluster",
                request_serializer=workstations.GetWorkstationClusterRequest.serialize,
                response_deserializer=workstations.WorkstationCluster.deserialize,
            )
        return self._stubs["get_workstation_cluster"]

    @property
    def list_workstation_clusters(
        self,
    ) -> Callable[
        [workstations.ListWorkstationClustersRequest],
        Awaitable[workstations.ListWorkstationClustersResponse],
    ]:
        r"""Return a callable for the list workstation clusters method over gRPC.

        Returns all workstation clusters in the specified
        location.

        Returns:
            Callable[[~.ListWorkstationClustersRequest],
                    Awaitable[~.ListWorkstationClustersResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_workstation_clusters" not in self._stubs:
            self._stubs["list_workstation_clusters"] = self.grpc_channel.unary_unary(
                "/google.cloud.workstations.v1beta.Workstations/ListWorkstationClusters",
                request_serializer=workstations.ListWorkstationClustersRequest.serialize,
                response_deserializer=workstations.ListWorkstationClustersResponse.deserialize,
            )
        return self._stubs["list_workstation_clusters"]

    @property
    def create_workstation_cluster(
        self,
    ) -> Callable[
        [workstations.CreateWorkstationClusterRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create workstation cluster method over gRPC.

        Creates a new workstation cluster.

        Returns:
            Callable[[~.CreateWorkstationClusterRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_workstation_cluster" not in self._stubs:
            self._stubs["create_workstation_cluster"] = self.grpc_channel.unary_unary(
                "/google.cloud.workstations.v1beta.Workstations/CreateWorkstationCluster",
                request_serializer=workstations.CreateWorkstationClusterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_workstation_cluster"]

    @property
    def update_workstation_cluster(
        self,
    ) -> Callable[
        [workstations.UpdateWorkstationClusterRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update workstation cluster method over gRPC.

        Updates an existing workstation cluster.

        Returns:
            Callable[[~.UpdateWorkstationClusterRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_workstation_cluster" not in self._stubs:
            self._stubs["update_workstation_cluster"] = self.grpc_channel.unary_unary(
                "/google.cloud.workstations.v1beta.Workstations/UpdateWorkstationCluster",
                request_serializer=workstations.UpdateWorkstationClusterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_workstation_cluster"]

    @property
    def delete_workstation_cluster(
        self,
    ) -> Callable[
        [workstations.DeleteWorkstationClusterRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete workstation cluster method over gRPC.

        Deletes the specified workstation cluster.

        Returns:
            Callable[[~.DeleteWorkstationClusterRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_workstation_cluster" not in self._stubs:
            self._stubs["delete_workstation_cluster"] = self.grpc_channel.unary_unary(
                "/google.cloud.workstations.v1beta.Workstations/DeleteWorkstationCluster",
                request_serializer=workstations.DeleteWorkstationClusterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_workstation_cluster"]

    @property
    def get_workstation_config(
        self,
    ) -> Callable[
        [workstations.GetWorkstationConfigRequest],
        Awaitable[workstations.WorkstationConfig],
    ]:
        r"""Return a callable for the get workstation config method over gRPC.

        Returns the requested workstation configuration.

        Returns:
            Callable[[~.GetWorkstationConfigRequest],
                    Awaitable[~.WorkstationConfig]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_workstation_config" not in self._stubs:
            self._stubs["get_workstation_config"] = self.grpc_channel.unary_unary(
                "/google.cloud.workstations.v1beta.Workstations/GetWorkstationConfig",
                request_serializer=workstations.GetWorkstationConfigRequest.serialize,
                response_deserializer=workstations.WorkstationConfig.deserialize,
            )
        return self._stubs["get_workstation_config"]

    @property
    def list_workstation_configs(
        self,
    ) -> Callable[
        [workstations.ListWorkstationConfigsRequest],
        Awaitable[workstations.ListWorkstationConfigsResponse],
    ]:
        r"""Return a callable for the list workstation configs method over gRPC.

        Returns all workstation configurations in the
        specified cluster.

        Returns:
            Callable[[~.ListWorkstationConfigsRequest],
                    Awaitable[~.ListWorkstationConfigsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_workstation_configs" not in self._stubs:
            self._stubs["list_workstation_configs"] = self.grpc_channel.unary_unary(
                "/google.cloud.workstations.v1beta.Workstations/ListWorkstationConfigs",
                request_serializer=workstations.ListWorkstationConfigsRequest.serialize,
                response_deserializer=workstations.ListWorkstationConfigsResponse.deserialize,
            )
        return self._stubs["list_workstation_configs"]

    @property
    def list_usable_workstation_configs(
        self,
    ) -> Callable[
        [workstations.ListUsableWorkstationConfigsRequest],
        Awaitable[workstations.ListUsableWorkstationConfigsResponse],
    ]:
        r"""Return a callable for the list usable workstation
        configs method over gRPC.

        Returns all workstation configurations in the
        specified cluster on which the caller has the
        "workstations.workstation.create" permission.

        Returns:
            Callable[[~.ListUsableWorkstationConfigsRequest],
                    Awaitable[~.ListUsableWorkstationConfigsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_usable_workstation_configs" not in self._stubs:
            self._stubs[
                "list_usable_workstation_configs"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.workstations.v1beta.Workstations/ListUsableWorkstationConfigs",
                request_serializer=workstations.ListUsableWorkstationConfigsRequest.serialize,
                response_deserializer=workstations.ListUsableWorkstationConfigsResponse.deserialize,
            )
        return self._stubs["list_usable_workstation_configs"]

    @property
    def create_workstation_config(
        self,
    ) -> Callable[
        [workstations.CreateWorkstationConfigRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create workstation config method over gRPC.

        Creates a new workstation configuration.

        Returns:
            Callable[[~.CreateWorkstationConfigRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_workstation_config" not in self._stubs:
            self._stubs["create_workstation_config"] = self.grpc_channel.unary_unary(
                "/google.cloud.workstations.v1beta.Workstations/CreateWorkstationConfig",
                request_serializer=workstations.CreateWorkstationConfigRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_workstation_config"]

    @property
    def update_workstation_config(
        self,
    ) -> Callable[
        [workstations.UpdateWorkstationConfigRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update workstation config method over gRPC.

        Updates an existing workstation configuration.

        Returns:
            Callable[[~.UpdateWorkstationConfigRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_workstation_config" not in self._stubs:
            self._stubs["update_workstation_config"] = self.grpc_channel.unary_unary(
                "/google.cloud.workstations.v1beta.Workstations/UpdateWorkstationConfig",
                request_serializer=workstations.UpdateWorkstationConfigRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_workstation_config"]

    @property
    def delete_workstation_config(
        self,
    ) -> Callable[
        [workstations.DeleteWorkstationConfigRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete workstation config method over gRPC.

        Deletes the specified workstation configuration.

        Returns:
            Callable[[~.DeleteWorkstationConfigRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_workstation_config" not in self._stubs:
            self._stubs["delete_workstation_config"] = self.grpc_channel.unary_unary(
                "/google.cloud.workstations.v1beta.Workstations/DeleteWorkstationConfig",
                request_serializer=workstations.DeleteWorkstationConfigRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_workstation_config"]

    @property
    def get_workstation(
        self,
    ) -> Callable[
        [workstations.GetWorkstationRequest], Awaitable[workstations.Workstation]
    ]:
        r"""Return a callable for the get workstation method over gRPC.

        Returns the requested workstation.

        Returns:
            Callable[[~.GetWorkstationRequest],
                    Awaitable[~.Workstation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_workstation" not in self._stubs:
            self._stubs["get_workstation"] = self.grpc_channel.unary_unary(
                "/google.cloud.workstations.v1beta.Workstations/GetWorkstation",
                request_serializer=workstations.GetWorkstationRequest.serialize,
                response_deserializer=workstations.Workstation.deserialize,
            )
        return self._stubs["get_workstation"]

    @property
    def list_workstations(
        self,
    ) -> Callable[
        [workstations.ListWorkstationsRequest],
        Awaitable[workstations.ListWorkstationsResponse],
    ]:
        r"""Return a callable for the list workstations method over gRPC.

        Returns all Workstations using the specified
        workstation configuration.

        Returns:
            Callable[[~.ListWorkstationsRequest],
                    Awaitable[~.ListWorkstationsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_workstations" not in self._stubs:
            self._stubs["list_workstations"] = self.grpc_channel.unary_unary(
                "/google.cloud.workstations.v1beta.Workstations/ListWorkstations",
                request_serializer=workstations.ListWorkstationsRequest.serialize,
                response_deserializer=workstations.ListWorkstationsResponse.deserialize,
            )
        return self._stubs["list_workstations"]

    @property
    def list_usable_workstations(
        self,
    ) -> Callable[
        [workstations.ListUsableWorkstationsRequest],
        Awaitable[workstations.ListUsableWorkstationsResponse],
    ]:
        r"""Return a callable for the list usable workstations method over gRPC.

        Returns all workstations using the specified
        workstation configuration on which the caller has the
        "workstations.workstations.use" permission.

        Returns:
            Callable[[~.ListUsableWorkstationsRequest],
                    Awaitable[~.ListUsableWorkstationsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_usable_workstations" not in self._stubs:
            self._stubs["list_usable_workstations"] = self.grpc_channel.unary_unary(
                "/google.cloud.workstations.v1beta.Workstations/ListUsableWorkstations",
                request_serializer=workstations.ListUsableWorkstationsRequest.serialize,
                response_deserializer=workstations.ListUsableWorkstationsResponse.deserialize,
            )
        return self._stubs["list_usable_workstations"]

    @property
    def create_workstation(
        self,
    ) -> Callable[
        [workstations.CreateWorkstationRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create workstation method over gRPC.

        Creates a new workstation.

        Returns:
            Callable[[~.CreateWorkstationRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_workstation" not in self._stubs:
            self._stubs["create_workstation"] = self.grpc_channel.unary_unary(
                "/google.cloud.workstations.v1beta.Workstations/CreateWorkstation",
                request_serializer=workstations.CreateWorkstationRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_workstation"]

    @property
    def update_workstation(
        self,
    ) -> Callable[
        [workstations.UpdateWorkstationRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update workstation method over gRPC.

        Updates an existing workstation.

        Returns:
            Callable[[~.UpdateWorkstationRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_workstation" not in self._stubs:
            self._stubs["update_workstation"] = self.grpc_channel.unary_unary(
                "/google.cloud.workstations.v1beta.Workstations/UpdateWorkstation",
                request_serializer=workstations.UpdateWorkstationRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_workstation"]

    @property
    def delete_workstation(
        self,
    ) -> Callable[
        [workstations.DeleteWorkstationRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete workstation method over gRPC.

        Deletes the specified workstation.

        Returns:
            Callable[[~.DeleteWorkstationRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_workstation" not in self._stubs:
            self._stubs["delete_workstation"] = self.grpc_channel.unary_unary(
                "/google.cloud.workstations.v1beta.Workstations/DeleteWorkstation",
                request_serializer=workstations.DeleteWorkstationRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_workstation"]

    @property
    def start_workstation(
        self,
    ) -> Callable[
        [workstations.StartWorkstationRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the start workstation method over gRPC.

        Starts running a workstation so that users can
        connect to it.

        Returns:
            Callable[[~.StartWorkstationRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "start_workstation" not in self._stubs:
            self._stubs["start_workstation"] = self.grpc_channel.unary_unary(
                "/google.cloud.workstations.v1beta.Workstations/StartWorkstation",
                request_serializer=workstations.StartWorkstationRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["start_workstation"]

    @property
    def stop_workstation(
        self,
    ) -> Callable[
        [workstations.StopWorkstationRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the stop workstation method over gRPC.

        Stops running a workstation, reducing costs.

        Returns:
            Callable[[~.StopWorkstationRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "stop_workstation" not in self._stubs:
            self._stubs["stop_workstation"] = self.grpc_channel.unary_unary(
                "/google.cloud.workstations.v1beta.Workstations/StopWorkstation",
                request_serializer=workstations.StopWorkstationRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["stop_workstation"]

    @property
    def generate_access_token(
        self,
    ) -> Callable[
        [workstations.GenerateAccessTokenRequest],
        Awaitable[workstations.GenerateAccessTokenResponse],
    ]:
        r"""Return a callable for the generate access token method over gRPC.

        Returns a short-lived credential that can be used to
        send authenticated and authorized traffic to a
        workstation.

        Returns:
            Callable[[~.GenerateAccessTokenRequest],
                    Awaitable[~.GenerateAccessTokenResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_access_token" not in self._stubs:
            self._stubs["generate_access_token"] = self.grpc_channel.unary_unary(
                "/google.cloud.workstations.v1beta.Workstations/GenerateAccessToken",
                request_serializer=workstations.GenerateAccessTokenRequest.serialize,
                response_deserializer=workstations.GenerateAccessTokenResponse.deserialize,
            )
        return self._stubs["generate_access_token"]

    def close(self):
        return self.grpc_channel.close()

    @property
    def delete_operation(
        self,
    ) -> Callable[[operations_pb2.DeleteOperationRequest], None]:
        r"""Return a callable for the delete_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_operation" not in self._stubs:
            self._stubs["delete_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/DeleteOperation",
                request_serializer=operations_pb2.DeleteOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["delete_operation"]

    @property
    def cancel_operation(
        self,
    ) -> Callable[[operations_pb2.CancelOperationRequest], None]:
        r"""Return a callable for the cancel_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_operation" not in self._stubs:
            self._stubs["cancel_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/CancelOperation",
                request_serializer=operations_pb2.CancelOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["cancel_operation"]

    @property
    def get_operation(
        self,
    ) -> Callable[[operations_pb2.GetOperationRequest], operations_pb2.Operation]:
        r"""Return a callable for the get_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_operation" not in self._stubs:
            self._stubs["get_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/GetOperation",
                request_serializer=operations_pb2.GetOperationRequest.SerializeToString,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["get_operation"]

    @property
    def list_operations(
        self,
    ) -> Callable[
        [operations_pb2.ListOperationsRequest], operations_pb2.ListOperationsResponse
    ]:
        r"""Return a callable for the list_operations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_operations" not in self._stubs:
            self._stubs["list_operations"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/ListOperations",
                request_serializer=operations_pb2.ListOperationsRequest.SerializeToString,
                response_deserializer=operations_pb2.ListOperationsResponse.FromString,
            )
        return self._stubs["list_operations"]

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], policy_pb2.Policy]:
        r"""Return a callable for the set iam policy method over gRPC.
        Sets the IAM access control policy on the specified
        function. Replaces any existing policy.
        Returns:
            Callable[[~.SetIamPolicyRequest],
                    ~.Policy]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_iam_policy" not in self._stubs:
            self._stubs["set_iam_policy"] = self.grpc_channel.unary_unary(
                "/google.iam.v1.IAMPolicy/SetIamPolicy",
                request_serializer=iam_policy_pb2.SetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["set_iam_policy"]

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], policy_pb2.Policy]:
        r"""Return a callable for the get iam policy method over gRPC.
        Gets the IAM access control policy for a function.
        Returns an empty policy if the function exists and does
        not have a policy set.
        Returns:
            Callable[[~.GetIamPolicyRequest],
                    ~.Policy]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_iam_policy" not in self._stubs:
            self._stubs["get_iam_policy"] = self.grpc_channel.unary_unary(
                "/google.iam.v1.IAMPolicy/GetIamPolicy",
                request_serializer=iam_policy_pb2.GetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["get_iam_policy"]

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        iam_policy_pb2.TestIamPermissionsResponse,
    ]:
        r"""Return a callable for the test iam permissions method over gRPC.
        Tests the specified permissions against the IAM access control
        policy for a function. If the function does not exist, this will
        return an empty set of permissions, not a NOT_FOUND error.
        Returns:
            Callable[[~.TestIamPermissionsRequest],
                    ~.TestIamPermissionsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "test_iam_permissions" not in self._stubs:
            self._stubs["test_iam_permissions"] = self.grpc_channel.unary_unary(
                "/google.iam.v1.IAMPolicy/TestIamPermissions",
                request_serializer=iam_policy_pb2.TestIamPermissionsRequest.SerializeToString,
                response_deserializer=iam_policy_pb2.TestIamPermissionsResponse.FromString,
            )
        return self._stubs["test_iam_permissions"]


__all__ = ("WorkstationsGrpcAsyncIOTransport",)
