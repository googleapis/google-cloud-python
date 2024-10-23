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
from google.cloud.compute import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.compute_v1.services.accelerator_types.client import AcceleratorTypesClient
from google.cloud.compute_v1.services.addresses.client import AddressesClient
from google.cloud.compute_v1.services.autoscalers.client import AutoscalersClient
from google.cloud.compute_v1.services.backend_buckets.client import BackendBucketsClient
from google.cloud.compute_v1.services.backend_services.client import BackendServicesClient
from google.cloud.compute_v1.services.disks.client import DisksClient
from google.cloud.compute_v1.services.disk_types.client import DiskTypesClient
from google.cloud.compute_v1.services.external_vpn_gateways.client import ExternalVpnGatewaysClient
from google.cloud.compute_v1.services.firewall_policies.client import FirewallPoliciesClient
from google.cloud.compute_v1.services.firewalls.client import FirewallsClient
from google.cloud.compute_v1.services.forwarding_rules.client import ForwardingRulesClient
from google.cloud.compute_v1.services.global_addresses.client import GlobalAddressesClient
from google.cloud.compute_v1.services.global_forwarding_rules.client import GlobalForwardingRulesClient
from google.cloud.compute_v1.services.global_network_endpoint_groups.client import GlobalNetworkEndpointGroupsClient
from google.cloud.compute_v1.services.global_operations.client import GlobalOperationsClient
from google.cloud.compute_v1.services.global_organization_operations.client import GlobalOrganizationOperationsClient
from google.cloud.compute_v1.services.global_public_delegated_prefixes.client import GlobalPublicDelegatedPrefixesClient
from google.cloud.compute_v1.services.health_checks.client import HealthChecksClient
from google.cloud.compute_v1.services.image_family_views.client import ImageFamilyViewsClient
from google.cloud.compute_v1.services.images.client import ImagesClient
from google.cloud.compute_v1.services.instance_group_manager_resize_requests.client import InstanceGroupManagerResizeRequestsClient
from google.cloud.compute_v1.services.instance_group_managers.client import InstanceGroupManagersClient
from google.cloud.compute_v1.services.instance_groups.client import InstanceGroupsClient
from google.cloud.compute_v1.services.instances.client import InstancesClient
from google.cloud.compute_v1.services.instance_settings_service.client import InstanceSettingsServiceClient
from google.cloud.compute_v1.services.instance_templates.client import InstanceTemplatesClient
from google.cloud.compute_v1.services.instant_snapshots.client import InstantSnapshotsClient
from google.cloud.compute_v1.services.interconnect_attachments.client import InterconnectAttachmentsClient
from google.cloud.compute_v1.services.interconnect_locations.client import InterconnectLocationsClient
from google.cloud.compute_v1.services.interconnect_remote_locations.client import InterconnectRemoteLocationsClient
from google.cloud.compute_v1.services.interconnects.client import InterconnectsClient
from google.cloud.compute_v1.services.license_codes.client import LicenseCodesClient
from google.cloud.compute_v1.services.licenses.client import LicensesClient
from google.cloud.compute_v1.services.machine_images.client import MachineImagesClient
from google.cloud.compute_v1.services.machine_types.client import MachineTypesClient
from google.cloud.compute_v1.services.network_attachments.client import NetworkAttachmentsClient
from google.cloud.compute_v1.services.network_edge_security_services.client import NetworkEdgeSecurityServicesClient
from google.cloud.compute_v1.services.network_endpoint_groups.client import NetworkEndpointGroupsClient
from google.cloud.compute_v1.services.network_firewall_policies.client import NetworkFirewallPoliciesClient
from google.cloud.compute_v1.services.networks.client import NetworksClient
from google.cloud.compute_v1.services.node_groups.client import NodeGroupsClient
from google.cloud.compute_v1.services.node_templates.client import NodeTemplatesClient
from google.cloud.compute_v1.services.node_types.client import NodeTypesClient
from google.cloud.compute_v1.services.packet_mirrorings.client import PacketMirroringsClient
from google.cloud.compute_v1.services.projects.client import ProjectsClient
from google.cloud.compute_v1.services.public_advertised_prefixes.client import PublicAdvertisedPrefixesClient
from google.cloud.compute_v1.services.public_delegated_prefixes.client import PublicDelegatedPrefixesClient
from google.cloud.compute_v1.services.region_autoscalers.client import RegionAutoscalersClient
from google.cloud.compute_v1.services.region_backend_services.client import RegionBackendServicesClient
from google.cloud.compute_v1.services.region_commitments.client import RegionCommitmentsClient
from google.cloud.compute_v1.services.region_disks.client import RegionDisksClient
from google.cloud.compute_v1.services.region_disk_types.client import RegionDiskTypesClient
from google.cloud.compute_v1.services.region_health_checks.client import RegionHealthChecksClient
from google.cloud.compute_v1.services.region_health_check_services.client import RegionHealthCheckServicesClient
from google.cloud.compute_v1.services.region_instance_group_managers.client import RegionInstanceGroupManagersClient
from google.cloud.compute_v1.services.region_instance_groups.client import RegionInstanceGroupsClient
from google.cloud.compute_v1.services.region_instances.client import RegionInstancesClient
from google.cloud.compute_v1.services.region_instance_templates.client import RegionInstanceTemplatesClient
from google.cloud.compute_v1.services.region_instant_snapshots.client import RegionInstantSnapshotsClient
from google.cloud.compute_v1.services.region_network_endpoint_groups.client import RegionNetworkEndpointGroupsClient
from google.cloud.compute_v1.services.region_network_firewall_policies.client import RegionNetworkFirewallPoliciesClient
from google.cloud.compute_v1.services.region_notification_endpoints.client import RegionNotificationEndpointsClient
from google.cloud.compute_v1.services.region_operations.client import RegionOperationsClient
from google.cloud.compute_v1.services.regions.client import RegionsClient
from google.cloud.compute_v1.services.region_security_policies.client import RegionSecurityPoliciesClient
from google.cloud.compute_v1.services.region_ssl_certificates.client import RegionSslCertificatesClient
from google.cloud.compute_v1.services.region_ssl_policies.client import RegionSslPoliciesClient
from google.cloud.compute_v1.services.region_target_http_proxies.client import RegionTargetHttpProxiesClient
from google.cloud.compute_v1.services.region_target_https_proxies.client import RegionTargetHttpsProxiesClient
from google.cloud.compute_v1.services.region_target_tcp_proxies.client import RegionTargetTcpProxiesClient
from google.cloud.compute_v1.services.region_url_maps.client import RegionUrlMapsClient
from google.cloud.compute_v1.services.region_zones.client import RegionZonesClient
from google.cloud.compute_v1.services.reservations.client import ReservationsClient
from google.cloud.compute_v1.services.resource_policies.client import ResourcePoliciesClient
from google.cloud.compute_v1.services.routers.client import RoutersClient
from google.cloud.compute_v1.services.routes.client import RoutesClient
from google.cloud.compute_v1.services.security_policies.client import SecurityPoliciesClient
from google.cloud.compute_v1.services.service_attachments.client import ServiceAttachmentsClient
from google.cloud.compute_v1.services.snapshots.client import SnapshotsClient
from google.cloud.compute_v1.services.snapshot_settings_service.client import SnapshotSettingsServiceClient
from google.cloud.compute_v1.services.ssl_certificates.client import SslCertificatesClient
from google.cloud.compute_v1.services.ssl_policies.client import SslPoliciesClient
from google.cloud.compute_v1.services.storage_pools.client import StoragePoolsClient
from google.cloud.compute_v1.services.storage_pool_types.client import StoragePoolTypesClient
from google.cloud.compute_v1.services.subnetworks.client import SubnetworksClient
from google.cloud.compute_v1.services.target_grpc_proxies.client import TargetGrpcProxiesClient
from google.cloud.compute_v1.services.target_http_proxies.client import TargetHttpProxiesClient
from google.cloud.compute_v1.services.target_https_proxies.client import TargetHttpsProxiesClient
from google.cloud.compute_v1.services.target_instances.client import TargetInstancesClient
from google.cloud.compute_v1.services.target_pools.client import TargetPoolsClient
from google.cloud.compute_v1.services.target_ssl_proxies.client import TargetSslProxiesClient
from google.cloud.compute_v1.services.target_tcp_proxies.client import TargetTcpProxiesClient
from google.cloud.compute_v1.services.target_vpn_gateways.client import TargetVpnGatewaysClient
from google.cloud.compute_v1.services.url_maps.client import UrlMapsClient
from google.cloud.compute_v1.services.vpn_gateways.client import VpnGatewaysClient
from google.cloud.compute_v1.services.vpn_tunnels.client import VpnTunnelsClient
from google.cloud.compute_v1.services.zone_operations.client import ZoneOperationsClient
from google.cloud.compute_v1.services.zones.client import ZonesClient

