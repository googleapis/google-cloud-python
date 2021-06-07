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

from google.cloud.compute_v1.services.accelerator_types.client import (
    AcceleratorTypesClient,
)
from google.cloud.compute_v1.services.addresses.client import AddressesClient
from google.cloud.compute_v1.services.autoscalers.client import AutoscalersClient
from google.cloud.compute_v1.services.backend_buckets.client import BackendBucketsClient
from google.cloud.compute_v1.services.backend_services.client import (
    BackendServicesClient,
)
from google.cloud.compute_v1.services.disks.client import DisksClient
from google.cloud.compute_v1.services.disk_types.client import DiskTypesClient
from google.cloud.compute_v1.services.external_vpn_gateways.client import (
    ExternalVpnGatewaysClient,
)
from google.cloud.compute_v1.services.firewall_policies.client import (
    FirewallPoliciesClient,
)
from google.cloud.compute_v1.services.firewalls.client import FirewallsClient
from google.cloud.compute_v1.services.forwarding_rules.client import (
    ForwardingRulesClient,
)
from google.cloud.compute_v1.services.global_addresses.client import (
    GlobalAddressesClient,
)
from google.cloud.compute_v1.services.global_forwarding_rules.client import (
    GlobalForwardingRulesClient,
)
from google.cloud.compute_v1.services.global_network_endpoint_groups.client import (
    GlobalNetworkEndpointGroupsClient,
)
from google.cloud.compute_v1.services.global_operations.client import (
    GlobalOperationsClient,
)
from google.cloud.compute_v1.services.global_organization_operations.client import (
    GlobalOrganizationOperationsClient,
)
from google.cloud.compute_v1.services.global_public_delegated_prefixes.client import (
    GlobalPublicDelegatedPrefixesClient,
)
from google.cloud.compute_v1.services.health_checks.client import HealthChecksClient
from google.cloud.compute_v1.services.images.client import ImagesClient
from google.cloud.compute_v1.services.instance_group_managers.client import (
    InstanceGroupManagersClient,
)
from google.cloud.compute_v1.services.instance_groups.client import InstanceGroupsClient
from google.cloud.compute_v1.services.instances.client import InstancesClient
from google.cloud.compute_v1.services.instance_templates.client import (
    InstanceTemplatesClient,
)
from google.cloud.compute_v1.services.interconnect_attachments.client import (
    InterconnectAttachmentsClient,
)
from google.cloud.compute_v1.services.interconnect_locations.client import (
    InterconnectLocationsClient,
)
from google.cloud.compute_v1.services.interconnects.client import InterconnectsClient
from google.cloud.compute_v1.services.license_codes.client import LicenseCodesClient
from google.cloud.compute_v1.services.licenses.client import LicensesClient
from google.cloud.compute_v1.services.machine_types.client import MachineTypesClient
from google.cloud.compute_v1.services.network_endpoint_groups.client import (
    NetworkEndpointGroupsClient,
)
from google.cloud.compute_v1.services.networks.client import NetworksClient
from google.cloud.compute_v1.services.node_groups.client import NodeGroupsClient
from google.cloud.compute_v1.services.node_templates.client import NodeTemplatesClient
from google.cloud.compute_v1.services.node_types.client import NodeTypesClient
from google.cloud.compute_v1.services.packet_mirrorings.client import (
    PacketMirroringsClient,
)
from google.cloud.compute_v1.services.projects.client import ProjectsClient
from google.cloud.compute_v1.services.public_advertised_prefixes.client import (
    PublicAdvertisedPrefixesClient,
)
from google.cloud.compute_v1.services.public_delegated_prefixes.client import (
    PublicDelegatedPrefixesClient,
)
from google.cloud.compute_v1.services.region_autoscalers.client import (
    RegionAutoscalersClient,
)
from google.cloud.compute_v1.services.region_backend_services.client import (
    RegionBackendServicesClient,
)
from google.cloud.compute_v1.services.region_commitments.client import (
    RegionCommitmentsClient,
)
from google.cloud.compute_v1.services.region_disks.client import RegionDisksClient
from google.cloud.compute_v1.services.region_disk_types.client import (
    RegionDiskTypesClient,
)
from google.cloud.compute_v1.services.region_health_checks.client import (
    RegionHealthChecksClient,
)
from google.cloud.compute_v1.services.region_health_check_services.client import (
    RegionHealthCheckServicesClient,
)
from google.cloud.compute_v1.services.region_instance_group_managers.client import (
    RegionInstanceGroupManagersClient,
)
from google.cloud.compute_v1.services.region_instance_groups.client import (
    RegionInstanceGroupsClient,
)
from google.cloud.compute_v1.services.region_instances.client import (
    RegionInstancesClient,
)
from google.cloud.compute_v1.services.region_network_endpoint_groups.client import (
    RegionNetworkEndpointGroupsClient,
)
from google.cloud.compute_v1.services.region_notification_endpoints.client import (
    RegionNotificationEndpointsClient,
)
from google.cloud.compute_v1.services.region_operations.client import (
    RegionOperationsClient,
)
from google.cloud.compute_v1.services.regions.client import RegionsClient
from google.cloud.compute_v1.services.region_ssl_certificates.client import (
    RegionSslCertificatesClient,
)
from google.cloud.compute_v1.services.region_target_http_proxies.client import (
    RegionTargetHttpProxiesClient,
)
from google.cloud.compute_v1.services.region_target_https_proxies.client import (
    RegionTargetHttpsProxiesClient,
)
from google.cloud.compute_v1.services.region_url_maps.client import RegionUrlMapsClient
from google.cloud.compute_v1.services.reservations.client import ReservationsClient
from google.cloud.compute_v1.services.resource_policies.client import (
    ResourcePoliciesClient,
)
from google.cloud.compute_v1.services.routers.client import RoutersClient
from google.cloud.compute_v1.services.routes.client import RoutesClient
from google.cloud.compute_v1.services.security_policies.client import (
    SecurityPoliciesClient,
)
from google.cloud.compute_v1.services.snapshots.client import SnapshotsClient
from google.cloud.compute_v1.services.ssl_certificates.client import (
    SslCertificatesClient,
)
from google.cloud.compute_v1.services.ssl_policies.client import SslPoliciesClient
from google.cloud.compute_v1.services.subnetworks.client import SubnetworksClient
from google.cloud.compute_v1.services.target_grpc_proxies.client import (
    TargetGrpcProxiesClient,
)
from google.cloud.compute_v1.services.target_http_proxies.client import (
    TargetHttpProxiesClient,
)
from google.cloud.compute_v1.services.target_https_proxies.client import (
    TargetHttpsProxiesClient,
)
from google.cloud.compute_v1.services.target_instances.client import (
    TargetInstancesClient,
)
from google.cloud.compute_v1.services.target_pools.client import TargetPoolsClient
from google.cloud.compute_v1.services.target_ssl_proxies.client import (
    TargetSslProxiesClient,
)
from google.cloud.compute_v1.services.target_tcp_proxies.client import (
    TargetTcpProxiesClient,
)
from google.cloud.compute_v1.services.target_vpn_gateways.client import (
    TargetVpnGatewaysClient,
)
from google.cloud.compute_v1.services.url_maps.client import UrlMapsClient
from google.cloud.compute_v1.services.vpn_gateways.client import VpnGatewaysClient
from google.cloud.compute_v1.services.vpn_tunnels.client import VpnTunnelsClient
from google.cloud.compute_v1.services.zone_operations.client import ZoneOperationsClient
from google.cloud.compute_v1.services.zones.client import ZonesClient

