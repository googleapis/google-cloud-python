# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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

import abc
import typing
import pkg_resources

from google import auth  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.securitycenter_v1beta1.types import finding
from google.cloud.securitycenter_v1beta1.types import finding as gcs_finding
from google.cloud.securitycenter_v1beta1.types import organization_settings
from google.cloud.securitycenter_v1beta1.types import (
    organization_settings as gcs_organization_settings,
)
from google.cloud.securitycenter_v1beta1.types import (
    security_marks as gcs_security_marks,
)
from google.cloud.securitycenter_v1beta1.types import securitycenter_service
from google.cloud.securitycenter_v1beta1.types import source
from google.cloud.securitycenter_v1beta1.types import source as gcs_source
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.longrunning import operations_pb2 as operations  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-securitycenter",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class SecurityCenterTransport(abc.ABC):
    """Abstract transport class for SecurityCenter."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "securitycenter.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: typing.Optional[str] = None,
        scopes: typing.Optional[typing.Sequence[str]] = AUTH_SCOPES,
        quota_project_id: typing.Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scope (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):	
                The client info used to send a user-agent string along with	
                API requests. If ``None``, then default info will be used.	
                Generally, you only need to set this if you're developing	
                your own client library.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                credentials_file, scopes=scopes, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = auth.default(
                scopes=scopes, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

        # Lifted into its own function so it can be stubbed out during tests.
        self._prep_wrapped_messages(client_info)

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.create_source: gapic_v1.method.wrap_method(
                self.create_source, default_timeout=60.0, client_info=client_info,
            ),
            self.create_finding: gapic_v1.method.wrap_method(
                self.create_finding, default_timeout=60.0, client_info=client_info,
            ),
            self.get_iam_policy: gapic_v1.method.wrap_method(
                self.get_iam_policy,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_organization_settings: gapic_v1.method.wrap_method(
                self.get_organization_settings,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_source: gapic_v1.method.wrap_method(
                self.get_source,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.group_assets: gapic_v1.method.wrap_method(
                self.group_assets,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=480.0,
                client_info=client_info,
            ),
            self.group_findings: gapic_v1.method.wrap_method(
                self.group_findings,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=480.0,
                client_info=client_info,
            ),
            self.list_assets: gapic_v1.method.wrap_method(
                self.list_assets,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=480.0,
                client_info=client_info,
            ),
            self.list_findings: gapic_v1.method.wrap_method(
                self.list_findings,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=480.0,
                client_info=client_info,
            ),
            self.list_sources: gapic_v1.method.wrap_method(
                self.list_sources,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.run_asset_discovery: gapic_v1.method.wrap_method(
                self.run_asset_discovery, default_timeout=60.0, client_info=client_info,
            ),
            self.set_finding_state: gapic_v1.method.wrap_method(
                self.set_finding_state, default_timeout=60.0, client_info=client_info,
            ),
            self.set_iam_policy: gapic_v1.method.wrap_method(
                self.set_iam_policy, default_timeout=60.0, client_info=client_info,
            ),
            self.test_iam_permissions: gapic_v1.method.wrap_method(
                self.test_iam_permissions,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_finding: gapic_v1.method.wrap_method(
                self.update_finding, default_timeout=60.0, client_info=client_info,
            ),
            self.update_organization_settings: gapic_v1.method.wrap_method(
                self.update_organization_settings,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_source: gapic_v1.method.wrap_method(
                self.update_source, default_timeout=60.0, client_info=client_info,
            ),
            self.update_security_marks: gapic_v1.method.wrap_method(
                self.update_security_marks,
                default_timeout=480.0,
                client_info=client_info,
            ),
        }

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def create_source(
        self,
    ) -> typing.Callable[
        [securitycenter_service.CreateSourceRequest],
        typing.Union[gcs_source.Source, typing.Awaitable[gcs_source.Source]],
    ]:
        raise NotImplementedError()

    @property
    def create_finding(
        self,
    ) -> typing.Callable[
        [securitycenter_service.CreateFindingRequest],
        typing.Union[gcs_finding.Finding, typing.Awaitable[gcs_finding.Finding]],
    ]:
        raise NotImplementedError()

    @property
    def get_iam_policy(
        self,
    ) -> typing.Callable[
        [iam_policy.GetIamPolicyRequest],
        typing.Union[policy.Policy, typing.Awaitable[policy.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def get_organization_settings(
        self,
    ) -> typing.Callable[
        [securitycenter_service.GetOrganizationSettingsRequest],
        typing.Union[
            organization_settings.OrganizationSettings,
            typing.Awaitable[organization_settings.OrganizationSettings],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_source(
        self,
    ) -> typing.Callable[
        [securitycenter_service.GetSourceRequest],
        typing.Union[source.Source, typing.Awaitable[source.Source]],
    ]:
        raise NotImplementedError()

    @property
    def group_assets(
        self,
    ) -> typing.Callable[
        [securitycenter_service.GroupAssetsRequest],
        typing.Union[
            securitycenter_service.GroupAssetsResponse,
            typing.Awaitable[securitycenter_service.GroupAssetsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def group_findings(
        self,
    ) -> typing.Callable[
        [securitycenter_service.GroupFindingsRequest],
        typing.Union[
            securitycenter_service.GroupFindingsResponse,
            typing.Awaitable[securitycenter_service.GroupFindingsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_assets(
        self,
    ) -> typing.Callable[
        [securitycenter_service.ListAssetsRequest],
        typing.Union[
            securitycenter_service.ListAssetsResponse,
            typing.Awaitable[securitycenter_service.ListAssetsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_findings(
        self,
    ) -> typing.Callable[
        [securitycenter_service.ListFindingsRequest],
        typing.Union[
            securitycenter_service.ListFindingsResponse,
            typing.Awaitable[securitycenter_service.ListFindingsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_sources(
        self,
    ) -> typing.Callable[
        [securitycenter_service.ListSourcesRequest],
        typing.Union[
            securitycenter_service.ListSourcesResponse,
            typing.Awaitable[securitycenter_service.ListSourcesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def run_asset_discovery(
        self,
    ) -> typing.Callable[
        [securitycenter_service.RunAssetDiscoveryRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_finding_state(
        self,
    ) -> typing.Callable[
        [securitycenter_service.SetFindingStateRequest],
        typing.Union[finding.Finding, typing.Awaitable[finding.Finding]],
    ]:
        raise NotImplementedError()

    @property
    def set_iam_policy(
        self,
    ) -> typing.Callable[
        [iam_policy.SetIamPolicyRequest],
        typing.Union[policy.Policy, typing.Awaitable[policy.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def test_iam_permissions(
        self,
    ) -> typing.Callable[
        [iam_policy.TestIamPermissionsRequest],
        typing.Union[
            iam_policy.TestIamPermissionsResponse,
            typing.Awaitable[iam_policy.TestIamPermissionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_finding(
        self,
    ) -> typing.Callable[
        [securitycenter_service.UpdateFindingRequest],
        typing.Union[gcs_finding.Finding, typing.Awaitable[gcs_finding.Finding]],
    ]:
        raise NotImplementedError()

    @property
    def update_organization_settings(
        self,
    ) -> typing.Callable[
        [securitycenter_service.UpdateOrganizationSettingsRequest],
        typing.Union[
            gcs_organization_settings.OrganizationSettings,
            typing.Awaitable[gcs_organization_settings.OrganizationSettings],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_source(
        self,
    ) -> typing.Callable[
        [securitycenter_service.UpdateSourceRequest],
        typing.Union[gcs_source.Source, typing.Awaitable[gcs_source.Source]],
    ]:
        raise NotImplementedError()

    @property
    def update_security_marks(
        self,
    ) -> typing.Callable[
        [securitycenter_service.UpdateSecurityMarksRequest],
        typing.Union[
            gcs_security_marks.SecurityMarks,
            typing.Awaitable[gcs_security_marks.SecurityMarks],
        ],
    ]:
        raise NotImplementedError()


__all__ = ("SecurityCenterTransport",)
