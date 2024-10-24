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
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.servicedirectory_v1.types import endpoint
from google.cloud.servicedirectory_v1.types import endpoint as gcs_endpoint
from google.cloud.servicedirectory_v1.types import namespace
from google.cloud.servicedirectory_v1.types import namespace as gcs_namespace
from google.cloud.servicedirectory_v1.types import registration_service
from google.cloud.servicedirectory_v1.types import service
from google.cloud.servicedirectory_v1.types import service as gcs_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseRegistrationServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class RegistrationServiceRestInterceptor:
    """Interceptor for RegistrationService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the RegistrationServiceRestTransport.

    .. code-block:: python
        class MyCustomRegistrationServiceInterceptor(RegistrationServiceRestInterceptor):
            def pre_create_endpoint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_endpoint(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_namespace(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_namespace(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_endpoint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_namespace(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_endpoint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_endpoint(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_iam_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_namespace(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_namespace(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_endpoints(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_endpoints(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_namespaces(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_namespaces(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_services(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_services(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_iam_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_test_iam_permissions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_test_iam_permissions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_endpoint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_endpoint(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_namespace(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_namespace(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_service(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = RegistrationServiceRestTransport(interceptor=MyCustomRegistrationServiceInterceptor())
        client = RegistrationServiceClient(transport=transport)


    """

    def pre_create_endpoint(
        self,
        request: registration_service.CreateEndpointRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registration_service.CreateEndpointRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_endpoint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegistrationService server.
        """
        return request, metadata

    def post_create_endpoint(
        self, response: gcs_endpoint.Endpoint
    ) -> gcs_endpoint.Endpoint:
        """Post-rpc interceptor for create_endpoint

        Override in a subclass to manipulate the response
        after it is returned by the RegistrationService server but before
        it is returned to user code.
        """
        return response

    def pre_create_namespace(
        self,
        request: registration_service.CreateNamespaceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registration_service.CreateNamespaceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_namespace

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegistrationService server.
        """
        return request, metadata

    def post_create_namespace(
        self, response: gcs_namespace.Namespace
    ) -> gcs_namespace.Namespace:
        """Post-rpc interceptor for create_namespace

        Override in a subclass to manipulate the response
        after it is returned by the RegistrationService server but before
        it is returned to user code.
        """
        return response

    def pre_create_service(
        self,
        request: registration_service.CreateServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registration_service.CreateServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegistrationService server.
        """
        return request, metadata

    def post_create_service(self, response: gcs_service.Service) -> gcs_service.Service:
        """Post-rpc interceptor for create_service

        Override in a subclass to manipulate the response
        after it is returned by the RegistrationService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_endpoint(
        self,
        request: registration_service.DeleteEndpointRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registration_service.DeleteEndpointRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_endpoint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegistrationService server.
        """
        return request, metadata

    def pre_delete_namespace(
        self,
        request: registration_service.DeleteNamespaceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registration_service.DeleteNamespaceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_namespace

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegistrationService server.
        """
        return request, metadata

    def pre_delete_service(
        self,
        request: registration_service.DeleteServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registration_service.DeleteServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegistrationService server.
        """
        return request, metadata

    def pre_get_endpoint(
        self,
        request: registration_service.GetEndpointRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registration_service.GetEndpointRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_endpoint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegistrationService server.
        """
        return request, metadata

    def post_get_endpoint(self, response: endpoint.Endpoint) -> endpoint.Endpoint:
        """Post-rpc interceptor for get_endpoint

        Override in a subclass to manipulate the response
        after it is returned by the RegistrationService server but before
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
        before they are sent to the RegistrationService server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the RegistrationService server but before
        it is returned to user code.
        """
        return response

    def pre_get_namespace(
        self,
        request: registration_service.GetNamespaceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registration_service.GetNamespaceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_namespace

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegistrationService server.
        """
        return request, metadata

    def post_get_namespace(self, response: namespace.Namespace) -> namespace.Namespace:
        """Post-rpc interceptor for get_namespace

        Override in a subclass to manipulate the response
        after it is returned by the RegistrationService server but before
        it is returned to user code.
        """
        return response

    def pre_get_service(
        self,
        request: registration_service.GetServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registration_service.GetServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegistrationService server.
        """
        return request, metadata

    def post_get_service(self, response: service.Service) -> service.Service:
        """Post-rpc interceptor for get_service

        Override in a subclass to manipulate the response
        after it is returned by the RegistrationService server but before
        it is returned to user code.
        """
        return response

    def pre_list_endpoints(
        self,
        request: registration_service.ListEndpointsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registration_service.ListEndpointsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_endpoints

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegistrationService server.
        """
        return request, metadata

    def post_list_endpoints(
        self, response: registration_service.ListEndpointsResponse
    ) -> registration_service.ListEndpointsResponse:
        """Post-rpc interceptor for list_endpoints

        Override in a subclass to manipulate the response
        after it is returned by the RegistrationService server but before
        it is returned to user code.
        """
        return response

    def pre_list_namespaces(
        self,
        request: registration_service.ListNamespacesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registration_service.ListNamespacesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_namespaces

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegistrationService server.
        """
        return request, metadata

    def post_list_namespaces(
        self, response: registration_service.ListNamespacesResponse
    ) -> registration_service.ListNamespacesResponse:
        """Post-rpc interceptor for list_namespaces

        Override in a subclass to manipulate the response
        after it is returned by the RegistrationService server but before
        it is returned to user code.
        """
        return response

    def pre_list_services(
        self,
        request: registration_service.ListServicesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registration_service.ListServicesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_services

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegistrationService server.
        """
        return request, metadata

    def post_list_services(
        self, response: registration_service.ListServicesResponse
    ) -> registration_service.ListServicesResponse:
        """Post-rpc interceptor for list_services

        Override in a subclass to manipulate the response
        after it is returned by the RegistrationService server but before
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
        before they are sent to the RegistrationService server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the RegistrationService server but before
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
        before they are sent to the RegistrationService server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the RegistrationService server but before
        it is returned to user code.
        """
        return response

    def pre_update_endpoint(
        self,
        request: registration_service.UpdateEndpointRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registration_service.UpdateEndpointRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_endpoint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegistrationService server.
        """
        return request, metadata

    def post_update_endpoint(
        self, response: gcs_endpoint.Endpoint
    ) -> gcs_endpoint.Endpoint:
        """Post-rpc interceptor for update_endpoint

        Override in a subclass to manipulate the response
        after it is returned by the RegistrationService server but before
        it is returned to user code.
        """
        return response

    def pre_update_namespace(
        self,
        request: registration_service.UpdateNamespaceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registration_service.UpdateNamespaceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_namespace

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegistrationService server.
        """
        return request, metadata

    def post_update_namespace(
        self, response: gcs_namespace.Namespace
    ) -> gcs_namespace.Namespace:
        """Post-rpc interceptor for update_namespace

        Override in a subclass to manipulate the response
        after it is returned by the RegistrationService server but before
        it is returned to user code.
        """
        return response

    def pre_update_service(
        self,
        request: registration_service.UpdateServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registration_service.UpdateServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegistrationService server.
        """
        return request, metadata

    def post_update_service(self, response: gcs_service.Service) -> gcs_service.Service:
        """Post-rpc interceptor for update_service

        Override in a subclass to manipulate the response
        after it is returned by the RegistrationService server but before
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
        before they are sent to the RegistrationService server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the RegistrationService server but before
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
        before they are sent to the RegistrationService server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the RegistrationService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class RegistrationServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: RegistrationServiceRestInterceptor


class RegistrationServiceRestTransport(_BaseRegistrationServiceRestTransport):
    """REST backend synchronous transport for RegistrationService.

    Service Directory API for registering services. It defines the
    following resource model:

    -  The API has a collection of
       [Namespace][google.cloud.servicedirectory.v1.Namespace]
       resources, named ``projects/*/locations/*/namespaces/*``.

    -  Each Namespace has a collection of
       [Service][google.cloud.servicedirectory.v1.Service] resources,
       named ``projects/*/locations/*/namespaces/*/services/*``.

    -  Each Service has a collection of
       [Endpoint][google.cloud.servicedirectory.v1.Endpoint] resources,
       named
       ``projects/*/locations/*/namespaces/*/services/*/endpoints/*``.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "servicedirectory.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[RegistrationServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'servicedirectory.googleapis.com').
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
        self._interceptor = interceptor or RegistrationServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateEndpoint(
        _BaseRegistrationServiceRestTransport._BaseCreateEndpoint,
        RegistrationServiceRestStub,
    ):
        def __hash__(self):
            return hash("RegistrationServiceRestTransport.CreateEndpoint")

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
            request: registration_service.CreateEndpointRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_endpoint.Endpoint:
            r"""Call the create endpoint method over HTTP.

            Args:
                request (~.registration_service.CreateEndpointRequest):
                    The request object. The request message for
                [RegistrationService.CreateEndpoint][google.cloud.servicedirectory.v1.RegistrationService.CreateEndpoint].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_endpoint.Endpoint:
                    An individual endpoint that provides a
                [service][google.cloud.servicedirectory.v1.Service]. The
                service must already exist to create an endpoint.

            """

            http_options = (
                _BaseRegistrationServiceRestTransport._BaseCreateEndpoint._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_endpoint(request, metadata)
            transcoded_request = _BaseRegistrationServiceRestTransport._BaseCreateEndpoint._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegistrationServiceRestTransport._BaseCreateEndpoint._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegistrationServiceRestTransport._BaseCreateEndpoint._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegistrationServiceRestTransport._CreateEndpoint._get_response(
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
            resp = gcs_endpoint.Endpoint()
            pb_resp = gcs_endpoint.Endpoint.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_endpoint(resp)
            return resp

    class _CreateNamespace(
        _BaseRegistrationServiceRestTransport._BaseCreateNamespace,
        RegistrationServiceRestStub,
    ):
        def __hash__(self):
            return hash("RegistrationServiceRestTransport.CreateNamespace")

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
            request: registration_service.CreateNamespaceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_namespace.Namespace:
            r"""Call the create namespace method over HTTP.

            Args:
                request (~.registration_service.CreateNamespaceRequest):
                    The request object. The request message for
                [RegistrationService.CreateNamespace][google.cloud.servicedirectory.v1.RegistrationService.CreateNamespace].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_namespace.Namespace:
                    A container for
                [services][google.cloud.servicedirectory.v1.Service].
                Namespaces allow administrators to group services
                together and define permissions for a collection of
                services.

            """

            http_options = (
                _BaseRegistrationServiceRestTransport._BaseCreateNamespace._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_namespace(
                request, metadata
            )
            transcoded_request = _BaseRegistrationServiceRestTransport._BaseCreateNamespace._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegistrationServiceRestTransport._BaseCreateNamespace._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegistrationServiceRestTransport._BaseCreateNamespace._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegistrationServiceRestTransport._CreateNamespace._get_response(
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
            resp = gcs_namespace.Namespace()
            pb_resp = gcs_namespace.Namespace.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_namespace(resp)
            return resp

    class _CreateService(
        _BaseRegistrationServiceRestTransport._BaseCreateService,
        RegistrationServiceRestStub,
    ):
        def __hash__(self):
            return hash("RegistrationServiceRestTransport.CreateService")

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
            request: registration_service.CreateServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_service.Service:
            r"""Call the create service method over HTTP.

            Args:
                request (~.registration_service.CreateServiceRequest):
                    The request object. The request message for
                [RegistrationService.CreateService][google.cloud.servicedirectory.v1.RegistrationService.CreateService].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_service.Service:
                    An individual service. A service contains a name and
                optional metadata. A service must exist before
                [endpoints][google.cloud.servicedirectory.v1.Endpoint]
                can be added to it.

            """

            http_options = (
                _BaseRegistrationServiceRestTransport._BaseCreateService._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_service(request, metadata)
            transcoded_request = _BaseRegistrationServiceRestTransport._BaseCreateService._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegistrationServiceRestTransport._BaseCreateService._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegistrationServiceRestTransport._BaseCreateService._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegistrationServiceRestTransport._CreateService._get_response(
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
            resp = gcs_service.Service()
            pb_resp = gcs_service.Service.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_service(resp)
            return resp

    class _DeleteEndpoint(
        _BaseRegistrationServiceRestTransport._BaseDeleteEndpoint,
        RegistrationServiceRestStub,
    ):
        def __hash__(self):
            return hash("RegistrationServiceRestTransport.DeleteEndpoint")

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
            request: registration_service.DeleteEndpointRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete endpoint method over HTTP.

            Args:
                request (~.registration_service.DeleteEndpointRequest):
                    The request object. The request message for
                [RegistrationService.DeleteEndpoint][google.cloud.servicedirectory.v1.RegistrationService.DeleteEndpoint].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseRegistrationServiceRestTransport._BaseDeleteEndpoint._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_endpoint(request, metadata)
            transcoded_request = _BaseRegistrationServiceRestTransport._BaseDeleteEndpoint._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegistrationServiceRestTransport._BaseDeleteEndpoint._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegistrationServiceRestTransport._DeleteEndpoint._get_response(
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

    class _DeleteNamespace(
        _BaseRegistrationServiceRestTransport._BaseDeleteNamespace,
        RegistrationServiceRestStub,
    ):
        def __hash__(self):
            return hash("RegistrationServiceRestTransport.DeleteNamespace")

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
            request: registration_service.DeleteNamespaceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete namespace method over HTTP.

            Args:
                request (~.registration_service.DeleteNamespaceRequest):
                    The request object. The request message for
                [RegistrationService.DeleteNamespace][google.cloud.servicedirectory.v1.RegistrationService.DeleteNamespace].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseRegistrationServiceRestTransport._BaseDeleteNamespace._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_namespace(
                request, metadata
            )
            transcoded_request = _BaseRegistrationServiceRestTransport._BaseDeleteNamespace._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegistrationServiceRestTransport._BaseDeleteNamespace._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegistrationServiceRestTransport._DeleteNamespace._get_response(
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

    class _DeleteService(
        _BaseRegistrationServiceRestTransport._BaseDeleteService,
        RegistrationServiceRestStub,
    ):
        def __hash__(self):
            return hash("RegistrationServiceRestTransport.DeleteService")

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
            request: registration_service.DeleteServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete service method over HTTP.

            Args:
                request (~.registration_service.DeleteServiceRequest):
                    The request object. The request message for
                [RegistrationService.DeleteService][google.cloud.servicedirectory.v1.RegistrationService.DeleteService].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseRegistrationServiceRestTransport._BaseDeleteService._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_service(request, metadata)
            transcoded_request = _BaseRegistrationServiceRestTransport._BaseDeleteService._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegistrationServiceRestTransport._BaseDeleteService._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegistrationServiceRestTransport._DeleteService._get_response(
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

    class _GetEndpoint(
        _BaseRegistrationServiceRestTransport._BaseGetEndpoint,
        RegistrationServiceRestStub,
    ):
        def __hash__(self):
            return hash("RegistrationServiceRestTransport.GetEndpoint")

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
            request: registration_service.GetEndpointRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> endpoint.Endpoint:
            r"""Call the get endpoint method over HTTP.

            Args:
                request (~.registration_service.GetEndpointRequest):
                    The request object. The request message for
                [RegistrationService.GetEndpoint][google.cloud.servicedirectory.v1.RegistrationService.GetEndpoint].
                This should not be used to lookup endpoints at runtime.
                Instead, use the ``resolve`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.endpoint.Endpoint:
                    An individual endpoint that provides a
                [service][google.cloud.servicedirectory.v1.Service]. The
                service must already exist to create an endpoint.

            """

            http_options = (
                _BaseRegistrationServiceRestTransport._BaseGetEndpoint._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_endpoint(request, metadata)
            transcoded_request = _BaseRegistrationServiceRestTransport._BaseGetEndpoint._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegistrationServiceRestTransport._BaseGetEndpoint._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegistrationServiceRestTransport._GetEndpoint._get_response(
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
            resp = endpoint.Endpoint()
            pb_resp = endpoint.Endpoint.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_endpoint(resp)
            return resp

    class _GetIamPolicy(
        _BaseRegistrationServiceRestTransport._BaseGetIamPolicy,
        RegistrationServiceRestStub,
    ):
        def __hash__(self):
            return hash("RegistrationServiceRestTransport.GetIamPolicy")

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
                request (~.iam_policy_pb2.GetIamPolicyRequest):
                    The request object. Request message for ``GetIamPolicy`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.policy_pb2.Policy:
                    An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources.

                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members``, or
                principals, to a single ``role``. Principals can be user
                accounts, service accounts, Google groups, and domains
                (such as G Suite). A ``role`` is a named list of
                permissions; each ``role`` can be an IAM predefined role
                or a user-created custom role.

                For some types of Google Cloud resources, a ``binding``
                can also specify a ``condition``, which is a logical
                expression that allows access to a resource only if the
                expression evaluates to ``true``. A condition can add
                constraints based on attributes of the request, the
                resource, or both. To learn which resources support
                conditions in their IAM policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.

                **JSON example:**

                ::

                       {
                         "bindings": [
                           {
                             "role": "roles/resourcemanager.organizationAdmin",
                             "members": [
                               "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                             ]
                           },
                           {
                             "role": "roles/resourcemanager.organizationViewer",
                             "members": [
                               "user:eve@example.com"
                             ],
                             "condition": {
                               "title": "expirable access",
                               "description": "Does not grant access after Sep 2020",
                               "expression": "request.time <
                               timestamp('2020-10-01T00:00:00.000Z')",
                             }
                           }
                         ],
                         "etag": "BwWWja0YfJA=",
                         "version": 3
                       }

                **YAML example:**

                ::

                       bindings:
                       - members:
                         - user:mike@example.com
                         - group:admins@example.com
                         - domain:google.com
                         - serviceAccount:my-project-id@appspot.gserviceaccount.com
                         role: roles/resourcemanager.organizationAdmin
                       - members:
                         - user:eve@example.com
                         role: roles/resourcemanager.organizationViewer
                         condition:
                           title: expirable access
                           description: Does not grant access after Sep 2020
                           expression: request.time < timestamp('2020-10-01T00:00:00.000Z')
                       etag: BwWWja0YfJA=
                       version: 3

                For a description of IAM and its features, see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

            """

            http_options = (
                _BaseRegistrationServiceRestTransport._BaseGetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            transcoded_request = _BaseRegistrationServiceRestTransport._BaseGetIamPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegistrationServiceRestTransport._BaseGetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegistrationServiceRestTransport._BaseGetIamPolicy._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegistrationServiceRestTransport._GetIamPolicy._get_response(
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
            resp = policy_pb2.Policy()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    class _GetNamespace(
        _BaseRegistrationServiceRestTransport._BaseGetNamespace,
        RegistrationServiceRestStub,
    ):
        def __hash__(self):
            return hash("RegistrationServiceRestTransport.GetNamespace")

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
            request: registration_service.GetNamespaceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> namespace.Namespace:
            r"""Call the get namespace method over HTTP.

            Args:
                request (~.registration_service.GetNamespaceRequest):
                    The request object. The request message for
                [RegistrationService.GetNamespace][google.cloud.servicedirectory.v1.RegistrationService.GetNamespace].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.namespace.Namespace:
                    A container for
                [services][google.cloud.servicedirectory.v1.Service].
                Namespaces allow administrators to group services
                together and define permissions for a collection of
                services.

            """

            http_options = (
                _BaseRegistrationServiceRestTransport._BaseGetNamespace._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_namespace(request, metadata)
            transcoded_request = _BaseRegistrationServiceRestTransport._BaseGetNamespace._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegistrationServiceRestTransport._BaseGetNamespace._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegistrationServiceRestTransport._GetNamespace._get_response(
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
            resp = namespace.Namespace()
            pb_resp = namespace.Namespace.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_namespace(resp)
            return resp

    class _GetService(
        _BaseRegistrationServiceRestTransport._BaseGetService,
        RegistrationServiceRestStub,
    ):
        def __hash__(self):
            return hash("RegistrationServiceRestTransport.GetService")

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
            request: registration_service.GetServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.Service:
            r"""Call the get service method over HTTP.

            Args:
                request (~.registration_service.GetServiceRequest):
                    The request object. The request message for
                [RegistrationService.GetService][google.cloud.servicedirectory.v1.RegistrationService.GetService].
                This should not be used for looking up a service.
                Instead, use the ``resolve`` method as it contains all
                endpoints and associated annotations.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.Service:
                    An individual service. A service contains a name and
                optional metadata. A service must exist before
                [endpoints][google.cloud.servicedirectory.v1.Endpoint]
                can be added to it.

            """

            http_options = (
                _BaseRegistrationServiceRestTransport._BaseGetService._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_service(request, metadata)
            transcoded_request = _BaseRegistrationServiceRestTransport._BaseGetService._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegistrationServiceRestTransport._BaseGetService._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegistrationServiceRestTransport._GetService._get_response(
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
            resp = service.Service()
            pb_resp = service.Service.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_service(resp)
            return resp

    class _ListEndpoints(
        _BaseRegistrationServiceRestTransport._BaseListEndpoints,
        RegistrationServiceRestStub,
    ):
        def __hash__(self):
            return hash("RegistrationServiceRestTransport.ListEndpoints")

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
            request: registration_service.ListEndpointsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registration_service.ListEndpointsResponse:
            r"""Call the list endpoints method over HTTP.

            Args:
                request (~.registration_service.ListEndpointsRequest):
                    The request object. The request message for
                [RegistrationService.ListEndpoints][google.cloud.servicedirectory.v1.RegistrationService.ListEndpoints].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registration_service.ListEndpointsResponse:
                    The response message for
                [RegistrationService.ListEndpoints][google.cloud.servicedirectory.v1.RegistrationService.ListEndpoints].

            """

            http_options = (
                _BaseRegistrationServiceRestTransport._BaseListEndpoints._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_endpoints(request, metadata)
            transcoded_request = _BaseRegistrationServiceRestTransport._BaseListEndpoints._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegistrationServiceRestTransport._BaseListEndpoints._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegistrationServiceRestTransport._ListEndpoints._get_response(
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
            resp = registration_service.ListEndpointsResponse()
            pb_resp = registration_service.ListEndpointsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_endpoints(resp)
            return resp

    class _ListNamespaces(
        _BaseRegistrationServiceRestTransport._BaseListNamespaces,
        RegistrationServiceRestStub,
    ):
        def __hash__(self):
            return hash("RegistrationServiceRestTransport.ListNamespaces")

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
            request: registration_service.ListNamespacesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registration_service.ListNamespacesResponse:
            r"""Call the list namespaces method over HTTP.

            Args:
                request (~.registration_service.ListNamespacesRequest):
                    The request object. The request message for
                [RegistrationService.ListNamespaces][google.cloud.servicedirectory.v1.RegistrationService.ListNamespaces].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registration_service.ListNamespacesResponse:
                    The response message for
                [RegistrationService.ListNamespaces][google.cloud.servicedirectory.v1.RegistrationService.ListNamespaces].

            """

            http_options = (
                _BaseRegistrationServiceRestTransport._BaseListNamespaces._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_namespaces(request, metadata)
            transcoded_request = _BaseRegistrationServiceRestTransport._BaseListNamespaces._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegistrationServiceRestTransport._BaseListNamespaces._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegistrationServiceRestTransport._ListNamespaces._get_response(
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
            resp = registration_service.ListNamespacesResponse()
            pb_resp = registration_service.ListNamespacesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_namespaces(resp)
            return resp

    class _ListServices(
        _BaseRegistrationServiceRestTransport._BaseListServices,
        RegistrationServiceRestStub,
    ):
        def __hash__(self):
            return hash("RegistrationServiceRestTransport.ListServices")

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
            request: registration_service.ListServicesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registration_service.ListServicesResponse:
            r"""Call the list services method over HTTP.

            Args:
                request (~.registration_service.ListServicesRequest):
                    The request object. The request message for
                [RegistrationService.ListServices][google.cloud.servicedirectory.v1.RegistrationService.ListServices].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registration_service.ListServicesResponse:
                    The response message for
                [RegistrationService.ListServices][google.cloud.servicedirectory.v1.RegistrationService.ListServices].

            """

            http_options = (
                _BaseRegistrationServiceRestTransport._BaseListServices._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_services(request, metadata)
            transcoded_request = _BaseRegistrationServiceRestTransport._BaseListServices._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegistrationServiceRestTransport._BaseListServices._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegistrationServiceRestTransport._ListServices._get_response(
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
            resp = registration_service.ListServicesResponse()
            pb_resp = registration_service.ListServicesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_services(resp)
            return resp

    class _SetIamPolicy(
        _BaseRegistrationServiceRestTransport._BaseSetIamPolicy,
        RegistrationServiceRestStub,
    ):
        def __hash__(self):
            return hash("RegistrationServiceRestTransport.SetIamPolicy")

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
                request (~.iam_policy_pb2.SetIamPolicyRequest):
                    The request object. Request message for ``SetIamPolicy`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.policy_pb2.Policy:
                    An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources.

                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members``, or
                principals, to a single ``role``. Principals can be user
                accounts, service accounts, Google groups, and domains
                (such as G Suite). A ``role`` is a named list of
                permissions; each ``role`` can be an IAM predefined role
                or a user-created custom role.

                For some types of Google Cloud resources, a ``binding``
                can also specify a ``condition``, which is a logical
                expression that allows access to a resource only if the
                expression evaluates to ``true``. A condition can add
                constraints based on attributes of the request, the
                resource, or both. To learn which resources support
                conditions in their IAM policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.

                **JSON example:**

                ::

                       {
                         "bindings": [
                           {
                             "role": "roles/resourcemanager.organizationAdmin",
                             "members": [
                               "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                             ]
                           },
                           {
                             "role": "roles/resourcemanager.organizationViewer",
                             "members": [
                               "user:eve@example.com"
                             ],
                             "condition": {
                               "title": "expirable access",
                               "description": "Does not grant access after Sep 2020",
                               "expression": "request.time <
                               timestamp('2020-10-01T00:00:00.000Z')",
                             }
                           }
                         ],
                         "etag": "BwWWja0YfJA=",
                         "version": 3
                       }

                **YAML example:**

                ::

                       bindings:
                       - members:
                         - user:mike@example.com
                         - group:admins@example.com
                         - domain:google.com
                         - serviceAccount:my-project-id@appspot.gserviceaccount.com
                         role: roles/resourcemanager.organizationAdmin
                       - members:
                         - user:eve@example.com
                         role: roles/resourcemanager.organizationViewer
                         condition:
                           title: expirable access
                           description: Does not grant access after Sep 2020
                           expression: request.time < timestamp('2020-10-01T00:00:00.000Z')
                       etag: BwWWja0YfJA=
                       version: 3

                For a description of IAM and its features, see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

            """

            http_options = (
                _BaseRegistrationServiceRestTransport._BaseSetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            transcoded_request = _BaseRegistrationServiceRestTransport._BaseSetIamPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegistrationServiceRestTransport._BaseSetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegistrationServiceRestTransport._BaseSetIamPolicy._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegistrationServiceRestTransport._SetIamPolicy._get_response(
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
            resp = policy_pb2.Policy()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    class _TestIamPermissions(
        _BaseRegistrationServiceRestTransport._BaseTestIamPermissions,
        RegistrationServiceRestStub,
    ):
        def __hash__(self):
            return hash("RegistrationServiceRestTransport.TestIamPermissions")

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
                request (~.iam_policy_pb2.TestIamPermissionsRequest):
                    The request object. Request message for ``TestIamPermissions`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.iam_policy_pb2.TestIamPermissionsResponse:
                    Response message for ``TestIamPermissions`` method.
            """

            http_options = (
                _BaseRegistrationServiceRestTransport._BaseTestIamPermissions._get_http_options()
            )
            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            transcoded_request = _BaseRegistrationServiceRestTransport._BaseTestIamPermissions._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegistrationServiceRestTransport._BaseTestIamPermissions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegistrationServiceRestTransport._BaseTestIamPermissions._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RegistrationServiceRestTransport._TestIamPermissions._get_response(
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
            resp = iam_policy_pb2.TestIamPermissionsResponse()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    class _UpdateEndpoint(
        _BaseRegistrationServiceRestTransport._BaseUpdateEndpoint,
        RegistrationServiceRestStub,
    ):
        def __hash__(self):
            return hash("RegistrationServiceRestTransport.UpdateEndpoint")

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
            request: registration_service.UpdateEndpointRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_endpoint.Endpoint:
            r"""Call the update endpoint method over HTTP.

            Args:
                request (~.registration_service.UpdateEndpointRequest):
                    The request object. The request message for
                [RegistrationService.UpdateEndpoint][google.cloud.servicedirectory.v1.RegistrationService.UpdateEndpoint].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_endpoint.Endpoint:
                    An individual endpoint that provides a
                [service][google.cloud.servicedirectory.v1.Service]. The
                service must already exist to create an endpoint.

            """

            http_options = (
                _BaseRegistrationServiceRestTransport._BaseUpdateEndpoint._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_endpoint(request, metadata)
            transcoded_request = _BaseRegistrationServiceRestTransport._BaseUpdateEndpoint._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegistrationServiceRestTransport._BaseUpdateEndpoint._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegistrationServiceRestTransport._BaseUpdateEndpoint._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegistrationServiceRestTransport._UpdateEndpoint._get_response(
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
            resp = gcs_endpoint.Endpoint()
            pb_resp = gcs_endpoint.Endpoint.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_endpoint(resp)
            return resp

    class _UpdateNamespace(
        _BaseRegistrationServiceRestTransport._BaseUpdateNamespace,
        RegistrationServiceRestStub,
    ):
        def __hash__(self):
            return hash("RegistrationServiceRestTransport.UpdateNamespace")

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
            request: registration_service.UpdateNamespaceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_namespace.Namespace:
            r"""Call the update namespace method over HTTP.

            Args:
                request (~.registration_service.UpdateNamespaceRequest):
                    The request object. The request message for
                [RegistrationService.UpdateNamespace][google.cloud.servicedirectory.v1.RegistrationService.UpdateNamespace].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_namespace.Namespace:
                    A container for
                [services][google.cloud.servicedirectory.v1.Service].
                Namespaces allow administrators to group services
                together and define permissions for a collection of
                services.

            """

            http_options = (
                _BaseRegistrationServiceRestTransport._BaseUpdateNamespace._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_namespace(
                request, metadata
            )
            transcoded_request = _BaseRegistrationServiceRestTransport._BaseUpdateNamespace._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegistrationServiceRestTransport._BaseUpdateNamespace._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegistrationServiceRestTransport._BaseUpdateNamespace._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegistrationServiceRestTransport._UpdateNamespace._get_response(
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
            resp = gcs_namespace.Namespace()
            pb_resp = gcs_namespace.Namespace.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_namespace(resp)
            return resp

    class _UpdateService(
        _BaseRegistrationServiceRestTransport._BaseUpdateService,
        RegistrationServiceRestStub,
    ):
        def __hash__(self):
            return hash("RegistrationServiceRestTransport.UpdateService")

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
            request: registration_service.UpdateServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_service.Service:
            r"""Call the update service method over HTTP.

            Args:
                request (~.registration_service.UpdateServiceRequest):
                    The request object. The request message for
                [RegistrationService.UpdateService][google.cloud.servicedirectory.v1.RegistrationService.UpdateService].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_service.Service:
                    An individual service. A service contains a name and
                optional metadata. A service must exist before
                [endpoints][google.cloud.servicedirectory.v1.Endpoint]
                can be added to it.

            """

            http_options = (
                _BaseRegistrationServiceRestTransport._BaseUpdateService._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_service(request, metadata)
            transcoded_request = _BaseRegistrationServiceRestTransport._BaseUpdateService._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegistrationServiceRestTransport._BaseUpdateService._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegistrationServiceRestTransport._BaseUpdateService._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegistrationServiceRestTransport._UpdateService._get_response(
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
            resp = gcs_service.Service()
            pb_resp = gcs_service.Service.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_service(resp)
            return resp

    @property
    def create_endpoint(
        self,
    ) -> Callable[[registration_service.CreateEndpointRequest], gcs_endpoint.Endpoint]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateEndpoint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_namespace(
        self,
    ) -> Callable[
        [registration_service.CreateNamespaceRequest], gcs_namespace.Namespace
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateNamespace(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_service(
        self,
    ) -> Callable[[registration_service.CreateServiceRequest], gcs_service.Service]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_endpoint(
        self,
    ) -> Callable[[registration_service.DeleteEndpointRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteEndpoint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_namespace(
        self,
    ) -> Callable[[registration_service.DeleteNamespaceRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteNamespace(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_service(
        self,
    ) -> Callable[[registration_service.DeleteServiceRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_endpoint(
        self,
    ) -> Callable[[registration_service.GetEndpointRequest], endpoint.Endpoint]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEndpoint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_namespace(
        self,
    ) -> Callable[[registration_service.GetNamespaceRequest], namespace.Namespace]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetNamespace(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_service(
        self,
    ) -> Callable[[registration_service.GetServiceRequest], service.Service]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_endpoints(
        self,
    ) -> Callable[
        [registration_service.ListEndpointsRequest],
        registration_service.ListEndpointsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEndpoints(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_namespaces(
        self,
    ) -> Callable[
        [registration_service.ListNamespacesRequest],
        registration_service.ListNamespacesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListNamespaces(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_services(
        self,
    ) -> Callable[
        [registration_service.ListServicesRequest],
        registration_service.ListServicesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListServices(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        iam_policy_pb2.TestIamPermissionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_endpoint(
        self,
    ) -> Callable[[registration_service.UpdateEndpointRequest], gcs_endpoint.Endpoint]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateEndpoint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_namespace(
        self,
    ) -> Callable[
        [registration_service.UpdateNamespaceRequest], gcs_namespace.Namespace
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateNamespace(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_service(
        self,
    ) -> Callable[[registration_service.UpdateServiceRequest], gcs_service.Service]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseRegistrationServiceRestTransport._BaseGetLocation,
        RegistrationServiceRestStub,
    ):
        def __hash__(self):
            return hash("RegistrationServiceRestTransport.GetLocation")

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
                _BaseRegistrationServiceRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = _BaseRegistrationServiceRestTransport._BaseGetLocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegistrationServiceRestTransport._BaseGetLocation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegistrationServiceRestTransport._GetLocation._get_response(
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
        _BaseRegistrationServiceRestTransport._BaseListLocations,
        RegistrationServiceRestStub,
    ):
        def __hash__(self):
            return hash("RegistrationServiceRestTransport.ListLocations")

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
                _BaseRegistrationServiceRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseRegistrationServiceRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegistrationServiceRestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegistrationServiceRestTransport._ListLocations._get_response(
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
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("RegistrationServiceRestTransport",)
