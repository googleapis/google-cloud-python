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
from google.cloud.gke_multicloud_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.attached_clusters import AttachedClustersClient
from .services.attached_clusters import AttachedClustersAsyncClient
from .services.aws_clusters import AwsClustersClient
from .services.aws_clusters import AwsClustersAsyncClient
from .services.azure_clusters import AzureClustersClient
from .services.azure_clusters import AzureClustersAsyncClient

from .types.attached_resources import AttachedCluster
from .types.attached_resources import AttachedClusterError
from .types.attached_resources import AttachedClustersAuthorization
from .types.attached_resources import AttachedClusterUser
from .types.attached_resources import AttachedOidcConfig
from .types.attached_resources import AttachedPlatformVersionInfo
from .types.attached_resources import AttachedServerConfig
from .types.attached_service import CreateAttachedClusterRequest
from .types.attached_service import DeleteAttachedClusterRequest
from .types.attached_service import GenerateAttachedClusterInstallManifestRequest
from .types.attached_service import GenerateAttachedClusterInstallManifestResponse
from .types.attached_service import GetAttachedClusterRequest
from .types.attached_service import GetAttachedServerConfigRequest
from .types.attached_service import ImportAttachedClusterRequest
from .types.attached_service import ListAttachedClustersRequest
from .types.attached_service import ListAttachedClustersResponse
from .types.attached_service import UpdateAttachedClusterRequest
from .types.aws_resources import AwsAuthorization
from .types.aws_resources import AwsAutoscalingGroupMetricsCollection
from .types.aws_resources import AwsCluster
from .types.aws_resources import AwsClusterError
from .types.aws_resources import AwsClusterNetworking
from .types.aws_resources import AwsClusterUser
from .types.aws_resources import AwsConfigEncryption
from .types.aws_resources import AwsControlPlane
from .types.aws_resources import AwsDatabaseEncryption
from .types.aws_resources import AwsInstancePlacement
from .types.aws_resources import AwsK8sVersionInfo
from .types.aws_resources import AwsNodeConfig
from .types.aws_resources import AwsNodePool
from .types.aws_resources import AwsNodePoolAutoscaling
from .types.aws_resources import AwsNodePoolError
from .types.aws_resources import AwsProxyConfig
from .types.aws_resources import AwsServerConfig
from .types.aws_resources import AwsServicesAuthentication
from .types.aws_resources import AwsSshConfig
from .types.aws_resources import AwsVolumeTemplate
from .types.aws_service import CreateAwsClusterRequest
from .types.aws_service import CreateAwsNodePoolRequest
from .types.aws_service import DeleteAwsClusterRequest
from .types.aws_service import DeleteAwsNodePoolRequest
from .types.aws_service import GenerateAwsAccessTokenRequest
from .types.aws_service import GenerateAwsAccessTokenResponse
from .types.aws_service import GetAwsClusterRequest
from .types.aws_service import GetAwsNodePoolRequest
from .types.aws_service import GetAwsServerConfigRequest
from .types.aws_service import ListAwsClustersRequest
from .types.aws_service import ListAwsClustersResponse
from .types.aws_service import ListAwsNodePoolsRequest
from .types.aws_service import ListAwsNodePoolsResponse
from .types.aws_service import UpdateAwsClusterRequest
from .types.aws_service import UpdateAwsNodePoolRequest
from .types.azure_resources import AzureAuthorization
from .types.azure_resources import AzureClient
from .types.azure_resources import AzureCluster
from .types.azure_resources import AzureClusterError
from .types.azure_resources import AzureClusterNetworking
from .types.azure_resources import AzureClusterResources
from .types.azure_resources import AzureClusterUser
from .types.azure_resources import AzureConfigEncryption
from .types.azure_resources import AzureControlPlane
from .types.azure_resources import AzureDatabaseEncryption
from .types.azure_resources import AzureDiskTemplate
from .types.azure_resources import AzureK8sVersionInfo
from .types.azure_resources import AzureNodeConfig
from .types.azure_resources import AzureNodePool
from .types.azure_resources import AzureNodePoolAutoscaling
from .types.azure_resources import AzureNodePoolError
from .types.azure_resources import AzureProxyConfig
from .types.azure_resources import AzureServerConfig
from .types.azure_resources import AzureServicesAuthentication
from .types.azure_resources import AzureSshConfig
from .types.azure_resources import ReplicaPlacement
from .types.azure_service import CreateAzureClientRequest
from .types.azure_service import CreateAzureClusterRequest
from .types.azure_service import CreateAzureNodePoolRequest
from .types.azure_service import DeleteAzureClientRequest
from .types.azure_service import DeleteAzureClusterRequest
from .types.azure_service import DeleteAzureNodePoolRequest
from .types.azure_service import GenerateAzureAccessTokenRequest
from .types.azure_service import GenerateAzureAccessTokenResponse
from .types.azure_service import GetAzureClientRequest
from .types.azure_service import GetAzureClusterRequest
from .types.azure_service import GetAzureNodePoolRequest
from .types.azure_service import GetAzureServerConfigRequest
from .types.azure_service import ListAzureClientsRequest
from .types.azure_service import ListAzureClientsResponse
from .types.azure_service import ListAzureClustersRequest
from .types.azure_service import ListAzureClustersResponse
from .types.azure_service import ListAzureNodePoolsRequest
from .types.azure_service import ListAzureNodePoolsResponse
from .types.azure_service import UpdateAzureClusterRequest
from .types.azure_service import UpdateAzureNodePoolRequest
from .types.common_resources import Fleet
from .types.common_resources import LoggingComponentConfig
from .types.common_resources import LoggingConfig
from .types.common_resources import ManagedPrometheusConfig
from .types.common_resources import MaxPodsConstraint
from .types.common_resources import MonitoringConfig
from .types.common_resources import NodeTaint
from .types.common_resources import OperationMetadata
from .types.common_resources import WorkloadIdentityConfig

