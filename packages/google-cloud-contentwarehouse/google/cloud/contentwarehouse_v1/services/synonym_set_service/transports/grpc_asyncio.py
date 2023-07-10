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

from google.api_core import gapic_v1, grpc_helpers_async
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.contentwarehouse_v1.types import (
    synonymset,
    synonymset_service_request,
)

from .base import DEFAULT_CLIENT_INFO, SynonymSetServiceTransport
from .grpc import SynonymSetServiceGrpcTransport


class SynonymSetServiceGrpcAsyncIOTransport(SynonymSetServiceTransport):
    """gRPC AsyncIO backend transport for SynonymSetService.

    A Service that manage/custom customer specified SynonymSets.

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
        host: str = "contentwarehouse.googleapis.com",
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
        host: str = "contentwarehouse.googleapis.com",
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
    def create_synonym_set(
        self,
    ) -> Callable[
        [synonymset_service_request.CreateSynonymSetRequest],
        Awaitable[synonymset.SynonymSet],
    ]:
        r"""Return a callable for the create synonym set method over gRPC.

        Creates a SynonymSet for a single context. Throws an
        ALREADY_EXISTS exception if a synonymset already exists for the
        context.

        Returns:
            Callable[[~.CreateSynonymSetRequest],
                    Awaitable[~.SynonymSet]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_synonym_set" not in self._stubs:
            self._stubs["create_synonym_set"] = self.grpc_channel.unary_unary(
                "/google.cloud.contentwarehouse.v1.SynonymSetService/CreateSynonymSet",
                request_serializer=synonymset_service_request.CreateSynonymSetRequest.serialize,
                response_deserializer=synonymset.SynonymSet.deserialize,
            )
        return self._stubs["create_synonym_set"]

    @property
    def get_synonym_set(
        self,
    ) -> Callable[
        [synonymset_service_request.GetSynonymSetRequest],
        Awaitable[synonymset.SynonymSet],
    ]:
        r"""Return a callable for the get synonym set method over gRPC.

        Gets a SynonymSet for a particular context. Throws a NOT_FOUND
        exception if the Synonymset does not exist

        Returns:
            Callable[[~.GetSynonymSetRequest],
                    Awaitable[~.SynonymSet]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_synonym_set" not in self._stubs:
            self._stubs["get_synonym_set"] = self.grpc_channel.unary_unary(
                "/google.cloud.contentwarehouse.v1.SynonymSetService/GetSynonymSet",
                request_serializer=synonymset_service_request.GetSynonymSetRequest.serialize,
                response_deserializer=synonymset.SynonymSet.deserialize,
            )
        return self._stubs["get_synonym_set"]

    @property
    def update_synonym_set(
        self,
    ) -> Callable[
        [synonymset_service_request.UpdateSynonymSetRequest],
        Awaitable[synonymset.SynonymSet],
    ]:
        r"""Return a callable for the update synonym set method over gRPC.

        Remove the existing SynonymSet for the context and replaces it
        with a new one. Throws a NOT_FOUND exception if the SynonymSet
        is not found.

        Returns:
            Callable[[~.UpdateSynonymSetRequest],
                    Awaitable[~.SynonymSet]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_synonym_set" not in self._stubs:
            self._stubs["update_synonym_set"] = self.grpc_channel.unary_unary(
                "/google.cloud.contentwarehouse.v1.SynonymSetService/UpdateSynonymSet",
                request_serializer=synonymset_service_request.UpdateSynonymSetRequest.serialize,
                response_deserializer=synonymset.SynonymSet.deserialize,
            )
        return self._stubs["update_synonym_set"]

    @property
    def delete_synonym_set(
        self,
    ) -> Callable[
        [synonymset_service_request.DeleteSynonymSetRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete synonym set method over gRPC.

        Deletes a SynonymSet for a given context. Throws a NOT_FOUND
        exception if the SynonymSet is not found.

        Returns:
            Callable[[~.DeleteSynonymSetRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_synonym_set" not in self._stubs:
            self._stubs["delete_synonym_set"] = self.grpc_channel.unary_unary(
                "/google.cloud.contentwarehouse.v1.SynonymSetService/DeleteSynonymSet",
                request_serializer=synonymset_service_request.DeleteSynonymSetRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_synonym_set"]

    @property
    def list_synonym_sets(
        self,
    ) -> Callable[
        [synonymset_service_request.ListSynonymSetsRequest],
        Awaitable[synonymset_service_request.ListSynonymSetsResponse],
    ]:
        r"""Return a callable for the list synonym sets method over gRPC.

        Returns all SynonymSets (for all contexts) for the
        specified location.

        Returns:
            Callable[[~.ListSynonymSetsRequest],
                    Awaitable[~.ListSynonymSetsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_synonym_sets" not in self._stubs:
            self._stubs["list_synonym_sets"] = self.grpc_channel.unary_unary(
                "/google.cloud.contentwarehouse.v1.SynonymSetService/ListSynonymSets",
                request_serializer=synonymset_service_request.ListSynonymSetsRequest.serialize,
                response_deserializer=synonymset_service_request.ListSynonymSetsResponse.deserialize,
            )
        return self._stubs["list_synonym_sets"]

    def close(self):
        return self.grpc_channel.close()

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


__all__ = ("SynonymSetServiceGrpcAsyncIOTransport",)
