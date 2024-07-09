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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async, operations_v1
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.developerconnect_v1.types import developer_connect

from .base import DEFAULT_CLIENT_INFO, DeveloperConnectTransport
from .grpc import DeveloperConnectGrpcTransport


class DeveloperConnectGrpcAsyncIOTransport(DeveloperConnectTransport):
    """gRPC AsyncIO backend transport for DeveloperConnect.

    Service describing handlers for resources

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
        host: str = "developerconnect.googleapis.com",
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
        host: str = "developerconnect.googleapis.com",
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
                 The hostname to connect to (default: 'developerconnect.googleapis.com').
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
    def list_connections(
        self,
    ) -> Callable[
        [developer_connect.ListConnectionsRequest],
        Awaitable[developer_connect.ListConnectionsResponse],
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
                "/google.cloud.developerconnect.v1.DeveloperConnect/ListConnections",
                request_serializer=developer_connect.ListConnectionsRequest.serialize,
                response_deserializer=developer_connect.ListConnectionsResponse.deserialize,
            )
        return self._stubs["list_connections"]

    @property
    def get_connection(
        self,
    ) -> Callable[
        [developer_connect.GetConnectionRequest],
        Awaitable[developer_connect.Connection],
    ]:
        r"""Return a callable for the get connection method over gRPC.

        Gets details of a single Connection.

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
                "/google.cloud.developerconnect.v1.DeveloperConnect/GetConnection",
                request_serializer=developer_connect.GetConnectionRequest.serialize,
                response_deserializer=developer_connect.Connection.deserialize,
            )
        return self._stubs["get_connection"]

    @property
    def create_connection(
        self,
    ) -> Callable[
        [developer_connect.CreateConnectionRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create connection method over gRPC.

        Creates a new Connection in a given project and
        location.

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
                "/google.cloud.developerconnect.v1.DeveloperConnect/CreateConnection",
                request_serializer=developer_connect.CreateConnectionRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_connection"]

    @property
    def update_connection(
        self,
    ) -> Callable[
        [developer_connect.UpdateConnectionRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update connection method over gRPC.

        Updates the parameters of a single Connection.

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
                "/google.cloud.developerconnect.v1.DeveloperConnect/UpdateConnection",
                request_serializer=developer_connect.UpdateConnectionRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_connection"]

    @property
    def delete_connection(
        self,
    ) -> Callable[
        [developer_connect.DeleteConnectionRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete connection method over gRPC.

        Deletes a single Connection.

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
                "/google.cloud.developerconnect.v1.DeveloperConnect/DeleteConnection",
                request_serializer=developer_connect.DeleteConnectionRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_connection"]

    @property
    def create_git_repository_link(
        self,
    ) -> Callable[
        [developer_connect.CreateGitRepositoryLinkRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create git repository link method over gRPC.

        Creates a GitRepositoryLink. Upon linking a Git
        Repository, Developer Connect will configure the Git
        Repository to send webhook events to Developer Connect.
        Connections that use Firebase GitHub Application will
        have events forwarded to the Firebase service. All other
        Connections will have events forwarded to Cloud Build.

        Returns:
            Callable[[~.CreateGitRepositoryLinkRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_git_repository_link" not in self._stubs:
            self._stubs["create_git_repository_link"] = self.grpc_channel.unary_unary(
                "/google.cloud.developerconnect.v1.DeveloperConnect/CreateGitRepositoryLink",
                request_serializer=developer_connect.CreateGitRepositoryLinkRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_git_repository_link"]

    @property
    def delete_git_repository_link(
        self,
    ) -> Callable[
        [developer_connect.DeleteGitRepositoryLinkRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete git repository link method over gRPC.

        Deletes a single GitRepositoryLink.

        Returns:
            Callable[[~.DeleteGitRepositoryLinkRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_git_repository_link" not in self._stubs:
            self._stubs["delete_git_repository_link"] = self.grpc_channel.unary_unary(
                "/google.cloud.developerconnect.v1.DeveloperConnect/DeleteGitRepositoryLink",
                request_serializer=developer_connect.DeleteGitRepositoryLinkRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_git_repository_link"]

    @property
    def list_git_repository_links(
        self,
    ) -> Callable[
        [developer_connect.ListGitRepositoryLinksRequest],
        Awaitable[developer_connect.ListGitRepositoryLinksResponse],
    ]:
        r"""Return a callable for the list git repository links method over gRPC.

        Lists GitRepositoryLinks in a given project,
        location, and connection.

        Returns:
            Callable[[~.ListGitRepositoryLinksRequest],
                    Awaitable[~.ListGitRepositoryLinksResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_git_repository_links" not in self._stubs:
            self._stubs["list_git_repository_links"] = self.grpc_channel.unary_unary(
                "/google.cloud.developerconnect.v1.DeveloperConnect/ListGitRepositoryLinks",
                request_serializer=developer_connect.ListGitRepositoryLinksRequest.serialize,
                response_deserializer=developer_connect.ListGitRepositoryLinksResponse.deserialize,
            )
        return self._stubs["list_git_repository_links"]

    @property
    def get_git_repository_link(
        self,
    ) -> Callable[
        [developer_connect.GetGitRepositoryLinkRequest],
        Awaitable[developer_connect.GitRepositoryLink],
    ]:
        r"""Return a callable for the get git repository link method over gRPC.

        Gets details of a single GitRepositoryLink.

        Returns:
            Callable[[~.GetGitRepositoryLinkRequest],
                    Awaitable[~.GitRepositoryLink]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_git_repository_link" not in self._stubs:
            self._stubs["get_git_repository_link"] = self.grpc_channel.unary_unary(
                "/google.cloud.developerconnect.v1.DeveloperConnect/GetGitRepositoryLink",
                request_serializer=developer_connect.GetGitRepositoryLinkRequest.serialize,
                response_deserializer=developer_connect.GitRepositoryLink.deserialize,
            )
        return self._stubs["get_git_repository_link"]

    @property
    def fetch_read_write_token(
        self,
    ) -> Callable[
        [developer_connect.FetchReadWriteTokenRequest],
        Awaitable[developer_connect.FetchReadWriteTokenResponse],
    ]:
        r"""Return a callable for the fetch read write token method over gRPC.

        Fetches read/write token of a given
        gitRepositoryLink.

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
                "/google.cloud.developerconnect.v1.DeveloperConnect/FetchReadWriteToken",
                request_serializer=developer_connect.FetchReadWriteTokenRequest.serialize,
                response_deserializer=developer_connect.FetchReadWriteTokenResponse.deserialize,
            )
        return self._stubs["fetch_read_write_token"]

    @property
    def fetch_read_token(
        self,
    ) -> Callable[
        [developer_connect.FetchReadTokenRequest],
        Awaitable[developer_connect.FetchReadTokenResponse],
    ]:
        r"""Return a callable for the fetch read token method over gRPC.

        Fetches read token of a given gitRepositoryLink.

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
                "/google.cloud.developerconnect.v1.DeveloperConnect/FetchReadToken",
                request_serializer=developer_connect.FetchReadTokenRequest.serialize,
                response_deserializer=developer_connect.FetchReadTokenResponse.deserialize,
            )
        return self._stubs["fetch_read_token"]

    @property
    def fetch_linkable_git_repositories(
        self,
    ) -> Callable[
        [developer_connect.FetchLinkableGitRepositoriesRequest],
        Awaitable[developer_connect.FetchLinkableGitRepositoriesResponse],
    ]:
        r"""Return a callable for the fetch linkable git
        repositories method over gRPC.

        FetchLinkableGitRepositories returns a list of git
        repositories from an SCM that are available to be added
        to a Connection.

        Returns:
            Callable[[~.FetchLinkableGitRepositoriesRequest],
                    Awaitable[~.FetchLinkableGitRepositoriesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_linkable_git_repositories" not in self._stubs:
            self._stubs[
                "fetch_linkable_git_repositories"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.developerconnect.v1.DeveloperConnect/FetchLinkableGitRepositories",
                request_serializer=developer_connect.FetchLinkableGitRepositoriesRequest.serialize,
                response_deserializer=developer_connect.FetchLinkableGitRepositoriesResponse.deserialize,
            )
        return self._stubs["fetch_linkable_git_repositories"]

    @property
    def fetch_git_hub_installations(
        self,
    ) -> Callable[
        [developer_connect.FetchGitHubInstallationsRequest],
        Awaitable[developer_connect.FetchGitHubInstallationsResponse],
    ]:
        r"""Return a callable for the fetch git hub installations method over gRPC.

        FetchGitHubInstallations returns the list of GitHub
        Installations that are available to be added to a
        Connection. For github.com, only installations
        accessible to the authorizer token are returned. For
        GitHub Enterprise, all installations are returned.

        Returns:
            Callable[[~.FetchGitHubInstallationsRequest],
                    Awaitable[~.FetchGitHubInstallationsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_git_hub_installations" not in self._stubs:
            self._stubs["fetch_git_hub_installations"] = self.grpc_channel.unary_unary(
                "/google.cloud.developerconnect.v1.DeveloperConnect/FetchGitHubInstallations",
                request_serializer=developer_connect.FetchGitHubInstallationsRequest.serialize,
                response_deserializer=developer_connect.FetchGitHubInstallationsResponse.deserialize,
            )
        return self._stubs["fetch_git_hub_installations"]

    @property
    def fetch_git_refs(
        self,
    ) -> Callable[
        [developer_connect.FetchGitRefsRequest],
        Awaitable[developer_connect.FetchGitRefsResponse],
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
                "/google.cloud.developerconnect.v1.DeveloperConnect/FetchGitRefs",
                request_serializer=developer_connect.FetchGitRefsRequest.serialize,
                response_deserializer=developer_connect.FetchGitRefsResponse.deserialize,
            )
        return self._stubs["fetch_git_refs"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.list_connections: gapic_v1.method_async.wrap_method(
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
            self.get_connection: gapic_v1.method_async.wrap_method(
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
            self.create_connection: gapic_v1.method_async.wrap_method(
                self.create_connection,
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
            self.update_connection: gapic_v1.method_async.wrap_method(
                self.update_connection,
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
            self.delete_connection: gapic_v1.method_async.wrap_method(
                self.delete_connection,
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
            self.create_git_repository_link: gapic_v1.method_async.wrap_method(
                self.create_git_repository_link,
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
            self.delete_git_repository_link: gapic_v1.method_async.wrap_method(
                self.delete_git_repository_link,
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
            self.list_git_repository_links: gapic_v1.method_async.wrap_method(
                self.list_git_repository_links,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_git_repository_link: gapic_v1.method_async.wrap_method(
                self.get_git_repository_link,
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
            self.fetch_read_write_token: gapic_v1.method_async.wrap_method(
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
            self.fetch_read_token: gapic_v1.method_async.wrap_method(
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
            self.fetch_linkable_git_repositories: gapic_v1.method_async.wrap_method(
                self.fetch_linkable_git_repositories,
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
            self.fetch_git_hub_installations: gapic_v1.method_async.wrap_method(
                self.fetch_git_hub_installations,
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
            self.fetch_git_refs: gapic_v1.method_async.wrap_method(
                self.fetch_git_refs,
                default_timeout=None,
                client_info=client_info,
            ),
        }

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


__all__ = ("DeveloperConnectGrpcAsyncIOTransport",)
