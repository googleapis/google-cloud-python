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

from .services.notebook_service import NotebookServiceClient
from .services.notebook_service import NotebookServiceAsyncClient

from .types.environment import ContainerImage
from .types.environment import Environment
from .types.environment import VmImage
from .types.instance import Instance
from .types.service import CreateEnvironmentRequest
from .types.service import CreateInstanceRequest
from .types.service import DeleteEnvironmentRequest
from .types.service import DeleteInstanceRequest
from .types.service import GetEnvironmentRequest
from .types.service import GetInstanceRequest
from .types.service import IsInstanceUpgradeableRequest
from .types.service import IsInstanceUpgradeableResponse
from .types.service import ListEnvironmentsRequest
from .types.service import ListEnvironmentsResponse
from .types.service import ListInstancesRequest
from .types.service import ListInstancesResponse
from .types.service import OperationMetadata
from .types.service import RegisterInstanceRequest
from .types.service import ReportInstanceInfoRequest
from .types.service import ResetInstanceRequest
from .types.service import SetInstanceAcceleratorRequest
from .types.service import SetInstanceLabelsRequest
from .types.service import SetInstanceMachineTypeRequest
from .types.service import StartInstanceRequest
from .types.service import StopInstanceRequest
from .types.service import UpgradeInstanceInternalRequest
from .types.service import UpgradeInstanceRequest

__all__ = (
    "NotebookServiceAsyncClient",
    "ContainerImage",
    "CreateEnvironmentRequest",
    "CreateInstanceRequest",
    "DeleteEnvironmentRequest",
    "DeleteInstanceRequest",
    "Environment",
    "GetEnvironmentRequest",
    "GetInstanceRequest",
    "Instance",
    "IsInstanceUpgradeableRequest",
    "IsInstanceUpgradeableResponse",
    "ListEnvironmentsRequest",
    "ListEnvironmentsResponse",
    "ListInstancesRequest",
    "ListInstancesResponse",
    "NotebookServiceClient",
    "OperationMetadata",
    "RegisterInstanceRequest",
    "ReportInstanceInfoRequest",
    "ResetInstanceRequest",
    "SetInstanceAcceleratorRequest",
    "SetInstanceLabelsRequest",
    "SetInstanceMachineTypeRequest",
    "StartInstanceRequest",
    "StopInstanceRequest",
    "UpgradeInstanceInternalRequest",
    "UpgradeInstanceRequest",
    "VmImage",
)
