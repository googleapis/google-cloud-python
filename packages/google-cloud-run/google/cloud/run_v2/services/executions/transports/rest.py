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

from google.cloud.run_v2.types import execution

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseExecutionsRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class ExecutionsRestInterceptor:
    """Interceptor for Executions.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ExecutionsRestTransport.

    .. code-block:: python
        class MyCustomExecutionsInterceptor(ExecutionsRestInterceptor):
            def pre_cancel_execution(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_cancel_execution(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_execution(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_execution(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_execution(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_execution(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_executions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_executions(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ExecutionsRestTransport(interceptor=MyCustomExecutionsInterceptor())
        client = ExecutionsClient(transport=transport)


    """

    def pre_cancel_execution(
        self,
        request: execution.CancelExecutionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[execution.CancelExecutionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_execution

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Executions server.
        """
        return request, metadata

    def post_cancel_execution(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for cancel_execution

        Override in a subclass to manipulate the response
        after it is returned by the Executions server but before
        it is returned to user code.
        """
        return response

    def pre_delete_execution(
        self,
        request: execution.DeleteExecutionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[execution.DeleteExecutionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_execution

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Executions server.
        """
        return request, metadata

    def post_delete_execution(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_execution

        Override in a subclass to manipulate the response
        after it is returned by the Executions server but before
        it is returned to user code.
        """
        return response

    def pre_get_execution(
        self,
        request: execution.GetExecutionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[execution.GetExecutionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_execution

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Executions server.
        """
        return request, metadata

    def post_get_execution(self, response: execution.Execution) -> execution.Execution:
        """Post-rpc interceptor for get_execution

        Override in a subclass to manipulate the response
        after it is returned by the Executions server but before
        it is returned to user code.
        """
        return response

    def pre_list_executions(
        self,
        request: execution.ListExecutionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[execution.ListExecutionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_executions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Executions server.
        """
        return request, metadata

    def post_list_executions(
        self, response: execution.ListExecutionsResponse
    ) -> execution.ListExecutionsResponse:
        """Post-rpc interceptor for list_executions

        Override in a subclass to manipulate the response
        after it is returned by the Executions server but before
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
        before they are sent to the Executions server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the Executions server but before
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
        before they are sent to the Executions server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Executions server but before
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
        before they are sent to the Executions server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Executions server but before
        it is returned to user code.
        """
        return response

    def pre_wait_operation(
        self,
        request: operations_pb2.WaitOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.WaitOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for wait_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Executions server.
        """
        return request, metadata

    def post_wait_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for wait_operation

        Override in a subclass to manipulate the response
        after it is returned by the Executions server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ExecutionsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ExecutionsRestInterceptor


class ExecutionsRestTransport(_BaseExecutionsRestTransport):
    """REST backend synchronous transport for Executions.

    Cloud Run Execution Control Plane API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "run.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ExecutionsRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'run.googleapis.com').
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
        self._interceptor = interceptor or ExecutionsRestInterceptor()
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
                        "uri": "/v2/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v2/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v2/{name=projects/*/locations/*}/operations",
                    },
                ],
                "google.longrunning.Operations.WaitOperation": [
                    {
                        "method": "post",
                        "uri": "/v2/{name=projects/*/locations/*/operations/*}:wait",
                        "body": "*",
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

    class _CancelExecution(
        _BaseExecutionsRestTransport._BaseCancelExecution, ExecutionsRestStub
    ):
        def __hash__(self):
            return hash("ExecutionsRestTransport.CancelExecution")

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
            request: execution.CancelExecutionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the cancel execution method over HTTP.

            Args:
                request (~.execution.CancelExecutionRequest):
                    The request object. Request message for deleting an
                Execution.
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
                _BaseExecutionsRestTransport._BaseCancelExecution._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_execution(
                request, metadata
            )
            transcoded_request = _BaseExecutionsRestTransport._BaseCancelExecution._get_transcoded_request(
                http_options, request
            )

            body = _BaseExecutionsRestTransport._BaseCancelExecution._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseExecutionsRestTransport._BaseCancelExecution._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ExecutionsRestTransport._CancelExecution._get_response(
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
            resp = self._interceptor.post_cancel_execution(resp)
            return resp

    class _DeleteExecution(
        _BaseExecutionsRestTransport._BaseDeleteExecution, ExecutionsRestStub
    ):
        def __hash__(self):
            return hash("ExecutionsRestTransport.DeleteExecution")

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
            request: execution.DeleteExecutionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete execution method over HTTP.

            Args:
                request (~.execution.DeleteExecutionRequest):
                    The request object. Request message for deleting an
                Execution.
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
                _BaseExecutionsRestTransport._BaseDeleteExecution._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_execution(
                request, metadata
            )
            transcoded_request = _BaseExecutionsRestTransport._BaseDeleteExecution._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseExecutionsRestTransport._BaseDeleteExecution._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ExecutionsRestTransport._DeleteExecution._get_response(
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
            resp = self._interceptor.post_delete_execution(resp)
            return resp

    class _GetExecution(
        _BaseExecutionsRestTransport._BaseGetExecution, ExecutionsRestStub
    ):
        def __hash__(self):
            return hash("ExecutionsRestTransport.GetExecution")

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
            request: execution.GetExecutionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> execution.Execution:
            r"""Call the get execution method over HTTP.

            Args:
                request (~.execution.GetExecutionRequest):
                    The request object. Request message for obtaining a
                Execution by its full name.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.execution.Execution:
                    Execution represents the
                configuration of a single execution. A
                execution an immutable resource that
                references a container image which is
                run to completion.

            """

            http_options = (
                _BaseExecutionsRestTransport._BaseGetExecution._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_execution(request, metadata)
            transcoded_request = (
                _BaseExecutionsRestTransport._BaseGetExecution._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseExecutionsRestTransport._BaseGetExecution._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ExecutionsRestTransport._GetExecution._get_response(
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
            resp = execution.Execution()
            pb_resp = execution.Execution.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_execution(resp)
            return resp

    class _ListExecutions(
        _BaseExecutionsRestTransport._BaseListExecutions, ExecutionsRestStub
    ):
        def __hash__(self):
            return hash("ExecutionsRestTransport.ListExecutions")

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
            request: execution.ListExecutionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> execution.ListExecutionsResponse:
            r"""Call the list executions method over HTTP.

            Args:
                request (~.execution.ListExecutionsRequest):
                    The request object. Request message for retrieving a list
                of Executions.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.execution.ListExecutionsResponse:
                    Response message containing a list of
                Executions.

            """

            http_options = (
                _BaseExecutionsRestTransport._BaseListExecutions._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_executions(request, metadata)
            transcoded_request = _BaseExecutionsRestTransport._BaseListExecutions._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseExecutionsRestTransport._BaseListExecutions._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ExecutionsRestTransport._ListExecutions._get_response(
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
            resp = execution.ListExecutionsResponse()
            pb_resp = execution.ListExecutionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_executions(resp)
            return resp

    @property
    def cancel_execution(
        self,
    ) -> Callable[[execution.CancelExecutionRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CancelExecution(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_execution(
        self,
    ) -> Callable[[execution.DeleteExecutionRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteExecution(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_execution(
        self,
    ) -> Callable[[execution.GetExecutionRequest], execution.Execution]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetExecution(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_executions(
        self,
    ) -> Callable[[execution.ListExecutionsRequest], execution.ListExecutionsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListExecutions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(
        _BaseExecutionsRestTransport._BaseDeleteOperation, ExecutionsRestStub
    ):
        def __hash__(self):
            return hash("ExecutionsRestTransport.DeleteOperation")

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
                _BaseExecutionsRestTransport._BaseDeleteOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BaseExecutionsRestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseExecutionsRestTransport._BaseDeleteOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ExecutionsRestTransport._DeleteOperation._get_response(
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
        _BaseExecutionsRestTransport._BaseGetOperation, ExecutionsRestStub
    ):
        def __hash__(self):
            return hash("ExecutionsRestTransport.GetOperation")

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
                _BaseExecutionsRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = (
                _BaseExecutionsRestTransport._BaseGetOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseExecutionsRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ExecutionsRestTransport._GetOperation._get_response(
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
        _BaseExecutionsRestTransport._BaseListOperations, ExecutionsRestStub
    ):
        def __hash__(self):
            return hash("ExecutionsRestTransport.ListOperations")

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
                _BaseExecutionsRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseExecutionsRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseExecutionsRestTransport._BaseListOperations._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ExecutionsRestTransport._ListOperations._get_response(
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
    def wait_operation(self):
        return self._WaitOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _WaitOperation(
        _BaseExecutionsRestTransport._BaseWaitOperation, ExecutionsRestStub
    ):
        def __hash__(self):
            return hash("ExecutionsRestTransport.WaitOperation")

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
            request: operations_pb2.WaitOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the wait operation method over HTTP.

            Args:
                request (operations_pb2.WaitOperationRequest):
                    The request object for WaitOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.Operation: Response from WaitOperation method.
            """

            http_options = (
                _BaseExecutionsRestTransport._BaseWaitOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_wait_operation(request, metadata)
            transcoded_request = (
                _BaseExecutionsRestTransport._BaseWaitOperation._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseExecutionsRestTransport._BaseWaitOperation._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseExecutionsRestTransport._BaseWaitOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ExecutionsRestTransport._WaitOperation._get_response(
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
            resp = operations_pb2.Operation()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_wait_operation(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ExecutionsRestTransport",)
