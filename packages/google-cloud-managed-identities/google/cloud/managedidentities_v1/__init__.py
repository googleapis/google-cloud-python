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

from .services.managed_identities_service import ManagedIdentitiesServiceClient
from .services.managed_identities_service import ManagedIdentitiesServiceAsyncClient

from .types.managed_identities_service import AttachTrustRequest
from .types.managed_identities_service import CreateMicrosoftAdDomainRequest
from .types.managed_identities_service import DeleteDomainRequest
from .types.managed_identities_service import DetachTrustRequest
from .types.managed_identities_service import GetDomainRequest
from .types.managed_identities_service import ListDomainsRequest
from .types.managed_identities_service import ListDomainsResponse
from .types.managed_identities_service import OpMetadata
from .types.managed_identities_service import ReconfigureTrustRequest
from .types.managed_identities_service import ResetAdminPasswordRequest
from .types.managed_identities_service import ResetAdminPasswordResponse
from .types.managed_identities_service import UpdateDomainRequest
from .types.managed_identities_service import ValidateTrustRequest
from .types.resource import Domain
from .types.resource import Trust

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
