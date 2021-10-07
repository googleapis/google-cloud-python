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
from typing import Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import grpc_helpers  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.api_core import gapic_v1  # type: ignore
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.cloud.network_security_v1beta1.types import authorization_policy
from google.cloud.network_security_v1beta1.types import (
    authorization_policy as gcn_authorization_policy,
)
from google.cloud.network_security_v1beta1.types import client_tls_policy
from google.cloud.network_security_v1beta1.types import (
    client_tls_policy as gcn_client_tls_policy,
)
from google.cloud.network_security_v1beta1.types import server_tls_policy
from google.cloud.network_security_v1beta1.types import (
    server_tls_policy as gcn_server_tls_policy,
)
from google.longrunning import operations_pb2  # type: ignore
from .base import NetworkSecurityTransport, DEFAULT_CLIENT_INFO


class NetworkSecurityGrpcTransport(NetworkSecurityTransport):
    """gRPC backend transport for NetworkSecurity.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "networksecurity.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        channel: grpc.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
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
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
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
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client = None

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

    @classmethod
    def create_channel(
        cls,
        host: str = "networksecurity.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """

        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service.
        """
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Sanity check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsClient(self.grpc_channel)

        # Return the client from cache.
        return self._operations_client

    @property
    def list_authorization_policies(
        self,
    ) -> Callable[
        [authorization_policy.ListAuthorizationPoliciesRequest],
        authorization_policy.ListAuthorizationPoliciesResponse,
    ]:
        r"""Return a callable for the list authorization policies method over gRPC.

        Lists AuthorizationPolicies in a given project and
        location.

        Returns:
            Callable[[~.ListAuthorizationPoliciesRequest],
                    ~.ListAuthorizationPoliciesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_authorization_policies" not in self._stubs:
            self._stubs["list_authorization_policies"] = self.grpc_channel.unary_unary(
                "/google.cloud.networksecurity.v1beta1.NetworkSecurity/ListAuthorizationPolicies",
                request_serializer=authorization_policy.ListAuthorizationPoliciesRequest.serialize,
                response_deserializer=authorization_policy.ListAuthorizationPoliciesResponse.deserialize,
            )
        return self._stubs["list_authorization_policies"]

    @property
    def get_authorization_policy(
        self,
    ) -> Callable[
        [authorization_policy.GetAuthorizationPolicyRequest],
        authorization_policy.AuthorizationPolicy,
    ]:
        r"""Return a callable for the get authorization policy method over gRPC.

        Gets details of a single AuthorizationPolicy.

        Returns:
            Callable[[~.GetAuthorizationPolicyRequest],
                    ~.AuthorizationPolicy]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_authorization_policy" not in self._stubs:
            self._stubs["get_authorization_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.networksecurity.v1beta1.NetworkSecurity/GetAuthorizationPolicy",
                request_serializer=authorization_policy.GetAuthorizationPolicyRequest.serialize,
                response_deserializer=authorization_policy.AuthorizationPolicy.deserialize,
            )
        return self._stubs["get_authorization_policy"]

    @property
    def create_authorization_policy(
        self,
    ) -> Callable[
        [gcn_authorization_policy.CreateAuthorizationPolicyRequest],
        operations_pb2.Operation,
    ]:
        r"""Return a callable for the create authorization policy method over gRPC.

        Creates a new AuthorizationPolicy in a given project
        and location.

        Returns:
            Callable[[~.CreateAuthorizationPolicyRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_authorization_policy" not in self._stubs:
            self._stubs["create_authorization_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.networksecurity.v1beta1.NetworkSecurity/CreateAuthorizationPolicy",
                request_serializer=gcn_authorization_policy.CreateAuthorizationPolicyRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_authorization_policy"]

    @property
    def update_authorization_policy(
        self,
    ) -> Callable[
        [gcn_authorization_policy.UpdateAuthorizationPolicyRequest],
        operations_pb2.Operation,
    ]:
        r"""Return a callable for the update authorization policy method over gRPC.

        Updates the parameters of a single
        AuthorizationPolicy.

        Returns:
            Callable[[~.UpdateAuthorizationPolicyRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_authorization_policy" not in self._stubs:
            self._stubs["update_authorization_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.networksecurity.v1beta1.NetworkSecurity/UpdateAuthorizationPolicy",
                request_serializer=gcn_authorization_policy.UpdateAuthorizationPolicyRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_authorization_policy"]

    @property
    def delete_authorization_policy(
        self,
    ) -> Callable[
        [authorization_policy.DeleteAuthorizationPolicyRequest],
        operations_pb2.Operation,
    ]:
        r"""Return a callable for the delete authorization policy method over gRPC.

        Deletes a single AuthorizationPolicy.

        Returns:
            Callable[[~.DeleteAuthorizationPolicyRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_authorization_policy" not in self._stubs:
            self._stubs["delete_authorization_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.networksecurity.v1beta1.NetworkSecurity/DeleteAuthorizationPolicy",
                request_serializer=authorization_policy.DeleteAuthorizationPolicyRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_authorization_policy"]

    @property
    def list_server_tls_policies(
        self,
    ) -> Callable[
        [server_tls_policy.ListServerTlsPoliciesRequest],
        server_tls_policy.ListServerTlsPoliciesResponse,
    ]:
        r"""Return a callable for the list server tls policies method over gRPC.

        Lists ServerTlsPolicies in a given project and
        location.

        Returns:
            Callable[[~.ListServerTlsPoliciesRequest],
                    ~.ListServerTlsPoliciesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_server_tls_policies" not in self._stubs:
            self._stubs["list_server_tls_policies"] = self.grpc_channel.unary_unary(
                "/google.cloud.networksecurity.v1beta1.NetworkSecurity/ListServerTlsPolicies",
                request_serializer=server_tls_policy.ListServerTlsPoliciesRequest.serialize,
                response_deserializer=server_tls_policy.ListServerTlsPoliciesResponse.deserialize,
            )
        return self._stubs["list_server_tls_policies"]

    @property
    def get_server_tls_policy(
        self,
    ) -> Callable[
        [server_tls_policy.GetServerTlsPolicyRequest], server_tls_policy.ServerTlsPolicy
    ]:
        r"""Return a callable for the get server tls policy method over gRPC.

        Gets details of a single ServerTlsPolicy.

        Returns:
            Callable[[~.GetServerTlsPolicyRequest],
                    ~.ServerTlsPolicy]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_server_tls_policy" not in self._stubs:
            self._stubs["get_server_tls_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.networksecurity.v1beta1.NetworkSecurity/GetServerTlsPolicy",
                request_serializer=server_tls_policy.GetServerTlsPolicyRequest.serialize,
                response_deserializer=server_tls_policy.ServerTlsPolicy.deserialize,
            )
        return self._stubs["get_server_tls_policy"]

    @property
    def create_server_tls_policy(
        self,
    ) -> Callable[
        [gcn_server_tls_policy.CreateServerTlsPolicyRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the create server tls policy method over gRPC.

        Creates a new ServerTlsPolicy in a given project and
        location.

        Returns:
            Callable[[~.CreateServerTlsPolicyRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_server_tls_policy" not in self._stubs:
            self._stubs["create_server_tls_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.networksecurity.v1beta1.NetworkSecurity/CreateServerTlsPolicy",
                request_serializer=gcn_server_tls_policy.CreateServerTlsPolicyRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_server_tls_policy"]

    @property
    def update_server_tls_policy(
        self,
    ) -> Callable[
        [gcn_server_tls_policy.UpdateServerTlsPolicyRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the update server tls policy method over gRPC.

        Updates the parameters of a single ServerTlsPolicy.

        Returns:
            Callable[[~.UpdateServerTlsPolicyRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_server_tls_policy" not in self._stubs:
            self._stubs["update_server_tls_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.networksecurity.v1beta1.NetworkSecurity/UpdateServerTlsPolicy",
                request_serializer=gcn_server_tls_policy.UpdateServerTlsPolicyRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_server_tls_policy"]

    @property
    def delete_server_tls_policy(
        self,
    ) -> Callable[
        [server_tls_policy.DeleteServerTlsPolicyRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the delete server tls policy method over gRPC.

        Deletes a single ServerTlsPolicy.

        Returns:
            Callable[[~.DeleteServerTlsPolicyRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_server_tls_policy" not in self._stubs:
            self._stubs["delete_server_tls_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.networksecurity.v1beta1.NetworkSecurity/DeleteServerTlsPolicy",
                request_serializer=server_tls_policy.DeleteServerTlsPolicyRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_server_tls_policy"]

    @property
    def list_client_tls_policies(
        self,
    ) -> Callable[
        [client_tls_policy.ListClientTlsPoliciesRequest],
        client_tls_policy.ListClientTlsPoliciesResponse,
    ]:
        r"""Return a callable for the list client tls policies method over gRPC.

        Lists ClientTlsPolicies in a given project and
        location.

        Returns:
            Callable[[~.ListClientTlsPoliciesRequest],
                    ~.ListClientTlsPoliciesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_client_tls_policies" not in self._stubs:
            self._stubs["list_client_tls_policies"] = self.grpc_channel.unary_unary(
                "/google.cloud.networksecurity.v1beta1.NetworkSecurity/ListClientTlsPolicies",
                request_serializer=client_tls_policy.ListClientTlsPoliciesRequest.serialize,
                response_deserializer=client_tls_policy.ListClientTlsPoliciesResponse.deserialize,
            )
        return self._stubs["list_client_tls_policies"]

    @property
    def get_client_tls_policy(
        self,
    ) -> Callable[
        [client_tls_policy.GetClientTlsPolicyRequest], client_tls_policy.ClientTlsPolicy
    ]:
        r"""Return a callable for the get client tls policy method over gRPC.

        Gets details of a single ClientTlsPolicy.

        Returns:
            Callable[[~.GetClientTlsPolicyRequest],
                    ~.ClientTlsPolicy]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_client_tls_policy" not in self._stubs:
            self._stubs["get_client_tls_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.networksecurity.v1beta1.NetworkSecurity/GetClientTlsPolicy",
                request_serializer=client_tls_policy.GetClientTlsPolicyRequest.serialize,
                response_deserializer=client_tls_policy.ClientTlsPolicy.deserialize,
            )
        return self._stubs["get_client_tls_policy"]

    @property
    def create_client_tls_policy(
        self,
    ) -> Callable[
        [gcn_client_tls_policy.CreateClientTlsPolicyRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the create client tls policy method over gRPC.

        Creates a new ClientTlsPolicy in a given project and
        location.

        Returns:
            Callable[[~.CreateClientTlsPolicyRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_client_tls_policy" not in self._stubs:
            self._stubs["create_client_tls_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.networksecurity.v1beta1.NetworkSecurity/CreateClientTlsPolicy",
                request_serializer=gcn_client_tls_policy.CreateClientTlsPolicyRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_client_tls_policy"]

    @property
    def update_client_tls_policy(
        self,
    ) -> Callable[
        [gcn_client_tls_policy.UpdateClientTlsPolicyRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the update client tls policy method over gRPC.

        Updates the parameters of a single ClientTlsPolicy.

        Returns:
            Callable[[~.UpdateClientTlsPolicyRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_client_tls_policy" not in self._stubs:
            self._stubs["update_client_tls_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.networksecurity.v1beta1.NetworkSecurity/UpdateClientTlsPolicy",
                request_serializer=gcn_client_tls_policy.UpdateClientTlsPolicyRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_client_tls_policy"]

    @property
    def delete_client_tls_policy(
        self,
    ) -> Callable[
        [client_tls_policy.DeleteClientTlsPolicyRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the delete client tls policy method over gRPC.

        Deletes a single ClientTlsPolicy.

        Returns:
            Callable[[~.DeleteClientTlsPolicyRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_client_tls_policy" not in self._stubs:
            self._stubs["delete_client_tls_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.networksecurity.v1beta1.NetworkSecurity/DeleteClientTlsPolicy",
                request_serializer=client_tls_policy.DeleteClientTlsPolicyRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_client_tls_policy"]

    def close(self):
        self.grpc_channel.close()


__all__ = ("NetworkSecurityGrpcTransport",)
