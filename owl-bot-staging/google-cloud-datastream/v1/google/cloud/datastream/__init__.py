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
from google.cloud.datastream import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.datastream_v1.services.datastream.client import DatastreamClient
from google.cloud.datastream_v1.services.datastream.async_client import DatastreamAsyncClient

from google.cloud.datastream_v1.types.datastream import CreateConnectionProfileRequest
from google.cloud.datastream_v1.types.datastream import CreatePrivateConnectionRequest
from google.cloud.datastream_v1.types.datastream import CreateRouteRequest
from google.cloud.datastream_v1.types.datastream import CreateStreamRequest
from google.cloud.datastream_v1.types.datastream import DeleteConnectionProfileRequest
from google.cloud.datastream_v1.types.datastream import DeletePrivateConnectionRequest
from google.cloud.datastream_v1.types.datastream import DeleteRouteRequest
from google.cloud.datastream_v1.types.datastream import DeleteStreamRequest
from google.cloud.datastream_v1.types.datastream import DiscoverConnectionProfileRequest
from google.cloud.datastream_v1.types.datastream import DiscoverConnectionProfileResponse
from google.cloud.datastream_v1.types.datastream import FetchStaticIpsRequest
from google.cloud.datastream_v1.types.datastream import FetchStaticIpsResponse
from google.cloud.datastream_v1.types.datastream import GetConnectionProfileRequest
from google.cloud.datastream_v1.types.datastream import GetPrivateConnectionRequest
from google.cloud.datastream_v1.types.datastream import GetRouteRequest
from google.cloud.datastream_v1.types.datastream import GetStreamObjectRequest
from google.cloud.datastream_v1.types.datastream import GetStreamRequest
from google.cloud.datastream_v1.types.datastream import ListConnectionProfilesRequest
from google.cloud.datastream_v1.types.datastream import ListConnectionProfilesResponse
from google.cloud.datastream_v1.types.datastream import ListPrivateConnectionsRequest
from google.cloud.datastream_v1.types.datastream import ListPrivateConnectionsResponse
from google.cloud.datastream_v1.types.datastream import ListRoutesRequest
from google.cloud.datastream_v1.types.datastream import ListRoutesResponse
from google.cloud.datastream_v1.types.datastream import ListStreamObjectsRequest
from google.cloud.datastream_v1.types.datastream import ListStreamObjectsResponse
from google.cloud.datastream_v1.types.datastream import ListStreamsRequest
from google.cloud.datastream_v1.types.datastream import ListStreamsResponse
from google.cloud.datastream_v1.types.datastream import LookupStreamObjectRequest
from google.cloud.datastream_v1.types.datastream import OperationMetadata
from google.cloud.datastream_v1.types.datastream import RunStreamRequest
from google.cloud.datastream_v1.types.datastream import StartBackfillJobRequest
from google.cloud.datastream_v1.types.datastream import StartBackfillJobResponse
from google.cloud.datastream_v1.types.datastream import StopBackfillJobRequest
from google.cloud.datastream_v1.types.datastream import StopBackfillJobResponse
from google.cloud.datastream_v1.types.datastream import UpdateConnectionProfileRequest
from google.cloud.datastream_v1.types.datastream import UpdateStreamRequest
from google.cloud.datastream_v1.types.datastream_resources import AvroFileFormat
from google.cloud.datastream_v1.types.datastream_resources import BackfillJob
from google.cloud.datastream_v1.types.datastream_resources import BigQueryDestinationConfig
from google.cloud.datastream_v1.types.datastream_resources import BigQueryProfile
from google.cloud.datastream_v1.types.datastream_resources import CdcStrategy
from google.cloud.datastream_v1.types.datastream_resources import ConnectionProfile
from google.cloud.datastream_v1.types.datastream_resources import DestinationConfig
from google.cloud.datastream_v1.types.datastream_resources import Error
from google.cloud.datastream_v1.types.datastream_resources import ForwardSshTunnelConnectivity
from google.cloud.datastream_v1.types.datastream_resources import GcsDestinationConfig
from google.cloud.datastream_v1.types.datastream_resources import GcsProfile
from google.cloud.datastream_v1.types.datastream_resources import HostAddress
from google.cloud.datastream_v1.types.datastream_resources import JsonFileFormat
from google.cloud.datastream_v1.types.datastream_resources import MongodbCluster
from google.cloud.datastream_v1.types.datastream_resources import MongodbCollection
from google.cloud.datastream_v1.types.datastream_resources import MongodbDatabase
from google.cloud.datastream_v1.types.datastream_resources import MongodbField
from google.cloud.datastream_v1.types.datastream_resources import MongodbProfile
from google.cloud.datastream_v1.types.datastream_resources import MongodbSourceConfig
from google.cloud.datastream_v1.types.datastream_resources import MongodbSslConfig
from google.cloud.datastream_v1.types.datastream_resources import MysqlColumn
from google.cloud.datastream_v1.types.datastream_resources import MysqlDatabase
from google.cloud.datastream_v1.types.datastream_resources import MysqlGtidPosition
from google.cloud.datastream_v1.types.datastream_resources import MysqlLogPosition
from google.cloud.datastream_v1.types.datastream_resources import MysqlProfile
from google.cloud.datastream_v1.types.datastream_resources import MysqlRdbms
from google.cloud.datastream_v1.types.datastream_resources import MysqlSourceConfig
from google.cloud.datastream_v1.types.datastream_resources import MysqlSslConfig
from google.cloud.datastream_v1.types.datastream_resources import MysqlTable
from google.cloud.datastream_v1.types.datastream_resources import OracleAsmConfig
from google.cloud.datastream_v1.types.datastream_resources import OracleColumn
from google.cloud.datastream_v1.types.datastream_resources import OracleProfile
from google.cloud.datastream_v1.types.datastream_resources import OracleRdbms
from google.cloud.datastream_v1.types.datastream_resources import OracleSchema
from google.cloud.datastream_v1.types.datastream_resources import OracleScnPosition
from google.cloud.datastream_v1.types.datastream_resources import OracleSourceConfig
from google.cloud.datastream_v1.types.datastream_resources import OracleSslConfig
from google.cloud.datastream_v1.types.datastream_resources import OracleTable
from google.cloud.datastream_v1.types.datastream_resources import PostgresqlColumn
from google.cloud.datastream_v1.types.datastream_resources import PostgresqlProfile
from google.cloud.datastream_v1.types.datastream_resources import PostgresqlRdbms
from google.cloud.datastream_v1.types.datastream_resources import PostgresqlSchema
from google.cloud.datastream_v1.types.datastream_resources import PostgresqlSourceConfig
from google.cloud.datastream_v1.types.datastream_resources import PostgresqlSslConfig
from google.cloud.datastream_v1.types.datastream_resources import PostgresqlTable
from google.cloud.datastream_v1.types.datastream_resources import PrivateConnection
from google.cloud.datastream_v1.types.datastream_resources import PrivateConnectivity
from google.cloud.datastream_v1.types.datastream_resources import PscInterfaceConfig
from google.cloud.datastream_v1.types.datastream_resources import Route
from google.cloud.datastream_v1.types.datastream_resources import SalesforceField
from google.cloud.datastream_v1.types.datastream_resources import SalesforceObject
from google.cloud.datastream_v1.types.datastream_resources import SalesforceOrg
from google.cloud.datastream_v1.types.datastream_resources import SalesforceProfile
from google.cloud.datastream_v1.types.datastream_resources import SalesforceSourceConfig
from google.cloud.datastream_v1.types.datastream_resources import SourceConfig
from google.cloud.datastream_v1.types.datastream_resources import SourceObjectIdentifier
from google.cloud.datastream_v1.types.datastream_resources import SqlServerChangeTables
from google.cloud.datastream_v1.types.datastream_resources import SqlServerColumn
from google.cloud.datastream_v1.types.datastream_resources import SqlServerLsnPosition
from google.cloud.datastream_v1.types.datastream_resources import SqlServerProfile
from google.cloud.datastream_v1.types.datastream_resources import SqlServerRdbms
from google.cloud.datastream_v1.types.datastream_resources import SqlServerSchema
from google.cloud.datastream_v1.types.datastream_resources import SqlServerSourceConfig
from google.cloud.datastream_v1.types.datastream_resources import SqlServerTable
from google.cloud.datastream_v1.types.datastream_resources import SqlServerTransactionLogs
from google.cloud.datastream_v1.types.datastream_resources import SrvConnectionFormat
from google.cloud.datastream_v1.types.datastream_resources import StandardConnectionFormat
from google.cloud.datastream_v1.types.datastream_resources import StaticServiceIpConnectivity
from google.cloud.datastream_v1.types.datastream_resources import Stream
from google.cloud.datastream_v1.types.datastream_resources import StreamObject
from google.cloud.datastream_v1.types.datastream_resources import Validation
from google.cloud.datastream_v1.types.datastream_resources import ValidationMessage
from google.cloud.datastream_v1.types.datastream_resources import ValidationResult
from google.cloud.datastream_v1.types.datastream_resources import VpcPeeringConfig

