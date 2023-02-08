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
from google.cloud.contentwarehouse import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.contentwarehouse_v1.services.document_link_service.client import DocumentLinkServiceClient
from google.cloud.contentwarehouse_v1.services.document_link_service.async_client import DocumentLinkServiceAsyncClient
from google.cloud.contentwarehouse_v1.services.document_schema_service.client import DocumentSchemaServiceClient
from google.cloud.contentwarehouse_v1.services.document_schema_service.async_client import DocumentSchemaServiceAsyncClient
from google.cloud.contentwarehouse_v1.services.document_service.client import DocumentServiceClient
from google.cloud.contentwarehouse_v1.services.document_service.async_client import DocumentServiceAsyncClient
from google.cloud.contentwarehouse_v1.services.rule_set_service.client import RuleSetServiceClient
from google.cloud.contentwarehouse_v1.services.rule_set_service.async_client import RuleSetServiceAsyncClient
from google.cloud.contentwarehouse_v1.services.synonym_set_service.client import SynonymSetServiceClient
from google.cloud.contentwarehouse_v1.services.synonym_set_service.async_client import SynonymSetServiceAsyncClient

from google.cloud.contentwarehouse_v1.types.async_document_service_request import CreateDocumentMetadata
from google.cloud.contentwarehouse_v1.types.async_document_service_request import UpdateDocumentMetadata
from google.cloud.contentwarehouse_v1.types.common import MergeFieldsOptions
from google.cloud.contentwarehouse_v1.types.common import RequestMetadata
from google.cloud.contentwarehouse_v1.types.common import ResponseMetadata
from google.cloud.contentwarehouse_v1.types.common import UpdateOptions
from google.cloud.contentwarehouse_v1.types.common import UserInfo
from google.cloud.contentwarehouse_v1.types.common import AccessControlMode
from google.cloud.contentwarehouse_v1.types.common import DatabaseType
from google.cloud.contentwarehouse_v1.types.common import UpdateType
from google.cloud.contentwarehouse_v1.types.document import DateTimeArray
from google.cloud.contentwarehouse_v1.types.document import Document
from google.cloud.contentwarehouse_v1.types.document import DocumentReference
from google.cloud.contentwarehouse_v1.types.document import EnumArray
from google.cloud.contentwarehouse_v1.types.document import EnumValue
from google.cloud.contentwarehouse_v1.types.document import FloatArray
from google.cloud.contentwarehouse_v1.types.document import IntegerArray
from google.cloud.contentwarehouse_v1.types.document import MapProperty
from google.cloud.contentwarehouse_v1.types.document import Property
from google.cloud.contentwarehouse_v1.types.document import PropertyArray
from google.cloud.contentwarehouse_v1.types.document import TextArray
from google.cloud.contentwarehouse_v1.types.document import TimestampArray
from google.cloud.contentwarehouse_v1.types.document import TimestampValue
from google.cloud.contentwarehouse_v1.types.document import Value
from google.cloud.contentwarehouse_v1.types.document import RawDocumentFileType
from google.cloud.contentwarehouse_v1.types.document_link_service import CreateDocumentLinkRequest
from google.cloud.contentwarehouse_v1.types.document_link_service import DeleteDocumentLinkRequest
from google.cloud.contentwarehouse_v1.types.document_link_service import DocumentLink
from google.cloud.contentwarehouse_v1.types.document_link_service import ListLinkedSourcesRequest
from google.cloud.contentwarehouse_v1.types.document_link_service import ListLinkedSourcesResponse
from google.cloud.contentwarehouse_v1.types.document_link_service import ListLinkedTargetsRequest
from google.cloud.contentwarehouse_v1.types.document_link_service import ListLinkedTargetsResponse
from google.cloud.contentwarehouse_v1.types.document_schema import DateTimeTypeOptions
from google.cloud.contentwarehouse_v1.types.document_schema import DocumentSchema
from google.cloud.contentwarehouse_v1.types.document_schema import EnumTypeOptions
from google.cloud.contentwarehouse_v1.types.document_schema import FloatTypeOptions
from google.cloud.contentwarehouse_v1.types.document_schema import IntegerTypeOptions
from google.cloud.contentwarehouse_v1.types.document_schema import MapTypeOptions
from google.cloud.contentwarehouse_v1.types.document_schema import PropertyDefinition
from google.cloud.contentwarehouse_v1.types.document_schema import PropertyTypeOptions
from google.cloud.contentwarehouse_v1.types.document_schema import TextTypeOptions
from google.cloud.contentwarehouse_v1.types.document_schema import TimestampTypeOptions
from google.cloud.contentwarehouse_v1.types.document_schema_service import CreateDocumentSchemaRequest
from google.cloud.contentwarehouse_v1.types.document_schema_service import DeleteDocumentSchemaRequest
from google.cloud.contentwarehouse_v1.types.document_schema_service import GetDocumentSchemaRequest
from google.cloud.contentwarehouse_v1.types.document_schema_service import ListDocumentSchemasRequest
from google.cloud.contentwarehouse_v1.types.document_schema_service import ListDocumentSchemasResponse
from google.cloud.contentwarehouse_v1.types.document_schema_service import UpdateDocumentSchemaRequest
from google.cloud.contentwarehouse_v1.types.document_service import CreateDocumentResponse
from google.cloud.contentwarehouse_v1.types.document_service import FetchAclResponse
from google.cloud.contentwarehouse_v1.types.document_service import QAResult
from google.cloud.contentwarehouse_v1.types.document_service import SearchDocumentsResponse
from google.cloud.contentwarehouse_v1.types.document_service import SetAclResponse
from google.cloud.contentwarehouse_v1.types.document_service import UpdateDocumentResponse
from google.cloud.contentwarehouse_v1.types.document_service_request import CloudAIDocumentOption
from google.cloud.contentwarehouse_v1.types.document_service_request import CreateDocumentRequest
from google.cloud.contentwarehouse_v1.types.document_service_request import DeleteDocumentRequest
from google.cloud.contentwarehouse_v1.types.document_service_request import FetchAclRequest
from google.cloud.contentwarehouse_v1.types.document_service_request import GetDocumentRequest
from google.cloud.contentwarehouse_v1.types.document_service_request import SearchDocumentsRequest
from google.cloud.contentwarehouse_v1.types.document_service_request import SetAclRequest
from google.cloud.contentwarehouse_v1.types.document_service_request import UpdateDocumentRequest
from google.cloud.contentwarehouse_v1.types.filters import DocumentQuery
from google.cloud.contentwarehouse_v1.types.filters import FileTypeFilter
from google.cloud.contentwarehouse_v1.types.filters import PropertyFilter
from google.cloud.contentwarehouse_v1.types.filters import TimeFilter
from google.cloud.contentwarehouse_v1.types.histogram import HistogramQuery
from google.cloud.contentwarehouse_v1.types.histogram import HistogramQueryPropertyNameFilter
from google.cloud.contentwarehouse_v1.types.histogram import HistogramQueryResult
from google.cloud.contentwarehouse_v1.types.rule_engine import AccessControlAction
from google.cloud.contentwarehouse_v1.types.rule_engine import Action
from google.cloud.contentwarehouse_v1.types.rule_engine import ActionExecutorOutput
from google.cloud.contentwarehouse_v1.types.rule_engine import ActionOutput
from google.cloud.contentwarehouse_v1.types.rule_engine import AddToFolderAction
from google.cloud.contentwarehouse_v1.types.rule_engine import DataUpdateAction
from google.cloud.contentwarehouse_v1.types.rule_engine import DataValidationAction
from google.cloud.contentwarehouse_v1.types.rule_engine import DeleteDocumentAction
from google.cloud.contentwarehouse_v1.types.rule_engine import InvalidRule
from google.cloud.contentwarehouse_v1.types.rule_engine import PublishAction
from google.cloud.contentwarehouse_v1.types.rule_engine import RemoveFromFolderAction
from google.cloud.contentwarehouse_v1.types.rule_engine import Rule
from google.cloud.contentwarehouse_v1.types.rule_engine import RuleActionsPair
from google.cloud.contentwarehouse_v1.types.rule_engine import RuleEngineOutput
from google.cloud.contentwarehouse_v1.types.rule_engine import RuleEvaluatorOutput
from google.cloud.contentwarehouse_v1.types.rule_engine import RuleSet
from google.cloud.contentwarehouse_v1.types.ruleset_service_request import CreateRuleSetRequest
from google.cloud.contentwarehouse_v1.types.ruleset_service_request import DeleteRuleSetRequest
from google.cloud.contentwarehouse_v1.types.ruleset_service_request import GetRuleSetRequest
from google.cloud.contentwarehouse_v1.types.ruleset_service_request import ListRuleSetsRequest
from google.cloud.contentwarehouse_v1.types.ruleset_service_request import ListRuleSetsResponse
from google.cloud.contentwarehouse_v1.types.ruleset_service_request import UpdateRuleSetRequest
from google.cloud.contentwarehouse_v1.types.synonymset import SynonymSet
from google.cloud.contentwarehouse_v1.types.synonymset_service_request import CreateSynonymSetRequest
from google.cloud.contentwarehouse_v1.types.synonymset_service_request import DeleteSynonymSetRequest
from google.cloud.contentwarehouse_v1.types.synonymset_service_request import GetSynonymSetRequest
from google.cloud.contentwarehouse_v1.types.synonymset_service_request import ListSynonymSetsRequest
from google.cloud.contentwarehouse_v1.types.synonymset_service_request import ListSynonymSetsResponse
from google.cloud.contentwarehouse_v1.types.synonymset_service_request import UpdateSynonymSetRequest

