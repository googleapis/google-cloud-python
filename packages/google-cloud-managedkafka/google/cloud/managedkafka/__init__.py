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
from google.cloud.managedkafka import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.managedkafka_v1.services.managed_kafka.async_client import (
    ManagedKafkaAsyncClient,
)
from google.cloud.managedkafka_v1.services.managed_kafka.client import (
    ManagedKafkaClient,
)
from google.cloud.managedkafka_v1.types.managed_kafka import (
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
from google.cloud.managedkafka_v1.types.resources import (
    AccessConfig,
    CapacityConfig,
    Cluster,
    ConsumerGroup,
    ConsumerPartitionMetadata,
    ConsumerTopicMetadata,
    GcpConfig,
    NetworkConfig,
    OperationMetadata,
    RebalanceConfig,
    Topic,
)

__all__ = (
    "ManagedKafkaClient",
    "ManagedKafkaAsyncClient",
    "CreateClusterRequest",
    "CreateTopicRequest",
    "DeleteClusterRequest",
    "DeleteConsumerGroupRequest",
    "DeleteTopicRequest",
    "GetClusterRequest",
    "GetConsumerGroupRequest",
    "GetTopicRequest",
    "ListClustersRequest",
    "ListClustersResponse",
    "ListConsumerGroupsRequest",
    "ListConsumerGroupsResponse",
    "ListTopicsRequest",
    "ListTopicsResponse",
    "UpdateClusterRequest",
    "UpdateConsumerGroupRequest",
    "UpdateTopicRequest",
    "AccessConfig",
    "CapacityConfig",
    "Cluster",
    "ConsumerGroup",
    "ConsumerPartitionMetadata",
    "ConsumerTopicMetadata",
    "GcpConfig",
    "NetworkConfig",
    "OperationMetadata",
    "RebalanceConfig",
    "Topic",
)
