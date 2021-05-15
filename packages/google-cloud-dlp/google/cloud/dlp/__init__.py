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

from google.cloud.dlp_v2.services.dlp_service.client import DlpServiceClient
from google.cloud.dlp_v2.services.dlp_service.async_client import DlpServiceAsyncClient

from google.cloud.dlp_v2.types.dlp import Action
from google.cloud.dlp_v2.types.dlp import ActivateJobTriggerRequest
from google.cloud.dlp_v2.types.dlp import AnalyzeDataSourceRiskDetails
from google.cloud.dlp_v2.types.dlp import BoundingBox
from google.cloud.dlp_v2.types.dlp import BucketingConfig
from google.cloud.dlp_v2.types.dlp import ByteContentItem
from google.cloud.dlp_v2.types.dlp import CancelDlpJobRequest
from google.cloud.dlp_v2.types.dlp import CharacterMaskConfig
from google.cloud.dlp_v2.types.dlp import CharsToIgnore
from google.cloud.dlp_v2.types.dlp import Color
from google.cloud.dlp_v2.types.dlp import Container
from google.cloud.dlp_v2.types.dlp import ContentItem
from google.cloud.dlp_v2.types.dlp import ContentLocation
from google.cloud.dlp_v2.types.dlp import CreateDeidentifyTemplateRequest
from google.cloud.dlp_v2.types.dlp import CreateDlpJobRequest
from google.cloud.dlp_v2.types.dlp import CreateInspectTemplateRequest
from google.cloud.dlp_v2.types.dlp import CreateJobTriggerRequest
from google.cloud.dlp_v2.types.dlp import CreateStoredInfoTypeRequest
from google.cloud.dlp_v2.types.dlp import CryptoDeterministicConfig
from google.cloud.dlp_v2.types.dlp import CryptoHashConfig
from google.cloud.dlp_v2.types.dlp import CryptoKey
from google.cloud.dlp_v2.types.dlp import CryptoReplaceFfxFpeConfig
from google.cloud.dlp_v2.types.dlp import DateShiftConfig
from google.cloud.dlp_v2.types.dlp import DateTime
from google.cloud.dlp_v2.types.dlp import DeidentifyConfig
from google.cloud.dlp_v2.types.dlp import DeidentifyContentRequest
from google.cloud.dlp_v2.types.dlp import DeidentifyContentResponse
from google.cloud.dlp_v2.types.dlp import DeidentifyTemplate
from google.cloud.dlp_v2.types.dlp import DeleteDeidentifyTemplateRequest
from google.cloud.dlp_v2.types.dlp import DeleteDlpJobRequest
from google.cloud.dlp_v2.types.dlp import DeleteInspectTemplateRequest
from google.cloud.dlp_v2.types.dlp import DeleteJobTriggerRequest
from google.cloud.dlp_v2.types.dlp import DeleteStoredInfoTypeRequest
from google.cloud.dlp_v2.types.dlp import DlpJob
from google.cloud.dlp_v2.types.dlp import DocumentLocation
from google.cloud.dlp_v2.types.dlp import Error
from google.cloud.dlp_v2.types.dlp import ExcludeInfoTypes
from google.cloud.dlp_v2.types.dlp import ExclusionRule
from google.cloud.dlp_v2.types.dlp import FieldTransformation
from google.cloud.dlp_v2.types.dlp import Finding
from google.cloud.dlp_v2.types.dlp import FinishDlpJobRequest
from google.cloud.dlp_v2.types.dlp import FixedSizeBucketingConfig
from google.cloud.dlp_v2.types.dlp import GetDeidentifyTemplateRequest
from google.cloud.dlp_v2.types.dlp import GetDlpJobRequest
from google.cloud.dlp_v2.types.dlp import GetInspectTemplateRequest
from google.cloud.dlp_v2.types.dlp import GetJobTriggerRequest
from google.cloud.dlp_v2.types.dlp import GetStoredInfoTypeRequest
from google.cloud.dlp_v2.types.dlp import HybridContentItem
from google.cloud.dlp_v2.types.dlp import HybridFindingDetails
from google.cloud.dlp_v2.types.dlp import HybridInspectDlpJobRequest
from google.cloud.dlp_v2.types.dlp import HybridInspectJobTriggerRequest
from google.cloud.dlp_v2.types.dlp import HybridInspectResponse
from google.cloud.dlp_v2.types.dlp import HybridInspectStatistics
from google.cloud.dlp_v2.types.dlp import ImageLocation
from google.cloud.dlp_v2.types.dlp import InfoTypeDescription
from google.cloud.dlp_v2.types.dlp import InfoTypeStats
from google.cloud.dlp_v2.types.dlp import InfoTypeTransformations
from google.cloud.dlp_v2.types.dlp import InspectConfig
from google.cloud.dlp_v2.types.dlp import InspectContentRequest
from google.cloud.dlp_v2.types.dlp import InspectContentResponse
from google.cloud.dlp_v2.types.dlp import InspectDataSourceDetails
from google.cloud.dlp_v2.types.dlp import InspectionRule
from google.cloud.dlp_v2.types.dlp import InspectionRuleSet
from google.cloud.dlp_v2.types.dlp import InspectJobConfig
from google.cloud.dlp_v2.types.dlp import InspectResult
from google.cloud.dlp_v2.types.dlp import InspectTemplate
from google.cloud.dlp_v2.types.dlp import JobTrigger
from google.cloud.dlp_v2.types.dlp import KmsWrappedCryptoKey
from google.cloud.dlp_v2.types.dlp import LargeCustomDictionaryConfig
from google.cloud.dlp_v2.types.dlp import LargeCustomDictionaryStats
from google.cloud.dlp_v2.types.dlp import ListDeidentifyTemplatesRequest
from google.cloud.dlp_v2.types.dlp import ListDeidentifyTemplatesResponse
from google.cloud.dlp_v2.types.dlp import ListDlpJobsRequest
from google.cloud.dlp_v2.types.dlp import ListDlpJobsResponse
from google.cloud.dlp_v2.types.dlp import ListInfoTypesRequest
from google.cloud.dlp_v2.types.dlp import ListInfoTypesResponse
from google.cloud.dlp_v2.types.dlp import ListInspectTemplatesRequest
from google.cloud.dlp_v2.types.dlp import ListInspectTemplatesResponse
from google.cloud.dlp_v2.types.dlp import ListJobTriggersRequest
from google.cloud.dlp_v2.types.dlp import ListJobTriggersResponse
from google.cloud.dlp_v2.types.dlp import ListStoredInfoTypesRequest
from google.cloud.dlp_v2.types.dlp import ListStoredInfoTypesResponse
from google.cloud.dlp_v2.types.dlp import Location
from google.cloud.dlp_v2.types.dlp import Manual
from google.cloud.dlp_v2.types.dlp import MetadataLocation
from google.cloud.dlp_v2.types.dlp import OutputStorageConfig
from google.cloud.dlp_v2.types.dlp import PrimitiveTransformation
from google.cloud.dlp_v2.types.dlp import PrivacyMetric
from google.cloud.dlp_v2.types.dlp import QuasiId
from google.cloud.dlp_v2.types.dlp import QuoteInfo
from google.cloud.dlp_v2.types.dlp import Range
from google.cloud.dlp_v2.types.dlp import RecordCondition
from google.cloud.dlp_v2.types.dlp import RecordLocation
from google.cloud.dlp_v2.types.dlp import RecordSuppression
from google.cloud.dlp_v2.types.dlp import RecordTransformations
from google.cloud.dlp_v2.types.dlp import RedactConfig
from google.cloud.dlp_v2.types.dlp import RedactImageRequest
from google.cloud.dlp_v2.types.dlp import RedactImageResponse
from google.cloud.dlp_v2.types.dlp import ReidentifyContentRequest
from google.cloud.dlp_v2.types.dlp import ReidentifyContentResponse
from google.cloud.dlp_v2.types.dlp import ReplaceValueConfig
from google.cloud.dlp_v2.types.dlp import ReplaceWithInfoTypeConfig
from google.cloud.dlp_v2.types.dlp import RiskAnalysisJobConfig
from google.cloud.dlp_v2.types.dlp import Schedule
from google.cloud.dlp_v2.types.dlp import StatisticalTable
from google.cloud.dlp_v2.types.dlp import StorageMetadataLabel
from google.cloud.dlp_v2.types.dlp import StoredInfoType
from google.cloud.dlp_v2.types.dlp import StoredInfoTypeConfig
from google.cloud.dlp_v2.types.dlp import StoredInfoTypeStats
from google.cloud.dlp_v2.types.dlp import StoredInfoTypeVersion
from google.cloud.dlp_v2.types.dlp import Table
from google.cloud.dlp_v2.types.dlp import TableLocation
from google.cloud.dlp_v2.types.dlp import TimePartConfig
from google.cloud.dlp_v2.types.dlp import TransformationErrorHandling
from google.cloud.dlp_v2.types.dlp import TransformationOverview
from google.cloud.dlp_v2.types.dlp import TransformationSummary
from google.cloud.dlp_v2.types.dlp import TransientCryptoKey
from google.cloud.dlp_v2.types.dlp import UnwrappedCryptoKey
from google.cloud.dlp_v2.types.dlp import UpdateDeidentifyTemplateRequest
from google.cloud.dlp_v2.types.dlp import UpdateInspectTemplateRequest
from google.cloud.dlp_v2.types.dlp import UpdateJobTriggerRequest
from google.cloud.dlp_v2.types.dlp import UpdateStoredInfoTypeRequest
from google.cloud.dlp_v2.types.dlp import Value
from google.cloud.dlp_v2.types.dlp import ValueFrequency
from google.cloud.dlp_v2.types.dlp import ContentOption
from google.cloud.dlp_v2.types.dlp import DlpJobType
from google.cloud.dlp_v2.types.dlp import InfoTypeSupportedBy
from google.cloud.dlp_v2.types.dlp import MatchingType
from google.cloud.dlp_v2.types.dlp import MetadataType
from google.cloud.dlp_v2.types.dlp import RelationalOperator
from google.cloud.dlp_v2.types.dlp import StoredInfoTypeState
from google.cloud.dlp_v2.types.storage import BigQueryField
from google.cloud.dlp_v2.types.storage import BigQueryKey
from google.cloud.dlp_v2.types.storage import BigQueryOptions
from google.cloud.dlp_v2.types.storage import BigQueryTable
from google.cloud.dlp_v2.types.storage import CloudStorageFileSet
from google.cloud.dlp_v2.types.storage import CloudStorageOptions
from google.cloud.dlp_v2.types.storage import CloudStoragePath
from google.cloud.dlp_v2.types.storage import CloudStorageRegexFileSet
from google.cloud.dlp_v2.types.storage import CustomInfoType
from google.cloud.dlp_v2.types.storage import DatastoreKey
from google.cloud.dlp_v2.types.storage import DatastoreOptions
from google.cloud.dlp_v2.types.storage import EntityId
from google.cloud.dlp_v2.types.storage import FieldId
from google.cloud.dlp_v2.types.storage import HybridOptions
from google.cloud.dlp_v2.types.storage import InfoType
from google.cloud.dlp_v2.types.storage import Key
from google.cloud.dlp_v2.types.storage import KindExpression
from google.cloud.dlp_v2.types.storage import PartitionId
from google.cloud.dlp_v2.types.storage import RecordKey
from google.cloud.dlp_v2.types.storage import StorageConfig
from google.cloud.dlp_v2.types.storage import StoredType
from google.cloud.dlp_v2.types.storage import TableOptions
from google.cloud.dlp_v2.types.storage import FileType
from google.cloud.dlp_v2.types.storage import Likelihood

