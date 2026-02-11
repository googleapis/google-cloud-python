# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
import sys

import google.api_core as api_core

from google.cloud.securitycenter_v2 import gapic_version as package_version

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata


from .services.security_center import SecurityCenterAsyncClient, SecurityCenterClient
from .types.access import Access, Geolocation, ServiceAccountDelegationInfo
from .types.affected_resources import AffectedResources
from .types.ai_model import AiModel
from .types.application import Application
from .types.attack_exposure import AttackExposure
from .types.attack_path import AttackPath
from .types.backup_disaster_recovery import BackupDisasterRecovery
from .types.bigquery_export import BigQueryExport
from .types.chokepoint import Chokepoint
from .types.cloud_armor import (
    AdaptiveProtection,
    Attack,
    CloudArmor,
    Requests,
    SecurityPolicy,
)
from .types.cloud_dlp_data_profile import CloudDlpDataProfile
from .types.cloud_dlp_inspection import CloudDlpInspection
from .types.compliance import Compliance
from .types.connection import Connection
from .types.contact_details import Contact, ContactDetails
from .types.container import Container
from .types.data_access_event import DataAccessEvent
from .types.data_flow_event import DataFlowEvent
from .types.data_retention_deletion_event import DataRetentionDeletionEvent
from .types.database import Database
from .types.disk import Disk
from .types.exfiltration import ExfilResource, Exfiltration
from .types.external_system import ExternalSystem
from .types.file import File
from .types.finding import Finding
from .types.folder import Folder
from .types.group_membership import GroupMembership
from .types.iam_binding import IamBinding
from .types.indicator import Indicator
from .types.ip_rules import Allowed, Denied, IpRule, IpRules
from .types.job import Job, JobState
from .types.kernel_rootkit import KernelRootkit
from .types.kubernetes import Kubernetes
from .types.label import Label
from .types.load_balancer import LoadBalancer
from .types.log_entry import CloudLoggingEntry, LogEntry
from .types.mitre_attack import MitreAttack
from .types.mute_config import MuteConfig
from .types.network import Network
from .types.notebook import Notebook
from .types.notification_config import NotificationConfig
from .types.notification_message import NotificationMessage
from .types.org_policy import OrgPolicy
from .types.process import EnvironmentVariable, Process
from .types.resource import (
    AwsMetadata,
    AzureMetadata,
    CloudProvider,
    GcpMetadata,
    Resource,
    ResourcePath,
)
from .types.resource_value_config import ResourceValue, ResourceValueConfig
from .types.security_marks import SecurityMarks
from .types.security_posture import SecurityPosture
from .types.securitycenter_service import (
    BatchCreateResourceValueConfigsRequest,
    BatchCreateResourceValueConfigsResponse,
    BigQueryDestination,
    BulkMuteFindingsRequest,
    BulkMuteFindingsResponse,
    CreateBigQueryExportRequest,
    CreateFindingRequest,
    CreateMuteConfigRequest,
    CreateNotificationConfigRequest,
    CreateResourceValueConfigRequest,
    CreateSourceRequest,
    DeleteBigQueryExportRequest,
    DeleteMuteConfigRequest,
    DeleteNotificationConfigRequest,
    DeleteResourceValueConfigRequest,
    ExportFindingsMetadata,
    ExportFindingsResponse,
    GetBigQueryExportRequest,
    GetMuteConfigRequest,
    GetNotificationConfigRequest,
    GetResourceValueConfigRequest,
    GetSimulationRequest,
    GetSourceRequest,
    GetValuedResourceRequest,
    GroupFindingsRequest,
    GroupFindingsResponse,
    GroupResult,
    ListAttackPathsRequest,
    ListAttackPathsResponse,
    ListBigQueryExportsRequest,
    ListBigQueryExportsResponse,
    ListFindingsRequest,
    ListFindingsResponse,
    ListMuteConfigsRequest,
    ListMuteConfigsResponse,
    ListNotificationConfigsRequest,
    ListNotificationConfigsResponse,
    ListResourceValueConfigsRequest,
    ListResourceValueConfigsResponse,
    ListSourcesRequest,
    ListSourcesResponse,
    ListValuedResourcesRequest,
    ListValuedResourcesResponse,
    SetFindingStateRequest,
    SetMuteRequest,
    UpdateBigQueryExportRequest,
    UpdateExternalSystemRequest,
    UpdateFindingRequest,
    UpdateMuteConfigRequest,
    UpdateNotificationConfigRequest,
    UpdateResourceValueConfigRequest,
    UpdateSecurityMarksRequest,
    UpdateSourceRequest,
)
from .types.simulation import Simulation
from .types.source import Source
from .types.toxic_combination import ToxicCombination
from .types.valued_resource import ResourceValueConfigMetadata, ValuedResource
from .types.vertex_ai import VertexAi
from .types.vulnerability import (
    Cve,
    Cvssv3,
    Cwe,
    Package,
    Reference,
    SecurityBulletin,
    Vulnerability,
)

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.cloud.securitycenter_v2")  # type: ignore
    api_core.check_dependency_versions("google.cloud.securitycenter_v2")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import sys
        import warnings

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.securitycenter_v2"
        if sys.version_info < (3, 9):
            warnings.warn(
                "You are using a non-supported Python version "
                + f"({_py_version_str}).  Google will not post any further "
                + f"updates to {_package_label} supporting this Python version. "
                + "Please upgrade to the latest Python version, or at "
                + f"least to Python 3.9, and then update {_package_label}.",
                FutureWarning,
            )
        if sys.version_info[:2] == (3, 9):
            warnings.warn(
                f"You are using a Python version ({_py_version_str}) "
                + f"which Google will stop supporting in {_package_label} in "
                + "January 2026. Please "
                + "upgrade to the latest Python version, or at "
                + "least to Python 3.10, before then, and "
                + f"then update {_package_label}.",
                FutureWarning,
            )

        def parse_version_to_tuple(version_string: str):
            """Safely converts a semantic version string to a comparable tuple of integers.
            Example: "4.25.8" -> (4, 25, 8)
            Ignores non-numeric parts and handles common version formats.
            Args:
                version_string: Version string in the format "x.y.z" or "x.y.z<suffix>"
            Returns:
                Tuple of integers for the parsed version string.
            """
            parts = []
            for part in version_string.split("."):
                try:
                    parts.append(int(part))
                except ValueError:
                    # If it's a non-numeric part (e.g., '1.0.0b1' -> 'b1'), stop here.
                    # This is a simplification compared to 'packaging.parse_version', but sufficient
                    # for comparing strictly numeric semantic versions.
                    break
            return tuple(parts)

        def _get_version(dependency_name):
            try:
                version_string: str = metadata.version(dependency_name)
                parsed_version = parse_version_to_tuple(version_string)
                return (parsed_version, version_string)
            except Exception:
                # Catch exceptions from metadata.version() (e.g., PackageNotFoundError)
                # or errors during parse_version_to_tuple
                return (None, "--")

        _dependency_package = "google.protobuf"
        _next_supported_version = "4.25.8"
        _next_supported_version_tuple = (4, 25, 8)
        _recommendation = " (we recommend 6.x)"
        (_version_used, _version_used_string) = _get_version(_dependency_package)
        if _version_used and _version_used < _next_supported_version_tuple:
            warnings.warn(
                f"Package {_package_label} depends on "
                + f"{_dependency_package}, currently installed at version "
                + f"{_version_used_string}. Future updates to "
                + f"{_package_label} will require {_dependency_package} at "
                + f"version {_next_supported_version} or higher{_recommendation}."
                + " Please ensure "
                + "that either (a) your Python environment doesn't pin the "
                + f"version of {_dependency_package}, so that updates to "
                + f"{_package_label} can require the higher version, or "
                + "(b) you manually update your Python environment to use at "
                + f"least version {_next_supported_version} of "
                + f"{_dependency_package}.",
                FutureWarning,
            )
    except Exception:
        warnings.warn(
            "Could not determine the version of Python "
            + "currently being used. To continue receiving "
            + "updates for {_package_label}, ensure you are "
            + "using a supported version of Python; see "
            + "https://devguide.python.org/versions/"
        )

