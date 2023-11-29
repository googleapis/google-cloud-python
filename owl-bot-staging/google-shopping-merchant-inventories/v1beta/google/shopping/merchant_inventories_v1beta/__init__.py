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
from google.shopping.merchant_inventories_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.local_inventory_service import LocalInventoryServiceClient
from .services.local_inventory_service import LocalInventoryServiceAsyncClient
from .services.regional_inventory_service import RegionalInventoryServiceClient
from .services.regional_inventory_service import RegionalInventoryServiceAsyncClient

from .types.localinventory import DeleteLocalInventoryRequest
from .types.localinventory import InsertLocalInventoryRequest
from .types.localinventory import ListLocalInventoriesRequest
from .types.localinventory import ListLocalInventoriesResponse
from .types.localinventory import LocalInventory
from .types.regionalinventory import DeleteRegionalInventoryRequest
from .types.regionalinventory import InsertRegionalInventoryRequest
from .types.regionalinventory import ListRegionalInventoriesRequest
from .types.regionalinventory import ListRegionalInventoriesResponse
from .types.regionalinventory import RegionalInventory

__all__ = (
    'LocalInventoryServiceAsyncClient',
    'RegionalInventoryServiceAsyncClient',
'DeleteLocalInventoryRequest',
'DeleteRegionalInventoryRequest',
'InsertLocalInventoryRequest',
'InsertRegionalInventoryRequest',
'ListLocalInventoriesRequest',
'ListLocalInventoriesResponse',
'ListRegionalInventoriesRequest',
'ListRegionalInventoriesResponse',
'LocalInventory',
'LocalInventoryServiceClient',
'RegionalInventory',
'RegionalInventoryServiceClient',
)
