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

from google.cloud.service_usage_v1.types import resources, serviceusage

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseServiceUsageRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class ServiceUsageRestInterceptor:
    """Interceptor for ServiceUsage.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ServiceUsageRestTransport.

    .. code-block:: python
        class MyCustomServiceUsageInterceptor(ServiceUsageRestInterceptor):
            def pre_batch_enable_services(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_enable_services(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_get_services(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_get_services(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_disable_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_disable_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_enable_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_enable_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_services(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_services(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ServiceUsageRestTransport(interceptor=MyCustomServiceUsageInterceptor())
        client = ServiceUsageClient(transport=transport)


    """

    def pre_batch_enable_services(
        self,
        request: serviceusage.BatchEnableServicesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[serviceusage.BatchEnableServicesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_enable_services

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceUsage server.
        """
        return request, metadata

    def post_batch_enable_services(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for batch_enable_services

        Override in a subclass to manipulate the response
        after it is returned by the ServiceUsage server but before
        it is returned to user code.
        """
        return response

    def pre_batch_get_services(
        self,
        request: serviceusage.BatchGetServicesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[serviceusage.BatchGetServicesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_get_services

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceUsage server.
        """
        return request, metadata

    def post_batch_get_services(
        self, response: serviceusage.BatchGetServicesResponse
    ) -> serviceusage.BatchGetServicesResponse:
        """Post-rpc interceptor for batch_get_services

        Override in a subclass to manipulate the response
        after it is returned by the ServiceUsage server but before
        it is returned to user code.
        """
        return response

    def pre_disable_service(
        self,
        request: serviceusage.DisableServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[serviceusage.DisableServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for disable_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceUsage server.
        """
        return request, metadata

    def post_disable_service(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for disable_service

        Override in a subclass to manipulate the response
        after it is returned by the ServiceUsage server but before
        it is returned to user code.
        """
        return response

    def pre_enable_service(
        self,
        request: serviceusage.EnableServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[serviceusage.EnableServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for enable_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceUsage server.
        """
        return request, metadata

    def post_enable_service(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for enable_service

        Override in a subclass to manipulate the response
        after it is returned by the ServiceUsage server but before
        it is returned to user code.
        """
        return response

    def pre_get_service(
        self,
        request: serviceusage.GetServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[serviceusage.GetServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceUsage server.
        """
        return request, metadata

    def post_get_service(self, response: resources.Service) -> resources.Service:
        """Post-rpc interceptor for get_service

        Override in a subclass to manipulate the response
        after it is returned by the ServiceUsage server but before
        it is returned to user code.
        """
        return response

    def pre_list_services(
        self,
        request: serviceusage.ListServicesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[serviceusage.ListServicesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_services

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceUsage server.
        """
        return request, metadata

    def post_list_services(
        self, response: serviceusage.ListServicesResponse
    ) -> serviceusage.ListServicesResponse:
        """Post-rpc interceptor for list_services

        Override in a subclass to manipulate the response
        after it is returned by the ServiceUsage server but before
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
        before they are sent to the ServiceUsage server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the ServiceUsage server but before
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
        before they are sent to the ServiceUsage server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the ServiceUsage server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ServiceUsageRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ServiceUsageRestInterceptor


class ServiceUsageRestTransport(_BaseServiceUsageRestTransport):
    """REST backend synchronous transport for ServiceUsage.

    Enables services that service consumers want to use on Google Cloud
    Platform, lists the available or enabled services, or disables
    services that service consumers no longer use.

    See `Service Usage
    API <https://cloud.google.com/service-usage/docs/overview>`__

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "serviceusage.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ServiceUsageRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'serviceusage.googleapis.com').
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
        self._interceptor = interceptor or ServiceUsageRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _BatchEnableServices(
        _BaseServiceUsageRestTransport._BaseBatchEnableServices, ServiceUsageRestStub
    ):
        def __hash__(self):
            return hash("ServiceUsageRestTransport.BatchEnableServices")

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
            request: serviceusage.BatchEnableServicesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the batch enable services method over HTTP.

            Args:
                request (~.serviceusage.BatchEnableServicesRequest):
                    The request object. Request message for the ``BatchEnableServices`` method.
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
                _BaseServiceUsageRestTransport._BaseBatchEnableServices._get_http_options()
            )
            request, metadata = self._interceptor.pre_batch_enable_services(
                request, metadata
            )
            transcoded_request = _BaseServiceUsageRestTransport._BaseBatchEnableServices._get_transcoded_request(
                http_options, request
            )

            body = _BaseServiceUsageRestTransport._BaseBatchEnableServices._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseServiceUsageRestTransport._BaseBatchEnableServices._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServiceUsageRestTransport._BatchEnableServices._get_response(
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
            resp = self._interceptor.post_batch_enable_services(resp)
            return resp

    class _BatchGetServices(
        _BaseServiceUsageRestTransport._BaseBatchGetServices, ServiceUsageRestStub
    ):
        def __hash__(self):
            return hash("ServiceUsageRestTransport.BatchGetServices")

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
            request: serviceusage.BatchGetServicesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> serviceusage.BatchGetServicesResponse:
            r"""Call the batch get services method over HTTP.

            Args:
                request (~.serviceusage.BatchGetServicesRequest):
                    The request object. Request message for the ``BatchGetServices`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.serviceusage.BatchGetServicesResponse:
                    Response message for the ``BatchGetServices`` method.
            """

            http_options = (
                _BaseServiceUsageRestTransport._BaseBatchGetServices._get_http_options()
            )
            request, metadata = self._interceptor.pre_batch_get_services(
                request, metadata
            )
            transcoded_request = _BaseServiceUsageRestTransport._BaseBatchGetServices._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseServiceUsageRestTransport._BaseBatchGetServices._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServiceUsageRestTransport._BatchGetServices._get_response(
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
            resp = serviceusage.BatchGetServicesResponse()
            pb_resp = serviceusage.BatchGetServicesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_get_services(resp)
            return resp

    class _DisableService(
        _BaseServiceUsageRestTransport._BaseDisableService, ServiceUsageRestStub
    ):
        def __hash__(self):
            return hash("ServiceUsageRestTransport.DisableService")

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
            request: serviceusage.DisableServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the disable service method over HTTP.

            Args:
                request (~.serviceusage.DisableServiceRequest):
                    The request object. Request message for the ``DisableService`` method.
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
                _BaseServiceUsageRestTransport._BaseDisableService._get_http_options()
            )
            request, metadata = self._interceptor.pre_disable_service(request, metadata)
            transcoded_request = _BaseServiceUsageRestTransport._BaseDisableService._get_transcoded_request(
                http_options, request
            )

            body = _BaseServiceUsageRestTransport._BaseDisableService._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseServiceUsageRestTransport._BaseDisableService._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServiceUsageRestTransport._DisableService._get_response(
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
            resp = self._interceptor.post_disable_service(resp)
            return resp

    class _EnableService(
        _BaseServiceUsageRestTransport._BaseEnableService, ServiceUsageRestStub
    ):
        def __hash__(self):
            return hash("ServiceUsageRestTransport.EnableService")

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
            request: serviceusage.EnableServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the enable service method over HTTP.

            Args:
                request (~.serviceusage.EnableServiceRequest):
                    The request object. Request message for the ``EnableService`` method.
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
                _BaseServiceUsageRestTransport._BaseEnableService._get_http_options()
            )
            request, metadata = self._interceptor.pre_enable_service(request, metadata)
            transcoded_request = _BaseServiceUsageRestTransport._BaseEnableService._get_transcoded_request(
                http_options, request
            )

            body = _BaseServiceUsageRestTransport._BaseEnableService._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseServiceUsageRestTransport._BaseEnableService._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServiceUsageRestTransport._EnableService._get_response(
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
            resp = self._interceptor.post_enable_service(resp)
            return resp

    class _GetService(
        _BaseServiceUsageRestTransport._BaseGetService, ServiceUsageRestStub
    ):
        def __hash__(self):
            return hash("ServiceUsageRestTransport.GetService")

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
            request: serviceusage.GetServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Service:
            r"""Call the get service method over HTTP.

            Args:
                request (~.serviceusage.GetServiceRequest):
                    The request object. Request message for the ``GetService`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Service:
                    A service that is available for use
                by the consumer.

            """

            http_options = (
                _BaseServiceUsageRestTransport._BaseGetService._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_service(request, metadata)
            transcoded_request = (
                _BaseServiceUsageRestTransport._BaseGetService._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseServiceUsageRestTransport._BaseGetService._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ServiceUsageRestTransport._GetService._get_response(
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
            resp = resources.Service()
            pb_resp = resources.Service.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_service(resp)
            return resp

    class _ListServices(
        _BaseServiceUsageRestTransport._BaseListServices, ServiceUsageRestStub
    ):
        def __hash__(self):
            return hash("ServiceUsageRestTransport.ListServices")

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
            request: serviceusage.ListServicesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> serviceusage.ListServicesResponse:
            r"""Call the list services method over HTTP.

            Args:
                request (~.serviceusage.ListServicesRequest):
                    The request object. Request message for the ``ListServices`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.serviceusage.ListServicesResponse:
                    Response message for the ``ListServices`` method.
            """

            http_options = (
                _BaseServiceUsageRestTransport._BaseListServices._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_services(request, metadata)
            transcoded_request = _BaseServiceUsageRestTransport._BaseListServices._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseServiceUsageRestTransport._BaseListServices._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ServiceUsageRestTransport._ListServices._get_response(
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
            resp = serviceusage.ListServicesResponse()
            pb_resp = serviceusage.ListServicesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_services(resp)
            return resp

    @property
    def batch_enable_services(
        self,
    ) -> Callable[[serviceusage.BatchEnableServicesRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchEnableServices(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_get_services(
        self,
    ) -> Callable[
        [serviceusage.BatchGetServicesRequest], serviceusage.BatchGetServicesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchGetServices(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def disable_service(
        self,
    ) -> Callable[[serviceusage.DisableServiceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DisableService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def enable_service(
        self,
    ) -> Callable[[serviceusage.EnableServiceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._EnableService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_service(
        self,
    ) -> Callable[[serviceusage.GetServiceRequest], resources.Service]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_services(
        self,
    ) -> Callable[
        [serviceusage.ListServicesRequest], serviceusage.ListServicesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListServices(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseServiceUsageRestTransport._BaseGetOperation, ServiceUsageRestStub
    ):
        def __hash__(self):
            return hash("ServiceUsageRestTransport.GetOperation")

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
                _BaseServiceUsageRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseServiceUsageRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseServiceUsageRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ServiceUsageRestTransport._GetOperation._get_response(
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
        _BaseServiceUsageRestTransport._BaseListOperations, ServiceUsageRestStub
    ):
        def __hash__(self):
            return hash("ServiceUsageRestTransport.ListOperations")

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
                _BaseServiceUsageRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseServiceUsageRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseServiceUsageRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServiceUsageRestTransport._ListOperations._get_response(
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


__all__ = ("ServiceUsageRestTransport",)
