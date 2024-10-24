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
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.cloudcontrolspartner_v1beta.types import (
    access_approval_requests,
    customer_workloads,
    customers,
    ekm_connections,
    partner_permissions,
    partners,
)

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseCloudControlsPartnerCoreRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class CloudControlsPartnerCoreRestInterceptor:
    """Interceptor for CloudControlsPartnerCore.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the CloudControlsPartnerCoreRestTransport.

    .. code-block:: python
        class MyCustomCloudControlsPartnerCoreInterceptor(CloudControlsPartnerCoreRestInterceptor):
            def pre_get_customer(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_customer(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_ekm_connections(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_ekm_connections(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_partner(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_partner(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_partner_permissions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_partner_permissions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_workload(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_workload(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_access_approval_requests(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_access_approval_requests(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_customers(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_customers(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_workloads(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_workloads(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = CloudControlsPartnerCoreRestTransport(interceptor=MyCustomCloudControlsPartnerCoreInterceptor())
        client = CloudControlsPartnerCoreClient(transport=transport)


    """

    def pre_get_customer(
        self, request: customers.GetCustomerRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[customers.GetCustomerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_customer

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudControlsPartnerCore server.
        """
        return request, metadata

    def post_get_customer(self, response: customers.Customer) -> customers.Customer:
        """Post-rpc interceptor for get_customer

        Override in a subclass to manipulate the response
        after it is returned by the CloudControlsPartnerCore server but before
        it is returned to user code.
        """
        return response

    def pre_get_ekm_connections(
        self,
        request: ekm_connections.GetEkmConnectionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[ekm_connections.GetEkmConnectionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_ekm_connections

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudControlsPartnerCore server.
        """
        return request, metadata

    def post_get_ekm_connections(
        self, response: ekm_connections.EkmConnections
    ) -> ekm_connections.EkmConnections:
        """Post-rpc interceptor for get_ekm_connections

        Override in a subclass to manipulate the response
        after it is returned by the CloudControlsPartnerCore server but before
        it is returned to user code.
        """
        return response

    def pre_get_partner(
        self, request: partners.GetPartnerRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[partners.GetPartnerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_partner

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudControlsPartnerCore server.
        """
        return request, metadata

    def post_get_partner(self, response: partners.Partner) -> partners.Partner:
        """Post-rpc interceptor for get_partner

        Override in a subclass to manipulate the response
        after it is returned by the CloudControlsPartnerCore server but before
        it is returned to user code.
        """
        return response

    def pre_get_partner_permissions(
        self,
        request: partner_permissions.GetPartnerPermissionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        partner_permissions.GetPartnerPermissionsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_partner_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudControlsPartnerCore server.
        """
        return request, metadata

    def post_get_partner_permissions(
        self, response: partner_permissions.PartnerPermissions
    ) -> partner_permissions.PartnerPermissions:
        """Post-rpc interceptor for get_partner_permissions

        Override in a subclass to manipulate the response
        after it is returned by the CloudControlsPartnerCore server but before
        it is returned to user code.
        """
        return response

    def pre_get_workload(
        self,
        request: customer_workloads.GetWorkloadRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[customer_workloads.GetWorkloadRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_workload

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudControlsPartnerCore server.
        """
        return request, metadata

    def post_get_workload(
        self, response: customer_workloads.Workload
    ) -> customer_workloads.Workload:
        """Post-rpc interceptor for get_workload

        Override in a subclass to manipulate the response
        after it is returned by the CloudControlsPartnerCore server but before
        it is returned to user code.
        """
        return response

    def pre_list_access_approval_requests(
        self,
        request: access_approval_requests.ListAccessApprovalRequestsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        access_approval_requests.ListAccessApprovalRequestsRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_access_approval_requests

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudControlsPartnerCore server.
        """
        return request, metadata

    def post_list_access_approval_requests(
        self, response: access_approval_requests.ListAccessApprovalRequestsResponse
    ) -> access_approval_requests.ListAccessApprovalRequestsResponse:
        """Post-rpc interceptor for list_access_approval_requests

        Override in a subclass to manipulate the response
        after it is returned by the CloudControlsPartnerCore server but before
        it is returned to user code.
        """
        return response

    def pre_list_customers(
        self,
        request: customers.ListCustomersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[customers.ListCustomersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_customers

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudControlsPartnerCore server.
        """
        return request, metadata

    def post_list_customers(
        self, response: customers.ListCustomersResponse
    ) -> customers.ListCustomersResponse:
        """Post-rpc interceptor for list_customers

        Override in a subclass to manipulate the response
        after it is returned by the CloudControlsPartnerCore server but before
        it is returned to user code.
        """
        return response

    def pre_list_workloads(
        self,
        request: customer_workloads.ListWorkloadsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[customer_workloads.ListWorkloadsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_workloads

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudControlsPartnerCore server.
        """
        return request, metadata

    def post_list_workloads(
        self, response: customer_workloads.ListWorkloadsResponse
    ) -> customer_workloads.ListWorkloadsResponse:
        """Post-rpc interceptor for list_workloads

        Override in a subclass to manipulate the response
        after it is returned by the CloudControlsPartnerCore server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class CloudControlsPartnerCoreRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: CloudControlsPartnerCoreRestInterceptor


class CloudControlsPartnerCoreRestTransport(_BaseCloudControlsPartnerCoreRestTransport):
    """REST backend synchronous transport for CloudControlsPartnerCore.

    Service describing handlers for resources

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "cloudcontrolspartner.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[CloudControlsPartnerCoreRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'cloudcontrolspartner.googleapis.com').
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
        self._interceptor = interceptor or CloudControlsPartnerCoreRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _GetCustomer(
        _BaseCloudControlsPartnerCoreRestTransport._BaseGetCustomer,
        CloudControlsPartnerCoreRestStub,
    ):
        def __hash__(self):
            return hash("CloudControlsPartnerCoreRestTransport.GetCustomer")

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
            request: customers.GetCustomerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> customers.Customer:
            r"""Call the get customer method over HTTP.

            Args:
                request (~.customers.GetCustomerRequest):
                    The request object. Message for getting a customer
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.customers.Customer:
                    Contains metadata around a Cloud
                Controls Partner Customer

            """

            http_options = (
                _BaseCloudControlsPartnerCoreRestTransport._BaseGetCustomer._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_customer(request, metadata)
            transcoded_request = _BaseCloudControlsPartnerCoreRestTransport._BaseGetCustomer._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudControlsPartnerCoreRestTransport._BaseGetCustomer._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CloudControlsPartnerCoreRestTransport._GetCustomer._get_response(
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
            resp = customers.Customer()
            pb_resp = customers.Customer.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_customer(resp)
            return resp

    class _GetEkmConnections(
        _BaseCloudControlsPartnerCoreRestTransport._BaseGetEkmConnections,
        CloudControlsPartnerCoreRestStub,
    ):
        def __hash__(self):
            return hash("CloudControlsPartnerCoreRestTransport.GetEkmConnections")

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
            request: ekm_connections.GetEkmConnectionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> ekm_connections.EkmConnections:
            r"""Call the get ekm connections method over HTTP.

            Args:
                request (~.ekm_connections.GetEkmConnectionsRequest):
                    The request object. Request for getting the EKM
                connections associated with a workload
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.ekm_connections.EkmConnections:
                    The EKM connections associated with a
                workload

            """

            http_options = (
                _BaseCloudControlsPartnerCoreRestTransport._BaseGetEkmConnections._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_ekm_connections(
                request, metadata
            )
            transcoded_request = _BaseCloudControlsPartnerCoreRestTransport._BaseGetEkmConnections._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudControlsPartnerCoreRestTransport._BaseGetEkmConnections._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                CloudControlsPartnerCoreRestTransport._GetEkmConnections._get_response(
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
            resp = ekm_connections.EkmConnections()
            pb_resp = ekm_connections.EkmConnections.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_ekm_connections(resp)
            return resp

    class _GetPartner(
        _BaseCloudControlsPartnerCoreRestTransport._BaseGetPartner,
        CloudControlsPartnerCoreRestStub,
    ):
        def __hash__(self):
            return hash("CloudControlsPartnerCoreRestTransport.GetPartner")

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
            request: partners.GetPartnerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> partners.Partner:
            r"""Call the get partner method over HTTP.

            Args:
                request (~.partners.GetPartnerRequest):
                    The request object. Message for getting a Partner
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.partners.Partner:
                    Message describing Partner resource
            """

            http_options = (
                _BaseCloudControlsPartnerCoreRestTransport._BaseGetPartner._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_partner(request, metadata)
            transcoded_request = _BaseCloudControlsPartnerCoreRestTransport._BaseGetPartner._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudControlsPartnerCoreRestTransport._BaseGetPartner._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CloudControlsPartnerCoreRestTransport._GetPartner._get_response(
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
            resp = partners.Partner()
            pb_resp = partners.Partner.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_partner(resp)
            return resp

    class _GetPartnerPermissions(
        _BaseCloudControlsPartnerCoreRestTransport._BaseGetPartnerPermissions,
        CloudControlsPartnerCoreRestStub,
    ):
        def __hash__(self):
            return hash("CloudControlsPartnerCoreRestTransport.GetPartnerPermissions")

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
            request: partner_permissions.GetPartnerPermissionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> partner_permissions.PartnerPermissions:
            r"""Call the get partner permissions method over HTTP.

            Args:
                request (~.partner_permissions.GetPartnerPermissionsRequest):
                    The request object. Request for getting the partner
                permissions granted for a workload
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.partner_permissions.PartnerPermissions:
                    The permissions granted to the
                partner for a workload

            """

            http_options = (
                _BaseCloudControlsPartnerCoreRestTransport._BaseGetPartnerPermissions._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_partner_permissions(
                request, metadata
            )
            transcoded_request = _BaseCloudControlsPartnerCoreRestTransport._BaseGetPartnerPermissions._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudControlsPartnerCoreRestTransport._BaseGetPartnerPermissions._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CloudControlsPartnerCoreRestTransport._GetPartnerPermissions._get_response(
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
            resp = partner_permissions.PartnerPermissions()
            pb_resp = partner_permissions.PartnerPermissions.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_partner_permissions(resp)
            return resp

    class _GetWorkload(
        _BaseCloudControlsPartnerCoreRestTransport._BaseGetWorkload,
        CloudControlsPartnerCoreRestStub,
    ):
        def __hash__(self):
            return hash("CloudControlsPartnerCoreRestTransport.GetWorkload")

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
            request: customer_workloads.GetWorkloadRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> customer_workloads.Workload:
            r"""Call the get workload method over HTTP.

            Args:
                request (~.customer_workloads.GetWorkloadRequest):
                    The request object. Message for getting a customer
                workload.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.customer_workloads.Workload:
                    Contains metadata around the `Workload
                resource <https://cloud.google.com/assured-workloads/docs/reference/rest/Shared.Types/Workload>`__
                in the Assured Workloads API.

            """

            http_options = (
                _BaseCloudControlsPartnerCoreRestTransport._BaseGetWorkload._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_workload(request, metadata)
            transcoded_request = _BaseCloudControlsPartnerCoreRestTransport._BaseGetWorkload._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudControlsPartnerCoreRestTransport._BaseGetWorkload._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CloudControlsPartnerCoreRestTransport._GetWorkload._get_response(
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
            resp = customer_workloads.Workload()
            pb_resp = customer_workloads.Workload.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_workload(resp)
            return resp

    class _ListAccessApprovalRequests(
        _BaseCloudControlsPartnerCoreRestTransport._BaseListAccessApprovalRequests,
        CloudControlsPartnerCoreRestStub,
    ):
        def __hash__(self):
            return hash(
                "CloudControlsPartnerCoreRestTransport.ListAccessApprovalRequests"
            )

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
            request: access_approval_requests.ListAccessApprovalRequestsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> access_approval_requests.ListAccessApprovalRequestsResponse:
            r"""Call the list access approval
            requests method over HTTP.

                Args:
                    request (~.access_approval_requests.ListAccessApprovalRequestsRequest):
                        The request object. Request for getting the access
                    requests associated with a workload.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.access_approval_requests.ListAccessApprovalRequestsResponse:
                        Response message for list access
                    requests.

            """

            http_options = (
                _BaseCloudControlsPartnerCoreRestTransport._BaseListAccessApprovalRequests._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_access_approval_requests(
                request, metadata
            )
            transcoded_request = _BaseCloudControlsPartnerCoreRestTransport._BaseListAccessApprovalRequests._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudControlsPartnerCoreRestTransport._BaseListAccessApprovalRequests._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CloudControlsPartnerCoreRestTransport._ListAccessApprovalRequests._get_response(
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
            resp = access_approval_requests.ListAccessApprovalRequestsResponse()
            pb_resp = access_approval_requests.ListAccessApprovalRequestsResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_access_approval_requests(resp)
            return resp

    class _ListCustomers(
        _BaseCloudControlsPartnerCoreRestTransport._BaseListCustomers,
        CloudControlsPartnerCoreRestStub,
    ):
        def __hash__(self):
            return hash("CloudControlsPartnerCoreRestTransport.ListCustomers")

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
            request: customers.ListCustomersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> customers.ListCustomersResponse:
            r"""Call the list customers method over HTTP.

            Args:
                request (~.customers.ListCustomersRequest):
                    The request object. Request to list customers
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.customers.ListCustomersResponse:
                    Response message for list customer
                Customers requests

            """

            http_options = (
                _BaseCloudControlsPartnerCoreRestTransport._BaseListCustomers._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_customers(request, metadata)
            transcoded_request = _BaseCloudControlsPartnerCoreRestTransport._BaseListCustomers._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudControlsPartnerCoreRestTransport._BaseListCustomers._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                CloudControlsPartnerCoreRestTransport._ListCustomers._get_response(
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
            resp = customers.ListCustomersResponse()
            pb_resp = customers.ListCustomersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_customers(resp)
            return resp

    class _ListWorkloads(
        _BaseCloudControlsPartnerCoreRestTransport._BaseListWorkloads,
        CloudControlsPartnerCoreRestStub,
    ):
        def __hash__(self):
            return hash("CloudControlsPartnerCoreRestTransport.ListWorkloads")

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
            request: customer_workloads.ListWorkloadsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> customer_workloads.ListWorkloadsResponse:
            r"""Call the list workloads method over HTTP.

            Args:
                request (~.customer_workloads.ListWorkloadsRequest):
                    The request object. Request to list customer workloads.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.customer_workloads.ListWorkloadsResponse:
                    Response message for list customer
                workloads requests.

            """

            http_options = (
                _BaseCloudControlsPartnerCoreRestTransport._BaseListWorkloads._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_workloads(request, metadata)
            transcoded_request = _BaseCloudControlsPartnerCoreRestTransport._BaseListWorkloads._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudControlsPartnerCoreRestTransport._BaseListWorkloads._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                CloudControlsPartnerCoreRestTransport._ListWorkloads._get_response(
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
            resp = customer_workloads.ListWorkloadsResponse()
            pb_resp = customer_workloads.ListWorkloadsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_workloads(resp)
            return resp

    @property
    def get_customer(
        self,
    ) -> Callable[[customers.GetCustomerRequest], customers.Customer]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCustomer(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_ekm_connections(
        self,
    ) -> Callable[
        [ekm_connections.GetEkmConnectionsRequest], ekm_connections.EkmConnections
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEkmConnections(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_partner(self) -> Callable[[partners.GetPartnerRequest], partners.Partner]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPartner(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_partner_permissions(
        self,
    ) -> Callable[
        [partner_permissions.GetPartnerPermissionsRequest],
        partner_permissions.PartnerPermissions,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPartnerPermissions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_workload(
        self,
    ) -> Callable[[customer_workloads.GetWorkloadRequest], customer_workloads.Workload]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetWorkload(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_access_approval_requests(
        self,
    ) -> Callable[
        [access_approval_requests.ListAccessApprovalRequestsRequest],
        access_approval_requests.ListAccessApprovalRequestsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAccessApprovalRequests(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_customers(
        self,
    ) -> Callable[[customers.ListCustomersRequest], customers.ListCustomersResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCustomers(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_workloads(
        self,
    ) -> Callable[
        [customer_workloads.ListWorkloadsRequest],
        customer_workloads.ListWorkloadsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListWorkloads(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("CloudControlsPartnerCoreRestTransport",)
