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
from google.cloud.data_fusion_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.data_fusion import DataFusionAsyncClient, DataFusionClient
from .types.datafusion import (
    Accelerator,
    CreateInstanceRequest,
    CryptoKeyConfig,
    DeleteInstanceRequest,
    GetInstanceRequest,
    Instance,
    ListAvailableVersionsRequest,
    ListAvailableVersionsResponse,
    ListInstancesRequest,
    ListInstancesResponse,
    NetworkConfig,
    OperationMetadata,
    RestartInstanceRequest,
    UpdateInstanceRequest,
    Version,
)

__all__ = (
    "DataFusionAsyncClient",
    "Accelerator",
    "CreateInstanceRequest",
    "CryptoKeyConfig",
    "DataFusionClient",
    "DeleteInstanceRequest",
    "GetInstanceRequest",
    "Instance",
    "ListAvailableVersionsRequest",
    "ListAvailableVersionsResponse",
    "ListInstancesRequest",
    "ListInstancesResponse",
    "NetworkConfig",
    "OperationMetadata",
    "RestartInstanceRequest",
    "UpdateInstanceRequest",
    "Version",
)
