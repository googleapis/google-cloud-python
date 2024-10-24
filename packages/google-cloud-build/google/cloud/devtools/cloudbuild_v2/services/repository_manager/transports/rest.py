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
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.devtools.cloudbuild_v2.types import repositories

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseRepositoryManagerRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class RepositoryManagerRestInterceptor:
    """Interceptor for RepositoryManager.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the RepositoryManagerRestTransport.

    .. code-block:: python
        class MyCustomRepositoryManagerInterceptor(RepositoryManagerRestInterceptor):
            def pre_batch_create_repositories(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_create_repositories(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_connection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_connection(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_repository(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_repository(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_connection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_connection(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_repository(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_repository(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_git_refs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_git_refs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_linkable_repositories(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_linkable_repositories(self, response):
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

            def pre_get_repository(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_repository(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_connections(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_connections(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_repositories(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_repositories(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_connection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_connection(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = RepositoryManagerRestTransport(interceptor=MyCustomRepositoryManagerInterceptor())
        client = RepositoryManagerClient(transport=transport)


    """

    def pre_batch_create_repositories(
        self,
        request: repositories.BatchCreateRepositoriesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[repositories.BatchCreateRepositoriesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_create_repositories

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RepositoryManager server.
        """
        return request, metadata

    def post_batch_create_repositories(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for batch_create_repositories

        Override in a subclass to manipulate the response
        after it is returned by the RepositoryManager server but before
        it is returned to user code.
        """
        return response

    def pre_create_connection(
        self,
        request: repositories.CreateConnectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[repositories.CreateConnectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_connection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RepositoryManager server.
        """
        return request, metadata

    def post_create_connection(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_connection

        Override in a subclass to manipulate the response
        after it is returned by the RepositoryManager server but before
        it is returned to user code.
        """
        return response

    def pre_create_repository(
        self,
        request: repositories.CreateRepositoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[repositories.CreateRepositoryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_repository

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RepositoryManager server.
        """
        return request, metadata

    def post_create_repository(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_repository

        Override in a subclass to manipulate the response
        after it is returned by the RepositoryManager server but before
        it is returned to user code.
        """
        return response

    def pre_delete_connection(
        self,
        request: repositories.DeleteConnectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[repositories.DeleteConnectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_connection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RepositoryManager server.
        """
        return request, metadata

    def post_delete_connection(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_connection

        Override in a subclass to manipulate the response
        after it is returned by the RepositoryManager server but before
        it is returned to user code.
        """
        return response

    def pre_delete_repository(
        self,
        request: repositories.DeleteRepositoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[repositories.DeleteRepositoryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_repository

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RepositoryManager server.
        """
        return request, metadata

    def post_delete_repository(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_repository

        Override in a subclass to manipulate the response
        after it is returned by the RepositoryManager server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_git_refs(
        self,
        request: repositories.FetchGitRefsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[repositories.FetchGitRefsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for fetch_git_refs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RepositoryManager server.
        """
        return request, metadata

    def post_fetch_git_refs(
        self, response: repositories.FetchGitRefsResponse
    ) -> repositories.FetchGitRefsResponse:
        """Post-rpc interceptor for fetch_git_refs

        Override in a subclass to manipulate the response
        after it is returned by the RepositoryManager server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_linkable_repositories(
        self,
        request: repositories.FetchLinkableRepositoriesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        repositories.FetchLinkableRepositoriesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for fetch_linkable_repositories

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RepositoryManager server.
        """
        return request, metadata

    def post_fetch_linkable_repositories(
        self, response: repositories.FetchLinkableRepositoriesResponse
    ) -> repositories.FetchLinkableRepositoriesResponse:
        """Post-rpc interceptor for fetch_linkable_repositories

        Override in a subclass to manipulate the response
        after it is returned by the RepositoryManager server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_read_token(
        self,
        request: repositories.FetchReadTokenRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[repositories.FetchReadTokenRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for fetch_read_token

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RepositoryManager server.
        """
        return request, metadata

    def post_fetch_read_token(
        self, response: repositories.FetchReadTokenResponse
    ) -> repositories.FetchReadTokenResponse:
        """Post-rpc interceptor for fetch_read_token

        Override in a subclass to manipulate the response
        after it is returned by the RepositoryManager server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_read_write_token(
        self,
        request: repositories.FetchReadWriteTokenRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[repositories.FetchReadWriteTokenRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for fetch_read_write_token

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RepositoryManager server.
        """
        return request, metadata

    def post_fetch_read_write_token(
        self, response: repositories.FetchReadWriteTokenResponse
    ) -> repositories.FetchReadWriteTokenResponse:
        """Post-rpc interceptor for fetch_read_write_token

        Override in a subclass to manipulate the response
        after it is returned by the RepositoryManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_connection(
        self,
        request: repositories.GetConnectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[repositories.GetConnectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_connection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RepositoryManager server.
        """
        return request, metadata

    def post_get_connection(
        self, response: repositories.Connection
    ) -> repositories.Connection:
        """Post-rpc interceptor for get_connection

        Override in a subclass to manipulate the response
        after it is returned by the RepositoryManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_repository(
        self,
        request: repositories.GetRepositoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[repositories.GetRepositoryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_repository

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RepositoryManager server.
        """
        return request, metadata

    def post_get_repository(
        self, response: repositories.Repository
    ) -> repositories.Repository:
        """Post-rpc interceptor for get_repository

        Override in a subclass to manipulate the response
        after it is returned by the RepositoryManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_connections(
        self,
        request: repositories.ListConnectionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[repositories.ListConnectionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_connections

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RepositoryManager server.
        """
        return request, metadata

    def post_list_connections(
        self, response: repositories.ListConnectionsResponse
    ) -> repositories.ListConnectionsResponse:
        """Post-rpc interceptor for list_connections

        Override in a subclass to manipulate the response
        after it is returned by the RepositoryManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_repositories(
        self,
        request: repositories.ListRepositoriesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[repositories.ListRepositoriesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_repositories

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RepositoryManager server.
        """
        return request, metadata

    def post_list_repositories(
        self, response: repositories.ListRepositoriesResponse
    ) -> repositories.ListRepositoriesResponse:
        """Post-rpc interceptor for list_repositories

        Override in a subclass to manipulate the response
        after it is returned by the RepositoryManager server but before
        it is returned to user code.
        """
        return response

    def pre_update_connection(
        self,
        request: repositories.UpdateConnectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[repositories.UpdateConnectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_connection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RepositoryManager server.
        """
        return request, metadata

    def post_update_connection(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_connection

        Override in a subclass to manipulate the response
        after it is returned by the RepositoryManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_iam_policy(
        self,
        request: iam_policy_pb2.GetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.GetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RepositoryManager server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the RepositoryManager server but before
        it is returned to user code.
        """
        return response

    def pre_set_iam_policy(
        self,
        request: iam_policy_pb2.SetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.SetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RepositoryManager server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the RepositoryManager server but before
        it is returned to user code.
        """
        return response

    def pre_test_iam_permissions(
        self,
        request: iam_policy_pb2.TestIamPermissionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.TestIamPermissionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RepositoryManager server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the RepositoryManager server but before
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
        before they are sent to the RepositoryManager server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the RepositoryManager server but before
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
        before they are sent to the RepositoryManager server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the RepositoryManager server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class RepositoryManagerRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: RepositoryManagerRestInterceptor


class RepositoryManagerRestTransport(_BaseRepositoryManagerRestTransport):
    """REST backend synchronous transport for RepositoryManager.

    Manages connections to source code repositories.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "cloudbuild.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[RepositoryManagerRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'cloudbuild.googleapis.com').
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
        self._interceptor = interceptor or RepositoryManagerRestInterceptor()
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
                        "uri": "/v2/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v2/{name=projects/*/locations/*/operations/*}",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v2",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _BatchCreateRepositories(
        _BaseRepositoryManagerRestTransport._BaseBatchCreateRepositories,
        RepositoryManagerRestStub,
    ):
        def __hash__(self):
            return hash("RepositoryManagerRestTransport.BatchCreateRepositories")

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
            request: repositories.BatchCreateRepositoriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the batch create repositories method over HTTP.

            Args:
                request (~.repositories.BatchCreateRepositoriesRequest):
                    The request object. Message for creating repositoritories
                in batch.
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
                _BaseRepositoryManagerRestTransport._BaseBatchCreateRepositories._get_http_options()
            )
            request, metadata = self._interceptor.pre_batch_create_repositories(
                request, metadata
            )
            transcoded_request = _BaseRepositoryManagerRestTransport._BaseBatchCreateRepositories._get_transcoded_request(
                http_options, request
            )

            body = _BaseRepositoryManagerRestTransport._BaseBatchCreateRepositories._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRepositoryManagerRestTransport._BaseBatchCreateRepositories._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RepositoryManagerRestTransport._BatchCreateRepositories._get_response(
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
            resp = self._interceptor.post_batch_create_repositories(resp)
            return resp

    class _CreateConnection(
        _BaseRepositoryManagerRestTransport._BaseCreateConnection,
        RepositoryManagerRestStub,
    ):
        def __hash__(self):
            return hash("RepositoryManagerRestTransport.CreateConnection")

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
            request: repositories.CreateConnectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create connection method over HTTP.

            Args:
                request (~.repositories.CreateConnectionRequest):
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
                _BaseRepositoryManagerRestTransport._BaseCreateConnection._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_connection(
                request, metadata
            )
            transcoded_request = _BaseRepositoryManagerRestTransport._BaseCreateConnection._get_transcoded_request(
                http_options, request
            )

            body = _BaseRepositoryManagerRestTransport._BaseCreateConnection._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRepositoryManagerRestTransport._BaseCreateConnection._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RepositoryManagerRestTransport._CreateConnection._get_response(
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

    class _CreateRepository(
        _BaseRepositoryManagerRestTransport._BaseCreateRepository,
        RepositoryManagerRestStub,
    ):
        def __hash__(self):
            return hash("RepositoryManagerRestTransport.CreateRepository")

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
            request: repositories.CreateRepositoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create repository method over HTTP.

            Args:
                request (~.repositories.CreateRepositoryRequest):
                    The request object. Message for creating a Repository.
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
                _BaseRepositoryManagerRestTransport._BaseCreateRepository._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_repository(
                request, metadata
            )
            transcoded_request = _BaseRepositoryManagerRestTransport._BaseCreateRepository._get_transcoded_request(
                http_options, request
            )

            body = _BaseRepositoryManagerRestTransport._BaseCreateRepository._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRepositoryManagerRestTransport._BaseCreateRepository._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RepositoryManagerRestTransport._CreateRepository._get_response(
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
            resp = self._interceptor.post_create_repository(resp)
            return resp

    class _DeleteConnection(
        _BaseRepositoryManagerRestTransport._BaseDeleteConnection,
        RepositoryManagerRestStub,
    ):
        def __hash__(self):
            return hash("RepositoryManagerRestTransport.DeleteConnection")

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
            request: repositories.DeleteConnectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete connection method over HTTP.

            Args:
                request (~.repositories.DeleteConnectionRequest):
                    The request object. Message for deleting a Connection.
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
                _BaseRepositoryManagerRestTransport._BaseDeleteConnection._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_connection(
                request, metadata
            )
            transcoded_request = _BaseRepositoryManagerRestTransport._BaseDeleteConnection._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRepositoryManagerRestTransport._BaseDeleteConnection._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RepositoryManagerRestTransport._DeleteConnection._get_response(
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

    class _DeleteRepository(
        _BaseRepositoryManagerRestTransport._BaseDeleteRepository,
        RepositoryManagerRestStub,
    ):
        def __hash__(self):
            return hash("RepositoryManagerRestTransport.DeleteRepository")

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
            request: repositories.DeleteRepositoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete repository method over HTTP.

            Args:
                request (~.repositories.DeleteRepositoryRequest):
                    The request object. Message for deleting a Repository.
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
                _BaseRepositoryManagerRestTransport._BaseDeleteRepository._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_repository(
                request, metadata
            )
            transcoded_request = _BaseRepositoryManagerRestTransport._BaseDeleteRepository._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRepositoryManagerRestTransport._BaseDeleteRepository._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RepositoryManagerRestTransport._DeleteRepository._get_response(
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
            resp = self._interceptor.post_delete_repository(resp)
            return resp

    class _FetchGitRefs(
        _BaseRepositoryManagerRestTransport._BaseFetchGitRefs, RepositoryManagerRestStub
    ):
        def __hash__(self):
            return hash("RepositoryManagerRestTransport.FetchGitRefs")

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
            request: repositories.FetchGitRefsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> repositories.FetchGitRefsResponse:
            r"""Call the fetch git refs method over HTTP.

            Args:
                request (~.repositories.FetchGitRefsRequest):
                    The request object. Request for fetching git refs
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.repositories.FetchGitRefsResponse:
                    Response for fetching git refs
            """

            http_options = (
                _BaseRepositoryManagerRestTransport._BaseFetchGitRefs._get_http_options()
            )
            request, metadata = self._interceptor.pre_fetch_git_refs(request, metadata)
            transcoded_request = _BaseRepositoryManagerRestTransport._BaseFetchGitRefs._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRepositoryManagerRestTransport._BaseFetchGitRefs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RepositoryManagerRestTransport._FetchGitRefs._get_response(
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
            resp = repositories.FetchGitRefsResponse()
            pb_resp = repositories.FetchGitRefsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_git_refs(resp)
            return resp

    class _FetchLinkableRepositories(
        _BaseRepositoryManagerRestTransport._BaseFetchLinkableRepositories,
        RepositoryManagerRestStub,
    ):
        def __hash__(self):
            return hash("RepositoryManagerRestTransport.FetchLinkableRepositories")

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
            request: repositories.FetchLinkableRepositoriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> repositories.FetchLinkableRepositoriesResponse:
            r"""Call the fetch linkable
            repositories method over HTTP.

                Args:
                    request (~.repositories.FetchLinkableRepositoriesRequest):
                        The request object. Request message for
                    FetchLinkableRepositories.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.repositories.FetchLinkableRepositoriesResponse:
                        Response message for
                    FetchLinkableRepositories.

            """

            http_options = (
                _BaseRepositoryManagerRestTransport._BaseFetchLinkableRepositories._get_http_options()
            )
            request, metadata = self._interceptor.pre_fetch_linkable_repositories(
                request, metadata
            )
            transcoded_request = _BaseRepositoryManagerRestTransport._BaseFetchLinkableRepositories._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRepositoryManagerRestTransport._BaseFetchLinkableRepositories._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RepositoryManagerRestTransport._FetchLinkableRepositories._get_response(
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
            resp = repositories.FetchLinkableRepositoriesResponse()
            pb_resp = repositories.FetchLinkableRepositoriesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_linkable_repositories(resp)
            return resp

    class _FetchReadToken(
        _BaseRepositoryManagerRestTransport._BaseFetchReadToken,
        RepositoryManagerRestStub,
    ):
        def __hash__(self):
            return hash("RepositoryManagerRestTransport.FetchReadToken")

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
            request: repositories.FetchReadTokenRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> repositories.FetchReadTokenResponse:
            r"""Call the fetch read token method over HTTP.

            Args:
                request (~.repositories.FetchReadTokenRequest):
                    The request object. Message for fetching SCM read token.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.repositories.FetchReadTokenResponse:
                    Message for responding to get read
                token.

            """

            http_options = (
                _BaseRepositoryManagerRestTransport._BaseFetchReadToken._get_http_options()
            )
            request, metadata = self._interceptor.pre_fetch_read_token(
                request, metadata
            )
            transcoded_request = _BaseRepositoryManagerRestTransport._BaseFetchReadToken._get_transcoded_request(
                http_options, request
            )

            body = _BaseRepositoryManagerRestTransport._BaseFetchReadToken._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRepositoryManagerRestTransport._BaseFetchReadToken._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RepositoryManagerRestTransport._FetchReadToken._get_response(
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
            resp = repositories.FetchReadTokenResponse()
            pb_resp = repositories.FetchReadTokenResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_read_token(resp)
            return resp

    class _FetchReadWriteToken(
        _BaseRepositoryManagerRestTransport._BaseFetchReadWriteToken,
        RepositoryManagerRestStub,
    ):
        def __hash__(self):
            return hash("RepositoryManagerRestTransport.FetchReadWriteToken")

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
            request: repositories.FetchReadWriteTokenRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> repositories.FetchReadWriteTokenResponse:
            r"""Call the fetch read write token method over HTTP.

            Args:
                request (~.repositories.FetchReadWriteTokenRequest):
                    The request object. Message for fetching SCM read/write
                token.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.repositories.FetchReadWriteTokenResponse:
                    Message for responding to get
                read/write token.

            """

            http_options = (
                _BaseRepositoryManagerRestTransport._BaseFetchReadWriteToken._get_http_options()
            )
            request, metadata = self._interceptor.pre_fetch_read_write_token(
                request, metadata
            )
            transcoded_request = _BaseRepositoryManagerRestTransport._BaseFetchReadWriteToken._get_transcoded_request(
                http_options, request
            )

            body = _BaseRepositoryManagerRestTransport._BaseFetchReadWriteToken._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRepositoryManagerRestTransport._BaseFetchReadWriteToken._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RepositoryManagerRestTransport._FetchReadWriteToken._get_response(
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
            resp = repositories.FetchReadWriteTokenResponse()
            pb_resp = repositories.FetchReadWriteTokenResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_read_write_token(resp)
            return resp

    class _GetConnection(
        _BaseRepositoryManagerRestTransport._BaseGetConnection,
        RepositoryManagerRestStub,
    ):
        def __hash__(self):
            return hash("RepositoryManagerRestTransport.GetConnection")

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
            request: repositories.GetConnectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> repositories.Connection:
            r"""Call the get connection method over HTTP.

            Args:
                request (~.repositories.GetConnectionRequest):
                    The request object. Message for getting the details of a
                Connection.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.repositories.Connection:
                    A connection to a SCM like GitHub,
                GitHub Enterprise, Bitbucket Data
                Center, Bitbucket Cloud or GitLab.

            """

            http_options = (
                _BaseRepositoryManagerRestTransport._BaseGetConnection._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_connection(request, metadata)
            transcoded_request = _BaseRepositoryManagerRestTransport._BaseGetConnection._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRepositoryManagerRestTransport._BaseGetConnection._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RepositoryManagerRestTransport._GetConnection._get_response(
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
            resp = repositories.Connection()
            pb_resp = repositories.Connection.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_connection(resp)
            return resp

    class _GetRepository(
        _BaseRepositoryManagerRestTransport._BaseGetRepository,
        RepositoryManagerRestStub,
    ):
        def __hash__(self):
            return hash("RepositoryManagerRestTransport.GetRepository")

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
            request: repositories.GetRepositoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> repositories.Repository:
            r"""Call the get repository method over HTTP.

            Args:
                request (~.repositories.GetRepositoryRequest):
                    The request object. Message for getting the details of a
                Repository.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.repositories.Repository:
                    A repository associated to a parent
                connection.

            """

            http_options = (
                _BaseRepositoryManagerRestTransport._BaseGetRepository._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_repository(request, metadata)
            transcoded_request = _BaseRepositoryManagerRestTransport._BaseGetRepository._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRepositoryManagerRestTransport._BaseGetRepository._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RepositoryManagerRestTransport._GetRepository._get_response(
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
            resp = repositories.Repository()
            pb_resp = repositories.Repository.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_repository(resp)
            return resp

    class _ListConnections(
        _BaseRepositoryManagerRestTransport._BaseListConnections,
        RepositoryManagerRestStub,
    ):
        def __hash__(self):
            return hash("RepositoryManagerRestTransport.ListConnections")

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
            request: repositories.ListConnectionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> repositories.ListConnectionsResponse:
            r"""Call the list connections method over HTTP.

            Args:
                request (~.repositories.ListConnectionsRequest):
                    The request object. Message for requesting list of
                Connections.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.repositories.ListConnectionsResponse:
                    Message for response to listing
                Connections.

            """

            http_options = (
                _BaseRepositoryManagerRestTransport._BaseListConnections._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_connections(
                request, metadata
            )
            transcoded_request = _BaseRepositoryManagerRestTransport._BaseListConnections._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRepositoryManagerRestTransport._BaseListConnections._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RepositoryManagerRestTransport._ListConnections._get_response(
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
            resp = repositories.ListConnectionsResponse()
            pb_resp = repositories.ListConnectionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_connections(resp)
            return resp

    class _ListRepositories(
        _BaseRepositoryManagerRestTransport._BaseListRepositories,
        RepositoryManagerRestStub,
    ):
        def __hash__(self):
            return hash("RepositoryManagerRestTransport.ListRepositories")

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
            request: repositories.ListRepositoriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> repositories.ListRepositoriesResponse:
            r"""Call the list repositories method over HTTP.

            Args:
                request (~.repositories.ListRepositoriesRequest):
                    The request object. Message for requesting list of
                Repositories.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.repositories.ListRepositoriesResponse:
                    Message for response to listing
                Repositories.

            """

            http_options = (
                _BaseRepositoryManagerRestTransport._BaseListRepositories._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_repositories(
                request, metadata
            )
            transcoded_request = _BaseRepositoryManagerRestTransport._BaseListRepositories._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRepositoryManagerRestTransport._BaseListRepositories._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RepositoryManagerRestTransport._ListRepositories._get_response(
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
            resp = repositories.ListRepositoriesResponse()
            pb_resp = repositories.ListRepositoriesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_repositories(resp)
            return resp

    class _UpdateConnection(
        _BaseRepositoryManagerRestTransport._BaseUpdateConnection,
        RepositoryManagerRestStub,
    ):
        def __hash__(self):
            return hash("RepositoryManagerRestTransport.UpdateConnection")

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
            request: repositories.UpdateConnectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update connection method over HTTP.

            Args:
                request (~.repositories.UpdateConnectionRequest):
                    The request object. Message for updating a Connection.
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
                _BaseRepositoryManagerRestTransport._BaseUpdateConnection._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_connection(
                request, metadata
            )
            transcoded_request = _BaseRepositoryManagerRestTransport._BaseUpdateConnection._get_transcoded_request(
                http_options, request
            )

            body = _BaseRepositoryManagerRestTransport._BaseUpdateConnection._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRepositoryManagerRestTransport._BaseUpdateConnection._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RepositoryManagerRestTransport._UpdateConnection._get_response(
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
    def batch_create_repositories(
        self,
    ) -> Callable[
        [repositories.BatchCreateRepositoriesRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchCreateRepositories(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_connection(
        self,
    ) -> Callable[[repositories.CreateConnectionRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateConnection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_repository(
        self,
    ) -> Callable[[repositories.CreateRepositoryRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRepository(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_connection(
        self,
    ) -> Callable[[repositories.DeleteConnectionRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteConnection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_repository(
        self,
    ) -> Callable[[repositories.DeleteRepositoryRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteRepository(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_git_refs(
        self,
    ) -> Callable[
        [repositories.FetchGitRefsRequest], repositories.FetchGitRefsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchGitRefs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_linkable_repositories(
        self,
    ) -> Callable[
        [repositories.FetchLinkableRepositoriesRequest],
        repositories.FetchLinkableRepositoriesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchLinkableRepositories(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_read_token(
        self,
    ) -> Callable[
        [repositories.FetchReadTokenRequest], repositories.FetchReadTokenResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchReadToken(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_read_write_token(
        self,
    ) -> Callable[
        [repositories.FetchReadWriteTokenRequest],
        repositories.FetchReadWriteTokenResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchReadWriteToken(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_connection(
        self,
    ) -> Callable[[repositories.GetConnectionRequest], repositories.Connection]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetConnection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_repository(
        self,
    ) -> Callable[[repositories.GetRepositoryRequest], repositories.Repository]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRepository(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_connections(
        self,
    ) -> Callable[
        [repositories.ListConnectionsRequest], repositories.ListConnectionsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListConnections(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_repositories(
        self,
    ) -> Callable[
        [repositories.ListRepositoriesRequest], repositories.ListRepositoriesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRepositories(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_connection(
        self,
    ) -> Callable[[repositories.UpdateConnectionRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateConnection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_iam_policy(self):
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _GetIamPolicy(
        _BaseRepositoryManagerRestTransport._BaseGetIamPolicy, RepositoryManagerRestStub
    ):
        def __hash__(self):
            return hash("RepositoryManagerRestTransport.GetIamPolicy")

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
            request: iam_policy_pb2.GetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.GetIamPolicyRequest):
                    The request object for GetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from GetIamPolicy method.
            """

            http_options = (
                _BaseRepositoryManagerRestTransport._BaseGetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            transcoded_request = _BaseRepositoryManagerRestTransport._BaseGetIamPolicy._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRepositoryManagerRestTransport._BaseGetIamPolicy._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RepositoryManagerRestTransport._GetIamPolicy._get_response(
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
            resp = policy_pb2.Policy()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    @property
    def set_iam_policy(self):
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _SetIamPolicy(
        _BaseRepositoryManagerRestTransport._BaseSetIamPolicy, RepositoryManagerRestStub
    ):
        def __hash__(self):
            return hash("RepositoryManagerRestTransport.SetIamPolicy")

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
            request: iam_policy_pb2.SetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the set iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.SetIamPolicyRequest):
                    The request object for SetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from SetIamPolicy method.
            """

            http_options = (
                _BaseRepositoryManagerRestTransport._BaseSetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            transcoded_request = _BaseRepositoryManagerRestTransport._BaseSetIamPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseRepositoryManagerRestTransport._BaseSetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRepositoryManagerRestTransport._BaseSetIamPolicy._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RepositoryManagerRestTransport._SetIamPolicy._get_response(
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

            content = response.content.decode("utf-8")
            resp = policy_pb2.Policy()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    @property
    def test_iam_permissions(self):
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    class _TestIamPermissions(
        _BaseRepositoryManagerRestTransport._BaseTestIamPermissions,
        RepositoryManagerRestStub,
    ):
        def __hash__(self):
            return hash("RepositoryManagerRestTransport.TestIamPermissions")

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
            request: iam_policy_pb2.TestIamPermissionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> iam_policy_pb2.TestIamPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (iam_policy_pb2.TestIamPermissionsRequest):
                    The request object for TestIamPermissions method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                iam_policy_pb2.TestIamPermissionsResponse: Response from TestIamPermissions method.
            """

            http_options = (
                _BaseRepositoryManagerRestTransport._BaseTestIamPermissions._get_http_options()
            )
            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            transcoded_request = _BaseRepositoryManagerRestTransport._BaseTestIamPermissions._get_transcoded_request(
                http_options, request
            )

            body = _BaseRepositoryManagerRestTransport._BaseTestIamPermissions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRepositoryManagerRestTransport._BaseTestIamPermissions._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RepositoryManagerRestTransport._TestIamPermissions._get_response(
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

            content = response.content.decode("utf-8")
            resp = iam_policy_pb2.TestIamPermissionsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseRepositoryManagerRestTransport._BaseCancelOperation,
        RepositoryManagerRestStub,
    ):
        def __hash__(self):
            return hash("RepositoryManagerRestTransport.CancelOperation")

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
                _BaseRepositoryManagerRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseRepositoryManagerRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = _BaseRepositoryManagerRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRepositoryManagerRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RepositoryManagerRestTransport._CancelOperation._get_response(
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
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseRepositoryManagerRestTransport._BaseGetOperation, RepositoryManagerRestStub
    ):
        def __hash__(self):
            return hash("RepositoryManagerRestTransport.GetOperation")

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
                _BaseRepositoryManagerRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseRepositoryManagerRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRepositoryManagerRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RepositoryManagerRestTransport._GetOperation._get_response(
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
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("RepositoryManagerRestTransport",)
