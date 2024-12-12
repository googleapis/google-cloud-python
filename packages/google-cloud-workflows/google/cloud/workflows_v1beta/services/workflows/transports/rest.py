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
import logging
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.workflows_v1beta.types import workflows

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseWorkflowsRestTransport

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


class WorkflowsRestInterceptor:
    """Interceptor for Workflows.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the WorkflowsRestTransport.

    .. code-block:: python
        class MyCustomWorkflowsInterceptor(WorkflowsRestInterceptor):
            def pre_create_workflow(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_workflow(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_workflow(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_workflow(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_workflow(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_workflow(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_workflows(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_workflows(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_workflow(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_workflow(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = WorkflowsRestTransport(interceptor=MyCustomWorkflowsInterceptor())
        client = WorkflowsClient(transport=transport)


    """

    def pre_create_workflow(
        self,
        request: workflows.CreateWorkflowRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        workflows.CreateWorkflowRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_workflow

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workflows server.
        """
        return request, metadata

    def post_create_workflow(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_workflow

        Override in a subclass to manipulate the response
        after it is returned by the Workflows server but before
        it is returned to user code.
        """
        return response

    def pre_delete_workflow(
        self,
        request: workflows.DeleteWorkflowRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        workflows.DeleteWorkflowRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_workflow

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workflows server.
        """
        return request, metadata

    def post_delete_workflow(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_workflow

        Override in a subclass to manipulate the response
        after it is returned by the Workflows server but before
        it is returned to user code.
        """
        return response

    def pre_get_workflow(
        self,
        request: workflows.GetWorkflowRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[workflows.GetWorkflowRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_workflow

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workflows server.
        """
        return request, metadata

    def post_get_workflow(self, response: workflows.Workflow) -> workflows.Workflow:
        """Post-rpc interceptor for get_workflow

        Override in a subclass to manipulate the response
        after it is returned by the Workflows server but before
        it is returned to user code.
        """
        return response

    def pre_list_workflows(
        self,
        request: workflows.ListWorkflowsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[workflows.ListWorkflowsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_workflows

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workflows server.
        """
        return request, metadata

    def post_list_workflows(
        self, response: workflows.ListWorkflowsResponse
    ) -> workflows.ListWorkflowsResponse:
        """Post-rpc interceptor for list_workflows

        Override in a subclass to manipulate the response
        after it is returned by the Workflows server but before
        it is returned to user code.
        """
        return response

    def pre_update_workflow(
        self,
        request: workflows.UpdateWorkflowRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        workflows.UpdateWorkflowRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_workflow

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workflows server.
        """
        return request, metadata

    def post_update_workflow(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_workflow

        Override in a subclass to manipulate the response
        after it is returned by the Workflows server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class WorkflowsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: WorkflowsRestInterceptor


class WorkflowsRestTransport(_BaseWorkflowsRestTransport):
    """REST backend synchronous transport for Workflows.

    Workflows is used to deploy and execute workflow programs.
    Workflows makes sure the program executes reliably, despite
    hardware and networking interruptions.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "workflows.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[WorkflowsRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'workflows.googleapis.com').
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
        self._interceptor = interceptor or WorkflowsRestInterceptor()
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
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1beta/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1beta",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateWorkflow(
        _BaseWorkflowsRestTransport._BaseCreateWorkflow, WorkflowsRestStub
    ):
        def __hash__(self):
            return hash("WorkflowsRestTransport.CreateWorkflow")

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
            request: workflows.CreateWorkflowRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create workflow method over HTTP.

            Args:
                request (~.workflows.CreateWorkflowRequest):
                    The request object. Request for the
                [CreateWorkflow][google.cloud.workflows.v1beta.Workflows.CreateWorkflow]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseWorkflowsRestTransport._BaseCreateWorkflow._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_workflow(request, metadata)
            transcoded_request = (
                _BaseWorkflowsRestTransport._BaseCreateWorkflow._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseWorkflowsRestTransport._BaseCreateWorkflow._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWorkflowsRestTransport._BaseCreateWorkflow._get_query_params_json(
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
                    f"Sending request for google.cloud.workflows_v1beta.WorkflowsClient.CreateWorkflow",
                    extra={
                        "serviceName": "google.cloud.workflows.v1beta.Workflows",
                        "rpcName": "CreateWorkflow",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = WorkflowsRestTransport._CreateWorkflow._get_response(
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

            resp = self._interceptor.post_create_workflow(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.workflows_v1beta.WorkflowsClient.create_workflow",
                    extra={
                        "serviceName": "google.cloud.workflows.v1beta.Workflows",
                        "rpcName": "CreateWorkflow",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteWorkflow(
        _BaseWorkflowsRestTransport._BaseDeleteWorkflow, WorkflowsRestStub
    ):
        def __hash__(self):
            return hash("WorkflowsRestTransport.DeleteWorkflow")

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
            request: workflows.DeleteWorkflowRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete workflow method over HTTP.

            Args:
                request (~.workflows.DeleteWorkflowRequest):
                    The request object. Request for the
                [DeleteWorkflow][google.cloud.workflows.v1beta.Workflows.DeleteWorkflow]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseWorkflowsRestTransport._BaseDeleteWorkflow._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_workflow(request, metadata)
            transcoded_request = (
                _BaseWorkflowsRestTransport._BaseDeleteWorkflow._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWorkflowsRestTransport._BaseDeleteWorkflow._get_query_params_json(
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
                    f"Sending request for google.cloud.workflows_v1beta.WorkflowsClient.DeleteWorkflow",
                    extra={
                        "serviceName": "google.cloud.workflows.v1beta.Workflows",
                        "rpcName": "DeleteWorkflow",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = WorkflowsRestTransport._DeleteWorkflow._get_response(
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

            resp = self._interceptor.post_delete_workflow(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.workflows_v1beta.WorkflowsClient.delete_workflow",
                    extra={
                        "serviceName": "google.cloud.workflows.v1beta.Workflows",
                        "rpcName": "DeleteWorkflow",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetWorkflow(_BaseWorkflowsRestTransport._BaseGetWorkflow, WorkflowsRestStub):
        def __hash__(self):
            return hash("WorkflowsRestTransport.GetWorkflow")

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
            request: workflows.GetWorkflowRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> workflows.Workflow:
            r"""Call the get workflow method over HTTP.

            Args:
                request (~.workflows.GetWorkflowRequest):
                    The request object. Request for the
                [GetWorkflow][google.cloud.workflows.v1beta.Workflows.GetWorkflow]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.workflows.Workflow:
                    Workflow program to be executed by
                Workflows.

            """

            http_options = (
                _BaseWorkflowsRestTransport._BaseGetWorkflow._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_workflow(request, metadata)
            transcoded_request = (
                _BaseWorkflowsRestTransport._BaseGetWorkflow._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWorkflowsRestTransport._BaseGetWorkflow._get_query_params_json(
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
                    f"Sending request for google.cloud.workflows_v1beta.WorkflowsClient.GetWorkflow",
                    extra={
                        "serviceName": "google.cloud.workflows.v1beta.Workflows",
                        "rpcName": "GetWorkflow",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = WorkflowsRestTransport._GetWorkflow._get_response(
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
            resp = workflows.Workflow()
            pb_resp = workflows.Workflow.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_workflow(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = workflows.Workflow.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.workflows_v1beta.WorkflowsClient.get_workflow",
                    extra={
                        "serviceName": "google.cloud.workflows.v1beta.Workflows",
                        "rpcName": "GetWorkflow",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListWorkflows(
        _BaseWorkflowsRestTransport._BaseListWorkflows, WorkflowsRestStub
    ):
        def __hash__(self):
            return hash("WorkflowsRestTransport.ListWorkflows")

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
            request: workflows.ListWorkflowsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> workflows.ListWorkflowsResponse:
            r"""Call the list workflows method over HTTP.

            Args:
                request (~.workflows.ListWorkflowsRequest):
                    The request object. Request for the
                [ListWorkflows][google.cloud.workflows.v1beta.Workflows.ListWorkflows]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.workflows.ListWorkflowsResponse:
                    Response for the
                [ListWorkflows][google.cloud.workflows.v1beta.Workflows.ListWorkflows]
                method.

            """

            http_options = (
                _BaseWorkflowsRestTransport._BaseListWorkflows._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_workflows(request, metadata)
            transcoded_request = (
                _BaseWorkflowsRestTransport._BaseListWorkflows._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWorkflowsRestTransport._BaseListWorkflows._get_query_params_json(
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
                    f"Sending request for google.cloud.workflows_v1beta.WorkflowsClient.ListWorkflows",
                    extra={
                        "serviceName": "google.cloud.workflows.v1beta.Workflows",
                        "rpcName": "ListWorkflows",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = WorkflowsRestTransport._ListWorkflows._get_response(
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
            resp = workflows.ListWorkflowsResponse()
            pb_resp = workflows.ListWorkflowsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_workflows(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = workflows.ListWorkflowsResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.workflows_v1beta.WorkflowsClient.list_workflows",
                    extra={
                        "serviceName": "google.cloud.workflows.v1beta.Workflows",
                        "rpcName": "ListWorkflows",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateWorkflow(
        _BaseWorkflowsRestTransport._BaseUpdateWorkflow, WorkflowsRestStub
    ):
        def __hash__(self):
            return hash("WorkflowsRestTransport.UpdateWorkflow")

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
            request: workflows.UpdateWorkflowRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update workflow method over HTTP.

            Args:
                request (~.workflows.UpdateWorkflowRequest):
                    The request object. Request for the
                [UpdateWorkflow][google.cloud.workflows.v1beta.Workflows.UpdateWorkflow]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseWorkflowsRestTransport._BaseUpdateWorkflow._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_workflow(request, metadata)
            transcoded_request = (
                _BaseWorkflowsRestTransport._BaseUpdateWorkflow._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseWorkflowsRestTransport._BaseUpdateWorkflow._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWorkflowsRestTransport._BaseUpdateWorkflow._get_query_params_json(
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
                    f"Sending request for google.cloud.workflows_v1beta.WorkflowsClient.UpdateWorkflow",
                    extra={
                        "serviceName": "google.cloud.workflows.v1beta.Workflows",
                        "rpcName": "UpdateWorkflow",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = WorkflowsRestTransport._UpdateWorkflow._get_response(
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

            resp = self._interceptor.post_update_workflow(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.workflows_v1beta.WorkflowsClient.update_workflow",
                    extra={
                        "serviceName": "google.cloud.workflows.v1beta.Workflows",
                        "rpcName": "UpdateWorkflow",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def create_workflow(
        self,
    ) -> Callable[[workflows.CreateWorkflowRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateWorkflow(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_workflow(
        self,
    ) -> Callable[[workflows.DeleteWorkflowRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteWorkflow(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_workflow(
        self,
    ) -> Callable[[workflows.GetWorkflowRequest], workflows.Workflow]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetWorkflow(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_workflows(
        self,
    ) -> Callable[[workflows.ListWorkflowsRequest], workflows.ListWorkflowsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListWorkflows(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_workflow(
        self,
    ) -> Callable[[workflows.UpdateWorkflowRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateWorkflow(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("WorkflowsRestTransport",)
