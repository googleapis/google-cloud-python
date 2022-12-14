# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
import re
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, path_template, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.analytics.data_v1beta.types import analytics_data_api

from .base import BetaAnalyticsDataTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
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

            def pre_get_metadata(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_metadata(self, response):
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


class BetaAnalyticsDataRestTransport(BetaAnalyticsDataTransport):
    """REST backend transport for BetaAnalyticsData.

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
                 The hostname to connect to.
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
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or BetaAnalyticsDataRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _BatchRunPivotReports(BetaAnalyticsDataRestStub):
        def __hash__(self):
            return hash("BatchRunPivotReports")

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{property=properties/*}:batchRunPivotReports",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_batch_run_pivot_reports(
                request, metadata
            )
            pb_request = analytics_data_api.BatchRunPivotReportsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
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

    class _BatchRunReports(BetaAnalyticsDataRestStub):
        def __hash__(self):
            return hash("BatchRunReports")

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{property=properties/*}:batchRunReports",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_batch_run_reports(
                request, metadata
            )
            pb_request = analytics_data_api.BatchRunReportsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
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

    class _CheckCompatibility(BetaAnalyticsDataRestStub):
        def __hash__(self):
            return hash("CheckCompatibility")

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{property=properties/*}:checkCompatibility",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_check_compatibility(
                request, metadata
            )
            pb_request = analytics_data_api.CheckCompatibilityRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
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

    class _GetMetadata(BetaAnalyticsDataRestStub):
        def __hash__(self):
            return hash("GetMetadata")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

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
                    The dimensions and metrics currently
                accepted in reporting methods.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{name=properties/*/metadata}",
                },
            ]
            request, metadata = self._interceptor.pre_get_metadata(request, metadata)
            pb_request = analytics_data_api.GetMetadataRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
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

    class _RunPivotReport(BetaAnalyticsDataRestStub):
        def __hash__(self):
            return hash("RunPivotReport")

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{property=properties/*}:runPivotReport",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_run_pivot_report(
                request, metadata
            )
            pb_request = analytics_data_api.RunPivotReportRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
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

    class _RunRealtimeReport(BetaAnalyticsDataRestStub):
        def __hash__(self):
            return hash("RunRealtimeReport")

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{property=properties/*}:runRealtimeReport",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_run_realtime_report(
                request, metadata
            )
            pb_request = analytics_data_api.RunRealtimeReportRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
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

    class _RunReport(BetaAnalyticsDataRestStub):
        def __hash__(self):
            return hash("RunReport")

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{property=properties/*}:runReport",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_run_report(request, metadata)
            pb_request = analytics_data_api.RunReportRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
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
    def get_metadata(
        self,
    ) -> Callable[[analytics_data_api.GetMetadataRequest], analytics_data_api.Metadata]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetMetadata(self._session, self._host, self._interceptor)  # type: ignore

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
