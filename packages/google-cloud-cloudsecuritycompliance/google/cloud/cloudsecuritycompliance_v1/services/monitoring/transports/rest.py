# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
import google.protobuf
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.cloudsecuritycompliance_v1.types import monitoring

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseMonitoringRestTransport

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

if hasattr(DEFAULT_CLIENT_INFO, "protobuf_runtime_version"):  # pragma: NO COVER
    DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__


class MonitoringRestInterceptor:
    """Interceptor for Monitoring.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the MonitoringRestTransport.

    .. code-block:: python
        class MyCustomMonitoringInterceptor(MonitoringRestInterceptor):
            def pre_aggregate_framework_compliance_report(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_aggregate_framework_compliance_report(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_framework_compliance_report(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_framework_compliance_report(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_control_compliance_summaries(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_control_compliance_summaries(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_finding_summaries(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_finding_summaries(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_framework_compliance_summaries(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_framework_compliance_summaries(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = MonitoringRestTransport(interceptor=MyCustomMonitoringInterceptor())
        client = MonitoringClient(transport=transport)


    """

    def pre_aggregate_framework_compliance_report(
        self,
        request: monitoring.AggregateFrameworkComplianceReportRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        monitoring.AggregateFrameworkComplianceReportRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for aggregate_framework_compliance_report

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Monitoring server.
        """
        return request, metadata

    def post_aggregate_framework_compliance_report(
        self, response: monitoring.AggregateFrameworkComplianceReportResponse
    ) -> monitoring.AggregateFrameworkComplianceReportResponse:
        """Post-rpc interceptor for aggregate_framework_compliance_report

        DEPRECATED. Please use the `post_aggregate_framework_compliance_report_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Monitoring server but before
        it is returned to user code. This `post_aggregate_framework_compliance_report` interceptor runs
        before the `post_aggregate_framework_compliance_report_with_metadata` interceptor.
        """
        return response

    def post_aggregate_framework_compliance_report_with_metadata(
        self,
        response: monitoring.AggregateFrameworkComplianceReportResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        monitoring.AggregateFrameworkComplianceReportResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for aggregate_framework_compliance_report

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Monitoring server but before it is returned to user code.

        We recommend only using this `post_aggregate_framework_compliance_report_with_metadata`
        interceptor in new development instead of the `post_aggregate_framework_compliance_report` interceptor.
        When both interceptors are used, this `post_aggregate_framework_compliance_report_with_metadata` interceptor runs after the
        `post_aggregate_framework_compliance_report` interceptor. The (possibly modified) response returned by
        `post_aggregate_framework_compliance_report` will be passed to
        `post_aggregate_framework_compliance_report_with_metadata`.
        """
        return response, metadata

    def pre_fetch_framework_compliance_report(
        self,
        request: monitoring.FetchFrameworkComplianceReportRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        monitoring.FetchFrameworkComplianceReportRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for fetch_framework_compliance_report

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Monitoring server.
        """
        return request, metadata

    def post_fetch_framework_compliance_report(
        self, response: monitoring.FrameworkComplianceReport
    ) -> monitoring.FrameworkComplianceReport:
        """Post-rpc interceptor for fetch_framework_compliance_report

        DEPRECATED. Please use the `post_fetch_framework_compliance_report_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Monitoring server but before
        it is returned to user code. This `post_fetch_framework_compliance_report` interceptor runs
        before the `post_fetch_framework_compliance_report_with_metadata` interceptor.
        """
        return response

    def post_fetch_framework_compliance_report_with_metadata(
        self,
        response: monitoring.FrameworkComplianceReport,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        monitoring.FrameworkComplianceReport, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for fetch_framework_compliance_report

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Monitoring server but before it is returned to user code.

        We recommend only using this `post_fetch_framework_compliance_report_with_metadata`
        interceptor in new development instead of the `post_fetch_framework_compliance_report` interceptor.
        When both interceptors are used, this `post_fetch_framework_compliance_report_with_metadata` interceptor runs after the
        `post_fetch_framework_compliance_report` interceptor. The (possibly modified) response returned by
        `post_fetch_framework_compliance_report` will be passed to
        `post_fetch_framework_compliance_report_with_metadata`.
        """
        return response, metadata

    def pre_list_control_compliance_summaries(
        self,
        request: monitoring.ListControlComplianceSummariesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        monitoring.ListControlComplianceSummariesRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_control_compliance_summaries

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Monitoring server.
        """
        return request, metadata

    def post_list_control_compliance_summaries(
        self, response: monitoring.ListControlComplianceSummariesResponse
    ) -> monitoring.ListControlComplianceSummariesResponse:
        """Post-rpc interceptor for list_control_compliance_summaries

        DEPRECATED. Please use the `post_list_control_compliance_summaries_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Monitoring server but before
        it is returned to user code. This `post_list_control_compliance_summaries` interceptor runs
        before the `post_list_control_compliance_summaries_with_metadata` interceptor.
        """
        return response

    def post_list_control_compliance_summaries_with_metadata(
        self,
        response: monitoring.ListControlComplianceSummariesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        monitoring.ListControlComplianceSummariesResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_control_compliance_summaries

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Monitoring server but before it is returned to user code.

        We recommend only using this `post_list_control_compliance_summaries_with_metadata`
        interceptor in new development instead of the `post_list_control_compliance_summaries` interceptor.
        When both interceptors are used, this `post_list_control_compliance_summaries_with_metadata` interceptor runs after the
        `post_list_control_compliance_summaries` interceptor. The (possibly modified) response returned by
        `post_list_control_compliance_summaries` will be passed to
        `post_list_control_compliance_summaries_with_metadata`.
        """
        return response, metadata

    def pre_list_finding_summaries(
        self,
        request: monitoring.ListFindingSummariesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        monitoring.ListFindingSummariesRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_finding_summaries

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Monitoring server.
        """
        return request, metadata

    def post_list_finding_summaries(
        self, response: monitoring.ListFindingSummariesResponse
    ) -> monitoring.ListFindingSummariesResponse:
        """Post-rpc interceptor for list_finding_summaries

        DEPRECATED. Please use the `post_list_finding_summaries_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Monitoring server but before
        it is returned to user code. This `post_list_finding_summaries` interceptor runs
        before the `post_list_finding_summaries_with_metadata` interceptor.
        """
        return response

    def post_list_finding_summaries_with_metadata(
        self,
        response: monitoring.ListFindingSummariesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        monitoring.ListFindingSummariesResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_finding_summaries

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Monitoring server but before it is returned to user code.

        We recommend only using this `post_list_finding_summaries_with_metadata`
        interceptor in new development instead of the `post_list_finding_summaries` interceptor.
        When both interceptors are used, this `post_list_finding_summaries_with_metadata` interceptor runs after the
        `post_list_finding_summaries` interceptor. The (possibly modified) response returned by
        `post_list_finding_summaries` will be passed to
        `post_list_finding_summaries_with_metadata`.
        """
        return response, metadata

    def pre_list_framework_compliance_summaries(
        self,
        request: monitoring.ListFrameworkComplianceSummariesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        monitoring.ListFrameworkComplianceSummariesRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_framework_compliance_summaries

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Monitoring server.
        """
        return request, metadata

    def post_list_framework_compliance_summaries(
        self, response: monitoring.ListFrameworkComplianceSummariesResponse
    ) -> monitoring.ListFrameworkComplianceSummariesResponse:
        """Post-rpc interceptor for list_framework_compliance_summaries

        DEPRECATED. Please use the `post_list_framework_compliance_summaries_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Monitoring server but before
        it is returned to user code. This `post_list_framework_compliance_summaries` interceptor runs
        before the `post_list_framework_compliance_summaries_with_metadata` interceptor.
        """
        return response

    def post_list_framework_compliance_summaries_with_metadata(
        self,
        response: monitoring.ListFrameworkComplianceSummariesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        monitoring.ListFrameworkComplianceSummariesResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_framework_compliance_summaries

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Monitoring server but before it is returned to user code.

        We recommend only using this `post_list_framework_compliance_summaries_with_metadata`
        interceptor in new development instead of the `post_list_framework_compliance_summaries` interceptor.
        When both interceptors are used, this `post_list_framework_compliance_summaries_with_metadata` interceptor runs after the
        `post_list_framework_compliance_summaries` interceptor. The (possibly modified) response returned by
        `post_list_framework_compliance_summaries` will be passed to
        `post_list_framework_compliance_summaries_with_metadata`.
        """
        return response, metadata

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.GetLocationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Monitoring server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the Monitoring server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.ListLocationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Monitoring server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the Monitoring server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.CancelOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Monitoring server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the Monitoring server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operation(
        self,
        request: operations_pb2.DeleteOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Monitoring server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the Monitoring server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.GetOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Monitoring server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Monitoring server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.ListOperationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Monitoring server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Monitoring server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class MonitoringRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: MonitoringRestInterceptor


class MonitoringRestTransport(_BaseMonitoringRestTransport):
    """REST backend synchronous transport for Monitoring.

    Service describing handlers for resources

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "cloudsecuritycompliance.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[MonitoringRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'cloudsecuritycompliance.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): Deprecated. A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided. This argument will be
                removed in the next major version of this library.
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
        self._interceptor = interceptor or MonitoringRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AggregateFrameworkComplianceReport(
        _BaseMonitoringRestTransport._BaseAggregateFrameworkComplianceReport,
        MonitoringRestStub,
    ):
        def __hash__(self):
            return hash("MonitoringRestTransport.AggregateFrameworkComplianceReport")

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
            request: monitoring.AggregateFrameworkComplianceReportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> monitoring.AggregateFrameworkComplianceReportResponse:
            r"""Call the aggregate framework
            compliance report method over HTTP.

                Args:
                    request (~.monitoring.AggregateFrameworkComplianceReportRequest):
                        The request object. The request message for
                    [AggregateFrameworkComplianceReport][].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.monitoring.AggregateFrameworkComplianceReportResponse:
                        The response message for
                    [AggregateFrameworkComplianceReport][].

            """

            http_options = (
                _BaseMonitoringRestTransport._BaseAggregateFrameworkComplianceReport._get_http_options()
            )

            (
                request,
                metadata,
            ) = self._interceptor.pre_aggregate_framework_compliance_report(
                request, metadata
            )
            transcoded_request = _BaseMonitoringRestTransport._BaseAggregateFrameworkComplianceReport._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMonitoringRestTransport._BaseAggregateFrameworkComplianceReport._get_query_params_json(
                transcoded_request
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.MonitoringClient.AggregateFrameworkComplianceReport",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Monitoring",
                        "rpcName": "AggregateFrameworkComplianceReport",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = MonitoringRestTransport._AggregateFrameworkComplianceReport._get_response(
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
            resp = monitoring.AggregateFrameworkComplianceReportResponse()
            pb_resp = monitoring.AggregateFrameworkComplianceReportResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_aggregate_framework_compliance_report(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            (
                resp,
                _,
            ) = self._interceptor.post_aggregate_framework_compliance_report_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        monitoring.AggregateFrameworkComplianceReportResponse.to_json(
                            response
                        )
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.cloudsecuritycompliance_v1.MonitoringClient.aggregate_framework_compliance_report",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Monitoring",
                        "rpcName": "AggregateFrameworkComplianceReport",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _FetchFrameworkComplianceReport(
        _BaseMonitoringRestTransport._BaseFetchFrameworkComplianceReport,
        MonitoringRestStub,
    ):
        def __hash__(self):
            return hash("MonitoringRestTransport.FetchFrameworkComplianceReport")

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
            request: monitoring.FetchFrameworkComplianceReportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> monitoring.FrameworkComplianceReport:
            r"""Call the fetch framework
            compliance report method over HTTP.

                Args:
                    request (~.monitoring.FetchFrameworkComplianceReportRequest):
                        The request object. The request message for
                    [FetchFrameworkComplianceReport][].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.monitoring.FrameworkComplianceReport:
                        The response message for
                    [GetFrameworkComplianceReport][].

            """

            http_options = (
                _BaseMonitoringRestTransport._BaseFetchFrameworkComplianceReport._get_http_options()
            )

            request, metadata = self._interceptor.pre_fetch_framework_compliance_report(
                request, metadata
            )
            transcoded_request = _BaseMonitoringRestTransport._BaseFetchFrameworkComplianceReport._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMonitoringRestTransport._BaseFetchFrameworkComplianceReport._get_query_params_json(
                transcoded_request
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.MonitoringClient.FetchFrameworkComplianceReport",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Monitoring",
                        "rpcName": "FetchFrameworkComplianceReport",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                MonitoringRestTransport._FetchFrameworkComplianceReport._get_response(
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
            resp = monitoring.FrameworkComplianceReport()
            pb_resp = monitoring.FrameworkComplianceReport.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_fetch_framework_compliance_report(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            (
                resp,
                _,
            ) = self._interceptor.post_fetch_framework_compliance_report_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = monitoring.FrameworkComplianceReport.to_json(
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
                    "Received response for google.cloud.cloudsecuritycompliance_v1.MonitoringClient.fetch_framework_compliance_report",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Monitoring",
                        "rpcName": "FetchFrameworkComplianceReport",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListControlComplianceSummaries(
        _BaseMonitoringRestTransport._BaseListControlComplianceSummaries,
        MonitoringRestStub,
    ):
        def __hash__(self):
            return hash("MonitoringRestTransport.ListControlComplianceSummaries")

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
            request: monitoring.ListControlComplianceSummariesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> monitoring.ListControlComplianceSummariesResponse:
            r"""Call the list control compliance
            summaries method over HTTP.

                Args:
                    request (~.monitoring.ListControlComplianceSummariesRequest):
                        The request object. The request message for
                    [ListControlComplianceSummaries][].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.monitoring.ListControlComplianceSummariesResponse:
                        The response message for
                    [ListControlComplianceSummaries][].

            """

            http_options = (
                _BaseMonitoringRestTransport._BaseListControlComplianceSummaries._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_control_compliance_summaries(
                request, metadata
            )
            transcoded_request = _BaseMonitoringRestTransport._BaseListControlComplianceSummaries._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMonitoringRestTransport._BaseListControlComplianceSummaries._get_query_params_json(
                transcoded_request
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.MonitoringClient.ListControlComplianceSummaries",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Monitoring",
                        "rpcName": "ListControlComplianceSummaries",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                MonitoringRestTransport._ListControlComplianceSummaries._get_response(
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
            resp = monitoring.ListControlComplianceSummariesResponse()
            pb_resp = monitoring.ListControlComplianceSummariesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_control_compliance_summaries(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            (
                resp,
                _,
            ) = self._interceptor.post_list_control_compliance_summaries_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        monitoring.ListControlComplianceSummariesResponse.to_json(
                            response
                        )
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.cloudsecuritycompliance_v1.MonitoringClient.list_control_compliance_summaries",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Monitoring",
                        "rpcName": "ListControlComplianceSummaries",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListFindingSummaries(
        _BaseMonitoringRestTransport._BaseListFindingSummaries, MonitoringRestStub
    ):
        def __hash__(self):
            return hash("MonitoringRestTransport.ListFindingSummaries")

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
            request: monitoring.ListFindingSummariesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> monitoring.ListFindingSummariesResponse:
            r"""Call the list finding summaries method over HTTP.

            Args:
                request (~.monitoring.ListFindingSummariesRequest):
                    The request object. The request message for [ListFindingSummaries][].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.monitoring.ListFindingSummariesResponse:
                    The response message for [ListFindingSummaries][].
            """

            http_options = (
                _BaseMonitoringRestTransport._BaseListFindingSummaries._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_finding_summaries(
                request, metadata
            )
            transcoded_request = _BaseMonitoringRestTransport._BaseListFindingSummaries._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMonitoringRestTransport._BaseListFindingSummaries._get_query_params_json(
                transcoded_request
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.MonitoringClient.ListFindingSummaries",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Monitoring",
                        "rpcName": "ListFindingSummaries",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = MonitoringRestTransport._ListFindingSummaries._get_response(
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
            resp = monitoring.ListFindingSummariesResponse()
            pb_resp = monitoring.ListFindingSummariesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_finding_summaries(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_finding_summaries_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = monitoring.ListFindingSummariesResponse.to_json(
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
                    "Received response for google.cloud.cloudsecuritycompliance_v1.MonitoringClient.list_finding_summaries",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Monitoring",
                        "rpcName": "ListFindingSummaries",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListFrameworkComplianceSummaries(
        _BaseMonitoringRestTransport._BaseListFrameworkComplianceSummaries,
        MonitoringRestStub,
    ):
        def __hash__(self):
            return hash("MonitoringRestTransport.ListFrameworkComplianceSummaries")

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
            request: monitoring.ListFrameworkComplianceSummariesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> monitoring.ListFrameworkComplianceSummariesResponse:
            r"""Call the list framework compliance
            summaries method over HTTP.

                Args:
                    request (~.monitoring.ListFrameworkComplianceSummariesRequest):
                        The request object. The request message for
                    [ListFrameworkComplianceSummariesRequest][google.cloud.cloudsecuritycompliance.v1.ListFrameworkComplianceSummariesRequest].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.monitoring.ListFrameworkComplianceSummariesResponse:
                        The response message for
                    [ListFrameworkComplianceSummariesResponse][google.cloud.cloudsecuritycompliance.v1.ListFrameworkComplianceSummariesResponse].

            """

            http_options = (
                _BaseMonitoringRestTransport._BaseListFrameworkComplianceSummaries._get_http_options()
            )

            (
                request,
                metadata,
            ) = self._interceptor.pre_list_framework_compliance_summaries(
                request, metadata
            )
            transcoded_request = _BaseMonitoringRestTransport._BaseListFrameworkComplianceSummaries._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMonitoringRestTransport._BaseListFrameworkComplianceSummaries._get_query_params_json(
                transcoded_request
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.MonitoringClient.ListFrameworkComplianceSummaries",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Monitoring",
                        "rpcName": "ListFrameworkComplianceSummaries",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                MonitoringRestTransport._ListFrameworkComplianceSummaries._get_response(
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
            resp = monitoring.ListFrameworkComplianceSummariesResponse()
            pb_resp = monitoring.ListFrameworkComplianceSummariesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_framework_compliance_summaries(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            (
                resp,
                _,
            ) = self._interceptor.post_list_framework_compliance_summaries_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        monitoring.ListFrameworkComplianceSummariesResponse.to_json(
                            response
                        )
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.cloudsecuritycompliance_v1.MonitoringClient.list_framework_compliance_summaries",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Monitoring",
                        "rpcName": "ListFrameworkComplianceSummaries",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def aggregate_framework_compliance_report(
        self,
    ) -> Callable[
        [monitoring.AggregateFrameworkComplianceReportRequest],
        monitoring.AggregateFrameworkComplianceReportResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AggregateFrameworkComplianceReport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_framework_compliance_report(
        self,
    ) -> Callable[
        [monitoring.FetchFrameworkComplianceReportRequest],
        monitoring.FrameworkComplianceReport,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchFrameworkComplianceReport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_control_compliance_summaries(
        self,
    ) -> Callable[
        [monitoring.ListControlComplianceSummariesRequest],
        monitoring.ListControlComplianceSummariesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListControlComplianceSummaries(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_finding_summaries(
        self,
    ) -> Callable[
        [monitoring.ListFindingSummariesRequest],
        monitoring.ListFindingSummariesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListFindingSummaries(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_framework_compliance_summaries(
        self,
    ) -> Callable[
        [monitoring.ListFrameworkComplianceSummariesRequest],
        monitoring.ListFrameworkComplianceSummariesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListFrameworkComplianceSummaries(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseMonitoringRestTransport._BaseGetLocation, MonitoringRestStub
    ):
        def __hash__(self):
            return hash("MonitoringRestTransport.GetLocation")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options = (
                _BaseMonitoringRestTransport._BaseGetLocation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = (
                _BaseMonitoringRestTransport._BaseGetLocation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseMonitoringRestTransport._BaseGetLocation._get_query_params_json(
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.MonitoringClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Monitoring",
                        "rpcName": "GetLocation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = MonitoringRestTransport._GetLocation._get_response(
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
                    "Received response for google.cloud.cloudsecuritycompliance_v1.MonitoringAsyncClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Monitoring",
                        "rpcName": "GetLocation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseMonitoringRestTransport._BaseListLocations, MonitoringRestStub
    ):
        def __hash__(self):
            return hash("MonitoringRestTransport.ListLocations")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options = (
                _BaseMonitoringRestTransport._BaseListLocations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = (
                _BaseMonitoringRestTransport._BaseListLocations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseMonitoringRestTransport._BaseListLocations._get_query_params_json(
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.MonitoringClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Monitoring",
                        "rpcName": "ListLocations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = MonitoringRestTransport._ListLocations._get_response(
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
                    "Received response for google.cloud.cloudsecuritycompliance_v1.MonitoringAsyncClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Monitoring",
                        "rpcName": "ListLocations",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseMonitoringRestTransport._BaseCancelOperation, MonitoringRestStub
    ):
        def __hash__(self):
            return hash("MonitoringRestTransport.CancelOperation")

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
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseMonitoringRestTransport._BaseCancelOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseMonitoringRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = _BaseMonitoringRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMonitoringRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.MonitoringClient.CancelOperation",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Monitoring",
                        "rpcName": "CancelOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = MonitoringRestTransport._CancelOperation._get_response(
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

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(
        _BaseMonitoringRestTransport._BaseDeleteOperation, MonitoringRestStub
    ):
        def __hash__(self):
            return hash("MonitoringRestTransport.DeleteOperation")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> None:
            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseMonitoringRestTransport._BaseDeleteOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BaseMonitoringRestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMonitoringRestTransport._BaseDeleteOperation._get_query_params_json(
                transcoded_request
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.MonitoringClient.DeleteOperation",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Monitoring",
                        "rpcName": "DeleteOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = MonitoringRestTransport._DeleteOperation._get_response(
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
        _BaseMonitoringRestTransport._BaseGetOperation, MonitoringRestStub
    ):
        def __hash__(self):
            return hash("MonitoringRestTransport.GetOperation")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options = (
                _BaseMonitoringRestTransport._BaseGetOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = (
                _BaseMonitoringRestTransport._BaseGetOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseMonitoringRestTransport._BaseGetOperation._get_query_params_json(
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.MonitoringClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Monitoring",
                        "rpcName": "GetOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = MonitoringRestTransport._GetOperation._get_response(
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
                    "Received response for google.cloud.cloudsecuritycompliance_v1.MonitoringAsyncClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Monitoring",
                        "rpcName": "GetOperation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseMonitoringRestTransport._BaseListOperations, MonitoringRestStub
    ):
        def __hash__(self):
            return hash("MonitoringRestTransport.ListOperations")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options = (
                _BaseMonitoringRestTransport._BaseListOperations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseMonitoringRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseMonitoringRestTransport._BaseListOperations._get_query_params_json(
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.MonitoringClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Monitoring",
                        "rpcName": "ListOperations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = MonitoringRestTransport._ListOperations._get_response(
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
                    "Received response for google.cloud.cloudsecuritycompliance_v1.MonitoringAsyncClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Monitoring",
                        "rpcName": "ListOperations",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("MonitoringRestTransport",)
