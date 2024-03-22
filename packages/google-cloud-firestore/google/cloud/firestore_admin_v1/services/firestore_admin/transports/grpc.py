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
import warnings
from typing import Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import grpc_helpers
from google.api_core import operations_v1
from google.api_core import gapic_v1
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.cloud.firestore_admin_v1.types import backup
from google.cloud.firestore_admin_v1.types import database
from google.cloud.firestore_admin_v1.types import field
from google.cloud.firestore_admin_v1.types import firestore_admin
from google.cloud.firestore_admin_v1.types import index
from google.cloud.firestore_admin_v1.types import schedule
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from .base import FirestoreAdminTransport, DEFAULT_CLIENT_INFO


class FirestoreAdminGrpcTransport(FirestoreAdminTransport):
    """gRPC backend transport for FirestoreAdmin.

    The Cloud Firestore Admin API.

    This API provides several administrative services for Cloud
    Firestore.

    Project, Database, Namespace, Collection, Collection Group, and
    Document are used as defined in the Google Cloud Firestore API.

    Operation: An Operation represents work being performed in the
    background.

    The index service manages Cloud Firestore indexes.

    Index creation is performed asynchronously. An Operation resource is
    created for each such asynchronous operation. The state of the
    operation (including any errors encountered) may be queried via the
    Operation resource.

    The Operations collection provides a record of actions performed for
    the specified Project (including any Operations in progress).
    Operations are not created directly but through calls on other
    collections or resources.

    An Operation that is done may be deleted so that it is no longer
    listed as part of the Operation collection. Operations are garbage
    collected after 30 days. By default, ListOperations will only return
    in progress and failed operations. To list completed operation,
    issue a ListOperations request with the filter ``done: true``.

    Operations are created by service ``FirestoreAdmin``, but are
    accessed via service ``google.longrunning.Operations``.

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
        host: str = "firestore.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[grpc.Channel] = None,
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
                 The hostname to connect to (default: 'firestore.googleapis.com').
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
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client: Optional[operations_v1.OperationsClient] = None

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

    @classmethod
    def create_channel(
        cls,
        host: str = "firestore.googleapis.com",
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
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsClient(self.grpc_channel)

        # Return the client from cache.
        return self._operations_client

    @property
    def create_index(
        self,
    ) -> Callable[[firestore_admin.CreateIndexRequest], operations_pb2.Operation]:
        r"""Return a callable for the create index method over gRPC.

        Creates a composite index. This returns a
        [google.longrunning.Operation][google.longrunning.Operation]
        which may be used to track the status of the creation. The
        metadata for the operation will be the type
        [IndexOperationMetadata][google.firestore.admin.v1.IndexOperationMetadata].

        Returns:
            Callable[[~.CreateIndexRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_index" not in self._stubs:
            self._stubs["create_index"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/CreateIndex",
                request_serializer=firestore_admin.CreateIndexRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_index"]

    @property
    def list_indexes(
        self,
    ) -> Callable[
        [firestore_admin.ListIndexesRequest], firestore_admin.ListIndexesResponse
    ]:
        r"""Return a callable for the list indexes method over gRPC.

        Lists composite indexes.

        Returns:
            Callable[[~.ListIndexesRequest],
                    ~.ListIndexesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_indexes" not in self._stubs:
            self._stubs["list_indexes"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/ListIndexes",
                request_serializer=firestore_admin.ListIndexesRequest.serialize,
                response_deserializer=firestore_admin.ListIndexesResponse.deserialize,
            )
        return self._stubs["list_indexes"]

    @property
    def get_index(self) -> Callable[[firestore_admin.GetIndexRequest], index.Index]:
        r"""Return a callable for the get index method over gRPC.

        Gets a composite index.

        Returns:
            Callable[[~.GetIndexRequest],
                    ~.Index]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_index" not in self._stubs:
            self._stubs["get_index"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/GetIndex",
                request_serializer=firestore_admin.GetIndexRequest.serialize,
                response_deserializer=index.Index.deserialize,
            )
        return self._stubs["get_index"]

    @property
    def delete_index(
        self,
    ) -> Callable[[firestore_admin.DeleteIndexRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete index method over gRPC.

        Deletes a composite index.

        Returns:
            Callable[[~.DeleteIndexRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_index" not in self._stubs:
            self._stubs["delete_index"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/DeleteIndex",
                request_serializer=firestore_admin.DeleteIndexRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_index"]

    @property
    def get_field(self) -> Callable[[firestore_admin.GetFieldRequest], field.Field]:
        r"""Return a callable for the get field method over gRPC.

        Gets the metadata and configuration for a Field.

        Returns:
            Callable[[~.GetFieldRequest],
                    ~.Field]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_field" not in self._stubs:
            self._stubs["get_field"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/GetField",
                request_serializer=firestore_admin.GetFieldRequest.serialize,
                response_deserializer=field.Field.deserialize,
            )
        return self._stubs["get_field"]

    @property
    def update_field(
        self,
    ) -> Callable[[firestore_admin.UpdateFieldRequest], operations_pb2.Operation]:
        r"""Return a callable for the update field method over gRPC.

        Updates a field configuration. Currently, field updates apply
        only to single field index configuration. However, calls to
        [FirestoreAdmin.UpdateField][google.firestore.admin.v1.FirestoreAdmin.UpdateField]
        should provide a field mask to avoid changing any configuration
        that the caller isn't aware of. The field mask should be
        specified as: ``{ paths: "index_config" }``.

        This call returns a
        [google.longrunning.Operation][google.longrunning.Operation]
        which may be used to track the status of the field update. The
        metadata for the operation will be the type
        [FieldOperationMetadata][google.firestore.admin.v1.FieldOperationMetadata].

        To configure the default field settings for the database, use
        the special ``Field`` with resource name:
        ``projects/{project_id}/databases/{database_id}/collectionGroups/__default__/fields/*``.

        Returns:
            Callable[[~.UpdateFieldRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_field" not in self._stubs:
            self._stubs["update_field"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/UpdateField",
                request_serializer=firestore_admin.UpdateFieldRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_field"]

    @property
    def list_fields(
        self,
    ) -> Callable[
        [firestore_admin.ListFieldsRequest], firestore_admin.ListFieldsResponse
    ]:
        r"""Return a callable for the list fields method over gRPC.

        Lists the field configuration and metadata for this database.

        Currently,
        [FirestoreAdmin.ListFields][google.firestore.admin.v1.FirestoreAdmin.ListFields]
        only supports listing fields that have been explicitly
        overridden. To issue this query, call
        [FirestoreAdmin.ListFields][google.firestore.admin.v1.FirestoreAdmin.ListFields]
        with the filter set to ``indexConfig.usesAncestorConfig:false``
        or ``ttlConfig:*``.

        Returns:
            Callable[[~.ListFieldsRequest],
                    ~.ListFieldsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_fields" not in self._stubs:
            self._stubs["list_fields"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/ListFields",
                request_serializer=firestore_admin.ListFieldsRequest.serialize,
                response_deserializer=firestore_admin.ListFieldsResponse.deserialize,
            )
        return self._stubs["list_fields"]

    @property
    def export_documents(
        self,
    ) -> Callable[[firestore_admin.ExportDocumentsRequest], operations_pb2.Operation]:
        r"""Return a callable for the export documents method over gRPC.

        Exports a copy of all or a subset of documents from
        Google Cloud Firestore to another storage system, such
        as Google Cloud Storage. Recent updates to documents may
        not be reflected in the export. The export occurs in the
        background and its progress can be monitored and managed
        via the Operation resource that is created. The output
        of an export may only be used once the associated
        operation is done. If an export operation is cancelled
        before completion it may leave partial data behind in
        Google Cloud Storage.

        For more details on export behavior and output format,
        refer to:

        https://cloud.google.com/firestore/docs/manage-data/export-import

        Returns:
            Callable[[~.ExportDocumentsRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "export_documents" not in self._stubs:
            self._stubs["export_documents"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/ExportDocuments",
                request_serializer=firestore_admin.ExportDocumentsRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["export_documents"]

    @property
    def import_documents(
        self,
    ) -> Callable[[firestore_admin.ImportDocumentsRequest], operations_pb2.Operation]:
        r"""Return a callable for the import documents method over gRPC.

        Imports documents into Google Cloud Firestore.
        Existing documents with the same name are overwritten.
        The import occurs in the background and its progress can
        be monitored and managed via the Operation resource that
        is created. If an ImportDocuments operation is
        cancelled, it is possible that a subset of the data has
        already been imported to Cloud Firestore.

        Returns:
            Callable[[~.ImportDocumentsRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "import_documents" not in self._stubs:
            self._stubs["import_documents"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/ImportDocuments",
                request_serializer=firestore_admin.ImportDocumentsRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["import_documents"]

    @property
    def create_database(
        self,
    ) -> Callable[[firestore_admin.CreateDatabaseRequest], operations_pb2.Operation]:
        r"""Return a callable for the create database method over gRPC.

        Create a database.

        Returns:
            Callable[[~.CreateDatabaseRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_database" not in self._stubs:
            self._stubs["create_database"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/CreateDatabase",
                request_serializer=firestore_admin.CreateDatabaseRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_database"]

    @property
    def get_database(
        self,
    ) -> Callable[[firestore_admin.GetDatabaseRequest], database.Database]:
        r"""Return a callable for the get database method over gRPC.

        Gets information about a database.

        Returns:
            Callable[[~.GetDatabaseRequest],
                    ~.Database]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_database" not in self._stubs:
            self._stubs["get_database"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/GetDatabase",
                request_serializer=firestore_admin.GetDatabaseRequest.serialize,
                response_deserializer=database.Database.deserialize,
            )
        return self._stubs["get_database"]

    @property
    def list_databases(
        self,
    ) -> Callable[
        [firestore_admin.ListDatabasesRequest], firestore_admin.ListDatabasesResponse
    ]:
        r"""Return a callable for the list databases method over gRPC.

        List all the databases in the project.

        Returns:
            Callable[[~.ListDatabasesRequest],
                    ~.ListDatabasesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_databases" not in self._stubs:
            self._stubs["list_databases"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/ListDatabases",
                request_serializer=firestore_admin.ListDatabasesRequest.serialize,
                response_deserializer=firestore_admin.ListDatabasesResponse.deserialize,
            )
        return self._stubs["list_databases"]

    @property
    def update_database(
        self,
    ) -> Callable[[firestore_admin.UpdateDatabaseRequest], operations_pb2.Operation]:
        r"""Return a callable for the update database method over gRPC.

        Updates a database.

        Returns:
            Callable[[~.UpdateDatabaseRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_database" not in self._stubs:
            self._stubs["update_database"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/UpdateDatabase",
                request_serializer=firestore_admin.UpdateDatabaseRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_database"]

    @property
    def delete_database(
        self,
    ) -> Callable[[firestore_admin.DeleteDatabaseRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete database method over gRPC.

        Deletes a database.

        Returns:
            Callable[[~.DeleteDatabaseRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_database" not in self._stubs:
            self._stubs["delete_database"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/DeleteDatabase",
                request_serializer=firestore_admin.DeleteDatabaseRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_database"]

    @property
    def get_backup(self) -> Callable[[firestore_admin.GetBackupRequest], backup.Backup]:
        r"""Return a callable for the get backup method over gRPC.

        Gets information about a backup.

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
                "/google.firestore.admin.v1.FirestoreAdmin/GetBackup",
                request_serializer=firestore_admin.GetBackupRequest.serialize,
                response_deserializer=backup.Backup.deserialize,
            )
        return self._stubs["get_backup"]

    @property
    def list_backups(
        self,
    ) -> Callable[
        [firestore_admin.ListBackupsRequest], firestore_admin.ListBackupsResponse
    ]:
        r"""Return a callable for the list backups method over gRPC.

        Lists all the backups.

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
                "/google.firestore.admin.v1.FirestoreAdmin/ListBackups",
                request_serializer=firestore_admin.ListBackupsRequest.serialize,
                response_deserializer=firestore_admin.ListBackupsResponse.deserialize,
            )
        return self._stubs["list_backups"]

    @property
    def delete_backup(
        self,
    ) -> Callable[[firestore_admin.DeleteBackupRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete backup method over gRPC.

        Deletes a backup.

        Returns:
            Callable[[~.DeleteBackupRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_backup" not in self._stubs:
            self._stubs["delete_backup"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/DeleteBackup",
                request_serializer=firestore_admin.DeleteBackupRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_backup"]

    @property
    def restore_database(
        self,
    ) -> Callable[[firestore_admin.RestoreDatabaseRequest], operations_pb2.Operation]:
        r"""Return a callable for the restore database method over gRPC.

        Creates a new database by restoring from an existing backup.

        The new database must be in the same cloud region or
        multi-region location as the existing backup. This behaves
        similar to
        [FirestoreAdmin.CreateDatabase][google.firestore.admin.v1.CreateDatabase]
        except instead of creating a new empty database, a new database
        is created with the database type, index configuration, and
        documents from an existing backup.

        The [long-running operation][google.longrunning.Operation] can
        be used to track the progress of the restore, with the
        Operation's [metadata][google.longrunning.Operation.metadata]
        field type being the
        [RestoreDatabaseMetadata][google.firestore.admin.v1.RestoreDatabaseMetadata].
        The [response][google.longrunning.Operation.response] type is
        the [Database][google.firestore.admin.v1.Database] if the
        restore was successful. The new database is not readable or
        writeable until the LRO has completed.

        Returns:
            Callable[[~.RestoreDatabaseRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "restore_database" not in self._stubs:
            self._stubs["restore_database"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/RestoreDatabase",
                request_serializer=firestore_admin.RestoreDatabaseRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["restore_database"]

    @property
    def create_backup_schedule(
        self,
    ) -> Callable[
        [firestore_admin.CreateBackupScheduleRequest], schedule.BackupSchedule
    ]:
        r"""Return a callable for the create backup schedule method over gRPC.

        Creates a backup schedule on a database.
        At most two backup schedules can be configured on a
        database, one daily backup schedule with retention up to
        7 days and one weekly backup schedule with retention up
        to 14 weeks.

        Returns:
            Callable[[~.CreateBackupScheduleRequest],
                    ~.BackupSchedule]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_backup_schedule" not in self._stubs:
            self._stubs["create_backup_schedule"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/CreateBackupSchedule",
                request_serializer=firestore_admin.CreateBackupScheduleRequest.serialize,
                response_deserializer=schedule.BackupSchedule.deserialize,
            )
        return self._stubs["create_backup_schedule"]

    @property
    def get_backup_schedule(
        self,
    ) -> Callable[[firestore_admin.GetBackupScheduleRequest], schedule.BackupSchedule]:
        r"""Return a callable for the get backup schedule method over gRPC.

        Gets information about a backup schedule.

        Returns:
            Callable[[~.GetBackupScheduleRequest],
                    ~.BackupSchedule]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_backup_schedule" not in self._stubs:
            self._stubs["get_backup_schedule"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/GetBackupSchedule",
                request_serializer=firestore_admin.GetBackupScheduleRequest.serialize,
                response_deserializer=schedule.BackupSchedule.deserialize,
            )
        return self._stubs["get_backup_schedule"]

    @property
    def list_backup_schedules(
        self,
    ) -> Callable[
        [firestore_admin.ListBackupSchedulesRequest],
        firestore_admin.ListBackupSchedulesResponse,
    ]:
        r"""Return a callable for the list backup schedules method over gRPC.

        List backup schedules.

        Returns:
            Callable[[~.ListBackupSchedulesRequest],
                    ~.ListBackupSchedulesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_backup_schedules" not in self._stubs:
            self._stubs["list_backup_schedules"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/ListBackupSchedules",
                request_serializer=firestore_admin.ListBackupSchedulesRequest.serialize,
                response_deserializer=firestore_admin.ListBackupSchedulesResponse.deserialize,
            )
        return self._stubs["list_backup_schedules"]

    @property
    def update_backup_schedule(
        self,
    ) -> Callable[
        [firestore_admin.UpdateBackupScheduleRequest], schedule.BackupSchedule
    ]:
        r"""Return a callable for the update backup schedule method over gRPC.

        Updates a backup schedule.

        Returns:
            Callable[[~.UpdateBackupScheduleRequest],
                    ~.BackupSchedule]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_backup_schedule" not in self._stubs:
            self._stubs["update_backup_schedule"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/UpdateBackupSchedule",
                request_serializer=firestore_admin.UpdateBackupScheduleRequest.serialize,
                response_deserializer=schedule.BackupSchedule.deserialize,
            )
        return self._stubs["update_backup_schedule"]

    @property
    def delete_backup_schedule(
        self,
    ) -> Callable[[firestore_admin.DeleteBackupScheduleRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete backup schedule method over gRPC.

        Deletes a backup schedule.

        Returns:
            Callable[[~.DeleteBackupScheduleRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_backup_schedule" not in self._stubs:
            self._stubs["delete_backup_schedule"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/DeleteBackupSchedule",
                request_serializer=firestore_admin.DeleteBackupScheduleRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_backup_schedule"]

    def close(self):
        self.grpc_channel.close()

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
    def kind(self) -> str:
        return "grpc"


__all__ = ("FirestoreAdminGrpcTransport",)
