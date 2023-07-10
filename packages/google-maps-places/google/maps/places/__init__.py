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
from google.maps.places import gapic_version as package_version

__version__ = package_version.__version__


from google.maps.places_v1.services.places.async_client import PlacesAsyncClient
from google.maps.places_v1.services.places.client import PlacesClient
from google.maps.places_v1.types.geometry import Circle
from google.maps.places_v1.types.place import Place, PriceLevel
from google.maps.places_v1.types.places_service import (
    Int32Range,
    SearchTextRequest,
    SearchTextResponse,
)

__all__ = (
    "PlacesClient",
    "PlacesAsyncClient",
    "Circle",
    "Place",
    "PriceLevel",
    "Int32Range",
    "SearchTextRequest",
    "SearchTextResponse",
)
