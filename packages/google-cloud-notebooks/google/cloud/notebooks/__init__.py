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

from google.cloud.notebooks_v1beta1.services.notebook_service.client import (
    NotebookServiceClient,
)
from google.cloud.notebooks_v1beta1.services.notebook_service.async_client import (
    NotebookServiceAsyncClient,
)

from google.cloud.notebooks_v1beta1.types.environment import ContainerImage
from google.cloud.notebooks_v1beta1.types.environment import Environment
from google.cloud.notebooks_v1beta1.types.environment import VmImage
from google.cloud.notebooks_v1beta1.types.instance import Instance
from google.cloud.notebooks_v1beta1.types.service import CreateEnvironmentRequest
from google.cloud.notebooks_v1beta1.types.service import CreateInstanceRequest
from google.cloud.notebooks_v1beta1.types.service import DeleteEnvironmentRequest
from google.cloud.notebooks_v1beta1.types.service import DeleteInstanceRequest
from google.cloud.notebooks_v1beta1.types.service import GetEnvironmentRequest
from google.cloud.notebooks_v1beta1.types.service import GetInstanceRequest
from google.cloud.notebooks_v1beta1.types.service import IsInstanceUpgradeableRequest
from google.cloud.notebooks_v1beta1.types.service import IsInstanceUpgradeableResponse
from google.cloud.notebooks_v1beta1.types.service import ListEnvironmentsRequest
from google.cloud.notebooks_v1beta1.types.service import ListEnvironmentsResponse
from google.cloud.notebooks_v1beta1.types.service import ListInstancesRequest
from google.cloud.notebooks_v1beta1.types.service import ListInstancesResponse
from google.cloud.notebooks_v1beta1.types.service import OperationMetadata
from google.cloud.notebooks_v1beta1.types.service import RegisterInstanceRequest
from google.cloud.notebooks_v1beta1.types.service import ReportInstanceInfoRequest
from google.cloud.notebooks_v1beta1.types.service import ResetInstanceRequest
from google.cloud.notebooks_v1beta1.types.service import SetInstanceAcceleratorRequest
from google.cloud.notebooks_v1beta1.types.service import SetInstanceLabelsRequest
from google.cloud.notebooks_v1beta1.types.service import SetInstanceMachineTypeRequest
from google.cloud.notebooks_v1beta1.types.service import StartInstanceRequest
from google.cloud.notebooks_v1beta1.types.service import StopInstanceRequest
from google.cloud.notebooks_v1beta1.types.service import UpgradeInstanceInternalRequest
from google.cloud.notebooks_v1beta1.types.service import UpgradeInstanceRequest

__all__ = (
    "NotebookServiceClient",
    "NotebookServiceAsyncClient",
    "ContainerImage",
    "Environment",
    "VmImage",
    "Instance",
    "CreateEnvironmentRequest",
    "CreateInstanceRequest",
    "DeleteEnvironmentRequest",
    "DeleteInstanceRequest",
    "GetEnvironmentRequest",
    "GetInstanceRequest",
    "IsInstanceUpgradeableRequest",
    "IsInstanceUpgradeableResponse",
    "ListEnvironmentsRequest",
    "ListEnvironmentsResponse",
    "ListInstancesRequest",
    "ListInstancesResponse",
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
)
