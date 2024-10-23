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
from google.cloud.dataplex_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.catalog_service import CatalogServiceClient
from .services.catalog_service import CatalogServiceAsyncClient
from .services.content_service import ContentServiceClient
from .services.content_service import ContentServiceAsyncClient
from .services.dataplex_service import DataplexServiceClient
from .services.dataplex_service import DataplexServiceAsyncClient
from .services.data_scan_service import DataScanServiceClient
from .services.data_scan_service import DataScanServiceAsyncClient
from .services.data_taxonomy_service import DataTaxonomyServiceClient
from .services.data_taxonomy_service import DataTaxonomyServiceAsyncClient
from .services.metadata_service import MetadataServiceClient
from .services.metadata_service import MetadataServiceAsyncClient

from .types.analyze import Content
from .types.analyze import Environment
from .types.analyze import Session
from .types.catalog import Aspect
from .types.catalog import AspectSource
from .types.catalog import AspectType
from .types.catalog import CreateAspectTypeRequest
from .types.catalog import CreateEntryGroupRequest
from .types.catalog import CreateEntryRequest
from .types.catalog import CreateEntryTypeRequest
from .types.catalog import DeleteAspectTypeRequest
from .types.catalog import DeleteEntryGroupRequest
from .types.catalog import DeleteEntryRequest
from .types.catalog import DeleteEntryTypeRequest
from .types.catalog import Entry
from .types.catalog import EntryGroup
from .types.catalog import EntrySource
from .types.catalog import EntryType
from .types.catalog import GetAspectTypeRequest
from .types.catalog import GetEntryGroupRequest
from .types.catalog import GetEntryRequest
from .types.catalog import GetEntryTypeRequest
from .types.catalog import ListAspectTypesRequest
from .types.catalog import ListAspectTypesResponse
from .types.catalog import ListEntriesRequest
from .types.catalog import ListEntriesResponse
from .types.catalog import ListEntryGroupsRequest
from .types.catalog import ListEntryGroupsResponse
from .types.catalog import ListEntryTypesRequest
from .types.catalog import ListEntryTypesResponse
from .types.catalog import LookupEntryRequest
from .types.catalog import SearchEntriesRequest
from .types.catalog import SearchEntriesResponse
from .types.catalog import SearchEntriesResult
from .types.catalog import UpdateAspectTypeRequest
from .types.catalog import UpdateEntryGroupRequest
from .types.catalog import UpdateEntryRequest
from .types.catalog import UpdateEntryTypeRequest
from .types.catalog import EntryView
from .types.catalog import TransferStatus
from .types.content import CreateContentRequest
from .types.content import DeleteContentRequest
from .types.content import GetContentRequest
from .types.content import ListContentRequest
from .types.content import ListContentResponse
from .types.content import UpdateContentRequest
from .types.data_profile import DataProfileResult
from .types.data_profile import DataProfileSpec
from .types.data_quality import DataQualityColumnResult
from .types.data_quality import DataQualityDimension
from .types.data_quality import DataQualityDimensionResult
from .types.data_quality import DataQualityResult
from .types.data_quality import DataQualityRule
from .types.data_quality import DataQualityRuleResult
from .types.data_quality import DataQualitySpec
from .types.data_taxonomy import CreateDataAttributeBindingRequest
from .types.data_taxonomy import CreateDataAttributeRequest
from .types.data_taxonomy import CreateDataTaxonomyRequest
from .types.data_taxonomy import DataAttribute
from .types.data_taxonomy import DataAttributeBinding
from .types.data_taxonomy import DataTaxonomy
from .types.data_taxonomy import DeleteDataAttributeBindingRequest
from .types.data_taxonomy import DeleteDataAttributeRequest
from .types.data_taxonomy import DeleteDataTaxonomyRequest
from .types.data_taxonomy import GetDataAttributeBindingRequest
from .types.data_taxonomy import GetDataAttributeRequest
from .types.data_taxonomy import GetDataTaxonomyRequest
from .types.data_taxonomy import ListDataAttributeBindingsRequest
from .types.data_taxonomy import ListDataAttributeBindingsResponse
from .types.data_taxonomy import ListDataAttributesRequest
from .types.data_taxonomy import ListDataAttributesResponse
from .types.data_taxonomy import ListDataTaxonomiesRequest
from .types.data_taxonomy import ListDataTaxonomiesResponse
from .types.data_taxonomy import UpdateDataAttributeBindingRequest
from .types.data_taxonomy import UpdateDataAttributeRequest
from .types.data_taxonomy import UpdateDataTaxonomyRequest
from .types.datascans import CreateDataScanRequest
from .types.datascans import DataScan
from .types.datascans import DataScanJob
from .types.datascans import DeleteDataScanRequest
from .types.datascans import GenerateDataQualityRulesRequest
from .types.datascans import GenerateDataQualityRulesResponse
from .types.datascans import GetDataScanJobRequest
from .types.datascans import GetDataScanRequest
from .types.datascans import ListDataScanJobsRequest
from .types.datascans import ListDataScanJobsResponse
from .types.datascans import ListDataScansRequest
from .types.datascans import ListDataScansResponse
from .types.datascans import RunDataScanRequest
from .types.datascans import RunDataScanResponse
from .types.datascans import UpdateDataScanRequest
from .types.datascans import DataScanType
from .types.logs import DataQualityScanRuleResult
from .types.logs import DataScanEvent
from .types.logs import DiscoveryEvent
from .types.logs import GovernanceEvent
from .types.logs import JobEvent
from .types.logs import SessionEvent
from .types.metadata_ import CreateEntityRequest
from .types.metadata_ import CreatePartitionRequest
from .types.metadata_ import DeleteEntityRequest
from .types.metadata_ import DeletePartitionRequest
from .types.metadata_ import Entity
from .types.metadata_ import GetEntityRequest
from .types.metadata_ import GetPartitionRequest
from .types.metadata_ import ListEntitiesRequest
from .types.metadata_ import ListEntitiesResponse
from .types.metadata_ import ListPartitionsRequest
from .types.metadata_ import ListPartitionsResponse
from .types.metadata_ import Partition
from .types.metadata_ import Schema
from .types.metadata_ import StorageAccess
from .types.metadata_ import StorageFormat
from .types.metadata_ import UpdateEntityRequest
from .types.metadata_ import StorageSystem
from .types.processing import DataSource
from .types.processing import ScannedData
from .types.processing import Trigger
from .types.resources import Action
from .types.resources import Asset
from .types.resources import AssetStatus
from .types.resources import Lake
from .types.resources import Zone
from .types.resources import State
from .types.security import DataAccessSpec
from .types.security import ResourceAccessSpec
from .types.service import CancelJobRequest
from .types.service import CreateAssetRequest
from .types.service import CreateEnvironmentRequest
from .types.service import CreateLakeRequest
from .types.service import CreateTaskRequest
from .types.service import CreateZoneRequest
from .types.service import DeleteAssetRequest
from .types.service import DeleteEnvironmentRequest
from .types.service import DeleteLakeRequest
from .types.service import DeleteTaskRequest
from .types.service import DeleteZoneRequest
from .types.service import GetAssetRequest
from .types.service import GetEnvironmentRequest
from .types.service import GetJobRequest
from .types.service import GetLakeRequest
from .types.service import GetTaskRequest
from .types.service import GetZoneRequest
from .types.service import ListActionsResponse
from .types.service import ListAssetActionsRequest
from .types.service import ListAssetsRequest
from .types.service import ListAssetsResponse
from .types.service import ListEnvironmentsRequest
from .types.service import ListEnvironmentsResponse
from .types.service import ListJobsRequest
from .types.service import ListJobsResponse
from .types.service import ListLakeActionsRequest
from .types.service import ListLakesRequest
from .types.service import ListLakesResponse
from .types.service import ListSessionsRequest
from .types.service import ListSessionsResponse
from .types.service import ListTasksRequest
from .types.service import ListTasksResponse
from .types.service import ListZoneActionsRequest
from .types.service import ListZonesRequest
from .types.service import ListZonesResponse
from .types.service import OperationMetadata
from .types.service import RunTaskRequest
from .types.service import RunTaskResponse
from .types.service import UpdateAssetRequest
from .types.service import UpdateEnvironmentRequest
from .types.service import UpdateLakeRequest
from .types.service import UpdateTaskRequest
from .types.service import UpdateZoneRequest
from .types.tasks import Job
from .types.tasks import Task

