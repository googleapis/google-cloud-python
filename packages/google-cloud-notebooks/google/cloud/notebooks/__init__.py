# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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

from google.cloud.notebooks_v1.services.managed_notebook_service.client import (
    ManagedNotebookServiceClient,
)
from google.cloud.notebooks_v1.services.managed_notebook_service.async_client import (
    ManagedNotebookServiceAsyncClient,
)
from google.cloud.notebooks_v1.services.notebook_service.client import (
    NotebookServiceClient,
)
from google.cloud.notebooks_v1.services.notebook_service.async_client import (
    NotebookServiceAsyncClient,
)

from google.cloud.notebooks_v1.types.environment import ContainerImage
from google.cloud.notebooks_v1.types.environment import Environment
from google.cloud.notebooks_v1.types.environment import VmImage
from google.cloud.notebooks_v1.types.event import Event
from google.cloud.notebooks_v1.types.execution import Execution
from google.cloud.notebooks_v1.types.execution import ExecutionTemplate
from google.cloud.notebooks_v1.types.instance import Instance
from google.cloud.notebooks_v1.types.instance import ReservationAffinity
from google.cloud.notebooks_v1.types.instance_config import InstanceConfig
from google.cloud.notebooks_v1.types.managed_service import CreateRuntimeRequest
from google.cloud.notebooks_v1.types.managed_service import DeleteRuntimeRequest
from google.cloud.notebooks_v1.types.managed_service import GetRuntimeRequest
from google.cloud.notebooks_v1.types.managed_service import ListRuntimesRequest
from google.cloud.notebooks_v1.types.managed_service import ListRuntimesResponse
from google.cloud.notebooks_v1.types.managed_service import ReportRuntimeEventRequest
from google.cloud.notebooks_v1.types.managed_service import ResetRuntimeRequest
from google.cloud.notebooks_v1.types.managed_service import StartRuntimeRequest
from google.cloud.notebooks_v1.types.managed_service import StopRuntimeRequest
from google.cloud.notebooks_v1.types.managed_service import SwitchRuntimeRequest
from google.cloud.notebooks_v1.types.runtime import EncryptionConfig
from google.cloud.notebooks_v1.types.runtime import LocalDisk
from google.cloud.notebooks_v1.types.runtime import LocalDiskInitializeParams
from google.cloud.notebooks_v1.types.runtime import Runtime
from google.cloud.notebooks_v1.types.runtime import RuntimeAcceleratorConfig
from google.cloud.notebooks_v1.types.runtime import RuntimeAccessConfig
from google.cloud.notebooks_v1.types.runtime import RuntimeMetrics
from google.cloud.notebooks_v1.types.runtime import RuntimeShieldedInstanceConfig
from google.cloud.notebooks_v1.types.runtime import RuntimeSoftwareConfig
from google.cloud.notebooks_v1.types.runtime import VirtualMachine
from google.cloud.notebooks_v1.types.runtime import VirtualMachineConfig
from google.cloud.notebooks_v1.types.schedule import Schedule
from google.cloud.notebooks_v1.types.service import CreateEnvironmentRequest
from google.cloud.notebooks_v1.types.service import CreateExecutionRequest
from google.cloud.notebooks_v1.types.service import CreateInstanceRequest
from google.cloud.notebooks_v1.types.service import CreateScheduleRequest
from google.cloud.notebooks_v1.types.service import DeleteEnvironmentRequest
from google.cloud.notebooks_v1.types.service import DeleteExecutionRequest
from google.cloud.notebooks_v1.types.service import DeleteInstanceRequest
from google.cloud.notebooks_v1.types.service import DeleteScheduleRequest
from google.cloud.notebooks_v1.types.service import GetEnvironmentRequest
from google.cloud.notebooks_v1.types.service import GetExecutionRequest
from google.cloud.notebooks_v1.types.service import GetInstanceHealthRequest
from google.cloud.notebooks_v1.types.service import GetInstanceHealthResponse
from google.cloud.notebooks_v1.types.service import GetInstanceRequest
from google.cloud.notebooks_v1.types.service import GetScheduleRequest
from google.cloud.notebooks_v1.types.service import IsInstanceUpgradeableRequest
from google.cloud.notebooks_v1.types.service import IsInstanceUpgradeableResponse
from google.cloud.notebooks_v1.types.service import ListEnvironmentsRequest
from google.cloud.notebooks_v1.types.service import ListEnvironmentsResponse
from google.cloud.notebooks_v1.types.service import ListExecutionsRequest
from google.cloud.notebooks_v1.types.service import ListExecutionsResponse
from google.cloud.notebooks_v1.types.service import ListInstancesRequest
from google.cloud.notebooks_v1.types.service import ListInstancesResponse
from google.cloud.notebooks_v1.types.service import ListSchedulesRequest
from google.cloud.notebooks_v1.types.service import ListSchedulesResponse
from google.cloud.notebooks_v1.types.service import OperationMetadata
from google.cloud.notebooks_v1.types.service import RegisterInstanceRequest
from google.cloud.notebooks_v1.types.service import ReportInstanceInfoRequest
from google.cloud.notebooks_v1.types.service import ResetInstanceRequest
from google.cloud.notebooks_v1.types.service import RollbackInstanceRequest
from google.cloud.notebooks_v1.types.service import SetInstanceAcceleratorRequest
from google.cloud.notebooks_v1.types.service import SetInstanceLabelsRequest
from google.cloud.notebooks_v1.types.service import SetInstanceMachineTypeRequest
from google.cloud.notebooks_v1.types.service import StartInstanceRequest
from google.cloud.notebooks_v1.types.service import StopInstanceRequest
from google.cloud.notebooks_v1.types.service import TriggerScheduleRequest
from google.cloud.notebooks_v1.types.service import UpdateInstanceConfigRequest
from google.cloud.notebooks_v1.types.service import UpdateShieldedInstanceConfigRequest
from google.cloud.notebooks_v1.types.service import UpgradeInstanceInternalRequest
from google.cloud.notebooks_v1.types.service import UpgradeInstanceRequest