from google.cloud.compute_v1.types.compute import AbandonInstancesInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import AbandonInstancesRegionInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import AcceleratorConfig
from google.cloud.compute_v1.types.compute import Accelerators
from google.cloud.compute_v1.types.compute import AcceleratorType
from google.cloud.compute_v1.types.compute import AcceleratorTypeAggregatedList
from google.cloud.compute_v1.types.compute import AcceleratorTypeList
from google.cloud.compute_v1.types.compute import AcceleratorTypesScopedList
from google.cloud.compute_v1.types.compute import AccessConfig
from google.cloud.compute_v1.types.compute import AddAccessConfigInstanceRequest
from google.cloud.compute_v1.types.compute import AddAssociationFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import AddAssociationNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import AddAssociationRegionNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import AddHealthCheckTargetPoolRequest
from google.cloud.compute_v1.types.compute import AddInstancesInstanceGroupRequest
from google.cloud.compute_v1.types.compute import AddInstanceTargetPoolRequest
from google.cloud.compute_v1.types.compute import AddNodesNodeGroupRequest
from google.cloud.compute_v1.types.compute import AddPeeringNetworkRequest
from google.cloud.compute_v1.types.compute import AddResourcePoliciesDiskRequest
from google.cloud.compute_v1.types.compute import AddResourcePoliciesInstanceRequest
from google.cloud.compute_v1.types.compute import AddResourcePoliciesRegionDiskRequest
from google.cloud.compute_v1.types.compute import Address
from google.cloud.compute_v1.types.compute import AddressAggregatedList
from google.cloud.compute_v1.types.compute import AddressesScopedList
from google.cloud.compute_v1.types.compute import AddressList
from google.cloud.compute_v1.types.compute import AddRuleFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import AddRuleNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import AddRuleRegionNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import AddRuleRegionSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import AddRuleSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import AddSignedUrlKeyBackendBucketRequest
from google.cloud.compute_v1.types.compute import AddSignedUrlKeyBackendServiceRequest
from google.cloud.compute_v1.types.compute import AdvancedMachineFeatures
from google.cloud.compute_v1.types.compute import AggregatedListAcceleratorTypesRequest
from google.cloud.compute_v1.types.compute import AggregatedListAddressesRequest
from google.cloud.compute_v1.types.compute import AggregatedListAutoscalersRequest
from google.cloud.compute_v1.types.compute import AggregatedListBackendServicesRequest
from google.cloud.compute_v1.types.compute import AggregatedListDisksRequest
from google.cloud.compute_v1.types.compute import AggregatedListDiskTypesRequest
from google.cloud.compute_v1.types.compute import AggregatedListForwardingRulesRequest
from google.cloud.compute_v1.types.compute import AggregatedListGlobalOperationsRequest
from google.cloud.compute_v1.types.compute import AggregatedListHealthChecksRequest
from google.cloud.compute_v1.types.compute import AggregatedListInstanceGroupManagersRequest
from google.cloud.compute_v1.types.compute import AggregatedListInstanceGroupsRequest
from google.cloud.compute_v1.types.compute import AggregatedListInstancesRequest
from google.cloud.compute_v1.types.compute import AggregatedListInstanceTemplatesRequest
from google.cloud.compute_v1.types.compute import AggregatedListInstantSnapshotsRequest
from google.cloud.compute_v1.types.compute import AggregatedListInterconnectAttachmentsRequest
from google.cloud.compute_v1.types.compute import AggregatedListMachineTypesRequest
from google.cloud.compute_v1.types.compute import AggregatedListNetworkAttachmentsRequest
from google.cloud.compute_v1.types.compute import AggregatedListNetworkEdgeSecurityServicesRequest
from google.cloud.compute_v1.types.compute import AggregatedListNetworkEndpointGroupsRequest
from google.cloud.compute_v1.types.compute import AggregatedListNodeGroupsRequest
from google.cloud.compute_v1.types.compute import AggregatedListNodeTemplatesRequest
from google.cloud.compute_v1.types.compute import AggregatedListNodeTypesRequest
from google.cloud.compute_v1.types.compute import AggregatedListPacketMirroringsRequest
from google.cloud.compute_v1.types.compute import AggregatedListPublicDelegatedPrefixesRequest
from google.cloud.compute_v1.types.compute import AggregatedListRegionCommitmentsRequest
from google.cloud.compute_v1.types.compute import AggregatedListReservationsRequest
from google.cloud.compute_v1.types.compute import AggregatedListResourcePoliciesRequest
from google.cloud.compute_v1.types.compute import AggregatedListRoutersRequest
from google.cloud.compute_v1.types.compute import AggregatedListSecurityPoliciesRequest
from google.cloud.compute_v1.types.compute import AggregatedListServiceAttachmentsRequest
from google.cloud.compute_v1.types.compute import AggregatedListSslCertificatesRequest
from google.cloud.compute_v1.types.compute import AggregatedListSslPoliciesRequest
from google.cloud.compute_v1.types.compute import AggregatedListStoragePoolsRequest
from google.cloud.compute_v1.types.compute import AggregatedListStoragePoolTypesRequest
from google.cloud.compute_v1.types.compute import AggregatedListSubnetworksRequest
from google.cloud.compute_v1.types.compute import AggregatedListTargetHttpProxiesRequest
from google.cloud.compute_v1.types.compute import AggregatedListTargetHttpsProxiesRequest
from google.cloud.compute_v1.types.compute import AggregatedListTargetInstancesRequest
from google.cloud.compute_v1.types.compute import AggregatedListTargetPoolsRequest
from google.cloud.compute_v1.types.compute import AggregatedListTargetTcpProxiesRequest
from google.cloud.compute_v1.types.compute import AggregatedListTargetVpnGatewaysRequest
from google.cloud.compute_v1.types.compute import AggregatedListUrlMapsRequest
from google.cloud.compute_v1.types.compute import AggregatedListVpnGatewaysRequest
from google.cloud.compute_v1.types.compute import AggregatedListVpnTunnelsRequest
from google.cloud.compute_v1.types.compute import AliasIpRange
from google.cloud.compute_v1.types.compute import AllocationAggregateReservation
from google.cloud.compute_v1.types.compute import AllocationAggregateReservationReservedResourceInfo
from google.cloud.compute_v1.types.compute import AllocationAggregateReservationReservedResourceInfoAccelerator
from google.cloud.compute_v1.types.compute import AllocationResourceStatus
from google.cloud.compute_v1.types.compute import AllocationResourceStatusSpecificSKUAllocation
from google.cloud.compute_v1.types.compute import AllocationSpecificSKUAllocationAllocatedInstancePropertiesReservedDisk
from google.cloud.compute_v1.types.compute import AllocationSpecificSKUAllocationReservedInstanceProperties
from google.cloud.compute_v1.types.compute import AllocationSpecificSKUReservation
from google.cloud.compute_v1.types.compute import Allowed
from google.cloud.compute_v1.types.compute import AnnouncePublicAdvertisedPrefixeRequest
from google.cloud.compute_v1.types.compute import AnnouncePublicDelegatedPrefixeRequest
from google.cloud.compute_v1.types.compute import ApplyUpdatesToInstancesInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import AttachDiskInstanceRequest
from google.cloud.compute_v1.types.compute import AttachedDisk
from google.cloud.compute_v1.types.compute import AttachedDiskInitializeParams
from google.cloud.compute_v1.types.compute import AttachNetworkEndpointsGlobalNetworkEndpointGroupRequest
from google.cloud.compute_v1.types.compute import AttachNetworkEndpointsNetworkEndpointGroupRequest
from google.cloud.compute_v1.types.compute import AttachNetworkEndpointsRegionNetworkEndpointGroupRequest
from google.cloud.compute_v1.types.compute import AuditConfig
from google.cloud.compute_v1.types.compute import AuditLogConfig
from google.cloud.compute_v1.types.compute import AuthorizationLoggingOptions
from google.cloud.compute_v1.types.compute import Autoscaler
from google.cloud.compute_v1.types.compute import AutoscalerAggregatedList
from google.cloud.compute_v1.types.compute import AutoscalerList
from google.cloud.compute_v1.types.compute import AutoscalersScopedList
from google.cloud.compute_v1.types.compute import AutoscalerStatusDetails
from google.cloud.compute_v1.types.compute import AutoscalingPolicy
from google.cloud.compute_v1.types.compute import AutoscalingPolicyCpuUtilization
from google.cloud.compute_v1.types.compute import AutoscalingPolicyCustomMetricUtilization
from google.cloud.compute_v1.types.compute import AutoscalingPolicyLoadBalancingUtilization
from google.cloud.compute_v1.types.compute import AutoscalingPolicyScaleInControl
from google.cloud.compute_v1.types.compute import AutoscalingPolicyScalingSchedule
from google.cloud.compute_v1.types.compute import AWSV4Signature
from google.cloud.compute_v1.types.compute import Backend
from google.cloud.compute_v1.types.compute import BackendBucket
from google.cloud.compute_v1.types.compute import BackendBucketCdnPolicy
from google.cloud.compute_v1.types.compute import BackendBucketCdnPolicyBypassCacheOnRequestHeader
from google.cloud.compute_v1.types.compute import BackendBucketCdnPolicyCacheKeyPolicy
from google.cloud.compute_v1.types.compute import BackendBucketCdnPolicyNegativeCachingPolicy
from google.cloud.compute_v1.types.compute import BackendBucketList
from google.cloud.compute_v1.types.compute import BackendService
from google.cloud.compute_v1.types.compute import BackendServiceAggregatedList
from google.cloud.compute_v1.types.compute import BackendServiceCdnPolicy
from google.cloud.compute_v1.types.compute import BackendServiceCdnPolicyBypassCacheOnRequestHeader
from google.cloud.compute_v1.types.compute import BackendServiceCdnPolicyNegativeCachingPolicy
from google.cloud.compute_v1.types.compute import BackendServiceConnectionTrackingPolicy
from google.cloud.compute_v1.types.compute import BackendServiceFailoverPolicy
from google.cloud.compute_v1.types.compute import BackendServiceGroupHealth
from google.cloud.compute_v1.types.compute import BackendServiceIAP
from google.cloud.compute_v1.types.compute import BackendServiceList
from google.cloud.compute_v1.types.compute import BackendServiceListUsable
from google.cloud.compute_v1.types.compute import BackendServiceLocalityLoadBalancingPolicyConfig
from google.cloud.compute_v1.types.compute import BackendServiceLocalityLoadBalancingPolicyConfigCustomPolicy
from google.cloud.compute_v1.types.compute import BackendServiceLocalityLoadBalancingPolicyConfigPolicy
from google.cloud.compute_v1.types.compute import BackendServiceLogConfig
from google.cloud.compute_v1.types.compute import BackendServiceReference
from google.cloud.compute_v1.types.compute import BackendServicesScopedList
from google.cloud.compute_v1.types.compute import BackendServiceUsedBy
from google.cloud.compute_v1.types.compute import BfdPacket
from google.cloud.compute_v1.types.compute import BfdStatus
from google.cloud.compute_v1.types.compute import BfdStatusPacketCounts
from google.cloud.compute_v1.types.compute import Binding
from google.cloud.compute_v1.types.compute import BulkInsertDiskRequest
from google.cloud.compute_v1.types.compute import BulkInsertDiskResource
from google.cloud.compute_v1.types.compute import BulkInsertInstanceRequest
from google.cloud.compute_v1.types.compute import BulkInsertInstanceResource
from google.cloud.compute_v1.types.compute import BulkInsertInstanceResourcePerInstanceProperties
from google.cloud.compute_v1.types.compute import BulkInsertOperationStatus
from google.cloud.compute_v1.types.compute import BulkInsertRegionDiskRequest
from google.cloud.compute_v1.types.compute import BulkInsertRegionInstanceRequest
from google.cloud.compute_v1.types.compute import CacheInvalidationRule
from google.cloud.compute_v1.types.compute import CacheKeyPolicy
from google.cloud.compute_v1.types.compute import CancelInstanceGroupManagerResizeRequestRequest
from google.cloud.compute_v1.types.compute import CircuitBreakers
from google.cloud.compute_v1.types.compute import CloneRulesFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import CloneRulesNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import CloneRulesRegionNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import Commitment
from google.cloud.compute_v1.types.compute import CommitmentAggregatedList
from google.cloud.compute_v1.types.compute import CommitmentList
from google.cloud.compute_v1.types.compute import CommitmentsScopedList
from google.cloud.compute_v1.types.compute import Condition
from google.cloud.compute_v1.types.compute import ConfidentialInstanceConfig
from google.cloud.compute_v1.types.compute import ConnectionDraining
from google.cloud.compute_v1.types.compute import ConsistentHashLoadBalancerSettings
from google.cloud.compute_v1.types.compute import ConsistentHashLoadBalancerSettingsHttpCookie
from google.cloud.compute_v1.types.compute import CorsPolicy
from google.cloud.compute_v1.types.compute import CreateInstancesInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import CreateInstancesRegionInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import CreateSnapshotDiskRequest
from google.cloud.compute_v1.types.compute import CreateSnapshotRegionDiskRequest
from google.cloud.compute_v1.types.compute import CustomerEncryptionKey
from google.cloud.compute_v1.types.compute import CustomerEncryptionKeyProtectedDisk
from google.cloud.compute_v1.types.compute import Data
from google.cloud.compute_v1.types.compute import DeleteAccessConfigInstanceRequest
from google.cloud.compute_v1.types.compute import DeleteAddressRequest
from google.cloud.compute_v1.types.compute import DeleteAutoscalerRequest
from google.cloud.compute_v1.types.compute import DeleteBackendBucketRequest
from google.cloud.compute_v1.types.compute import DeleteBackendServiceRequest
from google.cloud.compute_v1.types.compute import DeleteDiskRequest
from google.cloud.compute_v1.types.compute import DeleteExternalVpnGatewayRequest
from google.cloud.compute_v1.types.compute import DeleteFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import DeleteFirewallRequest
from google.cloud.compute_v1.types.compute import DeleteForwardingRuleRequest
from google.cloud.compute_v1.types.compute import DeleteGlobalAddressRequest
from google.cloud.compute_v1.types.compute import DeleteGlobalForwardingRuleRequest
from google.cloud.compute_v1.types.compute import DeleteGlobalNetworkEndpointGroupRequest
from google.cloud.compute_v1.types.compute import DeleteGlobalOperationRequest
from google.cloud.compute_v1.types.compute import DeleteGlobalOperationResponse
from google.cloud.compute_v1.types.compute import DeleteGlobalOrganizationOperationRequest
from google.cloud.compute_v1.types.compute import DeleteGlobalOrganizationOperationResponse
from google.cloud.compute_v1.types.compute import DeleteGlobalPublicDelegatedPrefixeRequest
from google.cloud.compute_v1.types.compute import DeleteHealthCheckRequest
from google.cloud.compute_v1.types.compute import DeleteImageRequest
from google.cloud.compute_v1.types.compute import DeleteInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import DeleteInstanceGroupManagerResizeRequestRequest
from google.cloud.compute_v1.types.compute import DeleteInstanceGroupRequest
from google.cloud.compute_v1.types.compute import DeleteInstanceRequest
from google.cloud.compute_v1.types.compute import DeleteInstancesInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import DeleteInstancesRegionInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import DeleteInstanceTemplateRequest
from google.cloud.compute_v1.types.compute import DeleteInstantSnapshotRequest
from google.cloud.compute_v1.types.compute import DeleteInterconnectAttachmentRequest
from google.cloud.compute_v1.types.compute import DeleteInterconnectRequest
from google.cloud.compute_v1.types.compute import DeleteLicenseRequest
from google.cloud.compute_v1.types.compute import DeleteMachineImageRequest
from google.cloud.compute_v1.types.compute import DeleteNetworkAttachmentRequest
from google.cloud.compute_v1.types.compute import DeleteNetworkEdgeSecurityServiceRequest
from google.cloud.compute_v1.types.compute import DeleteNetworkEndpointGroupRequest
from google.cloud.compute_v1.types.compute import DeleteNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import DeleteNetworkRequest
from google.cloud.compute_v1.types.compute import DeleteNodeGroupRequest
from google.cloud.compute_v1.types.compute import DeleteNodesNodeGroupRequest
from google.cloud.compute_v1.types.compute import DeleteNodeTemplateRequest
from google.cloud.compute_v1.types.compute import DeletePacketMirroringRequest
from google.cloud.compute_v1.types.compute import DeletePerInstanceConfigsInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import DeletePerInstanceConfigsRegionInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import DeletePublicAdvertisedPrefixeRequest
from google.cloud.compute_v1.types.compute import DeletePublicDelegatedPrefixeRequest
from google.cloud.compute_v1.types.compute import DeleteRegionAutoscalerRequest
from google.cloud.compute_v1.types.compute import DeleteRegionBackendServiceRequest
from google.cloud.compute_v1.types.compute import DeleteRegionDiskRequest
from google.cloud.compute_v1.types.compute import DeleteRegionHealthCheckRequest
from google.cloud.compute_v1.types.compute import DeleteRegionHealthCheckServiceRequest
from google.cloud.compute_v1.types.compute import DeleteRegionInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import DeleteRegionInstanceTemplateRequest
from google.cloud.compute_v1.types.compute import DeleteRegionInstantSnapshotRequest
from google.cloud.compute_v1.types.compute import DeleteRegionNetworkEndpointGroupRequest
from google.cloud.compute_v1.types.compute import DeleteRegionNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import DeleteRegionNotificationEndpointRequest
from google.cloud.compute_v1.types.compute import DeleteRegionOperationRequest
from google.cloud.compute_v1.types.compute import DeleteRegionOperationResponse
from google.cloud.compute_v1.types.compute import DeleteRegionSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import DeleteRegionSslCertificateRequest
from google.cloud.compute_v1.types.compute import DeleteRegionSslPolicyRequest
from google.cloud.compute_v1.types.compute import DeleteRegionTargetHttpProxyRequest
from google.cloud.compute_v1.types.compute import DeleteRegionTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import DeleteRegionTargetTcpProxyRequest
from google.cloud.compute_v1.types.compute import DeleteRegionUrlMapRequest
from google.cloud.compute_v1.types.compute import DeleteReservationRequest
from google.cloud.compute_v1.types.compute import DeleteResourcePolicyRequest
from google.cloud.compute_v1.types.compute import DeleteRouteRequest
from google.cloud.compute_v1.types.compute import DeleteRouterRequest
from google.cloud.compute_v1.types.compute import DeleteSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import DeleteServiceAttachmentRequest
from google.cloud.compute_v1.types.compute import DeleteSignedUrlKeyBackendBucketRequest
from google.cloud.compute_v1.types.compute import DeleteSignedUrlKeyBackendServiceRequest
from google.cloud.compute_v1.types.compute import DeleteSnapshotRequest
from google.cloud.compute_v1.types.compute import DeleteSslCertificateRequest
from google.cloud.compute_v1.types.compute import DeleteSslPolicyRequest
from google.cloud.compute_v1.types.compute import DeleteStoragePoolRequest
from google.cloud.compute_v1.types.compute import DeleteSubnetworkRequest
from google.cloud.compute_v1.types.compute import DeleteTargetGrpcProxyRequest
from google.cloud.compute_v1.types.compute import DeleteTargetHttpProxyRequest
from google.cloud.compute_v1.types.compute import DeleteTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import DeleteTargetInstanceRequest
from google.cloud.compute_v1.types.compute import DeleteTargetPoolRequest
from google.cloud.compute_v1.types.compute import DeleteTargetSslProxyRequest
from google.cloud.compute_v1.types.compute import DeleteTargetTcpProxyRequest
from google.cloud.compute_v1.types.compute import DeleteTargetVpnGatewayRequest
from google.cloud.compute_v1.types.compute import DeleteUrlMapRequest
from google.cloud.compute_v1.types.compute import DeleteVpnGatewayRequest
from google.cloud.compute_v1.types.compute import DeleteVpnTunnelRequest
from google.cloud.compute_v1.types.compute import DeleteZoneOperationRequest
from google.cloud.compute_v1.types.compute import DeleteZoneOperationResponse
from google.cloud.compute_v1.types.compute import Denied
from google.cloud.compute_v1.types.compute import DeprecateImageRequest
from google.cloud.compute_v1.types.compute import DeprecationStatus
from google.cloud.compute_v1.types.compute import DetachDiskInstanceRequest
from google.cloud.compute_v1.types.compute import DetachNetworkEndpointsGlobalNetworkEndpointGroupRequest
from google.cloud.compute_v1.types.compute import DetachNetworkEndpointsNetworkEndpointGroupRequest
from google.cloud.compute_v1.types.compute import DetachNetworkEndpointsRegionNetworkEndpointGroupRequest
from google.cloud.compute_v1.types.compute import DisableXpnHostProjectRequest
from google.cloud.compute_v1.types.compute import DisableXpnResourceProjectRequest
from google.cloud.compute_v1.types.compute import Disk
from google.cloud.compute_v1.types.compute import DiskAggregatedList
from google.cloud.compute_v1.types.compute import DiskAsyncReplication
from google.cloud.compute_v1.types.compute import DiskAsyncReplicationList
from google.cloud.compute_v1.types.compute import DiskInstantiationConfig
from google.cloud.compute_v1.types.compute import DiskList
from google.cloud.compute_v1.types.compute import DiskMoveRequest
from google.cloud.compute_v1.types.compute import DiskParams
from google.cloud.compute_v1.types.compute import DiskResourceStatus
from google.cloud.compute_v1.types.compute import DiskResourceStatusAsyncReplicationStatus
from google.cloud.compute_v1.types.compute import DisksAddResourcePoliciesRequest
from google.cloud.compute_v1.types.compute import DisksRemoveResourcePoliciesRequest
from google.cloud.compute_v1.types.compute import DisksResizeRequest
from google.cloud.compute_v1.types.compute import DisksScopedList
from google.cloud.compute_v1.types.compute import DisksStartAsyncReplicationRequest
from google.cloud.compute_v1.types.compute import DisksStopGroupAsyncReplicationResource
from google.cloud.compute_v1.types.compute import DiskType
from google.cloud.compute_v1.types.compute import DiskTypeAggregatedList
from google.cloud.compute_v1.types.compute import DiskTypeList
from google.cloud.compute_v1.types.compute import DiskTypesScopedList
from google.cloud.compute_v1.types.compute import DisplayDevice
from google.cloud.compute_v1.types.compute import DistributionPolicy
from google.cloud.compute_v1.types.compute import DistributionPolicyZoneConfiguration
from google.cloud.compute_v1.types.compute import Duration
from google.cloud.compute_v1.types.compute import EnableXpnHostProjectRequest
from google.cloud.compute_v1.types.compute import EnableXpnResourceProjectRequest
from google.cloud.compute_v1.types.compute import Error
from google.cloud.compute_v1.types.compute import ErrorDetails
from google.cloud.compute_v1.types.compute import ErrorInfo
from google.cloud.compute_v1.types.compute import Errors
from google.cloud.compute_v1.types.compute import ExchangedPeeringRoute
from google.cloud.compute_v1.types.compute import ExchangedPeeringRoutesList
from google.cloud.compute_v1.types.compute import ExpandIpCidrRangeSubnetworkRequest
from google.cloud.compute_v1.types.compute import Expr
from google.cloud.compute_v1.types.compute import ExternalVpnGateway
from google.cloud.compute_v1.types.compute import ExternalVpnGatewayInterface
from google.cloud.compute_v1.types.compute import ExternalVpnGatewayList
from google.cloud.compute_v1.types.compute import FileContentBuffer
from google.cloud.compute_v1.types.compute import Firewall
from google.cloud.compute_v1.types.compute import FirewallList
from google.cloud.compute_v1.types.compute import FirewallLogConfig
from google.cloud.compute_v1.types.compute import FirewallPoliciesListAssociationsResponse
from google.cloud.compute_v1.types.compute import FirewallPolicy
from google.cloud.compute_v1.types.compute import FirewallPolicyAssociation
from google.cloud.compute_v1.types.compute import FirewallPolicyList
from google.cloud.compute_v1.types.compute import FirewallPolicyRule
from google.cloud.compute_v1.types.compute import FirewallPolicyRuleMatcher
from google.cloud.compute_v1.types.compute import FirewallPolicyRuleMatcherLayer4Config
from google.cloud.compute_v1.types.compute import FirewallPolicyRuleSecureTag
from google.cloud.compute_v1.types.compute import FixedOrPercent
from google.cloud.compute_v1.types.compute import ForwardingRule
from google.cloud.compute_v1.types.compute import ForwardingRuleAggregatedList
from google.cloud.compute_v1.types.compute import ForwardingRuleList
from google.cloud.compute_v1.types.compute import ForwardingRuleReference
from google.cloud.compute_v1.types.compute import ForwardingRuleServiceDirectoryRegistration
from google.cloud.compute_v1.types.compute import ForwardingRulesScopedList
from google.cloud.compute_v1.types.compute import GetAcceleratorTypeRequest
from google.cloud.compute_v1.types.compute import GetAddressRequest
from google.cloud.compute_v1.types.compute import GetAssociationFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import GetAssociationNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import GetAssociationRegionNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import GetAutoscalerRequest
from google.cloud.compute_v1.types.compute import GetBackendBucketRequest
from google.cloud.compute_v1.types.compute import GetBackendServiceRequest
from google.cloud.compute_v1.types.compute import GetDiagnosticsInterconnectRequest
from google.cloud.compute_v1.types.compute import GetDiskRequest
from google.cloud.compute_v1.types.compute import GetDiskTypeRequest
from google.cloud.compute_v1.types.compute import GetEffectiveFirewallsInstanceRequest
from google.cloud.compute_v1.types.compute import GetEffectiveFirewallsNetworkRequest
from google.cloud.compute_v1.types.compute import GetEffectiveFirewallsRegionNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import GetExternalVpnGatewayRequest
from google.cloud.compute_v1.types.compute import GetFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import GetFirewallRequest
from google.cloud.compute_v1.types.compute import GetForwardingRuleRequest
from google.cloud.compute_v1.types.compute import GetFromFamilyImageRequest
from google.cloud.compute_v1.types.compute import GetGlobalAddressRequest
from google.cloud.compute_v1.types.compute import GetGlobalForwardingRuleRequest
from google.cloud.compute_v1.types.compute import GetGlobalNetworkEndpointGroupRequest
from google.cloud.compute_v1.types.compute import GetGlobalOperationRequest
from google.cloud.compute_v1.types.compute import GetGlobalOrganizationOperationRequest
from google.cloud.compute_v1.types.compute import GetGlobalPublicDelegatedPrefixeRequest
from google.cloud.compute_v1.types.compute import GetGuestAttributesInstanceRequest
from google.cloud.compute_v1.types.compute import GetHealthBackendServiceRequest
from google.cloud.compute_v1.types.compute import GetHealthCheckRequest
from google.cloud.compute_v1.types.compute import GetHealthRegionBackendServiceRequest
from google.cloud.compute_v1.types.compute import GetHealthTargetPoolRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyBackendBucketRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyBackendServiceRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyDiskRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyImageRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyInstanceRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyInstanceTemplateRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyInstantSnapshotRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyLicenseRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyMachineImageRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyNetworkAttachmentRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyNodeGroupRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyNodeTemplateRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyRegionBackendServiceRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyRegionDiskRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyRegionInstantSnapshotRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyRegionNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyReservationRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyResourcePolicyRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyServiceAttachmentRequest
from google.cloud.compute_v1.types.compute import GetIamPolicySnapshotRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyStoragePoolRequest
from google.cloud.compute_v1.types.compute import GetIamPolicySubnetworkRequest
from google.cloud.compute_v1.types.compute import GetImageFamilyViewRequest
from google.cloud.compute_v1.types.compute import GetImageRequest
from google.cloud.compute_v1.types.compute import GetInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import GetInstanceGroupManagerResizeRequestRequest
from google.cloud.compute_v1.types.compute import GetInstanceGroupRequest
from google.cloud.compute_v1.types.compute import GetInstanceRequest
from google.cloud.compute_v1.types.compute import GetInstanceSettingRequest
from google.cloud.compute_v1.types.compute import GetInstanceTemplateRequest
from google.cloud.compute_v1.types.compute import GetInstantSnapshotRequest
from google.cloud.compute_v1.types.compute import GetInterconnectAttachmentRequest
from google.cloud.compute_v1.types.compute import GetInterconnectLocationRequest
from google.cloud.compute_v1.types.compute import GetInterconnectRemoteLocationRequest
from google.cloud.compute_v1.types.compute import GetInterconnectRequest
from google.cloud.compute_v1.types.compute import GetLicenseCodeRequest
from google.cloud.compute_v1.types.compute import GetLicenseRequest
from google.cloud.compute_v1.types.compute import GetMachineImageRequest
from google.cloud.compute_v1.types.compute import GetMachineTypeRequest
from google.cloud.compute_v1.types.compute import GetMacsecConfigInterconnectRequest
from google.cloud.compute_v1.types.compute import GetNatIpInfoRouterRequest
from google.cloud.compute_v1.types.compute import GetNatMappingInfoRoutersRequest
from google.cloud.compute_v1.types.compute import GetNetworkAttachmentRequest
from google.cloud.compute_v1.types.compute import GetNetworkEdgeSecurityServiceRequest
from google.cloud.compute_v1.types.compute import GetNetworkEndpointGroupRequest
from google.cloud.compute_v1.types.compute import GetNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import GetNetworkRequest
from google.cloud.compute_v1.types.compute import GetNodeGroupRequest
from google.cloud.compute_v1.types.compute import GetNodeTemplateRequest
from google.cloud.compute_v1.types.compute import GetNodeTypeRequest
from google.cloud.compute_v1.types.compute import GetPacketMirroringRequest
from google.cloud.compute_v1.types.compute import GetProjectRequest
from google.cloud.compute_v1.types.compute import GetPublicAdvertisedPrefixeRequest
from google.cloud.compute_v1.types.compute import GetPublicDelegatedPrefixeRequest
from google.cloud.compute_v1.types.compute import GetRegionAutoscalerRequest
from google.cloud.compute_v1.types.compute import GetRegionBackendServiceRequest
from google.cloud.compute_v1.types.compute import GetRegionCommitmentRequest
from google.cloud.compute_v1.types.compute import GetRegionDiskRequest
from google.cloud.compute_v1.types.compute import GetRegionDiskTypeRequest
from google.cloud.compute_v1.types.compute import GetRegionHealthCheckRequest
from google.cloud.compute_v1.types.compute import GetRegionHealthCheckServiceRequest
from google.cloud.compute_v1.types.compute import GetRegionInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import GetRegionInstanceGroupRequest
from google.cloud.compute_v1.types.compute import GetRegionInstanceTemplateRequest
from google.cloud.compute_v1.types.compute import GetRegionInstantSnapshotRequest
from google.cloud.compute_v1.types.compute import GetRegionNetworkEndpointGroupRequest
from google.cloud.compute_v1.types.compute import GetRegionNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import GetRegionNotificationEndpointRequest
from google.cloud.compute_v1.types.compute import GetRegionOperationRequest
from google.cloud.compute_v1.types.compute import GetRegionRequest
from google.cloud.compute_v1.types.compute import GetRegionSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import GetRegionSslCertificateRequest
from google.cloud.compute_v1.types.compute import GetRegionSslPolicyRequest
from google.cloud.compute_v1.types.compute import GetRegionTargetHttpProxyRequest
from google.cloud.compute_v1.types.compute import GetRegionTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import GetRegionTargetTcpProxyRequest
from google.cloud.compute_v1.types.compute import GetRegionUrlMapRequest
from google.cloud.compute_v1.types.compute import GetReservationRequest
from google.cloud.compute_v1.types.compute import GetResourcePolicyRequest
from google.cloud.compute_v1.types.compute import GetRouteRequest
from google.cloud.compute_v1.types.compute import GetRouterRequest
from google.cloud.compute_v1.types.compute import GetRouterStatusRouterRequest
from google.cloud.compute_v1.types.compute import GetRuleFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import GetRuleNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import GetRuleRegionNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import GetRuleRegionSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import GetRuleSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import GetScreenshotInstanceRequest
from google.cloud.compute_v1.types.compute import GetSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import GetSerialPortOutputInstanceRequest
from google.cloud.compute_v1.types.compute import GetServiceAttachmentRequest
from google.cloud.compute_v1.types.compute import GetShieldedInstanceIdentityInstanceRequest
from google.cloud.compute_v1.types.compute import GetSnapshotRequest
from google.cloud.compute_v1.types.compute import GetSnapshotSettingRequest
from google.cloud.compute_v1.types.compute import GetSslCertificateRequest
from google.cloud.compute_v1.types.compute import GetSslPolicyRequest
from google.cloud.compute_v1.types.compute import GetStatusVpnGatewayRequest
from google.cloud.compute_v1.types.compute import GetStoragePoolRequest
from google.cloud.compute_v1.types.compute import GetStoragePoolTypeRequest
from google.cloud.compute_v1.types.compute import GetSubnetworkRequest
from google.cloud.compute_v1.types.compute import GetTargetGrpcProxyRequest
from google.cloud.compute_v1.types.compute import GetTargetHttpProxyRequest
from google.cloud.compute_v1.types.compute import GetTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import GetTargetInstanceRequest
from google.cloud.compute_v1.types.compute import GetTargetPoolRequest
from google.cloud.compute_v1.types.compute import GetTargetSslProxyRequest
from google.cloud.compute_v1.types.compute import GetTargetTcpProxyRequest
from google.cloud.compute_v1.types.compute import GetTargetVpnGatewayRequest
from google.cloud.compute_v1.types.compute import GetUrlMapRequest
from google.cloud.compute_v1.types.compute import GetVpnGatewayRequest
from google.cloud.compute_v1.types.compute import GetVpnTunnelRequest
from google.cloud.compute_v1.types.compute import GetXpnHostProjectRequest
from google.cloud.compute_v1.types.compute import GetXpnResourcesProjectsRequest
from google.cloud.compute_v1.types.compute import GetZoneOperationRequest
from google.cloud.compute_v1.types.compute import GetZoneRequest
from google.cloud.compute_v1.types.compute import GlobalAddressesMoveRequest
from google.cloud.compute_v1.types.compute import GlobalNetworkEndpointGroupsAttachEndpointsRequest
from google.cloud.compute_v1.types.compute import GlobalNetworkEndpointGroupsDetachEndpointsRequest
from google.cloud.compute_v1.types.compute import GlobalOrganizationSetPolicyRequest
from google.cloud.compute_v1.types.compute import GlobalSetLabelsRequest
from google.cloud.compute_v1.types.compute import GlobalSetPolicyRequest
from google.cloud.compute_v1.types.compute import GRPCHealthCheck
from google.cloud.compute_v1.types.compute import GuestAttributes
from google.cloud.compute_v1.types.compute import GuestAttributesEntry
from google.cloud.compute_v1.types.compute import GuestAttributesValue
from google.cloud.compute_v1.types.compute import GuestOsFeature
from google.cloud.compute_v1.types.compute import HealthCheck
from google.cloud.compute_v1.types.compute import HealthCheckList
from google.cloud.compute_v1.types.compute import HealthCheckLogConfig
from google.cloud.compute_v1.types.compute import HealthCheckReference
from google.cloud.compute_v1.types.compute import HealthChecksAggregatedList
from google.cloud.compute_v1.types.compute import HealthCheckService
from google.cloud.compute_v1.types.compute import HealthCheckServiceReference
from google.cloud.compute_v1.types.compute import HealthCheckServicesList
from google.cloud.compute_v1.types.compute import HealthChecksScopedList
from google.cloud.compute_v1.types.compute import HealthStatus
from google.cloud.compute_v1.types.compute import HealthStatusForNetworkEndpoint
from google.cloud.compute_v1.types.compute import Help
from google.cloud.compute_v1.types.compute import HelpLink
from google.cloud.compute_v1.types.compute import HostRule
from google.cloud.compute_v1.types.compute import HTTP2HealthCheck
from google.cloud.compute_v1.types.compute import HttpFaultAbort
from google.cloud.compute_v1.types.compute import HttpFaultDelay
from google.cloud.compute_v1.types.compute import HttpFaultInjection
from google.cloud.compute_v1.types.compute import HttpHeaderAction
from google.cloud.compute_v1.types.compute import HttpHeaderMatch
from google.cloud.compute_v1.types.compute import HttpHeaderOption
from google.cloud.compute_v1.types.compute import HTTPHealthCheck
from google.cloud.compute_v1.types.compute import HttpQueryParameterMatch
from google.cloud.compute_v1.types.compute import HttpRedirectAction
from google.cloud.compute_v1.types.compute import HttpRetryPolicy
from google.cloud.compute_v1.types.compute import HttpRouteAction
from google.cloud.compute_v1.types.compute import HttpRouteRule
from google.cloud.compute_v1.types.compute import HttpRouteRuleMatch
from google.cloud.compute_v1.types.compute import HTTPSHealthCheck
from google.cloud.compute_v1.types.compute import Image
from google.cloud.compute_v1.types.compute import ImageFamilyView
from google.cloud.compute_v1.types.compute import ImageList
from google.cloud.compute_v1.types.compute import InitialStateConfig
from google.cloud.compute_v1.types.compute import InsertAddressRequest
from google.cloud.compute_v1.types.compute import InsertAutoscalerRequest
from google.cloud.compute_v1.types.compute import InsertBackendBucketRequest
from google.cloud.compute_v1.types.compute import InsertBackendServiceRequest
from google.cloud.compute_v1.types.compute import InsertDiskRequest
from google.cloud.compute_v1.types.compute import InsertExternalVpnGatewayRequest
from google.cloud.compute_v1.types.compute import InsertFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import InsertFirewallRequest
from google.cloud.compute_v1.types.compute import InsertForwardingRuleRequest
from google.cloud.compute_v1.types.compute import InsertGlobalAddressRequest
from google.cloud.compute_v1.types.compute import InsertGlobalForwardingRuleRequest
from google.cloud.compute_v1.types.compute import InsertGlobalNetworkEndpointGroupRequest
from google.cloud.compute_v1.types.compute import InsertGlobalPublicDelegatedPrefixeRequest
from google.cloud.compute_v1.types.compute import InsertHealthCheckRequest
from google.cloud.compute_v1.types.compute import InsertImageRequest
from google.cloud.compute_v1.types.compute import InsertInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import InsertInstanceGroupManagerResizeRequestRequest
from google.cloud.compute_v1.types.compute import InsertInstanceGroupRequest
from google.cloud.compute_v1.types.compute import InsertInstanceRequest
from google.cloud.compute_v1.types.compute import InsertInstanceTemplateRequest
from google.cloud.compute_v1.types.compute import InsertInstantSnapshotRequest
from google.cloud.compute_v1.types.compute import InsertInterconnectAttachmentRequest
from google.cloud.compute_v1.types.compute import InsertInterconnectRequest
from google.cloud.compute_v1.types.compute import InsertLicenseRequest
from google.cloud.compute_v1.types.compute import InsertMachineImageRequest
from google.cloud.compute_v1.types.compute import InsertNetworkAttachmentRequest
from google.cloud.compute_v1.types.compute import InsertNetworkEdgeSecurityServiceRequest
from google.cloud.compute_v1.types.compute import InsertNetworkEndpointGroupRequest
from google.cloud.compute_v1.types.compute import InsertNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import InsertNetworkRequest
from google.cloud.compute_v1.types.compute import InsertNodeGroupRequest
from google.cloud.compute_v1.types.compute import InsertNodeTemplateRequest
from google.cloud.compute_v1.types.compute import InsertPacketMirroringRequest
from google.cloud.compute_v1.types.compute import InsertPublicAdvertisedPrefixeRequest
from google.cloud.compute_v1.types.compute import InsertPublicDelegatedPrefixeRequest
from google.cloud.compute_v1.types.compute import InsertRegionAutoscalerRequest
from google.cloud.compute_v1.types.compute import InsertRegionBackendServiceRequest
from google.cloud.compute_v1.types.compute import InsertRegionCommitmentRequest
from google.cloud.compute_v1.types.compute import InsertRegionDiskRequest
from google.cloud.compute_v1.types.compute import InsertRegionHealthCheckRequest
from google.cloud.compute_v1.types.compute import InsertRegionHealthCheckServiceRequest
from google.cloud.compute_v1.types.compute import InsertRegionInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import InsertRegionInstanceTemplateRequest
from google.cloud.compute_v1.types.compute import InsertRegionInstantSnapshotRequest
from google.cloud.compute_v1.types.compute import InsertRegionNetworkEndpointGroupRequest
from google.cloud.compute_v1.types.compute import InsertRegionNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import InsertRegionNotificationEndpointRequest
from google.cloud.compute_v1.types.compute import InsertRegionSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import InsertRegionSslCertificateRequest
from google.cloud.compute_v1.types.compute import InsertRegionSslPolicyRequest
from google.cloud.compute_v1.types.compute import InsertRegionTargetHttpProxyRequest
from google.cloud.compute_v1.types.compute import InsertRegionTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import InsertRegionTargetTcpProxyRequest
from google.cloud.compute_v1.types.compute import InsertRegionUrlMapRequest
from google.cloud.compute_v1.types.compute import InsertReservationRequest
from google.cloud.compute_v1.types.compute import InsertResourcePolicyRequest
from google.cloud.compute_v1.types.compute import InsertRouteRequest
from google.cloud.compute_v1.types.compute import InsertRouterRequest
from google.cloud.compute_v1.types.compute import InsertSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import InsertServiceAttachmentRequest
from google.cloud.compute_v1.types.compute import InsertSnapshotRequest
from google.cloud.compute_v1.types.compute import InsertSslCertificateRequest
from google.cloud.compute_v1.types.compute import InsertSslPolicyRequest
from google.cloud.compute_v1.types.compute import InsertStoragePoolRequest
from google.cloud.compute_v1.types.compute import InsertSubnetworkRequest
from google.cloud.compute_v1.types.compute import InsertTargetGrpcProxyRequest
from google.cloud.compute_v1.types.compute import InsertTargetHttpProxyRequest
from google.cloud.compute_v1.types.compute import InsertTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import InsertTargetInstanceRequest
from google.cloud.compute_v1.types.compute import InsertTargetPoolRequest
from google.cloud.compute_v1.types.compute import InsertTargetSslProxyRequest
from google.cloud.compute_v1.types.compute import InsertTargetTcpProxyRequest
from google.cloud.compute_v1.types.compute import InsertTargetVpnGatewayRequest
from google.cloud.compute_v1.types.compute import InsertUrlMapRequest
from google.cloud.compute_v1.types.compute import InsertVpnGatewayRequest
from google.cloud.compute_v1.types.compute import InsertVpnTunnelRequest
from google.cloud.compute_v1.types.compute import Instance
from google.cloud.compute_v1.types.compute import InstanceAggregatedList
from google.cloud.compute_v1.types.compute import InstanceConsumptionData
from google.cloud.compute_v1.types.compute import InstanceConsumptionInfo
from google.cloud.compute_v1.types.compute import InstanceGroup
from google.cloud.compute_v1.types.compute import InstanceGroupAggregatedList
from google.cloud.compute_v1.types.compute import InstanceGroupList
from google.cloud.compute_v1.types.compute import InstanceGroupManager
from google.cloud.compute_v1.types.compute import InstanceGroupManagerActionsSummary
from google.cloud.compute_v1.types.compute import InstanceGroupManagerAggregatedList
from google.cloud.compute_v1.types.compute import InstanceGroupManagerAllInstancesConfig
from google.cloud.compute_v1.types.compute import InstanceGroupManagerAutoHealingPolicy
from google.cloud.compute_v1.types.compute import InstanceGroupManagerInstanceLifecyclePolicy
from google.cloud.compute_v1.types.compute import InstanceGroupManagerList
from google.cloud.compute_v1.types.compute import InstanceGroupManagerResizeRequest
from google.cloud.compute_v1.types.compute import InstanceGroupManagerResizeRequestsListResponse
from google.cloud.compute_v1.types.compute import InstanceGroupManagerResizeRequestStatus
from google.cloud.compute_v1.types.compute import InstanceGroupManagerResizeRequestStatusLastAttempt
from google.cloud.compute_v1.types.compute import InstanceGroupManagersAbandonInstancesRequest
from google.cloud.compute_v1.types.compute import InstanceGroupManagersApplyUpdatesRequest
from google.cloud.compute_v1.types.compute import InstanceGroupManagersCreateInstancesRequest
from google.cloud.compute_v1.types.compute import InstanceGroupManagersDeleteInstancesRequest
from google.cloud.compute_v1.types.compute import InstanceGroupManagersDeletePerInstanceConfigsReq
from google.cloud.compute_v1.types.compute import InstanceGroupManagersListErrorsResponse
from google.cloud.compute_v1.types.compute import InstanceGroupManagersListManagedInstancesResponse
from google.cloud.compute_v1.types.compute import InstanceGroupManagersListPerInstanceConfigsResp
from google.cloud.compute_v1.types.compute import InstanceGroupManagersPatchPerInstanceConfigsReq
from google.cloud.compute_v1.types.compute import InstanceGroupManagersRecreateInstancesRequest
from google.cloud.compute_v1.types.compute import InstanceGroupManagersScopedList
from google.cloud.compute_v1.types.compute import InstanceGroupManagersSetInstanceTemplateRequest
from google.cloud.compute_v1.types.compute import InstanceGroupManagersSetTargetPoolsRequest
from google.cloud.compute_v1.types.compute import InstanceGroupManagerStatus
from google.cloud.compute_v1.types.compute import InstanceGroupManagerStatusAllInstancesConfig
from google.cloud.compute_v1.types.compute import InstanceGroupManagerStatusStateful
from google.cloud.compute_v1.types.compute import InstanceGroupManagerStatusStatefulPerInstanceConfigs
from google.cloud.compute_v1.types.compute import InstanceGroupManagerStatusVersionTarget
from google.cloud.compute_v1.types.compute import InstanceGroupManagersUpdatePerInstanceConfigsReq
from google.cloud.compute_v1.types.compute import InstanceGroupManagerUpdatePolicy
from google.cloud.compute_v1.types.compute import InstanceGroupManagerVersion
from google.cloud.compute_v1.types.compute import InstanceGroupsAddInstancesRequest
from google.cloud.compute_v1.types.compute import InstanceGroupsListInstances
from google.cloud.compute_v1.types.compute import InstanceGroupsListInstancesRequest
from google.cloud.compute_v1.types.compute import InstanceGroupsRemoveInstancesRequest
from google.cloud.compute_v1.types.compute import InstanceGroupsScopedList
from google.cloud.compute_v1.types.compute import InstanceGroupsSetNamedPortsRequest
from google.cloud.compute_v1.types.compute import InstanceList
from google.cloud.compute_v1.types.compute import InstanceListReferrers
from google.cloud.compute_v1.types.compute import InstanceManagedByIgmError
from google.cloud.compute_v1.types.compute import InstanceManagedByIgmErrorInstanceActionDetails
from google.cloud.compute_v1.types.compute import InstanceManagedByIgmErrorManagedInstanceError
from google.cloud.compute_v1.types.compute import InstanceMoveRequest
from google.cloud.compute_v1.types.compute import InstanceParams
from google.cloud.compute_v1.types.compute import InstanceProperties
from google.cloud.compute_v1.types.compute import InstancePropertiesPatch
from google.cloud.compute_v1.types.compute import InstanceReference
from google.cloud.compute_v1.types.compute import InstancesAddResourcePoliciesRequest
from google.cloud.compute_v1.types.compute import InstancesBulkInsertOperationMetadata
from google.cloud.compute_v1.types.compute import InstanceSettings
from google.cloud.compute_v1.types.compute import InstanceSettingsMetadata
from google.cloud.compute_v1.types.compute import InstancesGetEffectiveFirewallsResponse
from google.cloud.compute_v1.types.compute import InstancesGetEffectiveFirewallsResponseEffectiveFirewallPolicy
from google.cloud.compute_v1.types.compute import InstancesRemoveResourcePoliciesRequest
from google.cloud.compute_v1.types.compute import InstancesScopedList
from google.cloud.compute_v1.types.compute import InstancesSetLabelsRequest
from google.cloud.compute_v1.types.compute import InstancesSetMachineResourcesRequest
from google.cloud.compute_v1.types.compute import InstancesSetMachineTypeRequest
from google.cloud.compute_v1.types.compute import InstancesSetMinCpuPlatformRequest
from google.cloud.compute_v1.types.compute import InstancesSetNameRequest
from google.cloud.compute_v1.types.compute import InstancesSetSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import InstancesSetServiceAccountRequest
from google.cloud.compute_v1.types.compute import InstancesStartWithEncryptionKeyRequest
from google.cloud.compute_v1.types.compute import InstanceTemplate
from google.cloud.compute_v1.types.compute import InstanceTemplateAggregatedList
from google.cloud.compute_v1.types.compute import InstanceTemplateList
from google.cloud.compute_v1.types.compute import InstanceTemplatesScopedList
from google.cloud.compute_v1.types.compute import InstanceWithNamedPorts
from google.cloud.compute_v1.types.compute import InstantSnapshot
from google.cloud.compute_v1.types.compute import InstantSnapshotAggregatedList
from google.cloud.compute_v1.types.compute import InstantSnapshotList
from google.cloud.compute_v1.types.compute import InstantSnapshotResourceStatus
from google.cloud.compute_v1.types.compute import InstantSnapshotsScopedList
from google.cloud.compute_v1.types.compute import Int64RangeMatch
from google.cloud.compute_v1.types.compute import Interconnect
from google.cloud.compute_v1.types.compute import InterconnectAttachment
from google.cloud.compute_v1.types.compute import InterconnectAttachmentAggregatedList
from google.cloud.compute_v1.types.compute import InterconnectAttachmentConfigurationConstraints
from google.cloud.compute_v1.types.compute import InterconnectAttachmentConfigurationConstraintsBgpPeerASNRange
from google.cloud.compute_v1.types.compute import InterconnectAttachmentList
from google.cloud.compute_v1.types.compute import InterconnectAttachmentPartnerMetadata
from google.cloud.compute_v1.types.compute import InterconnectAttachmentPrivateInfo
from google.cloud.compute_v1.types.compute import InterconnectAttachmentsScopedList
from google.cloud.compute_v1.types.compute import InterconnectCircuitInfo
from google.cloud.compute_v1.types.compute import InterconnectDiagnostics
from google.cloud.compute_v1.types.compute import InterconnectDiagnosticsARPEntry
from google.cloud.compute_v1.types.compute import InterconnectDiagnosticsLinkLACPStatus
from google.cloud.compute_v1.types.compute import InterconnectDiagnosticsLinkOpticalPower
from google.cloud.compute_v1.types.compute import InterconnectDiagnosticsLinkStatus
from google.cloud.compute_v1.types.compute import InterconnectDiagnosticsMacsecStatus
from google.cloud.compute_v1.types.compute import InterconnectList
from google.cloud.compute_v1.types.compute import InterconnectLocation
from google.cloud.compute_v1.types.compute import InterconnectLocationList
from google.cloud.compute_v1.types.compute import InterconnectLocationRegionInfo
from google.cloud.compute_v1.types.compute import InterconnectMacsec
from google.cloud.compute_v1.types.compute import InterconnectMacsecConfig
from google.cloud.compute_v1.types.compute import InterconnectMacsecConfigPreSharedKey
from google.cloud.compute_v1.types.compute import InterconnectMacsecPreSharedKey
from google.cloud.compute_v1.types.compute import InterconnectOutageNotification
from google.cloud.compute_v1.types.compute import InterconnectRemoteLocation
from google.cloud.compute_v1.types.compute import InterconnectRemoteLocationConstraints
from google.cloud.compute_v1.types.compute import InterconnectRemoteLocationConstraintsSubnetLengthRange
from google.cloud.compute_v1.types.compute import InterconnectRemoteLocationList
from google.cloud.compute_v1.types.compute import InterconnectRemoteLocationPermittedConnections
from google.cloud.compute_v1.types.compute import InterconnectsGetDiagnosticsResponse
from google.cloud.compute_v1.types.compute import InterconnectsGetMacsecConfigResponse
from google.cloud.compute_v1.types.compute import InvalidateCacheUrlMapRequest
from google.cloud.compute_v1.types.compute import Items
from google.cloud.compute_v1.types.compute import License
from google.cloud.compute_v1.types.compute import LicenseCode
from google.cloud.compute_v1.types.compute import LicenseCodeLicenseAlias
from google.cloud.compute_v1.types.compute import LicenseResourceCommitment
from google.cloud.compute_v1.types.compute import LicenseResourceRequirements
from google.cloud.compute_v1.types.compute import LicensesListResponse
from google.cloud.compute_v1.types.compute import ListAcceleratorTypesRequest
from google.cloud.compute_v1.types.compute import ListAddressesRequest
from google.cloud.compute_v1.types.compute import ListAssociationsFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import ListAutoscalersRequest
from google.cloud.compute_v1.types.compute import ListAvailableFeaturesRegionSslPoliciesRequest
from google.cloud.compute_v1.types.compute import ListAvailableFeaturesSslPoliciesRequest
from google.cloud.compute_v1.types.compute import ListBackendBucketsRequest
from google.cloud.compute_v1.types.compute import ListBackendServicesRequest
from google.cloud.compute_v1.types.compute import ListDisksRequest
from google.cloud.compute_v1.types.compute import ListDisksStoragePoolsRequest
from google.cloud.compute_v1.types.compute import ListDiskTypesRequest
from google.cloud.compute_v1.types.compute import ListErrorsInstanceGroupManagersRequest
from google.cloud.compute_v1.types.compute import ListErrorsRegionInstanceGroupManagersRequest
from google.cloud.compute_v1.types.compute import ListExternalVpnGatewaysRequest
from google.cloud.compute_v1.types.compute import ListFirewallPoliciesRequest
from google.cloud.compute_v1.types.compute import ListFirewallsRequest
from google.cloud.compute_v1.types.compute import ListForwardingRulesRequest
from google.cloud.compute_v1.types.compute import ListGlobalAddressesRequest
from google.cloud.compute_v1.types.compute import ListGlobalForwardingRulesRequest
from google.cloud.compute_v1.types.compute import ListGlobalNetworkEndpointGroupsRequest
from google.cloud.compute_v1.types.compute import ListGlobalOperationsRequest
from google.cloud.compute_v1.types.compute import ListGlobalOrganizationOperationsRequest
from google.cloud.compute_v1.types.compute import ListGlobalPublicDelegatedPrefixesRequest
from google.cloud.compute_v1.types.compute import ListHealthChecksRequest
from google.cloud.compute_v1.types.compute import ListImagesRequest
from google.cloud.compute_v1.types.compute import ListInstanceGroupManagerResizeRequestsRequest
from google.cloud.compute_v1.types.compute import ListInstanceGroupManagersRequest
from google.cloud.compute_v1.types.compute import ListInstanceGroupsRequest
from google.cloud.compute_v1.types.compute import ListInstancesInstanceGroupsRequest
from google.cloud.compute_v1.types.compute import ListInstancesRegionInstanceGroupsRequest
from google.cloud.compute_v1.types.compute import ListInstancesRequest
from google.cloud.compute_v1.types.compute import ListInstanceTemplatesRequest
from google.cloud.compute_v1.types.compute import ListInstantSnapshotsRequest
from google.cloud.compute_v1.types.compute import ListInterconnectAttachmentsRequest
from google.cloud.compute_v1.types.compute import ListInterconnectLocationsRequest
from google.cloud.compute_v1.types.compute import ListInterconnectRemoteLocationsRequest
from google.cloud.compute_v1.types.compute import ListInterconnectsRequest
from google.cloud.compute_v1.types.compute import ListLicensesRequest
from google.cloud.compute_v1.types.compute import ListMachineImagesRequest
from google.cloud.compute_v1.types.compute import ListMachineTypesRequest
from google.cloud.compute_v1.types.compute import ListManagedInstancesInstanceGroupManagersRequest
from google.cloud.compute_v1.types.compute import ListManagedInstancesRegionInstanceGroupManagersRequest
from google.cloud.compute_v1.types.compute import ListNetworkAttachmentsRequest
from google.cloud.compute_v1.types.compute import ListNetworkEndpointGroupsRequest
from google.cloud.compute_v1.types.compute import ListNetworkEndpointsGlobalNetworkEndpointGroupsRequest
from google.cloud.compute_v1.types.compute import ListNetworkEndpointsNetworkEndpointGroupsRequest
from google.cloud.compute_v1.types.compute import ListNetworkEndpointsRegionNetworkEndpointGroupsRequest
from google.cloud.compute_v1.types.compute import ListNetworkFirewallPoliciesRequest
from google.cloud.compute_v1.types.compute import ListNetworksRequest
from google.cloud.compute_v1.types.compute import ListNodeGroupsRequest
from google.cloud.compute_v1.types.compute import ListNodesNodeGroupsRequest
from google.cloud.compute_v1.types.compute import ListNodeTemplatesRequest
from google.cloud.compute_v1.types.compute import ListNodeTypesRequest
from google.cloud.compute_v1.types.compute import ListPacketMirroringsRequest
from google.cloud.compute_v1.types.compute import ListPeeringRoutesNetworksRequest
from google.cloud.compute_v1.types.compute import ListPerInstanceConfigsInstanceGroupManagersRequest
from google.cloud.compute_v1.types.compute import ListPerInstanceConfigsRegionInstanceGroupManagersRequest
from google.cloud.compute_v1.types.compute import ListPreconfiguredExpressionSetsSecurityPoliciesRequest
from google.cloud.compute_v1.types.compute import ListPublicAdvertisedPrefixesRequest
from google.cloud.compute_v1.types.compute import ListPublicDelegatedPrefixesRequest
from google.cloud.compute_v1.types.compute import ListReferrersInstancesRequest
from google.cloud.compute_v1.types.compute import ListRegionAutoscalersRequest
from google.cloud.compute_v1.types.compute import ListRegionBackendServicesRequest
from google.cloud.compute_v1.types.compute import ListRegionCommitmentsRequest
from google.cloud.compute_v1.types.compute import ListRegionDisksRequest
from google.cloud.compute_v1.types.compute import ListRegionDiskTypesRequest
from google.cloud.compute_v1.types.compute import ListRegionHealthCheckServicesRequest
from google.cloud.compute_v1.types.compute import ListRegionHealthChecksRequest
from google.cloud.compute_v1.types.compute import ListRegionInstanceGroupManagersRequest
from google.cloud.compute_v1.types.compute import ListRegionInstanceGroupsRequest
from google.cloud.compute_v1.types.compute import ListRegionInstanceTemplatesRequest
from google.cloud.compute_v1.types.compute import ListRegionInstantSnapshotsRequest
from google.cloud.compute_v1.types.compute import ListRegionNetworkEndpointGroupsRequest
from google.cloud.compute_v1.types.compute import ListRegionNetworkFirewallPoliciesRequest
from google.cloud.compute_v1.types.compute import ListRegionNotificationEndpointsRequest
from google.cloud.compute_v1.types.compute import ListRegionOperationsRequest
from google.cloud.compute_v1.types.compute import ListRegionSecurityPoliciesRequest
from google.cloud.compute_v1.types.compute import ListRegionsRequest
from google.cloud.compute_v1.types.compute import ListRegionSslCertificatesRequest
from google.cloud.compute_v1.types.compute import ListRegionSslPoliciesRequest
from google.cloud.compute_v1.types.compute import ListRegionTargetHttpProxiesRequest
from google.cloud.compute_v1.types.compute import ListRegionTargetHttpsProxiesRequest
from google.cloud.compute_v1.types.compute import ListRegionTargetTcpProxiesRequest
from google.cloud.compute_v1.types.compute import ListRegionUrlMapsRequest
from google.cloud.compute_v1.types.compute import ListRegionZonesRequest
from google.cloud.compute_v1.types.compute import ListReservationsRequest
from google.cloud.compute_v1.types.compute import ListResourcePoliciesRequest
from google.cloud.compute_v1.types.compute import ListRoutersRequest
from google.cloud.compute_v1.types.compute import ListRoutesRequest
from google.cloud.compute_v1.types.compute import ListSecurityPoliciesRequest
from google.cloud.compute_v1.types.compute import ListServiceAttachmentsRequest
from google.cloud.compute_v1.types.compute import ListSnapshotsRequest
from google.cloud.compute_v1.types.compute import ListSslCertificatesRequest
from google.cloud.compute_v1.types.compute import ListSslPoliciesRequest
from google.cloud.compute_v1.types.compute import ListStoragePoolsRequest
from google.cloud.compute_v1.types.compute import ListStoragePoolTypesRequest
from google.cloud.compute_v1.types.compute import ListSubnetworksRequest
from google.cloud.compute_v1.types.compute import ListTargetGrpcProxiesRequest
from google.cloud.compute_v1.types.compute import ListTargetHttpProxiesRequest
from google.cloud.compute_v1.types.compute import ListTargetHttpsProxiesRequest
from google.cloud.compute_v1.types.compute import ListTargetInstancesRequest
from google.cloud.compute_v1.types.compute import ListTargetPoolsRequest
from google.cloud.compute_v1.types.compute import ListTargetSslProxiesRequest
from google.cloud.compute_v1.types.compute import ListTargetTcpProxiesRequest
from google.cloud.compute_v1.types.compute import ListTargetVpnGatewaysRequest
from google.cloud.compute_v1.types.compute import ListUrlMapsRequest
from google.cloud.compute_v1.types.compute import ListUsableBackendServicesRequest
from google.cloud.compute_v1.types.compute import ListUsableRegionBackendServicesRequest
from google.cloud.compute_v1.types.compute import ListUsableSubnetworksRequest
from google.cloud.compute_v1.types.compute import ListVpnGatewaysRequest
from google.cloud.compute_v1.types.compute import ListVpnTunnelsRequest
from google.cloud.compute_v1.types.compute import ListXpnHostsProjectsRequest
from google.cloud.compute_v1.types.compute import ListZoneOperationsRequest
from google.cloud.compute_v1.types.compute import ListZonesRequest
from google.cloud.compute_v1.types.compute import LocalDisk
from google.cloud.compute_v1.types.compute import LocalizedMessage
from google.cloud.compute_v1.types.compute import LocationPolicy
from google.cloud.compute_v1.types.compute import LocationPolicyLocation
from google.cloud.compute_v1.types.compute import LocationPolicyLocationConstraints
from google.cloud.compute_v1.types.compute import LogConfig
from google.cloud.compute_v1.types.compute import LogConfigCloudAuditOptions
from google.cloud.compute_v1.types.compute import LogConfigCounterOptions
from google.cloud.compute_v1.types.compute import LogConfigCounterOptionsCustomField
from google.cloud.compute_v1.types.compute import LogConfigDataAccessOptions
from google.cloud.compute_v1.types.compute import MachineImage
from google.cloud.compute_v1.types.compute import MachineImageList
from google.cloud.compute_v1.types.compute import MachineType
from google.cloud.compute_v1.types.compute import MachineTypeAggregatedList
from google.cloud.compute_v1.types.compute import MachineTypeList
from google.cloud.compute_v1.types.compute import MachineTypesScopedList
from google.cloud.compute_v1.types.compute import ManagedInstance
from google.cloud.compute_v1.types.compute import ManagedInstanceInstanceHealth
from google.cloud.compute_v1.types.compute import ManagedInstanceLastAttempt
from google.cloud.compute_v1.types.compute import ManagedInstanceVersion
from google.cloud.compute_v1.types.compute import Metadata
from google.cloud.compute_v1.types.compute import MetadataFilter
from google.cloud.compute_v1.types.compute import MetadataFilterLabelMatch
from google.cloud.compute_v1.types.compute import MoveAddressRequest
from google.cloud.compute_v1.types.compute import MoveDiskProjectRequest
from google.cloud.compute_v1.types.compute import MoveFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import MoveGlobalAddressRequest
from google.cloud.compute_v1.types.compute import MoveInstanceProjectRequest
from google.cloud.compute_v1.types.compute import NamedPort
from google.cloud.compute_v1.types.compute import NatIpInfo
from google.cloud.compute_v1.types.compute import NatIpInfoNatIpInfoMapping
from google.cloud.compute_v1.types.compute import NatIpInfoResponse
from google.cloud.compute_v1.types.compute import Network
from google.cloud.compute_v1.types.compute import NetworkAttachment
from google.cloud.compute_v1.types.compute import NetworkAttachmentAggregatedList
from google.cloud.compute_v1.types.compute import NetworkAttachmentConnectedEndpoint
from google.cloud.compute_v1.types.compute import NetworkAttachmentList
from google.cloud.compute_v1.types.compute import NetworkAttachmentsScopedList
from google.cloud.compute_v1.types.compute import NetworkEdgeSecurityService
from google.cloud.compute_v1.types.compute import NetworkEdgeSecurityServiceAggregatedList
from google.cloud.compute_v1.types.compute import NetworkEdgeSecurityServicesScopedList
from google.cloud.compute_v1.types.compute import NetworkEndpoint
from google.cloud.compute_v1.types.compute import NetworkEndpointGroup
from google.cloud.compute_v1.types.compute import NetworkEndpointGroupAggregatedList
from google.cloud.compute_v1.types.compute import NetworkEndpointGroupAppEngine
from google.cloud.compute_v1.types.compute import NetworkEndpointGroupCloudFunction
from google.cloud.compute_v1.types.compute import NetworkEndpointGroupCloudRun
from google.cloud.compute_v1.types.compute import NetworkEndpointGroupList
from google.cloud.compute_v1.types.compute import NetworkEndpointGroupPscData
from google.cloud.compute_v1.types.compute import NetworkEndpointGroupsAttachEndpointsRequest
from google.cloud.compute_v1.types.compute import NetworkEndpointGroupsDetachEndpointsRequest
from google.cloud.compute_v1.types.compute import NetworkEndpointGroupsListEndpointsRequest
from google.cloud.compute_v1.types.compute import NetworkEndpointGroupsListNetworkEndpoints
from google.cloud.compute_v1.types.compute import NetworkEndpointGroupsScopedList
from google.cloud.compute_v1.types.compute import NetworkEndpointWithHealthStatus
from google.cloud.compute_v1.types.compute import NetworkInterface
from google.cloud.compute_v1.types.compute import NetworkList
from google.cloud.compute_v1.types.compute import NetworkPeering
from google.cloud.compute_v1.types.compute import NetworkPerformanceConfig
from google.cloud.compute_v1.types.compute import NetworkRoutingConfig
from google.cloud.compute_v1.types.compute import NetworksAddPeeringRequest
from google.cloud.compute_v1.types.compute import NetworksGetEffectiveFirewallsResponse
from google.cloud.compute_v1.types.compute import NetworksGetEffectiveFirewallsResponseEffectiveFirewallPolicy
from google.cloud.compute_v1.types.compute import NetworksRemovePeeringRequest
from google.cloud.compute_v1.types.compute import NetworksUpdatePeeringRequest
from google.cloud.compute_v1.types.compute import NodeGroup
from google.cloud.compute_v1.types.compute import NodeGroupAggregatedList
from google.cloud.compute_v1.types.compute import NodeGroupAutoscalingPolicy
from google.cloud.compute_v1.types.compute import NodeGroupList
from google.cloud.compute_v1.types.compute import NodeGroupMaintenanceWindow
from google.cloud.compute_v1.types.compute import NodeGroupNode
from google.cloud.compute_v1.types.compute import NodeGroupsAddNodesRequest
from google.cloud.compute_v1.types.compute import NodeGroupsDeleteNodesRequest
from google.cloud.compute_v1.types.compute import NodeGroupsListNodes
from google.cloud.compute_v1.types.compute import NodeGroupsPerformMaintenanceRequest
from google.cloud.compute_v1.types.compute import NodeGroupsScopedList
from google.cloud.compute_v1.types.compute import NodeGroupsSetNodeTemplateRequest
from google.cloud.compute_v1.types.compute import NodeGroupsSimulateMaintenanceEventRequest
from google.cloud.compute_v1.types.compute import NodeTemplate
from google.cloud.compute_v1.types.compute import NodeTemplateAggregatedList
from google.cloud.compute_v1.types.compute import NodeTemplateList
from google.cloud.compute_v1.types.compute import NodeTemplateNodeTypeFlexibility
from google.cloud.compute_v1.types.compute import NodeTemplatesScopedList
from google.cloud.compute_v1.types.compute import NodeType
from google.cloud.compute_v1.types.compute import NodeTypeAggregatedList
from google.cloud.compute_v1.types.compute import NodeTypeList
from google.cloud.compute_v1.types.compute import NodeTypesScopedList
from google.cloud.compute_v1.types.compute import NotificationEndpoint
from google.cloud.compute_v1.types.compute import NotificationEndpointGrpcSettings
from google.cloud.compute_v1.types.compute import NotificationEndpointList
from google.cloud.compute_v1.types.compute import Operation
from google.cloud.compute_v1.types.compute import OperationAggregatedList
from google.cloud.compute_v1.types.compute import OperationList
from google.cloud.compute_v1.types.compute import OperationsScopedList
from google.cloud.compute_v1.types.compute import OutlierDetection
from google.cloud.compute_v1.types.compute import PacketIntervals
from google.cloud.compute_v1.types.compute import PacketMirroring
from google.cloud.compute_v1.types.compute import PacketMirroringAggregatedList
from google.cloud.compute_v1.types.compute import PacketMirroringFilter
from google.cloud.compute_v1.types.compute import PacketMirroringForwardingRuleInfo
from google.cloud.compute_v1.types.compute import PacketMirroringList
from google.cloud.compute_v1.types.compute import PacketMirroringMirroredResourceInfo
from google.cloud.compute_v1.types.compute import PacketMirroringMirroredResourceInfoInstanceInfo
from google.cloud.compute_v1.types.compute import PacketMirroringMirroredResourceInfoSubnetInfo
from google.cloud.compute_v1.types.compute import PacketMirroringNetworkInfo
from google.cloud.compute_v1.types.compute import PacketMirroringsScopedList
from google.cloud.compute_v1.types.compute import PatchAutoscalerRequest
from google.cloud.compute_v1.types.compute import PatchBackendBucketRequest
from google.cloud.compute_v1.types.compute import PatchBackendServiceRequest
from google.cloud.compute_v1.types.compute import PatchFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import PatchFirewallRequest
from google.cloud.compute_v1.types.compute import PatchForwardingRuleRequest
from google.cloud.compute_v1.types.compute import PatchGlobalForwardingRuleRequest
from google.cloud.compute_v1.types.compute import PatchGlobalPublicDelegatedPrefixeRequest
from google.cloud.compute_v1.types.compute import PatchHealthCheckRequest
from google.cloud.compute_v1.types.compute import PatchImageRequest
from google.cloud.compute_v1.types.compute import PatchInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import PatchInstanceSettingRequest
from google.cloud.compute_v1.types.compute import PatchInterconnectAttachmentRequest
from google.cloud.compute_v1.types.compute import PatchInterconnectRequest
from google.cloud.compute_v1.types.compute import PatchNetworkAttachmentRequest
from google.cloud.compute_v1.types.compute import PatchNetworkEdgeSecurityServiceRequest
from google.cloud.compute_v1.types.compute import PatchNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import PatchNetworkRequest
from google.cloud.compute_v1.types.compute import PatchNodeGroupRequest
from google.cloud.compute_v1.types.compute import PatchPacketMirroringRequest
from google.cloud.compute_v1.types.compute import PatchPerInstanceConfigsInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import PatchPerInstanceConfigsRegionInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import PatchPublicAdvertisedPrefixeRequest
from google.cloud.compute_v1.types.compute import PatchPublicDelegatedPrefixeRequest
from google.cloud.compute_v1.types.compute import PatchRegionAutoscalerRequest
from google.cloud.compute_v1.types.compute import PatchRegionBackendServiceRequest
from google.cloud.compute_v1.types.compute import PatchRegionHealthCheckRequest
from google.cloud.compute_v1.types.compute import PatchRegionHealthCheckServiceRequest
from google.cloud.compute_v1.types.compute import PatchRegionInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import PatchRegionNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import PatchRegionSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import PatchRegionSslPolicyRequest
from google.cloud.compute_v1.types.compute import PatchRegionTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import PatchRegionUrlMapRequest
from google.cloud.compute_v1.types.compute import PatchResourcePolicyRequest
from google.cloud.compute_v1.types.compute import PatchRouterRequest
from google.cloud.compute_v1.types.compute import PatchRuleFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import PatchRuleNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import PatchRuleRegionNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import PatchRuleRegionSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import PatchRuleSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import PatchSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import PatchServiceAttachmentRequest
from google.cloud.compute_v1.types.compute import PatchSnapshotSettingRequest
from google.cloud.compute_v1.types.compute import PatchSslPolicyRequest
from google.cloud.compute_v1.types.compute import PatchSubnetworkRequest
from google.cloud.compute_v1.types.compute import PatchTargetGrpcProxyRequest
from google.cloud.compute_v1.types.compute import PatchTargetHttpProxyRequest
from google.cloud.compute_v1.types.compute import PatchTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import PatchUrlMapRequest
from google.cloud.compute_v1.types.compute import PathMatcher
from google.cloud.compute_v1.types.compute import PathRule
from google.cloud.compute_v1.types.compute import PerformMaintenanceInstanceRequest
from google.cloud.compute_v1.types.compute import PerformMaintenanceNodeGroupRequest
from google.cloud.compute_v1.types.compute import PerInstanceConfig
from google.cloud.compute_v1.types.compute import Policy
from google.cloud.compute_v1.types.compute import PreconfiguredWafSet
from google.cloud.compute_v1.types.compute import PreservedState
from google.cloud.compute_v1.types.compute import PreservedStatePreservedDisk
from google.cloud.compute_v1.types.compute import PreservedStatePreservedNetworkIp
from google.cloud.compute_v1.types.compute import PreservedStatePreservedNetworkIpIpAddress
from google.cloud.compute_v1.types.compute import PreviewRouterRequest
from google.cloud.compute_v1.types.compute import Project
from google.cloud.compute_v1.types.compute import ProjectsDisableXpnResourceRequest
from google.cloud.compute_v1.types.compute import ProjectsEnableXpnResourceRequest
from google.cloud.compute_v1.types.compute import ProjectsGetXpnResources
from google.cloud.compute_v1.types.compute import ProjectsListXpnHostsRequest
from google.cloud.compute_v1.types.compute import ProjectsSetCloudArmorTierRequest
from google.cloud.compute_v1.types.compute import ProjectsSetDefaultNetworkTierRequest
from google.cloud.compute_v1.types.compute import PublicAdvertisedPrefix
from google.cloud.compute_v1.types.compute import PublicAdvertisedPrefixList
from google.cloud.compute_v1.types.compute import PublicAdvertisedPrefixPublicDelegatedPrefix
from google.cloud.compute_v1.types.compute import PublicDelegatedPrefix
from google.cloud.compute_v1.types.compute import PublicDelegatedPrefixAggregatedList
from google.cloud.compute_v1.types.compute import PublicDelegatedPrefixesScopedList
from google.cloud.compute_v1.types.compute import PublicDelegatedPrefixList
from google.cloud.compute_v1.types.compute import PublicDelegatedPrefixPublicDelegatedSubPrefix
from google.cloud.compute_v1.types.compute import Quota
from google.cloud.compute_v1.types.compute import QuotaExceededInfo
from google.cloud.compute_v1.types.compute import QuotaStatusWarning
from google.cloud.compute_v1.types.compute import RawDisk
from google.cloud.compute_v1.types.compute import RecreateInstancesInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import RecreateInstancesRegionInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import Reference
from google.cloud.compute_v1.types.compute import Region
from google.cloud.compute_v1.types.compute import RegionAddressesMoveRequest
from google.cloud.compute_v1.types.compute import RegionAutoscalerList
from google.cloud.compute_v1.types.compute import RegionDisksAddResourcePoliciesRequest
from google.cloud.compute_v1.types.compute import RegionDisksRemoveResourcePoliciesRequest
from google.cloud.compute_v1.types.compute import RegionDisksResizeRequest
from google.cloud.compute_v1.types.compute import RegionDisksStartAsyncReplicationRequest
from google.cloud.compute_v1.types.compute import RegionDiskTypeList
from google.cloud.compute_v1.types.compute import RegionInstanceGroupList
from google.cloud.compute_v1.types.compute import RegionInstanceGroupManagerDeleteInstanceConfigReq
from google.cloud.compute_v1.types.compute import RegionInstanceGroupManagerList
from google.cloud.compute_v1.types.compute import RegionInstanceGroupManagerPatchInstanceConfigReq
from google.cloud.compute_v1.types.compute import RegionInstanceGroupManagersAbandonInstancesRequest
from google.cloud.compute_v1.types.compute import RegionInstanceGroupManagersApplyUpdatesRequest
from google.cloud.compute_v1.types.compute import RegionInstanceGroupManagersCreateInstancesRequest
from google.cloud.compute_v1.types.compute import RegionInstanceGroupManagersDeleteInstancesRequest
from google.cloud.compute_v1.types.compute import RegionInstanceGroupManagersListErrorsResponse
from google.cloud.compute_v1.types.compute import RegionInstanceGroupManagersListInstanceConfigsResp
from google.cloud.compute_v1.types.compute import RegionInstanceGroupManagersListInstancesResponse
from google.cloud.compute_v1.types.compute import RegionInstanceGroupManagersRecreateRequest
from google.cloud.compute_v1.types.compute import RegionInstanceGroupManagersSetTargetPoolsRequest
from google.cloud.compute_v1.types.compute import RegionInstanceGroupManagersSetTemplateRequest
from google.cloud.compute_v1.types.compute import RegionInstanceGroupManagerUpdateInstanceConfigReq
from google.cloud.compute_v1.types.compute import RegionInstanceGroupsListInstances
from google.cloud.compute_v1.types.compute import RegionInstanceGroupsListInstancesRequest
from google.cloud.compute_v1.types.compute import RegionInstanceGroupsSetNamedPortsRequest
from google.cloud.compute_v1.types.compute import RegionList
from google.cloud.compute_v1.types.compute import RegionNetworkEndpointGroupsAttachEndpointsRequest
from google.cloud.compute_v1.types.compute import RegionNetworkEndpointGroupsDetachEndpointsRequest
from google.cloud.compute_v1.types.compute import RegionNetworkFirewallPoliciesGetEffectiveFirewallsResponse
from google.cloud.compute_v1.types.compute import RegionNetworkFirewallPoliciesGetEffectiveFirewallsResponseEffectiveFirewallPolicy
from google.cloud.compute_v1.types.compute import RegionSetLabelsRequest
from google.cloud.compute_v1.types.compute import RegionSetPolicyRequest
from google.cloud.compute_v1.types.compute import RegionTargetHttpsProxiesSetSslCertificatesRequest
from google.cloud.compute_v1.types.compute import RegionUrlMapsValidateRequest
from google.cloud.compute_v1.types.compute import RemoveAssociationFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import RemoveAssociationNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import RemoveAssociationRegionNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import RemoveHealthCheckTargetPoolRequest
from google.cloud.compute_v1.types.compute import RemoveInstancesInstanceGroupRequest
from google.cloud.compute_v1.types.compute import RemoveInstanceTargetPoolRequest
from google.cloud.compute_v1.types.compute import RemovePeeringNetworkRequest
from google.cloud.compute_v1.types.compute import RemoveResourcePoliciesDiskRequest
from google.cloud.compute_v1.types.compute import RemoveResourcePoliciesInstanceRequest
from google.cloud.compute_v1.types.compute import RemoveResourcePoliciesRegionDiskRequest
from google.cloud.compute_v1.types.compute import RemoveRuleFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import RemoveRuleNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import RemoveRuleRegionNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import RemoveRuleRegionSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import RemoveRuleSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import RequestMirrorPolicy
from google.cloud.compute_v1.types.compute import Reservation
from google.cloud.compute_v1.types.compute import ReservationAffinity
from google.cloud.compute_v1.types.compute import ReservationAggregatedList
from google.cloud.compute_v1.types.compute import ReservationList
from google.cloud.compute_v1.types.compute import ReservationsResizeRequest
from google.cloud.compute_v1.types.compute import ReservationsScopedList
from google.cloud.compute_v1.types.compute import ResetInstanceRequest
from google.cloud.compute_v1.types.compute import ResizeDiskRequest
from google.cloud.compute_v1.types.compute import ResizeInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import ResizeRegionDiskRequest
from google.cloud.compute_v1.types.compute import ResizeRegionInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import ResizeReservationRequest
from google.cloud.compute_v1.types.compute import ResourceCommitment
from google.cloud.compute_v1.types.compute import ResourceGroupReference
from google.cloud.compute_v1.types.compute import ResourcePoliciesScopedList
from google.cloud.compute_v1.types.compute import ResourcePolicy
from google.cloud.compute_v1.types.compute import ResourcePolicyAggregatedList
from google.cloud.compute_v1.types.compute import ResourcePolicyDailyCycle
from google.cloud.compute_v1.types.compute import ResourcePolicyDiskConsistencyGroupPolicy
from google.cloud.compute_v1.types.compute import ResourcePolicyGroupPlacementPolicy
from google.cloud.compute_v1.types.compute import ResourcePolicyHourlyCycle
from google.cloud.compute_v1.types.compute import ResourcePolicyInstanceSchedulePolicy
from google.cloud.compute_v1.types.compute import ResourcePolicyInstanceSchedulePolicySchedule
from google.cloud.compute_v1.types.compute import ResourcePolicyList
from google.cloud.compute_v1.types.compute import ResourcePolicyResourceStatus
from google.cloud.compute_v1.types.compute import ResourcePolicyResourceStatusInstanceSchedulePolicyStatus
from google.cloud.compute_v1.types.compute import ResourcePolicySnapshotSchedulePolicy
from google.cloud.compute_v1.types.compute import ResourcePolicySnapshotSchedulePolicyRetentionPolicy
from google.cloud.compute_v1.types.compute import ResourcePolicySnapshotSchedulePolicySchedule
from google.cloud.compute_v1.types.compute import ResourcePolicySnapshotSchedulePolicySnapshotProperties
from google.cloud.compute_v1.types.compute import ResourcePolicyWeeklyCycle
from google.cloud.compute_v1.types.compute import ResourcePolicyWeeklyCycleDayOfWeek
from google.cloud.compute_v1.types.compute import ResourceStatus
from google.cloud.compute_v1.types.compute import ResumeInstanceRequest
from google.cloud.compute_v1.types.compute import Route
from google.cloud.compute_v1.types.compute import RouteAsPath
from google.cloud.compute_v1.types.compute import RouteList
from google.cloud.compute_v1.types.compute import Router
from google.cloud.compute_v1.types.compute import RouterAdvertisedIpRange
from google.cloud.compute_v1.types.compute import RouterAggregatedList
from google.cloud.compute_v1.types.compute import RouterBgp
from google.cloud.compute_v1.types.compute import RouterBgpPeer
from google.cloud.compute_v1.types.compute import RouterBgpPeerBfd
from google.cloud.compute_v1.types.compute import RouterBgpPeerCustomLearnedIpRange
from google.cloud.compute_v1.types.compute import RouterInterface
from google.cloud.compute_v1.types.compute import RouterList
from google.cloud.compute_v1.types.compute import RouterMd5AuthenticationKey
from google.cloud.compute_v1.types.compute import RouterNat
from google.cloud.compute_v1.types.compute import RouterNatLogConfig
from google.cloud.compute_v1.types.compute import RouterNatRule
from google.cloud.compute_v1.types.compute import RouterNatRuleAction
from google.cloud.compute_v1.types.compute import RouterNatSubnetworkToNat
from google.cloud.compute_v1.types.compute import RoutersPreviewResponse
from google.cloud.compute_v1.types.compute import RoutersScopedList
from google.cloud.compute_v1.types.compute import RouterStatus
from google.cloud.compute_v1.types.compute import RouterStatusBgpPeerStatus
from google.cloud.compute_v1.types.compute import RouterStatusNatStatus
from google.cloud.compute_v1.types.compute import RouterStatusNatStatusNatRuleStatus
from google.cloud.compute_v1.types.compute import RouterStatusResponse
from google.cloud.compute_v1.types.compute import Rule
from google.cloud.compute_v1.types.compute import SavedAttachedDisk
from google.cloud.compute_v1.types.compute import SavedDisk
from google.cloud.compute_v1.types.compute import ScalingScheduleStatus
from google.cloud.compute_v1.types.compute import Scheduling
from google.cloud.compute_v1.types.compute import SchedulingNodeAffinity
from google.cloud.compute_v1.types.compute import ScratchDisks
from google.cloud.compute_v1.types.compute import Screenshot
from google.cloud.compute_v1.types.compute import SecurityPoliciesAggregatedList
from google.cloud.compute_v1.types.compute import SecurityPoliciesListPreconfiguredExpressionSetsResponse
from google.cloud.compute_v1.types.compute import SecurityPoliciesScopedList
from google.cloud.compute_v1.types.compute import SecurityPoliciesWafConfig
from google.cloud.compute_v1.types.compute import SecurityPolicy
from google.cloud.compute_v1.types.compute import SecurityPolicyAdaptiveProtectionConfig
from google.cloud.compute_v1.types.compute import SecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig
from google.cloud.compute_v1.types.compute import SecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfig
from google.cloud.compute_v1.types.compute import SecurityPolicyAdvancedOptionsConfig
from google.cloud.compute_v1.types.compute import SecurityPolicyAdvancedOptionsConfigJsonCustomConfig
from google.cloud.compute_v1.types.compute import SecurityPolicyDdosProtectionConfig
from google.cloud.compute_v1.types.compute import SecurityPolicyList
from google.cloud.compute_v1.types.compute import SecurityPolicyRecaptchaOptionsConfig
from google.cloud.compute_v1.types.compute import SecurityPolicyReference
from google.cloud.compute_v1.types.compute import SecurityPolicyRule
from google.cloud.compute_v1.types.compute import SecurityPolicyRuleHttpHeaderAction
from google.cloud.compute_v1.types.compute import SecurityPolicyRuleHttpHeaderActionHttpHeaderOption
from google.cloud.compute_v1.types.compute import SecurityPolicyRuleMatcher
from google.cloud.compute_v1.types.compute import SecurityPolicyRuleMatcherConfig
from google.cloud.compute_v1.types.compute import SecurityPolicyRuleMatcherExprOptions
from google.cloud.compute_v1.types.compute import SecurityPolicyRuleMatcherExprOptionsRecaptchaOptions
from google.cloud.compute_v1.types.compute import SecurityPolicyRuleNetworkMatcher
from google.cloud.compute_v1.types.compute import SecurityPolicyRuleNetworkMatcherUserDefinedFieldMatch
from google.cloud.compute_v1.types.compute import SecurityPolicyRulePreconfiguredWafConfig
from google.cloud.compute_v1.types.compute import SecurityPolicyRulePreconfiguredWafConfigExclusion
from google.cloud.compute_v1.types.compute import SecurityPolicyRulePreconfiguredWafConfigExclusionFieldParams
from google.cloud.compute_v1.types.compute import SecurityPolicyRuleRateLimitOptions
from google.cloud.compute_v1.types.compute import SecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfig
from google.cloud.compute_v1.types.compute import SecurityPolicyRuleRateLimitOptionsThreshold
from google.cloud.compute_v1.types.compute import SecurityPolicyRuleRedirectOptions
from google.cloud.compute_v1.types.compute import SecurityPolicyUserDefinedField
from google.cloud.compute_v1.types.compute import SecuritySettings
from google.cloud.compute_v1.types.compute import SendDiagnosticInterruptInstanceRequest
from google.cloud.compute_v1.types.compute import SendDiagnosticInterruptInstanceResponse
from google.cloud.compute_v1.types.compute import SerialPortOutput
from google.cloud.compute_v1.types.compute import ServerBinding
from google.cloud.compute_v1.types.compute import ServiceAccount
from google.cloud.compute_v1.types.compute import ServiceAttachment
from google.cloud.compute_v1.types.compute import ServiceAttachmentAggregatedList
from google.cloud.compute_v1.types.compute import ServiceAttachmentConnectedEndpoint
from google.cloud.compute_v1.types.compute import ServiceAttachmentConsumerProjectLimit
from google.cloud.compute_v1.types.compute import ServiceAttachmentList
from google.cloud.compute_v1.types.compute import ServiceAttachmentsScopedList
from google.cloud.compute_v1.types.compute import SetBackendServiceTargetSslProxyRequest
from google.cloud.compute_v1.types.compute import SetBackendServiceTargetTcpProxyRequest
from google.cloud.compute_v1.types.compute import SetBackupTargetPoolRequest
from google.cloud.compute_v1.types.compute import SetCertificateMapTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import SetCertificateMapTargetSslProxyRequest
from google.cloud.compute_v1.types.compute import SetCloudArmorTierProjectRequest
from google.cloud.compute_v1.types.compute import SetCommonInstanceMetadataOperationMetadata
from google.cloud.compute_v1.types.compute import SetCommonInstanceMetadataOperationMetadataPerLocationOperationInfo
from google.cloud.compute_v1.types.compute import SetCommonInstanceMetadataProjectRequest
from google.cloud.compute_v1.types.compute import SetDefaultNetworkTierProjectRequest
from google.cloud.compute_v1.types.compute import SetDeletionProtectionInstanceRequest
from google.cloud.compute_v1.types.compute import SetDiskAutoDeleteInstanceRequest
from google.cloud.compute_v1.types.compute import SetEdgeSecurityPolicyBackendBucketRequest
from google.cloud.compute_v1.types.compute import SetEdgeSecurityPolicyBackendServiceRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyBackendBucketRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyBackendServiceRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyDiskRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyImageRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyInstanceRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyInstanceTemplateRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyInstantSnapshotRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyLicenseRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyMachineImageRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyNetworkAttachmentRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyNodeGroupRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyNodeTemplateRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyRegionBackendServiceRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyRegionDiskRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyRegionInstantSnapshotRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyRegionNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyReservationRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyResourcePolicyRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyServiceAttachmentRequest
from google.cloud.compute_v1.types.compute import SetIamPolicySnapshotRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyStoragePoolRequest
from google.cloud.compute_v1.types.compute import SetIamPolicySubnetworkRequest
from google.cloud.compute_v1.types.compute import SetInstanceTemplateInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import SetInstanceTemplateRegionInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import SetLabelsAddressRequest
from google.cloud.compute_v1.types.compute import SetLabelsDiskRequest
from google.cloud.compute_v1.types.compute import SetLabelsExternalVpnGatewayRequest
from google.cloud.compute_v1.types.compute import SetLabelsForwardingRuleRequest
from google.cloud.compute_v1.types.compute import SetLabelsGlobalAddressRequest
from google.cloud.compute_v1.types.compute import SetLabelsGlobalForwardingRuleRequest
from google.cloud.compute_v1.types.compute import SetLabelsImageRequest
from google.cloud.compute_v1.types.compute import SetLabelsInstanceRequest
from google.cloud.compute_v1.types.compute import SetLabelsInstantSnapshotRequest
from google.cloud.compute_v1.types.compute import SetLabelsInterconnectAttachmentRequest
from google.cloud.compute_v1.types.compute import SetLabelsInterconnectRequest
from google.cloud.compute_v1.types.compute import SetLabelsRegionDiskRequest
from google.cloud.compute_v1.types.compute import SetLabelsRegionInstantSnapshotRequest
from google.cloud.compute_v1.types.compute import SetLabelsSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import SetLabelsSnapshotRequest
from google.cloud.compute_v1.types.compute import SetLabelsTargetVpnGatewayRequest
from google.cloud.compute_v1.types.compute import SetLabelsVpnGatewayRequest
from google.cloud.compute_v1.types.compute import SetLabelsVpnTunnelRequest
from google.cloud.compute_v1.types.compute import SetMachineResourcesInstanceRequest
from google.cloud.compute_v1.types.compute import SetMachineTypeInstanceRequest
from google.cloud.compute_v1.types.compute import SetMetadataInstanceRequest
from google.cloud.compute_v1.types.compute import SetMinCpuPlatformInstanceRequest
from google.cloud.compute_v1.types.compute import SetNamedPortsInstanceGroupRequest
from google.cloud.compute_v1.types.compute import SetNamedPortsRegionInstanceGroupRequest
from google.cloud.compute_v1.types.compute import SetNameInstanceRequest
from google.cloud.compute_v1.types.compute import SetNodeTemplateNodeGroupRequest
from google.cloud.compute_v1.types.compute import SetPrivateIpGoogleAccessSubnetworkRequest
from google.cloud.compute_v1.types.compute import SetProxyHeaderTargetSslProxyRequest
from google.cloud.compute_v1.types.compute import SetProxyHeaderTargetTcpProxyRequest
from google.cloud.compute_v1.types.compute import SetQuicOverrideTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import SetSchedulingInstanceRequest
from google.cloud.compute_v1.types.compute import SetSecurityPolicyBackendServiceRequest
from google.cloud.compute_v1.types.compute import SetSecurityPolicyInstanceRequest
from google.cloud.compute_v1.types.compute import SetSecurityPolicyRegionBackendServiceRequest
from google.cloud.compute_v1.types.compute import SetSecurityPolicyTargetInstanceRequest
from google.cloud.compute_v1.types.compute import SetSecurityPolicyTargetPoolRequest
from google.cloud.compute_v1.types.compute import SetServiceAccountInstanceRequest
from google.cloud.compute_v1.types.compute import SetShieldedInstanceIntegrityPolicyInstanceRequest
from google.cloud.compute_v1.types.compute import SetSslCertificatesRegionTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import SetSslCertificatesTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import SetSslCertificatesTargetSslProxyRequest
from google.cloud.compute_v1.types.compute import SetSslPolicyTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import SetSslPolicyTargetSslProxyRequest
from google.cloud.compute_v1.types.compute import SetTagsInstanceRequest
from google.cloud.compute_v1.types.compute import SetTargetForwardingRuleRequest
from google.cloud.compute_v1.types.compute import SetTargetGlobalForwardingRuleRequest
from google.cloud.compute_v1.types.compute import SetTargetPoolsInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import SetTargetPoolsRegionInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import SetUrlMapRegionTargetHttpProxyRequest
from google.cloud.compute_v1.types.compute import SetUrlMapRegionTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import SetUrlMapTargetHttpProxyRequest
from google.cloud.compute_v1.types.compute import SetUrlMapTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import SetUsageExportBucketProjectRequest
from google.cloud.compute_v1.types.compute import ShareSettings
from google.cloud.compute_v1.types.compute import ShareSettingsProjectConfig
from google.cloud.compute_v1.types.compute import ShieldedInstanceConfig
from google.cloud.compute_v1.types.compute import ShieldedInstanceIdentity
from google.cloud.compute_v1.types.compute import ShieldedInstanceIdentityEntry
from google.cloud.compute_v1.types.compute import ShieldedInstanceIntegrityPolicy
from google.cloud.compute_v1.types.compute import SignedUrlKey
from google.cloud.compute_v1.types.compute import SimulateMaintenanceEventInstanceRequest
from google.cloud.compute_v1.types.compute import SimulateMaintenanceEventNodeGroupRequest
from google.cloud.compute_v1.types.compute import Snapshot
from google.cloud.compute_v1.types.compute import SnapshotList
from google.cloud.compute_v1.types.compute import SnapshotSettings
from google.cloud.compute_v1.types.compute import SnapshotSettingsStorageLocationSettings
from google.cloud.compute_v1.types.compute import SnapshotSettingsStorageLocationSettingsStorageLocationPreference
from google.cloud.compute_v1.types.compute import SourceDiskEncryptionKey
from google.cloud.compute_v1.types.compute import SourceInstanceParams
from google.cloud.compute_v1.types.compute import SourceInstanceProperties
from google.cloud.compute_v1.types.compute import SslCertificate
from google.cloud.compute_v1.types.compute import SslCertificateAggregatedList
from google.cloud.compute_v1.types.compute import SslCertificateList
from google.cloud.compute_v1.types.compute import SslCertificateManagedSslCertificate
from google.cloud.compute_v1.types.compute import SslCertificateSelfManagedSslCertificate
from google.cloud.compute_v1.types.compute import SslCertificatesScopedList
from google.cloud.compute_v1.types.compute import SSLHealthCheck
from google.cloud.compute_v1.types.compute import SslPoliciesAggregatedList
from google.cloud.compute_v1.types.compute import SslPoliciesList
from google.cloud.compute_v1.types.compute import SslPoliciesListAvailableFeaturesResponse
from google.cloud.compute_v1.types.compute import SslPoliciesScopedList
from google.cloud.compute_v1.types.compute import SslPolicy
from google.cloud.compute_v1.types.compute import SslPolicyReference
from google.cloud.compute_v1.types.compute import StartAsyncReplicationDiskRequest
from google.cloud.compute_v1.types.compute import StartAsyncReplicationRegionDiskRequest
from google.cloud.compute_v1.types.compute import StartInstanceRequest
from google.cloud.compute_v1.types.compute import StartWithEncryptionKeyInstanceRequest
from google.cloud.compute_v1.types.compute import StatefulPolicy
from google.cloud.compute_v1.types.compute import StatefulPolicyPreservedState
from google.cloud.compute_v1.types.compute import StatefulPolicyPreservedStateDiskDevice
from google.cloud.compute_v1.types.compute import StatefulPolicyPreservedStateNetworkIp
from google.cloud.compute_v1.types.compute import Status
from google.cloud.compute_v1.types.compute import StopAsyncReplicationDiskRequest
from google.cloud.compute_v1.types.compute import StopAsyncReplicationRegionDiskRequest
from google.cloud.compute_v1.types.compute import StopGroupAsyncReplicationDiskRequest
from google.cloud.compute_v1.types.compute import StopGroupAsyncReplicationRegionDiskRequest
from google.cloud.compute_v1.types.compute import StopInstanceRequest
from google.cloud.compute_v1.types.compute import StoragePool
from google.cloud.compute_v1.types.compute import StoragePoolAggregatedList
from google.cloud.compute_v1.types.compute import StoragePoolDisk
from google.cloud.compute_v1.types.compute import StoragePoolList
from google.cloud.compute_v1.types.compute import StoragePoolListDisks
from google.cloud.compute_v1.types.compute import StoragePoolResourceStatus
from google.cloud.compute_v1.types.compute import StoragePoolsScopedList
from google.cloud.compute_v1.types.compute import StoragePoolType
from google.cloud.compute_v1.types.compute import StoragePoolTypeAggregatedList
from google.cloud.compute_v1.types.compute import StoragePoolTypeList
from google.cloud.compute_v1.types.compute import StoragePoolTypesScopedList
from google.cloud.compute_v1.types.compute import Subnetwork
from google.cloud.compute_v1.types.compute import SubnetworkAggregatedList
from google.cloud.compute_v1.types.compute import SubnetworkList
from google.cloud.compute_v1.types.compute import SubnetworkLogConfig
from google.cloud.compute_v1.types.compute import SubnetworkSecondaryRange
from google.cloud.compute_v1.types.compute import SubnetworksExpandIpCidrRangeRequest
from google.cloud.compute_v1.types.compute import SubnetworksScopedList
from google.cloud.compute_v1.types.compute import SubnetworksSetPrivateIpGoogleAccessRequest
from google.cloud.compute_v1.types.compute import Subsetting
from google.cloud.compute_v1.types.compute import SuspendInstanceRequest
from google.cloud.compute_v1.types.compute import SwitchToCustomModeNetworkRequest
from google.cloud.compute_v1.types.compute import Tags
from google.cloud.compute_v1.types.compute import TargetGrpcProxy
from google.cloud.compute_v1.types.compute import TargetGrpcProxyList
from google.cloud.compute_v1.types.compute import TargetHttpProxiesScopedList
from google.cloud.compute_v1.types.compute import TargetHttpProxy
from google.cloud.compute_v1.types.compute import TargetHttpProxyAggregatedList
from google.cloud.compute_v1.types.compute import TargetHttpProxyList
from google.cloud.compute_v1.types.compute import TargetHttpsProxiesScopedList
from google.cloud.compute_v1.types.compute import TargetHttpsProxiesSetCertificateMapRequest
from google.cloud.compute_v1.types.compute import TargetHttpsProxiesSetQuicOverrideRequest
from google.cloud.compute_v1.types.compute import TargetHttpsProxiesSetSslCertificatesRequest
from google.cloud.compute_v1.types.compute import TargetHttpsProxy
from google.cloud.compute_v1.types.compute import TargetHttpsProxyAggregatedList
from google.cloud.compute_v1.types.compute import TargetHttpsProxyList
from google.cloud.compute_v1.types.compute import TargetInstance
from google.cloud.compute_v1.types.compute import TargetInstanceAggregatedList
from google.cloud.compute_v1.types.compute import TargetInstanceList
from google.cloud.compute_v1.types.compute import TargetInstancesScopedList
from google.cloud.compute_v1.types.compute import TargetPool
from google.cloud.compute_v1.types.compute import TargetPoolAggregatedList
from google.cloud.compute_v1.types.compute import TargetPoolInstanceHealth
from google.cloud.compute_v1.types.compute import TargetPoolList
from google.cloud.compute_v1.types.compute import TargetPoolsAddHealthCheckRequest
from google.cloud.compute_v1.types.compute import TargetPoolsAddInstanceRequest
from google.cloud.compute_v1.types.compute import TargetPoolsRemoveHealthCheckRequest
from google.cloud.compute_v1.types.compute import TargetPoolsRemoveInstanceRequest
from google.cloud.compute_v1.types.compute import TargetPoolsScopedList
from google.cloud.compute_v1.types.compute import TargetReference
from google.cloud.compute_v1.types.compute import TargetSslProxiesSetBackendServiceRequest
from google.cloud.compute_v1.types.compute import TargetSslProxiesSetCertificateMapRequest
from google.cloud.compute_v1.types.compute import TargetSslProxiesSetProxyHeaderRequest
from google.cloud.compute_v1.types.compute import TargetSslProxiesSetSslCertificatesRequest
from google.cloud.compute_v1.types.compute import TargetSslProxy
from google.cloud.compute_v1.types.compute import TargetSslProxyList
from google.cloud.compute_v1.types.compute import TargetTcpProxiesScopedList
from google.cloud.compute_v1.types.compute import TargetTcpProxiesSetBackendServiceRequest
from google.cloud.compute_v1.types.compute import TargetTcpProxiesSetProxyHeaderRequest
from google.cloud.compute_v1.types.compute import TargetTcpProxy
from google.cloud.compute_v1.types.compute import TargetTcpProxyAggregatedList
from google.cloud.compute_v1.types.compute import TargetTcpProxyList
from google.cloud.compute_v1.types.compute import TargetVpnGateway
from google.cloud.compute_v1.types.compute import TargetVpnGatewayAggregatedList
from google.cloud.compute_v1.types.compute import TargetVpnGatewayList
from google.cloud.compute_v1.types.compute import TargetVpnGatewaysScopedList
from google.cloud.compute_v1.types.compute import TCPHealthCheck
from google.cloud.compute_v1.types.compute import TestFailure
from google.cloud.compute_v1.types.compute import TestIamPermissionsBackendBucketRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsBackendServiceRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsDiskRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsExternalVpnGatewayRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsImageRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsInstanceRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsInstanceTemplateRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsInstantSnapshotRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsLicenseCodeRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsLicenseRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsMachineImageRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsNetworkAttachmentRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsNetworkEndpointGroupRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsNodeGroupRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsNodeTemplateRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsPacketMirroringRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsRegionBackendServiceRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsRegionDiskRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsRegionInstantSnapshotRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsRegionNetworkFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsReservationRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsResourcePolicyRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsServiceAttachmentRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsSnapshotRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsStoragePoolRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsSubnetworkRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsVpnGatewayRequest
from google.cloud.compute_v1.types.compute import TestPermissionsRequest
from google.cloud.compute_v1.types.compute import TestPermissionsResponse
from google.cloud.compute_v1.types.compute import Uint128
from google.cloud.compute_v1.types.compute import UpcomingMaintenance
from google.cloud.compute_v1.types.compute import UpdateAccessConfigInstanceRequest
from google.cloud.compute_v1.types.compute import UpdateAutoscalerRequest
from google.cloud.compute_v1.types.compute import UpdateBackendBucketRequest
from google.cloud.compute_v1.types.compute import UpdateBackendServiceRequest
from google.cloud.compute_v1.types.compute import UpdateDiskRequest
from google.cloud.compute_v1.types.compute import UpdateDisplayDeviceInstanceRequest
from google.cloud.compute_v1.types.compute import UpdateFirewallRequest
from google.cloud.compute_v1.types.compute import UpdateHealthCheckRequest
from google.cloud.compute_v1.types.compute import UpdateInstanceRequest
from google.cloud.compute_v1.types.compute import UpdateNetworkInterfaceInstanceRequest
from google.cloud.compute_v1.types.compute import UpdatePeeringNetworkRequest
from google.cloud.compute_v1.types.compute import UpdatePerInstanceConfigsInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import UpdateRegionAutoscalerRequest
from google.cloud.compute_v1.types.compute import UpdateRegionBackendServiceRequest
from google.cloud.compute_v1.types.compute import UpdateRegionCommitmentRequest
from google.cloud.compute_v1.types.compute import UpdateRegionDiskRequest
from google.cloud.compute_v1.types.compute import UpdateRegionHealthCheckRequest
from google.cloud.compute_v1.types.compute import UpdateRegionUrlMapRequest
from google.cloud.compute_v1.types.compute import UpdateReservationRequest
from google.cloud.compute_v1.types.compute import UpdateRouterRequest
from google.cloud.compute_v1.types.compute import UpdateShieldedInstanceConfigInstanceRequest
from google.cloud.compute_v1.types.compute import UpdateStoragePoolRequest
from google.cloud.compute_v1.types.compute import UpdateUrlMapRequest
from google.cloud.compute_v1.types.compute import UrlMap
from google.cloud.compute_v1.types.compute import UrlMapList
from google.cloud.compute_v1.types.compute import UrlMapReference
from google.cloud.compute_v1.types.compute import UrlMapsAggregatedList
from google.cloud.compute_v1.types.compute import UrlMapsScopedList
from google.cloud.compute_v1.types.compute import UrlMapsValidateRequest
from google.cloud.compute_v1.types.compute import UrlMapsValidateResponse
from google.cloud.compute_v1.types.compute import UrlMapTest
from google.cloud.compute_v1.types.compute import UrlMapTestHeader
from google.cloud.compute_v1.types.compute import UrlMapValidationResult
from google.cloud.compute_v1.types.compute import UrlRewrite
from google.cloud.compute_v1.types.compute import UsableSubnetwork
from google.cloud.compute_v1.types.compute import UsableSubnetworksAggregatedList
from google.cloud.compute_v1.types.compute import UsableSubnetworkSecondaryRange
from google.cloud.compute_v1.types.compute import UsageExportLocation
from google.cloud.compute_v1.types.compute import ValidateRegionUrlMapRequest
from google.cloud.compute_v1.types.compute import ValidateUrlMapRequest
from google.cloud.compute_v1.types.compute import VmEndpointNatMappings
from google.cloud.compute_v1.types.compute import VmEndpointNatMappingsInterfaceNatMappings
from google.cloud.compute_v1.types.compute import VmEndpointNatMappingsInterfaceNatMappingsNatRuleMappings
from google.cloud.compute_v1.types.compute import VmEndpointNatMappingsList
from google.cloud.compute_v1.types.compute import VpnGateway
from google.cloud.compute_v1.types.compute import VpnGatewayAggregatedList
from google.cloud.compute_v1.types.compute import VpnGatewayList
from google.cloud.compute_v1.types.compute import VpnGatewaysGetStatusResponse
from google.cloud.compute_v1.types.compute import VpnGatewaysScopedList
from google.cloud.compute_v1.types.compute import VpnGatewayStatus
from google.cloud.compute_v1.types.compute import VpnGatewayStatusHighAvailabilityRequirementState
from google.cloud.compute_v1.types.compute import VpnGatewayStatusTunnel
from google.cloud.compute_v1.types.compute import VpnGatewayStatusVpnConnection
from google.cloud.compute_v1.types.compute import VpnGatewayVpnGatewayInterface
from google.cloud.compute_v1.types.compute import VpnTunnel
from google.cloud.compute_v1.types.compute import VpnTunnelAggregatedList
from google.cloud.compute_v1.types.compute import VpnTunnelList
from google.cloud.compute_v1.types.compute import VpnTunnelsScopedList
from google.cloud.compute_v1.types.compute import WafExpressionSet
from google.cloud.compute_v1.types.compute import WafExpressionSetExpression
from google.cloud.compute_v1.types.compute import WaitGlobalOperationRequest
from google.cloud.compute_v1.types.compute import WaitRegionOperationRequest
from google.cloud.compute_v1.types.compute import WaitZoneOperationRequest
from google.cloud.compute_v1.types.compute import Warning
from google.cloud.compute_v1.types.compute import Warnings
from google.cloud.compute_v1.types.compute import WeightedBackendService
from google.cloud.compute_v1.types.compute import WithdrawPublicAdvertisedPrefixeRequest
from google.cloud.compute_v1.types.compute import WithdrawPublicDelegatedPrefixeRequest
from google.cloud.compute_v1.types.compute import XpnHostList
from google.cloud.compute_v1.types.compute import XpnResourceId
from google.cloud.compute_v1.types.compute import Zone
from google.cloud.compute_v1.types.compute import ZoneList
from google.cloud.compute_v1.types.compute import ZoneSetLabelsRequest
from google.cloud.compute_v1.types.compute import ZoneSetPolicyRequest

