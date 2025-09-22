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
from google.cloud.capacityplanner_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.capacity_planning_service import CapacityPlanningServiceClient
from .services.capacity_planning_service import CapacityPlanningServiceAsyncClient
from .services.usage_service import UsageServiceClient
from .services.usage_service import UsageServiceAsyncClient

from .types.allocation import Allocation
from .types.capacity_planning_service import CapacityPlan
from .types.capacity_planning_service import CapacityPlanFilters
from .types.capacity_planning_service import CapacityPlanKey
from .types.capacity_planning_service import CapacityPlanView
from .types.capacity_planning_service import ChildResourceDemand
from .types.capacity_planning_service import DemandMetadata
from .types.capacity_planning_service import DemandPreference
from .types.capacity_planning_service import DemandValue
from .types.capacity_planning_service import DemandValues
from .types.capacity_planning_service import GetCapacityPlanRequest
from .types.capacity_planning_service import QueryCapacityPlanInsightsRequest
from .types.capacity_planning_service import QueryCapacityPlanInsightsResponse
from .types.capacity_planning_service import QueryCapacityPlansRequest
from .types.capacity_planning_service import QueryCapacityPlansResponse
from .types.capacity_planning_service import ResourceDemand
from .types.capacity_planning_service import ServiceDemand
from .types.capacity_planning_service import TimeSeriesView
from .types.capacity_planning_service import TimeValue
from .types.capacity_planning_service import User
from .types.capacity_planning_service import CapacityType
from .types.capacity_planning_service import State
from .types.future_reservation import FutureReservation
from .types.location import LocationIdentifier
from .types.location import LocationLevel
from .types.resource import ResourceAttribute
from .types.resource import ResourceContainer
from .types.resource import ResourceIdentifier
from .types.resource import ResourceIdKey
from .types.resource import ResourceValue
from .types.resource import Value
from .types.resource import Unit
from .types.usage_service import BigQueryDestination
from .types.usage_service import ExportForecastsRequest
from .types.usage_service import ExportForecastsResponse
from .types.usage_service import ExportReservationsUsageRequest
from .types.usage_service import ExportReservationsUsageResponse
from .types.usage_service import ExportUsageHistoriesRequest
from .types.usage_service import ExportUsageHistoriesResponse
from .types.usage_service import Forecast
from .types.usage_service import GcsDestination
from .types.usage_service import MachineShape
from .types.usage_service import OperationMetadata
from .types.usage_service import OutputConfig
from .types.usage_service import Point
from .types.usage_service import QueryForecastsRequest
from .types.usage_service import QueryForecastsResponse
from .types.usage_service import QueryReservationsRequest
from .types.usage_service import QueryReservationsResponse
from .types.usage_service import QueryUsageHistoriesRequest
from .types.usage_service import QueryUsageHistoriesResponse
from .types.usage_service import ReservationData
from .types.usage_service import TimeSeries
from .types.usage_service import UsageHistory

__all__ = (
    'CapacityPlanningServiceAsyncClient',
    'UsageServiceAsyncClient',
'Allocation',
'BigQueryDestination',
'CapacityPlan',
'CapacityPlanFilters',
'CapacityPlanKey',
'CapacityPlanView',
'CapacityPlanningServiceClient',
'CapacityType',
'ChildResourceDemand',
'DemandMetadata',
'DemandPreference',
'DemandValue',
'DemandValues',
'ExportForecastsRequest',
'ExportForecastsResponse',
'ExportReservationsUsageRequest',
'ExportReservationsUsageResponse',
'ExportUsageHistoriesRequest',
'ExportUsageHistoriesResponse',
'Forecast',
'FutureReservation',
'GcsDestination',
'GetCapacityPlanRequest',
'LocationIdentifier',
'LocationLevel',
'MachineShape',
'OperationMetadata',
'OutputConfig',
'Point',
'QueryCapacityPlanInsightsRequest',
'QueryCapacityPlanInsightsResponse',
'QueryCapacityPlansRequest',
'QueryCapacityPlansResponse',
'QueryForecastsRequest',
'QueryForecastsResponse',
'QueryReservationsRequest',
'QueryReservationsResponse',
'QueryUsageHistoriesRequest',
'QueryUsageHistoriesResponse',
'ReservationData',
'ResourceAttribute',
'ResourceContainer',
'ResourceDemand',
'ResourceIdKey',
'ResourceIdentifier',
'ResourceValue',
'ServiceDemand',
'State',
'TimeSeries',
'TimeSeriesView',
'TimeValue',
'Unit',
'UsageHistory',
'UsageServiceClient',
'User',
'Value',
)
