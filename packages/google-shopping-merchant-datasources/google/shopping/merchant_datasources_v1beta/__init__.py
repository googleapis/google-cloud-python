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
from google.shopping.merchant_datasources_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.data_sources_service import (
    DataSourcesServiceAsyncClient,
    DataSourcesServiceClient,
)
from .types.datasources import (
    CreateDataSourceRequest,
    DataSource,
    DeleteDataSourceRequest,
    FetchDataSourceRequest,
    GetDataSourceRequest,
    ListDataSourcesRequest,
    ListDataSourcesResponse,
    UpdateDataSourceRequest,
)
from .types.datasourcetypes import (
    LocalInventoryDataSource,
    PrimaryProductDataSource,
    PromotionDataSource,
    RegionalInventoryDataSource,
    SupplementalProductDataSource,
)
from .types.fileinputs import FileInput

__all__ = (
    "DataSourcesServiceAsyncClient",
    "CreateDataSourceRequest",
    "DataSource",
    "DataSourcesServiceClient",
    "DeleteDataSourceRequest",
    "FetchDataSourceRequest",
    "FileInput",
    "GetDataSourceRequest",
    "ListDataSourcesRequest",
    "ListDataSourcesResponse",
    "LocalInventoryDataSource",
    "PrimaryProductDataSource",
    "PromotionDataSource",
    "RegionalInventoryDataSource",
    "SupplementalProductDataSource",
    "UpdateDataSourceRequest",
)
