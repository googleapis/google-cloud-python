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
from google.cloud.datacatalog_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.data_catalog import DataCatalogClient
from .services.data_catalog import DataCatalogAsyncClient
from .services.policy_tag_manager import PolicyTagManagerClient
from .services.policy_tag_manager import PolicyTagManagerAsyncClient
from .services.policy_tag_manager_serialization import PolicyTagManagerSerializationClient
from .services.policy_tag_manager_serialization import PolicyTagManagerSerializationAsyncClient

from .types.bigquery import BigQueryConnectionSpec
from .types.bigquery import BigQueryRoutineSpec
from .types.bigquery import CloudSqlBigQueryConnectionSpec
from .types.common import PersonalDetails
from .types.common import IntegratedSystem
from .types.common import ManagingSystem
from .types.data_source import DataSource
from .types.data_source import StorageProperties
from .types.datacatalog import BusinessContext
from .types.datacatalog import CloudBigtableInstanceSpec
from .types.datacatalog import CloudBigtableSystemSpec
from .types.datacatalog import Contacts
from .types.datacatalog import CreateEntryGroupRequest
from .types.datacatalog import CreateEntryRequest
from .types.datacatalog import CreateTagRequest
from .types.datacatalog import CreateTagTemplateFieldRequest
from .types.datacatalog import CreateTagTemplateRequest
from .types.datacatalog import DatabaseTableSpec
from .types.datacatalog import DatasetSpec
from .types.datacatalog import DataSourceConnectionSpec
from .types.datacatalog import DeleteEntryGroupRequest
from .types.datacatalog import DeleteEntryRequest
from .types.datacatalog import DeleteTagRequest
from .types.datacatalog import DeleteTagTemplateFieldRequest
from .types.datacatalog import DeleteTagTemplateRequest
from .types.datacatalog import Entry
from .types.datacatalog import EntryGroup
from .types.datacatalog import EntryOverview
from .types.datacatalog import FeatureOnlineStoreSpec
from .types.datacatalog import FilesetSpec
from .types.datacatalog import GetEntryGroupRequest
from .types.datacatalog import GetEntryRequest
from .types.datacatalog import GetTagTemplateRequest
from .types.datacatalog import ImportEntriesMetadata
from .types.datacatalog import ImportEntriesRequest
from .types.datacatalog import ImportEntriesResponse
from .types.datacatalog import ListEntriesRequest
from .types.datacatalog import ListEntriesResponse
from .types.datacatalog import ListEntryGroupsRequest
from .types.datacatalog import ListEntryGroupsResponse
from .types.datacatalog import ListTagsRequest
from .types.datacatalog import ListTagsResponse
from .types.datacatalog import LookerSystemSpec
from .types.datacatalog import LookupEntryRequest
from .types.datacatalog import MigrationConfig
from .types.datacatalog import ModelSpec
from .types.datacatalog import ModifyEntryContactsRequest
from .types.datacatalog import ModifyEntryOverviewRequest
from .types.datacatalog import OrganizationConfig
from .types.datacatalog import ReconcileTagsMetadata
from .types.datacatalog import ReconcileTagsRequest
from .types.datacatalog import ReconcileTagsResponse
from .types.datacatalog import RenameTagTemplateFieldEnumValueRequest
from .types.datacatalog import RenameTagTemplateFieldRequest
from .types.datacatalog import RetrieveConfigRequest
from .types.datacatalog import RetrieveEffectiveConfigRequest
from .types.datacatalog import RoutineSpec
from .types.datacatalog import SearchCatalogRequest
from .types.datacatalog import SearchCatalogResponse
from .types.datacatalog import ServiceSpec
from .types.datacatalog import SetConfigRequest
from .types.datacatalog import SqlDatabaseSystemSpec
from .types.datacatalog import StarEntryRequest
from .types.datacatalog import StarEntryResponse
from .types.datacatalog import UnstarEntryRequest
from .types.datacatalog import UnstarEntryResponse
from .types.datacatalog import UpdateEntryGroupRequest
from .types.datacatalog import UpdateEntryRequest
from .types.datacatalog import UpdateTagRequest
from .types.datacatalog import UpdateTagTemplateFieldRequest
from .types.datacatalog import UpdateTagTemplateRequest
from .types.datacatalog import VertexDatasetSpec
from .types.datacatalog import VertexModelSourceInfo
from .types.datacatalog import VertexModelSpec
from .types.datacatalog import CatalogUIExperience
from .types.datacatalog import EntryType
from .types.datacatalog import TagTemplateMigration
from .types.dataplex_spec import DataplexExternalTable
from .types.dataplex_spec import DataplexFilesetSpec
from .types.dataplex_spec import DataplexSpec
from .types.dataplex_spec import DataplexTableSpec
from .types.dump_content import DumpItem
from .types.dump_content import TaggedEntry
from .types.gcs_fileset_spec import GcsFilesetSpec
from .types.gcs_fileset_spec import GcsFileSpec
from .types.physical_schema import PhysicalSchema
from .types.policytagmanager import CreatePolicyTagRequest
from .types.policytagmanager import CreateTaxonomyRequest
from .types.policytagmanager import DeletePolicyTagRequest
from .types.policytagmanager import DeleteTaxonomyRequest
from .types.policytagmanager import GetPolicyTagRequest
from .types.policytagmanager import GetTaxonomyRequest
from .types.policytagmanager import ListPolicyTagsRequest
from .types.policytagmanager import ListPolicyTagsResponse
from .types.policytagmanager import ListTaxonomiesRequest
from .types.policytagmanager import ListTaxonomiesResponse
from .types.policytagmanager import PolicyTag
from .types.policytagmanager import Taxonomy
from .types.policytagmanager import UpdatePolicyTagRequest
from .types.policytagmanager import UpdateTaxonomyRequest
from .types.policytagmanagerserialization import CrossRegionalSource
from .types.policytagmanagerserialization import ExportTaxonomiesRequest
from .types.policytagmanagerserialization import ExportTaxonomiesResponse
from .types.policytagmanagerserialization import ImportTaxonomiesRequest
from .types.policytagmanagerserialization import ImportTaxonomiesResponse
from .types.policytagmanagerserialization import InlineSource
from .types.policytagmanagerserialization import ReplaceTaxonomyRequest
from .types.policytagmanagerserialization import SerializedPolicyTag
from .types.policytagmanagerserialization import SerializedTaxonomy
from .types.schema import ColumnSchema
from .types.schema import Schema
from .types.search import SearchCatalogResult
from .types.search import SearchResultType
from .types.table_spec import BigQueryDateShardedSpec
from .types.table_spec import BigQueryTableSpec
from .types.table_spec import TableSpec
from .types.table_spec import ViewSpec
from .types.table_spec import TableSourceType
from .types.tags import FieldType
from .types.tags import Tag
from .types.tags import TagField
from .types.tags import TagTemplate
from .types.tags import TagTemplateField
from .types.timestamps import SystemTimestamps
from .types.usage import CommonUsageStats
from .types.usage import UsageSignal
from .types.usage import UsageStats

