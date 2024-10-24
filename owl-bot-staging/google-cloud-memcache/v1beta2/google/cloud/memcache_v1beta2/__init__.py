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
from google.cloud.memcache_v1beta2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.cloud_memcache import CloudMemcacheClient
from .services.cloud_memcache import CloudMemcacheAsyncClient

from .types.cloud_memcache import ApplyParametersRequest
from .types.cloud_memcache import ApplySoftwareUpdateRequest
from .types.cloud_memcache import CreateInstanceRequest
from .types.cloud_memcache import DeleteInstanceRequest
from .types.cloud_memcache import GetInstanceRequest
from .types.cloud_memcache import Instance
from .types.cloud_memcache import ListInstancesRequest
from .types.cloud_memcache import ListInstancesResponse
from .types.cloud_memcache import LocationMetadata
from .types.cloud_memcache import MaintenancePolicy
from .types.cloud_memcache import MaintenanceSchedule
from .types.cloud_memcache import MemcacheParameters
from .types.cloud_memcache import OperationMetadata
from .types.cloud_memcache import RescheduleMaintenanceRequest
from .types.cloud_memcache import UpdateInstanceRequest
from .types.cloud_memcache import UpdateParametersRequest
from .types.cloud_memcache import WeeklyMaintenanceWindow
from .types.cloud_memcache import ZoneMetadata
from .types.cloud_memcache import MemcacheVersion

__all__ = (
    'CloudMemcacheAsyncClient',
'ApplyParametersRequest',
'ApplySoftwareUpdateRequest',
'CloudMemcacheClient',
'CreateInstanceRequest',
'DeleteInstanceRequest',
'GetInstanceRequest',
'Instance',
'ListInstancesRequest',
'ListInstancesResponse',
'LocationMetadata',
'MaintenancePolicy',
'MaintenanceSchedule',
'MemcacheParameters',
'MemcacheVersion',
'OperationMetadata',
'RescheduleMaintenanceRequest',
'UpdateInstanceRequest',
'UpdateParametersRequest',
'WeeklyMaintenanceWindow',
'ZoneMetadata',
)
