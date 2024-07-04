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
from google.maps.routeoptimization_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.route_optimization import RouteOptimizationClient
from .services.route_optimization import RouteOptimizationAsyncClient

from .types.route_optimization_service import AggregatedMetrics
from .types.route_optimization_service import BatchOptimizeToursMetadata
from .types.route_optimization_service import BatchOptimizeToursRequest
from .types.route_optimization_service import BatchOptimizeToursResponse
from .types.route_optimization_service import BreakRule
from .types.route_optimization_service import DistanceLimit
from .types.route_optimization_service import GcsDestination
from .types.route_optimization_service import GcsSource
from .types.route_optimization_service import InjectedSolutionConstraint
from .types.route_optimization_service import InputConfig
from .types.route_optimization_service import Location
from .types.route_optimization_service import OptimizeToursRequest
from .types.route_optimization_service import OptimizeToursResponse
from .types.route_optimization_service import OptimizeToursValidationError
from .types.route_optimization_service import OutputConfig
from .types.route_optimization_service import Shipment
from .types.route_optimization_service import ShipmentModel
from .types.route_optimization_service import ShipmentRoute
from .types.route_optimization_service import ShipmentTypeIncompatibility
from .types.route_optimization_service import ShipmentTypeRequirement
from .types.route_optimization_service import SkippedShipment
from .types.route_optimization_service import TimeWindow
from .types.route_optimization_service import TransitionAttributes
from .types.route_optimization_service import Vehicle
from .types.route_optimization_service import Waypoint
from .types.route_optimization_service import DataFormat

__all__ = (
    'RouteOptimizationAsyncClient',
'AggregatedMetrics',
'BatchOptimizeToursMetadata',
'BatchOptimizeToursRequest',
'BatchOptimizeToursResponse',
'BreakRule',
'DataFormat',
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
'RouteOptimizationClient',
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
)
