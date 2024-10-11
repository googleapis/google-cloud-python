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

from google.cloud.metastore_v1.types import metastore

from .base import DEFAULT_CLIENT_INFO, DataprocMetastoreTransport
from .grpc import DataprocMetastoreGrpcTransport


class DataprocMetastoreGrpcAsyncIOTransport(DataprocMetastoreTransport):
    """gRPC AsyncIO backend transport for DataprocMetastore.

    Configures and manages metastore services. Metastore services are
    fully managed, highly available, autoscaled, autohealing, OSS-native
    deployments of technical metadata management software. Each
    metastore service exposes a network endpoint through which metadata
    queries are served. Metadata queries can originate from a variety of
    sources, including Apache Hive, Apache Presto, and Apache Spark.

    The Dataproc Metastore API defines the following resource model:

    -  The service works with a collection of Google Cloud projects,
       named: ``/projects/*``

    -  Each project has a collection of available locations, named:
       ``/locations/*`` (a location must refer to a Google Cloud
       ``region``)

    -  Each location has a collection of services, named:
       ``/services/*``

    -  Dataproc Metastore services are resources with names of the form:

       ``/projects/{project_number}/locations/{location_id}/services/{service_id}``.

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
        host: str = "metastore.googleapis.com",
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
        host: str = "metastore.googleapis.com",
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
                 The hostname to connect to (default: 'metastore.googleapis.com').
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
    def list_services(
        self,
    ) -> Callable[
        [metastore.ListServicesRequest], Awaitable[metastore.ListServicesResponse]
    ]:
        r"""Return a callable for the list services method over gRPC.

        Lists services in a project and location.

        Returns:
            Callable[[~.ListServicesRequest],
                    Awaitable[~.ListServicesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_services" not in self._stubs:
            self._stubs["list_services"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1.DataprocMetastore/ListServices",
                request_serializer=metastore.ListServicesRequest.serialize,
                response_deserializer=metastore.ListServicesResponse.deserialize,
            )
        return self._stubs["list_services"]

    @property
    def get_service(
        self,
    ) -> Callable[[metastore.GetServiceRequest], Awaitable[metastore.Service]]:
        r"""Return a callable for the get service method over gRPC.

        Gets the details of a single service.

        Returns:
            Callable[[~.GetServiceRequest],
                    Awaitable[~.Service]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_service" not in self._stubs:
            self._stubs["get_service"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1.DataprocMetastore/GetService",
                request_serializer=metastore.GetServiceRequest.serialize,
                response_deserializer=metastore.Service.deserialize,
            )
        return self._stubs["get_service"]

    @property
    def create_service(
        self,
    ) -> Callable[
        [metastore.CreateServiceRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create service method over gRPC.

        Creates a metastore service in a project and
        location.

        Returns:
            Callable[[~.CreateServiceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_service" not in self._stubs:
            self._stubs["create_service"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1.DataprocMetastore/CreateService",
                request_serializer=metastore.CreateServiceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_service"]

    @property
    def update_service(
        self,
    ) -> Callable[
        [metastore.UpdateServiceRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update service method over gRPC.

        Updates the parameters of a single service.

        Returns:
            Callable[[~.UpdateServiceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_service" not in self._stubs:
            self._stubs["update_service"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1.DataprocMetastore/UpdateService",
                request_serializer=metastore.UpdateServiceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_service"]

    @property
    def delete_service(
        self,
    ) -> Callable[
        [metastore.DeleteServiceRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete service method over gRPC.

        Deletes a single service.

        Returns:
            Callable[[~.DeleteServiceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_service" not in self._stubs:
            self._stubs["delete_service"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1.DataprocMetastore/DeleteService",
                request_serializer=metastore.DeleteServiceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_service"]

    @property
    def list_metadata_imports(
        self,
    ) -> Callable[
        [metastore.ListMetadataImportsRequest],
        Awaitable[metastore.ListMetadataImportsResponse],
    ]:
        r"""Return a callable for the list metadata imports method over gRPC.

        Lists imports in a service.

        Returns:
            Callable[[~.ListMetadataImportsRequest],
                    Awaitable[~.ListMetadataImportsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_metadata_imports" not in self._stubs:
            self._stubs["list_metadata_imports"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1.DataprocMetastore/ListMetadataImports",
                request_serializer=metastore.ListMetadataImportsRequest.serialize,
                response_deserializer=metastore.ListMetadataImportsResponse.deserialize,
            )
        return self._stubs["list_metadata_imports"]

    @property
    def get_metadata_import(
        self,
    ) -> Callable[
        [metastore.GetMetadataImportRequest], Awaitable[metastore.MetadataImport]
    ]:
        r"""Return a callable for the get metadata import method over gRPC.

        Gets details of a single import.

        Returns:
            Callable[[~.GetMetadataImportRequest],
                    Awaitable[~.MetadataImport]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_metadata_import" not in self._stubs:
            self._stubs["get_metadata_import"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1.DataprocMetastore/GetMetadataImport",
                request_serializer=metastore.GetMetadataImportRequest.serialize,
                response_deserializer=metastore.MetadataImport.deserialize,
            )
        return self._stubs["get_metadata_import"]

    @property
    def create_metadata_import(
        self,
    ) -> Callable[
        [metastore.CreateMetadataImportRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create metadata import method over gRPC.

        Creates a new MetadataImport in a given project and
        location.

        Returns:
            Callable[[~.CreateMetadataImportRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_metadata_import" not in self._stubs:
            self._stubs["create_metadata_import"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1.DataprocMetastore/CreateMetadataImport",
                request_serializer=metastore.CreateMetadataImportRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_metadata_import"]

    @property
    def update_metadata_import(
        self,
    ) -> Callable[
        [metastore.UpdateMetadataImportRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update metadata import method over gRPC.

        Updates a single import.
        Only the description field of MetadataImport is
        supported to be updated.

        Returns:
            Callable[[~.UpdateMetadataImportRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_metadata_import" not in self._stubs:
            self._stubs["update_metadata_import"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1.DataprocMetastore/UpdateMetadataImport",
                request_serializer=metastore.UpdateMetadataImportRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_metadata_import"]

    @property
    def export_metadata(
        self,
    ) -> Callable[
        [metastore.ExportMetadataRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the export metadata method over gRPC.

        Exports metadata from a service.

        Returns:
            Callable[[~.ExportMetadataRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "export_metadata" not in self._stubs:
            self._stubs["export_metadata"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1.DataprocMetastore/ExportMetadata",
                request_serializer=metastore.ExportMetadataRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["export_metadata"]

    @property
    def restore_service(
        self,
    ) -> Callable[
        [metastore.RestoreServiceRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the restore service method over gRPC.

        Restores a service from a backup.

        Returns:
            Callable[[~.RestoreServiceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "restore_service" not in self._stubs:
            self._stubs["restore_service"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1.DataprocMetastore/RestoreService",
                request_serializer=metastore.RestoreServiceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["restore_service"]

    @property
    def list_backups(
        self,
    ) -> Callable[
        [metastore.ListBackupsRequest], Awaitable[metastore.ListBackupsResponse]
    ]:
        r"""Return a callable for the list backups method over gRPC.

        Lists backups in a service.

        Returns:
            Callable[[~.ListBackupsRequest],
                    Awaitable[~.ListBackupsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_backups" not in self._stubs:
            self._stubs["list_backups"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1.DataprocMetastore/ListBackups",
                request_serializer=metastore.ListBackupsRequest.serialize,
                response_deserializer=metastore.ListBackupsResponse.deserialize,
            )
        return self._stubs["list_backups"]

    @property
    def get_backup(
        self,
    ) -> Callable[[metastore.GetBackupRequest], Awaitable[metastore.Backup]]:
        r"""Return a callable for the get backup method over gRPC.

        Gets details of a single backup.

        Returns:
            Callable[[~.GetBackupRequest],
                    Awaitable[~.Backup]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_backup" not in self._stubs:
            self._stubs["get_backup"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1.DataprocMetastore/GetBackup",
                request_serializer=metastore.GetBackupRequest.serialize,
                response_deserializer=metastore.Backup.deserialize,
            )
        return self._stubs["get_backup"]

    @property
    def create_backup(
        self,
    ) -> Callable[[metastore.CreateBackupRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the create backup method over gRPC.

        Creates a new backup in a given project and location.

        Returns:
            Callable[[~.CreateBackupRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_backup" not in self._stubs:
            self._stubs["create_backup"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1.DataprocMetastore/CreateBackup",
                request_serializer=metastore.CreateBackupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_backup"]

    @property
    def delete_backup(
        self,
    ) -> Callable[[metastore.DeleteBackupRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the delete backup method over gRPC.

        Deletes a single backup.

        Returns:
            Callable[[~.DeleteBackupRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_backup" not in self._stubs:
            self._stubs["delete_backup"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1.DataprocMetastore/DeleteBackup",
                request_serializer=metastore.DeleteBackupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_backup"]

    @property
    def query_metadata(
        self,
    ) -> Callable[
        [metastore.QueryMetadataRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the query metadata method over gRPC.

        Query DPMS metadata.

        Returns:
            Callable[[~.QueryMetadataRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "query_metadata" not in self._stubs:
            self._stubs["query_metadata"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1.DataprocMetastore/QueryMetadata",
                request_serializer=metastore.QueryMetadataRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["query_metadata"]

    @property
    def move_table_to_database(
        self,
    ) -> Callable[
        [metastore.MoveTableToDatabaseRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the move table to database method over gRPC.

        Move a table to another database.

        Returns:
            Callable[[~.MoveTableToDatabaseRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "move_table_to_database" not in self._stubs:
            self._stubs["move_table_to_database"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1.DataprocMetastore/MoveTableToDatabase",
                request_serializer=metastore.MoveTableToDatabaseRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["move_table_to_database"]

    @property
    def alter_metadata_resource_location(
        self,
    ) -> Callable[
        [metastore.AlterMetadataResourceLocationRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the alter metadata resource
        location method over gRPC.

        Alter metadata resource location. The metadata
        resource can be a database, table, or partition. This
        functionality only updates the parent directory for the
        respective metadata resource and does not transfer any
        existing data to the new location.

        Returns:
            Callable[[~.AlterMetadataResourceLocationRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "alter_metadata_resource_location" not in self._stubs:
            self._stubs[
                "alter_metadata_resource_location"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1.DataprocMetastore/AlterMetadataResourceLocation",
                request_serializer=metastore.AlterMetadataResourceLocationRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["alter_metadata_resource_location"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.list_services: self._wrap_method(
                self.list_services,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_service: self._wrap_method(
                self.get_service,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_service: self._wrap_method(
                self.create_service,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_service: self._wrap_method(
                self.update_service,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_service: self._wrap_method(
                self.delete_service,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_metadata_imports: self._wrap_method(
                self.list_metadata_imports,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_metadata_import: self._wrap_method(
                self.get_metadata_import,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_metadata_import: self._wrap_method(
                self.create_metadata_import,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_metadata_import: self._wrap_method(
                self.update_metadata_import,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.export_metadata: self._wrap_method(
                self.export_metadata,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.restore_service: self._wrap_method(
                self.restore_service,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_backups: self._wrap_method(
                self.list_backups,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_backup: self._wrap_method(
                self.get_backup,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_backup: self._wrap_method(
                self.create_backup,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_backup: self._wrap_method(
                self.delete_backup,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.query_metadata: self._wrap_method(
                self.query_metadata,
                default_timeout=None,
                client_info=client_info,
            ),
            self.move_table_to_database: self._wrap_method(
                self.move_table_to_database,
                default_timeout=None,
                client_info=client_info,
            ),
            self.alter_metadata_resource_location: self._wrap_method(
                self.alter_metadata_resource_location,
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
        return self.grpc_channel.close()

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


__all__ = ("DataprocMetastoreGrpcAsyncIOTransport",)
