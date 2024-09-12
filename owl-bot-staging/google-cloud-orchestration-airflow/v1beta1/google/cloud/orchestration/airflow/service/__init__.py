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
from google.cloud.orchestration.airflow.service import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.orchestration.airflow.service_v1beta1.services.environments.client import EnvironmentsClient
from google.cloud.orchestration.airflow.service_v1beta1.services.environments.async_client import EnvironmentsAsyncClient
from google.cloud.orchestration.airflow.service_v1beta1.services.image_versions.client import ImageVersionsClient
from google.cloud.orchestration.airflow.service_v1beta1.services.image_versions.async_client import ImageVersionsAsyncClient

from google.cloud.orchestration.airflow.service_v1beta1.types.environments import AirflowMetadataRetentionPolicyConfig
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import CheckUpgradeRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import CheckUpgradeResponse
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import CloudDataLineageIntegration
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import CreateEnvironmentRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import CreateUserWorkloadsConfigMapRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import CreateUserWorkloadsSecretRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import DatabaseConfig
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import DatabaseFailoverRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import DatabaseFailoverResponse
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import DataRetentionConfig
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import DeleteEnvironmentRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import DeleteUserWorkloadsConfigMapRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import DeleteUserWorkloadsSecretRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import EncryptionConfig
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import Environment
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import EnvironmentConfig
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import ExecuteAirflowCommandRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import ExecuteAirflowCommandResponse
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import FetchDatabasePropertiesRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import FetchDatabasePropertiesResponse
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import GetEnvironmentRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import GetUserWorkloadsConfigMapRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import GetUserWorkloadsSecretRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import IPAllocationPolicy
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import ListEnvironmentsRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import ListEnvironmentsResponse
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import ListUserWorkloadsConfigMapsRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import ListUserWorkloadsConfigMapsResponse
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import ListUserWorkloadsSecretsRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import ListUserWorkloadsSecretsResponse
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import ListWorkloadsRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import ListWorkloadsResponse
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import LoadSnapshotRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import LoadSnapshotResponse
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import MaintenanceWindow
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import MasterAuthorizedNetworksConfig
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import NetworkingConfig
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import NodeConfig
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import PollAirflowCommandRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import PollAirflowCommandResponse
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import PrivateClusterConfig
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import PrivateEnvironmentConfig
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import RecoveryConfig
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import RestartWebServerRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import SaveSnapshotRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import SaveSnapshotResponse
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import ScheduledSnapshotsConfig
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import SoftwareConfig
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import StopAirflowCommandRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import StopAirflowCommandResponse
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import StorageConfig
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import TaskLogsRetentionConfig
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import UpdateEnvironmentRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import UpdateUserWorkloadsConfigMapRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import UpdateUserWorkloadsSecretRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import UserWorkloadsConfigMap
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import UserWorkloadsSecret
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import WebServerConfig
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import WebServerNetworkAccessControl
from google.cloud.orchestration.airflow.service_v1beta1.types.environments import WorkloadsConfig
from google.cloud.orchestration.airflow.service_v1beta1.types.image_versions import ImageVersion
from google.cloud.orchestration.airflow.service_v1beta1.types.image_versions import ListImageVersionsRequest
from google.cloud.orchestration.airflow.service_v1beta1.types.image_versions import ListImageVersionsResponse
from google.cloud.orchestration.airflow.service_v1beta1.types.operations import OperationMetadata

__all__ = ('EnvironmentsClient',
    'EnvironmentsAsyncClient',
    'ImageVersionsClient',
    'ImageVersionsAsyncClient',
    'AirflowMetadataRetentionPolicyConfig',
    'CheckUpgradeRequest',
    'CheckUpgradeResponse',
    'CloudDataLineageIntegration',
    'CreateEnvironmentRequest',
    'CreateUserWorkloadsConfigMapRequest',
    'CreateUserWorkloadsSecretRequest',
    'DatabaseConfig',
    'DatabaseFailoverRequest',
    'DatabaseFailoverResponse',
    'DataRetentionConfig',
    'DeleteEnvironmentRequest',
    'DeleteUserWorkloadsConfigMapRequest',
    'DeleteUserWorkloadsSecretRequest',
    'EncryptionConfig',
    'Environment',
    'EnvironmentConfig',
    'ExecuteAirflowCommandRequest',
    'ExecuteAirflowCommandResponse',
    'FetchDatabasePropertiesRequest',
    'FetchDatabasePropertiesResponse',
    'GetEnvironmentRequest',
    'GetUserWorkloadsConfigMapRequest',
    'GetUserWorkloadsSecretRequest',
    'IPAllocationPolicy',
    'ListEnvironmentsRequest',
    'ListEnvironmentsResponse',
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
    'ImageVersion',
    'ListImageVersionsRequest',
    'ListImageVersionsResponse',
    'OperationMetadata',
)
