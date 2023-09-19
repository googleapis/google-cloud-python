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
from google.cloud.commerce_consumer_procurement_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.consumer_procurement_service import ConsumerProcurementServiceClient
from .services.consumer_procurement_service import ConsumerProcurementServiceAsyncClient

from .types.order import LineItem
from .types.order import LineItemChange
from .types.order import LineItemInfo
from .types.order import Order
from .types.order import Parameter
from .types.order import Subscription
from .types.order import LineItemChangeState
from .types.order import LineItemChangeStateReasonType
from .types.order import LineItemChangeType
from .types.procurement_service import GetOrderRequest
from .types.procurement_service import ListOrdersRequest
from .types.procurement_service import ListOrdersResponse
from .types.procurement_service import PlaceOrderMetadata
from .types.procurement_service import PlaceOrderRequest

__all__ = (
    'ConsumerProcurementServiceAsyncClient',
'ConsumerProcurementServiceClient',
'GetOrderRequest',
'LineItem',
'LineItemChange',
'LineItemChangeState',
'LineItemChangeStateReasonType',
'LineItemChangeType',
'LineItemInfo',
'ListOrdersRequest',
'ListOrdersResponse',
'Order',
'Parameter',
'PlaceOrderMetadata',
'PlaceOrderRequest',
'Subscription',
)
