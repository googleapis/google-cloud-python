# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from google.cloud.capacityplanner import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.capacityplanner_v1beta.services.capacity_planning_service.client import CapacityPlanningServiceClient
from google.cloud.capacityplanner_v1beta.services.capacity_planning_service.async_client import CapacityPlanningServiceAsyncClient
from google.cloud.capacityplanner_v1beta.services.usage_service.client import UsageServiceClient
from google.cloud.capacityplanner_v1beta.services.usage_service.async_client import UsageServiceAsyncClient

from google.cloud.capacityplanner_v1beta.types.allocation import Allocation
from google.cloud.capacityplanner_v1beta.types.capacity_planning_service import CapacityPlan
from google.cloud.capacityplanner_v1beta.types.capacity_planning_service import CapacityPlanFilters
from google.cloud.capacityplanner_v1beta.types.capacity_planning_service import CapacityPlanKey
from google.cloud.capacityplanner_v1beta.types.capacity_planning_service import CapacityPlanView
from google.cloud.capacityplanner_v1beta.types.capacity_planning_service import ChildResourceDemand
from google.cloud.capacityplanner_v1beta.types.capacity_planning_service import DemandMetadata
from google.cloud.capacityplanner_v1beta.types.capacity_planning_service import DemandPreference
from google.cloud.capacityplanner_v1beta.types.capacity_planning_service import DemandValue
from google.cloud.capacityplanner_v1beta.types.capacity_planning_service import DemandValues
from google.cloud.capacityplanner_v1beta.types.capacity_planning_service import GetCapacityPlanRequest
from google.cloud.capacityplanner_v1beta.types.capacity_planning_service import QueryCapacityPlanInsightsRequest
from google.cloud.capacityplanner_v1beta.types.capacity_planning_service import QueryCapacityPlanInsightsResponse
from google.cloud.capacityplanner_v1beta.types.capacity_planning_service import QueryCapacityPlansRequest
from google.cloud.capacityplanner_v1beta.types.capacity_planning_service import QueryCapacityPlansResponse
from google.cloud.capacityplanner_v1beta.types.capacity_planning_service import ResourceDemand
from google.cloud.capacityplanner_v1beta.types.capacity_planning_service import ServiceDemand
from google.cloud.capacityplanner_v1beta.types.capacity_planning_service import TimeSeriesView
from google.cloud.capacityplanner_v1beta.types.capacity_planning_service import TimeValue
from google.cloud.capacityplanner_v1beta.types.capacity_planning_service import User
from google.cloud.capacityplanner_v1beta.types.capacity_planning_service import CapacityType
from google.cloud.capacityplanner_v1beta.types.capacity_planning_service import State
from google.cloud.capacityplanner_v1beta.types.future_reservation import FutureReservation
from google.cloud.capacityplanner_v1beta.types.location import LocationIdentifier
from google.cloud.capacityplanner_v1beta.types.location import LocationLevel
from google.cloud.capacityplanner_v1beta.types.resource import ResourceAttribute
from google.cloud.capacityplanner_v1beta.types.resource import ResourceContainer
from google.cloud.capacityplanner_v1beta.types.resource import ResourceIdentifier
from google.cloud.capacityplanner_v1beta.types.resource import ResourceIdKey
from google.cloud.capacityplanner_v1beta.types.resource import ResourceValue
from google.cloud.capacityplanner_v1beta.types.resource import Value
from google.cloud.capacityplanner_v1beta.types.resource import Unit
from google.cloud.capacityplanner_v1beta.types.usage_service import BigQueryDestination
from google.cloud.capacityplanner_v1beta.types.usage_service import ExportForecastsRequest
from google.cloud.capacityplanner_v1beta.types.usage_service import ExportForecastsResponse
from google.cloud.capacityplanner_v1beta.types.usage_service import ExportReservationsUsageRequest
from google.cloud.capacityplanner_v1beta.types.usage_service import ExportReservationsUsageResponse
from google.cloud.capacityplanner_v1beta.types.usage_service import ExportUsageHistoriesRequest
from google.cloud.capacityplanner_v1beta.types.usage_service import ExportUsageHistoriesResponse
from google.cloud.capacityplanner_v1beta.types.usage_service import Forecast
from google.cloud.capacityplanner_v1beta.types.usage_service import GcsDestination
from google.cloud.capacityplanner_v1beta.types.usage_service import MachineShape
from google.cloud.capacityplanner_v1beta.types.usage_service import OperationMetadata
from google.cloud.capacityplanner_v1beta.types.usage_service import OutputConfig
from google.cloud.capacityplanner_v1beta.types.usage_service import Point
from google.cloud.capacityplanner_v1beta.types.usage_service import QueryForecastsRequest
from google.cloud.capacityplanner_v1beta.types.usage_service import QueryForecastsResponse
from google.cloud.capacityplanner_v1beta.types.usage_service import QueryReservationsRequest
from google.cloud.capacityplanner_v1beta.types.usage_service import QueryReservationsResponse
from google.cloud.capacityplanner_v1beta.types.usage_service import QueryUsageHistoriesRequest
from google.cloud.capacityplanner_v1beta.types.usage_service import QueryUsageHistoriesResponse
from google.cloud.capacityplanner_v1beta.types.usage_service import ReservationData
from google.cloud.capacityplanner_v1beta.types.usage_service import TimeSeries
from google.cloud.capacityplanner_v1beta.types.usage_service import UsageHistory

__all__ = ('CapacityPlanningServiceClient',
    'CapacityPlanningServiceAsyncClient',
    'UsageServiceClient',
    'UsageServiceAsyncClient',
    'Allocation',
    'CapacityPlan',
    'CapacityPlanFilters',
    'CapacityPlanKey',
    'CapacityPlanView',
    'ChildResourceDemand',
    'DemandMetadata',
    'DemandPreference',
    'DemandValue',
    'DemandValues',
    'GetCapacityPlanRequest',
    'QueryCapacityPlanInsightsRequest',
    'QueryCapacityPlanInsightsResponse',
    'QueryCapacityPlansRequest',
    'QueryCapacityPlansResponse',
    'ResourceDemand',
    'ServiceDemand',
    'TimeSeriesView',
    'TimeValue',
    'User',
    'CapacityType',
    'State',
    'FutureReservation',
    'LocationIdentifier',
    'LocationLevel',
    'ResourceAttribute',
    'ResourceContainer',
    'ResourceIdentifier',
    'ResourceIdKey',
    'ResourceValue',
    'Value',
    'Unit',
    'BigQueryDestination',
    'ExportForecastsRequest',
    'ExportForecastsResponse',
    'ExportReservationsUsageRequest',
    'ExportReservationsUsageResponse',
    'ExportUsageHistoriesRequest',
    'ExportUsageHistoriesResponse',
    'Forecast',
    'GcsDestination',
    'MachineShape',
    'OperationMetadata',
    'OutputConfig',
    'Point',
    'QueryForecastsRequest',
    'QueryForecastsResponse',
    'QueryReservationsRequest',
    'QueryReservationsResponse',
    'QueryUsageHistoriesRequest',
    'QueryUsageHistoriesResponse',
    'ReservationData',
    'TimeSeries',
    'UsageHistory',
)
