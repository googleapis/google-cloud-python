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

from .base import CloudMemcacheTransport
from .grpc import CloudMemcacheGrpcTransport
from .grpc_asyncio import CloudMemcacheGrpcAsyncIOTransport
from .rest import CloudMemcacheRestTransport
from .rest import CloudMemcacheRestInterceptor


# Compile a registry of transports.
_transport_registry = OrderedDict()  # type: Dict[str, Type[CloudMemcacheTransport]]
_transport_registry['grpc'] = CloudMemcacheGrpcTransport
_transport_registry['grpc_asyncio'] = CloudMemcacheGrpcAsyncIOTransport
_transport_registry['rest'] = CloudMemcacheRestTransport

__all__ = (
    'CloudMemcacheTransport',
    'CloudMemcacheGrpcTransport',
    'CloudMemcacheGrpcAsyncIOTransport',
    'CloudMemcacheRestTransport',
    'CloudMemcacheRestInterceptor',
)
