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

from .services.accelerator_types import AcceleratorTypesClient
from .services.addresses import AddressesClient
from .services.autoscalers import AutoscalersClient
from .services.backend_buckets import BackendBucketsClient
from .services.backend_services import BackendServicesClient
from .services.disks import DisksClient
from .services.disk_types import DiskTypesClient
from .services.external_vpn_gateways import ExternalVpnGatewaysClient
from .services.firewall_policies import FirewallPoliciesClient
from .services.firewalls import FirewallsClient
from .services.forwarding_rules import ForwardingRulesClient
from .services.global_addresses import GlobalAddressesClient
from .services.global_forwarding_rules import GlobalForwardingRulesClient
from .services.global_network_endpoint_groups import GlobalNetworkEndpointGroupsClient
from .services.global_operations import GlobalOperationsClient
from .services.global_organization_operations import GlobalOrganizationOperationsClient
from .services.global_public_delegated_prefixes import (
    GlobalPublicDelegatedPrefixesClient,
)
from .services.health_checks import HealthChecksClient
from .services.images import ImagesClient
from .services.instance_group_managers import InstanceGroupManagersClient
from .services.instance_groups import InstanceGroupsClient
from .services.instances import InstancesClient
from .services.instance_templates import InstanceTemplatesClient
from .services.interconnect_attachments import InterconnectAttachmentsClient
from .services.interconnect_locations import InterconnectLocationsClient
from .services.interconnects import InterconnectsClient
from .services.license_codes import LicenseCodesClient
from .services.licenses import LicensesClient
from .services.machine_types import MachineTypesClient
from .services.network_endpoint_groups import NetworkEndpointGroupsClient
from .services.networks import NetworksClient
from .services.node_groups import NodeGroupsClient
from .services.node_templates import NodeTemplatesClient
from .services.node_types import NodeTypesClient
from .services.packet_mirrorings import PacketMirroringsClient
from .services.projects import ProjectsClient
from .services.public_advertised_prefixes import PublicAdvertisedPrefixesClient
from .services.public_delegated_prefixes import PublicDelegatedPrefixesClient
from .services.region_autoscalers import RegionAutoscalersClient
from .services.region_backend_services import RegionBackendServicesClient
from .services.region_commitments import RegionCommitmentsClient
from .services.region_disks import RegionDisksClient
from .services.region_disk_types import RegionDiskTypesClient
from .services.region_health_checks import RegionHealthChecksClient
from .services.region_health_check_services import RegionHealthCheckServicesClient
from .services.region_instance_group_managers import RegionInstanceGroupManagersClient
from .services.region_instance_groups import RegionInstanceGroupsClient
from .services.region_instances import RegionInstancesClient
from .services.region_network_endpoint_groups import RegionNetworkEndpointGroupsClient
from .services.region_notification_endpoints import RegionNotificationEndpointsClient
from .services.region_operations import RegionOperationsClient
from .services.regions import RegionsClient
from .services.region_ssl_certificates import RegionSslCertificatesClient
from .services.region_target_http_proxies import RegionTargetHttpProxiesClient
from .services.region_target_https_proxies import RegionTargetHttpsProxiesClient
from .services.region_url_maps import RegionUrlMapsClient
from .services.reservations import ReservationsClient
from .services.resource_policies import ResourcePoliciesClient
from .services.routers import RoutersClient
from .services.routes import RoutesClient
from .services.security_policies import SecurityPoliciesClient
from .services.snapshots import SnapshotsClient
from .services.ssl_certificates import SslCertificatesClient
from .services.ssl_policies import SslPoliciesClient
from .services.subnetworks import SubnetworksClient
from .services.target_grpc_proxies import TargetGrpcProxiesClient
from .services.target_http_proxies import TargetHttpProxiesClient
from .services.target_https_proxies import TargetHttpsProxiesClient
from .services.target_instances import TargetInstancesClient
from .services.target_pools import TargetPoolsClient
from .services.target_ssl_proxies import TargetSslProxiesClient
from .services.target_tcp_proxies import TargetTcpProxiesClient
from .services.target_vpn_gateways import TargetVpnGatewaysClient
from .services.url_maps import UrlMapsClient
from .services.vpn_gateways import VpnGatewaysClient
from .services.vpn_tunnels import VpnTunnelsClient
from .services.zone_operations import ZoneOperationsClient
from .services.zones import ZonesClient

