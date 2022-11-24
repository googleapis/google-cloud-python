# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from google.cloud.gke_multicloud import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.gke_multicloud_v1.services.aws_clusters.async_client import (
    AwsClustersAsyncClient,
)
from google.cloud.gke_multicloud_v1.services.aws_clusters.client import (
    AwsClustersClient,
)
from google.cloud.gke_multicloud_v1.services.azure_clusters.async_client import (
    AzureClustersAsyncClient,
)
from google.cloud.gke_multicloud_v1.services.azure_clusters.client import (
    AzureClustersClient,
)
from google.cloud.gke_multicloud_v1.types.aws_resources import (
    AwsAuthorization,
    AwsCluster,
    AwsClusterNetworking,
    AwsClusterUser,
    AwsConfigEncryption,
    AwsControlPlane,
    AwsDatabaseEncryption,
    AwsInstancePlacement,
    AwsK8sVersionInfo,
    AwsNodeConfig,
    AwsNodePool,
    AwsNodePoolAutoscaling,
    AwsProxyConfig,
    AwsServerConfig,
    AwsServicesAuthentication,
    AwsSshConfig,
    AwsVolumeTemplate,
)
from google.cloud.gke_multicloud_v1.types.aws_service import (
    CreateAwsClusterRequest,
    CreateAwsNodePoolRequest,
    DeleteAwsClusterRequest,
    DeleteAwsNodePoolRequest,
    GenerateAwsAccessTokenRequest,
    GenerateAwsAccessTokenResponse,
    GetAwsClusterRequest,
    GetAwsNodePoolRequest,
    GetAwsServerConfigRequest,
    ListAwsClustersRequest,
    ListAwsClustersResponse,
    ListAwsNodePoolsRequest,
    ListAwsNodePoolsResponse,
    UpdateAwsClusterRequest,
    UpdateAwsNodePoolRequest,
)
from google.cloud.gke_multicloud_v1.types.azure_resources import (
    AzureAuthorization,
    AzureClient,
    AzureCluster,
    AzureClusterNetworking,
    AzureClusterResources,
    AzureClusterUser,
    AzureConfigEncryption,
    AzureControlPlane,
    AzureDatabaseEncryption,
    AzureDiskTemplate,
    AzureK8sVersionInfo,
    AzureNodeConfig,
    AzureNodePool,
    AzureNodePoolAutoscaling,
    AzureProxyConfig,
    AzureServerConfig,
    AzureSshConfig,
    ReplicaPlacement,
)
from google.cloud.gke_multicloud_v1.types.azure_service import (
    CreateAzureClientRequest,
    CreateAzureClusterRequest,
    CreateAzureNodePoolRequest,
    DeleteAzureClientRequest,
    DeleteAzureClusterRequest,
    DeleteAzureNodePoolRequest,
    GenerateAzureAccessTokenRequest,
    GenerateAzureAccessTokenResponse,
    GetAzureClientRequest,
    GetAzureClusterRequest,
    GetAzureNodePoolRequest,
    GetAzureServerConfigRequest,
    ListAzureClientsRequest,
    ListAzureClientsResponse,
    ListAzureClustersRequest,
    ListAzureClustersResponse,
    ListAzureNodePoolsRequest,
    ListAzureNodePoolsResponse,
    UpdateAzureClusterRequest,
    UpdateAzureNodePoolRequest,
)
from google.cloud.gke_multicloud_v1.types.common_resources import (
    Fleet,
    LoggingComponentConfig,
    LoggingConfig,
    MaxPodsConstraint,
    NodeTaint,
    OperationMetadata,
    WorkloadIdentityConfig,
)

__all__ = (
    "AwsClustersClient",
    "AwsClustersAsyncClient",
    "AzureClustersClient",
    "AzureClustersAsyncClient",
    "AwsAuthorization",
    "AwsCluster",
    "AwsClusterNetworking",
    "AwsClusterUser",
    "AwsConfigEncryption",
    "AwsControlPlane",
    "AwsDatabaseEncryption",
    "AwsInstancePlacement",
    "AwsK8sVersionInfo",
    "AwsNodeConfig",
    "AwsNodePool",
    "AwsNodePoolAutoscaling",
    "AwsProxyConfig",
    "AwsServerConfig",
    "AwsServicesAuthentication",
    "AwsSshConfig",
    "AwsVolumeTemplate",
    "CreateAwsClusterRequest",
    "CreateAwsNodePoolRequest",
    "DeleteAwsClusterRequest",
    "DeleteAwsNodePoolRequest",
    "GenerateAwsAccessTokenRequest",
    "GenerateAwsAccessTokenResponse",
    "GetAwsClusterRequest",
    "GetAwsNodePoolRequest",
    "GetAwsServerConfigRequest",
    "ListAwsClustersRequest",
    "ListAwsClustersResponse",
    "ListAwsNodePoolsRequest",
    "ListAwsNodePoolsResponse",
    "UpdateAwsClusterRequest",
    "UpdateAwsNodePoolRequest",
    "AzureAuthorization",
    "AzureClient",
    "AzureCluster",
    "AzureClusterNetworking",
    "AzureClusterResources",
    "AzureClusterUser",
    "AzureConfigEncryption",
    "AzureControlPlane",
    "AzureDatabaseEncryption",
    "AzureDiskTemplate",
    "AzureK8sVersionInfo",
    "AzureNodeConfig",
    "AzureNodePool",
    "AzureNodePoolAutoscaling",
    "AzureProxyConfig",
    "AzureServerConfig",
    "AzureSshConfig",
    "ReplicaPlacement",
    "CreateAzureClientRequest",
    "CreateAzureClusterRequest",
    "CreateAzureNodePoolRequest",
    "DeleteAzureClientRequest",
    "DeleteAzureClusterRequest",
    "DeleteAzureNodePoolRequest",
    "GenerateAzureAccessTokenRequest",
    "GenerateAzureAccessTokenResponse",
    "GetAzureClientRequest",
    "GetAzureClusterRequest",
    "GetAzureNodePoolRequest",
    "GetAzureServerConfigRequest",
    "ListAzureClientsRequest",
    "ListAzureClientsResponse",
    "ListAzureClustersRequest",
    "ListAzureClustersResponse",
    "ListAzureNodePoolsRequest",
    "ListAzureNodePoolsResponse",
    "UpdateAzureClusterRequest",
    "UpdateAzureNodePoolRequest",
    "Fleet",
    "LoggingComponentConfig",
    "LoggingConfig",
    "MaxPodsConstraint",
    "NodeTaint",
    "OperationMetadata",
    "WorkloadIdentityConfig",
)
