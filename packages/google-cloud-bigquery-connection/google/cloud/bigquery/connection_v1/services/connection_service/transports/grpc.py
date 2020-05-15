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

from typing import Callable, Dict, Tuple

from google.api_core import grpc_helpers  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore


import grpc  # type: ignore

from google.cloud.bigquery.connection_v1.types import connection
from google.cloud.bigquery.connection_v1.types import connection as gcbc_connection
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import ConnectionServiceTransport


class ConnectionServiceGrpcTransport(ConnectionServiceTransport):
    """gRPC backend transport for ConnectionService.

    Manages external data source connections and credentials.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    def __init__(
        self,
        *,
        host: str = "bigqueryconnection.googleapis.com",
        credentials: credentials.Credentials = None,
        channel: grpc.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): The mutual TLS endpoint. If
                provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]): A
                callback to provide client SSL certificate bytes and private key
                bytes, both in PEM format. It is ignored if ``api_mtls_endpoint``
                is None.

        Raises:
          google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
        """
        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
        elif api_mtls_endpoint:
            host = (
                api_mtls_endpoint
                if ":" in api_mtls_endpoint
                else api_mtls_endpoint + ":443"
            )

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = grpc_helpers.create_channel(
                host,
                credentials=credentials,
                ssl_credentials=ssl_credentials,
                scopes=self.AUTH_SCOPES,
            )

        # Run the base constructor.
        super().__init__(host=host, credentials=credentials)
        self._stubs = {}  # type: Dict[str, Callable]

    @classmethod
    def create_channel(
        cls,
        host: str = "bigqueryconnection.googleapis.com",
        credentials: credentials.Credentials = None,
        **kwargs
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            address (Optionsl[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return grpc_helpers.create_channel(
            host, credentials=credentials, scopes=cls.AUTH_SCOPES, **kwargs
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, "_grpc_channel"):
            self._grpc_channel = self.create_channel(
                self._host, credentials=self._credentials
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def create_connection(
        self
    ) -> Callable[
        [gcbc_connection.CreateConnectionRequest], gcbc_connection.Connection
    ]:
        r"""Return a callable for the create connection method over gRPC.

        Creates a new connection.

        Returns:
            Callable[[~.CreateConnectionRequest],
                    ~.Connection]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_connection" not in self._stubs:
            self._stubs["create_connection"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.connection.v1.ConnectionService/CreateConnection",
                request_serializer=gcbc_connection.CreateConnectionRequest.serialize,
                response_deserializer=gcbc_connection.Connection.deserialize,
            )
        return self._stubs["create_connection"]

    @property
    def get_connection(
        self
    ) -> Callable[[connection.GetConnectionRequest], connection.Connection]:
        r"""Return a callable for the get connection method over gRPC.

        Returns specified connection.

        Returns:
            Callable[[~.GetConnectionRequest],
                    ~.Connection]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_connection" not in self._stubs:
            self._stubs["get_connection"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.connection.v1.ConnectionService/GetConnection",
                request_serializer=connection.GetConnectionRequest.serialize,
                response_deserializer=connection.Connection.deserialize,
            )
        return self._stubs["get_connection"]

    @property
    def list_connections(
        self
    ) -> Callable[
        [connection.ListConnectionsRequest], connection.ListConnectionsResponse
    ]:
        r"""Return a callable for the list connections method over gRPC.

        Returns a list of connections in the given project.

        Returns:
            Callable[[~.ListConnectionsRequest],
                    ~.ListConnectionsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_connections" not in self._stubs:
            self._stubs["list_connections"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.connection.v1.ConnectionService/ListConnections",
                request_serializer=connection.ListConnectionsRequest.serialize,
                response_deserializer=connection.ListConnectionsResponse.deserialize,
            )
        return self._stubs["list_connections"]

    @property
    def update_connection(
        self
    ) -> Callable[
        [gcbc_connection.UpdateConnectionRequest], gcbc_connection.Connection
    ]:
        r"""Return a callable for the update connection method over gRPC.

        Updates the specified connection. For security
        reasons, also resets credential if connection properties
        are in the update field mask.

        Returns:
            Callable[[~.UpdateConnectionRequest],
                    ~.Connection]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_connection" not in self._stubs:
            self._stubs["update_connection"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.connection.v1.ConnectionService/UpdateConnection",
                request_serializer=gcbc_connection.UpdateConnectionRequest.serialize,
                response_deserializer=gcbc_connection.Connection.deserialize,
            )
        return self._stubs["update_connection"]

    @property
    def delete_connection(
        self
    ) -> Callable[[connection.DeleteConnectionRequest], empty.Empty]:
        r"""Return a callable for the delete connection method over gRPC.

        Deletes connection and associated credential.

        Returns:
            Callable[[~.DeleteConnectionRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_connection" not in self._stubs:
            self._stubs["delete_connection"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.connection.v1.ConnectionService/DeleteConnection",
                request_serializer=connection.DeleteConnectionRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_connection"]

    @property
    def get_iam_policy(
        self
    ) -> Callable[[iam_policy.GetIamPolicyRequest], policy.Policy]:
        r"""Return a callable for the get iam policy method over gRPC.

        Gets the access control policy for a resource.
        Returns an empty policy if the resource exists and does
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
                "/google.cloud.bigquery.connection.v1.ConnectionService/GetIamPolicy",
                request_serializer=iam_policy.GetIamPolicyRequest.SerializeToString,
                response_deserializer=policy.Policy.FromString,
            )
        return self._stubs["get_iam_policy"]

    @property
    def set_iam_policy(
        self
    ) -> Callable[[iam_policy.SetIamPolicyRequest], policy.Policy]:
        r"""Return a callable for the set iam policy method over gRPC.

        Sets the access control policy on the specified resource.
        Replaces any existing policy.

        Can return Public Errors: NOT_FOUND, INVALID_ARGUMENT and
        PERMISSION_DENIED

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
                "/google.cloud.bigquery.connection.v1.ConnectionService/SetIamPolicy",
                request_serializer=iam_policy.SetIamPolicyRequest.SerializeToString,
                response_deserializer=policy.Policy.FromString,
            )
        return self._stubs["set_iam_policy"]

    @property
    def test_iam_permissions(
        self
    ) -> Callable[
        [iam_policy.TestIamPermissionsRequest], iam_policy.TestIamPermissionsResponse
    ]:
        r"""Return a callable for the test iam permissions method over gRPC.

        Returns permissions that a caller has on the specified resource.
        If the resource does not exist, this will return an empty set of
        permissions, not a NOT_FOUND error.

        Note: This operation is designed to be used for building
        permission-aware UIs and command-line tools, not for
        authorization checking. This operation may "fail open" without
        warning.

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
                "/google.cloud.bigquery.connection.v1.ConnectionService/TestIamPermissions",
                request_serializer=iam_policy.TestIamPermissionsRequest.SerializeToString,
                response_deserializer=iam_policy.TestIamPermissionsResponse.FromString,
            )
        return self._stubs["test_iam_permissions"]


__all__ = ("ConnectionServiceGrpcTransport",)
