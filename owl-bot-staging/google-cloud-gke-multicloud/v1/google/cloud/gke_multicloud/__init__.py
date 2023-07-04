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


from google.cloud.gke_multicloud_v1.services.attached_clusters.client import AttachedClustersClient
from google.cloud.gke_multicloud_v1.services.attached_clusters.async_client import AttachedClustersAsyncClient
from google.cloud.gke_multicloud_v1.services.aws_clusters.client import AwsClustersClient
from google.cloud.gke_multicloud_v1.services.aws_clusters.async_client import AwsClustersAsyncClient
from google.cloud.gke_multicloud_v1.services.azure_clusters.client import AzureClustersClient
from google.cloud.gke_multicloud_v1.services.azure_clusters.async_client import AzureClustersAsyncClient

from google.cloud.gke_multicloud_v1.types.attached_resources import AttachedCluster
from google.cloud.gke_multicloud_v1.types.attached_resources import AttachedClusterError
from google.cloud.gke_multicloud_v1.types.attached_resources import AttachedClustersAuthorization
from google.cloud.gke_multicloud_v1.types.attached_resources import AttachedClusterUser
from google.cloud.gke_multicloud_v1.types.attached_resources import AttachedOidcConfig
from google.cloud.gke_multicloud_v1.types.attached_resources import AttachedPlatformVersionInfo
from google.cloud.gke_multicloud_v1.types.attached_resources import AttachedServerConfig
from google.cloud.gke_multicloud_v1.types.attached_service import CreateAttachedClusterRequest
from google.cloud.gke_multicloud_v1.types.attached_service import DeleteAttachedClusterRequest
from google.cloud.gke_multicloud_v1.types.attached_service import GenerateAttachedClusterInstallManifestRequest
from google.cloud.gke_multicloud_v1.types.attached_service import GenerateAttachedClusterInstallManifestResponse
from google.cloud.gke_multicloud_v1.types.attached_service import GetAttachedClusterRequest
from google.cloud.gke_multicloud_v1.types.attached_service import GetAttachedServerConfigRequest
from google.cloud.gke_multicloud_v1.types.attached_service import ImportAttachedClusterRequest
from google.cloud.gke_multicloud_v1.types.attached_service import ListAttachedClustersRequest
from google.cloud.gke_multicloud_v1.types.attached_service import ListAttachedClustersResponse
from google.cloud.gke_multicloud_v1.types.attached_service import UpdateAttachedClusterRequest
from google.cloud.gke_multicloud_v1.types.aws_resources import AwsAuthorization
from google.cloud.gke_multicloud_v1.types.aws_resources import AwsAutoscalingGroupMetricsCollection
from google.cloud.gke_multicloud_v1.types.aws_resources import AwsCluster
from google.cloud.gke_multicloud_v1.types.aws_resources import AwsClusterError
from google.cloud.gke_multicloud_v1.types.aws_resources import AwsClusterNetworking
from google.cloud.gke_multicloud_v1.types.aws_resources import AwsClusterUser
from google.cloud.gke_multicloud_v1.types.aws_resources import AwsConfigEncryption
from google.cloud.gke_multicloud_v1.types.aws_resources import AwsControlPlane
from google.cloud.gke_multicloud_v1.types.aws_resources import AwsDatabaseEncryption
from google.cloud.gke_multicloud_v1.types.aws_resources import AwsInstancePlacement
from google.cloud.gke_multicloud_v1.types.aws_resources import AwsK8sVersionInfo
from google.cloud.gke_multicloud_v1.types.aws_resources import AwsNodeConfig
from google.cloud.gke_multicloud_v1.types.aws_resources import AwsNodePool
from google.cloud.gke_multicloud_v1.types.aws_resources import AwsNodePoolAutoscaling
from google.cloud.gke_multicloud_v1.types.aws_resources import AwsNodePoolError
from google.cloud.gke_multicloud_v1.types.aws_resources import AwsProxyConfig
from google.cloud.gke_multicloud_v1.types.aws_resources import AwsServerConfig
from google.cloud.gke_multicloud_v1.types.aws_resources import AwsServicesAuthentication
from google.cloud.gke_multicloud_v1.types.aws_resources import AwsSshConfig
from google.cloud.gke_multicloud_v1.types.aws_resources import AwsVolumeTemplate
from google.cloud.gke_multicloud_v1.types.aws_service import CreateAwsClusterRequest
from google.cloud.gke_multicloud_v1.types.aws_service import CreateAwsNodePoolRequest
from google.cloud.gke_multicloud_v1.types.aws_service import DeleteAwsClusterRequest
from google.cloud.gke_multicloud_v1.types.aws_service import DeleteAwsNodePoolRequest
from google.cloud.gke_multicloud_v1.types.aws_service import GenerateAwsAccessTokenRequest
from google.cloud.gke_multicloud_v1.types.aws_service import GenerateAwsAccessTokenResponse
from google.cloud.gke_multicloud_v1.types.aws_service import GetAwsClusterRequest
from google.cloud.gke_multicloud_v1.types.aws_service import GetAwsNodePoolRequest
from google.cloud.gke_multicloud_v1.types.aws_service import GetAwsServerConfigRequest
from google.cloud.gke_multicloud_v1.types.aws_service import ListAwsClustersRequest
from google.cloud.gke_multicloud_v1.types.aws_service import ListAwsClustersResponse
from google.cloud.gke_multicloud_v1.types.aws_service import ListAwsNodePoolsRequest
from google.cloud.gke_multicloud_v1.types.aws_service import ListAwsNodePoolsResponse
from google.cloud.gke_multicloud_v1.types.aws_service import UpdateAwsClusterRequest
from google.cloud.gke_multicloud_v1.types.aws_service import UpdateAwsNodePoolRequest
from google.cloud.gke_multicloud_v1.types.azure_resources import AzureAuthorization
from google.cloud.gke_multicloud_v1.types.azure_resources import AzureClient
from google.cloud.gke_multicloud_v1.types.azure_resources import AzureCluster
from google.cloud.gke_multicloud_v1.types.azure_resources import AzureClusterError
from google.cloud.gke_multicloud_v1.types.azure_resources import AzureClusterNetworking
from google.cloud.gke_multicloud_v1.types.azure_resources import AzureClusterResources
from google.cloud.gke_multicloud_v1.types.azure_resources import AzureClusterUser
from google.cloud.gke_multicloud_v1.types.azure_resources import AzureConfigEncryption
from google.cloud.gke_multicloud_v1.types.azure_resources import AzureControlPlane
from google.cloud.gke_multicloud_v1.types.azure_resources import AzureDatabaseEncryption
from google.cloud.gke_multicloud_v1.types.azure_resources import AzureDiskTemplate
from google.cloud.gke_multicloud_v1.types.azure_resources import AzureK8sVersionInfo
from google.cloud.gke_multicloud_v1.types.azure_resources import AzureNodeConfig
from google.cloud.gke_multicloud_v1.types.azure_resources import AzureNodePool
from google.cloud.gke_multicloud_v1.types.azure_resources import AzureNodePoolAutoscaling
from google.cloud.gke_multicloud_v1.types.azure_resources import AzureNodePoolError
from google.cloud.gke_multicloud_v1.types.azure_resources import AzureProxyConfig
from google.cloud.gke_multicloud_v1.types.azure_resources import AzureServerConfig
from google.cloud.gke_multicloud_v1.types.azure_resources import AzureServicesAuthentication
from google.cloud.gke_multicloud_v1.types.azure_resources import AzureSshConfig
from google.cloud.gke_multicloud_v1.types.azure_resources import ReplicaPlacement
from google.cloud.gke_multicloud_v1.types.azure_service import CreateAzureClientRequest
from google.cloud.gke_multicloud_v1.types.azure_service import CreateAzureClusterRequest
from google.cloud.gke_multicloud_v1.types.azure_service import CreateAzureNodePoolRequest
from google.cloud.gke_multicloud_v1.types.azure_service import DeleteAzureClientRequest
from google.cloud.gke_multicloud_v1.types.azure_service import DeleteAzureClusterRequest
from google.cloud.gke_multicloud_v1.types.azure_service import DeleteAzureNodePoolRequest
from google.cloud.gke_multicloud_v1.types.azure_service import GenerateAzureAccessTokenRequest
from google.cloud.gke_multicloud_v1.types.azure_service import GenerateAzureAccessTokenResponse
from google.cloud.gke_multicloud_v1.types.azure_service import GetAzureClientRequest
from google.cloud.gke_multicloud_v1.types.azure_service import GetAzureClusterRequest
from google.cloud.gke_multicloud_v1.types.azure_service import GetAzureNodePoolRequest
from google.cloud.gke_multicloud_v1.types.azure_service import GetAzureServerConfigRequest
from google.cloud.gke_multicloud_v1.types.azure_service import ListAzureClientsRequest
from google.cloud.gke_multicloud_v1.types.azure_service import ListAzureClientsResponse
from google.cloud.gke_multicloud_v1.types.azure_service import ListAzureClustersRequest
from google.cloud.gke_multicloud_v1.types.azure_service import ListAzureClustersResponse
from google.cloud.gke_multicloud_v1.types.azure_service import ListAzureNodePoolsRequest
from google.cloud.gke_multicloud_v1.types.azure_service import ListAzureNodePoolsResponse
from google.cloud.gke_multicloud_v1.types.azure_service import UpdateAzureClusterRequest
from google.cloud.gke_multicloud_v1.types.azure_service import UpdateAzureNodePoolRequest
from google.cloud.gke_multicloud_v1.types.common_resources import Fleet
from google.cloud.gke_multicloud_v1.types.common_resources import LoggingComponentConfig
from google.cloud.gke_multicloud_v1.types.common_resources import LoggingConfig
from google.cloud.gke_multicloud_v1.types.common_resources import ManagedPrometheusConfig
from google.cloud.gke_multicloud_v1.types.common_resources import MaxPodsConstraint
from google.cloud.gke_multicloud_v1.types.common_resources import MonitoringConfig
from google.cloud.gke_multicloud_v1.types.common_resources import NodeTaint
from google.cloud.gke_multicloud_v1.types.common_resources import OperationMetadata
from google.cloud.gke_multicloud_v1.types.common_resources import WorkloadIdentityConfig

