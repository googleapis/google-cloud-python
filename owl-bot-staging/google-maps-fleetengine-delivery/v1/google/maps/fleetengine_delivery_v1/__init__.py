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
from google.maps.fleetengine_delivery_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.delivery_service import DeliveryServiceClient
from .services.delivery_service import DeliveryServiceAsyncClient

from .types.common import DeliveryVehicleAttribute
from .types.common import DeliveryVehicleLocation
from .types.common import TaskAttribute
from .types.common import TimeWindow
from .types.common import DeliveryVehicleLocationSensor
from .types.common import DeliveryVehicleNavigationStatus
from .types.delivery_api import BatchCreateTasksRequest
from .types.delivery_api import BatchCreateTasksResponse
from .types.delivery_api import CreateDeliveryVehicleRequest
from .types.delivery_api import CreateTaskRequest
from .types.delivery_api import GetDeliveryVehicleRequest
from .types.delivery_api import GetTaskRequest
from .types.delivery_api import GetTaskTrackingInfoRequest
from .types.delivery_api import ListDeliveryVehiclesRequest
from .types.delivery_api import ListDeliveryVehiclesResponse
from .types.delivery_api import ListTasksRequest
from .types.delivery_api import ListTasksResponse
from .types.delivery_api import SearchTasksRequest
from .types.delivery_api import SearchTasksResponse
from .types.delivery_api import UpdateDeliveryVehicleRequest
from .types.delivery_api import UpdateTaskRequest
from .types.delivery_vehicles import DeliveryVehicle
from .types.delivery_vehicles import LocationInfo
from .types.delivery_vehicles import VehicleJourneySegment
from .types.delivery_vehicles import VehicleStop
from .types.header import DeliveryRequestHeader
from .types.task_tracking_info import TaskTrackingInfo
from .types.tasks import Task
from .types.tasks import TaskTrackingViewConfig

__all__ = (
    'DeliveryServiceAsyncClient',
'BatchCreateTasksRequest',
'BatchCreateTasksResponse',
'CreateDeliveryVehicleRequest',
'CreateTaskRequest',
'DeliveryRequestHeader',
'DeliveryServiceClient',
'DeliveryVehicle',
'DeliveryVehicleAttribute',
'DeliveryVehicleLocation',
'DeliveryVehicleLocationSensor',
'DeliveryVehicleNavigationStatus',
'GetDeliveryVehicleRequest',
'GetTaskRequest',
'GetTaskTrackingInfoRequest',
'ListDeliveryVehiclesRequest',
'ListDeliveryVehiclesResponse',
'ListTasksRequest',
'ListTasksResponse',
'LocationInfo',
'SearchTasksRequest',
'SearchTasksResponse',
'Task',
'TaskAttribute',
'TaskTrackingInfo',
'TaskTrackingViewConfig',
'TimeWindow',
'UpdateDeliveryVehicleRequest',
'UpdateTaskRequest',
'VehicleJourneySegment',
'VehicleStop',
)
