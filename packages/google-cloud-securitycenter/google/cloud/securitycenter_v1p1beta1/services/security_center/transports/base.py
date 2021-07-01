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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Union
import packaging.version
import pkg_resources

import google.auth  # type: ignore
import google.api_core  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.securitycenter_v1p1beta1.types import finding
from google.cloud.securitycenter_v1p1beta1.types import finding as gcs_finding
from google.cloud.securitycenter_v1p1beta1.types import notification_config
from google.cloud.securitycenter_v1p1beta1.types import (
    notification_config as gcs_notification_config,
)
from google.cloud.securitycenter_v1p1beta1.types import organization_settings
from google.cloud.securitycenter_v1p1beta1.types import (
    organization_settings as gcs_organization_settings,
)
from google.cloud.securitycenter_v1p1beta1.types import (
    security_marks as gcs_security_marks,
)
from google.cloud.securitycenter_v1p1beta1.types import securitycenter_service
from google.cloud.securitycenter_v1p1beta1.types import source
from google.cloud.securitycenter_v1p1beta1.types import source as gcs_source
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-securitycenter",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()

try:
    # google.auth.__version__ was added in 1.26.0
    _GOOGLE_AUTH_VERSION = google.auth.__version__
except AttributeError:
    try:  # try pkg_resources if it is available
        _GOOGLE_AUTH_VERSION = pkg_resources.get_distribution("google-auth").version
    except pkg_resources.DistributionNotFound:  # pragma: NO COVER
        _GOOGLE_AUTH_VERSION = None


