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
from google.maps.fleetengine import gapic_version as package_version

__version__ = package_version.__version__


from google.maps.fleetengine_v1.services.trip_service.client import TripServiceClient
from google.maps.fleetengine_v1.services.trip_service.async_client import TripServiceAsyncClient
from google.maps.fleetengine_v1.services.vehicle_service.client import VehicleServiceClient
from google.maps.fleetengine_v1.services.vehicle_service.async_client import VehicleServiceAsyncClient

from google.maps.fleetengine_v1.types.fleetengine import TerminalLocation
from google.maps.fleetengine_v1.types.fleetengine import TerminalPointId
from google.maps.fleetengine_v1.types.fleetengine import TripWaypoint
from google.maps.fleetengine_v1.types.fleetengine import VehicleAttribute
from google.maps.fleetengine_v1.types.fleetengine import VehicleLocation
from google.maps.fleetengine_v1.types.fleetengine import LocationSensor
from google.maps.fleetengine_v1.types.fleetengine import NavigationStatus
from google.maps.fleetengine_v1.types.fleetengine import PolylineFormatType
from google.maps.fleetengine_v1.types.fleetengine import TripType
from google.maps.fleetengine_v1.types.fleetengine import WaypointType
from google.maps.fleetengine_v1.types.header import RequestHeader
from google.maps.fleetengine_v1.types.traffic import ConsumableTrafficPolyline
from google.maps.fleetengine_v1.types.traffic import SpeedReadingInterval
from google.maps.fleetengine_v1.types.trip_api import CreateTripRequest
from google.maps.fleetengine_v1.types.trip_api import GetTripRequest
from google.maps.fleetengine_v1.types.trip_api import ReportBillableTripRequest
from google.maps.fleetengine_v1.types.trip_api import SearchTripsRequest
from google.maps.fleetengine_v1.types.trip_api import SearchTripsResponse
from google.maps.fleetengine_v1.types.trip_api import UpdateTripRequest
from google.maps.fleetengine_v1.types.trips import StopLocation
from google.maps.fleetengine_v1.types.trips import Trip
from google.maps.fleetengine_v1.types.trips import BillingPlatformIdentifier
from google.maps.fleetengine_v1.types.trips import TripStatus
from google.maps.fleetengine_v1.types.trips import TripView
from google.maps.fleetengine_v1.types.vehicle_api import CreateVehicleRequest
from google.maps.fleetengine_v1.types.vehicle_api import GetVehicleRequest
from google.maps.fleetengine_v1.types.vehicle_api import ListVehiclesRequest
from google.maps.fleetengine_v1.types.vehicle_api import ListVehiclesResponse
from google.maps.fleetengine_v1.types.vehicle_api import SearchVehiclesRequest
from google.maps.fleetengine_v1.types.vehicle_api import SearchVehiclesResponse
from google.maps.fleetengine_v1.types.vehicle_api import UpdateVehicleAttributesRequest
from google.maps.fleetengine_v1.types.vehicle_api import UpdateVehicleAttributesResponse
from google.maps.fleetengine_v1.types.vehicle_api import UpdateVehicleLocationRequest
from google.maps.fleetengine_v1.types.vehicle_api import UpdateVehicleRequest
from google.maps.fleetengine_v1.types.vehicle_api import VehicleAttributeList
from google.maps.fleetengine_v1.types.vehicle_api import VehicleMatch
from google.maps.fleetengine_v1.types.vehicle_api import Waypoint
from google.maps.fleetengine_v1.types.vehicles import BatteryInfo
from google.maps.fleetengine_v1.types.vehicles import DeviceSettings
from google.maps.fleetengine_v1.types.vehicles import LicensePlate
from google.maps.fleetengine_v1.types.vehicles import TrafficPolylineData
from google.maps.fleetengine_v1.types.vehicles import Vehicle
from google.maps.fleetengine_v1.types.vehicles import VisualTrafficReportPolylineRendering
from google.maps.fleetengine_v1.types.vehicles import BatteryStatus
from google.maps.fleetengine_v1.types.vehicles import LocationPowerSaveMode
from google.maps.fleetengine_v1.types.vehicles import PowerSource
from google.maps.fleetengine_v1.types.vehicles import VehicleState

__all__ = ('TripServiceClient',
    'TripServiceAsyncClient',
    'VehicleServiceClient',
    'VehicleServiceAsyncClient',
    'TerminalLocation',
    'TerminalPointId',
    'TripWaypoint',
    'VehicleAttribute',
    'VehicleLocation',
    'LocationSensor',
    'NavigationStatus',
    'PolylineFormatType',
    'TripType',
    'WaypointType',
    'RequestHeader',
    'ConsumableTrafficPolyline',
    'SpeedReadingInterval',
    'CreateTripRequest',
    'GetTripRequest',
    'ReportBillableTripRequest',
    'SearchTripsRequest',
    'SearchTripsResponse',
    'UpdateTripRequest',
    'StopLocation',
    'Trip',
    'BillingPlatformIdentifier',
    'TripStatus',
    'TripView',
    'CreateVehicleRequest',
    'GetVehicleRequest',
    'ListVehiclesRequest',
    'ListVehiclesResponse',
    'SearchVehiclesRequest',
    'SearchVehiclesResponse',
    'UpdateVehicleAttributesRequest',
    'UpdateVehicleAttributesResponse',
    'UpdateVehicleLocationRequest',
    'UpdateVehicleRequest',
    'VehicleAttributeList',
    'VehicleMatch',
    'Waypoint',
    'BatteryInfo',
    'DeviceSettings',
    'LicensePlate',
    'TrafficPolylineData',
    'Vehicle',
    'VisualTrafficReportPolylineRendering',
    'BatteryStatus',
    'LocationPowerSaveMode',
    'PowerSource',
    'VehicleState',
)
