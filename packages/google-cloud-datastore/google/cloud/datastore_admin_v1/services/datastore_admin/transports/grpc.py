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
from typing import Callable, Dict, Optional, Sequence, Tuple

from google.api_core import grpc_helpers  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google import auth  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.cloud.datastore_admin_v1.types import datastore_admin
from google.cloud.datastore_admin_v1.types import index
from google.longrunning import operations_pb2 as operations  # type: ignore

from .base import DatastoreAdminTransport, DEFAULT_CLIENT_INFO


class DatastoreAdminGrpcTransport(DatastoreAdminTransport):
    """gRPC backend transport for DatastoreAdmin.

    Google Cloud Datastore Admin API
    The Datastore Admin API provides several admin services for
    Cloud Datastore.
    -----------------------------------------------------------------------------
    ## Concepts

    Project, namespace, kind, and entity as defined in the Google
    Cloud Datastore API.

    Operation: An Operation represents work being performed in the
    background.
    EntityFilter: Allows specifying a subset of entities in a
    project. This is specified as a combination of kinds and
    namespaces (either or both of which may be all).

    -----------------------------------------------------------------------------
    ## Services

    # Export/Import

    The Export/Import service provides the ability to copy all or a
    subset of entities to/from Google Cloud Storage.

    Exported data may be imported into Cloud Datastore for any
    Google Cloud Platform project. It is not restricted to the
    export source project. It is possible to export from one project
    and then import into another.
    Exported data can also be loaded into Google BigQuery for
    analysis.
    Exports and imports are performed asynchronously. An Operation
    resource is created for each export/import. The state (including
    any errors encountered) of the export/import may be queried via
    the Operation resource.
    # Index

    The index service manages Cloud Datastore composite indexes.
    Index creation and deletion are performed asynchronously. An
    Operation resource is created for each such asynchronous
    operation. The state of the operation (including any errors
    encountered) may be queried via the Operation resource.

    # Operation

    The Operations collection provides a record of actions performed
    for the specified project (including any operations in
    progress). Operations are not created directly but through calls
    on other collections or resources.
    An operation that is not yet done may be cancelled. The request
    to cancel is asynchronous and the operation may continue to run
    for some time after the request to cancel is made.

    An operation that is done may be deleted so that it is no longer
    listed as part of the Operation collection.

    ListOperations returns all pending operations, but not completed
    operations.
    Operations are created by service DatastoreAdmin,
    but are accessed via service google.longrunning.Operations.

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
        host: str = "datastore.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        channel: grpc.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
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
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._ssl_channel_credentials = ssl_channel_credentials

        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None
        elif api_mtls_endpoint:
            warnings.warn(
                "api_mtls_endpoint and client_cert_source are deprecated",
                DeprecationWarning,
            )

            host = (
                api_mtls_endpoint
                if ":" in api_mtls_endpoint
                else api_mtls_endpoint + ":443"
            )

            if credentials is None:
                credentials, _ = auth.default(
                    scopes=self.AUTH_SCOPES, quota_project_id=quota_project_id
                )

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
            )
            self._ssl_channel_credentials = ssl_credentials
        else:
            host = host if ":" in host else host + ":443"

            if credentials is None:
                credentials, _ = auth.default(
                    scopes=self.AUTH_SCOPES, quota_project_id=quota_project_id
                )

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_channel_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
            )

        self._stubs = {}  # type: Dict[str, Callable]

        # Run the base constructor.
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes or self.AUTH_SCOPES,
            quota_project_id=quota_project_id,
            client_info=client_info,
        )

    @classmethod
    def create_channel(
        cls,
        host: str = "datastore.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            address (Optionsl[str]): The host for the channel to use.
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
        scopes = scopes or cls.AUTH_SCOPES
        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
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
        if "operations_client" not in self.__dict__:
            self.__dict__["operations_client"] = operations_v1.OperationsClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self.__dict__["operations_client"]

    @property
    def export_entities(
        self,
    ) -> Callable[[datastore_admin.ExportEntitiesRequest], operations.Operation]:
        r"""Return a callable for the export entities method over gRPC.

        Exports a copy of all or a subset of entities from
        Google Cloud Datastore to another storage system, such
        as Google Cloud Storage. Recent updates to entities may
        not be reflected in the export. The export occurs in the
        background and its progress can be monitored and managed
        via the Operation resource that is created. The output
        of an export may only be used once the associated
        operation is done. If an export operation is cancelled
        before completion it may leave partial data behind in
        Google Cloud Storage.

        Returns:
            Callable[[~.ExportEntitiesRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "export_entities" not in self._stubs:
            self._stubs["export_entities"] = self.grpc_channel.unary_unary(
                "/google.datastore.admin.v1.DatastoreAdmin/ExportEntities",
                request_serializer=datastore_admin.ExportEntitiesRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["export_entities"]

    @property
    def import_entities(
        self,
    ) -> Callable[[datastore_admin.ImportEntitiesRequest], operations.Operation]:
        r"""Return a callable for the import entities method over gRPC.

        Imports entities into Google Cloud Datastore.
        Existing entities with the same key are overwritten. The
        import occurs in the background and its progress can be
        monitored and managed via the Operation resource that is
        created. If an ImportEntities operation is cancelled, it
        is possible that a subset of the data has already been
        imported to Cloud Datastore.

        Returns:
            Callable[[~.ImportEntitiesRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "import_entities" not in self._stubs:
            self._stubs["import_entities"] = self.grpc_channel.unary_unary(
                "/google.datastore.admin.v1.DatastoreAdmin/ImportEntities",
                request_serializer=datastore_admin.ImportEntitiesRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["import_entities"]

    @property
    def get_index(self) -> Callable[[datastore_admin.GetIndexRequest], index.Index]:
        r"""Return a callable for the get index method over gRPC.

        Gets an index.

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
                "/google.datastore.admin.v1.DatastoreAdmin/GetIndex",
                request_serializer=datastore_admin.GetIndexRequest.serialize,
                response_deserializer=index.Index.deserialize,
            )
        return self._stubs["get_index"]

    @property
    def list_indexes(
        self,
    ) -> Callable[
        [datastore_admin.ListIndexesRequest], datastore_admin.ListIndexesResponse
    ]:
        r"""Return a callable for the list indexes method over gRPC.

        Lists the indexes that match the specified filters.
        Datastore uses an eventually consistent query to fetch
        the list of indexes and may occasionally return stale
        results.

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
                "/google.datastore.admin.v1.DatastoreAdmin/ListIndexes",
                request_serializer=datastore_admin.ListIndexesRequest.serialize,
                response_deserializer=datastore_admin.ListIndexesResponse.deserialize,
            )
        return self._stubs["list_indexes"]


__all__ = ("DatastoreAdminGrpcTransport",)