from google.cloud.compute_v1.types.compute import (
    AbandonInstancesInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import (
    AbandonInstancesRegionInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import AcceleratorConfig
from google.cloud.compute_v1.types.compute import Accelerators
from google.cloud.compute_v1.types.compute import AcceleratorType
from google.cloud.compute_v1.types.compute import AcceleratorTypeAggregatedList
from google.cloud.compute_v1.types.compute import AcceleratorTypeList
from google.cloud.compute_v1.types.compute import AcceleratorTypesScopedList
from google.cloud.compute_v1.types.compute import AccessConfig
from google.cloud.compute_v1.types.compute import AddAccessConfigInstanceRequest
from google.cloud.compute_v1.types.compute import AddAssociationFirewallPolicyRequest
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
from google.cloud.compute_v1.types.compute import (
    AggregatedListInstanceGroupManagersRequest,
)
from google.cloud.compute_v1.types.compute import AggregatedListInstanceGroupsRequest
from google.cloud.compute_v1.types.compute import AggregatedListInstancesRequest
from google.cloud.compute_v1.types.compute import (
    AggregatedListInterconnectAttachmentsRequest,
)
from google.cloud.compute_v1.types.compute import AggregatedListMachineTypesRequest
from google.cloud.compute_v1.types.compute import (
    AggregatedListNetworkEndpointGroupsRequest,
)
from google.cloud.compute_v1.types.compute import AggregatedListNodeGroupsRequest
from google.cloud.compute_v1.types.compute import AggregatedListNodeTemplatesRequest
from google.cloud.compute_v1.types.compute import AggregatedListNodeTypesRequest
from google.cloud.compute_v1.types.compute import AggregatedListPacketMirroringsRequest
from google.cloud.compute_v1.types.compute import (
    AggregatedListPublicDelegatedPrefixesRequest,
)
from google.cloud.compute_v1.types.compute import AggregatedListRegionCommitmentsRequest
from google.cloud.compute_v1.types.compute import AggregatedListReservationsRequest
from google.cloud.compute_v1.types.compute import AggregatedListResourcePoliciesRequest
from google.cloud.compute_v1.types.compute import AggregatedListRoutersRequest
from google.cloud.compute_v1.types.compute import AggregatedListSslCertificatesRequest
from google.cloud.compute_v1.types.compute import AggregatedListSubnetworksRequest
from google.cloud.compute_v1.types.compute import AggregatedListTargetHttpProxiesRequest
from google.cloud.compute_v1.types.compute import (
    AggregatedListTargetHttpsProxiesRequest,
)
from google.cloud.compute_v1.types.compute import AggregatedListTargetInstancesRequest
from google.cloud.compute_v1.types.compute import AggregatedListTargetPoolsRequest
from google.cloud.compute_v1.types.compute import AggregatedListTargetVpnGatewaysRequest
from google.cloud.compute_v1.types.compute import AggregatedListUrlMapsRequest
from google.cloud.compute_v1.types.compute import AggregatedListVpnGatewaysRequest
from google.cloud.compute_v1.types.compute import AggregatedListVpnTunnelsRequest
from google.cloud.compute_v1.types.compute import AliasIpRange
from google.cloud.compute_v1.types.compute import (
    AllocationSpecificSKUAllocationAllocatedInstancePropertiesReservedDisk,
)
from google.cloud.compute_v1.types.compute import (
    AllocationSpecificSKUAllocationReservedInstanceProperties,
)
from google.cloud.compute_v1.types.compute import AllocationSpecificSKUReservation
from google.cloud.compute_v1.types.compute import Allowed
from google.cloud.compute_v1.types.compute import (
    ApplyUpdatesToInstancesInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import (
    ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import AttachDiskInstanceRequest
from google.cloud.compute_v1.types.compute import AttachedDisk
from google.cloud.compute_v1.types.compute import AttachedDiskInitializeParams
from google.cloud.compute_v1.types.compute import (
    AttachNetworkEndpointsGlobalNetworkEndpointGroupRequest,
)
from google.cloud.compute_v1.types.compute import (
    AttachNetworkEndpointsNetworkEndpointGroupRequest,
)
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
from google.cloud.compute_v1.types.compute import (
    AutoscalingPolicyCustomMetricUtilization,
)
from google.cloud.compute_v1.types.compute import (
    AutoscalingPolicyLoadBalancingUtilization,
)
from google.cloud.compute_v1.types.compute import AutoscalingPolicyScaleInControl
from google.cloud.compute_v1.types.compute import AutoscalingPolicyScalingSchedule
from google.cloud.compute_v1.types.compute import Backend
from google.cloud.compute_v1.types.compute import BackendBucket
from google.cloud.compute_v1.types.compute import BackendBucketCdnPolicy
from google.cloud.compute_v1.types.compute import (
    BackendBucketCdnPolicyBypassCacheOnRequestHeader,
)
from google.cloud.compute_v1.types.compute import (
    BackendBucketCdnPolicyNegativeCachingPolicy,
)
from google.cloud.compute_v1.types.compute import BackendBucketList
from google.cloud.compute_v1.types.compute import BackendService
from google.cloud.compute_v1.types.compute import BackendServiceAggregatedList
from google.cloud.compute_v1.types.compute import BackendServiceCdnPolicy
from google.cloud.compute_v1.types.compute import (
    BackendServiceCdnPolicyBypassCacheOnRequestHeader,
)
from google.cloud.compute_v1.types.compute import (
    BackendServiceCdnPolicyNegativeCachingPolicy,
)
from google.cloud.compute_v1.types.compute import BackendServiceFailoverPolicy
from google.cloud.compute_v1.types.compute import BackendServiceGroupHealth
from google.cloud.compute_v1.types.compute import BackendServiceIAP
from google.cloud.compute_v1.types.compute import BackendServiceList
from google.cloud.compute_v1.types.compute import BackendServiceLogConfig
from google.cloud.compute_v1.types.compute import BackendServiceReference
from google.cloud.compute_v1.types.compute import BackendServicesScopedList
from google.cloud.compute_v1.types.compute import Binding
from google.cloud.compute_v1.types.compute import BulkInsertInstanceRequest
from google.cloud.compute_v1.types.compute import BulkInsertInstanceResource
from google.cloud.compute_v1.types.compute import (
    BulkInsertInstanceResourcePerInstanceProperties,
)
from google.cloud.compute_v1.types.compute import BulkInsertRegionInstanceRequest
from google.cloud.compute_v1.types.compute import CacheInvalidationRule
from google.cloud.compute_v1.types.compute import CacheKeyPolicy
from google.cloud.compute_v1.types.compute import CircuitBreakers
from google.cloud.compute_v1.types.compute import CloneRulesFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import Commitment
from google.cloud.compute_v1.types.compute import CommitmentAggregatedList
from google.cloud.compute_v1.types.compute import CommitmentList
from google.cloud.compute_v1.types.compute import CommitmentsScopedList
from google.cloud.compute_v1.types.compute import Condition
from google.cloud.compute_v1.types.compute import ConfidentialInstanceConfig
from google.cloud.compute_v1.types.compute import ConnectionDraining
from google.cloud.compute_v1.types.compute import ConsistentHashLoadBalancerSettings
from google.cloud.compute_v1.types.compute import (
    ConsistentHashLoadBalancerSettingsHttpCookie,
)
from google.cloud.compute_v1.types.compute import CorsPolicy
from google.cloud.compute_v1.types.compute import (
    CreateInstancesInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import (
    CreateInstancesRegionInstanceGroupManagerRequest,
)
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
from google.cloud.compute_v1.types.compute import (
    DeleteGlobalNetworkEndpointGroupRequest,
)
from google.cloud.compute_v1.types.compute import DeleteGlobalOperationRequest
from google.cloud.compute_v1.types.compute import DeleteGlobalOperationResponse
from google.cloud.compute_v1.types.compute import (
    DeleteGlobalOrganizationOperationRequest,
)
from google.cloud.compute_v1.types.compute import (
    DeleteGlobalOrganizationOperationResponse,
)
from google.cloud.compute_v1.types.compute import (
    DeleteGlobalPublicDelegatedPrefixeRequest,
)
from google.cloud.compute_v1.types.compute import DeleteHealthCheckRequest
from google.cloud.compute_v1.types.compute import DeleteImageRequest
from google.cloud.compute_v1.types.compute import DeleteInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import DeleteInstanceGroupRequest
from google.cloud.compute_v1.types.compute import DeleteInstanceRequest
from google.cloud.compute_v1.types.compute import (
    DeleteInstancesInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import (
    DeleteInstancesRegionInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import DeleteInstanceTemplateRequest
from google.cloud.compute_v1.types.compute import DeleteInterconnectAttachmentRequest
from google.cloud.compute_v1.types.compute import DeleteInterconnectRequest
from google.cloud.compute_v1.types.compute import DeleteLicenseRequest
from google.cloud.compute_v1.types.compute import DeleteNetworkEndpointGroupRequest
from google.cloud.compute_v1.types.compute import DeleteNetworkRequest
from google.cloud.compute_v1.types.compute import DeleteNodeGroupRequest
from google.cloud.compute_v1.types.compute import DeleteNodesNodeGroupRequest
from google.cloud.compute_v1.types.compute import DeleteNodeTemplateRequest
from google.cloud.compute_v1.types.compute import DeletePacketMirroringRequest
from google.cloud.compute_v1.types.compute import (
    DeletePerInstanceConfigsInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import (
    DeletePerInstanceConfigsRegionInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import DeletePublicAdvertisedPrefixeRequest
from google.cloud.compute_v1.types.compute import DeletePublicDelegatedPrefixeRequest
from google.cloud.compute_v1.types.compute import DeleteRegionAutoscalerRequest
from google.cloud.compute_v1.types.compute import DeleteRegionBackendServiceRequest
from google.cloud.compute_v1.types.compute import DeleteRegionDiskRequest
from google.cloud.compute_v1.types.compute import DeleteRegionHealthCheckRequest
from google.cloud.compute_v1.types.compute import DeleteRegionHealthCheckServiceRequest
from google.cloud.compute_v1.types.compute import (
    DeleteRegionInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import (
    DeleteRegionNetworkEndpointGroupRequest,
)
from google.cloud.compute_v1.types.compute import (
    DeleteRegionNotificationEndpointRequest,
)
from google.cloud.compute_v1.types.compute import DeleteRegionOperationRequest
from google.cloud.compute_v1.types.compute import DeleteRegionOperationResponse
from google.cloud.compute_v1.types.compute import DeleteRegionSslCertificateRequest
from google.cloud.compute_v1.types.compute import DeleteRegionTargetHttpProxyRequest
from google.cloud.compute_v1.types.compute import DeleteRegionTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import DeleteRegionUrlMapRequest
from google.cloud.compute_v1.types.compute import DeleteReservationRequest
from google.cloud.compute_v1.types.compute import DeleteResourcePolicyRequest
from google.cloud.compute_v1.types.compute import DeleteRouteRequest
from google.cloud.compute_v1.types.compute import DeleteRouterRequest
from google.cloud.compute_v1.types.compute import DeleteSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import DeleteSignedUrlKeyBackendBucketRequest
from google.cloud.compute_v1.types.compute import (
    DeleteSignedUrlKeyBackendServiceRequest,
)
from google.cloud.compute_v1.types.compute import DeleteSnapshotRequest
from google.cloud.compute_v1.types.compute import DeleteSslCertificateRequest
from google.cloud.compute_v1.types.compute import DeleteSslPolicyRequest
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
from google.cloud.compute_v1.types.compute import (
    DetachNetworkEndpointsGlobalNetworkEndpointGroupRequest,
)
from google.cloud.compute_v1.types.compute import (
    DetachNetworkEndpointsNetworkEndpointGroupRequest,
)
from google.cloud.compute_v1.types.compute import DisableXpnHostProjectRequest
from google.cloud.compute_v1.types.compute import DisableXpnResourceProjectRequest
from google.cloud.compute_v1.types.compute import Disk
from google.cloud.compute_v1.types.compute import DiskAggregatedList
from google.cloud.compute_v1.types.compute import DiskInstantiationConfig
from google.cloud.compute_v1.types.compute import DiskList
from google.cloud.compute_v1.types.compute import DiskMoveRequest
from google.cloud.compute_v1.types.compute import DisksAddResourcePoliciesRequest
from google.cloud.compute_v1.types.compute import DisksRemoveResourcePoliciesRequest
from google.cloud.compute_v1.types.compute import DisksResizeRequest
from google.cloud.compute_v1.types.compute import DisksScopedList
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
from google.cloud.compute_v1.types.compute import (
    FirewallPoliciesListAssociationsResponse,
)
from google.cloud.compute_v1.types.compute import FirewallPolicy
from google.cloud.compute_v1.types.compute import FirewallPolicyAssociation
from google.cloud.compute_v1.types.compute import FirewallPolicyList
from google.cloud.compute_v1.types.compute import FirewallPolicyRule
from google.cloud.compute_v1.types.compute import FirewallPolicyRuleMatcher
from google.cloud.compute_v1.types.compute import FirewallPolicyRuleMatcherLayer4Config
from google.cloud.compute_v1.types.compute import FixedOrPercent
from google.cloud.compute_v1.types.compute import ForwardingRule
from google.cloud.compute_v1.types.compute import ForwardingRuleAggregatedList
from google.cloud.compute_v1.types.compute import ForwardingRuleList
from google.cloud.compute_v1.types.compute import ForwardingRuleReference
from google.cloud.compute_v1.types.compute import (
    ForwardingRuleServiceDirectoryRegistration,
)
from google.cloud.compute_v1.types.compute import ForwardingRulesScopedList
from google.cloud.compute_v1.types.compute import GetAcceleratorTypeRequest
from google.cloud.compute_v1.types.compute import GetAddressRequest
from google.cloud.compute_v1.types.compute import GetAssociationFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import GetAutoscalerRequest
from google.cloud.compute_v1.types.compute import GetBackendBucketRequest
from google.cloud.compute_v1.types.compute import GetBackendServiceRequest
from google.cloud.compute_v1.types.compute import GetDiagnosticsInterconnectRequest
from google.cloud.compute_v1.types.compute import GetDiskRequest
from google.cloud.compute_v1.types.compute import GetDiskTypeRequest
from google.cloud.compute_v1.types.compute import GetEffectiveFirewallsInstanceRequest
from google.cloud.compute_v1.types.compute import GetEffectiveFirewallsNetworkRequest
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
from google.cloud.compute_v1.types.compute import GetIamPolicyDiskRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyImageRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyInstanceRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyInstanceTemplateRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyLicenseRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyNodeGroupRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyNodeTemplateRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyRegionDiskRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyReservationRequest
from google.cloud.compute_v1.types.compute import GetIamPolicyResourcePolicyRequest
from google.cloud.compute_v1.types.compute import GetIamPolicySnapshotRequest
from google.cloud.compute_v1.types.compute import GetIamPolicySubnetworkRequest
from google.cloud.compute_v1.types.compute import GetImageRequest
from google.cloud.compute_v1.types.compute import GetInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import GetInstanceGroupRequest
from google.cloud.compute_v1.types.compute import GetInstanceRequest
from google.cloud.compute_v1.types.compute import GetInstanceTemplateRequest
from google.cloud.compute_v1.types.compute import GetInterconnectAttachmentRequest
from google.cloud.compute_v1.types.compute import GetInterconnectLocationRequest
from google.cloud.compute_v1.types.compute import GetInterconnectRequest
from google.cloud.compute_v1.types.compute import GetLicenseCodeRequest
from google.cloud.compute_v1.types.compute import GetLicenseRequest
from google.cloud.compute_v1.types.compute import GetMachineTypeRequest
from google.cloud.compute_v1.types.compute import GetNatMappingInfoRoutersRequest
from google.cloud.compute_v1.types.compute import GetNetworkEndpointGroupRequest
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
from google.cloud.compute_v1.types.compute import GetRegionNetworkEndpointGroupRequest
from google.cloud.compute_v1.types.compute import GetRegionNotificationEndpointRequest
from google.cloud.compute_v1.types.compute import GetRegionOperationRequest
from google.cloud.compute_v1.types.compute import GetRegionRequest
from google.cloud.compute_v1.types.compute import GetRegionSslCertificateRequest
from google.cloud.compute_v1.types.compute import GetRegionTargetHttpProxyRequest
from google.cloud.compute_v1.types.compute import GetRegionTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import GetRegionUrlMapRequest
from google.cloud.compute_v1.types.compute import GetReservationRequest
from google.cloud.compute_v1.types.compute import GetResourcePolicyRequest
from google.cloud.compute_v1.types.compute import GetRouteRequest
from google.cloud.compute_v1.types.compute import GetRouterRequest
from google.cloud.compute_v1.types.compute import GetRouterStatusRouterRequest
from google.cloud.compute_v1.types.compute import GetRuleFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import GetRuleSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import GetScreenshotInstanceRequest
from google.cloud.compute_v1.types.compute import GetSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import GetSerialPortOutputInstanceRequest
from google.cloud.compute_v1.types.compute import (
    GetShieldedInstanceIdentityInstanceRequest,
)
from google.cloud.compute_v1.types.compute import GetSnapshotRequest
from google.cloud.compute_v1.types.compute import GetSslCertificateRequest
from google.cloud.compute_v1.types.compute import GetSslPolicyRequest
from google.cloud.compute_v1.types.compute import GetStatusVpnGatewayRequest
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
from google.cloud.compute_v1.types.compute import (
    GlobalNetworkEndpointGroupsAttachEndpointsRequest,
)
from google.cloud.compute_v1.types.compute import (
    GlobalNetworkEndpointGroupsDetachEndpointsRequest,
)
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
from google.cloud.compute_v1.types.compute import (
    InsertGlobalNetworkEndpointGroupRequest,
)
from google.cloud.compute_v1.types.compute import (
    InsertGlobalPublicDelegatedPrefixeRequest,
)
from google.cloud.compute_v1.types.compute import InsertHealthCheckRequest
from google.cloud.compute_v1.types.compute import InsertImageRequest
from google.cloud.compute_v1.types.compute import InsertInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import InsertInstanceGroupRequest
from google.cloud.compute_v1.types.compute import InsertInstanceRequest
from google.cloud.compute_v1.types.compute import InsertInstanceTemplateRequest
from google.cloud.compute_v1.types.compute import InsertInterconnectAttachmentRequest
from google.cloud.compute_v1.types.compute import InsertInterconnectRequest
from google.cloud.compute_v1.types.compute import InsertLicenseRequest
from google.cloud.compute_v1.types.compute import InsertNetworkEndpointGroupRequest
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
from google.cloud.compute_v1.types.compute import (
    InsertRegionInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import (
    InsertRegionNetworkEndpointGroupRequest,
)
from google.cloud.compute_v1.types.compute import (
    InsertRegionNotificationEndpointRequest,
)
from google.cloud.compute_v1.types.compute import InsertRegionSslCertificateRequest
from google.cloud.compute_v1.types.compute import InsertRegionTargetHttpProxyRequest
from google.cloud.compute_v1.types.compute import InsertRegionTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import InsertRegionUrlMapRequest
from google.cloud.compute_v1.types.compute import InsertReservationRequest
from google.cloud.compute_v1.types.compute import InsertResourcePolicyRequest
from google.cloud.compute_v1.types.compute import InsertRouteRequest
from google.cloud.compute_v1.types.compute import InsertRouterRequest
from google.cloud.compute_v1.types.compute import InsertSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import InsertSslCertificateRequest
from google.cloud.compute_v1.types.compute import InsertSslPolicyRequest
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
from google.cloud.compute_v1.types.compute import InstanceGroup
from google.cloud.compute_v1.types.compute import InstanceGroupAggregatedList
from google.cloud.compute_v1.types.compute import InstanceGroupList
from google.cloud.compute_v1.types.compute import InstanceGroupManager
from google.cloud.compute_v1.types.compute import InstanceGroupManagerActionsSummary
from google.cloud.compute_v1.types.compute import InstanceGroupManagerAggregatedList
from google.cloud.compute_v1.types.compute import InstanceGroupManagerAutoHealingPolicy
from google.cloud.compute_v1.types.compute import InstanceGroupManagerList
from google.cloud.compute_v1.types.compute import (
    InstanceGroupManagersAbandonInstancesRequest,
)
from google.cloud.compute_v1.types.compute import (
    InstanceGroupManagersApplyUpdatesRequest,
)
from google.cloud.compute_v1.types.compute import (
    InstanceGroupManagersCreateInstancesRequest,
)
from google.cloud.compute_v1.types.compute import (
    InstanceGroupManagersDeleteInstancesRequest,
)
from google.cloud.compute_v1.types.compute import (
    InstanceGroupManagersDeletePerInstanceConfigsReq,
)
from google.cloud.compute_v1.types.compute import (
    InstanceGroupManagersListErrorsResponse,
)
from google.cloud.compute_v1.types.compute import (
    InstanceGroupManagersListManagedInstancesResponse,
)
from google.cloud.compute_v1.types.compute import (
    InstanceGroupManagersListPerInstanceConfigsResp,
)
from google.cloud.compute_v1.types.compute import (
    InstanceGroupManagersPatchPerInstanceConfigsReq,
)
from google.cloud.compute_v1.types.compute import (
    InstanceGroupManagersRecreateInstancesRequest,
)
from google.cloud.compute_v1.types.compute import InstanceGroupManagersScopedList
from google.cloud.compute_v1.types.compute import (
    InstanceGroupManagersSetInstanceTemplateRequest,
)
from google.cloud.compute_v1.types.compute import (
    InstanceGroupManagersSetTargetPoolsRequest,
)
from google.cloud.compute_v1.types.compute import InstanceGroupManagerStatus
from google.cloud.compute_v1.types.compute import InstanceGroupManagerStatusStateful
from google.cloud.compute_v1.types.compute import (
    InstanceGroupManagerStatusStatefulPerInstanceConfigs,
)
from google.cloud.compute_v1.types.compute import (
    InstanceGroupManagerStatusVersionTarget,
)
from google.cloud.compute_v1.types.compute import (
    InstanceGroupManagersUpdatePerInstanceConfigsReq,
)
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
from google.cloud.compute_v1.types.compute import (
    InstanceManagedByIgmErrorInstanceActionDetails,
)
from google.cloud.compute_v1.types.compute import (
    InstanceManagedByIgmErrorManagedInstanceError,
)
from google.cloud.compute_v1.types.compute import InstanceMoveRequest
from google.cloud.compute_v1.types.compute import InstanceProperties
from google.cloud.compute_v1.types.compute import InstanceReference
from google.cloud.compute_v1.types.compute import InstancesAddResourcePoliciesRequest
from google.cloud.compute_v1.types.compute import InstancesGetEffectiveFirewallsResponse
from google.cloud.compute_v1.types.compute import (
    InstancesGetEffectiveFirewallsResponseEffectiveFirewallPolicy,
)
from google.cloud.compute_v1.types.compute import InstancesRemoveResourcePoliciesRequest
from google.cloud.compute_v1.types.compute import InstancesScopedList
from google.cloud.compute_v1.types.compute import InstancesSetLabelsRequest
from google.cloud.compute_v1.types.compute import InstancesSetMachineResourcesRequest
from google.cloud.compute_v1.types.compute import InstancesSetMachineTypeRequest
from google.cloud.compute_v1.types.compute import InstancesSetMinCpuPlatformRequest
from google.cloud.compute_v1.types.compute import InstancesSetServiceAccountRequest
from google.cloud.compute_v1.types.compute import InstancesStartWithEncryptionKeyRequest
from google.cloud.compute_v1.types.compute import InstanceTemplate
from google.cloud.compute_v1.types.compute import InstanceTemplateList
from google.cloud.compute_v1.types.compute import InstanceWithNamedPorts
from google.cloud.compute_v1.types.compute import Int64RangeMatch
from google.cloud.compute_v1.types.compute import Interconnect
from google.cloud.compute_v1.types.compute import InterconnectAttachment
from google.cloud.compute_v1.types.compute import InterconnectAttachmentAggregatedList
from google.cloud.compute_v1.types.compute import InterconnectAttachmentList
from google.cloud.compute_v1.types.compute import InterconnectAttachmentPartnerMetadata
from google.cloud.compute_v1.types.compute import InterconnectAttachmentPrivateInfo
from google.cloud.compute_v1.types.compute import InterconnectAttachmentsScopedList
from google.cloud.compute_v1.types.compute import InterconnectCircuitInfo
from google.cloud.compute_v1.types.compute import InterconnectDiagnostics
from google.cloud.compute_v1.types.compute import InterconnectDiagnosticsARPEntry
from google.cloud.compute_v1.types.compute import InterconnectDiagnosticsLinkLACPStatus
from google.cloud.compute_v1.types.compute import (
    InterconnectDiagnosticsLinkOpticalPower,
)
from google.cloud.compute_v1.types.compute import InterconnectDiagnosticsLinkStatus
from google.cloud.compute_v1.types.compute import InterconnectList
from google.cloud.compute_v1.types.compute import InterconnectLocation
from google.cloud.compute_v1.types.compute import InterconnectLocationList
from google.cloud.compute_v1.types.compute import InterconnectLocationRegionInfo
from google.cloud.compute_v1.types.compute import InterconnectOutageNotification
from google.cloud.compute_v1.types.compute import InterconnectsGetDiagnosticsResponse
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
from google.cloud.compute_v1.types.compute import (
    ListAvailableFeaturesSslPoliciesRequest,
)
from google.cloud.compute_v1.types.compute import ListBackendBucketsRequest
from google.cloud.compute_v1.types.compute import ListBackendServicesRequest
from google.cloud.compute_v1.types.compute import ListDisksRequest
from google.cloud.compute_v1.types.compute import ListDiskTypesRequest
from google.cloud.compute_v1.types.compute import ListErrorsInstanceGroupManagersRequest
from google.cloud.compute_v1.types.compute import (
    ListErrorsRegionInstanceGroupManagersRequest,
)
from google.cloud.compute_v1.types.compute import ListExternalVpnGatewaysRequest
from google.cloud.compute_v1.types.compute import ListFirewallPoliciesRequest
from google.cloud.compute_v1.types.compute import ListFirewallsRequest
from google.cloud.compute_v1.types.compute import ListForwardingRulesRequest
from google.cloud.compute_v1.types.compute import ListGlobalAddressesRequest
from google.cloud.compute_v1.types.compute import ListGlobalForwardingRulesRequest
from google.cloud.compute_v1.types.compute import ListGlobalNetworkEndpointGroupsRequest
from google.cloud.compute_v1.types.compute import ListGlobalOperationsRequest
from google.cloud.compute_v1.types.compute import (
    ListGlobalOrganizationOperationsRequest,
)
from google.cloud.compute_v1.types.compute import (
    ListGlobalPublicDelegatedPrefixesRequest,
)
from google.cloud.compute_v1.types.compute import ListHealthChecksRequest
from google.cloud.compute_v1.types.compute import ListImagesRequest
from google.cloud.compute_v1.types.compute import ListInstanceGroupManagersRequest
from google.cloud.compute_v1.types.compute import ListInstanceGroupsRequest
from google.cloud.compute_v1.types.compute import ListInstancesInstanceGroupsRequest
from google.cloud.compute_v1.types.compute import (
    ListInstancesRegionInstanceGroupsRequest,
)
from google.cloud.compute_v1.types.compute import ListInstancesRequest
from google.cloud.compute_v1.types.compute import ListInstanceTemplatesRequest
from google.cloud.compute_v1.types.compute import ListInterconnectAttachmentsRequest
from google.cloud.compute_v1.types.compute import ListInterconnectLocationsRequest
from google.cloud.compute_v1.types.compute import ListInterconnectsRequest
from google.cloud.compute_v1.types.compute import ListLicensesRequest
from google.cloud.compute_v1.types.compute import ListMachineTypesRequest
from google.cloud.compute_v1.types.compute import (
    ListManagedInstancesInstanceGroupManagersRequest,
)
from google.cloud.compute_v1.types.compute import (
    ListManagedInstancesRegionInstanceGroupManagersRequest,
)
from google.cloud.compute_v1.types.compute import ListNetworkEndpointGroupsRequest
from google.cloud.compute_v1.types.compute import (
    ListNetworkEndpointsGlobalNetworkEndpointGroupsRequest,
)
from google.cloud.compute_v1.types.compute import (
    ListNetworkEndpointsNetworkEndpointGroupsRequest,
)
from google.cloud.compute_v1.types.compute import ListNetworksRequest
from google.cloud.compute_v1.types.compute import ListNodeGroupsRequest
from google.cloud.compute_v1.types.compute import ListNodesNodeGroupsRequest
from google.cloud.compute_v1.types.compute import ListNodeTemplatesRequest
from google.cloud.compute_v1.types.compute import ListNodeTypesRequest
from google.cloud.compute_v1.types.compute import ListPacketMirroringsRequest
from google.cloud.compute_v1.types.compute import ListPeeringRoutesNetworksRequest
from google.cloud.compute_v1.types.compute import (
    ListPerInstanceConfigsInstanceGroupManagersRequest,
)
from google.cloud.compute_v1.types.compute import (
    ListPerInstanceConfigsRegionInstanceGroupManagersRequest,
)
from google.cloud.compute_v1.types.compute import (
    ListPreconfiguredExpressionSetsSecurityPoliciesRequest,
)
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
from google.cloud.compute_v1.types.compute import ListRegionNetworkEndpointGroupsRequest
from google.cloud.compute_v1.types.compute import ListRegionNotificationEndpointsRequest
from google.cloud.compute_v1.types.compute import ListRegionOperationsRequest
from google.cloud.compute_v1.types.compute import ListRegionsRequest
from google.cloud.compute_v1.types.compute import ListRegionSslCertificatesRequest
from google.cloud.compute_v1.types.compute import ListRegionTargetHttpProxiesRequest
from google.cloud.compute_v1.types.compute import ListRegionTargetHttpsProxiesRequest
from google.cloud.compute_v1.types.compute import ListRegionUrlMapsRequest
from google.cloud.compute_v1.types.compute import ListReservationsRequest
from google.cloud.compute_v1.types.compute import ListResourcePoliciesRequest
from google.cloud.compute_v1.types.compute import ListRoutersRequest
from google.cloud.compute_v1.types.compute import ListRoutesRequest
from google.cloud.compute_v1.types.compute import ListSecurityPoliciesRequest
from google.cloud.compute_v1.types.compute import ListSnapshotsRequest
from google.cloud.compute_v1.types.compute import ListSslCertificatesRequest
from google.cloud.compute_v1.types.compute import ListSslPoliciesRequest
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
from google.cloud.compute_v1.types.compute import ListUsableSubnetworksRequest
from google.cloud.compute_v1.types.compute import ListVpnGatewaysRequest
from google.cloud.compute_v1.types.compute import ListVpnTunnelsRequest
from google.cloud.compute_v1.types.compute import ListXpnHostsProjectsRequest
from google.cloud.compute_v1.types.compute import ListZoneOperationsRequest
from google.cloud.compute_v1.types.compute import ListZonesRequest
from google.cloud.compute_v1.types.compute import LocalDisk
from google.cloud.compute_v1.types.compute import LocationPolicy
from google.cloud.compute_v1.types.compute import LocationPolicyLocation
from google.cloud.compute_v1.types.compute import LogConfig
from google.cloud.compute_v1.types.compute import LogConfigCloudAuditOptions
from google.cloud.compute_v1.types.compute import LogConfigCounterOptions
from google.cloud.compute_v1.types.compute import LogConfigCounterOptionsCustomField
from google.cloud.compute_v1.types.compute import LogConfigDataAccessOptions
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
from google.cloud.compute_v1.types.compute import MoveDiskProjectRequest
from google.cloud.compute_v1.types.compute import MoveFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import MoveInstanceProjectRequest
from google.cloud.compute_v1.types.compute import NamedPort
from google.cloud.compute_v1.types.compute import Network
from google.cloud.compute_v1.types.compute import NetworkEndpoint
from google.cloud.compute_v1.types.compute import NetworkEndpointGroup
from google.cloud.compute_v1.types.compute import NetworkEndpointGroupAggregatedList
from google.cloud.compute_v1.types.compute import NetworkEndpointGroupAppEngine
from google.cloud.compute_v1.types.compute import NetworkEndpointGroupCloudFunction
from google.cloud.compute_v1.types.compute import NetworkEndpointGroupCloudRun
from google.cloud.compute_v1.types.compute import NetworkEndpointGroupList
from google.cloud.compute_v1.types.compute import (
    NetworkEndpointGroupsAttachEndpointsRequest,
)
from google.cloud.compute_v1.types.compute import (
    NetworkEndpointGroupsDetachEndpointsRequest,
)
from google.cloud.compute_v1.types.compute import (
    NetworkEndpointGroupsListEndpointsRequest,
)
from google.cloud.compute_v1.types.compute import (
    NetworkEndpointGroupsListNetworkEndpoints,
)
from google.cloud.compute_v1.types.compute import NetworkEndpointGroupsScopedList
from google.cloud.compute_v1.types.compute import NetworkEndpointWithHealthStatus
from google.cloud.compute_v1.types.compute import NetworkInterface
from google.cloud.compute_v1.types.compute import NetworkList
from google.cloud.compute_v1.types.compute import NetworkPeering
from google.cloud.compute_v1.types.compute import NetworkRoutingConfig
from google.cloud.compute_v1.types.compute import NetworksAddPeeringRequest
from google.cloud.compute_v1.types.compute import NetworksGetEffectiveFirewallsResponse
from google.cloud.compute_v1.types.compute import (
    NetworksGetEffectiveFirewallsResponseEffectiveFirewallPolicy,
)
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
from google.cloud.compute_v1.types.compute import NodeGroupsScopedList
from google.cloud.compute_v1.types.compute import NodeGroupsSetNodeTemplateRequest
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
from google.cloud.compute_v1.types.compute import PacketMirroring
from google.cloud.compute_v1.types.compute import PacketMirroringAggregatedList
from google.cloud.compute_v1.types.compute import PacketMirroringFilter
from google.cloud.compute_v1.types.compute import PacketMirroringForwardingRuleInfo
from google.cloud.compute_v1.types.compute import PacketMirroringList
from google.cloud.compute_v1.types.compute import PacketMirroringMirroredResourceInfo
from google.cloud.compute_v1.types.compute import (
    PacketMirroringMirroredResourceInfoInstanceInfo,
)
from google.cloud.compute_v1.types.compute import (
    PacketMirroringMirroredResourceInfoSubnetInfo,
)
from google.cloud.compute_v1.types.compute import PacketMirroringNetworkInfo
from google.cloud.compute_v1.types.compute import PacketMirroringsScopedList
from google.cloud.compute_v1.types.compute import PatchAutoscalerRequest
from google.cloud.compute_v1.types.compute import PatchBackendBucketRequest
from google.cloud.compute_v1.types.compute import PatchBackendServiceRequest
from google.cloud.compute_v1.types.compute import PatchFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import PatchFirewallRequest
from google.cloud.compute_v1.types.compute import PatchForwardingRuleRequest
from google.cloud.compute_v1.types.compute import PatchGlobalForwardingRuleRequest
from google.cloud.compute_v1.types.compute import (
    PatchGlobalPublicDelegatedPrefixeRequest,
)
from google.cloud.compute_v1.types.compute import PatchHealthCheckRequest
from google.cloud.compute_v1.types.compute import PatchImageRequest
from google.cloud.compute_v1.types.compute import PatchInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import PatchInterconnectAttachmentRequest
from google.cloud.compute_v1.types.compute import PatchInterconnectRequest
from google.cloud.compute_v1.types.compute import PatchNetworkRequest
from google.cloud.compute_v1.types.compute import PatchNodeGroupRequest
from google.cloud.compute_v1.types.compute import PatchPacketMirroringRequest
from google.cloud.compute_v1.types.compute import (
    PatchPerInstanceConfigsInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import (
    PatchPerInstanceConfigsRegionInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import PatchPublicAdvertisedPrefixeRequest
from google.cloud.compute_v1.types.compute import PatchPublicDelegatedPrefixeRequest
from google.cloud.compute_v1.types.compute import PatchRegionAutoscalerRequest
from google.cloud.compute_v1.types.compute import PatchRegionBackendServiceRequest
from google.cloud.compute_v1.types.compute import PatchRegionHealthCheckRequest
from google.cloud.compute_v1.types.compute import PatchRegionHealthCheckServiceRequest
from google.cloud.compute_v1.types.compute import PatchRegionInstanceGroupManagerRequest
from google.cloud.compute_v1.types.compute import PatchRegionUrlMapRequest
from google.cloud.compute_v1.types.compute import PatchRouterRequest
from google.cloud.compute_v1.types.compute import PatchRuleFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import PatchRuleSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import PatchSecurityPolicyRequest
from google.cloud.compute_v1.types.compute import PatchSslPolicyRequest
from google.cloud.compute_v1.types.compute import PatchSubnetworkRequest
from google.cloud.compute_v1.types.compute import PatchTargetGrpcProxyRequest
from google.cloud.compute_v1.types.compute import PatchTargetHttpProxyRequest
from google.cloud.compute_v1.types.compute import PatchTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import PatchUrlMapRequest
from google.cloud.compute_v1.types.compute import PathMatcher
from google.cloud.compute_v1.types.compute import PathRule
from google.cloud.compute_v1.types.compute import PerInstanceConfig
from google.cloud.compute_v1.types.compute import Policy
from google.cloud.compute_v1.types.compute import PreconfiguredWafSet
from google.cloud.compute_v1.types.compute import PreservedState
from google.cloud.compute_v1.types.compute import PreservedStatePreservedDisk
from google.cloud.compute_v1.types.compute import PreviewRouterRequest
from google.cloud.compute_v1.types.compute import Project
from google.cloud.compute_v1.types.compute import ProjectsDisableXpnResourceRequest
from google.cloud.compute_v1.types.compute import ProjectsEnableXpnResourceRequest
from google.cloud.compute_v1.types.compute import ProjectsGetXpnResources
from google.cloud.compute_v1.types.compute import ProjectsListXpnHostsRequest
from google.cloud.compute_v1.types.compute import ProjectsSetDefaultNetworkTierRequest
from google.cloud.compute_v1.types.compute import PublicAdvertisedPrefix
from google.cloud.compute_v1.types.compute import PublicAdvertisedPrefixList
from google.cloud.compute_v1.types.compute import (
    PublicAdvertisedPrefixPublicDelegatedPrefix,
)
from google.cloud.compute_v1.types.compute import PublicDelegatedPrefix
from google.cloud.compute_v1.types.compute import PublicDelegatedPrefixAggregatedList
from google.cloud.compute_v1.types.compute import PublicDelegatedPrefixesScopedList
from google.cloud.compute_v1.types.compute import PublicDelegatedPrefixList
from google.cloud.compute_v1.types.compute import (
    PublicDelegatedPrefixPublicDelegatedSubPrefix,
)
from google.cloud.compute_v1.types.compute import Quota
from google.cloud.compute_v1.types.compute import RawDisk
from google.cloud.compute_v1.types.compute import (
    RecreateInstancesInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import (
    RecreateInstancesRegionInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import Reference
from google.cloud.compute_v1.types.compute import Region
from google.cloud.compute_v1.types.compute import RegionAutoscalerList
from google.cloud.compute_v1.types.compute import RegionDisksAddResourcePoliciesRequest
from google.cloud.compute_v1.types.compute import (
    RegionDisksRemoveResourcePoliciesRequest,
)
from google.cloud.compute_v1.types.compute import RegionDisksResizeRequest
from google.cloud.compute_v1.types.compute import RegionDiskTypeList
from google.cloud.compute_v1.types.compute import RegionInstanceGroupList
from google.cloud.compute_v1.types.compute import (
    RegionInstanceGroupManagerDeleteInstanceConfigReq,
)
from google.cloud.compute_v1.types.compute import RegionInstanceGroupManagerList
from google.cloud.compute_v1.types.compute import (
    RegionInstanceGroupManagerPatchInstanceConfigReq,
)
from google.cloud.compute_v1.types.compute import (
    RegionInstanceGroupManagersAbandonInstancesRequest,
)
from google.cloud.compute_v1.types.compute import (
    RegionInstanceGroupManagersApplyUpdatesRequest,
)
from google.cloud.compute_v1.types.compute import (
    RegionInstanceGroupManagersCreateInstancesRequest,
)
from google.cloud.compute_v1.types.compute import (
    RegionInstanceGroupManagersDeleteInstancesRequest,
)
from google.cloud.compute_v1.types.compute import (
    RegionInstanceGroupManagersListErrorsResponse,
)
from google.cloud.compute_v1.types.compute import (
    RegionInstanceGroupManagersListInstanceConfigsResp,
)
from google.cloud.compute_v1.types.compute import (
    RegionInstanceGroupManagersListInstancesResponse,
)
from google.cloud.compute_v1.types.compute import (
    RegionInstanceGroupManagersRecreateRequest,
)
from google.cloud.compute_v1.types.compute import (
    RegionInstanceGroupManagersSetTargetPoolsRequest,
)
from google.cloud.compute_v1.types.compute import (
    RegionInstanceGroupManagersSetTemplateRequest,
)
from google.cloud.compute_v1.types.compute import (
    RegionInstanceGroupManagerUpdateInstanceConfigReq,
)
from google.cloud.compute_v1.types.compute import RegionInstanceGroupsListInstances
from google.cloud.compute_v1.types.compute import (
    RegionInstanceGroupsListInstancesRequest,
)
from google.cloud.compute_v1.types.compute import (
    RegionInstanceGroupsSetNamedPortsRequest,
)
from google.cloud.compute_v1.types.compute import RegionList
from google.cloud.compute_v1.types.compute import RegionSetLabelsRequest
from google.cloud.compute_v1.types.compute import RegionSetPolicyRequest
from google.cloud.compute_v1.types.compute import (
    RegionTargetHttpsProxiesSetSslCertificatesRequest,
)
from google.cloud.compute_v1.types.compute import RegionUrlMapsValidateRequest
from google.cloud.compute_v1.types.compute import RemoveAssociationFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import RemoveHealthCheckTargetPoolRequest
from google.cloud.compute_v1.types.compute import RemoveInstancesInstanceGroupRequest
from google.cloud.compute_v1.types.compute import RemoveInstanceTargetPoolRequest
from google.cloud.compute_v1.types.compute import RemovePeeringNetworkRequest
from google.cloud.compute_v1.types.compute import RemoveResourcePoliciesDiskRequest
from google.cloud.compute_v1.types.compute import RemoveResourcePoliciesInstanceRequest
from google.cloud.compute_v1.types.compute import (
    RemoveResourcePoliciesRegionDiskRequest,
)
from google.cloud.compute_v1.types.compute import RemoveRuleFirewallPolicyRequest
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
from google.cloud.compute_v1.types.compute import (
    ResizeRegionInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import ResizeReservationRequest
from google.cloud.compute_v1.types.compute import ResourceCommitment
from google.cloud.compute_v1.types.compute import ResourceGroupReference
from google.cloud.compute_v1.types.compute import ResourcePoliciesScopedList
from google.cloud.compute_v1.types.compute import ResourcePolicy
from google.cloud.compute_v1.types.compute import ResourcePolicyAggregatedList
from google.cloud.compute_v1.types.compute import ResourcePolicyDailyCycle
from google.cloud.compute_v1.types.compute import ResourcePolicyGroupPlacementPolicy
from google.cloud.compute_v1.types.compute import ResourcePolicyHourlyCycle
from google.cloud.compute_v1.types.compute import ResourcePolicyInstanceSchedulePolicy
from google.cloud.compute_v1.types.compute import (
    ResourcePolicyInstanceSchedulePolicySchedule,
)
from google.cloud.compute_v1.types.compute import ResourcePolicyList
from google.cloud.compute_v1.types.compute import ResourcePolicyResourceStatus
from google.cloud.compute_v1.types.compute import (
    ResourcePolicyResourceStatusInstanceSchedulePolicyStatus,
)
from google.cloud.compute_v1.types.compute import ResourcePolicySnapshotSchedulePolicy
from google.cloud.compute_v1.types.compute import (
    ResourcePolicySnapshotSchedulePolicyRetentionPolicy,
)
from google.cloud.compute_v1.types.compute import (
    ResourcePolicySnapshotSchedulePolicySchedule,
)
from google.cloud.compute_v1.types.compute import (
    ResourcePolicySnapshotSchedulePolicySnapshotProperties,
)
from google.cloud.compute_v1.types.compute import ResourcePolicyWeeklyCycle
from google.cloud.compute_v1.types.compute import ResourcePolicyWeeklyCycleDayOfWeek
from google.cloud.compute_v1.types.compute import Route
from google.cloud.compute_v1.types.compute import RouteList
from google.cloud.compute_v1.types.compute import Router
from google.cloud.compute_v1.types.compute import RouterAdvertisedIpRange
from google.cloud.compute_v1.types.compute import RouterAggregatedList
from google.cloud.compute_v1.types.compute import RouterBgp
from google.cloud.compute_v1.types.compute import RouterBgpPeer
from google.cloud.compute_v1.types.compute import RouterInterface
from google.cloud.compute_v1.types.compute import RouterList
from google.cloud.compute_v1.types.compute import RouterNat
from google.cloud.compute_v1.types.compute import RouterNatLogConfig
from google.cloud.compute_v1.types.compute import RouterNatSubnetworkToNat
from google.cloud.compute_v1.types.compute import RoutersPreviewResponse
from google.cloud.compute_v1.types.compute import RoutersScopedList
from google.cloud.compute_v1.types.compute import RouterStatus
from google.cloud.compute_v1.types.compute import RouterStatusBgpPeerStatus
from google.cloud.compute_v1.types.compute import RouterStatusNatStatus
from google.cloud.compute_v1.types.compute import RouterStatusResponse
from google.cloud.compute_v1.types.compute import Rule
from google.cloud.compute_v1.types.compute import ScalingScheduleStatus
from google.cloud.compute_v1.types.compute import Scheduling
from google.cloud.compute_v1.types.compute import SchedulingNodeAffinity
from google.cloud.compute_v1.types.compute import ScratchDisks
from google.cloud.compute_v1.types.compute import Screenshot
from google.cloud.compute_v1.types.compute import (
    SecurityPoliciesListPreconfiguredExpressionSetsResponse,
)
from google.cloud.compute_v1.types.compute import SecurityPoliciesWafConfig
from google.cloud.compute_v1.types.compute import SecurityPolicy
from google.cloud.compute_v1.types.compute import SecurityPolicyList
from google.cloud.compute_v1.types.compute import SecurityPolicyReference
from google.cloud.compute_v1.types.compute import SecurityPolicyRule
from google.cloud.compute_v1.types.compute import SecurityPolicyRuleMatcher
from google.cloud.compute_v1.types.compute import SecurityPolicyRuleMatcherConfig
from google.cloud.compute_v1.types.compute import SecuritySettings
from google.cloud.compute_v1.types.compute import SerialPortOutput
from google.cloud.compute_v1.types.compute import ServerBinding
from google.cloud.compute_v1.types.compute import ServiceAccount
from google.cloud.compute_v1.types.compute import SetBackendServiceTargetSslProxyRequest
from google.cloud.compute_v1.types.compute import SetBackendServiceTargetTcpProxyRequest
from google.cloud.compute_v1.types.compute import SetBackupTargetPoolRequest
from google.cloud.compute_v1.types.compute import (
    SetCommonInstanceMetadataProjectRequest,
)
from google.cloud.compute_v1.types.compute import SetDefaultNetworkTierProjectRequest
from google.cloud.compute_v1.types.compute import SetDeletionProtectionInstanceRequest
from google.cloud.compute_v1.types.compute import SetDiskAutoDeleteInstanceRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyDiskRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyFirewallPolicyRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyImageRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyInstanceRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyInstanceTemplateRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyLicenseRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyNodeGroupRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyNodeTemplateRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyRegionDiskRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyReservationRequest
from google.cloud.compute_v1.types.compute import SetIamPolicyResourcePolicyRequest
from google.cloud.compute_v1.types.compute import SetIamPolicySnapshotRequest
from google.cloud.compute_v1.types.compute import SetIamPolicySubnetworkRequest
from google.cloud.compute_v1.types.compute import (
    SetInstanceTemplateInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import (
    SetInstanceTemplateRegionInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import SetLabelsDiskRequest
from google.cloud.compute_v1.types.compute import SetLabelsExternalVpnGatewayRequest
from google.cloud.compute_v1.types.compute import SetLabelsForwardingRuleRequest
from google.cloud.compute_v1.types.compute import SetLabelsGlobalForwardingRuleRequest
from google.cloud.compute_v1.types.compute import SetLabelsImageRequest
from google.cloud.compute_v1.types.compute import SetLabelsInstanceRequest
from google.cloud.compute_v1.types.compute import SetLabelsRegionDiskRequest
from google.cloud.compute_v1.types.compute import SetLabelsSnapshotRequest
from google.cloud.compute_v1.types.compute import SetLabelsVpnGatewayRequest
from google.cloud.compute_v1.types.compute import SetMachineResourcesInstanceRequest
from google.cloud.compute_v1.types.compute import SetMachineTypeInstanceRequest
from google.cloud.compute_v1.types.compute import SetMetadataInstanceRequest
from google.cloud.compute_v1.types.compute import SetMinCpuPlatformInstanceRequest
from google.cloud.compute_v1.types.compute import SetNamedPortsInstanceGroupRequest
from google.cloud.compute_v1.types.compute import (
    SetNamedPortsRegionInstanceGroupRequest,
)
from google.cloud.compute_v1.types.compute import SetNodeTemplateNodeGroupRequest
from google.cloud.compute_v1.types.compute import (
    SetPrivateIpGoogleAccessSubnetworkRequest,
)
from google.cloud.compute_v1.types.compute import SetProxyHeaderTargetSslProxyRequest
from google.cloud.compute_v1.types.compute import SetProxyHeaderTargetTcpProxyRequest
from google.cloud.compute_v1.types.compute import SetQuicOverrideTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import SetSchedulingInstanceRequest
from google.cloud.compute_v1.types.compute import SetSecurityPolicyBackendServiceRequest
from google.cloud.compute_v1.types.compute import SetServiceAccountInstanceRequest
from google.cloud.compute_v1.types.compute import (
    SetShieldedInstanceIntegrityPolicyInstanceRequest,
)
from google.cloud.compute_v1.types.compute import (
    SetSslCertificatesRegionTargetHttpsProxyRequest,
)
from google.cloud.compute_v1.types.compute import (
    SetSslCertificatesTargetHttpsProxyRequest,
)
from google.cloud.compute_v1.types.compute import (
    SetSslCertificatesTargetSslProxyRequest,
)
from google.cloud.compute_v1.types.compute import SetSslPolicyTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import SetSslPolicyTargetSslProxyRequest
from google.cloud.compute_v1.types.compute import SetTagsInstanceRequest
from google.cloud.compute_v1.types.compute import SetTargetForwardingRuleRequest
from google.cloud.compute_v1.types.compute import SetTargetGlobalForwardingRuleRequest
from google.cloud.compute_v1.types.compute import (
    SetTargetPoolsInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import (
    SetTargetPoolsRegionInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import SetUrlMapRegionTargetHttpProxyRequest
from google.cloud.compute_v1.types.compute import SetUrlMapRegionTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import SetUrlMapTargetHttpProxyRequest
from google.cloud.compute_v1.types.compute import SetUrlMapTargetHttpsProxyRequest
from google.cloud.compute_v1.types.compute import SetUsageExportBucketProjectRequest
from google.cloud.compute_v1.types.compute import ShieldedInstanceConfig
from google.cloud.compute_v1.types.compute import ShieldedInstanceIdentity
from google.cloud.compute_v1.types.compute import ShieldedInstanceIdentityEntry
from google.cloud.compute_v1.types.compute import ShieldedInstanceIntegrityPolicy
from google.cloud.compute_v1.types.compute import SignedUrlKey
from google.cloud.compute_v1.types.compute import (
    SimulateMaintenanceEventInstanceRequest,
)
from google.cloud.compute_v1.types.compute import Snapshot
from google.cloud.compute_v1.types.compute import SnapshotList
from google.cloud.compute_v1.types.compute import SourceInstanceParams
from google.cloud.compute_v1.types.compute import SslCertificate
from google.cloud.compute_v1.types.compute import SslCertificateAggregatedList
from google.cloud.compute_v1.types.compute import SslCertificateList
from google.cloud.compute_v1.types.compute import SslCertificateManagedSslCertificate
from google.cloud.compute_v1.types.compute import (
    SslCertificateSelfManagedSslCertificate,
)
from google.cloud.compute_v1.types.compute import SslCertificatesScopedList
from google.cloud.compute_v1.types.compute import SSLHealthCheck
from google.cloud.compute_v1.types.compute import SslPoliciesList
from google.cloud.compute_v1.types.compute import (
    SslPoliciesListAvailableFeaturesResponse,
)
from google.cloud.compute_v1.types.compute import SslPolicy
from google.cloud.compute_v1.types.compute import SslPolicyReference
from google.cloud.compute_v1.types.compute import StartInstanceRequest
from google.cloud.compute_v1.types.compute import StartWithEncryptionKeyInstanceRequest
from google.cloud.compute_v1.types.compute import StatefulPolicy
from google.cloud.compute_v1.types.compute import StatefulPolicyPreservedState
from google.cloud.compute_v1.types.compute import StatefulPolicyPreservedStateDiskDevice
from google.cloud.compute_v1.types.compute import StopInstanceRequest
from google.cloud.compute_v1.types.compute import Subnetwork
from google.cloud.compute_v1.types.compute import SubnetworkAggregatedList
from google.cloud.compute_v1.types.compute import SubnetworkList
from google.cloud.compute_v1.types.compute import SubnetworkLogConfig
from google.cloud.compute_v1.types.compute import SubnetworkSecondaryRange
from google.cloud.compute_v1.types.compute import SubnetworksExpandIpCidrRangeRequest
from google.cloud.compute_v1.types.compute import SubnetworksScopedList
from google.cloud.compute_v1.types.compute import (
    SubnetworksSetPrivateIpGoogleAccessRequest,
)
from google.cloud.compute_v1.types.compute import SwitchToCustomModeNetworkRequest
from google.cloud.compute_v1.types.compute import Tags
from google.cloud.compute_v1.types.compute import TargetGrpcProxy
from google.cloud.compute_v1.types.compute import TargetGrpcProxyList
from google.cloud.compute_v1.types.compute import TargetHttpProxiesScopedList
from google.cloud.compute_v1.types.compute import TargetHttpProxy
from google.cloud.compute_v1.types.compute import TargetHttpProxyAggregatedList
from google.cloud.compute_v1.types.compute import TargetHttpProxyList
from google.cloud.compute_v1.types.compute import TargetHttpsProxiesScopedList
from google.cloud.compute_v1.types.compute import (
    TargetHttpsProxiesSetQuicOverrideRequest,
)
from google.cloud.compute_v1.types.compute import (
    TargetHttpsProxiesSetSslCertificatesRequest,
)
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
from google.cloud.compute_v1.types.compute import (
    TargetSslProxiesSetBackendServiceRequest,
)
from google.cloud.compute_v1.types.compute import TargetSslProxiesSetProxyHeaderRequest
from google.cloud.compute_v1.types.compute import (
    TargetSslProxiesSetSslCertificatesRequest,
)
from google.cloud.compute_v1.types.compute import TargetSslProxy
from google.cloud.compute_v1.types.compute import TargetSslProxyList
from google.cloud.compute_v1.types.compute import (
    TargetTcpProxiesSetBackendServiceRequest,
)
from google.cloud.compute_v1.types.compute import TargetTcpProxiesSetProxyHeaderRequest
from google.cloud.compute_v1.types.compute import TargetTcpProxy
from google.cloud.compute_v1.types.compute import TargetTcpProxyList
from google.cloud.compute_v1.types.compute import TargetVpnGateway
from google.cloud.compute_v1.types.compute import TargetVpnGatewayAggregatedList
from google.cloud.compute_v1.types.compute import TargetVpnGatewayList
from google.cloud.compute_v1.types.compute import TargetVpnGatewaysScopedList
from google.cloud.compute_v1.types.compute import TCPHealthCheck
from google.cloud.compute_v1.types.compute import TestFailure
from google.cloud.compute_v1.types.compute import TestIamPermissionsDiskRequest
from google.cloud.compute_v1.types.compute import (
    TestIamPermissionsExternalVpnGatewayRequest,
)
from google.cloud.compute_v1.types.compute import (
    TestIamPermissionsFirewallPolicyRequest,
)
from google.cloud.compute_v1.types.compute import TestIamPermissionsImageRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsInstanceRequest
from google.cloud.compute_v1.types.compute import (
    TestIamPermissionsInstanceTemplateRequest,
)
from google.cloud.compute_v1.types.compute import TestIamPermissionsLicenseCodeRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsLicenseRequest
from google.cloud.compute_v1.types.compute import (
    TestIamPermissionsNetworkEndpointGroupRequest,
)
from google.cloud.compute_v1.types.compute import TestIamPermissionsNodeGroupRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsNodeTemplateRequest
from google.cloud.compute_v1.types.compute import (
    TestIamPermissionsPacketMirroringRequest,
)
from google.cloud.compute_v1.types.compute import TestIamPermissionsRegionDiskRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsReservationRequest
from google.cloud.compute_v1.types.compute import (
    TestIamPermissionsResourcePolicyRequest,
)
from google.cloud.compute_v1.types.compute import TestIamPermissionsSnapshotRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsSubnetworkRequest
from google.cloud.compute_v1.types.compute import TestIamPermissionsVpnGatewayRequest
from google.cloud.compute_v1.types.compute import TestPermissionsRequest
from google.cloud.compute_v1.types.compute import TestPermissionsResponse
from google.cloud.compute_v1.types.compute import UpdateAccessConfigInstanceRequest
from google.cloud.compute_v1.types.compute import UpdateAutoscalerRequest
from google.cloud.compute_v1.types.compute import UpdateBackendBucketRequest
from google.cloud.compute_v1.types.compute import UpdateBackendServiceRequest
from google.cloud.compute_v1.types.compute import UpdateDisplayDeviceInstanceRequest
from google.cloud.compute_v1.types.compute import UpdateFirewallRequest
from google.cloud.compute_v1.types.compute import UpdateHealthCheckRequest
from google.cloud.compute_v1.types.compute import UpdateInstanceRequest
from google.cloud.compute_v1.types.compute import UpdateNetworkInterfaceInstanceRequest
from google.cloud.compute_v1.types.compute import UpdatePeeringNetworkRequest
from google.cloud.compute_v1.types.compute import (
    UpdatePerInstanceConfigsInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import (
    UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest,
)
from google.cloud.compute_v1.types.compute import UpdateRegionAutoscalerRequest
from google.cloud.compute_v1.types.compute import UpdateRegionBackendServiceRequest
from google.cloud.compute_v1.types.compute import UpdateRegionHealthCheckRequest
from google.cloud.compute_v1.types.compute import UpdateRegionUrlMapRequest
from google.cloud.compute_v1.types.compute import UpdateRouterRequest
from google.cloud.compute_v1.types.compute import (
    UpdateShieldedInstanceConfigInstanceRequest,
)
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
from google.cloud.compute_v1.types.compute import (
    VmEndpointNatMappingsInterfaceNatMappings,
)
from google.cloud.compute_v1.types.compute import VmEndpointNatMappingsList
from google.cloud.compute_v1.types.compute import VpnGateway
from google.cloud.compute_v1.types.compute import VpnGatewayAggregatedList
from google.cloud.compute_v1.types.compute import VpnGatewayList
from google.cloud.compute_v1.types.compute import VpnGatewaysGetStatusResponse
from google.cloud.compute_v1.types.compute import VpnGatewaysScopedList
from google.cloud.compute_v1.types.compute import VpnGatewayStatus
from google.cloud.compute_v1.types.compute import (
    VpnGatewayStatusHighAvailabilityRequirementState,
)
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
from google.cloud.compute_v1.types.compute import XpnHostList
from google.cloud.compute_v1.types.compute import XpnResourceId
from google.cloud.compute_v1.types.compute import Zone
from google.cloud.compute_v1.types.compute import ZoneList
from google.cloud.compute_v1.types.compute import ZoneSetLabelsRequest
from google.cloud.compute_v1.types.compute import ZoneSetPolicyRequest

__all__ = (
    "AcceleratorTypesClient",
    "AddressesClient",
    "AutoscalersClient",
    "BackendBucketsClient",
    "BackendServicesClient",
    "DisksClient",
    "DiskTypesClient",
    "ExternalVpnGatewaysClient",
    "FirewallPoliciesClient",
    "FirewallsClient",
    "ForwardingRulesClient",
    "GlobalAddressesClient",
    "GlobalForwardingRulesClient",
    "GlobalNetworkEndpointGroupsClient",
    "GlobalOperationsClient",
    "GlobalOrganizationOperationsClient",
    "GlobalPublicDelegatedPrefixesClient",
    "HealthChecksClient",
    "ImagesClient",
    "InstanceGroupManagersClient",
    "InstanceGroupsClient",
    "InstancesClient",
    "InstanceTemplatesClient",
    "InterconnectAttachmentsClient",
    "InterconnectLocationsClient",
    "InterconnectsClient",
    "LicenseCodesClient",
    "LicensesClient",
    "MachineTypesClient",
    "NetworkEndpointGroupsClient",
    "NetworksClient",
    "NodeGroupsClient",
    "NodeTemplatesClient",
    "NodeTypesClient",
    "PacketMirroringsClient",
    "ProjectsClient",
    "PublicAdvertisedPrefixesClient",
    "PublicDelegatedPrefixesClient",
    "RegionAutoscalersClient",
    "RegionBackendServicesClient",
    "RegionCommitmentsClient",
    "RegionDisksClient",
    "RegionDiskTypesClient",
    "RegionHealthChecksClient",
    "RegionHealthCheckServicesClient",
    "RegionInstanceGroupManagersClient",
    "RegionInstanceGroupsClient",
    "RegionInstancesClient",
    "RegionNetworkEndpointGroupsClient",
    "RegionNotificationEndpointsClient",
    "RegionOperationsClient",
    "RegionsClient",
    "RegionSslCertificatesClient",
    "RegionTargetHttpProxiesClient",
    "RegionTargetHttpsProxiesClient",
    "RegionUrlMapsClient",
    "ReservationsClient",
    "ResourcePoliciesClient",
    "RoutersClient",
    "RoutesClient",
    "SecurityPoliciesClient",
    "SnapshotsClient",
    "SslCertificatesClient",
    "SslPoliciesClient",
    "SubnetworksClient",
    "TargetGrpcProxiesClient",
    "TargetHttpProxiesClient",
    "TargetHttpsProxiesClient",
    "TargetInstancesClient",
    "TargetPoolsClient",
    "TargetSslProxiesClient",
    "TargetTcpProxiesClient",
    "TargetVpnGatewaysClient",
    "UrlMapsClient",
    "VpnGatewaysClient",
    "VpnTunnelsClient",
    "ZoneOperationsClient",
    "ZonesClient",
    "AbandonInstancesInstanceGroupManagerRequest",
    "AbandonInstancesRegionInstanceGroupManagerRequest",
    "AcceleratorConfig",
    "Accelerators",
    "AcceleratorType",
    "AcceleratorTypeAggregatedList",
    "AcceleratorTypeList",
    "AcceleratorTypesScopedList",
    "AccessConfig",
    "AddAccessConfigInstanceRequest",
    "AddAssociationFirewallPolicyRequest",
    "AddHealthCheckTargetPoolRequest",
    "AddInstancesInstanceGroupRequest",
    "AddInstanceTargetPoolRequest",
    "AddNodesNodeGroupRequest",
    "AddPeeringNetworkRequest",
    "AddResourcePoliciesDiskRequest",
    "AddResourcePoliciesInstanceRequest",
    "AddResourcePoliciesRegionDiskRequest",
    "Address",
    "AddressAggregatedList",
    "AddressesScopedList",
    "AddressList",
    "AddRuleFirewallPolicyRequest",
    "AddRuleSecurityPolicyRequest",
    "AddSignedUrlKeyBackendBucketRequest",
    "AddSignedUrlKeyBackendServiceRequest",
    "AdvancedMachineFeatures",
    "AggregatedListAcceleratorTypesRequest",
    "AggregatedListAddressesRequest",
    "AggregatedListAutoscalersRequest",
    "AggregatedListBackendServicesRequest",
    "AggregatedListDisksRequest",
    "AggregatedListDiskTypesRequest",
    "AggregatedListForwardingRulesRequest",
    "AggregatedListGlobalOperationsRequest",
    "AggregatedListHealthChecksRequest",
    "AggregatedListInstanceGroupManagersRequest",
    "AggregatedListInstanceGroupsRequest",
    "AggregatedListInstancesRequest",
    "AggregatedListInterconnectAttachmentsRequest",
    "AggregatedListMachineTypesRequest",
    "AggregatedListNetworkEndpointGroupsRequest",
    "AggregatedListNodeGroupsRequest",
    "AggregatedListNodeTemplatesRequest",
    "AggregatedListNodeTypesRequest",
    "AggregatedListPacketMirroringsRequest",
    "AggregatedListPublicDelegatedPrefixesRequest",
    "AggregatedListRegionCommitmentsRequest",
    "AggregatedListReservationsRequest",
    "AggregatedListResourcePoliciesRequest",
    "AggregatedListRoutersRequest",
    "AggregatedListSslCertificatesRequest",
    "AggregatedListSubnetworksRequest",
    "AggregatedListTargetHttpProxiesRequest",
    "AggregatedListTargetHttpsProxiesRequest",
    "AggregatedListTargetInstancesRequest",
    "AggregatedListTargetPoolsRequest",
    "AggregatedListTargetVpnGatewaysRequest",
    "AggregatedListUrlMapsRequest",
    "AggregatedListVpnGatewaysRequest",
    "AggregatedListVpnTunnelsRequest",
    "AliasIpRange",
    "AllocationSpecificSKUAllocationAllocatedInstancePropertiesReservedDisk",
    "AllocationSpecificSKUAllocationReservedInstanceProperties",
    "AllocationSpecificSKUReservation",
    "Allowed",
    "ApplyUpdatesToInstancesInstanceGroupManagerRequest",
    "ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest",
    "AttachDiskInstanceRequest",
    "AttachedDisk",
    "AttachedDiskInitializeParams",
    "AttachNetworkEndpointsGlobalNetworkEndpointGroupRequest",
    "AttachNetworkEndpointsNetworkEndpointGroupRequest",
    "AuditConfig",
    "AuditLogConfig",
    "AuthorizationLoggingOptions",
    "Autoscaler",
    "AutoscalerAggregatedList",
    "AutoscalerList",
    "AutoscalersScopedList",
    "AutoscalerStatusDetails",
    "AutoscalingPolicy",
    "AutoscalingPolicyCpuUtilization",
    "AutoscalingPolicyCustomMetricUtilization",
    "AutoscalingPolicyLoadBalancingUtilization",
    "AutoscalingPolicyScaleInControl",
    "AutoscalingPolicyScalingSchedule",
    "Backend",
    "BackendBucket",
    "BackendBucketCdnPolicy",
    "BackendBucketCdnPolicyBypassCacheOnRequestHeader",
    "BackendBucketCdnPolicyNegativeCachingPolicy",
    "BackendBucketList",
    "BackendService",
    "BackendServiceAggregatedList",
    "BackendServiceCdnPolicy",
    "BackendServiceCdnPolicyBypassCacheOnRequestHeader",
    "BackendServiceCdnPolicyNegativeCachingPolicy",
    "BackendServiceFailoverPolicy",
    "BackendServiceGroupHealth",
    "BackendServiceIAP",
    "BackendServiceList",
    "BackendServiceLogConfig",
    "BackendServiceReference",
    "BackendServicesScopedList",
    "Binding",
    "BulkInsertInstanceRequest",
    "BulkInsertInstanceResource",
    "BulkInsertInstanceResourcePerInstanceProperties",
    "BulkInsertRegionInstanceRequest",
    "CacheInvalidationRule",
    "CacheKeyPolicy",
    "CircuitBreakers",
    "CloneRulesFirewallPolicyRequest",
    "Commitment",
    "CommitmentAggregatedList",
    "CommitmentList",
    "CommitmentsScopedList",
    "Condition",
    "ConfidentialInstanceConfig",
    "ConnectionDraining",
    "ConsistentHashLoadBalancerSettings",
    "ConsistentHashLoadBalancerSettingsHttpCookie",
    "CorsPolicy",
    "CreateInstancesInstanceGroupManagerRequest",
    "CreateInstancesRegionInstanceGroupManagerRequest",
    "CreateSnapshotDiskRequest",
    "CreateSnapshotRegionDiskRequest",
    "CustomerEncryptionKey",
    "CustomerEncryptionKeyProtectedDisk",
    "Data",
    "DeleteAccessConfigInstanceRequest",
    "DeleteAddressRequest",
    "DeleteAutoscalerRequest",
    "DeleteBackendBucketRequest",
    "DeleteBackendServiceRequest",
    "DeleteDiskRequest",
    "DeleteExternalVpnGatewayRequest",
    "DeleteFirewallPolicyRequest",
    "DeleteFirewallRequest",
    "DeleteForwardingRuleRequest",
    "DeleteGlobalAddressRequest",
    "DeleteGlobalForwardingRuleRequest",
    "DeleteGlobalNetworkEndpointGroupRequest",
    "DeleteGlobalOperationRequest",
    "DeleteGlobalOperationResponse",
    "DeleteGlobalOrganizationOperationRequest",
    "DeleteGlobalOrganizationOperationResponse",
    "DeleteGlobalPublicDelegatedPrefixeRequest",
    "DeleteHealthCheckRequest",
    "DeleteImageRequest",
    "DeleteInstanceGroupManagerRequest",
    "DeleteInstanceGroupRequest",
    "DeleteInstanceRequest",
    "DeleteInstancesInstanceGroupManagerRequest",
    "DeleteInstancesRegionInstanceGroupManagerRequest",
    "DeleteInstanceTemplateRequest",
    "DeleteInterconnectAttachmentRequest",
    "DeleteInterconnectRequest",
    "DeleteLicenseRequest",
    "DeleteNetworkEndpointGroupRequest",
    "DeleteNetworkRequest",
    "DeleteNodeGroupRequest",
    "DeleteNodesNodeGroupRequest",
    "DeleteNodeTemplateRequest",
    "DeletePacketMirroringRequest",
    "DeletePerInstanceConfigsInstanceGroupManagerRequest",
    "DeletePerInstanceConfigsRegionInstanceGroupManagerRequest",
    "DeletePublicAdvertisedPrefixeRequest",
    "DeletePublicDelegatedPrefixeRequest",
    "DeleteRegionAutoscalerRequest",
    "DeleteRegionBackendServiceRequest",
    "DeleteRegionDiskRequest",
    "DeleteRegionHealthCheckRequest",
    "DeleteRegionHealthCheckServiceRequest",
    "DeleteRegionInstanceGroupManagerRequest",
    "DeleteRegionNetworkEndpointGroupRequest",
    "DeleteRegionNotificationEndpointRequest",
    "DeleteRegionOperationRequest",
    "DeleteRegionOperationResponse",
    "DeleteRegionSslCertificateRequest",
    "DeleteRegionTargetHttpProxyRequest",
    "DeleteRegionTargetHttpsProxyRequest",
    "DeleteRegionUrlMapRequest",
    "DeleteReservationRequest",
    "DeleteResourcePolicyRequest",
    "DeleteRouteRequest",
    "DeleteRouterRequest",
    "DeleteSecurityPolicyRequest",
    "DeleteSignedUrlKeyBackendBucketRequest",
    "DeleteSignedUrlKeyBackendServiceRequest",
    "DeleteSnapshotRequest",
    "DeleteSslCertificateRequest",
    "DeleteSslPolicyRequest",
    "DeleteSubnetworkRequest",
    "DeleteTargetGrpcProxyRequest",
    "DeleteTargetHttpProxyRequest",
    "DeleteTargetHttpsProxyRequest",
    "DeleteTargetInstanceRequest",
    "DeleteTargetPoolRequest",
    "DeleteTargetSslProxyRequest",
    "DeleteTargetTcpProxyRequest",
    "DeleteTargetVpnGatewayRequest",
    "DeleteUrlMapRequest",
    "DeleteVpnGatewayRequest",
    "DeleteVpnTunnelRequest",
    "DeleteZoneOperationRequest",
    "DeleteZoneOperationResponse",
    "Denied",
    "DeprecateImageRequest",
    "DeprecationStatus",
    "DetachDiskInstanceRequest",
    "DetachNetworkEndpointsGlobalNetworkEndpointGroupRequest",
    "DetachNetworkEndpointsNetworkEndpointGroupRequest",
    "DisableXpnHostProjectRequest",
    "DisableXpnResourceProjectRequest",
    "Disk",
    "DiskAggregatedList",
    "DiskInstantiationConfig",
    "DiskList",
    "DiskMoveRequest",
    "DisksAddResourcePoliciesRequest",
    "DisksRemoveResourcePoliciesRequest",
    "DisksResizeRequest",
    "DisksScopedList",
    "DiskType",
    "DiskTypeAggregatedList",
    "DiskTypeList",
    "DiskTypesScopedList",
    "DisplayDevice",
    "DistributionPolicy",
    "DistributionPolicyZoneConfiguration",
    "Duration",
    "EnableXpnHostProjectRequest",
    "EnableXpnResourceProjectRequest",
    "Error",
    "Errors",
    "ExchangedPeeringRoute",
    "ExchangedPeeringRoutesList",
    "ExpandIpCidrRangeSubnetworkRequest",
    "Expr",
    "ExternalVpnGateway",
    "ExternalVpnGatewayInterface",
    "ExternalVpnGatewayList",
    "FileContentBuffer",
    "Firewall",
    "FirewallList",
    "FirewallLogConfig",
    "FirewallPoliciesListAssociationsResponse",
    "FirewallPolicy",
    "FirewallPolicyAssociation",
    "FirewallPolicyList",
    "FirewallPolicyRule",
    "FirewallPolicyRuleMatcher",
    "FirewallPolicyRuleMatcherLayer4Config",
    "FixedOrPercent",
    "ForwardingRule",
    "ForwardingRuleAggregatedList",
    "ForwardingRuleList",
    "ForwardingRuleReference",
    "ForwardingRuleServiceDirectoryRegistration",
    "ForwardingRulesScopedList",
    "GetAcceleratorTypeRequest",
    "GetAddressRequest",
    "GetAssociationFirewallPolicyRequest",
    "GetAutoscalerRequest",
    "GetBackendBucketRequest",
    "GetBackendServiceRequest",
    "GetDiagnosticsInterconnectRequest",
    "GetDiskRequest",
    "GetDiskTypeRequest",
    "GetEffectiveFirewallsInstanceRequest",
    "GetEffectiveFirewallsNetworkRequest",
    "GetExternalVpnGatewayRequest",
    "GetFirewallPolicyRequest",
    "GetFirewallRequest",
    "GetForwardingRuleRequest",
    "GetFromFamilyImageRequest",
    "GetGlobalAddressRequest",
    "GetGlobalForwardingRuleRequest",
    "GetGlobalNetworkEndpointGroupRequest",
    "GetGlobalOperationRequest",
    "GetGlobalOrganizationOperationRequest",
    "GetGlobalPublicDelegatedPrefixeRequest",
    "GetGuestAttributesInstanceRequest",
    "GetHealthBackendServiceRequest",
    "GetHealthCheckRequest",
    "GetHealthRegionBackendServiceRequest",
    "GetHealthTargetPoolRequest",
    "GetIamPolicyDiskRequest",
    "GetIamPolicyFirewallPolicyRequest",
    "GetIamPolicyImageRequest",
    "GetIamPolicyInstanceRequest",
    "GetIamPolicyInstanceTemplateRequest",
    "GetIamPolicyLicenseRequest",
    "GetIamPolicyNodeGroupRequest",
    "GetIamPolicyNodeTemplateRequest",
    "GetIamPolicyRegionDiskRequest",
    "GetIamPolicyReservationRequest",
    "GetIamPolicyResourcePolicyRequest",
    "GetIamPolicySnapshotRequest",
    "GetIamPolicySubnetworkRequest",
    "GetImageRequest",
    "GetInstanceGroupManagerRequest",
    "GetInstanceGroupRequest",
    "GetInstanceRequest",
    "GetInstanceTemplateRequest",
    "GetInterconnectAttachmentRequest",
    "GetInterconnectLocationRequest",
    "GetInterconnectRequest",
    "GetLicenseCodeRequest",
    "GetLicenseRequest",
    "GetMachineTypeRequest",
    "GetNatMappingInfoRoutersRequest",
    "GetNetworkEndpointGroupRequest",
    "GetNetworkRequest",
    "GetNodeGroupRequest",
    "GetNodeTemplateRequest",
    "GetNodeTypeRequest",
    "GetPacketMirroringRequest",
    "GetProjectRequest",
    "GetPublicAdvertisedPrefixeRequest",
    "GetPublicDelegatedPrefixeRequest",
    "GetRegionAutoscalerRequest",
    "GetRegionBackendServiceRequest",
    "GetRegionCommitmentRequest",
    "GetRegionDiskRequest",
    "GetRegionDiskTypeRequest",
    "GetRegionHealthCheckRequest",
    "GetRegionHealthCheckServiceRequest",
    "GetRegionInstanceGroupManagerRequest",
    "GetRegionInstanceGroupRequest",
    "GetRegionNetworkEndpointGroupRequest",
    "GetRegionNotificationEndpointRequest",
    "GetRegionOperationRequest",
    "GetRegionRequest",
    "GetRegionSslCertificateRequest",
    "GetRegionTargetHttpProxyRequest",
    "GetRegionTargetHttpsProxyRequest",
    "GetRegionUrlMapRequest",
    "GetReservationRequest",
    "GetResourcePolicyRequest",
    "GetRouteRequest",
    "GetRouterRequest",
    "GetRouterStatusRouterRequest",
    "GetRuleFirewallPolicyRequest",
    "GetRuleSecurityPolicyRequest",
    "GetScreenshotInstanceRequest",
    "GetSecurityPolicyRequest",
    "GetSerialPortOutputInstanceRequest",
    "GetShieldedInstanceIdentityInstanceRequest",
    "GetSnapshotRequest",
    "GetSslCertificateRequest",
    "GetSslPolicyRequest",
    "GetStatusVpnGatewayRequest",
    "GetSubnetworkRequest",
    "GetTargetGrpcProxyRequest",
    "GetTargetHttpProxyRequest",
    "GetTargetHttpsProxyRequest",
    "GetTargetInstanceRequest",
    "GetTargetPoolRequest",
    "GetTargetSslProxyRequest",
    "GetTargetTcpProxyRequest",
    "GetTargetVpnGatewayRequest",
    "GetUrlMapRequest",
    "GetVpnGatewayRequest",
    "GetVpnTunnelRequest",
    "GetXpnHostProjectRequest",
    "GetXpnResourcesProjectsRequest",
    "GetZoneOperationRequest",
    "GetZoneRequest",
    "GlobalNetworkEndpointGroupsAttachEndpointsRequest",
    "GlobalNetworkEndpointGroupsDetachEndpointsRequest",
    "GlobalOrganizationSetPolicyRequest",
    "GlobalSetLabelsRequest",
    "GlobalSetPolicyRequest",
    "GRPCHealthCheck",
    "GuestAttributes",
    "GuestAttributesEntry",
    "GuestAttributesValue",
    "GuestOsFeature",
    "HealthCheck",
    "HealthCheckList",
    "HealthCheckLogConfig",
    "HealthCheckReference",
    "HealthChecksAggregatedList",
    "HealthCheckService",
    "HealthCheckServiceReference",
    "HealthCheckServicesList",
    "HealthChecksScopedList",
    "HealthStatus",
    "HealthStatusForNetworkEndpoint",
    "HostRule",
    "HTTP2HealthCheck",
    "HttpFaultAbort",
    "HttpFaultDelay",
    "HttpFaultInjection",
    "HttpHeaderAction",
    "HttpHeaderMatch",
    "HttpHeaderOption",
    "HTTPHealthCheck",
    "HttpQueryParameterMatch",
    "HttpRedirectAction",
    "HttpRetryPolicy",
    "HttpRouteAction",
    "HttpRouteRule",
    "HttpRouteRuleMatch",
    "HTTPSHealthCheck",
    "Image",
    "ImageList",
    "InitialStateConfig",
    "InsertAddressRequest",
    "InsertAutoscalerRequest",
    "InsertBackendBucketRequest",
    "InsertBackendServiceRequest",
    "InsertDiskRequest",
    "InsertExternalVpnGatewayRequest",
    "InsertFirewallPolicyRequest",
    "InsertFirewallRequest",
    "InsertForwardingRuleRequest",
    "InsertGlobalAddressRequest",
    "InsertGlobalForwardingRuleRequest",
    "InsertGlobalNetworkEndpointGroupRequest",
    "InsertGlobalPublicDelegatedPrefixeRequest",
    "InsertHealthCheckRequest",
    "InsertImageRequest",
    "InsertInstanceGroupManagerRequest",
    "InsertInstanceGroupRequest",
    "InsertInstanceRequest",
    "InsertInstanceTemplateRequest",
    "InsertInterconnectAttachmentRequest",
    "InsertInterconnectRequest",
    "InsertLicenseRequest",
    "InsertNetworkEndpointGroupRequest",
    "InsertNetworkRequest",
    "InsertNodeGroupRequest",
    "InsertNodeTemplateRequest",
    "InsertPacketMirroringRequest",
    "InsertPublicAdvertisedPrefixeRequest",
    "InsertPublicDelegatedPrefixeRequest",
    "InsertRegionAutoscalerRequest",
    "InsertRegionBackendServiceRequest",
    "InsertRegionCommitmentRequest",
    "InsertRegionDiskRequest",
    "InsertRegionHealthCheckRequest",
    "InsertRegionHealthCheckServiceRequest",
    "InsertRegionInstanceGroupManagerRequest",
    "InsertRegionNetworkEndpointGroupRequest",
    "InsertRegionNotificationEndpointRequest",
    "InsertRegionSslCertificateRequest",
    "InsertRegionTargetHttpProxyRequest",
    "InsertRegionTargetHttpsProxyRequest",
    "InsertRegionUrlMapRequest",
    "InsertReservationRequest",
    "InsertResourcePolicyRequest",
    "InsertRouteRequest",
    "InsertRouterRequest",
    "InsertSecurityPolicyRequest",
    "InsertSslCertificateRequest",
    "InsertSslPolicyRequest",
    "InsertSubnetworkRequest",
    "InsertTargetGrpcProxyRequest",
    "InsertTargetHttpProxyRequest",
    "InsertTargetHttpsProxyRequest",
    "InsertTargetInstanceRequest",
    "InsertTargetPoolRequest",
    "InsertTargetSslProxyRequest",
    "InsertTargetTcpProxyRequest",
    "InsertTargetVpnGatewayRequest",
    "InsertUrlMapRequest",
    "InsertVpnGatewayRequest",
    "InsertVpnTunnelRequest",
    "Instance",
    "InstanceAggregatedList",
    "InstanceGroup",
    "InstanceGroupAggregatedList",
    "InstanceGroupList",
    "InstanceGroupManager",
    "InstanceGroupManagerActionsSummary",
    "InstanceGroupManagerAggregatedList",
    "InstanceGroupManagerAutoHealingPolicy",
    "InstanceGroupManagerList",
    "InstanceGroupManagersAbandonInstancesRequest",
    "InstanceGroupManagersApplyUpdatesRequest",
    "InstanceGroupManagersCreateInstancesRequest",
    "InstanceGroupManagersDeleteInstancesRequest",
    "InstanceGroupManagersDeletePerInstanceConfigsReq",
    "InstanceGroupManagersListErrorsResponse",
    "InstanceGroupManagersListManagedInstancesResponse",
    "InstanceGroupManagersListPerInstanceConfigsResp",
    "InstanceGroupManagersPatchPerInstanceConfigsReq",
    "InstanceGroupManagersRecreateInstancesRequest",
    "InstanceGroupManagersScopedList",
    "InstanceGroupManagersSetInstanceTemplateRequest",
    "InstanceGroupManagersSetTargetPoolsRequest",
    "InstanceGroupManagerStatus",
    "InstanceGroupManagerStatusStateful",
    "InstanceGroupManagerStatusStatefulPerInstanceConfigs",
    "InstanceGroupManagerStatusVersionTarget",
    "InstanceGroupManagersUpdatePerInstanceConfigsReq",
    "InstanceGroupManagerUpdatePolicy",
    "InstanceGroupManagerVersion",
    "InstanceGroupsAddInstancesRequest",
    "InstanceGroupsListInstances",
    "InstanceGroupsListInstancesRequest",
    "InstanceGroupsRemoveInstancesRequest",
    "InstanceGroupsScopedList",
    "InstanceGroupsSetNamedPortsRequest",
    "InstanceList",
    "InstanceListReferrers",
    "InstanceManagedByIgmError",
    "InstanceManagedByIgmErrorInstanceActionDetails",
    "InstanceManagedByIgmErrorManagedInstanceError",
    "InstanceMoveRequest",
    "InstanceProperties",
    "InstanceReference",
    "InstancesAddResourcePoliciesRequest",
    "InstancesGetEffectiveFirewallsResponse",
    "InstancesGetEffectiveFirewallsResponseEffectiveFirewallPolicy",
    "InstancesRemoveResourcePoliciesRequest",
    "InstancesScopedList",
    "InstancesSetLabelsRequest",
    "InstancesSetMachineResourcesRequest",
    "InstancesSetMachineTypeRequest",
    "InstancesSetMinCpuPlatformRequest",
    "InstancesSetServiceAccountRequest",
    "InstancesStartWithEncryptionKeyRequest",
    "InstanceTemplate",
    "InstanceTemplateList",
    "InstanceWithNamedPorts",
    "Int64RangeMatch",
    "Interconnect",
    "InterconnectAttachment",
    "InterconnectAttachmentAggregatedList",
    "InterconnectAttachmentList",
    "InterconnectAttachmentPartnerMetadata",
    "InterconnectAttachmentPrivateInfo",
    "InterconnectAttachmentsScopedList",
    "InterconnectCircuitInfo",
    "InterconnectDiagnostics",
    "InterconnectDiagnosticsARPEntry",
    "InterconnectDiagnosticsLinkLACPStatus",
    "InterconnectDiagnosticsLinkOpticalPower",
    "InterconnectDiagnosticsLinkStatus",
    "InterconnectList",
    "InterconnectLocation",
    "InterconnectLocationList",
    "InterconnectLocationRegionInfo",
    "InterconnectOutageNotification",
    "InterconnectsGetDiagnosticsResponse",
    "InvalidateCacheUrlMapRequest",
    "Items",
    "License",
    "LicenseCode",
    "LicenseCodeLicenseAlias",
    "LicenseResourceCommitment",
    "LicenseResourceRequirements",
    "LicensesListResponse",
    "ListAcceleratorTypesRequest",
    "ListAddressesRequest",
    "ListAssociationsFirewallPolicyRequest",
    "ListAutoscalersRequest",
    "ListAvailableFeaturesSslPoliciesRequest",
    "ListBackendBucketsRequest",
    "ListBackendServicesRequest",
    "ListDisksRequest",
    "ListDiskTypesRequest",
    "ListErrorsInstanceGroupManagersRequest",
    "ListErrorsRegionInstanceGroupManagersRequest",
    "ListExternalVpnGatewaysRequest",
    "ListFirewallPoliciesRequest",
    "ListFirewallsRequest",
    "ListForwardingRulesRequest",
    "ListGlobalAddressesRequest",
    "ListGlobalForwardingRulesRequest",
    "ListGlobalNetworkEndpointGroupsRequest",
    "ListGlobalOperationsRequest",
    "ListGlobalOrganizationOperationsRequest",
    "ListGlobalPublicDelegatedPrefixesRequest",
    "ListHealthChecksRequest",
    "ListImagesRequest",
    "ListInstanceGroupManagersRequest",
    "ListInstanceGroupsRequest",
    "ListInstancesInstanceGroupsRequest",
    "ListInstancesRegionInstanceGroupsRequest",
    "ListInstancesRequest",
    "ListInstanceTemplatesRequest",
    "ListInterconnectAttachmentsRequest",
    "ListInterconnectLocationsRequest",
    "ListInterconnectsRequest",
    "ListLicensesRequest",
    "ListMachineTypesRequest",
    "ListManagedInstancesInstanceGroupManagersRequest",
    "ListManagedInstancesRegionInstanceGroupManagersRequest",
    "ListNetworkEndpointGroupsRequest",
    "ListNetworkEndpointsGlobalNetworkEndpointGroupsRequest",
    "ListNetworkEndpointsNetworkEndpointGroupsRequest",
    "ListNetworksRequest",
    "ListNodeGroupsRequest",
    "ListNodesNodeGroupsRequest",
    "ListNodeTemplatesRequest",
    "ListNodeTypesRequest",
    "ListPacketMirroringsRequest",
    "ListPeeringRoutesNetworksRequest",
    "ListPerInstanceConfigsInstanceGroupManagersRequest",
    "ListPerInstanceConfigsRegionInstanceGroupManagersRequest",
    "ListPreconfiguredExpressionSetsSecurityPoliciesRequest",
    "ListPublicAdvertisedPrefixesRequest",
    "ListPublicDelegatedPrefixesRequest",
    "ListReferrersInstancesRequest",
    "ListRegionAutoscalersRequest",
    "ListRegionBackendServicesRequest",
    "ListRegionCommitmentsRequest",
    "ListRegionDisksRequest",
    "ListRegionDiskTypesRequest",
    "ListRegionHealthCheckServicesRequest",
    "ListRegionHealthChecksRequest",
    "ListRegionInstanceGroupManagersRequest",
    "ListRegionInstanceGroupsRequest",
    "ListRegionNetworkEndpointGroupsRequest",
    "ListRegionNotificationEndpointsRequest",
    "ListRegionOperationsRequest",
    "ListRegionsRequest",
    "ListRegionSslCertificatesRequest",
    "ListRegionTargetHttpProxiesRequest",
    "ListRegionTargetHttpsProxiesRequest",
    "ListRegionUrlMapsRequest",
    "ListReservationsRequest",
    "ListResourcePoliciesRequest",
    "ListRoutersRequest",
    "ListRoutesRequest",
    "ListSecurityPoliciesRequest",
    "ListSnapshotsRequest",
    "ListSslCertificatesRequest",
    "ListSslPoliciesRequest",
    "ListSubnetworksRequest",
    "ListTargetGrpcProxiesRequest",
    "ListTargetHttpProxiesRequest",
    "ListTargetHttpsProxiesRequest",
    "ListTargetInstancesRequest",
    "ListTargetPoolsRequest",
    "ListTargetSslProxiesRequest",
    "ListTargetTcpProxiesRequest",
    "ListTargetVpnGatewaysRequest",
    "ListUrlMapsRequest",
    "ListUsableSubnetworksRequest",
    "ListVpnGatewaysRequest",
    "ListVpnTunnelsRequest",
    "ListXpnHostsProjectsRequest",
    "ListZoneOperationsRequest",
    "ListZonesRequest",
    "LocalDisk",
    "LocationPolicy",
    "LocationPolicyLocation",
    "LogConfig",
    "LogConfigCloudAuditOptions",
    "LogConfigCounterOptions",
    "LogConfigCounterOptionsCustomField",
    "LogConfigDataAccessOptions",
    "MachineType",
    "MachineTypeAggregatedList",
    "MachineTypeList",
    "MachineTypesScopedList",
    "ManagedInstance",
    "ManagedInstanceInstanceHealth",
    "ManagedInstanceLastAttempt",
    "ManagedInstanceVersion",
    "Metadata",
    "MetadataFilter",
    "MetadataFilterLabelMatch",
    "MoveDiskProjectRequest",
    "MoveFirewallPolicyRequest",
    "MoveInstanceProjectRequest",
    "NamedPort",
    "Network",
    "NetworkEndpoint",
    "NetworkEndpointGroup",
    "NetworkEndpointGroupAggregatedList",
    "NetworkEndpointGroupAppEngine",
    "NetworkEndpointGroupCloudFunction",
    "NetworkEndpointGroupCloudRun",
    "NetworkEndpointGroupList",
    "NetworkEndpointGroupsAttachEndpointsRequest",
    "NetworkEndpointGroupsDetachEndpointsRequest",
    "NetworkEndpointGroupsListEndpointsRequest",
    "NetworkEndpointGroupsListNetworkEndpoints",
    "NetworkEndpointGroupsScopedList",
    "NetworkEndpointWithHealthStatus",
    "NetworkInterface",
    "NetworkList",
    "NetworkPeering",
    "NetworkRoutingConfig",
    "NetworksAddPeeringRequest",
    "NetworksGetEffectiveFirewallsResponse",
    "NetworksGetEffectiveFirewallsResponseEffectiveFirewallPolicy",
    "NetworksRemovePeeringRequest",
    "NetworksUpdatePeeringRequest",
    "NodeGroup",
    "NodeGroupAggregatedList",
    "NodeGroupAutoscalingPolicy",
    "NodeGroupList",
    "NodeGroupMaintenanceWindow",
    "NodeGroupNode",
    "NodeGroupsAddNodesRequest",
    "NodeGroupsDeleteNodesRequest",
    "NodeGroupsListNodes",
    "NodeGroupsScopedList",
    "NodeGroupsSetNodeTemplateRequest",
    "NodeTemplate",
    "NodeTemplateAggregatedList",
    "NodeTemplateList",
    "NodeTemplateNodeTypeFlexibility",
    "NodeTemplatesScopedList",
    "NodeType",
    "NodeTypeAggregatedList",
    "NodeTypeList",
    "NodeTypesScopedList",
    "NotificationEndpoint",
    "NotificationEndpointGrpcSettings",
    "NotificationEndpointList",
    "Operation",
    "OperationAggregatedList",
    "OperationList",
    "OperationsScopedList",
    "OutlierDetection",
    "PacketMirroring",
    "PacketMirroringAggregatedList",
    "PacketMirroringFilter",
    "PacketMirroringForwardingRuleInfo",
    "PacketMirroringList",
    "PacketMirroringMirroredResourceInfo",
    "PacketMirroringMirroredResourceInfoInstanceInfo",
    "PacketMirroringMirroredResourceInfoSubnetInfo",
    "PacketMirroringNetworkInfo",
    "PacketMirroringsScopedList",
    "PatchAutoscalerRequest",
    "PatchBackendBucketRequest",
    "PatchBackendServiceRequest",
    "PatchFirewallPolicyRequest",
    "PatchFirewallRequest",
    "PatchForwardingRuleRequest",
    "PatchGlobalForwardingRuleRequest",
    "PatchGlobalPublicDelegatedPrefixeRequest",
    "PatchHealthCheckRequest",
    "PatchImageRequest",
    "PatchInstanceGroupManagerRequest",
    "PatchInterconnectAttachmentRequest",
    "PatchInterconnectRequest",
    "PatchNetworkRequest",
    "PatchNodeGroupRequest",
    "PatchPacketMirroringRequest",
    "PatchPerInstanceConfigsInstanceGroupManagerRequest",
    "PatchPerInstanceConfigsRegionInstanceGroupManagerRequest",
    "PatchPublicAdvertisedPrefixeRequest",
    "PatchPublicDelegatedPrefixeRequest",
    "PatchRegionAutoscalerRequest",
    "PatchRegionBackendServiceRequest",
    "PatchRegionHealthCheckRequest",
    "PatchRegionHealthCheckServiceRequest",
    "PatchRegionInstanceGroupManagerRequest",
    "PatchRegionUrlMapRequest",
    "PatchRouterRequest",
    "PatchRuleFirewallPolicyRequest",
    "PatchRuleSecurityPolicyRequest",
    "PatchSecurityPolicyRequest",
    "PatchSslPolicyRequest",
    "PatchSubnetworkRequest",
    "PatchTargetGrpcProxyRequest",
    "PatchTargetHttpProxyRequest",
    "PatchTargetHttpsProxyRequest",
    "PatchUrlMapRequest",
    "PathMatcher",
    "PathRule",
    "PerInstanceConfig",
    "Policy",
    "PreconfiguredWafSet",
    "PreservedState",
    "PreservedStatePreservedDisk",
    "PreviewRouterRequest",
    "Project",
    "ProjectsDisableXpnResourceRequest",
    "ProjectsEnableXpnResourceRequest",
    "ProjectsGetXpnResources",
    "ProjectsListXpnHostsRequest",
    "ProjectsSetDefaultNetworkTierRequest",
    "PublicAdvertisedPrefix",
    "PublicAdvertisedPrefixList",
    "PublicAdvertisedPrefixPublicDelegatedPrefix",
    "PublicDelegatedPrefix",
    "PublicDelegatedPrefixAggregatedList",
    "PublicDelegatedPrefixesScopedList",
    "PublicDelegatedPrefixList",
    "PublicDelegatedPrefixPublicDelegatedSubPrefix",
    "Quota",
    "RawDisk",
    "RecreateInstancesInstanceGroupManagerRequest",
    "RecreateInstancesRegionInstanceGroupManagerRequest",
    "Reference",
    "Region",
    "RegionAutoscalerList",
    "RegionDisksAddResourcePoliciesRequest",
    "RegionDisksRemoveResourcePoliciesRequest",
    "RegionDisksResizeRequest",
    "RegionDiskTypeList",
    "RegionInstanceGroupList",
    "RegionInstanceGroupManagerDeleteInstanceConfigReq",
    "RegionInstanceGroupManagerList",
    "RegionInstanceGroupManagerPatchInstanceConfigReq",
    "RegionInstanceGroupManagersAbandonInstancesRequest",
    "RegionInstanceGroupManagersApplyUpdatesRequest",
    "RegionInstanceGroupManagersCreateInstancesRequest",
    "RegionInstanceGroupManagersDeleteInstancesRequest",
    "RegionInstanceGroupManagersListErrorsResponse",
    "RegionInstanceGroupManagersListInstanceConfigsResp",
    "RegionInstanceGroupManagersListInstancesResponse",
    "RegionInstanceGroupManagersRecreateRequest",
    "RegionInstanceGroupManagersSetTargetPoolsRequest",
    "RegionInstanceGroupManagersSetTemplateRequest",
    "RegionInstanceGroupManagerUpdateInstanceConfigReq",
    "RegionInstanceGroupsListInstances",
    "RegionInstanceGroupsListInstancesRequest",
    "RegionInstanceGroupsSetNamedPortsRequest",
    "RegionList",
    "RegionSetLabelsRequest",
    "RegionSetPolicyRequest",
    "RegionTargetHttpsProxiesSetSslCertificatesRequest",
    "RegionUrlMapsValidateRequest",
    "RemoveAssociationFirewallPolicyRequest",
    "RemoveHealthCheckTargetPoolRequest",
    "RemoveInstancesInstanceGroupRequest",
    "RemoveInstanceTargetPoolRequest",
    "RemovePeeringNetworkRequest",
    "RemoveResourcePoliciesDiskRequest",
    "RemoveResourcePoliciesInstanceRequest",
    "RemoveResourcePoliciesRegionDiskRequest",
    "RemoveRuleFirewallPolicyRequest",
    "RemoveRuleSecurityPolicyRequest",
    "RequestMirrorPolicy",
    "Reservation",
    "ReservationAffinity",
    "ReservationAggregatedList",
    "ReservationList",
    "ReservationsResizeRequest",
    "ReservationsScopedList",
    "ResetInstanceRequest",
    "ResizeDiskRequest",
    "ResizeInstanceGroupManagerRequest",
    "ResizeRegionDiskRequest",
    "ResizeRegionInstanceGroupManagerRequest",
    "ResizeReservationRequest",
    "ResourceCommitment",
    "ResourceGroupReference",
    "ResourcePoliciesScopedList",
    "ResourcePolicy",
    "ResourcePolicyAggregatedList",
    "ResourcePolicyDailyCycle",
    "ResourcePolicyGroupPlacementPolicy",
    "ResourcePolicyHourlyCycle",
    "ResourcePolicyInstanceSchedulePolicy",
    "ResourcePolicyInstanceSchedulePolicySchedule",
    "ResourcePolicyList",
    "ResourcePolicyResourceStatus",
    "ResourcePolicyResourceStatusInstanceSchedulePolicyStatus",
    "ResourcePolicySnapshotSchedulePolicy",
    "ResourcePolicySnapshotSchedulePolicyRetentionPolicy",
    "ResourcePolicySnapshotSchedulePolicySchedule",
    "ResourcePolicySnapshotSchedulePolicySnapshotProperties",
    "ResourcePolicyWeeklyCycle",
    "ResourcePolicyWeeklyCycleDayOfWeek",
    "Route",
    "RouteList",
    "Router",
    "RouterAdvertisedIpRange",
    "RouterAggregatedList",
    "RouterBgp",
    "RouterBgpPeer",
    "RouterInterface",
    "RouterList",
    "RouterNat",
    "RouterNatLogConfig",
    "RouterNatSubnetworkToNat",
    "RoutersPreviewResponse",
    "RoutersScopedList",
    "RouterStatus",
    "RouterStatusBgpPeerStatus",
    "RouterStatusNatStatus",
    "RouterStatusResponse",
    "Rule",
    "ScalingScheduleStatus",
    "Scheduling",
    "SchedulingNodeAffinity",
    "ScratchDisks",
    "Screenshot",
    "SecurityPoliciesListPreconfiguredExpressionSetsResponse",
    "SecurityPoliciesWafConfig",
    "SecurityPolicy",
    "SecurityPolicyList",
    "SecurityPolicyReference",
    "SecurityPolicyRule",
    "SecurityPolicyRuleMatcher",
    "SecurityPolicyRuleMatcherConfig",
    "SecuritySettings",
    "SerialPortOutput",
    "ServerBinding",
    "ServiceAccount",
    "SetBackendServiceTargetSslProxyRequest",
    "SetBackendServiceTargetTcpProxyRequest",
    "SetBackupTargetPoolRequest",
    "SetCommonInstanceMetadataProjectRequest",
    "SetDefaultNetworkTierProjectRequest",
    "SetDeletionProtectionInstanceRequest",
    "SetDiskAutoDeleteInstanceRequest",
    "SetIamPolicyDiskRequest",
    "SetIamPolicyFirewallPolicyRequest",
    "SetIamPolicyImageRequest",
    "SetIamPolicyInstanceRequest",
    "SetIamPolicyInstanceTemplateRequest",
    "SetIamPolicyLicenseRequest",
    "SetIamPolicyNodeGroupRequest",
    "SetIamPolicyNodeTemplateRequest",
    "SetIamPolicyRegionDiskRequest",
    "SetIamPolicyReservationRequest",
    "SetIamPolicyResourcePolicyRequest",
    "SetIamPolicySnapshotRequest",
    "SetIamPolicySubnetworkRequest",
    "SetInstanceTemplateInstanceGroupManagerRequest",
    "SetInstanceTemplateRegionInstanceGroupManagerRequest",
    "SetLabelsDiskRequest",
    "SetLabelsExternalVpnGatewayRequest",
    "SetLabelsForwardingRuleRequest",
    "SetLabelsGlobalForwardingRuleRequest",
    "SetLabelsImageRequest",
    "SetLabelsInstanceRequest",
    "SetLabelsRegionDiskRequest",
    "SetLabelsSnapshotRequest",
    "SetLabelsVpnGatewayRequest",
    "SetMachineResourcesInstanceRequest",
    "SetMachineTypeInstanceRequest",
    "SetMetadataInstanceRequest",
    "SetMinCpuPlatformInstanceRequest",
    "SetNamedPortsInstanceGroupRequest",
    "SetNamedPortsRegionInstanceGroupRequest",
    "SetNodeTemplateNodeGroupRequest",
    "SetPrivateIpGoogleAccessSubnetworkRequest",
    "SetProxyHeaderTargetSslProxyRequest",
    "SetProxyHeaderTargetTcpProxyRequest",
    "SetQuicOverrideTargetHttpsProxyRequest",
    "SetSchedulingInstanceRequest",
    "SetSecurityPolicyBackendServiceRequest",
    "SetServiceAccountInstanceRequest",
    "SetShieldedInstanceIntegrityPolicyInstanceRequest",
    "SetSslCertificatesRegionTargetHttpsProxyRequest",
    "SetSslCertificatesTargetHttpsProxyRequest",
    "SetSslCertificatesTargetSslProxyRequest",
    "SetSslPolicyTargetHttpsProxyRequest",
    "SetSslPolicyTargetSslProxyRequest",
    "SetTagsInstanceRequest",
    "SetTargetForwardingRuleRequest",
    "SetTargetGlobalForwardingRuleRequest",
    "SetTargetPoolsInstanceGroupManagerRequest",
    "SetTargetPoolsRegionInstanceGroupManagerRequest",
    "SetUrlMapRegionTargetHttpProxyRequest",
    "SetUrlMapRegionTargetHttpsProxyRequest",
    "SetUrlMapTargetHttpProxyRequest",
    "SetUrlMapTargetHttpsProxyRequest",
    "SetUsageExportBucketProjectRequest",
    "ShieldedInstanceConfig",
    "ShieldedInstanceIdentity",
    "ShieldedInstanceIdentityEntry",
    "ShieldedInstanceIntegrityPolicy",
    "SignedUrlKey",
    "SimulateMaintenanceEventInstanceRequest",
    "Snapshot",
    "SnapshotList",
    "SourceInstanceParams",
    "SslCertificate",
    "SslCertificateAggregatedList",
    "SslCertificateList",
    "SslCertificateManagedSslCertificate",
    "SslCertificateSelfManagedSslCertificate",
    "SslCertificatesScopedList",
    "SSLHealthCheck",
    "SslPoliciesList",
    "SslPoliciesListAvailableFeaturesResponse",
    "SslPolicy",
    "SslPolicyReference",
    "StartInstanceRequest",
    "StartWithEncryptionKeyInstanceRequest",
    "StatefulPolicy",
    "StatefulPolicyPreservedState",
    "StatefulPolicyPreservedStateDiskDevice",
    "StopInstanceRequest",
    "Subnetwork",
    "SubnetworkAggregatedList",
    "SubnetworkList",
    "SubnetworkLogConfig",
    "SubnetworkSecondaryRange",
    "SubnetworksExpandIpCidrRangeRequest",
    "SubnetworksScopedList",
    "SubnetworksSetPrivateIpGoogleAccessRequest",
    "SwitchToCustomModeNetworkRequest",
    "Tags",
    "TargetGrpcProxy",
    "TargetGrpcProxyList",
    "TargetHttpProxiesScopedList",
    "TargetHttpProxy",
    "TargetHttpProxyAggregatedList",
    "TargetHttpProxyList",
    "TargetHttpsProxiesScopedList",
    "TargetHttpsProxiesSetQuicOverrideRequest",
    "TargetHttpsProxiesSetSslCertificatesRequest",
    "TargetHttpsProxy",
    "TargetHttpsProxyAggregatedList",
    "TargetHttpsProxyList",
    "TargetInstance",
    "TargetInstanceAggregatedList",
    "TargetInstanceList",
    "TargetInstancesScopedList",
    "TargetPool",
    "TargetPoolAggregatedList",
    "TargetPoolInstanceHealth",
    "TargetPoolList",
    "TargetPoolsAddHealthCheckRequest",
    "TargetPoolsAddInstanceRequest",
    "TargetPoolsRemoveHealthCheckRequest",
    "TargetPoolsRemoveInstanceRequest",
    "TargetPoolsScopedList",
    "TargetReference",
    "TargetSslProxiesSetBackendServiceRequest",
    "TargetSslProxiesSetProxyHeaderRequest",
    "TargetSslProxiesSetSslCertificatesRequest",
    "TargetSslProxy",
    "TargetSslProxyList",
    "TargetTcpProxiesSetBackendServiceRequest",
    "TargetTcpProxiesSetProxyHeaderRequest",
    "TargetTcpProxy",
    "TargetTcpProxyList",
    "TargetVpnGateway",
    "TargetVpnGatewayAggregatedList",
    "TargetVpnGatewayList",
    "TargetVpnGatewaysScopedList",
    "TCPHealthCheck",
    "TestFailure",
    "TestIamPermissionsDiskRequest",
    "TestIamPermissionsExternalVpnGatewayRequest",
    "TestIamPermissionsFirewallPolicyRequest",
    "TestIamPermissionsImageRequest",
    "TestIamPermissionsInstanceRequest",
    "TestIamPermissionsInstanceTemplateRequest",
    "TestIamPermissionsLicenseCodeRequest",
    "TestIamPermissionsLicenseRequest",
    "TestIamPermissionsNetworkEndpointGroupRequest",
    "TestIamPermissionsNodeGroupRequest",
    "TestIamPermissionsNodeTemplateRequest",
    "TestIamPermissionsPacketMirroringRequest",
    "TestIamPermissionsRegionDiskRequest",
    "TestIamPermissionsReservationRequest",
    "TestIamPermissionsResourcePolicyRequest",
    "TestIamPermissionsSnapshotRequest",
    "TestIamPermissionsSubnetworkRequest",
    "TestIamPermissionsVpnGatewayRequest",
    "TestPermissionsRequest",
    "TestPermissionsResponse",
    "UpdateAccessConfigInstanceRequest",
    "UpdateAutoscalerRequest",
    "UpdateBackendBucketRequest",
    "UpdateBackendServiceRequest",
    "UpdateDisplayDeviceInstanceRequest",
    "UpdateFirewallRequest",
    "UpdateHealthCheckRequest",
    "UpdateInstanceRequest",
    "UpdateNetworkInterfaceInstanceRequest",
    "UpdatePeeringNetworkRequest",
    "UpdatePerInstanceConfigsInstanceGroupManagerRequest",
    "UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest",
    "UpdateRegionAutoscalerRequest",
    "UpdateRegionBackendServiceRequest",
    "UpdateRegionHealthCheckRequest",
    "UpdateRegionUrlMapRequest",
    "UpdateRouterRequest",
    "UpdateShieldedInstanceConfigInstanceRequest",
    "UpdateUrlMapRequest",
    "UrlMap",
    "UrlMapList",
    "UrlMapReference",
    "UrlMapsAggregatedList",
    "UrlMapsScopedList",
    "UrlMapsValidateRequest",
    "UrlMapsValidateResponse",
    "UrlMapTest",
    "UrlMapTestHeader",
    "UrlMapValidationResult",
    "UrlRewrite",
    "UsableSubnetwork",
    "UsableSubnetworksAggregatedList",
    "UsableSubnetworkSecondaryRange",
    "UsageExportLocation",
    "ValidateRegionUrlMapRequest",
    "ValidateUrlMapRequest",
    "VmEndpointNatMappings",
    "VmEndpointNatMappingsInterfaceNatMappings",
    "VmEndpointNatMappingsList",
    "VpnGateway",
    "VpnGatewayAggregatedList",
    "VpnGatewayList",
    "VpnGatewaysGetStatusResponse",
    "VpnGatewaysScopedList",
    "VpnGatewayStatus",
    "VpnGatewayStatusHighAvailabilityRequirementState",
    "VpnGatewayStatusTunnel",
    "VpnGatewayStatusVpnConnection",
    "VpnGatewayVpnGatewayInterface",
    "VpnTunnel",
    "VpnTunnelAggregatedList",
    "VpnTunnelList",
    "VpnTunnelsScopedList",
    "WafExpressionSet",
    "WafExpressionSetExpression",
    "WaitGlobalOperationRequest",
    "WaitRegionOperationRequest",
    "WaitZoneOperationRequest",
    "Warning",
    "Warnings",
    "WeightedBackendService",
    "XpnHostList",
    "XpnResourceId",
    "Zone",
    "ZoneList",
    "ZoneSetLabelsRequest",
    "ZoneSetPolicyRequest",
)
