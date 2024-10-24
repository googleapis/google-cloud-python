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
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.billing_v1.types import cloud_billing

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseCloudBillingRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class CloudBillingRestInterceptor:
    """Interceptor for CloudBilling.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the CloudBillingRestTransport.

    .. code-block:: python
        class MyCustomCloudBillingInterceptor(CloudBillingRestInterceptor):
            def pre_create_billing_account(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_billing_account(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_billing_account(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_billing_account(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_iam_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_project_billing_info(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_project_billing_info(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_billing_accounts(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_billing_accounts(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_project_billing_info(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_project_billing_info(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_move_billing_account(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_move_billing_account(self, response):
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

            def pre_update_billing_account(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_billing_account(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_project_billing_info(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_project_billing_info(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = CloudBillingRestTransport(interceptor=MyCustomCloudBillingInterceptor())
        client = CloudBillingClient(transport=transport)


    """

    def pre_create_billing_account(
        self,
        request: cloud_billing.CreateBillingAccountRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_billing.CreateBillingAccountRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_billing_account

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBilling server.
        """
        return request, metadata

    def post_create_billing_account(
        self, response: cloud_billing.BillingAccount
    ) -> cloud_billing.BillingAccount:
        """Post-rpc interceptor for create_billing_account

        Override in a subclass to manipulate the response
        after it is returned by the CloudBilling server but before
        it is returned to user code.
        """
        return response

    def pre_get_billing_account(
        self,
        request: cloud_billing.GetBillingAccountRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_billing.GetBillingAccountRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_billing_account

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBilling server.
        """
        return request, metadata

    def post_get_billing_account(
        self, response: cloud_billing.BillingAccount
    ) -> cloud_billing.BillingAccount:
        """Post-rpc interceptor for get_billing_account

        Override in a subclass to manipulate the response
        after it is returned by the CloudBilling server but before
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
        before they are sent to the CloudBilling server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the CloudBilling server but before
        it is returned to user code.
        """
        return response

    def pre_get_project_billing_info(
        self,
        request: cloud_billing.GetProjectBillingInfoRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_billing.GetProjectBillingInfoRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_project_billing_info

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBilling server.
        """
        return request, metadata

    def post_get_project_billing_info(
        self, response: cloud_billing.ProjectBillingInfo
    ) -> cloud_billing.ProjectBillingInfo:
        """Post-rpc interceptor for get_project_billing_info

        Override in a subclass to manipulate the response
        after it is returned by the CloudBilling server but before
        it is returned to user code.
        """
        return response

    def pre_list_billing_accounts(
        self,
        request: cloud_billing.ListBillingAccountsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_billing.ListBillingAccountsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_billing_accounts

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBilling server.
        """
        return request, metadata

    def post_list_billing_accounts(
        self, response: cloud_billing.ListBillingAccountsResponse
    ) -> cloud_billing.ListBillingAccountsResponse:
        """Post-rpc interceptor for list_billing_accounts

        Override in a subclass to manipulate the response
        after it is returned by the CloudBilling server but before
        it is returned to user code.
        """
        return response

    def pre_list_project_billing_info(
        self,
        request: cloud_billing.ListProjectBillingInfoRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_billing.ListProjectBillingInfoRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_project_billing_info

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBilling server.
        """
        return request, metadata

    def post_list_project_billing_info(
        self, response: cloud_billing.ListProjectBillingInfoResponse
    ) -> cloud_billing.ListProjectBillingInfoResponse:
        """Post-rpc interceptor for list_project_billing_info

        Override in a subclass to manipulate the response
        after it is returned by the CloudBilling server but before
        it is returned to user code.
        """
        return response

    def pre_move_billing_account(
        self,
        request: cloud_billing.MoveBillingAccountRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_billing.MoveBillingAccountRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for move_billing_account

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBilling server.
        """
        return request, metadata

    def post_move_billing_account(
        self, response: cloud_billing.BillingAccount
    ) -> cloud_billing.BillingAccount:
        """Post-rpc interceptor for move_billing_account

        Override in a subclass to manipulate the response
        after it is returned by the CloudBilling server but before
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
        before they are sent to the CloudBilling server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the CloudBilling server but before
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
        before they are sent to the CloudBilling server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the CloudBilling server but before
        it is returned to user code.
        """
        return response

    def pre_update_billing_account(
        self,
        request: cloud_billing.UpdateBillingAccountRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_billing.UpdateBillingAccountRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_billing_account

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBilling server.
        """
        return request, metadata

    def post_update_billing_account(
        self, response: cloud_billing.BillingAccount
    ) -> cloud_billing.BillingAccount:
        """Post-rpc interceptor for update_billing_account

        Override in a subclass to manipulate the response
        after it is returned by the CloudBilling server but before
        it is returned to user code.
        """
        return response

    def pre_update_project_billing_info(
        self,
        request: cloud_billing.UpdateProjectBillingInfoRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        cloud_billing.UpdateProjectBillingInfoRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_project_billing_info

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBilling server.
        """
        return request, metadata

    def post_update_project_billing_info(
        self, response: cloud_billing.ProjectBillingInfo
    ) -> cloud_billing.ProjectBillingInfo:
        """Post-rpc interceptor for update_project_billing_info

        Override in a subclass to manipulate the response
        after it is returned by the CloudBilling server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class CloudBillingRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: CloudBillingRestInterceptor


class CloudBillingRestTransport(_BaseCloudBillingRestTransport):
    """REST backend synchronous transport for CloudBilling.

    Retrieves the Google Cloud Console billing accounts and
    associates them with projects.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "cloudbilling.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[CloudBillingRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'cloudbilling.googleapis.com').
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
        self._interceptor = interceptor or CloudBillingRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateBillingAccount(
        _BaseCloudBillingRestTransport._BaseCreateBillingAccount, CloudBillingRestStub
    ):
        def __hash__(self):
            return hash("CloudBillingRestTransport.CreateBillingAccount")

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
            request: cloud_billing.CreateBillingAccountRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_billing.BillingAccount:
            r"""Call the create billing account method over HTTP.

            Args:
                request (~.cloud_billing.CreateBillingAccountRequest):
                    The request object. Request message for ``CreateBillingAccount``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_billing.BillingAccount:
                    A billing account in the `Google Cloud
                Console <https://console.cloud.google.com/>`__. You can
                assign a billing account to one or more projects.

            """

            http_options = (
                _BaseCloudBillingRestTransport._BaseCreateBillingAccount._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_billing_account(
                request, metadata
            )
            transcoded_request = _BaseCloudBillingRestTransport._BaseCreateBillingAccount._get_transcoded_request(
                http_options, request
            )

            body = _BaseCloudBillingRestTransport._BaseCreateBillingAccount._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCloudBillingRestTransport._BaseCreateBillingAccount._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CloudBillingRestTransport._CreateBillingAccount._get_response(
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
            resp = cloud_billing.BillingAccount()
            pb_resp = cloud_billing.BillingAccount.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_billing_account(resp)
            return resp

    class _GetBillingAccount(
        _BaseCloudBillingRestTransport._BaseGetBillingAccount, CloudBillingRestStub
    ):
        def __hash__(self):
            return hash("CloudBillingRestTransport.GetBillingAccount")

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
            request: cloud_billing.GetBillingAccountRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_billing.BillingAccount:
            r"""Call the get billing account method over HTTP.

            Args:
                request (~.cloud_billing.GetBillingAccountRequest):
                    The request object. Request message for ``GetBillingAccount``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_billing.BillingAccount:
                    A billing account in the `Google Cloud
                Console <https://console.cloud.google.com/>`__. You can
                assign a billing account to one or more projects.

            """

            http_options = (
                _BaseCloudBillingRestTransport._BaseGetBillingAccount._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_billing_account(
                request, metadata
            )
            transcoded_request = _BaseCloudBillingRestTransport._BaseGetBillingAccount._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudBillingRestTransport._BaseGetBillingAccount._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CloudBillingRestTransport._GetBillingAccount._get_response(
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
            resp = cloud_billing.BillingAccount()
            pb_resp = cloud_billing.BillingAccount.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_billing_account(resp)
            return resp

    class _GetIamPolicy(
        _BaseCloudBillingRestTransport._BaseGetIamPolicy, CloudBillingRestStub
    ):
        def __hash__(self):
            return hash("CloudBillingRestTransport.GetIamPolicy")

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
                _BaseCloudBillingRestTransport._BaseGetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            transcoded_request = _BaseCloudBillingRestTransport._BaseGetIamPolicy._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseCloudBillingRestTransport._BaseGetIamPolicy._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = CloudBillingRestTransport._GetIamPolicy._get_response(
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
            resp = policy_pb2.Policy()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    class _GetProjectBillingInfo(
        _BaseCloudBillingRestTransport._BaseGetProjectBillingInfo, CloudBillingRestStub
    ):
        def __hash__(self):
            return hash("CloudBillingRestTransport.GetProjectBillingInfo")

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
            request: cloud_billing.GetProjectBillingInfoRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_billing.ProjectBillingInfo:
            r"""Call the get project billing info method over HTTP.

            Args:
                request (~.cloud_billing.GetProjectBillingInfoRequest):
                    The request object. Request message for ``GetProjectBillingInfo``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_billing.ProjectBillingInfo:
                    Encapsulation of billing information
                for a Google Cloud Console project. A
                project has at most one associated
                billing account at a time (but a billing
                account can be assigned to multiple
                projects).

            """

            http_options = (
                _BaseCloudBillingRestTransport._BaseGetProjectBillingInfo._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_project_billing_info(
                request, metadata
            )
            transcoded_request = _BaseCloudBillingRestTransport._BaseGetProjectBillingInfo._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudBillingRestTransport._BaseGetProjectBillingInfo._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CloudBillingRestTransport._GetProjectBillingInfo._get_response(
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
            resp = cloud_billing.ProjectBillingInfo()
            pb_resp = cloud_billing.ProjectBillingInfo.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_project_billing_info(resp)
            return resp

    class _ListBillingAccounts(
        _BaseCloudBillingRestTransport._BaseListBillingAccounts, CloudBillingRestStub
    ):
        def __hash__(self):
            return hash("CloudBillingRestTransport.ListBillingAccounts")

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
            request: cloud_billing.ListBillingAccountsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_billing.ListBillingAccountsResponse:
            r"""Call the list billing accounts method over HTTP.

            Args:
                request (~.cloud_billing.ListBillingAccountsRequest):
                    The request object. Request message for ``ListBillingAccounts``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_billing.ListBillingAccountsResponse:
                    Response message for ``ListBillingAccounts``.
            """

            http_options = (
                _BaseCloudBillingRestTransport._BaseListBillingAccounts._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_billing_accounts(
                request, metadata
            )
            transcoded_request = _BaseCloudBillingRestTransport._BaseListBillingAccounts._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudBillingRestTransport._BaseListBillingAccounts._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CloudBillingRestTransport._ListBillingAccounts._get_response(
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
            resp = cloud_billing.ListBillingAccountsResponse()
            pb_resp = cloud_billing.ListBillingAccountsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_billing_accounts(resp)
            return resp

    class _ListProjectBillingInfo(
        _BaseCloudBillingRestTransport._BaseListProjectBillingInfo, CloudBillingRestStub
    ):
        def __hash__(self):
            return hash("CloudBillingRestTransport.ListProjectBillingInfo")

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
            request: cloud_billing.ListProjectBillingInfoRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_billing.ListProjectBillingInfoResponse:
            r"""Call the list project billing info method over HTTP.

            Args:
                request (~.cloud_billing.ListProjectBillingInfoRequest):
                    The request object. Request message for ``ListProjectBillingInfo``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_billing.ListProjectBillingInfoResponse:
                    Request message for ``ListProjectBillingInfoResponse``.
            """

            http_options = (
                _BaseCloudBillingRestTransport._BaseListProjectBillingInfo._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_project_billing_info(
                request, metadata
            )
            transcoded_request = _BaseCloudBillingRestTransport._BaseListProjectBillingInfo._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudBillingRestTransport._BaseListProjectBillingInfo._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CloudBillingRestTransport._ListProjectBillingInfo._get_response(
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
            resp = cloud_billing.ListProjectBillingInfoResponse()
            pb_resp = cloud_billing.ListProjectBillingInfoResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_project_billing_info(resp)
            return resp

    class _MoveBillingAccount(
        _BaseCloudBillingRestTransport._BaseMoveBillingAccount, CloudBillingRestStub
    ):
        def __hash__(self):
            return hash("CloudBillingRestTransport.MoveBillingAccount")

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
            request: cloud_billing.MoveBillingAccountRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_billing.BillingAccount:
            r"""Call the move billing account method over HTTP.

            Args:
                request (~.cloud_billing.MoveBillingAccountRequest):
                    The request object. Request message for ``MoveBillingAccount`` RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_billing.BillingAccount:
                    A billing account in the `Google Cloud
                Console <https://console.cloud.google.com/>`__. You can
                assign a billing account to one or more projects.

            """

            http_options = (
                _BaseCloudBillingRestTransport._BaseMoveBillingAccount._get_http_options()
            )
            request, metadata = self._interceptor.pre_move_billing_account(
                request, metadata
            )
            transcoded_request = _BaseCloudBillingRestTransport._BaseMoveBillingAccount._get_transcoded_request(
                http_options, request
            )

            body = _BaseCloudBillingRestTransport._BaseMoveBillingAccount._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCloudBillingRestTransport._BaseMoveBillingAccount._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CloudBillingRestTransport._MoveBillingAccount._get_response(
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
            resp = cloud_billing.BillingAccount()
            pb_resp = cloud_billing.BillingAccount.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_move_billing_account(resp)
            return resp

    class _SetIamPolicy(
        _BaseCloudBillingRestTransport._BaseSetIamPolicy, CloudBillingRestStub
    ):
        def __hash__(self):
            return hash("CloudBillingRestTransport.SetIamPolicy")

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
                _BaseCloudBillingRestTransport._BaseSetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            transcoded_request = _BaseCloudBillingRestTransport._BaseSetIamPolicy._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseCloudBillingRestTransport._BaseSetIamPolicy._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseCloudBillingRestTransport._BaseSetIamPolicy._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = CloudBillingRestTransport._SetIamPolicy._get_response(
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
        _BaseCloudBillingRestTransport._BaseTestIamPermissions, CloudBillingRestStub
    ):
        def __hash__(self):
            return hash("CloudBillingRestTransport.TestIamPermissions")

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
                _BaseCloudBillingRestTransport._BaseTestIamPermissions._get_http_options()
            )
            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            transcoded_request = _BaseCloudBillingRestTransport._BaseTestIamPermissions._get_transcoded_request(
                http_options, request
            )

            body = _BaseCloudBillingRestTransport._BaseTestIamPermissions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCloudBillingRestTransport._BaseTestIamPermissions._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CloudBillingRestTransport._TestIamPermissions._get_response(
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
            resp = iam_policy_pb2.TestIamPermissionsResponse()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    class _UpdateBillingAccount(
        _BaseCloudBillingRestTransport._BaseUpdateBillingAccount, CloudBillingRestStub
    ):
        def __hash__(self):
            return hash("CloudBillingRestTransport.UpdateBillingAccount")

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
            request: cloud_billing.UpdateBillingAccountRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_billing.BillingAccount:
            r"""Call the update billing account method over HTTP.

            Args:
                request (~.cloud_billing.UpdateBillingAccountRequest):
                    The request object. Request message for ``UpdateBillingAccount``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_billing.BillingAccount:
                    A billing account in the `Google Cloud
                Console <https://console.cloud.google.com/>`__. You can
                assign a billing account to one or more projects.

            """

            http_options = (
                _BaseCloudBillingRestTransport._BaseUpdateBillingAccount._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_billing_account(
                request, metadata
            )
            transcoded_request = _BaseCloudBillingRestTransport._BaseUpdateBillingAccount._get_transcoded_request(
                http_options, request
            )

            body = _BaseCloudBillingRestTransport._BaseUpdateBillingAccount._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCloudBillingRestTransport._BaseUpdateBillingAccount._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CloudBillingRestTransport._UpdateBillingAccount._get_response(
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
            resp = cloud_billing.BillingAccount()
            pb_resp = cloud_billing.BillingAccount.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_billing_account(resp)
            return resp

    class _UpdateProjectBillingInfo(
        _BaseCloudBillingRestTransport._BaseUpdateProjectBillingInfo,
        CloudBillingRestStub,
    ):
        def __hash__(self):
            return hash("CloudBillingRestTransport.UpdateProjectBillingInfo")

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
            request: cloud_billing.UpdateProjectBillingInfoRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_billing.ProjectBillingInfo:
            r"""Call the update project billing
            info method over HTTP.

                Args:
                    request (~.cloud_billing.UpdateProjectBillingInfoRequest):
                        The request object. Request message for ``UpdateProjectBillingInfo``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.cloud_billing.ProjectBillingInfo:
                        Encapsulation of billing information
                    for a Google Cloud Console project. A
                    project has at most one associated
                    billing account at a time (but a billing
                    account can be assigned to multiple
                    projects).

            """

            http_options = (
                _BaseCloudBillingRestTransport._BaseUpdateProjectBillingInfo._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_project_billing_info(
                request, metadata
            )
            transcoded_request = _BaseCloudBillingRestTransport._BaseUpdateProjectBillingInfo._get_transcoded_request(
                http_options, request
            )

            body = _BaseCloudBillingRestTransport._BaseUpdateProjectBillingInfo._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCloudBillingRestTransport._BaseUpdateProjectBillingInfo._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                CloudBillingRestTransport._UpdateProjectBillingInfo._get_response(
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
            resp = cloud_billing.ProjectBillingInfo()
            pb_resp = cloud_billing.ProjectBillingInfo.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_project_billing_info(resp)
            return resp

    @property
    def create_billing_account(
        self,
    ) -> Callable[
        [cloud_billing.CreateBillingAccountRequest], cloud_billing.BillingAccount
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBillingAccount(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_billing_account(
        self,
    ) -> Callable[
        [cloud_billing.GetBillingAccountRequest], cloud_billing.BillingAccount
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBillingAccount(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_project_billing_info(
        self,
    ) -> Callable[
        [cloud_billing.GetProjectBillingInfoRequest], cloud_billing.ProjectBillingInfo
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetProjectBillingInfo(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_billing_accounts(
        self,
    ) -> Callable[
        [cloud_billing.ListBillingAccountsRequest],
        cloud_billing.ListBillingAccountsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBillingAccounts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_project_billing_info(
        self,
    ) -> Callable[
        [cloud_billing.ListProjectBillingInfoRequest],
        cloud_billing.ListProjectBillingInfoResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListProjectBillingInfo(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def move_billing_account(
        self,
    ) -> Callable[
        [cloud_billing.MoveBillingAccountRequest], cloud_billing.BillingAccount
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._MoveBillingAccount(self._session, self._host, self._interceptor)  # type: ignore

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
    def update_billing_account(
        self,
    ) -> Callable[
        [cloud_billing.UpdateBillingAccountRequest], cloud_billing.BillingAccount
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateBillingAccount(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_project_billing_info(
        self,
    ) -> Callable[
        [cloud_billing.UpdateProjectBillingInfoRequest],
        cloud_billing.ProjectBillingInfo,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateProjectBillingInfo(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("CloudBillingRestTransport",)
