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
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.policysimulator_v1.types import simulator

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseSimulatorRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class SimulatorRestInterceptor:
    """Interceptor for Simulator.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the SimulatorRestTransport.

    .. code-block:: python
        class MyCustomSimulatorInterceptor(SimulatorRestInterceptor):
            def pre_create_replay(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_replay(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_replay(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_replay(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_replay_results(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_replay_results(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = SimulatorRestTransport(interceptor=MyCustomSimulatorInterceptor())
        client = SimulatorClient(transport=transport)


    """

    def pre_create_replay(
        self,
        request: simulator.CreateReplayRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[simulator.CreateReplayRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_replay

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Simulator server.
        """
        return request, metadata

    def post_create_replay(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_replay

        Override in a subclass to manipulate the response
        after it is returned by the Simulator server but before
        it is returned to user code.
        """
        return response

    def pre_get_replay(
        self, request: simulator.GetReplayRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[simulator.GetReplayRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_replay

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Simulator server.
        """
        return request, metadata

    def post_get_replay(self, response: simulator.Replay) -> simulator.Replay:
        """Post-rpc interceptor for get_replay

        Override in a subclass to manipulate the response
        after it is returned by the Simulator server but before
        it is returned to user code.
        """
        return response

    def pre_list_replay_results(
        self,
        request: simulator.ListReplayResultsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[simulator.ListReplayResultsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_replay_results

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Simulator server.
        """
        return request, metadata

    def post_list_replay_results(
        self, response: simulator.ListReplayResultsResponse
    ) -> simulator.ListReplayResultsResponse:
        """Post-rpc interceptor for list_replay_results

        Override in a subclass to manipulate the response
        after it is returned by the Simulator server but before
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
        before they are sent to the Simulator server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Simulator server but before
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
        before they are sent to the Simulator server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Simulator server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class SimulatorRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: SimulatorRestInterceptor


class SimulatorRestTransport(_BaseSimulatorRestTransport):
    """REST backend synchronous transport for Simulator.

    Policy Simulator API service.

    Policy Simulator is a collection of endpoints for creating, running,
    and viewing a [Replay][google.cloud.policysimulator.v1.Replay]. A
    [Replay][google.cloud.policysimulator.v1.Replay] is a type of
    simulation that lets you see how your principals' access to
    resources might change if you changed your IAM policy.

    During a [Replay][google.cloud.policysimulator.v1.Replay], Policy
    Simulator re-evaluates, or replays, past access attempts under both
    the current policy and your proposed policy, and compares those
    results to determine how your principals' access might change under
    the proposed policy.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "policysimulator.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[SimulatorRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'policysimulator.googleapis.com').
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
        self._interceptor = interceptor or SimulatorRestInterceptor()
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
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=operations/**}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/replays/*/operations/**}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=folders/*/locations/*/replays/*/operations/**}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=organizations/*/locations/*/replays/*/operations/**}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=operations}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/replays/*/operations}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=folders/*/locations/*/replays/*/operations}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=organizations/*/locations/*/replays/*/operations}",
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

    class _CreateReplay(
        _BaseSimulatorRestTransport._BaseCreateReplay, SimulatorRestStub
    ):
        def __hash__(self):
            return hash("SimulatorRestTransport.CreateReplay")

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
            request: simulator.CreateReplayRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create replay method over HTTP.

            Args:
                request (~.simulator.CreateReplayRequest):
                    The request object. Request message for
                [Simulator.CreateReplay][google.cloud.policysimulator.v1.Simulator.CreateReplay].
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
                _BaseSimulatorRestTransport._BaseCreateReplay._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_replay(request, metadata)
            transcoded_request = (
                _BaseSimulatorRestTransport._BaseCreateReplay._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseSimulatorRestTransport._BaseCreateReplay._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseSimulatorRestTransport._BaseCreateReplay._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SimulatorRestTransport._CreateReplay._get_response(
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
            resp = self._interceptor.post_create_replay(resp)
            return resp

    class _GetReplay(_BaseSimulatorRestTransport._BaseGetReplay, SimulatorRestStub):
        def __hash__(self):
            return hash("SimulatorRestTransport.GetReplay")

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
            request: simulator.GetReplayRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> simulator.Replay:
            r"""Call the get replay method over HTTP.

            Args:
                request (~.simulator.GetReplayRequest):
                    The request object. Request message for
                [Simulator.GetReplay][google.cloud.policysimulator.v1.Simulator.GetReplay].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.simulator.Replay:
                    A resource describing a ``Replay``, or simulation.
            """

            http_options = (
                _BaseSimulatorRestTransport._BaseGetReplay._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_replay(request, metadata)
            transcoded_request = (
                _BaseSimulatorRestTransport._BaseGetReplay._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSimulatorRestTransport._BaseGetReplay._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SimulatorRestTransport._GetReplay._get_response(
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
            resp = simulator.Replay()
            pb_resp = simulator.Replay.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_replay(resp)
            return resp

    class _ListReplayResults(
        _BaseSimulatorRestTransport._BaseListReplayResults, SimulatorRestStub
    ):
        def __hash__(self):
            return hash("SimulatorRestTransport.ListReplayResults")

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
            request: simulator.ListReplayResultsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> simulator.ListReplayResultsResponse:
            r"""Call the list replay results method over HTTP.

            Args:
                request (~.simulator.ListReplayResultsRequest):
                    The request object. Request message for
                [Simulator.ListReplayResults][google.cloud.policysimulator.v1.Simulator.ListReplayResults].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.simulator.ListReplayResultsResponse:
                    Response message for
                [Simulator.ListReplayResults][google.cloud.policysimulator.v1.Simulator.ListReplayResults].

            """

            http_options = (
                _BaseSimulatorRestTransport._BaseListReplayResults._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_replay_results(
                request, metadata
            )
            transcoded_request = _BaseSimulatorRestTransport._BaseListReplayResults._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSimulatorRestTransport._BaseListReplayResults._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SimulatorRestTransport._ListReplayResults._get_response(
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
            resp = simulator.ListReplayResultsResponse()
            pb_resp = simulator.ListReplayResultsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_replay_results(resp)
            return resp

    @property
    def create_replay(
        self,
    ) -> Callable[[simulator.CreateReplayRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateReplay(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_replay(self) -> Callable[[simulator.GetReplayRequest], simulator.Replay]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetReplay(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_replay_results(
        self,
    ) -> Callable[
        [simulator.ListReplayResultsRequest], simulator.ListReplayResultsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListReplayResults(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseSimulatorRestTransport._BaseGetOperation, SimulatorRestStub
    ):
        def __hash__(self):
            return hash("SimulatorRestTransport.GetOperation")

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
                _BaseSimulatorRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = (
                _BaseSimulatorRestTransport._BaseGetOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSimulatorRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SimulatorRestTransport._GetOperation._get_response(
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
        _BaseSimulatorRestTransport._BaseListOperations, SimulatorRestStub
    ):
        def __hash__(self):
            return hash("SimulatorRestTransport.ListOperations")

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
                _BaseSimulatorRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = (
                _BaseSimulatorRestTransport._BaseListOperations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSimulatorRestTransport._BaseListOperations._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SimulatorRestTransport._ListOperations._get_response(
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


__all__ = ("SimulatorRestTransport",)
