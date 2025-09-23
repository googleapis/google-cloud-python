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


from .services.capacity_planning_service import (
    CapacityPlanningServiceAsyncClient,
    CapacityPlanningServiceClient,
)
from .services.usage_service import UsageServiceAsyncClient, UsageServiceClient
from .types.allocation import Allocation
from .types.capacity_planning_service import (
    CapacityPlan,
    CapacityPlanFilters,
    CapacityPlanKey,
    CapacityPlanView,
    CapacityType,
    ChildResourceDemand,
    DemandMetadata,
    DemandPreference,
    DemandValue,
    DemandValues,
    GetCapacityPlanRequest,
    QueryCapacityPlanInsightsRequest,
    QueryCapacityPlanInsightsResponse,
    QueryCapacityPlansRequest,
    QueryCapacityPlansResponse,
    ResourceDemand,
    ServiceDemand,
    State,
    TimeSeriesView,
    TimeValue,
    User,
)
from .types.future_reservation import FutureReservation
from .types.location import LocationIdentifier, LocationLevel
from .types.resource import (
    ResourceAttribute,
    ResourceContainer,
    ResourceIdentifier,
    ResourceIdKey,
    ResourceValue,
    Unit,
    Value,
)
from .types.usage_service import (
    BigQueryDestination,
    ExportForecastsRequest,
    ExportForecastsResponse,
    ExportReservationsUsageRequest,
    ExportReservationsUsageResponse,
    ExportUsageHistoriesRequest,
    ExportUsageHistoriesResponse,
    Forecast,
    GcsDestination,
    MachineShape,
    OperationMetadata,
    OutputConfig,
    Point,
    QueryForecastsRequest,
    QueryForecastsResponse,
    QueryReservationsRequest,
    QueryReservationsResponse,
    QueryUsageHistoriesRequest,
    QueryUsageHistoriesResponse,
    ReservationData,
    TimeSeries,
    UsageHistory,
)

__all__ = (
    "CapacityPlanningServiceAsyncClient",
    "UsageServiceAsyncClient",
    "Allocation",
    "BigQueryDestination",
    "CapacityPlan",
    "CapacityPlanFilters",
    "CapacityPlanKey",
    "CapacityPlanView",
    "CapacityPlanningServiceClient",
    "CapacityType",
    "ChildResourceDemand",
    "DemandMetadata",
    "DemandPreference",
    "DemandValue",
    "DemandValues",
    "ExportForecastsRequest",
    "ExportForecastsResponse",
    "ExportReservationsUsageRequest",
    "ExportReservationsUsageResponse",
    "ExportUsageHistoriesRequest",
    "ExportUsageHistoriesResponse",
    "Forecast",
    "FutureReservation",
    "GcsDestination",
    "GetCapacityPlanRequest",
    "LocationIdentifier",
    "LocationLevel",
    "MachineShape",
    "OperationMetadata",
    "OutputConfig",
    "Point",
    "QueryCapacityPlanInsightsRequest",
    "QueryCapacityPlanInsightsResponse",
    "QueryCapacityPlansRequest",
    "QueryCapacityPlansResponse",
    "QueryForecastsRequest",
    "QueryForecastsResponse",
    "QueryReservationsRequest",
    "QueryReservationsResponse",
    "QueryUsageHistoriesRequest",
    "QueryUsageHistoriesResponse",
    "ReservationData",
    "ResourceAttribute",
    "ResourceContainer",
    "ResourceDemand",
    "ResourceIdKey",
    "ResourceIdentifier",
    "ResourceValue",
    "ServiceDemand",
    "State",
    "TimeSeries",
    "TimeSeriesView",
    "TimeValue",
    "Unit",
    "UsageHistory",
    "UsageServiceClient",
    "User",
    "Value",
)
