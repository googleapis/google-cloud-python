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
from .rest_base import _BaseRegionNetworkFirewallPoliciesRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class RegionNetworkFirewallPoliciesRestInterceptor:
    """Interceptor for RegionNetworkFirewallPolicies.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the RegionNetworkFirewallPoliciesRestTransport.

    .. code-block:: python
        class MyCustomRegionNetworkFirewallPoliciesInterceptor(RegionNetworkFirewallPoliciesRestInterceptor):
            def pre_add_association(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_add_association(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_add_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_add_rule(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_clone_rules(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_clone_rules(self, response):
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

            def pre_get_association(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_association(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_effective_firewalls(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_effective_firewalls(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_iam_policy(self, response):
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

            def pre_remove_association(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_remove_association(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_remove_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_remove_rule(self, response):
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

        transport = RegionNetworkFirewallPoliciesRestTransport(interceptor=MyCustomRegionNetworkFirewallPoliciesInterceptor())
        client = RegionNetworkFirewallPoliciesClient(transport=transport)


    """

    def pre_add_association(
        self,
        request: compute.AddAssociationRegionNetworkFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.AddAssociationRegionNetworkFirewallPolicyRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for add_association

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionNetworkFirewallPolicies server.
        """
        return request, metadata

    def post_add_association(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for add_association

        Override in a subclass to manipulate the response
        after it is returned by the RegionNetworkFirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_add_rule(
        self,
        request: compute.AddRuleRegionNetworkFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.AddRuleRegionNetworkFirewallPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for add_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionNetworkFirewallPolicies server.
        """
        return request, metadata

    def post_add_rule(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for add_rule

        Override in a subclass to manipulate the response
        after it is returned by the RegionNetworkFirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_clone_rules(
        self,
        request: compute.CloneRulesRegionNetworkFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.CloneRulesRegionNetworkFirewallPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for clone_rules

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionNetworkFirewallPolicies server.
        """
        return request, metadata

    def post_clone_rules(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for clone_rules

        Override in a subclass to manipulate the response
        after it is returned by the RegionNetworkFirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_delete(
        self,
        request: compute.DeleteRegionNetworkFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.DeleteRegionNetworkFirewallPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionNetworkFirewallPolicies server.
        """
        return request, metadata

    def post_delete(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for delete

        Override in a subclass to manipulate the response
        after it is returned by the RegionNetworkFirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_get(
        self,
        request: compute.GetRegionNetworkFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.GetRegionNetworkFirewallPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionNetworkFirewallPolicies server.
        """
        return request, metadata

    def post_get(self, response: compute.FirewallPolicy) -> compute.FirewallPolicy:
        """Post-rpc interceptor for get

        Override in a subclass to manipulate the response
        after it is returned by the RegionNetworkFirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_get_association(
        self,
        request: compute.GetAssociationRegionNetworkFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.GetAssociationRegionNetworkFirewallPolicyRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for get_association

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionNetworkFirewallPolicies server.
        """
        return request, metadata

    def post_get_association(
        self, response: compute.FirewallPolicyAssociation
    ) -> compute.FirewallPolicyAssociation:
        """Post-rpc interceptor for get_association

        Override in a subclass to manipulate the response
        after it is returned by the RegionNetworkFirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_get_effective_firewalls(
        self,
        request: compute.GetEffectiveFirewallsRegionNetworkFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.GetEffectiveFirewallsRegionNetworkFirewallPolicyRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for get_effective_firewalls

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionNetworkFirewallPolicies server.
        """
        return request, metadata

    def post_get_effective_firewalls(
        self,
        response: compute.RegionNetworkFirewallPoliciesGetEffectiveFirewallsResponse,
    ) -> compute.RegionNetworkFirewallPoliciesGetEffectiveFirewallsResponse:
        """Post-rpc interceptor for get_effective_firewalls

        Override in a subclass to manipulate the response
        after it is returned by the RegionNetworkFirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_get_iam_policy(
        self,
        request: compute.GetIamPolicyRegionNetworkFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.GetIamPolicyRegionNetworkFirewallPolicyRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionNetworkFirewallPolicies server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: compute.Policy) -> compute.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the RegionNetworkFirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_get_rule(
        self,
        request: compute.GetRuleRegionNetworkFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.GetRuleRegionNetworkFirewallPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionNetworkFirewallPolicies server.
        """
        return request, metadata

    def post_get_rule(
        self, response: compute.FirewallPolicyRule
    ) -> compute.FirewallPolicyRule:
        """Post-rpc interceptor for get_rule

        Override in a subclass to manipulate the response
        after it is returned by the RegionNetworkFirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_insert(
        self,
        request: compute.InsertRegionNetworkFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.InsertRegionNetworkFirewallPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for insert

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionNetworkFirewallPolicies server.
        """
        return request, metadata

    def post_insert(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for insert

        Override in a subclass to manipulate the response
        after it is returned by the RegionNetworkFirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_list(
        self,
        request: compute.ListRegionNetworkFirewallPoliciesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.ListRegionNetworkFirewallPoliciesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionNetworkFirewallPolicies server.
        """
        return request, metadata

    def post_list(
        self, response: compute.FirewallPolicyList
    ) -> compute.FirewallPolicyList:
        """Post-rpc interceptor for list

        Override in a subclass to manipulate the response
        after it is returned by the RegionNetworkFirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_patch(
        self,
        request: compute.PatchRegionNetworkFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.PatchRegionNetworkFirewallPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for patch

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionNetworkFirewallPolicies server.
        """
        return request, metadata

    def post_patch(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for patch

        Override in a subclass to manipulate the response
        after it is returned by the RegionNetworkFirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_patch_rule(
        self,
        request: compute.PatchRuleRegionNetworkFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.PatchRuleRegionNetworkFirewallPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for patch_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionNetworkFirewallPolicies server.
        """
        return request, metadata

    def post_patch_rule(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for patch_rule

        Override in a subclass to manipulate the response
        after it is returned by the RegionNetworkFirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_remove_association(
        self,
        request: compute.RemoveAssociationRegionNetworkFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.RemoveAssociationRegionNetworkFirewallPolicyRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for remove_association

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionNetworkFirewallPolicies server.
        """
        return request, metadata

    def post_remove_association(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for remove_association

        Override in a subclass to manipulate the response
        after it is returned by the RegionNetworkFirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_remove_rule(
        self,
        request: compute.RemoveRuleRegionNetworkFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.RemoveRuleRegionNetworkFirewallPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for remove_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionNetworkFirewallPolicies server.
        """
        return request, metadata

    def post_remove_rule(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for remove_rule

        Override in a subclass to manipulate the response
        after it is returned by the RegionNetworkFirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_set_iam_policy(
        self,
        request: compute.SetIamPolicyRegionNetworkFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.SetIamPolicyRegionNetworkFirewallPolicyRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionNetworkFirewallPolicies server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: compute.Policy) -> compute.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the RegionNetworkFirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_test_iam_permissions(
        self,
        request: compute.TestIamPermissionsRegionNetworkFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.TestIamPermissionsRegionNetworkFirewallPolicyRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionNetworkFirewallPolicies server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: compute.TestPermissionsResponse
    ) -> compute.TestPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the RegionNetworkFirewallPolicies server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class RegionNetworkFirewallPoliciesRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: RegionNetworkFirewallPoliciesRestInterceptor


class RegionNetworkFirewallPoliciesRestTransport(
    _BaseRegionNetworkFirewallPoliciesRestTransport
):
    """REST backend synchronous transport for RegionNetworkFirewallPolicies.

    The RegionNetworkFirewallPolicies API.

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
        interceptor: Optional[RegionNetworkFirewallPoliciesRestInterceptor] = None,
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
        self._interceptor = (
            interceptor or RegionNetworkFirewallPoliciesRestInterceptor()
        )
        self._prep_wrapped_messages(client_info)

    class _AddAssociation(
        _BaseRegionNetworkFirewallPoliciesRestTransport._BaseAddAssociation,
        RegionNetworkFirewallPoliciesRestStub,
    ):
        def __hash__(self):
            return hash("RegionNetworkFirewallPoliciesRestTransport.AddAssociation")

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
            request: compute.AddAssociationRegionNetworkFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the add association method over HTTP.

            Args:
                request (~.compute.AddAssociationRegionNetworkFirewallPolicyRequest):
                    The request object. A request message for
                RegionNetworkFirewallPolicies.AddAssociation.
                See the method description for details.
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
                _BaseRegionNetworkFirewallPoliciesRestTransport._BaseAddAssociation._get_http_options()
            )
            request, metadata = self._interceptor.pre_add_association(request, metadata)
            transcoded_request = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseAddAssociation._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseAddAssociation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseAddAssociation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionNetworkFirewallPoliciesRestTransport._AddAssociation._get_response(
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
            resp = self._interceptor.post_add_association(resp)
            return resp

    class _AddRule(
        _BaseRegionNetworkFirewallPoliciesRestTransport._BaseAddRule,
        RegionNetworkFirewallPoliciesRestStub,
    ):
        def __hash__(self):
            return hash("RegionNetworkFirewallPoliciesRestTransport.AddRule")

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
            request: compute.AddRuleRegionNetworkFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the add rule method over HTTP.

            Args:
                request (~.compute.AddRuleRegionNetworkFirewallPolicyRequest):
                    The request object. A request message for
                RegionNetworkFirewallPolicies.AddRule.
                See the method description for details.
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
                _BaseRegionNetworkFirewallPoliciesRestTransport._BaseAddRule._get_http_options()
            )
            request, metadata = self._interceptor.pre_add_rule(request, metadata)
            transcoded_request = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseAddRule._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseAddRule._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseAddRule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RegionNetworkFirewallPoliciesRestTransport._AddRule._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_add_rule(resp)
            return resp

    class _CloneRules(
        _BaseRegionNetworkFirewallPoliciesRestTransport._BaseCloneRules,
        RegionNetworkFirewallPoliciesRestStub,
    ):
        def __hash__(self):
            return hash("RegionNetworkFirewallPoliciesRestTransport.CloneRules")

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
            request: compute.CloneRulesRegionNetworkFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the clone rules method over HTTP.

            Args:
                request (~.compute.CloneRulesRegionNetworkFirewallPolicyRequest):
                    The request object. A request message for
                RegionNetworkFirewallPolicies.CloneRules.
                See the method description for details.
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
                _BaseRegionNetworkFirewallPoliciesRestTransport._BaseCloneRules._get_http_options()
            )
            request, metadata = self._interceptor.pre_clone_rules(request, metadata)
            transcoded_request = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseCloneRules._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseCloneRules._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RegionNetworkFirewallPoliciesRestTransport._CloneRules._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_clone_rules(resp)
            return resp

    class _Delete(
        _BaseRegionNetworkFirewallPoliciesRestTransport._BaseDelete,
        RegionNetworkFirewallPoliciesRestStub,
    ):
        def __hash__(self):
            return hash("RegionNetworkFirewallPoliciesRestTransport.Delete")

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
            request: compute.DeleteRegionNetworkFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the delete method over HTTP.

            Args:
                request (~.compute.DeleteRegionNetworkFirewallPolicyRequest):
                    The request object. A request message for
                RegionNetworkFirewallPolicies.Delete.
                See the method description for details.
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
                _BaseRegionNetworkFirewallPoliciesRestTransport._BaseDelete._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete(request, metadata)
            transcoded_request = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseDelete._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseDelete._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionNetworkFirewallPoliciesRestTransport._Delete._get_response(
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

    class _Get(
        _BaseRegionNetworkFirewallPoliciesRestTransport._BaseGet,
        RegionNetworkFirewallPoliciesRestStub,
    ):
        def __hash__(self):
            return hash("RegionNetworkFirewallPoliciesRestTransport.Get")

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
            request: compute.GetRegionNetworkFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.FirewallPolicy:
            r"""Call the get method over HTTP.

            Args:
                request (~.compute.GetRegionNetworkFirewallPolicyRequest):
                    The request object. A request message for
                RegionNetworkFirewallPolicies.Get. See
                the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.FirewallPolicy:
                    Represents a Firewall Policy
                resource.

            """

            http_options = (
                _BaseRegionNetworkFirewallPoliciesRestTransport._BaseGet._get_http_options()
            )
            request, metadata = self._interceptor.pre_get(request, metadata)
            transcoded_request = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseGet._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseGet._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionNetworkFirewallPoliciesRestTransport._Get._get_response(
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
            resp = compute.FirewallPolicy()
            pb_resp = compute.FirewallPolicy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get(resp)
            return resp

    class _GetAssociation(
        _BaseRegionNetworkFirewallPoliciesRestTransport._BaseGetAssociation,
        RegionNetworkFirewallPoliciesRestStub,
    ):
        def __hash__(self):
            return hash("RegionNetworkFirewallPoliciesRestTransport.GetAssociation")

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
            request: compute.GetAssociationRegionNetworkFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.FirewallPolicyAssociation:
            r"""Call the get association method over HTTP.

            Args:
                request (~.compute.GetAssociationRegionNetworkFirewallPolicyRequest):
                    The request object. A request message for
                RegionNetworkFirewallPolicies.GetAssociation.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.FirewallPolicyAssociation:

            """

            http_options = (
                _BaseRegionNetworkFirewallPoliciesRestTransport._BaseGetAssociation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_association(request, metadata)
            transcoded_request = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseGetAssociation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseGetAssociation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionNetworkFirewallPoliciesRestTransport._GetAssociation._get_response(
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
            resp = compute.FirewallPolicyAssociation()
            pb_resp = compute.FirewallPolicyAssociation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_association(resp)
            return resp

    class _GetEffectiveFirewalls(
        _BaseRegionNetworkFirewallPoliciesRestTransport._BaseGetEffectiveFirewalls,
        RegionNetworkFirewallPoliciesRestStub,
    ):
        def __hash__(self):
            return hash(
                "RegionNetworkFirewallPoliciesRestTransport.GetEffectiveFirewalls"
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
            request: compute.GetEffectiveFirewallsRegionNetworkFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.RegionNetworkFirewallPoliciesGetEffectiveFirewallsResponse:
            r"""Call the get effective firewalls method over HTTP.

            Args:
                request (~.compute.GetEffectiveFirewallsRegionNetworkFirewallPolicyRequest):
                    The request object. A request message for
                RegionNetworkFirewallPolicies.GetEffectiveFirewalls.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.RegionNetworkFirewallPoliciesGetEffectiveFirewallsResponse:

            """

            http_options = (
                _BaseRegionNetworkFirewallPoliciesRestTransport._BaseGetEffectiveFirewalls._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_effective_firewalls(
                request, metadata
            )
            transcoded_request = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseGetEffectiveFirewalls._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseGetEffectiveFirewalls._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionNetworkFirewallPoliciesRestTransport._GetEffectiveFirewalls._get_response(
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
            resp = compute.RegionNetworkFirewallPoliciesGetEffectiveFirewallsResponse()
            pb_resp = (
                compute.RegionNetworkFirewallPoliciesGetEffectiveFirewallsResponse.pb(
                    resp
                )
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_effective_firewalls(resp)
            return resp

    class _GetIamPolicy(
        _BaseRegionNetworkFirewallPoliciesRestTransport._BaseGetIamPolicy,
        RegionNetworkFirewallPoliciesRestStub,
    ):
        def __hash__(self):
            return hash("RegionNetworkFirewallPoliciesRestTransport.GetIamPolicy")

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
            request: compute.GetIamPolicyRegionNetworkFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (~.compute.GetIamPolicyRegionNetworkFirewallPolicyRequest):
                    The request object. A request message for
                RegionNetworkFirewallPolicies.GetIamPolicy.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Policy:
                    An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources. A
                ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members``, or
                principals, to a single ``role``. Principals can be user
                accounts, service accounts, Google groups, and domains
                (such as G Suite). A ``role`` is a named list of
                permissions; each ``role`` can be an IAM predefined role
                or a user-created custom role. For some types of Google
                Cloud resources, a ``binding`` can also specify a
                ``condition``, which is a logical expression that allows
                access to a resource only if the expression evaluates to
                ``true``. A condition can add constraints based on
                attributes of the request, the resource, or both. To
                learn which resources support conditions in their IAM
                policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.
                **JSON example:**
                ``{ "bindings": [ { "role": "roles/resourcemanager.organizationAdmin", "members": [ "user:mike@example.com", "group:admins@example.com", "domain:google.com", "serviceAccount:my-project-id@appspot.gserviceaccount.com" ] }, { "role": "roles/resourcemanager.organizationViewer", "members": [ "user:eve@example.com" ], "condition": { "title": "expirable access", "description": "Does not grant access after Sep 2020", "expression": "request.time < timestamp('2020-10-01T00:00:00.000Z')", } } ], "etag": "BwWWja0YfJA=", "version": 3 }``
                **YAML example:**
                ``bindings: - members: - user:mike@example.com - group:admins@example.com - domain:google.com - serviceAccount:my-project-id@appspot.gserviceaccount.com role: roles/resourcemanager.organizationAdmin - members: - user:eve@example.com role: roles/resourcemanager.organizationViewer condition: title: expirable access description: Does not grant access after Sep 2020 expression: request.time < timestamp('2020-10-01T00:00:00.000Z') etag: BwWWja0YfJA= version: 3``
                For a description of IAM and its features, see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

            """

            http_options = (
                _BaseRegionNetworkFirewallPoliciesRestTransport._BaseGetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            transcoded_request = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseGetIamPolicy._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseGetIamPolicy._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RegionNetworkFirewallPoliciesRestTransport._GetIamPolicy._get_response(
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
            resp = compute.Policy()
            pb_resp = compute.Policy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    class _GetRule(
        _BaseRegionNetworkFirewallPoliciesRestTransport._BaseGetRule,
        RegionNetworkFirewallPoliciesRestStub,
    ):
        def __hash__(self):
            return hash("RegionNetworkFirewallPoliciesRestTransport.GetRule")

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
            request: compute.GetRuleRegionNetworkFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.FirewallPolicyRule:
            r"""Call the get rule method over HTTP.

            Args:
                request (~.compute.GetRuleRegionNetworkFirewallPolicyRequest):
                    The request object. A request message for
                RegionNetworkFirewallPolicies.GetRule.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.FirewallPolicyRule:
                    Represents a rule that describes one
                or more match conditions along with the
                action to be taken when traffic matches
                this condition (allow or deny).

            """

            http_options = (
                _BaseRegionNetworkFirewallPoliciesRestTransport._BaseGetRule._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_rule(request, metadata)
            transcoded_request = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseGetRule._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseGetRule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RegionNetworkFirewallPoliciesRestTransport._GetRule._get_response(
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
            resp = compute.FirewallPolicyRule()
            pb_resp = compute.FirewallPolicyRule.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_rule(resp)
            return resp

    class _Insert(
        _BaseRegionNetworkFirewallPoliciesRestTransport._BaseInsert,
        RegionNetworkFirewallPoliciesRestStub,
    ):
        def __hash__(self):
            return hash("RegionNetworkFirewallPoliciesRestTransport.Insert")

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
            request: compute.InsertRegionNetworkFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the insert method over HTTP.

            Args:
                request (~.compute.InsertRegionNetworkFirewallPolicyRequest):
                    The request object. A request message for
                RegionNetworkFirewallPolicies.Insert.
                See the method description for details.
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
                _BaseRegionNetworkFirewallPoliciesRestTransport._BaseInsert._get_http_options()
            )
            request, metadata = self._interceptor.pre_insert(request, metadata)
            transcoded_request = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseInsert._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseInsert._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseInsert._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionNetworkFirewallPoliciesRestTransport._Insert._get_response(
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

    class _List(
        _BaseRegionNetworkFirewallPoliciesRestTransport._BaseList,
        RegionNetworkFirewallPoliciesRestStub,
    ):
        def __hash__(self):
            return hash("RegionNetworkFirewallPoliciesRestTransport.List")

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
            request: compute.ListRegionNetworkFirewallPoliciesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.FirewallPolicyList:
            r"""Call the list method over HTTP.

            Args:
                request (~.compute.ListRegionNetworkFirewallPoliciesRequest):
                    The request object. A request message for
                RegionNetworkFirewallPolicies.List. See
                the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.FirewallPolicyList:

            """

            http_options = (
                _BaseRegionNetworkFirewallPoliciesRestTransport._BaseList._get_http_options()
            )
            request, metadata = self._interceptor.pre_list(request, metadata)
            transcoded_request = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseList._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseList._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionNetworkFirewallPoliciesRestTransport._List._get_response(
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
            resp = compute.FirewallPolicyList()
            pb_resp = compute.FirewallPolicyList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list(resp)
            return resp

    class _Patch(
        _BaseRegionNetworkFirewallPoliciesRestTransport._BasePatch,
        RegionNetworkFirewallPoliciesRestStub,
    ):
        def __hash__(self):
            return hash("RegionNetworkFirewallPoliciesRestTransport.Patch")

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
            request: compute.PatchRegionNetworkFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the patch method over HTTP.

            Args:
                request (~.compute.PatchRegionNetworkFirewallPolicyRequest):
                    The request object. A request message for
                RegionNetworkFirewallPolicies.Patch. See
                the method description for details.
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
                _BaseRegionNetworkFirewallPoliciesRestTransport._BasePatch._get_http_options()
            )
            request, metadata = self._interceptor.pre_patch(request, metadata)
            transcoded_request = _BaseRegionNetworkFirewallPoliciesRestTransport._BasePatch._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionNetworkFirewallPoliciesRestTransport._BasePatch._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionNetworkFirewallPoliciesRestTransport._BasePatch._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionNetworkFirewallPoliciesRestTransport._Patch._get_response(
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
        _BaseRegionNetworkFirewallPoliciesRestTransport._BasePatchRule,
        RegionNetworkFirewallPoliciesRestStub,
    ):
        def __hash__(self):
            return hash("RegionNetworkFirewallPoliciesRestTransport.PatchRule")

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
            request: compute.PatchRuleRegionNetworkFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the patch rule method over HTTP.

            Args:
                request (~.compute.PatchRuleRegionNetworkFirewallPolicyRequest):
                    The request object. A request message for
                RegionNetworkFirewallPolicies.PatchRule.
                See the method description for details.
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
                _BaseRegionNetworkFirewallPoliciesRestTransport._BasePatchRule._get_http_options()
            )
            request, metadata = self._interceptor.pre_patch_rule(request, metadata)
            transcoded_request = _BaseRegionNetworkFirewallPoliciesRestTransport._BasePatchRule._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionNetworkFirewallPoliciesRestTransport._BasePatchRule._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionNetworkFirewallPoliciesRestTransport._BasePatchRule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RegionNetworkFirewallPoliciesRestTransport._PatchRule._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_patch_rule(resp)
            return resp

    class _RemoveAssociation(
        _BaseRegionNetworkFirewallPoliciesRestTransport._BaseRemoveAssociation,
        RegionNetworkFirewallPoliciesRestStub,
    ):
        def __hash__(self):
            return hash("RegionNetworkFirewallPoliciesRestTransport.RemoveAssociation")

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
            request: compute.RemoveAssociationRegionNetworkFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the remove association method over HTTP.

            Args:
                request (~.compute.RemoveAssociationRegionNetworkFirewallPolicyRequest):
                    The request object. A request message for
                RegionNetworkFirewallPolicies.RemoveAssociation.
                See the method description for details.
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
                _BaseRegionNetworkFirewallPoliciesRestTransport._BaseRemoveAssociation._get_http_options()
            )
            request, metadata = self._interceptor.pre_remove_association(
                request, metadata
            )
            transcoded_request = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseRemoveAssociation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseRemoveAssociation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionNetworkFirewallPoliciesRestTransport._RemoveAssociation._get_response(
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
            resp = self._interceptor.post_remove_association(resp)
            return resp

    class _RemoveRule(
        _BaseRegionNetworkFirewallPoliciesRestTransport._BaseRemoveRule,
        RegionNetworkFirewallPoliciesRestStub,
    ):
        def __hash__(self):
            return hash("RegionNetworkFirewallPoliciesRestTransport.RemoveRule")

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
            request: compute.RemoveRuleRegionNetworkFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the remove rule method over HTTP.

            Args:
                request (~.compute.RemoveRuleRegionNetworkFirewallPolicyRequest):
                    The request object. A request message for
                RegionNetworkFirewallPolicies.RemoveRule.
                See the method description for details.
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
                _BaseRegionNetworkFirewallPoliciesRestTransport._BaseRemoveRule._get_http_options()
            )
            request, metadata = self._interceptor.pre_remove_rule(request, metadata)
            transcoded_request = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseRemoveRule._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseRemoveRule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RegionNetworkFirewallPoliciesRestTransport._RemoveRule._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_remove_rule(resp)
            return resp

    class _SetIamPolicy(
        _BaseRegionNetworkFirewallPoliciesRestTransport._BaseSetIamPolicy,
        RegionNetworkFirewallPoliciesRestStub,
    ):
        def __hash__(self):
            return hash("RegionNetworkFirewallPoliciesRestTransport.SetIamPolicy")

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
            request: compute.SetIamPolicyRegionNetworkFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Policy:
            r"""Call the set iam policy method over HTTP.

            Args:
                request (~.compute.SetIamPolicyRegionNetworkFirewallPolicyRequest):
                    The request object. A request message for
                RegionNetworkFirewallPolicies.SetIamPolicy.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Policy:
                    An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources. A
                ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members``, or
                principals, to a single ``role``. Principals can be user
                accounts, service accounts, Google groups, and domains
                (such as G Suite). A ``role`` is a named list of
                permissions; each ``role`` can be an IAM predefined role
                or a user-created custom role. For some types of Google
                Cloud resources, a ``binding`` can also specify a
                ``condition``, which is a logical expression that allows
                access to a resource only if the expression evaluates to
                ``true``. A condition can add constraints based on
                attributes of the request, the resource, or both. To
                learn which resources support conditions in their IAM
                policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.
                **JSON example:**
                ``{ "bindings": [ { "role": "roles/resourcemanager.organizationAdmin", "members": [ "user:mike@example.com", "group:admins@example.com", "domain:google.com", "serviceAccount:my-project-id@appspot.gserviceaccount.com" ] }, { "role": "roles/resourcemanager.organizationViewer", "members": [ "user:eve@example.com" ], "condition": { "title": "expirable access", "description": "Does not grant access after Sep 2020", "expression": "request.time < timestamp('2020-10-01T00:00:00.000Z')", } } ], "etag": "BwWWja0YfJA=", "version": 3 }``
                **YAML example:**
                ``bindings: - members: - user:mike@example.com - group:admins@example.com - domain:google.com - serviceAccount:my-project-id@appspot.gserviceaccount.com role: roles/resourcemanager.organizationAdmin - members: - user:eve@example.com role: roles/resourcemanager.organizationViewer condition: title: expirable access description: Does not grant access after Sep 2020 expression: request.time < timestamp('2020-10-01T00:00:00.000Z') etag: BwWWja0YfJA= version: 3``
                For a description of IAM and its features, see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

            """

            http_options = (
                _BaseRegionNetworkFirewallPoliciesRestTransport._BaseSetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            transcoded_request = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseSetIamPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseSetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseSetIamPolicy._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RegionNetworkFirewallPoliciesRestTransport._SetIamPolicy._get_response(
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
            resp = compute.Policy()
            pb_resp = compute.Policy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    class _TestIamPermissions(
        _BaseRegionNetworkFirewallPoliciesRestTransport._BaseTestIamPermissions,
        RegionNetworkFirewallPoliciesRestStub,
    ):
        def __hash__(self):
            return hash("RegionNetworkFirewallPoliciesRestTransport.TestIamPermissions")

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
            request: compute.TestIamPermissionsRegionNetworkFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.TestPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (~.compute.TestIamPermissionsRegionNetworkFirewallPolicyRequest):
                    The request object. A request message for
                RegionNetworkFirewallPolicies.TestIamPermissions.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.TestPermissionsResponse:

            """

            http_options = (
                _BaseRegionNetworkFirewallPoliciesRestTransport._BaseTestIamPermissions._get_http_options()
            )
            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            transcoded_request = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseTestIamPermissions._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseTestIamPermissions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionNetworkFirewallPoliciesRestTransport._BaseTestIamPermissions._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionNetworkFirewallPoliciesRestTransport._TestIamPermissions._get_response(
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
            resp = compute.TestPermissionsResponse()
            pb_resp = compute.TestPermissionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    @property
    def add_association(
        self,
    ) -> Callable[
        [compute.AddAssociationRegionNetworkFirewallPolicyRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AddAssociation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def add_rule(
        self,
    ) -> Callable[
        [compute.AddRuleRegionNetworkFirewallPolicyRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AddRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def clone_rules(
        self,
    ) -> Callable[
        [compute.CloneRulesRegionNetworkFirewallPolicyRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CloneRules(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete(
        self,
    ) -> Callable[
        [compute.DeleteRegionNetworkFirewallPolicyRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Delete(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get(
        self,
    ) -> Callable[
        [compute.GetRegionNetworkFirewallPolicyRequest], compute.FirewallPolicy
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Get(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_association(
        self,
    ) -> Callable[
        [compute.GetAssociationRegionNetworkFirewallPolicyRequest],
        compute.FirewallPolicyAssociation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAssociation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_effective_firewalls(
        self,
    ) -> Callable[
        [compute.GetEffectiveFirewallsRegionNetworkFirewallPolicyRequest],
        compute.RegionNetworkFirewallPoliciesGetEffectiveFirewallsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEffectiveFirewalls(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_iam_policy(
        self,
    ) -> Callable[
        [compute.GetIamPolicyRegionNetworkFirewallPolicyRequest], compute.Policy
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_rule(
        self,
    ) -> Callable[
        [compute.GetRuleRegionNetworkFirewallPolicyRequest], compute.FirewallPolicyRule
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def insert(
        self,
    ) -> Callable[
        [compute.InsertRegionNetworkFirewallPolicyRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Insert(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list(
        self,
    ) -> Callable[
        [compute.ListRegionNetworkFirewallPoliciesRequest], compute.FirewallPolicyList
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._List(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def patch(
        self,
    ) -> Callable[[compute.PatchRegionNetworkFirewallPolicyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Patch(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def patch_rule(
        self,
    ) -> Callable[
        [compute.PatchRuleRegionNetworkFirewallPolicyRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PatchRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def remove_association(
        self,
    ) -> Callable[
        [compute.RemoveAssociationRegionNetworkFirewallPolicyRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemoveAssociation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def remove_rule(
        self,
    ) -> Callable[
        [compute.RemoveRuleRegionNetworkFirewallPolicyRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemoveRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_iam_policy(
        self,
    ) -> Callable[
        [compute.SetIamPolicyRegionNetworkFirewallPolicyRequest], compute.Policy
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [compute.TestIamPermissionsRegionNetworkFirewallPolicyRequest],
        compute.TestPermissionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("RegionNetworkFirewallPoliciesRestTransport",)
