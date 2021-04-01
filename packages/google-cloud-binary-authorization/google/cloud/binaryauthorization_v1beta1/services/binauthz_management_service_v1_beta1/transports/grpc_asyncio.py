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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple

from google.api_core import gapic_v1  # type: ignore
from google.api_core import grpc_helpers_async  # type: ignore
from google import auth  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.binaryauthorization_v1beta1.types import resources
from google.cloud.binaryauthorization_v1beta1.types import service
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import BinauthzManagementServiceV1Beta1Transport, DEFAULT_CLIENT_INFO
from .grpc import BinauthzManagementServiceV1Beta1GrpcTransport


class BinauthzManagementServiceV1Beta1GrpcAsyncIOTransport(
    BinauthzManagementServiceV1Beta1Transport
):
    """gRPC AsyncIO backend transport for BinauthzManagementServiceV1Beta1.

    Google Cloud Management Service for Binary Authorization admission
    policies and attestation authorities.

    This API implements a REST model with the following objects:

    -  [Policy][google.cloud.binaryauthorization.v1beta1.Policy]
    -  [Attestor][google.cloud.binaryauthorization.v1beta1.Attestor]

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
        host: str = "binaryauthorization.googleapis.com",
        credentials: credentials.Credentials = None,
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
        scopes = scopes or cls.AUTH_SCOPES
        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "binaryauthorization.googleapis.com",
        credentials: credentials.Credentials = None,
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
            host (Optional[str]): The hostname to connect to.
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
    def get_policy(
        self,
    ) -> Callable[[service.GetPolicyRequest], Awaitable[resources.Policy]]:
        r"""Return a callable for the get policy method over gRPC.

        A [policy][google.cloud.binaryauthorization.v1beta1.Policy]
        specifies the
        [attestors][google.cloud.binaryauthorization.v1beta1.Attestor]
        that must attest to a container image, before the project is
        allowed to deploy that image. There is at most one policy per
        project. All image admission requests are permitted if a project
        has no policy.

        Gets the
        [policy][google.cloud.binaryauthorization.v1beta1.Policy] for
        this project. Returns a default
        [policy][google.cloud.binaryauthorization.v1beta1.Policy] if the
        project does not have one.

        Returns:
            Callable[[~.GetPolicyRequest],
                    Awaitable[~.Policy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_policy" not in self._stubs:
            self._stubs["get_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.binaryauthorization.v1beta1.BinauthzManagementServiceV1Beta1/GetPolicy",
                request_serializer=service.GetPolicyRequest.serialize,
                response_deserializer=resources.Policy.deserialize,
            )
        return self._stubs["get_policy"]

    @property
    def update_policy(
        self,
    ) -> Callable[[service.UpdatePolicyRequest], Awaitable[resources.Policy]]:
        r"""Return a callable for the update policy method over gRPC.

        Creates or updates a project's
        [policy][google.cloud.binaryauthorization.v1beta1.Policy], and
        returns a copy of the new
        [policy][google.cloud.binaryauthorization.v1beta1.Policy]. A
        policy is always updated as a whole, to avoid race conditions
        with concurrent policy enforcement (or management!) requests.
        Returns NOT_FOUND if the project does not exist,
        INVALID_ARGUMENT if the request is malformed.

        Returns:
            Callable[[~.UpdatePolicyRequest],
                    Awaitable[~.Policy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_policy" not in self._stubs:
            self._stubs["update_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.binaryauthorization.v1beta1.BinauthzManagementServiceV1Beta1/UpdatePolicy",
                request_serializer=service.UpdatePolicyRequest.serialize,
                response_deserializer=resources.Policy.deserialize,
            )
        return self._stubs["update_policy"]

    @property
    def create_attestor(
        self,
    ) -> Callable[[service.CreateAttestorRequest], Awaitable[resources.Attestor]]:
        r"""Return a callable for the create attestor method over gRPC.

        Creates an
        [attestor][google.cloud.binaryauthorization.v1beta1.Attestor],
        and returns a copy of the new
        [attestor][google.cloud.binaryauthorization.v1beta1.Attestor].
        Returns NOT_FOUND if the project does not exist,
        INVALID_ARGUMENT if the request is malformed, ALREADY_EXISTS if
        the
        [attestor][google.cloud.binaryauthorization.v1beta1.Attestor]
        already exists.

        Returns:
            Callable[[~.CreateAttestorRequest],
                    Awaitable[~.Attestor]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_attestor" not in self._stubs:
            self._stubs["create_attestor"] = self.grpc_channel.unary_unary(
                "/google.cloud.binaryauthorization.v1beta1.BinauthzManagementServiceV1Beta1/CreateAttestor",
                request_serializer=service.CreateAttestorRequest.serialize,
                response_deserializer=resources.Attestor.deserialize,
            )
        return self._stubs["create_attestor"]

    @property
    def get_attestor(
        self,
    ) -> Callable[[service.GetAttestorRequest], Awaitable[resources.Attestor]]:
        r"""Return a callable for the get attestor method over gRPC.

        Gets an
        [attestor][google.cloud.binaryauthorization.v1beta1.Attestor].
        Returns NOT_FOUND if the
        [attestor][google.cloud.binaryauthorization.v1beta1.Attestor]
        does not exist.

        Returns:
            Callable[[~.GetAttestorRequest],
                    Awaitable[~.Attestor]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_attestor" not in self._stubs:
            self._stubs["get_attestor"] = self.grpc_channel.unary_unary(
                "/google.cloud.binaryauthorization.v1beta1.BinauthzManagementServiceV1Beta1/GetAttestor",
                request_serializer=service.GetAttestorRequest.serialize,
                response_deserializer=resources.Attestor.deserialize,
            )
        return self._stubs["get_attestor"]

    @property
    def update_attestor(
        self,
    ) -> Callable[[service.UpdateAttestorRequest], Awaitable[resources.Attestor]]:
        r"""Return a callable for the update attestor method over gRPC.

        Updates an
        [attestor][google.cloud.binaryauthorization.v1beta1.Attestor].
        Returns NOT_FOUND if the
        [attestor][google.cloud.binaryauthorization.v1beta1.Attestor]
        does not exist.

        Returns:
            Callable[[~.UpdateAttestorRequest],
                    Awaitable[~.Attestor]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_attestor" not in self._stubs:
            self._stubs["update_attestor"] = self.grpc_channel.unary_unary(
                "/google.cloud.binaryauthorization.v1beta1.BinauthzManagementServiceV1Beta1/UpdateAttestor",
                request_serializer=service.UpdateAttestorRequest.serialize,
                response_deserializer=resources.Attestor.deserialize,
            )
        return self._stubs["update_attestor"]

    @property
    def list_attestors(
        self,
    ) -> Callable[
        [service.ListAttestorsRequest], Awaitable[service.ListAttestorsResponse]
    ]:
        r"""Return a callable for the list attestors method over gRPC.

        Lists
        [attestors][google.cloud.binaryauthorization.v1beta1.Attestor].
        Returns INVALID_ARGUMENT if the project does not exist.

        Returns:
            Callable[[~.ListAttestorsRequest],
                    Awaitable[~.ListAttestorsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_attestors" not in self._stubs:
            self._stubs["list_attestors"] = self.grpc_channel.unary_unary(
                "/google.cloud.binaryauthorization.v1beta1.BinauthzManagementServiceV1Beta1/ListAttestors",
                request_serializer=service.ListAttestorsRequest.serialize,
                response_deserializer=service.ListAttestorsResponse.deserialize,
            )
        return self._stubs["list_attestors"]

    @property
    def delete_attestor(
        self,
    ) -> Callable[[service.DeleteAttestorRequest], Awaitable[empty.Empty]]:
        r"""Return a callable for the delete attestor method over gRPC.

        Deletes an
        [attestor][google.cloud.binaryauthorization.v1beta1.Attestor].
        Returns NOT_FOUND if the
        [attestor][google.cloud.binaryauthorization.v1beta1.Attestor]
        does not exist.

        Returns:
            Callable[[~.DeleteAttestorRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_attestor" not in self._stubs:
            self._stubs["delete_attestor"] = self.grpc_channel.unary_unary(
                "/google.cloud.binaryauthorization.v1beta1.BinauthzManagementServiceV1Beta1/DeleteAttestor",
                request_serializer=service.DeleteAttestorRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_attestor"]


__all__ = ("BinauthzManagementServiceV1Beta1GrpcAsyncIOTransport",)
