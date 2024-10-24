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
from .rest_base import _BaseFirewallPoliciesRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class FirewallPoliciesRestInterceptor:
    """Interceptor for FirewallPolicies.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the FirewallPoliciesRestTransport.

    .. code-block:: python
        class MyCustomFirewallPoliciesInterceptor(FirewallPoliciesRestInterceptor):
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

            def pre_list_associations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_associations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_move(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_move(self, response):
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

        transport = FirewallPoliciesRestTransport(interceptor=MyCustomFirewallPoliciesInterceptor())
        client = FirewallPoliciesClient(transport=transport)


    """

    def pre_add_association(
        self,
        request: compute.AddAssociationFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.AddAssociationFirewallPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for add_association

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FirewallPolicies server.
        """
        return request, metadata

    def post_add_association(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for add_association

        Override in a subclass to manipulate the response
        after it is returned by the FirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_add_rule(
        self,
        request: compute.AddRuleFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.AddRuleFirewallPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for add_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FirewallPolicies server.
        """
        return request, metadata

    def post_add_rule(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for add_rule

        Override in a subclass to manipulate the response
        after it is returned by the FirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_clone_rules(
        self,
        request: compute.CloneRulesFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.CloneRulesFirewallPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for clone_rules

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FirewallPolicies server.
        """
        return request, metadata

    def post_clone_rules(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for clone_rules

        Override in a subclass to manipulate the response
        after it is returned by the FirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_delete(
        self,
        request: compute.DeleteFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.DeleteFirewallPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FirewallPolicies server.
        """
        return request, metadata

    def post_delete(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for delete

        Override in a subclass to manipulate the response
        after it is returned by the FirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_get(
        self,
        request: compute.GetFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.GetFirewallPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FirewallPolicies server.
        """
        return request, metadata

    def post_get(self, response: compute.FirewallPolicy) -> compute.FirewallPolicy:
        """Post-rpc interceptor for get

        Override in a subclass to manipulate the response
        after it is returned by the FirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_get_association(
        self,
        request: compute.GetAssociationFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.GetAssociationFirewallPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_association

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FirewallPolicies server.
        """
        return request, metadata

    def post_get_association(
        self, response: compute.FirewallPolicyAssociation
    ) -> compute.FirewallPolicyAssociation:
        """Post-rpc interceptor for get_association

        Override in a subclass to manipulate the response
        after it is returned by the FirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_get_iam_policy(
        self,
        request: compute.GetIamPolicyFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.GetIamPolicyFirewallPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FirewallPolicies server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: compute.Policy) -> compute.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the FirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_get_rule(
        self,
        request: compute.GetRuleFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.GetRuleFirewallPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FirewallPolicies server.
        """
        return request, metadata

    def post_get_rule(
        self, response: compute.FirewallPolicyRule
    ) -> compute.FirewallPolicyRule:
        """Post-rpc interceptor for get_rule

        Override in a subclass to manipulate the response
        after it is returned by the FirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_insert(
        self,
        request: compute.InsertFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.InsertFirewallPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for insert

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FirewallPolicies server.
        """
        return request, metadata

    def post_insert(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for insert

        Override in a subclass to manipulate the response
        after it is returned by the FirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_list(
        self,
        request: compute.ListFirewallPoliciesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.ListFirewallPoliciesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FirewallPolicies server.
        """
        return request, metadata

    def post_list(
        self, response: compute.FirewallPolicyList
    ) -> compute.FirewallPolicyList:
        """Post-rpc interceptor for list

        Override in a subclass to manipulate the response
        after it is returned by the FirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_list_associations(
        self,
        request: compute.ListAssociationsFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.ListAssociationsFirewallPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_associations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FirewallPolicies server.
        """
        return request, metadata

    def post_list_associations(
        self, response: compute.FirewallPoliciesListAssociationsResponse
    ) -> compute.FirewallPoliciesListAssociationsResponse:
        """Post-rpc interceptor for list_associations

        Override in a subclass to manipulate the response
        after it is returned by the FirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_move(
        self,
        request: compute.MoveFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.MoveFirewallPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for move

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FirewallPolicies server.
        """
        return request, metadata

    def post_move(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for move

        Override in a subclass to manipulate the response
        after it is returned by the FirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_patch(
        self,
        request: compute.PatchFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.PatchFirewallPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for patch

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FirewallPolicies server.
        """
        return request, metadata

    def post_patch(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for patch

        Override in a subclass to manipulate the response
        after it is returned by the FirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_patch_rule(
        self,
        request: compute.PatchRuleFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.PatchRuleFirewallPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for patch_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FirewallPolicies server.
        """
        return request, metadata

    def post_patch_rule(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for patch_rule

        Override in a subclass to manipulate the response
        after it is returned by the FirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_remove_association(
        self,
        request: compute.RemoveAssociationFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.RemoveAssociationFirewallPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for remove_association

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FirewallPolicies server.
        """
        return request, metadata

    def post_remove_association(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for remove_association

        Override in a subclass to manipulate the response
        after it is returned by the FirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_remove_rule(
        self,
        request: compute.RemoveRuleFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.RemoveRuleFirewallPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for remove_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FirewallPolicies server.
        """
        return request, metadata

    def post_remove_rule(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for remove_rule

        Override in a subclass to manipulate the response
        after it is returned by the FirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_set_iam_policy(
        self,
        request: compute.SetIamPolicyFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.SetIamPolicyFirewallPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FirewallPolicies server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: compute.Policy) -> compute.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the FirewallPolicies server but before
        it is returned to user code.
        """
        return response

    def pre_test_iam_permissions(
        self,
        request: compute.TestIamPermissionsFirewallPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.TestIamPermissionsFirewallPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the FirewallPolicies server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: compute.TestPermissionsResponse
    ) -> compute.TestPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the FirewallPolicies server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class FirewallPoliciesRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: FirewallPoliciesRestInterceptor


class FirewallPoliciesRestTransport(_BaseFirewallPoliciesRestTransport):
    """REST backend synchronous transport for FirewallPolicies.

    The FirewallPolicies API.

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
        interceptor: Optional[FirewallPoliciesRestInterceptor] = None,
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
        self._interceptor = interceptor or FirewallPoliciesRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AddAssociation(
        _BaseFirewallPoliciesRestTransport._BaseAddAssociation, FirewallPoliciesRestStub
    ):
        def __hash__(self):
            return hash("FirewallPoliciesRestTransport.AddAssociation")

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
            request: compute.AddAssociationFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the add association method over HTTP.

            Args:
                request (~.compute.AddAssociationFirewallPolicyRequest):
                    The request object. A request message for
                FirewallPolicies.AddAssociation. See the
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
                _BaseFirewallPoliciesRestTransport._BaseAddAssociation._get_http_options()
            )
            request, metadata = self._interceptor.pre_add_association(request, metadata)
            transcoded_request = _BaseFirewallPoliciesRestTransport._BaseAddAssociation._get_transcoded_request(
                http_options, request
            )

            body = _BaseFirewallPoliciesRestTransport._BaseAddAssociation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseFirewallPoliciesRestTransport._BaseAddAssociation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = FirewallPoliciesRestTransport._AddAssociation._get_response(
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
        _BaseFirewallPoliciesRestTransport._BaseAddRule, FirewallPoliciesRestStub
    ):
        def __hash__(self):
            return hash("FirewallPoliciesRestTransport.AddRule")

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
            request: compute.AddRuleFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the add rule method over HTTP.

            Args:
                request (~.compute.AddRuleFirewallPolicyRequest):
                    The request object. A request message for
                FirewallPolicies.AddRule. See the method
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
                _BaseFirewallPoliciesRestTransport._BaseAddRule._get_http_options()
            )
            request, metadata = self._interceptor.pre_add_rule(request, metadata)
            transcoded_request = (
                _BaseFirewallPoliciesRestTransport._BaseAddRule._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseFirewallPoliciesRestTransport._BaseAddRule._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseFirewallPoliciesRestTransport._BaseAddRule._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = FirewallPoliciesRestTransport._AddRule._get_response(
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

    class _CloneRules(
        _BaseFirewallPoliciesRestTransport._BaseCloneRules, FirewallPoliciesRestStub
    ):
        def __hash__(self):
            return hash("FirewallPoliciesRestTransport.CloneRules")

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
            request: compute.CloneRulesFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the clone rules method over HTTP.

            Args:
                request (~.compute.CloneRulesFirewallPolicyRequest):
                    The request object. A request message for
                FirewallPolicies.CloneRules. See the
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
                _BaseFirewallPoliciesRestTransport._BaseCloneRules._get_http_options()
            )
            request, metadata = self._interceptor.pre_clone_rules(request, metadata)
            transcoded_request = _BaseFirewallPoliciesRestTransport._BaseCloneRules._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseFirewallPoliciesRestTransport._BaseCloneRules._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = FirewallPoliciesRestTransport._CloneRules._get_response(
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
            resp = self._interceptor.post_clone_rules(resp)
            return resp

    class _Delete(
        _BaseFirewallPoliciesRestTransport._BaseDelete, FirewallPoliciesRestStub
    ):
        def __hash__(self):
            return hash("FirewallPoliciesRestTransport.Delete")

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
            request: compute.DeleteFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the delete method over HTTP.

            Args:
                request (~.compute.DeleteFirewallPolicyRequest):
                    The request object. A request message for
                FirewallPolicies.Delete. See the method
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
                _BaseFirewallPoliciesRestTransport._BaseDelete._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete(request, metadata)
            transcoded_request = (
                _BaseFirewallPoliciesRestTransport._BaseDelete._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseFirewallPoliciesRestTransport._BaseDelete._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = FirewallPoliciesRestTransport._Delete._get_response(
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

    class _Get(_BaseFirewallPoliciesRestTransport._BaseGet, FirewallPoliciesRestStub):
        def __hash__(self):
            return hash("FirewallPoliciesRestTransport.Get")

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
            request: compute.GetFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.FirewallPolicy:
            r"""Call the get method over HTTP.

            Args:
                request (~.compute.GetFirewallPolicyRequest):
                    The request object. A request message for
                FirewallPolicies.Get. See the method
                description for details.
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
                _BaseFirewallPoliciesRestTransport._BaseGet._get_http_options()
            )
            request, metadata = self._interceptor.pre_get(request, metadata)
            transcoded_request = (
                _BaseFirewallPoliciesRestTransport._BaseGet._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseFirewallPoliciesRestTransport._BaseGet._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = FirewallPoliciesRestTransport._Get._get_response(
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
        _BaseFirewallPoliciesRestTransport._BaseGetAssociation, FirewallPoliciesRestStub
    ):
        def __hash__(self):
            return hash("FirewallPoliciesRestTransport.GetAssociation")

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
            request: compute.GetAssociationFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.FirewallPolicyAssociation:
            r"""Call the get association method over HTTP.

            Args:
                request (~.compute.GetAssociationFirewallPolicyRequest):
                    The request object. A request message for
                FirewallPolicies.GetAssociation. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.FirewallPolicyAssociation:

            """

            http_options = (
                _BaseFirewallPoliciesRestTransport._BaseGetAssociation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_association(request, metadata)
            transcoded_request = _BaseFirewallPoliciesRestTransport._BaseGetAssociation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseFirewallPoliciesRestTransport._BaseGetAssociation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = FirewallPoliciesRestTransport._GetAssociation._get_response(
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

    class _GetIamPolicy(
        _BaseFirewallPoliciesRestTransport._BaseGetIamPolicy, FirewallPoliciesRestStub
    ):
        def __hash__(self):
            return hash("FirewallPoliciesRestTransport.GetIamPolicy")

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
            request: compute.GetIamPolicyFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (~.compute.GetIamPolicyFirewallPolicyRequest):
                    The request object. A request message for
                FirewallPolicies.GetIamPolicy. See the
                method description for details.
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
                _BaseFirewallPoliciesRestTransport._BaseGetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            transcoded_request = _BaseFirewallPoliciesRestTransport._BaseGetIamPolicy._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseFirewallPoliciesRestTransport._BaseGetIamPolicy._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = FirewallPoliciesRestTransport._GetIamPolicy._get_response(
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
            resp = compute.Policy()
            pb_resp = compute.Policy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    class _GetRule(
        _BaseFirewallPoliciesRestTransport._BaseGetRule, FirewallPoliciesRestStub
    ):
        def __hash__(self):
            return hash("FirewallPoliciesRestTransport.GetRule")

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
            request: compute.GetRuleFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.FirewallPolicyRule:
            r"""Call the get rule method over HTTP.

            Args:
                request (~.compute.GetRuleFirewallPolicyRequest):
                    The request object. A request message for
                FirewallPolicies.GetRule. See the method
                description for details.
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
                _BaseFirewallPoliciesRestTransport._BaseGetRule._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_rule(request, metadata)
            transcoded_request = (
                _BaseFirewallPoliciesRestTransport._BaseGetRule._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseFirewallPoliciesRestTransport._BaseGetRule._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = FirewallPoliciesRestTransport._GetRule._get_response(
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
            resp = compute.FirewallPolicyRule()
            pb_resp = compute.FirewallPolicyRule.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_rule(resp)
            return resp

    class _Insert(
        _BaseFirewallPoliciesRestTransport._BaseInsert, FirewallPoliciesRestStub
    ):
        def __hash__(self):
            return hash("FirewallPoliciesRestTransport.Insert")

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
            request: compute.InsertFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the insert method over HTTP.

            Args:
                request (~.compute.InsertFirewallPolicyRequest):
                    The request object. A request message for
                FirewallPolicies.Insert. See the method
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
                _BaseFirewallPoliciesRestTransport._BaseInsert._get_http_options()
            )
            request, metadata = self._interceptor.pre_insert(request, metadata)
            transcoded_request = (
                _BaseFirewallPoliciesRestTransport._BaseInsert._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseFirewallPoliciesRestTransport._BaseInsert._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseFirewallPoliciesRestTransport._BaseInsert._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = FirewallPoliciesRestTransport._Insert._get_response(
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

    class _List(_BaseFirewallPoliciesRestTransport._BaseList, FirewallPoliciesRestStub):
        def __hash__(self):
            return hash("FirewallPoliciesRestTransport.List")

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
            request: compute.ListFirewallPoliciesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.FirewallPolicyList:
            r"""Call the list method over HTTP.

            Args:
                request (~.compute.ListFirewallPoliciesRequest):
                    The request object. A request message for
                FirewallPolicies.List. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.FirewallPolicyList:

            """

            http_options = (
                _BaseFirewallPoliciesRestTransport._BaseList._get_http_options()
            )
            request, metadata = self._interceptor.pre_list(request, metadata)
            transcoded_request = (
                _BaseFirewallPoliciesRestTransport._BaseList._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseFirewallPoliciesRestTransport._BaseList._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = FirewallPoliciesRestTransport._List._get_response(
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

    class _ListAssociations(
        _BaseFirewallPoliciesRestTransport._BaseListAssociations,
        FirewallPoliciesRestStub,
    ):
        def __hash__(self):
            return hash("FirewallPoliciesRestTransport.ListAssociations")

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
            request: compute.ListAssociationsFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.FirewallPoliciesListAssociationsResponse:
            r"""Call the list associations method over HTTP.

            Args:
                request (~.compute.ListAssociationsFirewallPolicyRequest):
                    The request object. A request message for
                FirewallPolicies.ListAssociations. See
                the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.FirewallPoliciesListAssociationsResponse:

            """

            http_options = (
                _BaseFirewallPoliciesRestTransport._BaseListAssociations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_associations(
                request, metadata
            )
            transcoded_request = _BaseFirewallPoliciesRestTransport._BaseListAssociations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseFirewallPoliciesRestTransport._BaseListAssociations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = FirewallPoliciesRestTransport._ListAssociations._get_response(
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
            resp = compute.FirewallPoliciesListAssociationsResponse()
            pb_resp = compute.FirewallPoliciesListAssociationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_associations(resp)
            return resp

    class _Move(_BaseFirewallPoliciesRestTransport._BaseMove, FirewallPoliciesRestStub):
        def __hash__(self):
            return hash("FirewallPoliciesRestTransport.Move")

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
            request: compute.MoveFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the move method over HTTP.

            Args:
                request (~.compute.MoveFirewallPolicyRequest):
                    The request object. A request message for
                FirewallPolicies.Move. See the method
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
                _BaseFirewallPoliciesRestTransport._BaseMove._get_http_options()
            )
            request, metadata = self._interceptor.pre_move(request, metadata)
            transcoded_request = (
                _BaseFirewallPoliciesRestTransport._BaseMove._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseFirewallPoliciesRestTransport._BaseMove._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = FirewallPoliciesRestTransport._Move._get_response(
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
            resp = self._interceptor.post_move(resp)
            return resp

    class _Patch(
        _BaseFirewallPoliciesRestTransport._BasePatch, FirewallPoliciesRestStub
    ):
        def __hash__(self):
            return hash("FirewallPoliciesRestTransport.Patch")

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
            request: compute.PatchFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the patch method over HTTP.

            Args:
                request (~.compute.PatchFirewallPolicyRequest):
                    The request object. A request message for
                FirewallPolicies.Patch. See the method
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
                _BaseFirewallPoliciesRestTransport._BasePatch._get_http_options()
            )
            request, metadata = self._interceptor.pre_patch(request, metadata)
            transcoded_request = (
                _BaseFirewallPoliciesRestTransport._BasePatch._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseFirewallPoliciesRestTransport._BasePatch._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseFirewallPoliciesRestTransport._BasePatch._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = FirewallPoliciesRestTransport._Patch._get_response(
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
        _BaseFirewallPoliciesRestTransport._BasePatchRule, FirewallPoliciesRestStub
    ):
        def __hash__(self):
            return hash("FirewallPoliciesRestTransport.PatchRule")

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
            request: compute.PatchRuleFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the patch rule method over HTTP.

            Args:
                request (~.compute.PatchRuleFirewallPolicyRequest):
                    The request object. A request message for
                FirewallPolicies.PatchRule. See the
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
                _BaseFirewallPoliciesRestTransport._BasePatchRule._get_http_options()
            )
            request, metadata = self._interceptor.pre_patch_rule(request, metadata)
            transcoded_request = _BaseFirewallPoliciesRestTransport._BasePatchRule._get_transcoded_request(
                http_options, request
            )

            body = _BaseFirewallPoliciesRestTransport._BasePatchRule._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseFirewallPoliciesRestTransport._BasePatchRule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = FirewallPoliciesRestTransport._PatchRule._get_response(
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

    class _RemoveAssociation(
        _BaseFirewallPoliciesRestTransport._BaseRemoveAssociation,
        FirewallPoliciesRestStub,
    ):
        def __hash__(self):
            return hash("FirewallPoliciesRestTransport.RemoveAssociation")

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
            request: compute.RemoveAssociationFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the remove association method over HTTP.

            Args:
                request (~.compute.RemoveAssociationFirewallPolicyRequest):
                    The request object. A request message for
                FirewallPolicies.RemoveAssociation. See
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
                _BaseFirewallPoliciesRestTransport._BaseRemoveAssociation._get_http_options()
            )
            request, metadata = self._interceptor.pre_remove_association(
                request, metadata
            )
            transcoded_request = _BaseFirewallPoliciesRestTransport._BaseRemoveAssociation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseFirewallPoliciesRestTransport._BaseRemoveAssociation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = FirewallPoliciesRestTransport._RemoveAssociation._get_response(
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
        _BaseFirewallPoliciesRestTransport._BaseRemoveRule, FirewallPoliciesRestStub
    ):
        def __hash__(self):
            return hash("FirewallPoliciesRestTransport.RemoveRule")

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
            request: compute.RemoveRuleFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the remove rule method over HTTP.

            Args:
                request (~.compute.RemoveRuleFirewallPolicyRequest):
                    The request object. A request message for
                FirewallPolicies.RemoveRule. See the
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
                _BaseFirewallPoliciesRestTransport._BaseRemoveRule._get_http_options()
            )
            request, metadata = self._interceptor.pre_remove_rule(request, metadata)
            transcoded_request = _BaseFirewallPoliciesRestTransport._BaseRemoveRule._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseFirewallPoliciesRestTransport._BaseRemoveRule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = FirewallPoliciesRestTransport._RemoveRule._get_response(
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

    class _SetIamPolicy(
        _BaseFirewallPoliciesRestTransport._BaseSetIamPolicy, FirewallPoliciesRestStub
    ):
        def __hash__(self):
            return hash("FirewallPoliciesRestTransport.SetIamPolicy")

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
            request: compute.SetIamPolicyFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Policy:
            r"""Call the set iam policy method over HTTP.

            Args:
                request (~.compute.SetIamPolicyFirewallPolicyRequest):
                    The request object. A request message for
                FirewallPolicies.SetIamPolicy. See the
                method description for details.
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
                _BaseFirewallPoliciesRestTransport._BaseSetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            transcoded_request = _BaseFirewallPoliciesRestTransport._BaseSetIamPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseFirewallPoliciesRestTransport._BaseSetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseFirewallPoliciesRestTransport._BaseSetIamPolicy._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = FirewallPoliciesRestTransport._SetIamPolicy._get_response(
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
            resp = compute.Policy()
            pb_resp = compute.Policy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    class _TestIamPermissions(
        _BaseFirewallPoliciesRestTransport._BaseTestIamPermissions,
        FirewallPoliciesRestStub,
    ):
        def __hash__(self):
            return hash("FirewallPoliciesRestTransport.TestIamPermissions")

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
            request: compute.TestIamPermissionsFirewallPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.TestPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (~.compute.TestIamPermissionsFirewallPolicyRequest):
                    The request object. A request message for
                FirewallPolicies.TestIamPermissions. See
                the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.TestPermissionsResponse:

            """

            http_options = (
                _BaseFirewallPoliciesRestTransport._BaseTestIamPermissions._get_http_options()
            )
            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            transcoded_request = _BaseFirewallPoliciesRestTransport._BaseTestIamPermissions._get_transcoded_request(
                http_options, request
            )

            body = _BaseFirewallPoliciesRestTransport._BaseTestIamPermissions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseFirewallPoliciesRestTransport._BaseTestIamPermissions._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = FirewallPoliciesRestTransport._TestIamPermissions._get_response(
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
    ) -> Callable[[compute.AddAssociationFirewallPolicyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AddAssociation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def add_rule(
        self,
    ) -> Callable[[compute.AddRuleFirewallPolicyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AddRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def clone_rules(
        self,
    ) -> Callable[[compute.CloneRulesFirewallPolicyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CloneRules(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete(
        self,
    ) -> Callable[[compute.DeleteFirewallPolicyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Delete(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get(
        self,
    ) -> Callable[[compute.GetFirewallPolicyRequest], compute.FirewallPolicy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Get(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_association(
        self,
    ) -> Callable[
        [compute.GetAssociationFirewallPolicyRequest], compute.FirewallPolicyAssociation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAssociation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[compute.GetIamPolicyFirewallPolicyRequest], compute.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_rule(
        self,
    ) -> Callable[[compute.GetRuleFirewallPolicyRequest], compute.FirewallPolicyRule]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def insert(
        self,
    ) -> Callable[[compute.InsertFirewallPolicyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Insert(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list(
        self,
    ) -> Callable[[compute.ListFirewallPoliciesRequest], compute.FirewallPolicyList]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._List(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_associations(
        self,
    ) -> Callable[
        [compute.ListAssociationsFirewallPolicyRequest],
        compute.FirewallPoliciesListAssociationsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAssociations(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def move(self) -> Callable[[compute.MoveFirewallPolicyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Move(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def patch(
        self,
    ) -> Callable[[compute.PatchFirewallPolicyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Patch(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def patch_rule(
        self,
    ) -> Callable[[compute.PatchRuleFirewallPolicyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PatchRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def remove_association(
        self,
    ) -> Callable[[compute.RemoveAssociationFirewallPolicyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemoveAssociation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def remove_rule(
        self,
    ) -> Callable[[compute.RemoveRuleFirewallPolicyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemoveRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[compute.SetIamPolicyFirewallPolicyRequest], compute.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [compute.TestIamPermissionsFirewallPolicyRequest],
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


__all__ = ("FirewallPoliciesRestTransport",)
