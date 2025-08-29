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
from google.cloud.managedkafka import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.managedkafka_v1.services.managed_kafka.client import ManagedKafkaClient
from google.cloud.managedkafka_v1.services.managed_kafka.async_client import ManagedKafkaAsyncClient
from google.cloud.managedkafka_v1.services.managed_kafka_connect.client import ManagedKafkaConnectClient
from google.cloud.managedkafka_v1.services.managed_kafka_connect.async_client import ManagedKafkaConnectAsyncClient

from google.cloud.managedkafka_v1.types.managed_kafka import AddAclEntryRequest
from google.cloud.managedkafka_v1.types.managed_kafka import AddAclEntryResponse
from google.cloud.managedkafka_v1.types.managed_kafka import CreateAclRequest
from google.cloud.managedkafka_v1.types.managed_kafka import CreateClusterRequest
from google.cloud.managedkafka_v1.types.managed_kafka import CreateTopicRequest
from google.cloud.managedkafka_v1.types.managed_kafka import DeleteAclRequest
from google.cloud.managedkafka_v1.types.managed_kafka import DeleteClusterRequest
from google.cloud.managedkafka_v1.types.managed_kafka import DeleteConsumerGroupRequest
from google.cloud.managedkafka_v1.types.managed_kafka import DeleteTopicRequest
from google.cloud.managedkafka_v1.types.managed_kafka import GetAclRequest
from google.cloud.managedkafka_v1.types.managed_kafka import GetClusterRequest
from google.cloud.managedkafka_v1.types.managed_kafka import GetConsumerGroupRequest
from google.cloud.managedkafka_v1.types.managed_kafka import GetTopicRequest
from google.cloud.managedkafka_v1.types.managed_kafka import ListAclsRequest
from google.cloud.managedkafka_v1.types.managed_kafka import ListAclsResponse
from google.cloud.managedkafka_v1.types.managed_kafka import ListClustersRequest
from google.cloud.managedkafka_v1.types.managed_kafka import ListClustersResponse
from google.cloud.managedkafka_v1.types.managed_kafka import ListConsumerGroupsRequest
from google.cloud.managedkafka_v1.types.managed_kafka import ListConsumerGroupsResponse
from google.cloud.managedkafka_v1.types.managed_kafka import ListTopicsRequest
from google.cloud.managedkafka_v1.types.managed_kafka import ListTopicsResponse
from google.cloud.managedkafka_v1.types.managed_kafka import RemoveAclEntryRequest
from google.cloud.managedkafka_v1.types.managed_kafka import RemoveAclEntryResponse
from google.cloud.managedkafka_v1.types.managed_kafka import UpdateAclRequest
from google.cloud.managedkafka_v1.types.managed_kafka import UpdateClusterRequest
from google.cloud.managedkafka_v1.types.managed_kafka import UpdateConsumerGroupRequest
from google.cloud.managedkafka_v1.types.managed_kafka import UpdateTopicRequest
from google.cloud.managedkafka_v1.types.managed_kafka_connect import CreateConnectClusterRequest
from google.cloud.managedkafka_v1.types.managed_kafka_connect import CreateConnectorRequest
from google.cloud.managedkafka_v1.types.managed_kafka_connect import DeleteConnectClusterRequest
from google.cloud.managedkafka_v1.types.managed_kafka_connect import DeleteConnectorRequest
from google.cloud.managedkafka_v1.types.managed_kafka_connect import GetConnectClusterRequest
from google.cloud.managedkafka_v1.types.managed_kafka_connect import GetConnectorRequest
from google.cloud.managedkafka_v1.types.managed_kafka_connect import ListConnectClustersRequest
from google.cloud.managedkafka_v1.types.managed_kafka_connect import ListConnectClustersResponse
from google.cloud.managedkafka_v1.types.managed_kafka_connect import ListConnectorsRequest
from google.cloud.managedkafka_v1.types.managed_kafka_connect import ListConnectorsResponse
from google.cloud.managedkafka_v1.types.managed_kafka_connect import PauseConnectorRequest
from google.cloud.managedkafka_v1.types.managed_kafka_connect import PauseConnectorResponse
from google.cloud.managedkafka_v1.types.managed_kafka_connect import RestartConnectorRequest
from google.cloud.managedkafka_v1.types.managed_kafka_connect import RestartConnectorResponse
from google.cloud.managedkafka_v1.types.managed_kafka_connect import ResumeConnectorRequest
from google.cloud.managedkafka_v1.types.managed_kafka_connect import ResumeConnectorResponse
from google.cloud.managedkafka_v1.types.managed_kafka_connect import StopConnectorRequest
from google.cloud.managedkafka_v1.types.managed_kafka_connect import StopConnectorResponse
from google.cloud.managedkafka_v1.types.managed_kafka_connect import UpdateConnectClusterRequest
from google.cloud.managedkafka_v1.types.managed_kafka_connect import UpdateConnectorRequest
from google.cloud.managedkafka_v1.types.resources import AccessConfig
from google.cloud.managedkafka_v1.types.resources import Acl
from google.cloud.managedkafka_v1.types.resources import AclEntry
from google.cloud.managedkafka_v1.types.resources import CapacityConfig
from google.cloud.managedkafka_v1.types.resources import Cluster
from google.cloud.managedkafka_v1.types.resources import ConnectAccessConfig
from google.cloud.managedkafka_v1.types.resources import ConnectCluster
from google.cloud.managedkafka_v1.types.resources import ConnectGcpConfig
from google.cloud.managedkafka_v1.types.resources import ConnectNetworkConfig
from google.cloud.managedkafka_v1.types.resources import Connector
from google.cloud.managedkafka_v1.types.resources import ConsumerGroup
from google.cloud.managedkafka_v1.types.resources import ConsumerPartitionMetadata
from google.cloud.managedkafka_v1.types.resources import ConsumerTopicMetadata
from google.cloud.managedkafka_v1.types.resources import GcpConfig
from google.cloud.managedkafka_v1.types.resources import NetworkConfig
from google.cloud.managedkafka_v1.types.resources import OperationMetadata
from google.cloud.managedkafka_v1.types.resources import RebalanceConfig
from google.cloud.managedkafka_v1.types.resources import TaskRetryPolicy
from google.cloud.managedkafka_v1.types.resources import TlsConfig
from google.cloud.managedkafka_v1.types.resources import Topic
from google.cloud.managedkafka_v1.types.resources import TrustConfig

