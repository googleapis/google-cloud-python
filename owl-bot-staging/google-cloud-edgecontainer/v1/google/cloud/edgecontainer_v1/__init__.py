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
from google.cloud.edgecontainer_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.edge_container import EdgeContainerClient
from .services.edge_container import EdgeContainerAsyncClient

from .types.resources import Authorization
from .types.resources import Cluster
from .types.resources import ClusterNetworking
from .types.resources import ClusterUser
from .types.resources import Fleet
from .types.resources import LocationMetadata
from .types.resources import Machine
from .types.resources import MaintenancePolicy
from .types.resources import MaintenanceWindow
from .types.resources import NodePool
from .types.resources import Quota
from .types.resources import RecurringTimeWindow
from .types.resources import TimeWindow
from .types.resources import VpnConnection
from .types.resources import ZoneMetadata
from .types.resources import KmsKeyState
from .types.service import CreateClusterRequest
from .types.service import CreateNodePoolRequest
from .types.service import CreateVpnConnectionRequest
from .types.service import DeleteClusterRequest
from .types.service import DeleteNodePoolRequest
from .types.service import DeleteVpnConnectionRequest
from .types.service import GenerateAccessTokenRequest
from .types.service import GenerateAccessTokenResponse
from .types.service import GetClusterRequest
from .types.service import GetMachineRequest
from .types.service import GetNodePoolRequest
from .types.service import GetVpnConnectionRequest
from .types.service import ListClustersRequest
from .types.service import ListClustersResponse
from .types.service import ListMachinesRequest
from .types.service import ListMachinesResponse
from .types.service import ListNodePoolsRequest
from .types.service import ListNodePoolsResponse
from .types.service import ListVpnConnectionsRequest
from .types.service import ListVpnConnectionsResponse
from .types.service import OperationMetadata
from .types.service import UpdateClusterRequest
from .types.service import UpdateNodePoolRequest

__all__ = (
    'EdgeContainerAsyncClient',
'Authorization',
'Cluster',
'ClusterNetworking',
'ClusterUser',
'CreateClusterRequest',
'CreateNodePoolRequest',
'CreateVpnConnectionRequest',
'DeleteClusterRequest',
'DeleteNodePoolRequest',
'DeleteVpnConnectionRequest',
'EdgeContainerClient',
'Fleet',
'GenerateAccessTokenRequest',
'GenerateAccessTokenResponse',
'GetClusterRequest',
'GetMachineRequest',
'GetNodePoolRequest',
'GetVpnConnectionRequest',
'KmsKeyState',
'ListClustersRequest',
'ListClustersResponse',
'ListMachinesRequest',
'ListMachinesResponse',
'ListNodePoolsRequest',
'ListNodePoolsResponse',
'ListVpnConnectionsRequest',
'ListVpnConnectionsResponse',
'LocationMetadata',
'Machine',
'MaintenancePolicy',
'MaintenanceWindow',
'NodePool',
'OperationMetadata',
'Quota',
'RecurringTimeWindow',
'TimeWindow',
'UpdateClusterRequest',
'UpdateNodePoolRequest',
'VpnConnection',
'ZoneMetadata',
)
