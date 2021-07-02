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
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
import packaging.version

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.gkehub_v1beta1.types import membership
from google.longrunning import operations_pb2  # type: ignore
from .base import GkeHubMembershipServiceTransport, DEFAULT_CLIENT_INFO
from .grpc import GkeHubMembershipServiceGrpcTransport


class GkeHubMembershipServiceGrpcAsyncIOTransport(GkeHubMembershipServiceTransport):
    """gRPC AsyncIO backend transport for GkeHubMembershipService.

    GKE Hub CRUD API for the Membership resource.
    The Membership service is currently only available in the global
    location.

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
        host: str = "gkehub.googleapis.com",
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
        host: str = "gkehub.googleapis.com",
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
        # Sanity check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsAsyncClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def list_memberships(
        self,
    ) -> Callable[
        [membership.ListMembershipsRequest],
        Awaitable[membership.ListMembershipsResponse],
    ]:
        r"""Return a callable for the list memberships method over gRPC.

        Lists Memberships in a given project and location.

        Returns:
            Callable[[~.ListMembershipsRequest],
                    Awaitable[~.ListMembershipsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_memberships" not in self._stubs:
            self._stubs["list_memberships"] = self.grpc_channel.unary_unary(
                "/google.cloud.gkehub.v1beta1.GkeHubMembershipService/ListMemberships",
                request_serializer=membership.ListMembershipsRequest.serialize,
                response_deserializer=membership.ListMembershipsResponse.deserialize,
            )
        return self._stubs["list_memberships"]

    @property
    def get_membership(
        self,
    ) -> Callable[[membership.GetMembershipRequest], Awaitable[membership.Membership]]:
        r"""Return a callable for the get membership method over gRPC.

        Gets the details of a Membership.

        Returns:
            Callable[[~.GetMembershipRequest],
                    Awaitable[~.Membership]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_membership" not in self._stubs:
            self._stubs["get_membership"] = self.grpc_channel.unary_unary(
                "/google.cloud.gkehub.v1beta1.GkeHubMembershipService/GetMembership",
                request_serializer=membership.GetMembershipRequest.serialize,
                response_deserializer=membership.Membership.deserialize,
            )
        return self._stubs["get_membership"]

    @property
    def create_membership(
        self,
    ) -> Callable[
        [membership.CreateMembershipRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create membership method over gRPC.

        Adds a new Membership.

        Returns:
            Callable[[~.CreateMembershipRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_membership" not in self._stubs:
            self._stubs["create_membership"] = self.grpc_channel.unary_unary(
                "/google.cloud.gkehub.v1beta1.GkeHubMembershipService/CreateMembership",
                request_serializer=membership.CreateMembershipRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_membership"]

    @property
    def delete_membership(
        self,
    ) -> Callable[
        [membership.DeleteMembershipRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete membership method over gRPC.

        Removes a Membership.

        Returns:
            Callable[[~.DeleteMembershipRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_membership" not in self._stubs:
            self._stubs["delete_membership"] = self.grpc_channel.unary_unary(
                "/google.cloud.gkehub.v1beta1.GkeHubMembershipService/DeleteMembership",
                request_serializer=membership.DeleteMembershipRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_membership"]

    @property
    def update_membership(
        self,
    ) -> Callable[
        [membership.UpdateMembershipRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update membership method over gRPC.

        Updates an existing Membership.

        Returns:
            Callable[[~.UpdateMembershipRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_membership" not in self._stubs:
            self._stubs["update_membership"] = self.grpc_channel.unary_unary(
                "/google.cloud.gkehub.v1beta1.GkeHubMembershipService/UpdateMembership",
                request_serializer=membership.UpdateMembershipRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_membership"]

    @property
    def generate_connect_manifest(
        self,
    ) -> Callable[
        [membership.GenerateConnectManifestRequest],
        Awaitable[membership.GenerateConnectManifestResponse],
    ]:
        r"""Return a callable for the generate connect manifest method over gRPC.

        Generates the manifest for deployment of the GKE
        connect agent.

        Returns:
            Callable[[~.GenerateConnectManifestRequest],
                    Awaitable[~.GenerateConnectManifestResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_connect_manifest" not in self._stubs:
            self._stubs["generate_connect_manifest"] = self.grpc_channel.unary_unary(
                "/google.cloud.gkehub.v1beta1.GkeHubMembershipService/GenerateConnectManifest",
                request_serializer=membership.GenerateConnectManifestRequest.serialize,
                response_deserializer=membership.GenerateConnectManifestResponse.deserialize,
            )
        return self._stubs["generate_connect_manifest"]

    @property
    def validate_exclusivity(
        self,
    ) -> Callable[
        [membership.ValidateExclusivityRequest],
        Awaitable[membership.ValidateExclusivityResponse],
    ]:
        r"""Return a callable for the validate exclusivity method over gRPC.

        ValidateExclusivity validates the state of
        exclusivity in the cluster. The validation does not
        depend on an existing Hub membership resource.

        Returns:
            Callable[[~.ValidateExclusivityRequest],
                    Awaitable[~.ValidateExclusivityResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "validate_exclusivity" not in self._stubs:
            self._stubs["validate_exclusivity"] = self.grpc_channel.unary_unary(
                "/google.cloud.gkehub.v1beta1.GkeHubMembershipService/ValidateExclusivity",
                request_serializer=membership.ValidateExclusivityRequest.serialize,
                response_deserializer=membership.ValidateExclusivityResponse.deserialize,
            )
        return self._stubs["validate_exclusivity"]

    @property
    def generate_exclusivity_manifest(
        self,
    ) -> Callable[
        [membership.GenerateExclusivityManifestRequest],
        Awaitable[membership.GenerateExclusivityManifestResponse],
    ]:
        r"""Return a callable for the generate exclusivity manifest method over gRPC.

        GenerateExclusivityManifest generates the manifests
        to update the exclusivity artifacts in the cluster if
        needed.
        Exclusivity artifacts include the Membership custom
        resource definition (CRD) and the singleton Membership
        custom resource (CR). Combined with ValidateExclusivity,
        exclusivity artifacts guarantee that a Kubernetes
        cluster is only registered to a single GKE Hub.

        The Membership CRD is versioned, and may require
        conversion when the GKE Hub API server begins serving a
        newer version of the CRD and corresponding CR. The
        response will be the converted CRD and CR if there are
        any differences between the versions.

        Returns:
            Callable[[~.GenerateExclusivityManifestRequest],
                    Awaitable[~.GenerateExclusivityManifestResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_exclusivity_manifest" not in self._stubs:
            self._stubs[
                "generate_exclusivity_manifest"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.gkehub.v1beta1.GkeHubMembershipService/GenerateExclusivityManifest",
                request_serializer=membership.GenerateExclusivityManifestRequest.serialize,
                response_deserializer=membership.GenerateExclusivityManifestResponse.deserialize,
            )
        return self._stubs["generate_exclusivity_manifest"]


__all__ = ("GkeHubMembershipServiceGrpcAsyncIOTransport",)
