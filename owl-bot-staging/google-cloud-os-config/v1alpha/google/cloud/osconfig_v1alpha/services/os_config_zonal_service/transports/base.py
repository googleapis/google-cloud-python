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
import abc
from typing import Awaitable, Callable, Dict, Optional, Sequence, Union

from google.cloud.osconfig_v1alpha import gapic_version as package_version

import google.auth  # type: ignore
import google.api_core
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.api_core import operations_v1
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account # type: ignore

from google.cloud.osconfig_v1alpha.types import instance_os_policies_compliance
from google.cloud.osconfig_v1alpha.types import inventory
from google.cloud.osconfig_v1alpha.types import os_policy_assignment_reports
from google.cloud.osconfig_v1alpha.types import os_policy_assignments
from google.cloud.osconfig_v1alpha.types import vulnerability
from google.longrunning import operations_pb2 # type: ignore

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(gapic_version=package_version.__version__)


class OsConfigZonalServiceTransport(abc.ABC):
    """Abstract transport class for OsConfigZonalService."""

    AUTH_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
    )

    DEFAULT_HOST: str = 'osconfig.googleapis.com'
    def __init__(
            self, *,
            host: str = DEFAULT_HOST,
            credentials: Optional[ga_credentials.Credentials] = None,
            credentials_file: Optional[str] = None,
            scopes: Optional[Sequence[str]] = None,
            quota_project_id: Optional[str] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            always_use_jwt_access: Optional[bool] = False,
            api_audience: Optional[str] = None,
            **kwargs,
            ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'osconfig.googleapis.com').
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

        scopes_kwargs = {"scopes": scopes, "default_scopes": self.AUTH_SCOPES}

        # Save the scopes.
        self._scopes = scopes
        if not hasattr(self, "_ignore_credentials"):
            self._ignore_credentials: bool = False

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise core_exceptions.DuplicateCredentialArgs("'credentials_file' and 'credentials' are mutually exclusive")

        if credentials_file is not None:
            credentials, _ = google.auth.load_credentials_from_file(
                                credentials_file,
                                **scopes_kwargs,
                                quota_project_id=quota_project_id
                            )
        elif credentials is None and not self._ignore_credentials:
            credentials, _ = google.auth.default(**scopes_kwargs, quota_project_id=quota_project_id)
            # Don't apply audience if the credentials file passed from user.
            if hasattr(credentials, "with_gdch_audience"):
                credentials = credentials.with_gdch_audience(api_audience if api_audience else host)

        # If the credentials are service account credentials, then always try to use self signed JWT.
        if always_use_jwt_access and isinstance(credentials, service_account.Credentials) and hasattr(service_account.Credentials, "with_always_use_jwt_access"):
            credentials = credentials.with_always_use_jwt_access(True)

        # Save the credentials.
        self._credentials = credentials

        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ':' not in host:
            host += ':443'
        self._host = host

    @property
    def host(self):
        return self._host

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.create_os_policy_assignment: gapic_v1.method.wrap_method(
                self.create_os_policy_assignment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_os_policy_assignment: gapic_v1.method.wrap_method(
                self.update_os_policy_assignment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_os_policy_assignment: gapic_v1.method.wrap_method(
                self.get_os_policy_assignment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_os_policy_assignments: gapic_v1.method.wrap_method(
                self.list_os_policy_assignments,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_os_policy_assignment_revisions: gapic_v1.method.wrap_method(
                self.list_os_policy_assignment_revisions,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_os_policy_assignment: gapic_v1.method.wrap_method(
                self.delete_os_policy_assignment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_instance_os_policies_compliance: gapic_v1.method.wrap_method(
                self.get_instance_os_policies_compliance,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_instance_os_policies_compliances: gapic_v1.method.wrap_method(
                self.list_instance_os_policies_compliances,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_os_policy_assignment_report: gapic_v1.method.wrap_method(
                self.get_os_policy_assignment_report,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_os_policy_assignment_reports: gapic_v1.method.wrap_method(
                self.list_os_policy_assignment_reports,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_inventory: gapic_v1.method.wrap_method(
                self.get_inventory,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_inventories: gapic_v1.method.wrap_method(
                self.list_inventories,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_vulnerability_report: gapic_v1.method.wrap_method(
                self.get_vulnerability_report,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_vulnerability_reports: gapic_v1.method.wrap_method(
                self.list_vulnerability_reports,
                default_timeout=None,
                client_info=client_info,
            ),
         }

    def close(self):
        """Closes resources associated with the transport.

       .. warning::
            Only call this method if the transport is NOT shared
            with other clients - this may cause errors in other clients!
        """
        raise NotImplementedError()

    @property
    def operations_client(self):
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def create_os_policy_assignment(self) -> Callable[
            [os_policy_assignments.CreateOSPolicyAssignmentRequest],
            Union[
                operations_pb2.Operation,
                Awaitable[operations_pb2.Operation]
            ]]:
        raise NotImplementedError()

    @property
    def update_os_policy_assignment(self) -> Callable[
            [os_policy_assignments.UpdateOSPolicyAssignmentRequest],
            Union[
                operations_pb2.Operation,
                Awaitable[operations_pb2.Operation]
            ]]:
        raise NotImplementedError()

    @property
    def get_os_policy_assignment(self) -> Callable[
            [os_policy_assignments.GetOSPolicyAssignmentRequest],
            Union[
                os_policy_assignments.OSPolicyAssignment,
                Awaitable[os_policy_assignments.OSPolicyAssignment]
            ]]:
        raise NotImplementedError()

    @property
    def list_os_policy_assignments(self) -> Callable[
            [os_policy_assignments.ListOSPolicyAssignmentsRequest],
            Union[
                os_policy_assignments.ListOSPolicyAssignmentsResponse,
                Awaitable[os_policy_assignments.ListOSPolicyAssignmentsResponse]
            ]]:
        raise NotImplementedError()

    @property
    def list_os_policy_assignment_revisions(self) -> Callable[
            [os_policy_assignments.ListOSPolicyAssignmentRevisionsRequest],
            Union[
                os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse,
                Awaitable[os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse]
            ]]:
        raise NotImplementedError()

    @property
    def delete_os_policy_assignment(self) -> Callable[
            [os_policy_assignments.DeleteOSPolicyAssignmentRequest],
            Union[
                operations_pb2.Operation,
                Awaitable[operations_pb2.Operation]
            ]]:
        raise NotImplementedError()

    @property
    def get_instance_os_policies_compliance(self) -> Callable[
            [instance_os_policies_compliance.GetInstanceOSPoliciesComplianceRequest],
            Union[
                instance_os_policies_compliance.InstanceOSPoliciesCompliance,
                Awaitable[instance_os_policies_compliance.InstanceOSPoliciesCompliance]
            ]]:
        raise NotImplementedError()

    @property
    def list_instance_os_policies_compliances(self) -> Callable[
            [instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesRequest],
            Union[
                instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse,
                Awaitable[instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse]
            ]]:
        raise NotImplementedError()

    @property
    def get_os_policy_assignment_report(self) -> Callable[
            [os_policy_assignment_reports.GetOSPolicyAssignmentReportRequest],
            Union[
                os_policy_assignment_reports.OSPolicyAssignmentReport,
                Awaitable[os_policy_assignment_reports.OSPolicyAssignmentReport]
            ]]:
        raise NotImplementedError()

    @property
    def list_os_policy_assignment_reports(self) -> Callable[
            [os_policy_assignment_reports.ListOSPolicyAssignmentReportsRequest],
            Union[
                os_policy_assignment_reports.ListOSPolicyAssignmentReportsResponse,
                Awaitable[os_policy_assignment_reports.ListOSPolicyAssignmentReportsResponse]
            ]]:
        raise NotImplementedError()

    @property
    def get_inventory(self) -> Callable[
            [inventory.GetInventoryRequest],
            Union[
                inventory.Inventory,
                Awaitable[inventory.Inventory]
            ]]:
        raise NotImplementedError()

    @property
    def list_inventories(self) -> Callable[
            [inventory.ListInventoriesRequest],
            Union[
                inventory.ListInventoriesResponse,
                Awaitable[inventory.ListInventoriesResponse]
            ]]:
        raise NotImplementedError()

    @property
    def get_vulnerability_report(self) -> Callable[
            [vulnerability.GetVulnerabilityReportRequest],
            Union[
                vulnerability.VulnerabilityReport,
                Awaitable[vulnerability.VulnerabilityReport]
            ]]:
        raise NotImplementedError()

    @property
    def list_vulnerability_reports(self) -> Callable[
            [vulnerability.ListVulnerabilityReportsRequest],
            Union[
                vulnerability.ListVulnerabilityReportsResponse,
                Awaitable[vulnerability.ListVulnerabilityReportsResponse]
            ]]:
        raise NotImplementedError()

    @property
    def kind(self) -> str:
        raise NotImplementedError()


__all__ = (
    'OsConfigZonalServiceTransport',
)
