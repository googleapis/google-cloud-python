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

from google.analytics.data_v1alpha.types import analytics_data_api

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseAlphaAnalyticsDataRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class AlphaAnalyticsDataRestInterceptor:
    """Interceptor for AlphaAnalyticsData.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the AlphaAnalyticsDataRestTransport.

    .. code-block:: python
        class MyCustomAlphaAnalyticsDataInterceptor(AlphaAnalyticsDataRestInterceptor):
            def pre_create_audience_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_audience_list(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_recurring_audience_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_recurring_audience_list(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_report_task(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_report_task(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_audience_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_audience_list(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_property_quotas_snapshot(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_property_quotas_snapshot(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_recurring_audience_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_recurring_audience_list(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_report_task(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_report_task(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_audience_lists(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_audience_lists(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_recurring_audience_lists(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_recurring_audience_lists(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_report_tasks(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_report_tasks(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_query_audience_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_query_audience_list(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_query_report_task(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_query_report_task(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_run_funnel_report(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_run_funnel_report(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_sheet_export_audience_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_sheet_export_audience_list(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = AlphaAnalyticsDataRestTransport(interceptor=MyCustomAlphaAnalyticsDataInterceptor())
        client = AlphaAnalyticsDataClient(transport=transport)


    """

    def pre_create_audience_list(
        self,
        request: analytics_data_api.CreateAudienceListRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_data_api.CreateAudienceListRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_audience_list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AlphaAnalyticsData server.
        """
        return request, metadata

    def post_create_audience_list(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_audience_list

        Override in a subclass to manipulate the response
        after it is returned by the AlphaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_create_recurring_audience_list(
        self,
        request: analytics_data_api.CreateRecurringAudienceListRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_data_api.CreateRecurringAudienceListRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_recurring_audience_list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AlphaAnalyticsData server.
        """
        return request, metadata

    def post_create_recurring_audience_list(
        self, response: analytics_data_api.RecurringAudienceList
    ) -> analytics_data_api.RecurringAudienceList:
        """Post-rpc interceptor for create_recurring_audience_list

        Override in a subclass to manipulate the response
        after it is returned by the AlphaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_create_report_task(
        self,
        request: analytics_data_api.CreateReportTaskRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_data_api.CreateReportTaskRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_report_task

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AlphaAnalyticsData server.
        """
        return request, metadata

    def post_create_report_task(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_report_task

        Override in a subclass to manipulate the response
        after it is returned by the AlphaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_get_audience_list(
        self,
        request: analytics_data_api.GetAudienceListRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_data_api.GetAudienceListRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_audience_list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AlphaAnalyticsData server.
        """
        return request, metadata

    def post_get_audience_list(
        self, response: analytics_data_api.AudienceList
    ) -> analytics_data_api.AudienceList:
        """Post-rpc interceptor for get_audience_list

        Override in a subclass to manipulate the response
        after it is returned by the AlphaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_get_property_quotas_snapshot(
        self,
        request: analytics_data_api.GetPropertyQuotasSnapshotRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_data_api.GetPropertyQuotasSnapshotRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_property_quotas_snapshot

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AlphaAnalyticsData server.
        """
        return request, metadata

    def post_get_property_quotas_snapshot(
        self, response: analytics_data_api.PropertyQuotasSnapshot
    ) -> analytics_data_api.PropertyQuotasSnapshot:
        """Post-rpc interceptor for get_property_quotas_snapshot

        Override in a subclass to manipulate the response
        after it is returned by the AlphaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_get_recurring_audience_list(
        self,
        request: analytics_data_api.GetRecurringAudienceListRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_data_api.GetRecurringAudienceListRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_recurring_audience_list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AlphaAnalyticsData server.
        """
        return request, metadata

    def post_get_recurring_audience_list(
        self, response: analytics_data_api.RecurringAudienceList
    ) -> analytics_data_api.RecurringAudienceList:
        """Post-rpc interceptor for get_recurring_audience_list

        Override in a subclass to manipulate the response
        after it is returned by the AlphaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_get_report_task(
        self,
        request: analytics_data_api.GetReportTaskRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_data_api.GetReportTaskRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_report_task

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AlphaAnalyticsData server.
        """
        return request, metadata

    def post_get_report_task(
        self, response: analytics_data_api.ReportTask
    ) -> analytics_data_api.ReportTask:
        """Post-rpc interceptor for get_report_task

        Override in a subclass to manipulate the response
        after it is returned by the AlphaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_list_audience_lists(
        self,
        request: analytics_data_api.ListAudienceListsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_data_api.ListAudienceListsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_audience_lists

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AlphaAnalyticsData server.
        """
        return request, metadata

    def post_list_audience_lists(
        self, response: analytics_data_api.ListAudienceListsResponse
    ) -> analytics_data_api.ListAudienceListsResponse:
        """Post-rpc interceptor for list_audience_lists

        Override in a subclass to manipulate the response
        after it is returned by the AlphaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_list_recurring_audience_lists(
        self,
        request: analytics_data_api.ListRecurringAudienceListsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_data_api.ListRecurringAudienceListsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_recurring_audience_lists

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AlphaAnalyticsData server.
        """
        return request, metadata

    def post_list_recurring_audience_lists(
        self, response: analytics_data_api.ListRecurringAudienceListsResponse
    ) -> analytics_data_api.ListRecurringAudienceListsResponse:
        """Post-rpc interceptor for list_recurring_audience_lists

        Override in a subclass to manipulate the response
        after it is returned by the AlphaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_list_report_tasks(
        self,
        request: analytics_data_api.ListReportTasksRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_data_api.ListReportTasksRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_report_tasks

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AlphaAnalyticsData server.
        """
        return request, metadata

    def post_list_report_tasks(
        self, response: analytics_data_api.ListReportTasksResponse
    ) -> analytics_data_api.ListReportTasksResponse:
        """Post-rpc interceptor for list_report_tasks

        Override in a subclass to manipulate the response
        after it is returned by the AlphaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_query_audience_list(
        self,
        request: analytics_data_api.QueryAudienceListRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_data_api.QueryAudienceListRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for query_audience_list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AlphaAnalyticsData server.
        """
        return request, metadata

    def post_query_audience_list(
        self, response: analytics_data_api.QueryAudienceListResponse
    ) -> analytics_data_api.QueryAudienceListResponse:
        """Post-rpc interceptor for query_audience_list

        Override in a subclass to manipulate the response
        after it is returned by the AlphaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_query_report_task(
        self,
        request: analytics_data_api.QueryReportTaskRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_data_api.QueryReportTaskRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for query_report_task

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AlphaAnalyticsData server.
        """
        return request, metadata

    def post_query_report_task(
        self, response: analytics_data_api.QueryReportTaskResponse
    ) -> analytics_data_api.QueryReportTaskResponse:
        """Post-rpc interceptor for query_report_task

        Override in a subclass to manipulate the response
        after it is returned by the AlphaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_run_funnel_report(
        self,
        request: analytics_data_api.RunFunnelReportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_data_api.RunFunnelReportRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for run_funnel_report

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AlphaAnalyticsData server.
        """
        return request, metadata

    def post_run_funnel_report(
        self, response: analytics_data_api.RunFunnelReportResponse
    ) -> analytics_data_api.RunFunnelReportResponse:
        """Post-rpc interceptor for run_funnel_report

        Override in a subclass to manipulate the response
        after it is returned by the AlphaAnalyticsData server but before
        it is returned to user code.
        """
        return response

    def pre_sheet_export_audience_list(
        self,
        request: analytics_data_api.SheetExportAudienceListRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_data_api.SheetExportAudienceListRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for sheet_export_audience_list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AlphaAnalyticsData server.
        """
        return request, metadata

    def post_sheet_export_audience_list(
        self, response: analytics_data_api.SheetExportAudienceListResponse
    ) -> analytics_data_api.SheetExportAudienceListResponse:
        """Post-rpc interceptor for sheet_export_audience_list

        Override in a subclass to manipulate the response
        after it is returned by the AlphaAnalyticsData server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class AlphaAnalyticsDataRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: AlphaAnalyticsDataRestInterceptor


class AlphaAnalyticsDataRestTransport(_BaseAlphaAnalyticsDataRestTransport):
    """REST backend synchronous transport for AlphaAnalyticsData.

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
        interceptor: Optional[AlphaAnalyticsDataRestInterceptor] = None,
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
        self._interceptor = interceptor or AlphaAnalyticsDataRestInterceptor()
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
                path_prefix="v1alpha",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateAudienceList(
        _BaseAlphaAnalyticsDataRestTransport._BaseCreateAudienceList,
        AlphaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("AlphaAnalyticsDataRestTransport.CreateAudienceList")

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
            request: analytics_data_api.CreateAudienceListRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create audience list method over HTTP.

            Args:
                request (~.analytics_data_api.CreateAudienceListRequest):
                    The request object. A request to create a new audience
                list.
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
                _BaseAlphaAnalyticsDataRestTransport._BaseCreateAudienceList._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_audience_list(
                request, metadata
            )
            transcoded_request = _BaseAlphaAnalyticsDataRestTransport._BaseCreateAudienceList._get_transcoded_request(
                http_options, request
            )

            body = _BaseAlphaAnalyticsDataRestTransport._BaseCreateAudienceList._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAlphaAnalyticsDataRestTransport._BaseCreateAudienceList._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                AlphaAnalyticsDataRestTransport._CreateAudienceList._get_response(
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
            resp = self._interceptor.post_create_audience_list(resp)
            return resp

    class _CreateRecurringAudienceList(
        _BaseAlphaAnalyticsDataRestTransport._BaseCreateRecurringAudienceList,
        AlphaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("AlphaAnalyticsDataRestTransport.CreateRecurringAudienceList")

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
            request: analytics_data_api.CreateRecurringAudienceListRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.RecurringAudienceList:
            r"""Call the create recurring audience
            list method over HTTP.

                Args:
                    request (~.analytics_data_api.CreateRecurringAudienceListRequest):
                        The request object. A request to create a new recurring
                    audience list.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.analytics_data_api.RecurringAudienceList:
                        A recurring audience list produces
                    new audience lists each day. Audience
                    lists are users in an audience at the
                    time of the list's creation. A recurring
                    audience list ensures that you have
                    audience list based on the most recent
                    data available for use each day.

            """

            http_options = (
                _BaseAlphaAnalyticsDataRestTransport._BaseCreateRecurringAudienceList._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_recurring_audience_list(
                request, metadata
            )
            transcoded_request = _BaseAlphaAnalyticsDataRestTransport._BaseCreateRecurringAudienceList._get_transcoded_request(
                http_options, request
            )

            body = _BaseAlphaAnalyticsDataRestTransport._BaseCreateRecurringAudienceList._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAlphaAnalyticsDataRestTransport._BaseCreateRecurringAudienceList._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AlphaAnalyticsDataRestTransport._CreateRecurringAudienceList._get_response(
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
            resp = analytics_data_api.RecurringAudienceList()
            pb_resp = analytics_data_api.RecurringAudienceList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_recurring_audience_list(resp)
            return resp

    class _CreateReportTask(
        _BaseAlphaAnalyticsDataRestTransport._BaseCreateReportTask,
        AlphaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("AlphaAnalyticsDataRestTransport.CreateReportTask")

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
            request: analytics_data_api.CreateReportTaskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create report task method over HTTP.

            Args:
                request (~.analytics_data_api.CreateReportTaskRequest):
                    The request object. A request to create a report task.
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
                _BaseAlphaAnalyticsDataRestTransport._BaseCreateReportTask._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_report_task(
                request, metadata
            )
            transcoded_request = _BaseAlphaAnalyticsDataRestTransport._BaseCreateReportTask._get_transcoded_request(
                http_options, request
            )

            body = _BaseAlphaAnalyticsDataRestTransport._BaseCreateReportTask._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAlphaAnalyticsDataRestTransport._BaseCreateReportTask._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AlphaAnalyticsDataRestTransport._CreateReportTask._get_response(
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
            resp = self._interceptor.post_create_report_task(resp)
            return resp

    class _GetAudienceList(
        _BaseAlphaAnalyticsDataRestTransport._BaseGetAudienceList,
        AlphaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("AlphaAnalyticsDataRestTransport.GetAudienceList")

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
            request: analytics_data_api.GetAudienceListRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.AudienceList:
            r"""Call the get audience list method over HTTP.

            Args:
                request (~.analytics_data_api.GetAudienceListRequest):
                    The request object. A request to retrieve configuration
                metadata about a specific audience list.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_data_api.AudienceList:
                    An audience list is a list of users
                in an audience at the time of the list's
                creation. One audience may have multiple
                audience lists created for different
                days.

            """

            http_options = (
                _BaseAlphaAnalyticsDataRestTransport._BaseGetAudienceList._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_audience_list(
                request, metadata
            )
            transcoded_request = _BaseAlphaAnalyticsDataRestTransport._BaseGetAudienceList._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAlphaAnalyticsDataRestTransport._BaseGetAudienceList._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AlphaAnalyticsDataRestTransport._GetAudienceList._get_response(
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
            resp = analytics_data_api.AudienceList()
            pb_resp = analytics_data_api.AudienceList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_audience_list(resp)
            return resp

    class _GetPropertyQuotasSnapshot(
        _BaseAlphaAnalyticsDataRestTransport._BaseGetPropertyQuotasSnapshot,
        AlphaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("AlphaAnalyticsDataRestTransport.GetPropertyQuotasSnapshot")

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
            request: analytics_data_api.GetPropertyQuotasSnapshotRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.PropertyQuotasSnapshot:
            r"""Call the get property quotas
            snapshot method over HTTP.

                Args:
                    request (~.analytics_data_api.GetPropertyQuotasSnapshotRequest):
                        The request object. A request to return the
                    PropertyQuotasSnapshot for a given
                    category.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.analytics_data_api.PropertyQuotasSnapshot:
                        Current state of all Property Quotas
                    organized by quota category.

            """

            http_options = (
                _BaseAlphaAnalyticsDataRestTransport._BaseGetPropertyQuotasSnapshot._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_property_quotas_snapshot(
                request, metadata
            )
            transcoded_request = _BaseAlphaAnalyticsDataRestTransport._BaseGetPropertyQuotasSnapshot._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAlphaAnalyticsDataRestTransport._BaseGetPropertyQuotasSnapshot._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AlphaAnalyticsDataRestTransport._GetPropertyQuotasSnapshot._get_response(
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
            resp = analytics_data_api.PropertyQuotasSnapshot()
            pb_resp = analytics_data_api.PropertyQuotasSnapshot.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_property_quotas_snapshot(resp)
            return resp

    class _GetRecurringAudienceList(
        _BaseAlphaAnalyticsDataRestTransport._BaseGetRecurringAudienceList,
        AlphaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("AlphaAnalyticsDataRestTransport.GetRecurringAudienceList")

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
            request: analytics_data_api.GetRecurringAudienceListRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.RecurringAudienceList:
            r"""Call the get recurring audience
            list method over HTTP.

                Args:
                    request (~.analytics_data_api.GetRecurringAudienceListRequest):
                        The request object. A request to retrieve configuration
                    metadata about a specific recurring
                    audience list.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.analytics_data_api.RecurringAudienceList:
                        A recurring audience list produces
                    new audience lists each day. Audience
                    lists are users in an audience at the
                    time of the list's creation. A recurring
                    audience list ensures that you have
                    audience list based on the most recent
                    data available for use each day.

            """

            http_options = (
                _BaseAlphaAnalyticsDataRestTransport._BaseGetRecurringAudienceList._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_recurring_audience_list(
                request, metadata
            )
            transcoded_request = _BaseAlphaAnalyticsDataRestTransport._BaseGetRecurringAudienceList._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAlphaAnalyticsDataRestTransport._BaseGetRecurringAudienceList._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                AlphaAnalyticsDataRestTransport._GetRecurringAudienceList._get_response(
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
            resp = analytics_data_api.RecurringAudienceList()
            pb_resp = analytics_data_api.RecurringAudienceList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_recurring_audience_list(resp)
            return resp

    class _GetReportTask(
        _BaseAlphaAnalyticsDataRestTransport._BaseGetReportTask,
        AlphaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("AlphaAnalyticsDataRestTransport.GetReportTask")

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
            request: analytics_data_api.GetReportTaskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.ReportTask:
            r"""Call the get report task method over HTTP.

            Args:
                request (~.analytics_data_api.GetReportTaskRequest):
                    The request object. A request to retrieve configuration
                metadata about a specific report task.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_data_api.ReportTask:
                    A specific report task configuration.
            """

            http_options = (
                _BaseAlphaAnalyticsDataRestTransport._BaseGetReportTask._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_report_task(request, metadata)
            transcoded_request = _BaseAlphaAnalyticsDataRestTransport._BaseGetReportTask._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAlphaAnalyticsDataRestTransport._BaseGetReportTask._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AlphaAnalyticsDataRestTransport._GetReportTask._get_response(
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
            resp = analytics_data_api.ReportTask()
            pb_resp = analytics_data_api.ReportTask.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_report_task(resp)
            return resp

    class _ListAudienceLists(
        _BaseAlphaAnalyticsDataRestTransport._BaseListAudienceLists,
        AlphaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("AlphaAnalyticsDataRestTransport.ListAudienceLists")

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
            request: analytics_data_api.ListAudienceListsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.ListAudienceListsResponse:
            r"""Call the list audience lists method over HTTP.

            Args:
                request (~.analytics_data_api.ListAudienceListsRequest):
                    The request object. A request to list all audience lists
                for a property.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_data_api.ListAudienceListsResponse:
                    A list of all audience lists for a
                property.

            """

            http_options = (
                _BaseAlphaAnalyticsDataRestTransport._BaseListAudienceLists._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_audience_lists(
                request, metadata
            )
            transcoded_request = _BaseAlphaAnalyticsDataRestTransport._BaseListAudienceLists._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAlphaAnalyticsDataRestTransport._BaseListAudienceLists._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AlphaAnalyticsDataRestTransport._ListAudienceLists._get_response(
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
            resp = analytics_data_api.ListAudienceListsResponse()
            pb_resp = analytics_data_api.ListAudienceListsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_audience_lists(resp)
            return resp

    class _ListRecurringAudienceLists(
        _BaseAlphaAnalyticsDataRestTransport._BaseListRecurringAudienceLists,
        AlphaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("AlphaAnalyticsDataRestTransport.ListRecurringAudienceLists")

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
            request: analytics_data_api.ListRecurringAudienceListsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.ListRecurringAudienceListsResponse:
            r"""Call the list recurring audience
            lists method over HTTP.

                Args:
                    request (~.analytics_data_api.ListRecurringAudienceListsRequest):
                        The request object. A request to list all recurring
                    audience lists for a property.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.analytics_data_api.ListRecurringAudienceListsResponse:
                        A list of all recurring audience
                    lists for a property.

            """

            http_options = (
                _BaseAlphaAnalyticsDataRestTransport._BaseListRecurringAudienceLists._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_recurring_audience_lists(
                request, metadata
            )
            transcoded_request = _BaseAlphaAnalyticsDataRestTransport._BaseListRecurringAudienceLists._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAlphaAnalyticsDataRestTransport._BaseListRecurringAudienceLists._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AlphaAnalyticsDataRestTransport._ListRecurringAudienceLists._get_response(
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
            resp = analytics_data_api.ListRecurringAudienceListsResponse()
            pb_resp = analytics_data_api.ListRecurringAudienceListsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_recurring_audience_lists(resp)
            return resp

    class _ListReportTasks(
        _BaseAlphaAnalyticsDataRestTransport._BaseListReportTasks,
        AlphaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("AlphaAnalyticsDataRestTransport.ListReportTasks")

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
            request: analytics_data_api.ListReportTasksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.ListReportTasksResponse:
            r"""Call the list report tasks method over HTTP.

            Args:
                request (~.analytics_data_api.ListReportTasksRequest):
                    The request object. A request to list all report tasks
                for a property.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_data_api.ListReportTasksResponse:
                    A list of all report tasks for a
                property.

            """

            http_options = (
                _BaseAlphaAnalyticsDataRestTransport._BaseListReportTasks._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_report_tasks(
                request, metadata
            )
            transcoded_request = _BaseAlphaAnalyticsDataRestTransport._BaseListReportTasks._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAlphaAnalyticsDataRestTransport._BaseListReportTasks._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AlphaAnalyticsDataRestTransport._ListReportTasks._get_response(
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
            resp = analytics_data_api.ListReportTasksResponse()
            pb_resp = analytics_data_api.ListReportTasksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_report_tasks(resp)
            return resp

    class _QueryAudienceList(
        _BaseAlphaAnalyticsDataRestTransport._BaseQueryAudienceList,
        AlphaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("AlphaAnalyticsDataRestTransport.QueryAudienceList")

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
            request: analytics_data_api.QueryAudienceListRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.QueryAudienceListResponse:
            r"""Call the query audience list method over HTTP.

            Args:
                request (~.analytics_data_api.QueryAudienceListRequest):
                    The request object. A request to list users in an
                audience list.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_data_api.QueryAudienceListResponse:
                    A list of users in an audience list.
            """

            http_options = (
                _BaseAlphaAnalyticsDataRestTransport._BaseQueryAudienceList._get_http_options()
            )
            request, metadata = self._interceptor.pre_query_audience_list(
                request, metadata
            )
            transcoded_request = _BaseAlphaAnalyticsDataRestTransport._BaseQueryAudienceList._get_transcoded_request(
                http_options, request
            )

            body = _BaseAlphaAnalyticsDataRestTransport._BaseQueryAudienceList._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAlphaAnalyticsDataRestTransport._BaseQueryAudienceList._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AlphaAnalyticsDataRestTransport._QueryAudienceList._get_response(
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
            resp = analytics_data_api.QueryAudienceListResponse()
            pb_resp = analytics_data_api.QueryAudienceListResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_query_audience_list(resp)
            return resp

    class _QueryReportTask(
        _BaseAlphaAnalyticsDataRestTransport._BaseQueryReportTask,
        AlphaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("AlphaAnalyticsDataRestTransport.QueryReportTask")

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
            request: analytics_data_api.QueryReportTaskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.QueryReportTaskResponse:
            r"""Call the query report task method over HTTP.

            Args:
                request (~.analytics_data_api.QueryReportTaskRequest):
                    The request object. A request to fetch the report content
                for a report task.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_data_api.QueryReportTaskResponse:
                    The report content corresponding to a
                report task.

            """

            http_options = (
                _BaseAlphaAnalyticsDataRestTransport._BaseQueryReportTask._get_http_options()
            )
            request, metadata = self._interceptor.pre_query_report_task(
                request, metadata
            )
            transcoded_request = _BaseAlphaAnalyticsDataRestTransport._BaseQueryReportTask._get_transcoded_request(
                http_options, request
            )

            body = _BaseAlphaAnalyticsDataRestTransport._BaseQueryReportTask._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAlphaAnalyticsDataRestTransport._BaseQueryReportTask._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AlphaAnalyticsDataRestTransport._QueryReportTask._get_response(
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
            resp = analytics_data_api.QueryReportTaskResponse()
            pb_resp = analytics_data_api.QueryReportTaskResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_query_report_task(resp)
            return resp

    class _RunFunnelReport(
        _BaseAlphaAnalyticsDataRestTransport._BaseRunFunnelReport,
        AlphaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("AlphaAnalyticsDataRestTransport.RunFunnelReport")

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
            request: analytics_data_api.RunFunnelReportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.RunFunnelReportResponse:
            r"""Call the run funnel report method over HTTP.

            Args:
                request (~.analytics_data_api.RunFunnelReportRequest):
                    The request object. The request for a funnel report.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_data_api.RunFunnelReportResponse:
                    The funnel report response contains
                two sub reports. The two sub reports are
                different combinations of dimensions and
                metrics.

            """

            http_options = (
                _BaseAlphaAnalyticsDataRestTransport._BaseRunFunnelReport._get_http_options()
            )
            request, metadata = self._interceptor.pre_run_funnel_report(
                request, metadata
            )
            transcoded_request = _BaseAlphaAnalyticsDataRestTransport._BaseRunFunnelReport._get_transcoded_request(
                http_options, request
            )

            body = _BaseAlphaAnalyticsDataRestTransport._BaseRunFunnelReport._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAlphaAnalyticsDataRestTransport._BaseRunFunnelReport._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AlphaAnalyticsDataRestTransport._RunFunnelReport._get_response(
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
            resp = analytics_data_api.RunFunnelReportResponse()
            pb_resp = analytics_data_api.RunFunnelReportResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_run_funnel_report(resp)
            return resp

    class _SheetExportAudienceList(
        _BaseAlphaAnalyticsDataRestTransport._BaseSheetExportAudienceList,
        AlphaAnalyticsDataRestStub,
    ):
        def __hash__(self):
            return hash("AlphaAnalyticsDataRestTransport.SheetExportAudienceList")

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
            request: analytics_data_api.SheetExportAudienceListRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_data_api.SheetExportAudienceListResponse:
            r"""Call the sheet export audience
            list method over HTTP.

                Args:
                    request (~.analytics_data_api.SheetExportAudienceListRequest):
                        The request object. A request to export users in an
                    audience list to a Google Sheet.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.analytics_data_api.SheetExportAudienceListResponse:
                        The created Google Sheet with the
                    list of users in an audience list.

            """

            http_options = (
                _BaseAlphaAnalyticsDataRestTransport._BaseSheetExportAudienceList._get_http_options()
            )
            request, metadata = self._interceptor.pre_sheet_export_audience_list(
                request, metadata
            )
            transcoded_request = _BaseAlphaAnalyticsDataRestTransport._BaseSheetExportAudienceList._get_transcoded_request(
                http_options, request
            )

            body = _BaseAlphaAnalyticsDataRestTransport._BaseSheetExportAudienceList._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAlphaAnalyticsDataRestTransport._BaseSheetExportAudienceList._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                AlphaAnalyticsDataRestTransport._SheetExportAudienceList._get_response(
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
            resp = analytics_data_api.SheetExportAudienceListResponse()
            pb_resp = analytics_data_api.SheetExportAudienceListResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_sheet_export_audience_list(resp)
            return resp

    @property
    def create_audience_list(
        self,
    ) -> Callable[
        [analytics_data_api.CreateAudienceListRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAudienceList(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_recurring_audience_list(
        self,
    ) -> Callable[
        [analytics_data_api.CreateRecurringAudienceListRequest],
        analytics_data_api.RecurringAudienceList,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRecurringAudienceList(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_report_task(
        self,
    ) -> Callable[
        [analytics_data_api.CreateReportTaskRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateReportTask(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_audience_list(
        self,
    ) -> Callable[
        [analytics_data_api.GetAudienceListRequest], analytics_data_api.AudienceList
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAudienceList(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_property_quotas_snapshot(
        self,
    ) -> Callable[
        [analytics_data_api.GetPropertyQuotasSnapshotRequest],
        analytics_data_api.PropertyQuotasSnapshot,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPropertyQuotasSnapshot(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_recurring_audience_list(
        self,
    ) -> Callable[
        [analytics_data_api.GetRecurringAudienceListRequest],
        analytics_data_api.RecurringAudienceList,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRecurringAudienceList(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_report_task(
        self,
    ) -> Callable[
        [analytics_data_api.GetReportTaskRequest], analytics_data_api.ReportTask
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetReportTask(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_audience_lists(
        self,
    ) -> Callable[
        [analytics_data_api.ListAudienceListsRequest],
        analytics_data_api.ListAudienceListsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAudienceLists(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_recurring_audience_lists(
        self,
    ) -> Callable[
        [analytics_data_api.ListRecurringAudienceListsRequest],
        analytics_data_api.ListRecurringAudienceListsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRecurringAudienceLists(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_report_tasks(
        self,
    ) -> Callable[
        [analytics_data_api.ListReportTasksRequest],
        analytics_data_api.ListReportTasksResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListReportTasks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def query_audience_list(
        self,
    ) -> Callable[
        [analytics_data_api.QueryAudienceListRequest],
        analytics_data_api.QueryAudienceListResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._QueryAudienceList(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def query_report_task(
        self,
    ) -> Callable[
        [analytics_data_api.QueryReportTaskRequest],
        analytics_data_api.QueryReportTaskResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._QueryReportTask(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def run_funnel_report(
        self,
    ) -> Callable[
        [analytics_data_api.RunFunnelReportRequest],
        analytics_data_api.RunFunnelReportResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RunFunnelReport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def sheet_export_audience_list(
        self,
    ) -> Callable[
        [analytics_data_api.SheetExportAudienceListRequest],
        analytics_data_api.SheetExportAudienceListResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SheetExportAudienceList(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("AlphaAnalyticsDataRestTransport",)
