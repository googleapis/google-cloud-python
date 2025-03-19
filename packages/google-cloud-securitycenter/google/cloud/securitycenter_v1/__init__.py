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
from google.cloud.securitycenter_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.security_center import SecurityCenterAsyncClient, SecurityCenterClient
from .types.access import Access, Geolocation, ServiceAccountDelegationInfo
from .types.application import Application
from .types.asset import Asset
from .types.attack_exposure import AttackExposure
from .types.attack_path import AttackPath
from .types.backup_disaster_recovery import BackupDisasterRecovery
from .types.bigquery_export import BigQueryExport
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
from .types.database import Database
from .types.effective_event_threat_detection_custom_module import (
    EffectiveEventThreatDetectionCustomModule,
)
from .types.effective_security_health_analytics_custom_module import (
    EffectiveSecurityHealthAnalyticsCustomModule,
)
from .types.event_threat_detection_custom_module import EventThreatDetectionCustomModule
from .types.event_threat_detection_custom_module_validation_errors import (
    CustomModuleValidationError,
    CustomModuleValidationErrors,
    Position,
)
from .types.exfiltration import ExfilResource, Exfiltration
from .types.external_system import ExternalSystem
from .types.file import File
from .types.finding import Finding
from .types.folder import Folder
from .types.group_membership import GroupMembership
from .types.iam_binding import IamBinding
from .types.indicator import Indicator
from .types.kernel_rootkit import KernelRootkit
from .types.kubernetes import Kubernetes
from .types.label import Label
from .types.load_balancer import LoadBalancer
from .types.log_entry import CloudLoggingEntry, LogEntry
from .types.mitre_attack import MitreAttack
from .types.mute_config import MuteConfig
from .types.notebook import Notebook
from .types.notification_config import NotificationConfig
from .types.notification_message import NotificationMessage
from .types.org_policy import OrgPolicy
from .types.organization_settings import OrganizationSettings
from .types.process import EnvironmentVariable, Process
from .types.resource import (
    AwsMetadata,
    AzureMetadata,
    CloudProvider,
    Resource,
    ResourcePath,
)
from .types.resource_value_config import ResourceValue, ResourceValueConfig
from .types.run_asset_discovery_response import RunAssetDiscoveryResponse
from .types.security_health_analytics_custom_config import CustomConfig
from .types.security_health_analytics_custom_module import (
    SecurityHealthAnalyticsCustomModule,
)
from .types.security_marks import SecurityMarks
from .types.security_posture import SecurityPosture
from .types.securitycenter_service import (
    BatchCreateResourceValueConfigsRequest,
    BatchCreateResourceValueConfigsResponse,
    BulkMuteFindingsRequest,
    BulkMuteFindingsResponse,
    CreateBigQueryExportRequest,
    CreateEventThreatDetectionCustomModuleRequest,
    CreateFindingRequest,
    CreateMuteConfigRequest,
    CreateNotificationConfigRequest,
    CreateResourceValueConfigRequest,
    CreateSecurityHealthAnalyticsCustomModuleRequest,
    CreateSourceRequest,
    DeleteBigQueryExportRequest,
    DeleteEventThreatDetectionCustomModuleRequest,
    DeleteMuteConfigRequest,
    DeleteNotificationConfigRequest,
    DeleteResourceValueConfigRequest,
    DeleteSecurityHealthAnalyticsCustomModuleRequest,
    GetBigQueryExportRequest,
    GetEffectiveEventThreatDetectionCustomModuleRequest,
    GetEffectiveSecurityHealthAnalyticsCustomModuleRequest,
    GetEventThreatDetectionCustomModuleRequest,
    GetMuteConfigRequest,
    GetNotificationConfigRequest,
    GetOrganizationSettingsRequest,
    GetResourceValueConfigRequest,
    GetSecurityHealthAnalyticsCustomModuleRequest,
    GetSimulationRequest,
    GetSourceRequest,
    GetValuedResourceRequest,
    GroupAssetsRequest,
    GroupAssetsResponse,
    GroupFindingsRequest,
    GroupFindingsResponse,
    GroupResult,
    ListAssetsRequest,
    ListAssetsResponse,
    ListAttackPathsRequest,
    ListAttackPathsResponse,
    ListBigQueryExportsRequest,
    ListBigQueryExportsResponse,
    ListDescendantEventThreatDetectionCustomModulesRequest,
    ListDescendantEventThreatDetectionCustomModulesResponse,
    ListDescendantSecurityHealthAnalyticsCustomModulesRequest,
    ListDescendantSecurityHealthAnalyticsCustomModulesResponse,
    ListEffectiveEventThreatDetectionCustomModulesRequest,
    ListEffectiveEventThreatDetectionCustomModulesResponse,
    ListEffectiveSecurityHealthAnalyticsCustomModulesRequest,
    ListEffectiveSecurityHealthAnalyticsCustomModulesResponse,
    ListEventThreatDetectionCustomModulesRequest,
    ListEventThreatDetectionCustomModulesResponse,
    ListFindingsRequest,
    ListFindingsResponse,
    ListMuteConfigsRequest,
    ListMuteConfigsResponse,
    ListNotificationConfigsRequest,
    ListNotificationConfigsResponse,
    ListResourceValueConfigsRequest,
    ListResourceValueConfigsResponse,
    ListSecurityHealthAnalyticsCustomModulesRequest,
    ListSecurityHealthAnalyticsCustomModulesResponse,
    ListSourcesRequest,
    ListSourcesResponse,
    ListValuedResourcesRequest,
    ListValuedResourcesResponse,
    RunAssetDiscoveryRequest,
    SetFindingStateRequest,
    SetMuteRequest,
    SimulateSecurityHealthAnalyticsCustomModuleRequest,
    SimulateSecurityHealthAnalyticsCustomModuleResponse,
    UpdateBigQueryExportRequest,
    UpdateEventThreatDetectionCustomModuleRequest,
    UpdateExternalSystemRequest,
    UpdateFindingRequest,
    UpdateMuteConfigRequest,
    UpdateNotificationConfigRequest,
    UpdateOrganizationSettingsRequest,
    UpdateResourceValueConfigRequest,
    UpdateSecurityHealthAnalyticsCustomModuleRequest,
    UpdateSecurityMarksRequest,
    UpdateSourceRequest,
    ValidateEventThreatDetectionCustomModuleRequest,
    ValidateEventThreatDetectionCustomModuleResponse,
)
from .types.simulation import Simulation
from .types.source import Source
from .types.toxic_combination import ToxicCombination
from .types.valued_resource import ResourceValueConfigMetadata, ValuedResource
from .types.vulnerability import (
    Cve,
    Cvssv3,
    Package,
    Reference,
    SecurityBulletin,
    Vulnerability,
)