__all__ = ('ManagedKafkaClient',
    'ManagedKafkaAsyncClient',
    'ManagedKafkaConnectClient',
    'ManagedKafkaConnectAsyncClient',
    'AddAclEntryRequest',
    'AddAclEntryResponse',
    'CreateAclRequest',
    'CreateClusterRequest',
    'CreateTopicRequest',
    'DeleteAclRequest',
    'DeleteClusterRequest',
    'DeleteConsumerGroupRequest',
    'DeleteTopicRequest',
    'GetAclRequest',
    'GetClusterRequest',
    'GetConsumerGroupRequest',
    'GetTopicRequest',
    'ListAclsRequest',
    'ListAclsResponse',
    'ListClustersRequest',
    'ListClustersResponse',
    'ListConsumerGroupsRequest',
    'ListConsumerGroupsResponse',
    'ListTopicsRequest',
    'ListTopicsResponse',
    'RemoveAclEntryRequest',
    'RemoveAclEntryResponse',
    'UpdateAclRequest',
    'UpdateClusterRequest',
    'UpdateConsumerGroupRequest',
    'UpdateTopicRequest',
    'CreateConnectClusterRequest',
    'CreateConnectorRequest',
    'DeleteConnectClusterRequest',
    'DeleteConnectorRequest',
    'GetConnectClusterRequest',
    'GetConnectorRequest',
    'ListConnectClustersRequest',
    'ListConnectClustersResponse',
    'ListConnectorsRequest',
    'ListConnectorsResponse',
    'PauseConnectorRequest',
    'PauseConnectorResponse',
    'RestartConnectorRequest',
    'RestartConnectorResponse',
    'ResumeConnectorRequest',
    'ResumeConnectorResponse',
    'StopConnectorRequest',
    'StopConnectorResponse',
    'UpdateConnectClusterRequest',
    'UpdateConnectorRequest',
    'AccessConfig',
    'Acl',
    'AclEntry',
    'CapacityConfig',
    'Cluster',
    'ConnectAccessConfig',
    'ConnectCluster',
    'ConnectGcpConfig',
    'ConnectNetworkConfig',
    'Connector',
    'ConsumerGroup',
    'ConsumerPartitionMetadata',
    'ConsumerTopicMetadata',
    'GcpConfig',
    'NetworkConfig',
    'OperationMetadata',
    'RebalanceConfig',
    'TaskRetryPolicy',
    'TlsConfig',
    'Topic',
    'TrustConfig',
)
