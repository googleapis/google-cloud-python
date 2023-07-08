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
from collections import OrderedDict
from typing import Dict, Type

from .base import MapsPlatformDatasetsV1AlphaTransport
from .grpc import MapsPlatformDatasetsV1AlphaGrpcTransport
from .grpc_asyncio import MapsPlatformDatasetsV1AlphaGrpcAsyncIOTransport
from .rest import (
    MapsPlatformDatasetsV1AlphaRestInterceptor,
    MapsPlatformDatasetsV1AlphaRestTransport,
)

# Compile a registry of transports.
_transport_registry = (
    OrderedDict()
)  # type: Dict[str, Type[MapsPlatformDatasetsV1AlphaTransport]]
_transport_registry["grpc"] = MapsPlatformDatasetsV1AlphaGrpcTransport
_transport_registry["grpc_asyncio"] = MapsPlatformDatasetsV1AlphaGrpcAsyncIOTransport
_transport_registry["rest"] = MapsPlatformDatasetsV1AlphaRestTransport

__all__ = (
    "MapsPlatformDatasetsV1AlphaTransport",
    "MapsPlatformDatasetsV1AlphaGrpcTransport",
    "MapsPlatformDatasetsV1AlphaGrpcAsyncIOTransport",
    "MapsPlatformDatasetsV1AlphaRestTransport",
    "MapsPlatformDatasetsV1AlphaRestInterceptor",
)
