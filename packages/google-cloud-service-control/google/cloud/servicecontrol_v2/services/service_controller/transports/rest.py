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

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.servicecontrol_v2.types import service_controller

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseServiceControllerRestTransport

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


class ServiceControllerRestInterceptor:
    """Interceptor for ServiceController.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ServiceControllerRestTransport.

    .. code-block:: python
        class MyCustomServiceControllerInterceptor(ServiceControllerRestInterceptor):
            def pre_check(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_check(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_report(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_report(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ServiceControllerRestTransport(interceptor=MyCustomServiceControllerInterceptor())
        client = ServiceControllerClient(transport=transport)


    """

    def pre_check(
        self,
        request: service_controller.CheckRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service_controller.CheckRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for check

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceController server.
        """
        return request, metadata

    def post_check(
        self, response: service_controller.CheckResponse
    ) -> service_controller.CheckResponse:
        """Post-rpc interceptor for check

        Override in a subclass to manipulate the response
        after it is returned by the ServiceController server but before
        it is returned to user code.
        """
        return response

    def pre_report(
        self,
        request: service_controller.ReportRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service_controller.ReportRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for report

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceController server.
        """
        return request, metadata

    def post_report(
        self, response: service_controller.ReportResponse
    ) -> service_controller.ReportResponse:
        """Post-rpc interceptor for report

        Override in a subclass to manipulate the response
        after it is returned by the ServiceController server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ServiceControllerRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ServiceControllerRestInterceptor


class ServiceControllerRestTransport(_BaseServiceControllerRestTransport):
    """REST backend synchronous transport for ServiceController.

    `Service Control API
    v2 <https://cloud.google.com/service-infrastructure/docs/service-control/access-control>`__

    Private Preview. This feature is only available for approved
    services.

    This API provides admission control and telemetry reporting for
    services that are integrated with `Service
    Infrastructure <https://cloud.google.com/service-infrastructure>`__.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "servicecontrol.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ServiceControllerRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'servicecontrol.googleapis.com').
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
        self._interceptor = interceptor or ServiceControllerRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _Check(
        _BaseServiceControllerRestTransport._BaseCheck, ServiceControllerRestStub
    ):
        def __hash__(self):
            return hash("ServiceControllerRestTransport.Check")

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
            request: service_controller.CheckRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service_controller.CheckResponse:
            r"""Call the check method over HTTP.

            Args:
                request (~.service_controller.CheckRequest):
                    The request object. Request message for the Check method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service_controller.CheckResponse:
                    Response message for the Check
                method.

            """

            http_options = (
                _BaseServiceControllerRestTransport._BaseCheck._get_http_options()
            )

            request, metadata = self._interceptor.pre_check(request, metadata)
            transcoded_request = (
                _BaseServiceControllerRestTransport._BaseCheck._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseServiceControllerRestTransport._BaseCheck._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseServiceControllerRestTransport._BaseCheck._get_query_params_json(
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
                    f"Sending request for google.api.servicecontrol_v2.ServiceControllerClient.Check",
                    extra={
                        "serviceName": "google.api.servicecontrol.v2.ServiceController",
                        "rpcName": "Check",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ServiceControllerRestTransport._Check._get_response(
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
            resp = service_controller.CheckResponse()
            pb_resp = service_controller.CheckResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_check(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service_controller.CheckResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.api.servicecontrol_v2.ServiceControllerClient.check",
                    extra={
                        "serviceName": "google.api.servicecontrol.v2.ServiceController",
                        "rpcName": "Check",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _Report(
        _BaseServiceControllerRestTransport._BaseReport, ServiceControllerRestStub
    ):
        def __hash__(self):
            return hash("ServiceControllerRestTransport.Report")

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
            request: service_controller.ReportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service_controller.ReportResponse:
            r"""Call the report method over HTTP.

            Args:
                request (~.service_controller.ReportRequest):
                    The request object. Request message for the Report
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service_controller.ReportResponse:
                    Response message for the Report
                method. If the request contains any
                invalid data, the server returns an RPC
                error.

            """

            http_options = (
                _BaseServiceControllerRestTransport._BaseReport._get_http_options()
            )

            request, metadata = self._interceptor.pre_report(request, metadata)
            transcoded_request = (
                _BaseServiceControllerRestTransport._BaseReport._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseServiceControllerRestTransport._BaseReport._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseServiceControllerRestTransport._BaseReport._get_query_params_json(
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
                    f"Sending request for google.api.servicecontrol_v2.ServiceControllerClient.Report",
                    extra={
                        "serviceName": "google.api.servicecontrol.v2.ServiceController",
                        "rpcName": "Report",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ServiceControllerRestTransport._Report._get_response(
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
            resp = service_controller.ReportResponse()
            pb_resp = service_controller.ReportResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_report(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service_controller.ReportResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.api.servicecontrol_v2.ServiceControllerClient.report",
                    extra={
                        "serviceName": "google.api.servicecontrol.v2.ServiceController",
                        "rpcName": "Report",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def check(
        self,
    ) -> Callable[[service_controller.CheckRequest], service_controller.CheckResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Check(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def report(
        self,
    ) -> Callable[
        [service_controller.ReportRequest], service_controller.ReportResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Report(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ServiceControllerRestTransport",)
