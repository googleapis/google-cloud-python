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
import json
import logging as std_logging
import pickle
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
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore
import proto  # type: ignore

from google.cloud.artifactregistry_v1beta2.types import apt_artifact, file, package
from google.cloud.artifactregistry_v1beta2.types import repository as gda_repository
from google.cloud.artifactregistry_v1beta2.types import repository
from google.cloud.artifactregistry_v1beta2.types import settings
from google.cloud.artifactregistry_v1beta2.types import tag
from google.cloud.artifactregistry_v1beta2.types import tag as gda_tag
from google.cloud.artifactregistry_v1beta2.types import version, yum_artifact

from .base import DEFAULT_CLIENT_INFO, ArtifactRegistryTransport
from .grpc import ArtifactRegistryGrpcTransport

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class _LoggingClientAIOInterceptor(
    grpc.aio.UnaryUnaryClientInterceptor
):  # pragma: NO COVER
    async def intercept_unary_unary(self, continuation, client_call_details, request):
        logging_enabled = CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
            std_logging.DEBUG
        )
        if logging_enabled:  # pragma: NO COVER
            request_metadata = client_call_details.metadata
            if isinstance(request, proto.Message):
                request_payload = type(request).to_json(request)
            elif isinstance(request, google.protobuf.message.Message):
                request_payload = MessageToJson(request)
            else:
                request_payload = f"{type(request).__name__}: {pickle.dumps(request)}"

            request_metadata = {
                key: value.decode("utf-8") if isinstance(value, bytes) else value
                for key, value in request_metadata
            }
            grpc_request = {
                "payload": request_payload,
                "requestMethod": "grpc",
                "metadata": dict(request_metadata),
            }
            _LOGGER.debug(
                f"Sending request for {client_call_details.method}",
                extra={
                    "serviceName": "google.devtools.artifactregistry.v1beta2.ArtifactRegistry",
                    "rpcName": str(client_call_details.method),
                    "request": grpc_request,
                    "metadata": grpc_request["metadata"],
                },
            )
        response = await continuation(client_call_details, request)
        if logging_enabled:  # pragma: NO COVER
            response_metadata = await response.trailing_metadata()
            # Convert gRPC metadata `<class 'grpc.aio._metadata.Metadata'>` to list of tuples
            metadata = (
                dict([(k, str(v)) for k, v in response_metadata])
                if response_metadata
                else None
            )
            result = await response
            if isinstance(result, proto.Message):
                response_payload = type(result).to_json(result)
            elif isinstance(result, google.protobuf.message.Message):
                response_payload = MessageToJson(result)
            else:
                response_payload = f"{type(result).__name__}: {pickle.dumps(result)}"
            grpc_response = {
                "payload": response_payload,
                "metadata": metadata,
                "status": "OK",
            }
            _LOGGER.debug(
                f"Received response to rpc {client_call_details.method}.",
                extra={
                    "serviceName": "google.devtools.artifactregistry.v1beta2.ArtifactRegistry",
                    "rpcName": str(client_call_details.method),
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


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
                 The hostname to connect to (default: 'artifactregistry.googleapis.com').
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

        self._interceptor = _LoggingClientAIOInterceptor()
        self._grpc_channel._unary_unary_interceptors.append(self._interceptor)
        self._logged_channel = self._grpc_channel
        self._wrap_with_kind = (
            "kind" in inspect.signature(gapic_v1.method_async.wrap_method).parameters
        )
        # Wrap messages. This must be done after self._logged_channel exists
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
                self._logged_channel
            )

        # Return the client from cache.
        return self._operations_client

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
            self._stubs["import_apt_artifacts"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/ImportAptArtifacts",
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
            self._stubs["import_yum_artifacts"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/ImportYumArtifacts",
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
            self._stubs["list_repositories"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/ListRepositories",
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
            self._stubs["get_repository"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/GetRepository",
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
            self._stubs["create_repository"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/CreateRepository",
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
            self._stubs["update_repository"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/UpdateRepository",
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
            self._stubs["delete_repository"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/DeleteRepository",
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
            self._stubs["list_packages"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/ListPackages",
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
            self._stubs["get_package"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/GetPackage",
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
            self._stubs["delete_package"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/DeletePackage",
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
            self._stubs["list_versions"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/ListVersions",
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
            self._stubs["get_version"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/GetVersion",
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
            self._stubs["delete_version"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/DeleteVersion",
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
            self._stubs["list_files"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/ListFiles",
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
            self._stubs["get_file"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/GetFile",
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
            self._stubs["list_tags"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/ListTags",
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
            self._stubs["get_tag"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/GetTag",
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
            self._stubs["create_tag"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/CreateTag",
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
            self._stubs["update_tag"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/UpdateTag",
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
            self._stubs["delete_tag"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/DeleteTag",
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
            self._stubs["set_iam_policy"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/SetIamPolicy",
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
            self._stubs["get_iam_policy"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/GetIamPolicy",
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
            self._stubs["test_iam_permissions"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/TestIamPermissions",
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
            self._stubs["get_project_settings"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/GetProjectSettings",
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
            self._stubs["update_project_settings"] = self._logged_channel.unary_unary(
                "/google.devtools.artifactregistry.v1beta2.ArtifactRegistry/UpdateProjectSettings",
                request_serializer=settings.UpdateProjectSettingsRequest.serialize,
                response_deserializer=settings.ProjectSettings.deserialize,
            )
        return self._stubs["update_project_settings"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.import_apt_artifacts: self._wrap_method(
                self.import_apt_artifacts,
                default_timeout=None,
                client_info=client_info,
            ),
            self.import_yum_artifacts: self._wrap_method(
                self.import_yum_artifacts,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_repositories: self._wrap_method(
                self.list_repositories,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_repository: self._wrap_method(
                self.get_repository,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_repository: self._wrap_method(
                self.create_repository,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.update_repository: self._wrap_method(
                self.update_repository,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_repository: self._wrap_method(
                self.delete_repository,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_packages: self._wrap_method(
                self.list_packages,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_package: self._wrap_method(
                self.get_package,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_package: self._wrap_method(
                self.delete_package,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_versions: self._wrap_method(
                self.list_versions,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_version: self._wrap_method(
                self.get_version,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_version: self._wrap_method(
                self.delete_version,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_files: self._wrap_method(
                self.list_files,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_file: self._wrap_method(
                self.get_file,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_tags: self._wrap_method(
                self.list_tags,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_tag: self._wrap_method(
                self.get_tag,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_tag: self._wrap_method(
                self.create_tag,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.update_tag: self._wrap_method(
                self.update_tag,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_tag: self._wrap_method(
                self.delete_tag,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.set_iam_policy: self._wrap_method(
                self.set_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_iam_policy: self._wrap_method(
                self.get_iam_policy,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.test_iam_permissions: self._wrap_method(
                self.test_iam_permissions,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_project_settings: self._wrap_method(
                self.get_project_settings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_project_settings: self._wrap_method(
                self.update_project_settings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_location: self._wrap_method(
                self.get_location,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_locations: self._wrap_method(
                self.list_locations,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    def _wrap_method(self, func, *args, **kwargs):
        if self._wrap_with_kind:  # pragma: NO COVER
            kwargs["kind"] = self.kind
        return gapic_v1.method_async.wrap_method(func, *args, **kwargs)

    def close(self):
        return self._logged_channel.close()

    @property
    def kind(self) -> str:
        return "grpc_asyncio"

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
            self._stubs["list_locations"] = self._logged_channel.unary_unary(
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
            self._stubs["get_location"] = self._logged_channel.unary_unary(
                "/google.cloud.location.Locations/GetLocation",
                request_serializer=locations_pb2.GetLocationRequest.SerializeToString,
                response_deserializer=locations_pb2.Location.FromString,
            )
        return self._stubs["get_location"]


__all__ = ("ArtifactRegistryGrpcAsyncIOTransport",)
