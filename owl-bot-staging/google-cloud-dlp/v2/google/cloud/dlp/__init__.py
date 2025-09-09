# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from google.cloud.dlp import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.dlp_v2.services.dlp_service.client import DlpServiceClient
from google.cloud.dlp_v2.services.dlp_service.async_client import DlpServiceAsyncClient

from google.cloud.dlp_v2.types.dlp import Action
from google.cloud.dlp_v2.types.dlp import ActionDetails
from google.cloud.dlp_v2.types.dlp import ActivateJobTriggerRequest
from google.cloud.dlp_v2.types.dlp import AllOtherDatabaseResources
from google.cloud.dlp_v2.types.dlp import AllOtherResources
from google.cloud.dlp_v2.types.dlp import AmazonS3Bucket
from google.cloud.dlp_v2.types.dlp import AmazonS3BucketConditions
from google.cloud.dlp_v2.types.dlp import AmazonS3BucketRegex
from google.cloud.dlp_v2.types.dlp import AnalyzeDataSourceRiskDetails
from google.cloud.dlp_v2.types.dlp import AwsAccount
from google.cloud.dlp_v2.types.dlp import AwsAccountRegex
from google.cloud.dlp_v2.types.dlp import BigQueryDiscoveryTarget
from google.cloud.dlp_v2.types.dlp import BigQueryRegex
from google.cloud.dlp_v2.types.dlp import BigQueryRegexes
from google.cloud.dlp_v2.types.dlp import BigQueryTableCollection
from google.cloud.dlp_v2.types.dlp import BigQueryTableTypes
from google.cloud.dlp_v2.types.dlp import BoundingBox
from google.cloud.dlp_v2.types.dlp import BucketingConfig
from google.cloud.dlp_v2.types.dlp import ByteContentItem
from google.cloud.dlp_v2.types.dlp import CancelDlpJobRequest
from google.cloud.dlp_v2.types.dlp import CharacterMaskConfig
from google.cloud.dlp_v2.types.dlp import CharsToIgnore
from google.cloud.dlp_v2.types.dlp import CloudSqlDiscoveryTarget
from google.cloud.dlp_v2.types.dlp import CloudSqlIamCredential
from google.cloud.dlp_v2.types.dlp import CloudSqlProperties
from google.cloud.dlp_v2.types.dlp import CloudStorageDiscoveryTarget
from google.cloud.dlp_v2.types.dlp import CloudStorageRegex
from google.cloud.dlp_v2.types.dlp import CloudStorageResourceReference
from google.cloud.dlp_v2.types.dlp import Color
from google.cloud.dlp_v2.types.dlp import ColumnDataProfile
from google.cloud.dlp_v2.types.dlp import Connection
from google.cloud.dlp_v2.types.dlp import Container
from google.cloud.dlp_v2.types.dlp import ContentItem
from google.cloud.dlp_v2.types.dlp import ContentLocation
from google.cloud.dlp_v2.types.dlp import CreateConnectionRequest
from google.cloud.dlp_v2.types.dlp import CreateDeidentifyTemplateRequest
from google.cloud.dlp_v2.types.dlp import CreateDiscoveryConfigRequest
from google.cloud.dlp_v2.types.dlp import CreateDlpJobRequest
from google.cloud.dlp_v2.types.dlp import CreateInspectTemplateRequest
from google.cloud.dlp_v2.types.dlp import CreateJobTriggerRequest
from google.cloud.dlp_v2.types.dlp import CreateStoredInfoTypeRequest
from google.cloud.dlp_v2.types.dlp import CryptoDeterministicConfig
from google.cloud.dlp_v2.types.dlp import CryptoHashConfig
from google.cloud.dlp_v2.types.dlp import CryptoKey
from google.cloud.dlp_v2.types.dlp import CryptoReplaceFfxFpeConfig
from google.cloud.dlp_v2.types.dlp import DatabaseResourceCollection
from google.cloud.dlp_v2.types.dlp import DatabaseResourceReference
from google.cloud.dlp_v2.types.dlp import DatabaseResourceRegex
from google.cloud.dlp_v2.types.dlp import DatabaseResourceRegexes
from google.cloud.dlp_v2.types.dlp import DataProfileAction
from google.cloud.dlp_v2.types.dlp import DataProfileBigQueryRowSchema
from google.cloud.dlp_v2.types.dlp import DataProfileConfigSnapshot
from google.cloud.dlp_v2.types.dlp import DataProfileFinding
from google.cloud.dlp_v2.types.dlp import DataProfileFindingLocation
from google.cloud.dlp_v2.types.dlp import DataProfileFindingRecordLocation
from google.cloud.dlp_v2.types.dlp import DataProfileJobConfig
from google.cloud.dlp_v2.types.dlp import DataProfileLocation
from google.cloud.dlp_v2.types.dlp import DataProfilePubSubCondition
from google.cloud.dlp_v2.types.dlp import DataProfilePubSubMessage
from google.cloud.dlp_v2.types.dlp import DataRiskLevel
from google.cloud.dlp_v2.types.dlp import DataSourceType
from google.cloud.dlp_v2.types.dlp import DateShiftConfig
from google.cloud.dlp_v2.types.dlp import DateTime
from google.cloud.dlp_v2.types.dlp import DeidentifyConfig
from google.cloud.dlp_v2.types.dlp import DeidentifyContentRequest
from google.cloud.dlp_v2.types.dlp import DeidentifyContentResponse
from google.cloud.dlp_v2.types.dlp import DeidentifyDataSourceDetails
from google.cloud.dlp_v2.types.dlp import DeidentifyDataSourceStats
from google.cloud.dlp_v2.types.dlp import DeidentifyTemplate
from google.cloud.dlp_v2.types.dlp import DeleteConnectionRequest
from google.cloud.dlp_v2.types.dlp import DeleteDeidentifyTemplateRequest
from google.cloud.dlp_v2.types.dlp import DeleteDiscoveryConfigRequest
from google.cloud.dlp_v2.types.dlp import DeleteDlpJobRequest
from google.cloud.dlp_v2.types.dlp import DeleteFileStoreDataProfileRequest
from google.cloud.dlp_v2.types.dlp import DeleteInspectTemplateRequest
from google.cloud.dlp_v2.types.dlp import DeleteJobTriggerRequest
from google.cloud.dlp_v2.types.dlp import DeleteStoredInfoTypeRequest
from google.cloud.dlp_v2.types.dlp import DeleteTableDataProfileRequest
from google.cloud.dlp_v2.types.dlp import Disabled
from google.cloud.dlp_v2.types.dlp import DiscoveryBigQueryConditions
from google.cloud.dlp_v2.types.dlp import DiscoveryBigQueryFilter
from google.cloud.dlp_v2.types.dlp import DiscoveryCloudSqlConditions
from google.cloud.dlp_v2.types.dlp import DiscoveryCloudSqlFilter
from google.cloud.dlp_v2.types.dlp import DiscoveryCloudSqlGenerationCadence
from google.cloud.dlp_v2.types.dlp import DiscoveryCloudStorageConditions
from google.cloud.dlp_v2.types.dlp import DiscoveryCloudStorageFilter
from google.cloud.dlp_v2.types.dlp import DiscoveryCloudStorageGenerationCadence
from google.cloud.dlp_v2.types.dlp import DiscoveryConfig
from google.cloud.dlp_v2.types.dlp import DiscoveryFileStoreConditions
from google.cloud.dlp_v2.types.dlp import DiscoveryGenerationCadence
from google.cloud.dlp_v2.types.dlp import DiscoveryInspectTemplateModifiedCadence
from google.cloud.dlp_v2.types.dlp import DiscoveryOtherCloudConditions
from google.cloud.dlp_v2.types.dlp import DiscoveryOtherCloudFilter
from google.cloud.dlp_v2.types.dlp import DiscoveryOtherCloudGenerationCadence
from google.cloud.dlp_v2.types.dlp import DiscoverySchemaModifiedCadence
from google.cloud.dlp_v2.types.dlp import DiscoveryStartingLocation
from google.cloud.dlp_v2.types.dlp import DiscoveryTableModifiedCadence
from google.cloud.dlp_v2.types.dlp import DiscoveryTarget
from google.cloud.dlp_v2.types.dlp import DiscoveryVertexDatasetConditions
from google.cloud.dlp_v2.types.dlp import DiscoveryVertexDatasetFilter
from google.cloud.dlp_v2.types.dlp import DiscoveryVertexDatasetGenerationCadence
from google.cloud.dlp_v2.types.dlp import DlpJob
from google.cloud.dlp_v2.types.dlp import DocumentLocation
from google.cloud.dlp_v2.types.dlp import Domain
from google.cloud.dlp_v2.types.dlp import Error
from google.cloud.dlp_v2.types.dlp import ExcludeByHotword
from google.cloud.dlp_v2.types.dlp import ExcludeInfoTypes
from google.cloud.dlp_v2.types.dlp import ExclusionRule
from google.cloud.dlp_v2.types.dlp import FieldTransformation
from google.cloud.dlp_v2.types.dlp import FileClusterSummary
from google.cloud.dlp_v2.types.dlp import FileClusterType
from google.cloud.dlp_v2.types.dlp import FileExtensionInfo
from google.cloud.dlp_v2.types.dlp import FileStoreCollection
from google.cloud.dlp_v2.types.dlp import FileStoreDataProfile
from google.cloud.dlp_v2.types.dlp import FileStoreInfoTypeSummary
from google.cloud.dlp_v2.types.dlp import FileStoreRegex
from google.cloud.dlp_v2.types.dlp import FileStoreRegexes
from google.cloud.dlp_v2.types.dlp import Finding
from google.cloud.dlp_v2.types.dlp import FinishDlpJobRequest
from google.cloud.dlp_v2.types.dlp import FixedSizeBucketingConfig
from google.cloud.dlp_v2.types.dlp import GetColumnDataProfileRequest
from google.cloud.dlp_v2.types.dlp import GetConnectionRequest
from google.cloud.dlp_v2.types.dlp import GetDeidentifyTemplateRequest
from google.cloud.dlp_v2.types.dlp import GetDiscoveryConfigRequest
from google.cloud.dlp_v2.types.dlp import GetDlpJobRequest
from google.cloud.dlp_v2.types.dlp import GetFileStoreDataProfileRequest
from google.cloud.dlp_v2.types.dlp import GetInspectTemplateRequest
from google.cloud.dlp_v2.types.dlp import GetJobTriggerRequest
from google.cloud.dlp_v2.types.dlp import GetProjectDataProfileRequest
from google.cloud.dlp_v2.types.dlp import GetStoredInfoTypeRequest
from google.cloud.dlp_v2.types.dlp import GetTableDataProfileRequest
from google.cloud.dlp_v2.types.dlp import HybridContentItem
from google.cloud.dlp_v2.types.dlp import HybridFindingDetails
from google.cloud.dlp_v2.types.dlp import HybridInspectDlpJobRequest
from google.cloud.dlp_v2.types.dlp import HybridInspectJobTriggerRequest
from google.cloud.dlp_v2.types.dlp import HybridInspectResponse
from google.cloud.dlp_v2.types.dlp import HybridInspectStatistics
from google.cloud.dlp_v2.types.dlp import ImageLocation
from google.cloud.dlp_v2.types.dlp import ImageTransformations
from google.cloud.dlp_v2.types.dlp import InfoTypeCategory
from google.cloud.dlp_v2.types.dlp import InfoTypeDescription
from google.cloud.dlp_v2.types.dlp import InfoTypeStats
from google.cloud.dlp_v2.types.dlp import InfoTypeSummary
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
from google.cloud.dlp_v2.types.dlp import ListColumnDataProfilesRequest
from google.cloud.dlp_v2.types.dlp import ListColumnDataProfilesResponse
from google.cloud.dlp_v2.types.dlp import ListConnectionsRequest
from google.cloud.dlp_v2.types.dlp import ListConnectionsResponse
from google.cloud.dlp_v2.types.dlp import ListDeidentifyTemplatesRequest
from google.cloud.dlp_v2.types.dlp import ListDeidentifyTemplatesResponse
from google.cloud.dlp_v2.types.dlp import ListDiscoveryConfigsRequest
from google.cloud.dlp_v2.types.dlp import ListDiscoveryConfigsResponse
from google.cloud.dlp_v2.types.dlp import ListDlpJobsRequest
from google.cloud.dlp_v2.types.dlp import ListDlpJobsResponse
from google.cloud.dlp_v2.types.dlp import ListFileStoreDataProfilesRequest
from google.cloud.dlp_v2.types.dlp import ListFileStoreDataProfilesResponse
from google.cloud.dlp_v2.types.dlp import ListInfoTypesRequest
from google.cloud.dlp_v2.types.dlp import ListInfoTypesResponse
from google.cloud.dlp_v2.types.dlp import ListInspectTemplatesRequest
from google.cloud.dlp_v2.types.dlp import ListInspectTemplatesResponse
from google.cloud.dlp_v2.types.dlp import ListJobTriggersRequest
from google.cloud.dlp_v2.types.dlp import ListJobTriggersResponse
from google.cloud.dlp_v2.types.dlp import ListProjectDataProfilesRequest
from google.cloud.dlp_v2.types.dlp import ListProjectDataProfilesResponse
from google.cloud.dlp_v2.types.dlp import ListStoredInfoTypesRequest
from google.cloud.dlp_v2.types.dlp import ListStoredInfoTypesResponse
from google.cloud.dlp_v2.types.dlp import ListTableDataProfilesRequest
from google.cloud.dlp_v2.types.dlp import ListTableDataProfilesResponse
from google.cloud.dlp_v2.types.dlp import Location
from google.cloud.dlp_v2.types.dlp import LocationSupport
from google.cloud.dlp_v2.types.dlp import Manual
from google.cloud.dlp_v2.types.dlp import MetadataLocation
from google.cloud.dlp_v2.types.dlp import OtherCloudDiscoveryStartingLocation
from google.cloud.dlp_v2.types.dlp import OtherCloudDiscoveryTarget
from google.cloud.dlp_v2.types.dlp import OtherCloudResourceCollection
from google.cloud.dlp_v2.types.dlp import OtherCloudResourceRegex
from google.cloud.dlp_v2.types.dlp import OtherCloudResourceRegexes
from google.cloud.dlp_v2.types.dlp import OtherCloudSingleResourceReference
from google.cloud.dlp_v2.types.dlp import OtherInfoTypeSummary
from google.cloud.dlp_v2.types.dlp import OutputStorageConfig
from google.cloud.dlp_v2.types.dlp import PrimitiveTransformation
from google.cloud.dlp_v2.types.dlp import PrivacyMetric
from google.cloud.dlp_v2.types.dlp import ProcessingLocation
from google.cloud.dlp_v2.types.dlp import ProfileStatus
from google.cloud.dlp_v2.types.dlp import ProjectDataProfile
from google.cloud.dlp_v2.types.dlp import QuasiId
from google.cloud.dlp_v2.types.dlp import QuoteInfo
from google.cloud.dlp_v2.types.dlp import Range
from google.cloud.dlp_v2.types.dlp import RecordCondition
from google.cloud.dlp_v2.types.dlp import RecordLocation
from google.cloud.dlp_v2.types.dlp import RecordSuppression
from google.cloud.dlp_v2.types.dlp import RecordTransformation
from google.cloud.dlp_v2.types.dlp import RecordTransformations
from google.cloud.dlp_v2.types.dlp import RedactConfig
from google.cloud.dlp_v2.types.dlp import RedactImageRequest
from google.cloud.dlp_v2.types.dlp import RedactImageResponse
from google.cloud.dlp_v2.types.dlp import ReidentifyContentRequest
from google.cloud.dlp_v2.types.dlp import ReidentifyContentResponse
from google.cloud.dlp_v2.types.dlp import RelatedResource
from google.cloud.dlp_v2.types.dlp import ReplaceDictionaryConfig
from google.cloud.dlp_v2.types.dlp import ReplaceValueConfig
from google.cloud.dlp_v2.types.dlp import ReplaceWithInfoTypeConfig
from google.cloud.dlp_v2.types.dlp import RiskAnalysisJobConfig
from google.cloud.dlp_v2.types.dlp import SaveToGcsFindingsOutput
from google.cloud.dlp_v2.types.dlp import Schedule
from google.cloud.dlp_v2.types.dlp import SearchConnectionsRequest
from google.cloud.dlp_v2.types.dlp import SearchConnectionsResponse
from google.cloud.dlp_v2.types.dlp import SecretManagerCredential
from google.cloud.dlp_v2.types.dlp import SecretsDiscoveryTarget
from google.cloud.dlp_v2.types.dlp import StatisticalTable
from google.cloud.dlp_v2.types.dlp import StorageMetadataLabel
from google.cloud.dlp_v2.types.dlp import StoredInfoType
from google.cloud.dlp_v2.types.dlp import StoredInfoTypeConfig
from google.cloud.dlp_v2.types.dlp import StoredInfoTypeStats
from google.cloud.dlp_v2.types.dlp import StoredInfoTypeVersion
from google.cloud.dlp_v2.types.dlp import Table
from google.cloud.dlp_v2.types.dlp import TableDataProfile
from google.cloud.dlp_v2.types.dlp import TableLocation
from google.cloud.dlp_v2.types.dlp import Tag
from google.cloud.dlp_v2.types.dlp import TimePartConfig
from google.cloud.dlp_v2.types.dlp import TransformationConfig
from google.cloud.dlp_v2.types.dlp import TransformationDescription
from google.cloud.dlp_v2.types.dlp import TransformationDetails
from google.cloud.dlp_v2.types.dlp import TransformationDetailsStorageConfig
from google.cloud.dlp_v2.types.dlp import TransformationErrorHandling
from google.cloud.dlp_v2.types.dlp import TransformationLocation
from google.cloud.dlp_v2.types.dlp import TransformationOverview
from google.cloud.dlp_v2.types.dlp import TransformationResultStatus
from google.cloud.dlp_v2.types.dlp import TransformationSummary
from google.cloud.dlp_v2.types.dlp import TransientCryptoKey
from google.cloud.dlp_v2.types.dlp import UnwrappedCryptoKey
from google.cloud.dlp_v2.types.dlp import UpdateConnectionRequest
from google.cloud.dlp_v2.types.dlp import UpdateDeidentifyTemplateRequest
from google.cloud.dlp_v2.types.dlp import UpdateDiscoveryConfigRequest
from google.cloud.dlp_v2.types.dlp import UpdateInspectTemplateRequest
from google.cloud.dlp_v2.types.dlp import UpdateJobTriggerRequest
from google.cloud.dlp_v2.types.dlp import UpdateStoredInfoTypeRequest
from google.cloud.dlp_v2.types.dlp import Value
from google.cloud.dlp_v2.types.dlp import ValueFrequency
from google.cloud.dlp_v2.types.dlp import VersionDescription
from google.cloud.dlp_v2.types.dlp import VertexDatasetCollection
from google.cloud.dlp_v2.types.dlp import VertexDatasetDiscoveryTarget
from google.cloud.dlp_v2.types.dlp import VertexDatasetRegex
from google.cloud.dlp_v2.types.dlp import VertexDatasetRegexes
from google.cloud.dlp_v2.types.dlp import VertexDatasetResourceReference
from google.cloud.dlp_v2.types.dlp import BigQuerySchemaModification
from google.cloud.dlp_v2.types.dlp import BigQueryTableModification
from google.cloud.dlp_v2.types.dlp import BigQueryTableType
from google.cloud.dlp_v2.types.dlp import BigQueryTableTypeCollection
from google.cloud.dlp_v2.types.dlp import ConnectionState
from google.cloud.dlp_v2.types.dlp import ContentOption
from google.cloud.dlp_v2.types.dlp import DataProfileUpdateFrequency
from google.cloud.dlp_v2.types.dlp import DlpJobType
from google.cloud.dlp_v2.types.dlp import EncryptionStatus
from google.cloud.dlp_v2.types.dlp import InfoTypeSupportedBy
from google.cloud.dlp_v2.types.dlp import MatchingType
from google.cloud.dlp_v2.types.dlp import MetadataType
from google.cloud.dlp_v2.types.dlp import NullPercentageLevel
from google.cloud.dlp_v2.types.dlp import ProfileGeneration
from google.cloud.dlp_v2.types.dlp import RelationalOperator
from google.cloud.dlp_v2.types.dlp import ResourceVisibility
from google.cloud.dlp_v2.types.dlp import StoredInfoTypeState
from google.cloud.dlp_v2.types.dlp import TransformationContainerType
from google.cloud.dlp_v2.types.dlp import TransformationResultStatusType
from google.cloud.dlp_v2.types.dlp import TransformationType
from google.cloud.dlp_v2.types.dlp import UniquenessScoreLevel
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
from google.cloud.dlp_v2.types.storage import SensitivityScore
from google.cloud.dlp_v2.types.storage import StorageConfig
from google.cloud.dlp_v2.types.storage import StoredType
from google.cloud.dlp_v2.types.storage import TableOptions
from google.cloud.dlp_v2.types.storage import TableReference
from google.cloud.dlp_v2.types.storage import FileType
from google.cloud.dlp_v2.types.storage import Likelihood

