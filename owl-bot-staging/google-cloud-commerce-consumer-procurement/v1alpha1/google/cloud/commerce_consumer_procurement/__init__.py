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
from google.cloud.commerce_consumer_procurement import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.commerce_consumer_procurement_v1alpha1.services.consumer_procurement_service.client import ConsumerProcurementServiceClient
from google.cloud.commerce_consumer_procurement_v1alpha1.services.consumer_procurement_service.async_client import ConsumerProcurementServiceAsyncClient

from google.cloud.commerce_consumer_procurement_v1alpha1.types.order import LineItem
from google.cloud.commerce_consumer_procurement_v1alpha1.types.order import LineItemChange
from google.cloud.commerce_consumer_procurement_v1alpha1.types.order import LineItemInfo
from google.cloud.commerce_consumer_procurement_v1alpha1.types.order import Order
from google.cloud.commerce_consumer_procurement_v1alpha1.types.order import Parameter
from google.cloud.commerce_consumer_procurement_v1alpha1.types.order import Subscription
from google.cloud.commerce_consumer_procurement_v1alpha1.types.order import LineItemChangeState
from google.cloud.commerce_consumer_procurement_v1alpha1.types.order import LineItemChangeStateReasonType
from google.cloud.commerce_consumer_procurement_v1alpha1.types.order import LineItemChangeType
from google.cloud.commerce_consumer_procurement_v1alpha1.types.procurement_service import GetOrderRequest
from google.cloud.commerce_consumer_procurement_v1alpha1.types.procurement_service import ListOrdersRequest
from google.cloud.commerce_consumer_procurement_v1alpha1.types.procurement_service import ListOrdersResponse
from google.cloud.commerce_consumer_procurement_v1alpha1.types.procurement_service import PlaceOrderMetadata
from google.cloud.commerce_consumer_procurement_v1alpha1.types.procurement_service import PlaceOrderRequest

__all__ = ('ConsumerProcurementServiceClient',
    'ConsumerProcurementServiceAsyncClient',
    'LineItem',
    'LineItemChange',
    'LineItemInfo',
    'Order',
    'Parameter',
    'Subscription',
    'LineItemChangeState',
    'LineItemChangeStateReasonType',
    'LineItemChangeType',
    'GetOrderRequest',
    'ListOrdersRequest',
    'ListOrdersResponse',
    'PlaceOrderMetadata',
    'PlaceOrderRequest',
)
