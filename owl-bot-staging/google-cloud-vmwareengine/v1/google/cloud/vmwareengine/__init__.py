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
from google.cloud.vmwareengine import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.vmwareengine_v1.services.vmware_engine.client import VmwareEngineClient
from google.cloud.vmwareengine_v1.services.vmware_engine.async_client import VmwareEngineAsyncClient

from google.cloud.vmwareengine_v1.types.vmwareengine import CreateClusterRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import CreateExternalAccessRuleRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import CreateExternalAddressRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import CreateHcxActivationKeyRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import CreateLoggingServerRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import CreateManagementDnsZoneBindingRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import CreateNetworkPeeringRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import CreateNetworkPolicyRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import CreatePrivateCloudRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import CreatePrivateConnectionRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import CreateVmwareEngineNetworkRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import DeleteClusterRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import DeleteExternalAccessRuleRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import DeleteExternalAddressRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import DeleteLoggingServerRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import DeleteManagementDnsZoneBindingRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import DeleteNetworkPeeringRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import DeleteNetworkPolicyRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import DeletePrivateCloudRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import DeletePrivateConnectionRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import DeleteVmwareEngineNetworkRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import FetchNetworkPolicyExternalAddressesRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import FetchNetworkPolicyExternalAddressesResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import GetClusterRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GetDnsBindPermissionRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GetDnsForwardingRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GetExternalAccessRuleRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GetExternalAddressRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GetHcxActivationKeyRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GetLoggingServerRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GetManagementDnsZoneBindingRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GetNetworkPeeringRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GetNetworkPolicyRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GetNodeRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GetNodeTypeRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GetPrivateCloudRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GetPrivateConnectionRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GetSubnetRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GetVmwareEngineNetworkRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GrantDnsBindPermissionRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListClustersRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListClustersResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import ListExternalAccessRulesRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListExternalAccessRulesResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import ListExternalAddressesRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListExternalAddressesResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import ListHcxActivationKeysRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListHcxActivationKeysResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import ListLoggingServersRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListLoggingServersResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import ListManagementDnsZoneBindingsRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListManagementDnsZoneBindingsResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import ListNetworkPeeringsRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListNetworkPeeringsResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import ListNetworkPoliciesRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListNetworkPoliciesResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import ListNodesRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListNodesResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import ListNodeTypesRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListNodeTypesResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import ListPeeringRoutesRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListPeeringRoutesResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import ListPrivateCloudsRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListPrivateCloudsResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import ListPrivateConnectionPeeringRoutesRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListPrivateConnectionPeeringRoutesResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import ListPrivateConnectionsRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListPrivateConnectionsResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import ListSubnetsRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListSubnetsResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import ListVmwareEngineNetworksRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListVmwareEngineNetworksResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import OperationMetadata
from google.cloud.vmwareengine_v1.types.vmwareengine import RepairManagementDnsZoneBindingRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ResetNsxCredentialsRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ResetVcenterCredentialsRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import RevokeDnsBindPermissionRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ShowNsxCredentialsRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ShowVcenterCredentialsRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import UndeletePrivateCloudRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import UpdateClusterRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import UpdateDnsForwardingRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import UpdateExternalAccessRuleRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import UpdateExternalAddressRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import UpdateLoggingServerRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import UpdateManagementDnsZoneBindingRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import UpdateNetworkPeeringRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import UpdateNetworkPolicyRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import UpdatePrivateCloudRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import UpdatePrivateConnectionRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import UpdateSubnetRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import UpdateVmwareEngineNetworkRequest
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import Cluster
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import Credentials
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import DnsBindPermission
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import DnsForwarding
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import ExternalAccessRule
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import ExternalAddress
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import Hcx
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import HcxActivationKey
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import LocationMetadata
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import LoggingServer
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import ManagementDnsZoneBinding
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import NetworkConfig
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import NetworkPeering
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import NetworkPolicy
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import Node
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import NodeType
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import NodeTypeConfig
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import Nsx
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import PeeringRoute
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import Principal
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import PrivateCloud
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import PrivateConnection
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import StretchedClusterConfig
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import Subnet
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import Vcenter
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import VmwareEngineNetwork

