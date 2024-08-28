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
from google.cloud.container_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.cluster_manager import ClusterManagerClient
from .services.cluster_manager import ClusterManagerAsyncClient

from .types.cluster_service import AcceleratorConfig
from .types.cluster_service import AdditionalNodeNetworkConfig
from .types.cluster_service import AdditionalPodNetworkConfig
from .types.cluster_service import AdditionalPodRangesConfig
from .types.cluster_service import AddonsConfig
from .types.cluster_service import AdvancedDatapathObservabilityConfig
from .types.cluster_service import AdvancedMachineFeatures
from .types.cluster_service import AuthenticatorGroupsConfig
from .types.cluster_service import Autopilot
from .types.cluster_service import AutopilotCompatibilityIssue
from .types.cluster_service import AutoprovisioningNodePoolDefaults
from .types.cluster_service import AutoUpgradeOptions
from .types.cluster_service import BestEffortProvisioning
from .types.cluster_service import BinaryAuthorization
from .types.cluster_service import BlueGreenSettings
from .types.cluster_service import CancelOperationRequest
from .types.cluster_service import CheckAutopilotCompatibilityRequest
from .types.cluster_service import CheckAutopilotCompatibilityResponse
from .types.cluster_service import ClientCertificateConfig
from .types.cluster_service import CloudRunConfig
from .types.cluster_service import Cluster
from .types.cluster_service import ClusterAutoscaling
from .types.cluster_service import ClusterUpdate
from .types.cluster_service import CompleteIPRotationRequest
from .types.cluster_service import CompleteNodePoolUpgradeRequest
from .types.cluster_service import ConfidentialNodes
from .types.cluster_service import ConfigConnectorConfig
from .types.cluster_service import ContainerdConfig
from .types.cluster_service import CostManagementConfig
from .types.cluster_service import CreateClusterRequest
from .types.cluster_service import CreateNodePoolRequest
from .types.cluster_service import DailyMaintenanceWindow
from .types.cluster_service import DatabaseEncryption
from .types.cluster_service import DefaultSnatStatus
from .types.cluster_service import DeleteClusterRequest
from .types.cluster_service import DeleteNodePoolRequest
from .types.cluster_service import DnsCacheConfig
from .types.cluster_service import DNSConfig
from .types.cluster_service import EnterpriseConfig
from .types.cluster_service import EphemeralStorageLocalSsdConfig
from .types.cluster_service import FastSocket
from .types.cluster_service import Fleet
from .types.cluster_service import GatewayAPIConfig
from .types.cluster_service import GcePersistentDiskCsiDriverConfig
from .types.cluster_service import GcfsConfig
from .types.cluster_service import GcpFilestoreCsiDriverConfig
from .types.cluster_service import GcsFuseCsiDriverConfig
from .types.cluster_service import GetClusterRequest
from .types.cluster_service import GetJSONWebKeysRequest
from .types.cluster_service import GetJSONWebKeysResponse
from .types.cluster_service import GetNodePoolRequest
from .types.cluster_service import GetOpenIDConfigRequest
from .types.cluster_service import GetOpenIDConfigResponse
from .types.cluster_service import GetOperationRequest
from .types.cluster_service import GetServerConfigRequest
from .types.cluster_service import GkeBackupAgentConfig
from .types.cluster_service import GPUDriverInstallationConfig
from .types.cluster_service import GPUSharingConfig
from .types.cluster_service import HorizontalPodAutoscaling
from .types.cluster_service import HttpLoadBalancing
from .types.cluster_service import IdentityServiceConfig
from .types.cluster_service import ILBSubsettingConfig
from .types.cluster_service import IntraNodeVisibilityConfig
from .types.cluster_service import IPAllocationPolicy
from .types.cluster_service import Jwk
from .types.cluster_service import K8sBetaAPIConfig
from .types.cluster_service import KubernetesDashboard
from .types.cluster_service import LegacyAbac
from .types.cluster_service import LinuxNodeConfig
from .types.cluster_service import ListClustersRequest
from .types.cluster_service import ListClustersResponse
from .types.cluster_service import ListNodePoolsRequest
from .types.cluster_service import ListNodePoolsResponse
from .types.cluster_service import ListOperationsRequest
from .types.cluster_service import ListOperationsResponse
from .types.cluster_service import ListUsableSubnetworksRequest
from .types.cluster_service import ListUsableSubnetworksResponse
from .types.cluster_service import LocalNvmeSsdBlockConfig
from .types.cluster_service import LoggingComponentConfig
from .types.cluster_service import LoggingConfig
from .types.cluster_service import LoggingVariantConfig
from .types.cluster_service import MaintenanceExclusionOptions
from .types.cluster_service import MaintenancePolicy
from .types.cluster_service import MaintenanceWindow
from .types.cluster_service import ManagedPrometheusConfig
from .types.cluster_service import MasterAuth
from .types.cluster_service import MasterAuthorizedNetworksConfig
from .types.cluster_service import MaxPodsConstraint
from .types.cluster_service import MeshCertificates
from .types.cluster_service import MonitoringComponentConfig
from .types.cluster_service import MonitoringConfig
from .types.cluster_service import NetworkConfig
from .types.cluster_service import NetworkPolicy
from .types.cluster_service import NetworkPolicyConfig
from .types.cluster_service import NetworkTags
from .types.cluster_service import NodeConfig
from .types.cluster_service import NodeConfigDefaults
from .types.cluster_service import NodeKubeletConfig
from .types.cluster_service import NodeLabels
from .types.cluster_service import NodeManagement
from .types.cluster_service import NodeNetworkConfig
from .types.cluster_service import NodePool
from .types.cluster_service import NodePoolAutoConfig
from .types.cluster_service import NodePoolAutoscaling
from .types.cluster_service import NodePoolDefaults
from .types.cluster_service import NodePoolLoggingConfig
from .types.cluster_service import NodeTaint
from .types.cluster_service import NodeTaints
from .types.cluster_service import NotificationConfig
from .types.cluster_service import Operation
from .types.cluster_service import OperationProgress
from .types.cluster_service import PodCIDROverprovisionConfig
from .types.cluster_service import PrivateClusterConfig
from .types.cluster_service import PrivateClusterMasterGlobalAccessConfig
from .types.cluster_service import RangeInfo
from .types.cluster_service import RayClusterLoggingConfig
from .types.cluster_service import RayClusterMonitoringConfig
from .types.cluster_service import RayOperatorConfig
from .types.cluster_service import RecurringTimeWindow
from .types.cluster_service import ReleaseChannel
from .types.cluster_service import ReservationAffinity
from .types.cluster_service import ResourceLabels
from .types.cluster_service import ResourceLimit
from .types.cluster_service import ResourceManagerTags
from .types.cluster_service import ResourceUsageExportConfig
from .types.cluster_service import RollbackNodePoolUpgradeRequest
from .types.cluster_service import SandboxConfig
from .types.cluster_service import SecondaryBootDisk
from .types.cluster_service import SecondaryBootDiskUpdateStrategy
from .types.cluster_service import SecurityBulletinEvent
from .types.cluster_service import SecurityPostureConfig
from .types.cluster_service import ServerConfig
from .types.cluster_service import ServiceExternalIPsConfig
from .types.cluster_service import SetAddonsConfigRequest
from .types.cluster_service import SetLabelsRequest
from .types.cluster_service import SetLegacyAbacRequest
from .types.cluster_service import SetLocationsRequest
from .types.cluster_service import SetLoggingServiceRequest
from .types.cluster_service import SetMaintenancePolicyRequest
from .types.cluster_service import SetMasterAuthRequest
from .types.cluster_service import SetMonitoringServiceRequest
from .types.cluster_service import SetNetworkPolicyRequest
from .types.cluster_service import SetNodePoolAutoscalingRequest
from .types.cluster_service import SetNodePoolManagementRequest
from .types.cluster_service import SetNodePoolSizeRequest
from .types.cluster_service import ShieldedInstanceConfig
from .types.cluster_service import ShieldedNodes
from .types.cluster_service import SoleTenantConfig
from .types.cluster_service import StartIPRotationRequest
from .types.cluster_service import StatefulHAConfig
from .types.cluster_service import StatusCondition
from .types.cluster_service import TimeWindow
from .types.cluster_service import UpdateClusterRequest
from .types.cluster_service import UpdateMasterRequest
from .types.cluster_service import UpdateNodePoolRequest
from .types.cluster_service import UpgradeAvailableEvent
from .types.cluster_service import UpgradeEvent
from .types.cluster_service import UsableSubnetwork
from .types.cluster_service import UsableSubnetworkSecondaryRange
from .types.cluster_service import VerticalPodAutoscaling
from .types.cluster_service import VirtualNIC
from .types.cluster_service import WindowsNodeConfig
from .types.cluster_service import WorkloadIdentityConfig
from .types.cluster_service import WorkloadMetadataConfig
from .types.cluster_service import WorkloadPolicyConfig
from .types.cluster_service import DatapathProvider
from .types.cluster_service import InTransitEncryptionConfig
from .types.cluster_service import IPv6AccessType
from .types.cluster_service import NodePoolUpdateStrategy
from .types.cluster_service import PrivateIPv6GoogleAccess
from .types.cluster_service import StackType
from .types.cluster_service import UpgradeResourceType

