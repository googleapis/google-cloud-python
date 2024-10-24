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
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.dialogflowcx_v3.types import environment
from google.cloud.dialogflowcx_v3.types import environment as gcdc_environment

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseEnvironmentsRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class EnvironmentsRestInterceptor:
    """Interceptor for Environments.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the EnvironmentsRestTransport.

    .. code-block:: python
        class MyCustomEnvironmentsInterceptor(EnvironmentsRestInterceptor):
            def pre_create_environment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_environment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_environment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_deploy_flow(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_deploy_flow(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_environment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_environment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_continuous_test_results(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_continuous_test_results(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_environments(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_environments(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_lookup_environment_history(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_lookup_environment_history(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_run_continuous_test(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_run_continuous_test(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_environment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_environment(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = EnvironmentsRestTransport(interceptor=MyCustomEnvironmentsInterceptor())
        client = EnvironmentsClient(transport=transport)


    """

    def pre_create_environment(
        self,
        request: gcdc_environment.CreateEnvironmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcdc_environment.CreateEnvironmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_environment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_create_environment(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_environment

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_delete_environment(
        self,
        request: environment.DeleteEnvironmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environment.DeleteEnvironmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_environment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def pre_deploy_flow(
        self,
        request: environment.DeployFlowRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environment.DeployFlowRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for deploy_flow

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_deploy_flow(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for deploy_flow

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_get_environment(
        self,
        request: environment.GetEnvironmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environment.GetEnvironmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_environment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_get_environment(
        self, response: environment.Environment
    ) -> environment.Environment:
        """Post-rpc interceptor for get_environment

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_list_continuous_test_results(
        self,
        request: environment.ListContinuousTestResultsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environment.ListContinuousTestResultsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_continuous_test_results

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_list_continuous_test_results(
        self, response: environment.ListContinuousTestResultsResponse
    ) -> environment.ListContinuousTestResultsResponse:
        """Post-rpc interceptor for list_continuous_test_results

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_list_environments(
        self,
        request: environment.ListEnvironmentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environment.ListEnvironmentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_environments

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_list_environments(
        self, response: environment.ListEnvironmentsResponse
    ) -> environment.ListEnvironmentsResponse:
        """Post-rpc interceptor for list_environments

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_lookup_environment_history(
        self,
        request: environment.LookupEnvironmentHistoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environment.LookupEnvironmentHistoryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for lookup_environment_history

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_lookup_environment_history(
        self, response: environment.LookupEnvironmentHistoryResponse
    ) -> environment.LookupEnvironmentHistoryResponse:
        """Post-rpc interceptor for lookup_environment_history

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_run_continuous_test(
        self,
        request: environment.RunContinuousTestRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environment.RunContinuousTestRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for run_continuous_test

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_run_continuous_test(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for run_continuous_test

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_update_environment(
        self,
        request: gcdc_environment.UpdateEnvironmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcdc_environment.UpdateEnvironmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_environment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_update_environment(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_environment

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
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
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
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
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
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
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
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
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
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
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class EnvironmentsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: EnvironmentsRestInterceptor


class EnvironmentsRestTransport(_BaseEnvironmentsRestTransport):
    """REST backend synchronous transport for Environments.

    Service for managing
    [Environments][google.cloud.dialogflow.cx.v3.Environment].

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "dialogflow.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[EnvironmentsRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'dialogflow.googleapis.com').
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
        self._interceptor = interceptor or EnvironmentsRestInterceptor()
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
                        "uri": "/v3/{name=projects/*/operations/*}:cancel",
                    },
                    {
                        "method": "post",
                        "uri": "/v3/{name=projects/*/locations/*/operations/*}:cancel",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v3/{name=projects/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v3/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v3/{name=projects/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v3/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v3",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateEnvironment(
        _BaseEnvironmentsRestTransport._BaseCreateEnvironment, EnvironmentsRestStub
    ):
        def __hash__(self):
            return hash("EnvironmentsRestTransport.CreateEnvironment")

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
            request: gcdc_environment.CreateEnvironmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create environment method over HTTP.

            Args:
                request (~.gcdc_environment.CreateEnvironmentRequest):
                    The request object. The request message for
                [Environments.CreateEnvironment][google.cloud.dialogflow.cx.v3.Environments.CreateEnvironment].
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
                _BaseEnvironmentsRestTransport._BaseCreateEnvironment._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_environment(
                request, metadata
            )
            transcoded_request = _BaseEnvironmentsRestTransport._BaseCreateEnvironment._get_transcoded_request(
                http_options, request
            )

            body = _BaseEnvironmentsRestTransport._BaseCreateEnvironment._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseEnvironmentsRestTransport._BaseCreateEnvironment._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EnvironmentsRestTransport._CreateEnvironment._get_response(
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
            resp = self._interceptor.post_create_environment(resp)
            return resp

    class _DeleteEnvironment(
        _BaseEnvironmentsRestTransport._BaseDeleteEnvironment, EnvironmentsRestStub
    ):
        def __hash__(self):
            return hash("EnvironmentsRestTransport.DeleteEnvironment")

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
            request: environment.DeleteEnvironmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete environment method over HTTP.

            Args:
                request (~.environment.DeleteEnvironmentRequest):
                    The request object. The request message for
                [Environments.DeleteEnvironment][google.cloud.dialogflow.cx.v3.Environments.DeleteEnvironment].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseEnvironmentsRestTransport._BaseDeleteEnvironment._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_environment(
                request, metadata
            )
            transcoded_request = _BaseEnvironmentsRestTransport._BaseDeleteEnvironment._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseEnvironmentsRestTransport._BaseDeleteEnvironment._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EnvironmentsRestTransport._DeleteEnvironment._get_response(
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

    class _DeployFlow(
        _BaseEnvironmentsRestTransport._BaseDeployFlow, EnvironmentsRestStub
    ):
        def __hash__(self):
            return hash("EnvironmentsRestTransport.DeployFlow")

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
            request: environment.DeployFlowRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the deploy flow method over HTTP.

            Args:
                request (~.environment.DeployFlowRequest):
                    The request object. The request message for
                [Environments.DeployFlow][google.cloud.dialogflow.cx.v3.Environments.DeployFlow].
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
                _BaseEnvironmentsRestTransport._BaseDeployFlow._get_http_options()
            )
            request, metadata = self._interceptor.pre_deploy_flow(request, metadata)
            transcoded_request = (
                _BaseEnvironmentsRestTransport._BaseDeployFlow._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseEnvironmentsRestTransport._BaseDeployFlow._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseEnvironmentsRestTransport._BaseDeployFlow._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EnvironmentsRestTransport._DeployFlow._get_response(
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
            resp = self._interceptor.post_deploy_flow(resp)
            return resp

    class _GetEnvironment(
        _BaseEnvironmentsRestTransport._BaseGetEnvironment, EnvironmentsRestStub
    ):
        def __hash__(self):
            return hash("EnvironmentsRestTransport.GetEnvironment")

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
            request: environment.GetEnvironmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> environment.Environment:
            r"""Call the get environment method over HTTP.

            Args:
                request (~.environment.GetEnvironmentRequest):
                    The request object. The request message for
                [Environments.GetEnvironment][google.cloud.dialogflow.cx.v3.Environments.GetEnvironment].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.environment.Environment:
                    Represents an environment for an
                agent. You can create multiple versions
                of your agent and publish them to
                separate environments. When you edit an
                agent, you are editing the draft agent.
                At any point, you can save the draft
                agent as an agent version, which is an
                immutable snapshot of your agent. When
                you save the draft agent, it is
                published to the default environment.
                When you create agent versions, you can
                publish them to custom environments. You
                can create a variety of custom
                environments for testing, development,
                production, etc.

            """

            http_options = (
                _BaseEnvironmentsRestTransport._BaseGetEnvironment._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_environment(request, metadata)
            transcoded_request = _BaseEnvironmentsRestTransport._BaseGetEnvironment._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseEnvironmentsRestTransport._BaseGetEnvironment._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EnvironmentsRestTransport._GetEnvironment._get_response(
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
            resp = environment.Environment()
            pb_resp = environment.Environment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_environment(resp)
            return resp

    class _ListContinuousTestResults(
        _BaseEnvironmentsRestTransport._BaseListContinuousTestResults,
        EnvironmentsRestStub,
    ):
        def __hash__(self):
            return hash("EnvironmentsRestTransport.ListContinuousTestResults")

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
            request: environment.ListContinuousTestResultsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> environment.ListContinuousTestResultsResponse:
            r"""Call the list continuous test
            results method over HTTP.

                Args:
                    request (~.environment.ListContinuousTestResultsRequest):
                        The request object. The request message for
                    [Environments.ListContinuousTestResults][google.cloud.dialogflow.cx.v3.Environments.ListContinuousTestResults].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.environment.ListContinuousTestResultsResponse:
                        The response message for
                    [Environments.ListTestCaseResults][].

            """

            http_options = (
                _BaseEnvironmentsRestTransport._BaseListContinuousTestResults._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_continuous_test_results(
                request, metadata
            )
            transcoded_request = _BaseEnvironmentsRestTransport._BaseListContinuousTestResults._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseEnvironmentsRestTransport._BaseListContinuousTestResults._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                EnvironmentsRestTransport._ListContinuousTestResults._get_response(
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
            resp = environment.ListContinuousTestResultsResponse()
            pb_resp = environment.ListContinuousTestResultsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_continuous_test_results(resp)
            return resp

    class _ListEnvironments(
        _BaseEnvironmentsRestTransport._BaseListEnvironments, EnvironmentsRestStub
    ):
        def __hash__(self):
            return hash("EnvironmentsRestTransport.ListEnvironments")

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
            request: environment.ListEnvironmentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> environment.ListEnvironmentsResponse:
            r"""Call the list environments method over HTTP.

            Args:
                request (~.environment.ListEnvironmentsRequest):
                    The request object. The request message for
                [Environments.ListEnvironments][google.cloud.dialogflow.cx.v3.Environments.ListEnvironments].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.environment.ListEnvironmentsResponse:
                    The response message for
                [Environments.ListEnvironments][google.cloud.dialogflow.cx.v3.Environments.ListEnvironments].

            """

            http_options = (
                _BaseEnvironmentsRestTransport._BaseListEnvironments._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_environments(
                request, metadata
            )
            transcoded_request = _BaseEnvironmentsRestTransport._BaseListEnvironments._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseEnvironmentsRestTransport._BaseListEnvironments._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EnvironmentsRestTransport._ListEnvironments._get_response(
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
            resp = environment.ListEnvironmentsResponse()
            pb_resp = environment.ListEnvironmentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_environments(resp)
            return resp

    class _LookupEnvironmentHistory(
        _BaseEnvironmentsRestTransport._BaseLookupEnvironmentHistory,
        EnvironmentsRestStub,
    ):
        def __hash__(self):
            return hash("EnvironmentsRestTransport.LookupEnvironmentHistory")

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
            request: environment.LookupEnvironmentHistoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> environment.LookupEnvironmentHistoryResponse:
            r"""Call the lookup environment
            history method over HTTP.

                Args:
                    request (~.environment.LookupEnvironmentHistoryRequest):
                        The request object. The request message for
                    [Environments.LookupEnvironmentHistory][google.cloud.dialogflow.cx.v3.Environments.LookupEnvironmentHistory].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.environment.LookupEnvironmentHistoryResponse:
                        The response message for
                    [Environments.LookupEnvironmentHistory][google.cloud.dialogflow.cx.v3.Environments.LookupEnvironmentHistory].

            """

            http_options = (
                _BaseEnvironmentsRestTransport._BaseLookupEnvironmentHistory._get_http_options()
            )
            request, metadata = self._interceptor.pre_lookup_environment_history(
                request, metadata
            )
            transcoded_request = _BaseEnvironmentsRestTransport._BaseLookupEnvironmentHistory._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseEnvironmentsRestTransport._BaseLookupEnvironmentHistory._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                EnvironmentsRestTransport._LookupEnvironmentHistory._get_response(
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
            resp = environment.LookupEnvironmentHistoryResponse()
            pb_resp = environment.LookupEnvironmentHistoryResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_lookup_environment_history(resp)
            return resp

    class _RunContinuousTest(
        _BaseEnvironmentsRestTransport._BaseRunContinuousTest, EnvironmentsRestStub
    ):
        def __hash__(self):
            return hash("EnvironmentsRestTransport.RunContinuousTest")

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
            request: environment.RunContinuousTestRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the run continuous test method over HTTP.

            Args:
                request (~.environment.RunContinuousTestRequest):
                    The request object. The request message for
                [Environments.RunContinuousTest][google.cloud.dialogflow.cx.v3.Environments.RunContinuousTest].
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
                _BaseEnvironmentsRestTransport._BaseRunContinuousTest._get_http_options()
            )
            request, metadata = self._interceptor.pre_run_continuous_test(
                request, metadata
            )
            transcoded_request = _BaseEnvironmentsRestTransport._BaseRunContinuousTest._get_transcoded_request(
                http_options, request
            )

            body = _BaseEnvironmentsRestTransport._BaseRunContinuousTest._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseEnvironmentsRestTransport._BaseRunContinuousTest._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EnvironmentsRestTransport._RunContinuousTest._get_response(
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
            resp = self._interceptor.post_run_continuous_test(resp)
            return resp

    class _UpdateEnvironment(
        _BaseEnvironmentsRestTransport._BaseUpdateEnvironment, EnvironmentsRestStub
    ):
        def __hash__(self):
            return hash("EnvironmentsRestTransport.UpdateEnvironment")

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
            request: gcdc_environment.UpdateEnvironmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update environment method over HTTP.

            Args:
                request (~.gcdc_environment.UpdateEnvironmentRequest):
                    The request object. The request message for
                [Environments.UpdateEnvironment][google.cloud.dialogflow.cx.v3.Environments.UpdateEnvironment].
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
                _BaseEnvironmentsRestTransport._BaseUpdateEnvironment._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_environment(
                request, metadata
            )
            transcoded_request = _BaseEnvironmentsRestTransport._BaseUpdateEnvironment._get_transcoded_request(
                http_options, request
            )

            body = _BaseEnvironmentsRestTransport._BaseUpdateEnvironment._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseEnvironmentsRestTransport._BaseUpdateEnvironment._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EnvironmentsRestTransport._UpdateEnvironment._get_response(
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
            resp = self._interceptor.post_update_environment(resp)
            return resp

    @property
    def create_environment(
        self,
    ) -> Callable[
        [gcdc_environment.CreateEnvironmentRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateEnvironment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_environment(
        self,
    ) -> Callable[[environment.DeleteEnvironmentRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteEnvironment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def deploy_flow(
        self,
    ) -> Callable[[environment.DeployFlowRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeployFlow(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_environment(
        self,
    ) -> Callable[[environment.GetEnvironmentRequest], environment.Environment]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEnvironment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_continuous_test_results(
        self,
    ) -> Callable[
        [environment.ListContinuousTestResultsRequest],
        environment.ListContinuousTestResultsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListContinuousTestResults(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_environments(
        self,
    ) -> Callable[
        [environment.ListEnvironmentsRequest], environment.ListEnvironmentsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEnvironments(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def lookup_environment_history(
        self,
    ) -> Callable[
        [environment.LookupEnvironmentHistoryRequest],
        environment.LookupEnvironmentHistoryResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._LookupEnvironmentHistory(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def run_continuous_test(
        self,
    ) -> Callable[[environment.RunContinuousTestRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RunContinuousTest(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_environment(
        self,
    ) -> Callable[
        [gcdc_environment.UpdateEnvironmentRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateEnvironment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseEnvironmentsRestTransport._BaseGetLocation, EnvironmentsRestStub
    ):
        def __hash__(self):
            return hash("EnvironmentsRestTransport.GetLocation")

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
                _BaseEnvironmentsRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = (
                _BaseEnvironmentsRestTransport._BaseGetLocation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseEnvironmentsRestTransport._BaseGetLocation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EnvironmentsRestTransport._GetLocation._get_response(
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
        _BaseEnvironmentsRestTransport._BaseListLocations, EnvironmentsRestStub
    ):
        def __hash__(self):
            return hash("EnvironmentsRestTransport.ListLocations")

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
                _BaseEnvironmentsRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseEnvironmentsRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseEnvironmentsRestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EnvironmentsRestTransport._ListLocations._get_response(
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
        _BaseEnvironmentsRestTransport._BaseCancelOperation, EnvironmentsRestStub
    ):
        def __hash__(self):
            return hash("EnvironmentsRestTransport.CancelOperation")

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
                _BaseEnvironmentsRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseEnvironmentsRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseEnvironmentsRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EnvironmentsRestTransport._CancelOperation._get_response(
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

            return self._interceptor.post_cancel_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseEnvironmentsRestTransport._BaseGetOperation, EnvironmentsRestStub
    ):
        def __hash__(self):
            return hash("EnvironmentsRestTransport.GetOperation")

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
                _BaseEnvironmentsRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseEnvironmentsRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseEnvironmentsRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EnvironmentsRestTransport._GetOperation._get_response(
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
        _BaseEnvironmentsRestTransport._BaseListOperations, EnvironmentsRestStub
    ):
        def __hash__(self):
            return hash("EnvironmentsRestTransport.ListOperations")

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
                _BaseEnvironmentsRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseEnvironmentsRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseEnvironmentsRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EnvironmentsRestTransport._ListOperations._get_response(
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


__all__ = ("EnvironmentsRestTransport",)
