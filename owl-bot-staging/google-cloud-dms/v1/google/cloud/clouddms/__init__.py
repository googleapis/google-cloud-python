# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.cloud.clouddms import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.clouddms_v1.services.data_migration_service.client import DataMigrationServiceClient
from google.cloud.clouddms_v1.services.data_migration_service.async_client import DataMigrationServiceAsyncClient

from google.cloud.clouddms_v1.types.clouddms import ApplyConversionWorkspaceRequest
from google.cloud.clouddms_v1.types.clouddms import CommitConversionWorkspaceRequest
from google.cloud.clouddms_v1.types.clouddms import ConvertConversionWorkspaceRequest
from google.cloud.clouddms_v1.types.clouddms import CreateConnectionProfileRequest
from google.cloud.clouddms_v1.types.clouddms import CreateConversionWorkspaceRequest
from google.cloud.clouddms_v1.types.clouddms import CreateMappingRuleRequest
from google.cloud.clouddms_v1.types.clouddms import CreateMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import CreatePrivateConnectionRequest
from google.cloud.clouddms_v1.types.clouddms import DeleteConnectionProfileRequest
from google.cloud.clouddms_v1.types.clouddms import DeleteConversionWorkspaceRequest
from google.cloud.clouddms_v1.types.clouddms import DeleteMappingRuleRequest
from google.cloud.clouddms_v1.types.clouddms import DeleteMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import DeletePrivateConnectionRequest
from google.cloud.clouddms_v1.types.clouddms import DescribeConversionWorkspaceRevisionsRequest
from google.cloud.clouddms_v1.types.clouddms import DescribeConversionWorkspaceRevisionsResponse
from google.cloud.clouddms_v1.types.clouddms import DescribeDatabaseEntitiesRequest
from google.cloud.clouddms_v1.types.clouddms import DescribeDatabaseEntitiesResponse
from google.cloud.clouddms_v1.types.clouddms import FetchStaticIpsRequest
from google.cloud.clouddms_v1.types.clouddms import FetchStaticIpsResponse
from google.cloud.clouddms_v1.types.clouddms import GenerateSshScriptRequest
from google.cloud.clouddms_v1.types.clouddms import GenerateTcpProxyScriptRequest
from google.cloud.clouddms_v1.types.clouddms import GetConnectionProfileRequest
from google.cloud.clouddms_v1.types.clouddms import GetConversionWorkspaceRequest
from google.cloud.clouddms_v1.types.clouddms import GetMappingRuleRequest
from google.cloud.clouddms_v1.types.clouddms import GetMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import GetPrivateConnectionRequest
from google.cloud.clouddms_v1.types.clouddms import ImportMappingRulesRequest
from google.cloud.clouddms_v1.types.clouddms import ListConnectionProfilesRequest
from google.cloud.clouddms_v1.types.clouddms import ListConnectionProfilesResponse
from google.cloud.clouddms_v1.types.clouddms import ListConversionWorkspacesRequest
from google.cloud.clouddms_v1.types.clouddms import ListConversionWorkspacesResponse
from google.cloud.clouddms_v1.types.clouddms import ListMappingRulesRequest
from google.cloud.clouddms_v1.types.clouddms import ListMappingRulesResponse
from google.cloud.clouddms_v1.types.clouddms import ListMigrationJobsRequest
from google.cloud.clouddms_v1.types.clouddms import ListMigrationJobsResponse
from google.cloud.clouddms_v1.types.clouddms import ListPrivateConnectionsRequest
from google.cloud.clouddms_v1.types.clouddms import ListPrivateConnectionsResponse
from google.cloud.clouddms_v1.types.clouddms import OperationMetadata
from google.cloud.clouddms_v1.types.clouddms import PromoteMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import RestartMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import ResumeMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import RollbackConversionWorkspaceRequest
from google.cloud.clouddms_v1.types.clouddms import SearchBackgroundJobsRequest
from google.cloud.clouddms_v1.types.clouddms import SearchBackgroundJobsResponse
from google.cloud.clouddms_v1.types.clouddms import SeedConversionWorkspaceRequest
from google.cloud.clouddms_v1.types.clouddms import SshScript
from google.cloud.clouddms_v1.types.clouddms import StartMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import StopMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import TcpProxyScript
from google.cloud.clouddms_v1.types.clouddms import UpdateConnectionProfileRequest
from google.cloud.clouddms_v1.types.clouddms import UpdateConversionWorkspaceRequest
from google.cloud.clouddms_v1.types.clouddms import UpdateMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import VerifyMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import VmCreationConfig
from google.cloud.clouddms_v1.types.clouddms import VmSelectionConfig
from google.cloud.clouddms_v1.types.clouddms import DatabaseEntityView
from google.cloud.clouddms_v1.types.clouddms_resources import AlloyDbConnectionProfile
from google.cloud.clouddms_v1.types.clouddms_resources import AlloyDbSettings
from google.cloud.clouddms_v1.types.clouddms_resources import CloudSqlConnectionProfile
from google.cloud.clouddms_v1.types.clouddms_resources import CloudSqlSettings
from google.cloud.clouddms_v1.types.clouddms_resources import ConnectionProfile
from google.cloud.clouddms_v1.types.clouddms_resources import ConversionWorkspaceInfo
from google.cloud.clouddms_v1.types.clouddms_resources import DatabaseType
from google.cloud.clouddms_v1.types.clouddms_resources import ForwardSshTunnelConnectivity
from google.cloud.clouddms_v1.types.clouddms_resources import MigrationJob
from google.cloud.clouddms_v1.types.clouddms_resources import MigrationJobVerificationError
from google.cloud.clouddms_v1.types.clouddms_resources import MySqlConnectionProfile
from google.cloud.clouddms_v1.types.clouddms_resources import OracleConnectionProfile
from google.cloud.clouddms_v1.types.clouddms_resources import PostgreSqlConnectionProfile
from google.cloud.clouddms_v1.types.clouddms_resources import PrivateConnection
from google.cloud.clouddms_v1.types.clouddms_resources import PrivateConnectivity
from google.cloud.clouddms_v1.types.clouddms_resources import PrivateServiceConnectConnectivity
from google.cloud.clouddms_v1.types.clouddms_resources import ReverseSshConnectivity
from google.cloud.clouddms_v1.types.clouddms_resources import SqlAclEntry
from google.cloud.clouddms_v1.types.clouddms_resources import SqlIpConfig
from google.cloud.clouddms_v1.types.clouddms_resources import SslConfig
from google.cloud.clouddms_v1.types.clouddms_resources import StaticIpConnectivity
from google.cloud.clouddms_v1.types.clouddms_resources import StaticServiceIpConnectivity
from google.cloud.clouddms_v1.types.clouddms_resources import VpcPeeringConfig
from google.cloud.clouddms_v1.types.clouddms_resources import VpcPeeringConnectivity
from google.cloud.clouddms_v1.types.clouddms_resources import DatabaseEngine
from google.cloud.clouddms_v1.types.clouddms_resources import DatabaseProvider
from google.cloud.clouddms_v1.types.clouddms_resources import NetworkArchitecture
from google.cloud.clouddms_v1.types.conversionworkspace_resources import ApplyHash
from google.cloud.clouddms_v1.types.conversionworkspace_resources import AssignSpecificValue
from google.cloud.clouddms_v1.types.conversionworkspace_resources import BackgroundJobLogEntry
from google.cloud.clouddms_v1.types.conversionworkspace_resources import ColumnEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import ConditionalColumnSetValue
from google.cloud.clouddms_v1.types.conversionworkspace_resources import ConstraintEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import ConversionWorkspace
from google.cloud.clouddms_v1.types.conversionworkspace_resources import ConvertRowIdToColumn
from google.cloud.clouddms_v1.types.conversionworkspace_resources import DatabaseEngineInfo
from google.cloud.clouddms_v1.types.conversionworkspace_resources import DatabaseEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import DatabaseInstanceEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import DoubleComparisonFilter
from google.cloud.clouddms_v1.types.conversionworkspace_resources import EntityDdl
from google.cloud.clouddms_v1.types.conversionworkspace_resources import EntityIssue
from google.cloud.clouddms_v1.types.conversionworkspace_resources import EntityMapping
from google.cloud.clouddms_v1.types.conversionworkspace_resources import EntityMappingLogEntry
from google.cloud.clouddms_v1.types.conversionworkspace_resources import EntityMove
from google.cloud.clouddms_v1.types.conversionworkspace_resources import FilterTableColumns
from google.cloud.clouddms_v1.types.conversionworkspace_resources import FunctionEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import IndexEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import IntComparisonFilter
from google.cloud.clouddms_v1.types.conversionworkspace_resources import MappingRule
from google.cloud.clouddms_v1.types.conversionworkspace_resources import MappingRuleFilter
from google.cloud.clouddms_v1.types.conversionworkspace_resources import MaterializedViewEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import MultiColumnDatatypeChange
from google.cloud.clouddms_v1.types.conversionworkspace_resources import MultiEntityRename
from google.cloud.clouddms_v1.types.conversionworkspace_resources import PackageEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import RoundToScale
from google.cloud.clouddms_v1.types.conversionworkspace_resources import SchemaEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import SequenceEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import SetTablePrimaryKey
from google.cloud.clouddms_v1.types.conversionworkspace_resources import SingleColumnChange
from google.cloud.clouddms_v1.types.conversionworkspace_resources import SingleEntityRename
from google.cloud.clouddms_v1.types.conversionworkspace_resources import SinglePackageChange
from google.cloud.clouddms_v1.types.conversionworkspace_resources import SourceNumericFilter
from google.cloud.clouddms_v1.types.conversionworkspace_resources import SourceSqlChange
from google.cloud.clouddms_v1.types.conversionworkspace_resources import SourceTextFilter
from google.cloud.clouddms_v1.types.conversionworkspace_resources import StoredProcedureEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import SynonymEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import TableEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import TriggerEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import UDTEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import ValueListFilter
from google.cloud.clouddms_v1.types.conversionworkspace_resources import ValueTransformation
from google.cloud.clouddms_v1.types.conversionworkspace_resources import ViewEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import BackgroundJobType
from google.cloud.clouddms_v1.types.conversionworkspace_resources import DatabaseEntityType
from google.cloud.clouddms_v1.types.conversionworkspace_resources import EntityNameTransformation
from google.cloud.clouddms_v1.types.conversionworkspace_resources import ImportRulesFileFormat
from google.cloud.clouddms_v1.types.conversionworkspace_resources import NumericFilterOption
from google.cloud.clouddms_v1.types.conversionworkspace_resources import ValueComparison
from google.cloud.clouddms_v1.types.conversionworkspace_resources import ValuePresentInList

