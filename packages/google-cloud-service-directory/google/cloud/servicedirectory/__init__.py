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

from google.cloud.servicedirectory_v1.services.lookup_service.client import (
    LookupServiceClient,
)
from google.cloud.servicedirectory_v1.services.lookup_service.async_client import (
    LookupServiceAsyncClient,
)
from google.cloud.servicedirectory_v1.services.registration_service.client import (
    RegistrationServiceClient,
)
from google.cloud.servicedirectory_v1.services.registration_service.async_client import (
    RegistrationServiceAsyncClient,
)

from google.cloud.servicedirectory_v1.types.endpoint import Endpoint
from google.cloud.servicedirectory_v1.types.lookup_service import ResolveServiceRequest
from google.cloud.servicedirectory_v1.types.lookup_service import ResolveServiceResponse
from google.cloud.servicedirectory_v1.types.namespace import Namespace
from google.cloud.servicedirectory_v1.types.registration_service import (
    CreateEndpointRequest,
)
from google.cloud.servicedirectory_v1.types.registration_service import (
    CreateNamespaceRequest,
)
from google.cloud.servicedirectory_v1.types.registration_service import (
    CreateServiceRequest,
)
from google.cloud.servicedirectory_v1.types.registration_service import (
    DeleteEndpointRequest,
)
from google.cloud.servicedirectory_v1.types.registration_service import (
    DeleteNamespaceRequest,
)
from google.cloud.servicedirectory_v1.types.registration_service import (
    DeleteServiceRequest,
)
from google.cloud.servicedirectory_v1.types.registration_service import (
    GetEndpointRequest,
)
from google.cloud.servicedirectory_v1.types.registration_service import (
    GetNamespaceRequest,
)
from google.cloud.servicedirectory_v1.types.registration_service import (
    GetServiceRequest,
)
from google.cloud.servicedirectory_v1.types.registration_service import (
    ListEndpointsRequest,
)
from google.cloud.servicedirectory_v1.types.registration_service import (
    ListEndpointsResponse,
)
from google.cloud.servicedirectory_v1.types.registration_service import (
    ListNamespacesRequest,
)
from google.cloud.servicedirectory_v1.types.registration_service import (
    ListNamespacesResponse,
)
from google.cloud.servicedirectory_v1.types.registration_service import (
    ListServicesRequest,
)
from google.cloud.servicedirectory_v1.types.registration_service import (
    ListServicesResponse,
)
from google.cloud.servicedirectory_v1.types.registration_service import (
    UpdateEndpointRequest,
)
from google.cloud.servicedirectory_v1.types.registration_service import (
    UpdateNamespaceRequest,
)
from google.cloud.servicedirectory_v1.types.registration_service import (
    UpdateServiceRequest,
)
from google.cloud.servicedirectory_v1.types.service import Service

__all__ = (
    "LookupServiceClient",
    "LookupServiceAsyncClient",
    "RegistrationServiceClient",
    "RegistrationServiceAsyncClient",
    "Endpoint",
    "ResolveServiceRequest",
    "ResolveServiceResponse",
    "Namespace",
    "CreateEndpointRequest",
    "CreateNamespaceRequest",
    "CreateServiceRequest",
    "DeleteEndpointRequest",
    "DeleteNamespaceRequest",
    "DeleteServiceRequest",
    "GetEndpointRequest",
    "GetNamespaceRequest",
    "GetServiceRequest",
    "ListEndpointsRequest",
    "ListEndpointsResponse",
    "ListNamespacesRequest",
    "ListNamespacesResponse",
    "ListServicesRequest",
    "ListServicesResponse",
    "UpdateEndpointRequest",
    "UpdateNamespaceRequest",
    "UpdateServiceRequest",
    "Service",
)
