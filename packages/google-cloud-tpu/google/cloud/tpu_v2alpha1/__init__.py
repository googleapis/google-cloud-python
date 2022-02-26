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

from .services.tpu import TpuClient
from .services.tpu import TpuAsyncClient

from .types.cloud_tpu import AcceleratorType
from .types.cloud_tpu import AccessConfig
from .types.cloud_tpu import AttachedDisk
from .types.cloud_tpu import CreateNodeRequest
from .types.cloud_tpu import DeleteNodeRequest
from .types.cloud_tpu import GenerateServiceIdentityRequest
from .types.cloud_tpu import GenerateServiceIdentityResponse
from .types.cloud_tpu import GetAcceleratorTypeRequest
from .types.cloud_tpu import GetGuestAttributesRequest
from .types.cloud_tpu import GetGuestAttributesResponse
from .types.cloud_tpu import GetNodeRequest
from .types.cloud_tpu import GetRuntimeVersionRequest
from .types.cloud_tpu import GuestAttributes
from .types.cloud_tpu import GuestAttributesEntry
from .types.cloud_tpu import GuestAttributesValue
from .types.cloud_tpu import ListAcceleratorTypesRequest
from .types.cloud_tpu import ListAcceleratorTypesResponse
from .types.cloud_tpu import ListNodesRequest
from .types.cloud_tpu import ListNodesResponse
from .types.cloud_tpu import ListRuntimeVersionsRequest
from .types.cloud_tpu import ListRuntimeVersionsResponse
from .types.cloud_tpu import NetworkConfig
from .types.cloud_tpu import NetworkEndpoint
from .types.cloud_tpu import Node
from .types.cloud_tpu import OperationMetadata
from .types.cloud_tpu import RuntimeVersion
from .types.cloud_tpu import SchedulingConfig
from .types.cloud_tpu import ServiceAccount
from .types.cloud_tpu import ServiceIdentity
from .types.cloud_tpu import StartNodeRequest
from .types.cloud_tpu import StopNodeRequest
from .types.cloud_tpu import Symptom
from .types.cloud_tpu import UpdateNodeRequest

__all__ = (
    "TpuAsyncClient",
    "AcceleratorType",
    "AccessConfig",
    "AttachedDisk",
    "CreateNodeRequest",
    "DeleteNodeRequest",
    "GenerateServiceIdentityRequest",
    "GenerateServiceIdentityResponse",
    "GetAcceleratorTypeRequest",
    "GetGuestAttributesRequest",
    "GetGuestAttributesResponse",
    "GetNodeRequest",
    "GetRuntimeVersionRequest",
    "GuestAttributes",
    "GuestAttributesEntry",
    "GuestAttributesValue",
    "ListAcceleratorTypesRequest",
    "ListAcceleratorTypesResponse",
    "ListNodesRequest",
    "ListNodesResponse",
    "ListRuntimeVersionsRequest",
    "ListRuntimeVersionsResponse",
    "NetworkConfig",
    "NetworkEndpoint",
    "Node",
    "OperationMetadata",
    "RuntimeVersion",
    "SchedulingConfig",
    "ServiceAccount",
    "ServiceIdentity",
    "StartNodeRequest",
    "StopNodeRequest",
    "Symptom",
    "TpuClient",
    "UpdateNodeRequest",
)
