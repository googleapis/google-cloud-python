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
from google.maps.fleetengine_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.trip_service import TripServiceClient
from .services.trip_service import TripServiceAsyncClient
from .services.vehicle_service import VehicleServiceClient
from .services.vehicle_service import VehicleServiceAsyncClient

from .types.fleetengine import TerminalLocation
from .types.fleetengine import TerminalPointId
from .types.fleetengine import TripWaypoint
from .types.fleetengine import VehicleAttribute
from .types.fleetengine import VehicleLocation
from .types.fleetengine import LocationSensor
from .types.fleetengine import NavigationStatus
from .types.fleetengine import PolylineFormatType
from .types.fleetengine import TripType
from .types.fleetengine import WaypointType
from .types.header import RequestHeader
from .types.traffic import ConsumableTrafficPolyline
from .types.traffic import SpeedReadingInterval
from .types.trip_api import CreateTripRequest
from .types.trip_api import GetTripRequest
from .types.trip_api import ReportBillableTripRequest
from .types.trip_api import SearchTripsRequest
from .types.trip_api import SearchTripsResponse
from .types.trip_api import UpdateTripRequest
from .types.trips import StopLocation
from .types.trips import Trip
from .types.trips import BillingPlatformIdentifier
from .types.trips import TripStatus
from .types.trips import TripView
from .types.vehicle_api import CreateVehicleRequest
from .types.vehicle_api import GetVehicleRequest
from .types.vehicle_api import ListVehiclesRequest
from .types.vehicle_api import ListVehiclesResponse
from .types.vehicle_api import SearchVehiclesRequest
from .types.vehicle_api import SearchVehiclesResponse
from .types.vehicle_api import UpdateVehicleAttributesRequest
from .types.vehicle_api import UpdateVehicleAttributesResponse
from .types.vehicle_api import UpdateVehicleLocationRequest
from .types.vehicle_api import UpdateVehicleRequest
from .types.vehicle_api import VehicleAttributeList
from .types.vehicle_api import VehicleMatch
from .types.vehicle_api import Waypoint
from .types.vehicles import BatteryInfo
from .types.vehicles import DeviceSettings
from .types.vehicles import LicensePlate
from .types.vehicles import TrafficPolylineData
from .types.vehicles import Vehicle
from .types.vehicles import VisualTrafficReportPolylineRendering
from .types.vehicles import BatteryStatus
from .types.vehicles import LocationPowerSaveMode
from .types.vehicles import PowerSource
from .types.vehicles import VehicleState

__all__ = (
    'TripServiceAsyncClient',
    'VehicleServiceAsyncClient',
'BatteryInfo',
'BatteryStatus',
'BillingPlatformIdentifier',
'ConsumableTrafficPolyline',
'CreateTripRequest',
'CreateVehicleRequest',
'DeviceSettings',
'GetTripRequest',
'GetVehicleRequest',
'LicensePlate',
'ListVehiclesRequest',
'ListVehiclesResponse',
'LocationPowerSaveMode',
'LocationSensor',
'NavigationStatus',
'PolylineFormatType',
'PowerSource',
'ReportBillableTripRequest',
'RequestHeader',
'SearchTripsRequest',
'SearchTripsResponse',
'SearchVehiclesRequest',
'SearchVehiclesResponse',
'SpeedReadingInterval',
'StopLocation',
'TerminalLocation',
'TerminalPointId',
'TrafficPolylineData',
'Trip',
'TripServiceClient',
'TripStatus',
'TripType',
'TripView',
'TripWaypoint',
'UpdateTripRequest',
'UpdateVehicleAttributesRequest',
'UpdateVehicleAttributesResponse',
'UpdateVehicleLocationRequest',
'UpdateVehicleRequest',
'Vehicle',
'VehicleAttribute',
'VehicleAttributeList',
'VehicleLocation',
'VehicleMatch',
'VehicleServiceClient',
'VehicleState',
'VisualTrafficReportPolylineRendering',
'Waypoint',
'WaypointType',
)
