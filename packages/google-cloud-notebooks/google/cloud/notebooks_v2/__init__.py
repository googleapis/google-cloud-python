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
from google.cloud.notebooks_v2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.notebook_service import NotebookServiceAsyncClient, NotebookServiceClient
from .types.diagnostic_config import DiagnosticConfig
from .types.event import Event
from .types.gce_setup import (
    AcceleratorConfig,
    BootDisk,
    ContainerImage,
    DataDisk,
    DiskEncryption,
    DiskType,
    GceSetup,
    GPUDriverConfig,
    NetworkInterface,
    ServiceAccount,
    ShieldedInstanceConfig,
    VmImage,
)
from .types.instance import HealthState, Instance, State, UpgradeHistoryEntry
from .types.service import (
    CheckInstanceUpgradabilityRequest,
    CheckInstanceUpgradabilityResponse,
    CreateInstanceRequest,
    DeleteInstanceRequest,
    DiagnoseInstanceRequest,
    GetInstanceRequest,
    ListInstancesRequest,
    ListInstancesResponse,
    OperationMetadata,
    ResetInstanceRequest,
    RollbackInstanceRequest,
    StartInstanceRequest,
    StopInstanceRequest,
    UpdateInstanceRequest,
    UpgradeInstanceRequest,
)

__all__ = (
    "NotebookServiceAsyncClient",
    "AcceleratorConfig",
    "BootDisk",
    "CheckInstanceUpgradabilityRequest",
    "CheckInstanceUpgradabilityResponse",
    "ContainerImage",
    "CreateInstanceRequest",
    "DataDisk",
    "DeleteInstanceRequest",
    "DiagnoseInstanceRequest",
    "DiagnosticConfig",
    "DiskEncryption",
    "DiskType",
    "Event",
    "GPUDriverConfig",
    "GceSetup",
    "GetInstanceRequest",
    "HealthState",
    "Instance",
    "ListInstancesRequest",
    "ListInstancesResponse",
    "NetworkInterface",
    "NotebookServiceClient",
    "OperationMetadata",
    "ResetInstanceRequest",
    "RollbackInstanceRequest",
    "ServiceAccount",
    "ShieldedInstanceConfig",
    "StartInstanceRequest",
    "State",
    "StopInstanceRequest",
    "UpdateInstanceRequest",
    "UpgradeHistoryEntry",
    "UpgradeInstanceRequest",
    "VmImage",
)
