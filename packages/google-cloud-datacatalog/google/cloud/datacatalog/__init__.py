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


from google.cloud.datacatalog_v1.services.data_catalog.async_client import (
    DataCatalogAsyncClient,
)
from google.cloud.datacatalog_v1.services.data_catalog.client import DataCatalogClient
from google.cloud.datacatalog_v1.services.policy_tag_manager.async_client import (
    PolicyTagManagerAsyncClient,
)
from google.cloud.datacatalog_v1.services.policy_tag_manager.client import (
    PolicyTagManagerClient,
)
from google.cloud.datacatalog_v1.services.policy_tag_manager_serialization.async_client import (
    PolicyTagManagerSerializationAsyncClient,
)
from google.cloud.datacatalog_v1.services.policy_tag_manager_serialization.client import (
    PolicyTagManagerSerializationClient,
)
from google.cloud.datacatalog_v1.types.bigquery import (
    BigQueryConnectionSpec,
    BigQueryRoutineSpec,
    CloudSqlBigQueryConnectionSpec,
)
from google.cloud.datacatalog_v1.types.common import (
    IntegratedSystem,
    ManagingSystem,
    PersonalDetails,
)
from google.cloud.datacatalog_v1.types.data_source import DataSource, StorageProperties
from google.cloud.datacatalog_v1.types.datacatalog import (
    BusinessContext,
    CloudBigtableInstanceSpec,
    CloudBigtableSystemSpec,
    Contacts,
    CreateEntryGroupRequest,
    CreateEntryRequest,
    CreateTagRequest,
    CreateTagTemplateFieldRequest,
    CreateTagTemplateRequest,
    DatabaseTableSpec,
    DatasetSpec,
    DataSourceConnectionSpec,
    DeleteEntryGroupRequest,
    DeleteEntryRequest,
    DeleteTagRequest,
    DeleteTagTemplateFieldRequest,
    DeleteTagTemplateRequest,
    Entry,
    EntryGroup,
    EntryOverview,
    EntryType,
    FeatureOnlineStoreSpec,
    FilesetSpec,
    GetEntryGroupRequest,
    GetEntryRequest,
    GetTagTemplateRequest,
    ImportEntriesMetadata,
    ImportEntriesRequest,
    ImportEntriesResponse,
    ListEntriesRequest,
    ListEntriesResponse,
    ListEntryGroupsRequest,
    ListEntryGroupsResponse,
    ListTagsRequest,
    ListTagsResponse,
    LookerSystemSpec,
    LookupEntryRequest,
    ModelSpec,
    ModifyEntryContactsRequest,
    ModifyEntryOverviewRequest,
    ReconcileTagsMetadata,
    ReconcileTagsRequest,
    ReconcileTagsResponse,
    RenameTagTemplateFieldEnumValueRequest,
    RenameTagTemplateFieldRequest,
    RoutineSpec,
    SearchCatalogRequest,
    SearchCatalogResponse,
    ServiceSpec,
    SqlDatabaseSystemSpec,
    StarEntryRequest,
    StarEntryResponse,
    UnstarEntryRequest,
    UnstarEntryResponse,
    UpdateEntryGroupRequest,
    UpdateEntryRequest,
    UpdateTagRequest,
    UpdateTagTemplateFieldRequest,
    UpdateTagTemplateRequest,
    VertexDatasetSpec,
    VertexModelSourceInfo,
    VertexModelSpec,
)
from google.cloud.datacatalog_v1.types.dataplex_spec import (
    DataplexExternalTable,
    DataplexFilesetSpec,
    DataplexSpec,
    DataplexTableSpec,
)
from google.cloud.datacatalog_v1.types.dump_content import DumpItem, TaggedEntry
from google.cloud.datacatalog_v1.types.gcs_fileset_spec import (
    GcsFilesetSpec,
    GcsFileSpec,
)
from google.cloud.datacatalog_v1.types.physical_schema import PhysicalSchema
from google.cloud.datacatalog_v1.types.policytagmanager import (
    CreatePolicyTagRequest,
    CreateTaxonomyRequest,
    DeletePolicyTagRequest,
    DeleteTaxonomyRequest,
    GetPolicyTagRequest,
    GetTaxonomyRequest,
    ListPolicyTagsRequest,
    ListPolicyTagsResponse,
    ListTaxonomiesRequest,
    ListTaxonomiesResponse,
    PolicyTag,
    Taxonomy,
    UpdatePolicyTagRequest,
    UpdateTaxonomyRequest,
)
from google.cloud.datacatalog_v1.types.policytagmanagerserialization import (
    CrossRegionalSource,
    ExportTaxonomiesRequest,
    ExportTaxonomiesResponse,
    ImportTaxonomiesRequest,
    ImportTaxonomiesResponse,
    InlineSource,
    ReplaceTaxonomyRequest,
    SerializedPolicyTag,
    SerializedTaxonomy,
)
from google.cloud.datacatalog_v1.types.schema import ColumnSchema, Schema
from google.cloud.datacatalog_v1.types.search import (
    SearchCatalogResult,
    SearchResultType,
)
from google.cloud.datacatalog_v1.types.table_spec import (
    BigQueryDateShardedSpec,
    BigQueryTableSpec,
    TableSourceType,
    TableSpec,
    ViewSpec,
)
from google.cloud.datacatalog_v1.types.tags import (
    FieldType,
    Tag,
    TagField,
    TagTemplate,
    TagTemplateField,
)
from google.cloud.datacatalog_v1.types.timestamps import SystemTimestamps
from google.cloud.datacatalog_v1.types.usage import (
    CommonUsageStats,
    UsageSignal,
    UsageStats,
)