__all__ = (
    'ClusterManagerAsyncClient',
'AcceleratorConfig',
'AdditionalNodeNetworkConfig',
'AdditionalPodNetworkConfig',
'AdditionalPodRangesConfig',
'AddonsConfig',
'AdvancedDatapathObservabilityConfig',
'AdvancedMachineFeatures',
'AuthenticatorGroupsConfig',
'AutoUpgradeOptions',
'Autopilot',
'AutopilotCompatibilityIssue',
'AutoprovisioningNodePoolDefaults',
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
'ClusterManagerClient',
'ClusterUpdate',
'CompleteIPRotationRequest',
'CompleteNodePoolUpgradeRequest',
'ConfidentialNodes',
'ConfigConnectorConfig',
'ContainerdConfig',
'CostManagementConfig',
'CreateClusterRequest',
'CreateNodePoolRequest',
'DNSConfig',
'DailyMaintenanceWindow',
'DatabaseEncryption',
'DatapathProvider',
'DefaultSnatStatus',
'DeleteClusterRequest',
'DeleteNodePoolRequest',
'DnsCacheConfig',
'EnterpriseConfig',
'EphemeralStorageLocalSsdConfig',
'FastSocket',
'Fleet',
'GPUDriverInstallationConfig',
'GPUSharingConfig',
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
'HorizontalPodAutoscaling',
'HttpLoadBalancing',
'ILBSubsettingConfig',
'IPAllocationPolicy',
'IPv6AccessType',
'IdentityServiceConfig',
'InTransitEncryptionConfig',
'IntraNodeVisibilityConfig',
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
'NodePoolUpdateStrategy',
'NodeTaint',
'NodeTaints',
'NotificationConfig',
'Operation',
'OperationProgress',
'PodCIDROverprovisionConfig',
'PrivateClusterConfig',
'PrivateClusterMasterGlobalAccessConfig',
'PrivateIPv6GoogleAccess',
'RangeInfo',
'RayClusterLoggingConfig',
'RayClusterMonitoringConfig',
'RayOperatorConfig',
'RecurringTimeWindow',
'ReleaseChannel',
'ReservationAffinity',
'ResourceLabels',
'ResourceLimit',
'ResourceManagerTags',
'ResourceUsageExportConfig',
'RollbackNodePoolUpgradeRequest',
'SandboxConfig',
'SecondaryBootDisk',
'SecondaryBootDiskUpdateStrategy',
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
'StackType',
'StartIPRotationRequest',
'StatefulHAConfig',
'StatusCondition',
'TimeWindow',
'UpdateClusterRequest',
'UpdateMasterRequest',
'UpdateNodePoolRequest',
'UpgradeAvailableEvent',
'UpgradeEvent',
'UpgradeResourceType',
'UsableSubnetwork',
'UsableSubnetworkSecondaryRange',
'VerticalPodAutoscaling',
'VirtualNIC',
'WindowsNodeConfig',
'WorkloadIdentityConfig',
'WorkloadMetadataConfig',
'WorkloadPolicyConfig',
)
