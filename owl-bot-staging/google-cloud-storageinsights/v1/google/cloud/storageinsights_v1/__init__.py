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
from google.cloud.storageinsights_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.storage_insights import StorageInsightsClient
from .services.storage_insights import StorageInsightsAsyncClient

from .types.storageinsights import CloudStorageDestinationOptions
from .types.storageinsights import CloudStorageFilters
from .types.storageinsights import CreateDatasetConfigRequest
from .types.storageinsights import CreateReportConfigRequest
from .types.storageinsights import CSVOptions
from .types.storageinsights import DatasetConfig
from .types.storageinsights import DeleteDatasetConfigRequest
from .types.storageinsights import DeleteReportConfigRequest
from .types.storageinsights import FrequencyOptions
from .types.storageinsights import GetDatasetConfigRequest
from .types.storageinsights import GetReportConfigRequest
from .types.storageinsights import GetReportDetailRequest
from .types.storageinsights import Identity
from .types.storageinsights import LinkDatasetRequest
from .types.storageinsights import LinkDatasetResponse
from .types.storageinsights import ListDatasetConfigsRequest
from .types.storageinsights import ListDatasetConfigsResponse
from .types.storageinsights import ListReportConfigsRequest
from .types.storageinsights import ListReportConfigsResponse
from .types.storageinsights import ListReportDetailsRequest
from .types.storageinsights import ListReportDetailsResponse
from .types.storageinsights import LocationMetadata
from .types.storageinsights import ObjectMetadataReportOptions
from .types.storageinsights import OperationMetadata
from .types.storageinsights import ParquetOptions
from .types.storageinsights import ReportConfig
from .types.storageinsights import ReportDetail
from .types.storageinsights import UnlinkDatasetRequest
from .types.storageinsights import UpdateDatasetConfigRequest
from .types.storageinsights import UpdateReportConfigRequest

__all__ = (
    'StorageInsightsAsyncClient',
'CSVOptions',
'CloudStorageDestinationOptions',
'CloudStorageFilters',
'CreateDatasetConfigRequest',
'CreateReportConfigRequest',
'DatasetConfig',
'DeleteDatasetConfigRequest',
'DeleteReportConfigRequest',
'FrequencyOptions',
'GetDatasetConfigRequest',
'GetReportConfigRequest',
'GetReportDetailRequest',
'Identity',
'LinkDatasetRequest',
'LinkDatasetResponse',
'ListDatasetConfigsRequest',
'ListDatasetConfigsResponse',
'ListReportConfigsRequest',
'ListReportConfigsResponse',
'ListReportDetailsRequest',
'ListReportDetailsResponse',
'LocationMetadata',
'ObjectMetadataReportOptions',
'OperationMetadata',
'ParquetOptions',
'ReportConfig',
'ReportDetail',
'StorageInsightsClient',
'UnlinkDatasetRequest',
'UpdateDatasetConfigRequest',
'UpdateReportConfigRequest',
)
