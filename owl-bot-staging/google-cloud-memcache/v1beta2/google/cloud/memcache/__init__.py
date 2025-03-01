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
from google.cloud.memcache import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.memcache_v1beta2.services.cloud_memcache.client import CloudMemcacheClient
from google.cloud.memcache_v1beta2.services.cloud_memcache.async_client import CloudMemcacheAsyncClient

from google.cloud.memcache_v1beta2.types.cloud_memcache import ApplyParametersRequest
from google.cloud.memcache_v1beta2.types.cloud_memcache import ApplySoftwareUpdateRequest
from google.cloud.memcache_v1beta2.types.cloud_memcache import CreateInstanceRequest
from google.cloud.memcache_v1beta2.types.cloud_memcache import DeleteInstanceRequest
from google.cloud.memcache_v1beta2.types.cloud_memcache import GetInstanceRequest
from google.cloud.memcache_v1beta2.types.cloud_memcache import Instance
from google.cloud.memcache_v1beta2.types.cloud_memcache import ListInstancesRequest
from google.cloud.memcache_v1beta2.types.cloud_memcache import ListInstancesResponse
from google.cloud.memcache_v1beta2.types.cloud_memcache import LocationMetadata
from google.cloud.memcache_v1beta2.types.cloud_memcache import MaintenancePolicy
from google.cloud.memcache_v1beta2.types.cloud_memcache import MaintenanceSchedule
from google.cloud.memcache_v1beta2.types.cloud_memcache import MemcacheParameters
from google.cloud.memcache_v1beta2.types.cloud_memcache import OperationMetadata
from google.cloud.memcache_v1beta2.types.cloud_memcache import RescheduleMaintenanceRequest
from google.cloud.memcache_v1beta2.types.cloud_memcache import UpdateInstanceRequest
from google.cloud.memcache_v1beta2.types.cloud_memcache import UpdateParametersRequest
from google.cloud.memcache_v1beta2.types.cloud_memcache import WeeklyMaintenanceWindow
from google.cloud.memcache_v1beta2.types.cloud_memcache import ZoneMetadata
from google.cloud.memcache_v1beta2.types.cloud_memcache import MemcacheVersion

__all__ = ('CloudMemcacheClient',
    'CloudMemcacheAsyncClient',
    'ApplyParametersRequest',
    'ApplySoftwareUpdateRequest',
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
    'OperationMetadata',
    'RescheduleMaintenanceRequest',
    'UpdateInstanceRequest',
    'UpdateParametersRequest',
    'WeeklyMaintenanceWindow',
    'ZoneMetadata',
    'MemcacheVersion',
)
