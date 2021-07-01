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
from typing import Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import grpc_helpers  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.api_core import gapic_v1  # type: ignore
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.cloud.metastore_v1beta.types import metastore
from google.longrunning import operations_pb2  # type: ignore
from .base import DataprocMetastoreTransport, DEFAULT_CLIENT_INFO


class DataprocMetastoreGrpcTransport(DataprocMetastoreTransport):
    """gRPC backend transport for DataprocMetastore.

    Configures and manages metastore services. Metastore services are
    fully managed, highly available, auto-scaled, auto-healing,
    OSS-native deployments of technical metadata management software.
    Each metastore service exposes a network endpoint through which
    metadata queries are served. Metadata queries can originate from a
    variety of sources, including Apache Hive, Apache Presto, and Apache
    Spark.

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

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "metastore.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        channel: grpc.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id: Optional[str] = None,
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
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
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
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
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

    @classmethod
    def create_channel(
        cls,
        host: str = "metastore.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
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
        """Return the channel designed to connect to this service.
        """
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Sanity check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsClient(self.grpc_channel)

        # Return the client from cache.
        return self._operations_client

    @property
    def list_services(
        self,
    ) -> Callable[[metastore.ListServicesRequest], metastore.ListServicesResponse]:
        r"""Return a callable for the list services method over gRPC.

        Lists services in a project and location.

        Returns:
            Callable[[~.ListServicesRequest],
                    ~.ListServicesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_services" not in self._stubs:
            self._stubs["list_services"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1beta.DataprocMetastore/ListServices",
                request_serializer=metastore.ListServicesRequest.serialize,
                response_deserializer=metastore.ListServicesResponse.deserialize,
            )
        return self._stubs["list_services"]

    @property
    def get_service(self) -> Callable[[metastore.GetServiceRequest], metastore.Service]:
        r"""Return a callable for the get service method over gRPC.

        Gets the details of a single service.

        Returns:
            Callable[[~.GetServiceRequest],
                    ~.Service]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_service" not in self._stubs:
            self._stubs["get_service"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1beta.DataprocMetastore/GetService",
                request_serializer=metastore.GetServiceRequest.serialize,
                response_deserializer=metastore.Service.deserialize,
            )
        return self._stubs["get_service"]

    @property
    def create_service(
        self,
    ) -> Callable[[metastore.CreateServiceRequest], operations_pb2.Operation]:
        r"""Return a callable for the create service method over gRPC.

        Creates a metastore service in a project and
        location.

        Returns:
            Callable[[~.CreateServiceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_service" not in self._stubs:
            self._stubs["create_service"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1beta.DataprocMetastore/CreateService",
                request_serializer=metastore.CreateServiceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_service"]

    @property
    def update_service(
        self,
    ) -> Callable[[metastore.UpdateServiceRequest], operations_pb2.Operation]:
        r"""Return a callable for the update service method over gRPC.

        Updates the parameters of a single service.

        Returns:
            Callable[[~.UpdateServiceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_service" not in self._stubs:
            self._stubs["update_service"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1beta.DataprocMetastore/UpdateService",
                request_serializer=metastore.UpdateServiceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_service"]

    @property
    def delete_service(
        self,
    ) -> Callable[[metastore.DeleteServiceRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete service method over gRPC.

        Deletes a single service.

        Returns:
            Callable[[~.DeleteServiceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_service" not in self._stubs:
            self._stubs["delete_service"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1beta.DataprocMetastore/DeleteService",
                request_serializer=metastore.DeleteServiceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_service"]

    @property
    def list_metadata_imports(
        self,
    ) -> Callable[
        [metastore.ListMetadataImportsRequest], metastore.ListMetadataImportsResponse
    ]:
        r"""Return a callable for the list metadata imports method over gRPC.

        Lists imports in a service.

        Returns:
            Callable[[~.ListMetadataImportsRequest],
                    ~.ListMetadataImportsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_metadata_imports" not in self._stubs:
            self._stubs["list_metadata_imports"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1beta.DataprocMetastore/ListMetadataImports",
                request_serializer=metastore.ListMetadataImportsRequest.serialize,
                response_deserializer=metastore.ListMetadataImportsResponse.deserialize,
            )
        return self._stubs["list_metadata_imports"]

    @property
    def get_metadata_import(
        self,
    ) -> Callable[[metastore.GetMetadataImportRequest], metastore.MetadataImport]:
        r"""Return a callable for the get metadata import method over gRPC.

        Gets details of a single import.

        Returns:
            Callable[[~.GetMetadataImportRequest],
                    ~.MetadataImport]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_metadata_import" not in self._stubs:
            self._stubs["get_metadata_import"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1beta.DataprocMetastore/GetMetadataImport",
                request_serializer=metastore.GetMetadataImportRequest.serialize,
                response_deserializer=metastore.MetadataImport.deserialize,
            )
        return self._stubs["get_metadata_import"]

    @property
    def create_metadata_import(
        self,
    ) -> Callable[[metastore.CreateMetadataImportRequest], operations_pb2.Operation]:
        r"""Return a callable for the create metadata import method over gRPC.

        Creates a new MetadataImport in a given project and
        location.

        Returns:
            Callable[[~.CreateMetadataImportRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_metadata_import" not in self._stubs:
            self._stubs["create_metadata_import"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1beta.DataprocMetastore/CreateMetadataImport",
                request_serializer=metastore.CreateMetadataImportRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_metadata_import"]

    @property
    def update_metadata_import(
        self,
    ) -> Callable[[metastore.UpdateMetadataImportRequest], operations_pb2.Operation]:
        r"""Return a callable for the update metadata import method over gRPC.

        Updates a single import.
        Only the description field of MetadataImport is
        supported to be updated.

        Returns:
            Callable[[~.UpdateMetadataImportRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_metadata_import" not in self._stubs:
            self._stubs["update_metadata_import"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1beta.DataprocMetastore/UpdateMetadataImport",
                request_serializer=metastore.UpdateMetadataImportRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_metadata_import"]

    @property
    def export_metadata(
        self,
    ) -> Callable[[metastore.ExportMetadataRequest], operations_pb2.Operation]:
        r"""Return a callable for the export metadata method over gRPC.

        Exports metadata from a service.

        Returns:
            Callable[[~.ExportMetadataRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "export_metadata" not in self._stubs:
            self._stubs["export_metadata"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1beta.DataprocMetastore/ExportMetadata",
                request_serializer=metastore.ExportMetadataRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["export_metadata"]

    @property
    def restore_service(
        self,
    ) -> Callable[[metastore.RestoreServiceRequest], operations_pb2.Operation]:
        r"""Return a callable for the restore service method over gRPC.

        Restores a service from a backup.

        Returns:
            Callable[[~.RestoreServiceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "restore_service" not in self._stubs:
            self._stubs["restore_service"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1beta.DataprocMetastore/RestoreService",
                request_serializer=metastore.RestoreServiceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["restore_service"]

    @property
    def list_backups(
        self,
    ) -> Callable[[metastore.ListBackupsRequest], metastore.ListBackupsResponse]:
        r"""Return a callable for the list backups method over gRPC.

        Lists backups in a service.

        Returns:
            Callable[[~.ListBackupsRequest],
                    ~.ListBackupsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_backups" not in self._stubs:
            self._stubs["list_backups"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1beta.DataprocMetastore/ListBackups",
                request_serializer=metastore.ListBackupsRequest.serialize,
                response_deserializer=metastore.ListBackupsResponse.deserialize,
            )
        return self._stubs["list_backups"]

    @property
    def get_backup(self) -> Callable[[metastore.GetBackupRequest], metastore.Backup]:
        r"""Return a callable for the get backup method over gRPC.

        Gets details of a single backup.

        Returns:
            Callable[[~.GetBackupRequest],
                    ~.Backup]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_backup" not in self._stubs:
            self._stubs["get_backup"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1beta.DataprocMetastore/GetBackup",
                request_serializer=metastore.GetBackupRequest.serialize,
                response_deserializer=metastore.Backup.deserialize,
            )
        return self._stubs["get_backup"]

    @property
    def create_backup(
        self,
    ) -> Callable[[metastore.CreateBackupRequest], operations_pb2.Operation]:
        r"""Return a callable for the create backup method over gRPC.

        Creates a new Backup in a given project and location.

        Returns:
            Callable[[~.CreateBackupRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_backup" not in self._stubs:
            self._stubs["create_backup"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1beta.DataprocMetastore/CreateBackup",
                request_serializer=metastore.CreateBackupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_backup"]

    @property
    def delete_backup(
        self,
    ) -> Callable[[metastore.DeleteBackupRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete backup method over gRPC.

        Deletes a single backup.

        Returns:
            Callable[[~.DeleteBackupRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_backup" not in self._stubs:
            self._stubs["delete_backup"] = self.grpc_channel.unary_unary(
                "/google.cloud.metastore.v1beta.DataprocMetastore/DeleteBackup",
                request_serializer=metastore.DeleteBackupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_backup"]


__all__ = ("DataprocMetastoreGrpcTransport",)
