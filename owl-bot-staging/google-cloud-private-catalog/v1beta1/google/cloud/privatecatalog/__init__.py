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
from google.cloud.privatecatalog import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.privatecatalog_v1beta1.services.private_catalog.client import PrivateCatalogClient
from google.cloud.privatecatalog_v1beta1.services.private_catalog.async_client import PrivateCatalogAsyncClient

from google.cloud.privatecatalog_v1beta1.types.private_catalog import AssetReference
from google.cloud.privatecatalog_v1beta1.types.private_catalog import Catalog
from google.cloud.privatecatalog_v1beta1.types.private_catalog import GcsSource
from google.cloud.privatecatalog_v1beta1.types.private_catalog import GitSource
from google.cloud.privatecatalog_v1beta1.types.private_catalog import Inputs
from google.cloud.privatecatalog_v1beta1.types.private_catalog import Product
from google.cloud.privatecatalog_v1beta1.types.private_catalog import SearchCatalogsRequest
from google.cloud.privatecatalog_v1beta1.types.private_catalog import SearchCatalogsResponse
from google.cloud.privatecatalog_v1beta1.types.private_catalog import SearchProductsRequest
from google.cloud.privatecatalog_v1beta1.types.private_catalog import SearchProductsResponse
from google.cloud.privatecatalog_v1beta1.types.private_catalog import SearchVersionsRequest
from google.cloud.privatecatalog_v1beta1.types.private_catalog import SearchVersionsResponse
from google.cloud.privatecatalog_v1beta1.types.private_catalog import Version

__all__ = ('PrivateCatalogClient',
    'PrivateCatalogAsyncClient',
    'AssetReference',
    'Catalog',
    'GcsSource',
    'GitSource',
    'Inputs',
    'Product',
    'SearchCatalogsRequest',
    'SearchCatalogsResponse',
    'SearchProductsRequest',
    'SearchProductsResponse',
    'SearchVersionsRequest',
    'SearchVersionsResponse',
    'Version',
)
