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
from google.cloud.managedkafka_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.managed_kafka import ManagedKafkaAsyncClient, ManagedKafkaClient
from .services.managed_kafka_connect import (
    ManagedKafkaConnectAsyncClient,
    ManagedKafkaConnectClient,
)
from .types.managed_kafka import (
    CreateClusterRequest,
    CreateTopicRequest,
    DeleteClusterRequest,
    DeleteConsumerGroupRequest,
    DeleteTopicRequest,
    GetClusterRequest,
    GetConsumerGroupRequest,
    GetTopicRequest,
    ListClustersRequest,
    ListClustersResponse,
    ListConsumerGroupsRequest,
    ListConsumerGroupsResponse,
    ListTopicsRequest,
    ListTopicsResponse,
    UpdateClusterRequest,
    UpdateConsumerGroupRequest,
    UpdateTopicRequest,
)
from .types.managed_kafka_connect import (
    CreateConnectClusterRequest,
    CreateConnectorRequest,
    DeleteConnectClusterRequest,
    DeleteConnectorRequest,
    GetConnectClusterRequest,
    GetConnectorRequest,
    ListConnectClustersRequest,
    ListConnectClustersResponse,
    ListConnectorsRequest,
    ListConnectorsResponse,
    PauseConnectorRequest,
    PauseConnectorResponse,
    RestartConnectorRequest,
    RestartConnectorResponse,
    ResumeConnectorRequest,
    ResumeConnectorResponse,
    StopConnectorRequest,
    StopConnectorResponse,
    UpdateConnectClusterRequest,
    UpdateConnectorRequest,
)
from .types.resources import (
    AccessConfig,
    CapacityConfig,
    Cluster,
    ConnectAccessConfig,
    ConnectCluster,
    ConnectGcpConfig,
    ConnectNetworkConfig,
    Connector,
    ConsumerGroup,
    ConsumerPartitionMetadata,
    ConsumerTopicMetadata,
    GcpConfig,
    NetworkConfig,
    OperationMetadata,
    RebalanceConfig,
    TaskRetryPolicy,
    Topic,
)

__all__ = (
    "ManagedKafkaAsyncClient",
    "ManagedKafkaConnectAsyncClient",
    "AccessConfig",
    "CapacityConfig",
    "Cluster",
    "ConnectAccessConfig",
    "ConnectCluster",
    "ConnectGcpConfig",
    "ConnectNetworkConfig",
    "Connector",
    "ConsumerGroup",
    "ConsumerPartitionMetadata",
    "ConsumerTopicMetadata",
    "CreateClusterRequest",
    "CreateConnectClusterRequest",
    "CreateConnectorRequest",
    "CreateTopicRequest",
    "DeleteClusterRequest",
    "DeleteConnectClusterRequest",
    "DeleteConnectorRequest",
    "DeleteConsumerGroupRequest",
    "DeleteTopicRequest",
    "GcpConfig",
    "GetClusterRequest",
    "GetConnectClusterRequest",
    "GetConnectorRequest",
    "GetConsumerGroupRequest",
    "GetTopicRequest",
    "ListClustersRequest",
    "ListClustersResponse",
    "ListConnectClustersRequest",
    "ListConnectClustersResponse",
    "ListConnectorsRequest",
    "ListConnectorsResponse",
    "ListConsumerGroupsRequest",
    "ListConsumerGroupsResponse",
    "ListTopicsRequest",
    "ListTopicsResponse",
    "ManagedKafkaClient",
    "ManagedKafkaConnectClient",
    "NetworkConfig",
    "OperationMetadata",
    "PauseConnectorRequest",
    "PauseConnectorResponse",
    "RebalanceConfig",
    "RestartConnectorRequest",
    "RestartConnectorResponse",
    "ResumeConnectorRequest",
    "ResumeConnectorResponse",
    "StopConnectorRequest",
    "StopConnectorResponse",
    "TaskRetryPolicy",
    "Topic",
    "UpdateClusterRequest",
    "UpdateConnectClusterRequest",
    "UpdateConnectorRequest",
    "UpdateConsumerGroupRequest",
    "UpdateTopicRequest",
)
