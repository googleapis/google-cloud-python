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
from google.cloud.edgenetwork import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.edgenetwork_v1.services.edge_network.client import EdgeNetworkClient
from google.cloud.edgenetwork_v1.services.edge_network.async_client import EdgeNetworkAsyncClient

from google.cloud.edgenetwork_v1.types.resources import Interconnect
from google.cloud.edgenetwork_v1.types.resources import InterconnectAttachment
from google.cloud.edgenetwork_v1.types.resources import InterconnectDiagnostics
from google.cloud.edgenetwork_v1.types.resources import LinkLayerAddress
from google.cloud.edgenetwork_v1.types.resources import Network
from google.cloud.edgenetwork_v1.types.resources import Router
from google.cloud.edgenetwork_v1.types.resources import RouterStatus
from google.cloud.edgenetwork_v1.types.resources import Subnet
from google.cloud.edgenetwork_v1.types.resources import SubnetStatus
from google.cloud.edgenetwork_v1.types.resources import Zone
from google.cloud.edgenetwork_v1.types.resources import ResourceState
from google.cloud.edgenetwork_v1.types.service import CreateInterconnectAttachmentRequest
from google.cloud.edgenetwork_v1.types.service import CreateNetworkRequest
from google.cloud.edgenetwork_v1.types.service import CreateRouterRequest
from google.cloud.edgenetwork_v1.types.service import CreateSubnetRequest
from google.cloud.edgenetwork_v1.types.service import DeleteInterconnectAttachmentRequest
from google.cloud.edgenetwork_v1.types.service import DeleteNetworkRequest
from google.cloud.edgenetwork_v1.types.service import DeleteRouterRequest
from google.cloud.edgenetwork_v1.types.service import DeleteSubnetRequest
from google.cloud.edgenetwork_v1.types.service import DiagnoseInterconnectRequest
from google.cloud.edgenetwork_v1.types.service import DiagnoseInterconnectResponse
from google.cloud.edgenetwork_v1.types.service import DiagnoseNetworkRequest
from google.cloud.edgenetwork_v1.types.service import DiagnoseNetworkResponse
from google.cloud.edgenetwork_v1.types.service import DiagnoseRouterRequest
from google.cloud.edgenetwork_v1.types.service import DiagnoseRouterResponse
from google.cloud.edgenetwork_v1.types.service import GetInterconnectAttachmentRequest
from google.cloud.edgenetwork_v1.types.service import GetInterconnectRequest
from google.cloud.edgenetwork_v1.types.service import GetNetworkRequest
from google.cloud.edgenetwork_v1.types.service import GetRouterRequest
from google.cloud.edgenetwork_v1.types.service import GetSubnetRequest
from google.cloud.edgenetwork_v1.types.service import GetZoneRequest
from google.cloud.edgenetwork_v1.types.service import InitializeZoneRequest
from google.cloud.edgenetwork_v1.types.service import InitializeZoneResponse
from google.cloud.edgenetwork_v1.types.service import ListInterconnectAttachmentsRequest
from google.cloud.edgenetwork_v1.types.service import ListInterconnectAttachmentsResponse
from google.cloud.edgenetwork_v1.types.service import ListInterconnectsRequest
from google.cloud.edgenetwork_v1.types.service import ListInterconnectsResponse
from google.cloud.edgenetwork_v1.types.service import ListNetworksRequest
from google.cloud.edgenetwork_v1.types.service import ListNetworksResponse
from google.cloud.edgenetwork_v1.types.service import ListRoutersRequest
from google.cloud.edgenetwork_v1.types.service import ListRoutersResponse
from google.cloud.edgenetwork_v1.types.service import ListSubnetsRequest
from google.cloud.edgenetwork_v1.types.service import ListSubnetsResponse
from google.cloud.edgenetwork_v1.types.service import ListZonesRequest
from google.cloud.edgenetwork_v1.types.service import ListZonesResponse
from google.cloud.edgenetwork_v1.types.service import OperationMetadata
from google.cloud.edgenetwork_v1.types.service import UpdateRouterRequest
from google.cloud.edgenetwork_v1.types.service import UpdateSubnetRequest

__all__ = ('EdgeNetworkClient',
    'EdgeNetworkAsyncClient',
    'Interconnect',
    'InterconnectAttachment',
    'InterconnectDiagnostics',
    'LinkLayerAddress',
    'Network',
    'Router',
    'RouterStatus',
    'Subnet',
    'SubnetStatus',
    'Zone',
    'ResourceState',
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
    'GetInterconnectAttachmentRequest',
    'GetInterconnectRequest',
    'GetNetworkRequest',
    'GetRouterRequest',
    'GetSubnetRequest',
    'GetZoneRequest',
    'InitializeZoneRequest',
    'InitializeZoneResponse',
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
    'OperationMetadata',
    'UpdateRouterRequest',
    'UpdateSubnetRequest',
)
