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
from google.cloud.bigquery_connection import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.bigquery_connection_v1.services.connection_service.client import ConnectionServiceClient
from google.cloud.bigquery_connection_v1.services.connection_service.async_client import ConnectionServiceAsyncClient

from google.cloud.bigquery_connection_v1.types.connection import AwsAccessRole
from google.cloud.bigquery_connection_v1.types.connection import AwsCrossAccountRole
from google.cloud.bigquery_connection_v1.types.connection import AwsProperties
from google.cloud.bigquery_connection_v1.types.connection import AzureProperties
from google.cloud.bigquery_connection_v1.types.connection import CloudResourceProperties
from google.cloud.bigquery_connection_v1.types.connection import CloudSpannerProperties
from google.cloud.bigquery_connection_v1.types.connection import CloudSqlCredential
from google.cloud.bigquery_connection_v1.types.connection import CloudSqlProperties
from google.cloud.bigquery_connection_v1.types.connection import Connection
from google.cloud.bigquery_connection_v1.types.connection import CreateConnectionRequest
from google.cloud.bigquery_connection_v1.types.connection import DeleteConnectionRequest
from google.cloud.bigquery_connection_v1.types.connection import GetConnectionRequest
from google.cloud.bigquery_connection_v1.types.connection import ListConnectionsRequest
from google.cloud.bigquery_connection_v1.types.connection import ListConnectionsResponse
from google.cloud.bigquery_connection_v1.types.connection import MetastoreServiceConfig
from google.cloud.bigquery_connection_v1.types.connection import SalesforceDataCloudProperties
from google.cloud.bigquery_connection_v1.types.connection import SparkHistoryServerConfig
from google.cloud.bigquery_connection_v1.types.connection import SparkProperties
from google.cloud.bigquery_connection_v1.types.connection import UpdateConnectionRequest

__all__ = ('ConnectionServiceClient',
    'ConnectionServiceAsyncClient',
    'AwsAccessRole',
    'AwsCrossAccountRole',
    'AwsProperties',
    'AzureProperties',
    'CloudResourceProperties',
    'CloudSpannerProperties',
    'CloudSqlCredential',
    'CloudSqlProperties',
    'Connection',
    'CreateConnectionRequest',
    'DeleteConnectionRequest',
    'GetConnectionRequest',
    'ListConnectionsRequest',
    'ListConnectionsResponse',
    'MetastoreServiceConfig',
    'SalesforceDataCloudProperties',
    'SparkHistoryServerConfig',
    'SparkProperties',
    'UpdateConnectionRequest',
)
