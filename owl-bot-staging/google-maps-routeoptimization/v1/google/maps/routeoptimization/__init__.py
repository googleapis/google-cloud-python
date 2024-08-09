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
from google.maps.routeoptimization import gapic_version as package_version

__version__ = package_version.__version__


from google.maps.routeoptimization_v1.services.route_optimization.client import RouteOptimizationClient
from google.maps.routeoptimization_v1.services.route_optimization.async_client import RouteOptimizationAsyncClient

from google.maps.routeoptimization_v1.types.route_optimization_service import AggregatedMetrics
from google.maps.routeoptimization_v1.types.route_optimization_service import BatchOptimizeToursMetadata
from google.maps.routeoptimization_v1.types.route_optimization_service import BatchOptimizeToursRequest
from google.maps.routeoptimization_v1.types.route_optimization_service import BatchOptimizeToursResponse
from google.maps.routeoptimization_v1.types.route_optimization_service import BreakRule
from google.maps.routeoptimization_v1.types.route_optimization_service import DistanceLimit
from google.maps.routeoptimization_v1.types.route_optimization_service import GcsDestination
from google.maps.routeoptimization_v1.types.route_optimization_service import GcsSource
from google.maps.routeoptimization_v1.types.route_optimization_service import InjectedSolutionConstraint
from google.maps.routeoptimization_v1.types.route_optimization_service import InputConfig
from google.maps.routeoptimization_v1.types.route_optimization_service import Location
from google.maps.routeoptimization_v1.types.route_optimization_service import OptimizeToursRequest
from google.maps.routeoptimization_v1.types.route_optimization_service import OptimizeToursResponse
from google.maps.routeoptimization_v1.types.route_optimization_service import OptimizeToursValidationError
from google.maps.routeoptimization_v1.types.route_optimization_service import OutputConfig
from google.maps.routeoptimization_v1.types.route_optimization_service import Shipment
from google.maps.routeoptimization_v1.types.route_optimization_service import ShipmentModel
from google.maps.routeoptimization_v1.types.route_optimization_service import ShipmentRoute
from google.maps.routeoptimization_v1.types.route_optimization_service import ShipmentTypeIncompatibility
from google.maps.routeoptimization_v1.types.route_optimization_service import ShipmentTypeRequirement
from google.maps.routeoptimization_v1.types.route_optimization_service import SkippedShipment
from google.maps.routeoptimization_v1.types.route_optimization_service import TimeWindow
from google.maps.routeoptimization_v1.types.route_optimization_service import TransitionAttributes
from google.maps.routeoptimization_v1.types.route_optimization_service import Vehicle
from google.maps.routeoptimization_v1.types.route_optimization_service import Waypoint
from google.maps.routeoptimization_v1.types.route_optimization_service import DataFormat

__all__ = ('RouteOptimizationClient',
    'RouteOptimizationAsyncClient',
    'AggregatedMetrics',
    'BatchOptimizeToursMetadata',
    'BatchOptimizeToursRequest',
    'BatchOptimizeToursResponse',
    'BreakRule',
    'DistanceLimit',
    'GcsDestination',
    'GcsSource',
    'InjectedSolutionConstraint',
    'InputConfig',
    'Location',
    'OptimizeToursRequest',
    'OptimizeToursResponse',
    'OptimizeToursValidationError',
    'OutputConfig',
    'Shipment',
    'ShipmentModel',
    'ShipmentRoute',
    'ShipmentTypeIncompatibility',
    'ShipmentTypeRequirement',
    'SkippedShipment',
    'TimeWindow',
    'TransitionAttributes',
    'Vehicle',
    'Waypoint',
    'DataFormat',
)
