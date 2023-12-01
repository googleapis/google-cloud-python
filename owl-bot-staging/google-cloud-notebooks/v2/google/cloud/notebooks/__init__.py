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
from google.cloud.notebooks import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.notebooks_v2.services.notebook_service.client import NotebookServiceClient
from google.cloud.notebooks_v2.services.notebook_service.async_client import NotebookServiceAsyncClient

from google.cloud.notebooks_v2.types.diagnostic_config import DiagnosticConfig
from google.cloud.notebooks_v2.types.event import Event
from google.cloud.notebooks_v2.types.gce_setup import AcceleratorConfig
from google.cloud.notebooks_v2.types.gce_setup import BootDisk
from google.cloud.notebooks_v2.types.gce_setup import ContainerImage
from google.cloud.notebooks_v2.types.gce_setup import DataDisk
from google.cloud.notebooks_v2.types.gce_setup import GceSetup
from google.cloud.notebooks_v2.types.gce_setup import GPUDriverConfig
from google.cloud.notebooks_v2.types.gce_setup import NetworkInterface
from google.cloud.notebooks_v2.types.gce_setup import ServiceAccount
from google.cloud.notebooks_v2.types.gce_setup import ShieldedInstanceConfig
from google.cloud.notebooks_v2.types.gce_setup import VmImage
from google.cloud.notebooks_v2.types.gce_setup import DiskEncryption
from google.cloud.notebooks_v2.types.gce_setup import DiskType
from google.cloud.notebooks_v2.types.instance import Instance
from google.cloud.notebooks_v2.types.instance import UpgradeHistoryEntry
from google.cloud.notebooks_v2.types.instance import HealthState
from google.cloud.notebooks_v2.types.instance import State
from google.cloud.notebooks_v2.types.service import CheckInstanceUpgradabilityRequest
from google.cloud.notebooks_v2.types.service import CheckInstanceUpgradabilityResponse
from google.cloud.notebooks_v2.types.service import CreateInstanceRequest
from google.cloud.notebooks_v2.types.service import DeleteInstanceRequest
from google.cloud.notebooks_v2.types.service import DiagnoseInstanceRequest
from google.cloud.notebooks_v2.types.service import GetInstanceRequest
from google.cloud.notebooks_v2.types.service import ListInstancesRequest
from google.cloud.notebooks_v2.types.service import ListInstancesResponse
from google.cloud.notebooks_v2.types.service import OperationMetadata
from google.cloud.notebooks_v2.types.service import ResetInstanceRequest
from google.cloud.notebooks_v2.types.service import RollbackInstanceRequest
from google.cloud.notebooks_v2.types.service import StartInstanceRequest
from google.cloud.notebooks_v2.types.service import StopInstanceRequest
from google.cloud.notebooks_v2.types.service import UpdateInstanceRequest
from google.cloud.notebooks_v2.types.service import UpgradeInstanceRequest

__all__ = ('NotebookServiceClient',
    'NotebookServiceAsyncClient',
    'DiagnosticConfig',
    'Event',
    'AcceleratorConfig',
    'BootDisk',
    'ContainerImage',
    'DataDisk',
    'GceSetup',
    'GPUDriverConfig',
    'NetworkInterface',
    'ServiceAccount',
    'ShieldedInstanceConfig',
    'VmImage',
    'DiskEncryption',
    'DiskType',
    'Instance',
    'UpgradeHistoryEntry',
    'HealthState',
    'State',
    'CheckInstanceUpgradabilityRequest',
    'CheckInstanceUpgradabilityResponse',
    'CreateInstanceRequest',
    'DeleteInstanceRequest',
    'DiagnoseInstanceRequest',
    'GetInstanceRequest',
    'ListInstancesRequest',
    'ListInstancesResponse',
    'OperationMetadata',
    'ResetInstanceRequest',
    'RollbackInstanceRequest',
    'StartInstanceRequest',
    'StopInstanceRequest',
    'UpdateInstanceRequest',
    'UpgradeInstanceRequest',
)
