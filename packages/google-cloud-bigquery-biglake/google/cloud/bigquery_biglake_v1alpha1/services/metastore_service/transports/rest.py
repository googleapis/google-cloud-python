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

from google.cloud.bigquery_biglake_v1alpha1.types import metastore

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseMetastoreServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class MetastoreServiceRestInterceptor:
    """Interceptor for MetastoreService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the MetastoreServiceRestTransport.

    .. code-block:: python
        class MyCustomMetastoreServiceInterceptor(MetastoreServiceRestInterceptor):
            def pre_check_lock(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_check_lock(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_catalog(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_catalog(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_database(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_database(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_lock(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_lock(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_table(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_table(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_catalog(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_catalog(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_database(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_database(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_lock(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_table(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_table(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_catalog(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_catalog(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_database(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_database(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_table(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_table(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_catalogs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_catalogs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_databases(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_databases(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_locks(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_locks(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_tables(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_tables(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_rename_table(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_rename_table(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_database(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_database(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_table(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_table(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = MetastoreServiceRestTransport(interceptor=MyCustomMetastoreServiceInterceptor())
        client = MetastoreServiceClient(transport=transport)


    """

    def pre_check_lock(
        self, request: metastore.CheckLockRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[metastore.CheckLockRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for check_lock

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastoreService server.
        """
        return request, metadata

    def post_check_lock(self, response: metastore.Lock) -> metastore.Lock:
        """Post-rpc interceptor for check_lock

        Override in a subclass to manipulate the response
        after it is returned by the MetastoreService server but before
        it is returned to user code.
        """
        return response

    def pre_create_catalog(
        self,
        request: metastore.CreateCatalogRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[metastore.CreateCatalogRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_catalog

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastoreService server.
        """
        return request, metadata

    def post_create_catalog(self, response: metastore.Catalog) -> metastore.Catalog:
        """Post-rpc interceptor for create_catalog

        Override in a subclass to manipulate the response
        after it is returned by the MetastoreService server but before
        it is returned to user code.
        """
        return response

    def pre_create_database(
        self,
        request: metastore.CreateDatabaseRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[metastore.CreateDatabaseRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_database

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastoreService server.
        """
        return request, metadata

    def post_create_database(self, response: metastore.Database) -> metastore.Database:
        """Post-rpc interceptor for create_database

        Override in a subclass to manipulate the response
        after it is returned by the MetastoreService server but before
        it is returned to user code.
        """
        return response

    def pre_create_lock(
        self, request: metastore.CreateLockRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[metastore.CreateLockRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_lock

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastoreService server.
        """
        return request, metadata

    def post_create_lock(self, response: metastore.Lock) -> metastore.Lock:
        """Post-rpc interceptor for create_lock

        Override in a subclass to manipulate the response
        after it is returned by the MetastoreService server but before
        it is returned to user code.
        """
        return response

    def pre_create_table(
        self, request: metastore.CreateTableRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[metastore.CreateTableRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_table

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastoreService server.
        """
        return request, metadata

    def post_create_table(self, response: metastore.Table) -> metastore.Table:
        """Post-rpc interceptor for create_table

        Override in a subclass to manipulate the response
        after it is returned by the MetastoreService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_catalog(
        self,
        request: metastore.DeleteCatalogRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[metastore.DeleteCatalogRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_catalog

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastoreService server.
        """
        return request, metadata

    def post_delete_catalog(self, response: metastore.Catalog) -> metastore.Catalog:
        """Post-rpc interceptor for delete_catalog

        Override in a subclass to manipulate the response
        after it is returned by the MetastoreService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_database(
        self,
        request: metastore.DeleteDatabaseRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[metastore.DeleteDatabaseRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_database

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastoreService server.
        """
        return request, metadata

    def post_delete_database(self, response: metastore.Database) -> metastore.Database:
        """Post-rpc interceptor for delete_database

        Override in a subclass to manipulate the response
        after it is returned by the MetastoreService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_lock(
        self, request: metastore.DeleteLockRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[metastore.DeleteLockRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_lock

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastoreService server.
        """
        return request, metadata

    def pre_delete_table(
        self, request: metastore.DeleteTableRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[metastore.DeleteTableRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_table

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastoreService server.
        """
        return request, metadata

    def post_delete_table(self, response: metastore.Table) -> metastore.Table:
        """Post-rpc interceptor for delete_table

        Override in a subclass to manipulate the response
        after it is returned by the MetastoreService server but before
        it is returned to user code.
        """
        return response

    def pre_get_catalog(
        self, request: metastore.GetCatalogRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[metastore.GetCatalogRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_catalog

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastoreService server.
        """
        return request, metadata

    def post_get_catalog(self, response: metastore.Catalog) -> metastore.Catalog:
        """Post-rpc interceptor for get_catalog

        Override in a subclass to manipulate the response
        after it is returned by the MetastoreService server but before
        it is returned to user code.
        """
        return response

    def pre_get_database(
        self, request: metastore.GetDatabaseRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[metastore.GetDatabaseRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_database

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastoreService server.
        """
        return request, metadata

    def post_get_database(self, response: metastore.Database) -> metastore.Database:
        """Post-rpc interceptor for get_database

        Override in a subclass to manipulate the response
        after it is returned by the MetastoreService server but before
        it is returned to user code.
        """
        return response

    def pre_get_table(
        self, request: metastore.GetTableRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[metastore.GetTableRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_table

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastoreService server.
        """
        return request, metadata

    def post_get_table(self, response: metastore.Table) -> metastore.Table:
        """Post-rpc interceptor for get_table

        Override in a subclass to manipulate the response
        after it is returned by the MetastoreService server but before
        it is returned to user code.
        """
        return response

    def pre_list_catalogs(
        self,
        request: metastore.ListCatalogsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[metastore.ListCatalogsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_catalogs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastoreService server.
        """
        return request, metadata

    def post_list_catalogs(
        self, response: metastore.ListCatalogsResponse
    ) -> metastore.ListCatalogsResponse:
        """Post-rpc interceptor for list_catalogs

        Override in a subclass to manipulate the response
        after it is returned by the MetastoreService server but before
        it is returned to user code.
        """
        return response

    def pre_list_databases(
        self,
        request: metastore.ListDatabasesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[metastore.ListDatabasesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_databases

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastoreService server.
        """
        return request, metadata

    def post_list_databases(
        self, response: metastore.ListDatabasesResponse
    ) -> metastore.ListDatabasesResponse:
        """Post-rpc interceptor for list_databases

        Override in a subclass to manipulate the response
        after it is returned by the MetastoreService server but before
        it is returned to user code.
        """
        return response

    def pre_list_locks(
        self, request: metastore.ListLocksRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[metastore.ListLocksRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_locks

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastoreService server.
        """
        return request, metadata

    def post_list_locks(
        self, response: metastore.ListLocksResponse
    ) -> metastore.ListLocksResponse:
        """Post-rpc interceptor for list_locks

        Override in a subclass to manipulate the response
        after it is returned by the MetastoreService server but before
        it is returned to user code.
        """
        return response

    def pre_list_tables(
        self, request: metastore.ListTablesRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[metastore.ListTablesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_tables

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastoreService server.
        """
        return request, metadata

    def post_list_tables(
        self, response: metastore.ListTablesResponse
    ) -> metastore.ListTablesResponse:
        """Post-rpc interceptor for list_tables

        Override in a subclass to manipulate the response
        after it is returned by the MetastoreService server but before
        it is returned to user code.
        """
        return response

    def pre_rename_table(
        self, request: metastore.RenameTableRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[metastore.RenameTableRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for rename_table

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastoreService server.
        """
        return request, metadata

    def post_rename_table(self, response: metastore.Table) -> metastore.Table:
        """Post-rpc interceptor for rename_table

        Override in a subclass to manipulate the response
        after it is returned by the MetastoreService server but before
        it is returned to user code.
        """
        return response

    def pre_update_database(
        self,
        request: metastore.UpdateDatabaseRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[metastore.UpdateDatabaseRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_database

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastoreService server.
        """
        return request, metadata

    def post_update_database(self, response: metastore.Database) -> metastore.Database:
        """Post-rpc interceptor for update_database

        Override in a subclass to manipulate the response
        after it is returned by the MetastoreService server but before
        it is returned to user code.
        """
        return response

    def pre_update_table(
        self, request: metastore.UpdateTableRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[metastore.UpdateTableRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_table

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastoreService server.
        """
        return request, metadata

    def post_update_table(self, response: metastore.Table) -> metastore.Table:
        """Post-rpc interceptor for update_table

        Override in a subclass to manipulate the response
        after it is returned by the MetastoreService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class MetastoreServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: MetastoreServiceRestInterceptor


class MetastoreServiceRestTransport(_BaseMetastoreServiceRestTransport):
    """REST backend synchronous transport for MetastoreService.

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

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "biglake.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[MetastoreServiceRestInterceptor] = None,
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
        self._interceptor = interceptor or MetastoreServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CheckLock(
        _BaseMetastoreServiceRestTransport._BaseCheckLock, MetastoreServiceRestStub
    ):
        def __hash__(self):
            return hash("MetastoreServiceRestTransport.CheckLock")

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
            request: metastore.CheckLockRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.Lock:
            r"""Call the check lock method over HTTP.

            Args:
                request (~.metastore.CheckLockRequest):
                    The request object. Request message for the CheckLock
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.Lock:
                    Represents a lock.
            """

            http_options = (
                _BaseMetastoreServiceRestTransport._BaseCheckLock._get_http_options()
            )
            request, metadata = self._interceptor.pre_check_lock(request, metadata)
            transcoded_request = _BaseMetastoreServiceRestTransport._BaseCheckLock._get_transcoded_request(
                http_options, request
            )

            body = _BaseMetastoreServiceRestTransport._BaseCheckLock._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMetastoreServiceRestTransport._BaseCheckLock._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MetastoreServiceRestTransport._CheckLock._get_response(
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
            resp = metastore.Lock()
            pb_resp = metastore.Lock.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_check_lock(resp)
            return resp

    class _CreateCatalog(
        _BaseMetastoreServiceRestTransport._BaseCreateCatalog, MetastoreServiceRestStub
    ):
        def __hash__(self):
            return hash("MetastoreServiceRestTransport.CreateCatalog")

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
            request: metastore.CreateCatalogRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.Catalog:
            r"""Call the create catalog method over HTTP.

            Args:
                request (~.metastore.CreateCatalogRequest):
                    The request object. Request message for the CreateCatalog
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.Catalog:
                    Catalog is the container of
                databases.

            """

            http_options = (
                _BaseMetastoreServiceRestTransport._BaseCreateCatalog._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_catalog(request, metadata)
            transcoded_request = _BaseMetastoreServiceRestTransport._BaseCreateCatalog._get_transcoded_request(
                http_options, request
            )

            body = _BaseMetastoreServiceRestTransport._BaseCreateCatalog._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMetastoreServiceRestTransport._BaseCreateCatalog._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MetastoreServiceRestTransport._CreateCatalog._get_response(
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
            resp = metastore.Catalog()
            pb_resp = metastore.Catalog.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_catalog(resp)
            return resp

    class _CreateDatabase(
        _BaseMetastoreServiceRestTransport._BaseCreateDatabase, MetastoreServiceRestStub
    ):
        def __hash__(self):
            return hash("MetastoreServiceRestTransport.CreateDatabase")

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
            request: metastore.CreateDatabaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.Database:
            r"""Call the create database method over HTTP.

            Args:
                request (~.metastore.CreateDatabaseRequest):
                    The request object. Request message for the
                CreateDatabase method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.Database:
                    Database is the container of tables.
            """

            http_options = (
                _BaseMetastoreServiceRestTransport._BaseCreateDatabase._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_database(request, metadata)
            transcoded_request = _BaseMetastoreServiceRestTransport._BaseCreateDatabase._get_transcoded_request(
                http_options, request
            )

            body = _BaseMetastoreServiceRestTransport._BaseCreateDatabase._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMetastoreServiceRestTransport._BaseCreateDatabase._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MetastoreServiceRestTransport._CreateDatabase._get_response(
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
            resp = metastore.Database()
            pb_resp = metastore.Database.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_database(resp)
            return resp

    class _CreateLock(
        _BaseMetastoreServiceRestTransport._BaseCreateLock, MetastoreServiceRestStub
    ):
        def __hash__(self):
            return hash("MetastoreServiceRestTransport.CreateLock")

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
            request: metastore.CreateLockRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.Lock:
            r"""Call the create lock method over HTTP.

            Args:
                request (~.metastore.CreateLockRequest):
                    The request object. Request message for the CreateLock
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.Lock:
                    Represents a lock.
            """

            http_options = (
                _BaseMetastoreServiceRestTransport._BaseCreateLock._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_lock(request, metadata)
            transcoded_request = _BaseMetastoreServiceRestTransport._BaseCreateLock._get_transcoded_request(
                http_options, request
            )

            body = _BaseMetastoreServiceRestTransport._BaseCreateLock._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMetastoreServiceRestTransport._BaseCreateLock._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MetastoreServiceRestTransport._CreateLock._get_response(
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
            resp = metastore.Lock()
            pb_resp = metastore.Lock.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_lock(resp)
            return resp

    class _CreateTable(
        _BaseMetastoreServiceRestTransport._BaseCreateTable, MetastoreServiceRestStub
    ):
        def __hash__(self):
            return hash("MetastoreServiceRestTransport.CreateTable")

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
            request: metastore.CreateTableRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.Table:
            r"""Call the create table method over HTTP.

            Args:
                request (~.metastore.CreateTableRequest):
                    The request object. Request message for the CreateTable
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.Table:
                    Represents a table.
            """

            http_options = (
                _BaseMetastoreServiceRestTransport._BaseCreateTable._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_table(request, metadata)
            transcoded_request = _BaseMetastoreServiceRestTransport._BaseCreateTable._get_transcoded_request(
                http_options, request
            )

            body = _BaseMetastoreServiceRestTransport._BaseCreateTable._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMetastoreServiceRestTransport._BaseCreateTable._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MetastoreServiceRestTransport._CreateTable._get_response(
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
            resp = metastore.Table()
            pb_resp = metastore.Table.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_table(resp)
            return resp

    class _DeleteCatalog(
        _BaseMetastoreServiceRestTransport._BaseDeleteCatalog, MetastoreServiceRestStub
    ):
        def __hash__(self):
            return hash("MetastoreServiceRestTransport.DeleteCatalog")

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
            request: metastore.DeleteCatalogRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.Catalog:
            r"""Call the delete catalog method over HTTP.

            Args:
                request (~.metastore.DeleteCatalogRequest):
                    The request object. Request message for the DeleteCatalog
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.Catalog:
                    Catalog is the container of
                databases.

            """

            http_options = (
                _BaseMetastoreServiceRestTransport._BaseDeleteCatalog._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_catalog(request, metadata)
            transcoded_request = _BaseMetastoreServiceRestTransport._BaseDeleteCatalog._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMetastoreServiceRestTransport._BaseDeleteCatalog._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MetastoreServiceRestTransport._DeleteCatalog._get_response(
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
            resp = metastore.Catalog()
            pb_resp = metastore.Catalog.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_catalog(resp)
            return resp

    class _DeleteDatabase(
        _BaseMetastoreServiceRestTransport._BaseDeleteDatabase, MetastoreServiceRestStub
    ):
        def __hash__(self):
            return hash("MetastoreServiceRestTransport.DeleteDatabase")

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
            request: metastore.DeleteDatabaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.Database:
            r"""Call the delete database method over HTTP.

            Args:
                request (~.metastore.DeleteDatabaseRequest):
                    The request object. Request message for the
                DeleteDatabase method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.Database:
                    Database is the container of tables.
            """

            http_options = (
                _BaseMetastoreServiceRestTransport._BaseDeleteDatabase._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_database(request, metadata)
            transcoded_request = _BaseMetastoreServiceRestTransport._BaseDeleteDatabase._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMetastoreServiceRestTransport._BaseDeleteDatabase._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MetastoreServiceRestTransport._DeleteDatabase._get_response(
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
            resp = metastore.Database()
            pb_resp = metastore.Database.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_database(resp)
            return resp

    class _DeleteLock(
        _BaseMetastoreServiceRestTransport._BaseDeleteLock, MetastoreServiceRestStub
    ):
        def __hash__(self):
            return hash("MetastoreServiceRestTransport.DeleteLock")

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
            request: metastore.DeleteLockRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete lock method over HTTP.

            Args:
                request (~.metastore.DeleteLockRequest):
                    The request object. Request message for the DeleteLock
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseMetastoreServiceRestTransport._BaseDeleteLock._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_lock(request, metadata)
            transcoded_request = _BaseMetastoreServiceRestTransport._BaseDeleteLock._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMetastoreServiceRestTransport._BaseDeleteLock._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MetastoreServiceRestTransport._DeleteLock._get_response(
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

    class _DeleteTable(
        _BaseMetastoreServiceRestTransport._BaseDeleteTable, MetastoreServiceRestStub
    ):
        def __hash__(self):
            return hash("MetastoreServiceRestTransport.DeleteTable")

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
            request: metastore.DeleteTableRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.Table:
            r"""Call the delete table method over HTTP.

            Args:
                request (~.metastore.DeleteTableRequest):
                    The request object. Request message for the DeleteTable
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.Table:
                    Represents a table.
            """

            http_options = (
                _BaseMetastoreServiceRestTransport._BaseDeleteTable._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_table(request, metadata)
            transcoded_request = _BaseMetastoreServiceRestTransport._BaseDeleteTable._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMetastoreServiceRestTransport._BaseDeleteTable._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MetastoreServiceRestTransport._DeleteTable._get_response(
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
            resp = metastore.Table()
            pb_resp = metastore.Table.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_table(resp)
            return resp

    class _GetCatalog(
        _BaseMetastoreServiceRestTransport._BaseGetCatalog, MetastoreServiceRestStub
    ):
        def __hash__(self):
            return hash("MetastoreServiceRestTransport.GetCatalog")

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
            request: metastore.GetCatalogRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.Catalog:
            r"""Call the get catalog method over HTTP.

            Args:
                request (~.metastore.GetCatalogRequest):
                    The request object. Request message for the GetCatalog
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.Catalog:
                    Catalog is the container of
                databases.

            """

            http_options = (
                _BaseMetastoreServiceRestTransport._BaseGetCatalog._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_catalog(request, metadata)
            transcoded_request = _BaseMetastoreServiceRestTransport._BaseGetCatalog._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMetastoreServiceRestTransport._BaseGetCatalog._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MetastoreServiceRestTransport._GetCatalog._get_response(
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
            resp = metastore.Catalog()
            pb_resp = metastore.Catalog.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_catalog(resp)
            return resp

    class _GetDatabase(
        _BaseMetastoreServiceRestTransport._BaseGetDatabase, MetastoreServiceRestStub
    ):
        def __hash__(self):
            return hash("MetastoreServiceRestTransport.GetDatabase")

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
            request: metastore.GetDatabaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.Database:
            r"""Call the get database method over HTTP.

            Args:
                request (~.metastore.GetDatabaseRequest):
                    The request object. Request message for the GetDatabase
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.Database:
                    Database is the container of tables.
            """

            http_options = (
                _BaseMetastoreServiceRestTransport._BaseGetDatabase._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_database(request, metadata)
            transcoded_request = _BaseMetastoreServiceRestTransport._BaseGetDatabase._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMetastoreServiceRestTransport._BaseGetDatabase._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MetastoreServiceRestTransport._GetDatabase._get_response(
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
            resp = metastore.Database()
            pb_resp = metastore.Database.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_database(resp)
            return resp

    class _GetTable(
        _BaseMetastoreServiceRestTransport._BaseGetTable, MetastoreServiceRestStub
    ):
        def __hash__(self):
            return hash("MetastoreServiceRestTransport.GetTable")

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
            request: metastore.GetTableRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.Table:
            r"""Call the get table method over HTTP.

            Args:
                request (~.metastore.GetTableRequest):
                    The request object. Request message for the GetTable
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.Table:
                    Represents a table.
            """

            http_options = (
                _BaseMetastoreServiceRestTransport._BaseGetTable._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_table(request, metadata)
            transcoded_request = _BaseMetastoreServiceRestTransport._BaseGetTable._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseMetastoreServiceRestTransport._BaseGetTable._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = MetastoreServiceRestTransport._GetTable._get_response(
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
            resp = metastore.Table()
            pb_resp = metastore.Table.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_table(resp)
            return resp

    class _ListCatalogs(
        _BaseMetastoreServiceRestTransport._BaseListCatalogs, MetastoreServiceRestStub
    ):
        def __hash__(self):
            return hash("MetastoreServiceRestTransport.ListCatalogs")

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
            request: metastore.ListCatalogsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.ListCatalogsResponse:
            r"""Call the list catalogs method over HTTP.

            Args:
                request (~.metastore.ListCatalogsRequest):
                    The request object. Request message for the ListCatalogs
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.ListCatalogsResponse:
                    Response message for the ListCatalogs
                method.

            """

            http_options = (
                _BaseMetastoreServiceRestTransport._BaseListCatalogs._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_catalogs(request, metadata)
            transcoded_request = _BaseMetastoreServiceRestTransport._BaseListCatalogs._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMetastoreServiceRestTransport._BaseListCatalogs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MetastoreServiceRestTransport._ListCatalogs._get_response(
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
            resp = metastore.ListCatalogsResponse()
            pb_resp = metastore.ListCatalogsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_catalogs(resp)
            return resp

    class _ListDatabases(
        _BaseMetastoreServiceRestTransport._BaseListDatabases, MetastoreServiceRestStub
    ):
        def __hash__(self):
            return hash("MetastoreServiceRestTransport.ListDatabases")

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
            request: metastore.ListDatabasesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.ListDatabasesResponse:
            r"""Call the list databases method over HTTP.

            Args:
                request (~.metastore.ListDatabasesRequest):
                    The request object. Request message for the ListDatabases
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.ListDatabasesResponse:
                    Response message for the
                ListDatabases method.

            """

            http_options = (
                _BaseMetastoreServiceRestTransport._BaseListDatabases._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_databases(request, metadata)
            transcoded_request = _BaseMetastoreServiceRestTransport._BaseListDatabases._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMetastoreServiceRestTransport._BaseListDatabases._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MetastoreServiceRestTransport._ListDatabases._get_response(
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
            resp = metastore.ListDatabasesResponse()
            pb_resp = metastore.ListDatabasesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_databases(resp)
            return resp

    class _ListLocks(
        _BaseMetastoreServiceRestTransport._BaseListLocks, MetastoreServiceRestStub
    ):
        def __hash__(self):
            return hash("MetastoreServiceRestTransport.ListLocks")

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
            request: metastore.ListLocksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.ListLocksResponse:
            r"""Call the list locks method over HTTP.

            Args:
                request (~.metastore.ListLocksRequest):
                    The request object. Request message for the ListLocks
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.ListLocksResponse:
                    Response message for the ListLocks
                method.

            """

            http_options = (
                _BaseMetastoreServiceRestTransport._BaseListLocks._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locks(request, metadata)
            transcoded_request = _BaseMetastoreServiceRestTransport._BaseListLocks._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMetastoreServiceRestTransport._BaseListLocks._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MetastoreServiceRestTransport._ListLocks._get_response(
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
            resp = metastore.ListLocksResponse()
            pb_resp = metastore.ListLocksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_locks(resp)
            return resp

    class _ListTables(
        _BaseMetastoreServiceRestTransport._BaseListTables, MetastoreServiceRestStub
    ):
        def __hash__(self):
            return hash("MetastoreServiceRestTransport.ListTables")

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
            request: metastore.ListTablesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.ListTablesResponse:
            r"""Call the list tables method over HTTP.

            Args:
                request (~.metastore.ListTablesRequest):
                    The request object. Request message for the ListTables
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.ListTablesResponse:
                    Response message for the ListTables
                method.

            """

            http_options = (
                _BaseMetastoreServiceRestTransport._BaseListTables._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_tables(request, metadata)
            transcoded_request = _BaseMetastoreServiceRestTransport._BaseListTables._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMetastoreServiceRestTransport._BaseListTables._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MetastoreServiceRestTransport._ListTables._get_response(
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
            resp = metastore.ListTablesResponse()
            pb_resp = metastore.ListTablesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_tables(resp)
            return resp

    class _RenameTable(
        _BaseMetastoreServiceRestTransport._BaseRenameTable, MetastoreServiceRestStub
    ):
        def __hash__(self):
            return hash("MetastoreServiceRestTransport.RenameTable")

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
            request: metastore.RenameTableRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.Table:
            r"""Call the rename table method over HTTP.

            Args:
                request (~.metastore.RenameTableRequest):
                    The request object. Request message for the RenameTable
                method in MetastoreService
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.Table:
                    Represents a table.
            """

            http_options = (
                _BaseMetastoreServiceRestTransport._BaseRenameTable._get_http_options()
            )
            request, metadata = self._interceptor.pre_rename_table(request, metadata)
            transcoded_request = _BaseMetastoreServiceRestTransport._BaseRenameTable._get_transcoded_request(
                http_options, request
            )

            body = _BaseMetastoreServiceRestTransport._BaseRenameTable._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMetastoreServiceRestTransport._BaseRenameTable._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MetastoreServiceRestTransport._RenameTable._get_response(
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
            resp = metastore.Table()
            pb_resp = metastore.Table.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_rename_table(resp)
            return resp

    class _UpdateDatabase(
        _BaseMetastoreServiceRestTransport._BaseUpdateDatabase, MetastoreServiceRestStub
    ):
        def __hash__(self):
            return hash("MetastoreServiceRestTransport.UpdateDatabase")

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
            request: metastore.UpdateDatabaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.Database:
            r"""Call the update database method over HTTP.

            Args:
                request (~.metastore.UpdateDatabaseRequest):
                    The request object. Request message for the
                UpdateDatabase method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.Database:
                    Database is the container of tables.
            """

            http_options = (
                _BaseMetastoreServiceRestTransport._BaseUpdateDatabase._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_database(request, metadata)
            transcoded_request = _BaseMetastoreServiceRestTransport._BaseUpdateDatabase._get_transcoded_request(
                http_options, request
            )

            body = _BaseMetastoreServiceRestTransport._BaseUpdateDatabase._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMetastoreServiceRestTransport._BaseUpdateDatabase._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MetastoreServiceRestTransport._UpdateDatabase._get_response(
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
            resp = metastore.Database()
            pb_resp = metastore.Database.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_database(resp)
            return resp

    class _UpdateTable(
        _BaseMetastoreServiceRestTransport._BaseUpdateTable, MetastoreServiceRestStub
    ):
        def __hash__(self):
            return hash("MetastoreServiceRestTransport.UpdateTable")

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
            request: metastore.UpdateTableRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.Table:
            r"""Call the update table method over HTTP.

            Args:
                request (~.metastore.UpdateTableRequest):
                    The request object. Request message for the UpdateTable
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.Table:
                    Represents a table.
            """

            http_options = (
                _BaseMetastoreServiceRestTransport._BaseUpdateTable._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_table(request, metadata)
            transcoded_request = _BaseMetastoreServiceRestTransport._BaseUpdateTable._get_transcoded_request(
                http_options, request
            )

            body = _BaseMetastoreServiceRestTransport._BaseUpdateTable._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMetastoreServiceRestTransport._BaseUpdateTable._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MetastoreServiceRestTransport._UpdateTable._get_response(
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
            resp = metastore.Table()
            pb_resp = metastore.Table.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_table(resp)
            return resp

    @property
    def check_lock(self) -> Callable[[metastore.CheckLockRequest], metastore.Lock]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CheckLock(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_catalog(
        self,
    ) -> Callable[[metastore.CreateCatalogRequest], metastore.Catalog]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCatalog(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_database(
        self,
    ) -> Callable[[metastore.CreateDatabaseRequest], metastore.Database]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDatabase(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_lock(self) -> Callable[[metastore.CreateLockRequest], metastore.Lock]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateLock(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_table(self) -> Callable[[metastore.CreateTableRequest], metastore.Table]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateTable(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_catalog(
        self,
    ) -> Callable[[metastore.DeleteCatalogRequest], metastore.Catalog]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCatalog(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_database(
        self,
    ) -> Callable[[metastore.DeleteDatabaseRequest], metastore.Database]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDatabase(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_lock(self) -> Callable[[metastore.DeleteLockRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteLock(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_table(self) -> Callable[[metastore.DeleteTableRequest], metastore.Table]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteTable(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_catalog(self) -> Callable[[metastore.GetCatalogRequest], metastore.Catalog]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCatalog(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_database(
        self,
    ) -> Callable[[metastore.GetDatabaseRequest], metastore.Database]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDatabase(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_table(self) -> Callable[[metastore.GetTableRequest], metastore.Table]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetTable(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_catalogs(
        self,
    ) -> Callable[[metastore.ListCatalogsRequest], metastore.ListCatalogsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCatalogs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_databases(
        self,
    ) -> Callable[[metastore.ListDatabasesRequest], metastore.ListDatabasesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDatabases(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_locks(
        self,
    ) -> Callable[[metastore.ListLocksRequest], metastore.ListLocksResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListLocks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_tables(
        self,
    ) -> Callable[[metastore.ListTablesRequest], metastore.ListTablesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListTables(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def rename_table(self) -> Callable[[metastore.RenameTableRequest], metastore.Table]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RenameTable(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_database(
        self,
    ) -> Callable[[metastore.UpdateDatabaseRequest], metastore.Database]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDatabase(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_table(self) -> Callable[[metastore.UpdateTableRequest], metastore.Table]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateTable(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("MetastoreServiceRestTransport",)
