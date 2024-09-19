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

from .base import AutokeyTransport
from .grpc import AutokeyGrpcTransport
from .grpc_asyncio import AutokeyGrpcAsyncIOTransport
from .rest import AutokeyRestTransport
from .rest import AutokeyRestInterceptor


# Compile a registry of transports.
_transport_registry = OrderedDict()  # type: Dict[str, Type[AutokeyTransport]]
_transport_registry['grpc'] = AutokeyGrpcTransport
_transport_registry['grpc_asyncio'] = AutokeyGrpcAsyncIOTransport
_transport_registry['rest'] = AutokeyRestTransport

__all__ = (
    'AutokeyTransport',
    'AutokeyGrpcTransport',
    'AutokeyGrpcAsyncIOTransport',
    'AutokeyRestTransport',
    'AutokeyRestInterceptor',
)
