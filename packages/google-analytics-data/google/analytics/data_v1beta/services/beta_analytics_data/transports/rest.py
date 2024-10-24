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

from google.analytics.data_v1beta.types import analytics_data_api

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseBetaAnalyticsDataRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class BetaAnalyticsDataRestInterceptor:
    """Interceptor for BetaAnalyticsData.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the BetaAnalyticsDataRestTransport.

    .. code-block:: python
        class MyCustomBetaAnalyticsDataInterceptor(BetaAnalyticsDataRestInterceptor):
            def pre_batch_run_pivot_reports(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_run_pivot_reports(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_run_reports(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_run_reports(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_check_compatibility(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_check_compatibility(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_audience_export(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_audience_export(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_audience_export(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_audience_export(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_metadata(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_metadata(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_audience_exports(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_audience_exports(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_query_audience_export(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_query_audience_export(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_run_pivot_report(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_run_pivot_report(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_run_realtime_report(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_run_realtime_report(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_run_report(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_run_report(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = BetaAnalyticsDataRestTransport(interceptor=MyCustomBetaAnalyticsDataInterceptor())
        client = BetaAnalyticsDataClient(transport=transport)


    """

    def pre_batch_run_pivot_reports(
        self,
        request: analytics_data_api.BatchRunPivotReportsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_data_api.BatchRunPivotReportsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for batch_run_pivot_reports

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BetaAnalyticsData server.
        """
        return request, metadata

    def post_batch_run_pivot_reports(
        self, response: analytics_data_api.BatchRunPivotReportsResponse
    ) -> analytics_data_api.BatchRunPivotReportsResponse:
        """Post-rpc interceptor for batch_run_pivot_reports

        Override in a subclass to manipulate the response
        after it is returned by the BetaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_batch_run_reports(
        self,
        request: analytics_data_api.BatchRunReportsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_data_api.BatchRunReportsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_run_reports

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BetaAnalyticsData server.
        """
        return request, metadata

    def post_batch_run_reports(
        self, response: analytics_data_api.BatchRunReportsResponse
    ) -> analytics_data_api.BatchRunReportsResponse:
        """Post-rpc interceptor for batch_run_reports

        Override in a subclass to manipulate the response
        after it is returned by the BetaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_check_compatibility(
        self,
        request: analytics_data_api.CheckCompatibilityRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_data_api.CheckCompatibilityRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for check_compatibility

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BetaAnalyticsData server.
        """
        return request, metadata

    def post_check_compatibility(
        self, response: analytics_data_api.CheckCompatibilityResponse
    ) -> analytics_data_api.CheckCompatibilityResponse:
        """Post-rpc interceptor for check_compatibility

        Override in a subclass to manipulate the response
        after it is returned by the BetaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_create_audience_export(
        self,
        request: analytics_data_api.CreateAudienceExportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_data_api.CreateAudienceExportRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_audience_export

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BetaAnalyticsData server.
        """
        return request, metadata

    def post_create_audience_export(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_audience_export

        Override in a subclass to manipulate the response
        after it is returned by the BetaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_get_audience_export(
        self,
        request: analytics_data_api.GetAudienceExportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_data_api.GetAudienceExportRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_audience_export

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BetaAnalyticsData server.
        """
        return request, metadata

    def post_get_audience_export(
        self, response: analytics_data_api.AudienceExport
    ) -> analytics_data_api.AudienceExport:
        """Post-rpc interceptor for get_audience_export

        Override in a subclass to manipulate the response
        after it is returned by the BetaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_get_metadata(
        self,
        request: analytics_data_api.GetMetadataRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_data_api.GetMetadataRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_metadata

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BetaAnalyticsData server.
        """
        return request, metadata

    def post_get_metadata(
        self, response: analytics_data_api.Metadata
    ) -> analytics_data_api.Metadata:
        """Post-rpc interceptor for get_metadata

        Override in a subclass to manipulate the response
        after it is returned by the BetaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_list_audience_exports(
        self,
        request: analytics_data_api.ListAudienceExportsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_data_api.ListAudienceExportsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_audience_exports

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BetaAnalyticsData server.
        """
        return request, metadata

    def post_list_audience_exports(
        self, response: analytics_data_api.ListAudienceExportsResponse
    ) -> analytics_data_api.ListAudienceExportsResponse:
        """Post-rpc interceptor for list_audience_exports

        Override in a subclass to manipulate the response
        after it is returned by the BetaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_query_audience_export(
        self,
        request: analytics_data_api.QueryAudienceExportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_data_api.QueryAudienceExportRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for query_audience_export

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BetaAnalyticsData server.
        """
        return request, metadata

    def post_query_audience_export(
        self, response: analytics_data_api.QueryAudienceExportResponse
    ) -> analytics_data_api.QueryAudienceExportResponse:
        """Post-rpc interceptor for query_audience_export

        Override in a subclass to manipulate the response
        after it is returned by the BetaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_run_pivot_report(
        self,
        request: analytics_data_api.RunPivotReportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_data_api.RunPivotReportRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for run_pivot_report

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BetaAnalyticsData server.
        """
        return request, metadata

    def post_run_pivot_report(
        self, response: analytics_data_api.RunPivotReportResponse
    ) -> analytics_data_api.RunPivotReportResponse:
        """Post-rpc interceptor for run_pivot_report

        Override in a subclass to manipulate the response
        after it is returned by the BetaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_run_realtime_report(
        self,
        request: analytics_data_api.RunRealtimeReportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_data_api.RunRealtimeReportRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for run_realtime_report

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BetaAnalyticsData server.
        """
        return request, metadata

    def post_run_realtime_report(
        self, response: analytics_data_api.RunRealtimeReportResponse
    ) -> analytics_data_api.RunRealtimeReportResponse:
        """Post-rpc interceptor for run_realtime_report

        Override in a subclass to manipulate the response
        after it is returned by the BetaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_run_report(
        self,
        request: analytics_data_api.RunReportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_data_api.RunReportRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for run_report

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BetaAnalyticsData server.
        """
        return request, metadata

    def post_run_report(
        self, response: analytics_data_api.RunReportResponse
    ) -> analytics_data_api.RunReportResponse:
        """Post-rpc interceptor for run_report

        Override in a subclass to manipulate the response
        after it is returned by the BetaAnalyticsData server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class BetaAnalyticsDataRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: BetaAnalyticsDataRestInterceptor


class BetaAnalyticsDataRestTransport(_BaseBetaAnalyticsDataRestTransport):
    """REST backend synchronous transport for BetaAnalyticsData.

    Google Analytics reporting data service.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "analyticsdata.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[BetaAnalyticsDataRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'analyticsdata.googleapis.com').
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
        self._interceptor = interceptor or BetaAnalyticsDataRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {}

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

    class _BatchRunPivotReports(
        _BaseBetaAnalyticsDataRestTransport._BaseBatchRunPivotReports,
        BetaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("BetaAnalyticsDataRestTransport.BatchRunPivotReports")

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
            request: analytics_data_api.BatchRunPivotReportsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.BatchRunPivotReportsResponse:
            r"""Call the batch run pivot reports method over HTTP.

            Args:
                request (~.analytics_data_api.BatchRunPivotReportsRequest):
                    The request object. The batch request containing multiple
                pivot report requests.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_data_api.BatchRunPivotReportsResponse:
                    The batch response containing
                multiple pivot reports.

            """

            http_options = (
                _BaseBetaAnalyticsDataRestTransport._BaseBatchRunPivotReports._get_http_options()
            )
            request, metadata = self._interceptor.pre_batch_run_pivot_reports(
                request, metadata
            )
            transcoded_request = _BaseBetaAnalyticsDataRestTransport._BaseBatchRunPivotReports._get_transcoded_request(
                http_options, request
            )

            body = _BaseBetaAnalyticsDataRestTransport._BaseBatchRunPivotReports._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBetaAnalyticsDataRestTransport._BaseBatchRunPivotReports._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                BetaAnalyticsDataRestTransport._BatchRunPivotReports._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = analytics_data_api.BatchRunPivotReportsResponse()
            pb_resp = analytics_data_api.BatchRunPivotReportsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_run_pivot_reports(resp)
            return resp

    class _BatchRunReports(
        _BaseBetaAnalyticsDataRestTransport._BaseBatchRunReports,
        BetaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("BetaAnalyticsDataRestTransport.BatchRunReports")

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
            request: analytics_data_api.BatchRunReportsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.BatchRunReportsResponse:
            r"""Call the batch run reports method over HTTP.

            Args:
                request (~.analytics_data_api.BatchRunReportsRequest):
                    The request object. The batch request containing multiple
                report requests.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_data_api.BatchRunReportsResponse:
                    The batch response containing
                multiple reports.

            """

            http_options = (
                _BaseBetaAnalyticsDataRestTransport._BaseBatchRunReports._get_http_options()
            )
            request, metadata = self._interceptor.pre_batch_run_reports(
                request, metadata
            )
            transcoded_request = _BaseBetaAnalyticsDataRestTransport._BaseBatchRunReports._get_transcoded_request(
                http_options, request
            )

            body = _BaseBetaAnalyticsDataRestTransport._BaseBatchRunReports._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBetaAnalyticsDataRestTransport._BaseBatchRunReports._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BetaAnalyticsDataRestTransport._BatchRunReports._get_response(
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
            resp = analytics_data_api.BatchRunReportsResponse()
            pb_resp = analytics_data_api.BatchRunReportsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_run_reports(resp)
            return resp

    class _CheckCompatibility(
        _BaseBetaAnalyticsDataRestTransport._BaseCheckCompatibility,
        BetaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("BetaAnalyticsDataRestTransport.CheckCompatibility")

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
            request: analytics_data_api.CheckCompatibilityRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.CheckCompatibilityResponse:
            r"""Call the check compatibility method over HTTP.

            Args:
                request (~.analytics_data_api.CheckCompatibilityRequest):
                    The request object. The request for compatibility information for a report's
                dimensions and metrics. Check compatibility provides a
                preview of the compatibility of a report; fields shared
                with the ``runReport`` request should be the same values
                as in your ``runReport`` request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_data_api.CheckCompatibilityResponse:
                    The compatibility response with the
                compatibility of each dimension &
                metric.

            """

            http_options = (
                _BaseBetaAnalyticsDataRestTransport._BaseCheckCompatibility._get_http_options()
            )
            request, metadata = self._interceptor.pre_check_compatibility(
                request, metadata
            )
            transcoded_request = _BaseBetaAnalyticsDataRestTransport._BaseCheckCompatibility._get_transcoded_request(
                http_options, request
            )

            body = _BaseBetaAnalyticsDataRestTransport._BaseCheckCompatibility._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBetaAnalyticsDataRestTransport._BaseCheckCompatibility._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BetaAnalyticsDataRestTransport._CheckCompatibility._get_response(
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
            resp = analytics_data_api.CheckCompatibilityResponse()
            pb_resp = analytics_data_api.CheckCompatibilityResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_check_compatibility(resp)
            return resp

    class _CreateAudienceExport(
        _BaseBetaAnalyticsDataRestTransport._BaseCreateAudienceExport,
        BetaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("BetaAnalyticsDataRestTransport.CreateAudienceExport")

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
            request: analytics_data_api.CreateAudienceExportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create audience export method over HTTP.

            Args:
                request (~.analytics_data_api.CreateAudienceExportRequest):
                    The request object. A request to create a new audience
                export.
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
                _BaseBetaAnalyticsDataRestTransport._BaseCreateAudienceExport._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_audience_export(
                request, metadata
            )
            transcoded_request = _BaseBetaAnalyticsDataRestTransport._BaseCreateAudienceExport._get_transcoded_request(
                http_options, request
            )

            body = _BaseBetaAnalyticsDataRestTransport._BaseCreateAudienceExport._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBetaAnalyticsDataRestTransport._BaseCreateAudienceExport._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                BetaAnalyticsDataRestTransport._CreateAudienceExport._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_audience_export(resp)
            return resp

    class _GetAudienceExport(
        _BaseBetaAnalyticsDataRestTransport._BaseGetAudienceExport,
        BetaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("BetaAnalyticsDataRestTransport.GetAudienceExport")

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
            request: analytics_data_api.GetAudienceExportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.AudienceExport:
            r"""Call the get audience export method over HTTP.

            Args:
                request (~.analytics_data_api.GetAudienceExportRequest):
                    The request object. A request to retrieve configuration
                metadata about a specific audience
                export.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_data_api.AudienceExport:
                    An audience export is a list of users
                in an audience at the time of the list's
                creation. One audience may have multiple
                audience exports created for different
                days.

            """

            http_options = (
                _BaseBetaAnalyticsDataRestTransport._BaseGetAudienceExport._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_audience_export(
                request, metadata
            )
            transcoded_request = _BaseBetaAnalyticsDataRestTransport._BaseGetAudienceExport._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBetaAnalyticsDataRestTransport._BaseGetAudienceExport._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BetaAnalyticsDataRestTransport._GetAudienceExport._get_response(
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
            resp = analytics_data_api.AudienceExport()
            pb_resp = analytics_data_api.AudienceExport.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_audience_export(resp)
            return resp

    class _GetMetadata(
        _BaseBetaAnalyticsDataRestTransport._BaseGetMetadata, BetaAnalyticsDataRestStub
    ):
        def __hash__(self):
            return hash("BetaAnalyticsDataRestTransport.GetMetadata")

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
            request: analytics_data_api.GetMetadataRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.Metadata:
            r"""Call the get metadata method over HTTP.

            Args:
                request (~.analytics_data_api.GetMetadataRequest):
                    The request object. Request for a property's dimension
                and metric metadata.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_data_api.Metadata:
                    The dimensions, metrics and
                comparisons currently accepted in
                reporting methods.

            """

            http_options = (
                _BaseBetaAnalyticsDataRestTransport._BaseGetMetadata._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_metadata(request, metadata)
            transcoded_request = _BaseBetaAnalyticsDataRestTransport._BaseGetMetadata._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBetaAnalyticsDataRestTransport._BaseGetMetadata._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BetaAnalyticsDataRestTransport._GetMetadata._get_response(
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
            resp = analytics_data_api.Metadata()
            pb_resp = analytics_data_api.Metadata.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_metadata(resp)
            return resp

    class _ListAudienceExports(
        _BaseBetaAnalyticsDataRestTransport._BaseListAudienceExports,
        BetaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("BetaAnalyticsDataRestTransport.ListAudienceExports")

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
            request: analytics_data_api.ListAudienceExportsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.ListAudienceExportsResponse:
            r"""Call the list audience exports method over HTTP.

            Args:
                request (~.analytics_data_api.ListAudienceExportsRequest):
                    The request object. A request to list all audience
                exports for a property.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_data_api.ListAudienceExportsResponse:
                    A list of all audience exports for a
                property.

            """

            http_options = (
                _BaseBetaAnalyticsDataRestTransport._BaseListAudienceExports._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_audience_exports(
                request, metadata
            )
            transcoded_request = _BaseBetaAnalyticsDataRestTransport._BaseListAudienceExports._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBetaAnalyticsDataRestTransport._BaseListAudienceExports._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                BetaAnalyticsDataRestTransport._ListAudienceExports._get_response(
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
            resp = analytics_data_api.ListAudienceExportsResponse()
            pb_resp = analytics_data_api.ListAudienceExportsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_audience_exports(resp)
            return resp

    class _QueryAudienceExport(
        _BaseBetaAnalyticsDataRestTransport._BaseQueryAudienceExport,
        BetaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("BetaAnalyticsDataRestTransport.QueryAudienceExport")

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
            request: analytics_data_api.QueryAudienceExportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.QueryAudienceExportResponse:
            r"""Call the query audience export method over HTTP.

            Args:
                request (~.analytics_data_api.QueryAudienceExportRequest):
                    The request object. A request to list users in an
                audience export.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_data_api.QueryAudienceExportResponse:
                    A list of users in an audience
                export.

            """

            http_options = (
                _BaseBetaAnalyticsDataRestTransport._BaseQueryAudienceExport._get_http_options()
            )
            request, metadata = self._interceptor.pre_query_audience_export(
                request, metadata
            )
            transcoded_request = _BaseBetaAnalyticsDataRestTransport._BaseQueryAudienceExport._get_transcoded_request(
                http_options, request
            )

            body = _BaseBetaAnalyticsDataRestTransport._BaseQueryAudienceExport._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBetaAnalyticsDataRestTransport._BaseQueryAudienceExport._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                BetaAnalyticsDataRestTransport._QueryAudienceExport._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = analytics_data_api.QueryAudienceExportResponse()
            pb_resp = analytics_data_api.QueryAudienceExportResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_query_audience_export(resp)
            return resp

    class _RunPivotReport(
        _BaseBetaAnalyticsDataRestTransport._BaseRunPivotReport,
        BetaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("BetaAnalyticsDataRestTransport.RunPivotReport")

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
            request: analytics_data_api.RunPivotReportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.RunPivotReportResponse:
            r"""Call the run pivot report method over HTTP.

            Args:
                request (~.analytics_data_api.RunPivotReportRequest):
                    The request object. The request to generate a pivot
                report.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_data_api.RunPivotReportResponse:
                    The response pivot report table
                corresponding to a pivot request.

            """

            http_options = (
                _BaseBetaAnalyticsDataRestTransport._BaseRunPivotReport._get_http_options()
            )
            request, metadata = self._interceptor.pre_run_pivot_report(
                request, metadata
            )
            transcoded_request = _BaseBetaAnalyticsDataRestTransport._BaseRunPivotReport._get_transcoded_request(
                http_options, request
            )

            body = _BaseBetaAnalyticsDataRestTransport._BaseRunPivotReport._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBetaAnalyticsDataRestTransport._BaseRunPivotReport._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BetaAnalyticsDataRestTransport._RunPivotReport._get_response(
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
            resp = analytics_data_api.RunPivotReportResponse()
            pb_resp = analytics_data_api.RunPivotReportResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_run_pivot_report(resp)
            return resp

    class _RunRealtimeReport(
        _BaseBetaAnalyticsDataRestTransport._BaseRunRealtimeReport,
        BetaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("BetaAnalyticsDataRestTransport.RunRealtimeReport")

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
            request: analytics_data_api.RunRealtimeReportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.RunRealtimeReportResponse:
            r"""Call the run realtime report method over HTTP.

            Args:
                request (~.analytics_data_api.RunRealtimeReportRequest):
                    The request object. The request to generate a realtime
                report.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_data_api.RunRealtimeReportResponse:
                    The response realtime report table
                corresponding to a request.

            """

            http_options = (
                _BaseBetaAnalyticsDataRestTransport._BaseRunRealtimeReport._get_http_options()
            )
            request, metadata = self._interceptor.pre_run_realtime_report(
                request, metadata
            )
            transcoded_request = _BaseBetaAnalyticsDataRestTransport._BaseRunRealtimeReport._get_transcoded_request(
                http_options, request
            )

            body = _BaseBetaAnalyticsDataRestTransport._BaseRunRealtimeReport._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBetaAnalyticsDataRestTransport._BaseRunRealtimeReport._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BetaAnalyticsDataRestTransport._RunRealtimeReport._get_response(
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
            resp = analytics_data_api.RunRealtimeReportResponse()
            pb_resp = analytics_data_api.RunRealtimeReportResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_run_realtime_report(resp)
            return resp

    class _RunReport(
        _BaseBetaAnalyticsDataRestTransport._BaseRunReport, BetaAnalyticsDataRestStub
    ):
        def __hash__(self):
            return hash("BetaAnalyticsDataRestTransport.RunReport")

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
            request: analytics_data_api.RunReportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.RunReportResponse:
            r"""Call the run report method over HTTP.

            Args:
                request (~.analytics_data_api.RunReportRequest):
                    The request object. The request to generate a report.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_data_api.RunReportResponse:
                    The response report table
                corresponding to a request.

            """

            http_options = (
                _BaseBetaAnalyticsDataRestTransport._BaseRunReport._get_http_options()
            )
            request, metadata = self._interceptor.pre_run_report(request, metadata)
            transcoded_request = _BaseBetaAnalyticsDataRestTransport._BaseRunReport._get_transcoded_request(
                http_options, request
            )

            body = _BaseBetaAnalyticsDataRestTransport._BaseRunReport._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBetaAnalyticsDataRestTransport._BaseRunReport._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BetaAnalyticsDataRestTransport._RunReport._get_response(
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
            resp = analytics_data_api.RunReportResponse()
            pb_resp = analytics_data_api.RunReportResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_run_report(resp)
            return resp

    @property
    def batch_run_pivot_reports(
        self,
    ) -> Callable[
        [analytics_data_api.BatchRunPivotReportsRequest],
        analytics_data_api.BatchRunPivotReportsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchRunPivotReports(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_run_reports(
        self,
    ) -> Callable[
        [analytics_data_api.BatchRunReportsRequest],
        analytics_data_api.BatchRunReportsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchRunReports(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def check_compatibility(
        self,
    ) -> Callable[
        [analytics_data_api.CheckCompatibilityRequest],
        analytics_data_api.CheckCompatibilityResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CheckCompatibility(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_audience_export(
        self,
    ) -> Callable[
        [analytics_data_api.CreateAudienceExportRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAudienceExport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_audience_export(
        self,
    ) -> Callable[
        [analytics_data_api.GetAudienceExportRequest], analytics_data_api.AudienceExport
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAudienceExport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_metadata(
        self,
    ) -> Callable[[analytics_data_api.GetMetadataRequest], analytics_data_api.Metadata]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetMetadata(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_audience_exports(
        self,
    ) -> Callable[
        [analytics_data_api.ListAudienceExportsRequest],
        analytics_data_api.ListAudienceExportsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAudienceExports(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def query_audience_export(
        self,
    ) -> Callable[
        [analytics_data_api.QueryAudienceExportRequest],
        analytics_data_api.QueryAudienceExportResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._QueryAudienceExport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def run_pivot_report(
        self,
    ) -> Callable[
        [analytics_data_api.RunPivotReportRequest],
        analytics_data_api.RunPivotReportResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RunPivotReport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def run_realtime_report(
        self,
    ) -> Callable[
        [analytics_data_api.RunRealtimeReportRequest],
        analytics_data_api.RunRealtimeReportResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RunRealtimeReport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def run_report(
        self,
    ) -> Callable[
        [analytics_data_api.RunReportRequest], analytics_data_api.RunReportResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RunReport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("BetaAnalyticsDataRestTransport",)
