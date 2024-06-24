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
from google.cloud.gdchardwaremanagement import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.gdchardwaremanagement_v1alpha.services.gdc_hardware_management.client import GDCHardwareManagementClient
from google.cloud.gdchardwaremanagement_v1alpha.services.gdc_hardware_management.async_client import GDCHardwareManagementAsyncClient

from google.cloud.gdchardwaremanagement_v1alpha.types.resources import ChangeLogEntry
from google.cloud.gdchardwaremanagement_v1alpha.types.resources import Comment
from google.cloud.gdchardwaremanagement_v1alpha.types.resources import Contact
from google.cloud.gdchardwaremanagement_v1alpha.types.resources import Dimensions
from google.cloud.gdchardwaremanagement_v1alpha.types.resources import Hardware
from google.cloud.gdchardwaremanagement_v1alpha.types.resources import HardwareConfig
from google.cloud.gdchardwaremanagement_v1alpha.types.resources import HardwareGroup
from google.cloud.gdchardwaremanagement_v1alpha.types.resources import HardwareInstallationInfo
from google.cloud.gdchardwaremanagement_v1alpha.types.resources import HardwareLocation
from google.cloud.gdchardwaremanagement_v1alpha.types.resources import HardwarePhysicalInfo
from google.cloud.gdchardwaremanagement_v1alpha.types.resources import Order
from google.cloud.gdchardwaremanagement_v1alpha.types.resources import OrganizationContact
from google.cloud.gdchardwaremanagement_v1alpha.types.resources import RackSpace
from google.cloud.gdchardwaremanagement_v1alpha.types.resources import Site
from google.cloud.gdchardwaremanagement_v1alpha.types.resources import Sku
from google.cloud.gdchardwaremanagement_v1alpha.types.resources import SkuConfig
from google.cloud.gdchardwaremanagement_v1alpha.types.resources import SkuInstance
from google.cloud.gdchardwaremanagement_v1alpha.types.resources import Subnet
from google.cloud.gdchardwaremanagement_v1alpha.types.resources import TimePeriod
from google.cloud.gdchardwaremanagement_v1alpha.types.resources import Zone
from google.cloud.gdchardwaremanagement_v1alpha.types.resources import ZoneNetworkConfig
from google.cloud.gdchardwaremanagement_v1alpha.types.resources import PowerSupply
from google.cloud.gdchardwaremanagement_v1alpha.types.service import CreateCommentRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import CreateHardwareGroupRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import CreateHardwareRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import CreateOrderRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import CreateSiteRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import CreateZoneRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import DeleteHardwareGroupRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import DeleteHardwareRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import DeleteOrderRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import DeleteZoneRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import GetChangeLogEntryRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import GetCommentRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import GetHardwareGroupRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import GetHardwareRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import GetOrderRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import GetSiteRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import GetSkuRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import GetZoneRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import ListChangeLogEntriesRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import ListChangeLogEntriesResponse
from google.cloud.gdchardwaremanagement_v1alpha.types.service import ListCommentsRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import ListCommentsResponse
from google.cloud.gdchardwaremanagement_v1alpha.types.service import ListHardwareGroupsRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import ListHardwareGroupsResponse
from google.cloud.gdchardwaremanagement_v1alpha.types.service import ListHardwareRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import ListHardwareResponse
from google.cloud.gdchardwaremanagement_v1alpha.types.service import ListOrdersRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import ListOrdersResponse
from google.cloud.gdchardwaremanagement_v1alpha.types.service import ListSitesRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import ListSitesResponse
from google.cloud.gdchardwaremanagement_v1alpha.types.service import ListSkusRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import ListSkusResponse
from google.cloud.gdchardwaremanagement_v1alpha.types.service import ListZonesRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import ListZonesResponse
from google.cloud.gdchardwaremanagement_v1alpha.types.service import OperationMetadata
from google.cloud.gdchardwaremanagement_v1alpha.types.service import SubmitOrderRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import UpdateHardwareGroupRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import UpdateHardwareRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import UpdateOrderRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import UpdateSiteRequest
from google.cloud.gdchardwaremanagement_v1alpha.types.service import UpdateZoneRequest

__all__ = ('GDCHardwareManagementClient',
    'GDCHardwareManagementAsyncClient',
    'ChangeLogEntry',
    'Comment',
    'Contact',
    'Dimensions',
    'Hardware',
    'HardwareConfig',
    'HardwareGroup',
    'HardwareInstallationInfo',
    'HardwareLocation',
    'HardwarePhysicalInfo',
    'Order',
    'OrganizationContact',
    'RackSpace',
    'Site',
    'Sku',
    'SkuConfig',
    'SkuInstance',
    'Subnet',
    'TimePeriod',
    'Zone',
    'ZoneNetworkConfig',
    'PowerSupply',
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
    'GetChangeLogEntryRequest',
    'GetCommentRequest',
    'GetHardwareGroupRequest',
    'GetHardwareRequest',
    'GetOrderRequest',
    'GetSiteRequest',
    'GetSkuRequest',
    'GetZoneRequest',
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
    'SubmitOrderRequest',
    'UpdateHardwareGroupRequest',
    'UpdateHardwareRequest',
    'UpdateOrderRequest',
    'UpdateSiteRequest',
    'UpdateZoneRequest',
)