class SecurityCenterTransport(abc.ABC):
    """Abstract transport class for SecurityCenter."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    DEFAULT_HOST: str = "securitycenter.googleapis.com"

    def __init__(
        self,
        *,
        host: str = DEFAULT_HOST,
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        scopes_kwargs = self._get_scopes_kwargs(self._host, scopes)

        # Save the scopes.
        self._scopes = scopes

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise core_exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = google.auth.load_credentials_from_file(
                credentials_file, **scopes_kwargs, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = google.auth.default(
                **scopes_kwargs, quota_project_id=quota_project_id
            )

        # If the credentials is service account credentials, then always try to use self signed JWT.
        if (
            always_use_jwt_access
            and isinstance(credentials, service_account.Credentials)
            and hasattr(service_account.Credentials, "with_always_use_jwt_access")
        ):
            credentials = credentials.with_always_use_jwt_access(True)

        # Save the credentials.
        self._credentials = credentials

    # TODO(busunkim): This method is in the base transport
    # to avoid duplicating code across the transport classes. These functions
    # should be deleted once the minimum required versions of google-auth is increased.

    # TODO: Remove this function once google-auth >= 1.25.0 is required
    @classmethod
    def _get_scopes_kwargs(
        cls, host: str, scopes: Optional[Sequence[str]]
    ) -> Dict[str, Optional[Sequence[str]]]:
        """Returns scopes kwargs to pass to google-auth methods depending on the google-auth version"""

        scopes_kwargs = {}

        if _GOOGLE_AUTH_VERSION and (
            packaging.version.parse(_GOOGLE_AUTH_VERSION)
            >= packaging.version.parse("1.25.0")
        ):
            scopes_kwargs = {"scopes": scopes, "default_scopes": cls.AUTH_SCOPES}
        else:
            scopes_kwargs = {"scopes": scopes or cls.AUTH_SCOPES}

        return scopes_kwargs

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.create_source: gapic_v1.method.wrap_method(
                self.create_source, default_timeout=60.0, client_info=client_info,
            ),
            self.create_finding: gapic_v1.method.wrap_method(
                self.create_finding, default_timeout=60.0, client_info=client_info,
            ),
            self.create_notification_config: gapic_v1.method.wrap_method(
                self.create_notification_config,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_notification_config: gapic_v1.method.wrap_method(
                self.delete_notification_config,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_iam_policy: gapic_v1.method.wrap_method(
                self.get_iam_policy,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_notification_config: gapic_v1.method.wrap_method(
                self.get_notification_config,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
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
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
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
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
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
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=480.0,
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
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=480.0,
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
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=480.0,
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
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=480.0,
                ),
                default_timeout=480.0,
                client_info=client_info,
            ),
            self.list_notification_configs: gapic_v1.method.wrap_method(
                self.list_notification_configs,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_sources: gapic_v1.method.wrap_method(
                self.list_sources,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
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
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_finding: gapic_v1.method.wrap_method(
                self.update_finding, default_timeout=60.0, client_info=client_info,
            ),
            self.update_notification_config: gapic_v1.method.wrap_method(
                self.update_notification_config,
                default_timeout=60.0,
                client_info=client_info,
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
    ) -> Callable[
        [securitycenter_service.CreateSourceRequest],
        Union[gcs_source.Source, Awaitable[gcs_source.Source]],
    ]:
        raise NotImplementedError()

    @property
    def create_finding(
        self,
    ) -> Callable[
        [securitycenter_service.CreateFindingRequest],
        Union[gcs_finding.Finding, Awaitable[gcs_finding.Finding]],
    ]:
        raise NotImplementedError()

    @property
    def create_notification_config(
        self,
    ) -> Callable[
        [securitycenter_service.CreateNotificationConfigRequest],
        Union[
            gcs_notification_config.NotificationConfig,
            Awaitable[gcs_notification_config.NotificationConfig],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_notification_config(
        self,
    ) -> Callable[
        [securitycenter_service.DeleteNotificationConfigRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def get_iam_policy(
        self,
    ) -> Callable[
        [iam_policy_pb2.GetIamPolicyRequest],
        Union[policy_pb2.Policy, Awaitable[policy_pb2.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def get_notification_config(
        self,
    ) -> Callable[
        [securitycenter_service.GetNotificationConfigRequest],
        Union[
            notification_config.NotificationConfig,
            Awaitable[notification_config.NotificationConfig],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_organization_settings(
        self,
    ) -> Callable[
        [securitycenter_service.GetOrganizationSettingsRequest],
        Union[
            organization_settings.OrganizationSettings,
            Awaitable[organization_settings.OrganizationSettings],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_source(
        self,
    ) -> Callable[
        [securitycenter_service.GetSourceRequest],
        Union[source.Source, Awaitable[source.Source]],
    ]:
        raise NotImplementedError()

    @property
    def group_assets(
        self,
    ) -> Callable[
        [securitycenter_service.GroupAssetsRequest],
        Union[
            securitycenter_service.GroupAssetsResponse,
            Awaitable[securitycenter_service.GroupAssetsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def group_findings(
        self,
    ) -> Callable[
        [securitycenter_service.GroupFindingsRequest],
        Union[
            securitycenter_service.GroupFindingsResponse,
            Awaitable[securitycenter_service.GroupFindingsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_assets(
        self,
    ) -> Callable[
        [securitycenter_service.ListAssetsRequest],
        Union[
            securitycenter_service.ListAssetsResponse,
            Awaitable[securitycenter_service.ListAssetsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_findings(
        self,
    ) -> Callable[
        [securitycenter_service.ListFindingsRequest],
        Union[
            securitycenter_service.ListFindingsResponse,
            Awaitable[securitycenter_service.ListFindingsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_notification_configs(
        self,
    ) -> Callable[
        [securitycenter_service.ListNotificationConfigsRequest],
        Union[
            securitycenter_service.ListNotificationConfigsResponse,
            Awaitable[securitycenter_service.ListNotificationConfigsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_sources(
        self,
    ) -> Callable[
        [securitycenter_service.ListSourcesRequest],
        Union[
            securitycenter_service.ListSourcesResponse,
            Awaitable[securitycenter_service.ListSourcesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def run_asset_discovery(
        self,
    ) -> Callable[
        [securitycenter_service.RunAssetDiscoveryRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_finding_state(
        self,
    ) -> Callable[
        [securitycenter_service.SetFindingStateRequest],
        Union[finding.Finding, Awaitable[finding.Finding]],
    ]:
        raise NotImplementedError()

    @property
    def set_iam_policy(
        self,
    ) -> Callable[
        [iam_policy_pb2.SetIamPolicyRequest],
        Union[policy_pb2.Policy, Awaitable[policy_pb2.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        Union[
            iam_policy_pb2.TestIamPermissionsResponse,
            Awaitable[iam_policy_pb2.TestIamPermissionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_finding(
        self,
    ) -> Callable[
        [securitycenter_service.UpdateFindingRequest],
        Union[gcs_finding.Finding, Awaitable[gcs_finding.Finding]],
    ]:
        raise NotImplementedError()

    @property
    def update_notification_config(
        self,
    ) -> Callable[
        [securitycenter_service.UpdateNotificationConfigRequest],
        Union[
            gcs_notification_config.NotificationConfig,
            Awaitable[gcs_notification_config.NotificationConfig],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_organization_settings(
        self,
    ) -> Callable[
        [securitycenter_service.UpdateOrganizationSettingsRequest],
        Union[
            gcs_organization_settings.OrganizationSettings,
            Awaitable[gcs_organization_settings.OrganizationSettings],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_source(
        self,
    ) -> Callable[
        [securitycenter_service.UpdateSourceRequest],
        Union[gcs_source.Source, Awaitable[gcs_source.Source]],
    ]:
        raise NotImplementedError()

    @property
    def update_security_marks(
        self,
    ) -> Callable[
        [securitycenter_service.UpdateSecurityMarksRequest],
        Union[
            gcs_security_marks.SecurityMarks,
            Awaitable[gcs_security_marks.SecurityMarks],
        ],
    ]:
        raise NotImplementedError()


__all__ = ("SecurityCenterTransport",)
