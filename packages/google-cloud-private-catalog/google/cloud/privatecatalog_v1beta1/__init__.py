# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

from .services.private_catalog import PrivateCatalogClient
from .services.private_catalog import PrivateCatalogAsyncClient

from .types.private_catalog import AssetReference
from .types.private_catalog import Catalog
from .types.private_catalog import GcsSource
from .types.private_catalog import GitSource
from .types.private_catalog import Inputs
from .types.private_catalog import Product
from .types.private_catalog import SearchCatalogsRequest
from .types.private_catalog import SearchCatalogsResponse
from .types.private_catalog import SearchProductsRequest
from .types.private_catalog import SearchProductsResponse
from .types.private_catalog import SearchVersionsRequest
from .types.private_catalog import SearchVersionsResponse
from .types.private_catalog import Version

__all__ = (
    "PrivateCatalogAsyncClient",
    "AssetReference",
    "Catalog",
    "GcsSource",
    "GitSource",
    "Inputs",
    "PrivateCatalogClient",
    "Product",
    "SearchCatalogsRequest",
    "SearchCatalogsResponse",
    "SearchProductsRequest",
    "SearchProductsResponse",
    "SearchVersionsRequest",
    "SearchVersionsResponse",
    "Version",
)
