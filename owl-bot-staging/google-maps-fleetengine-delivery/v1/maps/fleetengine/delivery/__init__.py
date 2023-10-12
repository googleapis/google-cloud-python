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
from maps.fleetengine.delivery import gapic_version as package_version

__version__ = package_version.__version__


from maps.fleetengine.delivery_v1.services.delivery_service.client import DeliveryServiceClient
from maps.fleetengine.delivery_v1.services.delivery_service.async_client import DeliveryServiceAsyncClient

from maps.fleetengine.delivery_v1.types.common import DeliveryVehicleAttribute
from maps.fleetengine.delivery_v1.types.common import DeliveryVehicleLocation
from maps.fleetengine.delivery_v1.types.common import TaskAttribute
from maps.fleetengine.delivery_v1.types.common import TimeWindow
from maps.fleetengine.delivery_v1.types.common import DeliveryVehicleLocationSensor
from maps.fleetengine.delivery_v1.types.common import DeliveryVehicleNavigationStatus
from maps.fleetengine.delivery_v1.types.delivery_api import BatchCreateTasksRequest
from maps.fleetengine.delivery_v1.types.delivery_api import BatchCreateTasksResponse
from maps.fleetengine.delivery_v1.types.delivery_api import CreateDeliveryVehicleRequest
from maps.fleetengine.delivery_v1.types.delivery_api import CreateTaskRequest
from maps.fleetengine.delivery_v1.types.delivery_api import GetDeliveryVehicleRequest
from maps.fleetengine.delivery_v1.types.delivery_api import GetTaskRequest
from maps.fleetengine.delivery_v1.types.delivery_api import GetTaskTrackingInfoRequest
from maps.fleetengine.delivery_v1.types.delivery_api import ListDeliveryVehiclesRequest
from maps.fleetengine.delivery_v1.types.delivery_api import ListDeliveryVehiclesResponse
from maps.fleetengine.delivery_v1.types.delivery_api import ListTasksRequest
from maps.fleetengine.delivery_v1.types.delivery_api import ListTasksResponse
from maps.fleetengine.delivery_v1.types.delivery_api import SearchTasksRequest
from maps.fleetengine.delivery_v1.types.delivery_api import SearchTasksResponse
from maps.fleetengine.delivery_v1.types.delivery_api import UpdateDeliveryVehicleRequest
from maps.fleetengine.delivery_v1.types.delivery_api import UpdateTaskRequest
from maps.fleetengine.delivery_v1.types.delivery_vehicles import DeliveryVehicle
from maps.fleetengine.delivery_v1.types.delivery_vehicles import LocationInfo
from maps.fleetengine.delivery_v1.types.delivery_vehicles import VehicleJourneySegment
from maps.fleetengine.delivery_v1.types.delivery_vehicles import VehicleStop
from maps.fleetengine.delivery_v1.types.header import DeliveryRequestHeader
from maps.fleetengine.delivery_v1.types.task_tracking_info import TaskTrackingInfo
from maps.fleetengine.delivery_v1.types.tasks import Task
from maps.fleetengine.delivery_v1.types.tasks import TaskTrackingViewConfig

__all__ = ('DeliveryServiceClient',
    'DeliveryServiceAsyncClient',
    'DeliveryVehicleAttribute',
    'DeliveryVehicleLocation',
    'TaskAttribute',
    'TimeWindow',
    'DeliveryVehicleLocationSensor',
    'DeliveryVehicleNavigationStatus',
    'BatchCreateTasksRequest',
    'BatchCreateTasksResponse',
    'CreateDeliveryVehicleRequest',
    'CreateTaskRequest',
    'GetDeliveryVehicleRequest',
    'GetTaskRequest',
    'GetTaskTrackingInfoRequest',
    'ListDeliveryVehiclesRequest',
    'ListDeliveryVehiclesResponse',
    'ListTasksRequest',
    'ListTasksResponse',
    'SearchTasksRequest',
    'SearchTasksResponse',
    'UpdateDeliveryVehicleRequest',
    'UpdateTaskRequest',
    'DeliveryVehicle',
    'LocationInfo',
    'VehicleJourneySegment',
    'VehicleStop',
    'DeliveryRequestHeader',
    'TaskTrackingInfo',
    'Task',
    'TaskTrackingViewConfig',
)
