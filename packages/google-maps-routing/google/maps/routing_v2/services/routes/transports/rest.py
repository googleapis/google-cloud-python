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
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.maps.routing_v2.types import routes_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseRoutesRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class RoutesRestInterceptor:
    """Interceptor for Routes.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the RoutesRestTransport.

    .. code-block:: python
        class MyCustomRoutesInterceptor(RoutesRestInterceptor):
            def pre_compute_route_matrix(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_compute_route_matrix(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_compute_routes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_compute_routes(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = RoutesRestTransport(interceptor=MyCustomRoutesInterceptor())
        client = RoutesClient(transport=transport)


    """

    def pre_compute_route_matrix(
        self,
        request: routes_service.ComputeRouteMatrixRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[routes_service.ComputeRouteMatrixRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for compute_route_matrix

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Routes server.
        """
        return request, metadata

    def post_compute_route_matrix(
        self, response: rest_streaming.ResponseIterator
    ) -> rest_streaming.ResponseIterator:
        """Post-rpc interceptor for compute_route_matrix

        Override in a subclass to manipulate the response
        after it is returned by the Routes server but before
        it is returned to user code.
        """
        return response

    def pre_compute_routes(
        self,
        request: routes_service.ComputeRoutesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[routes_service.ComputeRoutesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for compute_routes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Routes server.
        """
        return request, metadata

    def post_compute_routes(
        self, response: routes_service.ComputeRoutesResponse
    ) -> routes_service.ComputeRoutesResponse:
        """Post-rpc interceptor for compute_routes

        Override in a subclass to manipulate the response
        after it is returned by the Routes server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class RoutesRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: RoutesRestInterceptor


class RoutesRestTransport(_BaseRoutesRestTransport):
    """REST backend synchronous transport for Routes.

    The Routes API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "routes.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[RoutesRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'routes.googleapis.com').
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
        self._interceptor = interceptor or RoutesRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _ComputeRouteMatrix(
        _BaseRoutesRestTransport._BaseComputeRouteMatrix, RoutesRestStub
    ):
        def __hash__(self):
            return hash("RoutesRestTransport.ComputeRouteMatrix")

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
                stream=True,
            )
            return response

        def __call__(
            self,
            request: routes_service.ComputeRouteMatrixRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> rest_streaming.ResponseIterator:
            r"""Call the compute route matrix method over HTTP.

            Args:
                request (~.routes_service.ComputeRouteMatrixRequest):
                    The request object. ComputeRouteMatrix request message
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.routes_service.RouteMatrixElement:
                    Contains route information computed
                for an origin/destination pair in the
                ComputeRouteMatrix API. This proto can
                be streamed to the client.

            """

            http_options = (
                _BaseRoutesRestTransport._BaseComputeRouteMatrix._get_http_options()
            )
            request, metadata = self._interceptor.pre_compute_route_matrix(
                request, metadata
            )
            transcoded_request = _BaseRoutesRestTransport._BaseComputeRouteMatrix._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseRoutesRestTransport._BaseComputeRouteMatrix._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRoutesRestTransport._BaseComputeRouteMatrix._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = RoutesRestTransport._ComputeRouteMatrix._get_response(
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
            resp = rest_streaming.ResponseIterator(
                response, routes_service.RouteMatrixElement
            )
            resp = self._interceptor.post_compute_route_matrix(resp)
            return resp

    class _ComputeRoutes(_BaseRoutesRestTransport._BaseComputeRoutes, RoutesRestStub):
        def __hash__(self):
            return hash("RoutesRestTransport.ComputeRoutes")

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
            request: routes_service.ComputeRoutesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> routes_service.ComputeRoutesResponse:
            r"""Call the compute routes method over HTTP.

            Args:
                request (~.routes_service.ComputeRoutesRequest):
                    The request object. ComputeRoutes request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.routes_service.ComputeRoutesResponse:
                    ComputeRoutes the response message.
            """

            http_options = (
                _BaseRoutesRestTransport._BaseComputeRoutes._get_http_options()
            )
            request, metadata = self._interceptor.pre_compute_routes(request, metadata)
            transcoded_request = (
                _BaseRoutesRestTransport._BaseComputeRoutes._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseRoutesRestTransport._BaseComputeRoutes._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseRoutesRestTransport._BaseComputeRoutes._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = RoutesRestTransport._ComputeRoutes._get_response(
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
            resp = routes_service.ComputeRoutesResponse()
            pb_resp = routes_service.ComputeRoutesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_compute_routes(resp)
            return resp

    @property
    def compute_route_matrix(
        self,
    ) -> Callable[
        [routes_service.ComputeRouteMatrixRequest], routes_service.RouteMatrixElement
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ComputeRouteMatrix(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def compute_routes(
        self,
    ) -> Callable[
        [routes_service.ComputeRoutesRequest], routes_service.ComputeRoutesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ComputeRoutes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("RoutesRestTransport",)