__all__ = (
    'CatalogServiceAsyncClient',
    'ContentServiceAsyncClient',
    'DataScanServiceAsyncClient',
    'DataTaxonomyServiceAsyncClient',
    'DataplexServiceAsyncClient',
    'MetadataServiceAsyncClient',
'Action',
'Aspect',
'AspectSource',
'AspectType',
'Asset',
'AssetStatus',
'CancelJobRequest',
'CatalogServiceClient',
'Content',
'ContentServiceClient',
'CreateAspectTypeRequest',
'CreateAssetRequest',
'CreateContentRequest',
'CreateDataAttributeBindingRequest',
'CreateDataAttributeRequest',
'CreateDataScanRequest',
'CreateDataTaxonomyRequest',
'CreateEntityRequest',
'CreateEntryGroupRequest',
'CreateEntryRequest',
'CreateEntryTypeRequest',
'CreateEnvironmentRequest',
'CreateLakeRequest',
'CreatePartitionRequest',
'CreateTaskRequest',
'CreateZoneRequest',
'DataAccessSpec',
'DataAttribute',
'DataAttributeBinding',
'DataProfileResult',
'DataProfileSpec',
'DataQualityColumnResult',
'DataQualityDimension',
'DataQualityDimensionResult',
'DataQualityResult',
'DataQualityRule',
'DataQualityRuleResult',
'DataQualityScanRuleResult',
'DataQualitySpec',
'DataScan',
'DataScanEvent',
'DataScanJob',
'DataScanServiceClient',
'DataScanType',
'DataSource',
'DataTaxonomy',
'DataTaxonomyServiceClient',
'DataplexServiceClient',
'DeleteAspectTypeRequest',
'DeleteAssetRequest',
'DeleteContentRequest',
'DeleteDataAttributeBindingRequest',
'DeleteDataAttributeRequest',
'DeleteDataScanRequest',
'DeleteDataTaxonomyRequest',
'DeleteEntityRequest',
'DeleteEntryGroupRequest',
'DeleteEntryRequest',
'DeleteEntryTypeRequest',
'DeleteEnvironmentRequest',
'DeleteLakeRequest',
'DeletePartitionRequest',
'DeleteTaskRequest',
'DeleteZoneRequest',
'DiscoveryEvent',
'Entity',
'Entry',
'EntryGroup',
'EntrySource',
'EntryType',
'EntryView',
'Environment',
'GenerateDataQualityRulesRequest',
'GenerateDataQualityRulesResponse',
'GetAspectTypeRequest',
'GetAssetRequest',
'GetContentRequest',
'GetDataAttributeBindingRequest',
'GetDataAttributeRequest',
'GetDataScanJobRequest',
'GetDataScanRequest',
'GetDataTaxonomyRequest',
'GetEntityRequest',
'GetEntryGroupRequest',
'GetEntryRequest',
'GetEntryTypeRequest',
'GetEnvironmentRequest',
'GetJobRequest',
'GetLakeRequest',
'GetPartitionRequest',
'GetTaskRequest',
'GetZoneRequest',
'GovernanceEvent',
'Job',
'JobEvent',
'Lake',
'ListActionsResponse',
'ListAspectTypesRequest',
'ListAspectTypesResponse',
'ListAssetActionsRequest',
'ListAssetsRequest',
'ListAssetsResponse',
'ListContentRequest',
'ListContentResponse',
'ListDataAttributeBindingsRequest',
'ListDataAttributeBindingsResponse',
'ListDataAttributesRequest',
'ListDataAttributesResponse',
'ListDataScanJobsRequest',
'ListDataScanJobsResponse',
'ListDataScansRequest',
'ListDataScansResponse',
'ListDataTaxonomiesRequest',
'ListDataTaxonomiesResponse',
'ListEntitiesRequest',
'ListEntitiesResponse',
'ListEntriesRequest',
'ListEntriesResponse',
'ListEntryGroupsRequest',
'ListEntryGroupsResponse',
'ListEntryTypesRequest',
'ListEntryTypesResponse',
'ListEnvironmentsRequest',
'ListEnvironmentsResponse',
'ListJobsRequest',
'ListJobsResponse',
'ListLakeActionsRequest',
'ListLakesRequest',
'ListLakesResponse',
'ListPartitionsRequest',
'ListPartitionsResponse',
'ListSessionsRequest',
'ListSessionsResponse',
'ListTasksRequest',
'ListTasksResponse',
'ListZoneActionsRequest',
'ListZonesRequest',
'ListZonesResponse',
'LookupEntryRequest',
'MetadataServiceClient',
'OperationMetadata',
'Partition',
'ResourceAccessSpec',
'RunDataScanRequest',
'RunDataScanResponse',
'RunTaskRequest',
'RunTaskResponse',
'ScannedData',
'Schema',
'SearchEntriesRequest',
'SearchEntriesResponse',
'SearchEntriesResult',
'Session',
'SessionEvent',
'State',
'StorageAccess',
'StorageFormat',
'StorageSystem',
'Task',
'TransferStatus',
'Trigger',
'UpdateAspectTypeRequest',
'UpdateAssetRequest',
'UpdateContentRequest',
'UpdateDataAttributeBindingRequest',
'UpdateDataAttributeRequest',
'UpdateDataScanRequest',
'UpdateDataTaxonomyRequest',
'UpdateEntityRequest',
'UpdateEntryGroupRequest',
'UpdateEntryRequest',
'UpdateEntryTypeRequest',
'UpdateEnvironmentRequest',
'UpdateLakeRequest',
'UpdateTaskRequest',
'UpdateZoneRequest',
'Zone',
)
