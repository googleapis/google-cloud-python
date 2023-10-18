# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.cloud.container import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.container_v1.services.cluster_manager.client import ClusterManagerClient
from google.cloud.container_v1.services.cluster_manager.async_client import ClusterManagerAsyncClient

from google.cloud.container_v1.types.cluster_service import AcceleratorConfig
from google.cloud.container_v1.types.cluster_service import AdditionalNodeNetworkConfig
from google.cloud.container_v1.types.cluster_service import AdditionalPodNetworkConfig
from google.cloud.container_v1.types.cluster_service import AdditionalPodRangesConfig
from google.cloud.container_v1.types.cluster_service import AddonsConfig
from google.cloud.container_v1.types.cluster_service import AdvancedDatapathObservabilityConfig
from google.cloud.container_v1.types.cluster_service import AdvancedMachineFeatures
from google.cloud.container_v1.types.cluster_service import AuthenticatorGroupsConfig
from google.cloud.container_v1.types.cluster_service import Autopilot
from google.cloud.container_v1.types.cluster_service import AutopilotCompatibilityIssue
from google.cloud.container_v1.types.cluster_service import AutoprovisioningNodePoolDefaults
from google.cloud.container_v1.types.cluster_service import AutoUpgradeOptions
from google.cloud.container_v1.types.cluster_service import BestEffortProvisioning
from google.cloud.container_v1.types.cluster_service import BinaryAuthorization
from google.cloud.container_v1.types.cluster_service import BlueGreenSettings
from google.cloud.container_v1.types.cluster_service import CancelOperationRequest
from google.cloud.container_v1.types.cluster_service import CheckAutopilotCompatibilityRequest
from google.cloud.container_v1.types.cluster_service import CheckAutopilotCompatibilityResponse
from google.cloud.container_v1.types.cluster_service import ClientCertificateConfig
from google.cloud.container_v1.types.cluster_service import CloudRunConfig
from google.cloud.container_v1.types.cluster_service import Cluster
from google.cloud.container_v1.types.cluster_service import ClusterAutoscaling
from google.cloud.container_v1.types.cluster_service import ClusterUpdate
from google.cloud.container_v1.types.cluster_service import CompleteIPRotationRequest
from google.cloud.container_v1.types.cluster_service import CompleteNodePoolUpgradeRequest
from google.cloud.container_v1.types.cluster_service import ConfidentialNodes
from google.cloud.container_v1.types.cluster_service import ConfigConnectorConfig
from google.cloud.container_v1.types.cluster_service import CostManagementConfig
from google.cloud.container_v1.types.cluster_service import CreateClusterRequest
from google.cloud.container_v1.types.cluster_service import CreateNodePoolRequest
from google.cloud.container_v1.types.cluster_service import DailyMaintenanceWindow
from google.cloud.container_v1.types.cluster_service import DatabaseEncryption
from google.cloud.container_v1.types.cluster_service import DefaultSnatStatus
from google.cloud.container_v1.types.cluster_service import DeleteClusterRequest
from google.cloud.container_v1.types.cluster_service import DeleteNodePoolRequest
from google.cloud.container_v1.types.cluster_service import DnsCacheConfig
from google.cloud.container_v1.types.cluster_service import DNSConfig
from google.cloud.container_v1.types.cluster_service import EphemeralStorageLocalSsdConfig
from google.cloud.container_v1.types.cluster_service import FastSocket
from google.cloud.container_v1.types.cluster_service import Fleet
from google.cloud.container_v1.types.cluster_service import GatewayAPIConfig
from google.cloud.container_v1.types.cluster_service import GcePersistentDiskCsiDriverConfig
from google.cloud.container_v1.types.cluster_service import GcfsConfig
from google.cloud.container_v1.types.cluster_service import GcpFilestoreCsiDriverConfig
from google.cloud.container_v1.types.cluster_service import GcsFuseCsiDriverConfig
from google.cloud.container_v1.types.cluster_service import GetClusterRequest
from google.cloud.container_v1.types.cluster_service import GetJSONWebKeysRequest
from google.cloud.container_v1.types.cluster_service import GetJSONWebKeysResponse
from google.cloud.container_v1.types.cluster_service import GetNodePoolRequest
from google.cloud.container_v1.types.cluster_service import GetOpenIDConfigRequest
from google.cloud.container_v1.types.cluster_service import GetOpenIDConfigResponse
from google.cloud.container_v1.types.cluster_service import GetOperationRequest
from google.cloud.container_v1.types.cluster_service import GetServerConfigRequest
from google.cloud.container_v1.types.cluster_service import GkeBackupAgentConfig
from google.cloud.container_v1.types.cluster_service import GPUDriverInstallationConfig
from google.cloud.container_v1.types.cluster_service import GPUSharingConfig
from google.cloud.container_v1.types.cluster_service import HorizontalPodAutoscaling
from google.cloud.container_v1.types.cluster_service import HttpLoadBalancing
from google.cloud.container_v1.types.cluster_service import IdentityServiceConfig
from google.cloud.container_v1.types.cluster_service import ILBSubsettingConfig
from google.cloud.container_v1.types.cluster_service import IntraNodeVisibilityConfig
from google.cloud.container_v1.types.cluster_service import IPAllocationPolicy
from google.cloud.container_v1.types.cluster_service import Jwk
from google.cloud.container_v1.types.cluster_service import K8sBetaAPIConfig
from google.cloud.container_v1.types.cluster_service import KubernetesDashboard
from google.cloud.container_v1.types.cluster_service import LegacyAbac
from google.cloud.container_v1.types.cluster_service import LinuxNodeConfig
from google.cloud.container_v1.types.cluster_service import ListClustersRequest
from google.cloud.container_v1.types.cluster_service import ListClustersResponse
from google.cloud.container_v1.types.cluster_service import ListNodePoolsRequest
from google.cloud.container_v1.types.cluster_service import ListNodePoolsResponse
from google.cloud.container_v1.types.cluster_service import ListOperationsRequest
from google.cloud.container_v1.types.cluster_service import ListOperationsResponse
from google.cloud.container_v1.types.cluster_service import ListUsableSubnetworksRequest
from google.cloud.container_v1.types.cluster_service import ListUsableSubnetworksResponse
from google.cloud.container_v1.types.cluster_service import LocalNvmeSsdBlockConfig
from google.cloud.container_v1.types.cluster_service import LoggingComponentConfig
from google.cloud.container_v1.types.cluster_service import LoggingConfig
from google.cloud.container_v1.types.cluster_service import LoggingVariantConfig
from google.cloud.container_v1.types.cluster_service import MaintenanceExclusionOptions
from google.cloud.container_v1.types.cluster_service import MaintenancePolicy
from google.cloud.container_v1.types.cluster_service import MaintenanceWindow
from google.cloud.container_v1.types.cluster_service import ManagedPrometheusConfig
from google.cloud.container_v1.types.cluster_service import MasterAuth
from google.cloud.container_v1.types.cluster_service import MasterAuthorizedNetworksConfig
from google.cloud.container_v1.types.cluster_service import MaxPodsConstraint
from google.cloud.container_v1.types.cluster_service import MeshCertificates
from google.cloud.container_v1.types.cluster_service import MonitoringComponentConfig
from google.cloud.container_v1.types.cluster_service import MonitoringConfig
from google.cloud.container_v1.types.cluster_service import NetworkConfig
from google.cloud.container_v1.types.cluster_service import NetworkPolicy
from google.cloud.container_v1.types.cluster_service import NetworkPolicyConfig
from google.cloud.container_v1.types.cluster_service import NetworkTags
from google.cloud.container_v1.types.cluster_service import NodeConfig
from google.cloud.container_v1.types.cluster_service import NodeConfigDefaults
from google.cloud.container_v1.types.cluster_service import NodeKubeletConfig
from google.cloud.container_v1.types.cluster_service import NodeLabels
from google.cloud.container_v1.types.cluster_service import NodeManagement
from google.cloud.container_v1.types.cluster_service import NodeNetworkConfig
from google.cloud.container_v1.types.cluster_service import NodePool
from google.cloud.container_v1.types.cluster_service import NodePoolAutoConfig
from google.cloud.container_v1.types.cluster_service import NodePoolAutoscaling
from google.cloud.container_v1.types.cluster_service import NodePoolDefaults
from google.cloud.container_v1.types.cluster_service import NodePoolLoggingConfig
from google.cloud.container_v1.types.cluster_service import NodeTaint
from google.cloud.container_v1.types.cluster_service import NodeTaints
from google.cloud.container_v1.types.cluster_service import NotificationConfig
from google.cloud.container_v1.types.cluster_service import Operation
from google.cloud.container_v1.types.cluster_service import OperationProgress
from google.cloud.container_v1.types.cluster_service import PodCIDROverprovisionConfig
from google.cloud.container_v1.types.cluster_service import PrivateClusterConfig
from google.cloud.container_v1.types.cluster_service import PrivateClusterMasterGlobalAccessConfig
from google.cloud.container_v1.types.cluster_service import RangeInfo
from google.cloud.container_v1.types.cluster_service import RecurringTimeWindow
from google.cloud.container_v1.types.cluster_service import ReleaseChannel
from google.cloud.container_v1.types.cluster_service import ReservationAffinity
from google.cloud.container_v1.types.cluster_service import ResourceLabels
from google.cloud.container_v1.types.cluster_service import ResourceLimit
from google.cloud.container_v1.types.cluster_service import ResourceUsageExportConfig
from google.cloud.container_v1.types.cluster_service import RollbackNodePoolUpgradeRequest
from google.cloud.container_v1.types.cluster_service import SandboxConfig
from google.cloud.container_v1.types.cluster_service import SecurityBulletinEvent
from google.cloud.container_v1.types.cluster_service import SecurityPostureConfig
from google.cloud.container_v1.types.cluster_service import ServerConfig
from google.cloud.container_v1.types.cluster_service import ServiceExternalIPsConfig
from google.cloud.container_v1.types.cluster_service import SetAddonsConfigRequest
from google.cloud.container_v1.types.cluster_service import SetLabelsRequest
from google.cloud.container_v1.types.cluster_service import SetLegacyAbacRequest
from google.cloud.container_v1.types.cluster_service import SetLocationsRequest
from google.cloud.container_v1.types.cluster_service import SetLoggingServiceRequest
from google.cloud.container_v1.types.cluster_service import SetMaintenancePolicyRequest
from google.cloud.container_v1.types.cluster_service import SetMasterAuthRequest
from google.cloud.container_v1.types.cluster_service import SetMonitoringServiceRequest
from google.cloud.container_v1.types.cluster_service import SetNetworkPolicyRequest
from google.cloud.container_v1.types.cluster_service import SetNodePoolAutoscalingRequest
from google.cloud.container_v1.types.cluster_service import SetNodePoolManagementRequest
from google.cloud.container_v1.types.cluster_service import SetNodePoolSizeRequest
from google.cloud.container_v1.types.cluster_service import ShieldedInstanceConfig
from google.cloud.container_v1.types.cluster_service import ShieldedNodes
from google.cloud.container_v1.types.cluster_service import SoleTenantConfig
from google.cloud.container_v1.types.cluster_service import StartIPRotationRequest
from google.cloud.container_v1.types.cluster_service import StatusCondition
from google.cloud.container_v1.types.cluster_service import TimeWindow
from google.cloud.container_v1.types.cluster_service import UpdateClusterRequest
from google.cloud.container_v1.types.cluster_service import UpdateMasterRequest
from google.cloud.container_v1.types.cluster_service import UpdateNodePoolRequest
from google.cloud.container_v1.types.cluster_service import UpgradeAvailableEvent
from google.cloud.container_v1.types.cluster_service import UpgradeEvent
from google.cloud.container_v1.types.cluster_service import UsableSubnetwork
from google.cloud.container_v1.types.cluster_service import UsableSubnetworkSecondaryRange
from google.cloud.container_v1.types.cluster_service import VerticalPodAutoscaling
from google.cloud.container_v1.types.cluster_service import VirtualNIC
from google.cloud.container_v1.types.cluster_service import WindowsNodeConfig
from google.cloud.container_v1.types.cluster_service import WorkloadIdentityConfig
from google.cloud.container_v1.types.cluster_service import WorkloadMetadataConfig
from google.cloud.container_v1.types.cluster_service import WorkloadPolicyConfig
from google.cloud.container_v1.types.cluster_service import DatapathProvider
from google.cloud.container_v1.types.cluster_service import IPv6AccessType
from google.cloud.container_v1.types.cluster_service import NodePoolUpdateStrategy
from google.cloud.container_v1.types.cluster_service import PrivateIPv6GoogleAccess
from google.cloud.container_v1.types.cluster_service import StackType
from google.cloud.container_v1.types.cluster_service import UpgradeResourceType

