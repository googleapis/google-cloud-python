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
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.websecurityscanner_v1.types import (
    finding,
    scan_config,
    scan_run,
    web_security_scanner,
)

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseWebSecurityScannerRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class WebSecurityScannerRestInterceptor:
    """Interceptor for WebSecurityScanner.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the WebSecurityScannerRestTransport.

    .. code-block:: python
        class MyCustomWebSecurityScannerInterceptor(WebSecurityScannerRestInterceptor):
            def pre_create_scan_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_scan_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_scan_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_finding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_finding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_scan_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_scan_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_scan_run(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_scan_run(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_crawled_urls(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_crawled_urls(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_findings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_findings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_finding_type_stats(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_finding_type_stats(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_scan_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_scan_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_scan_runs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_scan_runs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_start_scan_run(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_start_scan_run(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_stop_scan_run(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_stop_scan_run(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_scan_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_scan_config(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = WebSecurityScannerRestTransport(interceptor=MyCustomWebSecurityScannerInterceptor())
        client = WebSecurityScannerClient(transport=transport)


    """

    def pre_create_scan_config(
        self,
        request: web_security_scanner.CreateScanConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[web_security_scanner.CreateScanConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_scan_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the WebSecurityScanner server.
        """
        return request, metadata

    def post_create_scan_config(
        self, response: scan_config.ScanConfig
    ) -> scan_config.ScanConfig:
        """Post-rpc interceptor for create_scan_config

        Override in a subclass to manipulate the response
        after it is returned by the WebSecurityScanner server but before
        it is returned to user code.
        """
        return response

    def pre_delete_scan_config(
        self,
        request: web_security_scanner.DeleteScanConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[web_security_scanner.DeleteScanConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_scan_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the WebSecurityScanner server.
        """
        return request, metadata

    def pre_get_finding(
        self,
        request: web_security_scanner.GetFindingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[web_security_scanner.GetFindingRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_finding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the WebSecurityScanner server.
        """
        return request, metadata

    def post_get_finding(self, response: finding.Finding) -> finding.Finding:
        """Post-rpc interceptor for get_finding

        Override in a subclass to manipulate the response
        after it is returned by the WebSecurityScanner server but before
        it is returned to user code.
        """
        return response

    def pre_get_scan_config(
        self,
        request: web_security_scanner.GetScanConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[web_security_scanner.GetScanConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_scan_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the WebSecurityScanner server.
        """
        return request, metadata

    def post_get_scan_config(
        self, response: scan_config.ScanConfig
    ) -> scan_config.ScanConfig:
        """Post-rpc interceptor for get_scan_config

        Override in a subclass to manipulate the response
        after it is returned by the WebSecurityScanner server but before
        it is returned to user code.
        """
        return response

    def pre_get_scan_run(
        self,
        request: web_security_scanner.GetScanRunRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[web_security_scanner.GetScanRunRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_scan_run

        Override in a subclass to manipulate the request or metadata
        before they are sent to the WebSecurityScanner server.
        """
        return request, metadata

    def post_get_scan_run(self, response: scan_run.ScanRun) -> scan_run.ScanRun:
        """Post-rpc interceptor for get_scan_run

        Override in a subclass to manipulate the response
        after it is returned by the WebSecurityScanner server but before
        it is returned to user code.
        """
        return response

    def pre_list_crawled_urls(
        self,
        request: web_security_scanner.ListCrawledUrlsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[web_security_scanner.ListCrawledUrlsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_crawled_urls

        Override in a subclass to manipulate the request or metadata
        before they are sent to the WebSecurityScanner server.
        """
        return request, metadata

    def post_list_crawled_urls(
        self, response: web_security_scanner.ListCrawledUrlsResponse
    ) -> web_security_scanner.ListCrawledUrlsResponse:
        """Post-rpc interceptor for list_crawled_urls

        Override in a subclass to manipulate the response
        after it is returned by the WebSecurityScanner server but before
        it is returned to user code.
        """
        return response

    def pre_list_findings(
        self,
        request: web_security_scanner.ListFindingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[web_security_scanner.ListFindingsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_findings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the WebSecurityScanner server.
        """
        return request, metadata

    def post_list_findings(
        self, response: web_security_scanner.ListFindingsResponse
    ) -> web_security_scanner.ListFindingsResponse:
        """Post-rpc interceptor for list_findings

        Override in a subclass to manipulate the response
        after it is returned by the WebSecurityScanner server but before
        it is returned to user code.
        """
        return response

    def pre_list_finding_type_stats(
        self,
        request: web_security_scanner.ListFindingTypeStatsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        web_security_scanner.ListFindingTypeStatsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_finding_type_stats

        Override in a subclass to manipulate the request or metadata
        before they are sent to the WebSecurityScanner server.
        """
        return request, metadata

    def post_list_finding_type_stats(
        self, response: web_security_scanner.ListFindingTypeStatsResponse
    ) -> web_security_scanner.ListFindingTypeStatsResponse:
        """Post-rpc interceptor for list_finding_type_stats

        Override in a subclass to manipulate the response
        after it is returned by the WebSecurityScanner server but before
        it is returned to user code.
        """
        return response

    def pre_list_scan_configs(
        self,
        request: web_security_scanner.ListScanConfigsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[web_security_scanner.ListScanConfigsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_scan_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the WebSecurityScanner server.
        """
        return request, metadata

    def post_list_scan_configs(
        self, response: web_security_scanner.ListScanConfigsResponse
    ) -> web_security_scanner.ListScanConfigsResponse:
        """Post-rpc interceptor for list_scan_configs

        Override in a subclass to manipulate the response
        after it is returned by the WebSecurityScanner server but before
        it is returned to user code.
        """
        return response

    def pre_list_scan_runs(
        self,
        request: web_security_scanner.ListScanRunsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[web_security_scanner.ListScanRunsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_scan_runs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the WebSecurityScanner server.
        """
        return request, metadata

    def post_list_scan_runs(
        self, response: web_security_scanner.ListScanRunsResponse
    ) -> web_security_scanner.ListScanRunsResponse:
        """Post-rpc interceptor for list_scan_runs

        Override in a subclass to manipulate the response
        after it is returned by the WebSecurityScanner server but before
        it is returned to user code.
        """
        return response

    def pre_start_scan_run(
        self,
        request: web_security_scanner.StartScanRunRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[web_security_scanner.StartScanRunRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for start_scan_run

        Override in a subclass to manipulate the request or metadata
        before they are sent to the WebSecurityScanner server.
        """
        return request, metadata

    def post_start_scan_run(self, response: scan_run.ScanRun) -> scan_run.ScanRun:
        """Post-rpc interceptor for start_scan_run

        Override in a subclass to manipulate the response
        after it is returned by the WebSecurityScanner server but before
        it is returned to user code.
        """
        return response

    def pre_stop_scan_run(
        self,
        request: web_security_scanner.StopScanRunRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[web_security_scanner.StopScanRunRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for stop_scan_run

        Override in a subclass to manipulate the request or metadata
        before they are sent to the WebSecurityScanner server.
        """
        return request, metadata

    def post_stop_scan_run(self, response: scan_run.ScanRun) -> scan_run.ScanRun:
        """Post-rpc interceptor for stop_scan_run

        Override in a subclass to manipulate the response
        after it is returned by the WebSecurityScanner server but before
        it is returned to user code.
        """
        return response

    def pre_update_scan_config(
        self,
        request: web_security_scanner.UpdateScanConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[web_security_scanner.UpdateScanConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_scan_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the WebSecurityScanner server.
        """
        return request, metadata

    def post_update_scan_config(
        self, response: scan_config.ScanConfig
    ) -> scan_config.ScanConfig:
        """Post-rpc interceptor for update_scan_config

        Override in a subclass to manipulate the response
        after it is returned by the WebSecurityScanner server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class WebSecurityScannerRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: WebSecurityScannerRestInterceptor


class WebSecurityScannerRestTransport(_BaseWebSecurityScannerRestTransport):
    """REST backend synchronous transport for WebSecurityScanner.

    Web Security Scanner Service identifies security
    vulnerabilities in web applications hosted on Google Cloud. It
    crawls your application, and attempts to exercise as many user
    inputs and event handlers as possible.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "websecurityscanner.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[WebSecurityScannerRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'websecurityscanner.googleapis.com').
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
        self._interceptor = interceptor or WebSecurityScannerRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateScanConfig(
        _BaseWebSecurityScannerRestTransport._BaseCreateScanConfig,
        WebSecurityScannerRestStub,
    ):
        def __hash__(self):
            return hash("WebSecurityScannerRestTransport.CreateScanConfig")

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
            request: web_security_scanner.CreateScanConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> scan_config.ScanConfig:
            r"""Call the create scan config method over HTTP.

            Args:
                request (~.web_security_scanner.CreateScanConfigRequest):
                    The request object. Request for the ``CreateScanConfig`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.scan_config.ScanConfig:
                    A ScanConfig resource contains the
                configurations to launch a scan.

            """

            http_options = (
                _BaseWebSecurityScannerRestTransport._BaseCreateScanConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_scan_config(
                request, metadata
            )
            transcoded_request = _BaseWebSecurityScannerRestTransport._BaseCreateScanConfig._get_transcoded_request(
                http_options, request
            )

            body = _BaseWebSecurityScannerRestTransport._BaseCreateScanConfig._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseWebSecurityScannerRestTransport._BaseCreateScanConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WebSecurityScannerRestTransport._CreateScanConfig._get_response(
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
            resp = scan_config.ScanConfig()
            pb_resp = scan_config.ScanConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_scan_config(resp)
            return resp

    class _DeleteScanConfig(
        _BaseWebSecurityScannerRestTransport._BaseDeleteScanConfig,
        WebSecurityScannerRestStub,
    ):
        def __hash__(self):
            return hash("WebSecurityScannerRestTransport.DeleteScanConfig")

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
            request: web_security_scanner.DeleteScanConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete scan config method over HTTP.

            Args:
                request (~.web_security_scanner.DeleteScanConfigRequest):
                    The request object. Request for the ``DeleteScanConfig`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseWebSecurityScannerRestTransport._BaseDeleteScanConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_scan_config(
                request, metadata
            )
            transcoded_request = _BaseWebSecurityScannerRestTransport._BaseDeleteScanConfig._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWebSecurityScannerRestTransport._BaseDeleteScanConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WebSecurityScannerRestTransport._DeleteScanConfig._get_response(
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

    class _GetFinding(
        _BaseWebSecurityScannerRestTransport._BaseGetFinding, WebSecurityScannerRestStub
    ):
        def __hash__(self):
            return hash("WebSecurityScannerRestTransport.GetFinding")

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
            request: web_security_scanner.GetFindingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> finding.Finding:
            r"""Call the get finding method over HTTP.

            Args:
                request (~.web_security_scanner.GetFindingRequest):
                    The request object. Request for the ``GetFinding`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.finding.Finding:
                    A Finding resource represents a
                vulnerability instance identified during
                a ScanRun.

            """

            http_options = (
                _BaseWebSecurityScannerRestTransport._BaseGetFinding._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_finding(request, metadata)
            transcoded_request = _BaseWebSecurityScannerRestTransport._BaseGetFinding._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWebSecurityScannerRestTransport._BaseGetFinding._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WebSecurityScannerRestTransport._GetFinding._get_response(
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
            resp = finding.Finding()
            pb_resp = finding.Finding.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_finding(resp)
            return resp

    class _GetScanConfig(
        _BaseWebSecurityScannerRestTransport._BaseGetScanConfig,
        WebSecurityScannerRestStub,
    ):
        def __hash__(self):
            return hash("WebSecurityScannerRestTransport.GetScanConfig")

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
            request: web_security_scanner.GetScanConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> scan_config.ScanConfig:
            r"""Call the get scan config method over HTTP.

            Args:
                request (~.web_security_scanner.GetScanConfigRequest):
                    The request object. Request for the ``GetScanConfig`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.scan_config.ScanConfig:
                    A ScanConfig resource contains the
                configurations to launch a scan.

            """

            http_options = (
                _BaseWebSecurityScannerRestTransport._BaseGetScanConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_scan_config(request, metadata)
            transcoded_request = _BaseWebSecurityScannerRestTransport._BaseGetScanConfig._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWebSecurityScannerRestTransport._BaseGetScanConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WebSecurityScannerRestTransport._GetScanConfig._get_response(
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
            resp = scan_config.ScanConfig()
            pb_resp = scan_config.ScanConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_scan_config(resp)
            return resp

    class _GetScanRun(
        _BaseWebSecurityScannerRestTransport._BaseGetScanRun, WebSecurityScannerRestStub
    ):
        def __hash__(self):
            return hash("WebSecurityScannerRestTransport.GetScanRun")

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
            request: web_security_scanner.GetScanRunRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> scan_run.ScanRun:
            r"""Call the get scan run method over HTTP.

            Args:
                request (~.web_security_scanner.GetScanRunRequest):
                    The request object. Request for the ``GetScanRun`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.scan_run.ScanRun:
                    A ScanRun is a output-only resource
                representing an actual run of the scan.
                Next id: 12

            """

            http_options = (
                _BaseWebSecurityScannerRestTransport._BaseGetScanRun._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_scan_run(request, metadata)
            transcoded_request = _BaseWebSecurityScannerRestTransport._BaseGetScanRun._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWebSecurityScannerRestTransport._BaseGetScanRun._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WebSecurityScannerRestTransport._GetScanRun._get_response(
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
            resp = scan_run.ScanRun()
            pb_resp = scan_run.ScanRun.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_scan_run(resp)
            return resp

    class _ListCrawledUrls(
        _BaseWebSecurityScannerRestTransport._BaseListCrawledUrls,
        WebSecurityScannerRestStub,
    ):
        def __hash__(self):
            return hash("WebSecurityScannerRestTransport.ListCrawledUrls")

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
            request: web_security_scanner.ListCrawledUrlsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> web_security_scanner.ListCrawledUrlsResponse:
            r"""Call the list crawled urls method over HTTP.

            Args:
                request (~.web_security_scanner.ListCrawledUrlsRequest):
                    The request object. Request for the ``ListCrawledUrls`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.web_security_scanner.ListCrawledUrlsResponse:
                    Response for the ``ListCrawledUrls`` method.
            """

            http_options = (
                _BaseWebSecurityScannerRestTransport._BaseListCrawledUrls._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_crawled_urls(
                request, metadata
            )
            transcoded_request = _BaseWebSecurityScannerRestTransport._BaseListCrawledUrls._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWebSecurityScannerRestTransport._BaseListCrawledUrls._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WebSecurityScannerRestTransport._ListCrawledUrls._get_response(
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
            resp = web_security_scanner.ListCrawledUrlsResponse()
            pb_resp = web_security_scanner.ListCrawledUrlsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_crawled_urls(resp)
            return resp

    class _ListFindings(
        _BaseWebSecurityScannerRestTransport._BaseListFindings,
        WebSecurityScannerRestStub,
    ):
        def __hash__(self):
            return hash("WebSecurityScannerRestTransport.ListFindings")

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
            request: web_security_scanner.ListFindingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> web_security_scanner.ListFindingsResponse:
            r"""Call the list findings method over HTTP.

            Args:
                request (~.web_security_scanner.ListFindingsRequest):
                    The request object. Request for the ``ListFindings`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.web_security_scanner.ListFindingsResponse:
                    Response for the ``ListFindings`` method.
            """

            http_options = (
                _BaseWebSecurityScannerRestTransport._BaseListFindings._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_findings(request, metadata)
            transcoded_request = _BaseWebSecurityScannerRestTransport._BaseListFindings._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWebSecurityScannerRestTransport._BaseListFindings._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WebSecurityScannerRestTransport._ListFindings._get_response(
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
            resp = web_security_scanner.ListFindingsResponse()
            pb_resp = web_security_scanner.ListFindingsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_findings(resp)
            return resp

    class _ListFindingTypeStats(
        _BaseWebSecurityScannerRestTransport._BaseListFindingTypeStats,
        WebSecurityScannerRestStub,
    ):
        def __hash__(self):
            return hash("WebSecurityScannerRestTransport.ListFindingTypeStats")

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
            request: web_security_scanner.ListFindingTypeStatsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> web_security_scanner.ListFindingTypeStatsResponse:
            r"""Call the list finding type stats method over HTTP.

            Args:
                request (~.web_security_scanner.ListFindingTypeStatsRequest):
                    The request object. Request for the ``ListFindingTypeStats`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.web_security_scanner.ListFindingTypeStatsResponse:
                    Response for the ``ListFindingTypeStats`` method.
            """

            http_options = (
                _BaseWebSecurityScannerRestTransport._BaseListFindingTypeStats._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_finding_type_stats(
                request, metadata
            )
            transcoded_request = _BaseWebSecurityScannerRestTransport._BaseListFindingTypeStats._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWebSecurityScannerRestTransport._BaseListFindingTypeStats._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                WebSecurityScannerRestTransport._ListFindingTypeStats._get_response(
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
            resp = web_security_scanner.ListFindingTypeStatsResponse()
            pb_resp = web_security_scanner.ListFindingTypeStatsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_finding_type_stats(resp)
            return resp

    class _ListScanConfigs(
        _BaseWebSecurityScannerRestTransport._BaseListScanConfigs,
        WebSecurityScannerRestStub,
    ):
        def __hash__(self):
            return hash("WebSecurityScannerRestTransport.ListScanConfigs")

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
            request: web_security_scanner.ListScanConfigsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> web_security_scanner.ListScanConfigsResponse:
            r"""Call the list scan configs method over HTTP.

            Args:
                request (~.web_security_scanner.ListScanConfigsRequest):
                    The request object. Request for the ``ListScanConfigs`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.web_security_scanner.ListScanConfigsResponse:
                    Response for the ``ListScanConfigs`` method.
            """

            http_options = (
                _BaseWebSecurityScannerRestTransport._BaseListScanConfigs._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_scan_configs(
                request, metadata
            )
            transcoded_request = _BaseWebSecurityScannerRestTransport._BaseListScanConfigs._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWebSecurityScannerRestTransport._BaseListScanConfigs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WebSecurityScannerRestTransport._ListScanConfigs._get_response(
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
            resp = web_security_scanner.ListScanConfigsResponse()
            pb_resp = web_security_scanner.ListScanConfigsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_scan_configs(resp)
            return resp

    class _ListScanRuns(
        _BaseWebSecurityScannerRestTransport._BaseListScanRuns,
        WebSecurityScannerRestStub,
    ):
        def __hash__(self):
            return hash("WebSecurityScannerRestTransport.ListScanRuns")

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
            request: web_security_scanner.ListScanRunsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> web_security_scanner.ListScanRunsResponse:
            r"""Call the list scan runs method over HTTP.

            Args:
                request (~.web_security_scanner.ListScanRunsRequest):
                    The request object. Request for the ``ListScanRuns`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.web_security_scanner.ListScanRunsResponse:
                    Response for the ``ListScanRuns`` method.
            """

            http_options = (
                _BaseWebSecurityScannerRestTransport._BaseListScanRuns._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_scan_runs(request, metadata)
            transcoded_request = _BaseWebSecurityScannerRestTransport._BaseListScanRuns._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWebSecurityScannerRestTransport._BaseListScanRuns._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WebSecurityScannerRestTransport._ListScanRuns._get_response(
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
            resp = web_security_scanner.ListScanRunsResponse()
            pb_resp = web_security_scanner.ListScanRunsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_scan_runs(resp)
            return resp

    class _StartScanRun(
        _BaseWebSecurityScannerRestTransport._BaseStartScanRun,
        WebSecurityScannerRestStub,
    ):
        def __hash__(self):
            return hash("WebSecurityScannerRestTransport.StartScanRun")

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
            request: web_security_scanner.StartScanRunRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> scan_run.ScanRun:
            r"""Call the start scan run method over HTTP.

            Args:
                request (~.web_security_scanner.StartScanRunRequest):
                    The request object. Request for the ``StartScanRun`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.scan_run.ScanRun:
                    A ScanRun is a output-only resource
                representing an actual run of the scan.
                Next id: 12

            """

            http_options = (
                _BaseWebSecurityScannerRestTransport._BaseStartScanRun._get_http_options()
            )
            request, metadata = self._interceptor.pre_start_scan_run(request, metadata)
            transcoded_request = _BaseWebSecurityScannerRestTransport._BaseStartScanRun._get_transcoded_request(
                http_options, request
            )

            body = _BaseWebSecurityScannerRestTransport._BaseStartScanRun._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseWebSecurityScannerRestTransport._BaseStartScanRun._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WebSecurityScannerRestTransport._StartScanRun._get_response(
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
            resp = scan_run.ScanRun()
            pb_resp = scan_run.ScanRun.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_start_scan_run(resp)
            return resp

    class _StopScanRun(
        _BaseWebSecurityScannerRestTransport._BaseStopScanRun,
        WebSecurityScannerRestStub,
    ):
        def __hash__(self):
            return hash("WebSecurityScannerRestTransport.StopScanRun")

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
            request: web_security_scanner.StopScanRunRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> scan_run.ScanRun:
            r"""Call the stop scan run method over HTTP.

            Args:
                request (~.web_security_scanner.StopScanRunRequest):
                    The request object. Request for the ``StopScanRun`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.scan_run.ScanRun:
                    A ScanRun is a output-only resource
                representing an actual run of the scan.
                Next id: 12

            """

            http_options = (
                _BaseWebSecurityScannerRestTransport._BaseStopScanRun._get_http_options()
            )
            request, metadata = self._interceptor.pre_stop_scan_run(request, metadata)
            transcoded_request = _BaseWebSecurityScannerRestTransport._BaseStopScanRun._get_transcoded_request(
                http_options, request
            )

            body = _BaseWebSecurityScannerRestTransport._BaseStopScanRun._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseWebSecurityScannerRestTransport._BaseStopScanRun._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WebSecurityScannerRestTransport._StopScanRun._get_response(
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
            resp = scan_run.ScanRun()
            pb_resp = scan_run.ScanRun.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_stop_scan_run(resp)
            return resp

    class _UpdateScanConfig(
        _BaseWebSecurityScannerRestTransport._BaseUpdateScanConfig,
        WebSecurityScannerRestStub,
    ):
        def __hash__(self):
            return hash("WebSecurityScannerRestTransport.UpdateScanConfig")

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
            request: web_security_scanner.UpdateScanConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> scan_config.ScanConfig:
            r"""Call the update scan config method over HTTP.

            Args:
                request (~.web_security_scanner.UpdateScanConfigRequest):
                    The request object. Request for the ``UpdateScanConfigRequest`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.scan_config.ScanConfig:
                    A ScanConfig resource contains the
                configurations to launch a scan.

            """

            http_options = (
                _BaseWebSecurityScannerRestTransport._BaseUpdateScanConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_scan_config(
                request, metadata
            )
            transcoded_request = _BaseWebSecurityScannerRestTransport._BaseUpdateScanConfig._get_transcoded_request(
                http_options, request
            )

            body = _BaseWebSecurityScannerRestTransport._BaseUpdateScanConfig._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseWebSecurityScannerRestTransport._BaseUpdateScanConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WebSecurityScannerRestTransport._UpdateScanConfig._get_response(
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
            resp = scan_config.ScanConfig()
            pb_resp = scan_config.ScanConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_scan_config(resp)
            return resp

    @property
    def create_scan_config(
        self,
    ) -> Callable[
        [web_security_scanner.CreateScanConfigRequest], scan_config.ScanConfig
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateScanConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_scan_config(
        self,
    ) -> Callable[[web_security_scanner.DeleteScanConfigRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteScanConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_finding(
        self,
    ) -> Callable[[web_security_scanner.GetFindingRequest], finding.Finding]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetFinding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_scan_config(
        self,
    ) -> Callable[[web_security_scanner.GetScanConfigRequest], scan_config.ScanConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetScanConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_scan_run(
        self,
    ) -> Callable[[web_security_scanner.GetScanRunRequest], scan_run.ScanRun]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetScanRun(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_crawled_urls(
        self,
    ) -> Callable[
        [web_security_scanner.ListCrawledUrlsRequest],
        web_security_scanner.ListCrawledUrlsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCrawledUrls(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_findings(
        self,
    ) -> Callable[
        [web_security_scanner.ListFindingsRequest],
        web_security_scanner.ListFindingsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListFindings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_finding_type_stats(
        self,
    ) -> Callable[
        [web_security_scanner.ListFindingTypeStatsRequest],
        web_security_scanner.ListFindingTypeStatsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListFindingTypeStats(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_scan_configs(
        self,
    ) -> Callable[
        [web_security_scanner.ListScanConfigsRequest],
        web_security_scanner.ListScanConfigsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListScanConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_scan_runs(
        self,
    ) -> Callable[
        [web_security_scanner.ListScanRunsRequest],
        web_security_scanner.ListScanRunsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListScanRuns(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def start_scan_run(
        self,
    ) -> Callable[[web_security_scanner.StartScanRunRequest], scan_run.ScanRun]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StartScanRun(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def stop_scan_run(
        self,
    ) -> Callable[[web_security_scanner.StopScanRunRequest], scan_run.ScanRun]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StopScanRun(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_scan_config(
        self,
    ) -> Callable[
        [web_security_scanner.UpdateScanConfigRequest], scan_config.ScanConfig
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateScanConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("WebSecurityScannerRestTransport",)
