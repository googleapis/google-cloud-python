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
from google.cloud.vmwareengine import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.vmwareengine_v1.services.vmware_engine.client import VmwareEngineClient
from google.cloud.vmwareengine_v1.services.vmware_engine.async_client import VmwareEngineAsyncClient

from google.cloud.vmwareengine_v1.types.vmwareengine import CreateClusterRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import CreateHcxActivationKeyRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import CreateNetworkPolicyRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import CreatePrivateCloudRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import CreateVmwareEngineNetworkRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import DeleteClusterRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import DeleteNetworkPolicyRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import DeletePrivateCloudRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import DeleteVmwareEngineNetworkRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GetClusterRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GetHcxActivationKeyRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GetNetworkPolicyRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GetNodeTypeRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GetPrivateCloudRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import GetVmwareEngineNetworkRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListClustersRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListClustersResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import ListHcxActivationKeysRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListHcxActivationKeysResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import ListNetworkPoliciesRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListNetworkPoliciesResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import ListNodeTypesRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListNodeTypesResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import ListPrivateCloudsRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListPrivateCloudsResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import ListSubnetsRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListSubnetsResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import ListVmwareEngineNetworksRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ListVmwareEngineNetworksResponse
from google.cloud.vmwareengine_v1.types.vmwareengine import OperationMetadata
from google.cloud.vmwareengine_v1.types.vmwareengine import ResetNsxCredentialsRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ResetVcenterCredentialsRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ShowNsxCredentialsRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import ShowVcenterCredentialsRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import UndeletePrivateCloudRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import UpdateClusterRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import UpdateNetworkPolicyRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import UpdatePrivateCloudRequest
from google.cloud.vmwareengine_v1.types.vmwareengine import UpdateVmwareEngineNetworkRequest
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import Cluster
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import Credentials
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import Hcx
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import HcxActivationKey
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import NetworkConfig
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import NetworkPolicy
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import NodeType
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import NodeTypeConfig
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import Nsx
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import PrivateCloud
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import Subnet
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import Vcenter
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import VmwareEngineNetwork

__all__ = ('VmwareEngineClient',
    'VmwareEngineAsyncClient',
    'CreateClusterRequest',
    'CreateHcxActivationKeyRequest',
    'CreateNetworkPolicyRequest',
    'CreatePrivateCloudRequest',
    'CreateVmwareEngineNetworkRequest',
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
    'OperationMetadata',
    'ResetNsxCredentialsRequest',
    'ResetVcenterCredentialsRequest',
    'ShowNsxCredentialsRequest',
    'ShowVcenterCredentialsRequest',
    'UndeletePrivateCloudRequest',
    'UpdateClusterRequest',
    'UpdateNetworkPolicyRequest',
    'UpdatePrivateCloudRequest',
    'UpdateVmwareEngineNetworkRequest',
    'Cluster',
    'Credentials',
    'Hcx',
    'HcxActivationKey',
    'NetworkConfig',
    'NetworkPolicy',
    'NodeType',
    'NodeTypeConfig',
    'Nsx',
    'PrivateCloud',
    'Subnet',
    'Vcenter',
    'VmwareEngineNetwork',
)