__all__ = (
    "SecurityCenterAsyncClient",
    "Access",
    "AdaptiveProtection",
    "Application",
    "Asset",
    "Attack",
    "AttackExposure",
    "AttackPath",
    "AwsMetadata",
    "AzureMetadata",
    "BackupDisasterRecovery",
    "BatchCreateResourceValueConfigsRequest",
    "BatchCreateResourceValueConfigsResponse",
    "BigQueryExport",
    "BulkMuteFindingsRequest",
    "BulkMuteFindingsResponse",
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
    "CreateEventThreatDetectionCustomModuleRequest",
    "CreateFindingRequest",
    "CreateMuteConfigRequest",
    "CreateNotificationConfigRequest",
    "CreateResourceValueConfigRequest",
    "CreateSecurityHealthAnalyticsCustomModuleRequest",
    "CreateSourceRequest",
    "CustomConfig",
    "CustomModuleValidationError",
    "CustomModuleValidationErrors",
    "Cve",
    "Cvssv3",
    "Database",
    "DeleteBigQueryExportRequest",
    "DeleteEventThreatDetectionCustomModuleRequest",
    "DeleteMuteConfigRequest",
    "DeleteNotificationConfigRequest",
    "DeleteResourceValueConfigRequest",
    "DeleteSecurityHealthAnalyticsCustomModuleRequest",
    "EffectiveEventThreatDetectionCustomModule",
    "EffectiveSecurityHealthAnalyticsCustomModule",
    "EnvironmentVariable",
    "EventThreatDetectionCustomModule",
    "ExfilResource",
    "Exfiltration",
    "ExternalSystem",
    "File",
    "Finding",
    "Folder",
    "Geolocation",
    "GetBigQueryExportRequest",
    "GetEffectiveEventThreatDetectionCustomModuleRequest",
    "GetEffectiveSecurityHealthAnalyticsCustomModuleRequest",
    "GetEventThreatDetectionCustomModuleRequest",
    "GetMuteConfigRequest",
    "GetNotificationConfigRequest",
    "GetOrganizationSettingsRequest",
    "GetResourceValueConfigRequest",
    "GetSecurityHealthAnalyticsCustomModuleRequest",
    "GetSimulationRequest",
    "GetSourceRequest",
    "GetValuedResourceRequest",
    "GroupAssetsRequest",
    "GroupAssetsResponse",
    "GroupFindingsRequest",
    "GroupFindingsResponse",
    "GroupMembership",
    "GroupResult",
    "IamBinding",
    "Indicator",
    "KernelRootkit",
    "Kubernetes",
    "Label",
    "ListAssetsRequest",
    "ListAssetsResponse",
    "ListAttackPathsRequest",
    "ListAttackPathsResponse",
    "ListBigQueryExportsRequest",
    "ListBigQueryExportsResponse",
    "ListDescendantEventThreatDetectionCustomModulesRequest",
    "ListDescendantEventThreatDetectionCustomModulesResponse",
    "ListDescendantSecurityHealthAnalyticsCustomModulesRequest",
    "ListDescendantSecurityHealthAnalyticsCustomModulesResponse",
    "ListEffectiveEventThreatDetectionCustomModulesRequest",
    "ListEffectiveEventThreatDetectionCustomModulesResponse",
    "ListEffectiveSecurityHealthAnalyticsCustomModulesRequest",
    "ListEffectiveSecurityHealthAnalyticsCustomModulesResponse",
    "ListEventThreatDetectionCustomModulesRequest",
    "ListEventThreatDetectionCustomModulesResponse",
    "ListFindingsRequest",
    "ListFindingsResponse",
    "ListMuteConfigsRequest",
    "ListMuteConfigsResponse",
    "ListNotificationConfigsRequest",
    "ListNotificationConfigsResponse",
    "ListResourceValueConfigsRequest",
    "ListResourceValueConfigsResponse",
    "ListSecurityHealthAnalyticsCustomModulesRequest",
    "ListSecurityHealthAnalyticsCustomModulesResponse",
    "ListSourcesRequest",
    "ListSourcesResponse",
    "ListValuedResourcesRequest",
    "ListValuedResourcesResponse",
    "LoadBalancer",
    "LogEntry",
    "MitreAttack",
    "MuteConfig",
    "Notebook",
    "NotificationConfig",
    "NotificationMessage",
    "OrgPolicy",
    "OrganizationSettings",
    "Package",
    "Position",
    "Process",
    "Reference",
    "Requests",
    "Resource",
    "ResourcePath",
    "ResourceValue",
    "ResourceValueConfig",
    "ResourceValueConfigMetadata",
    "RunAssetDiscoveryRequest",
    "RunAssetDiscoveryResponse",
    "SecurityBulletin",
    "SecurityCenterClient",
    "SecurityHealthAnalyticsCustomModule",
    "SecurityMarks",
    "SecurityPolicy",
    "SecurityPosture",
    "ServiceAccountDelegationInfo",
    "SetFindingStateRequest",
    "SetMuteRequest",
    "SimulateSecurityHealthAnalyticsCustomModuleRequest",
    "SimulateSecurityHealthAnalyticsCustomModuleResponse",
    "Simulation",
    "Source",
    "ToxicCombination",
    "UpdateBigQueryExportRequest",
    "UpdateEventThreatDetectionCustomModuleRequest",
    "UpdateExternalSystemRequest",
    "UpdateFindingRequest",
    "UpdateMuteConfigRequest",
    "UpdateNotificationConfigRequest",
    "UpdateOrganizationSettingsRequest",
    "UpdateResourceValueConfigRequest",
    "UpdateSecurityHealthAnalyticsCustomModuleRequest",
    "UpdateSecurityMarksRequest",
    "UpdateSourceRequest",
    "ValidateEventThreatDetectionCustomModuleRequest",
    "ValidateEventThreatDetectionCustomModuleResponse",
    "ValuedResource",
    "Vulnerability",
)
