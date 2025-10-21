# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore
import proto  # type: ignore

from google.cloud.oracledatabase_v1.types import (
    db_system_initial_storage_size,
    db_version,
    exadata_infra,
    exadb_vm_cluster,
)
from google.cloud.oracledatabase_v1.types import (
    autonomous_database,
    database,
    database_character_set,
)
from google.cloud.oracledatabase_v1.types import (
    oracledatabase,
    pluggable_database,
    vm_cluster,
)
from google.cloud.oracledatabase_v1.types import (
    exascale_db_storage_vault as gco_exascale_db_storage_vault,
)
from google.cloud.oracledatabase_v1.types import db_system
from google.cloud.oracledatabase_v1.types import db_system as gco_db_system
from google.cloud.oracledatabase_v1.types import exascale_db_storage_vault
from google.cloud.oracledatabase_v1.types import minor_version
from google.cloud.oracledatabase_v1.types import odb_network
from google.cloud.oracledatabase_v1.types import odb_network as gco_odb_network
from google.cloud.oracledatabase_v1.types import odb_subnet
from google.cloud.oracledatabase_v1.types import odb_subnet as gco_odb_subnet

from .base import DEFAULT_CLIENT_INFO, OracleDatabaseTransport
from .grpc import OracleDatabaseGrpcTransport

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
                    "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
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
                    "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                    "rpcName": str(client_call_details.method),
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class OracleDatabaseGrpcAsyncIOTransport(OracleDatabaseTransport):
    """gRPC AsyncIO backend transport for OracleDatabase.

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
        host: str = "oracledatabase.googleapis.com",
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
            credentials_file (Optional[str]): Deprecated. A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`. This argument will be
                removed in the next major version of this library.
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
        host: str = "oracledatabase.googleapis.com",
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
                 The hostname to connect to (default: 'oracledatabase.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): Deprecated. A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
                This argument will be removed in the next major version of this library.
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
    def list_cloud_exadata_infrastructures(
        self,
    ) -> Callable[
        [oracledatabase.ListCloudExadataInfrastructuresRequest],
        Awaitable[oracledatabase.ListCloudExadataInfrastructuresResponse],
    ]:
        r"""Return a callable for the list cloud exadata
        infrastructures method over gRPC.

        Lists Exadata Infrastructures in a given project and
        location.

        Returns:
            Callable[[~.ListCloudExadataInfrastructuresRequest],
                    Awaitable[~.ListCloudExadataInfrastructuresResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_cloud_exadata_infrastructures" not in self._stubs:
            self._stubs[
                "list_cloud_exadata_infrastructures"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListCloudExadataInfrastructures",
                request_serializer=oracledatabase.ListCloudExadataInfrastructuresRequest.serialize,
                response_deserializer=oracledatabase.ListCloudExadataInfrastructuresResponse.deserialize,
            )
        return self._stubs["list_cloud_exadata_infrastructures"]

    @property
    def get_cloud_exadata_infrastructure(
        self,
    ) -> Callable[
        [oracledatabase.GetCloudExadataInfrastructureRequest],
        Awaitable[exadata_infra.CloudExadataInfrastructure],
    ]:
        r"""Return a callable for the get cloud exadata
        infrastructure method over gRPC.

        Gets details of a single Exadata Infrastructure.

        Returns:
            Callable[[~.GetCloudExadataInfrastructureRequest],
                    Awaitable[~.CloudExadataInfrastructure]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_cloud_exadata_infrastructure" not in self._stubs:
            self._stubs[
                "get_cloud_exadata_infrastructure"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/GetCloudExadataInfrastructure",
                request_serializer=oracledatabase.GetCloudExadataInfrastructureRequest.serialize,
                response_deserializer=exadata_infra.CloudExadataInfrastructure.deserialize,
            )
        return self._stubs["get_cloud_exadata_infrastructure"]

    @property
    def create_cloud_exadata_infrastructure(
        self,
    ) -> Callable[
        [oracledatabase.CreateCloudExadataInfrastructureRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create cloud exadata
        infrastructure method over gRPC.

        Creates a new Exadata Infrastructure in a given
        project and location.

        Returns:
            Callable[[~.CreateCloudExadataInfrastructureRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_cloud_exadata_infrastructure" not in self._stubs:
            self._stubs[
                "create_cloud_exadata_infrastructure"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/CreateCloudExadataInfrastructure",
                request_serializer=oracledatabase.CreateCloudExadataInfrastructureRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_cloud_exadata_infrastructure"]

    @property
    def delete_cloud_exadata_infrastructure(
        self,
    ) -> Callable[
        [oracledatabase.DeleteCloudExadataInfrastructureRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete cloud exadata
        infrastructure method over gRPC.

        Deletes a single Exadata Infrastructure.

        Returns:
            Callable[[~.DeleteCloudExadataInfrastructureRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_cloud_exadata_infrastructure" not in self._stubs:
            self._stubs[
                "delete_cloud_exadata_infrastructure"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/DeleteCloudExadataInfrastructure",
                request_serializer=oracledatabase.DeleteCloudExadataInfrastructureRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_cloud_exadata_infrastructure"]

    @property
    def list_cloud_vm_clusters(
        self,
    ) -> Callable[
        [oracledatabase.ListCloudVmClustersRequest],
        Awaitable[oracledatabase.ListCloudVmClustersResponse],
    ]:
        r"""Return a callable for the list cloud vm clusters method over gRPC.

        Lists the VM Clusters in a given project and
        location.

        Returns:
            Callable[[~.ListCloudVmClustersRequest],
                    Awaitable[~.ListCloudVmClustersResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_cloud_vm_clusters" not in self._stubs:
            self._stubs["list_cloud_vm_clusters"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListCloudVmClusters",
                request_serializer=oracledatabase.ListCloudVmClustersRequest.serialize,
                response_deserializer=oracledatabase.ListCloudVmClustersResponse.deserialize,
            )
        return self._stubs["list_cloud_vm_clusters"]

    @property
    def get_cloud_vm_cluster(
        self,
    ) -> Callable[
        [oracledatabase.GetCloudVmClusterRequest], Awaitable[vm_cluster.CloudVmCluster]
    ]:
        r"""Return a callable for the get cloud vm cluster method over gRPC.

        Gets details of a single VM Cluster.

        Returns:
            Callable[[~.GetCloudVmClusterRequest],
                    Awaitable[~.CloudVmCluster]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_cloud_vm_cluster" not in self._stubs:
            self._stubs["get_cloud_vm_cluster"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/GetCloudVmCluster",
                request_serializer=oracledatabase.GetCloudVmClusterRequest.serialize,
                response_deserializer=vm_cluster.CloudVmCluster.deserialize,
            )
        return self._stubs["get_cloud_vm_cluster"]

    @property
    def create_cloud_vm_cluster(
        self,
    ) -> Callable[
        [oracledatabase.CreateCloudVmClusterRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create cloud vm cluster method over gRPC.

        Creates a new VM Cluster in a given project and
        location.

        Returns:
            Callable[[~.CreateCloudVmClusterRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_cloud_vm_cluster" not in self._stubs:
            self._stubs["create_cloud_vm_cluster"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/CreateCloudVmCluster",
                request_serializer=oracledatabase.CreateCloudVmClusterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_cloud_vm_cluster"]

    @property
    def delete_cloud_vm_cluster(
        self,
    ) -> Callable[
        [oracledatabase.DeleteCloudVmClusterRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete cloud vm cluster method over gRPC.

        Deletes a single VM Cluster.

        Returns:
            Callable[[~.DeleteCloudVmClusterRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_cloud_vm_cluster" not in self._stubs:
            self._stubs["delete_cloud_vm_cluster"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/DeleteCloudVmCluster",
                request_serializer=oracledatabase.DeleteCloudVmClusterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_cloud_vm_cluster"]

    @property
    def list_entitlements(
        self,
    ) -> Callable[
        [oracledatabase.ListEntitlementsRequest],
        Awaitable[oracledatabase.ListEntitlementsResponse],
    ]:
        r"""Return a callable for the list entitlements method over gRPC.

        Lists the entitlements in a given project.

        Returns:
            Callable[[~.ListEntitlementsRequest],
                    Awaitable[~.ListEntitlementsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_entitlements" not in self._stubs:
            self._stubs["list_entitlements"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListEntitlements",
                request_serializer=oracledatabase.ListEntitlementsRequest.serialize,
                response_deserializer=oracledatabase.ListEntitlementsResponse.deserialize,
            )
        return self._stubs["list_entitlements"]

    @property
    def list_db_servers(
        self,
    ) -> Callable[
        [oracledatabase.ListDbServersRequest],
        Awaitable[oracledatabase.ListDbServersResponse],
    ]:
        r"""Return a callable for the list db servers method over gRPC.

        Lists the database servers of an Exadata
        Infrastructure instance.

        Returns:
            Callable[[~.ListDbServersRequest],
                    Awaitable[~.ListDbServersResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_db_servers" not in self._stubs:
            self._stubs["list_db_servers"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListDbServers",
                request_serializer=oracledatabase.ListDbServersRequest.serialize,
                response_deserializer=oracledatabase.ListDbServersResponse.deserialize,
            )
        return self._stubs["list_db_servers"]

    @property
    def list_db_nodes(
        self,
    ) -> Callable[
        [oracledatabase.ListDbNodesRequest],
        Awaitable[oracledatabase.ListDbNodesResponse],
    ]:
        r"""Return a callable for the list db nodes method over gRPC.

        Lists the database nodes of a VM Cluster.

        Returns:
            Callable[[~.ListDbNodesRequest],
                    Awaitable[~.ListDbNodesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_db_nodes" not in self._stubs:
            self._stubs["list_db_nodes"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListDbNodes",
                request_serializer=oracledatabase.ListDbNodesRequest.serialize,
                response_deserializer=oracledatabase.ListDbNodesResponse.deserialize,
            )
        return self._stubs["list_db_nodes"]

    @property
    def list_gi_versions(
        self,
    ) -> Callable[
        [oracledatabase.ListGiVersionsRequest],
        Awaitable[oracledatabase.ListGiVersionsResponse],
    ]:
        r"""Return a callable for the list gi versions method over gRPC.

        Lists all the valid Oracle Grid Infrastructure (GI)
        versions for the given project and location.

        Returns:
            Callable[[~.ListGiVersionsRequest],
                    Awaitable[~.ListGiVersionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_gi_versions" not in self._stubs:
            self._stubs["list_gi_versions"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListGiVersions",
                request_serializer=oracledatabase.ListGiVersionsRequest.serialize,
                response_deserializer=oracledatabase.ListGiVersionsResponse.deserialize,
            )
        return self._stubs["list_gi_versions"]

    @property
    def list_minor_versions(
        self,
    ) -> Callable[
        [minor_version.ListMinorVersionsRequest],
        Awaitable[minor_version.ListMinorVersionsResponse],
    ]:
        r"""Return a callable for the list minor versions method over gRPC.

        Lists all the valid minor versions for the given
        project, location, gi version and shape family.

        Returns:
            Callable[[~.ListMinorVersionsRequest],
                    Awaitable[~.ListMinorVersionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_minor_versions" not in self._stubs:
            self._stubs["list_minor_versions"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListMinorVersions",
                request_serializer=minor_version.ListMinorVersionsRequest.serialize,
                response_deserializer=minor_version.ListMinorVersionsResponse.deserialize,
            )
        return self._stubs["list_minor_versions"]

    @property
    def list_db_system_shapes(
        self,
    ) -> Callable[
        [oracledatabase.ListDbSystemShapesRequest],
        Awaitable[oracledatabase.ListDbSystemShapesResponse],
    ]:
        r"""Return a callable for the list db system shapes method over gRPC.

        Lists the database system shapes available for the
        project and location.

        Returns:
            Callable[[~.ListDbSystemShapesRequest],
                    Awaitable[~.ListDbSystemShapesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_db_system_shapes" not in self._stubs:
            self._stubs["list_db_system_shapes"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListDbSystemShapes",
                request_serializer=oracledatabase.ListDbSystemShapesRequest.serialize,
                response_deserializer=oracledatabase.ListDbSystemShapesResponse.deserialize,
            )
        return self._stubs["list_db_system_shapes"]

    @property
    def list_autonomous_databases(
        self,
    ) -> Callable[
        [oracledatabase.ListAutonomousDatabasesRequest],
        Awaitable[oracledatabase.ListAutonomousDatabasesResponse],
    ]:
        r"""Return a callable for the list autonomous databases method over gRPC.

        Lists the Autonomous Databases in a given project and
        location.

        Returns:
            Callable[[~.ListAutonomousDatabasesRequest],
                    Awaitable[~.ListAutonomousDatabasesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_autonomous_databases" not in self._stubs:
            self._stubs["list_autonomous_databases"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListAutonomousDatabases",
                request_serializer=oracledatabase.ListAutonomousDatabasesRequest.serialize,
                response_deserializer=oracledatabase.ListAutonomousDatabasesResponse.deserialize,
            )
        return self._stubs["list_autonomous_databases"]

    @property
    def get_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.GetAutonomousDatabaseRequest],
        Awaitable[autonomous_database.AutonomousDatabase],
    ]:
        r"""Return a callable for the get autonomous database method over gRPC.

        Gets the details of a single Autonomous Database.

        Returns:
            Callable[[~.GetAutonomousDatabaseRequest],
                    Awaitable[~.AutonomousDatabase]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_autonomous_database" not in self._stubs:
            self._stubs["get_autonomous_database"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/GetAutonomousDatabase",
                request_serializer=oracledatabase.GetAutonomousDatabaseRequest.serialize,
                response_deserializer=autonomous_database.AutonomousDatabase.deserialize,
            )
        return self._stubs["get_autonomous_database"]

    @property
    def create_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.CreateAutonomousDatabaseRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create autonomous database method over gRPC.

        Creates a new Autonomous Database in a given project
        and location.

        Returns:
            Callable[[~.CreateAutonomousDatabaseRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_autonomous_database" not in self._stubs:
            self._stubs[
                "create_autonomous_database"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/CreateAutonomousDatabase",
                request_serializer=oracledatabase.CreateAutonomousDatabaseRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_autonomous_database"]

    @property
    def update_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.UpdateAutonomousDatabaseRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update autonomous database method over gRPC.

        Updates the parameters of a single Autonomous
        Database.

        Returns:
            Callable[[~.UpdateAutonomousDatabaseRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_autonomous_database" not in self._stubs:
            self._stubs[
                "update_autonomous_database"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/UpdateAutonomousDatabase",
                request_serializer=oracledatabase.UpdateAutonomousDatabaseRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_autonomous_database"]

    @property
    def delete_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.DeleteAutonomousDatabaseRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete autonomous database method over gRPC.

        Deletes a single Autonomous Database.

        Returns:
            Callable[[~.DeleteAutonomousDatabaseRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_autonomous_database" not in self._stubs:
            self._stubs[
                "delete_autonomous_database"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/DeleteAutonomousDatabase",
                request_serializer=oracledatabase.DeleteAutonomousDatabaseRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_autonomous_database"]

    @property
    def restore_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.RestoreAutonomousDatabaseRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the restore autonomous database method over gRPC.

        Restores a single Autonomous Database.

        Returns:
            Callable[[~.RestoreAutonomousDatabaseRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "restore_autonomous_database" not in self._stubs:
            self._stubs[
                "restore_autonomous_database"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/RestoreAutonomousDatabase",
                request_serializer=oracledatabase.RestoreAutonomousDatabaseRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["restore_autonomous_database"]

    @property
    def generate_autonomous_database_wallet(
        self,
    ) -> Callable[
        [oracledatabase.GenerateAutonomousDatabaseWalletRequest],
        Awaitable[oracledatabase.GenerateAutonomousDatabaseWalletResponse],
    ]:
        r"""Return a callable for the generate autonomous database
        wallet method over gRPC.

        Generates a wallet for an Autonomous Database.

        Returns:
            Callable[[~.GenerateAutonomousDatabaseWalletRequest],
                    Awaitable[~.GenerateAutonomousDatabaseWalletResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_autonomous_database_wallet" not in self._stubs:
            self._stubs[
                "generate_autonomous_database_wallet"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/GenerateAutonomousDatabaseWallet",
                request_serializer=oracledatabase.GenerateAutonomousDatabaseWalletRequest.serialize,
                response_deserializer=oracledatabase.GenerateAutonomousDatabaseWalletResponse.deserialize,
            )
        return self._stubs["generate_autonomous_database_wallet"]

    @property
    def list_autonomous_db_versions(
        self,
    ) -> Callable[
        [oracledatabase.ListAutonomousDbVersionsRequest],
        Awaitable[oracledatabase.ListAutonomousDbVersionsResponse],
    ]:
        r"""Return a callable for the list autonomous db versions method over gRPC.

        Lists all the available Autonomous Database versions
        for a project and location.

        Returns:
            Callable[[~.ListAutonomousDbVersionsRequest],
                    Awaitable[~.ListAutonomousDbVersionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_autonomous_db_versions" not in self._stubs:
            self._stubs[
                "list_autonomous_db_versions"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListAutonomousDbVersions",
                request_serializer=oracledatabase.ListAutonomousDbVersionsRequest.serialize,
                response_deserializer=oracledatabase.ListAutonomousDbVersionsResponse.deserialize,
            )
        return self._stubs["list_autonomous_db_versions"]

    @property
    def list_autonomous_database_character_sets(
        self,
    ) -> Callable[
        [oracledatabase.ListAutonomousDatabaseCharacterSetsRequest],
        Awaitable[oracledatabase.ListAutonomousDatabaseCharacterSetsResponse],
    ]:
        r"""Return a callable for the list autonomous database
        character sets method over gRPC.

        Lists Autonomous Database Character Sets in a given
        project and location.

        Returns:
            Callable[[~.ListAutonomousDatabaseCharacterSetsRequest],
                    Awaitable[~.ListAutonomousDatabaseCharacterSetsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_autonomous_database_character_sets" not in self._stubs:
            self._stubs[
                "list_autonomous_database_character_sets"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListAutonomousDatabaseCharacterSets",
                request_serializer=oracledatabase.ListAutonomousDatabaseCharacterSetsRequest.serialize,
                response_deserializer=oracledatabase.ListAutonomousDatabaseCharacterSetsResponse.deserialize,
            )
        return self._stubs["list_autonomous_database_character_sets"]

    @property
    def list_autonomous_database_backups(
        self,
    ) -> Callable[
        [oracledatabase.ListAutonomousDatabaseBackupsRequest],
        Awaitable[oracledatabase.ListAutonomousDatabaseBackupsResponse],
    ]:
        r"""Return a callable for the list autonomous database
        backups method over gRPC.

        Lists the long-term and automatic backups of an
        Autonomous Database.

        Returns:
            Callable[[~.ListAutonomousDatabaseBackupsRequest],
                    Awaitable[~.ListAutonomousDatabaseBackupsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_autonomous_database_backups" not in self._stubs:
            self._stubs[
                "list_autonomous_database_backups"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListAutonomousDatabaseBackups",
                request_serializer=oracledatabase.ListAutonomousDatabaseBackupsRequest.serialize,
                response_deserializer=oracledatabase.ListAutonomousDatabaseBackupsResponse.deserialize,
            )
        return self._stubs["list_autonomous_database_backups"]

    @property
    def stop_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.StopAutonomousDatabaseRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the stop autonomous database method over gRPC.

        Stops an Autonomous Database.

        Returns:
            Callable[[~.StopAutonomousDatabaseRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "stop_autonomous_database" not in self._stubs:
            self._stubs["stop_autonomous_database"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/StopAutonomousDatabase",
                request_serializer=oracledatabase.StopAutonomousDatabaseRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["stop_autonomous_database"]

    @property
    def start_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.StartAutonomousDatabaseRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the start autonomous database method over gRPC.

        Starts an Autonomous Database.

        Returns:
            Callable[[~.StartAutonomousDatabaseRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "start_autonomous_database" not in self._stubs:
            self._stubs["start_autonomous_database"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/StartAutonomousDatabase",
                request_serializer=oracledatabase.StartAutonomousDatabaseRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["start_autonomous_database"]

    @property
    def restart_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.RestartAutonomousDatabaseRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the restart autonomous database method over gRPC.

        Restarts an Autonomous Database.

        Returns:
            Callable[[~.RestartAutonomousDatabaseRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "restart_autonomous_database" not in self._stubs:
            self._stubs[
                "restart_autonomous_database"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/RestartAutonomousDatabase",
                request_serializer=oracledatabase.RestartAutonomousDatabaseRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["restart_autonomous_database"]

    @property
    def switchover_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.SwitchoverAutonomousDatabaseRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the switchover autonomous database method over gRPC.

        Initiates a switchover of specified autonomous
        database to the associated peer database.

        Returns:
            Callable[[~.SwitchoverAutonomousDatabaseRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "switchover_autonomous_database" not in self._stubs:
            self._stubs[
                "switchover_autonomous_database"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/SwitchoverAutonomousDatabase",
                request_serializer=oracledatabase.SwitchoverAutonomousDatabaseRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["switchover_autonomous_database"]

    @property
    def failover_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.FailoverAutonomousDatabaseRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the failover autonomous database method over gRPC.

        Initiates a failover to target autonomous database
        from the associated primary database.

        Returns:
            Callable[[~.FailoverAutonomousDatabaseRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "failover_autonomous_database" not in self._stubs:
            self._stubs[
                "failover_autonomous_database"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/FailoverAutonomousDatabase",
                request_serializer=oracledatabase.FailoverAutonomousDatabaseRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["failover_autonomous_database"]

    @property
    def list_odb_networks(
        self,
    ) -> Callable[
        [odb_network.ListOdbNetworksRequest],
        Awaitable[odb_network.ListOdbNetworksResponse],
    ]:
        r"""Return a callable for the list odb networks method over gRPC.

        Lists the ODB Networks in a given project and
        location.

        Returns:
            Callable[[~.ListOdbNetworksRequest],
                    Awaitable[~.ListOdbNetworksResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_odb_networks" not in self._stubs:
            self._stubs["list_odb_networks"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListOdbNetworks",
                request_serializer=odb_network.ListOdbNetworksRequest.serialize,
                response_deserializer=odb_network.ListOdbNetworksResponse.deserialize,
            )
        return self._stubs["list_odb_networks"]

    @property
    def get_odb_network(
        self,
    ) -> Callable[
        [odb_network.GetOdbNetworkRequest], Awaitable[odb_network.OdbNetwork]
    ]:
        r"""Return a callable for the get odb network method over gRPC.

        Gets details of a single ODB Network.

        Returns:
            Callable[[~.GetOdbNetworkRequest],
                    Awaitable[~.OdbNetwork]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_odb_network" not in self._stubs:
            self._stubs["get_odb_network"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/GetOdbNetwork",
                request_serializer=odb_network.GetOdbNetworkRequest.serialize,
                response_deserializer=odb_network.OdbNetwork.deserialize,
            )
        return self._stubs["get_odb_network"]

    @property
    def create_odb_network(
        self,
    ) -> Callable[
        [gco_odb_network.CreateOdbNetworkRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create odb network method over gRPC.

        Creates a new ODB Network in a given project and
        location.

        Returns:
            Callable[[~.CreateOdbNetworkRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_odb_network" not in self._stubs:
            self._stubs["create_odb_network"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/CreateOdbNetwork",
                request_serializer=gco_odb_network.CreateOdbNetworkRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_odb_network"]

    @property
    def delete_odb_network(
        self,
    ) -> Callable[
        [odb_network.DeleteOdbNetworkRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete odb network method over gRPC.

        Deletes a single ODB Network.

        Returns:
            Callable[[~.DeleteOdbNetworkRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_odb_network" not in self._stubs:
            self._stubs["delete_odb_network"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/DeleteOdbNetwork",
                request_serializer=odb_network.DeleteOdbNetworkRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_odb_network"]

    @property
    def list_odb_subnets(
        self,
    ) -> Callable[
        [odb_subnet.ListOdbSubnetsRequest], Awaitable[odb_subnet.ListOdbSubnetsResponse]
    ]:
        r"""Return a callable for the list odb subnets method over gRPC.

        Lists all the ODB Subnets in a given ODB Network.

        Returns:
            Callable[[~.ListOdbSubnetsRequest],
                    Awaitable[~.ListOdbSubnetsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_odb_subnets" not in self._stubs:
            self._stubs["list_odb_subnets"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListOdbSubnets",
                request_serializer=odb_subnet.ListOdbSubnetsRequest.serialize,
                response_deserializer=odb_subnet.ListOdbSubnetsResponse.deserialize,
            )
        return self._stubs["list_odb_subnets"]

    @property
    def get_odb_subnet(
        self,
    ) -> Callable[[odb_subnet.GetOdbSubnetRequest], Awaitable[odb_subnet.OdbSubnet]]:
        r"""Return a callable for the get odb subnet method over gRPC.

        Gets details of a single ODB Subnet.

        Returns:
            Callable[[~.GetOdbSubnetRequest],
                    Awaitable[~.OdbSubnet]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_odb_subnet" not in self._stubs:
            self._stubs["get_odb_subnet"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/GetOdbSubnet",
                request_serializer=odb_subnet.GetOdbSubnetRequest.serialize,
                response_deserializer=odb_subnet.OdbSubnet.deserialize,
            )
        return self._stubs["get_odb_subnet"]

    @property
    def create_odb_subnet(
        self,
    ) -> Callable[
        [gco_odb_subnet.CreateOdbSubnetRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create odb subnet method over gRPC.

        Creates a new ODB Subnet in a given ODB Network.

        Returns:
            Callable[[~.CreateOdbSubnetRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_odb_subnet" not in self._stubs:
            self._stubs["create_odb_subnet"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/CreateOdbSubnet",
                request_serializer=gco_odb_subnet.CreateOdbSubnetRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_odb_subnet"]

    @property
    def delete_odb_subnet(
        self,
    ) -> Callable[
        [odb_subnet.DeleteOdbSubnetRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete odb subnet method over gRPC.

        Deletes a single ODB Subnet.

        Returns:
            Callable[[~.DeleteOdbSubnetRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_odb_subnet" not in self._stubs:
            self._stubs["delete_odb_subnet"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/DeleteOdbSubnet",
                request_serializer=odb_subnet.DeleteOdbSubnetRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_odb_subnet"]

    @property
    def list_exadb_vm_clusters(
        self,
    ) -> Callable[
        [oracledatabase.ListExadbVmClustersRequest],
        Awaitable[oracledatabase.ListExadbVmClustersResponse],
    ]:
        r"""Return a callable for the list exadb vm clusters method over gRPC.

        Lists all the Exadb (Exascale) VM Clusters for the
        given project and location.

        Returns:
            Callable[[~.ListExadbVmClustersRequest],
                    Awaitable[~.ListExadbVmClustersResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_exadb_vm_clusters" not in self._stubs:
            self._stubs["list_exadb_vm_clusters"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListExadbVmClusters",
                request_serializer=oracledatabase.ListExadbVmClustersRequest.serialize,
                response_deserializer=oracledatabase.ListExadbVmClustersResponse.deserialize,
            )
        return self._stubs["list_exadb_vm_clusters"]

    @property
    def get_exadb_vm_cluster(
        self,
    ) -> Callable[
        [oracledatabase.GetExadbVmClusterRequest],
        Awaitable[exadb_vm_cluster.ExadbVmCluster],
    ]:
        r"""Return a callable for the get exadb vm cluster method over gRPC.

        Gets details of a single Exadb (Exascale) VM Cluster.

        Returns:
            Callable[[~.GetExadbVmClusterRequest],
                    Awaitable[~.ExadbVmCluster]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_exadb_vm_cluster" not in self._stubs:
            self._stubs["get_exadb_vm_cluster"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/GetExadbVmCluster",
                request_serializer=oracledatabase.GetExadbVmClusterRequest.serialize,
                response_deserializer=exadb_vm_cluster.ExadbVmCluster.deserialize,
            )
        return self._stubs["get_exadb_vm_cluster"]

    @property
    def create_exadb_vm_cluster(
        self,
    ) -> Callable[
        [oracledatabase.CreateExadbVmClusterRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create exadb vm cluster method over gRPC.

        Creates a new Exadb (Exascale) VM Cluster resource.

        Returns:
            Callable[[~.CreateExadbVmClusterRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_exadb_vm_cluster" not in self._stubs:
            self._stubs["create_exadb_vm_cluster"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/CreateExadbVmCluster",
                request_serializer=oracledatabase.CreateExadbVmClusterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_exadb_vm_cluster"]

    @property
    def delete_exadb_vm_cluster(
        self,
    ) -> Callable[
        [oracledatabase.DeleteExadbVmClusterRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete exadb vm cluster method over gRPC.

        Deletes a single Exadb (Exascale) VM Cluster.

        Returns:
            Callable[[~.DeleteExadbVmClusterRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_exadb_vm_cluster" not in self._stubs:
            self._stubs["delete_exadb_vm_cluster"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/DeleteExadbVmCluster",
                request_serializer=oracledatabase.DeleteExadbVmClusterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_exadb_vm_cluster"]

    @property
    def update_exadb_vm_cluster(
        self,
    ) -> Callable[
        [oracledatabase.UpdateExadbVmClusterRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update exadb vm cluster method over gRPC.

        Updates a single Exadb (Exascale) VM Cluster. To add
        virtual machines to existing exadb vm cluster, only pass
        the node count.

        Returns:
            Callable[[~.UpdateExadbVmClusterRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_exadb_vm_cluster" not in self._stubs:
            self._stubs["update_exadb_vm_cluster"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/UpdateExadbVmCluster",
                request_serializer=oracledatabase.UpdateExadbVmClusterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_exadb_vm_cluster"]

    @property
    def remove_virtual_machine_exadb_vm_cluster(
        self,
    ) -> Callable[
        [oracledatabase.RemoveVirtualMachineExadbVmClusterRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the remove virtual machine exadb
        vm cluster method over gRPC.

        Removes virtual machines from an existing exadb vm
        cluster.

        Returns:
            Callable[[~.RemoveVirtualMachineExadbVmClusterRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "remove_virtual_machine_exadb_vm_cluster" not in self._stubs:
            self._stubs[
                "remove_virtual_machine_exadb_vm_cluster"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/RemoveVirtualMachineExadbVmCluster",
                request_serializer=oracledatabase.RemoveVirtualMachineExadbVmClusterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["remove_virtual_machine_exadb_vm_cluster"]

    @property
    def list_exascale_db_storage_vaults(
        self,
    ) -> Callable[
        [exascale_db_storage_vault.ListExascaleDbStorageVaultsRequest],
        Awaitable[exascale_db_storage_vault.ListExascaleDbStorageVaultsResponse],
    ]:
        r"""Return a callable for the list exascale db storage
        vaults method over gRPC.

        Lists all the ExascaleDB Storage Vaults for the given
        project and location.

        Returns:
            Callable[[~.ListExascaleDbStorageVaultsRequest],
                    Awaitable[~.ListExascaleDbStorageVaultsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_exascale_db_storage_vaults" not in self._stubs:
            self._stubs[
                "list_exascale_db_storage_vaults"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListExascaleDbStorageVaults",
                request_serializer=exascale_db_storage_vault.ListExascaleDbStorageVaultsRequest.serialize,
                response_deserializer=exascale_db_storage_vault.ListExascaleDbStorageVaultsResponse.deserialize,
            )
        return self._stubs["list_exascale_db_storage_vaults"]

    @property
    def get_exascale_db_storage_vault(
        self,
    ) -> Callable[
        [exascale_db_storage_vault.GetExascaleDbStorageVaultRequest],
        Awaitable[exascale_db_storage_vault.ExascaleDbStorageVault],
    ]:
        r"""Return a callable for the get exascale db storage vault method over gRPC.

        Gets details of a single ExascaleDB Storage Vault.

        Returns:
            Callable[[~.GetExascaleDbStorageVaultRequest],
                    Awaitable[~.ExascaleDbStorageVault]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_exascale_db_storage_vault" not in self._stubs:
            self._stubs[
                "get_exascale_db_storage_vault"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/GetExascaleDbStorageVault",
                request_serializer=exascale_db_storage_vault.GetExascaleDbStorageVaultRequest.serialize,
                response_deserializer=exascale_db_storage_vault.ExascaleDbStorageVault.deserialize,
            )
        return self._stubs["get_exascale_db_storage_vault"]

    @property
    def create_exascale_db_storage_vault(
        self,
    ) -> Callable[
        [gco_exascale_db_storage_vault.CreateExascaleDbStorageVaultRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create exascale db storage
        vault method over gRPC.

        Creates a new ExascaleDB Storage Vault resource.

        Returns:
            Callable[[~.CreateExascaleDbStorageVaultRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_exascale_db_storage_vault" not in self._stubs:
            self._stubs[
                "create_exascale_db_storage_vault"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/CreateExascaleDbStorageVault",
                request_serializer=gco_exascale_db_storage_vault.CreateExascaleDbStorageVaultRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_exascale_db_storage_vault"]

    @property
    def delete_exascale_db_storage_vault(
        self,
    ) -> Callable[
        [exascale_db_storage_vault.DeleteExascaleDbStorageVaultRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete exascale db storage
        vault method over gRPC.

        Deletes a single ExascaleDB Storage Vault.

        Returns:
            Callable[[~.DeleteExascaleDbStorageVaultRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_exascale_db_storage_vault" not in self._stubs:
            self._stubs[
                "delete_exascale_db_storage_vault"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/DeleteExascaleDbStorageVault",
                request_serializer=exascale_db_storage_vault.DeleteExascaleDbStorageVaultRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_exascale_db_storage_vault"]

    @property
    def list_db_system_initial_storage_sizes(
        self,
    ) -> Callable[
        [db_system_initial_storage_size.ListDbSystemInitialStorageSizesRequest],
        Awaitable[
            db_system_initial_storage_size.ListDbSystemInitialStorageSizesResponse
        ],
    ]:
        r"""Return a callable for the list db system initial storage
        sizes method over gRPC.

        Lists all the DbSystemInitialStorageSizes for the
        given project and location.

        Returns:
            Callable[[~.ListDbSystemInitialStorageSizesRequest],
                    Awaitable[~.ListDbSystemInitialStorageSizesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_db_system_initial_storage_sizes" not in self._stubs:
            self._stubs[
                "list_db_system_initial_storage_sizes"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListDbSystemInitialStorageSizes",
                request_serializer=db_system_initial_storage_size.ListDbSystemInitialStorageSizesRequest.serialize,
                response_deserializer=db_system_initial_storage_size.ListDbSystemInitialStorageSizesResponse.deserialize,
            )
        return self._stubs["list_db_system_initial_storage_sizes"]

    @property
    def list_databases(
        self,
    ) -> Callable[
        [database.ListDatabasesRequest], Awaitable[database.ListDatabasesResponse]
    ]:
        r"""Return a callable for the list databases method over gRPC.

        Lists all the Databases for the given project,
        location and DbSystem.

        Returns:
            Callable[[~.ListDatabasesRequest],
                    Awaitable[~.ListDatabasesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_databases" not in self._stubs:
            self._stubs["list_databases"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListDatabases",
                request_serializer=database.ListDatabasesRequest.serialize,
                response_deserializer=database.ListDatabasesResponse.deserialize,
            )
        return self._stubs["list_databases"]

    @property
    def get_database(
        self,
    ) -> Callable[[database.GetDatabaseRequest], Awaitable[database.Database]]:
        r"""Return a callable for the get database method over gRPC.

        Gets details of a single Database.

        Returns:
            Callable[[~.GetDatabaseRequest],
                    Awaitable[~.Database]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_database" not in self._stubs:
            self._stubs["get_database"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/GetDatabase",
                request_serializer=database.GetDatabaseRequest.serialize,
                response_deserializer=database.Database.deserialize,
            )
        return self._stubs["get_database"]

    @property
    def list_pluggable_databases(
        self,
    ) -> Callable[
        [pluggable_database.ListPluggableDatabasesRequest],
        Awaitable[pluggable_database.ListPluggableDatabasesResponse],
    ]:
        r"""Return a callable for the list pluggable databases method over gRPC.

        Lists all the PluggableDatabases for the given
        project, location and Container Database.

        Returns:
            Callable[[~.ListPluggableDatabasesRequest],
                    Awaitable[~.ListPluggableDatabasesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_pluggable_databases" not in self._stubs:
            self._stubs["list_pluggable_databases"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListPluggableDatabases",
                request_serializer=pluggable_database.ListPluggableDatabasesRequest.serialize,
                response_deserializer=pluggable_database.ListPluggableDatabasesResponse.deserialize,
            )
        return self._stubs["list_pluggable_databases"]

    @property
    def get_pluggable_database(
        self,
    ) -> Callable[
        [pluggable_database.GetPluggableDatabaseRequest],
        Awaitable[pluggable_database.PluggableDatabase],
    ]:
        r"""Return a callable for the get pluggable database method over gRPC.

        Gets details of a single PluggableDatabase.

        Returns:
            Callable[[~.GetPluggableDatabaseRequest],
                    Awaitable[~.PluggableDatabase]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_pluggable_database" not in self._stubs:
            self._stubs["get_pluggable_database"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/GetPluggableDatabase",
                request_serializer=pluggable_database.GetPluggableDatabaseRequest.serialize,
                response_deserializer=pluggable_database.PluggableDatabase.deserialize,
            )
        return self._stubs["get_pluggable_database"]

    @property
    def list_db_systems(
        self,
    ) -> Callable[
        [db_system.ListDbSystemsRequest], Awaitable[db_system.ListDbSystemsResponse]
    ]:
        r"""Return a callable for the list db systems method over gRPC.

        Lists all the DbSystems for the given project and
        location.

        Returns:
            Callable[[~.ListDbSystemsRequest],
                    Awaitable[~.ListDbSystemsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_db_systems" not in self._stubs:
            self._stubs["list_db_systems"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListDbSystems",
                request_serializer=db_system.ListDbSystemsRequest.serialize,
                response_deserializer=db_system.ListDbSystemsResponse.deserialize,
            )
        return self._stubs["list_db_systems"]

    @property
    def get_db_system(
        self,
    ) -> Callable[[db_system.GetDbSystemRequest], Awaitable[db_system.DbSystem]]:
        r"""Return a callable for the get db system method over gRPC.

        Gets details of a single DbSystem.

        Returns:
            Callable[[~.GetDbSystemRequest],
                    Awaitable[~.DbSystem]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_db_system" not in self._stubs:
            self._stubs["get_db_system"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/GetDbSystem",
                request_serializer=db_system.GetDbSystemRequest.serialize,
                response_deserializer=db_system.DbSystem.deserialize,
            )
        return self._stubs["get_db_system"]

    @property
    def create_db_system(
        self,
    ) -> Callable[
        [gco_db_system.CreateDbSystemRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create db system method over gRPC.

        Creates a new DbSystem in a given project and
        location.

        Returns:
            Callable[[~.CreateDbSystemRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_db_system" not in self._stubs:
            self._stubs["create_db_system"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/CreateDbSystem",
                request_serializer=gco_db_system.CreateDbSystemRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_db_system"]

    @property
    def delete_db_system(
        self,
    ) -> Callable[
        [db_system.DeleteDbSystemRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete db system method over gRPC.

        Deletes a single DbSystem.

        Returns:
            Callable[[~.DeleteDbSystemRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_db_system" not in self._stubs:
            self._stubs["delete_db_system"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/DeleteDbSystem",
                request_serializer=db_system.DeleteDbSystemRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_db_system"]

    @property
    def list_db_versions(
        self,
    ) -> Callable[
        [db_version.ListDbVersionsRequest], Awaitable[db_version.ListDbVersionsResponse]
    ]:
        r"""Return a callable for the list db versions method over gRPC.

        List DbVersions for the given project and location.

        Returns:
            Callable[[~.ListDbVersionsRequest],
                    Awaitable[~.ListDbVersionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_db_versions" not in self._stubs:
            self._stubs["list_db_versions"] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListDbVersions",
                request_serializer=db_version.ListDbVersionsRequest.serialize,
                response_deserializer=db_version.ListDbVersionsResponse.deserialize,
            )
        return self._stubs["list_db_versions"]

    @property
    def list_database_character_sets(
        self,
    ) -> Callable[
        [database_character_set.ListDatabaseCharacterSetsRequest],
        Awaitable[database_character_set.ListDatabaseCharacterSetsResponse],
    ]:
        r"""Return a callable for the list database character sets method over gRPC.

        List DatabaseCharacterSets for the given project and
        location.

        Returns:
            Callable[[~.ListDatabaseCharacterSetsRequest],
                    Awaitable[~.ListDatabaseCharacterSetsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_database_character_sets" not in self._stubs:
            self._stubs[
                "list_database_character_sets"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.oracledatabase.v1.OracleDatabase/ListDatabaseCharacterSets",
                request_serializer=database_character_set.ListDatabaseCharacterSetsRequest.serialize,
                response_deserializer=database_character_set.ListDatabaseCharacterSetsResponse.deserialize,
            )
        return self._stubs["list_database_character_sets"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.list_cloud_exadata_infrastructures: self._wrap_method(
                self.list_cloud_exadata_infrastructures,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_cloud_exadata_infrastructure: self._wrap_method(
                self.get_cloud_exadata_infrastructure,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_cloud_exadata_infrastructure: self._wrap_method(
                self.create_cloud_exadata_infrastructure,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_cloud_exadata_infrastructure: self._wrap_method(
                self.delete_cloud_exadata_infrastructure,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_cloud_vm_clusters: self._wrap_method(
                self.list_cloud_vm_clusters,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_cloud_vm_cluster: self._wrap_method(
                self.get_cloud_vm_cluster,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_cloud_vm_cluster: self._wrap_method(
                self.create_cloud_vm_cluster,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_cloud_vm_cluster: self._wrap_method(
                self.delete_cloud_vm_cluster,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_entitlements: self._wrap_method(
                self.list_entitlements,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_db_servers: self._wrap_method(
                self.list_db_servers,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_db_nodes: self._wrap_method(
                self.list_db_nodes,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_gi_versions: self._wrap_method(
                self.list_gi_versions,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_minor_versions: self._wrap_method(
                self.list_minor_versions,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_db_system_shapes: self._wrap_method(
                self.list_db_system_shapes,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_autonomous_databases: self._wrap_method(
                self.list_autonomous_databases,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_autonomous_database: self._wrap_method(
                self.get_autonomous_database,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_autonomous_database: self._wrap_method(
                self.create_autonomous_database,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_autonomous_database: self._wrap_method(
                self.update_autonomous_database,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_autonomous_database: self._wrap_method(
                self.delete_autonomous_database,
                default_timeout=None,
                client_info=client_info,
            ),
            self.restore_autonomous_database: self._wrap_method(
                self.restore_autonomous_database,
                default_timeout=None,
                client_info=client_info,
            ),
            self.generate_autonomous_database_wallet: self._wrap_method(
                self.generate_autonomous_database_wallet,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_autonomous_db_versions: self._wrap_method(
                self.list_autonomous_db_versions,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_autonomous_database_character_sets: self._wrap_method(
                self.list_autonomous_database_character_sets,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_autonomous_database_backups: self._wrap_method(
                self.list_autonomous_database_backups,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.stop_autonomous_database: self._wrap_method(
                self.stop_autonomous_database,
                default_timeout=None,
                client_info=client_info,
            ),
            self.start_autonomous_database: self._wrap_method(
                self.start_autonomous_database,
                default_timeout=None,
                client_info=client_info,
            ),
            self.restart_autonomous_database: self._wrap_method(
                self.restart_autonomous_database,
                default_timeout=None,
                client_info=client_info,
            ),
            self.switchover_autonomous_database: self._wrap_method(
                self.switchover_autonomous_database,
                default_timeout=None,
                client_info=client_info,
            ),
            self.failover_autonomous_database: self._wrap_method(
                self.failover_autonomous_database,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_odb_networks: self._wrap_method(
                self.list_odb_networks,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_odb_network: self._wrap_method(
                self.get_odb_network,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_odb_network: self._wrap_method(
                self.create_odb_network,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_odb_network: self._wrap_method(
                self.delete_odb_network,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_odb_subnets: self._wrap_method(
                self.list_odb_subnets,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_odb_subnet: self._wrap_method(
                self.get_odb_subnet,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_odb_subnet: self._wrap_method(
                self.create_odb_subnet,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_odb_subnet: self._wrap_method(
                self.delete_odb_subnet,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_exadb_vm_clusters: self._wrap_method(
                self.list_exadb_vm_clusters,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_exadb_vm_cluster: self._wrap_method(
                self.get_exadb_vm_cluster,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_exadb_vm_cluster: self._wrap_method(
                self.create_exadb_vm_cluster,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_exadb_vm_cluster: self._wrap_method(
                self.delete_exadb_vm_cluster,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_exadb_vm_cluster: self._wrap_method(
                self.update_exadb_vm_cluster,
                default_timeout=None,
                client_info=client_info,
            ),
            self.remove_virtual_machine_exadb_vm_cluster: self._wrap_method(
                self.remove_virtual_machine_exadb_vm_cluster,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_exascale_db_storage_vaults: self._wrap_method(
                self.list_exascale_db_storage_vaults,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_exascale_db_storage_vault: self._wrap_method(
                self.get_exascale_db_storage_vault,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_exascale_db_storage_vault: self._wrap_method(
                self.create_exascale_db_storage_vault,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_exascale_db_storage_vault: self._wrap_method(
                self.delete_exascale_db_storage_vault,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_db_system_initial_storage_sizes: self._wrap_method(
                self.list_db_system_initial_storage_sizes,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_databases: self._wrap_method(
                self.list_databases,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_database: self._wrap_method(
                self.get_database,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_pluggable_databases: self._wrap_method(
                self.list_pluggable_databases,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_pluggable_database: self._wrap_method(
                self.get_pluggable_database,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_db_systems: self._wrap_method(
                self.list_db_systems,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_db_system: self._wrap_method(
                self.get_db_system,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_db_system: self._wrap_method(
                self.create_db_system,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_db_system: self._wrap_method(
                self.delete_db_system,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_db_versions: self._wrap_method(
                self.list_db_versions,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_database_character_sets: self._wrap_method(
                self.list_database_character_sets,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
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
            self.cancel_operation: self._wrap_method(
                self.cancel_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_operation: self._wrap_method(
                self.delete_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_operation: self._wrap_method(
                self.get_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_operations: self._wrap_method(
                self.list_operations,
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
    def delete_operation(
        self,
    ) -> Callable[[operations_pb2.DeleteOperationRequest], None]:
        r"""Return a callable for the delete_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_operation" not in self._stubs:
            self._stubs["delete_operation"] = self._logged_channel.unary_unary(
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
            self._stubs["cancel_operation"] = self._logged_channel.unary_unary(
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
            self._stubs["get_operation"] = self._logged_channel.unary_unary(
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
            self._stubs["list_operations"] = self._logged_channel.unary_unary(
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


__all__ = ("OracleDatabaseGrpcAsyncIOTransport",)
