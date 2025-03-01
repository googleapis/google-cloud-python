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
from google.cloud.datacatalog import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.datacatalog_v1.services.data_catalog.client import DataCatalogClient
from google.cloud.datacatalog_v1.services.data_catalog.async_client import DataCatalogAsyncClient
from google.cloud.datacatalog_v1.services.policy_tag_manager.client import PolicyTagManagerClient
from google.cloud.datacatalog_v1.services.policy_tag_manager.async_client import PolicyTagManagerAsyncClient
from google.cloud.datacatalog_v1.services.policy_tag_manager_serialization.client import PolicyTagManagerSerializationClient
from google.cloud.datacatalog_v1.services.policy_tag_manager_serialization.async_client import PolicyTagManagerSerializationAsyncClient

from google.cloud.datacatalog_v1.types.bigquery import BigQueryConnectionSpec
from google.cloud.datacatalog_v1.types.bigquery import BigQueryRoutineSpec
from google.cloud.datacatalog_v1.types.bigquery import CloudSqlBigQueryConnectionSpec
from google.cloud.datacatalog_v1.types.common import PersonalDetails
from google.cloud.datacatalog_v1.types.common import IntegratedSystem
from google.cloud.datacatalog_v1.types.common import ManagingSystem
from google.cloud.datacatalog_v1.types.data_source import DataSource
from google.cloud.datacatalog_v1.types.data_source import StorageProperties
from google.cloud.datacatalog_v1.types.datacatalog import BusinessContext
from google.cloud.datacatalog_v1.types.datacatalog import CloudBigtableInstanceSpec
from google.cloud.datacatalog_v1.types.datacatalog import CloudBigtableSystemSpec
from google.cloud.datacatalog_v1.types.datacatalog import Contacts
from google.cloud.datacatalog_v1.types.datacatalog import CreateEntryGroupRequest
from google.cloud.datacatalog_v1.types.datacatalog import CreateEntryRequest
from google.cloud.datacatalog_v1.types.datacatalog import CreateTagRequest
from google.cloud.datacatalog_v1.types.datacatalog import CreateTagTemplateFieldRequest
from google.cloud.datacatalog_v1.types.datacatalog import CreateTagTemplateRequest
from google.cloud.datacatalog_v1.types.datacatalog import DatabaseTableSpec
from google.cloud.datacatalog_v1.types.datacatalog import DatasetSpec
from google.cloud.datacatalog_v1.types.datacatalog import DataSourceConnectionSpec
from google.cloud.datacatalog_v1.types.datacatalog import DeleteEntryGroupRequest
from google.cloud.datacatalog_v1.types.datacatalog import DeleteEntryRequest
from google.cloud.datacatalog_v1.types.datacatalog import DeleteTagRequest
from google.cloud.datacatalog_v1.types.datacatalog import DeleteTagTemplateFieldRequest
from google.cloud.datacatalog_v1.types.datacatalog import DeleteTagTemplateRequest
from google.cloud.datacatalog_v1.types.datacatalog import Entry
from google.cloud.datacatalog_v1.types.datacatalog import EntryGroup
from google.cloud.datacatalog_v1.types.datacatalog import EntryOverview
from google.cloud.datacatalog_v1.types.datacatalog import FeatureOnlineStoreSpec
from google.cloud.datacatalog_v1.types.datacatalog import FilesetSpec
from google.cloud.datacatalog_v1.types.datacatalog import GetEntryGroupRequest
from google.cloud.datacatalog_v1.types.datacatalog import GetEntryRequest
from google.cloud.datacatalog_v1.types.datacatalog import GetTagTemplateRequest
from google.cloud.datacatalog_v1.types.datacatalog import ImportEntriesMetadata
from google.cloud.datacatalog_v1.types.datacatalog import ImportEntriesRequest
from google.cloud.datacatalog_v1.types.datacatalog import ImportEntriesResponse
from google.cloud.datacatalog_v1.types.datacatalog import ListEntriesRequest
from google.cloud.datacatalog_v1.types.datacatalog import ListEntriesResponse
from google.cloud.datacatalog_v1.types.datacatalog import ListEntryGroupsRequest
from google.cloud.datacatalog_v1.types.datacatalog import ListEntryGroupsResponse
from google.cloud.datacatalog_v1.types.datacatalog import ListTagsRequest
from google.cloud.datacatalog_v1.types.datacatalog import ListTagsResponse
from google.cloud.datacatalog_v1.types.datacatalog import LookerSystemSpec
from google.cloud.datacatalog_v1.types.datacatalog import LookupEntryRequest
from google.cloud.datacatalog_v1.types.datacatalog import MigrationConfig
from google.cloud.datacatalog_v1.types.datacatalog import ModelSpec
from google.cloud.datacatalog_v1.types.datacatalog import ModifyEntryContactsRequest
from google.cloud.datacatalog_v1.types.datacatalog import ModifyEntryOverviewRequest
from google.cloud.datacatalog_v1.types.datacatalog import OrganizationConfig
from google.cloud.datacatalog_v1.types.datacatalog import ReconcileTagsMetadata
from google.cloud.datacatalog_v1.types.datacatalog import ReconcileTagsRequest
from google.cloud.datacatalog_v1.types.datacatalog import ReconcileTagsResponse
from google.cloud.datacatalog_v1.types.datacatalog import RenameTagTemplateFieldEnumValueRequest
from google.cloud.datacatalog_v1.types.datacatalog import RenameTagTemplateFieldRequest
from google.cloud.datacatalog_v1.types.datacatalog import RetrieveConfigRequest
from google.cloud.datacatalog_v1.types.datacatalog import RetrieveEffectiveConfigRequest
from google.cloud.datacatalog_v1.types.datacatalog import RoutineSpec
from google.cloud.datacatalog_v1.types.datacatalog import SearchCatalogRequest
from google.cloud.datacatalog_v1.types.datacatalog import SearchCatalogResponse
from google.cloud.datacatalog_v1.types.datacatalog import ServiceSpec
from google.cloud.datacatalog_v1.types.datacatalog import SetConfigRequest
from google.cloud.datacatalog_v1.types.datacatalog import SqlDatabaseSystemSpec
from google.cloud.datacatalog_v1.types.datacatalog import StarEntryRequest
from google.cloud.datacatalog_v1.types.datacatalog import StarEntryResponse
from google.cloud.datacatalog_v1.types.datacatalog import UnstarEntryRequest
from google.cloud.datacatalog_v1.types.datacatalog import UnstarEntryResponse
from google.cloud.datacatalog_v1.types.datacatalog import UpdateEntryGroupRequest
from google.cloud.datacatalog_v1.types.datacatalog import UpdateEntryRequest
from google.cloud.datacatalog_v1.types.datacatalog import UpdateTagRequest
from google.cloud.datacatalog_v1.types.datacatalog import UpdateTagTemplateFieldRequest
from google.cloud.datacatalog_v1.types.datacatalog import UpdateTagTemplateRequest
from google.cloud.datacatalog_v1.types.datacatalog import VertexDatasetSpec
from google.cloud.datacatalog_v1.types.datacatalog import VertexModelSourceInfo
from google.cloud.datacatalog_v1.types.datacatalog import VertexModelSpec
from google.cloud.datacatalog_v1.types.datacatalog import CatalogUIExperience
from google.cloud.datacatalog_v1.types.datacatalog import EntryType
from google.cloud.datacatalog_v1.types.datacatalog import TagTemplateMigration
from google.cloud.datacatalog_v1.types.dataplex_spec import DataplexExternalTable
from google.cloud.datacatalog_v1.types.dataplex_spec import DataplexFilesetSpec
from google.cloud.datacatalog_v1.types.dataplex_spec import DataplexSpec
from google.cloud.datacatalog_v1.types.dataplex_spec import DataplexTableSpec
from google.cloud.datacatalog_v1.types.dump_content import DumpItem
from google.cloud.datacatalog_v1.types.dump_content import TaggedEntry
from google.cloud.datacatalog_v1.types.gcs_fileset_spec import GcsFilesetSpec
from google.cloud.datacatalog_v1.types.gcs_fileset_spec import GcsFileSpec
from google.cloud.datacatalog_v1.types.physical_schema import PhysicalSchema
from google.cloud.datacatalog_v1.types.policytagmanager import CreatePolicyTagRequest
from google.cloud.datacatalog_v1.types.policytagmanager import CreateTaxonomyRequest
from google.cloud.datacatalog_v1.types.policytagmanager import DeletePolicyTagRequest
from google.cloud.datacatalog_v1.types.policytagmanager import DeleteTaxonomyRequest
from google.cloud.datacatalog_v1.types.policytagmanager import GetPolicyTagRequest
from google.cloud.datacatalog_v1.types.policytagmanager import GetTaxonomyRequest
from google.cloud.datacatalog_v1.types.policytagmanager import ListPolicyTagsRequest
from google.cloud.datacatalog_v1.types.policytagmanager import ListPolicyTagsResponse
from google.cloud.datacatalog_v1.types.policytagmanager import ListTaxonomiesRequest
from google.cloud.datacatalog_v1.types.policytagmanager import ListTaxonomiesResponse
from google.cloud.datacatalog_v1.types.policytagmanager import PolicyTag
from google.cloud.datacatalog_v1.types.policytagmanager import Taxonomy
from google.cloud.datacatalog_v1.types.policytagmanager import UpdatePolicyTagRequest
from google.cloud.datacatalog_v1.types.policytagmanager import UpdateTaxonomyRequest
from google.cloud.datacatalog_v1.types.policytagmanagerserialization import CrossRegionalSource
from google.cloud.datacatalog_v1.types.policytagmanagerserialization import ExportTaxonomiesRequest
from google.cloud.datacatalog_v1.types.policytagmanagerserialization import ExportTaxonomiesResponse
from google.cloud.datacatalog_v1.types.policytagmanagerserialization import ImportTaxonomiesRequest
from google.cloud.datacatalog_v1.types.policytagmanagerserialization import ImportTaxonomiesResponse
from google.cloud.datacatalog_v1.types.policytagmanagerserialization import InlineSource
from google.cloud.datacatalog_v1.types.policytagmanagerserialization import ReplaceTaxonomyRequest
from google.cloud.datacatalog_v1.types.policytagmanagerserialization import SerializedPolicyTag
from google.cloud.datacatalog_v1.types.policytagmanagerserialization import SerializedTaxonomy
from google.cloud.datacatalog_v1.types.schema import ColumnSchema
from google.cloud.datacatalog_v1.types.schema import Schema
from google.cloud.datacatalog_v1.types.search import SearchCatalogResult
from google.cloud.datacatalog_v1.types.search import SearchResultType
from google.cloud.datacatalog_v1.types.table_spec import BigQueryDateShardedSpec
from google.cloud.datacatalog_v1.types.table_spec import BigQueryTableSpec
from google.cloud.datacatalog_v1.types.table_spec import TableSpec
from google.cloud.datacatalog_v1.types.table_spec import ViewSpec
from google.cloud.datacatalog_v1.types.table_spec import TableSourceType
from google.cloud.datacatalog_v1.types.tags import FieldType
from google.cloud.datacatalog_v1.types.tags import Tag
from google.cloud.datacatalog_v1.types.tags import TagField
from google.cloud.datacatalog_v1.types.tags import TagTemplate
from google.cloud.datacatalog_v1.types.tags import TagTemplateField
from google.cloud.datacatalog_v1.types.timestamps import SystemTimestamps
from google.cloud.datacatalog_v1.types.usage import CommonUsageStats
from google.cloud.datacatalog_v1.types.usage import UsageSignal
from google.cloud.datacatalog_v1.types.usage import UsageStats

