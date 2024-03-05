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
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import (
    gapic_v1,
    operations_v1,
    path_template,
    rest_helpers,
    rest_streaming,
)
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.datacatalog_lineage_v1.types import lineage

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import LineageTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class LineageRestInterceptor:
    """Interceptor for Lineage.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the LineageRestTransport.

    .. code-block:: python
        class MyCustomLineageInterceptor(LineageRestInterceptor):
            def pre_batch_search_link_processes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_search_link_processes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_lineage_event(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_lineage_event(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_process(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_process(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_run(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_run(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_lineage_event(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_process(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_process(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_run(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_run(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_lineage_event(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_lineage_event(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_process(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_process(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_run(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_run(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_lineage_events(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_lineage_events(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_processes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_processes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_runs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_runs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_process_open_lineage_run_event(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_process_open_lineage_run_event(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_links(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_links(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_process(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_process(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_run(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_run(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = LineageRestTransport(interceptor=MyCustomLineageInterceptor())
        client = LineageClient(transport=transport)


    """

    def pre_batch_search_link_processes(
        self,
        request: lineage.BatchSearchLinkProcessesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lineage.BatchSearchLinkProcessesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_search_link_processes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Lineage server.
        """
        return request, metadata

    def post_batch_search_link_processes(
        self, response: lineage.BatchSearchLinkProcessesResponse
    ) -> lineage.BatchSearchLinkProcessesResponse:
        """Post-rpc interceptor for batch_search_link_processes

        Override in a subclass to manipulate the response
        after it is returned by the Lineage server but before
        it is returned to user code.
        """
        return response

    def pre_create_lineage_event(
        self,
        request: lineage.CreateLineageEventRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lineage.CreateLineageEventRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_lineage_event

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Lineage server.
        """
        return request, metadata

    def post_create_lineage_event(
        self, response: lineage.LineageEvent
    ) -> lineage.LineageEvent:
        """Post-rpc interceptor for create_lineage_event

        Override in a subclass to manipulate the response
        after it is returned by the Lineage server but before
        it is returned to user code.
        """
        return response

    def pre_create_process(
        self, request: lineage.CreateProcessRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[lineage.CreateProcessRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_process

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Lineage server.
        """
        return request, metadata

    def post_create_process(self, response: lineage.Process) -> lineage.Process:
        """Post-rpc interceptor for create_process

        Override in a subclass to manipulate the response
        after it is returned by the Lineage server but before
        it is returned to user code.
        """
        return response

    def pre_create_run(
        self, request: lineage.CreateRunRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[lineage.CreateRunRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_run

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Lineage server.
        """
        return request, metadata

    def post_create_run(self, response: lineage.Run) -> lineage.Run:
        """Post-rpc interceptor for create_run

        Override in a subclass to manipulate the response
        after it is returned by the Lineage server but before
        it is returned to user code.
        """
        return response

    def pre_delete_lineage_event(
        self,
        request: lineage.DeleteLineageEventRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lineage.DeleteLineageEventRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_lineage_event

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Lineage server.
        """
        return request, metadata

    def pre_delete_process(
        self, request: lineage.DeleteProcessRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[lineage.DeleteProcessRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_process

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Lineage server.
        """
        return request, metadata

    def post_delete_process(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_process

        Override in a subclass to manipulate the response
        after it is returned by the Lineage server but before
        it is returned to user code.
        """
        return response

    def pre_delete_run(
        self, request: lineage.DeleteRunRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[lineage.DeleteRunRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_run

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Lineage server.
        """
        return request, metadata

    def post_delete_run(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_run

        Override in a subclass to manipulate the response
        after it is returned by the Lineage server but before
        it is returned to user code.
        """
        return response

    def pre_get_lineage_event(
        self,
        request: lineage.GetLineageEventRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lineage.GetLineageEventRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_lineage_event

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Lineage server.
        """
        return request, metadata

    def post_get_lineage_event(
        self, response: lineage.LineageEvent
    ) -> lineage.LineageEvent:
        """Post-rpc interceptor for get_lineage_event

        Override in a subclass to manipulate the response
        after it is returned by the Lineage server but before
        it is returned to user code.
        """
        return response

    def pre_get_process(
        self, request: lineage.GetProcessRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[lineage.GetProcessRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_process

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Lineage server.
        """
        return request, metadata

    def post_get_process(self, response: lineage.Process) -> lineage.Process:
        """Post-rpc interceptor for get_process

        Override in a subclass to manipulate the response
        after it is returned by the Lineage server but before
        it is returned to user code.
        """
        return response

    def pre_get_run(
        self, request: lineage.GetRunRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[lineage.GetRunRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_run

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Lineage server.
        """
        return request, metadata

    def post_get_run(self, response: lineage.Run) -> lineage.Run:
        """Post-rpc interceptor for get_run

        Override in a subclass to manipulate the response
        after it is returned by the Lineage server but before
        it is returned to user code.
        """
        return response

    def pre_list_lineage_events(
        self,
        request: lineage.ListLineageEventsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lineage.ListLineageEventsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_lineage_events

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Lineage server.
        """
        return request, metadata

    def post_list_lineage_events(
        self, response: lineage.ListLineageEventsResponse
    ) -> lineage.ListLineageEventsResponse:
        """Post-rpc interceptor for list_lineage_events

        Override in a subclass to manipulate the response
        after it is returned by the Lineage server but before
        it is returned to user code.
        """
        return response

    def pre_list_processes(
        self, request: lineage.ListProcessesRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[lineage.ListProcessesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_processes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Lineage server.
        """
        return request, metadata

    def post_list_processes(
        self, response: lineage.ListProcessesResponse
    ) -> lineage.ListProcessesResponse:
        """Post-rpc interceptor for list_processes

        Override in a subclass to manipulate the response
        after it is returned by the Lineage server but before
        it is returned to user code.
        """
        return response

    def pre_list_runs(
        self, request: lineage.ListRunsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[lineage.ListRunsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_runs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Lineage server.
        """
        return request, metadata

    def post_list_runs(
        self, response: lineage.ListRunsResponse
    ) -> lineage.ListRunsResponse:
        """Post-rpc interceptor for list_runs

        Override in a subclass to manipulate the response
        after it is returned by the Lineage server but before
        it is returned to user code.
        """
        return response

    def pre_process_open_lineage_run_event(
        self,
        request: lineage.ProcessOpenLineageRunEventRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lineage.ProcessOpenLineageRunEventRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for process_open_lineage_run_event

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Lineage server.
        """
        return request, metadata

    def post_process_open_lineage_run_event(
        self, response: lineage.ProcessOpenLineageRunEventResponse
    ) -> lineage.ProcessOpenLineageRunEventResponse:
        """Post-rpc interceptor for process_open_lineage_run_event

        Override in a subclass to manipulate the response
        after it is returned by the Lineage server but before
        it is returned to user code.
        """
        return response

    def pre_search_links(
        self, request: lineage.SearchLinksRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[lineage.SearchLinksRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for search_links

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Lineage server.
        """
        return request, metadata

    def post_search_links(
        self, response: lineage.SearchLinksResponse
    ) -> lineage.SearchLinksResponse:
        """Post-rpc interceptor for search_links

        Override in a subclass to manipulate the response
        after it is returned by the Lineage server but before
        it is returned to user code.
        """
        return response

    def pre_update_process(
        self, request: lineage.UpdateProcessRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[lineage.UpdateProcessRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_process

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Lineage server.
        """
        return request, metadata

    def post_update_process(self, response: lineage.Process) -> lineage.Process:
        """Post-rpc interceptor for update_process

        Override in a subclass to manipulate the response
        after it is returned by the Lineage server but before
        it is returned to user code.
        """
        return response

    def pre_update_run(
        self, request: lineage.UpdateRunRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[lineage.UpdateRunRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_run

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Lineage server.
        """
        return request, metadata

    def post_update_run(self, response: lineage.Run) -> lineage.Run:
        """Post-rpc interceptor for update_run

        Override in a subclass to manipulate the response
        after it is returned by the Lineage server but before
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
        before they are sent to the Lineage server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the Lineage server but before
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
        before they are sent to the Lineage server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the Lineage server but before
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
        before they are sent to the Lineage server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Lineage server but before
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
        before they are sent to the Lineage server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Lineage server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class LineageRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: LineageRestInterceptor


class LineageRestTransport(LineageTransport):
    """REST backend transport for Lineage.

    Lineage is used to track data flows between assets over time. You
    can create
    [LineageEvents][google.cloud.datacatalog.lineage.v1.LineageEvent] to
    record lineage between multiple sources and a single target, for
    example, when table data is based on data from multiple tables.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "datalineage.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[LineageRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'datalineage.googleapis.com').
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
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or LineageRestInterceptor()
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

    class _BatchSearchLinkProcesses(LineageRestStub):
        def __hash__(self):
            return hash("BatchSearchLinkProcesses")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lineage.BatchSearchLinkProcessesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lineage.BatchSearchLinkProcessesResponse:
            r"""Call the batch search link
            processes method over HTTP.

                Args:
                    request (~.lineage.BatchSearchLinkProcessesRequest):
                        The request object. Request message for
                    [BatchSearchLinkProcesses][google.cloud.datacatalog.lineage.v1.Lineage.BatchSearchLinkProcesses].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.lineage.BatchSearchLinkProcessesResponse:
                        Response message for
                    [BatchSearchLinkProcesses][google.cloud.datacatalog.lineage.v1.Lineage.BatchSearchLinkProcesses].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}:batchSearchLinkProcesses",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_batch_search_link_processes(
                request, metadata
            )
            pb_request = lineage.BatchSearchLinkProcessesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = lineage.BatchSearchLinkProcessesResponse()
            pb_resp = lineage.BatchSearchLinkProcessesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_search_link_processes(resp)
            return resp

    class _CreateLineageEvent(LineageRestStub):
        def __hash__(self):
            return hash("CreateLineageEvent")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lineage.CreateLineageEventRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lineage.LineageEvent:
            r"""Call the create lineage event method over HTTP.

            Args:
                request (~.lineage.CreateLineageEventRequest):
                    The request object. Request message for
                [CreateLineageEvent][google.cloud.datacatalog.lineage.v1.CreateLineageEvent].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lineage.LineageEvent:
                    A lineage event represents an
                operation on assets. Within the
                operation, the data flows from the
                source to the target defined in the
                links field.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/processes/*/runs/*}/lineageEvents",
                    "body": "lineage_event",
                },
            ]
            request, metadata = self._interceptor.pre_create_lineage_event(
                request, metadata
            )
            pb_request = lineage.CreateLineageEventRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = lineage.LineageEvent()
            pb_resp = lineage.LineageEvent.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_lineage_event(resp)
            return resp

    class _CreateProcess(LineageRestStub):
        def __hash__(self):
            return hash("CreateProcess")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lineage.CreateProcessRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lineage.Process:
            r"""Call the create process method over HTTP.

            Args:
                request (~.lineage.CreateProcessRequest):
                    The request object. Request message for
                [CreateProcess][google.cloud.datacatalog.lineage.v1.CreateProcess].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lineage.Process:
                    A process is the definition of a data
                transformation operation.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/processes",
                    "body": "process",
                },
            ]
            request, metadata = self._interceptor.pre_create_process(request, metadata)
            pb_request = lineage.CreateProcessRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = lineage.Process()
            pb_resp = lineage.Process.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_process(resp)
            return resp

    class _CreateRun(LineageRestStub):
        def __hash__(self):
            return hash("CreateRun")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lineage.CreateRunRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lineage.Run:
            r"""Call the create run method over HTTP.

            Args:
                request (~.lineage.CreateRunRequest):
                    The request object. Request message for
                [CreateRun][google.cloud.datacatalog.lineage.v1.CreateRun].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lineage.Run:
                    A lineage run represents an execution
                of a process that creates lineage
                events.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/processes/*}/runs",
                    "body": "run",
                },
            ]
            request, metadata = self._interceptor.pre_create_run(request, metadata)
            pb_request = lineage.CreateRunRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = lineage.Run()
            pb_resp = lineage.Run.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_run(resp)
            return resp

    class _DeleteLineageEvent(LineageRestStub):
        def __hash__(self):
            return hash("DeleteLineageEvent")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lineage.DeleteLineageEventRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete lineage event method over HTTP.

            Args:
                request (~.lineage.DeleteLineageEventRequest):
                    The request object. Request message for
                [DeleteLineageEvent][google.cloud.datacatalog.lineage.v1.DeleteLineageEvent].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/processes/*/runs/*/lineageEvents/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_lineage_event(
                request, metadata
            )
            pb_request = lineage.DeleteLineageEventRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteProcess(LineageRestStub):
        def __hash__(self):
            return hash("DeleteProcess")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lineage.DeleteProcessRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete process method over HTTP.

            Args:
                request (~.lineage.DeleteProcessRequest):
                    The request object. Request message for
                [DeleteProcess][google.cloud.datacatalog.lineage.v1.DeleteProcess].
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/processes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_process(request, metadata)
            pb_request = lineage.DeleteProcessRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_process(resp)
            return resp

    class _DeleteRun(LineageRestStub):
        def __hash__(self):
            return hash("DeleteRun")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lineage.DeleteRunRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete run method over HTTP.

            Args:
                request (~.lineage.DeleteRunRequest):
                    The request object. Request message for
                [DeleteRun][google.cloud.datacatalog.lineage.v1.DeleteRun].
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/processes/*/runs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_run(request, metadata)
            pb_request = lineage.DeleteRunRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_run(resp)
            return resp

    class _GetLineageEvent(LineageRestStub):
        def __hash__(self):
            return hash("GetLineageEvent")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lineage.GetLineageEventRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lineage.LineageEvent:
            r"""Call the get lineage event method over HTTP.

            Args:
                request (~.lineage.GetLineageEventRequest):
                    The request object. Request message for
                [GetLineageEvent][google.cloud.datacatalog.lineage.v1.GetLineageEvent].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lineage.LineageEvent:
                    A lineage event represents an
                operation on assets. Within the
                operation, the data flows from the
                source to the target defined in the
                links field.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/processes/*/runs/*/lineageEvents/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_lineage_event(
                request, metadata
            )
            pb_request = lineage.GetLineageEventRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = lineage.LineageEvent()
            pb_resp = lineage.LineageEvent.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_lineage_event(resp)
            return resp

    class _GetProcess(LineageRestStub):
        def __hash__(self):
            return hash("GetProcess")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lineage.GetProcessRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lineage.Process:
            r"""Call the get process method over HTTP.

            Args:
                request (~.lineage.GetProcessRequest):
                    The request object. Request message for
                [GetProcess][google.cloud.datacatalog.lineage.v1.GetProcess].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lineage.Process:
                    A process is the definition of a data
                transformation operation.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/processes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_process(request, metadata)
            pb_request = lineage.GetProcessRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = lineage.Process()
            pb_resp = lineage.Process.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_process(resp)
            return resp

    class _GetRun(LineageRestStub):
        def __hash__(self):
            return hash("GetRun")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lineage.GetRunRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lineage.Run:
            r"""Call the get run method over HTTP.

            Args:
                request (~.lineage.GetRunRequest):
                    The request object. Request message for
                [GetRun][google.cloud.datacatalog.lineage.v1.GetRun].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lineage.Run:
                    A lineage run represents an execution
                of a process that creates lineage
                events.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/processes/*/runs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_run(request, metadata)
            pb_request = lineage.GetRunRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = lineage.Run()
            pb_resp = lineage.Run.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_run(resp)
            return resp

    class _ListLineageEvents(LineageRestStub):
        def __hash__(self):
            return hash("ListLineageEvents")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lineage.ListLineageEventsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lineage.ListLineageEventsResponse:
            r"""Call the list lineage events method over HTTP.

            Args:
                request (~.lineage.ListLineageEventsRequest):
                    The request object. Request message for
                [ListLineageEvents][google.cloud.datacatalog.lineage.v1.ListLineageEvents].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lineage.ListLineageEventsResponse:
                    Response message for
                [ListLineageEvents][google.cloud.datacatalog.lineage.v1.ListLineageEvents].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/processes/*/runs/*}/lineageEvents",
                },
            ]
            request, metadata = self._interceptor.pre_list_lineage_events(
                request, metadata
            )
            pb_request = lineage.ListLineageEventsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = lineage.ListLineageEventsResponse()
            pb_resp = lineage.ListLineageEventsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_lineage_events(resp)
            return resp

    class _ListProcesses(LineageRestStub):
        def __hash__(self):
            return hash("ListProcesses")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lineage.ListProcessesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lineage.ListProcessesResponse:
            r"""Call the list processes method over HTTP.

            Args:
                request (~.lineage.ListProcessesRequest):
                    The request object. Request message for
                [ListProcesses][google.cloud.datacatalog.lineage.v1.ListProcesses].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lineage.ListProcessesResponse:
                    Response message for
                [ListProcesses][google.cloud.datacatalog.lineage.v1.ListProcesses].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/processes",
                },
            ]
            request, metadata = self._interceptor.pre_list_processes(request, metadata)
            pb_request = lineage.ListProcessesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = lineage.ListProcessesResponse()
            pb_resp = lineage.ListProcessesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_processes(resp)
            return resp

    class _ListRuns(LineageRestStub):
        def __hash__(self):
            return hash("ListRuns")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lineage.ListRunsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lineage.ListRunsResponse:
            r"""Call the list runs method over HTTP.

            Args:
                request (~.lineage.ListRunsRequest):
                    The request object. Request message for
                [ListRuns][google.cloud.datacatalog.lineage.v1.ListRuns].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lineage.ListRunsResponse:
                    Response message for
                [ListRuns][google.cloud.datacatalog.lineage.v1.ListRuns].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/processes/*}/runs",
                },
            ]
            request, metadata = self._interceptor.pre_list_runs(request, metadata)
            pb_request = lineage.ListRunsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = lineage.ListRunsResponse()
            pb_resp = lineage.ListRunsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_runs(resp)
            return resp

    class _ProcessOpenLineageRunEvent(LineageRestStub):
        def __hash__(self):
            return hash("ProcessOpenLineageRunEvent")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lineage.ProcessOpenLineageRunEventRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lineage.ProcessOpenLineageRunEventResponse:
            r"""Call the process open lineage run
            event method over HTTP.

                Args:
                    request (~.lineage.ProcessOpenLineageRunEventRequest):
                        The request object. Request message for
                    [ProcessOpenLineageRunEvent][google.cloud.datacatalog.lineage.v1.ProcessOpenLineageRunEvent].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.lineage.ProcessOpenLineageRunEventResponse:
                        Response message for
                    [ProcessOpenLineageRunEvent][google.cloud.datacatalog.lineage.v1.ProcessOpenLineageRunEvent].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}:processOpenLineageRunEvent",
                    "body": "open_lineage",
                },
            ]
            request, metadata = self._interceptor.pre_process_open_lineage_run_event(
                request, metadata
            )
            pb_request = lineage.ProcessOpenLineageRunEventRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = lineage.ProcessOpenLineageRunEventResponse()
            pb_resp = lineage.ProcessOpenLineageRunEventResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_process_open_lineage_run_event(resp)
            return resp

    class _SearchLinks(LineageRestStub):
        def __hash__(self):
            return hash("SearchLinks")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lineage.SearchLinksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lineage.SearchLinksResponse:
            r"""Call the search links method over HTTP.

            Args:
                request (~.lineage.SearchLinksRequest):
                    The request object. Request message for
                [SearchLinks][google.cloud.datacatalog.lineage.v1.Lineage.SearchLinks].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lineage.SearchLinksResponse:
                    Response message for
                [SearchLinks][google.cloud.datacatalog.lineage.v1.Lineage.SearchLinks].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}:searchLinks",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_search_links(request, metadata)
            pb_request = lineage.SearchLinksRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = lineage.SearchLinksResponse()
            pb_resp = lineage.SearchLinksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_search_links(resp)
            return resp

    class _UpdateProcess(LineageRestStub):
        def __hash__(self):
            return hash("UpdateProcess")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lineage.UpdateProcessRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lineage.Process:
            r"""Call the update process method over HTTP.

            Args:
                request (~.lineage.UpdateProcessRequest):
                    The request object. Request message for
                [UpdateProcess][google.cloud.datacatalog.lineage.v1.UpdateProcess].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lineage.Process:
                    A process is the definition of a data
                transformation operation.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{process.name=projects/*/locations/*/processes/*}",
                    "body": "process",
                },
            ]
            request, metadata = self._interceptor.pre_update_process(request, metadata)
            pb_request = lineage.UpdateProcessRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = lineage.Process()
            pb_resp = lineage.Process.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_process(resp)
            return resp

    class _UpdateRun(LineageRestStub):
        def __hash__(self):
            return hash("UpdateRun")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lineage.UpdateRunRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lineage.Run:
            r"""Call the update run method over HTTP.

            Args:
                request (~.lineage.UpdateRunRequest):
                    The request object. Request message for
                [UpdateRun][google.cloud.datacatalog.lineage.v1.UpdateRun].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lineage.Run:
                    A lineage run represents an execution
                of a process that creates lineage
                events.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{run.name=projects/*/locations/*/processes/*/runs/*}",
                    "body": "run",
                },
            ]
            request, metadata = self._interceptor.pre_update_run(request, metadata)
            pb_request = lineage.UpdateRunRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = lineage.Run()
            pb_resp = lineage.Run.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_run(resp)
            return resp

    @property
    def batch_search_link_processes(
        self,
    ) -> Callable[
        [lineage.BatchSearchLinkProcessesRequest],
        lineage.BatchSearchLinkProcessesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchSearchLinkProcesses(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_lineage_event(
        self,
    ) -> Callable[[lineage.CreateLineageEventRequest], lineage.LineageEvent]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateLineageEvent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_process(
        self,
    ) -> Callable[[lineage.CreateProcessRequest], lineage.Process]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateProcess(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_run(self) -> Callable[[lineage.CreateRunRequest], lineage.Run]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRun(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_lineage_event(
        self,
    ) -> Callable[[lineage.DeleteLineageEventRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteLineageEvent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_process(
        self,
    ) -> Callable[[lineage.DeleteProcessRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteProcess(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_run(
        self,
    ) -> Callable[[lineage.DeleteRunRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteRun(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_lineage_event(
        self,
    ) -> Callable[[lineage.GetLineageEventRequest], lineage.LineageEvent]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetLineageEvent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_process(self) -> Callable[[lineage.GetProcessRequest], lineage.Process]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetProcess(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_run(self) -> Callable[[lineage.GetRunRequest], lineage.Run]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRun(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_lineage_events(
        self,
    ) -> Callable[
        [lineage.ListLineageEventsRequest], lineage.ListLineageEventsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListLineageEvents(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_processes(
        self,
    ) -> Callable[[lineage.ListProcessesRequest], lineage.ListProcessesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListProcesses(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_runs(
        self,
    ) -> Callable[[lineage.ListRunsRequest], lineage.ListRunsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRuns(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def process_open_lineage_run_event(
        self,
    ) -> Callable[
        [lineage.ProcessOpenLineageRunEventRequest],
        lineage.ProcessOpenLineageRunEventResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ProcessOpenLineageRunEvent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_links(
        self,
    ) -> Callable[[lineage.SearchLinksRequest], lineage.SearchLinksResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchLinks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_process(
        self,
    ) -> Callable[[lineage.UpdateProcessRequest], lineage.Process]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateProcess(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_run(self) -> Callable[[lineage.UpdateRunRequest], lineage.Run]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateRun(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(LineageRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(LineageRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(LineageRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.Operation()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(LineageRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*}/operations",
                },
            ]

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("LineageRestTransport",)
