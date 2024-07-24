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
from google.cloud.dlp_v2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.dlp_service import DlpServiceClient
from .services.dlp_service import DlpServiceAsyncClient

from .types.dlp import Action
from .types.dlp import ActionDetails
from .types.dlp import ActivateJobTriggerRequest
from .types.dlp import AllOtherDatabaseResources
from .types.dlp import AllOtherResources
from .types.dlp import AnalyzeDataSourceRiskDetails
from .types.dlp import BigQueryDiscoveryTarget
from .types.dlp import BigQueryRegex
from .types.dlp import BigQueryRegexes
from .types.dlp import BigQueryTableCollection
from .types.dlp import BigQueryTableTypes
from .types.dlp import BoundingBox
from .types.dlp import BucketingConfig
from .types.dlp import ByteContentItem
from .types.dlp import CancelDlpJobRequest
from .types.dlp import CharacterMaskConfig
from .types.dlp import CharsToIgnore
from .types.dlp import CloudSqlDiscoveryTarget
from .types.dlp import CloudSqlIamCredential
from .types.dlp import CloudSqlProperties
from .types.dlp import CloudStorageDiscoveryTarget
from .types.dlp import CloudStorageRegex
from .types.dlp import CloudStorageResourceReference
from .types.dlp import Color
from .types.dlp import ColumnDataProfile
from .types.dlp import Connection
from .types.dlp import Container
from .types.dlp import ContentItem
from .types.dlp import ContentLocation
from .types.dlp import CreateConnectionRequest
from .types.dlp import CreateDeidentifyTemplateRequest
from .types.dlp import CreateDiscoveryConfigRequest
from .types.dlp import CreateDlpJobRequest
from .types.dlp import CreateInspectTemplateRequest
from .types.dlp import CreateJobTriggerRequest
from .types.dlp import CreateStoredInfoTypeRequest
from .types.dlp import CryptoDeterministicConfig
from .types.dlp import CryptoHashConfig
from .types.dlp import CryptoKey
from .types.dlp import CryptoReplaceFfxFpeConfig
from .types.dlp import DatabaseResourceCollection
from .types.dlp import DatabaseResourceReference
from .types.dlp import DatabaseResourceRegex
from .types.dlp import DatabaseResourceRegexes
from .types.dlp import DataProfileAction
from .types.dlp import DataProfileBigQueryRowSchema
from .types.dlp import DataProfileConfigSnapshot
from .types.dlp import DataProfileJobConfig
from .types.dlp import DataProfileLocation
from .types.dlp import DataProfilePubSubCondition
from .types.dlp import DataProfilePubSubMessage
from .types.dlp import DataRiskLevel
from .types.dlp import DataSourceType
from .types.dlp import DateShiftConfig
from .types.dlp import DateTime
from .types.dlp import DeidentifyConfig
from .types.dlp import DeidentifyContentRequest
from .types.dlp import DeidentifyContentResponse
from .types.dlp import DeidentifyDataSourceDetails
from .types.dlp import DeidentifyDataSourceStats
from .types.dlp import DeidentifyTemplate
from .types.dlp import DeleteConnectionRequest
from .types.dlp import DeleteDeidentifyTemplateRequest
from .types.dlp import DeleteDiscoveryConfigRequest
from .types.dlp import DeleteDlpJobRequest
from .types.dlp import DeleteFileStoreDataProfileRequest
from .types.dlp import DeleteInspectTemplateRequest
from .types.dlp import DeleteJobTriggerRequest
from .types.dlp import DeleteStoredInfoTypeRequest
from .types.dlp import DeleteTableDataProfileRequest
from .types.dlp import Disabled
from .types.dlp import DiscoveryBigQueryConditions
from .types.dlp import DiscoveryBigQueryFilter
from .types.dlp import DiscoveryCloudSqlConditions
from .types.dlp import DiscoveryCloudSqlFilter
from .types.dlp import DiscoveryCloudSqlGenerationCadence
from .types.dlp import DiscoveryCloudStorageConditions
from .types.dlp import DiscoveryCloudStorageFilter
from .types.dlp import DiscoveryCloudStorageGenerationCadence
from .types.dlp import DiscoveryConfig
from .types.dlp import DiscoveryFileStoreConditions
from .types.dlp import DiscoveryGenerationCadence
from .types.dlp import DiscoveryInspectTemplateModifiedCadence
from .types.dlp import DiscoverySchemaModifiedCadence
from .types.dlp import DiscoveryStartingLocation
from .types.dlp import DiscoveryTableModifiedCadence
from .types.dlp import DiscoveryTarget
from .types.dlp import DlpJob
from .types.dlp import DocumentLocation
from .types.dlp import Error
from .types.dlp import ExcludeByHotword
from .types.dlp import ExcludeInfoTypes
from .types.dlp import ExclusionRule
from .types.dlp import FieldTransformation
from .types.dlp import FileClusterSummary
from .types.dlp import FileClusterType
from .types.dlp import FileExtensionInfo
from .types.dlp import FileStoreCollection
from .types.dlp import FileStoreDataProfile
from .types.dlp import FileStoreInfoTypeSummary
from .types.dlp import FileStoreRegex
from .types.dlp import FileStoreRegexes
from .types.dlp import Finding
from .types.dlp import FinishDlpJobRequest
from .types.dlp import FixedSizeBucketingConfig
from .types.dlp import GetColumnDataProfileRequest
from .types.dlp import GetConnectionRequest
from .types.dlp import GetDeidentifyTemplateRequest
from .types.dlp import GetDiscoveryConfigRequest
from .types.dlp import GetDlpJobRequest
from .types.dlp import GetFileStoreDataProfileRequest
from .types.dlp import GetInspectTemplateRequest
from .types.dlp import GetJobTriggerRequest
from .types.dlp import GetProjectDataProfileRequest
from .types.dlp import GetStoredInfoTypeRequest
from .types.dlp import GetTableDataProfileRequest
from .types.dlp import HybridContentItem
from .types.dlp import HybridFindingDetails
from .types.dlp import HybridInspectDlpJobRequest
from .types.dlp import HybridInspectJobTriggerRequest
from .types.dlp import HybridInspectResponse
from .types.dlp import HybridInspectStatistics
from .types.dlp import ImageLocation
from .types.dlp import ImageTransformations
from .types.dlp import InfoTypeCategory
from .types.dlp import InfoTypeDescription
from .types.dlp import InfoTypeStats
from .types.dlp import InfoTypeSummary
from .types.dlp import InfoTypeTransformations
from .types.dlp import InspectConfig
from .types.dlp import InspectContentRequest
from .types.dlp import InspectContentResponse
from .types.dlp import InspectDataSourceDetails
from .types.dlp import InspectionRule
from .types.dlp import InspectionRuleSet
from .types.dlp import InspectJobConfig
from .types.dlp import InspectResult
from .types.dlp import InspectTemplate
from .types.dlp import JobTrigger
from .types.dlp import KmsWrappedCryptoKey
from .types.dlp import LargeCustomDictionaryConfig
from .types.dlp import LargeCustomDictionaryStats
from .types.dlp import ListColumnDataProfilesRequest
from .types.dlp import ListColumnDataProfilesResponse
from .types.dlp import ListConnectionsRequest
from .types.dlp import ListConnectionsResponse
from .types.dlp import ListDeidentifyTemplatesRequest
from .types.dlp import ListDeidentifyTemplatesResponse
from .types.dlp import ListDiscoveryConfigsRequest
from .types.dlp import ListDiscoveryConfigsResponse
from .types.dlp import ListDlpJobsRequest
from .types.dlp import ListDlpJobsResponse
from .types.dlp import ListFileStoreDataProfilesRequest
from .types.dlp import ListFileStoreDataProfilesResponse
from .types.dlp import ListInfoTypesRequest
from .types.dlp import ListInfoTypesResponse
from .types.dlp import ListInspectTemplatesRequest
from .types.dlp import ListInspectTemplatesResponse
from .types.dlp import ListJobTriggersRequest
from .types.dlp import ListJobTriggersResponse
from .types.dlp import ListProjectDataProfilesRequest
from .types.dlp import ListProjectDataProfilesResponse
from .types.dlp import ListStoredInfoTypesRequest
from .types.dlp import ListStoredInfoTypesResponse
from .types.dlp import ListTableDataProfilesRequest
from .types.dlp import ListTableDataProfilesResponse
from .types.dlp import Location
from .types.dlp import Manual
from .types.dlp import MetadataLocation
from .types.dlp import OtherInfoTypeSummary
from .types.dlp import OutputStorageConfig
from .types.dlp import PrimitiveTransformation
from .types.dlp import PrivacyMetric
from .types.dlp import ProfileStatus
from .types.dlp import ProjectDataProfile
from .types.dlp import QuasiId
from .types.dlp import QuoteInfo
from .types.dlp import Range
from .types.dlp import RecordCondition
from .types.dlp import RecordLocation
from .types.dlp import RecordSuppression
from .types.dlp import RecordTransformation
from .types.dlp import RecordTransformations
from .types.dlp import RedactConfig
from .types.dlp import RedactImageRequest
from .types.dlp import RedactImageResponse
from .types.dlp import ReidentifyContentRequest
from .types.dlp import ReidentifyContentResponse
from .types.dlp import ReplaceDictionaryConfig
from .types.dlp import ReplaceValueConfig
from .types.dlp import ReplaceWithInfoTypeConfig
from .types.dlp import RiskAnalysisJobConfig
from .types.dlp import Schedule
from .types.dlp import SearchConnectionsRequest
from .types.dlp import SearchConnectionsResponse
from .types.dlp import SecretManagerCredential
from .types.dlp import SecretsDiscoveryTarget
from .types.dlp import StatisticalTable
from .types.dlp import StorageMetadataLabel
from .types.dlp import StoredInfoType
from .types.dlp import StoredInfoTypeConfig
from .types.dlp import StoredInfoTypeStats
from .types.dlp import StoredInfoTypeVersion
from .types.dlp import Table
from .types.dlp import TableDataProfile
from .types.dlp import TableLocation
from .types.dlp import TimePartConfig
from .types.dlp import TransformationConfig
from .types.dlp import TransformationDescription
from .types.dlp import TransformationDetails
from .types.dlp import TransformationDetailsStorageConfig
from .types.dlp import TransformationErrorHandling
from .types.dlp import TransformationLocation
from .types.dlp import TransformationOverview
from .types.dlp import TransformationResultStatus
from .types.dlp import TransformationSummary
from .types.dlp import TransientCryptoKey
from .types.dlp import UnwrappedCryptoKey
from .types.dlp import UpdateConnectionRequest
from .types.dlp import UpdateDeidentifyTemplateRequest
from .types.dlp import UpdateDiscoveryConfigRequest
from .types.dlp import UpdateInspectTemplateRequest
from .types.dlp import UpdateJobTriggerRequest
from .types.dlp import UpdateStoredInfoTypeRequest
from .types.dlp import Value
from .types.dlp import ValueFrequency
from .types.dlp import VersionDescription
from .types.dlp import BigQuerySchemaModification
from .types.dlp import BigQueryTableModification
from .types.dlp import BigQueryTableType
from .types.dlp import BigQueryTableTypeCollection
from .types.dlp import ConnectionState
from .types.dlp import ContentOption
from .types.dlp import DataProfileUpdateFrequency
from .types.dlp import DlpJobType
from .types.dlp import EncryptionStatus
from .types.dlp import InfoTypeSupportedBy
from .types.dlp import MatchingType
from .types.dlp import MetadataType
from .types.dlp import NullPercentageLevel
from .types.dlp import RelationalOperator
from .types.dlp import ResourceVisibility
from .types.dlp import StoredInfoTypeState
from .types.dlp import TransformationContainerType
from .types.dlp import TransformationResultStatusType
from .types.dlp import TransformationType
from .types.dlp import UniquenessScoreLevel
from .types.storage import BigQueryField
from .types.storage import BigQueryKey
from .types.storage import BigQueryOptions
from .types.storage import BigQueryTable
from .types.storage import CloudStorageFileSet
from .types.storage import CloudStorageOptions
from .types.storage import CloudStoragePath
from .types.storage import CloudStorageRegexFileSet
from .types.storage import CustomInfoType
from .types.storage import DatastoreKey
from .types.storage import DatastoreOptions
from .types.storage import EntityId
from .types.storage import FieldId
from .types.storage import HybridOptions
from .types.storage import InfoType
from .types.storage import Key
from .types.storage import KindExpression
from .types.storage import PartitionId
from .types.storage import RecordKey
from .types.storage import SensitivityScore
from .types.storage import StorageConfig
from .types.storage import StoredType
from .types.storage import TableOptions
from .types.storage import TableReference
from .types.storage import FileType
from .types.storage import Likelihood

