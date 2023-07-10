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
from google.longrunning import operations_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.tpu_v1.types import cloud_tpu

from .base import DEFAULT_CLIENT_INFO, TpuTransport
from .grpc import TpuGrpcTransport


class TpuGrpcAsyncIOTransport(TpuTransport):
    """gRPC AsyncIO backend transport for Tpu.

    Manages TPU nodes and other resources
    TPU API v1

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
        host: str = "tpu.googleapis.com",
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
        host: str = "tpu.googleapis.com",
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
    def list_nodes(
        self,
    ) -> Callable[[cloud_tpu.ListNodesRequest], Awaitable[cloud_tpu.ListNodesResponse]]:
        r"""Return a callable for the list nodes method over gRPC.

        Lists nodes.

        Returns:
            Callable[[~.ListNodesRequest],
                    Awaitable[~.ListNodesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_nodes" not in self._stubs:
            self._stubs["list_nodes"] = self.grpc_channel.unary_unary(
                "/google.cloud.tpu.v1.Tpu/ListNodes",
                request_serializer=cloud_tpu.ListNodesRequest.serialize,
                response_deserializer=cloud_tpu.ListNodesResponse.deserialize,
            )
        return self._stubs["list_nodes"]

    @property
    def get_node(
        self,
    ) -> Callable[[cloud_tpu.GetNodeRequest], Awaitable[cloud_tpu.Node]]:
        r"""Return a callable for the get node method over gRPC.

        Gets the details of a node.

        Returns:
            Callable[[~.GetNodeRequest],
                    Awaitable[~.Node]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_node" not in self._stubs:
            self._stubs["get_node"] = self.grpc_channel.unary_unary(
                "/google.cloud.tpu.v1.Tpu/GetNode",
                request_serializer=cloud_tpu.GetNodeRequest.serialize,
                response_deserializer=cloud_tpu.Node.deserialize,
            )
        return self._stubs["get_node"]

    @property
    def create_node(
        self,
    ) -> Callable[[cloud_tpu.CreateNodeRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the create node method over gRPC.

        Creates a node.

        Returns:
            Callable[[~.CreateNodeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_node" not in self._stubs:
            self._stubs["create_node"] = self.grpc_channel.unary_unary(
                "/google.cloud.tpu.v1.Tpu/CreateNode",
                request_serializer=cloud_tpu.CreateNodeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_node"]

    @property
    def delete_node(
        self,
    ) -> Callable[[cloud_tpu.DeleteNodeRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the delete node method over gRPC.

        Deletes a node.

        Returns:
            Callable[[~.DeleteNodeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_node" not in self._stubs:
            self._stubs["delete_node"] = self.grpc_channel.unary_unary(
                "/google.cloud.tpu.v1.Tpu/DeleteNode",
                request_serializer=cloud_tpu.DeleteNodeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_node"]

    @property
    def reimage_node(
        self,
    ) -> Callable[[cloud_tpu.ReimageNodeRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the reimage node method over gRPC.

        Reimages a node's OS.

        Returns:
            Callable[[~.ReimageNodeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "reimage_node" not in self._stubs:
            self._stubs["reimage_node"] = self.grpc_channel.unary_unary(
                "/google.cloud.tpu.v1.Tpu/ReimageNode",
                request_serializer=cloud_tpu.ReimageNodeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["reimage_node"]

    @property
    def stop_node(
        self,
    ) -> Callable[[cloud_tpu.StopNodeRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the stop node method over gRPC.

        Stops a node, this operation is only available with
        single TPU nodes.

        Returns:
            Callable[[~.StopNodeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "stop_node" not in self._stubs:
            self._stubs["stop_node"] = self.grpc_channel.unary_unary(
                "/google.cloud.tpu.v1.Tpu/StopNode",
                request_serializer=cloud_tpu.StopNodeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["stop_node"]

    @property
    def start_node(
        self,
    ) -> Callable[[cloud_tpu.StartNodeRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the start node method over gRPC.

        Starts a node.

        Returns:
            Callable[[~.StartNodeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "start_node" not in self._stubs:
            self._stubs["start_node"] = self.grpc_channel.unary_unary(
                "/google.cloud.tpu.v1.Tpu/StartNode",
                request_serializer=cloud_tpu.StartNodeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["start_node"]

    @property
    def list_tensor_flow_versions(
        self,
    ) -> Callable[
        [cloud_tpu.ListTensorFlowVersionsRequest],
        Awaitable[cloud_tpu.ListTensorFlowVersionsResponse],
    ]:
        r"""Return a callable for the list tensor flow versions method over gRPC.

        List TensorFlow versions supported by this API.

        Returns:
            Callable[[~.ListTensorFlowVersionsRequest],
                    Awaitable[~.ListTensorFlowVersionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_tensor_flow_versions" not in self._stubs:
            self._stubs["list_tensor_flow_versions"] = self.grpc_channel.unary_unary(
                "/google.cloud.tpu.v1.Tpu/ListTensorFlowVersions",
                request_serializer=cloud_tpu.ListTensorFlowVersionsRequest.serialize,
                response_deserializer=cloud_tpu.ListTensorFlowVersionsResponse.deserialize,
            )
        return self._stubs["list_tensor_flow_versions"]

    @property
    def get_tensor_flow_version(
        self,
    ) -> Callable[
        [cloud_tpu.GetTensorFlowVersionRequest], Awaitable[cloud_tpu.TensorFlowVersion]
    ]:
        r"""Return a callable for the get tensor flow version method over gRPC.

        Gets TensorFlow Version.

        Returns:
            Callable[[~.GetTensorFlowVersionRequest],
                    Awaitable[~.TensorFlowVersion]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_tensor_flow_version" not in self._stubs:
            self._stubs["get_tensor_flow_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.tpu.v1.Tpu/GetTensorFlowVersion",
                request_serializer=cloud_tpu.GetTensorFlowVersionRequest.serialize,
                response_deserializer=cloud_tpu.TensorFlowVersion.deserialize,
            )
        return self._stubs["get_tensor_flow_version"]

    @property
    def list_accelerator_types(
        self,
    ) -> Callable[
        [cloud_tpu.ListAcceleratorTypesRequest],
        Awaitable[cloud_tpu.ListAcceleratorTypesResponse],
    ]:
        r"""Return a callable for the list accelerator types method over gRPC.

        Lists accelerator types supported by this API.

        Returns:
            Callable[[~.ListAcceleratorTypesRequest],
                    Awaitable[~.ListAcceleratorTypesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_accelerator_types" not in self._stubs:
            self._stubs["list_accelerator_types"] = self.grpc_channel.unary_unary(
                "/google.cloud.tpu.v1.Tpu/ListAcceleratorTypes",
                request_serializer=cloud_tpu.ListAcceleratorTypesRequest.serialize,
                response_deserializer=cloud_tpu.ListAcceleratorTypesResponse.deserialize,
            )
        return self._stubs["list_accelerator_types"]

    @property
    def get_accelerator_type(
        self,
    ) -> Callable[
        [cloud_tpu.GetAcceleratorTypeRequest], Awaitable[cloud_tpu.AcceleratorType]
    ]:
        r"""Return a callable for the get accelerator type method over gRPC.

        Gets AcceleratorType.

        Returns:
            Callable[[~.GetAcceleratorTypeRequest],
                    Awaitable[~.AcceleratorType]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_accelerator_type" not in self._stubs:
            self._stubs["get_accelerator_type"] = self.grpc_channel.unary_unary(
                "/google.cloud.tpu.v1.Tpu/GetAcceleratorType",
                request_serializer=cloud_tpu.GetAcceleratorTypeRequest.serialize,
                response_deserializer=cloud_tpu.AcceleratorType.deserialize,
            )
        return self._stubs["get_accelerator_type"]

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
    def list_locations(
        self,
    ) -> Callable[
        [locations_pb2.ListLocationsRequest], locations_pb2.ListLocationsResponse
    ]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_locations" not in self._stubs:
            self._stubs["list_locations"] = self.grpc_channel.unary_unary(
                "/google.cloud.location.Locations/ListLocations",
                request_serializer=locations_pb2.ListLocationsRequest.SerializeToString,
                response_deserializer=locations_pb2.ListLocationsResponse.FromString,
            )
        return self._stubs["list_locations"]

    @property
    def get_location(
        self,
    ) -> Callable[[locations_pb2.GetLocationRequest], locations_pb2.Location]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_location" not in self._stubs:
            self._stubs["get_location"] = self.grpc_channel.unary_unary(
                "/google.cloud.location.Locations/GetLocation",
                request_serializer=locations_pb2.GetLocationRequest.SerializeToString,
                response_deserializer=locations_pb2.Location.FromString,
            )
        return self._stubs["get_location"]


__all__ = ("TpuGrpcAsyncIOTransport",)
