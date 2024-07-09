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
from google.api_core import gapic_v1, grpc_helpers_async
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.area120.tables_v1alpha1.types import tables

from .base import DEFAULT_CLIENT_INFO, TablesServiceTransport
from .grpc import TablesServiceGrpcTransport


class TablesServiceGrpcAsyncIOTransport(TablesServiceTransport):
    """gRPC AsyncIO backend transport for TablesService.

    The Tables Service provides an API for reading and updating tables.
    It defines the following resource model:

    -  The API has a collection of
       [Table][google.area120.tables.v1alpha1.Table] resources, named
       ``tables/*``

    -  Each Table has a collection of
       [Row][google.area120.tables.v1alpha1.Row] resources, named
       ``tables/*/rows/*``

    -  The API has a collection of
       [Workspace][google.area120.tables.v1alpha1.Workspace] resources,
       named ``workspaces/*``.

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
        host: str = "area120tables.googleapis.com",
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
        host: str = "area120tables.googleapis.com",
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
                 The hostname to connect to (default: 'area120tables.googleapis.com').
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
    def get_table(self) -> Callable[[tables.GetTableRequest], Awaitable[tables.Table]]:
        r"""Return a callable for the get table method over gRPC.

        Gets a table. Returns NOT_FOUND if the table does not exist.

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
                "/google.area120.tables.v1alpha1.TablesService/GetTable",
                request_serializer=tables.GetTableRequest.serialize,
                response_deserializer=tables.Table.deserialize,
            )
        return self._stubs["get_table"]

    @property
    def list_tables(
        self,
    ) -> Callable[[tables.ListTablesRequest], Awaitable[tables.ListTablesResponse]]:
        r"""Return a callable for the list tables method over gRPC.

        Lists tables for the user.

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
                "/google.area120.tables.v1alpha1.TablesService/ListTables",
                request_serializer=tables.ListTablesRequest.serialize,
                response_deserializer=tables.ListTablesResponse.deserialize,
            )
        return self._stubs["list_tables"]

    @property
    def get_workspace(
        self,
    ) -> Callable[[tables.GetWorkspaceRequest], Awaitable[tables.Workspace]]:
        r"""Return a callable for the get workspace method over gRPC.

        Gets a workspace. Returns NOT_FOUND if the workspace does not
        exist.

        Returns:
            Callable[[~.GetWorkspaceRequest],
                    Awaitable[~.Workspace]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_workspace" not in self._stubs:
            self._stubs["get_workspace"] = self.grpc_channel.unary_unary(
                "/google.area120.tables.v1alpha1.TablesService/GetWorkspace",
                request_serializer=tables.GetWorkspaceRequest.serialize,
                response_deserializer=tables.Workspace.deserialize,
            )
        return self._stubs["get_workspace"]

    @property
    def list_workspaces(
        self,
    ) -> Callable[
        [tables.ListWorkspacesRequest], Awaitable[tables.ListWorkspacesResponse]
    ]:
        r"""Return a callable for the list workspaces method over gRPC.

        Lists workspaces for the user.

        Returns:
            Callable[[~.ListWorkspacesRequest],
                    Awaitable[~.ListWorkspacesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_workspaces" not in self._stubs:
            self._stubs["list_workspaces"] = self.grpc_channel.unary_unary(
                "/google.area120.tables.v1alpha1.TablesService/ListWorkspaces",
                request_serializer=tables.ListWorkspacesRequest.serialize,
                response_deserializer=tables.ListWorkspacesResponse.deserialize,
            )
        return self._stubs["list_workspaces"]

    @property
    def get_row(self) -> Callable[[tables.GetRowRequest], Awaitable[tables.Row]]:
        r"""Return a callable for the get row method over gRPC.

        Gets a row. Returns NOT_FOUND if the row does not exist in the
        table.

        Returns:
            Callable[[~.GetRowRequest],
                    Awaitable[~.Row]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_row" not in self._stubs:
            self._stubs["get_row"] = self.grpc_channel.unary_unary(
                "/google.area120.tables.v1alpha1.TablesService/GetRow",
                request_serializer=tables.GetRowRequest.serialize,
                response_deserializer=tables.Row.deserialize,
            )
        return self._stubs["get_row"]

    @property
    def list_rows(
        self,
    ) -> Callable[[tables.ListRowsRequest], Awaitable[tables.ListRowsResponse]]:
        r"""Return a callable for the list rows method over gRPC.

        Lists rows in a table. Returns NOT_FOUND if the table does not
        exist.

        Returns:
            Callable[[~.ListRowsRequest],
                    Awaitable[~.ListRowsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_rows" not in self._stubs:
            self._stubs["list_rows"] = self.grpc_channel.unary_unary(
                "/google.area120.tables.v1alpha1.TablesService/ListRows",
                request_serializer=tables.ListRowsRequest.serialize,
                response_deserializer=tables.ListRowsResponse.deserialize,
            )
        return self._stubs["list_rows"]

    @property
    def create_row(self) -> Callable[[tables.CreateRowRequest], Awaitable[tables.Row]]:
        r"""Return a callable for the create row method over gRPC.

        Creates a row.

        Returns:
            Callable[[~.CreateRowRequest],
                    Awaitable[~.Row]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_row" not in self._stubs:
            self._stubs["create_row"] = self.grpc_channel.unary_unary(
                "/google.area120.tables.v1alpha1.TablesService/CreateRow",
                request_serializer=tables.CreateRowRequest.serialize,
                response_deserializer=tables.Row.deserialize,
            )
        return self._stubs["create_row"]

    @property
    def batch_create_rows(
        self,
    ) -> Callable[
        [tables.BatchCreateRowsRequest], Awaitable[tables.BatchCreateRowsResponse]
    ]:
        r"""Return a callable for the batch create rows method over gRPC.

        Creates multiple rows.

        Returns:
            Callable[[~.BatchCreateRowsRequest],
                    Awaitable[~.BatchCreateRowsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_create_rows" not in self._stubs:
            self._stubs["batch_create_rows"] = self.grpc_channel.unary_unary(
                "/google.area120.tables.v1alpha1.TablesService/BatchCreateRows",
                request_serializer=tables.BatchCreateRowsRequest.serialize,
                response_deserializer=tables.BatchCreateRowsResponse.deserialize,
            )
        return self._stubs["batch_create_rows"]

    @property
    def update_row(self) -> Callable[[tables.UpdateRowRequest], Awaitable[tables.Row]]:
        r"""Return a callable for the update row method over gRPC.

        Updates a row.

        Returns:
            Callable[[~.UpdateRowRequest],
                    Awaitable[~.Row]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_row" not in self._stubs:
            self._stubs["update_row"] = self.grpc_channel.unary_unary(
                "/google.area120.tables.v1alpha1.TablesService/UpdateRow",
                request_serializer=tables.UpdateRowRequest.serialize,
                response_deserializer=tables.Row.deserialize,
            )
        return self._stubs["update_row"]

    @property
    def batch_update_rows(
        self,
    ) -> Callable[
        [tables.BatchUpdateRowsRequest], Awaitable[tables.BatchUpdateRowsResponse]
    ]:
        r"""Return a callable for the batch update rows method over gRPC.

        Updates multiple rows.

        Returns:
            Callable[[~.BatchUpdateRowsRequest],
                    Awaitable[~.BatchUpdateRowsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_update_rows" not in self._stubs:
            self._stubs["batch_update_rows"] = self.grpc_channel.unary_unary(
                "/google.area120.tables.v1alpha1.TablesService/BatchUpdateRows",
                request_serializer=tables.BatchUpdateRowsRequest.serialize,
                response_deserializer=tables.BatchUpdateRowsResponse.deserialize,
            )
        return self._stubs["batch_update_rows"]

    @property
    def delete_row(
        self,
    ) -> Callable[[tables.DeleteRowRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete row method over gRPC.

        Deletes a row.

        Returns:
            Callable[[~.DeleteRowRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_row" not in self._stubs:
            self._stubs["delete_row"] = self.grpc_channel.unary_unary(
                "/google.area120.tables.v1alpha1.TablesService/DeleteRow",
                request_serializer=tables.DeleteRowRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_row"]

    @property
    def batch_delete_rows(
        self,
    ) -> Callable[[tables.BatchDeleteRowsRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the batch delete rows method over gRPC.

        Deletes multiple rows.

        Returns:
            Callable[[~.BatchDeleteRowsRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_delete_rows" not in self._stubs:
            self._stubs["batch_delete_rows"] = self.grpc_channel.unary_unary(
                "/google.area120.tables.v1alpha1.TablesService/BatchDeleteRows",
                request_serializer=tables.BatchDeleteRowsRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["batch_delete_rows"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.get_table: gapic_v1.method_async.wrap_method(
                self.get_table,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_tables: gapic_v1.method_async.wrap_method(
                self.list_tables,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_workspace: gapic_v1.method_async.wrap_method(
                self.get_workspace,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_workspaces: gapic_v1.method_async.wrap_method(
                self.list_workspaces,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_row: gapic_v1.method_async.wrap_method(
                self.get_row,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_rows: gapic_v1.method_async.wrap_method(
                self.list_rows,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_row: gapic_v1.method_async.wrap_method(
                self.create_row,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.batch_create_rows: gapic_v1.method_async.wrap_method(
                self.batch_create_rows,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_row: gapic_v1.method_async.wrap_method(
                self.update_row,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.batch_update_rows: gapic_v1.method_async.wrap_method(
                self.batch_update_rows,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_row: gapic_v1.method_async.wrap_method(
                self.delete_row,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.batch_delete_rows: gapic_v1.method_async.wrap_method(
                self.batch_delete_rows,
                default_timeout=60.0,
                client_info=client_info,
            ),
        }

    def close(self):
        return self.grpc_channel.close()


__all__ = ("TablesServiceGrpcAsyncIOTransport",)