__all__ = (
    "DlpServiceClient",
    "DlpServiceAsyncClient",
    "Action",
    "ActivateJobTriggerRequest",
    "AnalyzeDataSourceRiskDetails",
    "BoundingBox",
    "BucketingConfig",
    "ByteContentItem",
    "CancelDlpJobRequest",
    "CharacterMaskConfig",
    "CharsToIgnore",
    "Color",
    "Container",
    "ContentItem",
    "ContentLocation",
    "CreateDeidentifyTemplateRequest",
    "CreateDlpJobRequest",
    "CreateInspectTemplateRequest",
    "CreateJobTriggerRequest",
    "CreateStoredInfoTypeRequest",
    "CryptoDeterministicConfig",
    "CryptoHashConfig",
    "CryptoKey",
    "CryptoReplaceFfxFpeConfig",
    "DateShiftConfig",
    "DateTime",
    "DeidentifyConfig",
    "DeidentifyContentRequest",
    "DeidentifyContentResponse",
    "DeidentifyTemplate",
    "DeleteDeidentifyTemplateRequest",
    "DeleteDlpJobRequest",
    "DeleteInspectTemplateRequest",
    "DeleteJobTriggerRequest",
    "DeleteStoredInfoTypeRequest",
    "DlpJob",
    "DocumentLocation",
    "Error",
    "ExcludeInfoTypes",
    "ExclusionRule",
    "FieldTransformation",
    "Finding",
    "FinishDlpJobRequest",
    "FixedSizeBucketingConfig",
    "GetDeidentifyTemplateRequest",
    "GetDlpJobRequest",
    "GetInspectTemplateRequest",
    "GetJobTriggerRequest",
    "GetStoredInfoTypeRequest",
    "HybridContentItem",
    "HybridFindingDetails",
    "HybridInspectDlpJobRequest",
    "HybridInspectJobTriggerRequest",
    "HybridInspectResponse",
    "HybridInspectStatistics",
    "ImageLocation",
    "InfoTypeDescription",
    "InfoTypeStats",
    "InfoTypeTransformations",
    "InspectConfig",
    "InspectContentRequest",
    "InspectContentResponse",
    "InspectDataSourceDetails",
    "InspectionRule",
    "InspectionRuleSet",
    "InspectJobConfig",
    "InspectResult",
    "InspectTemplate",
    "JobTrigger",
    "KmsWrappedCryptoKey",
    "LargeCustomDictionaryConfig",
    "LargeCustomDictionaryStats",
    "ListDeidentifyTemplatesRequest",
    "ListDeidentifyTemplatesResponse",
    "ListDlpJobsRequest",
    "ListDlpJobsResponse",
    "ListInfoTypesRequest",
    "ListInfoTypesResponse",
    "ListInspectTemplatesRequest",
    "ListInspectTemplatesResponse",
    "ListJobTriggersRequest",
    "ListJobTriggersResponse",
    "ListStoredInfoTypesRequest",
    "ListStoredInfoTypesResponse",
    "Location",
    "Manual",
    "MetadataLocation",
    "OutputStorageConfig",
    "PrimitiveTransformation",
    "PrivacyMetric",
    "QuasiId",
    "QuoteInfo",
    "Range",
    "RecordCondition",
    "RecordLocation",
    "RecordSuppression",
    "RecordTransformations",
    "RedactConfig",
    "RedactImageRequest",
    "RedactImageResponse",
    "ReidentifyContentRequest",
    "ReidentifyContentResponse",
    "ReplaceValueConfig",
    "ReplaceWithInfoTypeConfig",
    "RiskAnalysisJobConfig",
    "Schedule",
    "StatisticalTable",
    "StorageMetadataLabel",
    "StoredInfoType",
    "StoredInfoTypeConfig",
    "StoredInfoTypeStats",
    "StoredInfoTypeVersion",
    "Table",
    "TableLocation",
    "TimePartConfig",
    "TransformationErrorHandling",
    "TransformationOverview",
    "TransformationSummary",
    "TransientCryptoKey",
    "UnwrappedCryptoKey",
    "UpdateDeidentifyTemplateRequest",
    "UpdateInspectTemplateRequest",
    "UpdateJobTriggerRequest",
    "UpdateStoredInfoTypeRequest",
    "Value",
    "ValueFrequency",
    "ContentOption",
    "DlpJobType",
    "InfoTypeSupportedBy",
    "MatchingType",
    "MetadataType",
    "RelationalOperator",
    "StoredInfoTypeState",
    "BigQueryField",
    "BigQueryKey",
    "BigQueryOptions",
    "BigQueryTable",
    "CloudStorageFileSet",
    "CloudStorageOptions",
    "CloudStoragePath",
    "CloudStorageRegexFileSet",
    "CustomInfoType",
    "DatastoreKey",
    "DatastoreOptions",
    "EntityId",
    "FieldId",
    "HybridOptions",
    "InfoType",
    "Key",
    "KindExpression",
    "PartitionId",
    "RecordKey",
    "StorageConfig",
    "StoredType",
    "TableOptions",
    "FileType",
    "Likelihood",
)
