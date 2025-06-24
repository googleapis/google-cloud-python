# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from google.cloud.edgenetwork import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.edgenetwork_v1.services.edge_network.async_client import (
    EdgeNetworkAsyncClient,
)
from google.cloud.edgenetwork_v1.services.edge_network.client import EdgeNetworkClient
from google.cloud.edgenetwork_v1.types.resources import (
    Interconnect,
    InterconnectAttachment,
    InterconnectDiagnostics,
    LinkLayerAddress,
    Network,
    ResourceState,
    Router,
    RouterStatus,
    Subnet,
    SubnetStatus,
    Zone,
)
from google.cloud.edgenetwork_v1.types.service import (
    CreateInterconnectAttachmentRequest,
    CreateNetworkRequest,
    CreateRouterRequest,
    CreateSubnetRequest,
    DeleteInterconnectAttachmentRequest,
    DeleteNetworkRequest,
    DeleteRouterRequest,
    DeleteSubnetRequest,
    DiagnoseInterconnectRequest,
    DiagnoseInterconnectResponse,
    DiagnoseNetworkRequest,
    DiagnoseNetworkResponse,
    DiagnoseRouterRequest,
    DiagnoseRouterResponse,
    GetInterconnectAttachmentRequest,
    GetInterconnectRequest,
    GetNetworkRequest,
    GetRouterRequest,
    GetSubnetRequest,
    GetZoneRequest,
    InitializeZoneRequest,
    InitializeZoneResponse,
    ListInterconnectAttachmentsRequest,
    ListInterconnectAttachmentsResponse,
    ListInterconnectsRequest,
    ListInterconnectsResponse,
    ListNetworksRequest,
    ListNetworksResponse,
    ListRoutersRequest,
    ListRoutersResponse,
    ListSubnetsRequest,
    ListSubnetsResponse,
    ListZonesRequest,
    ListZonesResponse,
    OperationMetadata,
    UpdateRouterRequest,
    UpdateSubnetRequest,
)

__all__ = (
    "EdgeNetworkClient",
    "EdgeNetworkAsyncClient",
    "Interconnect",
    "InterconnectAttachment",
    "InterconnectDiagnostics",
    "LinkLayerAddress",
    "Network",
    "Router",
    "RouterStatus",
    "Subnet",
    "SubnetStatus",
    "Zone",
    "ResourceState",
    "CreateInterconnectAttachmentRequest",
    "CreateNetworkRequest",
    "CreateRouterRequest",
    "CreateSubnetRequest",
    "DeleteInterconnectAttachmentRequest",
    "DeleteNetworkRequest",
    "DeleteRouterRequest",
    "DeleteSubnetRequest",
    "DiagnoseInterconnectRequest",
    "DiagnoseInterconnectResponse",
    "DiagnoseNetworkRequest",
    "DiagnoseNetworkResponse",
    "DiagnoseRouterRequest",
    "DiagnoseRouterResponse",
    "GetInterconnectAttachmentRequest",
    "GetInterconnectRequest",
    "GetNetworkRequest",
    "GetRouterRequest",
    "GetSubnetRequest",
    "GetZoneRequest",
    "InitializeZoneRequest",
    "InitializeZoneResponse",
    "ListInterconnectAttachmentsRequest",
    "ListInterconnectAttachmentsResponse",
    "ListInterconnectsRequest",
    "ListInterconnectsResponse",
    "ListNetworksRequest",
    "ListNetworksResponse",
    "ListRoutersRequest",
    "ListRoutersResponse",
    "ListSubnetsRequest",
    "ListSubnetsResponse",
    "ListZonesRequest",
    "ListZonesResponse",
    "OperationMetadata",
    "UpdateRouterRequest",
    "UpdateSubnetRequest",
)
