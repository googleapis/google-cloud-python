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

from .base import ValidationHelperV1Transport
from .grpc import ValidationHelperV1GrpcTransport
from .grpc_asyncio import ValidationHelperV1GrpcAsyncIOTransport
from .rest import ValidationHelperV1RestTransport
from .rest import ValidationHelperV1RestInterceptor


# Compile a registry of transports.
_transport_registry = OrderedDict()  # type: Dict[str, Type[ValidationHelperV1Transport]]
_transport_registry['grpc'] = ValidationHelperV1GrpcTransport
_transport_registry['grpc_asyncio'] = ValidationHelperV1GrpcAsyncIOTransport
_transport_registry['rest'] = ValidationHelperV1RestTransport

__all__ = (
    'ValidationHelperV1Transport',
    'ValidationHelperV1GrpcTransport',
    'ValidationHelperV1GrpcAsyncIOTransport',
    'ValidationHelperV1RestTransport',
    'ValidationHelperV1RestInterceptor',
)
