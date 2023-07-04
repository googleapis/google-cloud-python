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
from google.cloud.dataplex import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.dataplex_v1.services.content_service.client import ContentServiceClient
from google.cloud.dataplex_v1.services.content_service.async_client import ContentServiceAsyncClient
from google.cloud.dataplex_v1.services.dataplex_service.client import DataplexServiceClient
from google.cloud.dataplex_v1.services.dataplex_service.async_client import DataplexServiceAsyncClient
from google.cloud.dataplex_v1.services.data_scan_service.client import DataScanServiceClient
from google.cloud.dataplex_v1.services.data_scan_service.async_client import DataScanServiceAsyncClient
from google.cloud.dataplex_v1.services.metadata_service.client import MetadataServiceClient
from google.cloud.dataplex_v1.services.metadata_service.async_client import MetadataServiceAsyncClient

from google.cloud.dataplex_v1.types.analyze import Content
from google.cloud.dataplex_v1.types.analyze import Environment
from google.cloud.dataplex_v1.types.analyze import Session
from google.cloud.dataplex_v1.types.content import CreateContentRequest
from google.cloud.dataplex_v1.types.content import DeleteContentRequest
from google.cloud.dataplex_v1.types.content import GetContentRequest
from google.cloud.dataplex_v1.types.content import ListContentRequest
from google.cloud.dataplex_v1.types.content import ListContentResponse
from google.cloud.dataplex_v1.types.content import UpdateContentRequest
from google.cloud.dataplex_v1.types.data_profile import DataProfileResult
from google.cloud.dataplex_v1.types.data_profile import DataProfileSpec
from google.cloud.dataplex_v1.types.data_quality import DataQualityDimensionResult
from google.cloud.dataplex_v1.types.data_quality import DataQualityResult
from google.cloud.dataplex_v1.types.data_quality import DataQualityRule
from google.cloud.dataplex_v1.types.data_quality import DataQualityRuleResult
from google.cloud.dataplex_v1.types.data_quality import DataQualitySpec
from google.cloud.dataplex_v1.types.datascans import CreateDataScanRequest
from google.cloud.dataplex_v1.types.datascans import DataScan
from google.cloud.dataplex_v1.types.datascans import DataScanJob
from google.cloud.dataplex_v1.types.datascans import DeleteDataScanRequest
from google.cloud.dataplex_v1.types.datascans import GetDataScanJobRequest
from google.cloud.dataplex_v1.types.datascans import GetDataScanRequest
from google.cloud.dataplex_v1.types.datascans import ListDataScanJobsRequest
from google.cloud.dataplex_v1.types.datascans import ListDataScanJobsResponse
from google.cloud.dataplex_v1.types.datascans import ListDataScansRequest
from google.cloud.dataplex_v1.types.datascans import ListDataScansResponse
from google.cloud.dataplex_v1.types.datascans import RunDataScanRequest
from google.cloud.dataplex_v1.types.datascans import RunDataScanResponse
from google.cloud.dataplex_v1.types.datascans import UpdateDataScanRequest
from google.cloud.dataplex_v1.types.datascans import DataScanType
from google.cloud.dataplex_v1.types.logs import DataScanEvent
from google.cloud.dataplex_v1.types.logs import DiscoveryEvent
from google.cloud.dataplex_v1.types.logs import JobEvent
from google.cloud.dataplex_v1.types.logs import SessionEvent
from google.cloud.dataplex_v1.types.metadata_ import CreateEntityRequest
from google.cloud.dataplex_v1.types.metadata_ import CreatePartitionRequest
from google.cloud.dataplex_v1.types.metadata_ import DeleteEntityRequest
from google.cloud.dataplex_v1.types.metadata_ import DeletePartitionRequest
from google.cloud.dataplex_v1.types.metadata_ import Entity
from google.cloud.dataplex_v1.types.metadata_ import GetEntityRequest
from google.cloud.dataplex_v1.types.metadata_ import GetPartitionRequest
from google.cloud.dataplex_v1.types.metadata_ import ListEntitiesRequest
from google.cloud.dataplex_v1.types.metadata_ import ListEntitiesResponse
from google.cloud.dataplex_v1.types.metadata_ import ListPartitionsRequest
from google.cloud.dataplex_v1.types.metadata_ import ListPartitionsResponse
from google.cloud.dataplex_v1.types.metadata_ import Partition
from google.cloud.dataplex_v1.types.metadata_ import Schema
from google.cloud.dataplex_v1.types.metadata_ import StorageAccess
from google.cloud.dataplex_v1.types.metadata_ import StorageFormat
from google.cloud.dataplex_v1.types.metadata_ import UpdateEntityRequest
from google.cloud.dataplex_v1.types.metadata_ import StorageSystem
from google.cloud.dataplex_v1.types.processing import DataSource
from google.cloud.dataplex_v1.types.processing import ScannedData
from google.cloud.dataplex_v1.types.processing import Trigger
from google.cloud.dataplex_v1.types.resources import Action
from google.cloud.dataplex_v1.types.resources import Asset
from google.cloud.dataplex_v1.types.resources import AssetStatus
from google.cloud.dataplex_v1.types.resources import Lake
from google.cloud.dataplex_v1.types.resources import Zone
from google.cloud.dataplex_v1.types.resources import State
from google.cloud.dataplex_v1.types.service import CancelJobRequest
from google.cloud.dataplex_v1.types.service import CreateAssetRequest
from google.cloud.dataplex_v1.types.service import CreateEnvironmentRequest
from google.cloud.dataplex_v1.types.service import CreateLakeRequest
from google.cloud.dataplex_v1.types.service import CreateTaskRequest
from google.cloud.dataplex_v1.types.service import CreateZoneRequest
from google.cloud.dataplex_v1.types.service import DeleteAssetRequest
from google.cloud.dataplex_v1.types.service import DeleteEnvironmentRequest
from google.cloud.dataplex_v1.types.service import DeleteLakeRequest
from google.cloud.dataplex_v1.types.service import DeleteTaskRequest
from google.cloud.dataplex_v1.types.service import DeleteZoneRequest
from google.cloud.dataplex_v1.types.service import GetAssetRequest
from google.cloud.dataplex_v1.types.service import GetEnvironmentRequest
from google.cloud.dataplex_v1.types.service import GetJobRequest
from google.cloud.dataplex_v1.types.service import GetLakeRequest
from google.cloud.dataplex_v1.types.service import GetTaskRequest
from google.cloud.dataplex_v1.types.service import GetZoneRequest
from google.cloud.dataplex_v1.types.service import ListActionsResponse
from google.cloud.dataplex_v1.types.service import ListAssetActionsRequest
from google.cloud.dataplex_v1.types.service import ListAssetsRequest
from google.cloud.dataplex_v1.types.service import ListAssetsResponse
from google.cloud.dataplex_v1.types.service import ListEnvironmentsRequest
from google.cloud.dataplex_v1.types.service import ListEnvironmentsResponse
from google.cloud.dataplex_v1.types.service import ListJobsRequest
from google.cloud.dataplex_v1.types.service import ListJobsResponse
from google.cloud.dataplex_v1.types.service import ListLakeActionsRequest
from google.cloud.dataplex_v1.types.service import ListLakesRequest
from google.cloud.dataplex_v1.types.service import ListLakesResponse
from google.cloud.dataplex_v1.types.service import ListSessionsRequest
from google.cloud.dataplex_v1.types.service import ListSessionsResponse
from google.cloud.dataplex_v1.types.service import ListTasksRequest
from google.cloud.dataplex_v1.types.service import ListTasksResponse
from google.cloud.dataplex_v1.types.service import ListZoneActionsRequest
from google.cloud.dataplex_v1.types.service import ListZonesRequest
from google.cloud.dataplex_v1.types.service import ListZonesResponse
from google.cloud.dataplex_v1.types.service import OperationMetadata
from google.cloud.dataplex_v1.types.service import RunTaskRequest
from google.cloud.dataplex_v1.types.service import RunTaskResponse
from google.cloud.dataplex_v1.types.service import UpdateAssetRequest
from google.cloud.dataplex_v1.types.service import UpdateEnvironmentRequest
from google.cloud.dataplex_v1.types.service import UpdateLakeRequest
from google.cloud.dataplex_v1.types.service import UpdateTaskRequest
from google.cloud.dataplex_v1.types.service import UpdateZoneRequest
from google.cloud.dataplex_v1.types.tasks import Job
from google.cloud.dataplex_v1.types.tasks import Task

