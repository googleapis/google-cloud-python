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
from google.cloud.tpu_v2alpha1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.tpu import TpuAsyncClient, TpuClient
from .types.cloud_tpu import (
    AcceleratorConfig,
    AcceleratorType,
    AccessConfig,
    AttachedDisk,
    BootDiskConfig,
    CreateNodeRequest,
    CreateQueuedResourceRequest,
    CustomerEncryptionKey,
    DeleteNodeRequest,
    DeleteQueuedResourceRequest,
    GenerateServiceIdentityRequest,
    GenerateServiceIdentityResponse,
    GetAcceleratorTypeRequest,
    GetGuestAttributesRequest,
    GetGuestAttributesResponse,
    GetNodeRequest,
    GetQueuedResourceRequest,
    GetRuntimeVersionRequest,
    GuestAttributes,
    GuestAttributesEntry,
    GuestAttributesValue,
    ListAcceleratorTypesRequest,
    ListAcceleratorTypesResponse,
    ListNodesRequest,
    ListNodesResponse,
    ListQueuedResourcesRequest,
    ListQueuedResourcesResponse,
    ListRuntimeVersionsRequest,
    ListRuntimeVersionsResponse,
    NetworkConfig,
    NetworkEndpoint,
    Node,
    OperationMetadata,
    QueuedResource,
    QueuedResourceState,
    ResetQueuedResourceRequest,
    RuntimeVersion,
    SchedulingConfig,
    ServiceAccount,
    ServiceIdentity,
    ShieldedInstanceConfig,
    SimulateMaintenanceEventRequest,
    StartNodeRequest,
    StopNodeRequest,
    Symptom,
    UpdateNodeRequest,
)

__all__ = (
    "TpuAsyncClient",
    "AcceleratorConfig",
    "AcceleratorType",
    "AccessConfig",
    "AttachedDisk",
    "BootDiskConfig",
    "CreateNodeRequest",
    "CreateQueuedResourceRequest",
    "CustomerEncryptionKey",
    "DeleteNodeRequest",
    "DeleteQueuedResourceRequest",
    "GenerateServiceIdentityRequest",
    "GenerateServiceIdentityResponse",
    "GetAcceleratorTypeRequest",
    "GetGuestAttributesRequest",
    "GetGuestAttributesResponse",
    "GetNodeRequest",
    "GetQueuedResourceRequest",
    "GetRuntimeVersionRequest",
    "GuestAttributes",
    "GuestAttributesEntry",
    "GuestAttributesValue",
    "ListAcceleratorTypesRequest",
    "ListAcceleratorTypesResponse",
    "ListNodesRequest",
    "ListNodesResponse",
    "ListQueuedResourcesRequest",
    "ListQueuedResourcesResponse",
    "ListRuntimeVersionsRequest",
    "ListRuntimeVersionsResponse",
    "NetworkConfig",
    "NetworkEndpoint",
    "Node",
    "OperationMetadata",
    "QueuedResource",
    "QueuedResourceState",
    "ResetQueuedResourceRequest",
    "RuntimeVersion",
    "SchedulingConfig",
    "ServiceAccount",
    "ServiceIdentity",
    "ShieldedInstanceConfig",
    "SimulateMaintenanceEventRequest",
    "StartNodeRequest",
    "StopNodeRequest",
    "Symptom",
    "TpuClient",
    "UpdateNodeRequest",
)
