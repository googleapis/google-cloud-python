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
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.storageinsights_v1.types import storageinsights

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseStorageInsightsRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class StorageInsightsRestInterceptor:
    """Interceptor for StorageInsights.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the StorageInsightsRestTransport.

    .. code-block:: python
        class MyCustomStorageInsightsInterceptor(StorageInsightsRestInterceptor):
            def pre_create_report_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_report_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_report_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_report_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_report_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_report_detail(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_report_detail(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_report_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_report_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_report_details(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_report_details(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_report_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_report_config(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = StorageInsightsRestTransport(interceptor=MyCustomStorageInsightsInterceptor())
        client = StorageInsightsClient(transport=transport)


    """

    def pre_create_report_config(
        self,
        request: storageinsights.CreateReportConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[storageinsights.CreateReportConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_report_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageInsights server.
        """
        return request, metadata

    def post_create_report_config(
        self, response: storageinsights.ReportConfig
    ) -> storageinsights.ReportConfig:
        """Post-rpc interceptor for create_report_config

        Override in a subclass to manipulate the response
        after it is returned by the StorageInsights server but before
        it is returned to user code.
        """
        return response

    def pre_delete_report_config(
        self,
        request: storageinsights.DeleteReportConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[storageinsights.DeleteReportConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_report_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageInsights server.
        """
        return request, metadata

    def pre_get_report_config(
        self,
        request: storageinsights.GetReportConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[storageinsights.GetReportConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_report_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageInsights server.
        """
        return request, metadata

    def post_get_report_config(
        self, response: storageinsights.ReportConfig
    ) -> storageinsights.ReportConfig:
        """Post-rpc interceptor for get_report_config

        Override in a subclass to manipulate the response
        after it is returned by the StorageInsights server but before
        it is returned to user code.
        """
        return response

    def pre_get_report_detail(
        self,
        request: storageinsights.GetReportDetailRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[storageinsights.GetReportDetailRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_report_detail

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageInsights server.
        """
        return request, metadata

    def post_get_report_detail(
        self, response: storageinsights.ReportDetail
    ) -> storageinsights.ReportDetail:
        """Post-rpc interceptor for get_report_detail

        Override in a subclass to manipulate the response
        after it is returned by the StorageInsights server but before
        it is returned to user code.
        """
        return response

    def pre_list_report_configs(
        self,
        request: storageinsights.ListReportConfigsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[storageinsights.ListReportConfigsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_report_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageInsights server.
        """
        return request, metadata

    def post_list_report_configs(
        self, response: storageinsights.ListReportConfigsResponse
    ) -> storageinsights.ListReportConfigsResponse:
        """Post-rpc interceptor for list_report_configs

        Override in a subclass to manipulate the response
        after it is returned by the StorageInsights server but before
        it is returned to user code.
        """
        return response

    def pre_list_report_details(
        self,
        request: storageinsights.ListReportDetailsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[storageinsights.ListReportDetailsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_report_details

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageInsights server.
        """
        return request, metadata

    def post_list_report_details(
        self, response: storageinsights.ListReportDetailsResponse
    ) -> storageinsights.ListReportDetailsResponse:
        """Post-rpc interceptor for list_report_details

        Override in a subclass to manipulate the response
        after it is returned by the StorageInsights server but before
        it is returned to user code.
        """
        return response

    def pre_update_report_config(
        self,
        request: storageinsights.UpdateReportConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[storageinsights.UpdateReportConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_report_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageInsights server.
        """
        return request, metadata

    def post_update_report_config(
        self, response: storageinsights.ReportConfig
    ) -> storageinsights.ReportConfig:
        """Post-rpc interceptor for update_report_config

        Override in a subclass to manipulate the response
        after it is returned by the StorageInsights server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.GetLocationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageInsights server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the StorageInsights server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.ListLocationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageInsights server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the StorageInsights server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.CancelOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageInsights server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the StorageInsights server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operation(
        self,
        request: operations_pb2.DeleteOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageInsights server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the StorageInsights server but before
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
        before they are sent to the StorageInsights server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the StorageInsights server but before
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
        before they are sent to the StorageInsights server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the StorageInsights server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class StorageInsightsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: StorageInsightsRestInterceptor


class StorageInsightsRestTransport(_BaseStorageInsightsRestTransport):
    """REST backend synchronous transport for StorageInsights.

    Service describing handlers for resources

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "storageinsights.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[StorageInsightsRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'storageinsights.googleapis.com').
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
        self._interceptor = interceptor or StorageInsightsRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateReportConfig(
        _BaseStorageInsightsRestTransport._BaseCreateReportConfig,
        StorageInsightsRestStub,
    ):
        def __hash__(self):
            return hash("StorageInsightsRestTransport.CreateReportConfig")

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
            request: storageinsights.CreateReportConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> storageinsights.ReportConfig:
            r"""Call the create report config method over HTTP.

            Args:
                request (~.storageinsights.CreateReportConfigRequest):
                    The request object. Message for creating a ReportConfig
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.storageinsights.ReportConfig:
                    Message describing ReportConfig
                object. ReportConfig is the
                configuration to generate reports. See
                https://cloud.google.com/storage/docs/insights/using-inventory-reports#create-config-rest
                for more details on how to set various
                fields. Next ID: 12

            """

            http_options = (
                _BaseStorageInsightsRestTransport._BaseCreateReportConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_report_config(
                request, metadata
            )
            transcoded_request = _BaseStorageInsightsRestTransport._BaseCreateReportConfig._get_transcoded_request(
                http_options, request
            )

            body = _BaseStorageInsightsRestTransport._BaseCreateReportConfig._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseStorageInsightsRestTransport._BaseCreateReportConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = StorageInsightsRestTransport._CreateReportConfig._get_response(
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
            resp = storageinsights.ReportConfig()
            pb_resp = storageinsights.ReportConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_report_config(resp)
            return resp

    class _DeleteReportConfig(
        _BaseStorageInsightsRestTransport._BaseDeleteReportConfig,
        StorageInsightsRestStub,
    ):
        def __hash__(self):
            return hash("StorageInsightsRestTransport.DeleteReportConfig")

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
            request: storageinsights.DeleteReportConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete report config method over HTTP.

            Args:
                request (~.storageinsights.DeleteReportConfigRequest):
                    The request object. Message for deleting a ReportConfig
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseStorageInsightsRestTransport._BaseDeleteReportConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_report_config(
                request, metadata
            )
            transcoded_request = _BaseStorageInsightsRestTransport._BaseDeleteReportConfig._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseStorageInsightsRestTransport._BaseDeleteReportConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = StorageInsightsRestTransport._DeleteReportConfig._get_response(
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

    class _GetReportConfig(
        _BaseStorageInsightsRestTransport._BaseGetReportConfig, StorageInsightsRestStub
    ):
        def __hash__(self):
            return hash("StorageInsightsRestTransport.GetReportConfig")

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
            request: storageinsights.GetReportConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> storageinsights.ReportConfig:
            r"""Call the get report config method over HTTP.

            Args:
                request (~.storageinsights.GetReportConfigRequest):
                    The request object. Message for getting a ReportConfig
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.storageinsights.ReportConfig:
                    Message describing ReportConfig
                object. ReportConfig is the
                configuration to generate reports. See
                https://cloud.google.com/storage/docs/insights/using-inventory-reports#create-config-rest
                for more details on how to set various
                fields. Next ID: 12

            """

            http_options = (
                _BaseStorageInsightsRestTransport._BaseGetReportConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_report_config(
                request, metadata
            )
            transcoded_request = _BaseStorageInsightsRestTransport._BaseGetReportConfig._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseStorageInsightsRestTransport._BaseGetReportConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = StorageInsightsRestTransport._GetReportConfig._get_response(
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
            resp = storageinsights.ReportConfig()
            pb_resp = storageinsights.ReportConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_report_config(resp)
            return resp

    class _GetReportDetail(
        _BaseStorageInsightsRestTransport._BaseGetReportDetail, StorageInsightsRestStub
    ):
        def __hash__(self):
            return hash("StorageInsightsRestTransport.GetReportDetail")

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
            request: storageinsights.GetReportDetailRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> storageinsights.ReportDetail:
            r"""Call the get report detail method over HTTP.

            Args:
                request (~.storageinsights.GetReportDetailRequest):
                    The request object. Message for getting a ReportDetail
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.storageinsights.ReportDetail:
                    Message describing ReportDetail
                object. ReportDetail represents metadata
                of generated reports for a ReportConfig.
                Next ID: 10

            """

            http_options = (
                _BaseStorageInsightsRestTransport._BaseGetReportDetail._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_report_detail(
                request, metadata
            )
            transcoded_request = _BaseStorageInsightsRestTransport._BaseGetReportDetail._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseStorageInsightsRestTransport._BaseGetReportDetail._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = StorageInsightsRestTransport._GetReportDetail._get_response(
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
            resp = storageinsights.ReportDetail()
            pb_resp = storageinsights.ReportDetail.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_report_detail(resp)
            return resp

    class _ListReportConfigs(
        _BaseStorageInsightsRestTransport._BaseListReportConfigs,
        StorageInsightsRestStub,
    ):
        def __hash__(self):
            return hash("StorageInsightsRestTransport.ListReportConfigs")

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
            request: storageinsights.ListReportConfigsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> storageinsights.ListReportConfigsResponse:
            r"""Call the list report configs method over HTTP.

            Args:
                request (~.storageinsights.ListReportConfigsRequest):
                    The request object. Message for requesting list of
                ReportConfigs
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.storageinsights.ListReportConfigsResponse:
                    Message for response to listing
                ReportConfigs

            """

            http_options = (
                _BaseStorageInsightsRestTransport._BaseListReportConfigs._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_report_configs(
                request, metadata
            )
            transcoded_request = _BaseStorageInsightsRestTransport._BaseListReportConfigs._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseStorageInsightsRestTransport._BaseListReportConfigs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = StorageInsightsRestTransport._ListReportConfigs._get_response(
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
            resp = storageinsights.ListReportConfigsResponse()
            pb_resp = storageinsights.ListReportConfigsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_report_configs(resp)
            return resp

    class _ListReportDetails(
        _BaseStorageInsightsRestTransport._BaseListReportDetails,
        StorageInsightsRestStub,
    ):
        def __hash__(self):
            return hash("StorageInsightsRestTransport.ListReportDetails")

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
            request: storageinsights.ListReportDetailsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> storageinsights.ListReportDetailsResponse:
            r"""Call the list report details method over HTTP.

            Args:
                request (~.storageinsights.ListReportDetailsRequest):
                    The request object. Message for requesting list of
                ReportDetails
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.storageinsights.ListReportDetailsResponse:
                    Message for response to listing
                ReportDetails

            """

            http_options = (
                _BaseStorageInsightsRestTransport._BaseListReportDetails._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_report_details(
                request, metadata
            )
            transcoded_request = _BaseStorageInsightsRestTransport._BaseListReportDetails._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseStorageInsightsRestTransport._BaseListReportDetails._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = StorageInsightsRestTransport._ListReportDetails._get_response(
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
            resp = storageinsights.ListReportDetailsResponse()
            pb_resp = storageinsights.ListReportDetailsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_report_details(resp)
            return resp

    class _UpdateReportConfig(
        _BaseStorageInsightsRestTransport._BaseUpdateReportConfig,
        StorageInsightsRestStub,
    ):
        def __hash__(self):
            return hash("StorageInsightsRestTransport.UpdateReportConfig")

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
            request: storageinsights.UpdateReportConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> storageinsights.ReportConfig:
            r"""Call the update report config method over HTTP.

            Args:
                request (~.storageinsights.UpdateReportConfigRequest):
                    The request object. Message for updating a ReportConfig
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.storageinsights.ReportConfig:
                    Message describing ReportConfig
                object. ReportConfig is the
                configuration to generate reports. See
                https://cloud.google.com/storage/docs/insights/using-inventory-reports#create-config-rest
                for more details on how to set various
                fields. Next ID: 12

            """

            http_options = (
                _BaseStorageInsightsRestTransport._BaseUpdateReportConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_report_config(
                request, metadata
            )
            transcoded_request = _BaseStorageInsightsRestTransport._BaseUpdateReportConfig._get_transcoded_request(
                http_options, request
            )

            body = _BaseStorageInsightsRestTransport._BaseUpdateReportConfig._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseStorageInsightsRestTransport._BaseUpdateReportConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = StorageInsightsRestTransport._UpdateReportConfig._get_response(
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
            resp = storageinsights.ReportConfig()
            pb_resp = storageinsights.ReportConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_report_config(resp)
            return resp

    @property
    def create_report_config(
        self,
    ) -> Callable[
        [storageinsights.CreateReportConfigRequest], storageinsights.ReportConfig
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateReportConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_report_config(
        self,
    ) -> Callable[[storageinsights.DeleteReportConfigRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteReportConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_report_config(
        self,
    ) -> Callable[
        [storageinsights.GetReportConfigRequest], storageinsights.ReportConfig
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetReportConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_report_detail(
        self,
    ) -> Callable[
        [storageinsights.GetReportDetailRequest], storageinsights.ReportDetail
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetReportDetail(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_report_configs(
        self,
    ) -> Callable[
        [storageinsights.ListReportConfigsRequest],
        storageinsights.ListReportConfigsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListReportConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_report_details(
        self,
    ) -> Callable[
        [storageinsights.ListReportDetailsRequest],
        storageinsights.ListReportDetailsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListReportDetails(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_report_config(
        self,
    ) -> Callable[
        [storageinsights.UpdateReportConfigRequest], storageinsights.ReportConfig
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateReportConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseStorageInsightsRestTransport._BaseGetLocation, StorageInsightsRestStub
    ):
        def __hash__(self):
            return hash("StorageInsightsRestTransport.GetLocation")

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
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options = (
                _BaseStorageInsightsRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = _BaseStorageInsightsRestTransport._BaseGetLocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseStorageInsightsRestTransport._BaseGetLocation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = StorageInsightsRestTransport._GetLocation._get_response(
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
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseStorageInsightsRestTransport._BaseListLocations, StorageInsightsRestStub
    ):
        def __hash__(self):
            return hash("StorageInsightsRestTransport.ListLocations")

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
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options = (
                _BaseStorageInsightsRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseStorageInsightsRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseStorageInsightsRestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = StorageInsightsRestTransport._ListLocations._get_response(
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
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseStorageInsightsRestTransport._BaseCancelOperation, StorageInsightsRestStub
    ):
        def __hash__(self):
            return hash("StorageInsightsRestTransport.CancelOperation")

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
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseStorageInsightsRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseStorageInsightsRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = _BaseStorageInsightsRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseStorageInsightsRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = StorageInsightsRestTransport._CancelOperation._get_response(
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
        _BaseStorageInsightsRestTransport._BaseDeleteOperation, StorageInsightsRestStub
    ):
        def __hash__(self):
            return hash("StorageInsightsRestTransport.DeleteOperation")

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
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseStorageInsightsRestTransport._BaseDeleteOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BaseStorageInsightsRestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseStorageInsightsRestTransport._BaseDeleteOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = StorageInsightsRestTransport._DeleteOperation._get_response(
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
        _BaseStorageInsightsRestTransport._BaseGetOperation, StorageInsightsRestStub
    ):
        def __hash__(self):
            return hash("StorageInsightsRestTransport.GetOperation")

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
                _BaseStorageInsightsRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseStorageInsightsRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseStorageInsightsRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = StorageInsightsRestTransport._GetOperation._get_response(
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
        _BaseStorageInsightsRestTransport._BaseListOperations, StorageInsightsRestStub
    ):
        def __hash__(self):
            return hash("StorageInsightsRestTransport.ListOperations")

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
                _BaseStorageInsightsRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseStorageInsightsRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseStorageInsightsRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = StorageInsightsRestTransport._ListOperations._get_response(
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


__all__ = ("StorageInsightsRestTransport",)
