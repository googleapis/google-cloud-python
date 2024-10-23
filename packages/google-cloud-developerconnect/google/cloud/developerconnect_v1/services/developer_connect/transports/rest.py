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

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.developerconnect_v1.types import developer_connect

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseDeveloperConnectRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class DeveloperConnectRestInterceptor:
    """Interceptor for DeveloperConnect.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the DeveloperConnectRestTransport.

    .. code-block:: python
        class MyCustomDeveloperConnectInterceptor(DeveloperConnectRestInterceptor):
            def pre_create_connection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_connection(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_git_repository_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_git_repository_link(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_connection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_connection(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_git_repository_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_git_repository_link(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_git_hub_installations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_git_hub_installations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_git_refs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_git_refs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_linkable_git_repositories(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_linkable_git_repositories(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_read_token(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_read_token(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_read_write_token(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_read_write_token(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_connection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_connection(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_git_repository_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_git_repository_link(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_connections(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_connections(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_git_repository_links(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_git_repository_links(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_connection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_connection(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = DeveloperConnectRestTransport(interceptor=MyCustomDeveloperConnectInterceptor())
        client = DeveloperConnectClient(transport=transport)


    """

    def pre_create_connection(
        self,
        request: developer_connect.CreateConnectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[developer_connect.CreateConnectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_connection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeveloperConnect server.
        """
        return request, metadata

    def post_create_connection(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_connection

        Override in a subclass to manipulate the response
        after it is returned by the DeveloperConnect server but before
        it is returned to user code.
        """
        return response

    def pre_create_git_repository_link(
        self,
        request: developer_connect.CreateGitRepositoryLinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        developer_connect.CreateGitRepositoryLinkRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_git_repository_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeveloperConnect server.
        """
        return request, metadata

    def post_create_git_repository_link(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_git_repository_link

        Override in a subclass to manipulate the response
        after it is returned by the DeveloperConnect server but before
        it is returned to user code.
        """
        return response

    def pre_delete_connection(
        self,
        request: developer_connect.DeleteConnectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[developer_connect.DeleteConnectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_connection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeveloperConnect server.
        """
        return request, metadata

    def post_delete_connection(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_connection

        Override in a subclass to manipulate the response
        after it is returned by the DeveloperConnect server but before
        it is returned to user code.
        """
        return response

    def pre_delete_git_repository_link(
        self,
        request: developer_connect.DeleteGitRepositoryLinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        developer_connect.DeleteGitRepositoryLinkRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_git_repository_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeveloperConnect server.
        """
        return request, metadata

    def post_delete_git_repository_link(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_git_repository_link

        Override in a subclass to manipulate the response
        after it is returned by the DeveloperConnect server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_git_hub_installations(
        self,
        request: developer_connect.FetchGitHubInstallationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        developer_connect.FetchGitHubInstallationsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for fetch_git_hub_installations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeveloperConnect server.
        """
        return request, metadata

    def post_fetch_git_hub_installations(
        self, response: developer_connect.FetchGitHubInstallationsResponse
    ) -> developer_connect.FetchGitHubInstallationsResponse:
        """Post-rpc interceptor for fetch_git_hub_installations

        Override in a subclass to manipulate the response
        after it is returned by the DeveloperConnect server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_git_refs(
        self,
        request: developer_connect.FetchGitRefsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[developer_connect.FetchGitRefsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for fetch_git_refs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeveloperConnect server.
        """
        return request, metadata

    def post_fetch_git_refs(
        self, response: developer_connect.FetchGitRefsResponse
    ) -> developer_connect.FetchGitRefsResponse:
        """Post-rpc interceptor for fetch_git_refs

        Override in a subclass to manipulate the response
        after it is returned by the DeveloperConnect server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_linkable_git_repositories(
        self,
        request: developer_connect.FetchLinkableGitRepositoriesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        developer_connect.FetchLinkableGitRepositoriesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for fetch_linkable_git_repositories

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeveloperConnect server.
        """
        return request, metadata

    def post_fetch_linkable_git_repositories(
        self, response: developer_connect.FetchLinkableGitRepositoriesResponse
    ) -> developer_connect.FetchLinkableGitRepositoriesResponse:
        """Post-rpc interceptor for fetch_linkable_git_repositories

        Override in a subclass to manipulate the response
        after it is returned by the DeveloperConnect server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_read_token(
        self,
        request: developer_connect.FetchReadTokenRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[developer_connect.FetchReadTokenRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for fetch_read_token

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeveloperConnect server.
        """
        return request, metadata

    def post_fetch_read_token(
        self, response: developer_connect.FetchReadTokenResponse
    ) -> developer_connect.FetchReadTokenResponse:
        """Post-rpc interceptor for fetch_read_token

        Override in a subclass to manipulate the response
        after it is returned by the DeveloperConnect server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_read_write_token(
        self,
        request: developer_connect.FetchReadWriteTokenRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[developer_connect.FetchReadWriteTokenRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for fetch_read_write_token

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeveloperConnect server.
        """
        return request, metadata

    def post_fetch_read_write_token(
        self, response: developer_connect.FetchReadWriteTokenResponse
    ) -> developer_connect.FetchReadWriteTokenResponse:
        """Post-rpc interceptor for fetch_read_write_token

        Override in a subclass to manipulate the response
        after it is returned by the DeveloperConnect server but before
        it is returned to user code.
        """
        return response

    def pre_get_connection(
        self,
        request: developer_connect.GetConnectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[developer_connect.GetConnectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_connection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeveloperConnect server.
        """
        return request, metadata

    def post_get_connection(
        self, response: developer_connect.Connection
    ) -> developer_connect.Connection:
        """Post-rpc interceptor for get_connection

        Override in a subclass to manipulate the response
        after it is returned by the DeveloperConnect server but before
        it is returned to user code.
        """
        return response

    def pre_get_git_repository_link(
        self,
        request: developer_connect.GetGitRepositoryLinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        developer_connect.GetGitRepositoryLinkRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_git_repository_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeveloperConnect server.
        """
        return request, metadata

    def post_get_git_repository_link(
        self, response: developer_connect.GitRepositoryLink
    ) -> developer_connect.GitRepositoryLink:
        """Post-rpc interceptor for get_git_repository_link

        Override in a subclass to manipulate the response
        after it is returned by the DeveloperConnect server but before
        it is returned to user code.
        """
        return response

    def pre_list_connections(
        self,
        request: developer_connect.ListConnectionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[developer_connect.ListConnectionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_connections

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeveloperConnect server.
        """
        return request, metadata

    def post_list_connections(
        self, response: developer_connect.ListConnectionsResponse
    ) -> developer_connect.ListConnectionsResponse:
        """Post-rpc interceptor for list_connections

        Override in a subclass to manipulate the response
        after it is returned by the DeveloperConnect server but before
        it is returned to user code.
        """
        return response

    def pre_list_git_repository_links(
        self,
        request: developer_connect.ListGitRepositoryLinksRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        developer_connect.ListGitRepositoryLinksRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_git_repository_links

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeveloperConnect server.
        """
        return request, metadata

    def post_list_git_repository_links(
        self, response: developer_connect.ListGitRepositoryLinksResponse
    ) -> developer_connect.ListGitRepositoryLinksResponse:
        """Post-rpc interceptor for list_git_repository_links

        Override in a subclass to manipulate the response
        after it is returned by the DeveloperConnect server but before
        it is returned to user code.
        """
        return response

    def pre_update_connection(
        self,
        request: developer_connect.UpdateConnectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[developer_connect.UpdateConnectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_connection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeveloperConnect server.
        """
        return request, metadata

    def post_update_connection(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_connection

        Override in a subclass to manipulate the response
        after it is returned by the DeveloperConnect server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.GetLocationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeveloperConnect server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the DeveloperConnect server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.ListLocationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeveloperConnect server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the DeveloperConnect server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.CancelOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeveloperConnect server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the DeveloperConnect server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operation(
        self,
        request: operations_pb2.DeleteOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeveloperConnect server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the DeveloperConnect server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.GetOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeveloperConnect server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the DeveloperConnect server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.ListOperationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeveloperConnect server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the DeveloperConnect server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class DeveloperConnectRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: DeveloperConnectRestInterceptor


class DeveloperConnectRestTransport(_BaseDeveloperConnectRestTransport):
    """REST backend synchronous transport for DeveloperConnect.

    Service describing handlers for resources

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "developerconnect.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[DeveloperConnectRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'developerconnect.googleapis.com').
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
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or DeveloperConnectRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.CancelOperation": [
                    {
                        "method": "post",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateConnection(
        _BaseDeveloperConnectRestTransport._BaseCreateConnection,
        DeveloperConnectRestStub,
    ):
        def __hash__(self):
            return hash("DeveloperConnectRestTransport.CreateConnection")

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
            request: developer_connect.CreateConnectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create connection method over HTTP.

            Args:
                request (~.developer_connect.CreateConnectionRequest):
                    The request object. Message for creating a Connection
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseDeveloperConnectRestTransport._BaseCreateConnection._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_connection(
                request, metadata
            )
            transcoded_request = _BaseDeveloperConnectRestTransport._BaseCreateConnection._get_transcoded_request(
                http_options, request
            )

            body = _BaseDeveloperConnectRestTransport._BaseCreateConnection._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDeveloperConnectRestTransport._BaseCreateConnection._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DeveloperConnectRestTransport._CreateConnection._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_connection(resp)
            return resp

    class _CreateGitRepositoryLink(
        _BaseDeveloperConnectRestTransport._BaseCreateGitRepositoryLink,
        DeveloperConnectRestStub,
    ):
        def __hash__(self):
            return hash("DeveloperConnectRestTransport.CreateGitRepositoryLink")

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
            request: developer_connect.CreateGitRepositoryLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create git repository
            link method over HTTP.

                Args:
                    request (~.developer_connect.CreateGitRepositoryLinkRequest):
                        The request object. Message for creating a
                    GitRepositoryLink
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = (
                _BaseDeveloperConnectRestTransport._BaseCreateGitRepositoryLink._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_git_repository_link(
                request, metadata
            )
            transcoded_request = _BaseDeveloperConnectRestTransport._BaseCreateGitRepositoryLink._get_transcoded_request(
                http_options, request
            )

            body = _BaseDeveloperConnectRestTransport._BaseCreateGitRepositoryLink._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDeveloperConnectRestTransport._BaseCreateGitRepositoryLink._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                DeveloperConnectRestTransport._CreateGitRepositoryLink._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_git_repository_link(resp)
            return resp

    class _DeleteConnection(
        _BaseDeveloperConnectRestTransport._BaseDeleteConnection,
        DeveloperConnectRestStub,
    ):
        def __hash__(self):
            return hash("DeveloperConnectRestTransport.DeleteConnection")

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
            request: developer_connect.DeleteConnectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete connection method over HTTP.

            Args:
                request (~.developer_connect.DeleteConnectionRequest):
                    The request object. Message for deleting a Connection
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseDeveloperConnectRestTransport._BaseDeleteConnection._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_connection(
                request, metadata
            )
            transcoded_request = _BaseDeveloperConnectRestTransport._BaseDeleteConnection._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDeveloperConnectRestTransport._BaseDeleteConnection._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DeveloperConnectRestTransport._DeleteConnection._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_connection(resp)
            return resp

    class _DeleteGitRepositoryLink(
        _BaseDeveloperConnectRestTransport._BaseDeleteGitRepositoryLink,
        DeveloperConnectRestStub,
    ):
        def __hash__(self):
            return hash("DeveloperConnectRestTransport.DeleteGitRepositoryLink")

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
            request: developer_connect.DeleteGitRepositoryLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete git repository
            link method over HTTP.

                Args:
                    request (~.developer_connect.DeleteGitRepositoryLinkRequest):
                        The request object. Message for deleting a
                    GitRepositoryLink
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = (
                _BaseDeveloperConnectRestTransport._BaseDeleteGitRepositoryLink._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_git_repository_link(
                request, metadata
            )
            transcoded_request = _BaseDeveloperConnectRestTransport._BaseDeleteGitRepositoryLink._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDeveloperConnectRestTransport._BaseDeleteGitRepositoryLink._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                DeveloperConnectRestTransport._DeleteGitRepositoryLink._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_git_repository_link(resp)
            return resp

    class _FetchGitHubInstallations(
        _BaseDeveloperConnectRestTransport._BaseFetchGitHubInstallations,
        DeveloperConnectRestStub,
    ):
        def __hash__(self):
            return hash("DeveloperConnectRestTransport.FetchGitHubInstallations")

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
            request: developer_connect.FetchGitHubInstallationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> developer_connect.FetchGitHubInstallationsResponse:
            r"""Call the fetch git hub
            installations method over HTTP.

                Args:
                    request (~.developer_connect.FetchGitHubInstallationsRequest):
                        The request object. Request for fetching github
                    installations.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.developer_connect.FetchGitHubInstallationsResponse:
                        Response of fetching github
                    installations.

            """

            http_options = (
                _BaseDeveloperConnectRestTransport._BaseFetchGitHubInstallations._get_http_options()
            )
            request, metadata = self._interceptor.pre_fetch_git_hub_installations(
                request, metadata
            )
            transcoded_request = _BaseDeveloperConnectRestTransport._BaseFetchGitHubInstallations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDeveloperConnectRestTransport._BaseFetchGitHubInstallations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                DeveloperConnectRestTransport._FetchGitHubInstallations._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = developer_connect.FetchGitHubInstallationsResponse()
            pb_resp = developer_connect.FetchGitHubInstallationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_git_hub_installations(resp)
            return resp

    class _FetchGitRefs(
        _BaseDeveloperConnectRestTransport._BaseFetchGitRefs, DeveloperConnectRestStub
    ):
        def __hash__(self):
            return hash("DeveloperConnectRestTransport.FetchGitRefs")

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
            request: developer_connect.FetchGitRefsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> developer_connect.FetchGitRefsResponse:
            r"""Call the fetch git refs method over HTTP.

            Args:
                request (~.developer_connect.FetchGitRefsRequest):
                    The request object. Request for fetching git refs.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.developer_connect.FetchGitRefsResponse:
                    Response for fetching git refs.
            """

            http_options = (
                _BaseDeveloperConnectRestTransport._BaseFetchGitRefs._get_http_options()
            )
            request, metadata = self._interceptor.pre_fetch_git_refs(request, metadata)
            transcoded_request = _BaseDeveloperConnectRestTransport._BaseFetchGitRefs._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDeveloperConnectRestTransport._BaseFetchGitRefs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DeveloperConnectRestTransport._FetchGitRefs._get_response(
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
            resp = developer_connect.FetchGitRefsResponse()
            pb_resp = developer_connect.FetchGitRefsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_git_refs(resp)
            return resp

    class _FetchLinkableGitRepositories(
        _BaseDeveloperConnectRestTransport._BaseFetchLinkableGitRepositories,
        DeveloperConnectRestStub,
    ):
        def __hash__(self):
            return hash("DeveloperConnectRestTransport.FetchLinkableGitRepositories")

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
            request: developer_connect.FetchLinkableGitRepositoriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> developer_connect.FetchLinkableGitRepositoriesResponse:
            r"""Call the fetch linkable git
            repositories method over HTTP.

                Args:
                    request (~.developer_connect.FetchLinkableGitRepositoriesRequest):
                        The request object. Request message for
                    FetchLinkableGitRepositoriesRequest.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.developer_connect.FetchLinkableGitRepositoriesResponse:
                        Response message for
                    FetchLinkableGitRepositories.

            """

            http_options = (
                _BaseDeveloperConnectRestTransport._BaseFetchLinkableGitRepositories._get_http_options()
            )
            request, metadata = self._interceptor.pre_fetch_linkable_git_repositories(
                request, metadata
            )
            transcoded_request = _BaseDeveloperConnectRestTransport._BaseFetchLinkableGitRepositories._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDeveloperConnectRestTransport._BaseFetchLinkableGitRepositories._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DeveloperConnectRestTransport._FetchLinkableGitRepositories._get_response(
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
            resp = developer_connect.FetchLinkableGitRepositoriesResponse()
            pb_resp = developer_connect.FetchLinkableGitRepositoriesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_linkable_git_repositories(resp)
            return resp

    class _FetchReadToken(
        _BaseDeveloperConnectRestTransport._BaseFetchReadToken, DeveloperConnectRestStub
    ):
        def __hash__(self):
            return hash("DeveloperConnectRestTransport.FetchReadToken")

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
            request: developer_connect.FetchReadTokenRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> developer_connect.FetchReadTokenResponse:
            r"""Call the fetch read token method over HTTP.

            Args:
                request (~.developer_connect.FetchReadTokenRequest):
                    The request object. Message for fetching SCM read token.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.developer_connect.FetchReadTokenResponse:
                    Message for responding to get read
                token.

            """

            http_options = (
                _BaseDeveloperConnectRestTransport._BaseFetchReadToken._get_http_options()
            )
            request, metadata = self._interceptor.pre_fetch_read_token(
                request, metadata
            )
            transcoded_request = _BaseDeveloperConnectRestTransport._BaseFetchReadToken._get_transcoded_request(
                http_options, request
            )

            body = _BaseDeveloperConnectRestTransport._BaseFetchReadToken._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDeveloperConnectRestTransport._BaseFetchReadToken._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DeveloperConnectRestTransport._FetchReadToken._get_response(
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
            resp = developer_connect.FetchReadTokenResponse()
            pb_resp = developer_connect.FetchReadTokenResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_read_token(resp)
            return resp

    class _FetchReadWriteToken(
        _BaseDeveloperConnectRestTransport._BaseFetchReadWriteToken,
        DeveloperConnectRestStub,
    ):
        def __hash__(self):
            return hash("DeveloperConnectRestTransport.FetchReadWriteToken")

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
            request: developer_connect.FetchReadWriteTokenRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> developer_connect.FetchReadWriteTokenResponse:
            r"""Call the fetch read write token method over HTTP.

            Args:
                request (~.developer_connect.FetchReadWriteTokenRequest):
                    The request object. Message for fetching SCM read/write
                token.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.developer_connect.FetchReadWriteTokenResponse:
                    Message for responding to get
                read/write token.

            """

            http_options = (
                _BaseDeveloperConnectRestTransport._BaseFetchReadWriteToken._get_http_options()
            )
            request, metadata = self._interceptor.pre_fetch_read_write_token(
                request, metadata
            )
            transcoded_request = _BaseDeveloperConnectRestTransport._BaseFetchReadWriteToken._get_transcoded_request(
                http_options, request
            )

            body = _BaseDeveloperConnectRestTransport._BaseFetchReadWriteToken._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDeveloperConnectRestTransport._BaseFetchReadWriteToken._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DeveloperConnectRestTransport._FetchReadWriteToken._get_response(
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
            resp = developer_connect.FetchReadWriteTokenResponse()
            pb_resp = developer_connect.FetchReadWriteTokenResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_read_write_token(resp)
            return resp

    class _GetConnection(
        _BaseDeveloperConnectRestTransport._BaseGetConnection, DeveloperConnectRestStub
    ):
        def __hash__(self):
            return hash("DeveloperConnectRestTransport.GetConnection")

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
            request: developer_connect.GetConnectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> developer_connect.Connection:
            r"""Call the get connection method over HTTP.

            Args:
                request (~.developer_connect.GetConnectionRequest):
                    The request object. Message for getting a Connection
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.developer_connect.Connection:
                    Message describing Connection object
            """

            http_options = (
                _BaseDeveloperConnectRestTransport._BaseGetConnection._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_connection(request, metadata)
            transcoded_request = _BaseDeveloperConnectRestTransport._BaseGetConnection._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDeveloperConnectRestTransport._BaseGetConnection._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DeveloperConnectRestTransport._GetConnection._get_response(
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
            resp = developer_connect.Connection()
            pb_resp = developer_connect.Connection.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_connection(resp)
            return resp

    class _GetGitRepositoryLink(
        _BaseDeveloperConnectRestTransport._BaseGetGitRepositoryLink,
        DeveloperConnectRestStub,
    ):
        def __hash__(self):
            return hash("DeveloperConnectRestTransport.GetGitRepositoryLink")

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
            request: developer_connect.GetGitRepositoryLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> developer_connect.GitRepositoryLink:
            r"""Call the get git repository link method over HTTP.

            Args:
                request (~.developer_connect.GetGitRepositoryLinkRequest):
                    The request object. Message for getting a
                GitRepositoryLink
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.developer_connect.GitRepositoryLink:
                    Message describing the
                GitRepositoryLink object

            """

            http_options = (
                _BaseDeveloperConnectRestTransport._BaseGetGitRepositoryLink._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_git_repository_link(
                request, metadata
            )
            transcoded_request = _BaseDeveloperConnectRestTransport._BaseGetGitRepositoryLink._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDeveloperConnectRestTransport._BaseGetGitRepositoryLink._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                DeveloperConnectRestTransport._GetGitRepositoryLink._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = developer_connect.GitRepositoryLink()
            pb_resp = developer_connect.GitRepositoryLink.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_git_repository_link(resp)
            return resp

    class _ListConnections(
        _BaseDeveloperConnectRestTransport._BaseListConnections,
        DeveloperConnectRestStub,
    ):
        def __hash__(self):
            return hash("DeveloperConnectRestTransport.ListConnections")

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
            request: developer_connect.ListConnectionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> developer_connect.ListConnectionsResponse:
            r"""Call the list connections method over HTTP.

            Args:
                request (~.developer_connect.ListConnectionsRequest):
                    The request object. Message for requesting list of
                Connections
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.developer_connect.ListConnectionsResponse:
                    Message for response to listing
                Connections

            """

            http_options = (
                _BaseDeveloperConnectRestTransport._BaseListConnections._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_connections(
                request, metadata
            )
            transcoded_request = _BaseDeveloperConnectRestTransport._BaseListConnections._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDeveloperConnectRestTransport._BaseListConnections._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DeveloperConnectRestTransport._ListConnections._get_response(
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
            resp = developer_connect.ListConnectionsResponse()
            pb_resp = developer_connect.ListConnectionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_connections(resp)
            return resp

    class _ListGitRepositoryLinks(
        _BaseDeveloperConnectRestTransport._BaseListGitRepositoryLinks,
        DeveloperConnectRestStub,
    ):
        def __hash__(self):
            return hash("DeveloperConnectRestTransport.ListGitRepositoryLinks")

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
            request: developer_connect.ListGitRepositoryLinksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> developer_connect.ListGitRepositoryLinksResponse:
            r"""Call the list git repository links method over HTTP.

            Args:
                request (~.developer_connect.ListGitRepositoryLinksRequest):
                    The request object. Message for requesting a list of
                GitRepositoryLinks
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.developer_connect.ListGitRepositoryLinksResponse:
                    Message for response to listing
                GitRepositoryLinks

            """

            http_options = (
                _BaseDeveloperConnectRestTransport._BaseListGitRepositoryLinks._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_git_repository_links(
                request, metadata
            )
            transcoded_request = _BaseDeveloperConnectRestTransport._BaseListGitRepositoryLinks._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDeveloperConnectRestTransport._BaseListGitRepositoryLinks._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                DeveloperConnectRestTransport._ListGitRepositoryLinks._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = developer_connect.ListGitRepositoryLinksResponse()
            pb_resp = developer_connect.ListGitRepositoryLinksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_git_repository_links(resp)
            return resp

    class _UpdateConnection(
        _BaseDeveloperConnectRestTransport._BaseUpdateConnection,
        DeveloperConnectRestStub,
    ):
        def __hash__(self):
            return hash("DeveloperConnectRestTransport.UpdateConnection")

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
            request: developer_connect.UpdateConnectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update connection method over HTTP.

            Args:
                request (~.developer_connect.UpdateConnectionRequest):
                    The request object. Message for updating a Connection
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseDeveloperConnectRestTransport._BaseUpdateConnection._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_connection(
                request, metadata
            )
            transcoded_request = _BaseDeveloperConnectRestTransport._BaseUpdateConnection._get_transcoded_request(
                http_options, request
            )

            body = _BaseDeveloperConnectRestTransport._BaseUpdateConnection._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDeveloperConnectRestTransport._BaseUpdateConnection._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DeveloperConnectRestTransport._UpdateConnection._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_connection(resp)
            return resp

    @property
    def create_connection(
        self,
    ) -> Callable[
        [developer_connect.CreateConnectionRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateConnection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_git_repository_link(
        self,
    ) -> Callable[
        [developer_connect.CreateGitRepositoryLinkRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateGitRepositoryLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_connection(
        self,
    ) -> Callable[
        [developer_connect.DeleteConnectionRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteConnection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_git_repository_link(
        self,
    ) -> Callable[
        [developer_connect.DeleteGitRepositoryLinkRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteGitRepositoryLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_git_hub_installations(
        self,
    ) -> Callable[
        [developer_connect.FetchGitHubInstallationsRequest],
        developer_connect.FetchGitHubInstallationsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchGitHubInstallations(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_git_refs(
        self,
    ) -> Callable[
        [developer_connect.FetchGitRefsRequest], developer_connect.FetchGitRefsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchGitRefs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_linkable_git_repositories(
        self,
    ) -> Callable[
        [developer_connect.FetchLinkableGitRepositoriesRequest],
        developer_connect.FetchLinkableGitRepositoriesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchLinkableGitRepositories(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_read_token(
        self,
    ) -> Callable[
        [developer_connect.FetchReadTokenRequest],
        developer_connect.FetchReadTokenResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchReadToken(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_read_write_token(
        self,
    ) -> Callable[
        [developer_connect.FetchReadWriteTokenRequest],
        developer_connect.FetchReadWriteTokenResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchReadWriteToken(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_connection(
        self,
    ) -> Callable[
        [developer_connect.GetConnectionRequest], developer_connect.Connection
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetConnection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_git_repository_link(
        self,
    ) -> Callable[
        [developer_connect.GetGitRepositoryLinkRequest],
        developer_connect.GitRepositoryLink,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetGitRepositoryLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_connections(
        self,
    ) -> Callable[
        [developer_connect.ListConnectionsRequest],
        developer_connect.ListConnectionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListConnections(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_git_repository_links(
        self,
    ) -> Callable[
        [developer_connect.ListGitRepositoryLinksRequest],
        developer_connect.ListGitRepositoryLinksResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListGitRepositoryLinks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_connection(
        self,
    ) -> Callable[
        [developer_connect.UpdateConnectionRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateConnection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseDeveloperConnectRestTransport._BaseGetLocation, DeveloperConnectRestStub
    ):
        def __hash__(self):
            return hash("DeveloperConnectRestTransport.GetLocation")

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
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options = (
                _BaseDeveloperConnectRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = _BaseDeveloperConnectRestTransport._BaseGetLocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDeveloperConnectRestTransport._BaseGetLocation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DeveloperConnectRestTransport._GetLocation._get_response(
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

            content = response.content.decode("utf-8")
            resp = locations_pb2.Location()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseDeveloperConnectRestTransport._BaseListLocations, DeveloperConnectRestStub
    ):
        def __hash__(self):
            return hash("DeveloperConnectRestTransport.ListLocations")

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
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options = (
                _BaseDeveloperConnectRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseDeveloperConnectRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDeveloperConnectRestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DeveloperConnectRestTransport._ListLocations._get_response(
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

            content = response.content.decode("utf-8")
            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseDeveloperConnectRestTransport._BaseCancelOperation,
        DeveloperConnectRestStub,
    ):
        def __hash__(self):
            return hash("DeveloperConnectRestTransport.CancelOperation")

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
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseDeveloperConnectRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseDeveloperConnectRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = _BaseDeveloperConnectRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDeveloperConnectRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DeveloperConnectRestTransport._CancelOperation._get_response(
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

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(
        _BaseDeveloperConnectRestTransport._BaseDeleteOperation,
        DeveloperConnectRestStub,
    ):
        def __hash__(self):
            return hash("DeveloperConnectRestTransport.DeleteOperation")

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
            request: operations_pb2.DeleteOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseDeveloperConnectRestTransport._BaseDeleteOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BaseDeveloperConnectRestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDeveloperConnectRestTransport._BaseDeleteOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DeveloperConnectRestTransport._DeleteOperation._get_response(
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

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseDeveloperConnectRestTransport._BaseGetOperation, DeveloperConnectRestStub
    ):
        def __hash__(self):
            return hash("DeveloperConnectRestTransport.GetOperation")

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
            request: operations_pb2.GetOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options = (
                _BaseDeveloperConnectRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseDeveloperConnectRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDeveloperConnectRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DeveloperConnectRestTransport._GetOperation._get_response(
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

            content = response.content.decode("utf-8")
            resp = operations_pb2.Operation()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseDeveloperConnectRestTransport._BaseListOperations, DeveloperConnectRestStub
    ):
        def __hash__(self):
            return hash("DeveloperConnectRestTransport.ListOperations")

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
            request: operations_pb2.ListOperationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options = (
                _BaseDeveloperConnectRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseDeveloperConnectRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDeveloperConnectRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DeveloperConnectRestTransport._ListOperations._get_response(
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

            content = response.content.decode("utf-8")
            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("DeveloperConnectRestTransport",)
