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

from .services.fleet_routing import FleetRoutingClient
from .services.fleet_routing import FleetRoutingAsyncClient

from .types.async_model import AsyncModelMetadata
from .types.async_model import GcsDestination
from .types.async_model import GcsSource
from .types.async_model import InputConfig
from .types.async_model import OutputConfig
from .types.async_model import DataFormat
from .types.fleet_routing import AggregatedMetrics
from .types.fleet_routing import BatchOptimizeToursRequest
from .types.fleet_routing import BatchOptimizeToursResponse
from .types.fleet_routing import BreakRule
from .types.fleet_routing import CapacityQuantity
from .types.fleet_routing import CapacityQuantityInterval
from .types.fleet_routing import DistanceLimit
from .types.fleet_routing import InjectedSolutionConstraint
from .types.fleet_routing import Location
from .types.fleet_routing import OptimizeToursRequest
from .types.fleet_routing import OptimizeToursResponse
from .types.fleet_routing import OptimizeToursValidationError
from .types.fleet_routing import Shipment
from .types.fleet_routing import ShipmentModel
from .types.fleet_routing import ShipmentRoute
from .types.fleet_routing import ShipmentTypeIncompatibility
from .types.fleet_routing import ShipmentTypeRequirement
from .types.fleet_routing import SkippedShipment
from .types.fleet_routing import TimeWindow
from .types.fleet_routing import TransitionAttributes
from .types.fleet_routing import Vehicle
from .types.fleet_routing import Waypoint

__all__ = (
    "FleetRoutingAsyncClient",
    "AggregatedMetrics",
    "AsyncModelMetadata",
    "BatchOptimizeToursRequest",
    "BatchOptimizeToursResponse",
    "BreakRule",
    "CapacityQuantity",
    "CapacityQuantityInterval",
    "DataFormat",
    "DistanceLimit",
    "FleetRoutingClient",
    "GcsDestination",
    "GcsSource",
    "InjectedSolutionConstraint",
    "InputConfig",
    "Location",
    "OptimizeToursRequest",
    "OptimizeToursResponse",
    "OptimizeToursValidationError",
    "OutputConfig",
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
)