__all__ = ('DatastreamClient',
    'DatastreamAsyncClient',
    'CreateConnectionProfileRequest',
    'CreatePrivateConnectionRequest',
    'CreateRouteRequest',
    'CreateStreamRequest',
    'DeleteConnectionProfileRequest',
    'DeletePrivateConnectionRequest',
    'DeleteRouteRequest',
    'DeleteStreamRequest',
    'DiscoverConnectionProfileRequest',
    'DiscoverConnectionProfileResponse',
    'FetchStaticIpsRequest',
    'FetchStaticIpsResponse',
    'GetConnectionProfileRequest',
    'GetPrivateConnectionRequest',
    'GetRouteRequest',
    'GetStreamObjectRequest',
    'GetStreamRequest',
    'ListConnectionProfilesRequest',
    'ListConnectionProfilesResponse',
    'ListPrivateConnectionsRequest',
    'ListPrivateConnectionsResponse',
    'ListRoutesRequest',
    'ListRoutesResponse',
    'ListStreamObjectsRequest',
    'ListStreamObjectsResponse',
    'ListStreamsRequest',
    'ListStreamsResponse',
    'LookupStreamObjectRequest',
    'OperationMetadata',
    'RunStreamRequest',
    'StartBackfillJobRequest',
    'StartBackfillJobResponse',
    'StopBackfillJobRequest',
    'StopBackfillJobResponse',
    'UpdateConnectionProfileRequest',
    'UpdateStreamRequest',
    'AvroFileFormat',
    'BackfillJob',
    'BigQueryDestinationConfig',
    'BigQueryProfile',
    'CdcStrategy',
    'ConnectionProfile',
    'DestinationConfig',
    'Error',
    'ForwardSshTunnelConnectivity',
    'GcsDestinationConfig',
    'GcsProfile',
    'HostAddress',
    'JsonFileFormat',
    'MongodbCluster',
    'MongodbCollection',
    'MongodbDatabase',
    'MongodbField',
    'MongodbProfile',
    'MongodbSourceConfig',
    'MongodbSslConfig',
    'MysqlColumn',
    'MysqlDatabase',
    'MysqlGtidPosition',
    'MysqlLogPosition',
    'MysqlProfile',
    'MysqlRdbms',
    'MysqlSourceConfig',
    'MysqlSslConfig',
    'MysqlTable',
    'OracleAsmConfig',
    'OracleColumn',
    'OracleProfile',
    'OracleRdbms',
    'OracleSchema',
    'OracleScnPosition',
    'OracleSourceConfig',
    'OracleSslConfig',
    'OracleTable',
    'PostgresqlColumn',
    'PostgresqlProfile',
    'PostgresqlRdbms',
    'PostgresqlSchema',
    'PostgresqlSourceConfig',
    'PostgresqlSslConfig',
    'PostgresqlTable',
    'PrivateConnection',
    'PrivateConnectivity',
    'PscInterfaceConfig',
    'Route',
    'SalesforceField',
    'SalesforceObject',
    'SalesforceOrg',
    'SalesforceProfile',
    'SalesforceSourceConfig',
    'SourceConfig',
    'SourceObjectIdentifier',
    'SqlServerChangeTables',
    'SqlServerColumn',
    'SqlServerLsnPosition',
    'SqlServerProfile',
    'SqlServerRdbms',
    'SqlServerSchema',
    'SqlServerSourceConfig',
    'SqlServerTable',
    'SqlServerTransactionLogs',
    'SrvConnectionFormat',
    'StandardConnectionFormat',
    'StaticServiceIpConnectivity',
    'Stream',
    'StreamObject',
    'Validation',
    'ValidationMessage',
    'ValidationResult',
    'VpcPeeringConfig',
)