__all__ = (
    "SecurityCenterAsyncClient",
    "Access",
    "AdaptiveProtection",
    "AffectedResources",
    "AiModel",
    "Allowed",
    "Application",
    "Attack",
    "AttackExposure",
    "AttackPath",
    "AwsMetadata",
    "AzureMetadata",
    "BackupDisasterRecovery",
    "BatchCreateResourceValueConfigsRequest",
    "BatchCreateResourceValueConfigsResponse",
    "BigQueryDestination",
    "BigQueryExport",
    "BulkMuteFindingsRequest",
    "BulkMuteFindingsResponse",
    "Chokepoint",
    "CloudArmor",
    "CloudDlpDataProfile",
    "CloudDlpInspection",
    "CloudLoggingEntry",
    "CloudProvider",
    "Compliance",
    "Connection",
    "Contact",
    "ContactDetails",
    "Container",
    "CreateBigQueryExportRequest",
    "CreateFindingRequest",
    "CreateMuteConfigRequest",
    "CreateNotificationConfigRequest",
    "CreateResourceValueConfigRequest",
    "CreateSourceRequest",
    "Cve",
    "Cvssv3",
    "Cwe",
    "DataAccessEvent",
    "DataFlowEvent",
    "DataRetentionDeletionEvent",
    "Database",
    "DeleteBigQueryExportRequest",
    "DeleteMuteConfigRequest",
    "DeleteNotificationConfigRequest",
    "DeleteResourceValueConfigRequest",
    "Denied",
    "Disk",
    "EnvironmentVariable",
    "ExfilResource",
    "Exfiltration",
    "ExportFindingsMetadata",
    "ExportFindingsResponse",
    "ExternalSystem",
    "File",
    "Finding",
    "Folder",
    "GcpMetadata",
    "Geolocation",
    "GetBigQueryExportRequest",
    "GetMuteConfigRequest",
    "GetNotificationConfigRequest",
    "GetResourceValueConfigRequest",
    "GetSimulationRequest",
    "GetSourceRequest",
    "GetValuedResourceRequest",
    "GroupFindingsRequest",
    "GroupFindingsResponse",
    "GroupMembership",
    "GroupResult",
    "IamBinding",
    "Indicator",
    "IpRule",
    "IpRules",
    "Job",
    "JobState",
    "KernelRootkit",
    "Kubernetes",
    "Label",
    "ListAttackPathsRequest",
    "ListAttackPathsResponse",
    "ListBigQueryExportsRequest",
    "ListBigQueryExportsResponse",
    "ListFindingsRequest",
    "ListFindingsResponse",
    "ListMuteConfigsRequest",
    "ListMuteConfigsResponse",
    "ListNotificationConfigsRequest",
    "ListNotificationConfigsResponse",
    "ListResourceValueConfigsRequest",
    "ListResourceValueConfigsResponse",
    "ListSourcesRequest",
    "ListSourcesResponse",
    "ListValuedResourcesRequest",
    "ListValuedResourcesResponse",
    "LoadBalancer",
    "LogEntry",
    "MitreAttack",
    "MuteConfig",
    "Network",
    "Notebook",
    "NotificationConfig",
    "NotificationMessage",
    "OrgPolicy",
    "Package",
    "Process",
    "Reference",
    "Requests",
    "Resource",
    "ResourcePath",
    "ResourceValue",
    "ResourceValueConfig",
    "ResourceValueConfigMetadata",
    "SecurityBulletin",
    "SecurityCenterClient",
    "SecurityMarks",
    "SecurityPolicy",
    "SecurityPosture",
    "ServiceAccountDelegationInfo",
    "SetFindingStateRequest",
    "SetMuteRequest",
    "Simulation",
    "Source",
    "ToxicCombination",
    "UpdateBigQueryExportRequest",
    "UpdateExternalSystemRequest",
    "UpdateFindingRequest",
    "UpdateMuteConfigRequest",
    "UpdateNotificationConfigRequest",
    "UpdateResourceValueConfigRequest",
    "UpdateSecurityMarksRequest",
    "UpdateSourceRequest",
    "ValuedResource",
    "VertexAi",
    "Vulnerability",
)
