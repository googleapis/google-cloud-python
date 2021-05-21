# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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

from .services.lookup_service import LookupServiceClient
from .services.lookup_service import LookupServiceAsyncClient
from .services.registration_service import RegistrationServiceClient
from .services.registration_service import RegistrationServiceAsyncClient

from .types.endpoint import Endpoint
from .types.lookup_service import ResolveServiceRequest
from .types.lookup_service import ResolveServiceResponse
from .types.namespace import Namespace
from .types.registration_service import CreateEndpointRequest
from .types.registration_service import CreateNamespaceRequest
from .types.registration_service import CreateServiceRequest
from .types.registration_service import DeleteEndpointRequest
from .types.registration_service import DeleteNamespaceRequest
from .types.registration_service import DeleteServiceRequest
from .types.registration_service import GetEndpointRequest
from .types.registration_service import GetNamespaceRequest
from .types.registration_service import GetServiceRequest
from .types.registration_service import ListEndpointsRequest
from .types.registration_service import ListEndpointsResponse
from .types.registration_service import ListNamespacesRequest
from .types.registration_service import ListNamespacesResponse
from .types.registration_service import ListServicesRequest
from .types.registration_service import ListServicesResponse
from .types.registration_service import UpdateEndpointRequest
from .types.registration_service import UpdateNamespaceRequest
from .types.registration_service import UpdateServiceRequest
from .types.service import Service

__all__ = (
    "LookupServiceAsyncClient",
    "RegistrationServiceAsyncClient",
    "CreateEndpointRequest",
    "CreateNamespaceRequest",
    "CreateServiceRequest",
    "DeleteEndpointRequest",
    "DeleteNamespaceRequest",
    "DeleteServiceRequest",
    "Endpoint",
    "GetEndpointRequest",
    "GetNamespaceRequest",
    "GetServiceRequest",
    "ListEndpointsRequest",
    "ListEndpointsResponse",
    "ListNamespacesRequest",
    "ListNamespacesResponse",
    "ListServicesRequest",
    "ListServicesResponse",
    "LookupServiceClient",
    "Namespace",
    "RegistrationServiceClient",
    "ResolveServiceRequest",
    "ResolveServiceResponse",
    "Service",
    "UpdateEndpointRequest",
    "UpdateNamespaceRequest",
    "UpdateServiceRequest",
)
