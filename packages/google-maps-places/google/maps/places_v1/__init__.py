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
from google.maps.places_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.places import PlacesAsyncClient, PlacesClient
from .types.address_descriptor import AddressDescriptor
from .types.attribution import AuthorAttribution
from .types.content_block import ContentBlock
from .types.contextual_content import ContextualContent
from .types.ev_charging import EVChargeOptions, EVConnectorType
from .types.fuel_options import FuelOptions
from .types.geometry import Circle
from .types.photo import Photo
from .types.place import Place, PriceLevel
from .types.places_service import (
    AutocompletePlacesRequest,
    AutocompletePlacesResponse,
    GetPhotoMediaRequest,
    GetPlaceRequest,
    PhotoMedia,
    RoutingParameters,
    SearchNearbyRequest,
    SearchNearbyResponse,
    SearchTextRequest,
    SearchTextResponse,
)
from .types.polyline import Polyline
from .types.price_range import PriceRange
from .types.reference import References
from .types.review import Review
from .types.route_modifiers import RouteModifiers
from .types.routing_preference import RoutingPreference
from .types.routing_summary import RoutingSummary
from .types.travel_mode import TravelMode

__all__ = (
    "PlacesAsyncClient",
    "AddressDescriptor",
    "AuthorAttribution",
    "AutocompletePlacesRequest",
    "AutocompletePlacesResponse",
    "Circle",
    "ContentBlock",
    "ContextualContent",
    "EVChargeOptions",
    "EVConnectorType",
    "FuelOptions",
    "GetPhotoMediaRequest",
    "GetPlaceRequest",
    "Photo",
    "PhotoMedia",
    "Place",
    "PlacesClient",
    "Polyline",
    "PriceLevel",
    "PriceRange",
    "References",
    "Review",
    "RouteModifiers",
    "RoutingParameters",
    "RoutingPreference",
    "RoutingSummary",
    "SearchNearbyRequest",
    "SearchNearbyResponse",
    "SearchTextRequest",
    "SearchTextResponse",
    "TravelMode",
)
