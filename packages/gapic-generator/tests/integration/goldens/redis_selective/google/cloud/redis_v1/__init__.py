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
from google.cloud.redis_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.cloud_redis import CloudRedisClient
from .services.cloud_redis import CloudRedisAsyncClient

from .types.cloud_redis import CreateInstanceRequest
from .types.cloud_redis import DeleteInstanceRequest
from .types.cloud_redis import GetInstanceRequest
from .types.cloud_redis import Instance
from .types.cloud_redis import ListInstancesRequest
from .types.cloud_redis import ListInstancesResponse
from .types.cloud_redis import MaintenancePolicy
from .types.cloud_redis import MaintenanceSchedule
from .types.cloud_redis import NodeInfo
from .types.cloud_redis import OperationMetadata
from .types.cloud_redis import PersistenceConfig
from .types.cloud_redis import TlsCertificate
from .types.cloud_redis import UpdateInstanceRequest
from .types.cloud_redis import WeeklyMaintenanceWindow

__all__ = (
    'CloudRedisAsyncClient',
'CloudRedisClient',
'CreateInstanceRequest',
'DeleteInstanceRequest',
'GetInstanceRequest',
'Instance',
'ListInstancesRequest',
'ListInstancesResponse',
'MaintenancePolicy',
'MaintenanceSchedule',
'NodeInfo',
'OperationMetadata',
'PersistenceConfig',
'TlsCertificate',
'UpdateInstanceRequest',
'WeeklyMaintenanceWindow',
)
