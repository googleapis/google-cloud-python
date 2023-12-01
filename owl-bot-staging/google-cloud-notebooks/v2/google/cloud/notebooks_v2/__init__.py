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
from google.cloud.notebooks_v2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.notebook_service import NotebookServiceClient
from .services.notebook_service import NotebookServiceAsyncClient

from .types.diagnostic_config import DiagnosticConfig
from .types.event import Event
from .types.gce_setup import AcceleratorConfig
from .types.gce_setup import BootDisk
from .types.gce_setup import ContainerImage
from .types.gce_setup import DataDisk
from .types.gce_setup import GceSetup
from .types.gce_setup import GPUDriverConfig
from .types.gce_setup import NetworkInterface
from .types.gce_setup import ServiceAccount
from .types.gce_setup import ShieldedInstanceConfig
from .types.gce_setup import VmImage
from .types.gce_setup import DiskEncryption
from .types.gce_setup import DiskType
from .types.instance import Instance
from .types.instance import UpgradeHistoryEntry
from .types.instance import HealthState
from .types.instance import State
from .types.service import CheckInstanceUpgradabilityRequest
from .types.service import CheckInstanceUpgradabilityResponse
from .types.service import CreateInstanceRequest
from .types.service import DeleteInstanceRequest
from .types.service import DiagnoseInstanceRequest
from .types.service import GetInstanceRequest
from .types.service import ListInstancesRequest
from .types.service import ListInstancesResponse
from .types.service import OperationMetadata
from .types.service import ResetInstanceRequest
from .types.service import RollbackInstanceRequest
from .types.service import StartInstanceRequest
from .types.service import StopInstanceRequest
from .types.service import UpdateInstanceRequest
from .types.service import UpgradeInstanceRequest

__all__ = (
    'NotebookServiceAsyncClient',
'AcceleratorConfig',
'BootDisk',
'CheckInstanceUpgradabilityRequest',
'CheckInstanceUpgradabilityResponse',
'ContainerImage',
'CreateInstanceRequest',
'DataDisk',
'DeleteInstanceRequest',
'DiagnoseInstanceRequest',
'DiagnosticConfig',
'DiskEncryption',
'DiskType',
'Event',
'GPUDriverConfig',
'GceSetup',
'GetInstanceRequest',
'HealthState',
'Instance',
'ListInstancesRequest',
'ListInstancesResponse',
'NetworkInterface',
'NotebookServiceClient',
'OperationMetadata',
'ResetInstanceRequest',
'RollbackInstanceRequest',
'ServiceAccount',
'ShieldedInstanceConfig',
'StartInstanceRequest',
'State',
'StopInstanceRequest',
'UpdateInstanceRequest',
'UpgradeHistoryEntry',
'UpgradeInstanceRequest',
'VmImage',
)
