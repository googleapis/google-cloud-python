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
from google.cloud.storageinsights import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.storageinsights_v1.services.storage_insights.client import StorageInsightsClient
from google.cloud.storageinsights_v1.services.storage_insights.async_client import StorageInsightsAsyncClient

from google.cloud.storageinsights_v1.types.storageinsights import CloudStorageDestinationOptions
from google.cloud.storageinsights_v1.types.storageinsights import CloudStorageFilters
from google.cloud.storageinsights_v1.types.storageinsights import CreateReportConfigRequest
from google.cloud.storageinsights_v1.types.storageinsights import CSVOptions
from google.cloud.storageinsights_v1.types.storageinsights import DeleteReportConfigRequest
from google.cloud.storageinsights_v1.types.storageinsights import FrequencyOptions
from google.cloud.storageinsights_v1.types.storageinsights import GetReportConfigRequest
from google.cloud.storageinsights_v1.types.storageinsights import GetReportDetailRequest
from google.cloud.storageinsights_v1.types.storageinsights import ListReportConfigsRequest
from google.cloud.storageinsights_v1.types.storageinsights import ListReportConfigsResponse
from google.cloud.storageinsights_v1.types.storageinsights import ListReportDetailsRequest
from google.cloud.storageinsights_v1.types.storageinsights import ListReportDetailsResponse
from google.cloud.storageinsights_v1.types.storageinsights import ObjectMetadataReportOptions
from google.cloud.storageinsights_v1.types.storageinsights import OperationMetadata
from google.cloud.storageinsights_v1.types.storageinsights import ParquetOptions
from google.cloud.storageinsights_v1.types.storageinsights import ReportConfig
from google.cloud.storageinsights_v1.types.storageinsights import ReportDetail
from google.cloud.storageinsights_v1.types.storageinsights import UpdateReportConfigRequest

__all__ = ('StorageInsightsClient',
    'StorageInsightsAsyncClient',
    'CloudStorageDestinationOptions',
    'CloudStorageFilters',
    'CreateReportConfigRequest',
    'CSVOptions',
    'DeleteReportConfigRequest',
    'FrequencyOptions',
    'GetReportConfigRequest',
    'GetReportDetailRequest',
    'ListReportConfigsRequest',
    'ListReportConfigsResponse',
    'ListReportDetailsRequest',
    'ListReportDetailsResponse',
    'ObjectMetadataReportOptions',
    'OperationMetadata',
    'ParquetOptions',
    'ReportConfig',
    'ReportDetail',
    'UpdateReportConfigRequest',
)