from .types.compute import AbandonInstancesInstanceGroupManagerRequest
from .types.compute import AbandonInstancesRegionInstanceGroupManagerRequest
from .types.compute import AcceleratorConfig
from .types.compute import Accelerators
from .types.compute import AcceleratorType
from .types.compute import AcceleratorTypeAggregatedList
from .types.compute import AcceleratorTypeList
from .types.compute import AcceleratorTypesScopedList
from .types.compute import AccessConfig
from .types.compute import AddAccessConfigInstanceRequest
from .types.compute import AddAssociationFirewallPolicyRequest
from .types.compute import AddHealthCheckTargetPoolRequest
from .types.compute import AddInstancesInstanceGroupRequest
from .types.compute import AddInstanceTargetPoolRequest
from .types.compute import AddNodesNodeGroupRequest
from .types.compute import AddPeeringNetworkRequest
from .types.compute import AddResourcePoliciesDiskRequest
from .types.compute import AddResourcePoliciesInstanceRequest
from .types.compute import AddResourcePoliciesRegionDiskRequest
from .types.compute import Address
from .types.compute import AddressAggregatedList
from .types.compute import AddressesScopedList
from .types.compute import AddressList
from .types.compute import AddRuleFirewallPolicyRequest
from .types.compute import AddRuleSecurityPolicyRequest
from .types.compute import AddSignedUrlKeyBackendBucketRequest
from .types.compute import AddSignedUrlKeyBackendServiceRequest
from .types.compute import AdvancedMachineFeatures
from .types.compute import AggregatedListAcceleratorTypesRequest
from .types.compute import AggregatedListAddressesRequest
from .types.compute import AggregatedListAutoscalersRequest
from .types.compute import AggregatedListBackendServicesRequest
from .types.compute import AggregatedListDisksRequest
from .types.compute import AggregatedListDiskTypesRequest
from .types.compute import AggregatedListForwardingRulesRequest
from .types.compute import AggregatedListGlobalOperationsRequest
from .types.compute import AggregatedListHealthChecksRequest
from .types.compute import AggregatedListInstanceGroupManagersRequest
from .types.compute import AggregatedListInstanceGroupsRequest
from .types.compute import AggregatedListInstancesRequest
from .types.compute import AggregatedListInterconnectAttachmentsRequest
from .types.compute import AggregatedListMachineTypesRequest
from .types.compute import AggregatedListNetworkEndpointGroupsRequest
from .types.compute import AggregatedListNodeGroupsRequest
from .types.compute import AggregatedListNodeTemplatesRequest
from .types.compute import AggregatedListNodeTypesRequest
from .types.compute import AggregatedListPacketMirroringsRequest
from .types.compute import AggregatedListPublicDelegatedPrefixesRequest
from .types.compute import AggregatedListRegionCommitmentsRequest
from .types.compute import AggregatedListReservationsRequest
from .types.compute import AggregatedListResourcePoliciesRequest
from .types.compute import AggregatedListRoutersRequest
from .types.compute import AggregatedListSslCertificatesRequest
from .types.compute import AggregatedListSubnetworksRequest
from .types.compute import AggregatedListTargetHttpProxiesRequest
from .types.compute import AggregatedListTargetHttpsProxiesRequest
from .types.compute import AggregatedListTargetInstancesRequest
from .types.compute import AggregatedListTargetPoolsRequest
from .types.compute import AggregatedListTargetVpnGatewaysRequest
from .types.compute import AggregatedListUrlMapsRequest
from .types.compute import AggregatedListVpnGatewaysRequest
from .types.compute import AggregatedListVpnTunnelsRequest
from .types.compute import AliasIpRange
from .types.compute import (
    AllocationSpecificSKUAllocationAllocatedInstancePropertiesReservedDisk,
)
from .types.compute import AllocationSpecificSKUAllocationReservedInstanceProperties
from .types.compute import AllocationSpecificSKUReservation
from .types.compute import Allowed
from .types.compute import ApplyUpdatesToInstancesInstanceGroupManagerRequest
from .types.compute import ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest
from .types.compute import AttachDiskInstanceRequest
from .types.compute import AttachedDisk
from .types.compute import AttachedDiskInitializeParams
from .types.compute import AttachNetworkEndpointsGlobalNetworkEndpointGroupRequest
from .types.compute import AttachNetworkEndpointsNetworkEndpointGroupRequest
from .types.compute import AuditConfig
from .types.compute import AuditLogConfig
from .types.compute import AuthorizationLoggingOptions
from .types.compute import Autoscaler
from .types.compute import AutoscalerAggregatedList
from .types.compute import AutoscalerList
from .types.compute import AutoscalersScopedList
from .types.compute import AutoscalerStatusDetails
from .types.compute import AutoscalingPolicy
from .types.compute import AutoscalingPolicyCpuUtilization
from .types.compute import AutoscalingPolicyCustomMetricUtilization
from .types.compute import AutoscalingPolicyLoadBalancingUtilization
from .types.compute import AutoscalingPolicyScaleInControl
from .types.compute import AutoscalingPolicyScalingSchedule
from .types.compute import Backend
from .types.compute import BackendBucket
from .types.compute import BackendBucketCdnPolicy
from .types.compute import BackendBucketCdnPolicyBypassCacheOnRequestHeader
from .types.compute import BackendBucketCdnPolicyNegativeCachingPolicy
from .types.compute import BackendBucketList
from .types.compute import BackendService
from .types.compute import BackendServiceAggregatedList
from .types.compute import BackendServiceCdnPolicy
from .types.compute import BackendServiceCdnPolicyBypassCacheOnRequestHeader
from .types.compute import BackendServiceCdnPolicyNegativeCachingPolicy
from .types.compute import BackendServiceFailoverPolicy
from .types.compute import BackendServiceGroupHealth
from .types.compute import BackendServiceIAP
from .types.compute import BackendServiceList
from .types.compute import BackendServiceLogConfig
from .types.compute import BackendServiceReference
from .types.compute import BackendServicesScopedList
from .types.compute import Binding
from .types.compute import BulkInsertInstanceRequest
from .types.compute import BulkInsertInstanceResource
from .types.compute import BulkInsertInstanceResourcePerInstanceProperties
from .types.compute import BulkInsertRegionInstanceRequest
from .types.compute import CacheInvalidationRule
from .types.compute import CacheKeyPolicy
from .types.compute import CircuitBreakers
from .types.compute import CloneRulesFirewallPolicyRequest
from .types.compute import Commitment
from .types.compute import CommitmentAggregatedList
from .types.compute import CommitmentList
from .types.compute import CommitmentsScopedList
from .types.compute import Condition
from .types.compute import ConfidentialInstanceConfig
from .types.compute import ConnectionDraining
from .types.compute import ConsistentHashLoadBalancerSettings
from .types.compute import ConsistentHashLoadBalancerSettingsHttpCookie
from .types.compute import CorsPolicy
from .types.compute import CreateInstancesInstanceGroupManagerRequest
from .types.compute import CreateInstancesRegionInstanceGroupManagerRequest
from .types.compute import CreateSnapshotDiskRequest
from .types.compute import CreateSnapshotRegionDiskRequest
from .types.compute import CustomerEncryptionKey
from .types.compute import CustomerEncryptionKeyProtectedDisk
from .types.compute import Data
from .types.compute import DeleteAccessConfigInstanceRequest
from .types.compute import DeleteAddressRequest
from .types.compute import DeleteAutoscalerRequest
from .types.compute import DeleteBackendBucketRequest
from .types.compute import DeleteBackendServiceRequest
from .types.compute import DeleteDiskRequest
from .types.compute import DeleteExternalVpnGatewayRequest
from .types.compute import DeleteFirewallPolicyRequest
from .types.compute import DeleteFirewallRequest
from .types.compute import DeleteForwardingRuleRequest
from .types.compute import DeleteGlobalAddressRequest
from .types.compute import DeleteGlobalForwardingRuleRequest
from .types.compute import DeleteGlobalNetworkEndpointGroupRequest
from .types.compute import DeleteGlobalOperationRequest
from .types.compute import DeleteGlobalOperationResponse
from .types.compute import DeleteGlobalOrganizationOperationRequest
from .types.compute import DeleteGlobalOrganizationOperationResponse
from .types.compute import DeleteGlobalPublicDelegatedPrefixeRequest
from .types.compute import DeleteHealthCheckRequest
from .types.compute import DeleteImageRequest
from .types.compute import DeleteInstanceGroupManagerRequest
from .types.compute import DeleteInstanceGroupRequest
from .types.compute import DeleteInstanceRequest
from .types.compute import DeleteInstancesInstanceGroupManagerRequest
from .types.compute import DeleteInstancesRegionInstanceGroupManagerRequest
from .types.compute import DeleteInstanceTemplateRequest
from .types.compute import DeleteInterconnectAttachmentRequest
from .types.compute import DeleteInterconnectRequest
from .types.compute import DeleteLicenseRequest
from .types.compute import DeleteNetworkEndpointGroupRequest
from .types.compute import DeleteNetworkRequest
from .types.compute import DeleteNodeGroupRequest
from .types.compute import DeleteNodesNodeGroupRequest
from .types.compute import DeleteNodeTemplateRequest
from .types.compute import DeletePacketMirroringRequest
from .types.compute import DeletePerInstanceConfigsInstanceGroupManagerRequest
from .types.compute import DeletePerInstanceConfigsRegionInstanceGroupManagerRequest
from .types.compute import DeletePublicAdvertisedPrefixeRequest
from .types.compute import DeletePublicDelegatedPrefixeRequest
from .types.compute import DeleteRegionAutoscalerRequest
from .types.compute import DeleteRegionBackendServiceRequest
from .types.compute import DeleteRegionDiskRequest
from .types.compute import DeleteRegionHealthCheckRequest
from .types.compute import DeleteRegionHealthCheckServiceRequest
from .types.compute import DeleteRegionInstanceGroupManagerRequest
from .types.compute import DeleteRegionNetworkEndpointGroupRequest
from .types.compute import DeleteRegionNotificationEndpointRequest
from .types.compute import DeleteRegionOperationRequest
from .types.compute import DeleteRegionOperationResponse
from .types.compute import DeleteRegionSslCertificateRequest
from .types.compute import DeleteRegionTargetHttpProxyRequest
from .types.compute import DeleteRegionTargetHttpsProxyRequest
from .types.compute import DeleteRegionUrlMapRequest
from .types.compute import DeleteReservationRequest
from .types.compute import DeleteResourcePolicyRequest
from .types.compute import DeleteRouteRequest
from .types.compute import DeleteRouterRequest
from .types.compute import DeleteSecurityPolicyRequest
from .types.compute import DeleteSignedUrlKeyBackendBucketRequest
from .types.compute import DeleteSignedUrlKeyBackendServiceRequest
from .types.compute import DeleteSnapshotRequest
from .types.compute import DeleteSslCertificateRequest
from .types.compute import DeleteSslPolicyRequest
from .types.compute import DeleteSubnetworkRequest
from .types.compute import DeleteTargetGrpcProxyRequest
from .types.compute import DeleteTargetHttpProxyRequest
from .types.compute import DeleteTargetHttpsProxyRequest
from .types.compute import DeleteTargetInstanceRequest
from .types.compute import DeleteTargetPoolRequest
from .types.compute import DeleteTargetSslProxyRequest
from .types.compute import DeleteTargetTcpProxyRequest
from .types.compute import DeleteTargetVpnGatewayRequest
from .types.compute import DeleteUrlMapRequest
from .types.compute import DeleteVpnGatewayRequest
from .types.compute import DeleteVpnTunnelRequest
from .types.compute import DeleteZoneOperationRequest
from .types.compute import DeleteZoneOperationResponse
from .types.compute import Denied
from .types.compute import DeprecateImageRequest
from .types.compute import DeprecationStatus
from .types.compute import DetachDiskInstanceRequest
from .types.compute import DetachNetworkEndpointsGlobalNetworkEndpointGroupRequest
from .types.compute import DetachNetworkEndpointsNetworkEndpointGroupRequest
from .types.compute import DisableXpnHostProjectRequest
from .types.compute import DisableXpnResourceProjectRequest
from .types.compute import Disk
from .types.compute import DiskAggregatedList
from .types.compute import DiskInstantiationConfig
from .types.compute import DiskList
from .types.compute import DiskMoveRequest
from .types.compute import DisksAddResourcePoliciesRequest
from .types.compute import DisksRemoveResourcePoliciesRequest
from .types.compute import DisksResizeRequest
from .types.compute import DisksScopedList
from .types.compute import DiskType
from .types.compute import DiskTypeAggregatedList
from .types.compute import DiskTypeList
from .types.compute import DiskTypesScopedList
from .types.compute import DisplayDevice
from .types.compute import DistributionPolicy
from .types.compute import DistributionPolicyZoneConfiguration
from .types.compute import Duration
from .types.compute import EnableXpnHostProjectRequest
from .types.compute import EnableXpnResourceProjectRequest
from .types.compute import Error
from .types.compute import Errors
from .types.compute import ExchangedPeeringRoute
from .types.compute import ExchangedPeeringRoutesList
from .types.compute import ExpandIpCidrRangeSubnetworkRequest
from .types.compute import Expr
from .types.compute import ExternalVpnGateway
from .types.compute import ExternalVpnGatewayInterface
from .types.compute import ExternalVpnGatewayList
from .types.compute import FileContentBuffer
from .types.compute import Firewall
from .types.compute import FirewallList
from .types.compute import FirewallLogConfig
from .types.compute import FirewallPoliciesListAssociationsResponse
from .types.compute import FirewallPolicy
from .types.compute import FirewallPolicyAssociation
from .types.compute import FirewallPolicyList
from .types.compute import FirewallPolicyRule
from .types.compute import FirewallPolicyRuleMatcher
from .types.compute import FirewallPolicyRuleMatcherLayer4Config
from .types.compute import FixedOrPercent
from .types.compute import ForwardingRule
from .types.compute import ForwardingRuleAggregatedList
from .types.compute import ForwardingRuleList
from .types.compute import ForwardingRuleReference
from .types.compute import ForwardingRuleServiceDirectoryRegistration
from .types.compute import ForwardingRulesScopedList
from .types.compute import GetAcceleratorTypeRequest
from .types.compute import GetAddressRequest
from .types.compute import GetAssociationFirewallPolicyRequest
from .types.compute import GetAutoscalerRequest
from .types.compute import GetBackendBucketRequest
from .types.compute import GetBackendServiceRequest
from .types.compute import GetDiagnosticsInterconnectRequest
from .types.compute import GetDiskRequest
from .types.compute import GetDiskTypeRequest
from .types.compute import GetEffectiveFirewallsInstanceRequest
from .types.compute import GetEffectiveFirewallsNetworkRequest
from .types.compute import GetExternalVpnGatewayRequest
from .types.compute import GetFirewallPolicyRequest
from .types.compute import GetFirewallRequest
from .types.compute import GetForwardingRuleRequest
from .types.compute import GetFromFamilyImageRequest
from .types.compute import GetGlobalAddressRequest
from .types.compute import GetGlobalForwardingRuleRequest
from .types.compute import GetGlobalNetworkEndpointGroupRequest
from .types.compute import GetGlobalOperationRequest
from .types.compute import GetGlobalOrganizationOperationRequest
from .types.compute import GetGlobalPublicDelegatedPrefixeRequest
from .types.compute import GetGuestAttributesInstanceRequest
from .types.compute import GetHealthBackendServiceRequest
from .types.compute import GetHealthCheckRequest
from .types.compute import GetHealthRegionBackendServiceRequest
from .types.compute import GetHealthTargetPoolRequest
from .types.compute import GetIamPolicyDiskRequest
from .types.compute import GetIamPolicyFirewallPolicyRequest
from .types.compute import GetIamPolicyImageRequest
from .types.compute import GetIamPolicyInstanceRequest
from .types.compute import GetIamPolicyInstanceTemplateRequest
from .types.compute import GetIamPolicyLicenseRequest
from .types.compute import GetIamPolicyNodeGroupRequest
from .types.compute import GetIamPolicyNodeTemplateRequest
from .types.compute import GetIamPolicyRegionDiskRequest
from .types.compute import GetIamPolicyReservationRequest
from .types.compute import GetIamPolicyResourcePolicyRequest
from .types.compute import GetIamPolicySnapshotRequest
from .types.compute import GetIamPolicySubnetworkRequest
from .types.compute import GetImageRequest
from .types.compute import GetInstanceGroupManagerRequest
from .types.compute import GetInstanceGroupRequest
from .types.compute import GetInstanceRequest
from .types.compute import GetInstanceTemplateRequest
from .types.compute import GetInterconnectAttachmentRequest
from .types.compute import GetInterconnectLocationRequest
from .types.compute import GetInterconnectRequest
from .types.compute import GetLicenseCodeRequest
from .types.compute import GetLicenseRequest
from .types.compute import GetMachineTypeRequest
from .types.compute import GetNatMappingInfoRoutersRequest
from .types.compute import GetNetworkEndpointGroupRequest
from .types.compute import GetNetworkRequest
from .types.compute import GetNodeGroupRequest
from .types.compute import GetNodeTemplateRequest
from .types.compute import GetNodeTypeRequest
from .types.compute import GetPacketMirroringRequest
from .types.compute import GetProjectRequest
from .types.compute import GetPublicAdvertisedPrefixeRequest
from .types.compute import GetPublicDelegatedPrefixeRequest
from .types.compute import GetRegionAutoscalerRequest
from .types.compute import GetRegionBackendServiceRequest
from .types.compute import GetRegionCommitmentRequest
from .types.compute import GetRegionDiskRequest
from .types.compute import GetRegionDiskTypeRequest
from .types.compute import GetRegionHealthCheckRequest
from .types.compute import GetRegionHealthCheckServiceRequest
from .types.compute import GetRegionInstanceGroupManagerRequest
from .types.compute import GetRegionInstanceGroupRequest
from .types.compute import GetRegionNetworkEndpointGroupRequest
from .types.compute import GetRegionNotificationEndpointRequest
from .types.compute import GetRegionOperationRequest
from .types.compute import GetRegionRequest
from .types.compute import GetRegionSslCertificateRequest
from .types.compute import GetRegionTargetHttpProxyRequest
from .types.compute import GetRegionTargetHttpsProxyRequest
from .types.compute import GetRegionUrlMapRequest
from .types.compute import GetReservationRequest
from .types.compute import GetResourcePolicyRequest
from .types.compute import GetRouteRequest
from .types.compute import GetRouterRequest
from .types.compute import GetRouterStatusRouterRequest
from .types.compute import GetRuleFirewallPolicyRequest
from .types.compute import GetRuleSecurityPolicyRequest
from .types.compute import GetScreenshotInstanceRequest
from .types.compute import GetSecurityPolicyRequest
from .types.compute import GetSerialPortOutputInstanceRequest
from .types.compute import GetShieldedInstanceIdentityInstanceRequest
from .types.compute import GetSnapshotRequest
from .types.compute import GetSslCertificateRequest
from .types.compute import GetSslPolicyRequest
from .types.compute import GetStatusVpnGatewayRequest
from .types.compute import GetSubnetworkRequest
from .types.compute import GetTargetGrpcProxyRequest
from .types.compute import GetTargetHttpProxyRequest
from .types.compute import GetTargetHttpsProxyRequest
from .types.compute import GetTargetInstanceRequest
from .types.compute import GetTargetPoolRequest
from .types.compute import GetTargetSslProxyRequest
from .types.compute import GetTargetTcpProxyRequest
from .types.compute import GetTargetVpnGatewayRequest
from .types.compute import GetUrlMapRequest
from .types.compute import GetVpnGatewayRequest
from .types.compute import GetVpnTunnelRequest
from .types.compute import GetXpnHostProjectRequest
from .types.compute import GetXpnResourcesProjectsRequest
from .types.compute import GetZoneOperationRequest
from .types.compute import GetZoneRequest
from .types.compute import GlobalNetworkEndpointGroupsAttachEndpointsRequest
from .types.compute import GlobalNetworkEndpointGroupsDetachEndpointsRequest
from .types.compute import GlobalOrganizationSetPolicyRequest
from .types.compute import GlobalSetLabelsRequest
from .types.compute import GlobalSetPolicyRequest
from .types.compute import GRPCHealthCheck
from .types.compute import GuestAttributes
from .types.compute import GuestAttributesEntry
from .types.compute import GuestAttributesValue
from .types.compute import GuestOsFeature
from .types.compute import HealthCheck
from .types.compute import HealthCheckList
from .types.compute import HealthCheckLogConfig
from .types.compute import HealthCheckReference
from .types.compute import HealthChecksAggregatedList
from .types.compute import HealthCheckService
from .types.compute import HealthCheckServiceReference
from .types.compute import HealthCheckServicesList
from .types.compute import HealthChecksScopedList
from .types.compute import HealthStatus
from .types.compute import HealthStatusForNetworkEndpoint
from .types.compute import HostRule
from .types.compute import HTTP2HealthCheck
from .types.compute import HttpFaultAbort
from .types.compute import HttpFaultDelay
from .types.compute import HttpFaultInjection
from .types.compute import HttpHeaderAction
from .types.compute import HttpHeaderMatch
from .types.compute import HttpHeaderOption
from .types.compute import HTTPHealthCheck
from .types.compute import HttpQueryParameterMatch
from .types.compute import HttpRedirectAction
from .types.compute import HttpRetryPolicy
from .types.compute import HttpRouteAction
from .types.compute import HttpRouteRule
from .types.compute import HttpRouteRuleMatch
from .types.compute import HTTPSHealthCheck
from .types.compute import Image
from .types.compute import ImageList
from .types.compute import InitialStateConfig
from .types.compute import InsertAddressRequest
from .types.compute import InsertAutoscalerRequest
from .types.compute import InsertBackendBucketRequest
from .types.compute import InsertBackendServiceRequest
from .types.compute import InsertDiskRequest
from .types.compute import InsertExternalVpnGatewayRequest
from .types.compute import InsertFirewallPolicyRequest
from .types.compute import InsertFirewallRequest
from .types.compute import InsertForwardingRuleRequest
from .types.compute import InsertGlobalAddressRequest
from .types.compute import InsertGlobalForwardingRuleRequest
from .types.compute import InsertGlobalNetworkEndpointGroupRequest
from .types.compute import InsertGlobalPublicDelegatedPrefixeRequest
from .types.compute import InsertHealthCheckRequest
from .types.compute import InsertImageRequest
from .types.compute import InsertInstanceGroupManagerRequest
from .types.compute import InsertInstanceGroupRequest
from .types.compute import InsertInstanceRequest
from .types.compute import InsertInstanceTemplateRequest
from .types.compute import InsertInterconnectAttachmentRequest
from .types.compute import InsertInterconnectRequest
from .types.compute import InsertLicenseRequest
from .types.compute import InsertNetworkEndpointGroupRequest
from .types.compute import InsertNetworkRequest
from .types.compute import InsertNodeGroupRequest
from .types.compute import InsertNodeTemplateRequest
from .types.compute import InsertPacketMirroringRequest
from .types.compute import InsertPublicAdvertisedPrefixeRequest
from .types.compute import InsertPublicDelegatedPrefixeRequest
from .types.compute import InsertRegionAutoscalerRequest
from .types.compute import InsertRegionBackendServiceRequest
from .types.compute import InsertRegionCommitmentRequest
from .types.compute import InsertRegionDiskRequest
from .types.compute import InsertRegionHealthCheckRequest
from .types.compute import InsertRegionHealthCheckServiceRequest
from .types.compute import InsertRegionInstanceGroupManagerRequest
from .types.compute import InsertRegionNetworkEndpointGroupRequest
from .types.compute import InsertRegionNotificationEndpointRequest
from .types.compute import InsertRegionSslCertificateRequest
from .types.compute import InsertRegionTargetHttpProxyRequest
from .types.compute import InsertRegionTargetHttpsProxyRequest
from .types.compute import InsertRegionUrlMapRequest
from .types.compute import InsertReservationRequest
from .types.compute import InsertResourcePolicyRequest
from .types.compute import InsertRouteRequest
from .types.compute import InsertRouterRequest
from .types.compute import InsertSecurityPolicyRequest
from .types.compute import InsertSslCertificateRequest
from .types.compute import InsertSslPolicyRequest
from .types.compute import InsertSubnetworkRequest
from .types.compute import InsertTargetGrpcProxyRequest
from .types.compute import InsertTargetHttpProxyRequest
from .types.compute import InsertTargetHttpsProxyRequest
from .types.compute import InsertTargetInstanceRequest
from .types.compute import InsertTargetPoolRequest
from .types.compute import InsertTargetSslProxyRequest
from .types.compute import InsertTargetTcpProxyRequest
from .types.compute import InsertTargetVpnGatewayRequest
from .types.compute import InsertUrlMapRequest
from .types.compute import InsertVpnGatewayRequest
from .types.compute import InsertVpnTunnelRequest
from .types.compute import Instance
from .types.compute import InstanceAggregatedList
from .types.compute import InstanceGroup
from .types.compute import InstanceGroupAggregatedList
from .types.compute import InstanceGroupList
from .types.compute import InstanceGroupManager
from .types.compute import InstanceGroupManagerActionsSummary
from .types.compute import InstanceGroupManagerAggregatedList
from .types.compute import InstanceGroupManagerAutoHealingPolicy
from .types.compute import InstanceGroupManagerList
from .types.compute import InstanceGroupManagersAbandonInstancesRequest
from .types.compute import InstanceGroupManagersApplyUpdatesRequest
from .types.compute import InstanceGroupManagersCreateInstancesRequest
from .types.compute import InstanceGroupManagersDeleteInstancesRequest
from .types.compute import InstanceGroupManagersDeletePerInstanceConfigsReq
from .types.compute import InstanceGroupManagersListErrorsResponse
from .types.compute import InstanceGroupManagersListManagedInstancesResponse
from .types.compute import InstanceGroupManagersListPerInstanceConfigsResp
from .types.compute import InstanceGroupManagersPatchPerInstanceConfigsReq
from .types.compute import InstanceGroupManagersRecreateInstancesRequest
from .types.compute import InstanceGroupManagersScopedList
from .types.compute import InstanceGroupManagersSetInstanceTemplateRequest
from .types.compute import InstanceGroupManagersSetTargetPoolsRequest
from .types.compute import InstanceGroupManagerStatus
from .types.compute import InstanceGroupManagerStatusStateful
from .types.compute import InstanceGroupManagerStatusStatefulPerInstanceConfigs
from .types.compute import InstanceGroupManagerStatusVersionTarget
from .types.compute import InstanceGroupManagersUpdatePerInstanceConfigsReq
from .types.compute import InstanceGroupManagerUpdatePolicy
from .types.compute import InstanceGroupManagerVersion
from .types.compute import InstanceGroupsAddInstancesRequest
from .types.compute import InstanceGroupsListInstances
from .types.compute import InstanceGroupsListInstancesRequest
from .types.compute import InstanceGroupsRemoveInstancesRequest
from .types.compute import InstanceGroupsScopedList
from .types.compute import InstanceGroupsSetNamedPortsRequest
from .types.compute import InstanceList
from .types.compute import InstanceListReferrers
from .types.compute import InstanceManagedByIgmError
from .types.compute import InstanceManagedByIgmErrorInstanceActionDetails
from .types.compute import InstanceManagedByIgmErrorManagedInstanceError
from .types.compute import InstanceMoveRequest
from .types.compute import InstanceProperties
from .types.compute import InstanceReference
from .types.compute import InstancesAddResourcePoliciesRequest
from .types.compute import InstancesGetEffectiveFirewallsResponse
from .types.compute import InstancesGetEffectiveFirewallsResponseEffectiveFirewallPolicy
from .types.compute import InstancesRemoveResourcePoliciesRequest
from .types.compute import InstancesScopedList
from .types.compute import InstancesSetLabelsRequest
from .types.compute import InstancesSetMachineResourcesRequest
from .types.compute import InstancesSetMachineTypeRequest
from .types.compute import InstancesSetMinCpuPlatformRequest
from .types.compute import InstancesSetServiceAccountRequest
from .types.compute import InstancesStartWithEncryptionKeyRequest
from .types.compute import InstanceTemplate
from .types.compute import InstanceTemplateList
from .types.compute import InstanceWithNamedPorts
from .types.compute import Int64RangeMatch
from .types.compute import Interconnect
from .types.compute import InterconnectAttachment
from .types.compute import InterconnectAttachmentAggregatedList
from .types.compute import InterconnectAttachmentList
from .types.compute import InterconnectAttachmentPartnerMetadata
from .types.compute import InterconnectAttachmentPrivateInfo
from .types.compute import InterconnectAttachmentsScopedList
from .types.compute import InterconnectCircuitInfo
from .types.compute import InterconnectDiagnostics
from .types.compute import InterconnectDiagnosticsARPEntry
from .types.compute import InterconnectDiagnosticsLinkLACPStatus
from .types.compute import InterconnectDiagnosticsLinkOpticalPower
from .types.compute import InterconnectDiagnosticsLinkStatus
from .types.compute import InterconnectList
from .types.compute import InterconnectLocation
from .types.compute import InterconnectLocationList
from .types.compute import InterconnectLocationRegionInfo
from .types.compute import InterconnectOutageNotification
from .types.compute import InterconnectsGetDiagnosticsResponse
from .types.compute import InvalidateCacheUrlMapRequest
from .types.compute import Items
from .types.compute import License
from .types.compute import LicenseCode
from .types.compute import LicenseCodeLicenseAlias
from .types.compute import LicenseResourceCommitment
from .types.compute import LicenseResourceRequirements
from .types.compute import LicensesListResponse
from .types.compute import ListAcceleratorTypesRequest
from .types.compute import ListAddressesRequest
from .types.compute import ListAssociationsFirewallPolicyRequest
from .types.compute import ListAutoscalersRequest
from .types.compute import ListAvailableFeaturesSslPoliciesRequest
from .types.compute import ListBackendBucketsRequest
from .types.compute import ListBackendServicesRequest
from .types.compute import ListDisksRequest
from .types.compute import ListDiskTypesRequest
from .types.compute import ListErrorsInstanceGroupManagersRequest
from .types.compute import ListErrorsRegionInstanceGroupManagersRequest
from .types.compute import ListExternalVpnGatewaysRequest
from .types.compute import ListFirewallPoliciesRequest
from .types.compute import ListFirewallsRequest
from .types.compute import ListForwardingRulesRequest
from .types.compute import ListGlobalAddressesRequest
from .types.compute import ListGlobalForwardingRulesRequest
from .types.compute import ListGlobalNetworkEndpointGroupsRequest
from .types.compute import ListGlobalOperationsRequest
from .types.compute import ListGlobalOrganizationOperationsRequest
from .types.compute import ListGlobalPublicDelegatedPrefixesRequest
from .types.compute import ListHealthChecksRequest
from .types.compute import ListImagesRequest
from .types.compute import ListInstanceGroupManagersRequest
from .types.compute import ListInstanceGroupsRequest
from .types.compute import ListInstancesInstanceGroupsRequest
from .types.compute import ListInstancesRegionInstanceGroupsRequest
from .types.compute import ListInstancesRequest
from .types.compute import ListInstanceTemplatesRequest
from .types.compute import ListInterconnectAttachmentsRequest
from .types.compute import ListInterconnectLocationsRequest
from .types.compute import ListInterconnectsRequest
from .types.compute import ListLicensesRequest
from .types.compute import ListMachineTypesRequest
from .types.compute import ListManagedInstancesInstanceGroupManagersRequest
from .types.compute import ListManagedInstancesRegionInstanceGroupManagersRequest
from .types.compute import ListNetworkEndpointGroupsRequest
from .types.compute import ListNetworkEndpointsGlobalNetworkEndpointGroupsRequest
from .types.compute import ListNetworkEndpointsNetworkEndpointGroupsRequest
from .types.compute import ListNetworksRequest
from .types.compute import ListNodeGroupsRequest
from .types.compute import ListNodesNodeGroupsRequest
from .types.compute import ListNodeTemplatesRequest
from .types.compute import ListNodeTypesRequest
from .types.compute import ListPacketMirroringsRequest
from .types.compute import ListPeeringRoutesNetworksRequest
from .types.compute import ListPerInstanceConfigsInstanceGroupManagersRequest
from .types.compute import ListPerInstanceConfigsRegionInstanceGroupManagersRequest
from .types.compute import ListPreconfiguredExpressionSetsSecurityPoliciesRequest
from .types.compute import ListPublicAdvertisedPrefixesRequest
from .types.compute import ListPublicDelegatedPrefixesRequest
from .types.compute import ListReferrersInstancesRequest
from .types.compute import ListRegionAutoscalersRequest
from .types.compute import ListRegionBackendServicesRequest
from .types.compute import ListRegionCommitmentsRequest
from .types.compute import ListRegionDisksRequest
from .types.compute import ListRegionDiskTypesRequest
from .types.compute import ListRegionHealthCheckServicesRequest
from .types.compute import ListRegionHealthChecksRequest
from .types.compute import ListRegionInstanceGroupManagersRequest
from .types.compute import ListRegionInstanceGroupsRequest
from .types.compute import ListRegionNetworkEndpointGroupsRequest
from .types.compute import ListRegionNotificationEndpointsRequest
from .types.compute import ListRegionOperationsRequest
from .types.compute import ListRegionsRequest
from .types.compute import ListRegionSslCertificatesRequest
from .types.compute import ListRegionTargetHttpProxiesRequest
from .types.compute import ListRegionTargetHttpsProxiesRequest
from .types.compute import ListRegionUrlMapsRequest
from .types.compute import ListReservationsRequest
from .types.compute import ListResourcePoliciesRequest
from .types.compute import ListRoutersRequest
from .types.compute import ListRoutesRequest
from .types.compute import ListSecurityPoliciesRequest
from .types.compute import ListSnapshotsRequest
from .types.compute import ListSslCertificatesRequest
from .types.compute import ListSslPoliciesRequest
from .types.compute import ListSubnetworksRequest
from .types.compute import ListTargetGrpcProxiesRequest
from .types.compute import ListTargetHttpProxiesRequest
from .types.compute import ListTargetHttpsProxiesRequest
from .types.compute import ListTargetInstancesRequest
from .types.compute import ListTargetPoolsRequest
from .types.compute import ListTargetSslProxiesRequest
from .types.compute import ListTargetTcpProxiesRequest
from .types.compute import ListTargetVpnGatewaysRequest
from .types.compute import ListUrlMapsRequest
from .types.compute import ListUsableSubnetworksRequest
from .types.compute import ListVpnGatewaysRequest
from .types.compute import ListVpnTunnelsRequest
from .types.compute import ListXpnHostsProjectsRequest
from .types.compute import ListZoneOperationsRequest
from .types.compute import ListZonesRequest
from .types.compute import LocalDisk
from .types.compute import LocationPolicy
from .types.compute import LocationPolicyLocation
from .types.compute import LogConfig
from .types.compute import LogConfigCloudAuditOptions
from .types.compute import LogConfigCounterOptions
from .types.compute import LogConfigCounterOptionsCustomField
from .types.compute import LogConfigDataAccessOptions
from .types.compute import MachineType
from .types.compute import MachineTypeAggregatedList
from .types.compute import MachineTypeList
from .types.compute import MachineTypesScopedList
from .types.compute import ManagedInstance
from .types.compute import ManagedInstanceInstanceHealth
from .types.compute import ManagedInstanceLastAttempt
from .types.compute import ManagedInstanceVersion
from .types.compute import Metadata
from .types.compute import MetadataFilter
from .types.compute import MetadataFilterLabelMatch
from .types.compute import MoveDiskProjectRequest
from .types.compute import MoveFirewallPolicyRequest
from .types.compute import MoveInstanceProjectRequest
from .types.compute import NamedPort
from .types.compute import Network
from .types.compute import NetworkEndpoint
from .types.compute import NetworkEndpointGroup
from .types.compute import NetworkEndpointGroupAggregatedList
from .types.compute import NetworkEndpointGroupAppEngine
from .types.compute import NetworkEndpointGroupCloudFunction
from .types.compute import NetworkEndpointGroupCloudRun
from .types.compute import NetworkEndpointGroupList
from .types.compute import NetworkEndpointGroupsAttachEndpointsRequest
from .types.compute import NetworkEndpointGroupsDetachEndpointsRequest
from .types.compute import NetworkEndpointGroupsListEndpointsRequest
from .types.compute import NetworkEndpointGroupsListNetworkEndpoints
from .types.compute import NetworkEndpointGroupsScopedList
from .types.compute import NetworkEndpointWithHealthStatus
from .types.compute import NetworkInterface
from .types.compute import NetworkList
from .types.compute import NetworkPeering
from .types.compute import NetworkRoutingConfig
from .types.compute import NetworksAddPeeringRequest
from .types.compute import NetworksGetEffectiveFirewallsResponse
from .types.compute import NetworksGetEffectiveFirewallsResponseEffectiveFirewallPolicy
from .types.compute import NetworksRemovePeeringRequest
from .types.compute import NetworksUpdatePeeringRequest
from .types.compute import NodeGroup
from .types.compute import NodeGroupAggregatedList
from .types.compute import NodeGroupAutoscalingPolicy
from .types.compute import NodeGroupList
from .types.compute import NodeGroupMaintenanceWindow
from .types.compute import NodeGroupNode
from .types.compute import NodeGroupsAddNodesRequest
from .types.compute import NodeGroupsDeleteNodesRequest
from .types.compute import NodeGroupsListNodes
from .types.compute import NodeGroupsScopedList
from .types.compute import NodeGroupsSetNodeTemplateRequest
from .types.compute import NodeTemplate
from .types.compute import NodeTemplateAggregatedList
from .types.compute import NodeTemplateList
from .types.compute import NodeTemplateNodeTypeFlexibility
from .types.compute import NodeTemplatesScopedList
from .types.compute import NodeType
from .types.compute import NodeTypeAggregatedList
from .types.compute import NodeTypeList
from .types.compute import NodeTypesScopedList
from .types.compute import NotificationEndpoint
from .types.compute import NotificationEndpointGrpcSettings
from .types.compute import NotificationEndpointList
from .types.compute import Operation
from .types.compute import OperationAggregatedList
from .types.compute import OperationList
from .types.compute import OperationsScopedList
from .types.compute import OutlierDetection
from .types.compute import PacketMirroring
from .types.compute import PacketMirroringAggregatedList
from .types.compute import PacketMirroringFilter
from .types.compute import PacketMirroringForwardingRuleInfo
from .types.compute import PacketMirroringList
from .types.compute import PacketMirroringMirroredResourceInfo
from .types.compute import PacketMirroringMirroredResourceInfoInstanceInfo
from .types.compute import PacketMirroringMirroredResourceInfoSubnetInfo
from .types.compute import PacketMirroringNetworkInfo
from .types.compute import PacketMirroringsScopedList
from .types.compute import PatchAutoscalerRequest
from .types.compute import PatchBackendBucketRequest
from .types.compute import PatchBackendServiceRequest
from .types.compute import PatchFirewallPolicyRequest
from .types.compute import PatchFirewallRequest
from .types.compute import PatchForwardingRuleRequest
from .types.compute import PatchGlobalForwardingRuleRequest
from .types.compute import PatchGlobalPublicDelegatedPrefixeRequest
from .types.compute import PatchHealthCheckRequest
from .types.compute import PatchImageRequest
from .types.compute import PatchInstanceGroupManagerRequest
from .types.compute import PatchInterconnectAttachmentRequest
from .types.compute import PatchInterconnectRequest
from .types.compute import PatchNetworkRequest
from .types.compute import PatchNodeGroupRequest
from .types.compute import PatchPacketMirroringRequest
from .types.compute import PatchPerInstanceConfigsInstanceGroupManagerRequest
from .types.compute import PatchPerInstanceConfigsRegionInstanceGroupManagerRequest
from .types.compute import PatchPublicAdvertisedPrefixeRequest
from .types.compute import PatchPublicDelegatedPrefixeRequest
from .types.compute import PatchRegionAutoscalerRequest
from .types.compute import PatchRegionBackendServiceRequest
from .types.compute import PatchRegionHealthCheckRequest
from .types.compute import PatchRegionHealthCheckServiceRequest
from .types.compute import PatchRegionInstanceGroupManagerRequest
from .types.compute import PatchRegionUrlMapRequest
from .types.compute import PatchRouterRequest
from .types.compute import PatchRuleFirewallPolicyRequest
from .types.compute import PatchRuleSecurityPolicyRequest
from .types.compute import PatchSecurityPolicyRequest
from .types.compute import PatchSslPolicyRequest
from .types.compute import PatchSubnetworkRequest
from .types.compute import PatchTargetGrpcProxyRequest
from .types.compute import PatchTargetHttpProxyRequest
from .types.compute import PatchTargetHttpsProxyRequest
from .types.compute import PatchUrlMapRequest
from .types.compute import PathMatcher
from .types.compute import PathRule
from .types.compute import PerInstanceConfig
from .types.compute import Policy
from .types.compute import PreconfiguredWafSet
from .types.compute import PreservedState
from .types.compute import PreservedStatePreservedDisk
from .types.compute import PreviewRouterRequest
from .types.compute import Project
from .types.compute import ProjectsDisableXpnResourceRequest
from .types.compute import ProjectsEnableXpnResourceRequest
from .types.compute import ProjectsGetXpnResources
from .types.compute import ProjectsListXpnHostsRequest
from .types.compute import ProjectsSetDefaultNetworkTierRequest
from .types.compute import PublicAdvertisedPrefix
from .types.compute import PublicAdvertisedPrefixList
from .types.compute import PublicAdvertisedPrefixPublicDelegatedPrefix
from .types.compute import PublicDelegatedPrefix
from .types.compute import PublicDelegatedPrefixAggregatedList
from .types.compute import PublicDelegatedPrefixesScopedList
from .types.compute import PublicDelegatedPrefixList
from .types.compute import PublicDelegatedPrefixPublicDelegatedSubPrefix
from .types.compute import Quota
from .types.compute import RawDisk
from .types.compute import RecreateInstancesInstanceGroupManagerRequest
from .types.compute import RecreateInstancesRegionInstanceGroupManagerRequest
from .types.compute import Reference
from .types.compute import Region
from .types.compute import RegionAutoscalerList
from .types.compute import RegionDisksAddResourcePoliciesRequest
from .types.compute import RegionDisksRemoveResourcePoliciesRequest
from .types.compute import RegionDisksResizeRequest
from .types.compute import RegionDiskTypeList
from .types.compute import RegionInstanceGroupList
from .types.compute import RegionInstanceGroupManagerDeleteInstanceConfigReq
from .types.compute import RegionInstanceGroupManagerList
from .types.compute import RegionInstanceGroupManagerPatchInstanceConfigReq
from .types.compute import RegionInstanceGroupManagersAbandonInstancesRequest
from .types.compute import RegionInstanceGroupManagersApplyUpdatesRequest
from .types.compute import RegionInstanceGroupManagersCreateInstancesRequest
from .types.compute import RegionInstanceGroupManagersDeleteInstancesRequest
from .types.compute import RegionInstanceGroupManagersListErrorsResponse
from .types.compute import RegionInstanceGroupManagersListInstanceConfigsResp
from .types.compute import RegionInstanceGroupManagersListInstancesResponse
from .types.compute import RegionInstanceGroupManagersRecreateRequest
from .types.compute import RegionInstanceGroupManagersSetTargetPoolsRequest
from .types.compute import RegionInstanceGroupManagersSetTemplateRequest
from .types.compute import RegionInstanceGroupManagerUpdateInstanceConfigReq
from .types.compute import RegionInstanceGroupsListInstances
from .types.compute import RegionInstanceGroupsListInstancesRequest
from .types.compute import RegionInstanceGroupsSetNamedPortsRequest
from .types.compute import RegionList
from .types.compute import RegionSetLabelsRequest
from .types.compute import RegionSetPolicyRequest
from .types.compute import RegionTargetHttpsProxiesSetSslCertificatesRequest
from .types.compute import RegionUrlMapsValidateRequest
from .types.compute import RemoveAssociationFirewallPolicyRequest
from .types.compute import RemoveHealthCheckTargetPoolRequest
from .types.compute import RemoveInstancesInstanceGroupRequest
from .types.compute import RemoveInstanceTargetPoolRequest
from .types.compute import RemovePeeringNetworkRequest
from .types.compute import RemoveResourcePoliciesDiskRequest
from .types.compute import RemoveResourcePoliciesInstanceRequest
from .types.compute import RemoveResourcePoliciesRegionDiskRequest
from .types.compute import RemoveRuleFirewallPolicyRequest
from .types.compute import RemoveRuleSecurityPolicyRequest
from .types.compute import RequestMirrorPolicy
from .types.compute import Reservation
from .types.compute import ReservationAffinity
from .types.compute import ReservationAggregatedList
from .types.compute import ReservationList
from .types.compute import ReservationsResizeRequest
from .types.compute import ReservationsScopedList
from .types.compute import ResetInstanceRequest
from .types.compute import ResizeDiskRequest
from .types.compute import ResizeInstanceGroupManagerRequest
from .types.compute import ResizeRegionDiskRequest
from .types.compute import ResizeRegionInstanceGroupManagerRequest
from .types.compute import ResizeReservationRequest
from .types.compute import ResourceCommitment
from .types.compute import ResourceGroupReference
from .types.compute import ResourcePoliciesScopedList
from .types.compute import ResourcePolicy
from .types.compute import ResourcePolicyAggregatedList
from .types.compute import ResourcePolicyDailyCycle
from .types.compute import ResourcePolicyGroupPlacementPolicy
from .types.compute import ResourcePolicyHourlyCycle
from .types.compute import ResourcePolicyInstanceSchedulePolicy
from .types.compute import ResourcePolicyInstanceSchedulePolicySchedule
from .types.compute import ResourcePolicyList
from .types.compute import ResourcePolicyResourceStatus
from .types.compute import ResourcePolicyResourceStatusInstanceSchedulePolicyStatus
from .types.compute import ResourcePolicySnapshotSchedulePolicy
from .types.compute import ResourcePolicySnapshotSchedulePolicyRetentionPolicy
from .types.compute import ResourcePolicySnapshotSchedulePolicySchedule
from .types.compute import ResourcePolicySnapshotSchedulePolicySnapshotProperties
from .types.compute import ResourcePolicyWeeklyCycle
from .types.compute import ResourcePolicyWeeklyCycleDayOfWeek
from .types.compute import Route
from .types.compute import RouteList
from .types.compute import Router
from .types.compute import RouterAdvertisedIpRange
from .types.compute import RouterAggregatedList
from .types.compute import RouterBgp
from .types.compute import RouterBgpPeer
from .types.compute import RouterInterface
from .types.compute import RouterList
from .types.compute import RouterNat
from .types.compute import RouterNatLogConfig
from .types.compute import RouterNatSubnetworkToNat
from .types.compute import RoutersPreviewResponse
from .types.compute import RoutersScopedList
from .types.compute import RouterStatus
from .types.compute import RouterStatusBgpPeerStatus
from .types.compute import RouterStatusNatStatus
from .types.compute import RouterStatusResponse
from .types.compute import Rule
from .types.compute import ScalingScheduleStatus
from .types.compute import Scheduling
from .types.compute import SchedulingNodeAffinity
from .types.compute import ScratchDisks
from .types.compute import Screenshot
from .types.compute import SecurityPoliciesListPreconfiguredExpressionSetsResponse
from .types.compute import SecurityPoliciesWafConfig
from .types.compute import SecurityPolicy
from .types.compute import SecurityPolicyList
from .types.compute import SecurityPolicyReference
from .types.compute import SecurityPolicyRule
from .types.compute import SecurityPolicyRuleMatcher
from .types.compute import SecurityPolicyRuleMatcherConfig
from .types.compute import SecuritySettings
from .types.compute import SerialPortOutput
from .types.compute import ServerBinding
from .types.compute import ServiceAccount
from .types.compute import SetBackendServiceTargetSslProxyRequest
from .types.compute import SetBackendServiceTargetTcpProxyRequest
from .types.compute import SetBackupTargetPoolRequest
from .types.compute import SetCommonInstanceMetadataProjectRequest
from .types.compute import SetDefaultNetworkTierProjectRequest
from .types.compute import SetDeletionProtectionInstanceRequest
from .types.compute import SetDiskAutoDeleteInstanceRequest
from .types.compute import SetIamPolicyDiskRequest
from .types.compute import SetIamPolicyFirewallPolicyRequest
from .types.compute import SetIamPolicyImageRequest
from .types.compute import SetIamPolicyInstanceRequest
from .types.compute import SetIamPolicyInstanceTemplateRequest
from .types.compute import SetIamPolicyLicenseRequest
from .types.compute import SetIamPolicyNodeGroupRequest
from .types.compute import SetIamPolicyNodeTemplateRequest
from .types.compute import SetIamPolicyRegionDiskRequest
from .types.compute import SetIamPolicyReservationRequest
from .types.compute import SetIamPolicyResourcePolicyRequest
from .types.compute import SetIamPolicySnapshotRequest
from .types.compute import SetIamPolicySubnetworkRequest
from .types.compute import SetInstanceTemplateInstanceGroupManagerRequest
from .types.compute import SetInstanceTemplateRegionInstanceGroupManagerRequest
from .types.compute import SetLabelsDiskRequest
from .types.compute import SetLabelsExternalVpnGatewayRequest
from .types.compute import SetLabelsForwardingRuleRequest
from .types.compute import SetLabelsGlobalForwardingRuleRequest
from .types.compute import SetLabelsImageRequest
from .types.compute import SetLabelsInstanceRequest
from .types.compute import SetLabelsRegionDiskRequest
from .types.compute import SetLabelsSnapshotRequest
from .types.compute import SetLabelsVpnGatewayRequest
from .types.compute import SetMachineResourcesInstanceRequest
from .types.compute import SetMachineTypeInstanceRequest
from .types.compute import SetMetadataInstanceRequest
from .types.compute import SetMinCpuPlatformInstanceRequest
from .types.compute import SetNamedPortsInstanceGroupRequest
from .types.compute import SetNamedPortsRegionInstanceGroupRequest
from .types.compute import SetNodeTemplateNodeGroupRequest
from .types.compute import SetPrivateIpGoogleAccessSubnetworkRequest
from .types.compute import SetProxyHeaderTargetSslProxyRequest
from .types.compute import SetProxyHeaderTargetTcpProxyRequest
from .types.compute import SetQuicOverrideTargetHttpsProxyRequest
from .types.compute import SetSchedulingInstanceRequest
from .types.compute import SetSecurityPolicyBackendServiceRequest
from .types.compute import SetServiceAccountInstanceRequest
from .types.compute import SetShieldedInstanceIntegrityPolicyInstanceRequest
from .types.compute import SetSslCertificatesRegionTargetHttpsProxyRequest
from .types.compute import SetSslCertificatesTargetHttpsProxyRequest
from .types.compute import SetSslCertificatesTargetSslProxyRequest
from .types.compute import SetSslPolicyTargetHttpsProxyRequest
from .types.compute import SetSslPolicyTargetSslProxyRequest
from .types.compute import SetTagsInstanceRequest
from .types.compute import SetTargetForwardingRuleRequest
from .types.compute import SetTargetGlobalForwardingRuleRequest
from .types.compute import SetTargetPoolsInstanceGroupManagerRequest
from .types.compute import SetTargetPoolsRegionInstanceGroupManagerRequest
from .types.compute import SetUrlMapRegionTargetHttpProxyRequest
from .types.compute import SetUrlMapRegionTargetHttpsProxyRequest
from .types.compute import SetUrlMapTargetHttpProxyRequest
from .types.compute import SetUrlMapTargetHttpsProxyRequest
from .types.compute import SetUsageExportBucketProjectRequest
from .types.compute import ShieldedInstanceConfig
from .types.compute import ShieldedInstanceIdentity
from .types.compute import ShieldedInstanceIdentityEntry
from .types.compute import ShieldedInstanceIntegrityPolicy
from .types.compute import SignedUrlKey
from .types.compute import SimulateMaintenanceEventInstanceRequest
from .types.compute import Snapshot
from .types.compute import SnapshotList
from .types.compute import SourceInstanceParams
from .types.compute import SslCertificate
from .types.compute import SslCertificateAggregatedList
from .types.compute import SslCertificateList
from .types.compute import SslCertificateManagedSslCertificate
from .types.compute import SslCertificateSelfManagedSslCertificate
from .types.compute import SslCertificatesScopedList
from .types.compute import SSLHealthCheck
from .types.compute import SslPoliciesList
from .types.compute import SslPoliciesListAvailableFeaturesResponse
from .types.compute import SslPolicy
from .types.compute import SslPolicyReference
from .types.compute import StartInstanceRequest
from .types.compute import StartWithEncryptionKeyInstanceRequest
from .types.compute import StatefulPolicy
from .types.compute import StatefulPolicyPreservedState
from .types.compute import StatefulPolicyPreservedStateDiskDevice
from .types.compute import StopInstanceRequest
from .types.compute import Subnetwork
from .types.compute import SubnetworkAggregatedList
from .types.compute import SubnetworkList
from .types.compute import SubnetworkLogConfig
from .types.compute import SubnetworkSecondaryRange
from .types.compute import SubnetworksExpandIpCidrRangeRequest
from .types.compute import SubnetworksScopedList
from .types.compute import SubnetworksSetPrivateIpGoogleAccessRequest
from .types.compute import SwitchToCustomModeNetworkRequest
from .types.compute import Tags
from .types.compute import TargetGrpcProxy
from .types.compute import TargetGrpcProxyList
from .types.compute import TargetHttpProxiesScopedList
from .types.compute import TargetHttpProxy
from .types.compute import TargetHttpProxyAggregatedList
from .types.compute import TargetHttpProxyList
from .types.compute import TargetHttpsProxiesScopedList
from .types.compute import TargetHttpsProxiesSetQuicOverrideRequest
from .types.compute import TargetHttpsProxiesSetSslCertificatesRequest
from .types.compute import TargetHttpsProxy
from .types.compute import TargetHttpsProxyAggregatedList
from .types.compute import TargetHttpsProxyList
from .types.compute import TargetInstance
from .types.compute import TargetInstanceAggregatedList
from .types.compute import TargetInstanceList
from .types.compute import TargetInstancesScopedList
from .types.compute import TargetPool
from .types.compute import TargetPoolAggregatedList
from .types.compute import TargetPoolInstanceHealth
from .types.compute import TargetPoolList
from .types.compute import TargetPoolsAddHealthCheckRequest
from .types.compute import TargetPoolsAddInstanceRequest
from .types.compute import TargetPoolsRemoveHealthCheckRequest
from .types.compute import TargetPoolsRemoveInstanceRequest
from .types.compute import TargetPoolsScopedList
from .types.compute import TargetReference
from .types.compute import TargetSslProxiesSetBackendServiceRequest
from .types.compute import TargetSslProxiesSetProxyHeaderRequest
from .types.compute import TargetSslProxiesSetSslCertificatesRequest
from .types.compute import TargetSslProxy
from .types.compute import TargetSslProxyList
from .types.compute import TargetTcpProxiesSetBackendServiceRequest
from .types.compute import TargetTcpProxiesSetProxyHeaderRequest
from .types.compute import TargetTcpProxy
from .types.compute import TargetTcpProxyList
from .types.compute import TargetVpnGateway
from .types.compute import TargetVpnGatewayAggregatedList
from .types.compute import TargetVpnGatewayList
from .types.compute import TargetVpnGatewaysScopedList
from .types.compute import TCPHealthCheck
from .types.compute import TestFailure
from .types.compute import TestIamPermissionsDiskRequest
from .types.compute import TestIamPermissionsExternalVpnGatewayRequest
from .types.compute import TestIamPermissionsFirewallPolicyRequest
from .types.compute import TestIamPermissionsImageRequest
from .types.compute import TestIamPermissionsInstanceRequest
from .types.compute import TestIamPermissionsInstanceTemplateRequest
from .types.compute import TestIamPermissionsLicenseCodeRequest
from .types.compute import TestIamPermissionsLicenseRequest
from .types.compute import TestIamPermissionsNetworkEndpointGroupRequest
from .types.compute import TestIamPermissionsNodeGroupRequest
from .types.compute import TestIamPermissionsNodeTemplateRequest
from .types.compute import TestIamPermissionsPacketMirroringRequest
from .types.compute import TestIamPermissionsRegionDiskRequest
from .types.compute import TestIamPermissionsReservationRequest
from .types.compute import TestIamPermissionsResourcePolicyRequest
from .types.compute import TestIamPermissionsSnapshotRequest
from .types.compute import TestIamPermissionsSubnetworkRequest
from .types.compute import TestIamPermissionsVpnGatewayRequest
from .types.compute import TestPermissionsRequest
from .types.compute import TestPermissionsResponse
from .types.compute import UpdateAccessConfigInstanceRequest
from .types.compute import UpdateAutoscalerRequest
from .types.compute import UpdateBackendBucketRequest
from .types.compute import UpdateBackendServiceRequest
from .types.compute import UpdateDisplayDeviceInstanceRequest
from .types.compute import UpdateFirewallRequest
from .types.compute import UpdateHealthCheckRequest
from .types.compute import UpdateInstanceRequest
from .types.compute import UpdateNetworkInterfaceInstanceRequest
from .types.compute import UpdatePeeringNetworkRequest
from .types.compute import UpdatePerInstanceConfigsInstanceGroupManagerRequest
from .types.compute import UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest
from .types.compute import UpdateRegionAutoscalerRequest
from .types.compute import UpdateRegionBackendServiceRequest
from .types.compute import UpdateRegionHealthCheckRequest
from .types.compute import UpdateRegionUrlMapRequest
from .types.compute import UpdateRouterRequest
from .types.compute import UpdateShieldedInstanceConfigInstanceRequest
from .types.compute import UpdateUrlMapRequest
from .types.compute import UrlMap
from .types.compute import UrlMapList
from .types.compute import UrlMapReference
from .types.compute import UrlMapsAggregatedList
from .types.compute import UrlMapsScopedList
from .types.compute import UrlMapsValidateRequest
from .types.compute import UrlMapsValidateResponse
from .types.compute import UrlMapTest
from .types.compute import UrlMapTestHeader
from .types.compute import UrlMapValidationResult
from .types.compute import UrlRewrite
from .types.compute import UsableSubnetwork
from .types.compute import UsableSubnetworksAggregatedList
from .types.compute import UsableSubnetworkSecondaryRange
from .types.compute import UsageExportLocation
from .types.compute import ValidateRegionUrlMapRequest
from .types.compute import ValidateUrlMapRequest
from .types.compute import VmEndpointNatMappings
from .types.compute import VmEndpointNatMappingsInterfaceNatMappings
from .types.compute import VmEndpointNatMappingsList
from .types.compute import VpnGateway
from .types.compute import VpnGatewayAggregatedList
from .types.compute import VpnGatewayList
from .types.compute import VpnGatewaysGetStatusResponse
from .types.compute import VpnGatewaysScopedList
from .types.compute import VpnGatewayStatus
from .types.compute import VpnGatewayStatusHighAvailabilityRequirementState
from .types.compute import VpnGatewayStatusTunnel
from .types.compute import VpnGatewayStatusVpnConnection
from .types.compute import VpnGatewayVpnGatewayInterface
from .types.compute import VpnTunnel
from .types.compute import VpnTunnelAggregatedList
from .types.compute import VpnTunnelList
from .types.compute import VpnTunnelsScopedList
from .types.compute import WafExpressionSet
from .types.compute import WafExpressionSetExpression
from .types.compute import WaitGlobalOperationRequest
from .types.compute import WaitRegionOperationRequest
from .types.compute import WaitZoneOperationRequest
from .types.compute import Warning
from .types.compute import Warnings
from .types.compute import WeightedBackendService
from .types.compute import XpnHostList
from .types.compute import XpnResourceId
from .types.compute import Zone
from .types.compute import ZoneList
from .types.compute import ZoneSetLabelsRequest
from .types.compute import ZoneSetPolicyRequest

