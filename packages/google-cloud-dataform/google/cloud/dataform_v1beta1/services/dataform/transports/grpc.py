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
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
import grpc  # type: ignore

from google.cloud.dataform_v1beta1.types import dataform

from .base import DEFAULT_CLIENT_INFO, DataformTransport


class DataformGrpcTransport(DataformTransport):
    """gRPC backend transport for Dataform.

    Dataform is a service to develop, create, document, test, and
    update curated tables in BigQuery.

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
        host: str = "dataform.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]] = None,
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
                 The hostname to connect to (default: 'dataform.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if a ``channel`` instance is provided.
            channel (Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]]):
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
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
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

        if isinstance(channel, grpc.Channel):
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

    @classmethod
    def create_channel(
        cls,
        host: str = "dataform.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
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
        """Return the channel designed to connect to this service."""
        return self._grpc_channel

    @property
    def list_repositories(
        self,
    ) -> Callable[
        [dataform.ListRepositoriesRequest], dataform.ListRepositoriesResponse
    ]:
        r"""Return a callable for the list repositories method over gRPC.

        Lists Repositories in a given project and location.

        Returns:
            Callable[[~.ListRepositoriesRequest],
                    ~.ListRepositoriesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_repositories" not in self._stubs:
            self._stubs["list_repositories"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/ListRepositories",
                request_serializer=dataform.ListRepositoriesRequest.serialize,
                response_deserializer=dataform.ListRepositoriesResponse.deserialize,
            )
        return self._stubs["list_repositories"]

    @property
    def get_repository(
        self,
    ) -> Callable[[dataform.GetRepositoryRequest], dataform.Repository]:
        r"""Return a callable for the get repository method over gRPC.

        Fetches a single Repository.

        Returns:
            Callable[[~.GetRepositoryRequest],
                    ~.Repository]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_repository" not in self._stubs:
            self._stubs["get_repository"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/GetRepository",
                request_serializer=dataform.GetRepositoryRequest.serialize,
                response_deserializer=dataform.Repository.deserialize,
            )
        return self._stubs["get_repository"]

    @property
    def create_repository(
        self,
    ) -> Callable[[dataform.CreateRepositoryRequest], dataform.Repository]:
        r"""Return a callable for the create repository method over gRPC.

        Creates a new Repository in a given project and
        location.

        Returns:
            Callable[[~.CreateRepositoryRequest],
                    ~.Repository]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_repository" not in self._stubs:
            self._stubs["create_repository"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/CreateRepository",
                request_serializer=dataform.CreateRepositoryRequest.serialize,
                response_deserializer=dataform.Repository.deserialize,
            )
        return self._stubs["create_repository"]

    @property
    def update_repository(
        self,
    ) -> Callable[[dataform.UpdateRepositoryRequest], dataform.Repository]:
        r"""Return a callable for the update repository method over gRPC.

        Updates a single Repository.

        Returns:
            Callable[[~.UpdateRepositoryRequest],
                    ~.Repository]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_repository" not in self._stubs:
            self._stubs["update_repository"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/UpdateRepository",
                request_serializer=dataform.UpdateRepositoryRequest.serialize,
                response_deserializer=dataform.Repository.deserialize,
            )
        return self._stubs["update_repository"]

    @property
    def delete_repository(
        self,
    ) -> Callable[[dataform.DeleteRepositoryRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete repository method over gRPC.

        Deletes a single Repository.

        Returns:
            Callable[[~.DeleteRepositoryRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_repository" not in self._stubs:
            self._stubs["delete_repository"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/DeleteRepository",
                request_serializer=dataform.DeleteRepositoryRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_repository"]

    @property
    def commit_repository_changes(
        self,
    ) -> Callable[[dataform.CommitRepositoryChangesRequest], empty_pb2.Empty]:
        r"""Return a callable for the commit repository changes method over gRPC.

        Applies a Git commit to a Repository. The Repository must not
        have a value for ``git_remote_settings.url``.

        Returns:
            Callable[[~.CommitRepositoryChangesRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "commit_repository_changes" not in self._stubs:
            self._stubs["commit_repository_changes"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/CommitRepositoryChanges",
                request_serializer=dataform.CommitRepositoryChangesRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["commit_repository_changes"]

    @property
    def read_repository_file(
        self,
    ) -> Callable[
        [dataform.ReadRepositoryFileRequest], dataform.ReadRepositoryFileResponse
    ]:
        r"""Return a callable for the read repository file method over gRPC.

        Returns the contents of a file (inside a Repository). The
        Repository must not have a value for
        ``git_remote_settings.url``.

        Returns:
            Callable[[~.ReadRepositoryFileRequest],
                    ~.ReadRepositoryFileResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "read_repository_file" not in self._stubs:
            self._stubs["read_repository_file"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/ReadRepositoryFile",
                request_serializer=dataform.ReadRepositoryFileRequest.serialize,
                response_deserializer=dataform.ReadRepositoryFileResponse.deserialize,
            )
        return self._stubs["read_repository_file"]

    @property
    def query_repository_directory_contents(
        self,
    ) -> Callable[
        [dataform.QueryRepositoryDirectoryContentsRequest],
        dataform.QueryRepositoryDirectoryContentsResponse,
    ]:
        r"""Return a callable for the query repository directory
        contents method over gRPC.

        Returns the contents of a given Repository directory. The
        Repository must not have a value for
        ``git_remote_settings.url``.

        Returns:
            Callable[[~.QueryRepositoryDirectoryContentsRequest],
                    ~.QueryRepositoryDirectoryContentsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "query_repository_directory_contents" not in self._stubs:
            self._stubs[
                "query_repository_directory_contents"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/QueryRepositoryDirectoryContents",
                request_serializer=dataform.QueryRepositoryDirectoryContentsRequest.serialize,
                response_deserializer=dataform.QueryRepositoryDirectoryContentsResponse.deserialize,
            )
        return self._stubs["query_repository_directory_contents"]

    @property
    def fetch_repository_history(
        self,
    ) -> Callable[
        [dataform.FetchRepositoryHistoryRequest],
        dataform.FetchRepositoryHistoryResponse,
    ]:
        r"""Return a callable for the fetch repository history method over gRPC.

        Fetches a Repository's history of commits. The Repository must
        not have a value for ``git_remote_settings.url``.

        Returns:
            Callable[[~.FetchRepositoryHistoryRequest],
                    ~.FetchRepositoryHistoryResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_repository_history" not in self._stubs:
            self._stubs["fetch_repository_history"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/FetchRepositoryHistory",
                request_serializer=dataform.FetchRepositoryHistoryRequest.serialize,
                response_deserializer=dataform.FetchRepositoryHistoryResponse.deserialize,
            )
        return self._stubs["fetch_repository_history"]

    @property
    def compute_repository_access_token_status(
        self,
    ) -> Callable[
        [dataform.ComputeRepositoryAccessTokenStatusRequest],
        dataform.ComputeRepositoryAccessTokenStatusResponse,
    ]:
        r"""Return a callable for the compute repository access
        token status method over gRPC.

        Computes a Repository's Git access token status.

        Returns:
            Callable[[~.ComputeRepositoryAccessTokenStatusRequest],
                    ~.ComputeRepositoryAccessTokenStatusResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "compute_repository_access_token_status" not in self._stubs:
            self._stubs[
                "compute_repository_access_token_status"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/ComputeRepositoryAccessTokenStatus",
                request_serializer=dataform.ComputeRepositoryAccessTokenStatusRequest.serialize,
                response_deserializer=dataform.ComputeRepositoryAccessTokenStatusResponse.deserialize,
            )
        return self._stubs["compute_repository_access_token_status"]

    @property
    def fetch_remote_branches(
        self,
    ) -> Callable[
        [dataform.FetchRemoteBranchesRequest], dataform.FetchRemoteBranchesResponse
    ]:
        r"""Return a callable for the fetch remote branches method over gRPC.

        Fetches a Repository's remote branches.

        Returns:
            Callable[[~.FetchRemoteBranchesRequest],
                    ~.FetchRemoteBranchesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_remote_branches" not in self._stubs:
            self._stubs["fetch_remote_branches"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/FetchRemoteBranches",
                request_serializer=dataform.FetchRemoteBranchesRequest.serialize,
                response_deserializer=dataform.FetchRemoteBranchesResponse.deserialize,
            )
        return self._stubs["fetch_remote_branches"]

    @property
    def list_workspaces(
        self,
    ) -> Callable[[dataform.ListWorkspacesRequest], dataform.ListWorkspacesResponse]:
        r"""Return a callable for the list workspaces method over gRPC.

        Lists Workspaces in a given Repository.

        Returns:
            Callable[[~.ListWorkspacesRequest],
                    ~.ListWorkspacesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_workspaces" not in self._stubs:
            self._stubs["list_workspaces"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/ListWorkspaces",
                request_serializer=dataform.ListWorkspacesRequest.serialize,
                response_deserializer=dataform.ListWorkspacesResponse.deserialize,
            )
        return self._stubs["list_workspaces"]

    @property
    def get_workspace(
        self,
    ) -> Callable[[dataform.GetWorkspaceRequest], dataform.Workspace]:
        r"""Return a callable for the get workspace method over gRPC.

        Fetches a single Workspace.

        Returns:
            Callable[[~.GetWorkspaceRequest],
                    ~.Workspace]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_workspace" not in self._stubs:
            self._stubs["get_workspace"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/GetWorkspace",
                request_serializer=dataform.GetWorkspaceRequest.serialize,
                response_deserializer=dataform.Workspace.deserialize,
            )
        return self._stubs["get_workspace"]

    @property
    def create_workspace(
        self,
    ) -> Callable[[dataform.CreateWorkspaceRequest], dataform.Workspace]:
        r"""Return a callable for the create workspace method over gRPC.

        Creates a new Workspace in a given Repository.

        Returns:
            Callable[[~.CreateWorkspaceRequest],
                    ~.Workspace]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_workspace" not in self._stubs:
            self._stubs["create_workspace"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/CreateWorkspace",
                request_serializer=dataform.CreateWorkspaceRequest.serialize,
                response_deserializer=dataform.Workspace.deserialize,
            )
        return self._stubs["create_workspace"]

    @property
    def delete_workspace(
        self,
    ) -> Callable[[dataform.DeleteWorkspaceRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete workspace method over gRPC.

        Deletes a single Workspace.

        Returns:
            Callable[[~.DeleteWorkspaceRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_workspace" not in self._stubs:
            self._stubs["delete_workspace"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/DeleteWorkspace",
                request_serializer=dataform.DeleteWorkspaceRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_workspace"]

    @property
    def install_npm_packages(
        self,
    ) -> Callable[
        [dataform.InstallNpmPackagesRequest], dataform.InstallNpmPackagesResponse
    ]:
        r"""Return a callable for the install npm packages method over gRPC.

        Installs dependency NPM packages (inside a
        Workspace).

        Returns:
            Callable[[~.InstallNpmPackagesRequest],
                    ~.InstallNpmPackagesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "install_npm_packages" not in self._stubs:
            self._stubs["install_npm_packages"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/InstallNpmPackages",
                request_serializer=dataform.InstallNpmPackagesRequest.serialize,
                response_deserializer=dataform.InstallNpmPackagesResponse.deserialize,
            )
        return self._stubs["install_npm_packages"]

    @property
    def pull_git_commits(
        self,
    ) -> Callable[[dataform.PullGitCommitsRequest], empty_pb2.Empty]:
        r"""Return a callable for the pull git commits method over gRPC.

        Pulls Git commits from the Repository's remote into a
        Workspace.

        Returns:
            Callable[[~.PullGitCommitsRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "pull_git_commits" not in self._stubs:
            self._stubs["pull_git_commits"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/PullGitCommits",
                request_serializer=dataform.PullGitCommitsRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["pull_git_commits"]

    @property
    def push_git_commits(
        self,
    ) -> Callable[[dataform.PushGitCommitsRequest], empty_pb2.Empty]:
        r"""Return a callable for the push git commits method over gRPC.

        Pushes Git commits from a Workspace to the
        Repository's remote.

        Returns:
            Callable[[~.PushGitCommitsRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "push_git_commits" not in self._stubs:
            self._stubs["push_git_commits"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/PushGitCommits",
                request_serializer=dataform.PushGitCommitsRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["push_git_commits"]

    @property
    def fetch_file_git_statuses(
        self,
    ) -> Callable[
        [dataform.FetchFileGitStatusesRequest], dataform.FetchFileGitStatusesResponse
    ]:
        r"""Return a callable for the fetch file git statuses method over gRPC.

        Fetches Git statuses for the files in a Workspace.

        Returns:
            Callable[[~.FetchFileGitStatusesRequest],
                    ~.FetchFileGitStatusesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_file_git_statuses" not in self._stubs:
            self._stubs["fetch_file_git_statuses"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/FetchFileGitStatuses",
                request_serializer=dataform.FetchFileGitStatusesRequest.serialize,
                response_deserializer=dataform.FetchFileGitStatusesResponse.deserialize,
            )
        return self._stubs["fetch_file_git_statuses"]

    @property
    def fetch_git_ahead_behind(
        self,
    ) -> Callable[
        [dataform.FetchGitAheadBehindRequest], dataform.FetchGitAheadBehindResponse
    ]:
        r"""Return a callable for the fetch git ahead behind method over gRPC.

        Fetches Git ahead/behind against a remote branch.

        Returns:
            Callable[[~.FetchGitAheadBehindRequest],
                    ~.FetchGitAheadBehindResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_git_ahead_behind" not in self._stubs:
            self._stubs["fetch_git_ahead_behind"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/FetchGitAheadBehind",
                request_serializer=dataform.FetchGitAheadBehindRequest.serialize,
                response_deserializer=dataform.FetchGitAheadBehindResponse.deserialize,
            )
        return self._stubs["fetch_git_ahead_behind"]

    @property
    def commit_workspace_changes(
        self,
    ) -> Callable[[dataform.CommitWorkspaceChangesRequest], empty_pb2.Empty]:
        r"""Return a callable for the commit workspace changes method over gRPC.

        Applies a Git commit for uncommitted files in a
        Workspace.

        Returns:
            Callable[[~.CommitWorkspaceChangesRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "commit_workspace_changes" not in self._stubs:
            self._stubs["commit_workspace_changes"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/CommitWorkspaceChanges",
                request_serializer=dataform.CommitWorkspaceChangesRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["commit_workspace_changes"]

    @property
    def reset_workspace_changes(
        self,
    ) -> Callable[[dataform.ResetWorkspaceChangesRequest], empty_pb2.Empty]:
        r"""Return a callable for the reset workspace changes method over gRPC.

        Performs a Git reset for uncommitted files in a
        Workspace.

        Returns:
            Callable[[~.ResetWorkspaceChangesRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "reset_workspace_changes" not in self._stubs:
            self._stubs["reset_workspace_changes"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/ResetWorkspaceChanges",
                request_serializer=dataform.ResetWorkspaceChangesRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["reset_workspace_changes"]

    @property
    def fetch_file_diff(
        self,
    ) -> Callable[[dataform.FetchFileDiffRequest], dataform.FetchFileDiffResponse]:
        r"""Return a callable for the fetch file diff method over gRPC.

        Fetches Git diff for an uncommitted file in a
        Workspace.

        Returns:
            Callable[[~.FetchFileDiffRequest],
                    ~.FetchFileDiffResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_file_diff" not in self._stubs:
            self._stubs["fetch_file_diff"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/FetchFileDiff",
                request_serializer=dataform.FetchFileDiffRequest.serialize,
                response_deserializer=dataform.FetchFileDiffResponse.deserialize,
            )
        return self._stubs["fetch_file_diff"]

    @property
    def query_directory_contents(
        self,
    ) -> Callable[
        [dataform.QueryDirectoryContentsRequest],
        dataform.QueryDirectoryContentsResponse,
    ]:
        r"""Return a callable for the query directory contents method over gRPC.

        Returns the contents of a given Workspace directory.

        Returns:
            Callable[[~.QueryDirectoryContentsRequest],
                    ~.QueryDirectoryContentsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "query_directory_contents" not in self._stubs:
            self._stubs["query_directory_contents"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/QueryDirectoryContents",
                request_serializer=dataform.QueryDirectoryContentsRequest.serialize,
                response_deserializer=dataform.QueryDirectoryContentsResponse.deserialize,
            )
        return self._stubs["query_directory_contents"]

    @property
    def make_directory(
        self,
    ) -> Callable[[dataform.MakeDirectoryRequest], dataform.MakeDirectoryResponse]:
        r"""Return a callable for the make directory method over gRPC.

        Creates a directory inside a Workspace.

        Returns:
            Callable[[~.MakeDirectoryRequest],
                    ~.MakeDirectoryResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "make_directory" not in self._stubs:
            self._stubs["make_directory"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/MakeDirectory",
                request_serializer=dataform.MakeDirectoryRequest.serialize,
                response_deserializer=dataform.MakeDirectoryResponse.deserialize,
            )
        return self._stubs["make_directory"]

    @property
    def remove_directory(
        self,
    ) -> Callable[[dataform.RemoveDirectoryRequest], empty_pb2.Empty]:
        r"""Return a callable for the remove directory method over gRPC.

        Deletes a directory (inside a Workspace) and all of
        its contents.

        Returns:
            Callable[[~.RemoveDirectoryRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "remove_directory" not in self._stubs:
            self._stubs["remove_directory"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/RemoveDirectory",
                request_serializer=dataform.RemoveDirectoryRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["remove_directory"]

    @property
    def move_directory(
        self,
    ) -> Callable[[dataform.MoveDirectoryRequest], dataform.MoveDirectoryResponse]:
        r"""Return a callable for the move directory method over gRPC.

        Moves a directory (inside a Workspace), and all of
        its contents, to a new location.

        Returns:
            Callable[[~.MoveDirectoryRequest],
                    ~.MoveDirectoryResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "move_directory" not in self._stubs:
            self._stubs["move_directory"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/MoveDirectory",
                request_serializer=dataform.MoveDirectoryRequest.serialize,
                response_deserializer=dataform.MoveDirectoryResponse.deserialize,
            )
        return self._stubs["move_directory"]

    @property
    def read_file(
        self,
    ) -> Callable[[dataform.ReadFileRequest], dataform.ReadFileResponse]:
        r"""Return a callable for the read file method over gRPC.

        Returns the contents of a file (inside a Workspace).

        Returns:
            Callable[[~.ReadFileRequest],
                    ~.ReadFileResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "read_file" not in self._stubs:
            self._stubs["read_file"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/ReadFile",
                request_serializer=dataform.ReadFileRequest.serialize,
                response_deserializer=dataform.ReadFileResponse.deserialize,
            )
        return self._stubs["read_file"]

    @property
    def remove_file(self) -> Callable[[dataform.RemoveFileRequest], empty_pb2.Empty]:
        r"""Return a callable for the remove file method over gRPC.

        Deletes a file (inside a Workspace).

        Returns:
            Callable[[~.RemoveFileRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "remove_file" not in self._stubs:
            self._stubs["remove_file"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/RemoveFile",
                request_serializer=dataform.RemoveFileRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["remove_file"]

    @property
    def move_file(
        self,
    ) -> Callable[[dataform.MoveFileRequest], dataform.MoveFileResponse]:
        r"""Return a callable for the move file method over gRPC.

        Moves a file (inside a Workspace) to a new location.

        Returns:
            Callable[[~.MoveFileRequest],
                    ~.MoveFileResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "move_file" not in self._stubs:
            self._stubs["move_file"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/MoveFile",
                request_serializer=dataform.MoveFileRequest.serialize,
                response_deserializer=dataform.MoveFileResponse.deserialize,
            )
        return self._stubs["move_file"]

    @property
    def write_file(
        self,
    ) -> Callable[[dataform.WriteFileRequest], dataform.WriteFileResponse]:
        r"""Return a callable for the write file method over gRPC.

        Writes to a file (inside a Workspace).

        Returns:
            Callable[[~.WriteFileRequest],
                    ~.WriteFileResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "write_file" not in self._stubs:
            self._stubs["write_file"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/WriteFile",
                request_serializer=dataform.WriteFileRequest.serialize,
                response_deserializer=dataform.WriteFileResponse.deserialize,
            )
        return self._stubs["write_file"]

    @property
    def list_release_configs(
        self,
    ) -> Callable[
        [dataform.ListReleaseConfigsRequest], dataform.ListReleaseConfigsResponse
    ]:
        r"""Return a callable for the list release configs method over gRPC.

        Lists ReleaseConfigs in a given Repository.

        Returns:
            Callable[[~.ListReleaseConfigsRequest],
                    ~.ListReleaseConfigsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_release_configs" not in self._stubs:
            self._stubs["list_release_configs"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/ListReleaseConfigs",
                request_serializer=dataform.ListReleaseConfigsRequest.serialize,
                response_deserializer=dataform.ListReleaseConfigsResponse.deserialize,
            )
        return self._stubs["list_release_configs"]

    @property
    def get_release_config(
        self,
    ) -> Callable[[dataform.GetReleaseConfigRequest], dataform.ReleaseConfig]:
        r"""Return a callable for the get release config method over gRPC.

        Fetches a single ReleaseConfig.

        Returns:
            Callable[[~.GetReleaseConfigRequest],
                    ~.ReleaseConfig]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_release_config" not in self._stubs:
            self._stubs["get_release_config"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/GetReleaseConfig",
                request_serializer=dataform.GetReleaseConfigRequest.serialize,
                response_deserializer=dataform.ReleaseConfig.deserialize,
            )
        return self._stubs["get_release_config"]

    @property
    def create_release_config(
        self,
    ) -> Callable[[dataform.CreateReleaseConfigRequest], dataform.ReleaseConfig]:
        r"""Return a callable for the create release config method over gRPC.

        Creates a new ReleaseConfig in a given Repository.

        Returns:
            Callable[[~.CreateReleaseConfigRequest],
                    ~.ReleaseConfig]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_release_config" not in self._stubs:
            self._stubs["create_release_config"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/CreateReleaseConfig",
                request_serializer=dataform.CreateReleaseConfigRequest.serialize,
                response_deserializer=dataform.ReleaseConfig.deserialize,
            )
        return self._stubs["create_release_config"]

    @property
    def update_release_config(
        self,
    ) -> Callable[[dataform.UpdateReleaseConfigRequest], dataform.ReleaseConfig]:
        r"""Return a callable for the update release config method over gRPC.

        Updates a single ReleaseConfig.

        Returns:
            Callable[[~.UpdateReleaseConfigRequest],
                    ~.ReleaseConfig]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_release_config" not in self._stubs:
            self._stubs["update_release_config"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/UpdateReleaseConfig",
                request_serializer=dataform.UpdateReleaseConfigRequest.serialize,
                response_deserializer=dataform.ReleaseConfig.deserialize,
            )
        return self._stubs["update_release_config"]

    @property
    def delete_release_config(
        self,
    ) -> Callable[[dataform.DeleteReleaseConfigRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete release config method over gRPC.

        Deletes a single ReleaseConfig.

        Returns:
            Callable[[~.DeleteReleaseConfigRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_release_config" not in self._stubs:
            self._stubs["delete_release_config"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/DeleteReleaseConfig",
                request_serializer=dataform.DeleteReleaseConfigRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_release_config"]

    @property
    def list_compilation_results(
        self,
    ) -> Callable[
        [dataform.ListCompilationResultsRequest],
        dataform.ListCompilationResultsResponse,
    ]:
        r"""Return a callable for the list compilation results method over gRPC.

        Lists CompilationResults in a given Repository.

        Returns:
            Callable[[~.ListCompilationResultsRequest],
                    ~.ListCompilationResultsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_compilation_results" not in self._stubs:
            self._stubs["list_compilation_results"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/ListCompilationResults",
                request_serializer=dataform.ListCompilationResultsRequest.serialize,
                response_deserializer=dataform.ListCompilationResultsResponse.deserialize,
            )
        return self._stubs["list_compilation_results"]

    @property
    def get_compilation_result(
        self,
    ) -> Callable[[dataform.GetCompilationResultRequest], dataform.CompilationResult]:
        r"""Return a callable for the get compilation result method over gRPC.

        Fetches a single CompilationResult.

        Returns:
            Callable[[~.GetCompilationResultRequest],
                    ~.CompilationResult]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_compilation_result" not in self._stubs:
            self._stubs["get_compilation_result"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/GetCompilationResult",
                request_serializer=dataform.GetCompilationResultRequest.serialize,
                response_deserializer=dataform.CompilationResult.deserialize,
            )
        return self._stubs["get_compilation_result"]

    @property
    def create_compilation_result(
        self,
    ) -> Callable[
        [dataform.CreateCompilationResultRequest], dataform.CompilationResult
    ]:
        r"""Return a callable for the create compilation result method over gRPC.

        Creates a new CompilationResult in a given project
        and location.

        Returns:
            Callable[[~.CreateCompilationResultRequest],
                    ~.CompilationResult]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_compilation_result" not in self._stubs:
            self._stubs["create_compilation_result"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/CreateCompilationResult",
                request_serializer=dataform.CreateCompilationResultRequest.serialize,
                response_deserializer=dataform.CompilationResult.deserialize,
            )
        return self._stubs["create_compilation_result"]

    @property
    def query_compilation_result_actions(
        self,
    ) -> Callable[
        [dataform.QueryCompilationResultActionsRequest],
        dataform.QueryCompilationResultActionsResponse,
    ]:
        r"""Return a callable for the query compilation result
        actions method over gRPC.

        Returns CompilationResultActions in a given
        CompilationResult.

        Returns:
            Callable[[~.QueryCompilationResultActionsRequest],
                    ~.QueryCompilationResultActionsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "query_compilation_result_actions" not in self._stubs:
            self._stubs[
                "query_compilation_result_actions"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/QueryCompilationResultActions",
                request_serializer=dataform.QueryCompilationResultActionsRequest.serialize,
                response_deserializer=dataform.QueryCompilationResultActionsResponse.deserialize,
            )
        return self._stubs["query_compilation_result_actions"]

    @property
    def list_workflow_configs(
        self,
    ) -> Callable[
        [dataform.ListWorkflowConfigsRequest], dataform.ListWorkflowConfigsResponse
    ]:
        r"""Return a callable for the list workflow configs method over gRPC.

        Lists WorkflowConfigs in a given Repository.

        Returns:
            Callable[[~.ListWorkflowConfigsRequest],
                    ~.ListWorkflowConfigsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_workflow_configs" not in self._stubs:
            self._stubs["list_workflow_configs"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/ListWorkflowConfigs",
                request_serializer=dataform.ListWorkflowConfigsRequest.serialize,
                response_deserializer=dataform.ListWorkflowConfigsResponse.deserialize,
            )
        return self._stubs["list_workflow_configs"]

    @property
    def get_workflow_config(
        self,
    ) -> Callable[[dataform.GetWorkflowConfigRequest], dataform.WorkflowConfig]:
        r"""Return a callable for the get workflow config method over gRPC.

        Fetches a single WorkflowConfig.

        Returns:
            Callable[[~.GetWorkflowConfigRequest],
                    ~.WorkflowConfig]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_workflow_config" not in self._stubs:
            self._stubs["get_workflow_config"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/GetWorkflowConfig",
                request_serializer=dataform.GetWorkflowConfigRequest.serialize,
                response_deserializer=dataform.WorkflowConfig.deserialize,
            )
        return self._stubs["get_workflow_config"]

    @property
    def create_workflow_config(
        self,
    ) -> Callable[[dataform.CreateWorkflowConfigRequest], dataform.WorkflowConfig]:
        r"""Return a callable for the create workflow config method over gRPC.

        Creates a new WorkflowConfig in a given Repository.

        Returns:
            Callable[[~.CreateWorkflowConfigRequest],
                    ~.WorkflowConfig]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_workflow_config" not in self._stubs:
            self._stubs["create_workflow_config"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/CreateWorkflowConfig",
                request_serializer=dataform.CreateWorkflowConfigRequest.serialize,
                response_deserializer=dataform.WorkflowConfig.deserialize,
            )
        return self._stubs["create_workflow_config"]

    @property
    def update_workflow_config(
        self,
    ) -> Callable[[dataform.UpdateWorkflowConfigRequest], dataform.WorkflowConfig]:
        r"""Return a callable for the update workflow config method over gRPC.

        Updates a single WorkflowConfig.

        Returns:
            Callable[[~.UpdateWorkflowConfigRequest],
                    ~.WorkflowConfig]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_workflow_config" not in self._stubs:
            self._stubs["update_workflow_config"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/UpdateWorkflowConfig",
                request_serializer=dataform.UpdateWorkflowConfigRequest.serialize,
                response_deserializer=dataform.WorkflowConfig.deserialize,
            )
        return self._stubs["update_workflow_config"]

    @property
    def delete_workflow_config(
        self,
    ) -> Callable[[dataform.DeleteWorkflowConfigRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete workflow config method over gRPC.

        Deletes a single WorkflowConfig.

        Returns:
            Callable[[~.DeleteWorkflowConfigRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_workflow_config" not in self._stubs:
            self._stubs["delete_workflow_config"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/DeleteWorkflowConfig",
                request_serializer=dataform.DeleteWorkflowConfigRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_workflow_config"]

    @property
    def list_workflow_invocations(
        self,
    ) -> Callable[
        [dataform.ListWorkflowInvocationsRequest],
        dataform.ListWorkflowInvocationsResponse,
    ]:
        r"""Return a callable for the list workflow invocations method over gRPC.

        Lists WorkflowInvocations in a given Repository.

        Returns:
            Callable[[~.ListWorkflowInvocationsRequest],
                    ~.ListWorkflowInvocationsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_workflow_invocations" not in self._stubs:
            self._stubs["list_workflow_invocations"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/ListWorkflowInvocations",
                request_serializer=dataform.ListWorkflowInvocationsRequest.serialize,
                response_deserializer=dataform.ListWorkflowInvocationsResponse.deserialize,
            )
        return self._stubs["list_workflow_invocations"]

    @property
    def get_workflow_invocation(
        self,
    ) -> Callable[[dataform.GetWorkflowInvocationRequest], dataform.WorkflowInvocation]:
        r"""Return a callable for the get workflow invocation method over gRPC.

        Fetches a single WorkflowInvocation.

        Returns:
            Callable[[~.GetWorkflowInvocationRequest],
                    ~.WorkflowInvocation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_workflow_invocation" not in self._stubs:
            self._stubs["get_workflow_invocation"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/GetWorkflowInvocation",
                request_serializer=dataform.GetWorkflowInvocationRequest.serialize,
                response_deserializer=dataform.WorkflowInvocation.deserialize,
            )
        return self._stubs["get_workflow_invocation"]

    @property
    def create_workflow_invocation(
        self,
    ) -> Callable[
        [dataform.CreateWorkflowInvocationRequest], dataform.WorkflowInvocation
    ]:
        r"""Return a callable for the create workflow invocation method over gRPC.

        Creates a new WorkflowInvocation in a given
        Repository.

        Returns:
            Callable[[~.CreateWorkflowInvocationRequest],
                    ~.WorkflowInvocation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_workflow_invocation" not in self._stubs:
            self._stubs["create_workflow_invocation"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/CreateWorkflowInvocation",
                request_serializer=dataform.CreateWorkflowInvocationRequest.serialize,
                response_deserializer=dataform.WorkflowInvocation.deserialize,
            )
        return self._stubs["create_workflow_invocation"]

    @property
    def delete_workflow_invocation(
        self,
    ) -> Callable[[dataform.DeleteWorkflowInvocationRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete workflow invocation method over gRPC.

        Deletes a single WorkflowInvocation.

        Returns:
            Callable[[~.DeleteWorkflowInvocationRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_workflow_invocation" not in self._stubs:
            self._stubs["delete_workflow_invocation"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/DeleteWorkflowInvocation",
                request_serializer=dataform.DeleteWorkflowInvocationRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_workflow_invocation"]

    @property
    def cancel_workflow_invocation(
        self,
    ) -> Callable[[dataform.CancelWorkflowInvocationRequest], empty_pb2.Empty]:
        r"""Return a callable for the cancel workflow invocation method over gRPC.

        Requests cancellation of a running
        WorkflowInvocation.

        Returns:
            Callable[[~.CancelWorkflowInvocationRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_workflow_invocation" not in self._stubs:
            self._stubs["cancel_workflow_invocation"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/CancelWorkflowInvocation",
                request_serializer=dataform.CancelWorkflowInvocationRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["cancel_workflow_invocation"]

    @property
    def query_workflow_invocation_actions(
        self,
    ) -> Callable[
        [dataform.QueryWorkflowInvocationActionsRequest],
        dataform.QueryWorkflowInvocationActionsResponse,
    ]:
        r"""Return a callable for the query workflow invocation
        actions method over gRPC.

        Returns WorkflowInvocationActions in a given
        WorkflowInvocation.

        Returns:
            Callable[[~.QueryWorkflowInvocationActionsRequest],
                    ~.QueryWorkflowInvocationActionsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "query_workflow_invocation_actions" not in self._stubs:
            self._stubs[
                "query_workflow_invocation_actions"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.dataform.v1beta1.Dataform/QueryWorkflowInvocationActions",
                request_serializer=dataform.QueryWorkflowInvocationActionsRequest.serialize,
                response_deserializer=dataform.QueryWorkflowInvocationActionsResponse.deserialize,
            )
        return self._stubs["query_workflow_invocation_actions"]

    def close(self):
        self.grpc_channel.close()

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

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("DataformGrpcTransport",)
