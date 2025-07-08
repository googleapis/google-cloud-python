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


from .services.managed_kafka import ManagedKafkaClient
from .services.managed_kafka import ManagedKafkaAsyncClient
from .services.managed_kafka_connect import ManagedKafkaConnectClient
from .services.managed_kafka_connect import ManagedKafkaConnectAsyncClient

from .types.managed_kafka import AddAclEntryRequest
from .types.managed_kafka import AddAclEntryResponse
from .types.managed_kafka import CreateAclRequest
from .types.managed_kafka import CreateClusterRequest
from .types.managed_kafka import CreateTopicRequest
from .types.managed_kafka import DeleteAclRequest
from .types.managed_kafka import DeleteClusterRequest
from .types.managed_kafka import DeleteConsumerGroupRequest
from .types.managed_kafka import DeleteTopicRequest
from .types.managed_kafka import GetAclRequest
from .types.managed_kafka import GetClusterRequest
from .types.managed_kafka import GetConsumerGroupRequest
from .types.managed_kafka import GetTopicRequest
from .types.managed_kafka import ListAclsRequest
from .types.managed_kafka import ListAclsResponse
from .types.managed_kafka import ListClustersRequest
from .types.managed_kafka import ListClustersResponse
from .types.managed_kafka import ListConsumerGroupsRequest
from .types.managed_kafka import ListConsumerGroupsResponse
from .types.managed_kafka import ListTopicsRequest
from .types.managed_kafka import ListTopicsResponse
from .types.managed_kafka import RemoveAclEntryRequest
from .types.managed_kafka import RemoveAclEntryResponse
from .types.managed_kafka import UpdateAclRequest
from .types.managed_kafka import UpdateClusterRequest
from .types.managed_kafka import UpdateConsumerGroupRequest
from .types.managed_kafka import UpdateTopicRequest
from .types.managed_kafka_connect import CreateConnectClusterRequest
from .types.managed_kafka_connect import CreateConnectorRequest
from .types.managed_kafka_connect import DeleteConnectClusterRequest
from .types.managed_kafka_connect import DeleteConnectorRequest
from .types.managed_kafka_connect import GetConnectClusterRequest
from .types.managed_kafka_connect import GetConnectorRequest
from .types.managed_kafka_connect import ListConnectClustersRequest
from .types.managed_kafka_connect import ListConnectClustersResponse
from .types.managed_kafka_connect import ListConnectorsRequest
from .types.managed_kafka_connect import ListConnectorsResponse
from .types.managed_kafka_connect import PauseConnectorRequest
from .types.managed_kafka_connect import PauseConnectorResponse
from .types.managed_kafka_connect import RestartConnectorRequest
from .types.managed_kafka_connect import RestartConnectorResponse
from .types.managed_kafka_connect import ResumeConnectorRequest
from .types.managed_kafka_connect import ResumeConnectorResponse
from .types.managed_kafka_connect import StopConnectorRequest
from .types.managed_kafka_connect import StopConnectorResponse
from .types.managed_kafka_connect import UpdateConnectClusterRequest
from .types.managed_kafka_connect import UpdateConnectorRequest
from .types.resources import AccessConfig
from .types.resources import Acl
from .types.resources import AclEntry
from .types.resources import CapacityConfig
from .types.resources import Cluster
from .types.resources import ConnectAccessConfig
from .types.resources import ConnectCluster
from .types.resources import ConnectGcpConfig
from .types.resources import ConnectNetworkConfig
from .types.resources import Connector
from .types.resources import ConsumerGroup
from .types.resources import ConsumerPartitionMetadata
from .types.resources import ConsumerTopicMetadata
from .types.resources import GcpConfig
from .types.resources import NetworkConfig
from .types.resources import OperationMetadata
from .types.resources import RebalanceConfig
from .types.resources import TaskRetryPolicy
from .types.resources import TlsConfig
from .types.resources import Topic
from .types.resources import TrustConfig

__all__ = (
    'ManagedKafkaAsyncClient',
    'ManagedKafkaConnectAsyncClient',
'AccessConfig',
'Acl',
'AclEntry',
'AddAclEntryRequest',
'AddAclEntryResponse',
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
'CreateAclRequest',
'CreateClusterRequest',
'CreateConnectClusterRequest',
'CreateConnectorRequest',
'CreateTopicRequest',
'DeleteAclRequest',
'DeleteClusterRequest',
'DeleteConnectClusterRequest',
'DeleteConnectorRequest',
'DeleteConsumerGroupRequest',
'DeleteTopicRequest',
'GcpConfig',
'GetAclRequest',
'GetClusterRequest',
'GetConnectClusterRequest',
'GetConnectorRequest',
'GetConsumerGroupRequest',
'GetTopicRequest',
'ListAclsRequest',
'ListAclsResponse',
'ListClustersRequest',
'ListClustersResponse',
'ListConnectClustersRequest',
'ListConnectClustersResponse',
'ListConnectorsRequest',
'ListConnectorsResponse',
'ListConsumerGroupsRequest',
'ListConsumerGroupsResponse',
'ListTopicsRequest',
'ListTopicsResponse',
'ManagedKafkaClient',
'ManagedKafkaConnectClient',
'NetworkConfig',
'OperationMetadata',
'PauseConnectorRequest',
'PauseConnectorResponse',
'RebalanceConfig',
'RemoveAclEntryRequest',
'RemoveAclEntryResponse',
'RestartConnectorRequest',
'RestartConnectorResponse',
'ResumeConnectorRequest',
'ResumeConnectorResponse',
'StopConnectorRequest',
'StopConnectorResponse',
'TaskRetryPolicy',
'TlsConfig',
'Topic',
'TrustConfig',
'UpdateAclRequest',
'UpdateClusterRequest',
'UpdateConnectClusterRequest',
'UpdateConnectorRequest',
'UpdateConsumerGroupRequest',
'UpdateTopicRequest',
)