__all__ = ('VmwareEngineClient',
    'VmwareEngineAsyncClient',
    'CreateClusterRequest',
    'CreateExternalAccessRuleRequest',
    'CreateExternalAddressRequest',
    'CreateHcxActivationKeyRequest',
    'CreateLoggingServerRequest',
    'CreateManagementDnsZoneBindingRequest',
    'CreateNetworkPeeringRequest',
    'CreateNetworkPolicyRequest',
    'CreatePrivateCloudRequest',
    'CreatePrivateConnectionRequest',
    'CreateVmwareEngineNetworkRequest',
    'DeleteClusterRequest',
    'DeleteExternalAccessRuleRequest',
    'DeleteExternalAddressRequest',
    'DeleteLoggingServerRequest',
    'DeleteManagementDnsZoneBindingRequest',
    'DeleteNetworkPeeringRequest',
    'DeleteNetworkPolicyRequest',
    'DeletePrivateCloudRequest',
    'DeletePrivateConnectionRequest',
    'DeleteVmwareEngineNetworkRequest',
    'FetchNetworkPolicyExternalAddressesRequest',
    'FetchNetworkPolicyExternalAddressesResponse',
    'GetClusterRequest',
    'GetDnsBindPermissionRequest',
    'GetDnsForwardingRequest',
    'GetExternalAccessRuleRequest',
    'GetExternalAddressRequest',
    'GetHcxActivationKeyRequest',
    'GetLoggingServerRequest',
    'GetManagementDnsZoneBindingRequest',
    'GetNetworkPeeringRequest',
    'GetNetworkPolicyRequest',
    'GetNodeRequest',
    'GetNodeTypeRequest',
    'GetPrivateCloudRequest',
    'GetPrivateConnectionRequest',
    'GetSubnetRequest',
    'GetVmwareEngineNetworkRequest',
    'GrantDnsBindPermissionRequest',
    'ListClustersRequest',
    'ListClustersResponse',
    'ListExternalAccessRulesRequest',
    'ListExternalAccessRulesResponse',
    'ListExternalAddressesRequest',
    'ListExternalAddressesResponse',
    'ListHcxActivationKeysRequest',
    'ListHcxActivationKeysResponse',
    'ListLoggingServersRequest',
    'ListLoggingServersResponse',
    'ListManagementDnsZoneBindingsRequest',
    'ListManagementDnsZoneBindingsResponse',
    'ListNetworkPeeringsRequest',
    'ListNetworkPeeringsResponse',
    'ListNetworkPoliciesRequest',
    'ListNetworkPoliciesResponse',
    'ListNodesRequest',
    'ListNodesResponse',
    'ListNodeTypesRequest',
    'ListNodeTypesResponse',
    'ListPeeringRoutesRequest',
    'ListPeeringRoutesResponse',
    'ListPrivateCloudsRequest',
    'ListPrivateCloudsResponse',
    'ListPrivateConnectionPeeringRoutesRequest',
    'ListPrivateConnectionPeeringRoutesResponse',
    'ListPrivateConnectionsRequest',
    'ListPrivateConnectionsResponse',
    'ListSubnetsRequest',
    'ListSubnetsResponse',
    'ListVmwareEngineNetworksRequest',
    'ListVmwareEngineNetworksResponse',
    'OperationMetadata',
    'RepairManagementDnsZoneBindingRequest',
    'ResetNsxCredentialsRequest',
    'ResetVcenterCredentialsRequest',
    'RevokeDnsBindPermissionRequest',
    'ShowNsxCredentialsRequest',
    'ShowVcenterCredentialsRequest',
    'UndeletePrivateCloudRequest',
    'UpdateClusterRequest',
    'UpdateDnsForwardingRequest',
    'UpdateExternalAccessRuleRequest',
    'UpdateExternalAddressRequest',
    'UpdateLoggingServerRequest',
    'UpdateManagementDnsZoneBindingRequest',
    'UpdateNetworkPeeringRequest',
    'UpdateNetworkPolicyRequest',
    'UpdatePrivateCloudRequest',
    'UpdatePrivateConnectionRequest',
    'UpdateSubnetRequest',
    'UpdateVmwareEngineNetworkRequest',
    'Cluster',
    'Credentials',
    'DnsBindPermission',
    'DnsForwarding',
    'ExternalAccessRule',
    'ExternalAddress',
    'Hcx',
    'HcxActivationKey',
    'LocationMetadata',
    'LoggingServer',
    'ManagementDnsZoneBinding',
    'NetworkConfig',
    'NetworkPeering',
    'NetworkPolicy',
    'Node',
    'NodeType',
    'NodeTypeConfig',
    'Nsx',
    'PeeringRoute',
    'Principal',
    'PrivateCloud',
    'PrivateConnection',
    'StretchedClusterConfig',
    'Subnet',
    'Vcenter',
    'VmwareEngineNetwork',
)
