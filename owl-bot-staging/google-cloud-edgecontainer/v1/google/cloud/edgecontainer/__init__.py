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
from google.cloud.edgecontainer import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.edgecontainer_v1.services.edge_container.client import EdgeContainerClient
from google.cloud.edgecontainer_v1.services.edge_container.async_client import EdgeContainerAsyncClient

from google.cloud.edgecontainer_v1.types.resources import Authorization
from google.cloud.edgecontainer_v1.types.resources import Cluster
from google.cloud.edgecontainer_v1.types.resources import ClusterNetworking
from google.cloud.edgecontainer_v1.types.resources import ClusterUser
from google.cloud.edgecontainer_v1.types.resources import Fleet
from google.cloud.edgecontainer_v1.types.resources import LocationMetadata
from google.cloud.edgecontainer_v1.types.resources import Machine
from google.cloud.edgecontainer_v1.types.resources import MaintenancePolicy
from google.cloud.edgecontainer_v1.types.resources import MaintenanceWindow
from google.cloud.edgecontainer_v1.types.resources import NodePool
from google.cloud.edgecontainer_v1.types.resources import Quota
from google.cloud.edgecontainer_v1.types.resources import RecurringTimeWindow
from google.cloud.edgecontainer_v1.types.resources import TimeWindow
from google.cloud.edgecontainer_v1.types.resources import VpnConnection
from google.cloud.edgecontainer_v1.types.resources import ZoneMetadata
from google.cloud.edgecontainer_v1.types.resources import KmsKeyState
from google.cloud.edgecontainer_v1.types.service import CreateClusterRequest
from google.cloud.edgecontainer_v1.types.service import CreateNodePoolRequest
from google.cloud.edgecontainer_v1.types.service import CreateVpnConnectionRequest
from google.cloud.edgecontainer_v1.types.service import DeleteClusterRequest
from google.cloud.edgecontainer_v1.types.service import DeleteNodePoolRequest
from google.cloud.edgecontainer_v1.types.service import DeleteVpnConnectionRequest
from google.cloud.edgecontainer_v1.types.service import GenerateAccessTokenRequest
from google.cloud.edgecontainer_v1.types.service import GenerateAccessTokenResponse
from google.cloud.edgecontainer_v1.types.service import GetClusterRequest
from google.cloud.edgecontainer_v1.types.service import GetMachineRequest
from google.cloud.edgecontainer_v1.types.service import GetNodePoolRequest
from google.cloud.edgecontainer_v1.types.service import GetVpnConnectionRequest
from google.cloud.edgecontainer_v1.types.service import ListClustersRequest
from google.cloud.edgecontainer_v1.types.service import ListClustersResponse
from google.cloud.edgecontainer_v1.types.service import ListMachinesRequest
from google.cloud.edgecontainer_v1.types.service import ListMachinesResponse
from google.cloud.edgecontainer_v1.types.service import ListNodePoolsRequest
from google.cloud.edgecontainer_v1.types.service import ListNodePoolsResponse
from google.cloud.edgecontainer_v1.types.service import ListVpnConnectionsRequest
from google.cloud.edgecontainer_v1.types.service import ListVpnConnectionsResponse
from google.cloud.edgecontainer_v1.types.service import OperationMetadata
from google.cloud.edgecontainer_v1.types.service import UpdateClusterRequest
from google.cloud.edgecontainer_v1.types.service import UpdateNodePoolRequest

__all__ = ('EdgeContainerClient',
    'EdgeContainerAsyncClient',
    'Authorization',
    'Cluster',
    'ClusterNetworking',
    'ClusterUser',
    'Fleet',
    'LocationMetadata',
    'Machine',
    'MaintenancePolicy',
    'MaintenanceWindow',
    'NodePool',
    'Quota',
    'RecurringTimeWindow',
    'TimeWindow',
    'VpnConnection',
    'ZoneMetadata',
    'KmsKeyState',
    'CreateClusterRequest',
    'CreateNodePoolRequest',
    'CreateVpnConnectionRequest',
    'DeleteClusterRequest',
    'DeleteNodePoolRequest',
    'DeleteVpnConnectionRequest',
    'GenerateAccessTokenRequest',
    'GenerateAccessTokenResponse',
    'GetClusterRequest',
    'GetMachineRequest',
    'GetNodePoolRequest',
    'GetVpnConnectionRequest',
    'ListClustersRequest',
    'ListClustersResponse',
    'ListMachinesRequest',
    'ListMachinesResponse',
    'ListNodePoolsRequest',
    'ListNodePoolsResponse',
    'ListVpnConnectionsRequest',
    'ListVpnConnectionsResponse',
    'OperationMetadata',
    'UpdateClusterRequest',
    'UpdateNodePoolRequest',
)
