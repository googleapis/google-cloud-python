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
from google.maps.fleetengine_delivery import gapic_version as package_version

__version__ = package_version.__version__


from google.maps.fleetengine_delivery_v1.services.delivery_service.client import DeliveryServiceClient
from google.maps.fleetengine_delivery_v1.services.delivery_service.async_client import DeliveryServiceAsyncClient

from google.maps.fleetengine_delivery_v1.types.common import DeliveryVehicleAttribute
from google.maps.fleetengine_delivery_v1.types.common import DeliveryVehicleLocation
from google.maps.fleetengine_delivery_v1.types.common import TaskAttribute
from google.maps.fleetengine_delivery_v1.types.common import TimeWindow
from google.maps.fleetengine_delivery_v1.types.common import DeliveryVehicleLocationSensor
from google.maps.fleetengine_delivery_v1.types.common import DeliveryVehicleNavigationStatus
from google.maps.fleetengine_delivery_v1.types.delivery_api import BatchCreateTasksRequest
from google.maps.fleetengine_delivery_v1.types.delivery_api import BatchCreateTasksResponse
from google.maps.fleetengine_delivery_v1.types.delivery_api import CreateDeliveryVehicleRequest
from google.maps.fleetengine_delivery_v1.types.delivery_api import CreateTaskRequest
from google.maps.fleetengine_delivery_v1.types.delivery_api import GetDeliveryVehicleRequest
from google.maps.fleetengine_delivery_v1.types.delivery_api import GetTaskRequest
from google.maps.fleetengine_delivery_v1.types.delivery_api import GetTaskTrackingInfoRequest
from google.maps.fleetengine_delivery_v1.types.delivery_api import ListDeliveryVehiclesRequest
from google.maps.fleetengine_delivery_v1.types.delivery_api import ListDeliveryVehiclesResponse
from google.maps.fleetengine_delivery_v1.types.delivery_api import ListTasksRequest
from google.maps.fleetengine_delivery_v1.types.delivery_api import ListTasksResponse
from google.maps.fleetengine_delivery_v1.types.delivery_api import SearchTasksRequest
from google.maps.fleetengine_delivery_v1.types.delivery_api import SearchTasksResponse
from google.maps.fleetengine_delivery_v1.types.delivery_api import UpdateDeliveryVehicleRequest
from google.maps.fleetengine_delivery_v1.types.delivery_api import UpdateTaskRequest
from google.maps.fleetengine_delivery_v1.types.delivery_vehicles import DeliveryVehicle
from google.maps.fleetengine_delivery_v1.types.delivery_vehicles import LocationInfo
from google.maps.fleetengine_delivery_v1.types.delivery_vehicles import VehicleJourneySegment
from google.maps.fleetengine_delivery_v1.types.delivery_vehicles import VehicleStop
from google.maps.fleetengine_delivery_v1.types.header import DeliveryRequestHeader
from google.maps.fleetengine_delivery_v1.types.task_tracking_info import TaskTrackingInfo
from google.maps.fleetengine_delivery_v1.types.tasks import Task
from google.maps.fleetengine_delivery_v1.types.tasks import TaskTrackingViewConfig

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
