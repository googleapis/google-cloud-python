# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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

from .services.data_catalog import DataCatalogClient
from .services.policy_tag_manager import PolicyTagManagerClient
from .services.policy_tag_manager_serialization import (
    PolicyTagManagerSerializationClient,
)
from .types.common import IntegratedSystem
from .types.datacatalog import CreateEntryGroupRequest
from .types.datacatalog import CreateEntryRequest
from .types.datacatalog import CreateTagRequest
from .types.datacatalog import CreateTagTemplateFieldRequest
from .types.datacatalog import CreateTagTemplateRequest
from .types.datacatalog import DeleteEntryGroupRequest
from .types.datacatalog import DeleteEntryRequest
from .types.datacatalog import DeleteTagRequest
from .types.datacatalog import DeleteTagTemplateFieldRequest
from .types.datacatalog import DeleteTagTemplateRequest
from .types.datacatalog import Entry
from .types.datacatalog import EntryGroup
from .types.datacatalog import EntryType
from .types.datacatalog import GetEntryGroupRequest
from .types.datacatalog import GetEntryRequest
from .types.datacatalog import GetTagTemplateRequest
from .types.datacatalog import ListEntriesRequest
from .types.datacatalog import ListEntriesResponse
from .types.datacatalog import ListEntryGroupsRequest
from .types.datacatalog import ListEntryGroupsResponse
from .types.datacatalog import ListTagsRequest
from .types.datacatalog import ListTagsResponse
from .types.datacatalog import LookupEntryRequest
from .types.datacatalog import RenameTagTemplateFieldRequest
from .types.datacatalog import SearchCatalogRequest
from .types.datacatalog import SearchCatalogResponse
from .types.datacatalog import UpdateEntryGroupRequest
from .types.datacatalog import UpdateEntryRequest
from .types.datacatalog import UpdateTagRequest
from .types.datacatalog import UpdateTagTemplateFieldRequest
from .types.datacatalog import UpdateTagTemplateRequest
from .types.gcs_fileset_spec import GcsFileSpec
from .types.gcs_fileset_spec import GcsFilesetSpec
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
from .types.policytagmanagerserialization import ExportTaxonomiesRequest
from .types.policytagmanagerserialization import ExportTaxonomiesResponse
from .types.policytagmanagerserialization import ImportTaxonomiesRequest
from .types.policytagmanagerserialization import ImportTaxonomiesResponse
from .types.policytagmanagerserialization import InlineSource
from .types.policytagmanagerserialization import SerializedPolicyTag
from .types.policytagmanagerserialization import SerializedTaxonomy
from .types.schema import ColumnSchema
from .types.schema import Schema
from .types.search import SearchCatalogResult
from .types.search import SearchResultType
from .types.table_spec import BigQueryDateShardedSpec
from .types.table_spec import BigQueryTableSpec
from .types.table_spec import TableSourceType
from .types.table_spec import TableSpec
from .types.table_spec import ViewSpec
from .types.tags import FieldType
from .types.tags import Tag
from .types.tags import TagField
from .types.tags import TagTemplate
from .types.tags import TagTemplateField
from .types.timestamps import SystemTimestamps


__all__ = (
    "BigQueryDateShardedSpec",
    "BigQueryTableSpec",
    "ColumnSchema",
    "CreateEntryGroupRequest",
    "CreateEntryRequest",
    "CreatePolicyTagRequest",
    "CreateTagRequest",
    "CreateTagTemplateFieldRequest",
    "CreateTagTemplateRequest",
    "CreateTaxonomyRequest",
    "DataCatalogClient",
    "DeleteEntryGroupRequest",
    "DeleteEntryRequest",
    "DeletePolicyTagRequest",
    "DeleteTagRequest",
    "DeleteTagTemplateFieldRequest",
    "DeleteTagTemplateRequest",
    "DeleteTaxonomyRequest",
    "Entry",
    "EntryGroup",
    "EntryType",
    "ExportTaxonomiesRequest",
    "ExportTaxonomiesResponse",
    "FieldType",
    "GcsFileSpec",
    "GcsFilesetSpec",
    "GetEntryGroupRequest",
    "GetEntryRequest",
    "GetPolicyTagRequest",
    "GetTagTemplateRequest",
    "GetTaxonomyRequest",
    "ImportTaxonomiesRequest",
    "ImportTaxonomiesResponse",
    "InlineSource",
    "IntegratedSystem",
    "ListEntriesRequest",
    "ListEntriesResponse",
    "ListEntryGroupsRequest",
    "ListEntryGroupsResponse",
    "ListPolicyTagsRequest",
    "ListPolicyTagsResponse",
    "ListTagsRequest",
    "ListTagsResponse",
    "ListTaxonomiesRequest",
    "ListTaxonomiesResponse",
    "LookupEntryRequest",
    "PolicyTag",
    "PolicyTagManagerClient",
    "RenameTagTemplateFieldRequest",
    "Schema",
    "SearchCatalogRequest",
    "SearchCatalogResponse",
    "SearchCatalogResult",
    "SearchResultType",
    "SerializedPolicyTag",
    "SerializedTaxonomy",
    "SystemTimestamps",
    "TableSourceType",
    "TableSpec",
    "Tag",
    "TagField",
    "TagTemplate",
    "TagTemplateField",
    "Taxonomy",
    "UpdateEntryGroupRequest",
    "UpdateEntryRequest",
    "UpdatePolicyTagRequest",
    "UpdateTagRequest",
    "UpdateTagTemplateFieldRequest",
    "UpdateTagTemplateRequest",
    "UpdateTaxonomyRequest",
    "ViewSpec",
    "PolicyTagManagerSerializationClient",
)