__all__ = (
    "AbandonInstancesInstanceGroupManagerRequest",
    "AbandonInstancesRegionInstanceGroupManagerRequest",
    "AcceleratorConfig",
    "AcceleratorType",
    "AcceleratorTypeAggregatedList",
    "AcceleratorTypeList",
    "AcceleratorTypesClient",
    "AcceleratorTypesScopedList",
    "Accelerators",
    "AccessConfig",
    "AddAccessConfigInstanceRequest",
    "AddAssociationFirewallPolicyRequest",
    "AddHealthCheckTargetPoolRequest",
    "AddInstanceTargetPoolRequest",
    "AddInstancesInstanceGroupRequest",
    "AddNodesNodeGroupRequest",
    "AddPeeringNetworkRequest",
    "AddResourcePoliciesDiskRequest",
    "AddResourcePoliciesInstanceRequest",
    "AddResourcePoliciesRegionDiskRequest",
    "AddRuleFirewallPolicyRequest",
    "AddRuleSecurityPolicyRequest",
    "AddSignedUrlKeyBackendBucketRequest",
    "AddSignedUrlKeyBackendServiceRequest",
    "Address",
    "AddressAggregatedList",
    "AddressList",
    "AddressesClient",
    "AddressesScopedList",
    "AdvancedMachineFeatures",
    "AggregatedListAcceleratorTypesRequest",
    "AggregatedListAddressesRequest",
    "AggregatedListAutoscalersRequest",
    "AggregatedListBackendServicesRequest",
    "AggregatedListDiskTypesRequest",
    "AggregatedListDisksRequest",
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
    "AttachNetworkEndpointsGlobalNetworkEndpointGroupRequest",
    "AttachNetworkEndpointsNetworkEndpointGroupRequest",
    "AttachedDisk",
    "AttachedDiskInitializeParams",
    "AuditConfig",
    "AuditLogConfig",
    "AuthorizationLoggingOptions",
    "Autoscaler",
    "AutoscalerAggregatedList",
    "AutoscalerList",
    "AutoscalerStatusDetails",
    "AutoscalersClient",
    "AutoscalersScopedList",
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
    "BackendBucketsClient",
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
    "BackendServicesClient",
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
    "DeleteInstanceTemplateRequest",
    "DeleteInstancesInstanceGroupManagerRequest",
    "DeleteInstancesRegionInstanceGroupManagerRequest",
    "DeleteInterconnectAttachmentRequest",
    "DeleteInterconnectRequest",
    "DeleteLicenseRequest",
    "DeleteNetworkEndpointGroupRequest",
    "DeleteNetworkRequest",
    "DeleteNodeGroupRequest",
    "DeleteNodeTemplateRequest",
    "DeleteNodesNodeGroupRequest",
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
    "DiskType",
    "DiskTypeAggregatedList",
    "DiskTypeList",
    "DiskTypesClient",
    "DiskTypesScopedList",
    "DisksAddResourcePoliciesRequest",
    "DisksClient",
    "DisksRemoveResourcePoliciesRequest",
    "DisksResizeRequest",
    "DisksScopedList",
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
    "ExternalVpnGatewaysClient",
    "FileContentBuffer",
    "Firewall",
    "FirewallList",
    "FirewallLogConfig",
    "FirewallPoliciesClient",
    "FirewallPoliciesListAssociationsResponse",
    "FirewallPolicy",
    "FirewallPolicyAssociation",
    "FirewallPolicyList",
    "FirewallPolicyRule",
    "FirewallPolicyRuleMatcher",
    "FirewallPolicyRuleMatcherLayer4Config",
    "FirewallsClient",
    "FixedOrPercent",
    "ForwardingRule",
    "ForwardingRuleAggregatedList",
    "ForwardingRuleList",
    "ForwardingRuleReference",
    "ForwardingRuleServiceDirectoryRegistration",
    "ForwardingRulesClient",
    "ForwardingRulesScopedList",
    "GRPCHealthCheck",
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
    "GlobalAddressesClient",
    "GlobalForwardingRulesClient",
    "GlobalNetworkEndpointGroupsAttachEndpointsRequest",
    "GlobalNetworkEndpointGroupsClient",
    "GlobalNetworkEndpointGroupsDetachEndpointsRequest",
    "GlobalOperationsClient",
    "GlobalOrganizationOperationsClient",
    "GlobalOrganizationSetPolicyRequest",
    "GlobalPublicDelegatedPrefixesClient",
    "GlobalSetLabelsRequest",
    "GlobalSetPolicyRequest",
    "GuestAttributes",
    "GuestAttributesEntry",
    "GuestAttributesValue",
    "GuestOsFeature",
    "HTTP2HealthCheck",
    "HTTPHealthCheck",
    "HTTPSHealthCheck",
    "HealthCheck",
    "HealthCheckList",
    "HealthCheckLogConfig",
    "HealthCheckReference",
    "HealthCheckService",
    "HealthCheckServiceReference",
    "HealthCheckServicesList",
    "HealthChecksAggregatedList",
    "HealthChecksClient",
    "HealthChecksScopedList",
    "HealthStatus",
    "HealthStatusForNetworkEndpoint",
    "HostRule",
    "HttpFaultAbort",
    "HttpFaultDelay",
    "HttpFaultInjection",
    "HttpHeaderAction",
    "HttpHeaderMatch",
    "HttpHeaderOption",
    "HttpQueryParameterMatch",
    "HttpRedirectAction",
    "HttpRetryPolicy",
    "HttpRouteAction",
    "HttpRouteRule",
    "HttpRouteRuleMatch",
    "Image",
    "ImageList",
    "ImagesClient",
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
    "InstanceGroupManagerStatus",
    "InstanceGroupManagerStatusStateful",
    "InstanceGroupManagerStatusStatefulPerInstanceConfigs",
    "InstanceGroupManagerStatusVersionTarget",
    "InstanceGroupManagerUpdatePolicy",
    "InstanceGroupManagerVersion",
    "InstanceGroupManagersAbandonInstancesRequest",
    "InstanceGroupManagersApplyUpdatesRequest",
    "InstanceGroupManagersClient",
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
    "InstanceGroupManagersUpdatePerInstanceConfigsReq",
    "InstanceGroupsAddInstancesRequest",
    "InstanceGroupsClient",
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
    "InstanceTemplate",
    "InstanceTemplateList",
    "InstanceTemplatesClient",
    "InstanceWithNamedPorts",
    "InstancesAddResourcePoliciesRequest",
    "InstancesClient",
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
    "Int64RangeMatch",
    "Interconnect",
    "InterconnectAttachment",
    "InterconnectAttachmentAggregatedList",
    "InterconnectAttachmentList",
    "InterconnectAttachmentPartnerMetadata",
    "InterconnectAttachmentPrivateInfo",
    "InterconnectAttachmentsClient",
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
    "InterconnectLocationsClient",
    "InterconnectOutageNotification",
    "InterconnectsClient",
    "InterconnectsGetDiagnosticsResponse",
    "InvalidateCacheUrlMapRequest",
    "Items",
    "License",
    "LicenseCode",
    "LicenseCodeLicenseAlias",
    "LicenseCodesClient",
    "LicenseResourceCommitment",
    "LicenseResourceRequirements",
    "LicensesClient",
    "LicensesListResponse",
    "ListAcceleratorTypesRequest",
    "ListAddressesRequest",
    "ListAssociationsFirewallPolicyRequest",
    "ListAutoscalersRequest",
    "ListAvailableFeaturesSslPoliciesRequest",
    "ListBackendBucketsRequest",
    "ListBackendServicesRequest",
    "ListDiskTypesRequest",
    "ListDisksRequest",
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
    "ListInstanceTemplatesRequest",
    "ListInstancesInstanceGroupsRequest",
    "ListInstancesRegionInstanceGroupsRequest",
    "ListInstancesRequest",
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
    "ListNodeTemplatesRequest",
    "ListNodeTypesRequest",
    "ListNodesNodeGroupsRequest",
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
    "ListRegionDiskTypesRequest",
    "ListRegionDisksRequest",
    "ListRegionHealthCheckServicesRequest",
    "ListRegionHealthChecksRequest",
    "ListRegionInstanceGroupManagersRequest",
    "ListRegionInstanceGroupsRequest",
    "ListRegionNetworkEndpointGroupsRequest",
    "ListRegionNotificationEndpointsRequest",
    "ListRegionOperationsRequest",
    "ListRegionSslCertificatesRequest",
    "ListRegionTargetHttpProxiesRequest",
    "ListRegionTargetHttpsProxiesRequest",
    "ListRegionUrlMapsRequest",
    "ListRegionsRequest",
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
    "MachineTypesClient",
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
    "NetworkEndpointGroupsClient",
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
    "NetworksClient",
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
    "NodeGroupsClient",
    "NodeGroupsDeleteNodesRequest",
    "NodeGroupsListNodes",
    "NodeGroupsScopedList",
    "NodeGroupsSetNodeTemplateRequest",
    "NodeTemplate",
    "NodeTemplateAggregatedList",
    "NodeTemplateList",
    "NodeTemplateNodeTypeFlexibility",
    "NodeTemplatesClient",
    "NodeTemplatesScopedList",
    "NodeType",
    "NodeTypeAggregatedList",
    "NodeTypeList",
    "NodeTypesClient",
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
    "PacketMirroringsClient",
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
    "ProjectsClient",
    "ProjectsDisableXpnResourceRequest",
    "ProjectsEnableXpnResourceRequest",
    "ProjectsGetXpnResources",
    "ProjectsListXpnHostsRequest",
    "ProjectsSetDefaultNetworkTierRequest",
    "PublicAdvertisedPrefix",
    "PublicAdvertisedPrefixList",
    "PublicAdvertisedPrefixPublicDelegatedPrefix",
    "PublicAdvertisedPrefixesClient",
    "PublicDelegatedPrefix",
    "PublicDelegatedPrefixAggregatedList",
    "PublicDelegatedPrefixList",
    "PublicDelegatedPrefixPublicDelegatedSubPrefix",
    "PublicDelegatedPrefixesClient",
    "PublicDelegatedPrefixesScopedList",
    "Quota",
    "RawDisk",
    "RecreateInstancesInstanceGroupManagerRequest",
    "RecreateInstancesRegionInstanceGroupManagerRequest",
    "Reference",
    "Region",
    "RegionAutoscalerList",
    "RegionAutoscalersClient",
    "RegionBackendServicesClient",
    "RegionCommitmentsClient",
    "RegionDiskTypeList",
    "RegionDiskTypesClient",
    "RegionDisksAddResourcePoliciesRequest",
    "RegionDisksClient",
    "RegionDisksRemoveResourcePoliciesRequest",
    "RegionDisksResizeRequest",
    "RegionHealthCheckServicesClient",
    "RegionHealthChecksClient",
    "RegionInstanceGroupList",
    "RegionInstanceGroupManagerDeleteInstanceConfigReq",
    "RegionInstanceGroupManagerList",
    "RegionInstanceGroupManagerPatchInstanceConfigReq",
    "RegionInstanceGroupManagerUpdateInstanceConfigReq",
    "RegionInstanceGroupManagersAbandonInstancesRequest",
    "RegionInstanceGroupManagersApplyUpdatesRequest",
    "RegionInstanceGroupManagersClient",
    "RegionInstanceGroupManagersCreateInstancesRequest",
    "RegionInstanceGroupManagersDeleteInstancesRequest",
    "RegionInstanceGroupManagersListErrorsResponse",
    "RegionInstanceGroupManagersListInstanceConfigsResp",
    "RegionInstanceGroupManagersListInstancesResponse",
    "RegionInstanceGroupManagersRecreateRequest",
    "RegionInstanceGroupManagersSetTargetPoolsRequest",
    "RegionInstanceGroupManagersSetTemplateRequest",
    "RegionInstanceGroupsClient",
    "RegionInstanceGroupsListInstances",
    "RegionInstanceGroupsListInstancesRequest",
    "RegionInstanceGroupsSetNamedPortsRequest",
    "RegionInstancesClient",
    "RegionList",
    "RegionNetworkEndpointGroupsClient",
    "RegionNotificationEndpointsClient",
    "RegionOperationsClient",
    "RegionSetLabelsRequest",
    "RegionSetPolicyRequest",
    "RegionSslCertificatesClient",
    "RegionTargetHttpProxiesClient",
    "RegionTargetHttpsProxiesClient",
    "RegionTargetHttpsProxiesSetSslCertificatesRequest",
    "RegionUrlMapsClient",
    "RegionUrlMapsValidateRequest",
    "RegionsClient",
    "RemoveAssociationFirewallPolicyRequest",
    "RemoveHealthCheckTargetPoolRequest",
    "RemoveInstanceTargetPoolRequest",
    "RemoveInstancesInstanceGroupRequest",
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
    "ReservationsClient",
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
    "ResourcePoliciesClient",
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
    "RouterStatus",
    "RouterStatusBgpPeerStatus",
    "RouterStatusNatStatus",
    "RouterStatusResponse",
    "RoutersClient",
    "RoutersPreviewResponse",
    "RoutersScopedList",
    "RoutesClient",
    "Rule",
    "SSLHealthCheck",
    "ScalingScheduleStatus",
    "Scheduling",
    "SchedulingNodeAffinity",
    "ScratchDisks",
    "Screenshot",
    "SecurityPoliciesClient",
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
    "SnapshotsClient",
    "SourceInstanceParams",
    "SslCertificate",
    "SslCertificateAggregatedList",
    "SslCertificateList",
    "SslCertificateManagedSslCertificate",
    "SslCertificateSelfManagedSslCertificate",
    "SslCertificatesClient",
    "SslCertificatesScopedList",
    "SslPoliciesClient",
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
    "SubnetworksClient",
    "SubnetworksExpandIpCidrRangeRequest",
    "SubnetworksScopedList",
    "SubnetworksSetPrivateIpGoogleAccessRequest",
    "SwitchToCustomModeNetworkRequest",
    "TCPHealthCheck",
    "Tags",
    "TargetGrpcProxiesClient",
    "TargetGrpcProxy",
    "TargetGrpcProxyList",
    "TargetHttpProxiesClient",
    "TargetHttpProxiesScopedList",
    "TargetHttpProxy",
    "TargetHttpProxyAggregatedList",
    "TargetHttpProxyList",
    "TargetHttpsProxiesClient",
    "TargetHttpsProxiesScopedList",
    "TargetHttpsProxiesSetQuicOverrideRequest",
    "TargetHttpsProxiesSetSslCertificatesRequest",
    "TargetHttpsProxy",
    "TargetHttpsProxyAggregatedList",
    "TargetHttpsProxyList",
    "TargetInstance",
    "TargetInstanceAggregatedList",
    "TargetInstanceList",
    "TargetInstancesClient",
    "TargetInstancesScopedList",
    "TargetPool",
    "TargetPoolAggregatedList",
    "TargetPoolInstanceHealth",
    "TargetPoolList",
    "TargetPoolsAddHealthCheckRequest",
    "TargetPoolsAddInstanceRequest",
    "TargetPoolsClient",
    "TargetPoolsRemoveHealthCheckRequest",
    "TargetPoolsRemoveInstanceRequest",
    "TargetPoolsScopedList",
    "TargetReference",
    "TargetSslProxiesClient",
    "TargetSslProxiesSetBackendServiceRequest",
    "TargetSslProxiesSetProxyHeaderRequest",
    "TargetSslProxiesSetSslCertificatesRequest",
    "TargetSslProxy",
    "TargetSslProxyList",
    "TargetTcpProxiesClient",
    "TargetTcpProxiesSetBackendServiceRequest",
    "TargetTcpProxiesSetProxyHeaderRequest",
    "TargetTcpProxy",
    "TargetTcpProxyList",
    "TargetVpnGateway",
    "TargetVpnGatewayAggregatedList",
    "TargetVpnGatewayList",
    "TargetVpnGatewaysClient",
    "TargetVpnGatewaysScopedList",
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
    "UrlMapTest",
    "UrlMapTestHeader",
    "UrlMapValidationResult",
    "UrlMapsAggregatedList",
    "UrlMapsClient",
    "UrlMapsScopedList",
    "UrlMapsValidateRequest",
    "UrlMapsValidateResponse",
    "UrlRewrite",
    "UsableSubnetwork",
    "UsableSubnetworkSecondaryRange",
    "UsableSubnetworksAggregatedList",
    "UsageExportLocation",
    "ValidateRegionUrlMapRequest",
    "ValidateUrlMapRequest",
    "VmEndpointNatMappings",
    "VmEndpointNatMappingsInterfaceNatMappings",
    "VmEndpointNatMappingsList",
    "VpnGateway",
    "VpnGatewayAggregatedList",
    "VpnGatewayList",
    "VpnGatewayStatus",
    "VpnGatewayStatusHighAvailabilityRequirementState",
    "VpnGatewayStatusTunnel",
    "VpnGatewayStatusVpnConnection",
    "VpnGatewayVpnGatewayInterface",
    "VpnGatewaysClient",
    "VpnGatewaysGetStatusResponse",
    "VpnGatewaysScopedList",
    "VpnTunnel",
    "VpnTunnelAggregatedList",
    "VpnTunnelList",
    "VpnTunnelsClient",
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
    "ZoneOperationsClient",
    "ZoneSetLabelsRequest",
    "ZoneSetPolicyRequest",
    "ZonesClient",
)