__all__ = ('ClusterManagerClient',
    'ClusterManagerAsyncClient',
    'AcceleratorConfig',
    'AdditionalNodeNetworkConfig',
    'AdditionalPodNetworkConfig',
    'AdditionalPodRangesConfig',
    'AddonsConfig',
    'AdvancedDatapathObservabilityConfig',
    'AdvancedMachineFeatures',
    'AuthenticatorGroupsConfig',
    'Autopilot',
    'AutopilotCompatibilityIssue',
    'AutoprovisioningNodePoolDefaults',
    'AutoUpgradeOptions',
    'BestEffortProvisioning',
    'BinaryAuthorization',
    'BlueGreenSettings',
    'CancelOperationRequest',
    'CheckAutopilotCompatibilityRequest',
    'CheckAutopilotCompatibilityResponse',
    'ClientCertificateConfig',
    'CloudRunConfig',
    'Cluster',
    'ClusterAutoscaling',
    'ClusterUpdate',
    'CompleteIPRotationRequest',
    'CompleteNodePoolUpgradeRequest',
    'ConfidentialNodes',
    'ConfigConnectorConfig',
    'CostManagementConfig',
    'CreateClusterRequest',
    'CreateNodePoolRequest',
    'DailyMaintenanceWindow',
    'DatabaseEncryption',
    'DefaultSnatStatus',
    'DeleteClusterRequest',
    'DeleteNodePoolRequest',
    'DnsCacheConfig',
    'DNSConfig',
    'EphemeralStorageLocalSsdConfig',
    'FastSocket',
    'Fleet',
    'GatewayAPIConfig',
    'GcePersistentDiskCsiDriverConfig',
    'GcfsConfig',
    'GcpFilestoreCsiDriverConfig',
    'GcsFuseCsiDriverConfig',
    'GetClusterRequest',
    'GetJSONWebKeysRequest',
    'GetJSONWebKeysResponse',
    'GetNodePoolRequest',
    'GetOpenIDConfigRequest',
    'GetOpenIDConfigResponse',
    'GetOperationRequest',
    'GetServerConfigRequest',
    'GkeBackupAgentConfig',
    'GPUDriverInstallationConfig',
    'GPUSharingConfig',
    'HorizontalPodAutoscaling',
    'HttpLoadBalancing',
    'IdentityServiceConfig',
    'ILBSubsettingConfig',
    'IntraNodeVisibilityConfig',
    'IPAllocationPolicy',
    'Jwk',
    'K8sBetaAPIConfig',
    'KubernetesDashboard',
    'LegacyAbac',
    'LinuxNodeConfig',
    'ListClustersRequest',
    'ListClustersResponse',
    'ListNodePoolsRequest',
    'ListNodePoolsResponse',
    'ListOperationsRequest',
    'ListOperationsResponse',
    'ListUsableSubnetworksRequest',
    'ListUsableSubnetworksResponse',
    'LocalNvmeSsdBlockConfig',
    'LoggingComponentConfig',
    'LoggingConfig',
    'LoggingVariantConfig',
    'MaintenanceExclusionOptions',
    'MaintenancePolicy',
    'MaintenanceWindow',
    'ManagedPrometheusConfig',
    'MasterAuth',
    'MasterAuthorizedNetworksConfig',
    'MaxPodsConstraint',
    'MeshCertificates',
    'MonitoringComponentConfig',
    'MonitoringConfig',
    'NetworkConfig',
    'NetworkPolicy',
    'NetworkPolicyConfig',
    'NetworkTags',
    'NodeConfig',
    'NodeConfigDefaults',
    'NodeKubeletConfig',
    'NodeLabels',
    'NodeManagement',
    'NodeNetworkConfig',
    'NodePool',
    'NodePoolAutoConfig',
    'NodePoolAutoscaling',
    'NodePoolDefaults',
    'NodePoolLoggingConfig',
    'NodeTaint',
    'NodeTaints',
    'NotificationConfig',
    'Operation',
    'OperationProgress',
    'PodCIDROverprovisionConfig',
    'PrivateClusterConfig',
    'PrivateClusterMasterGlobalAccessConfig',
    'RangeInfo',
    'RecurringTimeWindow',
    'ReleaseChannel',
    'ReservationAffinity',
    'ResourceLabels',
    'ResourceLimit',
    'ResourceUsageExportConfig',
    'RollbackNodePoolUpgradeRequest',
    'SandboxConfig',
    'SecurityBulletinEvent',
    'SecurityPostureConfig',
    'ServerConfig',
    'ServiceExternalIPsConfig',
    'SetAddonsConfigRequest',
    'SetLabelsRequest',
    'SetLegacyAbacRequest',
    'SetLocationsRequest',
    'SetLoggingServiceRequest',
    'SetMaintenancePolicyRequest',
    'SetMasterAuthRequest',
    'SetMonitoringServiceRequest',
    'SetNetworkPolicyRequest',
    'SetNodePoolAutoscalingRequest',
    'SetNodePoolManagementRequest',
    'SetNodePoolSizeRequest',
    'ShieldedInstanceConfig',
    'ShieldedNodes',
    'SoleTenantConfig',
    'StartIPRotationRequest',
    'StatusCondition',
    'TimeWindow',
    'UpdateClusterRequest',
    'UpdateMasterRequest',
    'UpdateNodePoolRequest',
    'UpgradeAvailableEvent',
    'UpgradeEvent',
    'UsableSubnetwork',
    'UsableSubnetworkSecondaryRange',
    'VerticalPodAutoscaling',
    'VirtualNIC',
    'WindowsNodeConfig',
    'WorkloadIdentityConfig',
    'WorkloadMetadataConfig',
    'WorkloadPolicyConfig',
    'DatapathProvider',
    'IPv6AccessType',
    'NodePoolUpdateStrategy',
    'PrivateIPv6GoogleAccess',
    'StackType',
    'UpgradeResourceType',
)