__all__ = ('DocumentLinkServiceClient',
    'DocumentLinkServiceAsyncClient',
    'DocumentSchemaServiceClient',
    'DocumentSchemaServiceAsyncClient',
    'DocumentServiceClient',
    'DocumentServiceAsyncClient',
    'RuleSetServiceClient',
    'RuleSetServiceAsyncClient',
    'SynonymSetServiceClient',
    'SynonymSetServiceAsyncClient',
    'CreateDocumentMetadata',
    'UpdateDocumentMetadata',
    'MergeFieldsOptions',
    'RequestMetadata',
    'ResponseMetadata',
    'UpdateOptions',
    'UserInfo',
    'AccessControlMode',
    'DatabaseType',
    'UpdateType',
    'DateTimeArray',
    'Document',
    'DocumentReference',
    'EnumArray',
    'EnumValue',
    'FloatArray',
    'IntegerArray',
    'MapProperty',
    'Property',
    'PropertyArray',
    'TextArray',
    'TimestampArray',
    'TimestampValue',
    'Value',
    'RawDocumentFileType',
    'CreateDocumentLinkRequest',
    'DeleteDocumentLinkRequest',
    'DocumentLink',
    'ListLinkedSourcesRequest',
    'ListLinkedSourcesResponse',
    'ListLinkedTargetsRequest',
    'ListLinkedTargetsResponse',
    'DateTimeTypeOptions',
    'DocumentSchema',
    'EnumTypeOptions',
    'FloatTypeOptions',
    'IntegerTypeOptions',
    'MapTypeOptions',
    'PropertyDefinition',
    'PropertyTypeOptions',
    'TextTypeOptions',
    'TimestampTypeOptions',
    'CreateDocumentSchemaRequest',
    'DeleteDocumentSchemaRequest',
    'GetDocumentSchemaRequest',
    'ListDocumentSchemasRequest',
    'ListDocumentSchemasResponse',
    'UpdateDocumentSchemaRequest',
    'CreateDocumentResponse',
    'FetchAclResponse',
    'QAResult',
    'SearchDocumentsResponse',
    'SetAclResponse',
    'UpdateDocumentResponse',
    'CloudAIDocumentOption',
    'CreateDocumentRequest',
    'DeleteDocumentRequest',
    'FetchAclRequest',
    'GetDocumentRequest',
    'SearchDocumentsRequest',
    'SetAclRequest',
    'UpdateDocumentRequest',
    'DocumentQuery',
    'FileTypeFilter',
    'PropertyFilter',
    'TimeFilter',
    'HistogramQuery',
    'HistogramQueryPropertyNameFilter',
    'HistogramQueryResult',
    'AccessControlAction',
    'Action',
    'ActionExecutorOutput',
    'ActionOutput',
    'AddToFolderAction',
    'DataUpdateAction',
    'DataValidationAction',
    'DeleteDocumentAction',
    'InvalidRule',
    'PublishAction',
    'RemoveFromFolderAction',
    'Rule',
    'RuleActionsPair',
    'RuleEngineOutput',
    'RuleEvaluatorOutput',
    'RuleSet',
    'CreateRuleSetRequest',
    'DeleteRuleSetRequest',
    'GetRuleSetRequest',
    'ListRuleSetsRequest',
    'ListRuleSetsResponse',
    'UpdateRuleSetRequest',
    'SynonymSet',
    'CreateSynonymSetRequest',
    'DeleteSynonymSetRequest',
    'GetSynonymSetRequest',
    'ListSynonymSetsRequest',
    'ListSynonymSetsResponse',
    'UpdateSynonymSetRequest',
)
