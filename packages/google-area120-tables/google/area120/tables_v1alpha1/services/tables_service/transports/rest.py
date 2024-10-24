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

import dataclasses
import json  # type: ignore
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
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


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


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
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[tables.BatchCreateRowsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_create_rows

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def post_batch_create_rows(
        self, response: tables.BatchCreateRowsResponse
    ) -> tables.BatchCreateRowsResponse:
        """Post-rpc interceptor for batch_create_rows

        Override in a subclass to manipulate the response
        after it is returned by the TablesService server but before
        it is returned to user code.
        """
        return response

    def pre_batch_delete_rows(
        self,
        request: tables.BatchDeleteRowsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[tables.BatchDeleteRowsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_delete_rows

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def pre_batch_update_rows(
        self,
        request: tables.BatchUpdateRowsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[tables.BatchUpdateRowsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_update_rows

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def post_batch_update_rows(
        self, response: tables.BatchUpdateRowsResponse
    ) -> tables.BatchUpdateRowsResponse:
        """Post-rpc interceptor for batch_update_rows

        Override in a subclass to manipulate the response
        after it is returned by the TablesService server but before
        it is returned to user code.
        """
        return response

    def pre_create_row(
        self, request: tables.CreateRowRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[tables.CreateRowRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_row

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def post_create_row(self, response: tables.Row) -> tables.Row:
        """Post-rpc interceptor for create_row

        Override in a subclass to manipulate the response
        after it is returned by the TablesService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_row(
        self, request: tables.DeleteRowRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[tables.DeleteRowRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_row

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def pre_get_row(
        self, request: tables.GetRowRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[tables.GetRowRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_row

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def post_get_row(self, response: tables.Row) -> tables.Row:
        """Post-rpc interceptor for get_row

        Override in a subclass to manipulate the response
        after it is returned by the TablesService server but before
        it is returned to user code.
        """
        return response

    def pre_get_table(
        self, request: tables.GetTableRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[tables.GetTableRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_table

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def post_get_table(self, response: tables.Table) -> tables.Table:
        """Post-rpc interceptor for get_table

        Override in a subclass to manipulate the response
        after it is returned by the TablesService server but before
        it is returned to user code.
        """
        return response

    def pre_get_workspace(
        self, request: tables.GetWorkspaceRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[tables.GetWorkspaceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_workspace

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def post_get_workspace(self, response: tables.Workspace) -> tables.Workspace:
        """Post-rpc interceptor for get_workspace

        Override in a subclass to manipulate the response
        after it is returned by the TablesService server but before
        it is returned to user code.
        """
        return response

    def pre_list_rows(
        self, request: tables.ListRowsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[tables.ListRowsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_rows

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def post_list_rows(
        self, response: tables.ListRowsResponse
    ) -> tables.ListRowsResponse:
        """Post-rpc interceptor for list_rows

        Override in a subclass to manipulate the response
        after it is returned by the TablesService server but before
        it is returned to user code.
        """
        return response

    def pre_list_tables(
        self, request: tables.ListTablesRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[tables.ListTablesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_tables

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def post_list_tables(
        self, response: tables.ListTablesResponse
    ) -> tables.ListTablesResponse:
        """Post-rpc interceptor for list_tables

        Override in a subclass to manipulate the response
        after it is returned by the TablesService server but before
        it is returned to user code.
        """
        return response

    def pre_list_workspaces(
        self, request: tables.ListWorkspacesRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[tables.ListWorkspacesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_workspaces

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def post_list_workspaces(
        self, response: tables.ListWorkspacesResponse
    ) -> tables.ListWorkspacesResponse:
        """Post-rpc interceptor for list_workspaces

        Override in a subclass to manipulate the response
        after it is returned by the TablesService server but before
        it is returned to user code.
        """
        return response

    def pre_update_row(
        self, request: tables.UpdateRowRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[tables.UpdateRowRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_row

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TablesService server.
        """
        return request, metadata

    def post_update_row(self, response: tables.Row) -> tables.Row:
        """Post-rpc interceptor for update_row

        Override in a subclass to manipulate the response
        after it is returned by the TablesService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class TablesServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: TablesServiceRestInterceptor


class TablesServiceRestTransport(_BaseTablesServiceRestTransport):
    """REST backend synchronous transport for TablesService.

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

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
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
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> tables.BatchCreateRowsResponse:
            r"""Call the batch create rows method over HTTP.

            Args:
                request (~.tables.BatchCreateRowsRequest):
                    The request object. Request message for
                TablesService.BatchCreateRows.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

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
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the batch delete rows method over HTTP.

            Args:
                request (~.tables.BatchDeleteRowsRequest):
                    The request object. Request message for
                TablesService.BatchDeleteRows
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
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
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> tables.BatchUpdateRowsResponse:
            r"""Call the batch update rows method over HTTP.

            Args:
                request (~.tables.BatchUpdateRowsRequest):
                    The request object. Request message for
                TablesService.BatchUpdateRows.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

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
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> tables.Row:
            r"""Call the create row method over HTTP.

            Args:
                request (~.tables.CreateRowRequest):
                    The request object. Request message for
                TablesService.CreateRow.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

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
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete row method over HTTP.

            Args:
                request (~.tables.DeleteRowRequest):
                    The request object. Request message for
                TablesService.DeleteRow
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
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
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> tables.Row:
            r"""Call the get row method over HTTP.

            Args:
                request (~.tables.GetRowRequest):
                    The request object. Request message for
                TablesService.GetRow.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

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
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> tables.Table:
            r"""Call the get table method over HTTP.

            Args:
                request (~.tables.GetTableRequest):
                    The request object. Request message for
                TablesService.GetTable.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

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
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> tables.Workspace:
            r"""Call the get workspace method over HTTP.

            Args:
                request (~.tables.GetWorkspaceRequest):
                    The request object. Request message for
                TablesService.GetWorkspace.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

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
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> tables.ListRowsResponse:
            r"""Call the list rows method over HTTP.

            Args:
                request (~.tables.ListRowsRequest):
                    The request object. Request message for
                TablesService.ListRows.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

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
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> tables.ListTablesResponse:
            r"""Call the list tables method over HTTP.

            Args:
                request (~.tables.ListTablesRequest):
                    The request object. Request message for
                TablesService.ListTables.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

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
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> tables.ListWorkspacesResponse:
            r"""Call the list workspaces method over HTTP.

            Args:
                request (~.tables.ListWorkspacesRequest):
                    The request object. Request message for
                TablesService.ListWorkspaces.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

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
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> tables.Row:
            r"""Call the update row method over HTTP.

            Args:
                request (~.tables.UpdateRowRequest):
                    The request object. Request message for
                TablesService.UpdateRow.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

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
