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
from google.shopping.merchant_datasources import gapic_version as package_version

__version__ = package_version.__version__


from google.shopping.merchant_datasources_v1beta.services.data_sources_service.async_client import (
    DataSourcesServiceAsyncClient,
)
from google.shopping.merchant_datasources_v1beta.services.data_sources_service.client import (
    DataSourcesServiceClient,
)
from google.shopping.merchant_datasources_v1beta.types.datasources import (
    CreateDataSourceRequest,
    DataSource,
    DeleteDataSourceRequest,
    FetchDataSourceRequest,
    GetDataSourceRequest,
    ListDataSourcesRequest,
    ListDataSourcesResponse,
    UpdateDataSourceRequest,
)
from google.shopping.merchant_datasources_v1beta.types.datasourcetypes import (
    LocalInventoryDataSource,
    PrimaryProductDataSource,
    PromotionDataSource,
    RegionalInventoryDataSource,
    SupplementalProductDataSource,
)
from google.shopping.merchant_datasources_v1beta.types.fileinputs import FileInput

__all__ = (
    "DataSourcesServiceClient",
    "DataSourcesServiceAsyncClient",
    "CreateDataSourceRequest",
    "DataSource",
    "DeleteDataSourceRequest",
    "FetchDataSourceRequest",
    "GetDataSourceRequest",
    "ListDataSourcesRequest",
    "ListDataSourcesResponse",
    "UpdateDataSourceRequest",
    "LocalInventoryDataSource",
    "PrimaryProductDataSource",
    "PromotionDataSource",
    "RegionalInventoryDataSource",
    "SupplementalProductDataSource",
    "FileInput",
)
