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
from google.cloud.redis_cluster import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.redis_cluster_v1.services.cloud_redis_cluster.async_client import (
    CloudRedisClusterAsyncClient,
)
from google.cloud.redis_cluster_v1.services.cloud_redis_cluster.client import (
    CloudRedisClusterClient,
)
from google.cloud.redis_cluster_v1.types.cloud_redis_cluster import (
    AuthorizationMode,
    CertificateAuthority,
    Cluster,
    ClusterPersistenceConfig,
    CreateClusterRequest,
    DeleteClusterRequest,
    DiscoveryEndpoint,
    GetClusterCertificateAuthorityRequest,
    GetClusterRequest,
    ListClustersRequest,
    ListClustersResponse,
    NodeType,
    OperationMetadata,
    PscConfig,
    PscConnection,
    TransitEncryptionMode,
    UpdateClusterRequest,
    ZoneDistributionConfig,
)

__all__ = (
    "CloudRedisClusterClient",
    "CloudRedisClusterAsyncClient",
    "CertificateAuthority",
    "Cluster",
    "ClusterPersistenceConfig",
    "CreateClusterRequest",
    "DeleteClusterRequest",
    "DiscoveryEndpoint",
    "GetClusterCertificateAuthorityRequest",
    "GetClusterRequest",
    "ListClustersRequest",
    "ListClustersResponse",
    "OperationMetadata",
    "PscConfig",
    "PscConnection",
    "UpdateClusterRequest",
    "ZoneDistributionConfig",
    "AuthorizationMode",
    "NodeType",
    "TransitEncryptionMode",
)
