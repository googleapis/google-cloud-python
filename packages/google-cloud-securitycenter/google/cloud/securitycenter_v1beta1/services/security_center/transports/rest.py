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
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.securitycenter_v1beta1.types import (
    organization_settings as gcs_organization_settings,
)
from google.cloud.securitycenter_v1beta1.types import (
    security_marks as gcs_security_marks,
)
from google.cloud.securitycenter_v1beta1.types import finding
from google.cloud.securitycenter_v1beta1.types import finding as gcs_finding
from google.cloud.securitycenter_v1beta1.types import organization_settings
from google.cloud.securitycenter_v1beta1.types import securitycenter_service
from google.cloud.securitycenter_v1beta1.types import source
from google.cloud.securitycenter_v1beta1.types import source as gcs_source

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseSecurityCenterRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class SecurityCenterRestInterceptor:
    """Interceptor for SecurityCenter.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the SecurityCenterRestTransport.

    .. code-block:: python
        class MyCustomSecurityCenterInterceptor(SecurityCenterRestInterceptor):
            def pre_create_finding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_finding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_source(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_iam_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_organization_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_organization_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_source(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_group_assets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_group_assets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_group_findings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_group_findings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_assets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_assets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_findings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_findings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_sources(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_sources(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_run_asset_discovery(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_run_asset_discovery(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_finding_state(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_finding_state(self, response):
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

            def pre_update_finding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_finding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_organization_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_organization_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_security_marks(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_security_marks(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_source(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = SecurityCenterRestTransport(interceptor=MyCustomSecurityCenterInterceptor())
        client = SecurityCenterClient(transport=transport)


    """

    def pre_create_finding(
        self,
        request: securitycenter_service.CreateFindingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[securitycenter_service.CreateFindingRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_finding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_create_finding(self, response: gcs_finding.Finding) -> gcs_finding.Finding:
        """Post-rpc interceptor for create_finding

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_create_source(
        self,
        request: securitycenter_service.CreateSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[securitycenter_service.CreateSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_create_source(self, response: gcs_source.Source) -> gcs_source.Source:
        """Post-rpc interceptor for create_source

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
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
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_get_organization_settings(
        self,
        request: securitycenter_service.GetOrganizationSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.GetOrganizationSettingsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_organization_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_get_organization_settings(
        self, response: organization_settings.OrganizationSettings
    ) -> organization_settings.OrganizationSettings:
        """Post-rpc interceptor for get_organization_settings

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_get_source(
        self,
        request: securitycenter_service.GetSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[securitycenter_service.GetSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_get_source(self, response: source.Source) -> source.Source:
        """Post-rpc interceptor for get_source

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_group_assets(
        self,
        request: securitycenter_service.GroupAssetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[securitycenter_service.GroupAssetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for group_assets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_group_assets(
        self, response: securitycenter_service.GroupAssetsResponse
    ) -> securitycenter_service.GroupAssetsResponse:
        """Post-rpc interceptor for group_assets

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_group_findings(
        self,
        request: securitycenter_service.GroupFindingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[securitycenter_service.GroupFindingsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for group_findings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_group_findings(
        self, response: securitycenter_service.GroupFindingsResponse
    ) -> securitycenter_service.GroupFindingsResponse:
        """Post-rpc interceptor for group_findings

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_assets(
        self,
        request: securitycenter_service.ListAssetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[securitycenter_service.ListAssetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_assets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_list_assets(
        self, response: securitycenter_service.ListAssetsResponse
    ) -> securitycenter_service.ListAssetsResponse:
        """Post-rpc interceptor for list_assets

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_findings(
        self,
        request: securitycenter_service.ListFindingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[securitycenter_service.ListFindingsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_findings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_list_findings(
        self, response: securitycenter_service.ListFindingsResponse
    ) -> securitycenter_service.ListFindingsResponse:
        """Post-rpc interceptor for list_findings

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_sources(
        self,
        request: securitycenter_service.ListSourcesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[securitycenter_service.ListSourcesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_sources

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_list_sources(
        self, response: securitycenter_service.ListSourcesResponse
    ) -> securitycenter_service.ListSourcesResponse:
        """Post-rpc interceptor for list_sources

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_run_asset_discovery(
        self,
        request: securitycenter_service.RunAssetDiscoveryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.RunAssetDiscoveryRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for run_asset_discovery

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_run_asset_discovery(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for run_asset_discovery

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_set_finding_state(
        self,
        request: securitycenter_service.SetFindingStateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.SetFindingStateRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for set_finding_state

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_set_finding_state(self, response: finding.Finding) -> finding.Finding:
        """Post-rpc interceptor for set_finding_state

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
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
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
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
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_update_finding(
        self,
        request: securitycenter_service.UpdateFindingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[securitycenter_service.UpdateFindingRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_finding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_update_finding(self, response: gcs_finding.Finding) -> gcs_finding.Finding:
        """Post-rpc interceptor for update_finding

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_update_organization_settings(
        self,
        request: securitycenter_service.UpdateOrganizationSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.UpdateOrganizationSettingsRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for update_organization_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_update_organization_settings(
        self, response: gcs_organization_settings.OrganizationSettings
    ) -> gcs_organization_settings.OrganizationSettings:
        """Post-rpc interceptor for update_organization_settings

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_update_security_marks(
        self,
        request: securitycenter_service.UpdateSecurityMarksRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.UpdateSecurityMarksRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_security_marks

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_update_security_marks(
        self, response: gcs_security_marks.SecurityMarks
    ) -> gcs_security_marks.SecurityMarks:
        """Post-rpc interceptor for update_security_marks

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_update_source(
        self,
        request: securitycenter_service.UpdateSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[securitycenter_service.UpdateSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_update_source(self, response: gcs_source.Source) -> gcs_source.Source:
        """Post-rpc interceptor for update_source

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class SecurityCenterRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: SecurityCenterRestInterceptor


class SecurityCenterRestTransport(_BaseSecurityCenterRestTransport):
    """REST backend synchronous transport for SecurityCenter.

    V1 Beta APIs for Security Center service.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "securitycenter.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[SecurityCenterRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'securitycenter.googleapis.com').
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
        self._interceptor = interceptor or SecurityCenterRestInterceptor()
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
                "google.longrunning.Operations.CancelOperation": [
                    {
                        "method": "post",
                        "uri": "/v1beta1/{name=organizations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1beta1/{name=organizations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1beta1/{name=organizations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1beta1/{name=organizations/*/operations}",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1beta1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateFinding(
        _BaseSecurityCenterRestTransport._BaseCreateFinding, SecurityCenterRestStub
    ):
        def __hash__(self):
            return hash("SecurityCenterRestTransport.CreateFinding")

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
            request: securitycenter_service.CreateFindingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_finding.Finding:
            r"""Call the create finding method over HTTP.

            Args:
                request (~.securitycenter_service.CreateFindingRequest):
                    The request object. Request message for creating a
                finding.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_finding.Finding:
                    Security Command Center finding.

                A finding is a record of assessment data
                (security, risk, health or privacy)
                ingested into Security Command Center
                for presentation, notification,
                analysis, policy testing, and
                enforcement. For example, an XSS
                vulnerability in an App Engine
                application is a finding.

            """

            http_options = (
                _BaseSecurityCenterRestTransport._BaseCreateFinding._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_finding(request, metadata)
            transcoded_request = _BaseSecurityCenterRestTransport._BaseCreateFinding._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityCenterRestTransport._BaseCreateFinding._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterRestTransport._BaseCreateFinding._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterRestTransport._CreateFinding._get_response(
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
            resp = gcs_finding.Finding()
            pb_resp = gcs_finding.Finding.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_finding(resp)
            return resp

    class _CreateSource(
        _BaseSecurityCenterRestTransport._BaseCreateSource, SecurityCenterRestStub
    ):
        def __hash__(self):
            return hash("SecurityCenterRestTransport.CreateSource")

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
            request: securitycenter_service.CreateSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_source.Source:
            r"""Call the create source method over HTTP.

            Args:
                request (~.securitycenter_service.CreateSourceRequest):
                    The request object. Request message for creating a
                source.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_source.Source:
                    Security Command Center finding
                source. A finding source is an entity or
                a mechanism that can produce a finding.
                A source is like a container of findings
                that come from the same scanner, logger,
                monitor, etc.

            """

            http_options = (
                _BaseSecurityCenterRestTransport._BaseCreateSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_source(request, metadata)
            transcoded_request = _BaseSecurityCenterRestTransport._BaseCreateSource._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityCenterRestTransport._BaseCreateSource._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterRestTransport._BaseCreateSource._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterRestTransport._CreateSource._get_response(
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
            resp = gcs_source.Source()
            pb_resp = gcs_source.Source.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_source(resp)
            return resp

    class _GetIamPolicy(
        _BaseSecurityCenterRestTransport._BaseGetIamPolicy, SecurityCenterRestStub
    ):
        def __hash__(self):
            return hash("SecurityCenterRestTransport.GetIamPolicy")

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
                _BaseSecurityCenterRestTransport._BaseGetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            transcoded_request = _BaseSecurityCenterRestTransport._BaseGetIamPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityCenterRestTransport._BaseGetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterRestTransport._BaseGetIamPolicy._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterRestTransport._GetIamPolicy._get_response(
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

    class _GetOrganizationSettings(
        _BaseSecurityCenterRestTransport._BaseGetOrganizationSettings,
        SecurityCenterRestStub,
    ):
        def __hash__(self):
            return hash("SecurityCenterRestTransport.GetOrganizationSettings")

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
            request: securitycenter_service.GetOrganizationSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> organization_settings.OrganizationSettings:
            r"""Call the get organization settings method over HTTP.

            Args:
                request (~.securitycenter_service.GetOrganizationSettingsRequest):
                    The request object. Request message for getting
                organization settings.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.organization_settings.OrganizationSettings:
                    User specified settings that are
                attached to the Security Command Center
                organization.

            """

            http_options = (
                _BaseSecurityCenterRestTransport._BaseGetOrganizationSettings._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_organization_settings(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterRestTransport._BaseGetOrganizationSettings._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterRestTransport._BaseGetOrganizationSettings._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SecurityCenterRestTransport._GetOrganizationSettings._get_response(
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
            resp = organization_settings.OrganizationSettings()
            pb_resp = organization_settings.OrganizationSettings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_organization_settings(resp)
            return resp

    class _GetSource(
        _BaseSecurityCenterRestTransport._BaseGetSource, SecurityCenterRestStub
    ):
        def __hash__(self):
            return hash("SecurityCenterRestTransport.GetSource")

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
            request: securitycenter_service.GetSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> source.Source:
            r"""Call the get source method over HTTP.

            Args:
                request (~.securitycenter_service.GetSourceRequest):
                    The request object. Request message for getting a source.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.source.Source:
                    Security Command Center finding
                source. A finding source is an entity or
                a mechanism that can produce a finding.
                A source is like a container of findings
                that come from the same scanner, logger,
                monitor, etc.

            """

            http_options = (
                _BaseSecurityCenterRestTransport._BaseGetSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_source(request, metadata)
            transcoded_request = (
                _BaseSecurityCenterRestTransport._BaseGetSource._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSecurityCenterRestTransport._BaseGetSource._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SecurityCenterRestTransport._GetSource._get_response(
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
            resp = source.Source()
            pb_resp = source.Source.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_source(resp)
            return resp

    class _GroupAssets(
        _BaseSecurityCenterRestTransport._BaseGroupAssets, SecurityCenterRestStub
    ):
        def __hash__(self):
            return hash("SecurityCenterRestTransport.GroupAssets")

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
            request: securitycenter_service.GroupAssetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> securitycenter_service.GroupAssetsResponse:
            r"""Call the group assets method over HTTP.

            Args:
                request (~.securitycenter_service.GroupAssetsRequest):
                    The request object. Request message for grouping by
                assets.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.securitycenter_service.GroupAssetsResponse:
                    Response message for grouping by
                assets.

            """

            http_options = (
                _BaseSecurityCenterRestTransport._BaseGroupAssets._get_http_options()
            )
            request, metadata = self._interceptor.pre_group_assets(request, metadata)
            transcoded_request = _BaseSecurityCenterRestTransport._BaseGroupAssets._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityCenterRestTransport._BaseGroupAssets._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterRestTransport._BaseGroupAssets._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterRestTransport._GroupAssets._get_response(
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
            resp = securitycenter_service.GroupAssetsResponse()
            pb_resp = securitycenter_service.GroupAssetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_group_assets(resp)
            return resp

    class _GroupFindings(
        _BaseSecurityCenterRestTransport._BaseGroupFindings, SecurityCenterRestStub
    ):
        def __hash__(self):
            return hash("SecurityCenterRestTransport.GroupFindings")

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
            request: securitycenter_service.GroupFindingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> securitycenter_service.GroupFindingsResponse:
            r"""Call the group findings method over HTTP.

            Args:
                request (~.securitycenter_service.GroupFindingsRequest):
                    The request object. Request message for grouping by
                findings.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.securitycenter_service.GroupFindingsResponse:
                    Response message for group by
                findings.

            """

            http_options = (
                _BaseSecurityCenterRestTransport._BaseGroupFindings._get_http_options()
            )
            request, metadata = self._interceptor.pre_group_findings(request, metadata)
            transcoded_request = _BaseSecurityCenterRestTransport._BaseGroupFindings._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityCenterRestTransport._BaseGroupFindings._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterRestTransport._BaseGroupFindings._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterRestTransport._GroupFindings._get_response(
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
            resp = securitycenter_service.GroupFindingsResponse()
            pb_resp = securitycenter_service.GroupFindingsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_group_findings(resp)
            return resp

    class _ListAssets(
        _BaseSecurityCenterRestTransport._BaseListAssets, SecurityCenterRestStub
    ):
        def __hash__(self):
            return hash("SecurityCenterRestTransport.ListAssets")

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
            request: securitycenter_service.ListAssetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> securitycenter_service.ListAssetsResponse:
            r"""Call the list assets method over HTTP.

            Args:
                request (~.securitycenter_service.ListAssetsRequest):
                    The request object. Request message for listing assets.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.securitycenter_service.ListAssetsResponse:
                    Response message for listing assets.
            """

            http_options = (
                _BaseSecurityCenterRestTransport._BaseListAssets._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_assets(request, metadata)
            transcoded_request = _BaseSecurityCenterRestTransport._BaseListAssets._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseSecurityCenterRestTransport._BaseListAssets._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SecurityCenterRestTransport._ListAssets._get_response(
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
            resp = securitycenter_service.ListAssetsResponse()
            pb_resp = securitycenter_service.ListAssetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_assets(resp)
            return resp

    class _ListFindings(
        _BaseSecurityCenterRestTransport._BaseListFindings, SecurityCenterRestStub
    ):
        def __hash__(self):
            return hash("SecurityCenterRestTransport.ListFindings")

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
            request: securitycenter_service.ListFindingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> securitycenter_service.ListFindingsResponse:
            r"""Call the list findings method over HTTP.

            Args:
                request (~.securitycenter_service.ListFindingsRequest):
                    The request object. Request message for listing findings.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.securitycenter_service.ListFindingsResponse:
                    Response message for listing
                findings.

            """

            http_options = (
                _BaseSecurityCenterRestTransport._BaseListFindings._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_findings(request, metadata)
            transcoded_request = _BaseSecurityCenterRestTransport._BaseListFindings._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterRestTransport._BaseListFindings._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterRestTransport._ListFindings._get_response(
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
            resp = securitycenter_service.ListFindingsResponse()
            pb_resp = securitycenter_service.ListFindingsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_findings(resp)
            return resp

    class _ListSources(
        _BaseSecurityCenterRestTransport._BaseListSources, SecurityCenterRestStub
    ):
        def __hash__(self):
            return hash("SecurityCenterRestTransport.ListSources")

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
            request: securitycenter_service.ListSourcesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> securitycenter_service.ListSourcesResponse:
            r"""Call the list sources method over HTTP.

            Args:
                request (~.securitycenter_service.ListSourcesRequest):
                    The request object. Request message for listing sources.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.securitycenter_service.ListSourcesResponse:
                    Response message for listing sources.
            """

            http_options = (
                _BaseSecurityCenterRestTransport._BaseListSources._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_sources(request, metadata)
            transcoded_request = _BaseSecurityCenterRestTransport._BaseListSources._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterRestTransport._BaseListSources._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterRestTransport._ListSources._get_response(
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
            resp = securitycenter_service.ListSourcesResponse()
            pb_resp = securitycenter_service.ListSourcesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_sources(resp)
            return resp

    class _RunAssetDiscovery(
        _BaseSecurityCenterRestTransport._BaseRunAssetDiscovery, SecurityCenterRestStub
    ):
        def __hash__(self):
            return hash("SecurityCenterRestTransport.RunAssetDiscovery")

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
            request: securitycenter_service.RunAssetDiscoveryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the run asset discovery method over HTTP.

            Args:
                request (~.securitycenter_service.RunAssetDiscoveryRequest):
                    The request object. Request message for running asset
                discovery for an organization.
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
                _BaseSecurityCenterRestTransport._BaseRunAssetDiscovery._get_http_options()
            )
            request, metadata = self._interceptor.pre_run_asset_discovery(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterRestTransport._BaseRunAssetDiscovery._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityCenterRestTransport._BaseRunAssetDiscovery._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterRestTransport._BaseRunAssetDiscovery._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterRestTransport._RunAssetDiscovery._get_response(
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
            resp = self._interceptor.post_run_asset_discovery(resp)
            return resp

    class _SetFindingState(
        _BaseSecurityCenterRestTransport._BaseSetFindingState, SecurityCenterRestStub
    ):
        def __hash__(self):
            return hash("SecurityCenterRestTransport.SetFindingState")

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
            request: securitycenter_service.SetFindingStateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> finding.Finding:
            r"""Call the set finding state method over HTTP.

            Args:
                request (~.securitycenter_service.SetFindingStateRequest):
                    The request object. Request message for updating a
                finding's state.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.finding.Finding:
                    Security Command Center finding.

                A finding is a record of assessment data
                (security, risk, health or privacy)
                ingested into Security Command Center
                for presentation, notification,
                analysis, policy testing, and
                enforcement. For example, an XSS
                vulnerability in an App Engine
                application is a finding.

            """

            http_options = (
                _BaseSecurityCenterRestTransport._BaseSetFindingState._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_finding_state(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterRestTransport._BaseSetFindingState._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityCenterRestTransport._BaseSetFindingState._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterRestTransport._BaseSetFindingState._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterRestTransport._SetFindingState._get_response(
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
            resp = finding.Finding()
            pb_resp = finding.Finding.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_finding_state(resp)
            return resp

    class _SetIamPolicy(
        _BaseSecurityCenterRestTransport._BaseSetIamPolicy, SecurityCenterRestStub
    ):
        def __hash__(self):
            return hash("SecurityCenterRestTransport.SetIamPolicy")

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
                _BaseSecurityCenterRestTransport._BaseSetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            transcoded_request = _BaseSecurityCenterRestTransport._BaseSetIamPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityCenterRestTransport._BaseSetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterRestTransport._BaseSetIamPolicy._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterRestTransport._SetIamPolicy._get_response(
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
        _BaseSecurityCenterRestTransport._BaseTestIamPermissions, SecurityCenterRestStub
    ):
        def __hash__(self):
            return hash("SecurityCenterRestTransport.TestIamPermissions")

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
                _BaseSecurityCenterRestTransport._BaseTestIamPermissions._get_http_options()
            )
            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterRestTransport._BaseTestIamPermissions._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityCenterRestTransport._BaseTestIamPermissions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterRestTransport._BaseTestIamPermissions._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterRestTransport._TestIamPermissions._get_response(
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

    class _UpdateFinding(
        _BaseSecurityCenterRestTransport._BaseUpdateFinding, SecurityCenterRestStub
    ):
        def __hash__(self):
            return hash("SecurityCenterRestTransport.UpdateFinding")

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
            request: securitycenter_service.UpdateFindingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_finding.Finding:
            r"""Call the update finding method over HTTP.

            Args:
                request (~.securitycenter_service.UpdateFindingRequest):
                    The request object. Request message for updating or
                creating a finding.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_finding.Finding:
                    Security Command Center finding.

                A finding is a record of assessment data
                (security, risk, health or privacy)
                ingested into Security Command Center
                for presentation, notification,
                analysis, policy testing, and
                enforcement. For example, an XSS
                vulnerability in an App Engine
                application is a finding.

            """

            http_options = (
                _BaseSecurityCenterRestTransport._BaseUpdateFinding._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_finding(request, metadata)
            transcoded_request = _BaseSecurityCenterRestTransport._BaseUpdateFinding._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityCenterRestTransport._BaseUpdateFinding._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterRestTransport._BaseUpdateFinding._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterRestTransport._UpdateFinding._get_response(
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
            resp = gcs_finding.Finding()
            pb_resp = gcs_finding.Finding.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_finding(resp)
            return resp

    class _UpdateOrganizationSettings(
        _BaseSecurityCenterRestTransport._BaseUpdateOrganizationSettings,
        SecurityCenterRestStub,
    ):
        def __hash__(self):
            return hash("SecurityCenterRestTransport.UpdateOrganizationSettings")

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
            request: securitycenter_service.UpdateOrganizationSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_organization_settings.OrganizationSettings:
            r"""Call the update organization
            settings method over HTTP.

                Args:
                    request (~.securitycenter_service.UpdateOrganizationSettingsRequest):
                        The request object. Request message for updating an
                    organization's settings.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.gcs_organization_settings.OrganizationSettings:
                        User specified settings that are
                    attached to the Security Command Center
                    organization.

            """

            http_options = (
                _BaseSecurityCenterRestTransport._BaseUpdateOrganizationSettings._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_organization_settings(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterRestTransport._BaseUpdateOrganizationSettings._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityCenterRestTransport._BaseUpdateOrganizationSettings._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterRestTransport._BaseUpdateOrganizationSettings._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SecurityCenterRestTransport._UpdateOrganizationSettings._get_response(
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
            resp = gcs_organization_settings.OrganizationSettings()
            pb_resp = gcs_organization_settings.OrganizationSettings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_organization_settings(resp)
            return resp

    class _UpdateSecurityMarks(
        _BaseSecurityCenterRestTransport._BaseUpdateSecurityMarks,
        SecurityCenterRestStub,
    ):
        def __hash__(self):
            return hash("SecurityCenterRestTransport.UpdateSecurityMarks")

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
            request: securitycenter_service.UpdateSecurityMarksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_security_marks.SecurityMarks:
            r"""Call the update security marks method over HTTP.

            Args:
                request (~.securitycenter_service.UpdateSecurityMarksRequest):
                    The request object. Request message for updating a
                SecurityMarks resource.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_security_marks.SecurityMarks:
                    User specified security marks that
                are attached to the parent Security
                Command Center resource. Security marks
                are scoped within a Security Command
                Center organization -- they can be
                modified and viewed by all users who
                have proper permissions on the
                organization.

            """

            http_options = (
                _BaseSecurityCenterRestTransport._BaseUpdateSecurityMarks._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_security_marks(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterRestTransport._BaseUpdateSecurityMarks._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityCenterRestTransport._BaseUpdateSecurityMarks._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterRestTransport._BaseUpdateSecurityMarks._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterRestTransport._UpdateSecurityMarks._get_response(
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
            resp = gcs_security_marks.SecurityMarks()
            pb_resp = gcs_security_marks.SecurityMarks.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_security_marks(resp)
            return resp

    class _UpdateSource(
        _BaseSecurityCenterRestTransport._BaseUpdateSource, SecurityCenterRestStub
    ):
        def __hash__(self):
            return hash("SecurityCenterRestTransport.UpdateSource")

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
            request: securitycenter_service.UpdateSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_source.Source:
            r"""Call the update source method over HTTP.

            Args:
                request (~.securitycenter_service.UpdateSourceRequest):
                    The request object. Request message for updating a
                source.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_source.Source:
                    Security Command Center finding
                source. A finding source is an entity or
                a mechanism that can produce a finding.
                A source is like a container of findings
                that come from the same scanner, logger,
                monitor, etc.

            """

            http_options = (
                _BaseSecurityCenterRestTransport._BaseUpdateSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_source(request, metadata)
            transcoded_request = _BaseSecurityCenterRestTransport._BaseUpdateSource._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityCenterRestTransport._BaseUpdateSource._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterRestTransport._BaseUpdateSource._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterRestTransport._UpdateSource._get_response(
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
            resp = gcs_source.Source()
            pb_resp = gcs_source.Source.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_source(resp)
            return resp

    @property
    def create_finding(
        self,
    ) -> Callable[[securitycenter_service.CreateFindingRequest], gcs_finding.Finding]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateFinding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_source(
        self,
    ) -> Callable[[securitycenter_service.CreateSourceRequest], gcs_source.Source]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_organization_settings(
        self,
    ) -> Callable[
        [securitycenter_service.GetOrganizationSettingsRequest],
        organization_settings.OrganizationSettings,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetOrganizationSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_source(
        self,
    ) -> Callable[[securitycenter_service.GetSourceRequest], source.Source]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def group_assets(
        self,
    ) -> Callable[
        [securitycenter_service.GroupAssetsRequest],
        securitycenter_service.GroupAssetsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GroupAssets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def group_findings(
        self,
    ) -> Callable[
        [securitycenter_service.GroupFindingsRequest],
        securitycenter_service.GroupFindingsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GroupFindings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_assets(
        self,
    ) -> Callable[
        [securitycenter_service.ListAssetsRequest],
        securitycenter_service.ListAssetsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAssets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_findings(
        self,
    ) -> Callable[
        [securitycenter_service.ListFindingsRequest],
        securitycenter_service.ListFindingsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListFindings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_sources(
        self,
    ) -> Callable[
        [securitycenter_service.ListSourcesRequest],
        securitycenter_service.ListSourcesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSources(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def run_asset_discovery(
        self,
    ) -> Callable[
        [securitycenter_service.RunAssetDiscoveryRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RunAssetDiscovery(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_finding_state(
        self,
    ) -> Callable[[securitycenter_service.SetFindingStateRequest], finding.Finding]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetFindingState(self._session, self._host, self._interceptor)  # type: ignore

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
    def update_finding(
        self,
    ) -> Callable[[securitycenter_service.UpdateFindingRequest], gcs_finding.Finding]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateFinding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_organization_settings(
        self,
    ) -> Callable[
        [securitycenter_service.UpdateOrganizationSettingsRequest],
        gcs_organization_settings.OrganizationSettings,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateOrganizationSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_security_marks(
        self,
    ) -> Callable[
        [securitycenter_service.UpdateSecurityMarksRequest],
        gcs_security_marks.SecurityMarks,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSecurityMarks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_source(
        self,
    ) -> Callable[[securitycenter_service.UpdateSourceRequest], gcs_source.Source]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("SecurityCenterRestTransport",)
