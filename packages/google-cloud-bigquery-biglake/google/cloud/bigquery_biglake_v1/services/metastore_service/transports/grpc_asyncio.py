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
from google.api_core import gapic_v1, grpc_helpers_async
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.bigquery_biglake_v1.types import metastore

from .base import DEFAULT_CLIENT_INFO, MetastoreServiceTransport
from .grpc import MetastoreServiceGrpcTransport


class MetastoreServiceGrpcAsyncIOTransport(MetastoreServiceTransport):
    """gRPC AsyncIO backend transport for MetastoreService.

    BigLake Metastore is a serverless, highly available, multi-tenant
    runtime metastore for Google Cloud Data Analytics products.

    The BigLake Metastore API defines the following resource model:

    -  A collection of Google Cloud projects: ``/projects/*``
    -  Each project has a collection of available locations:
       ``/locations/*``
    -  Each location has a collection of catalogs: ``/catalogs/*``
    -  Each catalog has a collection of databases: ``/databases/*``
    -  Each database has a collection of tables: ``/tables/*``

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
        host: str = "biglake.googleapis.com",
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
        host: str = "biglake.googleapis.com",
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
                 The hostname to connect to (default: 'biglake.googleapis.com').
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
    def create_catalog(
        self,
    ) -> Callable[[metastore.CreateCatalogRequest], Awaitable[metastore.Catalog]]:
        r"""Return a callable for the create catalog method over gRPC.

        Creates a new catalog.

        Returns:
            Callable[[~.CreateCatalogRequest],
                    Awaitable[~.Catalog]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_catalog" not in self._stubs:
            self._stubs["create_catalog"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.biglake.v1.MetastoreService/CreateCatalog",
                request_serializer=metastore.CreateCatalogRequest.serialize,
                response_deserializer=metastore.Catalog.deserialize,
            )
        return self._stubs["create_catalog"]

    @property
    def delete_catalog(
        self,
    ) -> Callable[[metastore.DeleteCatalogRequest], Awaitable[metastore.Catalog]]:
        r"""Return a callable for the delete catalog method over gRPC.

        Deletes an existing catalog specified by the catalog
        ID.

        Returns:
            Callable[[~.DeleteCatalogRequest],
                    Awaitable[~.Catalog]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_catalog" not in self._stubs:
            self._stubs["delete_catalog"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.biglake.v1.MetastoreService/DeleteCatalog",
                request_serializer=metastore.DeleteCatalogRequest.serialize,
                response_deserializer=metastore.Catalog.deserialize,
            )
        return self._stubs["delete_catalog"]

    @property
    def get_catalog(
        self,
    ) -> Callable[[metastore.GetCatalogRequest], Awaitable[metastore.Catalog]]:
        r"""Return a callable for the get catalog method over gRPC.

        Gets the catalog specified by the resource name.

        Returns:
            Callable[[~.GetCatalogRequest],
                    Awaitable[~.Catalog]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_catalog" not in self._stubs:
            self._stubs["get_catalog"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.biglake.v1.MetastoreService/GetCatalog",
                request_serializer=metastore.GetCatalogRequest.serialize,
                response_deserializer=metastore.Catalog.deserialize,
            )
        return self._stubs["get_catalog"]

    @property
    def list_catalogs(
        self,
    ) -> Callable[
        [metastore.ListCatalogsRequest], Awaitable[metastore.ListCatalogsResponse]
    ]:
        r"""Return a callable for the list catalogs method over gRPC.

        List all catalogs in a specified project.

        Returns:
            Callable[[~.ListCatalogsRequest],
                    Awaitable[~.ListCatalogsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_catalogs" not in self._stubs:
            self._stubs["list_catalogs"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.biglake.v1.MetastoreService/ListCatalogs",
                request_serializer=metastore.ListCatalogsRequest.serialize,
                response_deserializer=metastore.ListCatalogsResponse.deserialize,
            )
        return self._stubs["list_catalogs"]

    @property
    def create_database(
        self,
    ) -> Callable[[metastore.CreateDatabaseRequest], Awaitable[metastore.Database]]:
        r"""Return a callable for the create database method over gRPC.

        Creates a new database.

        Returns:
            Callable[[~.CreateDatabaseRequest],
                    Awaitable[~.Database]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_database" not in self._stubs:
            self._stubs["create_database"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.biglake.v1.MetastoreService/CreateDatabase",
                request_serializer=metastore.CreateDatabaseRequest.serialize,
                response_deserializer=metastore.Database.deserialize,
            )
        return self._stubs["create_database"]

    @property
    def delete_database(
        self,
    ) -> Callable[[metastore.DeleteDatabaseRequest], Awaitable[metastore.Database]]:
        r"""Return a callable for the delete database method over gRPC.

        Deletes an existing database specified by the
        database ID.

        Returns:
            Callable[[~.DeleteDatabaseRequest],
                    Awaitable[~.Database]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_database" not in self._stubs:
            self._stubs["delete_database"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.biglake.v1.MetastoreService/DeleteDatabase",
                request_serializer=metastore.DeleteDatabaseRequest.serialize,
                response_deserializer=metastore.Database.deserialize,
            )
        return self._stubs["delete_database"]

    @property
    def update_database(
        self,
    ) -> Callable[[metastore.UpdateDatabaseRequest], Awaitable[metastore.Database]]:
        r"""Return a callable for the update database method over gRPC.

        Updates an existing database specified by the
        database ID.

        Returns:
            Callable[[~.UpdateDatabaseRequest],
                    Awaitable[~.Database]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_database" not in self._stubs:
            self._stubs["update_database"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.biglake.v1.MetastoreService/UpdateDatabase",
                request_serializer=metastore.UpdateDatabaseRequest.serialize,
                response_deserializer=metastore.Database.deserialize,
            )
        return self._stubs["update_database"]

    @property
    def get_database(
        self,
    ) -> Callable[[metastore.GetDatabaseRequest], Awaitable[metastore.Database]]:
        r"""Return a callable for the get database method over gRPC.

        Gets the database specified by the resource name.

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
            self._stubs["get_database"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.biglake.v1.MetastoreService/GetDatabase",
                request_serializer=metastore.GetDatabaseRequest.serialize,
                response_deserializer=metastore.Database.deserialize,
            )
        return self._stubs["get_database"]

    @property
    def list_databases(
        self,
    ) -> Callable[
        [metastore.ListDatabasesRequest], Awaitable[metastore.ListDatabasesResponse]
    ]:
        r"""Return a callable for the list databases method over gRPC.

        List all databases in a specified catalog.

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
            self._stubs["list_databases"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.biglake.v1.MetastoreService/ListDatabases",
                request_serializer=metastore.ListDatabasesRequest.serialize,
                response_deserializer=metastore.ListDatabasesResponse.deserialize,
            )
        return self._stubs["list_databases"]

    @property
    def create_table(
        self,
    ) -> Callable[[metastore.CreateTableRequest], Awaitable[metastore.Table]]:
        r"""Return a callable for the create table method over gRPC.

        Creates a new table.

        Returns:
            Callable[[~.CreateTableRequest],
                    Awaitable[~.Table]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_table" not in self._stubs:
            self._stubs["create_table"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.biglake.v1.MetastoreService/CreateTable",
                request_serializer=metastore.CreateTableRequest.serialize,
                response_deserializer=metastore.Table.deserialize,
            )
        return self._stubs["create_table"]

    @property
    def delete_table(
        self,
    ) -> Callable[[metastore.DeleteTableRequest], Awaitable[metastore.Table]]:
        r"""Return a callable for the delete table method over gRPC.

        Deletes an existing table specified by the table ID.

        Returns:
            Callable[[~.DeleteTableRequest],
                    Awaitable[~.Table]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_table" not in self._stubs:
            self._stubs["delete_table"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.biglake.v1.MetastoreService/DeleteTable",
                request_serializer=metastore.DeleteTableRequest.serialize,
                response_deserializer=metastore.Table.deserialize,
            )
        return self._stubs["delete_table"]

    @property
    def update_table(
        self,
    ) -> Callable[[metastore.UpdateTableRequest], Awaitable[metastore.Table]]:
        r"""Return a callable for the update table method over gRPC.

        Updates an existing table specified by the table ID.

        Returns:
            Callable[[~.UpdateTableRequest],
                    Awaitable[~.Table]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_table" not in self._stubs:
            self._stubs["update_table"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.biglake.v1.MetastoreService/UpdateTable",
                request_serializer=metastore.UpdateTableRequest.serialize,
                response_deserializer=metastore.Table.deserialize,
            )
        return self._stubs["update_table"]

    @property
    def rename_table(
        self,
    ) -> Callable[[metastore.RenameTableRequest], Awaitable[metastore.Table]]:
        r"""Return a callable for the rename table method over gRPC.

        Renames an existing table specified by the table ID.

        Returns:
            Callable[[~.RenameTableRequest],
                    Awaitable[~.Table]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "rename_table" not in self._stubs:
            self._stubs["rename_table"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.biglake.v1.MetastoreService/RenameTable",
                request_serializer=metastore.RenameTableRequest.serialize,
                response_deserializer=metastore.Table.deserialize,
            )
        return self._stubs["rename_table"]

    @property
    def get_table(
        self,
    ) -> Callable[[metastore.GetTableRequest], Awaitable[metastore.Table]]:
        r"""Return a callable for the get table method over gRPC.

        Gets the table specified by the resource name.

        Returns:
            Callable[[~.GetTableRequest],
                    Awaitable[~.Table]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_table" not in self._stubs:
            self._stubs["get_table"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.biglake.v1.MetastoreService/GetTable",
                request_serializer=metastore.GetTableRequest.serialize,
                response_deserializer=metastore.Table.deserialize,
            )
        return self._stubs["get_table"]

    @property
    def list_tables(
        self,
    ) -> Callable[
        [metastore.ListTablesRequest], Awaitable[metastore.ListTablesResponse]
    ]:
        r"""Return a callable for the list tables method over gRPC.

        List all tables in a specified database.

        Returns:
            Callable[[~.ListTablesRequest],
                    Awaitable[~.ListTablesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_tables" not in self._stubs:
            self._stubs["list_tables"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.biglake.v1.MetastoreService/ListTables",
                request_serializer=metastore.ListTablesRequest.serialize,
                response_deserializer=metastore.ListTablesResponse.deserialize,
            )
        return self._stubs["list_tables"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.create_catalog: self._wrap_method(
                self.create_catalog,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_catalog: self._wrap_method(
                self.delete_catalog,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_catalog: self._wrap_method(
                self.get_catalog,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_catalogs: self._wrap_method(
                self.list_catalogs,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_database: self._wrap_method(
                self.create_database,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_database: self._wrap_method(
                self.delete_database,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_database: self._wrap_method(
                self.update_database,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_database: self._wrap_method(
                self.get_database,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_databases: self._wrap_method(
                self.list_databases,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_table: self._wrap_method(
                self.create_table,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_table: self._wrap_method(
                self.delete_table,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_table: self._wrap_method(
                self.update_table,
                default_timeout=None,
                client_info=client_info,
            ),
            self.rename_table: self._wrap_method(
                self.rename_table,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_table: self._wrap_method(
                self.get_table,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_tables: self._wrap_method(
                self.list_tables,
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


__all__ = ("MetastoreServiceGrpcAsyncIOTransport",)