__all__ = ('DlpServiceClient',
    'DlpServiceAsyncClient',
    'Action',
    'ActionDetails',
    'ActivateJobTriggerRequest',
    'AllOtherDatabaseResources',
    'AllOtherResources',
    'AmazonS3Bucket',
    'AmazonS3BucketConditions',
    'AmazonS3BucketRegex',
    'AnalyzeDataSourceRiskDetails',
    'AwsAccount',
    'AwsAccountRegex',
    'BigQueryDiscoveryTarget',
    'BigQueryRegex',
    'BigQueryRegexes',
    'BigQueryTableCollection',
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
    'CloudStorageRegex',
    'CloudStorageResourceReference',
    'Color',
    'ColumnDataProfile',
    'Connection',
    'Container',
    'ContentItem',
    'ContentLocation',
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
    'DatabaseResourceCollection',
    'DatabaseResourceReference',
    'DatabaseResourceRegex',
    'DatabaseResourceRegexes',
    'DataProfileAction',
    'DataProfileBigQueryRowSchema',
    'DataProfileConfigSnapshot',
    'DataProfileFinding',
    'DataProfileFindingLocation',
    'DataProfileFindingRecordLocation',
    'DataProfileJobConfig',
    'DataProfileLocation',
    'DataProfilePubSubCondition',
    'DataProfilePubSubMessage',
    'DataRiskLevel',
    'DataSourceType',
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
    'DiscoveryOtherCloudConditions',
    'DiscoveryOtherCloudFilter',
    'DiscoveryOtherCloudGenerationCadence',
    'DiscoverySchemaModifiedCadence',
    'DiscoveryStartingLocation',
    'DiscoveryTableModifiedCadence',
    'DiscoveryTarget',
    'DiscoveryVertexDatasetConditions',
    'DiscoveryVertexDatasetFilter',
    'DiscoveryVertexDatasetGenerationCadence',
    'DlpJob',
    'DocumentLocation',
    'Domain',
    'Error',
    'ExcludeByHotword',
    'ExcludeInfoTypes',
    'ExclusionRule',
    'FieldTransformation',
    'FileClusterSummary',
    'FileClusterType',
    'FileExtensionInfo',
    'FileStoreCollection',
    'FileStoreDataProfile',
    'FileStoreInfoTypeSummary',
    'FileStoreRegex',
    'FileStoreRegexes',
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
    'ImageLocation',
    'ImageTransformations',
    'InfoTypeCategory',
    'InfoTypeDescription',
    'InfoTypeStats',
    'InfoTypeSummary',
    'InfoTypeTransformations',
    'InspectConfig',
    'InspectContentRequest',
    'InspectContentResponse',
    'InspectDataSourceDetails',
    'InspectionRule',
    'InspectionRuleSet',
    'InspectJobConfig',
    'InspectResult',
    'InspectTemplate',
    'JobTrigger',
    'KmsWrappedCryptoKey',
    'LargeCustomDictionaryConfig',
    'LargeCustomDictionaryStats',
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
    'LocationSupport',
    'Manual',
    'MetadataLocation',
    'OtherCloudDiscoveryStartingLocation',
    'OtherCloudDiscoveryTarget',
    'OtherCloudResourceCollection',
    'OtherCloudResourceRegex',
    'OtherCloudResourceRegexes',
    'OtherCloudSingleResourceReference',
    'OtherInfoTypeSummary',
    'OutputStorageConfig',
    'PrimitiveTransformation',
    'PrivacyMetric',
    'ProcessingLocation',
    'ProfileStatus',
    'ProjectDataProfile',
    'QuasiId',
    'QuoteInfo',
    'Range',
    'RecordCondition',
    'RecordLocation',
    'RecordSuppression',
    'RecordTransformation',
    'RecordTransformations',
    'RedactConfig',
    'RedactImageRequest',
    'RedactImageResponse',
    'ReidentifyContentRequest',
    'ReidentifyContentResponse',
    'RelatedResource',
    'ReplaceDictionaryConfig',
    'ReplaceValueConfig',
    'ReplaceWithInfoTypeConfig',
    'RiskAnalysisJobConfig',
    'SaveToGcsFindingsOutput',
    'Schedule',
    'SearchConnectionsRequest',
    'SearchConnectionsResponse',
    'SecretManagerCredential',
    'SecretsDiscoveryTarget',
    'StatisticalTable',
    'StorageMetadataLabel',
    'StoredInfoType',
    'StoredInfoTypeConfig',
    'StoredInfoTypeStats',
    'StoredInfoTypeVersion',
    'Table',
    'TableDataProfile',
    'TableLocation',
    'Tag',
    'TimePartConfig',
    'TransformationConfig',
    'TransformationDescription',
    'TransformationDetails',
    'TransformationDetailsStorageConfig',
    'TransformationErrorHandling',
    'TransformationLocation',
    'TransformationOverview',
    'TransformationResultStatus',
    'TransformationSummary',
    'TransientCryptoKey',
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
    'VertexDatasetCollection',
    'VertexDatasetDiscoveryTarget',
    'VertexDatasetRegex',
    'VertexDatasetRegexes',
    'VertexDatasetResourceReference',
    'BigQuerySchemaModification',
    'BigQueryTableModification',
    'BigQueryTableType',
    'BigQueryTableTypeCollection',
    'ConnectionState',
    'ContentOption',
    'DataProfileUpdateFrequency',
    'DlpJobType',
    'EncryptionStatus',
    'InfoTypeSupportedBy',
    'MatchingType',
    'MetadataType',
    'NullPercentageLevel',
    'ProfileGeneration',
    'RelationalOperator',
    'ResourceVisibility',
    'StoredInfoTypeState',
    'TransformationContainerType',
    'TransformationResultStatusType',
    'TransformationType',
    'UniquenessScoreLevel',
    'BigQueryField',
    'BigQueryKey',
    'BigQueryOptions',
    'BigQueryTable',
    'CloudStorageFileSet',
    'CloudStorageOptions',
    'CloudStoragePath',
    'CloudStorageRegexFileSet',
    'CustomInfoType',
    'DatastoreKey',
    'DatastoreOptions',
    'EntityId',
    'FieldId',
    'HybridOptions',
    'InfoType',
    'Key',
    'KindExpression',
    'PartitionId',
    'RecordKey',
    'SensitivityScore',
    'StorageConfig',
    'StoredType',
    'TableOptions',
    'TableReference',
    'FileType',
    'Likelihood',
)
