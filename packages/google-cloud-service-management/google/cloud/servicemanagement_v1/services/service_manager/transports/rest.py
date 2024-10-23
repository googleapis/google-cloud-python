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

from google.api import service_pb2  # type: ignore
from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.servicemanagement_v1.types import resources, servicemanager

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseServiceManagerRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class ServiceManagerRestInterceptor:
    """Interceptor for ServiceManager.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ServiceManagerRestTransport.

    .. code-block:: python
        class MyCustomServiceManagerInterceptor(ServiceManagerRestInterceptor):
            def pre_create_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_service_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_service_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_service_rollout(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_service_rollout(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_generate_config_report(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_generate_config_report(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_service_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_service_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_service_rollout(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_service_rollout(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_service_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_service_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_service_rollouts(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_service_rollouts(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_services(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_services(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_submit_config_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_submit_config_source(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_undelete_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_undelete_service(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ServiceManagerRestTransport(interceptor=MyCustomServiceManagerInterceptor())
        client = ServiceManagerClient(transport=transport)


    """

    def pre_create_service(
        self,
        request: servicemanager.CreateServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[servicemanager.CreateServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceManager server.
        """
        return request, metadata

    def post_create_service(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_service

        Override in a subclass to manipulate the response
        after it is returned by the ServiceManager server but before
        it is returned to user code.
        """
        return response

    def pre_create_service_config(
        self,
        request: servicemanager.CreateServiceConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[servicemanager.CreateServiceConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_service_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceManager server.
        """
        return request, metadata

    def post_create_service_config(
        self, response: service_pb2.Service
    ) -> service_pb2.Service:
        """Post-rpc interceptor for create_service_config

        Override in a subclass to manipulate the response
        after it is returned by the ServiceManager server but before
        it is returned to user code.
        """
        return response

    def pre_create_service_rollout(
        self,
        request: servicemanager.CreateServiceRolloutRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[servicemanager.CreateServiceRolloutRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_service_rollout

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceManager server.
        """
        return request, metadata

    def post_create_service_rollout(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_service_rollout

        Override in a subclass to manipulate the response
        after it is returned by the ServiceManager server but before
        it is returned to user code.
        """
        return response

    def pre_delete_service(
        self,
        request: servicemanager.DeleteServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[servicemanager.DeleteServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceManager server.
        """
        return request, metadata

    def post_delete_service(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_service

        Override in a subclass to manipulate the response
        after it is returned by the ServiceManager server but before
        it is returned to user code.
        """
        return response

    def pre_generate_config_report(
        self,
        request: servicemanager.GenerateConfigReportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[servicemanager.GenerateConfigReportRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for generate_config_report

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceManager server.
        """
        return request, metadata

    def post_generate_config_report(
        self, response: servicemanager.GenerateConfigReportResponse
    ) -> servicemanager.GenerateConfigReportResponse:
        """Post-rpc interceptor for generate_config_report

        Override in a subclass to manipulate the response
        after it is returned by the ServiceManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_service(
        self,
        request: servicemanager.GetServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[servicemanager.GetServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceManager server.
        """
        return request, metadata

    def post_get_service(
        self, response: resources.ManagedService
    ) -> resources.ManagedService:
        """Post-rpc interceptor for get_service

        Override in a subclass to manipulate the response
        after it is returned by the ServiceManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_service_config(
        self,
        request: servicemanager.GetServiceConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[servicemanager.GetServiceConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_service_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceManager server.
        """
        return request, metadata

    def post_get_service_config(
        self, response: service_pb2.Service
    ) -> service_pb2.Service:
        """Post-rpc interceptor for get_service_config

        Override in a subclass to manipulate the response
        after it is returned by the ServiceManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_service_rollout(
        self,
        request: servicemanager.GetServiceRolloutRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[servicemanager.GetServiceRolloutRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_service_rollout

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceManager server.
        """
        return request, metadata

    def post_get_service_rollout(
        self, response: resources.Rollout
    ) -> resources.Rollout:
        """Post-rpc interceptor for get_service_rollout

        Override in a subclass to manipulate the response
        after it is returned by the ServiceManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_service_configs(
        self,
        request: servicemanager.ListServiceConfigsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[servicemanager.ListServiceConfigsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_service_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceManager server.
        """
        return request, metadata

    def post_list_service_configs(
        self, response: servicemanager.ListServiceConfigsResponse
    ) -> servicemanager.ListServiceConfigsResponse:
        """Post-rpc interceptor for list_service_configs

        Override in a subclass to manipulate the response
        after it is returned by the ServiceManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_service_rollouts(
        self,
        request: servicemanager.ListServiceRolloutsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[servicemanager.ListServiceRolloutsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_service_rollouts

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceManager server.
        """
        return request, metadata

    def post_list_service_rollouts(
        self, response: servicemanager.ListServiceRolloutsResponse
    ) -> servicemanager.ListServiceRolloutsResponse:
        """Post-rpc interceptor for list_service_rollouts

        Override in a subclass to manipulate the response
        after it is returned by the ServiceManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_services(
        self,
        request: servicemanager.ListServicesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[servicemanager.ListServicesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_services

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceManager server.
        """
        return request, metadata

    def post_list_services(
        self, response: servicemanager.ListServicesResponse
    ) -> servicemanager.ListServicesResponse:
        """Post-rpc interceptor for list_services

        Override in a subclass to manipulate the response
        after it is returned by the ServiceManager server but before
        it is returned to user code.
        """
        return response

    def pre_submit_config_source(
        self,
        request: servicemanager.SubmitConfigSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[servicemanager.SubmitConfigSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for submit_config_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceManager server.
        """
        return request, metadata

    def post_submit_config_source(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for submit_config_source

        Override in a subclass to manipulate the response
        after it is returned by the ServiceManager server but before
        it is returned to user code.
        """
        return response

    def pre_undelete_service(
        self,
        request: servicemanager.UndeleteServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[servicemanager.UndeleteServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for undelete_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceManager server.
        """
        return request, metadata

    def post_undelete_service(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for undelete_service

        Override in a subclass to manipulate the response
        after it is returned by the ServiceManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_iam_policy(
        self,
        request: iam_policy_pb2.GetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.GetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceManager server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the ServiceManager server but before
        it is returned to user code.
        """
        return response

    def pre_set_iam_policy(
        self,
        request: iam_policy_pb2.SetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.SetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceManager server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the ServiceManager server but before
        it is returned to user code.
        """
        return response

    def pre_test_iam_permissions(
        self,
        request: iam_policy_pb2.TestIamPermissionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.TestIamPermissionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceManager server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the ServiceManager server but before
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
        before they are sent to the ServiceManager server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the ServiceManager server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ServiceManagerRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ServiceManagerRestInterceptor


class ServiceManagerRestTransport(_BaseServiceManagerRestTransport):
    """REST backend synchronous transport for ServiceManager.

    `Google Service Management
    API <https://cloud.google.com/service-infrastructure/docs/overview>`__

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "servicemanagement.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ServiceManagerRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'servicemanagement.googleapis.com').
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
        self._interceptor = interceptor or ServiceManagerRestInterceptor()
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

    class _CreateService(
        _BaseServiceManagerRestTransport._BaseCreateService, ServiceManagerRestStub
    ):
        def __hash__(self):
            return hash("ServiceManagerRestTransport.CreateService")

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
            request: servicemanager.CreateServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create service method over HTTP.

            Args:
                request (~.servicemanager.CreateServiceRequest):
                    The request object. Request message for CreateService
                method.
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
                _BaseServiceManagerRestTransport._BaseCreateService._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_service(request, metadata)
            transcoded_request = _BaseServiceManagerRestTransport._BaseCreateService._get_transcoded_request(
                http_options, request
            )

            body = _BaseServiceManagerRestTransport._BaseCreateService._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseServiceManagerRestTransport._BaseCreateService._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServiceManagerRestTransport._CreateService._get_response(
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
            resp = self._interceptor.post_create_service(resp)
            return resp

    class _CreateServiceConfig(
        _BaseServiceManagerRestTransport._BaseCreateServiceConfig,
        ServiceManagerRestStub,
    ):
        def __hash__(self):
            return hash("ServiceManagerRestTransport.CreateServiceConfig")

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
            request: servicemanager.CreateServiceConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service_pb2.Service:
            r"""Call the create service config method over HTTP.

            Args:
                request (~.servicemanager.CreateServiceConfigRequest):
                    The request object. Request message for
                CreateServiceConfig method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service_pb2.Service:
                    ``Service`` is the root object of Google API service
                configuration (service config). It describes the basic
                information about a logical service, such as the service
                name and the user-facing title, and delegates other
                aspects to sub-sections. Each sub-section is either a
                proto message or a repeated proto message that
                configures a specific aspect, such as auth. For more
                information, see each proto message definition.

                Example:

                ::

                    type: google.api.Service
                    name: calendar.googleapis.com
                    title: Google Calendar API
                    apis:
                    - name: google.calendar.v3.Calendar

                    visibility:
                      rules:
                      - selector: "google.calendar.v3.*"
                        restriction: PREVIEW
                    backend:
                      rules:
                      - selector: "google.calendar.v3.*"
                        address: calendar.example.com

                    authentication:
                      providers:
                      - id: google_calendar_auth
                        jwks_uri: https://www.googleapis.com/oauth2/v1/certs
                        issuer: https://securetoken.google.com
                      rules:
                      - selector: "*"
                        requirements:
                          provider_id: google_calendar_auth

            """

            http_options = (
                _BaseServiceManagerRestTransport._BaseCreateServiceConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_service_config(
                request, metadata
            )
            transcoded_request = _BaseServiceManagerRestTransport._BaseCreateServiceConfig._get_transcoded_request(
                http_options, request
            )

            body = _BaseServiceManagerRestTransport._BaseCreateServiceConfig._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseServiceManagerRestTransport._BaseCreateServiceConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServiceManagerRestTransport._CreateServiceConfig._get_response(
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
            resp = service_pb2.Service()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_service_config(resp)
            return resp

    class _CreateServiceRollout(
        _BaseServiceManagerRestTransport._BaseCreateServiceRollout,
        ServiceManagerRestStub,
    ):
        def __hash__(self):
            return hash("ServiceManagerRestTransport.CreateServiceRollout")

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
            request: servicemanager.CreateServiceRolloutRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create service rollout method over HTTP.

            Args:
                request (~.servicemanager.CreateServiceRolloutRequest):
                    The request object. Request message for
                'CreateServiceRollout'
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
                _BaseServiceManagerRestTransport._BaseCreateServiceRollout._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_service_rollout(
                request, metadata
            )
            transcoded_request = _BaseServiceManagerRestTransport._BaseCreateServiceRollout._get_transcoded_request(
                http_options, request
            )

            body = _BaseServiceManagerRestTransport._BaseCreateServiceRollout._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseServiceManagerRestTransport._BaseCreateServiceRollout._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServiceManagerRestTransport._CreateServiceRollout._get_response(
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
            resp = self._interceptor.post_create_service_rollout(resp)
            return resp

    class _DeleteService(
        _BaseServiceManagerRestTransport._BaseDeleteService, ServiceManagerRestStub
    ):
        def __hash__(self):
            return hash("ServiceManagerRestTransport.DeleteService")

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
            request: servicemanager.DeleteServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete service method over HTTP.

            Args:
                request (~.servicemanager.DeleteServiceRequest):
                    The request object. Request message for DeleteService
                method.
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
                _BaseServiceManagerRestTransport._BaseDeleteService._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_service(request, metadata)
            transcoded_request = _BaseServiceManagerRestTransport._BaseDeleteService._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseServiceManagerRestTransport._BaseDeleteService._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServiceManagerRestTransport._DeleteService._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_service(resp)
            return resp

    class _GenerateConfigReport(
        _BaseServiceManagerRestTransport._BaseGenerateConfigReport,
        ServiceManagerRestStub,
    ):
        def __hash__(self):
            return hash("ServiceManagerRestTransport.GenerateConfigReport")

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
            request: servicemanager.GenerateConfigReportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> servicemanager.GenerateConfigReportResponse:
            r"""Call the generate config report method over HTTP.

            Args:
                request (~.servicemanager.GenerateConfigReportRequest):
                    The request object. Request message for
                GenerateConfigReport method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.servicemanager.GenerateConfigReportResponse:
                    Response message for
                GenerateConfigReport method.

            """

            http_options = (
                _BaseServiceManagerRestTransport._BaseGenerateConfigReport._get_http_options()
            )
            request, metadata = self._interceptor.pre_generate_config_report(
                request, metadata
            )
            transcoded_request = _BaseServiceManagerRestTransport._BaseGenerateConfigReport._get_transcoded_request(
                http_options, request
            )

            body = _BaseServiceManagerRestTransport._BaseGenerateConfigReport._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseServiceManagerRestTransport._BaseGenerateConfigReport._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServiceManagerRestTransport._GenerateConfigReport._get_response(
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
            resp = servicemanager.GenerateConfigReportResponse()
            pb_resp = servicemanager.GenerateConfigReportResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_generate_config_report(resp)
            return resp

    class _GetService(
        _BaseServiceManagerRestTransport._BaseGetService, ServiceManagerRestStub
    ):
        def __hash__(self):
            return hash("ServiceManagerRestTransport.GetService")

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
            request: servicemanager.GetServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.ManagedService:
            r"""Call the get service method over HTTP.

            Args:
                request (~.servicemanager.GetServiceRequest):
                    The request object. Request message for ``GetService`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.ManagedService:
                    The full representation of a Service
                that is managed by Google Service
                Management.

            """

            http_options = (
                _BaseServiceManagerRestTransport._BaseGetService._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_service(request, metadata)
            transcoded_request = _BaseServiceManagerRestTransport._BaseGetService._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseServiceManagerRestTransport._BaseGetService._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ServiceManagerRestTransport._GetService._get_response(
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
            resp = resources.ManagedService()
            pb_resp = resources.ManagedService.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_service(resp)
            return resp

    class _GetServiceConfig(
        _BaseServiceManagerRestTransport._BaseGetServiceConfig, ServiceManagerRestStub
    ):
        def __hash__(self):
            return hash("ServiceManagerRestTransport.GetServiceConfig")

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
            request: servicemanager.GetServiceConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service_pb2.Service:
            r"""Call the get service config method over HTTP.

            Args:
                request (~.servicemanager.GetServiceConfigRequest):
                    The request object. Request message for GetServiceConfig
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service_pb2.Service:
                    ``Service`` is the root object of Google API service
                configuration (service config). It describes the basic
                information about a logical service, such as the service
                name and the user-facing title, and delegates other
                aspects to sub-sections. Each sub-section is either a
                proto message or a repeated proto message that
                configures a specific aspect, such as auth. For more
                information, see each proto message definition.

                Example:

                ::

                    type: google.api.Service
                    name: calendar.googleapis.com
                    title: Google Calendar API
                    apis:
                    - name: google.calendar.v3.Calendar

                    visibility:
                      rules:
                      - selector: "google.calendar.v3.*"
                        restriction: PREVIEW
                    backend:
                      rules:
                      - selector: "google.calendar.v3.*"
                        address: calendar.example.com

                    authentication:
                      providers:
                      - id: google_calendar_auth
                        jwks_uri: https://www.googleapis.com/oauth2/v1/certs
                        issuer: https://securetoken.google.com
                      rules:
                      - selector: "*"
                        requirements:
                          provider_id: google_calendar_auth

            """

            http_options = (
                _BaseServiceManagerRestTransport._BaseGetServiceConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_service_config(
                request, metadata
            )
            transcoded_request = _BaseServiceManagerRestTransport._BaseGetServiceConfig._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseServiceManagerRestTransport._BaseGetServiceConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServiceManagerRestTransport._GetServiceConfig._get_response(
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
            resp = service_pb2.Service()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_service_config(resp)
            return resp

    class _GetServiceRollout(
        _BaseServiceManagerRestTransport._BaseGetServiceRollout, ServiceManagerRestStub
    ):
        def __hash__(self):
            return hash("ServiceManagerRestTransport.GetServiceRollout")

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
            request: servicemanager.GetServiceRolloutRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Rollout:
            r"""Call the get service rollout method over HTTP.

            Args:
                request (~.servicemanager.GetServiceRolloutRequest):
                    The request object. Request message for GetServiceRollout
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Rollout:
                    A rollout resource that defines how
                service configuration versions are
                pushed to control plane systems.
                Typically, you create a new version of
                the service config, and then create a
                Rollout to push the service config.

            """

            http_options = (
                _BaseServiceManagerRestTransport._BaseGetServiceRollout._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_service_rollout(
                request, metadata
            )
            transcoded_request = _BaseServiceManagerRestTransport._BaseGetServiceRollout._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseServiceManagerRestTransport._BaseGetServiceRollout._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServiceManagerRestTransport._GetServiceRollout._get_response(
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
            resp = resources.Rollout()
            pb_resp = resources.Rollout.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_service_rollout(resp)
            return resp

    class _ListServiceConfigs(
        _BaseServiceManagerRestTransport._BaseListServiceConfigs, ServiceManagerRestStub
    ):
        def __hash__(self):
            return hash("ServiceManagerRestTransport.ListServiceConfigs")

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
            request: servicemanager.ListServiceConfigsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> servicemanager.ListServiceConfigsResponse:
            r"""Call the list service configs method over HTTP.

            Args:
                request (~.servicemanager.ListServiceConfigsRequest):
                    The request object. Request message for
                ListServiceConfigs method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.servicemanager.ListServiceConfigsResponse:
                    Response message for
                ListServiceConfigs method.

            """

            http_options = (
                _BaseServiceManagerRestTransport._BaseListServiceConfigs._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_service_configs(
                request, metadata
            )
            transcoded_request = _BaseServiceManagerRestTransport._BaseListServiceConfigs._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseServiceManagerRestTransport._BaseListServiceConfigs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServiceManagerRestTransport._ListServiceConfigs._get_response(
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
            resp = servicemanager.ListServiceConfigsResponse()
            pb_resp = servicemanager.ListServiceConfigsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_service_configs(resp)
            return resp

    class _ListServiceRollouts(
        _BaseServiceManagerRestTransport._BaseListServiceRollouts,
        ServiceManagerRestStub,
    ):
        def __hash__(self):
            return hash("ServiceManagerRestTransport.ListServiceRollouts")

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
            request: servicemanager.ListServiceRolloutsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> servicemanager.ListServiceRolloutsResponse:
            r"""Call the list service rollouts method over HTTP.

            Args:
                request (~.servicemanager.ListServiceRolloutsRequest):
                    The request object. Request message for
                'ListServiceRollouts'
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.servicemanager.ListServiceRolloutsResponse:
                    Response message for
                ListServiceRollouts method.

            """

            http_options = (
                _BaseServiceManagerRestTransport._BaseListServiceRollouts._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_service_rollouts(
                request, metadata
            )
            transcoded_request = _BaseServiceManagerRestTransport._BaseListServiceRollouts._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseServiceManagerRestTransport._BaseListServiceRollouts._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServiceManagerRestTransport._ListServiceRollouts._get_response(
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
            resp = servicemanager.ListServiceRolloutsResponse()
            pb_resp = servicemanager.ListServiceRolloutsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_service_rollouts(resp)
            return resp

    class _ListServices(
        _BaseServiceManagerRestTransport._BaseListServices, ServiceManagerRestStub
    ):
        def __hash__(self):
            return hash("ServiceManagerRestTransport.ListServices")

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
            request: servicemanager.ListServicesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> servicemanager.ListServicesResponse:
            r"""Call the list services method over HTTP.

            Args:
                request (~.servicemanager.ListServicesRequest):
                    The request object. Request message for ``ListServices`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.servicemanager.ListServicesResponse:
                    Response message for ``ListServices`` method.
            """

            http_options = (
                _BaseServiceManagerRestTransport._BaseListServices._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_services(request, metadata)
            transcoded_request = _BaseServiceManagerRestTransport._BaseListServices._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseServiceManagerRestTransport._BaseListServices._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServiceManagerRestTransport._ListServices._get_response(
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
            resp = servicemanager.ListServicesResponse()
            pb_resp = servicemanager.ListServicesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_services(resp)
            return resp

    class _SubmitConfigSource(
        _BaseServiceManagerRestTransport._BaseSubmitConfigSource, ServiceManagerRestStub
    ):
        def __hash__(self):
            return hash("ServiceManagerRestTransport.SubmitConfigSource")

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
            request: servicemanager.SubmitConfigSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the submit config source method over HTTP.

            Args:
                request (~.servicemanager.SubmitConfigSourceRequest):
                    The request object. Request message for
                SubmitConfigSource method.
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
                _BaseServiceManagerRestTransport._BaseSubmitConfigSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_submit_config_source(
                request, metadata
            )
            transcoded_request = _BaseServiceManagerRestTransport._BaseSubmitConfigSource._get_transcoded_request(
                http_options, request
            )

            body = _BaseServiceManagerRestTransport._BaseSubmitConfigSource._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseServiceManagerRestTransport._BaseSubmitConfigSource._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServiceManagerRestTransport._SubmitConfigSource._get_response(
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
            resp = self._interceptor.post_submit_config_source(resp)
            return resp

    class _UndeleteService(
        _BaseServiceManagerRestTransport._BaseUndeleteService, ServiceManagerRestStub
    ):
        def __hash__(self):
            return hash("ServiceManagerRestTransport.UndeleteService")

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
            request: servicemanager.UndeleteServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the undelete service method over HTTP.

            Args:
                request (~.servicemanager.UndeleteServiceRequest):
                    The request object. Request message for UndeleteService
                method.
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
                _BaseServiceManagerRestTransport._BaseUndeleteService._get_http_options()
            )
            request, metadata = self._interceptor.pre_undelete_service(
                request, metadata
            )
            transcoded_request = _BaseServiceManagerRestTransport._BaseUndeleteService._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseServiceManagerRestTransport._BaseUndeleteService._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServiceManagerRestTransport._UndeleteService._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_undelete_service(resp)
            return resp

    @property
    def create_service(
        self,
    ) -> Callable[[servicemanager.CreateServiceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_service_config(
        self,
    ) -> Callable[[servicemanager.CreateServiceConfigRequest], service_pb2.Service]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateServiceConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_service_rollout(
        self,
    ) -> Callable[
        [servicemanager.CreateServiceRolloutRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateServiceRollout(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_service(
        self,
    ) -> Callable[[servicemanager.DeleteServiceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def generate_config_report(
        self,
    ) -> Callable[
        [servicemanager.GenerateConfigReportRequest],
        servicemanager.GenerateConfigReportResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GenerateConfigReport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_service(
        self,
    ) -> Callable[[servicemanager.GetServiceRequest], resources.ManagedService]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_service_config(
        self,
    ) -> Callable[[servicemanager.GetServiceConfigRequest], service_pb2.Service]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetServiceConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_service_rollout(
        self,
    ) -> Callable[[servicemanager.GetServiceRolloutRequest], resources.Rollout]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetServiceRollout(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_service_configs(
        self,
    ) -> Callable[
        [servicemanager.ListServiceConfigsRequest],
        servicemanager.ListServiceConfigsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListServiceConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_service_rollouts(
        self,
    ) -> Callable[
        [servicemanager.ListServiceRolloutsRequest],
        servicemanager.ListServiceRolloutsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListServiceRollouts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_services(
        self,
    ) -> Callable[
        [servicemanager.ListServicesRequest], servicemanager.ListServicesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListServices(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def submit_config_source(
        self,
    ) -> Callable[[servicemanager.SubmitConfigSourceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SubmitConfigSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def undelete_service(
        self,
    ) -> Callable[[servicemanager.UndeleteServiceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UndeleteService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_iam_policy(self):
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _GetIamPolicy(
        _BaseServiceManagerRestTransport._BaseGetIamPolicy, ServiceManagerRestStub
    ):
        def __hash__(self):
            return hash("ServiceManagerRestTransport.GetIamPolicy")

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
            request: iam_policy_pb2.GetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.GetIamPolicyRequest):
                    The request object for GetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from GetIamPolicy method.
            """

            http_options = (
                _BaseServiceManagerRestTransport._BaseGetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            transcoded_request = _BaseServiceManagerRestTransport._BaseGetIamPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseServiceManagerRestTransport._BaseGetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseServiceManagerRestTransport._BaseGetIamPolicy._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServiceManagerRestTransport._GetIamPolicy._get_response(
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

            content = response.content.decode("utf-8")
            resp = policy_pb2.Policy()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    @property
    def set_iam_policy(self):
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _SetIamPolicy(
        _BaseServiceManagerRestTransport._BaseSetIamPolicy, ServiceManagerRestStub
    ):
        def __hash__(self):
            return hash("ServiceManagerRestTransport.SetIamPolicy")

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
            request: iam_policy_pb2.SetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the set iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.SetIamPolicyRequest):
                    The request object for SetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from SetIamPolicy method.
            """

            http_options = (
                _BaseServiceManagerRestTransport._BaseSetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            transcoded_request = _BaseServiceManagerRestTransport._BaseSetIamPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseServiceManagerRestTransport._BaseSetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseServiceManagerRestTransport._BaseSetIamPolicy._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServiceManagerRestTransport._SetIamPolicy._get_response(
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

            content = response.content.decode("utf-8")
            resp = policy_pb2.Policy()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    @property
    def test_iam_permissions(self):
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    class _TestIamPermissions(
        _BaseServiceManagerRestTransport._BaseTestIamPermissions, ServiceManagerRestStub
    ):
        def __hash__(self):
            return hash("ServiceManagerRestTransport.TestIamPermissions")

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
            request: iam_policy_pb2.TestIamPermissionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> iam_policy_pb2.TestIamPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (iam_policy_pb2.TestIamPermissionsRequest):
                    The request object for TestIamPermissions method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                iam_policy_pb2.TestIamPermissionsResponse: Response from TestIamPermissions method.
            """

            http_options = (
                _BaseServiceManagerRestTransport._BaseTestIamPermissions._get_http_options()
            )
            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            transcoded_request = _BaseServiceManagerRestTransport._BaseTestIamPermissions._get_transcoded_request(
                http_options, request
            )

            body = _BaseServiceManagerRestTransport._BaseTestIamPermissions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseServiceManagerRestTransport._BaseTestIamPermissions._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServiceManagerRestTransport._TestIamPermissions._get_response(
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

            content = response.content.decode("utf-8")
            resp = iam_policy_pb2.TestIamPermissionsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseServiceManagerRestTransport._BaseListOperations, ServiceManagerRestStub
    ):
        def __hash__(self):
            return hash("ServiceManagerRestTransport.ListOperations")

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
                _BaseServiceManagerRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseServiceManagerRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseServiceManagerRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServiceManagerRestTransport._ListOperations._get_response(
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


__all__ = ("ServiceManagerRestTransport",)
