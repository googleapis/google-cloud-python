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
from google.shopping.merchant_lfp_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.lfp_inventory_service import LfpInventoryServiceClient
from .services.lfp_inventory_service import LfpInventoryServiceAsyncClient
from .services.lfp_merchant_state_service import LfpMerchantStateServiceClient
from .services.lfp_merchant_state_service import LfpMerchantStateServiceAsyncClient
from .services.lfp_sale_service import LfpSaleServiceClient
from .services.lfp_sale_service import LfpSaleServiceAsyncClient
from .services.lfp_store_service import LfpStoreServiceClient
from .services.lfp_store_service import LfpStoreServiceAsyncClient

from .types.lfpinventory import InsertLfpInventoryRequest
from .types.lfpinventory import LfpInventory
from .types.lfpmerchantstate import GetLfpMerchantStateRequest
from .types.lfpmerchantstate import LfpMerchantState
from .types.lfpsale import InsertLfpSaleRequest
from .types.lfpsale import LfpSale
from .types.lfpstore import DeleteLfpStoreRequest
from .types.lfpstore import GetLfpStoreRequest
from .types.lfpstore import InsertLfpStoreRequest
from .types.lfpstore import LfpStore
from .types.lfpstore import ListLfpStoresRequest
from .types.lfpstore import ListLfpStoresResponse

__all__ = (
    'LfpInventoryServiceAsyncClient',
    'LfpMerchantStateServiceAsyncClient',
    'LfpSaleServiceAsyncClient',
    'LfpStoreServiceAsyncClient',
'DeleteLfpStoreRequest',
'GetLfpMerchantStateRequest',
'GetLfpStoreRequest',
'InsertLfpInventoryRequest',
'InsertLfpSaleRequest',
'InsertLfpStoreRequest',
'LfpInventory',
'LfpInventoryServiceClient',
'LfpMerchantState',
'LfpMerchantStateServiceClient',
'LfpSale',
'LfpSaleServiceClient',
'LfpStore',
'LfpStoreServiceClient',
'ListLfpStoresRequest',
'ListLfpStoresResponse',
)
