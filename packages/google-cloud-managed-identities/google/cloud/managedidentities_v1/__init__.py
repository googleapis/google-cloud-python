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
from google.cloud.managedidentities_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.managed_identities_service import (
    ManagedIdentitiesServiceAsyncClient,
    ManagedIdentitiesServiceClient,
)
from .types.managed_identities_service import (
    AttachTrustRequest,
    CreateMicrosoftAdDomainRequest,
    DeleteDomainRequest,
    DetachTrustRequest,
    GetDomainRequest,
    ListDomainsRequest,
    ListDomainsResponse,
    OpMetadata,
    ReconfigureTrustRequest,
    ResetAdminPasswordRequest,
    ResetAdminPasswordResponse,
    UpdateDomainRequest,
    ValidateTrustRequest,
)
from .types.resource import Domain, Trust

__all__ = (
    "ManagedIdentitiesServiceAsyncClient",
    "AttachTrustRequest",
    "CreateMicrosoftAdDomainRequest",
    "DeleteDomainRequest",
    "DetachTrustRequest",
    "Domain",
    "GetDomainRequest",
    "ListDomainsRequest",
    "ListDomainsResponse",
    "ManagedIdentitiesServiceClient",
    "OpMetadata",
    "ReconfigureTrustRequest",
    "ResetAdminPasswordRequest",
    "ResetAdminPasswordResponse",
    "Trust",
    "UpdateDomainRequest",
    "ValidateTrustRequest",
)
