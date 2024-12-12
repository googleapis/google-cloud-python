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


from .services.data_sources_service import DataSourcesServiceClient
from .services.data_sources_service import DataSourcesServiceAsyncClient
from .services.file_uploads_service import FileUploadsServiceClient
from .services.file_uploads_service import FileUploadsServiceAsyncClient

from .types.datasources import CreateDataSourceRequest
from .types.datasources import DataSource
from .types.datasources import DeleteDataSourceRequest
from .types.datasources import FetchDataSourceRequest
from .types.datasources import GetDataSourceRequest
from .types.datasources import ListDataSourcesRequest
from .types.datasources import ListDataSourcesResponse
from .types.datasources import UpdateDataSourceRequest
from .types.datasourcetypes import DataSourceReference
from .types.datasourcetypes import LocalInventoryDataSource
from .types.datasourcetypes import PrimaryProductDataSource
from .types.datasourcetypes import PromotionDataSource
from .types.datasourcetypes import RegionalInventoryDataSource
from .types.datasourcetypes import SupplementalProductDataSource
from .types.fileinputs import FileInput
from .types.fileuploads import FileUpload
from .types.fileuploads import GetFileUploadRequest

__all__ = (
    'DataSourcesServiceAsyncClient',
    'FileUploadsServiceAsyncClient',
'CreateDataSourceRequest',
'DataSource',
'DataSourceReference',
'DataSourcesServiceClient',
'DeleteDataSourceRequest',
'FetchDataSourceRequest',
'FileInput',
'FileUpload',
'FileUploadsServiceClient',
'GetDataSourceRequest',
'GetFileUploadRequest',
'ListDataSourcesRequest',
'ListDataSourcesResponse',
'LocalInventoryDataSource',
'PrimaryProductDataSource',
'PromotionDataSource',
'RegionalInventoryDataSource',
'SupplementalProductDataSource',
'UpdateDataSourceRequest',
)
