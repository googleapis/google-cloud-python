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
from google.cloud.clouddms import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.clouddms_v1.services.data_migration_service.client import DataMigrationServiceClient
from google.cloud.clouddms_v1.services.data_migration_service.async_client import DataMigrationServiceAsyncClient

from google.cloud.clouddms_v1.types.clouddms import ApplyConversionWorkspaceRequest
from google.cloud.clouddms_v1.types.clouddms import CommitConversionWorkspaceRequest
from google.cloud.clouddms_v1.types.clouddms import ConvertConversionWorkspaceRequest
from google.cloud.clouddms_v1.types.clouddms import CreateConnectionProfileRequest
from google.cloud.clouddms_v1.types.clouddms import CreateConversionWorkspaceRequest
from google.cloud.clouddms_v1.types.clouddms import CreateMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import CreatePrivateConnectionRequest
from google.cloud.clouddms_v1.types.clouddms import DeleteConnectionProfileRequest
from google.cloud.clouddms_v1.types.clouddms import DeleteConversionWorkspaceRequest
from google.cloud.clouddms_v1.types.clouddms import DeleteMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import DeletePrivateConnectionRequest
from google.cloud.clouddms_v1.types.clouddms import DescribeConversionWorkspaceRevisionsRequest
from google.cloud.clouddms_v1.types.clouddms import DescribeConversionWorkspaceRevisionsResponse
from google.cloud.clouddms_v1.types.clouddms import DescribeDatabaseEntitiesRequest
from google.cloud.clouddms_v1.types.clouddms import DescribeDatabaseEntitiesResponse
from google.cloud.clouddms_v1.types.clouddms import FetchStaticIpsRequest
from google.cloud.clouddms_v1.types.clouddms import FetchStaticIpsResponse
from google.cloud.clouddms_v1.types.clouddms import GenerateSshScriptRequest
from google.cloud.clouddms_v1.types.clouddms import GetConnectionProfileRequest
from google.cloud.clouddms_v1.types.clouddms import GetConversionWorkspaceRequest
from google.cloud.clouddms_v1.types.clouddms import GetMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import GetPrivateConnectionRequest
from google.cloud.clouddms_v1.types.clouddms import ImportMappingRulesRequest
from google.cloud.clouddms_v1.types.clouddms import ListConnectionProfilesRequest
from google.cloud.clouddms_v1.types.clouddms import ListConnectionProfilesResponse
from google.cloud.clouddms_v1.types.clouddms import ListConversionWorkspacesRequest
from google.cloud.clouddms_v1.types.clouddms import ListConversionWorkspacesResponse
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
from google.cloud.clouddms_v1.types.clouddms import UpdateConnectionProfileRequest
from google.cloud.clouddms_v1.types.clouddms import UpdateConversionWorkspaceRequest
from google.cloud.clouddms_v1.types.clouddms import UpdateMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import VerifyMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import VmCreationConfig
from google.cloud.clouddms_v1.types.clouddms import VmSelectionConfig
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
from google.cloud.clouddms_v1.types.conversionworkspace_resources import BackgroundJobLogEntry
from google.cloud.clouddms_v1.types.conversionworkspace_resources import ColumnEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import ConstraintEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import ConversionWorkspace
from google.cloud.clouddms_v1.types.conversionworkspace_resources import DatabaseEngineInfo
from google.cloud.clouddms_v1.types.conversionworkspace_resources import DatabaseEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import EntityMapping
from google.cloud.clouddms_v1.types.conversionworkspace_resources import EntityMappingLogEntry
from google.cloud.clouddms_v1.types.conversionworkspace_resources import FunctionEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import IndexEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import PackageEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import SchemaEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import SequenceEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import StoredProcedureEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import SynonymEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import TableEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import TriggerEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import ViewEntity
from google.cloud.clouddms_v1.types.conversionworkspace_resources import BackgroundJobType
from google.cloud.clouddms_v1.types.conversionworkspace_resources import DatabaseEntityType
from google.cloud.clouddms_v1.types.conversionworkspace_resources import ImportRulesFileFormat

__all__ = ('DataMigrationServiceClient',
    'DataMigrationServiceAsyncClient',
    'ApplyConversionWorkspaceRequest',
    'CommitConversionWorkspaceRequest',
    'ConvertConversionWorkspaceRequest',
    'CreateConnectionProfileRequest',
    'CreateConversionWorkspaceRequest',
    'CreateMigrationJobRequest',
    'CreatePrivateConnectionRequest',
    'DeleteConnectionProfileRequest',
    'DeleteConversionWorkspaceRequest',
    'DeleteMigrationJobRequest',
    'DeletePrivateConnectionRequest',
    'DescribeConversionWorkspaceRevisionsRequest',
    'DescribeConversionWorkspaceRevisionsResponse',
    'DescribeDatabaseEntitiesRequest',
    'DescribeDatabaseEntitiesResponse',
    'FetchStaticIpsRequest',
    'FetchStaticIpsResponse',
    'GenerateSshScriptRequest',
    'GetConnectionProfileRequest',
    'GetConversionWorkspaceRequest',
    'GetMigrationJobRequest',
    'GetPrivateConnectionRequest',
    'ImportMappingRulesRequest',
    'ListConnectionProfilesRequest',
    'ListConnectionProfilesResponse',
    'ListConversionWorkspacesRequest',
    'ListConversionWorkspacesResponse',
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
    'UpdateConnectionProfileRequest',
    'UpdateConversionWorkspaceRequest',
    'UpdateMigrationJobRequest',
    'VerifyMigrationJobRequest',
    'VmCreationConfig',
    'VmSelectionConfig',
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
    'BackgroundJobLogEntry',
    'ColumnEntity',
    'ConstraintEntity',
    'ConversionWorkspace',
    'DatabaseEngineInfo',
    'DatabaseEntity',
    'EntityMapping',
    'EntityMappingLogEntry',
    'FunctionEntity',
    'IndexEntity',
    'PackageEntity',
    'SchemaEntity',
    'SequenceEntity',
    'StoredProcedureEntity',
    'SynonymEntity',
    'TableEntity',
    'TriggerEntity',
    'ViewEntity',
    'BackgroundJobType',
    'DatabaseEntityType',
    'ImportRulesFileFormat',
)
