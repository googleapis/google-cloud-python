# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
from google.cloud.gdchardwaremanagement_v1alpha import gapic_version as package_version

__version__ = package_version.__version__


from .services.gdc_hardware_management import GDCHardwareManagementClient
from .services.gdc_hardware_management import GDCHardwareManagementAsyncClient

from .types.resources import ChangeLogEntry
from .types.resources import Comment
from .types.resources import Contact
from .types.resources import Dimensions
from .types.resources import Hardware
from .types.resources import HardwareConfig
from .types.resources import HardwareGroup
from .types.resources import HardwareInstallationInfo
from .types.resources import HardwareLocation
from .types.resources import HardwarePhysicalInfo
from .types.resources import Order
from .types.resources import OrganizationContact
from .types.resources import RackSpace
from .types.resources import Site
from .types.resources import Sku
from .types.resources import SkuConfig
from .types.resources import SkuInstance
from .types.resources import Subnet
from .types.resources import TimePeriod
from .types.resources import Zone
from .types.resources import ZoneNetworkConfig
from .types.resources import PowerSupply
from .types.service import CreateCommentRequest
from .types.service import CreateHardwareGroupRequest
from .types.service import CreateHardwareRequest
from .types.service import CreateOrderRequest
from .types.service import CreateSiteRequest
from .types.service import CreateZoneRequest
from .types.service import DeleteHardwareGroupRequest
from .types.service import DeleteHardwareRequest
from .types.service import DeleteOrderRequest
from .types.service import DeleteZoneRequest
from .types.service import GetChangeLogEntryRequest
from .types.service import GetCommentRequest
from .types.service import GetHardwareGroupRequest
from .types.service import GetHardwareRequest
from .types.service import GetOrderRequest
from .types.service import GetSiteRequest
from .types.service import GetSkuRequest
from .types.service import GetZoneRequest
from .types.service import ListChangeLogEntriesRequest
from .types.service import ListChangeLogEntriesResponse
from .types.service import ListCommentsRequest
from .types.service import ListCommentsResponse
from .types.service import ListHardwareGroupsRequest
from .types.service import ListHardwareGroupsResponse
from .types.service import ListHardwareRequest
from .types.service import ListHardwareResponse
from .types.service import ListOrdersRequest
from .types.service import ListOrdersResponse
from .types.service import ListSitesRequest
from .types.service import ListSitesResponse
from .types.service import ListSkusRequest
from .types.service import ListSkusResponse
from .types.service import ListZonesRequest
from .types.service import ListZonesResponse
from .types.service import OperationMetadata
from .types.service import SignalZoneStateRequest
from .types.service import SubmitOrderRequest
from .types.service import UpdateHardwareGroupRequest
from .types.service import UpdateHardwareRequest
from .types.service import UpdateOrderRequest
from .types.service import UpdateSiteRequest
from .types.service import UpdateZoneRequest

__all__ = (
    'GDCHardwareManagementAsyncClient',
'ChangeLogEntry',
'Comment',
'Contact',
'CreateCommentRequest',
'CreateHardwareGroupRequest',
'CreateHardwareRequest',
'CreateOrderRequest',
'CreateSiteRequest',
'CreateZoneRequest',
'DeleteHardwareGroupRequest',
'DeleteHardwareRequest',
'DeleteOrderRequest',
'DeleteZoneRequest',
'Dimensions',
'GDCHardwareManagementClient',
'GetChangeLogEntryRequest',
'GetCommentRequest',
'GetHardwareGroupRequest',
'GetHardwareRequest',
'GetOrderRequest',
'GetSiteRequest',
'GetSkuRequest',
'GetZoneRequest',
'Hardware',
'HardwareConfig',
'HardwareGroup',
'HardwareInstallationInfo',
'HardwareLocation',
'HardwarePhysicalInfo',
'ListChangeLogEntriesRequest',
'ListChangeLogEntriesResponse',
'ListCommentsRequest',
'ListCommentsResponse',
'ListHardwareGroupsRequest',
'ListHardwareGroupsResponse',
'ListHardwareRequest',
'ListHardwareResponse',
'ListOrdersRequest',
'ListOrdersResponse',
'ListSitesRequest',
'ListSitesResponse',
'ListSkusRequest',
'ListSkusResponse',
'ListZonesRequest',
'ListZonesResponse',
'OperationMetadata',
'Order',
'OrganizationContact',
'PowerSupply',
'RackSpace',
'SignalZoneStateRequest',
'Site',
'Sku',
'SkuConfig',
'SkuInstance',
'SubmitOrderRequest',
'Subnet',
'TimePeriod',
'UpdateHardwareGroupRequest',
'UpdateHardwareRequest',
'UpdateOrderRequest',
'UpdateSiteRequest',
'UpdateZoneRequest',
'Zone',
'ZoneNetworkConfig',
)