__all__ = ('AcceleratorTypesClient',
    'AddressesClient',
    'AutoscalersClient',
    'BackendBucketsClient',
    'BackendServicesClient',
    'DisksClient',
    'DiskTypesClient',
    'ExternalVpnGatewaysClient',
    'FirewallPoliciesClient',
    'FirewallsClient',
    'ForwardingRulesClient',
    'GlobalAddressesClient',
    'GlobalForwardingRulesClient',
    'GlobalNetworkEndpointGroupsClient',
    'GlobalOperationsClient',
    'GlobalOrganizationOperationsClient',
    'GlobalPublicDelegatedPrefixesClient',
    'HealthChecksClient',
    'ImageFamilyViewsClient',
    'ImagesClient',
    'InstanceGroupManagerResizeRequestsClient',
    'InstanceGroupManagersClient',
    'InstanceGroupsClient',
    'InstancesClient',
    'InstanceSettingsServiceClient',
    'InstanceTemplatesClient',
    'InstantSnapshotsClient',
    'InterconnectAttachmentsClient',
    'InterconnectLocationsClient',
    'InterconnectRemoteLocationsClient',
    'InterconnectsClient',
    'LicenseCodesClient',
    'LicensesClient',
    'MachineImagesClient',
    'MachineTypesClient',
    'NetworkAttachmentsClient',
    'NetworkEdgeSecurityServicesClient',
    'NetworkEndpointGroupsClient',
    'NetworkFirewallPoliciesClient',
    'NetworksClient',
    'NodeGroupsClient',
    'NodeTemplatesClient',
    'NodeTypesClient',
    'PacketMirroringsClient',
    'ProjectsClient',
    'PublicAdvertisedPrefixesClient',
    'PublicDelegatedPrefixesClient',
    'RegionAutoscalersClient',
    'RegionBackendServicesClient',
    'RegionCommitmentsClient',
    'RegionDisksClient',
    'RegionDiskTypesClient',
    'RegionHealthChecksClient',
    'RegionHealthCheckServicesClient',
    'RegionInstanceGroupManagersClient',
    'RegionInstanceGroupsClient',
    'RegionInstancesClient',
    'RegionInstanceTemplatesClient',
    'RegionInstantSnapshotsClient',
    'RegionNetworkEndpointGroupsClient',
    'RegionNetworkFirewallPoliciesClient',
    'RegionNotificationEndpointsClient',
    'RegionOperationsClient',
    'RegionsClient',
    'RegionSecurityPoliciesClient',
    'RegionSslCertificatesClient',
    'RegionSslPoliciesClient',
    'RegionTargetHttpProxiesClient',
    'RegionTargetHttpsProxiesClient',
    'RegionTargetTcpProxiesClient',
    'RegionUrlMapsClient',
    'RegionZonesClient',
    'ReservationsClient',
    'ResourcePoliciesClient',
    'RoutersClient',
    'RoutesClient',
    'SecurityPoliciesClient',
    'ServiceAttachmentsClient',
    'SnapshotsClient',
    'SnapshotSettingsServiceClient',
    'SslCertificatesClient',
    'SslPoliciesClient',
    'StoragePoolsClient',
    'StoragePoolTypesClient',
    'SubnetworksClient',
    'TargetGrpcProxiesClient',
    'TargetHttpProxiesClient',
    'TargetHttpsProxiesClient',
    'TargetInstancesClient',
    'TargetPoolsClient',
    'TargetSslProxiesClient',
    'TargetTcpProxiesClient',
    'TargetVpnGatewaysClient',
    'UrlMapsClient',
    'VpnGatewaysClient',
    'VpnTunnelsClient',
    'ZoneOperationsClient',
    'ZonesClient',
    'AbandonInstancesInstanceGroupManagerRequest',
    'AbandonInstancesRegionInstanceGroupManagerRequest',
    'AcceleratorConfig',
    'Accelerators',
    'AcceleratorType',
    'AcceleratorTypeAggregatedList',
    'AcceleratorTypeList',
    'AcceleratorTypesScopedList',
    'AccessConfig',
    'AddAccessConfigInstanceRequest',
    'AddAssociationFirewallPolicyRequest',
    'AddAssociationNetworkFirewallPolicyRequest',
    'AddAssociationRegionNetworkFirewallPolicyRequest',
    'AddHealthCheckTargetPoolRequest',
    'AddInstancesInstanceGroupRequest',
    'AddInstanceTargetPoolRequest',
    'AddNodesNodeGroupRequest',
    'AddPeeringNetworkRequest',
    'AddResourcePoliciesDiskRequest',
    'AddResourcePoliciesInstanceRequest',
    'AddResourcePoliciesRegionDiskRequest',
    'Address',
    'AddressAggregatedList',
    'AddressesScopedList',
    'AddressList',
    'AddRuleFirewallPolicyRequest',
    'AddRuleNetworkFirewallPolicyRequest',
    'AddRuleRegionNetworkFirewallPolicyRequest',
    'AddRuleRegionSecurityPolicyRequest',
    'AddRuleSecurityPolicyRequest',
    'AddSignedUrlKeyBackendBucketRequest',
    'AddSignedUrlKeyBackendServiceRequest',
    'AdvancedMachineFeatures',
    'AggregatedListAcceleratorTypesRequest',
    'AggregatedListAddressesRequest',
    'AggregatedListAutoscalersRequest',
    'AggregatedListBackendServicesRequest',
    'AggregatedListDisksRequest',
    'AggregatedListDiskTypesRequest',
    'AggregatedListForwardingRulesRequest',
    'AggregatedListGlobalOperationsRequest',
    'AggregatedListHealthChecksRequest',
    'AggregatedListInstanceGroupManagersRequest',
    'AggregatedListInstanceGroupsRequest',
    'AggregatedListInstancesRequest',
    'AggregatedListInstanceTemplatesRequest',
    'AggregatedListInstantSnapshotsRequest',
    'AggregatedListInterconnectAttachmentsRequest',
    'AggregatedListMachineTypesRequest',
    'AggregatedListNetworkAttachmentsRequest',
    'AggregatedListNetworkEdgeSecurityServicesRequest',
    'AggregatedListNetworkEndpointGroupsRequest',
    'AggregatedListNodeGroupsRequest',
    'AggregatedListNodeTemplatesRequest',
    'AggregatedListNodeTypesRequest',
    'AggregatedListPacketMirroringsRequest',
    'AggregatedListPublicDelegatedPrefixesRequest',
    'AggregatedListRegionCommitmentsRequest',
    'AggregatedListReservationsRequest',
    'AggregatedListResourcePoliciesRequest',
    'AggregatedListRoutersRequest',
    'AggregatedListSecurityPoliciesRequest',
    'AggregatedListServiceAttachmentsRequest',
    'AggregatedListSslCertificatesRequest',
    'AggregatedListSslPoliciesRequest',
    'AggregatedListStoragePoolsRequest',
    'AggregatedListStoragePoolTypesRequest',
    'AggregatedListSubnetworksRequest',
    'AggregatedListTargetHttpProxiesRequest',
    'AggregatedListTargetHttpsProxiesRequest',
    'AggregatedListTargetInstancesRequest',
    'AggregatedListTargetPoolsRequest',
    'AggregatedListTargetTcpProxiesRequest',
    'AggregatedListTargetVpnGatewaysRequest',
    'AggregatedListUrlMapsRequest',
    'AggregatedListVpnGatewaysRequest',
    'AggregatedListVpnTunnelsRequest',
    'AliasIpRange',
    'AllocationAggregateReservation',
    'AllocationAggregateReservationReservedResourceInfo',
    'AllocationAggregateReservationReservedResourceInfoAccelerator',
    'AllocationResourceStatus',
    'AllocationResourceStatusSpecificSKUAllocation',
    'AllocationSpecificSKUAllocationAllocatedInstancePropertiesReservedDisk',
    'AllocationSpecificSKUAllocationReservedInstanceProperties',
    'AllocationSpecificSKUReservation',
    'Allowed',
    'AnnouncePublicAdvertisedPrefixeRequest',
    'AnnouncePublicDelegatedPrefixeRequest',
    'ApplyUpdatesToInstancesInstanceGroupManagerRequest',
    'ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest',
    'AttachDiskInstanceRequest',
    'AttachedDisk',
    'AttachedDiskInitializeParams',
    'AttachNetworkEndpointsGlobalNetworkEndpointGroupRequest',
    'AttachNetworkEndpointsNetworkEndpointGroupRequest',
    'AttachNetworkEndpointsRegionNetworkEndpointGroupRequest',
    'AuditConfig',
    'AuditLogConfig',
    'AuthorizationLoggingOptions',
    'Autoscaler',
    'AutoscalerAggregatedList',
    'AutoscalerList',
    'AutoscalersScopedList',
    'AutoscalerStatusDetails',
    'AutoscalingPolicy',
    'AutoscalingPolicyCpuUtilization',
    'AutoscalingPolicyCustomMetricUtilization',
    'AutoscalingPolicyLoadBalancingUtilization',
    'AutoscalingPolicyScaleInControl',
    'AutoscalingPolicyScalingSchedule',
    'AWSV4Signature',
    'Backend',
    'BackendBucket',
    'BackendBucketCdnPolicy',
    'BackendBucketCdnPolicyBypassCacheOnRequestHeader',
    'BackendBucketCdnPolicyCacheKeyPolicy',
    'BackendBucketCdnPolicyNegativeCachingPolicy',
    'BackendBucketList',
    'BackendService',
    'BackendServiceAggregatedList',
    'BackendServiceCdnPolicy',
    'BackendServiceCdnPolicyBypassCacheOnRequestHeader',
    'BackendServiceCdnPolicyNegativeCachingPolicy',
    'BackendServiceConnectionTrackingPolicy',
    'BackendServiceFailoverPolicy',
    'BackendServiceGroupHealth',
    'BackendServiceIAP',
    'BackendServiceList',
    'BackendServiceListUsable',
    'BackendServiceLocalityLoadBalancingPolicyConfig',
    'BackendServiceLocalityLoadBalancingPolicyConfigCustomPolicy',
    'BackendServiceLocalityLoadBalancingPolicyConfigPolicy',
    'BackendServiceLogConfig',
    'BackendServiceReference',
    'BackendServicesScopedList',
    'BackendServiceUsedBy',
    'BfdPacket',
    'BfdStatus',
    'BfdStatusPacketCounts',
    'Binding',
    'BulkInsertDiskRequest',
    'BulkInsertDiskResource',
    'BulkInsertInstanceRequest',
    'BulkInsertInstanceResource',
    'BulkInsertInstanceResourcePerInstanceProperties',
    'BulkInsertOperationStatus',
    'BulkInsertRegionDiskRequest',
    'BulkInsertRegionInstanceRequest',
    'CacheInvalidationRule',
    'CacheKeyPolicy',
    'CancelInstanceGroupManagerResizeRequestRequest',
    'CircuitBreakers',
    'CloneRulesFirewallPolicyRequest',
    'CloneRulesNetworkFirewallPolicyRequest',
    'CloneRulesRegionNetworkFirewallPolicyRequest',
    'Commitment',
    'CommitmentAggregatedList',
    'CommitmentList',
    'CommitmentsScopedList',
    'Condition',
    'ConfidentialInstanceConfig',
    'ConnectionDraining',
    'ConsistentHashLoadBalancerSettings',
    'ConsistentHashLoadBalancerSettingsHttpCookie',
    'CorsPolicy',
    'CreateInstancesInstanceGroupManagerRequest',
    'CreateInstancesRegionInstanceGroupManagerRequest',
    'CreateSnapshotDiskRequest',
    'CreateSnapshotRegionDiskRequest',
    'CustomerEncryptionKey',
    'CustomerEncryptionKeyProtectedDisk',
    'Data',
    'DeleteAccessConfigInstanceRequest',
    'DeleteAddressRequest',
    'DeleteAutoscalerRequest',
    'DeleteBackendBucketRequest',
    'DeleteBackendServiceRequest',
    'DeleteDiskRequest',
    'DeleteExternalVpnGatewayRequest',
    'DeleteFirewallPolicyRequest',
    'DeleteFirewallRequest',
    'DeleteForwardingRuleRequest',
    'DeleteGlobalAddressRequest',
    'DeleteGlobalForwardingRuleRequest',
    'DeleteGlobalNetworkEndpointGroupRequest',
    'DeleteGlobalOperationRequest',
    'DeleteGlobalOperationResponse',
    'DeleteGlobalOrganizationOperationRequest',
    'DeleteGlobalOrganizationOperationResponse',
    'DeleteGlobalPublicDelegatedPrefixeRequest',
    'DeleteHealthCheckRequest',
    'DeleteImageRequest',
    'DeleteInstanceGroupManagerRequest',
    'DeleteInstanceGroupManagerResizeRequestRequest',
    'DeleteInstanceGroupRequest',
    'DeleteInstanceRequest',
    'DeleteInstancesInstanceGroupManagerRequest',
    'DeleteInstancesRegionInstanceGroupManagerRequest',
    'DeleteInstanceTemplateRequest',
    'DeleteInstantSnapshotRequest',
    'DeleteInterconnectAttachmentRequest',
    'DeleteInterconnectRequest',
    'DeleteLicenseRequest',
    'DeleteMachineImageRequest',
    'DeleteNetworkAttachmentRequest',
    'DeleteNetworkEdgeSecurityServiceRequest',
    'DeleteNetworkEndpointGroupRequest',
    'DeleteNetworkFirewallPolicyRequest',
    'DeleteNetworkRequest',
    'DeleteNodeGroupRequest',
    'DeleteNodesNodeGroupRequest',
    'DeleteNodeTemplateRequest',
    'DeletePacketMirroringRequest',
    'DeletePerInstanceConfigsInstanceGroupManagerRequest',
    'DeletePerInstanceConfigsRegionInstanceGroupManagerRequest',
    'DeletePublicAdvertisedPrefixeRequest',
    'DeletePublicDelegatedPrefixeRequest',
    'DeleteRegionAutoscalerRequest',
    'DeleteRegionBackendServiceRequest',
    'DeleteRegionDiskRequest',
    'DeleteRegionHealthCheckRequest',
    'DeleteRegionHealthCheckServiceRequest',
    'DeleteRegionInstanceGroupManagerRequest',
    'DeleteRegionInstanceTemplateRequest',
    'DeleteRegionInstantSnapshotRequest',
    'DeleteRegionNetworkEndpointGroupRequest',
    'DeleteRegionNetworkFirewallPolicyRequest',
    'DeleteRegionNotificationEndpointRequest',
    'DeleteRegionOperationRequest',
    'DeleteRegionOperationResponse',
    'DeleteRegionSecurityPolicyRequest',
    'DeleteRegionSslCertificateRequest',
    'DeleteRegionSslPolicyRequest',
    'DeleteRegionTargetHttpProxyRequest',
    'DeleteRegionTargetHttpsProxyRequest',
    'DeleteRegionTargetTcpProxyRequest',
    'DeleteRegionUrlMapRequest',
    'DeleteReservationRequest',
    'DeleteResourcePolicyRequest',
    'DeleteRouteRequest',
    'DeleteRouterRequest',
    'DeleteSecurityPolicyRequest',
    'DeleteServiceAttachmentRequest',
    'DeleteSignedUrlKeyBackendBucketRequest',
    'DeleteSignedUrlKeyBackendServiceRequest',
    'DeleteSnapshotRequest',
    'DeleteSslCertificateRequest',
    'DeleteSslPolicyRequest',
    'DeleteStoragePoolRequest',
    'DeleteSubnetworkRequest',
    'DeleteTargetGrpcProxyRequest',
    'DeleteTargetHttpProxyRequest',
    'DeleteTargetHttpsProxyRequest',
    'DeleteTargetInstanceRequest',
    'DeleteTargetPoolRequest',
    'DeleteTargetSslProxyRequest',
    'DeleteTargetTcpProxyRequest',
    'DeleteTargetVpnGatewayRequest',
    'DeleteUrlMapRequest',
    'DeleteVpnGatewayRequest',
    'DeleteVpnTunnelRequest',
    'DeleteZoneOperationRequest',
    'DeleteZoneOperationResponse',
    'Denied',
    'DeprecateImageRequest',
    'DeprecationStatus',
    'DetachDiskInstanceRequest',
    'DetachNetworkEndpointsGlobalNetworkEndpointGroupRequest',
    'DetachNetworkEndpointsNetworkEndpointGroupRequest',
    'DetachNetworkEndpointsRegionNetworkEndpointGroupRequest',
    'DisableXpnHostProjectRequest',
    'DisableXpnResourceProjectRequest',
    'Disk',
    'DiskAggregatedList',
    'DiskAsyncReplication',
    'DiskAsyncReplicationList',
    'DiskInstantiationConfig',
    'DiskList',
    'DiskMoveRequest',
    'DiskParams',
    'DiskResourceStatus',
    'DiskResourceStatusAsyncReplicationStatus',
    'DisksAddResourcePoliciesRequest',
    'DisksRemoveResourcePoliciesRequest',
    'DisksResizeRequest',
    'DisksScopedList',
    'DisksStartAsyncReplicationRequest',
    'DisksStopGroupAsyncReplicationResource',
    'DiskType',
    'DiskTypeAggregatedList',
    'DiskTypeList',
    'DiskTypesScopedList',
    'DisplayDevice',
    'DistributionPolicy',
    'DistributionPolicyZoneConfiguration',
    'Duration',
    'EnableXpnHostProjectRequest',
    'EnableXpnResourceProjectRequest',
    'Error',
    'ErrorDetails',
    'ErrorInfo',
    'Errors',
    'ExchangedPeeringRoute',
    'ExchangedPeeringRoutesList',
    'ExpandIpCidrRangeSubnetworkRequest',
    'Expr',
    'ExternalVpnGateway',
    'ExternalVpnGatewayInterface',
    'ExternalVpnGatewayList',
    'FileContentBuffer',
    'Firewall',
    'FirewallList',
    'FirewallLogConfig',
    'FirewallPoliciesListAssociationsResponse',
    'FirewallPolicy',
    'FirewallPolicyAssociation',
    'FirewallPolicyList',
    'FirewallPolicyRule',
    'FirewallPolicyRuleMatcher',
    'FirewallPolicyRuleMatcherLayer4Config',
    'FirewallPolicyRuleSecureTag',
    'FixedOrPercent',
    'ForwardingRule',
    'ForwardingRuleAggregatedList',
    'ForwardingRuleList',
    'ForwardingRuleReference',
    'ForwardingRuleServiceDirectoryRegistration',
    'ForwardingRulesScopedList',
    'GetAcceleratorTypeRequest',
    'GetAddressRequest',
    'GetAssociationFirewallPolicyRequest',
    'GetAssociationNetworkFirewallPolicyRequest',
    'GetAssociationRegionNetworkFirewallPolicyRequest',
    'GetAutoscalerRequest',
    'GetBackendBucketRequest',
    'GetBackendServiceRequest',
    'GetDiagnosticsInterconnectRequest',
    'GetDiskRequest',
    'GetDiskTypeRequest',
    'GetEffectiveFirewallsInstanceRequest',
    'GetEffectiveFirewallsNetworkRequest',
    'GetEffectiveFirewallsRegionNetworkFirewallPolicyRequest',
    'GetExternalVpnGatewayRequest',
    'GetFirewallPolicyRequest',
    'GetFirewallRequest',
    'GetForwardingRuleRequest',
    'GetFromFamilyImageRequest',
    'GetGlobalAddressRequest',
    'GetGlobalForwardingRuleRequest',
    'GetGlobalNetworkEndpointGroupRequest',
    'GetGlobalOperationRequest',
    'GetGlobalOrganizationOperationRequest',
    'GetGlobalPublicDelegatedPrefixeRequest',
    'GetGuestAttributesInstanceRequest',
    'GetHealthBackendServiceRequest',
    'GetHealthCheckRequest',
    'GetHealthRegionBackendServiceRequest',
    'GetHealthTargetPoolRequest',
    'GetIamPolicyBackendBucketRequest',
    'GetIamPolicyBackendServiceRequest',
    'GetIamPolicyDiskRequest',
    'GetIamPolicyFirewallPolicyRequest',
    'GetIamPolicyImageRequest',
    'GetIamPolicyInstanceRequest',
    'GetIamPolicyInstanceTemplateRequest',
    'GetIamPolicyInstantSnapshotRequest',
    'GetIamPolicyLicenseRequest',
    'GetIamPolicyMachineImageRequest',
    'GetIamPolicyNetworkAttachmentRequest',
    'GetIamPolicyNetworkFirewallPolicyRequest',
    'GetIamPolicyNodeGroupRequest',
    'GetIamPolicyNodeTemplateRequest',
    'GetIamPolicyRegionBackendServiceRequest',
    'GetIamPolicyRegionDiskRequest',
    'GetIamPolicyRegionInstantSnapshotRequest',
    'GetIamPolicyRegionNetworkFirewallPolicyRequest',
    'GetIamPolicyReservationRequest',
    'GetIamPolicyResourcePolicyRequest',
    'GetIamPolicyServiceAttachmentRequest',
    'GetIamPolicySnapshotRequest',
    'GetIamPolicyStoragePoolRequest',
    'GetIamPolicySubnetworkRequest',
    'GetImageFamilyViewRequest',
    'GetImageRequest',
    'GetInstanceGroupManagerRequest',
    'GetInstanceGroupManagerResizeRequestRequest',
    'GetInstanceGroupRequest',
    'GetInstanceRequest',
    'GetInstanceSettingRequest',
    'GetInstanceTemplateRequest',
    'GetInstantSnapshotRequest',
    'GetInterconnectAttachmentRequest',
    'GetInterconnectLocationRequest',
    'GetInterconnectRemoteLocationRequest',
    'GetInterconnectRequest',
    'GetLicenseCodeRequest',
    'GetLicenseRequest',
    'GetMachineImageRequest',
    'GetMachineTypeRequest',
    'GetMacsecConfigInterconnectRequest',
    'GetNatIpInfoRouterRequest',
    'GetNatMappingInfoRoutersRequest',
    'GetNetworkAttachmentRequest',
    'GetNetworkEdgeSecurityServiceRequest',
    'GetNetworkEndpointGroupRequest',
    'GetNetworkFirewallPolicyRequest',
    'GetNetworkRequest',
    'GetNodeGroupRequest',
    'GetNodeTemplateRequest',
    'GetNodeTypeRequest',
    'GetPacketMirroringRequest',
    'GetProjectRequest',
    'GetPublicAdvertisedPrefixeRequest',
    'GetPublicDelegatedPrefixeRequest',
    'GetRegionAutoscalerRequest',
    'GetRegionBackendServiceRequest',
    'GetRegionCommitmentRequest',
    'GetRegionDiskRequest',
    'GetRegionDiskTypeRequest',
    'GetRegionHealthCheckRequest',
    'GetRegionHealthCheckServiceRequest',
    'GetRegionInstanceGroupManagerRequest',
    'GetRegionInstanceGroupRequest',
    'GetRegionInstanceTemplateRequest',
    'GetRegionInstantSnapshotRequest',
    'GetRegionNetworkEndpointGroupRequest',
    'GetRegionNetworkFirewallPolicyRequest',
    'GetRegionNotificationEndpointRequest',
    'GetRegionOperationRequest',
    'GetRegionRequest',
    'GetRegionSecurityPolicyRequest',
    'GetRegionSslCertificateRequest',
    'GetRegionSslPolicyRequest',
    'GetRegionTargetHttpProxyRequest',
    'GetRegionTargetHttpsProxyRequest',
    'GetRegionTargetTcpProxyRequest',
    'GetRegionUrlMapRequest',
    'GetReservationRequest',
    'GetResourcePolicyRequest',
    'GetRouteRequest',
    'GetRouterRequest',
    'GetRouterStatusRouterRequest',
    'GetRuleFirewallPolicyRequest',
    'GetRuleNetworkFirewallPolicyRequest',
    'GetRuleRegionNetworkFirewallPolicyRequest',
    'GetRuleRegionSecurityPolicyRequest',
    'GetRuleSecurityPolicyRequest',
    'GetScreenshotInstanceRequest',
    'GetSecurityPolicyRequest',
    'GetSerialPortOutputInstanceRequest',
    'GetServiceAttachmentRequest',
    'GetShieldedInstanceIdentityInstanceRequest',
    'GetSnapshotRequest',
    'GetSnapshotSettingRequest',
    'GetSslCertificateRequest',
    'GetSslPolicyRequest',
    'GetStatusVpnGatewayRequest',
    'GetStoragePoolRequest',
    'GetStoragePoolTypeRequest',
    'GetSubnetworkRequest',
    'GetTargetGrpcProxyRequest',
    'GetTargetHttpProxyRequest',
    'GetTargetHttpsProxyRequest',
    'GetTargetInstanceRequest',
    'GetTargetPoolRequest',
    'GetTargetSslProxyRequest',
    'GetTargetTcpProxyRequest',
    'GetTargetVpnGatewayRequest',
    'GetUrlMapRequest',
    'GetVpnGatewayRequest',
    'GetVpnTunnelRequest',
    'GetXpnHostProjectRequest',
    'GetXpnResourcesProjectsRequest',
    'GetZoneOperationRequest',
    'GetZoneRequest',
    'GlobalAddressesMoveRequest',
    'GlobalNetworkEndpointGroupsAttachEndpointsRequest',
    'GlobalNetworkEndpointGroupsDetachEndpointsRequest',
    'GlobalOrganizationSetPolicyRequest',
    'GlobalSetLabelsRequest',
    'GlobalSetPolicyRequest',
    'GRPCHealthCheck',
    'GuestAttributes',
    'GuestAttributesEntry',
    'GuestAttributesValue',
    'GuestOsFeature',
    'HealthCheck',
    'HealthCheckList',
    'HealthCheckLogConfig',
    'HealthCheckReference',
    'HealthChecksAggregatedList',
    'HealthCheckService',
    'HealthCheckServiceReference',
    'HealthCheckServicesList',
    'HealthChecksScopedList',
    'HealthStatus',
    'HealthStatusForNetworkEndpoint',
    'Help',
    'HelpLink',
    'HostRule',
    'HTTP2HealthCheck',
    'HttpFaultAbort',
    'HttpFaultDelay',
    'HttpFaultInjection',
    'HttpHeaderAction',
    'HttpHeaderMatch',
    'HttpHeaderOption',
    'HTTPHealthCheck',
    'HttpQueryParameterMatch',
    'HttpRedirectAction',
    'HttpRetryPolicy',
    'HttpRouteAction',
    'HttpRouteRule',
    'HttpRouteRuleMatch',
    'HTTPSHealthCheck',
    'Image',
    'ImageFamilyView',
    'ImageList',
    'InitialStateConfig',
    'InsertAddressRequest',
    'InsertAutoscalerRequest',
    'InsertBackendBucketRequest',
    'InsertBackendServiceRequest',
    'InsertDiskRequest',
    'InsertExternalVpnGatewayRequest',
    'InsertFirewallPolicyRequest',
    'InsertFirewallRequest',
    'InsertForwardingRuleRequest',
    'InsertGlobalAddressRequest',
    'InsertGlobalForwardingRuleRequest',
    'InsertGlobalNetworkEndpointGroupRequest',
    'InsertGlobalPublicDelegatedPrefixeRequest',
    'InsertHealthCheckRequest',
    'InsertImageRequest',
    'InsertInstanceGroupManagerRequest',
    'InsertInstanceGroupManagerResizeRequestRequest',
    'InsertInstanceGroupRequest',
    'InsertInstanceRequest',
    'InsertInstanceTemplateRequest',
    'InsertInstantSnapshotRequest',
    'InsertInterconnectAttachmentRequest',
    'InsertInterconnectRequest',
    'InsertLicenseRequest',
    'InsertMachineImageRequest',
    'InsertNetworkAttachmentRequest',
    'InsertNetworkEdgeSecurityServiceRequest',
    'InsertNetworkEndpointGroupRequest',
    'InsertNetworkFirewallPolicyRequest',
    'InsertNetworkRequest',
    'InsertNodeGroupRequest',
    'InsertNodeTemplateRequest',
    'InsertPacketMirroringRequest',
    'InsertPublicAdvertisedPrefixeRequest',
    'InsertPublicDelegatedPrefixeRequest',
    'InsertRegionAutoscalerRequest',
    'InsertRegionBackendServiceRequest',
    'InsertRegionCommitmentRequest',
    'InsertRegionDiskRequest',
    'InsertRegionHealthCheckRequest',
    'InsertRegionHealthCheckServiceRequest',
    'InsertRegionInstanceGroupManagerRequest',
    'InsertRegionInstanceTemplateRequest',
    'InsertRegionInstantSnapshotRequest',
    'InsertRegionNetworkEndpointGroupRequest',
    'InsertRegionNetworkFirewallPolicyRequest',
    'InsertRegionNotificationEndpointRequest',
    'InsertRegionSecurityPolicyRequest',
    'InsertRegionSslCertificateRequest',
    'InsertRegionSslPolicyRequest',
    'InsertRegionTargetHttpProxyRequest',
    'InsertRegionTargetHttpsProxyRequest',
    'InsertRegionTargetTcpProxyRequest',
    'InsertRegionUrlMapRequest',
    'InsertReservationRequest',
    'InsertResourcePolicyRequest',
    'InsertRouteRequest',
    'InsertRouterRequest',
    'InsertSecurityPolicyRequest',
    'InsertServiceAttachmentRequest',
    'InsertSnapshotRequest',
    'InsertSslCertificateRequest',
    'InsertSslPolicyRequest',
    'InsertStoragePoolRequest',
    'InsertSubnetworkRequest',
    'InsertTargetGrpcProxyRequest',
    'InsertTargetHttpProxyRequest',
    'InsertTargetHttpsProxyRequest',
    'InsertTargetInstanceRequest',
    'InsertTargetPoolRequest',
    'InsertTargetSslProxyRequest',
    'InsertTargetTcpProxyRequest',
    'InsertTargetVpnGatewayRequest',
    'InsertUrlMapRequest',
    'InsertVpnGatewayRequest',
    'InsertVpnTunnelRequest',
    'Instance',
    'InstanceAggregatedList',
    'InstanceConsumptionData',
    'InstanceConsumptionInfo',
    'InstanceGroup',
    'InstanceGroupAggregatedList',
    'InstanceGroupList',
    'InstanceGroupManager',
    'InstanceGroupManagerActionsSummary',
    'InstanceGroupManagerAggregatedList',
    'InstanceGroupManagerAllInstancesConfig',
    'InstanceGroupManagerAutoHealingPolicy',
    'InstanceGroupManagerInstanceLifecyclePolicy',
    'InstanceGroupManagerList',
    'InstanceGroupManagerResizeRequest',
    'InstanceGroupManagerResizeRequestsListResponse',
    'InstanceGroupManagerResizeRequestStatus',
    'InstanceGroupManagerResizeRequestStatusLastAttempt',
    'InstanceGroupManagersAbandonInstancesRequest',
    'InstanceGroupManagersApplyUpdatesRequest',
    'InstanceGroupManagersCreateInstancesRequest',
    'InstanceGroupManagersDeleteInstancesRequest',
    'InstanceGroupManagersDeletePerInstanceConfigsReq',
    'InstanceGroupManagersListErrorsResponse',
    'InstanceGroupManagersListManagedInstancesResponse',
    'InstanceGroupManagersListPerInstanceConfigsResp',
    'InstanceGroupManagersPatchPerInstanceConfigsReq',
    'InstanceGroupManagersRecreateInstancesRequest',
    'InstanceGroupManagersScopedList',
    'InstanceGroupManagersSetInstanceTemplateRequest',
    'InstanceGroupManagersSetTargetPoolsRequest',
    'InstanceGroupManagerStatus',
    'InstanceGroupManagerStatusAllInstancesConfig',
    'InstanceGroupManagerStatusStateful',
    'InstanceGroupManagerStatusStatefulPerInstanceConfigs',
    'InstanceGroupManagerStatusVersionTarget',
    'InstanceGroupManagersUpdatePerInstanceConfigsReq',
    'InstanceGroupManagerUpdatePolicy',
    'InstanceGroupManagerVersion',
    'InstanceGroupsAddInstancesRequest',
    'InstanceGroupsListInstances',
    'InstanceGroupsListInstancesRequest',
    'InstanceGroupsRemoveInstancesRequest',
    'InstanceGroupsScopedList',
    'InstanceGroupsSetNamedPortsRequest',
    'InstanceList',
    'InstanceListReferrers',
    'InstanceManagedByIgmError',
    'InstanceManagedByIgmErrorInstanceActionDetails',
    'InstanceManagedByIgmErrorManagedInstanceError',
    'InstanceMoveRequest',
    'InstanceParams',
    'InstanceProperties',
    'InstancePropertiesPatch',
    'InstanceReference',
    'InstancesAddResourcePoliciesRequest',
    'InstancesBulkInsertOperationMetadata',
    'InstanceSettings',
    'InstanceSettingsMetadata',
    'InstancesGetEffectiveFirewallsResponse',
    'InstancesGetEffectiveFirewallsResponseEffectiveFirewallPolicy',
    'InstancesRemoveResourcePoliciesRequest',
    'InstancesScopedList',
    'InstancesSetLabelsRequest',
    'InstancesSetMachineResourcesRequest',
    'InstancesSetMachineTypeRequest',
    'InstancesSetMinCpuPlatformRequest',
    'InstancesSetNameRequest',
    'InstancesSetSecurityPolicyRequest',
    'InstancesSetServiceAccountRequest',
    'InstancesStartWithEncryptionKeyRequest',
    'InstanceTemplate',
    'InstanceTemplateAggregatedList',
    'InstanceTemplateList',
    'InstanceTemplatesScopedList',
    'InstanceWithNamedPorts',
    'InstantSnapshot',
    'InstantSnapshotAggregatedList',
    'InstantSnapshotList',
    'InstantSnapshotResourceStatus',
    'InstantSnapshotsScopedList',
    'Int64RangeMatch',
    'Interconnect',
    'InterconnectAttachment',
    'InterconnectAttachmentAggregatedList',
    'InterconnectAttachmentConfigurationConstraints',
    'InterconnectAttachmentConfigurationConstraintsBgpPeerASNRange',
    'InterconnectAttachmentList',
    'InterconnectAttachmentPartnerMetadata',
    'InterconnectAttachmentPrivateInfo',
    'InterconnectAttachmentsScopedList',
    'InterconnectCircuitInfo',
    'InterconnectDiagnostics',
    'InterconnectDiagnosticsARPEntry',
    'InterconnectDiagnosticsLinkLACPStatus',
    'InterconnectDiagnosticsLinkOpticalPower',
    'InterconnectDiagnosticsLinkStatus',
    'InterconnectDiagnosticsMacsecStatus',
    'InterconnectList',
    'InterconnectLocation',
    'InterconnectLocationList',
    'InterconnectLocationRegionInfo',
    'InterconnectMacsec',
    'InterconnectMacsecConfig',
    'InterconnectMacsecConfigPreSharedKey',
    'InterconnectMacsecPreSharedKey',
    'InterconnectOutageNotification',
    'InterconnectRemoteLocation',
    'InterconnectRemoteLocationConstraints',
    'InterconnectRemoteLocationConstraintsSubnetLengthRange',
    'InterconnectRemoteLocationList',
    'InterconnectRemoteLocationPermittedConnections',
    'InterconnectsGetDiagnosticsResponse',
    'InterconnectsGetMacsecConfigResponse',
    'InvalidateCacheUrlMapRequest',
    'Items',
    'License',
    'LicenseCode',
    'LicenseCodeLicenseAlias',
    'LicenseResourceCommitment',
    'LicenseResourceRequirements',
    'LicensesListResponse',
    'ListAcceleratorTypesRequest',
    'ListAddressesRequest',
    'ListAssociationsFirewallPolicyRequest',
    'ListAutoscalersRequest',
    'ListAvailableFeaturesRegionSslPoliciesRequest',
    'ListAvailableFeaturesSslPoliciesRequest',
    'ListBackendBucketsRequest',
    'ListBackendServicesRequest',
    'ListDisksRequest',
    'ListDisksStoragePoolsRequest',
    'ListDiskTypesRequest',
    'ListErrorsInstanceGroupManagersRequest',
    'ListErrorsRegionInstanceGroupManagersRequest',
    'ListExternalVpnGatewaysRequest',
    'ListFirewallPoliciesRequest',
    'ListFirewallsRequest',
    'ListForwardingRulesRequest',
    'ListGlobalAddressesRequest',
    'ListGlobalForwardingRulesRequest',
    'ListGlobalNetworkEndpointGroupsRequest',
    'ListGlobalOperationsRequest',
    'ListGlobalOrganizationOperationsRequest',
    'ListGlobalPublicDelegatedPrefixesRequest',
    'ListHealthChecksRequest',
    'ListImagesRequest',
    'ListInstanceGroupManagerResizeRequestsRequest',
    'ListInstanceGroupManagersRequest',
    'ListInstanceGroupsRequest',
    'ListInstancesInstanceGroupsRequest',
    'ListInstancesRegionInstanceGroupsRequest',
    'ListInstancesRequest',
    'ListInstanceTemplatesRequest',
    'ListInstantSnapshotsRequest',
    'ListInterconnectAttachmentsRequest',
    'ListInterconnectLocationsRequest',
    'ListInterconnectRemoteLocationsRequest',
    'ListInterconnectsRequest',
    'ListLicensesRequest',
    'ListMachineImagesRequest',
    'ListMachineTypesRequest',
    'ListManagedInstancesInstanceGroupManagersRequest',
    'ListManagedInstancesRegionInstanceGroupManagersRequest',
    'ListNetworkAttachmentsRequest',
    'ListNetworkEndpointGroupsRequest',
    'ListNetworkEndpointsGlobalNetworkEndpointGroupsRequest',
    'ListNetworkEndpointsNetworkEndpointGroupsRequest',
    'ListNetworkEndpointsRegionNetworkEndpointGroupsRequest',
    'ListNetworkFirewallPoliciesRequest',
    'ListNetworksRequest',
    'ListNodeGroupsRequest',
    'ListNodesNodeGroupsRequest',
    'ListNodeTemplatesRequest',
    'ListNodeTypesRequest',
    'ListPacketMirroringsRequest',
    'ListPeeringRoutesNetworksRequest',
    'ListPerInstanceConfigsInstanceGroupManagersRequest',
    'ListPerInstanceConfigsRegionInstanceGroupManagersRequest',
    'ListPreconfiguredExpressionSetsSecurityPoliciesRequest',
    'ListPublicAdvertisedPrefixesRequest',
    'ListPublicDelegatedPrefixesRequest',
    'ListReferrersInstancesRequest',
    'ListRegionAutoscalersRequest',
    'ListRegionBackendServicesRequest',
    'ListRegionCommitmentsRequest',
    'ListRegionDisksRequest',
    'ListRegionDiskTypesRequest',
    'ListRegionHealthCheckServicesRequest',
    'ListRegionHealthChecksRequest',
    'ListRegionInstanceGroupManagersRequest',
    'ListRegionInstanceGroupsRequest',
    'ListRegionInstanceTemplatesRequest',
    'ListRegionInstantSnapshotsRequest',
    'ListRegionNetworkEndpointGroupsRequest',
    'ListRegionNetworkFirewallPoliciesRequest',
    'ListRegionNotificationEndpointsRequest',
    'ListRegionOperationsRequest',
    'ListRegionSecurityPoliciesRequest',
    'ListRegionsRequest',
    'ListRegionSslCertificatesRequest',
    'ListRegionSslPoliciesRequest',
    'ListRegionTargetHttpProxiesRequest',
    'ListRegionTargetHttpsProxiesRequest',
    'ListRegionTargetTcpProxiesRequest',
    'ListRegionUrlMapsRequest',
    'ListRegionZonesRequest',
    'ListReservationsRequest',
    'ListResourcePoliciesRequest',
    'ListRoutersRequest',
    'ListRoutesRequest',
    'ListSecurityPoliciesRequest',
    'ListServiceAttachmentsRequest',
    'ListSnapshotsRequest',
    'ListSslCertificatesRequest',
    'ListSslPoliciesRequest',
    'ListStoragePoolsRequest',
    'ListStoragePoolTypesRequest',
    'ListSubnetworksRequest',
    'ListTargetGrpcProxiesRequest',
    'ListTargetHttpProxiesRequest',
    'ListTargetHttpsProxiesRequest',
    'ListTargetInstancesRequest',
    'ListTargetPoolsRequest',
    'ListTargetSslProxiesRequest',
    'ListTargetTcpProxiesRequest',
    'ListTargetVpnGatewaysRequest',
    'ListUrlMapsRequest',
    'ListUsableBackendServicesRequest',
    'ListUsableRegionBackendServicesRequest',
    'ListUsableSubnetworksRequest',
    'ListVpnGatewaysRequest',
    'ListVpnTunnelsRequest',
    'ListXpnHostsProjectsRequest',
    'ListZoneOperationsRequest',
    'ListZonesRequest',
    'LocalDisk',
    'LocalizedMessage',
    'LocationPolicy',
    'LocationPolicyLocation',
    'LocationPolicyLocationConstraints',
    'LogConfig',
    'LogConfigCloudAuditOptions',
    'LogConfigCounterOptions',
    'LogConfigCounterOptionsCustomField',
    'LogConfigDataAccessOptions',
    'MachineImage',
    'MachineImageList',
    'MachineType',
    'MachineTypeAggregatedList',
    'MachineTypeList',
    'MachineTypesScopedList',
    'ManagedInstance',
    'ManagedInstanceInstanceHealth',
    'ManagedInstanceLastAttempt',
    'ManagedInstanceVersion',
    'Metadata',
    'MetadataFilter',
    'MetadataFilterLabelMatch',
    'MoveAddressRequest',
    'MoveDiskProjectRequest',
    'MoveFirewallPolicyRequest',
    'MoveGlobalAddressRequest',
    'MoveInstanceProjectRequest',
    'NamedPort',
    'NatIpInfo',
    'NatIpInfoNatIpInfoMapping',
    'NatIpInfoResponse',
    'Network',
    'NetworkAttachment',
    'NetworkAttachmentAggregatedList',
    'NetworkAttachmentConnectedEndpoint',
    'NetworkAttachmentList',
    'NetworkAttachmentsScopedList',
    'NetworkEdgeSecurityService',
    'NetworkEdgeSecurityServiceAggregatedList',
    'NetworkEdgeSecurityServicesScopedList',
    'NetworkEndpoint',
    'NetworkEndpointGroup',
    'NetworkEndpointGroupAggregatedList',
    'NetworkEndpointGroupAppEngine',
    'NetworkEndpointGroupCloudFunction',
    'NetworkEndpointGroupCloudRun',
    'NetworkEndpointGroupList',
    'NetworkEndpointGroupPscData',
    'NetworkEndpointGroupsAttachEndpointsRequest',
    'NetworkEndpointGroupsDetachEndpointsRequest',
    'NetworkEndpointGroupsListEndpointsRequest',
    'NetworkEndpointGroupsListNetworkEndpoints',
    'NetworkEndpointGroupsScopedList',
    'NetworkEndpointWithHealthStatus',
    'NetworkInterface',
    'NetworkList',
    'NetworkPeering',
    'NetworkPerformanceConfig',
    'NetworkRoutingConfig',
    'NetworksAddPeeringRequest',
    'NetworksGetEffectiveFirewallsResponse',
    'NetworksGetEffectiveFirewallsResponseEffectiveFirewallPolicy',
    'NetworksRemovePeeringRequest',
    'NetworksUpdatePeeringRequest',
    'NodeGroup',
    'NodeGroupAggregatedList',
    'NodeGroupAutoscalingPolicy',
    'NodeGroupList',
    'NodeGroupMaintenanceWindow',
    'NodeGroupNode',
    'NodeGroupsAddNodesRequest',
    'NodeGroupsDeleteNodesRequest',
    'NodeGroupsListNodes',
    'NodeGroupsPerformMaintenanceRequest',
    'NodeGroupsScopedList',
    'NodeGroupsSetNodeTemplateRequest',
    'NodeGroupsSimulateMaintenanceEventRequest',
    'NodeTemplate',
    'NodeTemplateAggregatedList',
    'NodeTemplateList',
    'NodeTemplateNodeTypeFlexibility',
    'NodeTemplatesScopedList',
    'NodeType',
    'NodeTypeAggregatedList',
    'NodeTypeList',
    'NodeTypesScopedList',
    'NotificationEndpoint',
    'NotificationEndpointGrpcSettings',
    'NotificationEndpointList',
    'Operation',
    'OperationAggregatedList',
    'OperationList',
    'OperationsScopedList',
    'OutlierDetection',
    'PacketIntervals',
    'PacketMirroring',
    'PacketMirroringAggregatedList',
    'PacketMirroringFilter',
    'PacketMirroringForwardingRuleInfo',
    'PacketMirroringList',
    'PacketMirroringMirroredResourceInfo',
    'PacketMirroringMirroredResourceInfoInstanceInfo',
    'PacketMirroringMirroredResourceInfoSubnetInfo',
    'PacketMirroringNetworkInfo',
    'PacketMirroringsScopedList',
    'PatchAutoscalerRequest',
    'PatchBackendBucketRequest',
    'PatchBackendServiceRequest',
    'PatchFirewallPolicyRequest',
    'PatchFirewallRequest',
    'PatchForwardingRuleRequest',
    'PatchGlobalForwardingRuleRequest',
    'PatchGlobalPublicDelegatedPrefixeRequest',
    'PatchHealthCheckRequest',
    'PatchImageRequest',
    'PatchInstanceGroupManagerRequest',
    'PatchInstanceSettingRequest',
    'PatchInterconnectAttachmentRequest',
    'PatchInterconnectRequest',
    'PatchNetworkAttachmentRequest',
    'PatchNetworkEdgeSecurityServiceRequest',
    'PatchNetworkFirewallPolicyRequest',
    'PatchNetworkRequest',
    'PatchNodeGroupRequest',
    'PatchPacketMirroringRequest',
    'PatchPerInstanceConfigsInstanceGroupManagerRequest',
    'PatchPerInstanceConfigsRegionInstanceGroupManagerRequest',
    'PatchPublicAdvertisedPrefixeRequest',
    'PatchPublicDelegatedPrefixeRequest',
    'PatchRegionAutoscalerRequest',
    'PatchRegionBackendServiceRequest',
    'PatchRegionHealthCheckRequest',
    'PatchRegionHealthCheckServiceRequest',
    'PatchRegionInstanceGroupManagerRequest',
    'PatchRegionNetworkFirewallPolicyRequest',
    'PatchRegionSecurityPolicyRequest',
    'PatchRegionSslPolicyRequest',
    'PatchRegionTargetHttpsProxyRequest',
    'PatchRegionUrlMapRequest',
    'PatchResourcePolicyRequest',
    'PatchRouterRequest',
    'PatchRuleFirewallPolicyRequest',
    'PatchRuleNetworkFirewallPolicyRequest',
    'PatchRuleRegionNetworkFirewallPolicyRequest',
    'PatchRuleRegionSecurityPolicyRequest',
    'PatchRuleSecurityPolicyRequest',
    'PatchSecurityPolicyRequest',
    'PatchServiceAttachmentRequest',
    'PatchSnapshotSettingRequest',
    'PatchSslPolicyRequest',
    'PatchSubnetworkRequest',
    'PatchTargetGrpcProxyRequest',
    'PatchTargetHttpProxyRequest',
    'PatchTargetHttpsProxyRequest',
    'PatchUrlMapRequest',
    'PathMatcher',
    'PathRule',
    'PerformMaintenanceInstanceRequest',
    'PerformMaintenanceNodeGroupRequest',
    'PerInstanceConfig',
    'Policy',
    'PreconfiguredWafSet',
    'PreservedState',
    'PreservedStatePreservedDisk',
    'PreservedStatePreservedNetworkIp',
    'PreservedStatePreservedNetworkIpIpAddress',
    'PreviewRouterRequest',
    'Project',
    'ProjectsDisableXpnResourceRequest',
    'ProjectsEnableXpnResourceRequest',
    'ProjectsGetXpnResources',
    'ProjectsListXpnHostsRequest',
    'ProjectsSetCloudArmorTierRequest',
    'ProjectsSetDefaultNetworkTierRequest',
    'PublicAdvertisedPrefix',
    'PublicAdvertisedPrefixList',
    'PublicAdvertisedPrefixPublicDelegatedPrefix',
    'PublicDelegatedPrefix',
    'PublicDelegatedPrefixAggregatedList',
    'PublicDelegatedPrefixesScopedList',
    'PublicDelegatedPrefixList',
    'PublicDelegatedPrefixPublicDelegatedSubPrefix',
    'Quota',
    'QuotaExceededInfo',
    'QuotaStatusWarning',
    'RawDisk',
    'RecreateInstancesInstanceGroupManagerRequest',
    'RecreateInstancesRegionInstanceGroupManagerRequest',
    'Reference',
    'Region',
    'RegionAddressesMoveRequest',
    'RegionAutoscalerList',
    'RegionDisksAddResourcePoliciesRequest',
    'RegionDisksRemoveResourcePoliciesRequest',
    'RegionDisksResizeRequest',
    'RegionDisksStartAsyncReplicationRequest',
    'RegionDiskTypeList',
    'RegionInstanceGroupList',
    'RegionInstanceGroupManagerDeleteInstanceConfigReq',
    'RegionInstanceGroupManagerList',
    'RegionInstanceGroupManagerPatchInstanceConfigReq',
    'RegionInstanceGroupManagersAbandonInstancesRequest',
    'RegionInstanceGroupManagersApplyUpdatesRequest',
    'RegionInstanceGroupManagersCreateInstancesRequest',
    'RegionInstanceGroupManagersDeleteInstancesRequest',
    'RegionInstanceGroupManagersListErrorsResponse',
    'RegionInstanceGroupManagersListInstanceConfigsResp',
    'RegionInstanceGroupManagersListInstancesResponse',
    'RegionInstanceGroupManagersRecreateRequest',
    'RegionInstanceGroupManagersSetTargetPoolsRequest',
    'RegionInstanceGroupManagersSetTemplateRequest',
    'RegionInstanceGroupManagerUpdateInstanceConfigReq',
    'RegionInstanceGroupsListInstances',
    'RegionInstanceGroupsListInstancesRequest',
    'RegionInstanceGroupsSetNamedPortsRequest',
    'RegionList',
    'RegionNetworkEndpointGroupsAttachEndpointsRequest',
    'RegionNetworkEndpointGroupsDetachEndpointsRequest',
    'RegionNetworkFirewallPoliciesGetEffectiveFirewallsResponse',
    'RegionNetworkFirewallPoliciesGetEffectiveFirewallsResponseEffectiveFirewallPolicy',
    'RegionSetLabelsRequest',
    'RegionSetPolicyRequest',
    'RegionTargetHttpsProxiesSetSslCertificatesRequest',
    'RegionUrlMapsValidateRequest',
    'RemoveAssociationFirewallPolicyRequest',
    'RemoveAssociationNetworkFirewallPolicyRequest',
    'RemoveAssociationRegionNetworkFirewallPolicyRequest',
    'RemoveHealthCheckTargetPoolRequest',
    'RemoveInstancesInstanceGroupRequest',
    'RemoveInstanceTargetPoolRequest',
    'RemovePeeringNetworkRequest',
    'RemoveResourcePoliciesDiskRequest',
    'RemoveResourcePoliciesInstanceRequest',
    'RemoveResourcePoliciesRegionDiskRequest',
    'RemoveRuleFirewallPolicyRequest',
    'RemoveRuleNetworkFirewallPolicyRequest',
    'RemoveRuleRegionNetworkFirewallPolicyRequest',
    'RemoveRuleRegionSecurityPolicyRequest',
    'RemoveRuleSecurityPolicyRequest',
    'RequestMirrorPolicy',
    'Reservation',
    'ReservationAffinity',
    'ReservationAggregatedList',
    'ReservationList',
    'ReservationsResizeRequest',
    'ReservationsScopedList',
    'ResetInstanceRequest',
    'ResizeDiskRequest',
    'ResizeInstanceGroupManagerRequest',
    'ResizeRegionDiskRequest',
    'ResizeRegionInstanceGroupManagerRequest',
    'ResizeReservationRequest',
    'ResourceCommitment',
    'ResourceGroupReference',
    'ResourcePoliciesScopedList',
    'ResourcePolicy',
    'ResourcePolicyAggregatedList',
    'ResourcePolicyDailyCycle',
    'ResourcePolicyDiskConsistencyGroupPolicy',
    'ResourcePolicyGroupPlacementPolicy',
    'ResourcePolicyHourlyCycle',
    'ResourcePolicyInstanceSchedulePolicy',
    'ResourcePolicyInstanceSchedulePolicySchedule',
    'ResourcePolicyList',
    'ResourcePolicyResourceStatus',
    'ResourcePolicyResourceStatusInstanceSchedulePolicyStatus',
    'ResourcePolicySnapshotSchedulePolicy',
    'ResourcePolicySnapshotSchedulePolicyRetentionPolicy',
    'ResourcePolicySnapshotSchedulePolicySchedule',
    'ResourcePolicySnapshotSchedulePolicySnapshotProperties',
    'ResourcePolicyWeeklyCycle',
    'ResourcePolicyWeeklyCycleDayOfWeek',
    'ResourceStatus',
    'ResumeInstanceRequest',
    'Route',
    'RouteAsPath',
    'RouteList',
    'Router',
    'RouterAdvertisedIpRange',
    'RouterAggregatedList',
    'RouterBgp',
    'RouterBgpPeer',
    'RouterBgpPeerBfd',
    'RouterBgpPeerCustomLearnedIpRange',
    'RouterInterface',
    'RouterList',
    'RouterMd5AuthenticationKey',
    'RouterNat',
    'RouterNatLogConfig',
    'RouterNatRule',
    'RouterNatRuleAction',
    'RouterNatSubnetworkToNat',
    'RoutersPreviewResponse',
    'RoutersScopedList',
    'RouterStatus',
    'RouterStatusBgpPeerStatus',
    'RouterStatusNatStatus',
    'RouterStatusNatStatusNatRuleStatus',
    'RouterStatusResponse',
    'Rule',
    'SavedAttachedDisk',
    'SavedDisk',
    'ScalingScheduleStatus',
    'Scheduling',
    'SchedulingNodeAffinity',
    'ScratchDisks',
    'Screenshot',
    'SecurityPoliciesAggregatedList',
    'SecurityPoliciesListPreconfiguredExpressionSetsResponse',
    'SecurityPoliciesScopedList',
    'SecurityPoliciesWafConfig',
    'SecurityPolicy',
    'SecurityPolicyAdaptiveProtectionConfig',
    'SecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig',
    'SecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfig',
    'SecurityPolicyAdvancedOptionsConfig',
    'SecurityPolicyAdvancedOptionsConfigJsonCustomConfig',
    'SecurityPolicyDdosProtectionConfig',
    'SecurityPolicyList',
    'SecurityPolicyRecaptchaOptionsConfig',
    'SecurityPolicyReference',
    'SecurityPolicyRule',
    'SecurityPolicyRuleHttpHeaderAction',
    'SecurityPolicyRuleHttpHeaderActionHttpHeaderOption',
    'SecurityPolicyRuleMatcher',
    'SecurityPolicyRuleMatcherConfig',
    'SecurityPolicyRuleMatcherExprOptions',
    'SecurityPolicyRuleMatcherExprOptionsRecaptchaOptions',
    'SecurityPolicyRuleNetworkMatcher',
    'SecurityPolicyRuleNetworkMatcherUserDefinedFieldMatch',
    'SecurityPolicyRulePreconfiguredWafConfig',
    'SecurityPolicyRulePreconfiguredWafConfigExclusion',
    'SecurityPolicyRulePreconfiguredWafConfigExclusionFieldParams',
    'SecurityPolicyRuleRateLimitOptions',
    'SecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfig',
    'SecurityPolicyRuleRateLimitOptionsThreshold',
    'SecurityPolicyRuleRedirectOptions',
    'SecurityPolicyUserDefinedField',
    'SecuritySettings',
    'SendDiagnosticInterruptInstanceRequest',
    'SendDiagnosticInterruptInstanceResponse',
    'SerialPortOutput',
    'ServerBinding',
    'ServiceAccount',
    'ServiceAttachment',
    'ServiceAttachmentAggregatedList',
    'ServiceAttachmentConnectedEndpoint',
    'ServiceAttachmentConsumerProjectLimit',
    'ServiceAttachmentList',
    'ServiceAttachmentsScopedList',
    'SetBackendServiceTargetSslProxyRequest',
    'SetBackendServiceTargetTcpProxyRequest',
    'SetBackupTargetPoolRequest',
    'SetCertificateMapTargetHttpsProxyRequest',
    'SetCertificateMapTargetSslProxyRequest',
    'SetCloudArmorTierProjectRequest',
    'SetCommonInstanceMetadataOperationMetadata',
    'SetCommonInstanceMetadataOperationMetadataPerLocationOperationInfo',
    'SetCommonInstanceMetadataProjectRequest',
    'SetDefaultNetworkTierProjectRequest',
    'SetDeletionProtectionInstanceRequest',
    'SetDiskAutoDeleteInstanceRequest',
    'SetEdgeSecurityPolicyBackendBucketRequest',
    'SetEdgeSecurityPolicyBackendServiceRequest',
    'SetIamPolicyBackendBucketRequest',
    'SetIamPolicyBackendServiceRequest',
    'SetIamPolicyDiskRequest',
    'SetIamPolicyFirewallPolicyRequest',
    'SetIamPolicyImageRequest',
    'SetIamPolicyInstanceRequest',
    'SetIamPolicyInstanceTemplateRequest',
    'SetIamPolicyInstantSnapshotRequest',
    'SetIamPolicyLicenseRequest',
    'SetIamPolicyMachineImageRequest',
    'SetIamPolicyNetworkAttachmentRequest',
    'SetIamPolicyNetworkFirewallPolicyRequest',
    'SetIamPolicyNodeGroupRequest',
    'SetIamPolicyNodeTemplateRequest',
    'SetIamPolicyRegionBackendServiceRequest',
    'SetIamPolicyRegionDiskRequest',
    'SetIamPolicyRegionInstantSnapshotRequest',
    'SetIamPolicyRegionNetworkFirewallPolicyRequest',
    'SetIamPolicyReservationRequest',
    'SetIamPolicyResourcePolicyRequest',
    'SetIamPolicyServiceAttachmentRequest',
    'SetIamPolicySnapshotRequest',
    'SetIamPolicyStoragePoolRequest',
    'SetIamPolicySubnetworkRequest',
    'SetInstanceTemplateInstanceGroupManagerRequest',
    'SetInstanceTemplateRegionInstanceGroupManagerRequest',
    'SetLabelsAddressRequest',
    'SetLabelsDiskRequest',
    'SetLabelsExternalVpnGatewayRequest',
    'SetLabelsForwardingRuleRequest',
    'SetLabelsGlobalAddressRequest',
    'SetLabelsGlobalForwardingRuleRequest',
    'SetLabelsImageRequest',
    'SetLabelsInstanceRequest',
    'SetLabelsInstantSnapshotRequest',
    'SetLabelsInterconnectAttachmentRequest',
    'SetLabelsInterconnectRequest',
    'SetLabelsRegionDiskRequest',
    'SetLabelsRegionInstantSnapshotRequest',
    'SetLabelsSecurityPolicyRequest',
    'SetLabelsSnapshotRequest',
    'SetLabelsTargetVpnGatewayRequest',
    'SetLabelsVpnGatewayRequest',
    'SetLabelsVpnTunnelRequest',
    'SetMachineResourcesInstanceRequest',
    'SetMachineTypeInstanceRequest',
    'SetMetadataInstanceRequest',
    'SetMinCpuPlatformInstanceRequest',
    'SetNamedPortsInstanceGroupRequest',
    'SetNamedPortsRegionInstanceGroupRequest',
    'SetNameInstanceRequest',
    'SetNodeTemplateNodeGroupRequest',
    'SetPrivateIpGoogleAccessSubnetworkRequest',
    'SetProxyHeaderTargetSslProxyRequest',
    'SetProxyHeaderTargetTcpProxyRequest',
    'SetQuicOverrideTargetHttpsProxyRequest',
    'SetSchedulingInstanceRequest',
    'SetSecurityPolicyBackendServiceRequest',
    'SetSecurityPolicyInstanceRequest',
    'SetSecurityPolicyRegionBackendServiceRequest',
    'SetSecurityPolicyTargetInstanceRequest',
    'SetSecurityPolicyTargetPoolRequest',
    'SetServiceAccountInstanceRequest',
    'SetShieldedInstanceIntegrityPolicyInstanceRequest',
    'SetSslCertificatesRegionTargetHttpsProxyRequest',
    'SetSslCertificatesTargetHttpsProxyRequest',
    'SetSslCertificatesTargetSslProxyRequest',
    'SetSslPolicyTargetHttpsProxyRequest',
    'SetSslPolicyTargetSslProxyRequest',
    'SetTagsInstanceRequest',
    'SetTargetForwardingRuleRequest',
    'SetTargetGlobalForwardingRuleRequest',
    'SetTargetPoolsInstanceGroupManagerRequest',
    'SetTargetPoolsRegionInstanceGroupManagerRequest',
    'SetUrlMapRegionTargetHttpProxyRequest',
    'SetUrlMapRegionTargetHttpsProxyRequest',
    'SetUrlMapTargetHttpProxyRequest',
    'SetUrlMapTargetHttpsProxyRequest',
    'SetUsageExportBucketProjectRequest',
    'ShareSettings',
    'ShareSettingsProjectConfig',
    'ShieldedInstanceConfig',
    'ShieldedInstanceIdentity',
    'ShieldedInstanceIdentityEntry',
    'ShieldedInstanceIntegrityPolicy',
    'SignedUrlKey',
    'SimulateMaintenanceEventInstanceRequest',
    'SimulateMaintenanceEventNodeGroupRequest',
    'Snapshot',
    'SnapshotList',
    'SnapshotSettings',
    'SnapshotSettingsStorageLocationSettings',
    'SnapshotSettingsStorageLocationSettingsStorageLocationPreference',
    'SourceDiskEncryptionKey',
    'SourceInstanceParams',
    'SourceInstanceProperties',
    'SslCertificate',
    'SslCertificateAggregatedList',
    'SslCertificateList',
    'SslCertificateManagedSslCertificate',
    'SslCertificateSelfManagedSslCertificate',
    'SslCertificatesScopedList',
    'SSLHealthCheck',
    'SslPoliciesAggregatedList',
    'SslPoliciesList',
    'SslPoliciesListAvailableFeaturesResponse',
    'SslPoliciesScopedList',
    'SslPolicy',
    'SslPolicyReference',
    'StartAsyncReplicationDiskRequest',
    'StartAsyncReplicationRegionDiskRequest',
    'StartInstanceRequest',
    'StartWithEncryptionKeyInstanceRequest',
    'StatefulPolicy',
    'StatefulPolicyPreservedState',
    'StatefulPolicyPreservedStateDiskDevice',
    'StatefulPolicyPreservedStateNetworkIp',
    'Status',
    'StopAsyncReplicationDiskRequest',
    'StopAsyncReplicationRegionDiskRequest',
    'StopGroupAsyncReplicationDiskRequest',
    'StopGroupAsyncReplicationRegionDiskRequest',
    'StopInstanceRequest',
    'StoragePool',
    'StoragePoolAggregatedList',
    'StoragePoolDisk',
    'StoragePoolList',
    'StoragePoolListDisks',
    'StoragePoolResourceStatus',
    'StoragePoolsScopedList',
    'StoragePoolType',
    'StoragePoolTypeAggregatedList',
    'StoragePoolTypeList',
    'StoragePoolTypesScopedList',
    'Subnetwork',
    'SubnetworkAggregatedList',
    'SubnetworkList',
    'SubnetworkLogConfig',
    'SubnetworkSecondaryRange',
    'SubnetworksExpandIpCidrRangeRequest',
    'SubnetworksScopedList',
    'SubnetworksSetPrivateIpGoogleAccessRequest',
    'Subsetting',
    'SuspendInstanceRequest',
    'SwitchToCustomModeNetworkRequest',
    'Tags',
    'TargetGrpcProxy',
    'TargetGrpcProxyList',
    'TargetHttpProxiesScopedList',
    'TargetHttpProxy',
    'TargetHttpProxyAggregatedList',
    'TargetHttpProxyList',
    'TargetHttpsProxiesScopedList',
    'TargetHttpsProxiesSetCertificateMapRequest',
    'TargetHttpsProxiesSetQuicOverrideRequest',
    'TargetHttpsProxiesSetSslCertificatesRequest',
    'TargetHttpsProxy',
    'TargetHttpsProxyAggregatedList',
    'TargetHttpsProxyList',
    'TargetInstance',
    'TargetInstanceAggregatedList',
    'TargetInstanceList',
    'TargetInstancesScopedList',
    'TargetPool',
    'TargetPoolAggregatedList',
    'TargetPoolInstanceHealth',
    'TargetPoolList',
    'TargetPoolsAddHealthCheckRequest',
    'TargetPoolsAddInstanceRequest',
    'TargetPoolsRemoveHealthCheckRequest',
    'TargetPoolsRemoveInstanceRequest',
    'TargetPoolsScopedList',
    'TargetReference',
    'TargetSslProxiesSetBackendServiceRequest',
    'TargetSslProxiesSetCertificateMapRequest',
    'TargetSslProxiesSetProxyHeaderRequest',
    'TargetSslProxiesSetSslCertificatesRequest',
    'TargetSslProxy',
    'TargetSslProxyList',
    'TargetTcpProxiesScopedList',
    'TargetTcpProxiesSetBackendServiceRequest',
    'TargetTcpProxiesSetProxyHeaderRequest',
    'TargetTcpProxy',
    'TargetTcpProxyAggregatedList',
    'TargetTcpProxyList',
    'TargetVpnGateway',
    'TargetVpnGatewayAggregatedList',
    'TargetVpnGatewayList',
    'TargetVpnGatewaysScopedList',
    'TCPHealthCheck',
    'TestFailure',
    'TestIamPermissionsBackendBucketRequest',
    'TestIamPermissionsBackendServiceRequest',
    'TestIamPermissionsDiskRequest',
    'TestIamPermissionsExternalVpnGatewayRequest',
    'TestIamPermissionsFirewallPolicyRequest',
    'TestIamPermissionsImageRequest',
    'TestIamPermissionsInstanceRequest',
    'TestIamPermissionsInstanceTemplateRequest',
    'TestIamPermissionsInstantSnapshotRequest',
    'TestIamPermissionsLicenseCodeRequest',
    'TestIamPermissionsLicenseRequest',
    'TestIamPermissionsMachineImageRequest',
    'TestIamPermissionsNetworkAttachmentRequest',
    'TestIamPermissionsNetworkEndpointGroupRequest',
    'TestIamPermissionsNetworkFirewallPolicyRequest',
    'TestIamPermissionsNodeGroupRequest',
    'TestIamPermissionsNodeTemplateRequest',
    'TestIamPermissionsPacketMirroringRequest',
    'TestIamPermissionsRegionBackendServiceRequest',
    'TestIamPermissionsRegionDiskRequest',
    'TestIamPermissionsRegionInstantSnapshotRequest',
    'TestIamPermissionsRegionNetworkFirewallPolicyRequest',
    'TestIamPermissionsReservationRequest',
    'TestIamPermissionsResourcePolicyRequest',
    'TestIamPermissionsServiceAttachmentRequest',
    'TestIamPermissionsSnapshotRequest',
    'TestIamPermissionsStoragePoolRequest',
    'TestIamPermissionsSubnetworkRequest',
    'TestIamPermissionsVpnGatewayRequest',
    'TestPermissionsRequest',
    'TestPermissionsResponse',
    'Uint128',
    'UpcomingMaintenance',
    'UpdateAccessConfigInstanceRequest',
    'UpdateAutoscalerRequest',
    'UpdateBackendBucketRequest',
    'UpdateBackendServiceRequest',
    'UpdateDiskRequest',
    'UpdateDisplayDeviceInstanceRequest',
    'UpdateFirewallRequest',
    'UpdateHealthCheckRequest',
    'UpdateInstanceRequest',
    'UpdateNetworkInterfaceInstanceRequest',
    'UpdatePeeringNetworkRequest',
    'UpdatePerInstanceConfigsInstanceGroupManagerRequest',
    'UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest',
    'UpdateRegionAutoscalerRequest',
    'UpdateRegionBackendServiceRequest',
    'UpdateRegionCommitmentRequest',
    'UpdateRegionDiskRequest',
    'UpdateRegionHealthCheckRequest',
    'UpdateRegionUrlMapRequest',
    'UpdateReservationRequest',
    'UpdateRouterRequest',
    'UpdateShieldedInstanceConfigInstanceRequest',
    'UpdateStoragePoolRequest',
    'UpdateUrlMapRequest',
    'UrlMap',
    'UrlMapList',
    'UrlMapReference',
    'UrlMapsAggregatedList',
    'UrlMapsScopedList',
    'UrlMapsValidateRequest',
    'UrlMapsValidateResponse',
    'UrlMapTest',
    'UrlMapTestHeader',
    'UrlMapValidationResult',
    'UrlRewrite',
    'UsableSubnetwork',
    'UsableSubnetworksAggregatedList',
    'UsableSubnetworkSecondaryRange',
    'UsageExportLocation',
    'ValidateRegionUrlMapRequest',
    'ValidateUrlMapRequest',
    'VmEndpointNatMappings',
    'VmEndpointNatMappingsInterfaceNatMappings',
    'VmEndpointNatMappingsInterfaceNatMappingsNatRuleMappings',
    'VmEndpointNatMappingsList',
    'VpnGateway',
    'VpnGatewayAggregatedList',
    'VpnGatewayList',
    'VpnGatewaysGetStatusResponse',
    'VpnGatewaysScopedList',
    'VpnGatewayStatus',
    'VpnGatewayStatusHighAvailabilityRequirementState',
    'VpnGatewayStatusTunnel',
    'VpnGatewayStatusVpnConnection',
    'VpnGatewayVpnGatewayInterface',
    'VpnTunnel',
    'VpnTunnelAggregatedList',
    'VpnTunnelList',
    'VpnTunnelsScopedList',
    'WafExpressionSet',
    'WafExpressionSetExpression',
    'WaitGlobalOperationRequest',
    'WaitRegionOperationRequest',
    'WaitZoneOperationRequest',
    'Warning',
    'Warnings',
    'WeightedBackendService',
    'WithdrawPublicAdvertisedPrefixeRequest',
    'WithdrawPublicDelegatedPrefixeRequest',
    'XpnHostList',
    'XpnResourceId',
    'Zone',
    'ZoneList',
    'ZoneSetLabelsRequest',
    'ZoneSetPolicyRequest',
)
