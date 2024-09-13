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


from google.maps.routeoptimization_v1.services.route_optimization.async_client import (
    RouteOptimizationAsyncClient,
)
from google.maps.routeoptimization_v1.services.route_optimization.client import (
    RouteOptimizationClient,
)
from google.maps.routeoptimization_v1.types.route_optimization_service import (
    AggregatedMetrics,
    BatchOptimizeToursMetadata,
    BatchOptimizeToursRequest,
    BatchOptimizeToursResponse,
    BreakRule,
    DataFormat,
    DistanceLimit,
    GcsDestination,
    GcsSource,
    InjectedSolutionConstraint,
    InputConfig,
    Location,
    OptimizeToursRequest,
    OptimizeToursResponse,
    OptimizeToursValidationError,
    OutputConfig,
    RouteModifiers,
    Shipment,
    ShipmentModel,
    ShipmentRoute,
    ShipmentTypeIncompatibility,
    ShipmentTypeRequirement,
    SkippedShipment,
    TimeWindow,
    TransitionAttributes,
    Vehicle,
    Waypoint,
)

__all__ = (
    "RouteOptimizationClient",
    "RouteOptimizationAsyncClient",
    "AggregatedMetrics",
    "BatchOptimizeToursMetadata",
    "BatchOptimizeToursRequest",
    "BatchOptimizeToursResponse",
    "BreakRule",
    "DistanceLimit",
    "GcsDestination",
    "GcsSource",
    "InjectedSolutionConstraint",
    "InputConfig",
    "Location",
    "OptimizeToursRequest",
    "OptimizeToursResponse",
    "OptimizeToursValidationError",
    "OutputConfig",
    "RouteModifiers",
    "Shipment",
    "ShipmentModel",
    "ShipmentRoute",
    "ShipmentTypeIncompatibility",
    "ShipmentTypeRequirement",
    "SkippedShipment",
    "TimeWindow",
    "TransitionAttributes",
    "Vehicle",
    "Waypoint",
    "DataFormat",
)
