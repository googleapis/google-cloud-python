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
from google.cloud.edgecontainer import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.edgecontainer_v1.services.edge_container.async_client import (
    EdgeContainerAsyncClient,
)
from google.cloud.edgecontainer_v1.services.edge_container.client import (
    EdgeContainerClient,
)
from google.cloud.edgecontainer_v1.types.resources import (
    Authorization,
    Cluster,
    ClusterNetworking,
    ClusterUser,
    Fleet,
    KmsKeyState,
    LocationMetadata,
    Machine,
    MaintenancePolicy,
    MaintenanceWindow,
    NodePool,
    Quota,
    RecurringTimeWindow,
    TimeWindow,
    VpnConnection,
    ZoneMetadata,
)
from google.cloud.edgecontainer_v1.types.service import (
    CreateClusterRequest,
    CreateNodePoolRequest,
    CreateVpnConnectionRequest,
    DeleteClusterRequest,
    DeleteNodePoolRequest,
    DeleteVpnConnectionRequest,
    GenerateAccessTokenRequest,
    GenerateAccessTokenResponse,
    GetClusterRequest,
    GetMachineRequest,
    GetNodePoolRequest,
    GetVpnConnectionRequest,
    ListClustersRequest,
    ListClustersResponse,
    ListMachinesRequest,
    ListMachinesResponse,
    ListNodePoolsRequest,
    ListNodePoolsResponse,
    ListVpnConnectionsRequest,
    ListVpnConnectionsResponse,
    OperationMetadata,
    UpdateClusterRequest,
    UpdateNodePoolRequest,
)

__all__ = (
    "EdgeContainerClient",
    "EdgeContainerAsyncClient",
    "Authorization",
    "Cluster",
    "ClusterNetworking",
    "ClusterUser",
    "Fleet",
    "LocationMetadata",
    "Machine",
    "MaintenancePolicy",
    "MaintenanceWindow",
    "NodePool",
    "Quota",
    "RecurringTimeWindow",
    "TimeWindow",
    "VpnConnection",
    "ZoneMetadata",
    "KmsKeyState",
    "CreateClusterRequest",
    "CreateNodePoolRequest",
    "CreateVpnConnectionRequest",
    "DeleteClusterRequest",
    "DeleteNodePoolRequest",
    "DeleteVpnConnectionRequest",
    "GenerateAccessTokenRequest",
    "GenerateAccessTokenResponse",
    "GetClusterRequest",
    "GetMachineRequest",
    "GetNodePoolRequest",
    "GetVpnConnectionRequest",
    "ListClustersRequest",
    "ListClustersResponse",
    "ListMachinesRequest",
    "ListMachinesResponse",
    "ListNodePoolsRequest",
    "ListNodePoolsResponse",
    "ListVpnConnectionsRequest",
    "ListVpnConnectionsResponse",
    "OperationMetadata",
    "UpdateClusterRequest",
    "UpdateNodePoolRequest",
)
