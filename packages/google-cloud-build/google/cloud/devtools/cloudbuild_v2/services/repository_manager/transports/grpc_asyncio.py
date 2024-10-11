# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
import inspect
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async, operations_v1
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.devtools.cloudbuild_v2.types import repositories

from .base import DEFAULT_CLIENT_INFO, RepositoryManagerTransport
from .grpc import RepositoryManagerGrpcTransport


class RepositoryManagerGrpcAsyncIOTransport(RepositoryManagerTransport):
    """gRPC AsyncIO backend transport for RepositoryManager.

    Manages connections to source code repositories.

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
        host: str = "cloudbuild.googleapis.com",
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
        host: str = "cloudbuild.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[aio.Channel, Callable[..., aio.Channel]]] = None,
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
                 The hostname to connect to (default: 'cloudbuild.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[Union[aio.Channel, Callable[..., aio.Channel]]]):
                A ``Channel`` instance through which to make calls, or a Callable
                that constructs and returns one. If set to None, ``self.create_channel``
                is used to create the channel. If a Callable is given, it will be called
                with the same arguments as used in ``self.create_channel``.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if a ``channel`` instance is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if a ``channel`` instance or ``ssl_channel_credentials`` is provided.
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

        if isinstance(channel, aio.Channel):
            # Ignore credentials if a channel was passed.
            credentials = None
            self._ignore_credentials = True
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
            # initialize with the provided callable or the default channel
            channel_init = channel or type(self).create_channel
            self._grpc_channel = channel_init(
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
        self._wrap_with_kind = (
            "kind" in inspect.signature(gapic_v1.method_async.wrap_method).parameters
        )
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
    def create_connection(
        self,
    ) -> Callable[
        [repositories.CreateConnectionRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create connection method over gRPC.

        Creates a Connection.

        Returns:
            Callable[[~.CreateConnectionRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_connection" not in self._stubs:
            self._stubs["create_connection"] = self.grpc_channel.unary_unary(
                "/google.devtools.cloudbuild.v2.RepositoryManager/CreateConnection",
                request_serializer=repositories.CreateConnectionRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_connection"]

    @property
    def get_connection(
        self,
    ) -> Callable[
        [repositories.GetConnectionRequest], Awaitable[repositories.Connection]
    ]:
        r"""Return a callable for the get connection method over gRPC.

        Gets details of a single connection.

        Returns:
            Callable[[~.GetConnectionRequest],
                    Awaitable[~.Connection]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_connection" not in self._stubs:
            self._stubs["get_connection"] = self.grpc_channel.unary_unary(
                "/google.devtools.cloudbuild.v2.RepositoryManager/GetConnection",
                request_serializer=repositories.GetConnectionRequest.serialize,
                response_deserializer=repositories.Connection.deserialize,
            )
        return self._stubs["get_connection"]

    @property
    def list_connections(
        self,
    ) -> Callable[
        [repositories.ListConnectionsRequest],
        Awaitable[repositories.ListConnectionsResponse],
    ]:
        r"""Return a callable for the list connections method over gRPC.

        Lists Connections in a given project and location.

        Returns:
            Callable[[~.ListConnectionsRequest],
                    Awaitable[~.ListConnectionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_connections" not in self._stubs:
            self._stubs["list_connections"] = self.grpc_channel.unary_unary(
                "/google.devtools.cloudbuild.v2.RepositoryManager/ListConnections",
                request_serializer=repositories.ListConnectionsRequest.serialize,
                response_deserializer=repositories.ListConnectionsResponse.deserialize,
            )
        return self._stubs["list_connections"]

    @property
    def update_connection(
        self,
    ) -> Callable[
        [repositories.UpdateConnectionRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update connection method over gRPC.

        Updates a single connection.

        Returns:
            Callable[[~.UpdateConnectionRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_connection" not in self._stubs:
            self._stubs["update_connection"] = self.grpc_channel.unary_unary(
                "/google.devtools.cloudbuild.v2.RepositoryManager/UpdateConnection",
                request_serializer=repositories.UpdateConnectionRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_connection"]

    @property
    def delete_connection(
        self,
    ) -> Callable[
        [repositories.DeleteConnectionRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete connection method over gRPC.

        Deletes a single connection.

        Returns:
            Callable[[~.DeleteConnectionRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_connection" not in self._stubs:
            self._stubs["delete_connection"] = self.grpc_channel.unary_unary(
                "/google.devtools.cloudbuild.v2.RepositoryManager/DeleteConnection",
                request_serializer=repositories.DeleteConnectionRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_connection"]

    @property
    def create_repository(
        self,
    ) -> Callable[
        [repositories.CreateRepositoryRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create repository method over gRPC.

        Creates a Repository.

        Returns:
            Callable[[~.CreateRepositoryRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_repository" not in self._stubs:
            self._stubs["create_repository"] = self.grpc_channel.unary_unary(
                "/google.devtools.cloudbuild.v2.RepositoryManager/CreateRepository",
                request_serializer=repositories.CreateRepositoryRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_repository"]

    @property
    def batch_create_repositories(
        self,
    ) -> Callable[
        [repositories.BatchCreateRepositoriesRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the batch create repositories method over gRPC.

        Creates multiple repositories inside a connection.

        Returns:
            Callable[[~.BatchCreateRepositoriesRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_create_repositories" not in self._stubs:
            self._stubs["batch_create_repositories"] = self.grpc_channel.unary_unary(
                "/google.devtools.cloudbuild.v2.RepositoryManager/BatchCreateRepositories",
                request_serializer=repositories.BatchCreateRepositoriesRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["batch_create_repositories"]

    @property
    def get_repository(
        self,
    ) -> Callable[
        [repositories.GetRepositoryRequest], Awaitable[repositories.Repository]
    ]:
        r"""Return a callable for the get repository method over gRPC.

        Gets details of a single repository.

        Returns:
            Callable[[~.GetRepositoryRequest],
                    Awaitable[~.Repository]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_repository" not in self._stubs:
            self._stubs["get_repository"] = self.grpc_channel.unary_unary(
                "/google.devtools.cloudbuild.v2.RepositoryManager/GetRepository",
                request_serializer=repositories.GetRepositoryRequest.serialize,
                response_deserializer=repositories.Repository.deserialize,
            )
        return self._stubs["get_repository"]

    @property
    def list_repositories(
        self,
    ) -> Callable[
        [repositories.ListRepositoriesRequest],
        Awaitable[repositories.ListRepositoriesResponse],
    ]:
        r"""Return a callable for the list repositories method over gRPC.

        Lists Repositories in a given connection.

        Returns:
            Callable[[~.ListRepositoriesRequest],
                    Awaitable[~.ListRepositoriesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_repositories" not in self._stubs:
            self._stubs["list_repositories"] = self.grpc_channel.unary_unary(
                "/google.devtools.cloudbuild.v2.RepositoryManager/ListRepositories",
                request_serializer=repositories.ListRepositoriesRequest.serialize,
                response_deserializer=repositories.ListRepositoriesResponse.deserialize,
            )
        return self._stubs["list_repositories"]

    @property
    def delete_repository(
        self,
    ) -> Callable[
        [repositories.DeleteRepositoryRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete repository method over gRPC.

        Deletes a single repository.

        Returns:
            Callable[[~.DeleteRepositoryRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_repository" not in self._stubs:
            self._stubs["delete_repository"] = self.grpc_channel.unary_unary(
                "/google.devtools.cloudbuild.v2.RepositoryManager/DeleteRepository",
                request_serializer=repositories.DeleteRepositoryRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_repository"]

    @property
    def fetch_read_write_token(
        self,
    ) -> Callable[
        [repositories.FetchReadWriteTokenRequest],
        Awaitable[repositories.FetchReadWriteTokenResponse],
    ]:
        r"""Return a callable for the fetch read write token method over gRPC.

        Fetches read/write token of a given repository.

        Returns:
            Callable[[~.FetchReadWriteTokenRequest],
                    Awaitable[~.FetchReadWriteTokenResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_read_write_token" not in self._stubs:
            self._stubs["fetch_read_write_token"] = self.grpc_channel.unary_unary(
                "/google.devtools.cloudbuild.v2.RepositoryManager/FetchReadWriteToken",
                request_serializer=repositories.FetchReadWriteTokenRequest.serialize,
                response_deserializer=repositories.FetchReadWriteTokenResponse.deserialize,
            )
        return self._stubs["fetch_read_write_token"]

    @property
    def fetch_read_token(
        self,
    ) -> Callable[
        [repositories.FetchReadTokenRequest],
        Awaitable[repositories.FetchReadTokenResponse],
    ]:
        r"""Return a callable for the fetch read token method over gRPC.

        Fetches read token of a given repository.

        Returns:
            Callable[[~.FetchReadTokenRequest],
                    Awaitable[~.FetchReadTokenResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_read_token" not in self._stubs:
            self._stubs["fetch_read_token"] = self.grpc_channel.unary_unary(
                "/google.devtools.cloudbuild.v2.RepositoryManager/FetchReadToken",
                request_serializer=repositories.FetchReadTokenRequest.serialize,
                response_deserializer=repositories.FetchReadTokenResponse.deserialize,
            )
        return self._stubs["fetch_read_token"]

    @property
    def fetch_linkable_repositories(
        self,
    ) -> Callable[
        [repositories.FetchLinkableRepositoriesRequest],
        Awaitable[repositories.FetchLinkableRepositoriesResponse],
    ]:
        r"""Return a callable for the fetch linkable repositories method over gRPC.

        FetchLinkableRepositories get repositories from SCM
        that are accessible and could be added to the
        connection.

        Returns:
            Callable[[~.FetchLinkableRepositoriesRequest],
                    Awaitable[~.FetchLinkableRepositoriesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_linkable_repositories" not in self._stubs:
            self._stubs["fetch_linkable_repositories"] = self.grpc_channel.unary_unary(
                "/google.devtools.cloudbuild.v2.RepositoryManager/FetchLinkableRepositories",
                request_serializer=repositories.FetchLinkableRepositoriesRequest.serialize,
                response_deserializer=repositories.FetchLinkableRepositoriesResponse.deserialize,
            )
        return self._stubs["fetch_linkable_repositories"]

    @property
    def fetch_git_refs(
        self,
    ) -> Callable[
        [repositories.FetchGitRefsRequest], Awaitable[repositories.FetchGitRefsResponse]
    ]:
        r"""Return a callable for the fetch git refs method over gRPC.

        Fetch the list of branches or tags for a given
        repository.

        Returns:
            Callable[[~.FetchGitRefsRequest],
                    Awaitable[~.FetchGitRefsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_git_refs" not in self._stubs:
            self._stubs["fetch_git_refs"] = self.grpc_channel.unary_unary(
                "/google.devtools.cloudbuild.v2.RepositoryManager/FetchGitRefs",
                request_serializer=repositories.FetchGitRefsRequest.serialize,
                response_deserializer=repositories.FetchGitRefsResponse.deserialize,
            )
        return self._stubs["fetch_git_refs"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.create_connection: self._wrap_method(
                self.create_connection,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_connection: self._wrap_method(
                self.get_connection,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_connections: self._wrap_method(
                self.list_connections,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_connection: self._wrap_method(
                self.update_connection,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_connection: self._wrap_method(
                self.delete_connection,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_repository: self._wrap_method(
                self.create_repository,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.batch_create_repositories: self._wrap_method(
                self.batch_create_repositories,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_repository: self._wrap_method(
                self.get_repository,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_repositories: self._wrap_method(
                self.list_repositories,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_repository: self._wrap_method(
                self.delete_repository,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.fetch_read_write_token: self._wrap_method(
                self.fetch_read_write_token,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.fetch_read_token: self._wrap_method(
                self.fetch_read_token,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.fetch_linkable_repositories: self._wrap_method(
                self.fetch_linkable_repositories,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.fetch_git_refs: self._wrap_method(
                self.fetch_git_refs,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_iam_policy: self._wrap_method(
                self.get_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_iam_policy: self._wrap_method(
                self.set_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.test_iam_permissions: self._wrap_method(
                self.test_iam_permissions,
                default_timeout=None,
                client_info=client_info,
            ),
            self.cancel_operation: self._wrap_method(
                self.cancel_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_operation: self._wrap_method(
                self.get_operation,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    def _wrap_method(self, func, *args, **kwargs):
        if self._wrap_with_kind:  # pragma: NO COVER
            kwargs["kind"] = self.kind
        return gapic_v1.method_async.wrap_method(func, *args, **kwargs)

    def close(self):
        return self.grpc_channel.close()

    @property
    def kind(self) -> str:
        return "grpc_asyncio"

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


__all__ = ("RepositoryManagerGrpcAsyncIOTransport",)