__all__ = (
    'DlpServiceAsyncClient',
'Action',
'ActionDetails',
'ActivateJobTriggerRequest',
'AllOtherDatabaseResources',
'AllOtherResources',
'AnalyzeDataSourceRiskDetails',
'BigQueryDiscoveryTarget',
'BigQueryField',
'BigQueryKey',
'BigQueryOptions',
'BigQueryRegex',
'BigQueryRegexes',
'BigQuerySchemaModification',
'BigQueryTable',
'BigQueryTableCollection',
'BigQueryTableModification',
'BigQueryTableType',
'BigQueryTableTypeCollection',
'BigQueryTableTypes',
'BoundingBox',
'BucketingConfig',
'ByteContentItem',
'CancelDlpJobRequest',
'CharacterMaskConfig',
'CharsToIgnore',
'CloudSqlDiscoveryTarget',
'CloudSqlIamCredential',
'CloudSqlProperties',
'CloudStorageDiscoveryTarget',
'CloudStorageFileSet',
'CloudStorageOptions',
'CloudStoragePath',
'CloudStorageRegex',
'CloudStorageRegexFileSet',
'CloudStorageResourceReference',
'Color',
'ColumnDataProfile',
'Connection',
'ConnectionState',
'Container',
'ContentItem',
'ContentLocation',
'ContentOption',
'CreateConnectionRequest',
'CreateDeidentifyTemplateRequest',
'CreateDiscoveryConfigRequest',
'CreateDlpJobRequest',
'CreateInspectTemplateRequest',
'CreateJobTriggerRequest',
'CreateStoredInfoTypeRequest',
'CryptoDeterministicConfig',
'CryptoHashConfig',
'CryptoKey',
'CryptoReplaceFfxFpeConfig',
'CustomInfoType',
'DataProfileAction',
'DataProfileBigQueryRowSchema',
'DataProfileConfigSnapshot',
'DataProfileJobConfig',
'DataProfileLocation',
'DataProfilePubSubCondition',
'DataProfilePubSubMessage',
'DataProfileUpdateFrequency',
'DataRiskLevel',
'DataSourceType',
'DatabaseResourceCollection',
'DatabaseResourceReference',
'DatabaseResourceRegex',
'DatabaseResourceRegexes',
'DatastoreKey',
'DatastoreOptions',
'DateShiftConfig',
'DateTime',
'DeidentifyConfig',
'DeidentifyContentRequest',
'DeidentifyContentResponse',
'DeidentifyDataSourceDetails',
'DeidentifyDataSourceStats',
'DeidentifyTemplate',
'DeleteConnectionRequest',
'DeleteDeidentifyTemplateRequest',
'DeleteDiscoveryConfigRequest',
'DeleteDlpJobRequest',
'DeleteFileStoreDataProfileRequest',
'DeleteInspectTemplateRequest',
'DeleteJobTriggerRequest',
'DeleteStoredInfoTypeRequest',
'DeleteTableDataProfileRequest',
'Disabled',
'DiscoveryBigQueryConditions',
'DiscoveryBigQueryFilter',
'DiscoveryCloudSqlConditions',
'DiscoveryCloudSqlFilter',
'DiscoveryCloudSqlGenerationCadence',
'DiscoveryCloudStorageConditions',
'DiscoveryCloudStorageFilter',
'DiscoveryCloudStorageGenerationCadence',
'DiscoveryConfig',
'DiscoveryFileStoreConditions',
'DiscoveryGenerationCadence',
'DiscoveryInspectTemplateModifiedCadence',
'DiscoverySchemaModifiedCadence',
'DiscoveryStartingLocation',
'DiscoveryTableModifiedCadence',
'DiscoveryTarget',
'DlpJob',
'DlpJobType',
'DlpServiceClient',
'DocumentLocation',
'EncryptionStatus',
'EntityId',
'Error',
'ExcludeByHotword',
'ExcludeInfoTypes',
'ExclusionRule',
'FieldId',
'FieldTransformation',
'FileClusterSummary',
'FileClusterType',
'FileExtensionInfo',
'FileStoreCollection',
'FileStoreDataProfile',
'FileStoreInfoTypeSummary',
'FileStoreRegex',
'FileStoreRegexes',
'FileType',
'Finding',
'FinishDlpJobRequest',
'FixedSizeBucketingConfig',
'GetColumnDataProfileRequest',
'GetConnectionRequest',
'GetDeidentifyTemplateRequest',
'GetDiscoveryConfigRequest',
'GetDlpJobRequest',
'GetFileStoreDataProfileRequest',
'GetInspectTemplateRequest',
'GetJobTriggerRequest',
'GetProjectDataProfileRequest',
'GetStoredInfoTypeRequest',
'GetTableDataProfileRequest',
'HybridContentItem',
'HybridFindingDetails',
'HybridInspectDlpJobRequest',
'HybridInspectJobTriggerRequest',
'HybridInspectResponse',
'HybridInspectStatistics',
'HybridOptions',
'ImageLocation',
'ImageTransformations',
'InfoType',
'InfoTypeCategory',
'InfoTypeDescription',
'InfoTypeStats',
'InfoTypeSummary',
'InfoTypeSupportedBy',
'InfoTypeTransformations',
'InspectConfig',
'InspectContentRequest',
'InspectContentResponse',
'InspectDataSourceDetails',
'InspectJobConfig',
'InspectResult',
'InspectTemplate',
'InspectionRule',
'InspectionRuleSet',
'JobTrigger',
'Key',
'KindExpression',
'KmsWrappedCryptoKey',
'LargeCustomDictionaryConfig',
'LargeCustomDictionaryStats',
'Likelihood',
'ListColumnDataProfilesRequest',
'ListColumnDataProfilesResponse',
'ListConnectionsRequest',
'ListConnectionsResponse',
'ListDeidentifyTemplatesRequest',
'ListDeidentifyTemplatesResponse',
'ListDiscoveryConfigsRequest',
'ListDiscoveryConfigsResponse',
'ListDlpJobsRequest',
'ListDlpJobsResponse',
'ListFileStoreDataProfilesRequest',
'ListFileStoreDataProfilesResponse',
'ListInfoTypesRequest',
'ListInfoTypesResponse',
'ListInspectTemplatesRequest',
'ListInspectTemplatesResponse',
'ListJobTriggersRequest',
'ListJobTriggersResponse',
'ListProjectDataProfilesRequest',
'ListProjectDataProfilesResponse',
'ListStoredInfoTypesRequest',
'ListStoredInfoTypesResponse',
'ListTableDataProfilesRequest',
'ListTableDataProfilesResponse',
'Location',
'Manual',
'MatchingType',
'MetadataLocation',
'MetadataType',
'NullPercentageLevel',
'OtherInfoTypeSummary',
'OutputStorageConfig',
'PartitionId',
'PrimitiveTransformation',
'PrivacyMetric',
'ProfileStatus',
'ProjectDataProfile',
'QuasiId',
'QuoteInfo',
'Range',
'RecordCondition',
'RecordKey',
'RecordLocation',
'RecordSuppression',
'RecordTransformation',
'RecordTransformations',
'RedactConfig',
'RedactImageRequest',
'RedactImageResponse',
'ReidentifyContentRequest',
'ReidentifyContentResponse',
'RelationalOperator',
'ReplaceDictionaryConfig',
'ReplaceValueConfig',
'ReplaceWithInfoTypeConfig',
'ResourceVisibility',
'RiskAnalysisJobConfig',
'Schedule',
'SearchConnectionsRequest',
'SearchConnectionsResponse',
'SecretManagerCredential',
'SecretsDiscoveryTarget',
'SensitivityScore',
'StatisticalTable',
'StorageConfig',
'StorageMetadataLabel',
'StoredInfoType',
'StoredInfoTypeConfig',
'StoredInfoTypeState',
'StoredInfoTypeStats',
'StoredInfoTypeVersion',
'StoredType',
'Table',
'TableDataProfile',
'TableLocation',
'TableOptions',
'TableReference',
'TimePartConfig',
'TransformationConfig',
'TransformationContainerType',
'TransformationDescription',
'TransformationDetails',
'TransformationDetailsStorageConfig',
'TransformationErrorHandling',
'TransformationLocation',
'TransformationOverview',
'TransformationResultStatus',
'TransformationResultStatusType',
'TransformationSummary',
'TransformationType',
'TransientCryptoKey',
'UniquenessScoreLevel',
'UnwrappedCryptoKey',
'UpdateConnectionRequest',
'UpdateDeidentifyTemplateRequest',
'UpdateDiscoveryConfigRequest',
'UpdateInspectTemplateRequest',
'UpdateJobTriggerRequest',
'UpdateStoredInfoTypeRequest',
'Value',
'ValueFrequency',
'VersionDescription',
)