__all__ = (
    'DataCatalogAsyncClient',
    'PolicyTagManagerAsyncClient',
    'PolicyTagManagerSerializationAsyncClient',
'BigQueryConnectionSpec',
'BigQueryDateShardedSpec',
'BigQueryRoutineSpec',
'BigQueryTableSpec',
'BusinessContext',
'CatalogUIExperience',
'CloudBigtableInstanceSpec',
'CloudBigtableSystemSpec',
'CloudSqlBigQueryConnectionSpec',
'ColumnSchema',
'CommonUsageStats',
'Contacts',
'CreateEntryGroupRequest',
'CreateEntryRequest',
'CreatePolicyTagRequest',
'CreateTagRequest',
'CreateTagTemplateFieldRequest',
'CreateTagTemplateRequest',
'CreateTaxonomyRequest',
'CrossRegionalSource',
'DataCatalogClient',
'DataSource',
'DataSourceConnectionSpec',
'DatabaseTableSpec',
'DataplexExternalTable',
'DataplexFilesetSpec',
'DataplexSpec',
'DataplexTableSpec',
'DatasetSpec',
'DeleteEntryGroupRequest',
'DeleteEntryRequest',
'DeletePolicyTagRequest',
'DeleteTagRequest',
'DeleteTagTemplateFieldRequest',
'DeleteTagTemplateRequest',
'DeleteTaxonomyRequest',
'DumpItem',
'Entry',
'EntryGroup',
'EntryOverview',
'EntryType',
'ExportTaxonomiesRequest',
'ExportTaxonomiesResponse',
'FeatureOnlineStoreSpec',
'FieldType',
'FilesetSpec',
'GcsFileSpec',
'GcsFilesetSpec',
'GetEntryGroupRequest',
'GetEntryRequest',
'GetPolicyTagRequest',
'GetTagTemplateRequest',
'GetTaxonomyRequest',
'ImportEntriesMetadata',
'ImportEntriesRequest',
'ImportEntriesResponse',
'ImportTaxonomiesRequest',
'ImportTaxonomiesResponse',
'InlineSource',
'IntegratedSystem',
'ListEntriesRequest',
'ListEntriesResponse',
'ListEntryGroupsRequest',
'ListEntryGroupsResponse',
'ListPolicyTagsRequest',
'ListPolicyTagsResponse',
'ListTagsRequest',
'ListTagsResponse',
'ListTaxonomiesRequest',
'ListTaxonomiesResponse',
'LookerSystemSpec',
'LookupEntryRequest',
'ManagingSystem',
'MigrationConfig',
'ModelSpec',
'ModifyEntryContactsRequest',
'ModifyEntryOverviewRequest',
'OrganizationConfig',
'PersonalDetails',
'PhysicalSchema',
'PolicyTag',
'PolicyTagManagerClient',
'PolicyTagManagerSerializationClient',
'ReconcileTagsMetadata',
'ReconcileTagsRequest',
'ReconcileTagsResponse',
'RenameTagTemplateFieldEnumValueRequest',
'RenameTagTemplateFieldRequest',
'ReplaceTaxonomyRequest',
'RetrieveConfigRequest',
'RetrieveEffectiveConfigRequest',
'RoutineSpec',
'Schema',
'SearchCatalogRequest',
'SearchCatalogResponse',
'SearchCatalogResult',
'SearchResultType',
'SerializedPolicyTag',
'SerializedTaxonomy',
'ServiceSpec',
'SetConfigRequest',
'SqlDatabaseSystemSpec',
'StarEntryRequest',
'StarEntryResponse',
'StorageProperties',
'SystemTimestamps',
'TableSourceType',
'TableSpec',
'Tag',
'TagField',
'TagTemplate',
'TagTemplateField',
'TagTemplateMigration',
'TaggedEntry',
'Taxonomy',
'UnstarEntryRequest',
'UnstarEntryResponse',
'UpdateEntryGroupRequest',
'UpdateEntryRequest',
'UpdatePolicyTagRequest',
'UpdateTagRequest',
'UpdateTagTemplateFieldRequest',
'UpdateTagTemplateRequest',
'UpdateTaxonomyRequest',
'UsageSignal',
'UsageStats',
'VertexDatasetSpec',
'VertexModelSourceInfo',
'VertexModelSpec',
'ViewSpec',
)
