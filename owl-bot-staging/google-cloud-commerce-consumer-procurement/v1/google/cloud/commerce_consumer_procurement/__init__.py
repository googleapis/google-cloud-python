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
from google.cloud.commerce_consumer_procurement import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.commerce_consumer_procurement_v1.services.consumer_procurement_service.client import ConsumerProcurementServiceClient
from google.cloud.commerce_consumer_procurement_v1.services.consumer_procurement_service.async_client import ConsumerProcurementServiceAsyncClient
from google.cloud.commerce_consumer_procurement_v1.services.license_management_service.client import LicenseManagementServiceClient
from google.cloud.commerce_consumer_procurement_v1.services.license_management_service.async_client import LicenseManagementServiceAsyncClient

from google.cloud.commerce_consumer_procurement_v1.types.license_management_service import AssignmentProtocol
from google.cloud.commerce_consumer_procurement_v1.types.license_management_service import AssignRequest
from google.cloud.commerce_consumer_procurement_v1.types.license_management_service import AssignResponse
from google.cloud.commerce_consumer_procurement_v1.types.license_management_service import EnumerateLicensedUsersRequest
from google.cloud.commerce_consumer_procurement_v1.types.license_management_service import EnumerateLicensedUsersResponse
from google.cloud.commerce_consumer_procurement_v1.types.license_management_service import GetLicensePoolRequest
from google.cloud.commerce_consumer_procurement_v1.types.license_management_service import LicensedUser
from google.cloud.commerce_consumer_procurement_v1.types.license_management_service import LicensePool
from google.cloud.commerce_consumer_procurement_v1.types.license_management_service import UnassignRequest
from google.cloud.commerce_consumer_procurement_v1.types.license_management_service import UnassignResponse
from google.cloud.commerce_consumer_procurement_v1.types.license_management_service import UpdateLicensePoolRequest
from google.cloud.commerce_consumer_procurement_v1.types.order import LineItem
from google.cloud.commerce_consumer_procurement_v1.types.order import LineItemChange
from google.cloud.commerce_consumer_procurement_v1.types.order import LineItemInfo
from google.cloud.commerce_consumer_procurement_v1.types.order import Order
from google.cloud.commerce_consumer_procurement_v1.types.order import Parameter
from google.cloud.commerce_consumer_procurement_v1.types.order import Subscription
from google.cloud.commerce_consumer_procurement_v1.types.order import LineItemChangeState
from google.cloud.commerce_consumer_procurement_v1.types.order import LineItemChangeStateReasonType
from google.cloud.commerce_consumer_procurement_v1.types.order import LineItemChangeType
from google.cloud.commerce_consumer_procurement_v1.types.procurement_service import CancelOrderMetadata
from google.cloud.commerce_consumer_procurement_v1.types.procurement_service import CancelOrderRequest
from google.cloud.commerce_consumer_procurement_v1.types.procurement_service import GetOrderRequest
from google.cloud.commerce_consumer_procurement_v1.types.procurement_service import ListOrdersRequest
from google.cloud.commerce_consumer_procurement_v1.types.procurement_service import ListOrdersResponse
from google.cloud.commerce_consumer_procurement_v1.types.procurement_service import ModifyOrderMetadata
from google.cloud.commerce_consumer_procurement_v1.types.procurement_service import ModifyOrderRequest
from google.cloud.commerce_consumer_procurement_v1.types.procurement_service import PlaceOrderMetadata
from google.cloud.commerce_consumer_procurement_v1.types.procurement_service import PlaceOrderRequest
from google.cloud.commerce_consumer_procurement_v1.types.procurement_service import AutoRenewalBehavior

__all__ = ('ConsumerProcurementServiceClient',
    'ConsumerProcurementServiceAsyncClient',
    'LicenseManagementServiceClient',
    'LicenseManagementServiceAsyncClient',
    'AssignmentProtocol',
    'AssignRequest',
    'AssignResponse',
    'EnumerateLicensedUsersRequest',
    'EnumerateLicensedUsersResponse',
    'GetLicensePoolRequest',
    'LicensedUser',
    'LicensePool',
    'UnassignRequest',
    'UnassignResponse',
    'UpdateLicensePoolRequest',
    'LineItem',
    'LineItemChange',
    'LineItemInfo',
    'Order',
    'Parameter',
    'Subscription',
    'LineItemChangeState',
    'LineItemChangeStateReasonType',
    'LineItemChangeType',
    'CancelOrderMetadata',
    'CancelOrderRequest',
    'GetOrderRequest',
    'ListOrdersRequest',
    'ListOrdersResponse',
    'ModifyOrderMetadata',
    'ModifyOrderRequest',
    'PlaceOrderMetadata',
    'PlaceOrderRequest',
    'AutoRenewalBehavior',
)
