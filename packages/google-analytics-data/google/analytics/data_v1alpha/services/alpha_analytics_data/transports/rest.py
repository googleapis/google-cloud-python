# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import (
    gapic_v1,
    operations_v1,
    path_template,
    rest_helpers,
    rest_streaming,
)
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.analytics.data_v1alpha.types import analytics_data_api

from .base import AlphaAnalyticsDataTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

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

            def pre_get_audience_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_audience_list(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_recurring_audience_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_recurring_audience_list(self, response):
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

            def pre_query_audience_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_query_audience_list(self, response):
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


class AlphaAnalyticsDataRestTransport(AlphaAnalyticsDataTransport):
    """REST backend transport for AlphaAnalyticsData.

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

    class _CreateAudienceList(AlphaAnalyticsDataRestStub):
        def __hash__(self):
            return hash("CreateAudienceList")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=properties/*}/audienceLists",
                    "body": "audience_list",
                },
            ]
            request, metadata = self._interceptor.pre_create_audience_list(
                request, metadata
            )
            pb_request = analytics_data_api.CreateAudienceListRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
                data=body,
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

    class _CreateRecurringAudienceList(AlphaAnalyticsDataRestStub):
        def __hash__(self):
            return hash("CreateRecurringAudienceList")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=properties/*}/recurringAudienceLists",
                    "body": "recurring_audience_list",
                },
            ]
            request, metadata = self._interceptor.pre_create_recurring_audience_list(
                request, metadata
            )
            pb_request = analytics_data_api.CreateRecurringAudienceListRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
                data=body,
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

    class _GetAudienceList(AlphaAnalyticsDataRestStub):
        def __hash__(self):
            return hash("GetAudienceList")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=properties/*/audienceLists/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_audience_list(
                request, metadata
            )
            pb_request = analytics_data_api.GetAudienceListRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = analytics_data_api.AudienceList()
            pb_resp = analytics_data_api.AudienceList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_audience_list(resp)
            return resp

    class _GetRecurringAudienceList(AlphaAnalyticsDataRestStub):
        def __hash__(self):
            return hash("GetRecurringAudienceList")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=properties/*/recurringAudienceLists/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_recurring_audience_list(
                request, metadata
            )
            pb_request = analytics_data_api.GetRecurringAudienceListRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = analytics_data_api.RecurringAudienceList()
            pb_resp = analytics_data_api.RecurringAudienceList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_recurring_audience_list(resp)
            return resp

    class _ListAudienceLists(AlphaAnalyticsDataRestStub):
        def __hash__(self):
            return hash("ListAudienceLists")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=properties/*}/audienceLists",
                },
            ]
            request, metadata = self._interceptor.pre_list_audience_lists(
                request, metadata
            )
            pb_request = analytics_data_api.ListAudienceListsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = analytics_data_api.ListAudienceListsResponse()
            pb_resp = analytics_data_api.ListAudienceListsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_audience_lists(resp)
            return resp

    class _ListRecurringAudienceLists(AlphaAnalyticsDataRestStub):
        def __hash__(self):
            return hash("ListRecurringAudienceLists")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=properties/*}/recurringAudienceLists",
                },
            ]
            request, metadata = self._interceptor.pre_list_recurring_audience_lists(
                request, metadata
            )
            pb_request = analytics_data_api.ListRecurringAudienceListsRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = analytics_data_api.ListRecurringAudienceListsResponse()
            pb_resp = analytics_data_api.ListRecurringAudienceListsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_recurring_audience_lists(resp)
            return resp

    class _QueryAudienceList(AlphaAnalyticsDataRestStub):
        def __hash__(self):
            return hash("QueryAudienceList")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{name=properties/*/audienceLists/*}:query",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_query_audience_list(
                request, metadata
            )
            pb_request = analytics_data_api.QueryAudienceListRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
                data=body,
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

    class _RunFunnelReport(AlphaAnalyticsDataRestStub):
        def __hash__(self):
            return hash("RunFunnelReport")

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{property=properties/*}:runFunnelReport",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_run_funnel_report(
                request, metadata
            )
            pb_request = analytics_data_api.RunFunnelReportRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = analytics_data_api.RunFunnelReportResponse()
            pb_resp = analytics_data_api.RunFunnelReportResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_run_funnel_report(resp)
            return resp

    class _SheetExportAudienceList(AlphaAnalyticsDataRestStub):
        def __hash__(self):
            return hash("SheetExportAudienceList")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{name=properties/*/audienceLists/*}:exportSheet",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_sheet_export_audience_list(
                request, metadata
            )
            pb_request = analytics_data_api.SheetExportAudienceListRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
                data=body,
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
    def get_audience_list(
        self,
    ) -> Callable[
        [analytics_data_api.GetAudienceListRequest], analytics_data_api.AudienceList
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAudienceList(self._session, self._host, self._interceptor)  # type: ignore

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