__all__ = ('DataCatalogClient',
    'DataCatalogAsyncClient',
    'PolicyTagManagerClient',
    'PolicyTagManagerAsyncClient',
    'PolicyTagManagerSerializationClient',
    'PolicyTagManagerSerializationAsyncClient',
    'BigQueryConnectionSpec',
    'BigQueryRoutineSpec',
    'CloudSqlBigQueryConnectionSpec',
    'PersonalDetails',
    'IntegratedSystem',
    'ManagingSystem',
    'DataSource',
    'StorageProperties',
    'BusinessContext',
    'CloudBigtableInstanceSpec',
    'CloudBigtableSystemSpec',
    'Contacts',
    'CreateEntryGroupRequest',
    'CreateEntryRequest',
    'CreateTagRequest',
    'CreateTagTemplateFieldRequest',
    'CreateTagTemplateRequest',
    'DatabaseTableSpec',
    'DatasetSpec',
    'DataSourceConnectionSpec',
    'DeleteEntryGroupRequest',
    'DeleteEntryRequest',
    'DeleteTagRequest',
    'DeleteTagTemplateFieldRequest',
    'DeleteTagTemplateRequest',
    'Entry',
    'EntryGroup',
    'EntryOverview',
    'FeatureOnlineStoreSpec',
    'FilesetSpec',
    'GetEntryGroupRequest',
    'GetEntryRequest',
    'GetTagTemplateRequest',
    'ImportEntriesMetadata',
    'ImportEntriesRequest',
    'ImportEntriesResponse',
    'ListEntriesRequest',
    'ListEntriesResponse',
    'ListEntryGroupsRequest',
    'ListEntryGroupsResponse',
    'ListTagsRequest',
    'ListTagsResponse',
    'LookerSystemSpec',
    'LookupEntryRequest',
    'MigrationConfig',
    'ModelSpec',
    'ModifyEntryContactsRequest',
    'ModifyEntryOverviewRequest',
    'OrganizationConfig',
    'ReconcileTagsMetadata',
    'ReconcileTagsRequest',
    'ReconcileTagsResponse',
    'RenameTagTemplateFieldEnumValueRequest',
    'RenameTagTemplateFieldRequest',
    'RetrieveConfigRequest',
    'RetrieveEffectiveConfigRequest',
    'RoutineSpec',
    'SearchCatalogRequest',
    'SearchCatalogResponse',
    'ServiceSpec',
    'SetConfigRequest',
    'SqlDatabaseSystemSpec',
    'StarEntryRequest',
    'StarEntryResponse',
    'UnstarEntryRequest',
    'UnstarEntryResponse',
    'UpdateEntryGroupRequest',
    'UpdateEntryRequest',
    'UpdateTagRequest',
    'UpdateTagTemplateFieldRequest',
    'UpdateTagTemplateRequest',
    'VertexDatasetSpec',
    'VertexModelSourceInfo',
    'VertexModelSpec',
    'CatalogUIExperience',
    'EntryType',
    'TagTemplateMigration',
    'DataplexExternalTable',
    'DataplexFilesetSpec',
    'DataplexSpec',
    'DataplexTableSpec',
    'DumpItem',
    'TaggedEntry',
    'GcsFilesetSpec',
    'GcsFileSpec',
    'PhysicalSchema',
    'CreatePolicyTagRequest',
    'CreateTaxonomyRequest',
    'DeletePolicyTagRequest',
    'DeleteTaxonomyRequest',
    'GetPolicyTagRequest',
    'GetTaxonomyRequest',
    'ListPolicyTagsRequest',
    'ListPolicyTagsResponse',
    'ListTaxonomiesRequest',
    'ListTaxonomiesResponse',
    'PolicyTag',
    'Taxonomy',
    'UpdatePolicyTagRequest',
    'UpdateTaxonomyRequest',
    'CrossRegionalSource',
    'ExportTaxonomiesRequest',
    'ExportTaxonomiesResponse',
    'ImportTaxonomiesRequest',
    'ImportTaxonomiesResponse',
    'InlineSource',
    'ReplaceTaxonomyRequest',
    'SerializedPolicyTag',
    'SerializedTaxonomy',
    'ColumnSchema',
    'Schema',
    'SearchCatalogResult',
    'SearchResultType',
    'BigQueryDateShardedSpec',
    'BigQueryTableSpec',
    'TableSpec',
    'ViewSpec',
    'TableSourceType',
    'FieldType',
    'Tag',
    'TagField',
    'TagTemplate',
    'TagTemplateField',
    'SystemTimestamps',
    'CommonUsageStats',
    'UsageSignal',
    'UsageStats',
)
