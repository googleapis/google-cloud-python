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
from google.cloud.tpu import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.tpu_v2.services.tpu.client import TpuClient
from google.cloud.tpu_v2.services.tpu.async_client import TpuAsyncClient

from google.cloud.tpu_v2.types.cloud_tpu import AcceleratorConfig
from google.cloud.tpu_v2.types.cloud_tpu import AcceleratorType
from google.cloud.tpu_v2.types.cloud_tpu import AccessConfig
from google.cloud.tpu_v2.types.cloud_tpu import AttachedDisk
from google.cloud.tpu_v2.types.cloud_tpu import CreateNodeRequest
from google.cloud.tpu_v2.types.cloud_tpu import DeleteNodeRequest
from google.cloud.tpu_v2.types.cloud_tpu import GenerateServiceIdentityRequest
from google.cloud.tpu_v2.types.cloud_tpu import GenerateServiceIdentityResponse
from google.cloud.tpu_v2.types.cloud_tpu import GetAcceleratorTypeRequest
from google.cloud.tpu_v2.types.cloud_tpu import GetGuestAttributesRequest
from google.cloud.tpu_v2.types.cloud_tpu import GetGuestAttributesResponse
from google.cloud.tpu_v2.types.cloud_tpu import GetNodeRequest
from google.cloud.tpu_v2.types.cloud_tpu import GetRuntimeVersionRequest
from google.cloud.tpu_v2.types.cloud_tpu import GuestAttributes
from google.cloud.tpu_v2.types.cloud_tpu import GuestAttributesEntry
from google.cloud.tpu_v2.types.cloud_tpu import GuestAttributesValue
from google.cloud.tpu_v2.types.cloud_tpu import ListAcceleratorTypesRequest
from google.cloud.tpu_v2.types.cloud_tpu import ListAcceleratorTypesResponse
from google.cloud.tpu_v2.types.cloud_tpu import ListNodesRequest
from google.cloud.tpu_v2.types.cloud_tpu import ListNodesResponse
from google.cloud.tpu_v2.types.cloud_tpu import ListRuntimeVersionsRequest
from google.cloud.tpu_v2.types.cloud_tpu import ListRuntimeVersionsResponse
from google.cloud.tpu_v2.types.cloud_tpu import NetworkConfig
from google.cloud.tpu_v2.types.cloud_tpu import NetworkEndpoint
from google.cloud.tpu_v2.types.cloud_tpu import Node
from google.cloud.tpu_v2.types.cloud_tpu import OperationMetadata
from google.cloud.tpu_v2.types.cloud_tpu import RuntimeVersion
from google.cloud.tpu_v2.types.cloud_tpu import SchedulingConfig
from google.cloud.tpu_v2.types.cloud_tpu import ServiceAccount
from google.cloud.tpu_v2.types.cloud_tpu import ServiceIdentity
from google.cloud.tpu_v2.types.cloud_tpu import ShieldedInstanceConfig
from google.cloud.tpu_v2.types.cloud_tpu import StartNodeRequest
from google.cloud.tpu_v2.types.cloud_tpu import StopNodeRequest
from google.cloud.tpu_v2.types.cloud_tpu import Symptom
from google.cloud.tpu_v2.types.cloud_tpu import UpdateNodeRequest

__all__ = ('TpuClient',
    'TpuAsyncClient',
    'AcceleratorConfig',
    'AcceleratorType',
    'AccessConfig',
    'AttachedDisk',
    'CreateNodeRequest',
    'DeleteNodeRequest',
    'GenerateServiceIdentityRequest',
    'GenerateServiceIdentityResponse',
    'GetAcceleratorTypeRequest',
    'GetGuestAttributesRequest',
    'GetGuestAttributesResponse',
    'GetNodeRequest',
    'GetRuntimeVersionRequest',
    'GuestAttributes',
    'GuestAttributesEntry',
    'GuestAttributesValue',
    'ListAcceleratorTypesRequest',
    'ListAcceleratorTypesResponse',
    'ListNodesRequest',
    'ListNodesResponse',
    'ListRuntimeVersionsRequest',
    'ListRuntimeVersionsResponse',
    'NetworkConfig',
    'NetworkEndpoint',
    'Node',
    'OperationMetadata',
    'RuntimeVersion',
    'SchedulingConfig',
    'ServiceAccount',
    'ServiceIdentity',
    'ShieldedInstanceConfig',
    'StartNodeRequest',
    'StopNodeRequest',
    'Symptom',
    'UpdateNodeRequest',
)