__all__ = (
    'AttachedClustersAsyncClient',
    'AwsClustersAsyncClient',
    'AzureClustersAsyncClient',
'AttachedCluster',
'AttachedClusterError',
'AttachedClusterUser',
'AttachedClustersAuthorization',
'AttachedClustersClient',
'AttachedOidcConfig',
'AttachedPlatformVersionInfo',
'AttachedServerConfig',
'AwsAuthorization',
'AwsAutoscalingGroupMetricsCollection',
'AwsCluster',
'AwsClusterError',
'AwsClusterNetworking',
'AwsClusterUser',
'AwsClustersClient',
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
'AzureAuthorization',
'AzureClient',
'AzureCluster',
'AzureClusterError',
'AzureClusterNetworking',
'AzureClusterResources',
'AzureClusterUser',
'AzureClustersClient',
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
'CreateAttachedClusterRequest',
'CreateAwsClusterRequest',
'CreateAwsNodePoolRequest',
'CreateAzureClientRequest',
'CreateAzureClusterRequest',
'CreateAzureNodePoolRequest',
'DeleteAttachedClusterRequest',
'DeleteAwsClusterRequest',
'DeleteAwsNodePoolRequest',
'DeleteAzureClientRequest',
'DeleteAzureClusterRequest',
'DeleteAzureNodePoolRequest',
'Fleet',
'GenerateAttachedClusterInstallManifestRequest',
'GenerateAttachedClusterInstallManifestResponse',
'GenerateAwsAccessTokenRequest',
'GenerateAwsAccessTokenResponse',
'GenerateAzureAccessTokenRequest',
'GenerateAzureAccessTokenResponse',
'GetAttachedClusterRequest',
'GetAttachedServerConfigRequest',
'GetAwsClusterRequest',
'GetAwsNodePoolRequest',
'GetAwsServerConfigRequest',
'GetAzureClientRequest',
'GetAzureClusterRequest',
'GetAzureNodePoolRequest',
'GetAzureServerConfigRequest',
'ImportAttachedClusterRequest',
'ListAttachedClustersRequest',
'ListAttachedClustersResponse',
'ListAwsClustersRequest',
'ListAwsClustersResponse',
'ListAwsNodePoolsRequest',
'ListAwsNodePoolsResponse',
'ListAzureClientsRequest',
'ListAzureClientsResponse',
'ListAzureClustersRequest',
'ListAzureClustersResponse',
'ListAzureNodePoolsRequest',
'ListAzureNodePoolsResponse',
'LoggingComponentConfig',
'LoggingConfig',
'ManagedPrometheusConfig',
'MaxPodsConstraint',
'MonitoringConfig',
'NodeTaint',
'OperationMetadata',
'ReplicaPlacement',
'UpdateAttachedClusterRequest',
'UpdateAwsClusterRequest',
'UpdateAwsNodePoolRequest',
'UpdateAzureClusterRequest',
'UpdateAzureNodePoolRequest',
'WorkloadIdentityConfig',
)
