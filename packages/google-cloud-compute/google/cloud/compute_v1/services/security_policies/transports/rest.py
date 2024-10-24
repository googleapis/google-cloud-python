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

from google.cloud.compute_v1.types import compute

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseSecurityPoliciesRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class SecurityPoliciesRestInterceptor:
    """Interceptor for SecurityPolicies.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the SecurityPoliciesRestTransport.

    .. code-block:: python
        class MyCustomSecurityPoliciesInterceptor(SecurityPoliciesRestInterceptor):
            def pre_add_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_add_rule(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_aggregated_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_aggregated_list(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_rule(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_insert(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_insert(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_preconfigured_expression_sets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_preconfigured_expression_sets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_patch(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_patch(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_patch_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_patch_rule(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_remove_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_remove_rule(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_labels(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_labels(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = SecurityPoliciesRestTransport(interceptor=MyCustomSecurityPoliciesInterceptor())
        client = SecurityPoliciesClient(transport=transport)


    """

    def pre_add_rule(
        self,
        request: compute.AddRuleSecurityPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.AddRuleSecurityPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for add_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityPolicies server.
        """
        return request, metadata

    def post_add_rule(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for add_rule

        Override in a subclass to manipulate the response
        after it is returned by the SecurityPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_aggregated_list(
        self,
        request: compute.AggregatedListSecurityPoliciesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.AggregatedListSecurityPoliciesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for aggregated_list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityPolicies server.
        """
        return request, metadata

    def post_aggregated_list(
        self, response: compute.SecurityPoliciesAggregatedList
    ) -> compute.SecurityPoliciesAggregatedList:
        """Post-rpc interceptor for aggregated_list

        Override in a subclass to manipulate the response
        after it is returned by the SecurityPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_delete(
        self,
        request: compute.DeleteSecurityPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.DeleteSecurityPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityPolicies server.
        """
        return request, metadata

    def post_delete(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for delete

        Override in a subclass to manipulate the response
        after it is returned by the SecurityPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_get(
        self,
        request: compute.GetSecurityPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.GetSecurityPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityPolicies server.
        """
        return request, metadata

    def post_get(self, response: compute.SecurityPolicy) -> compute.SecurityPolicy:
        """Post-rpc interceptor for get

        Override in a subclass to manipulate the response
        after it is returned by the SecurityPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_get_rule(
        self,
        request: compute.GetRuleSecurityPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.GetRuleSecurityPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityPolicies server.
        """
        return request, metadata

    def post_get_rule(
        self, response: compute.SecurityPolicyRule
    ) -> compute.SecurityPolicyRule:
        """Post-rpc interceptor for get_rule

        Override in a subclass to manipulate the response
        after it is returned by the SecurityPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_insert(
        self,
        request: compute.InsertSecurityPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.InsertSecurityPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for insert

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityPolicies server.
        """
        return request, metadata

    def post_insert(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for insert

        Override in a subclass to manipulate the response
        after it is returned by the SecurityPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_list(
        self,
        request: compute.ListSecurityPoliciesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.ListSecurityPoliciesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityPolicies server.
        """
        return request, metadata

    def post_list(
        self, response: compute.SecurityPolicyList
    ) -> compute.SecurityPolicyList:
        """Post-rpc interceptor for list

        Override in a subclass to manipulate the response
        after it is returned by the SecurityPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_list_preconfigured_expression_sets(
        self,
        request: compute.ListPreconfiguredExpressionSetsSecurityPoliciesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.ListPreconfiguredExpressionSetsSecurityPoliciesRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_preconfigured_expression_sets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityPolicies server.
        """
        return request, metadata

    def post_list_preconfigured_expression_sets(
        self, response: compute.SecurityPoliciesListPreconfiguredExpressionSetsResponse
    ) -> compute.SecurityPoliciesListPreconfiguredExpressionSetsResponse:
        """Post-rpc interceptor for list_preconfigured_expression_sets

        Override in a subclass to manipulate the response
        after it is returned by the SecurityPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_patch(
        self,
        request: compute.PatchSecurityPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.PatchSecurityPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for patch

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityPolicies server.
        """
        return request, metadata

    def post_patch(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for patch

        Override in a subclass to manipulate the response
        after it is returned by the SecurityPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_patch_rule(
        self,
        request: compute.PatchRuleSecurityPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.PatchRuleSecurityPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for patch_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityPolicies server.
        """
        return request, metadata

    def post_patch_rule(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for patch_rule

        Override in a subclass to manipulate the response
        after it is returned by the SecurityPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_remove_rule(
        self,
        request: compute.RemoveRuleSecurityPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.RemoveRuleSecurityPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for remove_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityPolicies server.
        """
        return request, metadata

    def post_remove_rule(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for remove_rule

        Override in a subclass to manipulate the response
        after it is returned by the SecurityPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_set_labels(
        self,
        request: compute.SetLabelsSecurityPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.SetLabelsSecurityPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_labels

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityPolicies server.
        """
        return request, metadata

    def post_set_labels(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for set_labels

        Override in a subclass to manipulate the response
        after it is returned by the SecurityPolicies server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class SecurityPoliciesRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: SecurityPoliciesRestInterceptor


class SecurityPoliciesRestTransport(_BaseSecurityPoliciesRestTransport):
    """REST backend synchronous transport for SecurityPolicies.

    The SecurityPolicies API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "compute.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[SecurityPoliciesRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        NOTE: This REST transport functionality is currently in a beta
        state (preview). We welcome your feedback via a GitHub issue in
        this library's repository. Thank you!

         Args:
             host (Optional[str]):
                  The hostname to connect to (default: 'compute.googleapis.com').
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
        self._interceptor = interceptor or SecurityPoliciesRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AddRule(
        _BaseSecurityPoliciesRestTransport._BaseAddRule, SecurityPoliciesRestStub
    ):
        def __hash__(self):
            return hash("SecurityPoliciesRestTransport.AddRule")

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
            request: compute.AddRuleSecurityPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the add rule method over HTTP.

            Args:
                request (~.compute.AddRuleSecurityPolicyRequest):
                    The request object. A request message for
                SecurityPolicies.AddRule. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options = (
                _BaseSecurityPoliciesRestTransport._BaseAddRule._get_http_options()
            )
            request, metadata = self._interceptor.pre_add_rule(request, metadata)
            transcoded_request = (
                _BaseSecurityPoliciesRestTransport._BaseAddRule._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseSecurityPoliciesRestTransport._BaseAddRule._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSecurityPoliciesRestTransport._BaseAddRule._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SecurityPoliciesRestTransport._AddRule._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_add_rule(resp)
            return resp

    class _AggregatedList(
        _BaseSecurityPoliciesRestTransport._BaseAggregatedList, SecurityPoliciesRestStub
    ):
        def __hash__(self):
            return hash("SecurityPoliciesRestTransport.AggregatedList")

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
            request: compute.AggregatedListSecurityPoliciesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.SecurityPoliciesAggregatedList:
            r"""Call the aggregated list method over HTTP.

            Args:
                request (~.compute.AggregatedListSecurityPoliciesRequest):
                    The request object. A request message for
                SecurityPolicies.AggregatedList. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.SecurityPoliciesAggregatedList:

            """

            http_options = (
                _BaseSecurityPoliciesRestTransport._BaseAggregatedList._get_http_options()
            )
            request, metadata = self._interceptor.pre_aggregated_list(request, metadata)
            transcoded_request = _BaseSecurityPoliciesRestTransport._BaseAggregatedList._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityPoliciesRestTransport._BaseAggregatedList._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityPoliciesRestTransport._AggregatedList._get_response(
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
            resp = compute.SecurityPoliciesAggregatedList()
            pb_resp = compute.SecurityPoliciesAggregatedList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_aggregated_list(resp)
            return resp

    class _Delete(
        _BaseSecurityPoliciesRestTransport._BaseDelete, SecurityPoliciesRestStub
    ):
        def __hash__(self):
            return hash("SecurityPoliciesRestTransport.Delete")

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
            request: compute.DeleteSecurityPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the delete method over HTTP.

            Args:
                request (~.compute.DeleteSecurityPolicyRequest):
                    The request object. A request message for
                SecurityPolicies.Delete. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options = (
                _BaseSecurityPoliciesRestTransport._BaseDelete._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete(request, metadata)
            transcoded_request = (
                _BaseSecurityPoliciesRestTransport._BaseDelete._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSecurityPoliciesRestTransport._BaseDelete._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SecurityPoliciesRestTransport._Delete._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete(resp)
            return resp

    class _Get(_BaseSecurityPoliciesRestTransport._BaseGet, SecurityPoliciesRestStub):
        def __hash__(self):
            return hash("SecurityPoliciesRestTransport.Get")

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
            request: compute.GetSecurityPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.SecurityPolicy:
            r"""Call the get method over HTTP.

            Args:
                request (~.compute.GetSecurityPolicyRequest):
                    The request object. A request message for
                SecurityPolicies.Get. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.SecurityPolicy:
                    Represents a Google Cloud Armor
                security policy resource. Only external
                backend services that use load balancers
                can reference a security policy. For
                more information, see Google Cloud Armor
                security policy overview.

            """

            http_options = (
                _BaseSecurityPoliciesRestTransport._BaseGet._get_http_options()
            )
            request, metadata = self._interceptor.pre_get(request, metadata)
            transcoded_request = (
                _BaseSecurityPoliciesRestTransport._BaseGet._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSecurityPoliciesRestTransport._BaseGet._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SecurityPoliciesRestTransport._Get._get_response(
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
            resp = compute.SecurityPolicy()
            pb_resp = compute.SecurityPolicy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get(resp)
            return resp

    class _GetRule(
        _BaseSecurityPoliciesRestTransport._BaseGetRule, SecurityPoliciesRestStub
    ):
        def __hash__(self):
            return hash("SecurityPoliciesRestTransport.GetRule")

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
            request: compute.GetRuleSecurityPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.SecurityPolicyRule:
            r"""Call the get rule method over HTTP.

            Args:
                request (~.compute.GetRuleSecurityPolicyRequest):
                    The request object. A request message for
                SecurityPolicies.GetRule. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.SecurityPolicyRule:
                    Represents a rule that describes one
                or more match conditions along with the
                action to be taken when traffic matches
                this condition (allow or deny).

            """

            http_options = (
                _BaseSecurityPoliciesRestTransport._BaseGetRule._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_rule(request, metadata)
            transcoded_request = (
                _BaseSecurityPoliciesRestTransport._BaseGetRule._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSecurityPoliciesRestTransport._BaseGetRule._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SecurityPoliciesRestTransport._GetRule._get_response(
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
            resp = compute.SecurityPolicyRule()
            pb_resp = compute.SecurityPolicyRule.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_rule(resp)
            return resp

    class _Insert(
        _BaseSecurityPoliciesRestTransport._BaseInsert, SecurityPoliciesRestStub
    ):
        def __hash__(self):
            return hash("SecurityPoliciesRestTransport.Insert")

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
            request: compute.InsertSecurityPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the insert method over HTTP.

            Args:
                request (~.compute.InsertSecurityPolicyRequest):
                    The request object. A request message for
                SecurityPolicies.Insert. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options = (
                _BaseSecurityPoliciesRestTransport._BaseInsert._get_http_options()
            )
            request, metadata = self._interceptor.pre_insert(request, metadata)
            transcoded_request = (
                _BaseSecurityPoliciesRestTransport._BaseInsert._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseSecurityPoliciesRestTransport._BaseInsert._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSecurityPoliciesRestTransport._BaseInsert._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SecurityPoliciesRestTransport._Insert._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_insert(resp)
            return resp

    class _List(_BaseSecurityPoliciesRestTransport._BaseList, SecurityPoliciesRestStub):
        def __hash__(self):
            return hash("SecurityPoliciesRestTransport.List")

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
            request: compute.ListSecurityPoliciesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.SecurityPolicyList:
            r"""Call the list method over HTTP.

            Args:
                request (~.compute.ListSecurityPoliciesRequest):
                    The request object. A request message for
                SecurityPolicies.List. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.SecurityPolicyList:

            """

            http_options = (
                _BaseSecurityPoliciesRestTransport._BaseList._get_http_options()
            )
            request, metadata = self._interceptor.pre_list(request, metadata)
            transcoded_request = (
                _BaseSecurityPoliciesRestTransport._BaseList._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSecurityPoliciesRestTransport._BaseList._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SecurityPoliciesRestTransport._List._get_response(
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
            resp = compute.SecurityPolicyList()
            pb_resp = compute.SecurityPolicyList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list(resp)
            return resp

    class _ListPreconfiguredExpressionSets(
        _BaseSecurityPoliciesRestTransport._BaseListPreconfiguredExpressionSets,
        SecurityPoliciesRestStub,
    ):
        def __hash__(self):
            return hash("SecurityPoliciesRestTransport.ListPreconfiguredExpressionSets")

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
            request: compute.ListPreconfiguredExpressionSetsSecurityPoliciesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.SecurityPoliciesListPreconfiguredExpressionSetsResponse:
            r"""Call the list preconfigured
            expression sets method over HTTP.

                Args:
                    request (~.compute.ListPreconfiguredExpressionSetsSecurityPoliciesRequest):
                        The request object. A request message for
                    SecurityPolicies.ListPreconfiguredExpressionSets.
                    See the method description for details.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.compute.SecurityPoliciesListPreconfiguredExpressionSetsResponse:

            """

            http_options = (
                _BaseSecurityPoliciesRestTransport._BaseListPreconfiguredExpressionSets._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_list_preconfigured_expression_sets(
                request, metadata
            )
            transcoded_request = _BaseSecurityPoliciesRestTransport._BaseListPreconfiguredExpressionSets._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityPoliciesRestTransport._BaseListPreconfiguredExpressionSets._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityPoliciesRestTransport._ListPreconfiguredExpressionSets._get_response(
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
            resp = compute.SecurityPoliciesListPreconfiguredExpressionSetsResponse()
            pb_resp = (
                compute.SecurityPoliciesListPreconfiguredExpressionSetsResponse.pb(resp)
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_preconfigured_expression_sets(resp)
            return resp

    class _Patch(
        _BaseSecurityPoliciesRestTransport._BasePatch, SecurityPoliciesRestStub
    ):
        def __hash__(self):
            return hash("SecurityPoliciesRestTransport.Patch")

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
            request: compute.PatchSecurityPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the patch method over HTTP.

            Args:
                request (~.compute.PatchSecurityPolicyRequest):
                    The request object. A request message for
                SecurityPolicies.Patch. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options = (
                _BaseSecurityPoliciesRestTransport._BasePatch._get_http_options()
            )
            request, metadata = self._interceptor.pre_patch(request, metadata)
            transcoded_request = (
                _BaseSecurityPoliciesRestTransport._BasePatch._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseSecurityPoliciesRestTransport._BasePatch._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseSecurityPoliciesRestTransport._BasePatch._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SecurityPoliciesRestTransport._Patch._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_patch(resp)
            return resp

    class _PatchRule(
        _BaseSecurityPoliciesRestTransport._BasePatchRule, SecurityPoliciesRestStub
    ):
        def __hash__(self):
            return hash("SecurityPoliciesRestTransport.PatchRule")

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
            request: compute.PatchRuleSecurityPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the patch rule method over HTTP.

            Args:
                request (~.compute.PatchRuleSecurityPolicyRequest):
                    The request object. A request message for
                SecurityPolicies.PatchRule. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options = (
                _BaseSecurityPoliciesRestTransport._BasePatchRule._get_http_options()
            )
            request, metadata = self._interceptor.pre_patch_rule(request, metadata)
            transcoded_request = _BaseSecurityPoliciesRestTransport._BasePatchRule._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityPoliciesRestTransport._BasePatchRule._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityPoliciesRestTransport._BasePatchRule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityPoliciesRestTransport._PatchRule._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_patch_rule(resp)
            return resp

    class _RemoveRule(
        _BaseSecurityPoliciesRestTransport._BaseRemoveRule, SecurityPoliciesRestStub
    ):
        def __hash__(self):
            return hash("SecurityPoliciesRestTransport.RemoveRule")

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
            request: compute.RemoveRuleSecurityPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the remove rule method over HTTP.

            Args:
                request (~.compute.RemoveRuleSecurityPolicyRequest):
                    The request object. A request message for
                SecurityPolicies.RemoveRule. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options = (
                _BaseSecurityPoliciesRestTransport._BaseRemoveRule._get_http_options()
            )
            request, metadata = self._interceptor.pre_remove_rule(request, metadata)
            transcoded_request = _BaseSecurityPoliciesRestTransport._BaseRemoveRule._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityPoliciesRestTransport._BaseRemoveRule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityPoliciesRestTransport._RemoveRule._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_remove_rule(resp)
            return resp

    class _SetLabels(
        _BaseSecurityPoliciesRestTransport._BaseSetLabels, SecurityPoliciesRestStub
    ):
        def __hash__(self):
            return hash("SecurityPoliciesRestTransport.SetLabels")

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
            request: compute.SetLabelsSecurityPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set labels method over HTTP.

            Args:
                request (~.compute.SetLabelsSecurityPolicyRequest):
                    The request object. A request message for
                SecurityPolicies.SetLabels. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options = (
                _BaseSecurityPoliciesRestTransport._BaseSetLabels._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_labels(request, metadata)
            transcoded_request = _BaseSecurityPoliciesRestTransport._BaseSetLabels._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityPoliciesRestTransport._BaseSetLabels._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityPoliciesRestTransport._BaseSetLabels._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityPoliciesRestTransport._SetLabels._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_labels(resp)
            return resp

    @property
    def add_rule(
        self,
    ) -> Callable[[compute.AddRuleSecurityPolicyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AddRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def aggregated_list(
        self,
    ) -> Callable[
        [compute.AggregatedListSecurityPoliciesRequest],
        compute.SecurityPoliciesAggregatedList,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AggregatedList(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete(
        self,
    ) -> Callable[[compute.DeleteSecurityPolicyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Delete(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get(
        self,
    ) -> Callable[[compute.GetSecurityPolicyRequest], compute.SecurityPolicy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Get(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_rule(
        self,
    ) -> Callable[[compute.GetRuleSecurityPolicyRequest], compute.SecurityPolicyRule]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def insert(
        self,
    ) -> Callable[[compute.InsertSecurityPolicyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Insert(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list(
        self,
    ) -> Callable[[compute.ListSecurityPoliciesRequest], compute.SecurityPolicyList]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._List(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_preconfigured_expression_sets(
        self,
    ) -> Callable[
        [compute.ListPreconfiguredExpressionSetsSecurityPoliciesRequest],
        compute.SecurityPoliciesListPreconfiguredExpressionSetsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPreconfiguredExpressionSets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def patch(
        self,
    ) -> Callable[[compute.PatchSecurityPolicyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Patch(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def patch_rule(
        self,
    ) -> Callable[[compute.PatchRuleSecurityPolicyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PatchRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def remove_rule(
        self,
    ) -> Callable[[compute.RemoveRuleSecurityPolicyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemoveRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_labels(
        self,
    ) -> Callable[[compute.SetLabelsSecurityPolicyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetLabels(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("SecurityPoliciesRestTransport",)
