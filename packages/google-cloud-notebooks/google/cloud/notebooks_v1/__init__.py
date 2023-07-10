# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.cloud.notebooks_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.managed_notebook_service import (
    ManagedNotebookServiceAsyncClient,
    ManagedNotebookServiceClient,
)
from .services.notebook_service import NotebookServiceAsyncClient, NotebookServiceClient
from .types.diagnostic_config import DiagnosticConfig
from .types.environment import ContainerImage, Environment, VmImage
from .types.event import Event
from .types.execution import Execution, ExecutionTemplate
from .types.instance import Instance, ReservationAffinity
from .types.instance_config import InstanceConfig
from .types.managed_service import (
    CreateRuntimeRequest,
    DeleteRuntimeRequest,
    DiagnoseRuntimeRequest,
    GetRuntimeRequest,
    ListRuntimesRequest,
    ListRuntimesResponse,
    RefreshRuntimeTokenInternalRequest,
    RefreshRuntimeTokenInternalResponse,
    ReportRuntimeEventRequest,
    ResetRuntimeRequest,
    StartRuntimeRequest,
    StopRuntimeRequest,
    SwitchRuntimeRequest,
    UpdateRuntimeRequest,
    UpgradeRuntimeRequest,
)
from .types.runtime import (
    EncryptionConfig,
    LocalDisk,
    LocalDiskInitializeParams,
    Runtime,
    RuntimeAcceleratorConfig,
    RuntimeAccessConfig,
    RuntimeMetrics,
    RuntimeShieldedInstanceConfig,
    RuntimeSoftwareConfig,
    VirtualMachine,
    VirtualMachineConfig,
)
from .types.schedule import Schedule
from .types.service import (
    CreateEnvironmentRequest,
    CreateExecutionRequest,
    CreateInstanceRequest,
    CreateScheduleRequest,
    DeleteEnvironmentRequest,
    DeleteExecutionRequest,
    DeleteInstanceRequest,
    DeleteScheduleRequest,
    DiagnoseInstanceRequest,
    GetEnvironmentRequest,
    GetExecutionRequest,
    GetInstanceHealthRequest,
    GetInstanceHealthResponse,
    GetInstanceRequest,
    GetScheduleRequest,
    IsInstanceUpgradeableRequest,
    IsInstanceUpgradeableResponse,
    ListEnvironmentsRequest,
    ListEnvironmentsResponse,
    ListExecutionsRequest,
    ListExecutionsResponse,
    ListInstancesRequest,
    ListInstancesResponse,
    ListSchedulesRequest,
    ListSchedulesResponse,
    OperationMetadata,
    RegisterInstanceRequest,
    ReportInstanceInfoRequest,
    ResetInstanceRequest,
    RollbackInstanceRequest,
    SetInstanceAcceleratorRequest,
    SetInstanceLabelsRequest,
    SetInstanceMachineTypeRequest,
    StartInstanceRequest,
    StopInstanceRequest,
    TriggerScheduleRequest,
    UpdateInstanceConfigRequest,
    UpdateInstanceMetadataItemsRequest,
    UpdateInstanceMetadataItemsResponse,
    UpdateShieldedInstanceConfigRequest,
    UpgradeInstanceInternalRequest,
    UpgradeInstanceRequest,
    UpgradeType,
)

__all__ = (
    "ManagedNotebookServiceAsyncClient",
    "NotebookServiceAsyncClient",
    "ContainerImage",
    "CreateEnvironmentRequest",
    "CreateExecutionRequest",
    "CreateInstanceRequest",
    "CreateRuntimeRequest",
    "CreateScheduleRequest",
    "DeleteEnvironmentRequest",
    "DeleteExecutionRequest",
    "DeleteInstanceRequest",
    "DeleteRuntimeRequest",
    "DeleteScheduleRequest",
    "DiagnoseInstanceRequest",
    "DiagnoseRuntimeRequest",
    "DiagnosticConfig",
    "EncryptionConfig",
    "Environment",
    "Event",
    "Execution",
    "ExecutionTemplate",
    "GetEnvironmentRequest",
    "GetExecutionRequest",
    "GetInstanceHealthRequest",
    "GetInstanceHealthResponse",
    "GetInstanceRequest",
    "GetRuntimeRequest",
    "GetScheduleRequest",
    "Instance",
    "InstanceConfig",
    "IsInstanceUpgradeableRequest",
    "IsInstanceUpgradeableResponse",
    "ListEnvironmentsRequest",
    "ListEnvironmentsResponse",
    "ListExecutionsRequest",
    "ListExecutionsResponse",
    "ListInstancesRequest",
    "ListInstancesResponse",
    "ListRuntimesRequest",
    "ListRuntimesResponse",
    "ListSchedulesRequest",
    "ListSchedulesResponse",
    "LocalDisk",
    "LocalDiskInitializeParams",
    "ManagedNotebookServiceClient",
    "NotebookServiceClient",
    "OperationMetadata",
    "RefreshRuntimeTokenInternalRequest",
    "RefreshRuntimeTokenInternalResponse",
    "RegisterInstanceRequest",
    "ReportInstanceInfoRequest",
    "ReportRuntimeEventRequest",
    "ReservationAffinity",
    "ResetInstanceRequest",
    "ResetRuntimeRequest",
    "RollbackInstanceRequest",
    "Runtime",
    "RuntimeAcceleratorConfig",
    "RuntimeAccessConfig",
    "RuntimeMetrics",
    "RuntimeShieldedInstanceConfig",
    "RuntimeSoftwareConfig",
    "Schedule",
    "SetInstanceAcceleratorRequest",
    "SetInstanceLabelsRequest",
    "SetInstanceMachineTypeRequest",
    "StartInstanceRequest",
    "StartRuntimeRequest",
    "StopInstanceRequest",
    "StopRuntimeRequest",
    "SwitchRuntimeRequest",
    "TriggerScheduleRequest",
    "UpdateInstanceConfigRequest",
    "UpdateInstanceMetadataItemsRequest",
    "UpdateInstanceMetadataItemsResponse",
    "UpdateRuntimeRequest",
    "UpdateShieldedInstanceConfigRequest",
    "UpgradeInstanceInternalRequest",
    "UpgradeInstanceRequest",
    "UpgradeRuntimeRequest",
    "UpgradeType",
    "VirtualMachine",
    "VirtualMachineConfig",
    "VmImage",
)
