# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from google.cloud.vmwareengine_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.vmware_engine import VmwareEngineClient
from .services.vmware_engine import VmwareEngineAsyncClient

from .types.vmwareengine import CreateClusterRequest
from .types.vmwareengine import CreateHcxActivationKeyRequest
from .types.vmwareengine import CreateNetworkPolicyRequest
from .types.vmwareengine import CreatePrivateCloudRequest
from .types.vmwareengine import CreateVmwareEngineNetworkRequest
from .types.vmwareengine import DeleteClusterRequest
from .types.vmwareengine import DeleteNetworkPolicyRequest
from .types.vmwareengine import DeletePrivateCloudRequest
from .types.vmwareengine import DeleteVmwareEngineNetworkRequest
from .types.vmwareengine import GetClusterRequest
from .types.vmwareengine import GetHcxActivationKeyRequest
from .types.vmwareengine import GetNetworkPolicyRequest
from .types.vmwareengine import GetNodeTypeRequest
from .types.vmwareengine import GetPrivateCloudRequest
from .types.vmwareengine import GetVmwareEngineNetworkRequest
from .types.vmwareengine import ListClustersRequest
from .types.vmwareengine import ListClustersResponse
from .types.vmwareengine import ListHcxActivationKeysRequest
from .types.vmwareengine import ListHcxActivationKeysResponse
from .types.vmwareengine import ListNetworkPoliciesRequest
from .types.vmwareengine import ListNetworkPoliciesResponse
from .types.vmwareengine import ListNodeTypesRequest
from .types.vmwareengine import ListNodeTypesResponse
from .types.vmwareengine import ListPrivateCloudsRequest
from .types.vmwareengine import ListPrivateCloudsResponse
from .types.vmwareengine import ListSubnetsRequest
from .types.vmwareengine import ListSubnetsResponse
from .types.vmwareengine import ListVmwareEngineNetworksRequest
from .types.vmwareengine import ListVmwareEngineNetworksResponse
from .types.vmwareengine import OperationMetadata
from .types.vmwareengine import ResetNsxCredentialsRequest
from .types.vmwareengine import ResetVcenterCredentialsRequest
from .types.vmwareengine import ShowNsxCredentialsRequest
from .types.vmwareengine import ShowVcenterCredentialsRequest
from .types.vmwareengine import UndeletePrivateCloudRequest
from .types.vmwareengine import UpdateClusterRequest
from .types.vmwareengine import UpdateNetworkPolicyRequest
from .types.vmwareengine import UpdatePrivateCloudRequest
from .types.vmwareengine import UpdateVmwareEngineNetworkRequest
from .types.vmwareengine_resources import Cluster
from .types.vmwareengine_resources import Credentials
from .types.vmwareengine_resources import Hcx
from .types.vmwareengine_resources import HcxActivationKey
from .types.vmwareengine_resources import NetworkConfig
from .types.vmwareengine_resources import NetworkPolicy
from .types.vmwareengine_resources import NodeType
from .types.vmwareengine_resources import NodeTypeConfig
from .types.vmwareengine_resources import Nsx
from .types.vmwareengine_resources import PrivateCloud
from .types.vmwareengine_resources import Subnet
from .types.vmwareengine_resources import Vcenter
from .types.vmwareengine_resources import VmwareEngineNetwork

__all__ = (
    'VmwareEngineAsyncClient',
'Cluster',
'CreateClusterRequest',
'CreateHcxActivationKeyRequest',
'CreateNetworkPolicyRequest',
'CreatePrivateCloudRequest',
'CreateVmwareEngineNetworkRequest',
'Credentials',
'DeleteClusterRequest',
'DeleteNetworkPolicyRequest',
'DeletePrivateCloudRequest',
'DeleteVmwareEngineNetworkRequest',
'GetClusterRequest',
'GetHcxActivationKeyRequest',
'GetNetworkPolicyRequest',
'GetNodeTypeRequest',
'GetPrivateCloudRequest',
'GetVmwareEngineNetworkRequest',
'Hcx',
'HcxActivationKey',
'ListClustersRequest',
'ListClustersResponse',
'ListHcxActivationKeysRequest',
'ListHcxActivationKeysResponse',
'ListNetworkPoliciesRequest',
'ListNetworkPoliciesResponse',
'ListNodeTypesRequest',
'ListNodeTypesResponse',
'ListPrivateCloudsRequest',
'ListPrivateCloudsResponse',
'ListSubnetsRequest',
'ListSubnetsResponse',
'ListVmwareEngineNetworksRequest',
'ListVmwareEngineNetworksResponse',
'NetworkConfig',
'NetworkPolicy',
'NodeType',
'NodeTypeConfig',
'Nsx',
'OperationMetadata',
'PrivateCloud',
'ResetNsxCredentialsRequest',
'ResetVcenterCredentialsRequest',
'ShowNsxCredentialsRequest',
'ShowVcenterCredentialsRequest',
'Subnet',
'UndeletePrivateCloudRequest',
'UpdateClusterRequest',
'UpdateNetworkPolicyRequest',
'UpdatePrivateCloudRequest',
'UpdateVmwareEngineNetworkRequest',
'Vcenter',
'VmwareEngineClient',
'VmwareEngineNetwork',
)
