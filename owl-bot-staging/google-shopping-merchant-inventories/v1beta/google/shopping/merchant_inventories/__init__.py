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
from google.shopping.merchant_inventories import gapic_version as package_version

__version__ = package_version.__version__


from google.shopping.merchant_inventories_v1beta.services.local_inventory_service.client import LocalInventoryServiceClient
from google.shopping.merchant_inventories_v1beta.services.local_inventory_service.async_client import LocalInventoryServiceAsyncClient
from google.shopping.merchant_inventories_v1beta.services.regional_inventory_service.client import RegionalInventoryServiceClient
from google.shopping.merchant_inventories_v1beta.services.regional_inventory_service.async_client import RegionalInventoryServiceAsyncClient

from google.shopping.merchant_inventories_v1beta.types.localinventory import DeleteLocalInventoryRequest
from google.shopping.merchant_inventories_v1beta.types.localinventory import InsertLocalInventoryRequest
from google.shopping.merchant_inventories_v1beta.types.localinventory import ListLocalInventoriesRequest
from google.shopping.merchant_inventories_v1beta.types.localinventory import ListLocalInventoriesResponse
from google.shopping.merchant_inventories_v1beta.types.localinventory import LocalInventory
from google.shopping.merchant_inventories_v1beta.types.regionalinventory import DeleteRegionalInventoryRequest
from google.shopping.merchant_inventories_v1beta.types.regionalinventory import InsertRegionalInventoryRequest
from google.shopping.merchant_inventories_v1beta.types.regionalinventory import ListRegionalInventoriesRequest
from google.shopping.merchant_inventories_v1beta.types.regionalinventory import ListRegionalInventoriesResponse
from google.shopping.merchant_inventories_v1beta.types.regionalinventory import RegionalInventory

__all__ = ('LocalInventoryServiceClient',
    'LocalInventoryServiceAsyncClient',
    'RegionalInventoryServiceClient',
    'RegionalInventoryServiceAsyncClient',
    'DeleteLocalInventoryRequest',
    'InsertLocalInventoryRequest',
    'ListLocalInventoriesRequest',
    'ListLocalInventoriesResponse',
    'LocalInventory',
    'DeleteRegionalInventoryRequest',
    'InsertRegionalInventoryRequest',
    'ListRegionalInventoriesRequest',
    'ListRegionalInventoriesResponse',
    'RegionalInventory',
)