__all__ = ('ContentServiceClient',
    'ContentServiceAsyncClient',
    'DataplexServiceClient',
    'DataplexServiceAsyncClient',
    'DataScanServiceClient',
    'DataScanServiceAsyncClient',
    'MetadataServiceClient',
    'MetadataServiceAsyncClient',
    'Content',
    'Environment',
    'Session',
    'CreateContentRequest',
    'DeleteContentRequest',
    'GetContentRequest',
    'ListContentRequest',
    'ListContentResponse',
    'UpdateContentRequest',
    'DataProfileResult',
    'DataProfileSpec',
    'DataQualityDimensionResult',
    'DataQualityResult',
    'DataQualityRule',
    'DataQualityRuleResult',
    'DataQualitySpec',
    'CreateDataScanRequest',
    'DataScan',
    'DataScanJob',
    'DeleteDataScanRequest',
    'GetDataScanJobRequest',
    'GetDataScanRequest',
    'ListDataScanJobsRequest',
    'ListDataScanJobsResponse',
    'ListDataScansRequest',
    'ListDataScansResponse',
    'RunDataScanRequest',
    'RunDataScanResponse',
    'UpdateDataScanRequest',
    'DataScanType',
    'DataScanEvent',
    'DiscoveryEvent',
    'JobEvent',
    'SessionEvent',
    'CreateEntityRequest',
    'CreatePartitionRequest',
    'DeleteEntityRequest',
    'DeletePartitionRequest',
    'Entity',
    'GetEntityRequest',
    'GetPartitionRequest',
    'ListEntitiesRequest',
    'ListEntitiesResponse',
    'ListPartitionsRequest',
    'ListPartitionsResponse',
    'Partition',
    'Schema',
    'StorageAccess',
    'StorageFormat',
    'UpdateEntityRequest',
    'StorageSystem',
    'DataSource',
    'ScannedData',
    'Trigger',
    'Action',
    'Asset',
    'AssetStatus',
    'Lake',
    'Zone',
    'State',
    'CancelJobRequest',
    'CreateAssetRequest',
    'CreateEnvironmentRequest',
    'CreateLakeRequest',
    'CreateTaskRequest',
    'CreateZoneRequest',
    'DeleteAssetRequest',
    'DeleteEnvironmentRequest',
    'DeleteLakeRequest',
    'DeleteTaskRequest',
    'DeleteZoneRequest',
    'GetAssetRequest',
    'GetEnvironmentRequest',
    'GetJobRequest',
    'GetLakeRequest',
    'GetTaskRequest',
    'GetZoneRequest',
    'ListActionsResponse',
    'ListAssetActionsRequest',
    'ListAssetsRequest',
    'ListAssetsResponse',
    'ListEnvironmentsRequest',
    'ListEnvironmentsResponse',
    'ListJobsRequest',
    'ListJobsResponse',
    'ListLakeActionsRequest',
    'ListLakesRequest',
    'ListLakesResponse',
    'ListSessionsRequest',
    'ListSessionsResponse',
    'ListTasksRequest',
    'ListTasksResponse',
    'ListZoneActionsRequest',
    'ListZonesRequest',
    'ListZonesResponse',
    'OperationMetadata',
    'RunTaskRequest',
    'RunTaskResponse',
    'UpdateAssetRequest',
    'UpdateEnvironmentRequest',
    'UpdateLakeRequest',
    'UpdateTaskRequest',
    'UpdateZoneRequest',
    'Job',
    'Task',
)
