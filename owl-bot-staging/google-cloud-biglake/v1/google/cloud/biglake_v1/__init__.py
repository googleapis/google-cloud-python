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
from google.cloud.biglake_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.iceberg_catalog_service import IcebergCatalogServiceClient
from .services.iceberg_catalog_service import IcebergCatalogServiceAsyncClient

from .types.iceberg_rest_catalog import CreateIcebergCatalogRequest
from .types.iceberg_rest_catalog import FailoverIcebergCatalogRequest
from .types.iceberg_rest_catalog import FailoverIcebergCatalogResponse
from .types.iceberg_rest_catalog import GetIcebergCatalogRequest
from .types.iceberg_rest_catalog import IcebergCatalog
from .types.iceberg_rest_catalog import ListIcebergCatalogsRequest
from .types.iceberg_rest_catalog import ListIcebergCatalogsResponse
from .types.iceberg_rest_catalog import UpdateIcebergCatalogRequest

__all__ = (
    'IcebergCatalogServiceAsyncClient',
'CreateIcebergCatalogRequest',
'FailoverIcebergCatalogRequest',
'FailoverIcebergCatalogResponse',
'GetIcebergCatalogRequest',
'IcebergCatalog',
'IcebergCatalogServiceClient',
'ListIcebergCatalogsRequest',
'ListIcebergCatalogsResponse',
'UpdateIcebergCatalogRequest',
)