__all__ = ('DataMigrationServiceClient',
    'DataMigrationServiceAsyncClient',
    'ApplyConversionWorkspaceRequest',
    'CommitConversionWorkspaceRequest',
    'ConvertConversionWorkspaceRequest',
    'CreateConnectionProfileRequest',
    'CreateConversionWorkspaceRequest',
    'CreateMappingRuleRequest',
    'CreateMigrationJobRequest',
    'CreatePrivateConnectionRequest',
    'DeleteConnectionProfileRequest',
    'DeleteConversionWorkspaceRequest',
    'DeleteMappingRuleRequest',
    'DeleteMigrationJobRequest',
    'DeletePrivateConnectionRequest',
    'DescribeConversionWorkspaceRevisionsRequest',
    'DescribeConversionWorkspaceRevisionsResponse',
    'DescribeDatabaseEntitiesRequest',
    'DescribeDatabaseEntitiesResponse',
    'FetchStaticIpsRequest',
    'FetchStaticIpsResponse',
    'GenerateSshScriptRequest',
    'GenerateTcpProxyScriptRequest',
    'GetConnectionProfileRequest',
    'GetConversionWorkspaceRequest',
    'GetMappingRuleRequest',
    'GetMigrationJobRequest',
    'GetPrivateConnectionRequest',
    'ImportMappingRulesRequest',
    'ListConnectionProfilesRequest',
    'ListConnectionProfilesResponse',
    'ListConversionWorkspacesRequest',
    'ListConversionWorkspacesResponse',
    'ListMappingRulesRequest',
    'ListMappingRulesResponse',
    'ListMigrationJobsRequest',
    'ListMigrationJobsResponse',
    'ListPrivateConnectionsRequest',
    'ListPrivateConnectionsResponse',
    'OperationMetadata',
    'PromoteMigrationJobRequest',
    'RestartMigrationJobRequest',
    'ResumeMigrationJobRequest',
    'RollbackConversionWorkspaceRequest',
    'SearchBackgroundJobsRequest',
    'SearchBackgroundJobsResponse',
    'SeedConversionWorkspaceRequest',
    'SshScript',
    'StartMigrationJobRequest',
    'StopMigrationJobRequest',
    'TcpProxyScript',
    'UpdateConnectionProfileRequest',
    'UpdateConversionWorkspaceRequest',
    'UpdateMigrationJobRequest',
    'VerifyMigrationJobRequest',
    'VmCreationConfig',
    'VmSelectionConfig',
    'DatabaseEntityView',
    'AlloyDbConnectionProfile',
    'AlloyDbSettings',
    'CloudSqlConnectionProfile',
    'CloudSqlSettings',
    'ConnectionProfile',
    'ConversionWorkspaceInfo',
    'DatabaseType',
    'ForwardSshTunnelConnectivity',
    'MigrationJob',
    'MigrationJobVerificationError',
    'MySqlConnectionProfile',
    'OracleConnectionProfile',
    'PostgreSqlConnectionProfile',
    'PrivateConnection',
    'PrivateConnectivity',
    'PrivateServiceConnectConnectivity',
    'ReverseSshConnectivity',
    'SqlAclEntry',
    'SqlIpConfig',
    'SslConfig',
    'StaticIpConnectivity',
    'StaticServiceIpConnectivity',
    'VpcPeeringConfig',
    'VpcPeeringConnectivity',
    'DatabaseEngine',
    'DatabaseProvider',
    'NetworkArchitecture',
    'ApplyHash',
    'AssignSpecificValue',
    'BackgroundJobLogEntry',
    'ColumnEntity',
    'ConditionalColumnSetValue',
    'ConstraintEntity',
    'ConversionWorkspace',
    'ConvertRowIdToColumn',
    'DatabaseEngineInfo',
    'DatabaseEntity',
    'DatabaseInstanceEntity',
    'DoubleComparisonFilter',
    'EntityDdl',
    'EntityIssue',
    'EntityMapping',
    'EntityMappingLogEntry',
    'EntityMove',
    'FilterTableColumns',
    'FunctionEntity',
    'IndexEntity',
    'IntComparisonFilter',
    'MappingRule',
    'MappingRuleFilter',
    'MaterializedViewEntity',
    'MultiColumnDatatypeChange',
    'MultiEntityRename',
    'PackageEntity',
    'RoundToScale',
    'SchemaEntity',
    'SequenceEntity',
    'SetTablePrimaryKey',
    'SingleColumnChange',
    'SingleEntityRename',
    'SinglePackageChange',
    'SourceNumericFilter',
    'SourceSqlChange',
    'SourceTextFilter',
    'StoredProcedureEntity',
    'SynonymEntity',
    'TableEntity',
    'TriggerEntity',
    'UDTEntity',
    'ValueListFilter',
    'ValueTransformation',
    'ViewEntity',
    'BackgroundJobType',
    'DatabaseEntityType',
    'EntityNameTransformation',
    'ImportRulesFileFormat',
    'NumericFilterOption',
    'ValueComparison',
    'ValuePresentInList',
)
