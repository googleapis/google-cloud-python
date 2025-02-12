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
from collections import OrderedDict
from typing import Dict, Type

from .base import AppConnectorsServiceTransport
from .grpc import AppConnectorsServiceGrpcTransport
from .grpc_asyncio import AppConnectorsServiceGrpcAsyncIOTransport
from .rest import AppConnectorsServiceRestTransport
from .rest import AppConnectorsServiceRestInterceptor


# Compile a registry of transports.
_transport_registry = OrderedDict()  # type: Dict[str, Type[AppConnectorsServiceTransport]]
_transport_registry['grpc'] = AppConnectorsServiceGrpcTransport
_transport_registry['grpc_asyncio'] = AppConnectorsServiceGrpcAsyncIOTransport
_transport_registry['rest'] = AppConnectorsServiceRestTransport

__all__ = (
    'AppConnectorsServiceTransport',
    'AppConnectorsServiceGrpcTransport',
    'AppConnectorsServiceGrpcAsyncIOTransport',
    'AppConnectorsServiceRestTransport',
    'AppConnectorsServiceRestInterceptor',
)
