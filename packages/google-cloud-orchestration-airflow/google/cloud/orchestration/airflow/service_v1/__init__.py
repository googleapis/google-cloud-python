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
from google.cloud.orchestration.airflow.service_v1 import (
    gapic_version as package_version,
)

__version__ = package_version.__version__


from .services.environments import EnvironmentsAsyncClient, EnvironmentsClient
from .services.image_versions import ImageVersionsAsyncClient, ImageVersionsClient
from .types.environments import (
    CheckUpgradeResponse,
    CreateEnvironmentRequest,
    DatabaseConfig,
    DatabaseFailoverRequest,
    DatabaseFailoverResponse,
    DeleteEnvironmentRequest,
    EncryptionConfig,
    Environment,
    EnvironmentConfig,
    ExecuteAirflowCommandRequest,
    ExecuteAirflowCommandResponse,
    FetchDatabasePropertiesRequest,
    FetchDatabasePropertiesResponse,
    GetEnvironmentRequest,
    IPAllocationPolicy,
    ListEnvironmentsRequest,
    ListEnvironmentsResponse,
    LoadSnapshotRequest,
    LoadSnapshotResponse,
    MaintenanceWindow,
    MasterAuthorizedNetworksConfig,
    NetworkingConfig,
    NodeConfig,
    PollAirflowCommandRequest,
    PollAirflowCommandResponse,
    PrivateClusterConfig,
    PrivateEnvironmentConfig,
    RecoveryConfig,
    SaveSnapshotRequest,
    SaveSnapshotResponse,
    ScheduledSnapshotsConfig,
    SoftwareConfig,
    StopAirflowCommandRequest,
    StopAirflowCommandResponse,
    UpdateEnvironmentRequest,
    WebServerConfig,
    WebServerNetworkAccessControl,
    WorkloadsConfig,
)
from .types.image_versions import (
    ImageVersion,
    ListImageVersionsRequest,
    ListImageVersionsResponse,
)
from .types.operations import OperationMetadata

__all__ = (
    "EnvironmentsAsyncClient",
    "ImageVersionsAsyncClient",
    "CheckUpgradeResponse",
    "CreateEnvironmentRequest",
    "DatabaseConfig",
    "DatabaseFailoverRequest",
    "DatabaseFailoverResponse",
    "DeleteEnvironmentRequest",
    "EncryptionConfig",
    "Environment",
    "EnvironmentConfig",
    "EnvironmentsClient",
    "ExecuteAirflowCommandRequest",
    "ExecuteAirflowCommandResponse",
    "FetchDatabasePropertiesRequest",
    "FetchDatabasePropertiesResponse",
    "GetEnvironmentRequest",
    "IPAllocationPolicy",
    "ImageVersion",
    "ImageVersionsClient",
    "ListEnvironmentsRequest",
    "ListEnvironmentsResponse",
    "ListImageVersionsRequest",
    "ListImageVersionsResponse",
    "LoadSnapshotRequest",
    "LoadSnapshotResponse",
    "MaintenanceWindow",
    "MasterAuthorizedNetworksConfig",
    "NetworkingConfig",
    "NodeConfig",
    "OperationMetadata",
    "PollAirflowCommandRequest",
    "PollAirflowCommandResponse",
    "PrivateClusterConfig",
    "PrivateEnvironmentConfig",
    "RecoveryConfig",
    "SaveSnapshotRequest",
    "SaveSnapshotResponse",
    "ScheduledSnapshotsConfig",
    "SoftwareConfig",
    "StopAirflowCommandRequest",
    "StopAirflowCommandResponse",
    "UpdateEnvironmentRequest",
    "WebServerConfig",
    "WebServerNetworkAccessControl",
    "WorkloadsConfig",
)
