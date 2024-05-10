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
from google.maps.fleetengine_delivery_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.delivery_service import DeliveryServiceAsyncClient, DeliveryServiceClient
from .types.common import (
    DeliveryVehicleAttribute,
    DeliveryVehicleLocation,
    DeliveryVehicleLocationSensor,
    DeliveryVehicleNavigationStatus,
    TaskAttribute,
    TimeWindow,
)
from .types.delivery_api import (
    BatchCreateTasksRequest,
    BatchCreateTasksResponse,
    CreateDeliveryVehicleRequest,
    CreateTaskRequest,
    GetDeliveryVehicleRequest,
    GetTaskRequest,
    GetTaskTrackingInfoRequest,
    ListDeliveryVehiclesRequest,
    ListDeliveryVehiclesResponse,
    ListTasksRequest,
    ListTasksResponse,
    UpdateDeliveryVehicleRequest,
    UpdateTaskRequest,
)
from .types.delivery_vehicles import (
    DeliveryVehicle,
    LocationInfo,
    VehicleJourneySegment,
    VehicleStop,
)
from .types.header import DeliveryRequestHeader
from .types.task_tracking_info import TaskTrackingInfo
from .types.tasks import Task, TaskTrackingViewConfig

__all__ = (
    "DeliveryServiceAsyncClient",
    "BatchCreateTasksRequest",
    "BatchCreateTasksResponse",
    "CreateDeliveryVehicleRequest",
    "CreateTaskRequest",
    "DeliveryRequestHeader",
    "DeliveryServiceClient",
    "DeliveryVehicle",
    "DeliveryVehicleAttribute",
    "DeliveryVehicleLocation",
    "DeliveryVehicleLocationSensor",
    "DeliveryVehicleNavigationStatus",
    "GetDeliveryVehicleRequest",
    "GetTaskRequest",
    "GetTaskTrackingInfoRequest",
    "ListDeliveryVehiclesRequest",
    "ListDeliveryVehiclesResponse",
    "ListTasksRequest",
    "ListTasksResponse",
    "LocationInfo",
    "Task",
    "TaskAttribute",
    "TaskTrackingInfo",
    "TaskTrackingViewConfig",
    "TimeWindow",
    "UpdateDeliveryVehicleRequest",
    "UpdateTaskRequest",
    "VehicleJourneySegment",
    "VehicleStop",
)
