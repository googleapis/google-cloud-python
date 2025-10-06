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
import dataclasses
import json  # type: ignore
import logging
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
import google.protobuf
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.area120.tables_v1alpha1.types import tables

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseTablesServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = logging.getLogger(__name__)

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)

if hasattr(DEFAULT_CLIENT_INFO, "protobuf_runtime_version"):  # pragma: NO COVER
    DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__


class TablesServiceRestInterceptor:
    """Interceptor for TablesService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the TablesServiceRestTransport.

    .. code-block:: python
        class MyCustomTablesServiceInterceptor(TablesServiceRestInterceptor):
            def pre_batch_create_rows(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_create_rows(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_delete_rows(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_batch_update_rows(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_update_rows(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_row(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_row(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_row(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_row(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_row(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_table(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_table(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_workspace(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_workspace(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_rows(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_rows(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_tables(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_tables(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_workspaces(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_workspaces(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_row(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_row(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = TablesServiceRestTransport(interceptor=MyCustomTablesServiceInterceptor())
        client = TablesServiceClient(transport=transport)


    """

    def pre_batch_create_rows(
        self,
        request: tables.BatchCreateRowsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[tables.BatchCreateRowsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for batch_create_rows

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def post_batch_create_rows(
        self, response: tables.BatchCreateRowsResponse
    ) -> tables.BatchCreateRowsResponse:
        """Post-rpc interceptor for batch_create_rows

        DEPRECATED. Please use the `post_batch_create_rows_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the TablesService server but before
        it is returned to user code. This `post_batch_create_rows` interceptor runs
        before the `post_batch_create_rows_with_metadata` interceptor.
        """
        return response

    def post_batch_create_rows_with_metadata(
        self,
        response: tables.BatchCreateRowsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[tables.BatchCreateRowsResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for batch_create_rows

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the TablesService server but before it is returned to user code.

        We recommend only using this `post_batch_create_rows_with_metadata`
        interceptor in new development instead of the `post_batch_create_rows` interceptor.
        When both interceptors are used, this `post_batch_create_rows_with_metadata` interceptor runs after the
        `post_batch_create_rows` interceptor. The (possibly modified) response returned by
        `post_batch_create_rows` will be passed to
        `post_batch_create_rows_with_metadata`.
        """
        return response, metadata

    def pre_batch_delete_rows(
        self,
        request: tables.BatchDeleteRowsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[tables.BatchDeleteRowsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for batch_delete_rows

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def pre_batch_update_rows(
        self,
        request: tables.BatchUpdateRowsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[tables.BatchUpdateRowsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for batch_update_rows

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def post_batch_update_rows(
        self, response: tables.BatchUpdateRowsResponse
    ) -> tables.BatchUpdateRowsResponse:
        """Post-rpc interceptor for batch_update_rows

        DEPRECATED. Please use the `post_batch_update_rows_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the TablesService server but before
        it is returned to user code. This `post_batch_update_rows` interceptor runs
        before the `post_batch_update_rows_with_metadata` interceptor.
        """
        return response

    def post_batch_update_rows_with_metadata(
        self,
        response: tables.BatchUpdateRowsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[tables.BatchUpdateRowsResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for batch_update_rows

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the TablesService server but before it is returned to user code.

        We recommend only using this `post_batch_update_rows_with_metadata`
        interceptor in new development instead of the `post_batch_update_rows` interceptor.
        When both interceptors are used, this `post_batch_update_rows_with_metadata` interceptor runs after the
        `post_batch_update_rows` interceptor. The (possibly modified) response returned by
        `post_batch_update_rows` will be passed to
        `post_batch_update_rows_with_metadata`.
        """
        return response, metadata

    def pre_create_row(
        self,
        request: tables.CreateRowRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[tables.CreateRowRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for create_row

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def post_create_row(self, response: tables.Row) -> tables.Row:
        """Post-rpc interceptor for create_row

        DEPRECATED. Please use the `post_create_row_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the TablesService server but before
        it is returned to user code. This `post_create_row` interceptor runs
        before the `post_create_row_with_metadata` interceptor.
        """
        return response

    def post_create_row_with_metadata(
        self, response: tables.Row, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[tables.Row, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_row

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the TablesService server but before it is returned to user code.

        We recommend only using this `post_create_row_with_metadata`
        interceptor in new development instead of the `post_create_row` interceptor.
        When both interceptors are used, this `post_create_row_with_metadata` interceptor runs after the
        `post_create_row` interceptor. The (possibly modified) response returned by
        `post_create_row` will be passed to
        `post_create_row_with_metadata`.
        """
        return response, metadata

    def pre_delete_row(
        self,
        request: tables.DeleteRowRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[tables.DeleteRowRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for delete_row

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def pre_get_row(
        self,
        request: tables.GetRowRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[tables.GetRowRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_row

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def post_get_row(self, response: tables.Row) -> tables.Row:
        """Post-rpc interceptor for get_row

        DEPRECATED. Please use the `post_get_row_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the TablesService server but before
        it is returned to user code. This `post_get_row` interceptor runs
        before the `post_get_row_with_metadata` interceptor.
        """
        return response

    def post_get_row_with_metadata(
        self, response: tables.Row, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[tables.Row, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_row

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the TablesService server but before it is returned to user code.

        We recommend only using this `post_get_row_with_metadata`
        interceptor in new development instead of the `post_get_row` interceptor.
        When both interceptors are used, this `post_get_row_with_metadata` interceptor runs after the
        `post_get_row` interceptor. The (possibly modified) response returned by
        `post_get_row` will be passed to
        `post_get_row_with_metadata`.
        """
        return response, metadata

    def pre_get_table(
        self,
        request: tables.GetTableRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[tables.GetTableRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_table

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def post_get_table(self, response: tables.Table) -> tables.Table:
        """Post-rpc interceptor for get_table

        DEPRECATED. Please use the `post_get_table_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the TablesService server but before
        it is returned to user code. This `post_get_table` interceptor runs
        before the `post_get_table_with_metadata` interceptor.
        """
        return response

    def post_get_table_with_metadata(
        self, response: tables.Table, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[tables.Table, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_table

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the TablesService server but before it is returned to user code.

        We recommend only using this `post_get_table_with_metadata`
        interceptor in new development instead of the `post_get_table` interceptor.
        When both interceptors are used, this `post_get_table_with_metadata` interceptor runs after the
        `post_get_table` interceptor. The (possibly modified) response returned by
        `post_get_table` will be passed to
        `post_get_table_with_metadata`.
        """
        return response, metadata

    def pre_get_workspace(
        self,
        request: tables.GetWorkspaceRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[tables.GetWorkspaceRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_workspace

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def post_get_workspace(self, response: tables.Workspace) -> tables.Workspace:
        """Post-rpc interceptor for get_workspace

        DEPRECATED. Please use the `post_get_workspace_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the TablesService server but before
        it is returned to user code. This `post_get_workspace` interceptor runs
        before the `post_get_workspace_with_metadata` interceptor.
        """
        return response

    def post_get_workspace_with_metadata(
        self,
        response: tables.Workspace,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[tables.Workspace, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_workspace

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the TablesService server but before it is returned to user code.

        We recommend only using this `post_get_workspace_with_metadata`
        interceptor in new development instead of the `post_get_workspace` interceptor.
        When both interceptors are used, this `post_get_workspace_with_metadata` interceptor runs after the
        `post_get_workspace` interceptor. The (possibly modified) response returned by
        `post_get_workspace` will be passed to
        `post_get_workspace_with_metadata`.
        """
        return response, metadata

    def pre_list_rows(
        self,
        request: tables.ListRowsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[tables.ListRowsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_rows

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def post_list_rows(
        self, response: tables.ListRowsResponse
    ) -> tables.ListRowsResponse:
        """Post-rpc interceptor for list_rows

        DEPRECATED. Please use the `post_list_rows_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the TablesService server but before
        it is returned to user code. This `post_list_rows` interceptor runs
        before the `post_list_rows_with_metadata` interceptor.
        """
        return response

    def post_list_rows_with_metadata(
        self,
        response: tables.ListRowsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[tables.ListRowsResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for list_rows

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the TablesService server but before it is returned to user code.

        We recommend only using this `post_list_rows_with_metadata`
        interceptor in new development instead of the `post_list_rows` interceptor.
        When both interceptors are used, this `post_list_rows_with_metadata` interceptor runs after the
        `post_list_rows` interceptor. The (possibly modified) response returned by
        `post_list_rows` will be passed to
        `post_list_rows_with_metadata`.
        """
        return response, metadata

    def pre_list_tables(
        self,
        request: tables.ListTablesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[tables.ListTablesRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_tables

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def post_list_tables(
        self, response: tables.ListTablesResponse
    ) -> tables.ListTablesResponse:
        """Post-rpc interceptor for list_tables

        DEPRECATED. Please use the `post_list_tables_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the TablesService server but before
        it is returned to user code. This `post_list_tables` interceptor runs
        before the `post_list_tables_with_metadata` interceptor.
        """
        return response

    def post_list_tables_with_metadata(
        self,
        response: tables.ListTablesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[tables.ListTablesResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for list_tables

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the TablesService server but before it is returned to user code.

        We recommend only using this `post_list_tables_with_metadata`
        interceptor in new development instead of the `post_list_tables` interceptor.
        When both interceptors are used, this `post_list_tables_with_metadata` interceptor runs after the
        `post_list_tables` interceptor. The (possibly modified) response returned by
        `post_list_tables` will be passed to
        `post_list_tables_with_metadata`.
        """
        return response, metadata

    def pre_list_workspaces(
        self,
        request: tables.ListWorkspacesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[tables.ListWorkspacesRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_workspaces

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def post_list_workspaces(
        self, response: tables.ListWorkspacesResponse
    ) -> tables.ListWorkspacesResponse:
        """Post-rpc interceptor for list_workspaces

        DEPRECATED. Please use the `post_list_workspaces_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the TablesService server but before
        it is returned to user code. This `post_list_workspaces` interceptor runs
        before the `post_list_workspaces_with_metadata` interceptor.
        """
        return response

    def post_list_workspaces_with_metadata(
        self,
        response: tables.ListWorkspacesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[tables.ListWorkspacesResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for list_workspaces

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the TablesService server but before it is returned to user code.

        We recommend only using this `post_list_workspaces_with_metadata`
        interceptor in new development instead of the `post_list_workspaces` interceptor.
        When both interceptors are used, this `post_list_workspaces_with_metadata` interceptor runs after the
        `post_list_workspaces` interceptor. The (possibly modified) response returned by
        `post_list_workspaces` will be passed to
        `post_list_workspaces_with_metadata`.
        """
        return response, metadata

    def pre_update_row(
        self,
        request: tables.UpdateRowRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[tables.UpdateRowRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for update_row

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def post_update_row(self, response: tables.Row) -> tables.Row:
        """Post-rpc interceptor for update_row

        DEPRECATED. Please use the `post_update_row_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the TablesService server but before
        it is returned to user code. This `post_update_row` interceptor runs
        before the `post_update_row_with_metadata` interceptor.
        """
        return response

    def post_update_row_with_metadata(
        self, response: tables.Row, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[tables.Row, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_row

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the TablesService server but before it is returned to user code.

        We recommend only using this `post_update_row_with_metadata`
        interceptor in new development instead of the `post_update_row` interceptor.
        When both interceptors are used, this `post_update_row_with_metadata` interceptor runs after the
        `post_update_row` interceptor. The (possibly modified) response returned by
        `post_update_row` will be passed to
        `post_update_row_with_metadata`.
        """
        return response, metadata


@dataclasses.dataclass
class TablesServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: TablesServiceRestInterceptor


class TablesServiceRestTransport(_BaseTablesServiceRestTransport):
    """REST backend synchronous transport for TablesService.

    The Tables Service provides an API for reading and updating tables.
    It defines the following resource model:

    - The API has a collection of
      [Table][google.area120.tables.v1alpha1.Table] resources, named
      ``tables/*``

    - Each Table has a collection of
      [Row][google.area120.tables.v1alpha1.Row] resources, named
      ``tables/*/rows/*``

    - The API has a collection of
      [Workspace][google.area120.tables.v1alpha1.Workspace] resources,
      named ``workspaces/*``.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "area120tables.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[TablesServiceRestInterceptor] = None,
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

            credentials_file (Optional[str]): Deprecated. A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided. This argument will be
                removed in the next major version of this library.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            url_scheme=url_scheme,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or TablesServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _BatchCreateRows(
        _BaseTablesServiceRestTransport._BaseBatchCreateRows, TablesServiceRestStub
    ):
        def __hash__(self):
            return hash("TablesServiceRestTransport.BatchCreateRows")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: tables.BatchCreateRowsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> tables.BatchCreateRowsResponse:
            r"""Call the batch create rows method over HTTP.

            Args:
                request (~.tables.BatchCreateRowsRequest):
                    The request object. Request message for
                TablesService.BatchCreateRows.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.tables.BatchCreateRowsResponse:
                    Response message for
                TablesService.BatchCreateRows.

            """

            http_options = (
                _BaseTablesServiceRestTransport._BaseBatchCreateRows._get_http_options()
            )

            request, metadata = self._interceptor.pre_batch_create_rows(
                request, metadata
            )
            transcoded_request = _BaseTablesServiceRestTransport._BaseBatchCreateRows._get_transcoded_request(
                http_options, request
            )

            body = _BaseTablesServiceRestTransport._BaseBatchCreateRows._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseTablesServiceRestTransport._BaseBatchCreateRows._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.area120.tables_v1alpha1.TablesServiceClient.BatchCreateRows",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "BatchCreateRows",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = TablesServiceRestTransport._BatchCreateRows._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = tables.BatchCreateRowsResponse()
            pb_resp = tables.BatchCreateRowsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_batch_create_rows(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_batch_create_rows_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = tables.BatchCreateRowsResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.area120.tables_v1alpha1.TablesServiceClient.batch_create_rows",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "BatchCreateRows",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _BatchDeleteRows(
        _BaseTablesServiceRestTransport._BaseBatchDeleteRows, TablesServiceRestStub
    ):
        def __hash__(self):
            return hash("TablesServiceRestTransport.BatchDeleteRows")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: tables.BatchDeleteRowsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the batch delete rows method over HTTP.

            Args:
                request (~.tables.BatchDeleteRowsRequest):
                    The request object. Request message for
                TablesService.BatchDeleteRows
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseTablesServiceRestTransport._BaseBatchDeleteRows._get_http_options()
            )

            request, metadata = self._interceptor.pre_batch_delete_rows(
                request, metadata
            )
            transcoded_request = _BaseTablesServiceRestTransport._BaseBatchDeleteRows._get_transcoded_request(
                http_options, request
            )

            body = _BaseTablesServiceRestTransport._BaseBatchDeleteRows._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseTablesServiceRestTransport._BaseBatchDeleteRows._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.area120.tables_v1alpha1.TablesServiceClient.BatchDeleteRows",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "BatchDeleteRows",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = TablesServiceRestTransport._BatchDeleteRows._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _BatchUpdateRows(
        _BaseTablesServiceRestTransport._BaseBatchUpdateRows, TablesServiceRestStub
    ):
        def __hash__(self):
            return hash("TablesServiceRestTransport.BatchUpdateRows")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: tables.BatchUpdateRowsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> tables.BatchUpdateRowsResponse:
            r"""Call the batch update rows method over HTTP.

            Args:
                request (~.tables.BatchUpdateRowsRequest):
                    The request object. Request message for
                TablesService.BatchUpdateRows.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.tables.BatchUpdateRowsResponse:
                    Response message for
                TablesService.BatchUpdateRows.

            """

            http_options = (
                _BaseTablesServiceRestTransport._BaseBatchUpdateRows._get_http_options()
            )

            request, metadata = self._interceptor.pre_batch_update_rows(
                request, metadata
            )
            transcoded_request = _BaseTablesServiceRestTransport._BaseBatchUpdateRows._get_transcoded_request(
                http_options, request
            )

            body = _BaseTablesServiceRestTransport._BaseBatchUpdateRows._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseTablesServiceRestTransport._BaseBatchUpdateRows._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.area120.tables_v1alpha1.TablesServiceClient.BatchUpdateRows",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "BatchUpdateRows",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = TablesServiceRestTransport._BatchUpdateRows._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = tables.BatchUpdateRowsResponse()
            pb_resp = tables.BatchUpdateRowsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_batch_update_rows(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_batch_update_rows_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = tables.BatchUpdateRowsResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.area120.tables_v1alpha1.TablesServiceClient.batch_update_rows",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "BatchUpdateRows",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateRow(
        _BaseTablesServiceRestTransport._BaseCreateRow, TablesServiceRestStub
    ):
        def __hash__(self):
            return hash("TablesServiceRestTransport.CreateRow")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: tables.CreateRowRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> tables.Row:
            r"""Call the create row method over HTTP.

            Args:
                request (~.tables.CreateRowRequest):
                    The request object. Request message for
                TablesService.CreateRow.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.tables.Row:
                    A single row in a table.
            """

            http_options = (
                _BaseTablesServiceRestTransport._BaseCreateRow._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_row(request, metadata)
            transcoded_request = (
                _BaseTablesServiceRestTransport._BaseCreateRow._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseTablesServiceRestTransport._BaseCreateRow._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseTablesServiceRestTransport._BaseCreateRow._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.area120.tables_v1alpha1.TablesServiceClient.CreateRow",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "CreateRow",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = TablesServiceRestTransport._CreateRow._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = tables.Row()
            pb_resp = tables.Row.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_row(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_row_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = tables.Row.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.area120.tables_v1alpha1.TablesServiceClient.create_row",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "CreateRow",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteRow(
        _BaseTablesServiceRestTransport._BaseDeleteRow, TablesServiceRestStub
    ):
        def __hash__(self):
            return hash("TablesServiceRestTransport.DeleteRow")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: tables.DeleteRowRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete row method over HTTP.

            Args:
                request (~.tables.DeleteRowRequest):
                    The request object. Request message for
                TablesService.DeleteRow
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseTablesServiceRestTransport._BaseDeleteRow._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_row(request, metadata)
            transcoded_request = (
                _BaseTablesServiceRestTransport._BaseDeleteRow._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseTablesServiceRestTransport._BaseDeleteRow._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.area120.tables_v1alpha1.TablesServiceClient.DeleteRow",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "DeleteRow",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = TablesServiceRestTransport._DeleteRow._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _GetRow(_BaseTablesServiceRestTransport._BaseGetRow, TablesServiceRestStub):
        def __hash__(self):
            return hash("TablesServiceRestTransport.GetRow")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: tables.GetRowRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> tables.Row:
            r"""Call the get row method over HTTP.

            Args:
                request (~.tables.GetRowRequest):
                    The request object. Request message for
                TablesService.GetRow.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.tables.Row:
                    A single row in a table.
            """

            http_options = (
                _BaseTablesServiceRestTransport._BaseGetRow._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_row(request, metadata)
            transcoded_request = (
                _BaseTablesServiceRestTransport._BaseGetRow._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseTablesServiceRestTransport._BaseGetRow._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.area120.tables_v1alpha1.TablesServiceClient.GetRow",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "GetRow",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = TablesServiceRestTransport._GetRow._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = tables.Row()
            pb_resp = tables.Row.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_row(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_row_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = tables.Row.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.area120.tables_v1alpha1.TablesServiceClient.get_row",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "GetRow",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetTable(
        _BaseTablesServiceRestTransport._BaseGetTable, TablesServiceRestStub
    ):
        def __hash__(self):
            return hash("TablesServiceRestTransport.GetTable")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: tables.GetTableRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> tables.Table:
            r"""Call the get table method over HTTP.

            Args:
                request (~.tables.GetTableRequest):
                    The request object. Request message for
                TablesService.GetTable.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.tables.Table:
                    A single table.
            """

            http_options = (
                _BaseTablesServiceRestTransport._BaseGetTable._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_table(request, metadata)
            transcoded_request = (
                _BaseTablesServiceRestTransport._BaseGetTable._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseTablesServiceRestTransport._BaseGetTable._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.area120.tables_v1alpha1.TablesServiceClient.GetTable",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "GetTable",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = TablesServiceRestTransport._GetTable._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = tables.Table()
            pb_resp = tables.Table.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_table(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_table_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = tables.Table.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.area120.tables_v1alpha1.TablesServiceClient.get_table",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "GetTable",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetWorkspace(
        _BaseTablesServiceRestTransport._BaseGetWorkspace, TablesServiceRestStub
    ):
        def __hash__(self):
            return hash("TablesServiceRestTransport.GetWorkspace")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: tables.GetWorkspaceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> tables.Workspace:
            r"""Call the get workspace method over HTTP.

            Args:
                request (~.tables.GetWorkspaceRequest):
                    The request object. Request message for
                TablesService.GetWorkspace.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.tables.Workspace:
                    A single workspace.
            """

            http_options = (
                _BaseTablesServiceRestTransport._BaseGetWorkspace._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_workspace(request, metadata)
            transcoded_request = _BaseTablesServiceRestTransport._BaseGetWorkspace._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseTablesServiceRestTransport._BaseGetWorkspace._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.area120.tables_v1alpha1.TablesServiceClient.GetWorkspace",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "GetWorkspace",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = TablesServiceRestTransport._GetWorkspace._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = tables.Workspace()
            pb_resp = tables.Workspace.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_workspace(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_workspace_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = tables.Workspace.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.area120.tables_v1alpha1.TablesServiceClient.get_workspace",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "GetWorkspace",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListRows(
        _BaseTablesServiceRestTransport._BaseListRows, TablesServiceRestStub
    ):
        def __hash__(self):
            return hash("TablesServiceRestTransport.ListRows")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: tables.ListRowsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> tables.ListRowsResponse:
            r"""Call the list rows method over HTTP.

            Args:
                request (~.tables.ListRowsRequest):
                    The request object. Request message for
                TablesService.ListRows.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.tables.ListRowsResponse:
                    Response message for
                TablesService.ListRows.

            """

            http_options = (
                _BaseTablesServiceRestTransport._BaseListRows._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_rows(request, metadata)
            transcoded_request = (
                _BaseTablesServiceRestTransport._BaseListRows._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseTablesServiceRestTransport._BaseListRows._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.area120.tables_v1alpha1.TablesServiceClient.ListRows",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "ListRows",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = TablesServiceRestTransport._ListRows._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = tables.ListRowsResponse()
            pb_resp = tables.ListRowsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_rows(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_rows_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = tables.ListRowsResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.area120.tables_v1alpha1.TablesServiceClient.list_rows",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "ListRows",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListTables(
        _BaseTablesServiceRestTransport._BaseListTables, TablesServiceRestStub
    ):
        def __hash__(self):
            return hash("TablesServiceRestTransport.ListTables")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: tables.ListTablesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> tables.ListTablesResponse:
            r"""Call the list tables method over HTTP.

            Args:
                request (~.tables.ListTablesRequest):
                    The request object. Request message for
                TablesService.ListTables.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.tables.ListTablesResponse:
                    Response message for
                TablesService.ListTables.

            """

            http_options = (
                _BaseTablesServiceRestTransport._BaseListTables._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_tables(request, metadata)
            transcoded_request = (
                _BaseTablesServiceRestTransport._BaseListTables._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseTablesServiceRestTransport._BaseListTables._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.area120.tables_v1alpha1.TablesServiceClient.ListTables",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "ListTables",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = TablesServiceRestTransport._ListTables._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = tables.ListTablesResponse()
            pb_resp = tables.ListTablesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_tables(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_tables_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = tables.ListTablesResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.area120.tables_v1alpha1.TablesServiceClient.list_tables",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "ListTables",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListWorkspaces(
        _BaseTablesServiceRestTransport._BaseListWorkspaces, TablesServiceRestStub
    ):
        def __hash__(self):
            return hash("TablesServiceRestTransport.ListWorkspaces")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: tables.ListWorkspacesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> tables.ListWorkspacesResponse:
            r"""Call the list workspaces method over HTTP.

            Args:
                request (~.tables.ListWorkspacesRequest):
                    The request object. Request message for
                TablesService.ListWorkspaces.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.tables.ListWorkspacesResponse:
                    Response message for
                TablesService.ListWorkspaces.

            """

            http_options = (
                _BaseTablesServiceRestTransport._BaseListWorkspaces._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_workspaces(request, metadata)
            transcoded_request = _BaseTablesServiceRestTransport._BaseListWorkspaces._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseTablesServiceRestTransport._BaseListWorkspaces._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.area120.tables_v1alpha1.TablesServiceClient.ListWorkspaces",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "ListWorkspaces",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = TablesServiceRestTransport._ListWorkspaces._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = tables.ListWorkspacesResponse()
            pb_resp = tables.ListWorkspacesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_workspaces(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_workspaces_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = tables.ListWorkspacesResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.area120.tables_v1alpha1.TablesServiceClient.list_workspaces",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "ListWorkspaces",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateRow(
        _BaseTablesServiceRestTransport._BaseUpdateRow, TablesServiceRestStub
    ):
        def __hash__(self):
            return hash("TablesServiceRestTransport.UpdateRow")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: tables.UpdateRowRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> tables.Row:
            r"""Call the update row method over HTTP.

            Args:
                request (~.tables.UpdateRowRequest):
                    The request object. Request message for
                TablesService.UpdateRow.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.tables.Row:
                    A single row in a table.
            """

            http_options = (
                _BaseTablesServiceRestTransport._BaseUpdateRow._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_row(request, metadata)
            transcoded_request = (
                _BaseTablesServiceRestTransport._BaseUpdateRow._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseTablesServiceRestTransport._BaseUpdateRow._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseTablesServiceRestTransport._BaseUpdateRow._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.area120.tables_v1alpha1.TablesServiceClient.UpdateRow",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "UpdateRow",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = TablesServiceRestTransport._UpdateRow._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = tables.Row()
            pb_resp = tables.Row.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_row(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_row_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = tables.Row.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.area120.tables_v1alpha1.TablesServiceClient.update_row",
                    extra={
                        "serviceName": "google.area120.tables.v1alpha1.TablesService",
                        "rpcName": "UpdateRow",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def batch_create_rows(
        self,
    ) -> Callable[[tables.BatchCreateRowsRequest], tables.BatchCreateRowsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchCreateRows(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_delete_rows(
        self,
    ) -> Callable[[tables.BatchDeleteRowsRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchDeleteRows(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_update_rows(
        self,
    ) -> Callable[[tables.BatchUpdateRowsRequest], tables.BatchUpdateRowsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchUpdateRows(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_row(self) -> Callable[[tables.CreateRowRequest], tables.Row]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRow(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_row(self) -> Callable[[tables.DeleteRowRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteRow(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_row(self) -> Callable[[tables.GetRowRequest], tables.Row]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRow(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_table(self) -> Callable[[tables.GetTableRequest], tables.Table]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetTable(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_workspace(self) -> Callable[[tables.GetWorkspaceRequest], tables.Workspace]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetWorkspace(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_rows(self) -> Callable[[tables.ListRowsRequest], tables.ListRowsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRows(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_tables(
        self,
    ) -> Callable[[tables.ListTablesRequest], tables.ListTablesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListTables(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_workspaces(
        self,
    ) -> Callable[[tables.ListWorkspacesRequest], tables.ListWorkspacesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListWorkspaces(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_row(self) -> Callable[[tables.UpdateRowRequest], tables.Row]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateRow(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("TablesServiceRestTransport",)
