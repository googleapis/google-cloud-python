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
from google.cloud.optimization import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.optimization_v1.services.fleet_routing.client import (
    FleetRoutingClient,
)
from google.cloud.optimization_v1.services.fleet_routing.async_client import (
    FleetRoutingAsyncClient,
)

from google.cloud.optimization_v1.types.async_model import AsyncModelMetadata
from google.cloud.optimization_v1.types.async_model import GcsDestination
from google.cloud.optimization_v1.types.async_model import GcsSource
from google.cloud.optimization_v1.types.async_model import InputConfig
from google.cloud.optimization_v1.types.async_model import OutputConfig
from google.cloud.optimization_v1.types.async_model import DataFormat
from google.cloud.optimization_v1.types.fleet_routing import AggregatedMetrics
from google.cloud.optimization_v1.types.fleet_routing import BatchOptimizeToursRequest
from google.cloud.optimization_v1.types.fleet_routing import BatchOptimizeToursResponse
from google.cloud.optimization_v1.types.fleet_routing import BreakRule
from google.cloud.optimization_v1.types.fleet_routing import CapacityQuantity
from google.cloud.optimization_v1.types.fleet_routing import CapacityQuantityInterval
from google.cloud.optimization_v1.types.fleet_routing import DistanceLimit
from google.cloud.optimization_v1.types.fleet_routing import InjectedSolutionConstraint
from google.cloud.optimization_v1.types.fleet_routing import Location
from google.cloud.optimization_v1.types.fleet_routing import OptimizeToursRequest
from google.cloud.optimization_v1.types.fleet_routing import OptimizeToursResponse
from google.cloud.optimization_v1.types.fleet_routing import (
    OptimizeToursValidationError,
)
from google.cloud.optimization_v1.types.fleet_routing import Shipment
from google.cloud.optimization_v1.types.fleet_routing import ShipmentModel
from google.cloud.optimization_v1.types.fleet_routing import ShipmentRoute
from google.cloud.optimization_v1.types.fleet_routing import ShipmentTypeIncompatibility
from google.cloud.optimization_v1.types.fleet_routing import ShipmentTypeRequirement
from google.cloud.optimization_v1.types.fleet_routing import SkippedShipment
from google.cloud.optimization_v1.types.fleet_routing import TimeWindow
from google.cloud.optimization_v1.types.fleet_routing import TransitionAttributes
from google.cloud.optimization_v1.types.fleet_routing import Vehicle
from google.cloud.optimization_v1.types.fleet_routing import Waypoint

__all__ = (
    "FleetRoutingClient",
    "FleetRoutingAsyncClient",
    "AsyncModelMetadata",
    "GcsDestination",
    "GcsSource",
    "InputConfig",
    "OutputConfig",
    "DataFormat",
    "AggregatedMetrics",
    "BatchOptimizeToursRequest",
    "BatchOptimizeToursResponse",
    "BreakRule",
    "CapacityQuantity",
    "CapacityQuantityInterval",
    "DistanceLimit",
    "InjectedSolutionConstraint",
    "Location",
    "OptimizeToursRequest",
    "OptimizeToursResponse",
    "OptimizeToursValidationError",
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