__all__ = (
    "DataCatalogClient",
    "DataCatalogAsyncClient",
    "PolicyTagManagerClient",
    "PolicyTagManagerAsyncClient",
    "PolicyTagManagerSerializationClient",
    "PolicyTagManagerSerializationAsyncClient",
    "BigQueryConnectionSpec",
    "BigQueryRoutineSpec",
    "CloudSqlBigQueryConnectionSpec",
    "PersonalDetails",
    "IntegratedSystem",
    "ManagingSystem",
    "DataSource",
    "StorageProperties",
    "BusinessContext",
    "CloudBigtableInstanceSpec",
    "CloudBigtableSystemSpec",
    "Contacts",
    "CreateEntryGroupRequest",
    "CreateEntryRequest",
    "CreateTagRequest",
    "CreateTagTemplateFieldRequest",
    "CreateTagTemplateRequest",
    "DatabaseTableSpec",
    "DatasetSpec",
    "DataSourceConnectionSpec",
    "DeleteEntryGroupRequest",
    "DeleteEntryRequest",
    "DeleteTagRequest",
    "DeleteTagTemplateFieldRequest",
    "DeleteTagTemplateRequest",
    "Entry",
    "EntryGroup",
    "EntryOverview",
    "FeatureOnlineStoreSpec",
    "FilesetSpec",
    "GetEntryGroupRequest",
    "GetEntryRequest",
    "GetTagTemplateRequest",
    "ImportEntriesMetadata",
    "ImportEntriesRequest",
    "ImportEntriesResponse",
    "ListEntriesRequest",
    "ListEntriesResponse",
    "ListEntryGroupsRequest",
    "ListEntryGroupsResponse",
    "ListTagsRequest",
    "ListTagsResponse",
    "LookerSystemSpec",
    "LookupEntryRequest",
    "ModelSpec",
    "ModifyEntryContactsRequest",
    "ModifyEntryOverviewRequest",
    "ReconcileTagsMetadata",
    "ReconcileTagsRequest",
    "ReconcileTagsResponse",
    "RenameTagTemplateFieldEnumValueRequest",
    "RenameTagTemplateFieldRequest",
    "RoutineSpec",
    "SearchCatalogRequest",
    "SearchCatalogResponse",
    "ServiceSpec",
    "SqlDatabaseSystemSpec",
    "StarEntryRequest",
    "StarEntryResponse",
    "UnstarEntryRequest",
    "UnstarEntryResponse",
    "UpdateEntryGroupRequest",
    "UpdateEntryRequest",
    "UpdateTagRequest",
    "UpdateTagTemplateFieldRequest",
    "UpdateTagTemplateRequest",
    "VertexDatasetSpec",
    "VertexModelSourceInfo",
    "VertexModelSpec",
    "EntryType",
    "DataplexExternalTable",
    "DataplexFilesetSpec",
    "DataplexSpec",
    "DataplexTableSpec",
    "DumpItem",
    "TaggedEntry",
    "GcsFilesetSpec",
    "GcsFileSpec",
    "PhysicalSchema",
    "CreatePolicyTagRequest",
    "CreateTaxonomyRequest",
    "DeletePolicyTagRequest",
    "DeleteTaxonomyRequest",
    "GetPolicyTagRequest",
    "GetTaxonomyRequest",
    "ListPolicyTagsRequest",
    "ListPolicyTagsResponse",
    "ListTaxonomiesRequest",
    "ListTaxonomiesResponse",
    "PolicyTag",
    "Taxonomy",
    "UpdatePolicyTagRequest",
    "UpdateTaxonomyRequest",
    "CrossRegionalSource",
    "ExportTaxonomiesRequest",
    "ExportTaxonomiesResponse",
    "ImportTaxonomiesRequest",
    "ImportTaxonomiesResponse",
    "InlineSource",
    "ReplaceTaxonomyRequest",
    "SerializedPolicyTag",
    "SerializedTaxonomy",
    "ColumnSchema",
    "Schema",
    "SearchCatalogResult",
    "SearchResultType",
    "BigQueryDateShardedSpec",
    "BigQueryTableSpec",
    "TableSpec",
    "ViewSpec",
    "TableSourceType",
    "FieldType",
    "Tag",
    "TagField",
    "TagTemplate",
    "TagTemplateField",
    "SystemTimestamps",
    "CommonUsageStats",
    "UsageSignal",
    "UsageStats",
)
