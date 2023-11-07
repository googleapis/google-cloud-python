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
from google.cloud.edgenetwork_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.edge_network import EdgeNetworkClient
from .services.edge_network import EdgeNetworkAsyncClient

from .types.resources import Interconnect
from .types.resources import InterconnectAttachment
from .types.resources import InterconnectDiagnostics
from .types.resources import LinkLayerAddress
from .types.resources import Network
from .types.resources import Router
from .types.resources import RouterStatus
from .types.resources import Subnet
from .types.resources import SubnetStatus
from .types.resources import Zone
from .types.resources import ResourceState
from .types.service import CreateInterconnectAttachmentRequest
from .types.service import CreateNetworkRequest
from .types.service import CreateRouterRequest
from .types.service import CreateSubnetRequest
from .types.service import DeleteInterconnectAttachmentRequest
from .types.service import DeleteNetworkRequest
from .types.service import DeleteRouterRequest
from .types.service import DeleteSubnetRequest
from .types.service import DiagnoseInterconnectRequest
from .types.service import DiagnoseInterconnectResponse
from .types.service import DiagnoseNetworkRequest
from .types.service import DiagnoseNetworkResponse
from .types.service import DiagnoseRouterRequest
from .types.service import DiagnoseRouterResponse
from .types.service import GetInterconnectAttachmentRequest
from .types.service import GetInterconnectRequest
from .types.service import GetNetworkRequest
from .types.service import GetRouterRequest
from .types.service import GetSubnetRequest
from .types.service import GetZoneRequest
from .types.service import InitializeZoneRequest
from .types.service import InitializeZoneResponse
from .types.service import ListInterconnectAttachmentsRequest
from .types.service import ListInterconnectAttachmentsResponse
from .types.service import ListInterconnectsRequest
from .types.service import ListInterconnectsResponse
from .types.service import ListNetworksRequest
from .types.service import ListNetworksResponse
from .types.service import ListRoutersRequest
from .types.service import ListRoutersResponse
from .types.service import ListSubnetsRequest
from .types.service import ListSubnetsResponse
from .types.service import ListZonesRequest
from .types.service import ListZonesResponse
from .types.service import OperationMetadata
from .types.service import UpdateRouterRequest
from .types.service import UpdateSubnetRequest

__all__ = (
    'EdgeNetworkAsyncClient',
'CreateInterconnectAttachmentRequest',
'CreateNetworkRequest',
'CreateRouterRequest',
'CreateSubnetRequest',
'DeleteInterconnectAttachmentRequest',
'DeleteNetworkRequest',
'DeleteRouterRequest',
'DeleteSubnetRequest',
'DiagnoseInterconnectRequest',
'DiagnoseInterconnectResponse',
'DiagnoseNetworkRequest',
'DiagnoseNetworkResponse',
'DiagnoseRouterRequest',
'DiagnoseRouterResponse',
'EdgeNetworkClient',
'GetInterconnectAttachmentRequest',
'GetInterconnectRequest',
'GetNetworkRequest',
'GetRouterRequest',
'GetSubnetRequest',
'GetZoneRequest',
'InitializeZoneRequest',
'InitializeZoneResponse',
'Interconnect',
'InterconnectAttachment',
'InterconnectDiagnostics',
'LinkLayerAddress',
'ListInterconnectAttachmentsRequest',
'ListInterconnectAttachmentsResponse',
'ListInterconnectsRequest',
'ListInterconnectsResponse',
'ListNetworksRequest',
'ListNetworksResponse',
'ListRoutersRequest',
'ListRoutersResponse',
'ListSubnetsRequest',
'ListSubnetsResponse',
'ListZonesRequest',
'ListZonesResponse',
'Network',
'OperationMetadata',
'ResourceState',
'Router',
'RouterStatus',
'Subnet',
'SubnetStatus',
'UpdateRouterRequest',
'UpdateSubnetRequest',
'Zone',
)
