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
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.visionai_v1.types import lva_resources, lva_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import LiveVideoAnalyticsTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class LiveVideoAnalyticsRestInterceptor:
    """Interceptor for LiveVideoAnalytics.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the LiveVideoAnalyticsRestTransport.

    .. code-block:: python
        class MyCustomLiveVideoAnalyticsInterceptor(LiveVideoAnalyticsRestInterceptor):
            def pre_batch_run_process(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_run_process(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_analysis(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_analysis(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_operator(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_operator(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_process(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_process(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_analysis(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_analysis(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_operator(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_operator(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_process(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_process(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_analysis(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_analysis(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_operator(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_operator(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_process(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_process(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_analyses(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_analyses(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_operators(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_operators(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_processes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_processes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_public_operators(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_public_operators(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_resolve_operator_info(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_resolve_operator_info(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_analysis(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_analysis(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_operator(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_operator(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_process(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_process(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = LiveVideoAnalyticsRestTransport(interceptor=MyCustomLiveVideoAnalyticsInterceptor())
        client = LiveVideoAnalyticsClient(transport=transport)


    """

    def pre_batch_run_process(
        self,
        request: lva_service.BatchRunProcessRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lva_service.BatchRunProcessRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_run_process

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_batch_run_process(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for batch_run_process

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
        it is returned to user code.
        """
        return response

    def pre_create_analysis(
        self,
        request: lva_service.CreateAnalysisRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lva_service.CreateAnalysisRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_analysis

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_create_analysis(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_analysis

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
        it is returned to user code.
        """
        return response

    def pre_create_operator(
        self,
        request: lva_service.CreateOperatorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lva_service.CreateOperatorRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_operator

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_create_operator(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_operator

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
        it is returned to user code.
        """
        return response

    def pre_create_process(
        self,
        request: lva_service.CreateProcessRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lva_service.CreateProcessRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_process

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_create_process(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_process

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
        it is returned to user code.
        """
        return response

    def pre_delete_analysis(
        self,
        request: lva_service.DeleteAnalysisRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lva_service.DeleteAnalysisRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_analysis

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_delete_analysis(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_analysis

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operator(
        self,
        request: lva_service.DeleteOperatorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lva_service.DeleteOperatorRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_operator

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_delete_operator(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_operator

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
        it is returned to user code.
        """
        return response

    def pre_delete_process(
        self,
        request: lva_service.DeleteProcessRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lva_service.DeleteProcessRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_process

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_delete_process(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_process

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
        it is returned to user code.
        """
        return response

    def pre_get_analysis(
        self,
        request: lva_service.GetAnalysisRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lva_service.GetAnalysisRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_analysis

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_get_analysis(
        self, response: lva_resources.Analysis
    ) -> lva_resources.Analysis:
        """Post-rpc interceptor for get_analysis

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
        it is returned to user code.
        """
        return response

    def pre_get_operator(
        self,
        request: lva_service.GetOperatorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lva_service.GetOperatorRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_operator

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_get_operator(
        self, response: lva_resources.Operator
    ) -> lva_resources.Operator:
        """Post-rpc interceptor for get_operator

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
        it is returned to user code.
        """
        return response

    def pre_get_process(
        self,
        request: lva_service.GetProcessRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lva_service.GetProcessRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_process

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_get_process(
        self, response: lva_resources.Process
    ) -> lva_resources.Process:
        """Post-rpc interceptor for get_process

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
        it is returned to user code.
        """
        return response

    def pre_list_analyses(
        self,
        request: lva_service.ListAnalysesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lva_service.ListAnalysesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_analyses

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_list_analyses(
        self, response: lva_service.ListAnalysesResponse
    ) -> lva_service.ListAnalysesResponse:
        """Post-rpc interceptor for list_analyses

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
        it is returned to user code.
        """
        return response

    def pre_list_operators(
        self,
        request: lva_service.ListOperatorsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lva_service.ListOperatorsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_operators

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_list_operators(
        self, response: lva_service.ListOperatorsResponse
    ) -> lva_service.ListOperatorsResponse:
        """Post-rpc interceptor for list_operators

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
        it is returned to user code.
        """
        return response

    def pre_list_processes(
        self,
        request: lva_service.ListProcessesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lva_service.ListProcessesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_processes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_list_processes(
        self, response: lva_service.ListProcessesResponse
    ) -> lva_service.ListProcessesResponse:
        """Post-rpc interceptor for list_processes

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
        it is returned to user code.
        """
        return response

    def pre_list_public_operators(
        self,
        request: lva_service.ListPublicOperatorsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lva_service.ListPublicOperatorsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_public_operators

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_list_public_operators(
        self, response: lva_service.ListPublicOperatorsResponse
    ) -> lva_service.ListPublicOperatorsResponse:
        """Post-rpc interceptor for list_public_operators

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
        it is returned to user code.
        """
        return response

    def pre_resolve_operator_info(
        self,
        request: lva_service.ResolveOperatorInfoRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lva_service.ResolveOperatorInfoRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for resolve_operator_info

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_resolve_operator_info(
        self, response: lva_service.ResolveOperatorInfoResponse
    ) -> lva_service.ResolveOperatorInfoResponse:
        """Post-rpc interceptor for resolve_operator_info

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
        it is returned to user code.
        """
        return response

    def pre_update_analysis(
        self,
        request: lva_service.UpdateAnalysisRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lva_service.UpdateAnalysisRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_analysis

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_update_analysis(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_analysis

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
        it is returned to user code.
        """
        return response

    def pre_update_operator(
        self,
        request: lva_service.UpdateOperatorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lva_service.UpdateOperatorRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_operator

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_update_operator(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_operator

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
        it is returned to user code.
        """
        return response

    def pre_update_process(
        self,
        request: lva_service.UpdateProcessRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[lva_service.UpdateProcessRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_process

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_update_process(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_process

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
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
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
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
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
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
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
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
        before they are sent to the LiveVideoAnalytics server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the LiveVideoAnalytics server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class LiveVideoAnalyticsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: LiveVideoAnalyticsRestInterceptor


class LiveVideoAnalyticsRestTransport(LiveVideoAnalyticsTransport):
    """REST backend transport for LiveVideoAnalytics.

    Service describing handlers for resources. The service
    enables clients to run Live Video Analytics (LVA) on the
    streaming inputs.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "visionai.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[LiveVideoAnalyticsRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'visionai.googleapis.com').
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
        self._interceptor = interceptor or LiveVideoAnalyticsRestInterceptor()
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
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/warehouseOperations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/corpora/*/assets/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/corpora/*/collections/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/corpora/*/imageIndexes/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/corpora/*/indexes/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/corpora/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/indexEndpoints/*/operations/*}",
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

    class _BatchRunProcess(LiveVideoAnalyticsRestStub):
        def __hash__(self):
            return hash("BatchRunProcess")

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
            request: lva_service.BatchRunProcessRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the batch run process method over HTTP.

            Args:
                request (~.lva_service.BatchRunProcessRequest):
                    The request object. Request message for running the
                processes in a batch.
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
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/clusters/*}/processes:batchRun",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_batch_run_process(
                request, metadata
            )
            pb_request = lva_service.BatchRunProcessRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_run_process(resp)
            return resp

    class _CreateAnalysis(LiveVideoAnalyticsRestStub):
        def __hash__(self):
            return hash("CreateAnalysis")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "analysisId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lva_service.CreateAnalysisRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create analysis method over HTTP.

            Args:
                request (~.lva_service.CreateAnalysisRequest):
                    The request object. Message for creating an Analysis.
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
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/clusters/*}/analyses",
                    "body": "analysis",
                },
            ]
            request, metadata = self._interceptor.pre_create_analysis(request, metadata)
            pb_request = lva_service.CreateAnalysisRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_analysis(resp)
            return resp

    class _CreateOperator(LiveVideoAnalyticsRestStub):
        def __hash__(self):
            return hash("CreateOperator")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "operatorId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lva_service.CreateOperatorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create operator method over HTTP.

            Args:
                request (~.lva_service.CreateOperatorRequest):
                    The request object. Message for creating a Operator.
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
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/operators",
                    "body": "operator",
                },
            ]
            request, metadata = self._interceptor.pre_create_operator(request, metadata)
            pb_request = lva_service.CreateOperatorRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_operator(resp)
            return resp

    class _CreateProcess(LiveVideoAnalyticsRestStub):
        def __hash__(self):
            return hash("CreateProcess")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "processId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lva_service.CreateProcessRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create process method over HTTP.

            Args:
                request (~.lva_service.CreateProcessRequest):
                    The request object. Message for creating a Process.
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
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/clusters/*}/processes",
                    "body": "process",
                },
            ]
            request, metadata = self._interceptor.pre_create_process(request, metadata)
            pb_request = lva_service.CreateProcessRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_process(resp)
            return resp

    class _DeleteAnalysis(LiveVideoAnalyticsRestStub):
        def __hash__(self):
            return hash("DeleteAnalysis")

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
            request: lva_service.DeleteAnalysisRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete analysis method over HTTP.

            Args:
                request (~.lva_service.DeleteAnalysisRequest):
                    The request object. Message for deleting an Analysis.
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
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*/analyses/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_analysis(request, metadata)
            pb_request = lva_service.DeleteAnalysisRequest.pb(request)
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
            resp = self._interceptor.post_delete_analysis(resp)
            return resp

    class _DeleteOperator(LiveVideoAnalyticsRestStub):
        def __hash__(self):
            return hash("DeleteOperator")

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
            request: lva_service.DeleteOperatorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete operator method over HTTP.

            Args:
                request (~.lva_service.DeleteOperatorRequest):
                    The request object. Message for deleting a Operator
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
                    "uri": "/v1/{name=projects/*/locations/*/operators/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_operator(request, metadata)
            pb_request = lva_service.DeleteOperatorRequest.pb(request)
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
            resp = self._interceptor.post_delete_operator(resp)
            return resp

    class _DeleteProcess(LiveVideoAnalyticsRestStub):
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
            request: lva_service.DeleteProcessRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete process method over HTTP.

            Args:
                request (~.lva_service.DeleteProcessRequest):
                    The request object. Message for deleting a Process.
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
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*/processes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_process(request, metadata)
            pb_request = lva_service.DeleteProcessRequest.pb(request)
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

    class _GetAnalysis(LiveVideoAnalyticsRestStub):
        def __hash__(self):
            return hash("GetAnalysis")

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
            request: lva_service.GetAnalysisRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lva_resources.Analysis:
            r"""Call the get analysis method over HTTP.

            Args:
                request (~.lva_service.GetAnalysisRequest):
                    The request object. Message for getting an Analysis.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lva_resources.Analysis:
                    Message describing the Analysis
                object.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*/analyses/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_analysis(request, metadata)
            pb_request = lva_service.GetAnalysisRequest.pb(request)
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
            resp = lva_resources.Analysis()
            pb_resp = lva_resources.Analysis.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_analysis(resp)
            return resp

    class _GetOperator(LiveVideoAnalyticsRestStub):
        def __hash__(self):
            return hash("GetOperator")

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
            request: lva_service.GetOperatorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lva_resources.Operator:
            r"""Call the get operator method over HTTP.

            Args:
                request (~.lva_service.GetOperatorRequest):
                    The request object. Message for getting a Operator.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lva_resources.Operator:
                    Message describing the Operator
                object.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/operators/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_operator(request, metadata)
            pb_request = lva_service.GetOperatorRequest.pb(request)
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
            resp = lva_resources.Operator()
            pb_resp = lva_resources.Operator.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_operator(resp)
            return resp

    class _GetProcess(LiveVideoAnalyticsRestStub):
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
            request: lva_service.GetProcessRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lva_resources.Process:
            r"""Call the get process method over HTTP.

            Args:
                request (~.lva_service.GetProcessRequest):
                    The request object. Message for getting a Process.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lva_resources.Process:
                    Message describing the Process
                object.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*/processes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_process(request, metadata)
            pb_request = lva_service.GetProcessRequest.pb(request)
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
            resp = lva_resources.Process()
            pb_resp = lva_resources.Process.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_process(resp)
            return resp

    class _ListAnalyses(LiveVideoAnalyticsRestStub):
        def __hash__(self):
            return hash("ListAnalyses")

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
            request: lva_service.ListAnalysesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lva_service.ListAnalysesResponse:
            r"""Call the list analyses method over HTTP.

            Args:
                request (~.lva_service.ListAnalysesRequest):
                    The request object. Message for requesting list of
                Analyses
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lva_service.ListAnalysesResponse:
                    Message for response to listing
                Analyses

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/clusters/*}/analyses",
                },
            ]
            request, metadata = self._interceptor.pre_list_analyses(request, metadata)
            pb_request = lva_service.ListAnalysesRequest.pb(request)
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
            resp = lva_service.ListAnalysesResponse()
            pb_resp = lva_service.ListAnalysesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_analyses(resp)
            return resp

    class _ListOperators(LiveVideoAnalyticsRestStub):
        def __hash__(self):
            return hash("ListOperators")

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
            request: lva_service.ListOperatorsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lva_service.ListOperatorsResponse:
            r"""Call the list operators method over HTTP.

            Args:
                request (~.lva_service.ListOperatorsRequest):
                    The request object. Message for requesting list of
                Operators.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lva_service.ListOperatorsResponse:
                    Message for response to listing
                Operators.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/operators",
                },
            ]
            request, metadata = self._interceptor.pre_list_operators(request, metadata)
            pb_request = lva_service.ListOperatorsRequest.pb(request)
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
            resp = lva_service.ListOperatorsResponse()
            pb_resp = lva_service.ListOperatorsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_operators(resp)
            return resp

    class _ListProcesses(LiveVideoAnalyticsRestStub):
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
            request: lva_service.ListProcessesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lva_service.ListProcessesResponse:
            r"""Call the list processes method over HTTP.

            Args:
                request (~.lva_service.ListProcessesRequest):
                    The request object. Message for requesting list of
                Processes.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lva_service.ListProcessesResponse:
                    Message for response to listing
                Processes.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/clusters/*}/processes",
                },
            ]
            request, metadata = self._interceptor.pre_list_processes(request, metadata)
            pb_request = lva_service.ListProcessesRequest.pb(request)
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
            resp = lva_service.ListProcessesResponse()
            pb_resp = lva_service.ListProcessesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_processes(resp)
            return resp

    class _ListPublicOperators(LiveVideoAnalyticsRestStub):
        def __hash__(self):
            return hash("ListPublicOperators")

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
            request: lva_service.ListPublicOperatorsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lva_service.ListPublicOperatorsResponse:
            r"""Call the list public operators method over HTTP.

            Args:
                request (~.lva_service.ListPublicOperatorsRequest):
                    The request object. Request message of
                ListPublicOperatorsRequest API.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lva_service.ListPublicOperatorsResponse:
                    Response message of
                ListPublicOperators API.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}:listPublicOperators",
                },
            ]
            request, metadata = self._interceptor.pre_list_public_operators(
                request, metadata
            )
            pb_request = lva_service.ListPublicOperatorsRequest.pb(request)
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
            resp = lva_service.ListPublicOperatorsResponse()
            pb_resp = lva_service.ListPublicOperatorsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_public_operators(resp)
            return resp

    class _ResolveOperatorInfo(LiveVideoAnalyticsRestStub):
        def __hash__(self):
            return hash("ResolveOperatorInfo")

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
            request: lva_service.ResolveOperatorInfoRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lva_service.ResolveOperatorInfoResponse:
            r"""Call the resolve operator info method over HTTP.

            Args:
                request (~.lva_service.ResolveOperatorInfoRequest):
                    The request object. Request message for querying operator
                info.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lva_service.ResolveOperatorInfoResponse:
                    Response message of
                ResolveOperatorInfo API.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}:resolveOperatorInfo",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_resolve_operator_info(
                request, metadata
            )
            pb_request = lva_service.ResolveOperatorInfoRequest.pb(request)
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
            resp = lva_service.ResolveOperatorInfoResponse()
            pb_resp = lva_service.ResolveOperatorInfoResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_resolve_operator_info(resp)
            return resp

    class _UpdateAnalysis(LiveVideoAnalyticsRestStub):
        def __hash__(self):
            return hash("UpdateAnalysis")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lva_service.UpdateAnalysisRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update analysis method over HTTP.

            Args:
                request (~.lva_service.UpdateAnalysisRequest):
                    The request object. Message for updating an Analysis.
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
                    "method": "patch",
                    "uri": "/v1/{analysis.name=projects/*/locations/*/clusters/*/analyses/*}",
                    "body": "analysis",
                },
            ]
            request, metadata = self._interceptor.pre_update_analysis(request, metadata)
            pb_request = lva_service.UpdateAnalysisRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_analysis(resp)
            return resp

    class _UpdateOperator(LiveVideoAnalyticsRestStub):
        def __hash__(self):
            return hash("UpdateOperator")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lva_service.UpdateOperatorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update operator method over HTTP.

            Args:
                request (~.lva_service.UpdateOperatorRequest):
                    The request object. Message for updating a Operator.
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
                    "method": "patch",
                    "uri": "/v1/{operator.name=projects/*/locations/*/operators/*}",
                    "body": "operator",
                },
            ]
            request, metadata = self._interceptor.pre_update_operator(request, metadata)
            pb_request = lva_service.UpdateOperatorRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_operator(resp)
            return resp

    class _UpdateProcess(LiveVideoAnalyticsRestStub):
        def __hash__(self):
            return hash("UpdateProcess")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lva_service.UpdateProcessRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update process method over HTTP.

            Args:
                request (~.lva_service.UpdateProcessRequest):
                    The request object. Message for updating a Process.
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
                    "method": "patch",
                    "uri": "/v1/{process.name=projects/*/locations/*/clusters/*/processes/*}",
                    "body": "process",
                },
            ]
            request, metadata = self._interceptor.pre_update_process(request, metadata)
            pb_request = lva_service.UpdateProcessRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_process(resp)
            return resp

    @property
    def batch_run_process(
        self,
    ) -> Callable[[lva_service.BatchRunProcessRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchRunProcess(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_analysis(
        self,
    ) -> Callable[[lva_service.CreateAnalysisRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAnalysis(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_operator(
        self,
    ) -> Callable[[lva_service.CreateOperatorRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateOperator(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_process(
        self,
    ) -> Callable[[lva_service.CreateProcessRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateProcess(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_analysis(
        self,
    ) -> Callable[[lva_service.DeleteAnalysisRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAnalysis(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_operator(
        self,
    ) -> Callable[[lva_service.DeleteOperatorRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteOperator(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_process(
        self,
    ) -> Callable[[lva_service.DeleteProcessRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteProcess(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_analysis(
        self,
    ) -> Callable[[lva_service.GetAnalysisRequest], lva_resources.Analysis]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAnalysis(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operator(
        self,
    ) -> Callable[[lva_service.GetOperatorRequest], lva_resources.Operator]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetOperator(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_process(
        self,
    ) -> Callable[[lva_service.GetProcessRequest], lva_resources.Process]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetProcess(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_analyses(
        self,
    ) -> Callable[[lva_service.ListAnalysesRequest], lva_service.ListAnalysesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAnalyses(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_operators(
        self,
    ) -> Callable[
        [lva_service.ListOperatorsRequest], lva_service.ListOperatorsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListOperators(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_processes(
        self,
    ) -> Callable[
        [lva_service.ListProcessesRequest], lva_service.ListProcessesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListProcesses(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_public_operators(
        self,
    ) -> Callable[
        [lva_service.ListPublicOperatorsRequest],
        lva_service.ListPublicOperatorsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPublicOperators(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def resolve_operator_info(
        self,
    ) -> Callable[
        [lva_service.ResolveOperatorInfoRequest],
        lva_service.ResolveOperatorInfoResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ResolveOperatorInfo(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_analysis(
        self,
    ) -> Callable[[lva_service.UpdateAnalysisRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAnalysis(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_operator(
        self,
    ) -> Callable[[lva_service.UpdateOperatorRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateOperator(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_process(
        self,
    ) -> Callable[[lva_service.UpdateProcessRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateProcess(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(LiveVideoAnalyticsRestStub):
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

    class _DeleteOperation(LiveVideoAnalyticsRestStub):
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

    class _GetOperation(LiveVideoAnalyticsRestStub):
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
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/warehouseOperations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/corpora/*/assets/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/corpora/*/collections/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/corpora/*/imageIndexes/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/corpora/*/indexes/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/corpora/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/indexEndpoints/*/operations/*}",
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

    class _ListOperations(LiveVideoAnalyticsRestStub):
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


__all__ = ("LiveVideoAnalyticsRestTransport",)