__all__ = ('AttachedClustersClient',
    'AttachedClustersAsyncClient',
    'AwsClustersClient',
    'AwsClustersAsyncClient',
    'AzureClustersClient',
    'AzureClustersAsyncClient',
    'AttachedCluster',
    'AttachedClusterError',
    'AttachedClustersAuthorization',
    'AttachedClusterUser',
    'AttachedOidcConfig',
    'AttachedPlatformVersionInfo',
    'AttachedServerConfig',
    'CreateAttachedClusterRequest',
    'DeleteAttachedClusterRequest',
    'GenerateAttachedClusterInstallManifestRequest',
    'GenerateAttachedClusterInstallManifestResponse',
    'GetAttachedClusterRequest',
    'GetAttachedServerConfigRequest',
    'ImportAttachedClusterRequest',
    'ListAttachedClustersRequest',
    'ListAttachedClustersResponse',
    'UpdateAttachedClusterRequest',
    'AwsAuthorization',
    'AwsAutoscalingGroupMetricsCollection',
    'AwsCluster',
    'AwsClusterError',
    'AwsClusterNetworking',
    'AwsClusterUser',
    'AwsConfigEncryption',
    'AwsControlPlane',
    'AwsDatabaseEncryption',
    'AwsInstancePlacement',
    'AwsK8sVersionInfo',
    'AwsNodeConfig',
    'AwsNodePool',
    'AwsNodePoolAutoscaling',
    'AwsNodePoolError',
    'AwsProxyConfig',
    'AwsServerConfig',
    'AwsServicesAuthentication',
    'AwsSshConfig',
    'AwsVolumeTemplate',
    'CreateAwsClusterRequest',
    'CreateAwsNodePoolRequest',
    'DeleteAwsClusterRequest',
    'DeleteAwsNodePoolRequest',
    'GenerateAwsAccessTokenRequest',
    'GenerateAwsAccessTokenResponse',
    'GetAwsClusterRequest',
    'GetAwsNodePoolRequest',
    'GetAwsServerConfigRequest',
    'ListAwsClustersRequest',
    'ListAwsClustersResponse',
    'ListAwsNodePoolsRequest',
    'ListAwsNodePoolsResponse',
    'UpdateAwsClusterRequest',
    'UpdateAwsNodePoolRequest',
    'AzureAuthorization',
    'AzureClient',
    'AzureCluster',
    'AzureClusterError',
    'AzureClusterNetworking',
    'AzureClusterResources',
    'AzureClusterUser',
    'AzureConfigEncryption',
    'AzureControlPlane',
    'AzureDatabaseEncryption',
    'AzureDiskTemplate',
    'AzureK8sVersionInfo',
    'AzureNodeConfig',
    'AzureNodePool',
    'AzureNodePoolAutoscaling',
    'AzureNodePoolError',
    'AzureProxyConfig',
    'AzureServerConfig',
    'AzureServicesAuthentication',
    'AzureSshConfig',
    'ReplicaPlacement',
    'CreateAzureClientRequest',
    'CreateAzureClusterRequest',
    'CreateAzureNodePoolRequest',
    'DeleteAzureClientRequest',
    'DeleteAzureClusterRequest',
    'DeleteAzureNodePoolRequest',
    'GenerateAzureAccessTokenRequest',
    'GenerateAzureAccessTokenResponse',
    'GetAzureClientRequest',
    'GetAzureClusterRequest',
    'GetAzureNodePoolRequest',
    'GetAzureServerConfigRequest',
    'ListAzureClientsRequest',
    'ListAzureClientsResponse',
    'ListAzureClustersRequest',
    'ListAzureClustersResponse',
    'ListAzureNodePoolsRequest',
    'ListAzureNodePoolsResponse',
    'UpdateAzureClusterRequest',
    'UpdateAzureNodePoolRequest',
    'Fleet',
    'LoggingComponentConfig',
    'LoggingConfig',
    'ManagedPrometheusConfig',
    'MaxPodsConstraint',
    'MonitoringConfig',
    'NodeTaint',
    'OperationMetadata',
    'WorkloadIdentityConfig',
)