__all__ = (
    "ManagedNotebookServiceClient",
    "ManagedNotebookServiceAsyncClient",
    "NotebookServiceClient",
    "NotebookServiceAsyncClient",
    "ContainerImage",
    "Environment",
    "VmImage",
    "Event",
    "Execution",
    "ExecutionTemplate",
    "Instance",
    "ReservationAffinity",
    "InstanceConfig",
    "CreateRuntimeRequest",
    "DeleteRuntimeRequest",
    "GetRuntimeRequest",
    "ListRuntimesRequest",
    "ListRuntimesResponse",
    "ReportRuntimeEventRequest",
    "ResetRuntimeRequest",
    "StartRuntimeRequest",
    "StopRuntimeRequest",
    "SwitchRuntimeRequest",
    "EncryptionConfig",
    "LocalDisk",
    "LocalDiskInitializeParams",
    "Runtime",
    "RuntimeAcceleratorConfig",
    "RuntimeAccessConfig",
    "RuntimeMetrics",
    "RuntimeShieldedInstanceConfig",
    "RuntimeSoftwareConfig",
    "VirtualMachine",
    "VirtualMachineConfig",
    "Schedule",
    "CreateEnvironmentRequest",
    "CreateExecutionRequest",
    "CreateInstanceRequest",
    "CreateScheduleRequest",
    "DeleteEnvironmentRequest",
    "DeleteExecutionRequest",
    "DeleteInstanceRequest",
    "DeleteScheduleRequest",
    "GetEnvironmentRequest",
    "GetExecutionRequest",
    "GetInstanceHealthRequest",
    "GetInstanceHealthResponse",
    "GetInstanceRequest",
    "GetScheduleRequest",
    "IsInstanceUpgradeableRequest",
    "IsInstanceUpgradeableResponse",
    "ListEnvironmentsRequest",
    "ListEnvironmentsResponse",
    "ListExecutionsRequest",
    "ListExecutionsResponse",
    "ListInstancesRequest",
    "ListInstancesResponse",
    "ListSchedulesRequest",
    "ListSchedulesResponse",
    "OperationMetadata",
    "RegisterInstanceRequest",
    "ReportInstanceInfoRequest",
    "ResetInstanceRequest",
    "RollbackInstanceRequest",
    "SetInstanceAcceleratorRequest",
    "SetInstanceLabelsRequest",
    "SetInstanceMachineTypeRequest",
    "StartInstanceRequest",
    "StopInstanceRequest",
    "TriggerScheduleRequest",
    "UpdateInstanceConfigRequest",
    "UpdateShieldedInstanceConfigRequest",
    "UpgradeInstanceInternalRequest",
    "UpgradeInstanceRequest",
)
