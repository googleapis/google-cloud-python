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
from google.protobuf import empty_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.artifactregistry_v1.types import apt_artifact, artifact, file, package
from google.cloud.artifactregistry_v1.types import vpcsc_config as gda_vpcsc_config
from google.cloud.artifactregistry_v1.types import repository
from google.cloud.artifactregistry_v1.types import repository as gda_repository
from google.cloud.artifactregistry_v1.types import settings
from google.cloud.artifactregistry_v1.types import tag
from google.cloud.artifactregistry_v1.types import tag as gda_tag
from google.cloud.artifactregistry_v1.types import version
from google.cloud.artifactregistry_v1.types import vpcsc_config
from google.cloud.artifactregistry_v1.types import yum_artifact

from .base import DEFAULT_CLIENT_INFO, ArtifactRegistryTransport
from .grpc import ArtifactRegistryGrpcTransport


class ArtifactRegistryGrpcAsyncIOTransport(ArtifactRegistryTransport):
    """gRPC AsyncIO backend transport for ArtifactRegistry.

    The Artifact Registry API service.

    Artifact Registry is an artifact management system for storing
    artifacts from different package management systems.

    The resources managed by this API are:

    -  Repositories, which group packages and their data.
    -  Packages, which group versions and their tags.
    -  Versions, which are specific forms of a package.
    -  Tags, which represent alternative names for versions.
    -  Files, which contain content and are optionally associated with a
       Package or Version.

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
        host: str = "artifactregistry.googleapis.com",
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
        host: str = "artifactregistry.googleapis.com",
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
    def list_docker_images(
        self,
    ) -> Callable[
        [artifact.ListDockerImagesRequest], Awaitable[artifact.ListDockerImagesResponse]
    ]:
        r"""Return a callable for the list docker images method over gRPC.

        Lists docker images.

        Returns:
            Callable[[~.ListDockerImagesRequest],
                    Awaitable[~.ListDockerImagesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_docker_images" not in self._stubs:
            self._stubs["list_docker_images"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/ListDockerImages",
                request_serializer=artifact.ListDockerImagesRequest.serialize,
                response_deserializer=artifact.ListDockerImagesResponse.deserialize,
            )
        return self._stubs["list_docker_images"]

    @property
    def get_docker_image(
        self,
    ) -> Callable[[artifact.GetDockerImageRequest], Awaitable[artifact.DockerImage]]:
        r"""Return a callable for the get docker image method over gRPC.

        Gets a docker image.

        Returns:
            Callable[[~.GetDockerImageRequest],
                    Awaitable[~.DockerImage]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_docker_image" not in self._stubs:
            self._stubs["get_docker_image"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/GetDockerImage",
                request_serializer=artifact.GetDockerImageRequest.serialize,
                response_deserializer=artifact.DockerImage.deserialize,
            )
        return self._stubs["get_docker_image"]

    @property
    def list_maven_artifacts(
        self,
    ) -> Callable[
        [artifact.ListMavenArtifactsRequest],
        Awaitable[artifact.ListMavenArtifactsResponse],
    ]:
        r"""Return a callable for the list maven artifacts method over gRPC.

        Lists maven artifacts.

        Returns:
            Callable[[~.ListMavenArtifactsRequest],
                    Awaitable[~.ListMavenArtifactsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_maven_artifacts" not in self._stubs:
            self._stubs["list_maven_artifacts"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/ListMavenArtifacts",
                request_serializer=artifact.ListMavenArtifactsRequest.serialize,
                response_deserializer=artifact.ListMavenArtifactsResponse.deserialize,
            )
        return self._stubs["list_maven_artifacts"]

    @property
    def get_maven_artifact(
        self,
    ) -> Callable[
        [artifact.GetMavenArtifactRequest], Awaitable[artifact.MavenArtifact]
    ]:
        r"""Return a callable for the get maven artifact method over gRPC.

        Gets a maven artifact.

        Returns:
            Callable[[~.GetMavenArtifactRequest],
                    Awaitable[~.MavenArtifact]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_maven_artifact" not in self._stubs:
            self._stubs["get_maven_artifact"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/GetMavenArtifact",
                request_serializer=artifact.GetMavenArtifactRequest.serialize,
                response_deserializer=artifact.MavenArtifact.deserialize,
            )
        return self._stubs["get_maven_artifact"]

    @property
    def list_npm_packages(
        self,
    ) -> Callable[
        [artifact.ListNpmPackagesRequest], Awaitable[artifact.ListNpmPackagesResponse]
    ]:
        r"""Return a callable for the list npm packages method over gRPC.

        Lists npm packages.

        Returns:
            Callable[[~.ListNpmPackagesRequest],
                    Awaitable[~.ListNpmPackagesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_npm_packages" not in self._stubs:
            self._stubs["list_npm_packages"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/ListNpmPackages",
                request_serializer=artifact.ListNpmPackagesRequest.serialize,
                response_deserializer=artifact.ListNpmPackagesResponse.deserialize,
            )
        return self._stubs["list_npm_packages"]

    @property
    def get_npm_package(
        self,
    ) -> Callable[[artifact.GetNpmPackageRequest], Awaitable[artifact.NpmPackage]]:
        r"""Return a callable for the get npm package method over gRPC.

        Gets a npm package.

        Returns:
            Callable[[~.GetNpmPackageRequest],
                    Awaitable[~.NpmPackage]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_npm_package" not in self._stubs:
            self._stubs["get_npm_package"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/GetNpmPackage",
                request_serializer=artifact.GetNpmPackageRequest.serialize,
                response_deserializer=artifact.NpmPackage.deserialize,
            )
        return self._stubs["get_npm_package"]

    @property
    def list_python_packages(
        self,
    ) -> Callable[
        [artifact.ListPythonPackagesRequest],
        Awaitable[artifact.ListPythonPackagesResponse],
    ]:
        r"""Return a callable for the list python packages method over gRPC.

        Lists python packages.

        Returns:
            Callable[[~.ListPythonPackagesRequest],
                    Awaitable[~.ListPythonPackagesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_python_packages" not in self._stubs:
            self._stubs["list_python_packages"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/ListPythonPackages",
                request_serializer=artifact.ListPythonPackagesRequest.serialize,
                response_deserializer=artifact.ListPythonPackagesResponse.deserialize,
            )
        return self._stubs["list_python_packages"]

    @property
    def get_python_package(
        self,
    ) -> Callable[
        [artifact.GetPythonPackageRequest], Awaitable[artifact.PythonPackage]
    ]:
        r"""Return a callable for the get python package method over gRPC.

        Gets a python package.

        Returns:
            Callable[[~.GetPythonPackageRequest],
                    Awaitable[~.PythonPackage]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_python_package" not in self._stubs:
            self._stubs["get_python_package"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/GetPythonPackage",
                request_serializer=artifact.GetPythonPackageRequest.serialize,
                response_deserializer=artifact.PythonPackage.deserialize,
            )
        return self._stubs["get_python_package"]

    @property
    def import_apt_artifacts(
        self,
    ) -> Callable[
        [apt_artifact.ImportAptArtifactsRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the import apt artifacts method over gRPC.

        Imports Apt artifacts. The returned Operation will
        complete once the resources are imported. Package,
        Version, and File resources are created based on the
        imported artifacts. Imported artifacts that conflict
        with existing resources are ignored.

        Returns:
            Callable[[~.ImportAptArtifactsRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "import_apt_artifacts" not in self._stubs:
            self._stubs["import_apt_artifacts"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/ImportAptArtifacts",
                request_serializer=apt_artifact.ImportAptArtifactsRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["import_apt_artifacts"]

    @property
    def import_yum_artifacts(
        self,
    ) -> Callable[
        [yum_artifact.ImportYumArtifactsRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the import yum artifacts method over gRPC.

        Imports Yum (RPM) artifacts. The returned Operation
        will complete once the resources are imported. Package,
        Version, and File resources are created based on the
        imported artifacts. Imported artifacts that conflict
        with existing resources are ignored.

        Returns:
            Callable[[~.ImportYumArtifactsRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "import_yum_artifacts" not in self._stubs:
            self._stubs["import_yum_artifacts"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/ImportYumArtifacts",
                request_serializer=yum_artifact.ImportYumArtifactsRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["import_yum_artifacts"]

    @property
    def list_repositories(
        self,
    ) -> Callable[
        [repository.ListRepositoriesRequest],
        Awaitable[repository.ListRepositoriesResponse],
    ]:
        r"""Return a callable for the list repositories method over gRPC.

        Lists repositories.

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
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/ListRepositories",
                request_serializer=repository.ListRepositoriesRequest.serialize,
                response_deserializer=repository.ListRepositoriesResponse.deserialize,
            )
        return self._stubs["list_repositories"]

    @property
    def get_repository(
        self,
    ) -> Callable[[repository.GetRepositoryRequest], Awaitable[repository.Repository]]:
        r"""Return a callable for the get repository method over gRPC.

        Gets a repository.

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
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/GetRepository",
                request_serializer=repository.GetRepositoryRequest.serialize,
                response_deserializer=repository.Repository.deserialize,
            )
        return self._stubs["get_repository"]

    @property
    def create_repository(
        self,
    ) -> Callable[
        [gda_repository.CreateRepositoryRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create repository method over gRPC.

        Creates a repository. The returned Operation will
        finish once the repository has been created. Its
        response will be the created Repository.

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
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/CreateRepository",
                request_serializer=gda_repository.CreateRepositoryRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_repository"]

    @property
    def update_repository(
        self,
    ) -> Callable[
        [gda_repository.UpdateRepositoryRequest], Awaitable[gda_repository.Repository]
    ]:
        r"""Return a callable for the update repository method over gRPC.

        Updates a repository.

        Returns:
            Callable[[~.UpdateRepositoryRequest],
                    Awaitable[~.Repository]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_repository" not in self._stubs:
            self._stubs["update_repository"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/UpdateRepository",
                request_serializer=gda_repository.UpdateRepositoryRequest.serialize,
                response_deserializer=gda_repository.Repository.deserialize,
            )
        return self._stubs["update_repository"]

    @property
    def delete_repository(
        self,
    ) -> Callable[
        [repository.DeleteRepositoryRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete repository method over gRPC.

        Deletes a repository and all of its contents. The
        returned Operation will finish once the repository has
        been deleted. It will not have any Operation metadata
        and will return a google.protobuf.Empty response.

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
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/DeleteRepository",
                request_serializer=repository.DeleteRepositoryRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_repository"]

    @property
    def list_packages(
        self,
    ) -> Callable[
        [package.ListPackagesRequest], Awaitable[package.ListPackagesResponse]
    ]:
        r"""Return a callable for the list packages method over gRPC.

        Lists packages.

        Returns:
            Callable[[~.ListPackagesRequest],
                    Awaitable[~.ListPackagesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_packages" not in self._stubs:
            self._stubs["list_packages"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/ListPackages",
                request_serializer=package.ListPackagesRequest.serialize,
                response_deserializer=package.ListPackagesResponse.deserialize,
            )
        return self._stubs["list_packages"]

    @property
    def get_package(
        self,
    ) -> Callable[[package.GetPackageRequest], Awaitable[package.Package]]:
        r"""Return a callable for the get package method over gRPC.

        Gets a package.

        Returns:
            Callable[[~.GetPackageRequest],
                    Awaitable[~.Package]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_package" not in self._stubs:
            self._stubs["get_package"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/GetPackage",
                request_serializer=package.GetPackageRequest.serialize,
                response_deserializer=package.Package.deserialize,
            )
        return self._stubs["get_package"]

    @property
    def delete_package(
        self,
    ) -> Callable[[package.DeletePackageRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the delete package method over gRPC.

        Deletes a package and all of its versions and tags.
        The returned operation will complete once the package
        has been deleted.

        Returns:
            Callable[[~.DeletePackageRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_package" not in self._stubs:
            self._stubs["delete_package"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/DeletePackage",
                request_serializer=package.DeletePackageRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_package"]

    @property
    def list_versions(
        self,
    ) -> Callable[
        [version.ListVersionsRequest], Awaitable[version.ListVersionsResponse]
    ]:
        r"""Return a callable for the list versions method over gRPC.

        Lists versions.

        Returns:
            Callable[[~.ListVersionsRequest],
                    Awaitable[~.ListVersionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_versions" not in self._stubs:
            self._stubs["list_versions"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/ListVersions",
                request_serializer=version.ListVersionsRequest.serialize,
                response_deserializer=version.ListVersionsResponse.deserialize,
            )
        return self._stubs["list_versions"]

    @property
    def get_version(
        self,
    ) -> Callable[[version.GetVersionRequest], Awaitable[version.Version]]:
        r"""Return a callable for the get version method over gRPC.

        Gets a version

        Returns:
            Callable[[~.GetVersionRequest],
                    Awaitable[~.Version]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_version" not in self._stubs:
            self._stubs["get_version"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/GetVersion",
                request_serializer=version.GetVersionRequest.serialize,
                response_deserializer=version.Version.deserialize,
            )
        return self._stubs["get_version"]

    @property
    def delete_version(
        self,
    ) -> Callable[[version.DeleteVersionRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the delete version method over gRPC.

        Deletes a version and all of its content. The
        returned operation will complete once the version has
        been deleted.

        Returns:
            Callable[[~.DeleteVersionRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_version" not in self._stubs:
            self._stubs["delete_version"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/DeleteVersion",
                request_serializer=version.DeleteVersionRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_version"]

    @property
    def list_files(
        self,
    ) -> Callable[[file.ListFilesRequest], Awaitable[file.ListFilesResponse]]:
        r"""Return a callable for the list files method over gRPC.

        Lists files.

        Returns:
            Callable[[~.ListFilesRequest],
                    Awaitable[~.ListFilesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_files" not in self._stubs:
            self._stubs["list_files"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/ListFiles",
                request_serializer=file.ListFilesRequest.serialize,
                response_deserializer=file.ListFilesResponse.deserialize,
            )
        return self._stubs["list_files"]

    @property
    def get_file(self) -> Callable[[file.GetFileRequest], Awaitable[file.File]]:
        r"""Return a callable for the get file method over gRPC.

        Gets a file.

        Returns:
            Callable[[~.GetFileRequest],
                    Awaitable[~.File]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_file" not in self._stubs:
            self._stubs["get_file"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/GetFile",
                request_serializer=file.GetFileRequest.serialize,
                response_deserializer=file.File.deserialize,
            )
        return self._stubs["get_file"]

    @property
    def list_tags(
        self,
    ) -> Callable[[tag.ListTagsRequest], Awaitable[tag.ListTagsResponse]]:
        r"""Return a callable for the list tags method over gRPC.

        Lists tags.

        Returns:
            Callable[[~.ListTagsRequest],
                    Awaitable[~.ListTagsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_tags" not in self._stubs:
            self._stubs["list_tags"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/ListTags",
                request_serializer=tag.ListTagsRequest.serialize,
                response_deserializer=tag.ListTagsResponse.deserialize,
            )
        return self._stubs["list_tags"]

    @property
    def get_tag(self) -> Callable[[tag.GetTagRequest], Awaitable[tag.Tag]]:
        r"""Return a callable for the get tag method over gRPC.

        Gets a tag.

        Returns:
            Callable[[~.GetTagRequest],
                    Awaitable[~.Tag]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_tag" not in self._stubs:
            self._stubs["get_tag"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/GetTag",
                request_serializer=tag.GetTagRequest.serialize,
                response_deserializer=tag.Tag.deserialize,
            )
        return self._stubs["get_tag"]

    @property
    def create_tag(
        self,
    ) -> Callable[[gda_tag.CreateTagRequest], Awaitable[gda_tag.Tag]]:
        r"""Return a callable for the create tag method over gRPC.

        Creates a tag.

        Returns:
            Callable[[~.CreateTagRequest],
                    Awaitable[~.Tag]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_tag" not in self._stubs:
            self._stubs["create_tag"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/CreateTag",
                request_serializer=gda_tag.CreateTagRequest.serialize,
                response_deserializer=gda_tag.Tag.deserialize,
            )
        return self._stubs["create_tag"]

    @property
    def update_tag(
        self,
    ) -> Callable[[gda_tag.UpdateTagRequest], Awaitable[gda_tag.Tag]]:
        r"""Return a callable for the update tag method over gRPC.

        Updates a tag.

        Returns:
            Callable[[~.UpdateTagRequest],
                    Awaitable[~.Tag]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_tag" not in self._stubs:
            self._stubs["update_tag"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/UpdateTag",
                request_serializer=gda_tag.UpdateTagRequest.serialize,
                response_deserializer=gda_tag.Tag.deserialize,
            )
        return self._stubs["update_tag"]

    @property
    def delete_tag(
        self,
    ) -> Callable[[tag.DeleteTagRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete tag method over gRPC.

        Deletes a tag.

        Returns:
            Callable[[~.DeleteTagRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_tag" not in self._stubs:
            self._stubs["delete_tag"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/DeleteTag",
                request_serializer=tag.DeleteTagRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_tag"]

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], Awaitable[policy_pb2.Policy]]:
        r"""Return a callable for the set iam policy method over gRPC.

        Updates the IAM policy for a given resource.

        Returns:
            Callable[[~.SetIamPolicyRequest],
                    Awaitable[~.Policy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_iam_policy" not in self._stubs:
            self._stubs["set_iam_policy"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/SetIamPolicy",
                request_serializer=iam_policy_pb2.SetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["set_iam_policy"]

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], Awaitable[policy_pb2.Policy]]:
        r"""Return a callable for the get iam policy method over gRPC.

        Gets the IAM policy for a given resource.

        Returns:
            Callable[[~.GetIamPolicyRequest],
                    Awaitable[~.Policy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_iam_policy" not in self._stubs:
            self._stubs["get_iam_policy"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/GetIamPolicy",
                request_serializer=iam_policy_pb2.GetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["get_iam_policy"]

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        Awaitable[iam_policy_pb2.TestIamPermissionsResponse],
    ]:
        r"""Return a callable for the test iam permissions method over gRPC.

        Tests if the caller has a list of permissions on a
        resource.

        Returns:
            Callable[[~.TestIamPermissionsRequest],
                    Awaitable[~.TestIamPermissionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "test_iam_permissions" not in self._stubs:
            self._stubs["test_iam_permissions"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/TestIamPermissions",
                request_serializer=iam_policy_pb2.TestIamPermissionsRequest.SerializeToString,
                response_deserializer=iam_policy_pb2.TestIamPermissionsResponse.FromString,
            )
        return self._stubs["test_iam_permissions"]

    @property
    def get_project_settings(
        self,
    ) -> Callable[
        [settings.GetProjectSettingsRequest], Awaitable[settings.ProjectSettings]
    ]:
        r"""Return a callable for the get project settings method over gRPC.

        Retrieves the Settings for the Project.

        Returns:
            Callable[[~.GetProjectSettingsRequest],
                    Awaitable[~.ProjectSettings]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_project_settings" not in self._stubs:
            self._stubs["get_project_settings"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/GetProjectSettings",
                request_serializer=settings.GetProjectSettingsRequest.serialize,
                response_deserializer=settings.ProjectSettings.deserialize,
            )
        return self._stubs["get_project_settings"]

    @property
    def update_project_settings(
        self,
    ) -> Callable[
        [settings.UpdateProjectSettingsRequest], Awaitable[settings.ProjectSettings]
    ]:
        r"""Return a callable for the update project settings method over gRPC.

        Updates the Settings for the Project.

        Returns:
            Callable[[~.UpdateProjectSettingsRequest],
                    Awaitable[~.ProjectSettings]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_project_settings" not in self._stubs:
            self._stubs["update_project_settings"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/UpdateProjectSettings",
                request_serializer=settings.UpdateProjectSettingsRequest.serialize,
                response_deserializer=settings.ProjectSettings.deserialize,
            )
        return self._stubs["update_project_settings"]

    @property
    def get_vpcsc_config(
        self,
    ) -> Callable[
        [vpcsc_config.GetVPCSCConfigRequest], Awaitable[vpcsc_config.VPCSCConfig]
    ]:
        r"""Return a callable for the get vpcsc config method over gRPC.

        Retrieves the VPCSC Config for the Project.

        Returns:
            Callable[[~.GetVPCSCConfigRequest],
                    Awaitable[~.VPCSCConfig]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_vpcsc_config" not in self._stubs:
            self._stubs["get_vpcsc_config"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/GetVPCSCConfig",
                request_serializer=vpcsc_config.GetVPCSCConfigRequest.serialize,
                response_deserializer=vpcsc_config.VPCSCConfig.deserialize,
            )
        return self._stubs["get_vpcsc_config"]

    @property
    def update_vpcsc_config(
        self,
    ) -> Callable[
        [gda_vpcsc_config.UpdateVPCSCConfigRequest],
        Awaitable[gda_vpcsc_config.VPCSCConfig],
    ]:
        r"""Return a callable for the update vpcsc config method over gRPC.

        Updates the VPCSC Config for the Project.

        Returns:
            Callable[[~.UpdateVPCSCConfigRequest],
                    Awaitable[~.VPCSCConfig]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_vpcsc_config" not in self._stubs:
            self._stubs["update_vpcsc_config"] = self.grpc_channel.unary_unary(
                "/google.devtools.artifactregistry.v1.ArtifactRegistry/UpdateVPCSCConfig",
                request_serializer=gda_vpcsc_config.UpdateVPCSCConfigRequest.serialize,
                response_deserializer=gda_vpcsc_config.VPCSCConfig.deserialize,
            )
        return self._stubs["update_vpcsc_config"]

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


__all__ = ("ArtifactRegistryGrpcAsyncIOTransport",)
