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
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.ads.admanager_v1.types import placement_messages, placement_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BasePlacementServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class PlacementServiceRestInterceptor:
    """Interceptor for PlacementService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the PlacementServiceRestTransport.

    .. code-block:: python
        class MyCustomPlacementServiceInterceptor(PlacementServiceRestInterceptor):
            def pre_get_placement(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_placement(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_placements(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_placements(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = PlacementServiceRestTransport(interceptor=MyCustomPlacementServiceInterceptor())
        client = PlacementServiceClient(transport=transport)


    """

    def pre_get_placement(
        self,
        request: placement_service.GetPlacementRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[placement_service.GetPlacementRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_placement

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PlacementService server.
        """
        return request, metadata

    def post_get_placement(
        self, response: placement_messages.Placement
    ) -> placement_messages.Placement:
        """Post-rpc interceptor for get_placement

        Override in a subclass to manipulate the response
        after it is returned by the PlacementService server but before
        it is returned to user code.
        """
        return response

    def pre_list_placements(
        self,
        request: placement_service.ListPlacementsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[placement_service.ListPlacementsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_placements

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PlacementService server.
        """
        return request, metadata

    def post_list_placements(
        self, response: placement_service.ListPlacementsResponse
    ) -> placement_service.ListPlacementsResponse:
        """Post-rpc interceptor for list_placements

        Override in a subclass to manipulate the response
        after it is returned by the PlacementService server but before
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
        before they are sent to the PlacementService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the PlacementService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class PlacementServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: PlacementServiceRestInterceptor


class PlacementServiceRestTransport(_BasePlacementServiceRestTransport):
    """REST backend synchronous transport for PlacementService.

    Provides methods for handling ``Placement`` objects.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "admanager.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[PlacementServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'admanager.googleapis.com').
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
        self._interceptor = interceptor or PlacementServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _GetPlacement(
        _BasePlacementServiceRestTransport._BaseGetPlacement, PlacementServiceRestStub
    ):
        def __hash__(self):
            return hash("PlacementServiceRestTransport.GetPlacement")

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
            request: placement_service.GetPlacementRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> placement_messages.Placement:
            r"""Call the get placement method over HTTP.

            Args:
                request (~.placement_service.GetPlacementRequest):
                    The request object. Request object for ``GetPlacement`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.placement_messages.Placement:
                    The ``Placement`` resource.
            """

            http_options = (
                _BasePlacementServiceRestTransport._BaseGetPlacement._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_placement(request, metadata)
            transcoded_request = _BasePlacementServiceRestTransport._BaseGetPlacement._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePlacementServiceRestTransport._BaseGetPlacement._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PlacementServiceRestTransport._GetPlacement._get_response(
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
            resp = placement_messages.Placement()
            pb_resp = placement_messages.Placement.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_placement(resp)
            return resp

    class _ListPlacements(
        _BasePlacementServiceRestTransport._BaseListPlacements, PlacementServiceRestStub
    ):
        def __hash__(self):
            return hash("PlacementServiceRestTransport.ListPlacements")

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
            request: placement_service.ListPlacementsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> placement_service.ListPlacementsResponse:
            r"""Call the list placements method over HTTP.

            Args:
                request (~.placement_service.ListPlacementsRequest):
                    The request object. Request object for ``ListPlacements`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.placement_service.ListPlacementsResponse:
                    Response object for ``ListPlacementsRequest`` containing
                matching ``Placement`` objects.

            """

            http_options = (
                _BasePlacementServiceRestTransport._BaseListPlacements._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_placements(request, metadata)
            transcoded_request = _BasePlacementServiceRestTransport._BaseListPlacements._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePlacementServiceRestTransport._BaseListPlacements._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PlacementServiceRestTransport._ListPlacements._get_response(
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
            resp = placement_service.ListPlacementsResponse()
            pb_resp = placement_service.ListPlacementsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_placements(resp)
            return resp

    @property
    def get_placement(
        self,
    ) -> Callable[
        [placement_service.GetPlacementRequest], placement_messages.Placement
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPlacement(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_placements(
        self,
    ) -> Callable[
        [placement_service.ListPlacementsRequest],
        placement_service.ListPlacementsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPlacements(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BasePlacementServiceRestTransport._BaseGetOperation, PlacementServiceRestStub
    ):
        def __hash__(self):
            return hash("PlacementServiceRestTransport.GetOperation")

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
                _BasePlacementServiceRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BasePlacementServiceRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePlacementServiceRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PlacementServiceRestTransport._GetOperation._get_response(
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


__all__ = ("PlacementServiceRestTransport",)
