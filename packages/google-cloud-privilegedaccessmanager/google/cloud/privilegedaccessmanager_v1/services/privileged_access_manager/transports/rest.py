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
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.privilegedaccessmanager_v1.types import privilegedaccessmanager

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BasePrivilegedAccessManagerRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class PrivilegedAccessManagerRestInterceptor:
    """Interceptor for PrivilegedAccessManager.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the PrivilegedAccessManagerRestTransport.

    .. code-block:: python
        class MyCustomPrivilegedAccessManagerInterceptor(PrivilegedAccessManagerRestInterceptor):
            def pre_approve_grant(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_approve_grant(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_check_onboarding_status(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_check_onboarding_status(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_entitlement(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_entitlement(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_grant(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_grant(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_entitlement(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_entitlement(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_deny_grant(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_deny_grant(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_entitlement(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_entitlement(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_grant(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_grant(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_entitlements(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_entitlements(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_grants(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_grants(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_revoke_grant(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_revoke_grant(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_entitlements(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_entitlements(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_grants(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_grants(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_entitlement(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_entitlement(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = PrivilegedAccessManagerRestTransport(interceptor=MyCustomPrivilegedAccessManagerInterceptor())
        client = PrivilegedAccessManagerClient(transport=transport)


    """

    def pre_approve_grant(
        self,
        request: privilegedaccessmanager.ApproveGrantRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[privilegedaccessmanager.ApproveGrantRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for approve_grant

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PrivilegedAccessManager server.
        """
        return request, metadata

    def post_approve_grant(
        self, response: privilegedaccessmanager.Grant
    ) -> privilegedaccessmanager.Grant:
        """Post-rpc interceptor for approve_grant

        Override in a subclass to manipulate the response
        after it is returned by the PrivilegedAccessManager server but before
        it is returned to user code.
        """
        return response

    def pre_check_onboarding_status(
        self,
        request: privilegedaccessmanager.CheckOnboardingStatusRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        privilegedaccessmanager.CheckOnboardingStatusRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for check_onboarding_status

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PrivilegedAccessManager server.
        """
        return request, metadata

    def post_check_onboarding_status(
        self, response: privilegedaccessmanager.CheckOnboardingStatusResponse
    ) -> privilegedaccessmanager.CheckOnboardingStatusResponse:
        """Post-rpc interceptor for check_onboarding_status

        Override in a subclass to manipulate the response
        after it is returned by the PrivilegedAccessManager server but before
        it is returned to user code.
        """
        return response

    def pre_create_entitlement(
        self,
        request: privilegedaccessmanager.CreateEntitlementRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        privilegedaccessmanager.CreateEntitlementRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_entitlement

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PrivilegedAccessManager server.
        """
        return request, metadata

    def post_create_entitlement(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_entitlement

        Override in a subclass to manipulate the response
        after it is returned by the PrivilegedAccessManager server but before
        it is returned to user code.
        """
        return response

    def pre_create_grant(
        self,
        request: privilegedaccessmanager.CreateGrantRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[privilegedaccessmanager.CreateGrantRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_grant

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PrivilegedAccessManager server.
        """
        return request, metadata

    def post_create_grant(
        self, response: privilegedaccessmanager.Grant
    ) -> privilegedaccessmanager.Grant:
        """Post-rpc interceptor for create_grant

        Override in a subclass to manipulate the response
        after it is returned by the PrivilegedAccessManager server but before
        it is returned to user code.
        """
        return response

    def pre_delete_entitlement(
        self,
        request: privilegedaccessmanager.DeleteEntitlementRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        privilegedaccessmanager.DeleteEntitlementRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_entitlement

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PrivilegedAccessManager server.
        """
        return request, metadata

    def post_delete_entitlement(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_entitlement

        Override in a subclass to manipulate the response
        after it is returned by the PrivilegedAccessManager server but before
        it is returned to user code.
        """
        return response

    def pre_deny_grant(
        self,
        request: privilegedaccessmanager.DenyGrantRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[privilegedaccessmanager.DenyGrantRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for deny_grant

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PrivilegedAccessManager server.
        """
        return request, metadata

    def post_deny_grant(
        self, response: privilegedaccessmanager.Grant
    ) -> privilegedaccessmanager.Grant:
        """Post-rpc interceptor for deny_grant

        Override in a subclass to manipulate the response
        after it is returned by the PrivilegedAccessManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_entitlement(
        self,
        request: privilegedaccessmanager.GetEntitlementRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        privilegedaccessmanager.GetEntitlementRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_entitlement

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PrivilegedAccessManager server.
        """
        return request, metadata

    def post_get_entitlement(
        self, response: privilegedaccessmanager.Entitlement
    ) -> privilegedaccessmanager.Entitlement:
        """Post-rpc interceptor for get_entitlement

        Override in a subclass to manipulate the response
        after it is returned by the PrivilegedAccessManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_grant(
        self,
        request: privilegedaccessmanager.GetGrantRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[privilegedaccessmanager.GetGrantRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_grant

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PrivilegedAccessManager server.
        """
        return request, metadata

    def post_get_grant(
        self, response: privilegedaccessmanager.Grant
    ) -> privilegedaccessmanager.Grant:
        """Post-rpc interceptor for get_grant

        Override in a subclass to manipulate the response
        after it is returned by the PrivilegedAccessManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_entitlements(
        self,
        request: privilegedaccessmanager.ListEntitlementsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        privilegedaccessmanager.ListEntitlementsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_entitlements

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PrivilegedAccessManager server.
        """
        return request, metadata

    def post_list_entitlements(
        self, response: privilegedaccessmanager.ListEntitlementsResponse
    ) -> privilegedaccessmanager.ListEntitlementsResponse:
        """Post-rpc interceptor for list_entitlements

        Override in a subclass to manipulate the response
        after it is returned by the PrivilegedAccessManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_grants(
        self,
        request: privilegedaccessmanager.ListGrantsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[privilegedaccessmanager.ListGrantsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_grants

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PrivilegedAccessManager server.
        """
        return request, metadata

    def post_list_grants(
        self, response: privilegedaccessmanager.ListGrantsResponse
    ) -> privilegedaccessmanager.ListGrantsResponse:
        """Post-rpc interceptor for list_grants

        Override in a subclass to manipulate the response
        after it is returned by the PrivilegedAccessManager server but before
        it is returned to user code.
        """
        return response

    def pre_revoke_grant(
        self,
        request: privilegedaccessmanager.RevokeGrantRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[privilegedaccessmanager.RevokeGrantRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for revoke_grant

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PrivilegedAccessManager server.
        """
        return request, metadata

    def post_revoke_grant(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for revoke_grant

        Override in a subclass to manipulate the response
        after it is returned by the PrivilegedAccessManager server but before
        it is returned to user code.
        """
        return response

    def pre_search_entitlements(
        self,
        request: privilegedaccessmanager.SearchEntitlementsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        privilegedaccessmanager.SearchEntitlementsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for search_entitlements

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PrivilegedAccessManager server.
        """
        return request, metadata

    def post_search_entitlements(
        self, response: privilegedaccessmanager.SearchEntitlementsResponse
    ) -> privilegedaccessmanager.SearchEntitlementsResponse:
        """Post-rpc interceptor for search_entitlements

        Override in a subclass to manipulate the response
        after it is returned by the PrivilegedAccessManager server but before
        it is returned to user code.
        """
        return response

    def pre_search_grants(
        self,
        request: privilegedaccessmanager.SearchGrantsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[privilegedaccessmanager.SearchGrantsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for search_grants

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PrivilegedAccessManager server.
        """
        return request, metadata

    def post_search_grants(
        self, response: privilegedaccessmanager.SearchGrantsResponse
    ) -> privilegedaccessmanager.SearchGrantsResponse:
        """Post-rpc interceptor for search_grants

        Override in a subclass to manipulate the response
        after it is returned by the PrivilegedAccessManager server but before
        it is returned to user code.
        """
        return response

    def pre_update_entitlement(
        self,
        request: privilegedaccessmanager.UpdateEntitlementRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        privilegedaccessmanager.UpdateEntitlementRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_entitlement

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PrivilegedAccessManager server.
        """
        return request, metadata

    def post_update_entitlement(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_entitlement

        Override in a subclass to manipulate the response
        after it is returned by the PrivilegedAccessManager server but before
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
        before they are sent to the PrivilegedAccessManager server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the PrivilegedAccessManager server but before
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
        before they are sent to the PrivilegedAccessManager server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the PrivilegedAccessManager server but before
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
        before they are sent to the PrivilegedAccessManager server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the PrivilegedAccessManager server but before
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
        before they are sent to the PrivilegedAccessManager server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the PrivilegedAccessManager server but before
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
        before they are sent to the PrivilegedAccessManager server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the PrivilegedAccessManager server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class PrivilegedAccessManagerRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: PrivilegedAccessManagerRestInterceptor


class PrivilegedAccessManagerRestTransport(_BasePrivilegedAccessManagerRestTransport):
    """REST backend synchronous transport for PrivilegedAccessManager.

    This API allows customers to manage temporary, request based
    privileged access to their resources.

    It defines the following resource model:

    -  A collection of ``Entitlement`` resources. An entitlement allows
       configuring (among other things):

       -  Some kind of privileged access that users can request.
       -  A set of users called *requesters* who can request this
          access.
       -  A maximum duration for which the access can be requested.
       -  An optional approval workflow which must be satisfied before
          access is granted.

    -  A collection of ``Grant`` resources. A grant is a request by a
       requester to get the privileged access specified in an
       entitlement for some duration.

       After the approval workflow as specified in the entitlement is
       satisfied, the specified access is given to the requester. The
       access is automatically taken back after the requested duration
       is over.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "privilegedaccessmanager.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[PrivilegedAccessManagerRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'privilegedaccessmanager.googleapis.com').
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
        self._interceptor = interceptor or PrivilegedAccessManagerRestInterceptor()
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
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                    {
                        "method": "delete",
                        "uri": "/v1/{name=organizations/*/locations/*/operations/*}",
                    },
                    {
                        "method": "delete",
                        "uri": "/v1/{name=folders/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=organizations/*/locations/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=folders/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=organizations/*/locations/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=folders/*/locations/*}/operations",
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

    class _ApproveGrant(
        _BasePrivilegedAccessManagerRestTransport._BaseApproveGrant,
        PrivilegedAccessManagerRestStub,
    ):
        def __hash__(self):
            return hash("PrivilegedAccessManagerRestTransport.ApproveGrant")

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
            request: privilegedaccessmanager.ApproveGrantRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> privilegedaccessmanager.Grant:
            r"""Call the approve grant method over HTTP.

            Args:
                request (~.privilegedaccessmanager.ApproveGrantRequest):
                    The request object. Request message for ``ApproveGrant`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.privilegedaccessmanager.Grant:
                    This is to ensure that the ``Grants`` and
                ``ProducerGrants`` proto are byte compatible. A grant
                represents a request from a user for obtaining the
                access specified in an entitlement they are eligible
                for.

            """

            http_options = (
                _BasePrivilegedAccessManagerRestTransport._BaseApproveGrant._get_http_options()
            )
            request, metadata = self._interceptor.pre_approve_grant(request, metadata)
            transcoded_request = _BasePrivilegedAccessManagerRestTransport._BaseApproveGrant._get_transcoded_request(
                http_options, request
            )

            body = _BasePrivilegedAccessManagerRestTransport._BaseApproveGrant._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BasePrivilegedAccessManagerRestTransport._BaseApproveGrant._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PrivilegedAccessManagerRestTransport._ApproveGrant._get_response(
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
            resp = privilegedaccessmanager.Grant()
            pb_resp = privilegedaccessmanager.Grant.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_approve_grant(resp)
            return resp

    class _CheckOnboardingStatus(
        _BasePrivilegedAccessManagerRestTransport._BaseCheckOnboardingStatus,
        PrivilegedAccessManagerRestStub,
    ):
        def __hash__(self):
            return hash("PrivilegedAccessManagerRestTransport.CheckOnboardingStatus")

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
            request: privilegedaccessmanager.CheckOnboardingStatusRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> privilegedaccessmanager.CheckOnboardingStatusResponse:
            r"""Call the check onboarding status method over HTTP.

            Args:
                request (~.privilegedaccessmanager.CheckOnboardingStatusRequest):
                    The request object. Request message for ``CheckOnboardingStatus`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.privilegedaccessmanager.CheckOnboardingStatusResponse:
                    Response message for ``CheckOnboardingStatus`` method.
            """

            http_options = (
                _BasePrivilegedAccessManagerRestTransport._BaseCheckOnboardingStatus._get_http_options()
            )
            request, metadata = self._interceptor.pre_check_onboarding_status(
                request, metadata
            )
            transcoded_request = _BasePrivilegedAccessManagerRestTransport._BaseCheckOnboardingStatus._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePrivilegedAccessManagerRestTransport._BaseCheckOnboardingStatus._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PrivilegedAccessManagerRestTransport._CheckOnboardingStatus._get_response(
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
            resp = privilegedaccessmanager.CheckOnboardingStatusResponse()
            pb_resp = privilegedaccessmanager.CheckOnboardingStatusResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_check_onboarding_status(resp)
            return resp

    class _CreateEntitlement(
        _BasePrivilegedAccessManagerRestTransport._BaseCreateEntitlement,
        PrivilegedAccessManagerRestStub,
    ):
        def __hash__(self):
            return hash("PrivilegedAccessManagerRestTransport.CreateEntitlement")

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
            request: privilegedaccessmanager.CreateEntitlementRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create entitlement method over HTTP.

            Args:
                request (~.privilegedaccessmanager.CreateEntitlementRequest):
                    The request object. Message for creating an entitlement.
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
                _BasePrivilegedAccessManagerRestTransport._BaseCreateEntitlement._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_entitlement(
                request, metadata
            )
            transcoded_request = _BasePrivilegedAccessManagerRestTransport._BaseCreateEntitlement._get_transcoded_request(
                http_options, request
            )

            body = _BasePrivilegedAccessManagerRestTransport._BaseCreateEntitlement._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BasePrivilegedAccessManagerRestTransport._BaseCreateEntitlement._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                PrivilegedAccessManagerRestTransport._CreateEntitlement._get_response(
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
            resp = self._interceptor.post_create_entitlement(resp)
            return resp

    class _CreateGrant(
        _BasePrivilegedAccessManagerRestTransport._BaseCreateGrant,
        PrivilegedAccessManagerRestStub,
    ):
        def __hash__(self):
            return hash("PrivilegedAccessManagerRestTransport.CreateGrant")

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
            request: privilegedaccessmanager.CreateGrantRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> privilegedaccessmanager.Grant:
            r"""Call the create grant method over HTTP.

            Args:
                request (~.privilegedaccessmanager.CreateGrantRequest):
                    The request object. Message for creating a grant
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.privilegedaccessmanager.Grant:
                    This is to ensure that the ``Grants`` and
                ``ProducerGrants`` proto are byte compatible. A grant
                represents a request from a user for obtaining the
                access specified in an entitlement they are eligible
                for.

            """

            http_options = (
                _BasePrivilegedAccessManagerRestTransport._BaseCreateGrant._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_grant(request, metadata)
            transcoded_request = _BasePrivilegedAccessManagerRestTransport._BaseCreateGrant._get_transcoded_request(
                http_options, request
            )

            body = _BasePrivilegedAccessManagerRestTransport._BaseCreateGrant._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BasePrivilegedAccessManagerRestTransport._BaseCreateGrant._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PrivilegedAccessManagerRestTransport._CreateGrant._get_response(
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
            resp = privilegedaccessmanager.Grant()
            pb_resp = privilegedaccessmanager.Grant.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_grant(resp)
            return resp

    class _DeleteEntitlement(
        _BasePrivilegedAccessManagerRestTransport._BaseDeleteEntitlement,
        PrivilegedAccessManagerRestStub,
    ):
        def __hash__(self):
            return hash("PrivilegedAccessManagerRestTransport.DeleteEntitlement")

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
            request: privilegedaccessmanager.DeleteEntitlementRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete entitlement method over HTTP.

            Args:
                request (~.privilegedaccessmanager.DeleteEntitlementRequest):
                    The request object. Message for deleting an entitlement.
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
                _BasePrivilegedAccessManagerRestTransport._BaseDeleteEntitlement._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_entitlement(
                request, metadata
            )
            transcoded_request = _BasePrivilegedAccessManagerRestTransport._BaseDeleteEntitlement._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePrivilegedAccessManagerRestTransport._BaseDeleteEntitlement._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                PrivilegedAccessManagerRestTransport._DeleteEntitlement._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_entitlement(resp)
            return resp

    class _DenyGrant(
        _BasePrivilegedAccessManagerRestTransport._BaseDenyGrant,
        PrivilegedAccessManagerRestStub,
    ):
        def __hash__(self):
            return hash("PrivilegedAccessManagerRestTransport.DenyGrant")

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
            request: privilegedaccessmanager.DenyGrantRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> privilegedaccessmanager.Grant:
            r"""Call the deny grant method over HTTP.

            Args:
                request (~.privilegedaccessmanager.DenyGrantRequest):
                    The request object. Request message for ``DenyGrant`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.privilegedaccessmanager.Grant:
                    This is to ensure that the ``Grants`` and
                ``ProducerGrants`` proto are byte compatible. A grant
                represents a request from a user for obtaining the
                access specified in an entitlement they are eligible
                for.

            """

            http_options = (
                _BasePrivilegedAccessManagerRestTransport._BaseDenyGrant._get_http_options()
            )
            request, metadata = self._interceptor.pre_deny_grant(request, metadata)
            transcoded_request = _BasePrivilegedAccessManagerRestTransport._BaseDenyGrant._get_transcoded_request(
                http_options, request
            )

            body = _BasePrivilegedAccessManagerRestTransport._BaseDenyGrant._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BasePrivilegedAccessManagerRestTransport._BaseDenyGrant._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PrivilegedAccessManagerRestTransport._DenyGrant._get_response(
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
            resp = privilegedaccessmanager.Grant()
            pb_resp = privilegedaccessmanager.Grant.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_deny_grant(resp)
            return resp

    class _GetEntitlement(
        _BasePrivilegedAccessManagerRestTransport._BaseGetEntitlement,
        PrivilegedAccessManagerRestStub,
    ):
        def __hash__(self):
            return hash("PrivilegedAccessManagerRestTransport.GetEntitlement")

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
            request: privilegedaccessmanager.GetEntitlementRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> privilegedaccessmanager.Entitlement:
            r"""Call the get entitlement method over HTTP.

            Args:
                request (~.privilegedaccessmanager.GetEntitlementRequest):
                    The request object. Message for getting an entitlement.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.privilegedaccessmanager.Entitlement:
                    An entitlement defines the
                eligibility of a set of users to obtain
                predefined access for some time possibly
                after going through an approval
                workflow.

            """

            http_options = (
                _BasePrivilegedAccessManagerRestTransport._BaseGetEntitlement._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_entitlement(request, metadata)
            transcoded_request = _BasePrivilegedAccessManagerRestTransport._BaseGetEntitlement._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePrivilegedAccessManagerRestTransport._BaseGetEntitlement._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                PrivilegedAccessManagerRestTransport._GetEntitlement._get_response(
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
            resp = privilegedaccessmanager.Entitlement()
            pb_resp = privilegedaccessmanager.Entitlement.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_entitlement(resp)
            return resp

    class _GetGrant(
        _BasePrivilegedAccessManagerRestTransport._BaseGetGrant,
        PrivilegedAccessManagerRestStub,
    ):
        def __hash__(self):
            return hash("PrivilegedAccessManagerRestTransport.GetGrant")

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
            request: privilegedaccessmanager.GetGrantRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> privilegedaccessmanager.Grant:
            r"""Call the get grant method over HTTP.

            Args:
                request (~.privilegedaccessmanager.GetGrantRequest):
                    The request object. Message for getting a grant.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.privilegedaccessmanager.Grant:
                    This is to ensure that the ``Grants`` and
                ``ProducerGrants`` proto are byte compatible. A grant
                represents a request from a user for obtaining the
                access specified in an entitlement they are eligible
                for.

            """

            http_options = (
                _BasePrivilegedAccessManagerRestTransport._BaseGetGrant._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_grant(request, metadata)
            transcoded_request = _BasePrivilegedAccessManagerRestTransport._BaseGetGrant._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePrivilegedAccessManagerRestTransport._BaseGetGrant._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PrivilegedAccessManagerRestTransport._GetGrant._get_response(
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
            resp = privilegedaccessmanager.Grant()
            pb_resp = privilegedaccessmanager.Grant.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_grant(resp)
            return resp

    class _ListEntitlements(
        _BasePrivilegedAccessManagerRestTransport._BaseListEntitlements,
        PrivilegedAccessManagerRestStub,
    ):
        def __hash__(self):
            return hash("PrivilegedAccessManagerRestTransport.ListEntitlements")

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
            request: privilegedaccessmanager.ListEntitlementsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> privilegedaccessmanager.ListEntitlementsResponse:
            r"""Call the list entitlements method over HTTP.

            Args:
                request (~.privilegedaccessmanager.ListEntitlementsRequest):
                    The request object. Message for requesting list of
                entitlements.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.privilegedaccessmanager.ListEntitlementsResponse:
                    Message for response to listing
                entitlements.

            """

            http_options = (
                _BasePrivilegedAccessManagerRestTransport._BaseListEntitlements._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_entitlements(
                request, metadata
            )
            transcoded_request = _BasePrivilegedAccessManagerRestTransport._BaseListEntitlements._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePrivilegedAccessManagerRestTransport._BaseListEntitlements._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                PrivilegedAccessManagerRestTransport._ListEntitlements._get_response(
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
            resp = privilegedaccessmanager.ListEntitlementsResponse()
            pb_resp = privilegedaccessmanager.ListEntitlementsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_entitlements(resp)
            return resp

    class _ListGrants(
        _BasePrivilegedAccessManagerRestTransport._BaseListGrants,
        PrivilegedAccessManagerRestStub,
    ):
        def __hash__(self):
            return hash("PrivilegedAccessManagerRestTransport.ListGrants")

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
            request: privilegedaccessmanager.ListGrantsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> privilegedaccessmanager.ListGrantsResponse:
            r"""Call the list grants method over HTTP.

            Args:
                request (~.privilegedaccessmanager.ListGrantsRequest):
                    The request object. Message for requesting list of
                grants.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.privilegedaccessmanager.ListGrantsResponse:
                    Message for response to listing
                grants.

            """

            http_options = (
                _BasePrivilegedAccessManagerRestTransport._BaseListGrants._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_grants(request, metadata)
            transcoded_request = _BasePrivilegedAccessManagerRestTransport._BaseListGrants._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePrivilegedAccessManagerRestTransport._BaseListGrants._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PrivilegedAccessManagerRestTransport._ListGrants._get_response(
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
            resp = privilegedaccessmanager.ListGrantsResponse()
            pb_resp = privilegedaccessmanager.ListGrantsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_grants(resp)
            return resp

    class _RevokeGrant(
        _BasePrivilegedAccessManagerRestTransport._BaseRevokeGrant,
        PrivilegedAccessManagerRestStub,
    ):
        def __hash__(self):
            return hash("PrivilegedAccessManagerRestTransport.RevokeGrant")

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
            request: privilegedaccessmanager.RevokeGrantRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the revoke grant method over HTTP.

            Args:
                request (~.privilegedaccessmanager.RevokeGrantRequest):
                    The request object. Request message for ``RevokeGrant`` method.
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
                _BasePrivilegedAccessManagerRestTransport._BaseRevokeGrant._get_http_options()
            )
            request, metadata = self._interceptor.pre_revoke_grant(request, metadata)
            transcoded_request = _BasePrivilegedAccessManagerRestTransport._BaseRevokeGrant._get_transcoded_request(
                http_options, request
            )

            body = _BasePrivilegedAccessManagerRestTransport._BaseRevokeGrant._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BasePrivilegedAccessManagerRestTransport._BaseRevokeGrant._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PrivilegedAccessManagerRestTransport._RevokeGrant._get_response(
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
            resp = self._interceptor.post_revoke_grant(resp)
            return resp

    class _SearchEntitlements(
        _BasePrivilegedAccessManagerRestTransport._BaseSearchEntitlements,
        PrivilegedAccessManagerRestStub,
    ):
        def __hash__(self):
            return hash("PrivilegedAccessManagerRestTransport.SearchEntitlements")

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
            request: privilegedaccessmanager.SearchEntitlementsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> privilegedaccessmanager.SearchEntitlementsResponse:
            r"""Call the search entitlements method over HTTP.

            Args:
                request (~.privilegedaccessmanager.SearchEntitlementsRequest):
                    The request object. Request message for ``SearchEntitlements`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.privilegedaccessmanager.SearchEntitlementsResponse:
                    Response message for ``SearchEntitlements`` method.
            """

            http_options = (
                _BasePrivilegedAccessManagerRestTransport._BaseSearchEntitlements._get_http_options()
            )
            request, metadata = self._interceptor.pre_search_entitlements(
                request, metadata
            )
            transcoded_request = _BasePrivilegedAccessManagerRestTransport._BaseSearchEntitlements._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePrivilegedAccessManagerRestTransport._BaseSearchEntitlements._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                PrivilegedAccessManagerRestTransport._SearchEntitlements._get_response(
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
            resp = privilegedaccessmanager.SearchEntitlementsResponse()
            pb_resp = privilegedaccessmanager.SearchEntitlementsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_search_entitlements(resp)
            return resp

    class _SearchGrants(
        _BasePrivilegedAccessManagerRestTransport._BaseSearchGrants,
        PrivilegedAccessManagerRestStub,
    ):
        def __hash__(self):
            return hash("PrivilegedAccessManagerRestTransport.SearchGrants")

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
            request: privilegedaccessmanager.SearchGrantsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> privilegedaccessmanager.SearchGrantsResponse:
            r"""Call the search grants method over HTTP.

            Args:
                request (~.privilegedaccessmanager.SearchGrantsRequest):
                    The request object. Request message for ``SearchGrants`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.privilegedaccessmanager.SearchGrantsResponse:
                    Response message for ``SearchGrants`` method.
            """

            http_options = (
                _BasePrivilegedAccessManagerRestTransport._BaseSearchGrants._get_http_options()
            )
            request, metadata = self._interceptor.pre_search_grants(request, metadata)
            transcoded_request = _BasePrivilegedAccessManagerRestTransport._BaseSearchGrants._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePrivilegedAccessManagerRestTransport._BaseSearchGrants._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PrivilegedAccessManagerRestTransport._SearchGrants._get_response(
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
            resp = privilegedaccessmanager.SearchGrantsResponse()
            pb_resp = privilegedaccessmanager.SearchGrantsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_search_grants(resp)
            return resp

    class _UpdateEntitlement(
        _BasePrivilegedAccessManagerRestTransport._BaseUpdateEntitlement,
        PrivilegedAccessManagerRestStub,
    ):
        def __hash__(self):
            return hash("PrivilegedAccessManagerRestTransport.UpdateEntitlement")

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
            request: privilegedaccessmanager.UpdateEntitlementRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update entitlement method over HTTP.

            Args:
                request (~.privilegedaccessmanager.UpdateEntitlementRequest):
                    The request object. Message for updating an entitlement.
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
                _BasePrivilegedAccessManagerRestTransport._BaseUpdateEntitlement._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_entitlement(
                request, metadata
            )
            transcoded_request = _BasePrivilegedAccessManagerRestTransport._BaseUpdateEntitlement._get_transcoded_request(
                http_options, request
            )

            body = _BasePrivilegedAccessManagerRestTransport._BaseUpdateEntitlement._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BasePrivilegedAccessManagerRestTransport._BaseUpdateEntitlement._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                PrivilegedAccessManagerRestTransport._UpdateEntitlement._get_response(
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
            resp = self._interceptor.post_update_entitlement(resp)
            return resp

    @property
    def approve_grant(
        self,
    ) -> Callable[
        [privilegedaccessmanager.ApproveGrantRequest], privilegedaccessmanager.Grant
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ApproveGrant(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def check_onboarding_status(
        self,
    ) -> Callable[
        [privilegedaccessmanager.CheckOnboardingStatusRequest],
        privilegedaccessmanager.CheckOnboardingStatusResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CheckOnboardingStatus(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_entitlement(
        self,
    ) -> Callable[
        [privilegedaccessmanager.CreateEntitlementRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateEntitlement(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_grant(
        self,
    ) -> Callable[
        [privilegedaccessmanager.CreateGrantRequest], privilegedaccessmanager.Grant
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateGrant(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_entitlement(
        self,
    ) -> Callable[
        [privilegedaccessmanager.DeleteEntitlementRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteEntitlement(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def deny_grant(
        self,
    ) -> Callable[
        [privilegedaccessmanager.DenyGrantRequest], privilegedaccessmanager.Grant
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DenyGrant(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_entitlement(
        self,
    ) -> Callable[
        [privilegedaccessmanager.GetEntitlementRequest],
        privilegedaccessmanager.Entitlement,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEntitlement(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_grant(
        self,
    ) -> Callable[
        [privilegedaccessmanager.GetGrantRequest], privilegedaccessmanager.Grant
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetGrant(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_entitlements(
        self,
    ) -> Callable[
        [privilegedaccessmanager.ListEntitlementsRequest],
        privilegedaccessmanager.ListEntitlementsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEntitlements(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_grants(
        self,
    ) -> Callable[
        [privilegedaccessmanager.ListGrantsRequest],
        privilegedaccessmanager.ListGrantsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListGrants(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def revoke_grant(
        self,
    ) -> Callable[
        [privilegedaccessmanager.RevokeGrantRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RevokeGrant(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_entitlements(
        self,
    ) -> Callable[
        [privilegedaccessmanager.SearchEntitlementsRequest],
        privilegedaccessmanager.SearchEntitlementsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchEntitlements(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_grants(
        self,
    ) -> Callable[
        [privilegedaccessmanager.SearchGrantsRequest],
        privilegedaccessmanager.SearchGrantsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchGrants(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_entitlement(
        self,
    ) -> Callable[
        [privilegedaccessmanager.UpdateEntitlementRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateEntitlement(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BasePrivilegedAccessManagerRestTransport._BaseGetLocation,
        PrivilegedAccessManagerRestStub,
    ):
        def __hash__(self):
            return hash("PrivilegedAccessManagerRestTransport.GetLocation")

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
                _BasePrivilegedAccessManagerRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = _BasePrivilegedAccessManagerRestTransport._BaseGetLocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePrivilegedAccessManagerRestTransport._BaseGetLocation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PrivilegedAccessManagerRestTransport._GetLocation._get_response(
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
        _BasePrivilegedAccessManagerRestTransport._BaseListLocations,
        PrivilegedAccessManagerRestStub,
    ):
        def __hash__(self):
            return hash("PrivilegedAccessManagerRestTransport.ListLocations")

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
                _BasePrivilegedAccessManagerRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BasePrivilegedAccessManagerRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePrivilegedAccessManagerRestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                PrivilegedAccessManagerRestTransport._ListLocations._get_response(
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

            content = response.content.decode("utf-8")
            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(
        _BasePrivilegedAccessManagerRestTransport._BaseDeleteOperation,
        PrivilegedAccessManagerRestStub,
    ):
        def __hash__(self):
            return hash("PrivilegedAccessManagerRestTransport.DeleteOperation")

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
                _BasePrivilegedAccessManagerRestTransport._BaseDeleteOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BasePrivilegedAccessManagerRestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePrivilegedAccessManagerRestTransport._BaseDeleteOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                PrivilegedAccessManagerRestTransport._DeleteOperation._get_response(
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

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BasePrivilegedAccessManagerRestTransport._BaseGetOperation,
        PrivilegedAccessManagerRestStub,
    ):
        def __hash__(self):
            return hash("PrivilegedAccessManagerRestTransport.GetOperation")

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
                _BasePrivilegedAccessManagerRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BasePrivilegedAccessManagerRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePrivilegedAccessManagerRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PrivilegedAccessManagerRestTransport._GetOperation._get_response(
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
        _BasePrivilegedAccessManagerRestTransport._BaseListOperations,
        PrivilegedAccessManagerRestStub,
    ):
        def __hash__(self):
            return hash("PrivilegedAccessManagerRestTransport.ListOperations")

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
                _BasePrivilegedAccessManagerRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BasePrivilegedAccessManagerRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePrivilegedAccessManagerRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                PrivilegedAccessManagerRestTransport._ListOperations._get_response(
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


__all__ = ("PrivilegedAccessManagerRestTransport",)
