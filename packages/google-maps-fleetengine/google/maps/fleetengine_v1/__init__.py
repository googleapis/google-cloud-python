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
from google.maps.fleetengine_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.trip_service import TripServiceAsyncClient, TripServiceClient
from .services.vehicle_service import VehicleServiceAsyncClient, VehicleServiceClient
from .types.fleetengine import (
    LocationSensor,
    NavigationStatus,
    PolylineFormatType,
    TerminalLocation,
    TerminalPointId,
    TripType,
    TripWaypoint,
    VehicleAttribute,
    VehicleLocation,
    WaypointType,
)
from .types.header import RequestHeader
from .types.traffic import ConsumableTrafficPolyline, SpeedReadingInterval
from .types.trip_api import (
    CreateTripRequest,
    GetTripRequest,
    ReportBillableTripRequest,
    SearchTripsRequest,
    SearchTripsResponse,
    UpdateTripRequest,
)
from .types.trips import (
    BillingPlatformIdentifier,
    StopLocation,
    Trip,
    TripStatus,
    TripView,
)
from .types.vehicle_api import (
    CreateVehicleRequest,
    GetVehicleRequest,
    ListVehiclesRequest,
    ListVehiclesResponse,
    SearchVehiclesRequest,
    SearchVehiclesResponse,
    UpdateVehicleAttributesRequest,
    UpdateVehicleAttributesResponse,
    UpdateVehicleRequest,
    VehicleAttributeList,
    VehicleMatch,
    Waypoint,
)
from .types.vehicles import (
    BatteryInfo,
    BatteryStatus,
    DeviceSettings,
    LicensePlate,
    LocationPowerSaveMode,
    PowerSource,
    TrafficPolylineData,
    Vehicle,
    VehicleState,
    VisualTrafficReportPolylineRendering,
)

__all__ = (
    "TripServiceAsyncClient",
    "VehicleServiceAsyncClient",
    "BatteryInfo",
    "BatteryStatus",
    "BillingPlatformIdentifier",
    "ConsumableTrafficPolyline",
    "CreateTripRequest",
    "CreateVehicleRequest",
    "DeviceSettings",
    "GetTripRequest",
    "GetVehicleRequest",
    "LicensePlate",
    "ListVehiclesRequest",
    "ListVehiclesResponse",
    "LocationPowerSaveMode",
    "LocationSensor",
    "NavigationStatus",
    "PolylineFormatType",
    "PowerSource",
    "ReportBillableTripRequest",
    "RequestHeader",
    "SearchTripsRequest",
    "SearchTripsResponse",
    "SearchVehiclesRequest",
    "SearchVehiclesResponse",
    "SpeedReadingInterval",
    "StopLocation",
    "TerminalLocation",
    "TerminalPointId",
    "TrafficPolylineData",
    "Trip",
    "TripServiceClient",
    "TripStatus",
    "TripType",
    "TripView",
    "TripWaypoint",
    "UpdateTripRequest",
    "UpdateVehicleAttributesRequest",
    "UpdateVehicleAttributesResponse",
    "UpdateVehicleRequest",
    "Vehicle",
    "VehicleAttribute",
    "VehicleAttributeList",
    "VehicleLocation",
    "VehicleMatch",
    "VehicleServiceClient",
    "VehicleState",
    "VisualTrafficReportPolylineRendering",
    "Waypoint",
    "WaypointType",
)
