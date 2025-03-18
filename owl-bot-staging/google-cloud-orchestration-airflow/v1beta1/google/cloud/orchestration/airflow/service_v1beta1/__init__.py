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
from google.cloud.orchestration.airflow.service_v1beta1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.environments import EnvironmentsClient
from .services.environments import EnvironmentsAsyncClient
from .services.image_versions import ImageVersionsClient
from .services.image_versions import ImageVersionsAsyncClient

from .types.environments import AirflowMetadataRetentionPolicyConfig
from .types.environments import CheckUpgradeRequest
from .types.environments import CheckUpgradeResponse
from .types.environments import CloudDataLineageIntegration
from .types.environments import CreateEnvironmentRequest
from .types.environments import CreateUserWorkloadsConfigMapRequest
from .types.environments import CreateUserWorkloadsSecretRequest
from .types.environments import DatabaseConfig
from .types.environments import DatabaseFailoverRequest
from .types.environments import DatabaseFailoverResponse
from .types.environments import DataRetentionConfig
from .types.environments import DeleteEnvironmentRequest
from .types.environments import DeleteUserWorkloadsConfigMapRequest
from .types.environments import DeleteUserWorkloadsSecretRequest
from .types.environments import EncryptionConfig
from .types.environments import Environment
from .types.environments import EnvironmentConfig
from .types.environments import ExecuteAirflowCommandRequest
from .types.environments import ExecuteAirflowCommandResponse
from .types.environments import FetchDatabasePropertiesRequest
from .types.environments import FetchDatabasePropertiesResponse
from .types.environments import GetEnvironmentRequest
from .types.environments import GetUserWorkloadsConfigMapRequest
from .types.environments import GetUserWorkloadsSecretRequest
from .types.environments import IPAllocationPolicy
from .types.environments import ListEnvironmentsRequest
from .types.environments import ListEnvironmentsResponse
from .types.environments import ListUserWorkloadsConfigMapsRequest
from .types.environments import ListUserWorkloadsConfigMapsResponse
from .types.environments import ListUserWorkloadsSecretsRequest
from .types.environments import ListUserWorkloadsSecretsResponse
from .types.environments import ListWorkloadsRequest
from .types.environments import ListWorkloadsResponse
from .types.environments import LoadSnapshotRequest
from .types.environments import LoadSnapshotResponse
from .types.environments import MaintenanceWindow
from .types.environments import MasterAuthorizedNetworksConfig
from .types.environments import NetworkingConfig
from .types.environments import NodeConfig
from .types.environments import PollAirflowCommandRequest
from .types.environments import PollAirflowCommandResponse
from .types.environments import PrivateClusterConfig
from .types.environments import PrivateEnvironmentConfig
from .types.environments import RecoveryConfig
from .types.environments import RestartWebServerRequest
from .types.environments import SaveSnapshotRequest
from .types.environments import SaveSnapshotResponse
from .types.environments import ScheduledSnapshotsConfig
from .types.environments import SoftwareConfig
from .types.environments import StopAirflowCommandRequest
from .types.environments import StopAirflowCommandResponse
from .types.environments import StorageConfig
from .types.environments import TaskLogsRetentionConfig
from .types.environments import UpdateEnvironmentRequest
from .types.environments import UpdateUserWorkloadsConfigMapRequest
from .types.environments import UpdateUserWorkloadsSecretRequest
from .types.environments import UserWorkloadsConfigMap
from .types.environments import UserWorkloadsSecret
from .types.environments import WebServerConfig
from .types.environments import WebServerNetworkAccessControl
from .types.environments import WorkloadsConfig
from .types.image_versions import ImageVersion
from .types.image_versions import ListImageVersionsRequest
from .types.image_versions import ListImageVersionsResponse
from .types.operations import OperationMetadata

__all__ = (
    'EnvironmentsAsyncClient',
    'ImageVersionsAsyncClient',
'AirflowMetadataRetentionPolicyConfig',
'CheckUpgradeRequest',
'CheckUpgradeResponse',
'CloudDataLineageIntegration',
'CreateEnvironmentRequest',
'CreateUserWorkloadsConfigMapRequest',
'CreateUserWorkloadsSecretRequest',
'DataRetentionConfig',
'DatabaseConfig',
'DatabaseFailoverRequest',
'DatabaseFailoverResponse',
'DeleteEnvironmentRequest',
'DeleteUserWorkloadsConfigMapRequest',
'DeleteUserWorkloadsSecretRequest',
'EncryptionConfig',
'Environment',
'EnvironmentConfig',
'EnvironmentsClient',
'ExecuteAirflowCommandRequest',
'ExecuteAirflowCommandResponse',
'FetchDatabasePropertiesRequest',
'FetchDatabasePropertiesResponse',
'GetEnvironmentRequest',
'GetUserWorkloadsConfigMapRequest',
'GetUserWorkloadsSecretRequest',
'IPAllocationPolicy',
'ImageVersion',
'ImageVersionsClient',
'ListEnvironmentsRequest',
'ListEnvironmentsResponse',
'ListImageVersionsRequest',
'ListImageVersionsResponse',
'ListUserWorkloadsConfigMapsRequest',
'ListUserWorkloadsConfigMapsResponse',
'ListUserWorkloadsSecretsRequest',
'ListUserWorkloadsSecretsResponse',
'ListWorkloadsRequest',
'ListWorkloadsResponse',
'LoadSnapshotRequest',
'LoadSnapshotResponse',
'MaintenanceWindow',
'MasterAuthorizedNetworksConfig',
'NetworkingConfig',
'NodeConfig',
'OperationMetadata',
'PollAirflowCommandRequest',
'PollAirflowCommandResponse',
'PrivateClusterConfig',
'PrivateEnvironmentConfig',
'RecoveryConfig',
'RestartWebServerRequest',
'SaveSnapshotRequest',
'SaveSnapshotResponse',
'ScheduledSnapshotsConfig',
'SoftwareConfig',
'StopAirflowCommandRequest',
'StopAirflowCommandResponse',
'StorageConfig',
'TaskLogsRetentionConfig',
'UpdateEnvironmentRequest',
'UpdateUserWorkloadsConfigMapRequest',
'UpdateUserWorkloadsSecretRequest',
'UserWorkloadsConfigMap',
'UserWorkloadsSecret',
'WebServerConfig',
'WebServerNetworkAccessControl',
'WorkloadsConfig',
)
