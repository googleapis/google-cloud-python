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
from google.cloud.hypercomputecluster import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.hypercomputecluster_v1beta.services.hypercompute_cluster.async_client import (
    HypercomputeClusterAsyncClient,
)
from google.cloud.hypercomputecluster_v1beta.services.hypercompute_cluster.client import (
    HypercomputeClusterClient,
)
from google.cloud.hypercomputecluster_v1beta.types.hypercompute_cluster import (
    BootDisk,
    BucketReference,
    Cluster,
    ComputeInstance,
    ComputeInstanceSlurmNodeSet,
    ComputeResource,
    ComputeResourceConfig,
    CreateClusterRequest,
    DeleteClusterRequest,
    ExistingBucketConfig,
    ExistingFilestoreConfig,
    ExistingLustreConfig,
    ExistingNetworkConfig,
    FileShareConfig,
    FilestoreReference,
    GcsAutoclassConfig,
    GcsHierarchicalNamespaceConfig,
    GetClusterRequest,
    ListClustersRequest,
    ListClustersResponse,
    LustreReference,
    NetworkReference,
    NetworkResource,
    NetworkResourceConfig,
    NewBucketConfig,
    NewFilestoreConfig,
    NewFlexStartInstancesConfig,
    NewLustreConfig,
    NewNetworkConfig,
    NewOnDemandInstancesConfig,
    NewReservedInstancesConfig,
    NewSpotInstancesConfig,
    Orchestrator,
    SlurmLoginNodes,
    SlurmNodeSet,
    SlurmOrchestrator,
    SlurmPartition,
    StorageConfig,
    StorageResource,
    StorageResourceConfig,
    UpdateClusterRequest,
)
from google.cloud.hypercomputecluster_v1beta.types.operation_metadata import (
    OperationMetadata,
)

__all__ = (
    "HypercomputeClusterClient",
    "HypercomputeClusterAsyncClient",
    "BootDisk",
    "BucketReference",
    "Cluster",
    "ComputeInstance",
    "ComputeInstanceSlurmNodeSet",
    "ComputeResource",
    "ComputeResourceConfig",
    "CreateClusterRequest",
    "DeleteClusterRequest",
    "ExistingBucketConfig",
    "ExistingFilestoreConfig",
    "ExistingLustreConfig",
    "ExistingNetworkConfig",
    "FileShareConfig",
    "FilestoreReference",
    "GcsAutoclassConfig",
    "GcsHierarchicalNamespaceConfig",
    "GetClusterRequest",
    "ListClustersRequest",
    "ListClustersResponse",
    "LustreReference",
    "NetworkReference",
    "NetworkResource",
    "NetworkResourceConfig",
    "NewBucketConfig",
    "NewFilestoreConfig",
    "NewFlexStartInstancesConfig",
    "NewLustreConfig",
    "NewNetworkConfig",
    "NewOnDemandInstancesConfig",
    "NewReservedInstancesConfig",
    "NewSpotInstancesConfig",
    "Orchestrator",
    "SlurmLoginNodes",
    "SlurmNodeSet",
    "SlurmOrchestrator",
    "SlurmPartition",
    "StorageConfig",
    "StorageResource",
    "StorageResourceConfig",
    "UpdateClusterRequest",
    "OperationMetadata",
)
