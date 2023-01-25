# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from google.maps.routing_v2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.routes import RoutesAsyncClient, RoutesClient
from .types.fallback_info import FallbackInfo, FallbackReason, FallbackRoutingMode
from .types.location import Location
from .types.maneuver import Maneuver
from .types.navigation_instruction import NavigationInstruction
from .types.polyline import Polyline, PolylineEncoding, PolylineQuality
from .types.route import (
    Route,
    RouteLeg,
    RouteLegStep,
    RouteLegStepTravelAdvisory,
    RouteLegTravelAdvisory,
    RouteTravelAdvisory,
)
from .types.route_label import RouteLabel
from .types.route_modifiers import RouteModifiers
from .types.route_travel_mode import RouteTravelMode
from .types.routes_service import (
    ComputeRouteMatrixRequest,
    ComputeRoutesRequest,
    ComputeRoutesResponse,
    RouteMatrixDestination,
    RouteMatrixElement,
    RouteMatrixElementCondition,
    RouteMatrixOrigin,
)
from .types.routing_preference import RoutingPreference
from .types.speed_reading_interval import SpeedReadingInterval
from .types.toll_info import TollInfo
from .types.toll_passes import TollPass
from .types.units import Units
from .types.vehicle_emission_type import VehicleEmissionType
from .types.vehicle_info import VehicleInfo
from .types.waypoint import Waypoint

__all__ = (
    "RoutesAsyncClient",
    "ComputeRouteMatrixRequest",
    "ComputeRoutesRequest",
    "ComputeRoutesResponse",
    "FallbackInfo",
    "FallbackReason",
    "FallbackRoutingMode",
    "Location",
    "Maneuver",
    "NavigationInstruction",
    "Polyline",
    "PolylineEncoding",
    "PolylineQuality",
    "Route",
    "RouteLabel",
    "RouteLeg",
    "RouteLegStep",
    "RouteLegStepTravelAdvisory",
    "RouteLegTravelAdvisory",
    "RouteMatrixDestination",
    "RouteMatrixElement",
    "RouteMatrixElementCondition",
    "RouteMatrixOrigin",
    "RouteModifiers",
    "RouteTravelAdvisory",
    "RouteTravelMode",
    "RoutesClient",
    "RoutingPreference",
    "SpeedReadingInterval",
    "TollInfo",
    "TollPass",
    "Units",
    "VehicleEmissionType",
    "VehicleInfo",
    "Waypoint",
)
